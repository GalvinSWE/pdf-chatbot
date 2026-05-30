import uuid

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from pgvector.sqlalchemy import Vector

from app.db.base import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=False,
    )

    page_number = Column(Integer, nullable=False)

    chunk_index = Column(Integer, nullable=False)

    content = Column(Text, nullable=False)

    embedding = Column(Vector(1024), nullable=True)