from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class FeedbackType(str, Enum):
    assignment = "assignment"
    essay = "essay"
    project = "project"
    presentation = "presentation"
    quiz = "quiz"

class FeedbackTone(str, Enum):
    encouraging = "encouraging"
    constructive = "constructive"
    detailed = "detailed"
    brief = "brief"

class FeedbackRequest(BaseModel):
    student_work: str = Field(..., description="The student's work to provide feedback on")
    subject: str = Field(..., description="Subject of the assignment")
    grade_level: str = Field(..., description="Grade level of the student")
    assignment_description: str = Field(..., description="Description of the assignment")
    feedback_type: FeedbackType = Field(..., description="Type of feedback to provide")
    feedback_tone: FeedbackTone = Field(FeedbackTone.constructive, description="Tone of the feedback")
    include_strengths: bool = Field(True, description="Whether to include strengths")
    include_areas_for_improvement: bool = Field(True, description="Whether to include areas for improvement")
    include_next_steps: bool = Field(True, description="Whether to include next steps for improvement")
