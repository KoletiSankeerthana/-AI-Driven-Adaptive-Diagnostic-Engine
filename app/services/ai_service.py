import os
from typing import List, Dict, Any
from openai import OpenAI
from app.database.connection import get_sessions_collection

# Load API Key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_study_plan(session_id: str) -> Dict[str, Any]:
    """
    Generates a personalized study plan using OpenAI API based on the user's
    diagnostic session performance.
    """
    sessions_coll = get_sessions_collection()
    session = sessions_coll.find_one({"session_id": session_id})
    
    if not session:
        raise ValueError(f"Session {session_id} not found")

    responses = session.get("responses", [])
    if not responses:
        raise ValueError("Not enough data to generate a study plan. No questions answered.")

    # Calculate metrics
    incorrect_responses = [r for r in responses if not r.get("is_correct")]
    weak_topics_set = {r.get("topic") for r in incorrect_responses if r.get("topic")}
    weak_topics = list(weak_topics_set)

    highest_difficulty = max((r.get("difficulty", 0.0) for r in responses), default=0.0)
    
    correct_count = sum(1 for r in responses if r.get("is_correct"))
    accuracy = (correct_count / len(responses)) * 100 if responses else 0.0

    # Fallback to general topics if no weak topics found
    if not weak_topics:
        weak_topics = ["General comprehensive review"]

    # Generate prompt
    prompt = (
        f"A student completed an adaptive diagnostic test. "
        f"Weak topics: {', '.join(weak_topics)}. "
        f"Highest difficulty reached: {highest_difficulty:.2f}. "
        f"Accuracy: {accuracy:.0f}%. "
        f"Provide a concise 3-step study plan to improve performance. Format output strictly as 3 bullet points starting with 'Step'."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert AI tutor offering highly concise and actionable study advice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        plan_text = response.choices[0].message.content.strip()
        # Parse output into array
        steps = [step.strip() for step in plan_text.split("\n") if step.strip()]
        
        return {"study_plan": steps}
    except Exception as e:
        print(f"Error generating study plan from AI: {e}")
        # Return fallback study plan
        return {
            "study_plan": [
                "Review the fundamentals of the weak topics identified.",
                "Practice medium difficulty GRE-style questions related to those topics.",
                "Take timed quizzes to improve accuracy and speed."
            ]
        }
