from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from ..rag.retriever import RetrievalService
from ..rag.generator import GenerationService
from ..rag.ingestion import IngestionService
from ..utils.exceptions import handle_validation_error, handle_no_content_error
from ..utils.logging import get_logger
import uuid
from datetime import datetime

logger = get_logger(__name__)

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = None
    confidence_threshold: Optional[float] = 0.7

class IngestRequest(BaseModel):
    content: str
    title: str
    source_file: str
    section: Optional[str] = None
    page_number: Optional[int] = None
    metadata: Optional[dict] = None

class QueryResponse(BaseModel):
    answer: str
    confidence_score: float
    referenced_chunks: List[dict]
    query_id: str
    metadata: dict

class IngestResponse(BaseModel):
    status: str
    indexed_chunks: int
    content_id: str
    processing_time: str
    details: dict

@router.get("/test")
async def test_endpoint():
    return {"message": "API is working!"}

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Endpoint to query the textbook content and receive an AI-generated answer.
    """
    # Validate input
    if not request.question or len(request.question.strip()) < 3:
        raise handle_validation_error("Question must be at least 3 characters long")

    if request.confidence_threshold < 0 or request.confidence_threshold > 1:
        raise handle_validation_error("Confidence threshold must be between 0 and 1")

    query_id = str(uuid.uuid4())
    logger.info(f"Processing query {query_id} from user {request.user_id}: {request.question}")

    try:
        # Initialize services
        retrieval_service = RetrievalService()
        generation_service = GenerationService()

        # Retrieve relevant context for the question
        context_chunks = await retrieval_service.retrieve_context(
            query_text=request.question,
            top_k=5,
            similarity_threshold=request.confidence_threshold
        )

        # If no relevant context is found, refuse to answer
        if not context_chunks:
            logger.warning(f"No relevant context found for query {query_id}")
            raise handle_no_content_error("No relevant textbook content found to answer the question")

        # Generate an answer based on the retrieved context
        result = await generation_service.generate_answer(
            question=request.question,
            context_chunks=context_chunks,
            confidence_threshold=request.confidence_threshold
        )

        # Prepare response
        response = QueryResponse(
            answer=result["answer"],
            confidence_score=result["confidence_score"],
            referenced_chunks=result["referenced_chunks"],
            query_id=query_id,
            metadata={
                "processing_time": "TBD",  # Would be calculated in a real implementation
                "total_chunks_retrieved": len(context_chunks),
                "model_used": result.get("model_used", "unknown")
            }
        )

        logger.info(f"Successfully processed query {query_id}")
        return response

    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors and no content errors)
        raise
    except Exception as e:
        logger.error(f"Error processing query {query_id}: {str(e)}")
        raise handle_validation_error(f"Error processing query: {str(e)}")

@router.post("/ingest", response_model=IngestResponse)
async def ingest_endpoint(request: IngestRequest):
    """
    Endpoint to ingest textbook content for indexing in the RAG system.
    """
    # Validate input
    if not request.content or len(request.content.strip()) < 10:
        raise handle_validation_error("Content must be at least 10 characters long")

    if not request.title or len(request.title.strip()) < 1:
        raise handle_validation_error("Title is required")

    if not request.source_file or len(request.source_file.strip()) < 1:
        raise handle_validation_error("Source file is required")

    content_id = str(uuid.uuid4())
    logger.info(f"Starting ingestion for content ID {content_id}, source: {request.source_file}")

    try:
        # Initialize ingestion service
        ingestion_service = IngestionService()

        # Validate ingestion data
        is_valid = await ingestion_service.validate_ingestion_data(
            content=request.content,
            title=request.title,
            source_file=request.source_file
        )

        if not is_valid:
            raise handle_validation_error("Invalid ingestion data provided")

        # Ingest the content
        result = await ingestion_service.ingest_content(
            content=request.content,
            title=request.title,
            source_file=request.source_file,
            section=request.section,
            page_number=request.page_number,
            metadata=request.metadata
        )

        logger.info(f"Successfully ingested content {content_id}")
        return IngestResponse(
            status=result["status"],
            indexed_chunks=result["indexed_chunks"],
            content_id=result["content_id"],
            processing_time=result["processing_time"],
            details=result["details"]
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        logger.error(f"Error processing ingestion {content_id}: {str(e)}")
        raise handle_validation_error(f"Error processing ingestion: {str(e)}")