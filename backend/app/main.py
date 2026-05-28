from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine
from app.services.openrouter_service import create_chat_response
from app.services.ollama_embedding_service import create_embedding

from app.db.base import Base
from app.models.document import Document, DocumentPage
from app.api.documents import router as documents_router

app = FastAPI()

app.include_router(documents_router)

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