from fastapi import APIRouter, HTTPException
from app.models.quizzes import QuizRequest
from app.services.llama_service import generate_quiz

router = APIRouter()

@router.post("/")
async def create_quiz(request: QuizRequest):
    """
    Generate a quiz based on the provided parameters.
    Returns the quiz text and detected educational resources.
    """
    try:
        result = await generate_quiz(request)
        return {
            "quiz": result["text"],
            "resources": result["resources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
