from app.services.openrouter_service import create_chat_response
from app.services.prompt_service import build_rag_prompt
from app.services.retrieval_service import (
    retrieve_relevant_chunks,
)


def ask_document_question(
    document_id: str,
    question: str,
    db,
):
    chunks = retrieve_relevant_chunks(
        document_id=document_id,
        query=question,
        db=db,
    )

    prompt = build_rag_prompt(
        question=question,
        chunks=chunks,
    )

    answer = create_chat_response(prompt)

    sources = []

    seen_pages = set()

    for chunk in chunks:
      if chunk.page_number not in seen_pages:
        sources.append(
            {
                "page_number": chunk.page_number
            }
        )

        seen_pages.add(chunk.page_number)

    return {
        "answer": answer,
        "sources": sources,
    }