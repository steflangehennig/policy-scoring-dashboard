from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from unstructured.partition.auto import partition
from transformers import pipeline
from typing import Dict
import time
import uvicorn
import os
from io import BytesIO

app = FastAPI()

# allow all origins for dev (revisit in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load model pipeline (more to come)
scorer = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1")

# rate limit tracker (max request per IP/ 30min in seconds)
RATE_LIMIT = 5 
TIME_WINDOW = 30 * 60  
ip_log: Dict[str, list] = {}

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    ip = request.client.host
    now = time.time()
    ip_log.setdefault(ip, [])
    # Drop expired entries
    ip_log[ip] = [t for t in ip_log[ip] if now - t < TIME_WINDOW]
    if len(ip_log[ip]) >= RATE_LIMIT:
        return JSONResponse(
            content={"detail": "Rate limit exceeded. Please wait before uploading again."},
            status_code=HTTP_429_TOO_MANY_REQUESTS
        )
    ip_log[ip].append(now)
    response = await call_next(request)
    return response

@app.post("/score")
async def score_document(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        raw = await file.read()
        elements = partition(file=BytesIO(raw), filename=file.filename)
        full_text = "\n".join([el.text for el in elements if el.text.strip()])

        prompt = f"""
You are an expert in evidence-based policymaking. Score the following policy document using a rubric with five dimensions:
1. Use of Empirical Research
2. Formal Evidence-Gathering Process
3. Transparency and Accessibility
4. Expert and Stakeholder Input
5. Evaluation and Iteration

Respond in JSON format like:
{{
  "Use of Empirical Research": 3,
  "Formal Evidence-Gathering Process": 4,
  "Transparency and Accessibility": 2,
  "Expert and Stakeholder Input": 3,
  "Evaluation and Iteration": 1
}}

Document:
"""
        input_text = prompt + full_text[:12000]  # prevent overly long prompts

        output = scorer(input_text, max_new_tokens=300, do_sample=True)[0]["generated_text"]

        # extract json part (fallback parsing)
        json_start = output.find("{")
        json_end = output.find("}", json_start)
        json_text = output[json_start:json_end+1]
        scores = eval(json_text) if json_start != -1 and json_end != -1 else {}

        return {"filename": file.filename, "scores": scores}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring document: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
