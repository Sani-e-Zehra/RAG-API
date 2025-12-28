#!/usr/bin/env python3
"""
Script to delete and recreate the Qdrant collection with proper vector configuration
"""

import os
from pathlib import Path

# Add the project root to the Python path
import sys
project_root = Path(__file__).parent.parent  # Go up one more level to project root
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from src.utils.config import settings


def recreate_collection():
    # Get API keys from environment variables
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "content")
    
    if not qdrant_url:
        print("Error: QDRANT_URL environment variable not set")
        return
    
    if not qdrant_api_key:
        print("Error: QDRANT_API_KEY environment variable not set")
        return

    # Initialize the Qdrant client
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

    try:
        # Delete the existing collection
        print(f"Deleting existing collection: {collection_name}")
        client.delete_collection(collection_name)
        print(f"Collection {collection_name} deleted successfully")
    except Exception as e:
        print(f"Collection {collection_name} might not exist yet, creating new one. Error: {e}")

    try:
        # Create a new collection with the named vector
        print(f"Creating new collection: {collection_name}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config={"content": VectorParams(size=1536, distance=Distance.COSINE)}  # Named vector "content" for OpenAI embeddings
        )
        print(f"Collection {collection_name} created successfully with named vector 'content'")
    except Exception as e:
        print(f"Error creating collection: {e}")

    # Verify the collection exists with the correct configuration
    try:
        collection_info = client.get_collection(collection_name)
        print(f"Collection info: {collection_info}")
        print("Collection verification complete!")
    except Exception as e:
        print(f"Error verifying collection: {e}")


if __name__ == "__main__":
    recreate_collection()