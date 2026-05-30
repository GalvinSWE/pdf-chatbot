from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.evaluation_schema import EvaluationRequest
from app.models.evaluation import EvaluationResult

from app.services.evaluation_service import (
    run_batch_evaluation,
)

router = APIRouter(
    prefix="/evaluation",
    tags=["evaluation"],
)

@router.post("/run")
async def run_evaluation(
    request: EvaluationRequest,
    db: Session = Depends(get_db),
):
    return run_batch_evaluation(
        document_id=request.document_id,
        items=request.items,
        db=db,
    )

@router.get("/results")
async def evaluation_results(
    db: Session = Depends(get_db),
):
    records = (
        db.query(EvaluationResult)
        .order_by(EvaluationResult.created_at.desc())
        .all()
    )

    return [
        {
            "question": record.question,
            "score": record.score,
            "created_at": record.created_at,
        }
        for record in records
    ]