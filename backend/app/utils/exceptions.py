from typing import Optional
from fastapi import HTTPException, status


class RAGBaseException(Exception):
    """
    Base exception class for RAG system specific errors
    """
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ContentNotFoundException(RAGBaseException):
    """
    Raised when requested content is not found in the system
    """
    pass


class NoRelevantContentException(RAGBaseException):
    """
    Raised when no relevant content is found for a query
    """
    pass


class InvalidQueryException(RAGBaseException):
    """
    Raised when a query is invalid or doesn't meet requirements
    """
    pass


class IngestionException(RAGBaseException):
    """
    Raised when content ingestion fails
    """
    pass


class EmbeddingGenerationException(RAGBaseException):
    """
    Raised when embedding generation fails
    """
    pass


class DatabaseException(RAGBaseException):
    """
    Raised when database operations fail
    """
    pass


class ExternalServiceException(RAGBaseException):
    """
    Raised when external services (Qdrant, Gemini, etc.) are unavailable
    """
    pass


def create_http_exception(
    status_code: int,
    detail: str,
    error_code: Optional[str] = None
) -> HTTPException:
    """
    Create an HTTP exception with structured error details.
    
    Args:
        status_code: HTTP status code
        detail: Error detail message
        error_code: Optional application-specific error code
        
    Returns:
        HTTPException instance
    """
    error_detail = {
        "message": detail
    }
    
    if error_code:
        error_detail["error_code"] = error_code
    
    return HTTPException(
        status_code=status_code,
        detail=error_detail
    )


def handle_validation_error(detail: str) -> HTTPException:
    """
    Create a validation error HTTP exception.
    
    Args:
        detail: Validation error detail
        
    Returns:
        HTTPException instance with 400 status
    """
    return create_http_exception(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
        error_code="VALIDATION_ERROR"
    )


def handle_not_found_error(detail: str) -> HTTPException:
    """
    Create a not found error HTTP exception.
    
    Args:
        detail: Not found error detail
        
    Returns:
        HTTPException instance with 404 status
    """
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
        error_code="NOT_FOUND"
    )


def handle_internal_error(detail: str = "Internal server error") -> HTTPException:
    """
    Create an internal server error HTTP exception.
    
    Args:
        detail: Internal error detail (default: generic message)
        
    Returns:
        HTTPException instance with 500 status
    """
    return create_http_exception(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail,
        error_code="INTERNAL_ERROR"
    )


def handle_no_content_error(detail: str = "No relevant content found to answer the question") -> HTTPException:
    """
    Create a no content error HTTP exception for cases where no relevant content exists.
    
    Args:
        detail: No content error detail
        
    Returns:
        HTTPException instance with 404 status
    """
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
        error_code="NO_RELEVANT_CONTENT"
    )