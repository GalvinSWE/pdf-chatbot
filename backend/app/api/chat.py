from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.chat import ChatRequest
from app.services.rag_chat_service import (
    ask_document_question,
)

from fastapi.responses import StreamingResponse
from app.services.rag_stream_service import stream_document_answer

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

@router.post("/")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    result = ask_document_question(
        document_id=request.document_id,
        question=request.message,
        conversation_id=request.conversation_id,
        db=db,
    )

    return result

@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    return StreamingResponse(
        stream_document_answer(
            document_id=request.document_id,
            question=request.message,
            conversation_id=request.conversation_id,
            db=db,
        ),
        media_type="application/x-ndjson",
    )