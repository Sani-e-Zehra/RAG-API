from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ..models.user_models import (
    UserProfileResponse,
    UserProfileUpdate,
    PersonalizationPreferenceResponse,
    PersonalizationPreferenceCreate,
    PersonalizationPreferenceUpdate
)
from ..models.base_models import PreferenceResponse, PreferenceUpdate
from ..services.user_service import UserService
from ..services.personalization_service import PersonalizationService
from ..utils.config import settings
from ..utils.logging import AppException


router = APIRouter(prefix="/user", tags=["User Preferences"])


@router.get("/preferences", response_model=PreferenceResponse)
async def get_user_preferences(
    user_service: UserService = Depends(UserService),
    personalization_service: PersonalizationService = Depends(PersonalizationService)
):
    """
    Retrieve the current user's preferences
    """
    # In a real implementation, we would get the user ID from the JWT token
    # For now, we'll use a placeholder
    user_id = "placeholder-user-id"  # This should come from the authenticated user
    
    try:
        # Get user profile
        profile = await user_service.get_user_profile(UUID(user_id))
        
        # Get user preferences
        preferences = await personalization_service.get_user_preferences(UUID(user_id))
        
        if not profile and not preferences:
            # If no profile exists yet, return defaults
            return PreferenceResponse(
                user_id=UUID(user_id),
                technical_background=None,
                hardware_specs=None,
                language_preference="en",
                content_level=None,
                examples_preference=None,
                updated_at=datetime.now()
            )
        
        # Return combined preferences
        content_level = None
        examples_preference = None
        
        if preferences:
            # Get the most recent preference
            latest_pref = preferences[-1]  # Most recent is the last one
            content_level = latest_pref.content_level
            examples_preference = latest_pref.examples_preference
        
        return PreferenceResponse(
            user_id=UUID(user_id),
            technical_background=profile.technical_background if profile else None,
            hardware_specs=profile.hardware_specs if profile else None,
            language_preference=profile.language_preference if profile else "en",
            content_level=content_level,
            examples_preference=examples_preference,
            updated_at=profile.updated_at if profile else datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user preferences"
        )


@router.put("/preferences", response_model=PreferenceResponse)
async def update_user_preferences(
    preferences_update: PreferenceUpdate,
    user_service: UserService = Depends(UserService),
    personalization_service: PersonalizationService = Depends(PersonalizationService)
):
    """
    Update the current user's preferences
    """
    # In a real implementation, we would get the user ID from the JWT token
    # For now, we'll use a placeholder
    user_id = "placeholder-user-id"  # This should come from the authenticated user
    
    try:
        # Update user profile if needed
        if any([preferences_update.technical_background, 
                preferences_update.hardware_specs, 
                preferences_update.language_preference]):
            profile_update = UserProfileUpdate(
                technical_background=preferences_update.technical_background,
                hardware_specs=preferences_update.hardware_specs,
                language_preference=preferences_update.language_preference
            )
            updated_profile = await user_service.update_user_profile(
                UUID(user_id), profile_update
            )
        
        # Create or update personalization preference
        pref_create = PersonalizationPreferenceCreate(
            user_id=UUID(user_id),
            content_level=preferences_update.content_level,
            examples_preference=preferences_update.examples_preference
        )
        
        # Check if a preference already exists for this user
        existing_prefs = await personalization_service.get_user_preferences(UUID(user_id))
        if existing_prefs:
            # Update the existing preference
            latest_pref = existing_prefs[-1]  # Most recent is the last one
            updated_pref = await personalization_service.update_preference(
                latest_pref.pref_id, 
                PersonalizationPreferenceUpdate(
                    content_level=preferences_update.content_level,
                    examples_preference=preferences_update.examples_preference
                )
            )
        else:
            # Create a new preference
            updated_pref = await personalization_service.create_preference(pref_create)
        
        # Return updated preferences
        profile = await user_service.get_user_profile(UUID(user_id))
        
        return PreferenceResponse(
            user_id=UUID(user_id),
            technical_background=profile.technical_background if profile else preferences_update.technical_background,
            hardware_specs=profile.hardware_specs if profile else preferences_update.hardware_specs,
            language_preference=profile.language_preference if profile else preferences_update.language_preference or "en",
            content_level=updated_pref.content_level,
            examples_preference=updated_pref.examples_preference,
            updated_at=updated_pref.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user preferences"
        )