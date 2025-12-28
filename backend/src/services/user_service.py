from typing import Optional
from uuid import UUID
from ..models.user_models import UserCreate, UserUpdate, UserResponse, UserProfileCreate, UserProfileUpdate, UserProfileResponse
from ..utils.logging import log_function_call
from datetime import datetime
from uuid import uuid4
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    Service class to manage user operations
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, we'll use an in-memory store
        self.users = {}
        self.profiles = {}
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against the hashed password
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """
        Generate a hash for the given password
        """
        return pwd_context.hash(password)
    
    @log_function_call
    async def create_user(self, user: UserCreate) -> UserResponse:
        """
        Creates a new user
        """
        from datetime import datetime
        from uuid import uuid4
        
        # Check if user with this email already exists
        for existing_user in self.users.values():
            if existing_user.email == user.email:
                raise ValueError("Email already registered")
        
        user_id = uuid4()
        now = datetime.now()
        
        # Hash the password
        password_hash = self.get_password_hash(user.password)
        
        user_response = UserResponse(
            user_id=user_id,
            email=user.email,
            created_at=now,
            updated_at=now,
            is_active=True,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Store the user with hashed password
        self.users[user_id] = {
            'user': user_response,
            'password_hash': password_hash
        }
        return user_response
    
    @log_function_call
    async def get_user(self, user_id: UUID) -> Optional[UserResponse]:
        """
        Retrieves a user by their ID
        """
        user_data = self.users.get(user_id)
        if user_data:
            return user_data['user']
        return None
    
    @log_function_call
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """
        Retrieves a user by their email
        """
        for user_data in self.users.values():
            if user_data['user'].email == email:
                return user_data['user']
        return None
    
    @log_function_call
    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> Optional[UserResponse]:
        """
        Updates a user
        """
        if user_id not in self.users:
            return None
        
        existing_user = self.users[user_id]['user']
        update_data = user_update.dict(exclude_unset=True)
        
        # Create updated user
        updated_user = existing_user.copy(update=update_data)
        updated_user.updated_at = datetime.now()
        
        # Update the stored user
        self.users[user_id]['user'] = updated_user
        return updated_user
    
    @log_function_call
    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """
        Authenticates a user with email and password
        """
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        user_data = self.users[user.user_id]
        if not self.verify_password(password, user_data['password_hash']):
            return None
        
        return user
    
    # Profile-related methods
    @log_function_call
    async def create_user_profile(self, profile: UserProfileCreate) -> UserProfileResponse:
        """
        Creates a profile for a user
        """
        # Check if user exists
        if profile.user_id not in self.users:
            raise ValueError("User does not exist")
        
        # Check if profile already exists for this user
        for existing_profile in self.profiles.values():
            if existing_profile.user_id == profile.user_id:
                raise ValueError("Profile already exists for this user")
        
        profile_id = uuid4()
        now = datetime.now()
        
        profile_response = UserProfileResponse(
            profile_id=profile_id,
            user_id=profile.user_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            technical_background=profile.technical_background,
            hardware_specs=profile.hardware_specs,
            language_preference=profile.language_preference,
            created_at=now,
            updated_at=now
        )
        
        self.profiles[profile_id] = profile_response
        return profile_response
    
    @log_function_call
    async def get_user_profile(self, user_id: UUID) -> Optional[UserProfileResponse]:
        """
        Retrieves a user's profile
        """
        for profile in self.profiles.values():
            if profile.user_id == user_id:
                return profile
        return None
    
    @log_function_call
    async def update_user_profile(self, user_id: UUID, profile_update: UserProfileUpdate) -> Optional[UserProfileResponse]:
        """
        Updates a user's profile
        """
        profile_to_update = None
        profile_id = None
        
        # Find the profile for this user
        for pid, profile in self.profiles.items():
            if profile.user_id == user_id:
                profile_to_update = profile
                profile_id = pid
                break
        
        if profile_to_update is None:
            return None
        
        update_data = profile_update.dict(exclude_unset=True)
        
        # Create updated profile
        updated_profile = profile_to_update.copy(update=update_data)
        updated_profile.updated_at = datetime.now()
        
        self.profiles[profile_id] = updated_profile
        return updated_profile