from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.ollama_embedding_service import create_embedding


def retrieve_relevant_chunks(
    document_id: str,
    query: str,
    db: Session,
    limit: int = 5,
):
    query_embedding = create_embedding(query)

    sql = text("""
        SELECT
            content,
            page_number,
            embedding <-> CAST(:embedding AS vector) AS distance
        FROM document_chunks
        WHERE document_id = :document_id
        ORDER BY embedding <-> CAST(:embedding AS vector)
        LIMIT :limit
    """)

    result = db.execute(
        sql,
        {
            "embedding": str(query_embedding),
            "document_id": document_id,
            "limit": limit,
        },
    )

    rows = result.fetchall()

    return rows