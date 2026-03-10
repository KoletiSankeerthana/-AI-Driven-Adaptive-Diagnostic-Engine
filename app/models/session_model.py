from typing import List, Optional
from pydantic import BaseModel, Field

class SessionModel(BaseModel):
    """
    Pydantic model representing a user's diagnostic test session.
    """
    session_id: str = Field(..., description="Unique identifier for the session")
    ability_score: float = Field(default=0.5, description="Initial ability score of the user")
    questions_answered: List[str] = Field(default_factory=list, description="List of answered question IDs")
    responses: List[dict] = Field(default_factory=list, description="Detailed records of responses including correctness and topic")
    current_question: Optional[str] = Field(default=None, description="ID of the question currently being presented")
    completed: bool = Field(default=False, description="Whether the diagnostic session is fully completed")
