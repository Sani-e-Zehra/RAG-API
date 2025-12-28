# Quickstart Guide: AI-Native Unified Book + RAG Chatbot Platform

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- Git
- Access to OpenAI API (for embeddings and AI features)
- Access to Anthropic API (for Claude Subagents, if using)
- PostgreSQL database (or Neon Postgres account)
- Qdrant Cloud account

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-native-textbook
```

### 2. Install Dependencies

Install dependencies for each component:

```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Book frontend dependencies
cd ../book
npm install

# Root level (if needed)
cd ..
```

### 3. Environment Configuration

Create `.env` files in the appropriate directories with the following variables:

**Backend (.env file in backend/):**
```env
DATABASE_URL="postgresql://username:password@host:port/dbname"
OPENAI_API_KEY="your-openai-api-key"
QDRANT_URL="your-qdrant-url"
QDRANT_API_KEY="your-qdrant-api-key"
NEON_DB_URL="your-neon-db-url"
BETTER_AUTH_SECRET="your-better-auth-secret"
BETTER_AUTH_URL="http://localhost:3000"
```

**Book Frontend (.env file in book/):**
```env
REACT_APP_API_BASE_URL="http://localhost:8000" # or your backend URL
REACT_APP_BETTER_AUTH_URL="http://localhost:3000" # or your auth URL
```

### 4. Database Setup

#### Setup Neon Postgres:

1. Create a Neon account and project
2. Get your connection string
3. Update your backend `.env` file with the Neon connection string
4. Run database migrations:

```bash
cd backend
python -m pip install alembic  # if not already installed
alembic upgrade head
```

#### Setup Qdrant Cloud:

1. Create a Qdrant Cloud account
2. Create a collection for book vectors with the appropriate dimensions
3. Update your environment variables with Qdrant credentials

### 5. Run the Application

#### Development Mode:

1. Start the backend:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

2. Start the book frontend:
```bash
cd book
npm run start
```

3. The application should now be accessible at `http://localhost:3000`

#### Production Mode:

1. Build the book frontend:
```bash
cd book
npm run build
```

2. Serve the book frontend (typically deployed to GitHub Pages per project requirements)

3. Deploy the backend to a cloud platform (Render, Fly.io, etc.)

### 6. Initial Content Ingestion

To populate the book with content:

1. Add your book Markdown files to the `book/docs` directory
2. Run the ingestion pipeline:

```bash
cd pipelines
python uploader.py
```

This will chunk the content, generate embeddings, and upload them to Qdrant.

### 7. API Documentation

The backend API follows REST principles and has automatic documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 8. Testing

Run tests for each component:

**Backend tests:**
```bash
cd backend
python -m pytest
```

**Frontend tests:**
```bash
cd book
npm run test
```

## Key Endpoints

- `POST /auth/signup` - Create new user
- `POST /auth/signin` - User login
- `GET/PUT /user/preferences` - Manage user preferences
- `POST /rag/query` - Ask questions about the book
- `POST /rag/highlight-query` - Ask about selected text
- `POST /translate/urdu` - Translate content to Urdu
- `POST /skills/glossary` - Generate glossary
- `POST /skills/summarize` - Generate summary
- `POST /skills/tutor` - Interact with tutor

## Troubleshooting

1. **Database Connection Issues:**
   - Verify your Neon Postgres connection string
   - Ensure you've run the migrations

2. **Qdrant Connection Issues:**
   - Verify your Qdrant URL and API key
   - Check that your collection exists with the correct schema

3. **API Keys Not Working:**
   - Verify your OpenAI and other API keys are valid and have sufficient quota
   - Ensure environment variables are correctly set

4. **Frontend-Backend Communication:**
   - Check that CORS settings allow communication between frontend and backend
   - Verify that the backend is running and accessible from the frontend