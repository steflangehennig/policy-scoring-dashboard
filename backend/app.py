from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
import os
import requests
import json
import re
import time
import tempfile
from typing import Dict
import spacy
import pdfplumber
import docx

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

app = FastAPI()

# Allow all origins for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face Inference API setup
model_id = "mistralai/Mistral-7B-Instruct-v0.3"
HF_API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
hf_token = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {hf_token}"}
print("✅ HF_TOKEN Present:", hf_token is not None)

# Rate limiting
RATE_LIMIT = 5  # max requests
TIME_WINDOW = 30 * 60  # 30 minutes
ip_log: Dict[str, list] = {}

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    ip = request.client.host
    now = time.time()
    ip_log.setdefault(ip, [])
    ip_log[ip] = [t for t in ip_log[ip] if now - t < TIME_WINDOW]
    if len(ip_log[ip]) >= RATE_LIMIT:
        return JSONResponse(
            content={"detail": "Rate limit exceeded. Please wait before uploading again."},
            status_code=HTTP_429_TOO_MANY_REQUESTS
        )
    ip_log[ip].append(now)
    response = await call_next(request)
    return response

rubric_prompt = """
Use the rubric below to score the policy document on five dimensions of evidence-based policymaking,
even if the document lacks relevant content (assign 'NA' in that case).
Each dimension should receive a score from 0 to 3, where:
0 = No evidence of the dimension
1 = Minimal or implicit evidence
2 = Moderate or partial evidence
3 = Clear, strong, and explicit evidence
### Dimensions:
1. Use of Empirical Research
- 0: No references to empirical evidence or data
- 1: Vague or anecdotal references (e.g., “studies show”)
- 2: Clear empirical support, but limited sourcing
- 3: Multiple, clearly cited, high-quality sources (e.g., peer-reviewed, systematic reviews)
2. Formal Evidence-Gathering Process
- 0: No structured data gathering
- 1: Informal or anecdotal input
- 2: Basic assessments (e.g., internal reports, cost estimates)
- 3: Formal tools (e.g., RCTs, modeling, pilot programs)
3. Transparency and Accessibility
- 0: No documentation or rationale
- 1: Minimal or internal-only documentation
- 2: Public access with basic explanation
- 3: Fully open access, replicable, with detailed methods
4. Expert and Stakeholder Input
- 0: No input from external parties
- 1: Informal or minimal consultation
- 2: Some formal consultation or review by stakeholders
- 3: Broad engagement with named experts or stakeholders
5. Evaluation and Iteration
- 0: No plan or evidence of evaluation
- 1: A vague or one-time evaluation mention
- 2: Evaluation included with some details
- 3: Robust plan or evidence of ongoing evaluation and iteration
### Note:
You will be asked to return a JSON object based on a policy document. Each dimension must include:
- A `score` (0–3)
- A `justification` with a full sentence explaining the score
Do not reuse this rubric text or copy examples into your answer.
"""

def extract_text(tmp_path: str, suffix: str) -> str:
    if suffix.lower().endswith(".pdf"):
        with pdfplumber.open(tmp_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif suffix.lower().endswith(".docx"):
        doc = docx.Document(tmp_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    elif suffix.lower().endswith(".txt"):
        with open(tmp_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type")

def extract_first_json(text):
    matches = re.findall(r"\{(?:[^{}]|(?:\{.*?\}))*\}", text, re.DOTALL)
    for match in matches:
        try:
            result = json.loads(match)
            required_keys = [
                "Use of Empirical Research",
                "Formal Evidence-Gathering Process",
                "Transparency and Accessibility",
                "Expert and Stakeholder Input",
                "Evaluation and Iteration"
            ]
            if all(key in result for key in required_keys):
                return result
        except json.JSONDecodeError:
            continue
    return None

@app.post("/score")
async def score_document(file: UploadFile = File(...)):
    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    ]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        raw = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            tmp.write(raw)
            tmp_path = tmp.name

        full_text = extract_text(tmp_path, tmp_path)

        # Use spaCy to split into sentences and truncate
        doc = nlp(full_text)
        truncated_text = " ".join([sent.text for sent in doc.sents][:30])

        full_prompt = (
            "You are a policy analyst evaluating how evidence-based a policy document is.\n"
            "Below is a policy document. Read it carefully and then apply the rubric that follows.\n\n"
            + truncated_text + "\n\n"
            + "Now use this rubric to evaluate:\n"
            + rubric_prompt + "\n\n"
            + "Return only a JSON object. Each key should be a rubric dimension. Each value should be an object "
              "with a 'score' (0–3) and a 'justification' — a sentence explaining why that score was given based on the text of the document.\n"
            + "Do not reuse examples or include placeholder text like '...'. Be specific, original, and concise in your justifications."
        )

        payload = {"inputs": full_prompt}
        res = requests.post(HF_API_URL, headers=headers, json=payload)
        if res.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Model error: {res.text}")

        response_text = res.json()[0]["generated_text"]
        parsed = extract_first_json(response_text)

        if not parsed:
            raise HTTPException(status_code=500, detail="Model response did not include valid JSON.")

        return {"filename": file.filename, "scores": parsed}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring document: {str(e)}")