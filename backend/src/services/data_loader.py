"""
Service to load book content into Qdrant vector database on startup
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Dict
import logging
import httpx

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from backend.src.utils.config import settings
from backend.src.utils.qdrant import get_collection_count, get_qdrant_client
from pipelines.main_ingestion import IngestionPipeline
from pipelines.chunker import TextChunker
from pipelines.embedder import Embedder
from pipelines.uploader import Uploader

logger = logging.getLogger(__name__)

# GitHub repository configuration - using hardcoded raw URLs
GITHUB_REPO_OWNER = "Sani-e-Zehra"
GITHUB_REPO_NAME = "ai-native-book"
GITHUB_REPO_BRANCH = "main"
GITHUB_DOCS_PATH = "docs"
# Base URL for raw GitHub content (no API needed)
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/{GITHUB_REPO_BRANCH}/{GITHUB_DOCS_PATH}"


class DataLoader:
    """
    Service to check and load book content into Qdrant if needed
    """
    
    def __init__(self):
        self.pipeline = None
        self._initialize_pipeline()
    
    def _initialize_pipeline(self):
        """Initialize the ingestion pipeline"""
        try:
            if not settings.OPENAI_API_KEY:
                logger.warning("OpenAI API key not configured, data loading will be skipped")
                return
            
            if not settings.QDRANT_URL:
                logger.warning("Qdrant URL not configured, data loading will be skipped")
                return
            
            # Initialize pipeline with proper collection name
            self.pipeline = IngestionPipeline(
                openai_api_key=settings.OPENAI_API_KEY,
                qdrant_url=settings.QDRANT_URL,
                qdrant_api_key=settings.QDRANT_API_KEY or "",
                collection_name=settings.QDRANT_COLLECTION_NAME
            )
            
            logger.info(f"Data loader pipeline initialized with collection: {settings.QDRANT_COLLECTION_NAME}")
        except Exception as e:
            logger.error(f"Failed to initialize data loader pipeline: {e}", exc_info=True)
            # Don't fail completely - allow the app to start even if pipeline init fails
    
    async def check_and_load_data(self) -> bool:
        """
        Check if Qdrant collection has data, and load if empty
        
        Returns:
            True if data exists or was successfully loaded, False otherwise
        """
        try:
            # Check collection count
            count = get_collection_count()
            logger.info(f"Current vector count in collection: {count}")
            
            if count > 0:
                logger.info(f"Vector database already has {count} vectors, skipping data load")
                return True
            
            logger.info("Vector database is empty, attempting to load book content...")
            
            # Try to find and load book content
            loaded = await self._load_book_content()
            
            if loaded:
                new_count = get_collection_count()
                logger.info(f"Successfully loaded data. New vector count: {new_count}")
                return True
            else:
                logger.warning("No book content found to load. Vector database remains empty.")
                return False
                
        except Exception as e:
            logger.error(f"Error checking/loading data: {e}", exc_info=True)
            return False
    
    async def _load_book_content(self) -> bool:
        """
        Load book content from GitHub repository first, then fallback to other sources
        
        Returns:
            True if content was loaded, False otherwise
        """
        if not self.pipeline:
            logger.warning("Pipeline not initialized, cannot load data")
            return False
        
        loaded_any = False
        
        # First, try loading from GitHub repository
        try:
            loaded_any = await self._load_from_github()
            if loaded_any:
                logger.info("Successfully loaded content from GitHub repository")
                return True
        except Exception as e:
            logger.warning(f"Could not load from GitHub: {e}. Trying database...")
        
        # Fallback: Try loading from PostgreSQL book_content table
        try:
            loaded_any = await self._load_from_database()
            if loaded_any:
                logger.info("Successfully loaded content from PostgreSQL database")
                return True
        except Exception as e:
            logger.warning(f"Could not load from database: {e}. Trying local markdown files...")
        
        # Fallback: Try loading from local markdown files
        try:
            loaded_any = await self._load_from_markdown_files()
            if loaded_any:
                logger.info("Successfully loaded content from local markdown files")
                return True
        except Exception as e:
            logger.warning(f"Could not load from local markdown files: {e}")
        
        # Last resort: Load sample content
        if not loaded_any:
            logger.info("No content found, loading sample content...")
            loaded_any = await self._load_sample_content()
        
        return loaded_any
    
    async def _load_from_github(self) -> bool:
        """
        Load book content from GitHub repository using hardcoded raw URLs
        No GitHub API integration needed - fetches directly from raw.githubusercontent.com
        
        Returns:
            True if content was loaded, False otherwise
        """
        try:
            logger.info(f"Fetching content from GitHub using raw URLs: {GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/{GITHUB_DOCS_PATH}")
            
            # Try to fetch common markdown files directly from raw URLs
            # This avoids any GitHub API calls
            common_files = self._get_expected_files()
            
            loaded_count = 0
            for file_name in common_files:
                try:
                    # Get file content directly from raw GitHub URL (no API needed!)
                    content = await self._get_github_file_content_raw(file_name)
                    
                    if content:
                        # Process the content
                        count = await self.pipeline.process_document(
                            content=content,
                            source=f"github/{file_name}",
                            doc_id=file_name
                        )
                        
                        if count > 0:
                            loaded_count += count
                            logger.info(f"Loaded {count} chunks from GitHub: {file_name}")
                except Exception as e:
                    # File might not exist, that's okay - just skip it
                    logger.debug(f"File {file_name} not found or error: {e}")
                    continue
            
            if loaded_count > 0:
                logger.info(f"Successfully loaded {loaded_count} total chunks from GitHub")
                return True
            else:
                logger.warning("No files could be loaded from GitHub repository")
                return False
            
        except Exception as e:
            logger.error(f"Error loading from GitHub: {e}", exc_info=True)
            return False
    
    def _get_expected_files(self) -> List[str]:
        """
        Get list of expected markdown files to fetch from GitHub
        Based on the actual file structure in the repository
        
        Returns:
            List of expected file names
        """
        # Known chapter files from the repository (as of latest commit)
        expected_files = [
            "chapter-1-introduction.md",
            "chapter-2-fundamentals.md",
            "chapter-3-design.md",
            "chapter-4-motor-control.md",
            "chapter-5-sensor-fusion.md",
            "chapter-6-locomotion.md",
            "chapter-7-ai-systems.md",
            "chapter-8-control-theory.md",
            "chapter-9-applications.md",
            "conclusion.md",
            "index.md",
            "intro.md",
        ]
        
        return expected_files
    
    async def _get_github_file_content_raw(self, file_name: str) -> Optional[str]:
        """
        Get content of a file directly from GitHub raw URL (no API needed)
        
        Uses raw.githubusercontent.com to fetch file content directly.
        Format: https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}/{file}
        Example: https://raw.githubusercontent.com/Sani-e-Zehra/ai-native-book/main/docs/chapter-1-introduction.md
        
        Args:
            file_name: Name of the file in the docs directory (e.g., "chapter-1-introduction.md")
        
        Returns:
            File content as string, or None if error
        """
        try:
            # Use raw.githubusercontent.com URL - no API needed!
            # Format: https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}/{file}
            raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/{GITHUB_REPO_BRANCH}/{GITHUB_DOCS_PATH}/{file_name}"
            
            logger.debug(f"Fetching from: {raw_url}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(raw_url)
                
                # If file doesn't exist, return None (don't treat as error)
                if response.status_code == 404:
                    logger.debug(f"File not found: {file_name}")
                    return None
                
                response.raise_for_status()
                content = response.text
                logger.info(f"Successfully fetched {file_name} ({len(content)} characters)")
                return content
                    
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                # File doesn't exist - that's okay, just return None
                logger.debug(f"File {file_name} not found (404)")
                return None
            logger.error(f"Error fetching raw file {file_name}: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error fetching GitHub file content {file_name}: {e}", exc_info=True)
            return None
    
    async def _load_from_database(self) -> bool:
        """
        Load book content from PostgreSQL book_content table
        
        Returns:
            True if content was loaded, False otherwise
        """
        try:
            from sqlalchemy import create_engine, text
            from sqlalchemy.orm import sessionmaker
            
            if not settings.DATABASE_URL:
                logger.warning("DATABASE_URL not configured, skipping database load")
                return False
            
            # Create database connection
            engine = create_engine(settings.DATABASE_URL)
            Session = sessionmaker(bind=engine)
            session = Session()
            
            try:
                # Query all book content
                result = session.execute(text("""
                    SELECT content_id, title, slug, content, content_type, order_index
                    FROM book_content
                    ORDER BY order_index, content_type
                """))
                
                rows = result.fetchall()
                
                if not rows:
                    logger.info("No content found in book_content table")
                    return False
                
                logger.info(f"Found {len(rows)} content items in database")
                
                # Process each content item
                loaded_count = 0
                for row in rows:
                    content_id, title, slug, content, content_type, order_index = row
                    
                    try:
                        # Combine title and content for better context
                        full_content = f"# {title}\n\n{content}"
                        
                        count = await self.pipeline.process_document(
                            content=full_content,
                            source=f"db/{slug}",
                            doc_id=str(content_id)
                        )
                        
                        if count > 0:
                            loaded_count += count
                            logger.info(f"Loaded {count} chunks from database: {title} ({slug})")
                    except Exception as e:
                        logger.error(f"Error processing content {slug}: {e}")
                
                return loaded_count > 0
                
            finally:
                session.close()
                engine.dispose()
                
        except Exception as e:
            logger.error(f"Error loading from database: {e}", exc_info=True)
            return False
    
    async def _load_from_markdown_files(self) -> bool:
        """
        Load book content from markdown files as fallback
        
        Returns:
            True if content was loaded, False otherwise
        """
        # Try multiple possible locations for book content
        possible_paths = [
            Path(project_root) / "book" / "docs",
            Path(project_root) / "docs",
            Path(project_root) / "content",
            Path(project_root) / "book" / "content",
        ]
        
        # Also check for markdown files in project root
        project_md_files = list(Path(project_root).glob("*.md"))
        
        loaded_any = False
        
        # Try loading from directory paths
        for docs_path in possible_paths:
            if docs_path.exists() and docs_path.is_dir():
                logger.info(f"Found book content directory: {docs_path}")
                md_files = list(docs_path.glob("*.md"))
                
                if md_files:
                    logger.info(f"Found {len(md_files)} markdown files in {docs_path}")
                    for md_file in md_files:
                        try:
                            count = await self.pipeline.process_document_file(
                                str(md_file),
                                source=f"book/{md_file.name}"
                            )
                            if count > 0:
                                loaded_any = True
                                logger.info(f"Loaded {count} chunks from {md_file.name}")
                        except Exception as e:
                            logger.error(f"Error loading {md_file}: {e}")
        
        # Try loading markdown files from project root (excluding README, etc.)
        exclude_files = {"README.md", "CONTEXT_MANAGEMENT_ANALYSIS.md", "IMPLEMENTATION_SUMMARY.md", "QWEN.md"}
        for md_file in project_md_files:
            if md_file.name not in exclude_files:
                try:
                    count = await self.pipeline.process_document_file(
                        str(md_file),
                        source=f"root/{md_file.name}"
                    )
                    if count > 0:
                        loaded_any = True
                        logger.info(f"Loaded {count} chunks from {md_file.name}")
                except Exception as e:
                    logger.error(f"Error loading {md_file}: {e}")
        
        return loaded_any
    
    async def _load_sample_content(self) -> bool:
        """
        Load sample content as last resort
        
        Returns:
            True if content was loaded, False otherwise
        """
        sample_content = self._get_sample_content()
        if sample_content:
            try:
                count = await self.pipeline.process_document(
                    content=sample_content,
                    source="sample-content",
                    doc_id="sample"
                )
                if count > 0:
                    logger.info(f"Loaded {count} chunks from sample content")
                    return True
            except Exception as e:
                logger.error(f"Error loading sample content: {e}")
        return False
    
    def _get_sample_content(self) -> str:
        """
        Get sample content to load if no files are found
        """
        return """
