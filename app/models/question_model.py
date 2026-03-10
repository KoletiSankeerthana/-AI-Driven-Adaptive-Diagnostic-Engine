from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class QuestionModel(BaseModel):
    """
    Pydantic model representing a single exam question.
    """
    id: Optional[str] = Field(default=None, description="Optional document ID")
    question: str = Field(..., description="The text of the question")
    options: List[str] = Field(..., min_length=4, description="List of possible answers")
    correct_answer: str = Field(..., description="The correct answer, must exist in options")
    difficulty: float = Field(..., ge=0.1, le=1.0, description="Difficulty score from 0.1 to 1.0")
    topic: str = Field(..., description="Topic category (e.g., Algebra, Vocabulary)")
    tags: List[str] = Field(default_factory=list, description="Relevant tags for the question")

    @model_validator(mode='after')
    def validate_correct_answer(self) -> 'QuestionModel':
        """
        Validates that the correct_answer is present in the options list.
        """
        if self.correct_answer not in self.options:
            raise ValueError("correct_answer must be one of the provided options")
        return self
