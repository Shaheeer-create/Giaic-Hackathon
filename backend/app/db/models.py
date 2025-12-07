"""
Database models for the RAG Textbook Tutor application.

This module defines the SQLAlchemy models for all entities
required for the application based on the data-model.md specification.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Query(Base):
    """
    Model for storing user queries
    """
    __tablename__ = "queries"
    
    id = Column(String, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, index=True)  # Optional user identifier
    confidence_threshold = Column(Float, default=0.7)  # Default 70% confidence threshold


class TextbookContent(Base):
    """
    Model for storing textbook content sections
    """
    __tablename__ = "textbook_content"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    source_file = Column(String, nullable=False)
    page_number = Column(Integer)  # Optional
    section = Column(String)  # Optional
    metadata = Column(JSON)  # Additional metadata as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DocumentChunk(Base):
    """
    Model for storing semantic chunks of textbook content
    """
    __tablename__ = "document_chunks"
    
    id = Column(String, primary_key=True, index=True)
    content_id = Column(String, index=True)  # References TextbookContent.id
    text = Column(Text, nullable=False)
    chunk_order = Column(Integer, nullable=False)  # Position in original content
    semantic_boundary = Column(Integer, default=0)  # Boolean as integer: 0 or 1
    metadata = Column(JSON)  # Additional metadata as JSON
    created_at = Column(DateTime, default=datetime.utcnow)


class RetrievedContext(Base):
    """
    Model for storing retrieved context for a query
    """
    __tablename__ = "retrieved_context"
    
    id = Column(String, primary_key=True, index=True)
    query_id = Column(String, index=True)  # References Query.id
    chunk_id = Column(String, index=True)  # References DocumentChunk.id
    similarity_score = Column(Float)  # Similarity score (0-1)
    rank = Column(Integer, nullable=False)  # Position in relevance ranking
    retrieved_at = Column(DateTime, default=datetime.utcnow)


class GeneratedAnswer(Base):
    """
    Model for storing generated answers
    """
    __tablename__ = "generated_answers"
    
    id = Column(String, primary_key=True, index=True)
    query_id = Column(String, index=True)  # References Query.id
    retrieved_context_ids = Column(JSON)  # Array of retrieved context IDs
    answer_text = Column(Text, nullable=False)
    confidence_score = Column(Float)  # Confidence score (0-1)
    source_chunks = Column(JSON)  # Array of chunk IDs that informed the answer
    generated_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)  # Additional generation metadata


class Embedding(Base):
    """
    Model for storing embeddings
    """
    __tablename__ = "embeddings"
    
    id = Column(String, primary_key=True, index=True)
    chunk_id = Column(String, index=True)  # References DocumentChunk.id
    model_used = Column(String, nullable=False)  # Name of the embedding model
    created_at = Column(DateTime, default=datetime.utcnow)


class ConfidenceMetadata(Base):
    """
    Model for storing confidence metadata for answers
    """
    __tablename__ = "confidence_metadata"
    
    id = Column(String, primary_key=True, index=True)
    answer_id = Column(String, index=True)  # References GeneratedAnswer.id
    overall_confidence = Column(Float)  # Overall confidence (0-1)
    context_relevance = Column(Float)  # Context relevance (0-1)
    coverage_score = Column(Float)  # Coverage score (0-1)
    warning_flags = Column(JSON)  # Array of warning flags
    calculated_at = Column(DateTime, default=datetime.utcnow)