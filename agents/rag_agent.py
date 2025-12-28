# RAG Agent for question answering from book content

import asyncio
import sys
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import backend utilities
from backend.src.utils.embeddings import generate_embedding
from backend.src.utils.qdrant import search_similar_chunks
from backend.src.utils.config import settings
import logging

logger = logging.getLogger(__name__)


class QARequest(BaseModel):
    question: str
    context: str = None


class QAResponse(BaseModel):
    answer: str
    sources: List[str] = []
    confidence: float = 0.0


class RAGAgent:
    """
    RAG (Retrieval-Augmented Generation) agent that answers questions
    based on book content retrieved from Qdrant vector database.
    """
    
    def __init__(self, openai_client):
        self.client = openai_client
        
    async def answer_question(self, question: str, context: str = None) -> QAResponse:
        """
        Answers a question based on retrieved book content or provided context
        
        Args:
            question: The user's question
            context: Optional explicit context (if provided, skips vector search)
        
        Returns:
            QAResponse with answer, sources, and confidence
        """
        try:
            retrieved_chunks = []
            sources = []
            retrieved_context = ""
            
            # If no explicit context provided, retrieve from vector database
            if not context:
                # Generate embedding for the question
                question_embedding = await generate_embedding(question)
                
                if question_embedding:
                    # Search Qdrant for similar content chunks
                    retrieved_chunks = await search_similar_chunks(
                        query_embedding=question_embedding,
                        top_k=5,
                        score_threshold=0.5
                    )
                    
                    if retrieved_chunks:
                        # Combine retrieved chunks into context
                        retrieved_context = "\n\n".join([
                            f"[Source: {chunk.get('source', 'unknown')}]\n{chunk.get('text', '')}"
                            for chunk in retrieved_chunks
                        ])
                        
                        # Extract unique sources
                        sources = list(set([
                            chunk.get('source', 'unknown') 
                            for chunk in retrieved_chunks 
                            if chunk.get('source')
                        ]))
                        
                        logger.info(f"Retrieved {len(retrieved_chunks)} chunks from vector database")
                    else:
                        logger.warning("No chunks retrieved from vector database, using general knowledge")
                else:
                    logger.warning("Failed to generate embedding, using general knowledge")
            
            # Use retrieved context or provided context
            if context:
                # Use explicit context provided by user
                prompt = f"Based on the following context:\n\n{context}\n\nAnswer the question: {question}"
                sources = ["user-provided"]
                confidence = 0.9
            elif retrieved_context:
                # Use retrieved context from vector database
                prompt = f"""Based on the following context from the book content:

{retrieved_context}

Answer the question: {question}

If the context doesn't contain enough information to answer the question, say so."""
                # Calculate confidence based on average similarity scores
                if retrieved_chunks:
                    avg_score = sum(chunk.get('score', 0) for chunk in retrieved_chunks) / len(retrieved_chunks)
                    confidence = min(0.95, max(0.5, avg_score))
                else:
                    confidence = 0.7
            else:
                # Fallback to general knowledge
                prompt = f"Answer the question based on your knowledge of AI-native systems and humanoid robotics: {question}"
                sources = ["general-knowledge"]
                confidence = 0.6
                logger.warning("No context available, using general knowledge")
                
            # Call LLM with the prompt
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3
            )
            
            answer = response.choices[0].message.content
            
            return QAResponse(
                answer=answer,
                sources=sources if sources else ["general-knowledge"],
                confidence=confidence
            )
        except Exception as e:
            logger.error(f"Error in RAG agent: {e}", exc_info=True)
            return QAResponse(
                answer="Sorry, I couldn't process your question at the moment. Please try again.",
                sources=[],
                confidence=0.0
            )