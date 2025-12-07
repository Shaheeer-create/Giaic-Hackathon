from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from ..utils.exceptions import RAGBaseException
import traceback
import logging

logger = logging.getLogger(__name__)


async def exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for the application.
    
    Args:
        request: The incoming request
        exc: The exception that occurred
        
    Returns:
        JSONResponse with error details
    """
    if isinstance(exc, RAGBaseException):
        # Handle custom RAG exceptions
        logger.error(f"RAG Exception: {exc.message}, Error Code: {exc.error_code}")
        
        error_detail = {
            "error": {
                "code": exc.error_code or "RAG_ERROR",
                "message": exc.message
            }
        }
        
        return JSONResponse(
            status_code=400,
            content=error_detail
        )
    
    elif isinstance(exc, HTTPException):
        # Handle HTTP exceptions
        logger.error(f"HTTP Exception: {exc.detail}, Status: {exc.status_code}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": "HTTP_ERROR", "message": str(exc.detail)}}
        )
    
    else:
        # Handle unexpected exceptions
        logger.error(f"Unexpected error: {str(exc)}")
        logger.error(traceback.format_exc())
        
        error_detail = {
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred"
            }
        }
        
        return JSONResponse(
            status_code=500,
            content=error_detail
        )


def add_exception_middleware(app):
    """
    Add exception handling middleware to the FastAPI app.
    
    Args:
        app: The FastAPI application instance
    """
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return await exception_handler(request, exc)
    
    @app.exception_handler(RAGBaseException)
    async def rag_exception_handler(request: Request, exc: RAGBaseException):
        return await exception_handler(request, exc)
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return await exception_handler(request, exc)