import uuid
from fastapi import APIRouter, HTTPException
from typing import Dict
from app.models.session_model import SessionModel
from app.database.connection import get_sessions_collection

router = APIRouter(
    prefix="/session",
    tags=["Session"]
)

@router.post("/start-session", response_model=Dict[str, str])
async def start_session() -> dict:
    """
    Starts a new diagnostic session.
    Generates a unique session_id, creates a session document, and stores it in MongoDB.
    """
    try:
        session_id = str(uuid.uuid4())
        
        # Initialize the session document
        new_session = SessionModel(
            session_id=session_id
        )
        
        # Get the sessions collection and insert
        collection = get_sessions_collection()
        collection.insert_one(new_session.model_dump())
        
        return {"session_id": session_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")

from app.services.ai_service import generate_study_plan

@router.get("/study-plan/{session_id}")
async def get_study_plan(session_id: str) -> dict:
    """
    Retrieves an AI-powered study plan for the completed session.
    """
    try:
        plan = generate_study_plan(session_id)
        return plan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating study plan: {str(e)}")

@router.get("/summary/{session_id}")
async def get_session_summary(session_id: str) -> dict:
    """
    Retrieves the session summary including accuracy, final ability score, 
    weak topics, and the AI-generated study plan.
    """
    try:
        sessions_coll = get_sessions_collection()
        session = sessions_coll.find_one({"session_id": session_id})
        
        if not session:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        responses = session.get("responses", [])
        total_questions = len(responses)
        
        if total_questions == 0:
            raise HTTPException(status_code=400, detail="Cannot generate summary for an empty session.")
            
        correct_answers = sum(1 for r in responses if r.get("is_correct"))
        accuracy = (correct_answers / total_questions) * 100
        final_ability_score = session.get("ability_score", 0.5)
        
        incorrect_responses = [r for r in responses if not r.get("is_correct")]
        weak_topics = list({r.get("topic") for r in incorrect_responses if r.get("topic")})
        
        study_plan_result = generate_study_plan(session_id)
        
        return {
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy": round(accuracy, 2),
            "final_ability_score": round(final_ability_score, 4),
            "weak_topics": weak_topics,
            "study_plan": study_plan_result.get("study_plan", [])
        }
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating session summary: {str(e)}")
