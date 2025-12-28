from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    technical_background: Optional[str] = None  # beginner, intermediate, advanced
    hardware_specs: Optional[str] = None  # low-end, mid-range, high-end
    language_preference: Optional[str] = None


class UserResponse(UserBase):
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    technical_background: Optional[str] = None
    hardware_specs: Optional[str] = None
    language_preference: Optional[str] = None


class UserProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    technical_background: Optional[str] = None  # beginner, intermediate, advanced
    hardware_specs: Optional[str] = None  # low-end, mid-range, high-end
    language_preference: Optional[str] = "en"


class UserProfileCreate(UserProfileBase):
    user_id: UUID


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    technical_background: Optional[str] = None
    hardware_specs: Optional[str] = None
    language_preference: Optional[str] = None


class UserProfileResponse(UserProfileBase):
    profile_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class PersonalizationPreferenceBase(BaseModel):
    user_id: UUID
    chapter_id: Optional[str] = None
    content_level: Optional[str] = None  # simplified, detailed, technical
    examples_preference: Optional[str] = None  # practical, theoretical


class PersonalizationPreferenceCreate(PersonalizationPreferenceBase):
    pass


class PersonalizationPreferenceUpdate(BaseModel):
    chapter_id: Optional[str] = None
    content_level: Optional[str] = None
    examples_preference: Optional[str] = None


class PersonalizationPreferenceResponse(PersonalizationPreferenceBase):
    pref_id: UUID
    created_at: datetime
    updated_at: datetime