from fastapi import APIRouter, HTTPException
from app.models.content_adaptation import ContentAdaptationRequest
from app.services.llama_service import adapt_content

router = APIRouter()

@router.post("/")
async def adapt_educational_content(request: ContentAdaptationRequest):
    """
    Adapt educational content based on the provided parameters.
    """
    try:
        adapted_content = await adapt_content(request)
        return {"adapted_content": adapted_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
