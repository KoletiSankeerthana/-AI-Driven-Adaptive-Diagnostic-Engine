from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.services.adaptive_engine import get_next_question, submit_answer

router = APIRouter(
    prefix="/question",
    tags=["Question"]
)

class AnswerSubmission(BaseModel):
    """Payload for submitting an answer."""
    session_id: str
    question_id: str
    answer: str

@router.get("/next/{session_id}")
async def fetch_next_question(session_id: str) -> Dict[str, Any]:
    """
    Retrieves the next question adapted to the user's ability score.
    Returns a completion message if the session is completed or 10 questions are answered.
    """
    try:
        question = get_next_question(session_id)
        if question is None:
            # Session completed logic
            return {"message": "Test completed. Generate study plan."}
        return question
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch next question: {str(e)}")

@router.post("/submit-answer")
async def process_answer(submission: AnswerSubmission) -> Dict[str, Any]:
    """
    Processes the answer, updates the ability score, and returns correctness.
    """
    try:
        result = submit_answer(
            session_id=submission.session_id,
            question_id=submission.question_id,
            selected_answer=submission.answer
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")
