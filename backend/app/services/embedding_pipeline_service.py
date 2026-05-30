from sqlalchemy.orm import Session

from app.models.chunk import DocumentChunk
from app.models.document import DocumentPage
from app.services.chunking_service import chunk_text
from app.services.embedding_service import create_embeddings


BATCH_SIZE = 10


def process_document_embeddings(
    document_id: str,
    db: Session,
):
    db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id
    ).delete()

    pages = (
        db.query(DocumentPage)
        .filter(DocumentPage.document_id == document_id)
        .order_by(DocumentPage.page_number)
        .all()
    )

    chunk_counter = 0

    for page in pages:
        chunks = chunk_text(page.content)

        if not chunks:
            print(
                f"Skipping empty page {page.page_number}"
            )
            continue

        print(
            f"Embedding page {page.page_number} "
            f"({len(chunks)} chunks)"
        )

        for start in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[start:start + BATCH_SIZE]

            if not batch:
                continue

            print(
                f"Embedding page {page.page_number}, "
                f"batch {start // BATCH_SIZE + 1}, "
                f"{len(batch)} chunks"
            )

            embeddings = create_embeddings(batch)

            for chunk, embedding in zip(batch, embeddings):
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

    print(
        f"Finished embedding "
        f"{chunk_counter} chunks"
    )

    return {
        "chunks_created": chunk_counter,
    }