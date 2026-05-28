from sqlalchemy.orm import Session

from app.models.chunk import DocumentChunk
from app.models.document import DocumentPage
from app.services.chunking_service import chunk_text
from app.services.ollama_embedding_service import create_embedding


def process_document_embeddings(
    document_id: str,
    db: Session,
):
    pages = (
        db.query(DocumentPage)
        .filter(DocumentPage.document_id == document_id)
        .all()
    )

    chunk_counter = 0

    for page in pages:
        chunks = chunk_text(page.content)

        for chunk in chunks:
            embedding = create_embedding(chunk)

            document_chunk = DocumentChunk(
                document_id=document_id,
                page_number=page.page_number,
                chunk_index=chunk_counter,
                content=chunk,
                embedding=embedding,
            )

            db.add(document_chunk)

            chunk_counter += 1

    db.commit()