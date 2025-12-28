from typing import Optional
from ..models.base_models import TranslateRequest, TranslateResponse
from ..utils.logging import log_function_call
from ..utils.config import settings
from openai import AsyncOpenAI
import os


class TranslationService:
    """
    Service class to handle content translation using LLMs
    """
    
    def __init__(self):
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = AsyncOpenAI(api_key=api_key)
    
    @log_function_call
    async def translate_content(self, request: TranslateRequest) -> TranslateResponse:
        """
        Translates content from source language to target language
        """
        try:
            # Create a prompt for translation
            prompt = f"Translate the following text from {request.source_language} to {request.target_language}:\n\n{request.content}"
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=len(request.content) * 2,  # Allow more tokens for longer content
                temperature=0.3
            )
            
            translated_content = response.choices[0].message.content
            
            return TranslateResponse(
                translated_content=translated_content,
                source_language=request.source_language,
                target_language=request.target_language
            )
        except Exception as e:
            print(f"Error in translation service: {e}")
            raise e
    
    @log_function_call
    async def translate_text_segment(self, text: str, target_language: str = "ur", source_language: str = "en") -> str:
        """
        Translates a segment of text
        """
        request = TranslateRequest(
            content=text,
            source_language=source_language,
            target_language=target_language
        )
        
        response = await self.translate_content(request)
        return response.translated_content