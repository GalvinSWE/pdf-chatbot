Đây là phiên bản README mà mình sẽ dùng nếu là recruiter nhìn vào GitHub của một Junior AI Engineer.

PDF Chatbot RAG

An end-to-end Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and chat with them using AI.

The system extracts text from PDFs, generates embeddings locally with Ollama, stores vectors in PostgreSQL + pgvector, retrieves relevant context through semantic search, and generates grounded answers using an LLM via OpenRouter.

⸻

Demo

Features

* PDF Upload
* PDF Text Extraction
* Semantic Search
* RAG Pipeline
* Streaming Responses
* Source Citations
* Conversation History
* Follow-up Questions
* Async Embedding Jobs
* Evaluation Dashboard
* Dockerized Deployment

⸻

Architecture

                    +------------------+
                    |     Frontend     |
                    |     Next.js      |
                    +--------+---------+
                             |
                             v
                    +--------+---------+
                    |      FastAPI     |
                    |      Backend     |
                    +--------+---------+
                             |
           +-----------------+------------------+
           |                                    |
           v                                    v
+----------+-----------+           +------------+-----------+
| PostgreSQL + pgvector|           |   OpenRouter LLM      |
+----------+-----------+           +------------+-----------+
           |
           v
+----------+-----------+
|      Ollama          |
| nomic-embed-text     |
+----------------------+

⸻

RAG Flow

PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embedding Generation
 ↓
pgvector Storage
 ↓
Semantic Retrieval
 ↓
Prompt Construction
 ↓
LLM Generation
 ↓
Grounded Answer

⸻

Tech Stack

Backend

* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* pgvector

AI

* Ollama
* nomic-embed-text
* OpenRouter
* DeepSeek / Qwen / Llama

Frontend

* Next.js
* React
* TailwindCSS

Infrastructure

* Docker
* Docker Compose

⸻

Project Structure

backend/
├── alembic/
├── app/
│   ├── api/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── worker.py
│
└── requirements.txt
frontend/
├── src/
└── package.json
docker-compose.yml
README.md

⸻

Quick Start

Clone Repository

git clone https://github.com/YOUR_USERNAME/pdf-chatbot.git
cd pdf-chatbot

Configure Environment

Create .env

DATABASE_URL=postgresql://postgres:postgres@db:5432/pdfchatbot
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

Start Services

docker compose up --build

Run Database Migration

docker compose exec backend python -m alembic upgrade head

Pull Embedding Model

docker exec -it pdf-chatbot-ollama \
ollama pull nomic-embed-text

⸻

API Overview

Documents

POST /documents/upload
GET  /documents
GET  /documents/{id}

Embedding Jobs

POST /documents/{id}/embed-jobs
GET  /jobs/{id}

Chat

POST /chat
POST /chat/stream

Conversations

GET /conversations
GET /conversations/{id}/messages

Evaluation

POST /evaluation/run
GET  /evaluation/results

⸻

Example Workflow

1. Upload PDF

User uploads:

The Design of Everyday Things.pdf

2. Generate Embeddings

pending
 ↓
running
 ↓
completed

3. Ask Questions

What is this book about?
Explain affordances.
What are signifiers?

4. Receive Grounded Answers

Answer generated from retrieved document chunks
with page citations.

⸻

What I Learned

This project was built as a hands-on journey to transition from Web Development to AI Engineering.

Key concepts learned:

* Retrieval-Augmented Generation (RAG)
* Embeddings and Vector Search
* pgvector and Semantic Retrieval
* Prompt Engineering
* Hallucination Reduction
* Context Grounding
* Streaming LLM Responses
* Async Job Processing
* AI Evaluation
* Dockerized AI Applications

⸻

Future Improvements

* Hybrid Search (Keyword + Vector)
* Reranking Models
* OCR Support
* Multi-document Chat
* Agentic RAG
* LangGraph Workflows
* Authentication & User Accounts

⸻

Screenshots

Add screenshots here:

docs/images/upload.png
docs/images/chat.png
docs/images/sources.png

⸻

Author

Galvin Nguyen

Web Developer → AI Engineer

Building AI applications to learn production-grade RAG systems.

Một điểm quan trọng: khi project hoàn thành, hãy thay dòng:

Web Developer → AI Engineer

bằng:

AI Engineer | FastAPI | RAG | LLM Applications