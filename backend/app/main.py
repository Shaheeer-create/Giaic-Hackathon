from datetime import datetime
from fastapi import FastAPI
from .api.routes import router as api_router
from .core.config import settings
from .utils.logging import get_logger
from .api.middleware import add_exception_middleware

# Configure logging
logger = get_logger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="RAG Textbook Tutor API",
    description="Backend API for Physical AI & Humanoid Robotics textbook tutor",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "query",
            "description": "Query the textbook content"
        },
        {
            "name": "ingest",
            "description": "Ingest textbook content for indexing"
        }
    ]
)

# Add middleware
add_exception_middleware(app)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Textbook Tutor API"}

@app.get("/health")
async def health_check():
    from .db.qdrant_client import qdrant_client_manager
    from .core.config import settings

    # Check Qdrant connection
    try:
        client = qdrant_client_manager.get_client()
        client.health()
        qdrant_status = "healthy"
    except Exception:
        qdrant_status = "unhealthy"

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "qdrant": qdrant_status,
            "config": settings.environment
        }
    }


# Initialize the application components
def initialize_app():
    """
    Initialize application components like database connections, etc.
    """
    logger.info("Initializing application components...")
    # Any initialization code can go here
    logger.info("Application components initialized successfully")


# Initialize the app when module is loaded
initialize_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.reload
    )