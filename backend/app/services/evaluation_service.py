from app.services.openrouter_service import create_chat_response
from app.services.rag_chat_service import ask_document_question
from app.models.evaluation import EvaluationResult

def judge_answer(
    question: str,
    expected_answer: str,
    generated_answer: str,
) -> float:
    prompt = f"""
      You are an evaluation judge.
      Question:
      {question}

      Expected Answer:
      {expected_answer}

      Generated Answer:
      {generated_answer}

      Give a score from 0 to 10.

      Return only the number.
    """

    result = create_chat_response(prompt)

    try:
        return float(result.strip())
    except Exception:
        return 0.0

def run_single_evaluation(
    document_id: str,
    question: str,
    expected_answer: str,
    db,
):
    result = ask_document_question(
        document_id=document_id,
        question=question,
        db=db,
    )

    generated_answer = result["answer"]

    score = judge_answer(
        question=question,
        expected_answer=expected_answer,
        generated_answer=generated_answer,
    )

    return {
        "question": question,
        "expected_answer": expected_answer,
        "generated_answer": generated_answer,
        "score": score,
    }

def save_evaluation_result(
    document_id: str,
    question: str,
    expected_answer: str,
    generated_answer: str,
    score: float,
    db,
):
    record = EvaluationResult(
        document_id=document_id,
        question=question,
        expected_answer=expected_answer,
        generated_answer=generated_answer,
        score=score,
    )

    db.add(record)
    db.commit()

    return record


def run_batch_evaluation(
    document_id: str,
    items: list,
    db,
):
    results = []

    for item in items:
        result = run_single_evaluation(
            document_id=document_id,
            question=item.question,
            expected_answer=item.expected_answer,
            db=db,
        )

        save_evaluation_result(
            document_id=document_id,
            question=item.question,
            expected_answer=item.expected_answer,
            generated_answer=result["generated_answer"],
            score=result["score"],
            db=db,
        )

        results.append(result)

    average_score = (
        sum(r["score"] for r in results)
        / len(results)
    )

    return {
        "average_score": average_score,
        "results": results,
    }