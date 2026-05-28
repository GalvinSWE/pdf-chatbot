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