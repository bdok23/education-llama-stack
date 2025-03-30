from fastapi import APIRouter, HTTPException
from app.models.lesson_plans import LessonPlanRequest
from app.services.llama_service import generate_lesson_plan

router = APIRouter()

@router.post("/")
async def create_lesson_plan(request: LessonPlanRequest):
    """
    Generate a lesson plan based on the provided parameters.
    """
    try:
        lesson_plan = await generate_lesson_plan(request)
        return {"lesson_plan": lesson_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
