import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=False)
    generated_answer = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)