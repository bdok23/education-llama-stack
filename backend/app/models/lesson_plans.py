from pydantic import BaseModel, Field
from typing import List

class LessonPlanRequest(BaseModel):
    subject: str = Field(..., description="Subject of the lesson plan")
    grade_level: str = Field(..., description="Grade level of the students")
    topic: str = Field(..., description="Specific topic within the subject")
    learning_objectives: List[str] = Field(..., description="List of learning objectives")
    duration_minutes: int = Field(60, description="Duration of the lesson in minutes")
