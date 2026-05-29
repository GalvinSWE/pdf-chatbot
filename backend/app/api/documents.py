from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.document import Document, DocumentPage
from app.services.pdf_service import extract_pdf_pages

from app.services.embedding_pipeline_service import (
    process_document_embeddings,
)

from sqlalchemy import text
from app.services.ollama_embedding_service import create_embedding
from app.services.retrieval_service import retrieve_relevant_chunks

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    file_bytes = await file.read()

    pages = extract_pdf_pages(file_bytes)

    document = Document(
        filename=file.filename,
        status="processed",
        total_pages=len(pages),
    )

    db.add(document)
    db.flush()

    for page in pages:
        if not page["content"]:
            continue

        document_page = DocumentPage(
            document_id=document.id,
            page_number=page["page_number"],
            content=page["content"],
        )

        db.add(document_page)

    db.commit()
    db.refresh(document)

    return {
        "document_id": str(document.id),
        "filename": document.filename,
        "total_pages": document.total_pages,
        "status": document.status,
    }

@router.get("/{document_id}/pages")
async def get_document_pages(
    document_id: str,
    db: Session = Depends(get_db),
):
    pages = (
        db.query(DocumentPage)
        .filter(DocumentPage.document_id == document_id)
        .order_by(DocumentPage.page_number)
        .all()
    )

    return [
        {
            "page_number": page.page_number,
            "content_preview": page.content[:500],
        }
        for page in pages
    ]

@router.post("/{document_id}/embed")
async def embed_document(
    document_id: str,
    db: Session = Depends(get_db),
):
    result = process_document_embeddings(
        document_id=document_id,
        db=db,
    )

    return {
        "status": "embedded",
        "document_id": document_id,
        "chunks_created": result["chunks_created"],
    }

@router.get("/{document_id}/search")
async def search_document(
    document_id: str,
    query: str,
    db: Session = Depends(get_db),
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
        LIMIT 5
    """)

    result = db.execute(
        sql,
        {
            "embedding": str(query_embedding),
            "document_id": document_id,
        },
    )

    rows = result.fetchall()

    return [
        {
            "page_number": row.page_number,
            "content_preview": row.content[:300],
            "distance": row.distance,
        }
        for row in rows
    ]

@router.get("/{document_id}/debug/retrieval")
async def debug_retrieval(
    document_id: str,
    query: str,
    db: Session = Depends(get_db),
):
    chunks = retrieve_relevant_chunks(
        document_id=document_id,
        query=query,
        db=db,
        limit=5,
    )

    return {
        "query": query,
        "results": [
            {
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
                "distance": chunk["distance"],
                "content_preview": chunk["content"][:500],
            }
            for chunk in chunks
        ],
    }