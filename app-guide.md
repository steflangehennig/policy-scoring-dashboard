
# Policy Scoring App: Full-Stack Documentation

This guidebook documents the complete architecture, setup, and deployment process for the Evidence-Based Policy Scoring App, from the FastAPI backend to the React frontend dashboard hosted on GitHub Pages and powered by Hugging Face Inference API (Mistral-7B-Instruct).

---

## Project Overview

- **Backend**: FastAPI app hosted on Hugging Face Spaces (via Docker)
- **Frontend**: React-based UI hosted on GitHub Pages
- **Model**: `mistralai/Mistral-7B-Instruct-v0.3` via Hugging Face Inference API
- **Function**: Accepts PDF/DOCX/TXT policy files, extracts text, sends to LLM for scoring against a 5-part rubric, and returns JSON-formatted evidence-based scores

---

## Core Rubric

Each document is scored on five dimensions (0-3 scale each):

1. Use of Empirical Research  
2. Formal Evidence-Gathering Process  
3. Transparency and Accessibility  
4. Expert and Stakeholder Input  
5. Evaluation and Iteration

---

## Backend Setup (FastAPI on Hugging Face Spaces)

### File Structure
```
app.py
Dockerfile
requirements.txt
```

### Requirements (requirements.txt)
```
fastapi
uvicorn
transformers
python-multipart
torch
accelerate
requests
pydantic
pdfplumber
python-docx
spacy
```

### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

### FastAPI app highlights (app.py)
- Accepts file uploads
- Uses `pdfplumber` and `python-docx` to extract text
- Uses spaCy (`en_core_web_sm`) for sentence splitting
- Sends prompt to Hugging Face model API
- Parses JSON result from response and returns it

---

## Hugging Face Model Integration

- Model used: [`mistralai/Mistral-7B-Instruct-v0.3`](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3)
- Requires manual approval for API access via HF web interface
- API call structure:
```python
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {hf_token}"}
response = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt})
```

---

## Frontend Setup (React on GitHub Pages)

### Tech Used:
- React
- Axios (for POST requests)
- Bootstrap (or optional styling frameworks)

### Key Components:
- `PolicyScoringDashboard.js`: 
  - File upload
  - Submits form to backend API
  - Renders response JSON in table form

### Example API call from React:
```js
const formData = new FormData();
formData.append("file", selectedFile);
axios.post("https://<your-hf-space>.hf.space/score", formData);
```

---

## Testing & Deployment

### Backend:
- Hugging Face Space: ensure `HF_TOKEN` secret is set
- Model must be accepted before first call
- Confirm `500` errors aren't model access-related

### Frontend:
- Deploy via `gh-pages` (optional GitHub Action)
- Works cross-browser
- React app accepts `.pdf`, `.docx`, `.txt`

---

## Troubleshooting

| Issue | Fix |
|------|-----|
| 500 error (NLTK) | Removed nltk and unstructured dependencies relying on it |
| 500 error (Model error) | Accept usage of gated Mistral model manually on HF |
| API Timeout | Ensure input length isn't too large; truncate text |
| Cross-Origin errors | CORSMiddleware enabled in backend |

---

## To Do / Future Enhancements

- Style cleanup and user-friendly error messages
- Highlight scores with color-coded heatmaps
- Add CSV export and comparison across documents
- GPU optimization for faster inference

---

## Attribution

Developed by Stefani Langehennig, Center for Analytics and Innovation with Data (CAID), University of Denver Daniels College of Business.

---
