from datetime import datetime
from sqlalchemy.orm import Session
from app.models.job import Job

def get_active_job(
    job_type: str,
    document_id: str,
    db: Session,
):
    return (
        db.query(Job)
        .filter(Job.type == job_type)
        .filter(Job.document_id == document_id)
        .filter(Job.status.in_(["pending", "running"]))
        .order_by(Job.created_at.desc())
        .first()
    )

def create_job(
    job_type: str,
    document_id: str,
    db: Session,
):
    existing_job = get_active_job(
        job_type=job_type,
        document_id=document_id,
        db=db,
    )

    if existing_job:
        return existing_job

    job = Job(
        type=job_type,
        status="pending",
        document_id=document_id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job

def mark_job_running(
    job: Job,
    db: Session,
):
    job.status = "running"
    job.started_at = datetime.utcnow()

    db.commit()
    db.refresh(job)

    return job


def mark_job_completed(
    job: Job,
    db: Session,
):
    job.status = "completed"
    job.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(job)

    return job

def mark_job_failed(
    job: Job,
    error: str,
    db: Session,
):
    job.status = "failed"
    job.error = error
    job.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(job)

    return job