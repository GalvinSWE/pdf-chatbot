from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.db.session import engine
from app.db.base import Base

from app.services.openrouter_service import create_chat_response
from app.services.ollama_embedding_service import create_embedding

from app.api.documents import router as documents_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router
from app.api.evaluation import router as evaluation_router
from app.api.jobs import router as jobs_router

from app.models.conversation import Conversation, ChatMessage
from app.models.chunk import DocumentChunk
from app.models.document import Document, DocumentPage
from app.models.evaluation import EvaluationResult
from app.models.job import Job

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(chat_router)
app.include_router(conversations_router)
app.include_router(evaluation_router)
app.include_router(jobs_router)

@app.get("/")
async def root():
    return {"message": "PDF Chatbot API"}

@app.get("/health/db")
async def health_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {"status": "ok"}

@app.get("/health/chat")
async def health_chat():
    answer = create_chat_response("Say hello in one short sentence.")

    return {
        "status": "ok",
        "provider": "openrouter",
        "answer": answer,
    }

@app.get("/health/embedding")
async def health_embedding():
    embedding = create_embedding("Hello PDF chatbot")

    return {
        "status": "ok",
        "provider": "ollama",
        "model": "nomic-embed-text",
        "dimension": len(embedding),
        "preview": embedding[:5],
    }

@app.get("/health/pgvector")
async def health_pgvector():
    with engine.connect() as conn:
        result = conn.execute(
            text("CREATE EXTENSION IF NOT EXISTS vector")
        )

    return {"status": "ok"}

@app.post("/dev/create-tables")
async def create_tables():
    Base.metadata.create_all(bind=engine)
    return {"status": "tables created"}