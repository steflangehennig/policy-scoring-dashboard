# slim Python base
FROM python:3.10-slim

# working directory to app
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# download spacy model
RUN python -m spacy download en_core_web_sm

# copy app code
COPY . .

# expose port
EXPOSE 7860

# start fastapi with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
