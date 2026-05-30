from pydantic import BaseModel

class EvaluationItem(BaseModel):
    question: str
    expected_answer: str

class EvaluationRequest(BaseModel):
    document_id: str
    items: list[EvaluationItem]