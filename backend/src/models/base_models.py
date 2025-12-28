from pydantic import BaseModel, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class BaseResponse(BaseModel):
    """Base response model with common fields"""
    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = datetime.now()


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    technical_background: Optional[str] = None
    hardware_specs: Optional[str] = None
    language_preference: Optional[str] = None


class UserResponse(UserBase):
    user_id: UUID4
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    technical_background: Optional[str] = None
    hardware_specs: Optional[str] = None
    language_preference: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PreferenceResponse(BaseModel):
    user_id: UUID4
    technical_background: Optional[str] = None
    hardware_specs: Optional[str] = None
    language_preference: Optional[str] = "en"
    content_level: Optional[str] = None
    examples_preference: Optional[str] = None
    updated_at: datetime


class PreferenceUpdate(BaseModel):
    technical_background: Optional[str] = None
    hardware_specs: Optional[str] = None
    language_preference: Optional[str] = None
    content_level: Optional[str] = None
    examples_preference: Optional[str] = None


class ChatMessageBase(BaseModel):
    sender_type: str  # 'user' or 'assistant'
    content: str
    context_reference: Optional[str] = None


class ChatMessageResponse(ChatMessageBase):
    message_id: UUID4
    session_id: UUID4
    timestamp: datetime


class ChatSessionResponse(BaseModel):
    session_id: UUID4
    user_id: Optional[UUID4] = None
    created_at: datetime
    updated_at: datetime


class RagQueryRequest(BaseModel):
    question: str
    context: Optional[str] = None


class RagQueryResponse(BaseModel):
    answer: str
    sources: List[str] = []
    confidence: float = 0.0


class HighlightQueryRequest(BaseModel):
    question: str
    selected_text: str
    context: Optional[str] = None


class TranslateRequest(BaseModel):
    content: str
    source_language: str = "en"
    target_language: str = "ur"


class TranslateResponse(BaseModel):
    translated_content: str
    source_language: str
    target_language: str


class SkillContentRequest(BaseModel):
    content: str
    context: Optional[str] = None


class GlossaryTerm(BaseModel):
    term: str
    definition: str


class GlossaryResponse(BaseModel):
    terms: List[GlossaryTerm]
    context: Optional[str] = None


class SummaryResponse(BaseModel):
    summary: str
    key_points: List[str]
    context: Optional[str] = None


class TutorRequest(BaseModel):
    question: str
    context: Optional[str] = None
    student_level: str = "intermediate"  # beginner, intermediate, advanced


class TutorResponse(BaseModel):
    explanation: str
    examples: List[str]
    followup_questions: List[str]