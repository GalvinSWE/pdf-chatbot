Dưới đây là README mà mình nghĩ đủ mạnh để đưa vào CV/GitHub khi apply AI Engineer Junior.

PDF Chatbot RAG

An end-to-end AI-powered PDF Chatbot built with Retrieval-Augmented Generation (RAG).

Users can upload PDF documents, automatically generate embeddings, store vectors in PostgreSQL + pgvector, and ask questions about the document with source citations and streaming responses.

⸻

Features

Document Processing

* Upload PDF files
* Extract text from PDFs
* Page-level storage
* Chunking pipeline
* Embedding generation using Ollama

Retrieval-Augmented Generation (RAG)

* Semantic search
* Vector similarity retrieval
* Context injection
* Source citations
* Hallucination reduction

Chat Experience

* Streaming responses
* Conversation history
* Follow-up questions
* Question rewriting
* Multi-turn conversations

Evaluation

* Groundedness evaluation
* Retrieval quality evaluation
* LLM answer evaluation

Infrastructure

* PostgreSQL
* pgvector
* Dockerized deployment
* Background workers
* Async job processing

⸻

Architecture

                     +----------------+
                     |    Frontend    |
                     |    Next.js     |
                     +-------+--------+
                             |
                             v
                     +-------+--------+
                     |    FastAPI     |
                     |    Backend     |
                     +-------+--------+
                             |
          +------------------+------------------+
          |                                     |
          v                                     v
+---------+----------+              +-----------+----------+
| PostgreSQL         |              | OpenRouter           |
| pgvector           |              | LLM Provider         |
+---------+----------+              +-----------+----------+
          |
          v
+---------+----------+
| Ollama             |
| Embedding Model    |
+--------------------+

⸻

RAG Pipeline

PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
pgvector
 ↓
Semantic Retrieval
 ↓
Prompt Construction
 ↓
OpenRouter LLM
 ↓
Streaming Answer

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
* Llama / Qwen / DeepSeek

Frontend

* Next.js
* React
* TailwindCSS

DevOps

* Docker
* Docker Compose

⸻

Project Structure

backend/
│
├── alembic/
├── app/
│   ├── api/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── worker.py
│
├── requirements.txt
└── Dockerfile
frontend/
│
├── src/
├── public/
├── package.json
└── Dockerfile
docker-compose.yml
README.md

⸻

Database Schema

documents

Stores uploaded PDFs.

id
filename
status
total_pages
created_at

document_pages

Stores extracted page content.

id
document_id
page_number
content

document_chunks

Stores chunks and embeddings.

id
document_id
page_number
chunk_index
content
embedding

conversations

Stores chat sessions.

id
document_id
title
created_at

chat_messages

Stores conversation history.

id
conversation_id
role
content
created_at

jobs

Stores background embedding jobs.

id
type
status
document_id
error
created_at
started_at
completed_at

⸻

Setup

Clone

git clone https://github.com/YOUR_USERNAME/pdf-chatbot.git
cd pdf-chatbot

⸻

Environment Variables

Create:

cp .env.example .env

Example:

DATABASE_URL=postgresql://postgres:postgres@db:5432/pdfchatbot
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

⸻

Start Application

docker compose up --build

⸻

Run Database Migration

docker compose exec backend python -m alembic upgrade head

⸻

Pull Embedding Model

docker exec -it pdf-chatbot-ollama \
ollama pull nomic-embed-text

⸻

Verify Ollama

curl http://localhost:11434/api/tags

⸻

API Endpoints

Health

GET /health

⸻

Documents

Upload PDF

POST /documents/upload

List documents

GET /documents

Get document

GET /documents/{document_id}

⸻

Jobs

Create embedding job

POST /documents/{document_id}/embed-jobs

Get job status

GET /jobs/{job_id}

⸻

Chat

Chat

POST /chat

Streaming chat

POST /chat/stream

⸻

Conversations

List conversations

GET /conversations

Messages

GET /conversations/{conversation_id}/messages

⸻

Evaluation

Run evaluation

POST /evaluation/run

List results

GET /evaluation/results

⸻

Example Workflow

1 Upload PDF

The Design of Everyday Things.pdf

↓

2 Create Embedding Job

pending

↓

running

↓

completed

↓

3 Ask Questions

What is this book about?
Explain affordances.
What does Don Norman mean by signifiers?

⸻

Example RAG Flow

User Question

What is affordance?

↓

Embedding Query

↓

Vector Search

↓

Top 5 Relevant Chunks

↓

Prompt Construction

↓

LLM Answer

↓

Source Citations

⸻

What I Learned

AI Engineering

* Retrieval-Augmented Generation (RAG)
* Embeddings
* Vector Databases
* Semantic Search
* Prompt Engineering
* Hallucination Reduction
* Evaluation Techniques

Backend Engineering

* FastAPI
* SQLAlchemy
* Alembic
* Background Workers
* Streaming APIs

Data Engineering

* PDF Parsing
* Chunking Strategies
* Embedding Pipelines

Infrastructure

* Docker
* PostgreSQL
* pgvector
* Local AI Models with Ollama

⸻

Future Improvements

* Hybrid Search (Keyword + Vector)
* Reranking Models
* Multi-document Chat
* OCR Support
* Image Understanding
* Agentic RAG
* LangGraph Workflow
* Authentication
* Team Workspaces

⸻

Screenshots

Add screenshots here:

docs/images/upload.png
docs/images/chat.png
docs/images/sources.png

⸻

License

MIT License

⸻

Author

Galvin Nguyen

Aspiring AI Engineer

Built as a personal project to learn production-grade RAG systems.

Sau README này, project của bạn đã ở mức khá ổn cho portfolio. Bước tiếp theo hợp lý nhất không phải thêm tính năng nữa mà là làm Phase 15 — Hybrid Search + Reranking, vì đó là thứ thường được hỏi trong phỏng vấn AI Engineer khi bạn đã có một RAG chatbot hoàn chỉnh.