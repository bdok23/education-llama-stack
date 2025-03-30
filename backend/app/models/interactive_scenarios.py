from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ScenarioType(str, Enum):
    role_playing = "role_playing"
    problem_solving = "problem_solving"
    simulation = "simulation"
    case_study = "case_study"

class InteractiveScenarioRequest(BaseModel):
    subject: str = Field(..., description="Subject of the scenario")
    grade_level: str = Field(..., description="Grade level of the students")
    topic: str = Field(..., description="Specific topic within the subject")
    scenario_type: ScenarioType = Field(..., description="Type of interactive scenario")
    learning_objectives: List[str] = Field(..., description="List of learning objectives")
    duration_minutes: int = Field(30, description="Estimated duration in minutes")
    complexity: int = Field(3, ge=1, le=5, description="Complexity level (1-5)")
    include_materials: bool = Field(True, description="Whether to include required materials")
    include_instructions: bool = Field(True, description="Whether to include teacher instructions")
