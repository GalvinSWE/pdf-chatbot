import json

from sqlalchemy.orm import Session

from app.models.document import Document
from app.services.openrouter_service import stream_chat_response
from app.services.prompt_service import build_rag_prompt
from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.rag_chat_service import is_context_too_weak


def stream_document_answer(
    document_id: str,
    question: str,
    db: Session,
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        yield json.dumps({
            "type": "error",
            "message": "Document not found.",
        }) + "\n"
        return

    chunks = retrieve_relevant_chunks(
        document_id=document_id,
        query=question,
        db=db,
        limit=5,
    )

    if not chunks:
        yield json.dumps({
            "type": "error",
            "message": "I could not find the answer in the document.",
        }) + "\n"
        return
    
    if is_context_too_weak(chunks):
        return {
            "answer": "I could not find the answer in the document.",
            "sources": [],
            "debug": {
                "reason": "weak_context",
                "best_distance": min(
                    chunk["distance"]
                    for chunk in chunks
                    if chunk.get("strategy") == "semantic"
                ),
            }
        }

    sources = [
        {
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
            "distance": chunk["distance"],
            "content_preview": chunk["content"][:200],
        }
        for chunk in chunks
    ]

    yield json.dumps({
        "type": "sources",
        "sources": sources,
    }) + "\n"

    prompt = build_rag_prompt(
        question=question,
        chunks=chunks,
    )

    for token in stream_chat_response(prompt):
        yield json.dumps({
            "type": "token",
            "content": token,
        }) + "\n"

    yield json.dumps({
        "type": "done",
    }) + "\n"