from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.job import Job

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


@router.get("/{job_id}")
async def get_job(
    job_id: str,
    db: Session = Depends(get_db),
):
    try:
        job_uuid = UUID(job_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid job_id. Expected UUID format.",
        )

    job = (
        db.query(Job)
        .filter(Job.id == job_uuid)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "id": str(job.id),
        "type": job.type,
        "status": job.status,
        "document_id": job.document_id,
        "error": job.error,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
    }