from fastapi import APIRouter, HTTPException
from app.models.interactive_scenarios import InteractiveScenarioRequest
from app.services.llama_service import generate_interactive_scenario

router = APIRouter()

@router.post("/")
async def create_interactive_scenario(request: InteractiveScenarioRequest):
    """
    Generate an interactive learning scenario based on the provided parameters.
    Returns the scenario text and detected educational resources.
    """
    try:
        result = await generate_interactive_scenario(request)
        return {
            "scenario": result["text"],
            "resources": result["resources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
