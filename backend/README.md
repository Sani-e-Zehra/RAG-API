# Backend: AI-Native Book + RAG Chatbot Platform

This directory contains the backend implementation for the AI-Native Book + RAG Chatbot Platform.

## Overview

The backend is built with FastAPI and provides the following functionality:
- Authentication and user management
- RAG (Retrieval-Augmented Generation) services
- Content management
- Personalization features
- AI-powered tools

## Architecture

- **API Layer**: FastAPI routes in `/src/api/`
- **Service Layer**: Business logic in `/src/services/`
- **Model Layer**: Pydantic models in `/src/models/`
- **Utility Layer**: Configuration, logging, and helper functions in `/src/utils/`
- **Agent Layer**: AI agents in `/agents/`

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (for user data)
- Qdrant (for vector storage)
- OpenAI API key

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run database migrations:
```bash
alembic upgrade head
```

## Key Components

### Services
- `UserService`: Handles user registration, authentication, and profiles
- `BookService`: Manages book content
- `ChatService`: Handles chat sessions and messages
- `PersonalizationService`: Manages user preferences
- `TranslationService`: Handles content translation

### APIs
- `/auth/*`: Authentication endpoints
- `/rag/*`: RAG query endpoints
- `/user/*`: User management endpoints
- `/translate/*`: Translation endpoints
- `/skills/*`: AI skill endpoints

## Running the Server

```bash
uvicorn src.main:app --reload
```

The server will run on `http://localhost:8000` by default.

## Environment Variables

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `QDRANT_URL`: Qdrant connection URL
- `QDRANT_API_KEY`: Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection
- `OPENAI_API_KEY`: OpenAI API key
- `OPENAI_EMBEDDING_MODEL`: Model for generating embeddings (default: "text-embedding-3-small")
- `OPENAI_MODEL`: Model for text generation (default: "gpt-3.5-turbo")
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: Algorithm for JWT signing (default: "HS256")
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration time (default: 7)
- `FRONTEND_URL`: URL of the frontend (default: "http://localhost:3000")
- `BACKEND_CORS_ORIGINS`: Comma-separated list of allowed origins (default: "*")
- `DEBUG`: Enable debug mode (default: "False")