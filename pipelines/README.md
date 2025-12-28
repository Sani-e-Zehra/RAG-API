# Pipelines: AI-Native Book + RAG Chatbot Platform

This directory contains data processing pipelines for the platform.

## Overview

The ingestion pipeline handles processing book content for the RAG system:
- Text chunking
- Embedding generation
- Vector upload to Qdrant

## Components

### Chunker (`chunker.py`)
Responsible for breaking down large text documents into smaller, manageable chunks.

Features:
- Configurable chunk size
- Overlap between chunks to maintain context
- Sentence-aware chunking to preserve meaning

### Embedder (`embedder.py`)
Generates vector embeddings for text chunks using OpenAI's API.

Features:
- Asynchronous embedding generation
- Batch processing support
- Error handling for API failures

### Uploader (`uploader.py`)
Uploads embedded content to the Qdrant vector database.

Features:
- Vector storage in Qdrant
- Metadata attachment to vectors
- Batch upload capability

### Main Ingestion Script (`main_ingestion.py`)
Coordinates the entire ingestion process from document to vector database.

## Usage

### Processing a Document
```python
from pipelines.main_ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    openai_api_key="your-api-key",
    qdrant_url="your-qdrant-url",
    qdrant_api_key="your-qdrant-api-key"
)

# Process a single document
uploaded_count = await pipeline.process_document(
    content="Your document content here",
    source="document_source_name"
)
```

### Processing Multiple Documents
```python
# Process multiple documents
file_paths = ["doc1.txt", "doc2.txt", "doc3.txt"]
results = await pipeline.process_multiple_documents(file_paths)
```

## Configuration

The pipeline uses the following configuration:
- OpenAI API key for embedding generation
- Qdrant connection details for vector storage
- Chunk size and overlap settings

## Integration

The ingestion pipeline is typically used during:
- Initial content population
- Content updates
- Batch processing of new documents

It can be integrated into the backend via the content management services or run as a standalone script for bulk operations.