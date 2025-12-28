# Context Management Analysis - Backend RAG System

## Current Implementation Status

### ❌ **Issue: RAG Agent is NOT Retrieving from Vector Database**

The current implementation has a **critical gap**: The RAG agent does not actually retrieve content from the Qdrant vector database. It only uses context if explicitly provided by the client.

---

## How Context is Currently Managed

### 1. **Request Flow**

```
Client Request → FastAPI Route → RAG Agent → OpenAI API
```

**Files:**
- `backend/src/api/rag_routes.py` - API endpoints
- `agents/rag_agent.py` - RAG agent implementation

### 2. **Two Query Types**

#### A. **Regular Query** (`/v1/rag/query`)
- **Request Model**: `RagQueryRequest`
  - `question: str` - The user's question
  - `context: Optional[str]` - Optional context (if provided by client)

- **Current Behavior**:
  - If `context` is provided → Uses that context directly
  - If `context` is None → Falls back to general knowledge prompt
  - **NO vector search is performed**

#### B. **Highlight Query** (`/v1/rag/highlight-query`)
- **Request Model**: `HighlightQueryRequest`
  - `question: str` - The user's question
  - `selected_text: str` - Text selected by user
  - `context: Optional[str]` - Optional additional context

- **Current Behavior**:
  - Uses `selected_text` as the context
  - **NO vector search is performed**

### 3. **RAG Agent Implementation** (`agents/rag_agent.py`)

```python
async def answer_question(self, question: str, context: str = None) -> QAResponse:
    # Line 34-35: Comment says "In a real implementation, we would retrieve 
    # relevant content from our vector database here"
    # BUT: No actual retrieval happens!
    
    if context:
        # Uses provided context directly
        prompt = f"Based on the following context: {context}\n\nAnswer the question: {question}"
    else:
        # Falls back to general knowledge
        prompt = f"Answer the question based on your knowledge of AI-native systems: {question}"
    
    # Just calls OpenAI with the prompt
    response = await self.client.chat.completions.create(...)
    
    # Returns placeholder sources
    return QAResponse(
        answer=answer,
        sources=["source-placeholder"] if context else ["general-knowledge"],
        confidence=0.85  # Hardcoded, not calculated
    )
```

**Problems:**
1. ❌ No vector database query
2. ❌ No embedding generation for the question
3. ❌ No similarity search in Qdrant
4. ❌ No retrieval of relevant book chunks
5. ❌ Sources are placeholders
6. ❌ Confidence is hardcoded

---

## What Content Should Be Read (But Isn't)

### Expected Flow (What Should Happen):

```
1. User asks question
2. Generate embedding for question
3. Search Qdrant for similar content chunks
4. Retrieve top-k relevant chunks
5. Combine chunks as context
6. Send question + context to LLM
7. Return answer with actual sources
```

### Available Infrastructure (But Not Used):

1. **Qdrant Client** (`backend/src/utils/qdrant.py`)
   - ✅ Connection management exists
   - ✅ Collection setup exists
   - ❌ **NOT used for retrieval in RAG agent**

2. **Embedding Model** (`backend/src/utils/config.py`)
   - ✅ `OPENAI_EMBEDDING_MODEL` configured (text-embedding-3-small)
   - ❌ **NOT used to generate question embeddings**

3. **Ingestion Pipeline** (`pipelines/`)
   - ✅ Content is being uploaded to Qdrant
   - ✅ Embeddings are generated for book content
   - ❌ **But this content is never retrieved during queries**

4. **Qdrant Collection**
   - ✅ Collection name: `book_vectors` (or `content` based on config)
   - ✅ Vector size: 1536 (for text-embedding-3-small)
   - ✅ Distance metric: COSINE
   - ❌ **Collection exists but is not queried**

---

## Current Context Sources

### What the System Actually Uses:

1. **Explicit Context** (if provided in request)
   - User-provided context string
   - Selected text from highlight query

2. **General Knowledge** (fallback)
   - LLM's training data
   - No book-specific content

