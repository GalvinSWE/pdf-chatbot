from app.db.session import SessionLocal
from app.models.document import Document
from app.models.job import Job
from app.services.embedding_pipeline_service import process_document_embeddings
from app.services.job_service import (
    mark_job_completed,
    mark_job_failed,
    mark_job_running,
)

def run_embedding_job(job_id: str):
    db = SessionLocal()

    try:
        job = (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

        if not job:
            return

        mark_job_running(job, db)

        document = (
            db.query(Document)
            .filter(Document.id == job.document_id)
            .first()
        )

        try:
            if document:
                document.status = "embedding"
                db.commit()

            process_document_embeddings(
                document_id=job.document_id,
                db=db,
            )

            if document:
                document.status = "embedded"
                db.commit()

            mark_job_completed(job, db)

        except Exception as error:
            if document:
                document.status = "failed"
                db.commit()

            mark_job_failed(
                job=job,
                error=str(error),
                db=db,
            )

    finally:
        db.close()