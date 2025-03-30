from fastapi import APIRouter, HTTPException
from app.models.content_adaptation import ContentAdaptationRequest
from app.services.llama_service import adapt_content

router = APIRouter()

@router.post("/")
async def adapt_educational_content(request: ContentAdaptationRequest):
    """
    Adapt educational content based on the provided parameters.
    Returns the adapted content text and detected educational resources.
    """
    try:
        result = await adapt_content(request)
        return {
            "adapted_content": result["text"],
            "resources": result["resources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
