import logging
from typing import Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime
import traceback
import asyncio
from functools import wraps


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AppException(HTTPException):
    """
    Custom application exception with additional logging
    """
    def __init__(self, status_code: int, detail: str, error_code: Optional[str] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        logger.error(f"AppException: {error_code or 'GENERIC_ERROR'} - {detail}")


class ValidationError(AppException):
    """Exception raised for validation errors"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )


class AuthenticationError(AppException):
    """Exception raised for authentication errors"""
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationError(AppException):
    """Exception raised for authorization errors"""
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTHORIZATION_ERROR"
        )


class NotFoundError(AppException):
    """Exception raised when a resource is not found"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND_ERROR"
        )


def log_exceptions(func):
    """
    Decorator to log exceptions in async functions
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    return wrapper


def log_function_call(func):
    """
    Decorator to log function calls with arguments and return values
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = await func(*args, **kwargs)
        logger.info(f"{func.__name__} returned {result}")
        return result
    return wrapper


class Logger:
    """
    Wrapper class for logging with context
    """
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def info(self, message: str, **kwargs):
        self.logger.info(f"{message} | context={kwargs}")

    def error(self, message: str, **kwargs):
        self.logger.error(f"{message} | context={kwargs}")

    def warning(self, message: str, **kwargs):
        self.logger.warning(f"{message} | context={kwargs}")

    def debug(self, message: str, **kwargs):
        self.logger.debug(f"{message} | context={kwargs}")


# Create a global logger instance
app_logger = Logger(__name__)