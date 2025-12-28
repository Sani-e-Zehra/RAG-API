import sys
import os
# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Go up 3 levels to project root
if project_root not in sys.path:
    sys.path.append(project_root)

from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api import initialize_app
from .utils.config import settings
from .utils.logging import app_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup: Load data into vector database if needed
    app_logger.info("Starting up application...")
    try:
        from .services.data_loader import ensure_data_loaded
        await ensure_data_loaded()
        app_logger.info("Startup data loading completed")
    except Exception as e:
        app_logger.error(f"Error during startup data loading: {e}", exc_info=True)
        # Don't fail startup if data loading fails
    
    yield
    
    # Shutdown: Cleanup if needed
    app_logger.info("Shutting down application...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan
    )

    # Initialize the app with routes, middleware, and exception handlers
    app = initialize_app(app)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True if settings.DEBUG else False
    )