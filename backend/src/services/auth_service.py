"""
Better-Auth implementation for the AI-Native Book + RAG Chatbot Platform
"""
from fastapi import Request, Response, HTTPException, status
from typing import Optional
from ..utils.config import settings
from ..utils.auth import create_access_token, create_refresh_token, verify_token
from ..services.user_service import UserService
from jose import JWTError


class BetterAuth:
    """
    BetterAuth implementation for handling authentication/authorization
    """
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    async def sign_up(self, email: str, password: str, first_name: Optional[str] = None, last_name: Optional[str] = None):
        """
        Create a new user account
        """
        from ..models.user_models import UserCreate
        
        user_create = UserCreate(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create the new user
        user = await self.user_service.create_user(user_create)
        
        # Create access and refresh tokens
        access_token = create_access_token(data={"sub": str(user.user_id), "email": user.email})
        refresh_token = create_refresh_token(data={"sub": str(user.user_id), "email": user.email})
        
        return {
            "user": user,
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        }
    
    async def sign_in(self, email: str, password: str):
        """
        Authenticate user and return session tokens
        """
        user = await self.user_service.authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create access and refresh tokens
        access_token = create_access_token(data={"sub": str(user.user_id), "email": user.email})
        refresh_token = create_refresh_token(data={"sub": str(user.user_id), "email": user.email})
        
        return {
            "user": user,
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        }
    
    async def sign_out(self, token: str):
        """
        Sign out user (invalidate session)
        """
        # In a real implementation, we would add the token to a blacklist
        # For now, we just return a success response
        return {"message": "Successfully signed out"}
    
    async def get_user_from_token(self, token: str):
        """
        Get user information from a JWT token
        """
        try:
            payload = verify_token(token)
            user_id = payload.get("sub")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            
            user = await self.user_service.get_user(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            
            return user
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
    
    async def update_user_profile(self, user_id: str, profile_data: dict):
        """
        Update user profile information
        """
        # In a real implementation, we'd have more specific methods for profile updates
        # For now, this is a placeholder
        pass