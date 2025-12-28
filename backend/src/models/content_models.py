from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class BookContentBase(BaseModel):
    title: str
    slug: str
    content: str
    content_type: str  # chapter, section, appendix
    parent_id: Optional[UUID] = None
    order_index: int


class BookContentCreate(BookContentBase):
    pass


class BookContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    order_index: Optional[int] = None


class BookContentResponse(BookContentBase):
    content_id: UUID
    created_at: datetime
    updated_at: datetime


class ChatSessionBase(BaseModel):
    user_id: Optional[UUID] = None


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    user_id: Optional[UUID] = None


class ChatSessionResponse(ChatSessionBase):
    session_id: UUID
    created_at: datetime
    updated_at: datetime


class ChatMessageBase(BaseModel):
    session_id: UUID
    sender_type: str  # 'user' or 'assistant'
    content: str
    context_reference: Optional[str] = None


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageUpdate(BaseModel):
    content: Optional[str] = None


class ChatMessageResponse(ChatMessageBase):
    message_id: UUID
    timestamp: datetime