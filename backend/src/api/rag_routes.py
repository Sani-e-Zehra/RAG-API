from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from uuid import UUID
import os
from ..models.base_models import RagQueryRequest, RagQueryResponse, HighlightQueryRequest
from ..models.content_models import ChatMessageCreate
from ..services.chat_service import ChatService
from ..utils.config import settings
from ..utils.qdrant import get_qdrant_client
from ..utils.logging import AppException
from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/rag", tags=["RAG"])


def get_openai_client():
    """
    Dependency to get OpenAI client
    """
    from ..utils.config import settings
    from openai import AsyncOpenAI
    api_key = settings.OPENAI_API_KEY
    if not api_key or api_key == "sk-proj-REPLACE-WITH-YOUR-OPENAI-API-KEY":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI API key not configured"
        )
    return AsyncOpenAI(api_key=api_key)


def get_rag_agent():
    """
    Dependency to get RAG agent instance
    """
    from agents.rag_agent import RAGAgent
    openai_client = get_openai_client()
    return RAGAgent(openai_client)


@router.post("/query", response_model=RagQueryResponse)
async def rag_query(
    request: RagQueryRequest,
    rag_agent=Depends(get_rag_agent)
):
    """
    Submit a question to the RAG system to get an answer based on book content
    """
    try:
        response = await rag_agent.answer_question(
            question=request.question,
            context=request.context
        )
        
        return RagQueryResponse(
            answer=response.answer,
            sources=response.sources,
            confidence=response.confidence
        )
    except Exception as e:
        logger.error(f"Error in RAG query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing RAG query"
        )


@router.post("/highlight-query", response_model=RagQueryResponse)
async def highlight_query(
    request: HighlightQueryRequest,
    rag_agent=Depends(get_rag_agent)
):
    """
    Submit a question about specific highlighted text from the book
    """
    try:
        # For highlight-based queries, we specifically use the selected text as context
        response = await rag_agent.answer_question(
            question=request.question,
            context=request.selected_text
        )
        
        return RagQueryResponse(
            answer=response.answer,
            sources=response.sources,
            confidence=response.confidence
        )
    except Exception as e:
        logger.error(f"Error in highlight query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing highlight query"
        )