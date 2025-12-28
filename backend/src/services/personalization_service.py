from typing import List, Optional
from uuid import UUID
from ..models.user_models import (
    PersonalizationPreferenceCreate, 
    PersonalizationPreferenceUpdate, 
    PersonalizationPreferenceResponse
)
from ..utils.logging import log_function_call
from datetime import datetime
from uuid import uuid4


class PersonalizationService:
    """
    Service class to manage personalization preferences
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, we'll use an in-memory store
        self.preferences = {}
    
    @log_function_call
    async def create_preference(self, preference: PersonalizationPreferenceCreate) -> PersonalizationPreferenceResponse:
        """
        Creates a new personalization preference
        """
        # Check if preference already exists for this user and chapter
        for existing_pref in self.preferences.values():
            if existing_pref.user_id == preference.user_id and existing_pref.chapter_id == preference.chapter_id:
                raise ValueError("Preference already exists for this user and chapter")
        
        pref_id = uuid4()
        now = datetime.now()
        
        preference_response = PersonalizationPreferenceResponse(
            pref_id=pref_id,
            user_id=preference.user_id,
            chapter_id=preference.chapter_id,
            content_level=preference.content_level,
            examples_preference=preference.examples_preference,
            created_at=now,
            updated_at=now
        )
        
        self.preferences[pref_id] = preference_response
        return preference_response
    
    @log_function_call
    async def get_preference(self, pref_id: UUID) -> Optional[PersonalizationPreferenceResponse]:
        """
        Retrieves a personalization preference by its ID
        """
        return self.preferences.get(pref_id)
    
    @log_function_call
    async def get_preference_by_user_and_chapter(self, user_id: UUID, chapter_id: Optional[str] = None) -> List[PersonalizationPreferenceResponse]:
        """
        Retrieves personalization preferences by user and optionally chapter
        """
        user_preferences = [
            pref for pref in self.preferences.values()
            if pref.user_id == user_id and (chapter_id is None or pref.chapter_id == chapter_id)
        ]
        return user_preferences
    
    @log_function_call
    async def get_user_preferences(self, user_id: UUID) -> List[PersonalizationPreferenceResponse]:
        """
        Retrieves all personalization preferences for a user
        """
        return self.get_preference_by_user_and_chapter(user_id)
    
    @log_function_call
    async def update_preference(self, pref_id: UUID, preference_update: PersonalizationPreferenceUpdate) -> Optional[PersonalizationPreferenceResponse]:
        """
        Updates a personalization preference
        """
        if pref_id not in self.preferences:
            return None
        
        existing_preference = self.preferences[pref_id]
        update_data = preference_update.dict(exclude_unset=True)
        
        # Create updated preference
        updated_preference = existing_preference.copy(update=update_data)
        updated_preference.updated_at = datetime.now()
        
        self.preferences[pref_id] = updated_preference
        return updated_preference
    
    @log_function_call
    async def delete_preference(self, pref_id: UUID) -> bool:
        """
        Deletes a personalization preference
        """
        if pref_id in self.preferences:
            del self.preferences[pref_id]
            return True
        return False