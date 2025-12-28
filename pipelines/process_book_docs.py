#!/usr/bin/env python3
"""
Script to process book documentation files and feed them to the vector database
"""

import asyncio
import os
from pathlib import Path

# Add the project root to the Python path
import sys
project_root = Path(__file__).parent.parent  # Go up one more level to project root
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from pipelines.main_ingestion import IngestionPipeline


async def process_book_docs():
    """
    Process all documentation files in the book/docs directory
    """
    # Get API keys from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return
    
    if not qdrant_url:
        print("Error: QDRANT_URL environment variable not set")
        return
    
    if not qdrant_api_key:
        print("Error: QDRANT_API_KEY environment variable not set")
        return

    # Initialize the ingestion pipeline
    pipeline = IngestionPipeline(
        openai_api_key=openai_api_key,
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key
    )

    # Path to the book docs directory
    docs_dir = Path("C:/AI Agentic/AI-native-textbook/book/docs")
    
    if not docs_dir.exists():
        print(f"Error: Documentation directory does not exist: {docs_dir}")
        return

    # Get all markdown files in the docs directory
    md_files = list(docs_dir.glob("*.md"))
    
    if not md_files:
        print(f"No markdown files found in {docs_dir}")
        return

    print(f"Found {len(md_files)} markdown files to process")
    
    # Process each markdown file
    for file_path in md_files:
        print(f"Processing {file_path.name}...")
        try:
            uploaded_count = await pipeline.process_document_file(
                file_path=str(file_path),
                source=f"book_docs/{file_path.name}"
            )
            print(f"  - Uploaded {uploaded_count} vectors to Qdrant")
        except Exception as e:
            print(f"  - Error processing {file_path.name}: {e}")

    print("Finished processing all documentation files")


if __name__ == "__main__":
    asyncio.run(process_book_docs())