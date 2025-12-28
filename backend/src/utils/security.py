"""
Security utilities and middleware for the AI-Native Book + RAG Chatbot Platform
"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from ..utils.config import settings
import secrets


def verify_csrf_token(token: str, session_token: str) -> bool:
    """
    Verify CSRF token to prevent cross-site request forgery
    """
    # In a real implementation, we would compare the token with 
    # the one stored in the user's session
    return secrets.compare_digest(token, session_token)


def validate_input(input_str: str, max_length: int = 1000) -> str:
    """
    Validate and sanitize user input to prevent injection attacks
    """
    if not input_str:
        return input_str
        
    # Check length
    if len(input_str) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Input exceeds maximum length of {max_length} characters"
        )
    
    # Basic sanitization (in a real implementation, use a more comprehensive sanitizer)
    # Remove or escape potentially dangerous characters
    sanitized = input_str.replace('<script', '&lt;script').replace('javascript:', 'javascript-')
    
    return sanitized


def is_safe_url(url: str) -> bool:
    """
    Check if a URL is safe to redirect to (prevent open redirect vulnerabilities)
    """
    if not url or url.startswith('//') or url.startswith('http://') or url.startswith('https://'):
        return False
    
    # Check if the URL is relative
    if url.startswith('/') and not url.startswith('//'):
        return True
    
    return False


def validate_content_security(content: str) -> bool:
    """
    Validate content to ensure it doesn't contain malicious code
    """
    dangerous_patterns = [
        '<script',
        'javascript:',
        'vbscript:',
        '<iframe',
        '<object',
        '<embed',
        'onerror',
        'onload',
        'onmouseover'
    ]
    
    content_lower = content.lower()
    for pattern in dangerous_patterns:
        if pattern in content_lower:
            return False
    
    return True