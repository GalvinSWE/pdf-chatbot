from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.chat import ChatRequest
from app.services.rag_chat_service import (
    ask_document_question,
)

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
        db=db,
    )

    return result