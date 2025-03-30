from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class SubjectType(str, Enum):
    math = "math"
    coding = "coding"
    biology = "biology"
    chemistry = "chemistry"
    physics = "physics"

class SubjectLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class SubjectRequest(BaseModel):
    subject_type: SubjectType = Field(..., description="Type of subject")
    level: SubjectLevel = Field(..., description="Level of difficulty")
    topic: Optional[str] = Field(None, description="Specific topic within the subject")
    
class CurriculumRequest(BaseModel):
    subject_type: SubjectType = Field(..., description="Type of subject")
    level: SubjectLevel = Field(..., description="Level of difficulty")
    duration_weeks: int = Field(12, description="Duration of the curriculum in weeks")
    include_assessments: bool = Field(True, description="Whether to include assessments")
    include_resources: bool = Field(True, description="Whether to include additional resources")

class StudentKnowledgeRequest(BaseModel):
    subject_type: SubjectType = Field(..., description="Type of subject")
    topics_known: List[str] = Field(..., description="List of topics the student already knows")
    learning_objectives: List[str] = Field(..., description="List of learning objectives")
    preferred_learning_style: Optional[str] = Field(None, description="Student's preferred learning style")
