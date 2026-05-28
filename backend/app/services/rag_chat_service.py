from sqlalchemy.orm import Session

from app.models.document import Document
from app.services.openrouter_service import create_chat_response
from app.services.prompt_service import build_rag_prompt
from app.services.retrieval_service import retrieve_relevant_chunks


def ask_document_question(
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
        return {
            "answer": "Document not found.",
            "sources": [],
            "debug": {
                "reason": "document_not_found"
            }
        }

    chunks = retrieve_relevant_chunks(
        document_id=document_id,
        query=question,
        db=db,
        limit=5,
    )

    if not chunks:
        return {
            "answer": "I could not find the answer in the document.",
            "sources": [],
            "debug": {
                "reason": "no_chunks_retrieved"
            }
        }

    prompt = build_rag_prompt(
        question=question,
        chunks=chunks,
    )

    answer = create_chat_response(prompt)

    sources = []

    seen = set()

    for chunk in chunks:
        key = (chunk["page_number"], chunk["chunk_index"])

        if key not in seen:
            sources.append(
                {
                    "page_number": chunk["page_number"],
                    "chunk_index": chunk["chunk_index"],
                    "distance": chunk["distance"],
                    "content_preview": chunk["content"][:200],
                }
            )

            seen.add(key)

    return {
        "answer": answer,
        "sources": sources,
        "debug": {
            "retrieved_chunks": len(chunks),
            "best_distance": chunks[0]["distance"],
        }
    }