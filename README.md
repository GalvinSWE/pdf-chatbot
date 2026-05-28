# PDF Chatbot

AI-powered PDF chatbot built with:

- FastAPI
- PostgreSQL + pgvector
- OpenRouter
- Ollama embeddings

## Features
## Features

### Phase 0
- FastAPI backend
- PostgreSQL setup
- pgvector support
- OpenRouter chat integration
- Ollama local embeddings
- Dockerized infrastructure

### PHASE 1 — PDF Ingestion Pipeline

Mục tiêu:
User upload PDF
↓
Backend nhận file
↓
Extract text theo từng page
↓
Lưu document metadata
↓
Lưu page content vào DB

Sau Phase 1, ta chưa làm embedding.
Ta chỉ biến PDF thành text có cấu trúc.

## Project Structure

```txt
backend/
  app/
    api/
    core/
    db/
    models/
    services/
```

## Setup

Install dependencies
pip install -r requirements.txt

Run PostgreSQL
docker compose up

Run backend
uvicorn app.main:app --reload

Health Endpoints
/health/db
/health/chat
/health/embedding
/health/pgvector