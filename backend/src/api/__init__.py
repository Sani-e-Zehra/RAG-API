"""
API routing and middleware setup for the AI-Native Book + RAG Chatbot Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .rag_routes import router as rag_router
from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .translation_routes import router as translation_router
from .skill_routes import router as skill_router
from ..utils.config import settings
from ..utils.logging import app_logger


def setup_api_routes(app: FastAPI):
    """
    Set up all API routes for the application
    """
    # Include API routes with version prefix
    app.include_router(rag_router, prefix=settings.API_V1_STR)
    app.include_router(auth_router, prefix=settings.API_V1_STR)
    app.include_router(user_router, prefix=settings.API_V1_STR)
    app.include_router(translation_router, prefix=settings.API_V1_STR)
    app.include_router(skill_router, prefix=settings.API_V1_STR)


def setup_middleware(app: FastAPI):
    """
    Set up middleware for the application
    """
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS.split(",") if settings.BACKEND_CORS_ORIGINS != "*" else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    if settings.DEBUG:
        # In debug mode, allow all hosts
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    else:
        # In production, only allow the specified hosts
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=[settings.FRONTEND_URL.split("//")[1]])


def setup_exception_handlers(app: FastAPI):
    """
    Set up global exception handlers
    """
    @app.exception_handler(500)
    async def internal_exception_handler(request, exc):
        app_logger.error(f"Internal server error: {exc}", extra={"url": str(request.url)})
        return {"detail": "Internal server error"}
    
    @app.exception_handler(404)
    async def not_found_exception_handler(request, exc):
        app_logger.warning(f"Resource not found: {exc}", extra={"url": str(request.url)})
        return {"detail": "Resource not found"}


def initialize_app(app: FastAPI):
    """
    Initialize the FastAPI application with routes and middleware
    """
    setup_middleware(app)
    setup_api_routes(app)
    setup_exception_handlers(app)
    
    # Add health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": settings.VERSION}
        
    # Add root endpoint
    @app.get("/")
    async def root():
        return {"message": settings.PROJECT_NAME}
    
    return app