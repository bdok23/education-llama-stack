from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ReadingLevel(str, Enum):
    elementary = "elementary"
    middle_school = "middle_school"
    high_school = "high_school"
    college = "college"

class LearningStyle(str, Enum):
    visual = "visual"
    auditory = "auditory"
    reading_writing = "reading_writing"
    kinesthetic = "kinesthetic"

class ContentAdaptationRequest(BaseModel):
    content: str = Field(..., description="Original educational content to adapt")
    target_reading_level: ReadingLevel = Field(..., description="Target reading level")
    target_learning_style: Optional[LearningStyle] = Field(
        None, description="Target learning style"
    )
    simplify: bool = Field(False, description="Whether to simplify the content")
