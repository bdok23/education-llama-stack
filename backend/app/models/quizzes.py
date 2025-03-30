from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class QuestionType(str, Enum):
    multiple_choice = "multiple_choice"
    short_answer = "short_answer"
    essay = "essay"
    true_false = "true_false"

class QuizRequest(BaseModel):
    subject: str = Field(..., description="Subject of the quiz")
    topic: str = Field(..., description="Specific topic within the subject")
    difficulty: int = Field(..., ge=1, le=5, description="Difficulty level (1-5)")
    num_questions: int = Field(..., ge=1, le=20, description="Number of questions")
    question_types: List[QuestionType] = Field(
        default=[QuestionType.multiple_choice],
        description="Types of questions to include"
    )