### What the System Should Use:

1. **Retrieved Book Content** (from Qdrant)
   - Relevant chunks from the book
   - Based on semantic similarity to question
   - Multiple chunks combined for comprehensive context

2. **Metadata** (from retrieved chunks)
   - Source chapter/section
   - Chunk ID
   - Original document reference

---

## Code Locations

### Key Files:

1. **RAG Routes**: `backend/src/api/rag_routes.py`
   - Lines 44-68: Regular query endpoint
   - Lines 71-96: Highlight query endpoint
   - **Missing**: Vector search integration

2. **RAG Agent**: `agents/rag_agent.py`
   - Lines 29-63: `answer_question` method
   - **Missing**: Qdrant retrieval logic

3. **Qdrant Utils**: `backend/src/utils/qdrant.py`
   - ✅ Connection management
   - ❌ **No search/retrieval methods**

4. **Config**: `backend/src/utils/config.py`
   - ✅ Qdrant settings available
   - ✅ Embedding model configured
   - ❌ **Not used in RAG flow**

---

## What Needs to Be Implemented

### 1. **Add Vector Search to RAG Agent**

The `RAGAgent.answer_question()` method needs to:

```python
async def answer_question(self, question: str, context: str = None) -> QAResponse:
    # 1. Generate embedding for question
    question_embedding = await self.generate_question_embedding(question)
    
    # 2. Search Qdrant for similar chunks
    if not context:  # Only search if no explicit context provided
        retrieved_chunks = await self.search_qdrant(question_embedding, top_k=5)
        context = self.combine_chunks(retrieved_chunks)
        sources = [chunk['source'] for chunk in retrieved_chunks]
    else:
        sources = ["user-provided"]
    
    # 3. Use retrieved context for LLM
    prompt = f"Based on the following context: {context}\n\nAnswer: {question}"
    
    # 4. Call LLM
    response = await self.client.chat.completions.create(...)
    
    # 5. Return with actual sources
    return QAResponse(
        answer=response.choices[0].message.content,
        sources=sources,
        confidence=self.calculate_confidence(retrieved_chunks)
    )
```

### 2. **Add Qdrant Search Method**

In `backend/src/utils/qdrant.py` or `agents/rag_agent.py`:

```python
async def search_similar_chunks(
    self, 
    query_embedding: List[float], 
    top_k: int = 5,
    score_threshold: float = 0.7
) -> List[Dict]:
    """
    Search Qdrant for similar content chunks
    """
    qdrant_client = get_qdrant_client()
    if not qdrant_client:
        return []
    
    results = qdrant_client.search(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k,
        score_threshold=score_threshold
    )
    
    chunks = []
    for result in results:
        chunks.append({
            'text': result.payload.get('text', ''),
            'source': result.payload.get('source', 'unknown'),
            'score': result.score,
            'metadata': {k: v for k, v in result.payload.items() 
                        if k not in ['text', 'source']}
        })
    
    return chunks
```

### 3. **Add Embedding Generation**

```python
async def generate_question_embedding(self, question: str) -> List[float]:
    """
    Generate embedding for the question using OpenAI
    """
    from openai import AsyncOpenAI
    from ..utils.config import settings
    
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    response = await client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=[question]
    )
    return response.data[0].embedding
```

---

## Summary

### Current State:
- ✅ Infrastructure exists (Qdrant, embeddings, ingestion)
- ✅ API endpoints are set up
- ❌ **No actual vector retrieval happens**
- ❌ RAG agent only uses explicit context or general knowledge
- ❌ Book content in Qdrant is never queried

### Impact:
- Users get answers from general knowledge, not from the book
- No source citations from actual book content
- Highlight queries work (use selected text) but regular queries don't use book content
- The "RAG" system is not actually doing retrieval-augmented generation

### Fix Required:
Implement vector search in the RAG agent to:
1. Generate question embeddings
2. Search Qdrant for similar content
3. Use retrieved chunks as context
4. Return actual sources and confidence scores


