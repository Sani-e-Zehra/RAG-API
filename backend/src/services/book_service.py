from typing import List, Optional
from uuid import UUID
from ..models.content_models import BookContentCreate, BookContentUpdate, BookContentResponse
from ..utils.logging import log_function_call


class BookService:
    """
    Service class to manage book content operations
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, we'll use an in-memory store
        self.contents = {}
    
    @log_function_call
    async def create_content(self, content: BookContentCreate) -> BookContentResponse:
        """
        Creates a new book content item
        """
        from datetime import datetime
        from uuid import uuid4
        
        content_id = uuid4()
        now = datetime.now()
        
        content_response = BookContentResponse(
            content_id=content_id,
            title=content.title,
            slug=content.slug,
            content=content.content,
            content_type=content.content_type,
            parent_id=content.parent_id,
            order_index=content.order_index,
            created_at=now,
            updated_at=now
        )
        
        self.contents[content_id] = content_response
        return content_response
    
    @log_function_call
    async def get_content(self, content_id: UUID) -> Optional[BookContentResponse]:
        """
        Retrieves a book content item by its ID
        """
        return self.contents.get(content_id)
    
    @log_function_call
    async def get_content_by_slug(self, slug: str) -> Optional[BookContentResponse]:
        """
        Retrieves a book content item by its slug
        """
        for content in self.contents.values():
            if content.slug == slug:
                return content
        return None
    
    @log_function_call
    async def get_all_contents(self, content_type: Optional[str] = None) -> List[BookContentResponse]:
        """
        Retrieves all book content items, optionally filtered by content type
        """
        if content_type:
            return [content for content in self.contents.values() if content.content_type == content_type]
        return list(self.contents.values())
    
    @log_function_call
    async def update_content(self, content_id: UUID, content_update: BookContentUpdate) -> Optional[BookContentResponse]:
        """
        Updates a book content item
        """
        if content_id not in self.contents:
            return None
        
        existing_content = self.contents[content_id]
        update_data = content_update.dict(exclude_unset=True)
        
        # Create updated content
        updated_content = existing_content.copy(update=update_data)
        updated_content.updated_at = datetime.now()
        
        self.contents[content_id] = updated_content
        return updated_content
    
    @log_function_call
    async def delete_content(self, content_id: UUID) -> bool:
        """
        Deletes a book content item
        """
        if content_id in self.contents:
            del self.contents[content_id]
            return True
        return False