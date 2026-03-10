import math
from typing import Optional
from bson.objectid import ObjectId
from app.database.connection import get_sessions_collection, get_questions_collection

def get_next_question(session_id: str) -> Optional[dict]:
    """
    Fetches the next question for a given session based on the user's ability score.
    Finds the question whose difficulty is closest to the current ability score,
    excluding previously answered questions.
    Returns None if completed.
    """
    sessions_coll = get_sessions_collection()
    questions_coll = get_questions_collection()

    session = sessions_coll.find_one({"session_id": session_id})
    if not session:
        raise ValueError(f"Session {session_id} not found")

    if session.get("completed", False):
        return None

    ability_score = session.get("ability_score", 0.5)
    answered_qs = session.get("questions_answered", [])
    
    if len(answered_qs) >= 10:
        return None
    
    # Fetch all questions
    all_questions = list(questions_coll.find({}))
    
    # Filter out answered questions
    available_qs = [
        q for q in all_questions 
        if str(q.get("_id")) not in answered_qs
    ]

    if not available_qs:
        return None  # No more questions

    # Find the question closest to ability score
    best_question = min(
        available_qs,
        key=lambda q: abs(q.get("difficulty", 0.5) - ability_score)
    )

    # Format output for the API
    return {
        "question_id": str(best_question["_id"]),
        "question": best_question["question"],
        "options": best_question["options"],
        "difficulty": best_question["difficulty"]
    }

def submit_answer(session_id: str, question_id: str, selected_answer: str) -> dict:
    """
    Submits an answer, evaluates if it's correct, and updates the session's ability score
    using simplified Item Response Theory. Marks session completed at 10 questions.
    """
    sessions_coll = get_sessions_collection()
    questions_coll = get_questions_collection()

    session = sessions_coll.find_one({"session_id": session_id})
    if not session:
        raise ValueError(f"Session {session_id} not found")
        
    if session.get("completed", False):
        raise ValueError(f"Session {session_id} is already completed")

    try:
        q_object_id = ObjectId(question_id)
    except Exception:
        raise ValueError(f"Invalid question_id format: {question_id}")

    question = questions_coll.find_one({"_id": q_object_id})
    if not question:
        raise ValueError(f"Question {question_id} not found")

    correct_answer = question.get("correct_answer")
    is_correct = (selected_answer == correct_answer)

    # Simplified IRT
    ability = session.get("ability_score", 0.5)
    difficulty = question.get("difficulty", 0.5)
    
    # Probability of correct response
    p_correct = 1.0 / (1.0 + math.exp(-(ability - difficulty)))
    
    actual = 1.0 if is_correct else 0.0
    learning_rate = 0.1

    new_ability = ability + learning_rate * (actual - p_correct)
    
    # Clamp between 0.1 and 1.0
    new_ability = max(0.1, min(1.0, new_ability))

    answered_qs = session.get("questions_answered", [])
    answered_qs.append(question_id)

    responses = session.get("responses", [])
    responses.append({
        "question_id": question_id,
        "is_correct": is_correct,
        "difficulty": difficulty,
        "topic": question.get("topic", "Unknown")
    })
    
    completed = len(answered_qs) >= 10

    # Update session
    sessions_coll.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "ability_score": new_ability, 
                "questions_answered": answered_qs,
                "responses": responses,
                "completed": completed
            }
        }
    )

    return {
        "correct": is_correct,
        "updated_ability": new_ability
    }
