from fastapi import APIRouter, Depends, HTTPException, status
from ..models.base_models import TranslateRequest, TranslateResponse
from ..services.translation_service import TranslationService
from ..utils.config import settings
from ..utils.logging import AppException


router = APIRouter(prefix="/translate", tags=["Translation"])


@router.post("/urdu", response_model=TranslateResponse)
async def translate_to_urdu(
    request: TranslateRequest,
    translation_service: TranslationService = Depends(TranslationService)
):
    """
    Translate book content to Urdu
    """
    try:
        # Ensure the target language is Urdu
        request.target_language = "ur"
        
        response = await translation_service.translate_content(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error translating content to Urdu: {str(e)}"
        )


# General translation endpoint
@router.post("", response_model=TranslateResponse)
async def translate_content(
    request: TranslateRequest,
    translation_service: TranslationService = Depends(TranslationService)
):
    """
    Translate book content from source to target language
    """
    try:
        response = await translation_service.translate_content(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error translating content: {str(e)}"
        )