import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from ...agents.rag_agent import RAGAgent
from ...utils.config import settings


@pytest.mark.asyncio
async def test_rag_query_performance():
    """
    Test that RAG queries perform within acceptable time limits
    """
    # Mock the OpenAI client
    mock_client = AsyncMock()
    
    # Create RAG agent instance
    rag_agent = RAGAgent(mock_client)
    
    # Mock the retrieve_context method to simulate fast response
    rag_agent.retrieve_context = AsyncMock(return_value=[
        {'text': 'Test context for performance evaluation', 'source': 'test-source', 'score': 0.9}
    ])
    
    # Measure query execution time
    import time
    start_time = time.time()
    
    response = await rag_agent.answer_question("What are AI-native systems?")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Assert query completed within performance target
    assert execution_time <= 1.5, f"Query took {execution_time:.2f}s, exceeding 1.5s target"
    
    # Verify response structure
    assert hasattr(response, 'answer')
    assert hasattr(response, 'sources')
    assert hasattr(response, 'confidence')


@pytest.mark.asyncio
async def test_rag_batch_queries_performance():
    """
    Test that multiple RAG queries perform acceptably
    """
    mock_client = AsyncMock()
    rag_agent = RAGAgent(mock_client)
    
    # Mock the retrieve_context method
    rag_agent.retrieve_context = AsyncMock(return_value=[
        {'text': 'Test context for performance evaluation', 'source': 'test-source', 'score': 0.9}
    ])
    
    # Test multiple queries in sequence
    queries = [
        "What are AI-native systems?",
        "How does RAG work?",
        "What is vector embedding?",
        "Explain neural networks",
        "What is machine learning?"
    ]
    
    start_time = time.time()
    
    for query in queries:
        response = await rag_agent.answer_question(query)
        assert response is not None
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / len(queries)
    
    # Average should be under 1.5s per query
    assert avg_time <= 1.5, f"Average query time was {avg_time:.2f}s, exceeding 1.5s target"
    
    # Total time should be reasonable for 5 queries
    assert total_time <= 7.5, f"Total time was {total_time:.2f}s, exceeding 7.5s target for 5 queries"