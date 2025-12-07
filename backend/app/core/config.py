"""
Configuration module for the RAG Textbook Tutor application.

This module defines the application's configuration settings
that are loaded from environment variables and .env files.
"""

from .settings import settings

# Application configuration constants
APP_NAME = "RAG Textbook Tutor"
VERSION = "0.1.0"
DEBUG = settings.environment.lower() == "development"

# External service configurations
GEMINI_CONFIG = {
    "api_key": settings.gemini_api_key,
    "model": "gemini-pro"  # Default model, can be overridden
}

COHERE_CONFIG = {
    "api_key": settings.cohere_api_key,
    "model": "embed-english-v3.0"  # Default embedding model
}

QDRANT_CONFIG = {
    "url": settings.qdrant_url,
    "api_key": settings.qdrant_api_key,
    "collection_name": "textbook_chunks"
}

NEON_CONFIG = {
    "database_url": settings.neon_database_url
}

# RAG pipeline configurations
RAG_CONFIG = {
    "max_chunks_to_retrieve": 5,
    "similarity_threshold": 0.7,  # 70% similarity threshold
    "max_query_processing_time": 10,  # 10 seconds max processing time
    "concurrent_query_limit": 200  # Support up to 200 concurrent queries
}

# Validation configurations
VALIDATION_CONFIG = {
    "min_question_length": 3,  # Minimum characters in a question
    "min_confidence_score": 0.5,  # Minimum confidence for valid answers
    "max_content_size": 1000000  # Maximum content size in bytes (1MB)
}