# Introduction to Physical AI & Humanoid Robotics

Physical AI represents the intersection of artificial intelligence and physical systems, 
enabling robots and autonomous systems to interact with the real world. Unlike purely 
software-based AI, Physical AI must account for real-world physics, uncertainty, and 
the complexities of physical interaction.

## Key Concepts

### Physical AI Fundamentals
Physical AI systems combine:
- Sensor perception and processing
- Real-time decision making
- Actuator control and manipulation
- Adaptation to physical constraints

### Humanoid Robotics
Humanoid robots are designed to mimic human form and function, enabling them to:
- Navigate human environments
- Use human tools and interfaces
- Interact naturally with people
- Perform tasks designed for human capabilities

## Applications

Physical AI and humanoid robotics have applications in:
- Manufacturing and industrial automation
- Healthcare and assistance
- Search and rescue operations
- Space exploration
- Education and research

## Challenges

Key challenges in Physical AI include:
- Real-time processing requirements
- Safety and reliability
- Energy efficiency
- Robustness to uncertainty
- Integration of multiple subsystems
"""


# Global instance
data_loader = DataLoader()


async def ensure_data_loaded() -> bool:
    """
    Ensure vector database has data, loading if necessary
    
    Returns:
        True if data exists or was loaded successfully
    """
    return await data_loader.check_and_load_data()

