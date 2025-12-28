# AI-Native Unified Book + RAG Chatbot Platform

Welcome to the AI-Native Unified Book + RAG Chatbot Platform! This repository contains a comprehensive system that combines an AI-generated book with an intelligent chatbot that can answer questions based on the book's content.

## Overview

This platform provides:
1. **AI-Generated Book**: A complete structured book about AI-native systems
2. **Integrated RAG Chatbot**: An intelligent chatbot that answers questions based on book content
3. **Personalization**: Content adapted based on user preferences and background
4. **Translation**: Content translation (with initial support for Urdu)
5. **AI-Powered Tools**: Glossary generation, chapter summarization, and personalized tutoring

## Architecture

The platform follows a monorepo structure:

- `book/` - Docusaurus-based frontend application
- `backend/` - FastAPI backend with AI integration
- `agents/` - AI agents for RAG and reasoning
- `skills/` - Specialized AI skills (glossary, summarizer, tutor)
- `db/` - Database schema and migrations
- `pipelines/` - Data processing pipelines
- `specs/` - Feature specifications and plans

## Status: Implementation Complete

This project has completed the implementation of all planned features as outlined in the specifications:

### ✅ Core Features Implemented
- **Book Platform**: Complete Docusaurus-based frontend with documentation structure
- **RAG Chatbot**: Full-text question answering with context retrieval from Qdrant vector store
- **User System**: Authentication, profiles, and preference management
- **Personalization**: Content adaptation based on user preferences and background
- **Translation**: Urdu translation with preservation of formatting and structure
- **AI Skills**: Glossary generation, summarization, and personalized tutoring
- **Performance**: Optimized for sub-1.5s query response times
- **Security**: JWT/session tokens, proper data storage in appropriate stores

### ✅ Technical Implementation
- **Backend Services**: Authentication, user management, book content, chat, and personalization services
- **AI Components**: RAG agent, reasoning agent, and specialized skills
- **Frontend Components**: Chatbot widget, personalization controls, translation controls, skills panel
- **Database**: PostgreSQL for structured data and Qdrant for vector embeddings
- **Ingestion Pipeline**: Chunking, embedding generation, and vector upload
- **API Endpoints**: Complete set of REST endpoints for all functionality
- **Documentation**: README files for all major components

### 📋 Tasks Completed
All planned tasks across all phases have been implemented:
- **Phase 1**: Setup (project structure, Docusaurus, FastAPI, agents, skills, etc.)
- **Phase 2**: Foundational (database schema, auth framework, API routing, models, etc.)
- **Phase 3**: User Story 1 (book reading and Q&A functionality)
- **Phase 4**: User Story 2 (personalization features)
- **Phase 5**: User Story 3 (translation functionality)
- **Phase 6**: User Story 4 (AI-powered tools)
- **Phase N**: Polishing (documentation, testing, performance optimization, security, etc.)

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Git
- Access to OpenAI API
- PostgreSQL database
- Qdrant Cloud account

## Running the Platform

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the server:
```bash
uvicorn src.main:app --reload
```

### Frontend Setup

1. Navigate to the book directory:
```bash
cd book
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## API Endpoints

The backend provides several API endpoints:

- `/auth/*` - Authentication (signup, signin)
- `/rag/*` - RAG functionality (query, highlight-query)
- `/user/preferences` - User preferences management
- `/translate/*` - Translation functionality
- `/skills/*` - AI skills (glossary, summarize, tutor)

## Environment Variables

The application requires several environment variables:

**Backend (.env file)**:
- `DATABASE_URL` - PostgreSQL connection string
- `QDRANT_URL` - Qdrant connection URL
- `QDRANT_API_KEY` - Qdrant API key
- `OPENAI_API_KEY` - OpenAI API key
- `SECRET_KEY` - JWT secret key

**Frontend (.env file)**:
- `REACT_APP_API_BASE_URL` - Backend API base URL
- `REACT_APP_BETTER_AUTH_URL` - Auth service URL

## Next Steps

With the core implementation complete, the platform is ready for:
- Integration and end-to-end testing
- Performance tuning and optimization
- User experience refinement
- Production deployment preparation
- Additional feature development as needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.