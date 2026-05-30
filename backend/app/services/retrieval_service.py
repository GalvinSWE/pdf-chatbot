from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.embedding_service import create_embedding
from app.services.question_classifier_service import is_overview_question

def retrieve_semantic_chunks(
    document_id: str,
    query: str,
    db: Session,
    limit: int = 5,
):
    query_embedding = create_embedding(query)

    sql = text("""
        SELECT
            id,
            content,
            page_number,
            chunk_index,
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

    return [
        {
            "chunk_id": str(row.id),
            "content": row.content,
            "page_number": row.page_number,
            "chunk_index": row.chunk_index,
            "distance": float(row.distance),
            "strategy": "semantic",
        }
        for row in result.fetchall()
    ]

def retrieve_first_chunks(
    document_id: str,
    db: Session,
    limit: int = 5,
):
    sql = text("""
        SELECT
            id,
            content,
            page_number,
            chunk_index,
            0.0 AS distance
        FROM document_chunks
        WHERE document_id = :document_id
        ORDER BY chunk_index ASC
        LIMIT :limit
    """)

    result = db.execute(
        sql,
        {
            "document_id": document_id,
            "limit": limit,
        },
    )

    return [
        {
            "chunk_id": str(row.id),
            "content": row.content,
            "page_number": row.page_number,
            "chunk_index": row.chunk_index,
            "distance": float(row.distance),
            "strategy": "first_chunks",
        }
        for row in result.fetchall()
    ]

def deduplicate_chunks(chunks: list[dict]) -> list[dict]:
    seen = set()
    deduped = []

    for chunk in chunks:
        if chunk["chunk_id"] in seen:
            continue

        seen.add(chunk["chunk_id"])
        deduped.append(chunk)

    return deduped

def retrieve_relevant_chunks(
    document_id: str,
    query: str,
    db: Session,
    limit: int = 5,
):
    semantic_chunks = retrieve_semantic_chunks(
        document_id=document_id,
        query=query,
        db=db,
        limit=limit,
    )

    if is_overview_question(query):
        first_chunks = retrieve_first_chunks(
            document_id=document_id,
            db=db,
            limit=5,
        )

        return deduplicate_chunks(first_chunks + semantic_chunks)

    return semantic_chunks