from fastapi import APIRouter, HTTPException
from app.models.feedback import FeedbackRequest
from app.services.llama_service import generate_feedback

router = APIRouter()

@router.post("/")
async def create_feedback(request: FeedbackRequest):
    """
    Generate feedback for student work based on the provided parameters.
    """
    try:
        feedback = await generate_feedback(request)
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
