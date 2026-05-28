from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.document import Document, DocumentPage
from app.services.pdf_service import extract_pdf_pages

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