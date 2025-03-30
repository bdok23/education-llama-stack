from fastapi import APIRouter, HTTPException
from app.models.subjects import SubjectRequest, CurriculumRequest, StudentKnowledgeRequest
from app.services.subject_service import generate_subject_resources, generate_curriculum, generate_personalized_path
from app.utils.hyperlink_processor import enrich_content_with_hyperlinks

router = APIRouter()

@router.post("/resources")
async def get_subject_resources(request: SubjectRequest):
    """
    Generate resources for a specific subject and level.
    Returns the resources text and detected educational resources.
    """
    try:
        resources_text = await generate_subject_resources(request)
        result = enrich_content_with_hyperlinks(resources_text)
        return {
            "resources": result["text"],
            "resource_links": result["resources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/curriculum")
async def create_curriculum(request: CurriculumRequest):
    """
    Generate a curriculum for a specific subject and level.
    Returns the curriculum text and detected educational resources.
    """
    try:
        curriculum_text = await generate_curriculum(request)
        result = enrich_content_with_hyperlinks(curriculum_text)
        return {
            "curriculum": result["text"],
            "resources": result["resources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/personalized-path")
async def create_personalized_path(request: StudentKnowledgeRequest):
    """
    Generate a personalized learning path based on student's prior knowledge.
    Returns the learning path text and detected educational resources.
    """
    try:
        learning_path_text = await generate_personalized_path(request)
        result = enrich_content_with_hyperlinks(learning_path_text)
        return {
            "learning_path": result["text"],
            "resources": result["resources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
