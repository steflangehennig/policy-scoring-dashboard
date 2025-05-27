from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from unstructured.partition.auto import partition
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import json
import re
import time
from io import BytesIO
from typing import Dict
import os

app = FastAPI()

# Allow all origins for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model with Hugging Face token from environment
model_id = "mistralai/Mistral-7B-Instruct-v0.2"
hf_token = os.getenv("HF_TOKEN")

tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    token=hf_token  # no device_map, no dtype
)
llm = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=2048)

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
2. Formal Evidence-Gathering Process
3. Transparency and Accessibility
4. Expert and Stakeholder Input
5. Evaluation and Iteration

Each dimension must include:
- A `score` (0–3)
- A `justification` explaining the score based on the document
"""

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
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        raw = await file.read()
        elements = partition(file=BytesIO(raw), filename=file.filename)
        full_text = "\n".join([el.text for el in elements if el.text.strip()])

        full_prompt = (
            "You are a policy analyst evaluating how evidence-based a policy document is.\n"
            "Below is a policy document. Read it carefully and then apply the rubric that follows.\n\n"
            + full_text[:10000] + "\n\n"
            + "Now use this rubric to evaluate:\n"
            + rubric_prompt + "\n\n"
            + "Return only a JSON object. Each key should be a rubric dimension. Each value should be an object "
              "with a 'score' (0–3) and a 'justification' — a sentence explaining why that score was given based on the text of the document.\n"
            + "Do not reuse examples or include placeholder text like '...'. Be specific, original, and concise in your justifications."
        )

        response = llm(full_prompt)[0]["generated_text"]
        parsed = extract_first_json(response)

        if not parsed:
            raise HTTPException(status_code=500, detail="Model response did not include valid JSON.")

        return {"filename": file.filename, "scores": parsed}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring document: {str(e)}")
