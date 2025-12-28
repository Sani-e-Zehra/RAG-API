from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..models.base_models import (
    SkillContentRequest, GlossaryResponse, SummaryResponse, 
    TutorRequest, TutorResponse
)
from ..services.translation_service import TranslationService
from ..utils.config import settings
from ..utils.logging import AppException


router = APIRouter(prefix="/skills", tags=["Skills"])


@router.post("/glossary", response_model=GlossaryResponse)
async def generate_glossary(
    request: SkillContentRequest
):
    """
    Generate a glossary of important terms from book content
    """
    try:
        # Import the glossary generator skill
        from skills.glossary_generator import GlossaryGenerator
        generator = GlossaryGenerator()
        
        response = await generator.generate_glossary(request.content, request.context)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating glossary: {str(e)}"
        )


@router.post("/summarize", response_model=SummaryResponse)
async def generate_summary(
    request: SkillContentRequest
):
    """
    Generate a summary of book content
    """
    try:
        # Import the chapter summarizer skill
        from skills.chapter_summarizer import ChapterSummarizer
        summarizer = ChapterSummarizer()
        
        response = await summarizer.generate_summary(request.content, request.context)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating summary: {str(e)}"
        )


@router.post("/tutor", response_model=TutorResponse)
async def interact_with_tutor(
    request: TutorRequest
):
    """
    Get explanations and guidance from a personalized tutor
    """
    try:
        # Import the personalized tutor skill
        from skills.personalized_tutor import PersonalizedTutor
        tutor = PersonalizedTutor()
        
        response = await tutor.provide_explanation(
            request.question, 
            request.context, 
            request.student_level
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error with personalized tutor: {str(e)}"
        )