# Upload to vector DB for ingestion pipeline

from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
import uuid


class Uploader:
    """
    Uploads embedded content to Qdrant vector database
    """
    
    def __init__(self, qdrant_url: str, qdrant_api_key: str, collection_name: str = "book_vectors"):
        self.collection_name = collection_name
        try:
            self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            self._ensure_collection_exists()
        except Exception as e:
            print(f"Warning: Failed to initialize Qdrant client: {e}")
            print("Uploader will be available but uploads will fail until Qdrant is configured correctly.")
            self.client = None

    def _ensure_collection_exists(self):
        """
        Ensures the collection exists in Qdrant
        """
        if not self.client:
            raise Exception("Qdrant client not initialized")
            
        try:
            # Try to get collection info
            self.client.get_collection(self.collection_name)
            print(f"Collection {self.collection_name} already exists")
        except Exception as e:
            # Collection doesn't exist, create it
            try:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)  # Default for OpenAI embeddings
                )
                print(f"Created collection: {self.collection_name}")
            except Exception as create_error:
                error_msg = str(create_error)
                # Check if it's a 404 - might be URL/API key issue
                if "404" in error_msg or "Not Found" in error_msg:
                    print(f"Warning: Qdrant collection creation failed with 404. This might indicate:")
                    print(f"  - Incorrect Qdrant URL format for cloud instances")
                    print(f"  - Missing or incorrect API key")
                    print(f"  - Collection endpoint not accessible")
                    print(f"Please check your QDRANT_URL and QDRANT_API_KEY configuration.")
                raise Exception(f"Failed to create collection {self.collection_name}: {create_error}")

    def upload_chunks(self, texts: List[str], embeddings: List[List[float]], metadata: List[Dict[str, Any]] = None):
        """
        Uploads text chunks with their embeddings to Qdrant
        """
        if metadata is None:
            metadata = [{}] * len(texts)
        
        # Prepare points for upload
        points = []
        for i, (text, embedding, meta) in enumerate(zip(texts, embeddings, metadata)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": text,
                    "source": meta.get("source", "unknown"),
                    "chunk_id": meta.get("chunk_id", i),
                    **{k: v for k, v in meta.items() if k not in ["source", "chunk_id"]}  # Include other metadata
                }
            )
            points.append(point)
        
        # Upload points to collection
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return len(points)