# Database: AI-Native Book + RAG Chatbot Platform

This directory contains database schema and migration files for the platform.

## Overview

The platform uses a hybrid approach:
- PostgreSQL for structured user and application data
- Qdrant for vector embeddings and semantic search

## PostgreSQL Schema

### Tables

#### `users`
- Stores user account information
- Contains email, password hash, and account status

#### `user_profiles`
- Stores extended user profile information
- Links to users table via foreign key
- Contains technical background, hardware specs, language preference

#### `personalization_preferences`
- Stores content personalization preferences
- Links to users table via foreign key
- Contains content level and examples preferences

#### `book_content`
- Stores the book content hierarchy
- Contains titles, content, and structural information

#### `chat_sessions`
- Stores chat session information
- Can be linked to users or anonymous

#### `chat_messages`
- Stores individual chat messages
- Links to chat_sessions via foreign key

## Migrations

Database migrations are handled using Alembic. The initial migration creates all necessary tables with appropriate constraints and indexes.

### Running Migrations

To apply all migrations to the database:
```bash
alembic upgrade head
```

To create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

## Qdrant Configuration

Qdrant is used for vector storage with the following characteristics:
- Collection name configured via environment variable
- Vector dimensions appropriate for the embedding model used
- Metadata storage for content source tracking

## Environment Configuration

The database connection is configured through the following environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `QDRANT_URL`: Qdrant connection URL
- `QDRANT_API_KEY`: Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection