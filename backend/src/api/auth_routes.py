from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Optional
import os
from ..models.user_models import UserCreate, UserResponse
from ..models.base_models import TokenResponse
from ..services.user_service import UserService
from ..services.auth_service import BetterAuth
from ..utils.config import settings
from ..utils.logging import AppException


router = APIRouter(prefix="/auth", tags=["Authentication"])

# Security scheme for bearer token
security = HTTPBearer()


@router.post("/signup", response_model=TokenResponse)
async def signup(user: UserCreate, user_service: UserService = Depends(UserService)):
    """
    Create a new user account
    """
    try:
        better_auth = BetterAuth(user_service)
        result = await better_auth.sign_up(
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name
        )

        # Return tokens instead of just user
        return result["tokens"]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@router.post("/signin", response_model=TokenResponse)
async def signin(email: str, password: str, user_service: UserService = Depends(UserService)):
    """
    Authenticate user and return session token
    """
    try:
        better_auth = BetterAuth(user_service)
        result = await better_auth.sign_in(email, password)

        return result["tokens"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during authentication"
        )


@router.post("/signout")
async def signout(token: str = Depends(security)):
    """
    Sign out user (invalidate session)
    """
    # In a real implementation, we would add the token to a blacklist
    # For now, we just return a success response
    return {"message": "Successfully signed out"}