from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.conversation_service import (
    list_conversations,
    list_messages,
)

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)

@router.get("")
async def get_conversations(
    db: Session = Depends(get_db),
):
    conversations = list_conversations(db)

    return [
        {
            "id": str(conversation.id),
            "document_id": str(conversation.document_id),
            "title": conversation.title,
            "created_at": conversation.created_at,
        }
        for conversation in conversations
    ]

@router.get("/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    messages = list_messages(
        conversation_id=conversation_id,
        db=db,
    )

    return [
        {
            "id": str(message.id),
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at,
        }
        for message in messages
    ]