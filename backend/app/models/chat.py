from pydantic import BaseModel

class ChatRequest(BaseModel):
    document_id: str
    message: str
    conversation_id: str | None = None