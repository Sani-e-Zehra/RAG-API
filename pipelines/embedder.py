# Embedding generation for ingestion pipeline

from typing import List
import asyncio
from openai import OpenAI


class Embedder:
    """
    Generates embeddings for text chunks using OpenAI's embedding API
    """
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts
        """
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.embeddings.create(
                    input=texts,
                    model=self.model
                )
            )
            
            embeddings = [item.embedding for item in response.data]
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return [[] for _ in texts]  # Return empty embeddings in case of error

    def generate_embedding_sync(self, text: str) -> List[float]:
        """
        Synchronously generates embedding for a single text
        """
        try:
            response = self.client.embeddings.create(
                input=[text],
                model=self.model
            )
            
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []