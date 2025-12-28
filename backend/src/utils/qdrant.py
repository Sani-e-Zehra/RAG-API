from qdrant_client import QdrantClient
from qdrant_client.http.models import CollectionConfig, VectorParams, Distance
from qdrant_client.http.exceptions import UnexpectedResponse
from typing import Optional, List, Dict
from ..utils.config import settings
import logging

logger = logging.getLogger(__name__)


class QdrantConnection:
    """
    Singleton class to manage Qdrant connection and collection setup
    """
    _instance: Optional['QdrantConnection'] = None
    client: Optional[QdrantClient] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _initialize(self):
        """
        Lazy initialization of Qdrant client and collection
        """
        if self._initialized:
            return
        
        try:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )
            self._ensure_collection_exists()
            self._initialized = True
        except Exception as e:
            logger.warning(f"Failed to initialize Qdrant connection: {e}. The service will continue but RAG features may not work.")
            self._initialized = True  # Mark as initialized to prevent repeated attempts

    def _ensure_collection_exists(self):
        """
        Ensures the collection exists in Qdrant with the correct configuration
        """
        if not self.client:
            return
            
        try:
            # Try to get collection info
            self.client.get_collection(settings.QDRANT_COLLECTION_NAME)
            logger.info(f"Collection {settings.QDRANT_COLLECTION_NAME} already exists")
        except UnexpectedResponse as e:
            if e.status_code == 404:
                # Collection doesn't exist, create it
                try:
                    # Vector size for text-embedding-3-small is 1536
                    self.client.create_collection(
                        collection_name=settings.QDRANT_COLLECTION_NAME,
                        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
                    )
                    logger.info(f"Created collection: {settings.QDRANT_COLLECTION_NAME}")
                except Exception as create_error:
                    logger.error(f"Failed to create collection: {create_error}")
                    raise
            else:
                logger.error(f"Unexpected Qdrant response: {e}")
                raise
        except Exception as e:
            logger.error(f"Error checking/creating collection: {e}")
            raise

    def get_client(self) -> Optional[QdrantClient]:
        """
        Returns the Qdrant client instance, initializing if necessary
        """
        if not self._initialized:
            self._initialize()
        return self.client


# Create a global instance (lazy initialization)
qdrant_connection = QdrantConnection()


def get_qdrant_client() -> Optional[QdrantClient]:
    """
    Function to get the Qdrant client instance
    """
    return qdrant_connection.get_client()


async def search_similar_chunks(
    query_embedding: List[float],
    top_k: int = 5,
    score_threshold: float = 0.5,
    collection_name: Optional[str] = None
) -> List[Dict]:
    """
    Search Qdrant for similar content chunks based on query embedding
    
    Args:
        query_embedding: The embedding vector for the query
        top_k: Number of top results to return
        score_threshold: Minimum similarity score (0-1)
        collection_name: Optional collection name override
    
    Returns:
        List of dictionaries containing text, source, score, and metadata
    """
    qdrant_client = get_qdrant_client()
    if not qdrant_client:
        logger.warning("Qdrant client not available for search")
        return []
    
    collection = collection_name or settings.QDRANT_COLLECTION_NAME
    
    try:
        # Try with named vector first (for collections created with named vectors)
        try:
            results = qdrant_client.search(
                collection_name=collection,
                query_vector=("content", query_embedding),  # Named vector
                limit=top_k,
                score_threshold=score_threshold
            )
        except Exception:
            # Fallback to unnamed vector (for collections created without named vectors)
            results = qdrant_client.search(
                collection_name=collection,
                query_vector=query_embedding,  # Unnamed vector
                limit=top_k,
                score_threshold=score_threshold
            )
        
        chunks = []
        for result in results:
            chunks.append({
                'text': result.payload.get('text', ''),
                'source': result.payload.get('source', 'unknown'),
                'score': result.score,
                'chunk_id': result.payload.get('chunk_id', ''),
                'doc_id': result.payload.get('doc_id', ''),
                'metadata': {k: v for k, v in result.payload.items() 
                            if k not in ['text', 'source', 'chunk_id', 'doc_id']}
            })
        
        logger.info(f"Retrieved {len(chunks)} chunks from Qdrant")
        return chunks
    except Exception as e:
        logger.error(f"Error searching Qdrant: {e}")
        return []


def get_collection_count(collection_name: Optional[str] = None) -> int:
    """
    Get the number of vectors in the collection
    
    Args:
        collection_name: Optional collection name override
    
    Returns:
        Number of vectors in the collection, or 0 if error
    """
    qdrant_client = get_qdrant_client()
    if not qdrant_client:
        return 0
    
    collection = collection_name or settings.QDRANT_COLLECTION_NAME
    
    try:
        collection_info = qdrant_client.get_collection(collection)
        return collection_info.points_count
    except Exception as e:
        logger.error(f"Error getting collection count: {e}")
        return 0