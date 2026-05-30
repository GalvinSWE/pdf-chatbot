from sqlalchemy.orm import Session

from app.models.conversation import Conversation, ChatMessage

def create_conversation(
    document_id: str,
    title: str | None,
    db: Session,
):
    conversation = Conversation(
        document_id=document_id,
        title=title,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

def add_message(
    conversation_id: str,
    role: str,
    content: str,
    db: Session,
):
    message = ChatMessage(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message

def list_conversations(db: Session):
    return (
        db.query(Conversation)
        .order_by(Conversation.created_at.desc())
        .all()
    )

def list_messages(
    conversation_id: str,
    db: Session,
):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )