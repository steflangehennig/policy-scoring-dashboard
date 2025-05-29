# Evidence-Based Policy Scoring App

This project is a full-stack web application for uploading and scoring policy documents against a five-dimension evidence-based policy rubric. It combines a React frontend with a FastAPI backend, powered by the open-source Mistral-7B-Instruct model via Hugging Face's Inference API.

## Features

- Upload `.txt`, `.pdf`, or `.docx` files
- Automatic document partitioning and text extraction
- LLM-based evaluation using the EBP rubric
- Justification text for each score
- Rate limiting to prevent overload
- CORS enabled for frontend-backend communication

## Frontend

- Built with React and Tailwind CSS
- Located in `src/components/PolicyScoringDashboard.js`
- Uploads files and displays scoring output

## Backend

- Built with FastAPI
- `app.py` handles uploads, scoring requests, and communication with the Hugging Face model
- Model used: `mistralai/Mistral-7B-Instruct-v0.3`

## Deployment

- Hosted on Hugging Face Spaces (backend) and GitHub Pages (frontend)
- Dockerized backend with lightweight Python 3.10 slim image
- CORS and API key handling integrated

## Scoring Rubric

Five dimensions scored from 0-3:
1. Use of Empirical Research
2. Formal Evidence-Gathering Process
3. Transparency and Accessibility
4. Expert and Stakeholder Input
5. Evaluation and Iteration

Each dimension includes:
- A numeric score
- A text justification

## To Reproduce

See the full guide [`policy_scoring_guide.md`](./policy_scoring_guide.md) for complete setup instructions including environment, API setup, Docker build, and integration.

## License

MIT License

---
Created by Stefani Langehennig, Center for Analytics and Innovation with Data (CAID), University of Denver Daniels College of Business. 2025.
