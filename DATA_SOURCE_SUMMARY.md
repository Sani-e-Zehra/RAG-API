# Data Source Summary

## Primary Data Source: GitHub Repository

The **primary source** of book content is the GitHub repository:
- **Repository**: [Sani-e-Zehra/ai-native-book](https://github.com/Sani-e-Zehra/ai-native-book)
- **Path**: `docs/` directory in the `main` branch
- **Content**: Markdown files containing book chapters

The system automatically fetches all `.md` files from the GitHub repository's `docs` directory on startup.

## Fallback Data Sources

If GitHub is unavailable, the system will try:

1. **PostgreSQL `book_content` Table** - Database table with book chapters:

### Table Structure:
- `content_id` (UUID) - Primary key
- `title` (VARCHAR 500) - Chapter/section title
- `slug` (VARCHAR 500) - URL-friendly identifier
- `content` (TEXT) - The actual book content
- `content_type` (VARCHAR 50) - Type: "chapter", "section", or "appendix"
- `parent_id` (UUID) - For hierarchical structure
- `order_index` (INTEGER) - Display order

### Expected Content:
According to `IMPLEMENTATION_SUMMARY.md`, the book contains:
- **9 Chapters** on "Teaching Physical AI & Humanoid Robotics"
  1. Introduction to Physical AI & Humanoid Robotics
  2. Fundamentals of Physical AI
  3. Humanoid Robot Design Principles
  4. Motor Control Systems
  5. Sensor Fusion in Physical Systems
  6. Locomotion Algorithms
  7. AI for Physical Systems
  8. Control Theory Applications
  9. Case Studies & Applications

## Fallback Data Sources

If the PostgreSQL table is empty, the system will try:

1. **Markdown Files** in `book/docs/` directory
2. **Markdown Files** in project root (excluding README files)
3. **Sample Content** (hardcoded introduction chapter)

## Data Loading Flow

On backend startup, the `DataLoader` service:

1. ✅ Checks if Qdrant collection has vectors
2. ✅ If empty, loads from GitHub repository `docs/` directory (PRIMARY)
3. ✅ If GitHub fails, loads from PostgreSQL `book_content` table (FALLBACK 1)
4. ✅ If database is empty, loads from local markdown files (FALLBACK 2)
5. ✅ If no files found, loads sample content (LAST RESORT)
6. ✅ Processes content through ingestion pipeline:
   - Chunks text into smaller pieces
   - Generates embeddings using OpenAI
   - Uploads to Qdrant vector database

## How to Populate Data

### Option 1: GitHub Repository (Automatic - Current Setup)
The system automatically fetches content from:
- **Repository**: https://github.com/Sani-e-Zehra/ai-native-book
- **Path**: `docs/` directory
- **Branch**: `main`

Simply ensure the repository is public and contains markdown files in the `docs/` directory. The system will fetch them automatically on startup.

### Option 2: Populate PostgreSQL Database (Fallback)
Insert book content into the `book_content` table:

```sql
INSERT INTO book_content (title, slug, content, content_type, order_index)
VALUES 
  ('Introduction to Physical AI', 'intro-physical-ai', 'Content here...', 'chapter', 1),
  ('Fundamentals of Physical AI', 'fundamentals-physical-ai', 'Content here...', 'chapter', 2),
  -- ... more chapters
```

### Option 3: Use Local Markdown Files (Fallback)
Place markdown files in `book/docs/` directory. The system will automatically process them on startup if GitHub is unavailable.

### Option 4: Use API Endpoints
Use the book content API endpoints to create content programmatically.

## Current Implementation

The updated `data_loader.py` now:
- ✅ **Fetches content from GitHub repository** as the primary source
- ✅ Uses GitHub API to retrieve markdown files from `docs/` directory
- ✅ Falls back to PostgreSQL database if GitHub is unavailable
- ✅ Falls back to local markdown files if database is empty
- ✅ Loads sample content as last resort
- ✅ Processes all content through the ingestion pipeline
- ✅ Logs detailed information about what was loaded

## Next Steps

The system is now configured to automatically fetch content from GitHub:

1. ✅ **GitHub Repository**: Content is automatically fetched from https://github.com/Sani-e-Zehra/ai-native-book/tree/main/docs
2. ✅ **Automatic Processing**: All markdown files are processed and loaded into Qdrant on startup
3. ✅ **RAG Ready**: The RAG system will retrieve content from Qdrant based on semantic similarity to user questions

### To Update Content:
- Simply update the markdown files in the GitHub repository
- Restart the backend server to reload the content
- The system will automatically fetch and process the updated files

The RAG system will now retrieve content from Qdrant based on semantic similarity to user questions!

