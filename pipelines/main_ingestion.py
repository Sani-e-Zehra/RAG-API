# Main ingestion script that ties together chunker, embedder, and uploader

import asyncio
import os
from typing import List, Dict, Any
from pathlib import Path

# Add the project root to the Python path so we can import from pipelines
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pipelines.chunker import TextChunker
from pipelines.embedder import Embedder
from pipelines.uploader import Uploader


class IngestionPipeline:
    """
    Main class to manage the ingestion pipeline: chunking, embedding, and uploading
    """
    
    def __init__(self, openai_api_key: str, qdrant_url: str, qdrant_api_key: str, collection_name: str = None):
        import os
        self.chunker = TextChunker()
        self.embedder = Embedder(api_key=openai_api_key)
        # Use provided collection name or default from env
        collection = collection_name or os.getenv("QDRANT_COLLECTION_NAME", "book_vectors")
        self.uploader = Uploader(qdrant_url=qdrant_url, qdrant_api_key=qdrant_api_key, collection_name=collection)

    async def process_document(self, content: str, source: str = "unknown", doc_id: str = None) -> int:
        """
        Process a single document through the entire pipeline
        """
        # Step 1: Chunk the text
        chunks = self.chunker.chunk_text(content)
        
        # Step 2: Generate embeddings for chunks
        embeddings = await self.embedder.generate_embeddings(chunks)
        
        # Step 3: Prepare metadata for each chunk
        metadata = []
        for i, chunk in enumerate(chunks):
            meta = {
                "source": source,
                "chunk_id": i,
                "doc_id": doc_id or "unknown",
                "original_length": len(chunk),
            }
            metadata.append(meta)
        
        # Step 4: Upload to vector DB
        uploaded_count = self.uploader.upload_chunks(chunks, embeddings, metadata)
        
        return uploaded_count

    async def process_document_file(self, file_path: str, source: str = None) -> int:
        """
        Process a document file through the entire pipeline
        """
        if source is None:
            source = Path(file_path).name
            
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        doc_id = Path(file_path).stem  # Use filename without extension as doc ID
        return await self.process_document(content, source, doc_id)

    async def process_multiple_documents(self, file_paths: List[str]) -> Dict[str, int]:
        """
        Process multiple documents and return results
        """
        results = {}
        for file_path in file_paths:
            try:
                count = await self.process_document_file(file_path)
                results[file_path] = count
                print(f"Successfully processed {file_path}: uploaded {count} vectors")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                results[file_path] = 0
        
        return results


# Example usage
async def main():
    # These would typically come from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", "")
    
    if not openai_api_key:
        print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return
    
    pipeline = IngestionPipeline(
        openai_api_key=openai_api_key,
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key
    )
    
    # Example of processing a single piece of content
    sample_content = """
    AI-native systems are designed with artificial intelligence as a fundamental component from the ground up. 
    Unlike traditional systems where AI is added as an afterthought, AI-native systems are architected to 
    leverage AI capabilities at their core, enabling more sophisticated and adaptive functionality.
    
    Key characteristics of AI-native systems include:
    - Intelligence at the core: AI is not an add-on but a foundational element
    - Adaptive behavior: The system learns and evolves based on data and interactions
    - Natural interfaces: Interaction through natural language, computer vision, etc.
    - Continuous learning: Ongoing model updates and improvements
    """
    
    uploaded_count = await pipeline.process_document(
        content=sample_content,
        source="example_content"
    )
    
    print(f"Uploaded {uploaded_count} vectors to Qdrant")


if __name__ == "__main__":
    asyncio.run(main())