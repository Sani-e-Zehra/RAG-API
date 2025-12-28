"""
Utility functions for generating embeddings using OpenAI
"""

from typing import List
from openai import AsyncOpenAI
from .config import settings
import logging

logger = logging.getLogger(__name__)


async def generate_embedding(text: str, model: str = None) -> List[float]:
    """
    Generate embedding for a single text using OpenAI
    
    Args:
        text: The text to generate embedding for
        model: Optional model override (defaults to settings.OPENAI_EMBEDDING_MODEL)
    
    Returns:
        List of floats representing the embedding vector
    """
    if not settings.OPENAI_API_KEY:
        logger.error("OpenAI API key not configured")
        return []
    
    model = model or settings.OPENAI_EMBEDDING_MODEL
    
    try:
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        response = await client.embeddings.create(
            model=model,
            input=[text]
        )
        
        if response.data and len(response.data) > 0:
            return response.data[0].embedding
        else:
            logger.warning("No embedding data returned from OpenAI")
            return []
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return []


async def generate_embeddings(texts: List[str], model: str = None) -> List[List[float]]:
    """
    Generate embeddings for multiple texts using OpenAI
    
    Args:
        texts: List of texts to generate embeddings for
        model: Optional model override (defaults to settings.OPENAI_EMBEDDING_MODEL)
    
    Returns:
        List of embedding vectors
    """
    if not settings.OPENAI_API_KEY:
        logger.error("OpenAI API key not configured")
        return [[] for _ in texts]
    
    if not texts:
        return []
    
    model = model or settings.OPENAI_EMBEDDING_MODEL
    
    try:
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        response = await client.embeddings.create(
            model=model,
            input=texts
        )
        
        return [item.embedding for item in response.data]
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return [[] for _ in texts]



