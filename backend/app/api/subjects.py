from fastapi import APIRouter, HTTPException
from app.models.subjects import SubjectRequest, CurriculumRequest, StudentKnowledgeRequest
from app.services.subject_service import generate_subject_resources, generate_curriculum, generate_personalized_path

router = APIRouter()

@router.post("/resources")
async def get_subject_resources(request: SubjectRequest):
    """
    Generate resources for a specific subject and level.
    """
    try:
        resources = await generate_subject_resources(request)
        return {"resources": resources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/curriculum")
async def create_curriculum(request: CurriculumRequest):
    """
    Generate a curriculum for a specific subject and level.
    """
    try:
        curriculum = await generate_curriculum(request)
        return {"curriculum": curriculum}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/personalized-path")
async def create_personalized_path(request: StudentKnowledgeRequest):
    """
    Generate a personalized learning path based on student's prior knowledge.
    """
    try:
        learning_path = await generate_personalized_path(request)
        return {"learning_path": learning_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
