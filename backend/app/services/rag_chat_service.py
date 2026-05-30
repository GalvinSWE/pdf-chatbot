from sqlalchemy.orm import Session
from app.models.document import Document

from app.services.openrouter_service import create_chat_response
from app.services.prompt_service import build_rag_prompt
from app.services.retrieval_service import retrieve_relevant_chunks

from app.services.conversation_service import (
    add_message,
    create_conversation,
    list_messages,
)

from app.services.question_rewrite_service import (
    get_last_assistant_message,
    rewrite_question_with_history,
)

FOLLOW_UP_EXPAND_PHRASES = [
    "giải thích kỹ hơn phần đó",
    "giải thích thêm",
    "nói rõ hơn",
    "explain more",
]

def is_expand_follow_up(question: str) -> bool:
    return question.lower().strip() in FOLLOW_UP_EXPAND_PHRASES

def ask_document_question(
    document_id: str,
    question: str,
    db: Session,
    conversation_id: str | None = None,
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
            "conversation_id": None,
            "debug": {
                "reason": "document_not_found",
            },
        }

    if conversation_id is None:
        conversation = create_conversation(
            document_id=document_id,
            title=question[:80],
            db=db,
        )
        conversation_id = str(conversation.id)

    recent_messages = list_messages(
        conversation_id=conversation_id,
        db=db,
    )

    last_answer = get_last_assistant_message(recent_messages)

    add_message(
        conversation_id=conversation_id,
        role="user",
        content=question,
        db=db,
    )

    if last_answer and is_expand_follow_up(question):
        prompt = f"""
            You are a PDF question-answering assistant.
            The user asks to explain the previous answer in more detail.

            Previous answer:
            {last_answer}

            User follow-up:
            {question}

            Explain more clearly in Vietnamese.
            Do not introduce unrelated topics.
        """

        answer = create_chat_response(prompt)

        add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
            db=db,
        )

        return {
            "answer": answer,
            "sources": [],
            "conversation_id": conversation_id,
            "debug": {
                "strategy": "last_assistant_message",
            },
        }

    retrieval_question = question

    if len(recent_messages) >= 2:
        retrieval_question = rewrite_question_with_history(
            question=question,
            recent_messages=recent_messages,
        )

    chunks = retrieve_relevant_chunks(
        document_id=document_id,
        query=retrieval_question,
        db=db,
        limit=5,
    )

    if not chunks:
        answer = "I could not find the answer in the document."

        add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
            db=db,
        )

        return {
            "answer": answer,
            "sources": [],
            "conversation_id": conversation_id,
            "debug": {
                "reason": "no_chunks_retrieved",
                "retrieval_question": retrieval_question,
            },
        }

    prompt = build_rag_prompt(
        question=retrieval_question,
        chunks=chunks,
    )

    answer = create_chat_response(prompt)

    add_message(
        conversation_id=conversation_id,
        role="assistant",
        content=answer,
        db=db,
    )

    sources = [
        {
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
            "distance": chunk["distance"],
            "strategy": chunk.get("strategy"),
            "content_preview": chunk["content"][:200],
        }
        for chunk in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
        "conversation_id": conversation_id,
        "debug": {
            "strategy": "rag_retrieval",
            "retrieval_question": retrieval_question,
            "retrieved_chunks": len(chunks),
            "best_distance": chunks[0]["distance"],
        },
    }