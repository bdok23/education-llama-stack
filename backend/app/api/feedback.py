from fastapi import APIRouter, HTTPException
from app.models.feedback import FeedbackRequest
from app.services.llama_service import generate_feedback

router = APIRouter()

@router.post("/")
async def create_feedback(request: FeedbackRequest):
    """
    Generate feedback for student work based on the provided parameters.
    Returns the feedback text and detected educational resources.
    """
    try:
        result = await generate_feedback(request)
        return {
            "feedback": result["text"],
            "resources": result["resources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
