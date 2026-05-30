import json

from sqlalchemy.orm import Session

from app.models.document import Document

from app.services.openrouter_service import stream_chat_response
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

def stream_document_answer(
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
        yield json.dumps({
            "type": "error",
            "message": "Document not found.",
        }) + "\n"
        return

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

    yield json.dumps({
        "type": "conversation",
        "conversation_id": conversation_id,
    }) + "\n"

    if last_answer and is_expand_follow_up(question):
        yield json.dumps({
            "type": "follow_up_context",
            "source": "last_assistant_message",
        }) + "\n"

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

        answer_parts = []

        for token in stream_chat_response(prompt):
            answer_parts.append(token)

            yield json.dumps({
                "type": "token",
                "content": token,
            }) + "\n"

        full_answer = "".join(answer_parts)

        add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=full_answer,
            db=db,
        )

        yield json.dumps({
            "type": "done",
        }) + "\n"

        return

    retrieval_question = question

    if len(recent_messages) >= 2:
        retrieval_question = rewrite_question_with_history(
            question=question,
            recent_messages=recent_messages,
        )

    yield json.dumps({
        "type": "rewritten_question",
        "question": retrieval_question,
    }) + "\n"

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

        yield json.dumps({
            "type": "error",
            "message": answer,
        }) + "\n"
        return

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

    yield json.dumps({
        "type": "sources",
        "sources": sources,
    }) + "\n"

    prompt = build_rag_prompt(
        question=retrieval_question,
        chunks=chunks,
    )

    answer_parts = []

    for token in stream_chat_response(prompt):
        answer_parts.append(token)

        yield json.dumps({
            "type": "token",
            "content": token,
        }) + "\n"

    full_answer = "".join(answer_parts)

    add_message(
        conversation_id=conversation_id,
        role="assistant",
        content=full_answer,
        db=db,
    )

    yield json.dumps({
        "type": "done",
    }) + "\n"