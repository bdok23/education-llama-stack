from fastapi import APIRouter, HTTPException
from app.models.quizzes import QuizRequest
from app.services.llama_service import generate_quiz

router = APIRouter()

@router.post("/")
async def create_quiz(request: QuizRequest):
    """
    Generate a quiz based on the provided parameters.
    """
    try:
        quiz = await generate_quiz(request)
        return {"quiz": quiz}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
