import time

from app.db.session import SessionLocal
from app.models.job import Job
from app.services.embedding_pipeline_service import process_document_embeddings
from app.services.job_service import (
    mark_job_completed,
    mark_job_failed,
    mark_job_running,
)

def process_pending_jobs():
    db = SessionLocal()

    try:
        job = (
            db.query(Job)
            .filter(Job.status == "pending")
            .order_by(Job.created_at.asc())
            .first()
        )

        if not job:
            return

        mark_job_running(job, db)

        try:
            if job.type == "document_embedding":
                process_document_embeddings(
                    document_id=job.document_id,
                    db=db,
                )

            mark_job_completed(job, db)

        except Exception as error:
            mark_job_failed(
                job=job,
                error=str(error),
                db=db,
            )

    finally:
        db.close()


def run_worker():
    print("Worker started...")

    while True:
        process_pending_jobs()
        time.sleep(2)


if __name__ == "__main__":
    run_worker()