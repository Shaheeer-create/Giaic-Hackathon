from typing import List, Dict, Any
import uuid
from datetime import datetime
from ..utils.chunking import chunk_content, DocumentChunk
from ..utils.text_cleaner import validate_content, normalize_content
from ..db.qdrant_client import qdrant_client_manager
from ..core.config import COHERE_CONFIG, QDRANT_CONFIG
from ..utils.exceptions import IngestionException, EmbeddingGenerationException
from ..utils.logging import get_logger
import cohere

logger = get_logger(__name__)


class IngestionService:
    """
    Service for ingesting textbook content into the RAG system.
    Handles content processing, chunking, embedding generation, and storage.
    """
    
    def __init__(self):
        api_key = COHERE_CONFIG["api_key"]
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")
        
        self.cohere_client = cohere.Client(api_key)
        self.qdrant_client = qdrant_client_manager.get_client()
        self.collection_name = QDRANT_CONFIG["collection_name"]
    
    async def ingest_content(
        self,
        content: str,
        title: str,
        source_file: str,
        section: str = None,
        page_number: int = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Ingest content into the RAG system.
        
        Args:
            content: The content to ingest
            title: Title of the content
            source_file: Original source file name
            section: Section identifier (optional)
            page_number: Page number (optional)
            metadata: Additional metadata (optional)
            
        Returns:
            Dictionary with ingestion results
        """
        # Validate the content
        if not validate_content(content):
            raise IngestionException(
                "Content does not meet minimum requirements",
                "INVALID_CONTENT"
            )
        
        if not title or not source_file:
            raise IngestionException(
                "Title and source_file are required fields",
                "MISSING_REQUIRED_FIELDS"
            )
        
        content_id = str(uuid.uuid4())
        logger.info(f"Starting ingestion for content ID {content_id}")
        
        try:
            # Normalize the content
            normalized_content = normalize_content(content)
            
            # Create metadata object
            content_metadata = {
                "title": title,
                "source_file": source_file,
                "section": section,
                "page_number": page_number,
                "created_at": datetime.utcnow().isoformat(),
                **(metadata or {})
            }
            
            # Chunk the content semantically
            chunks: List[DocumentChunk] = chunk_content(
                content=normalized_content,
                content_id=content_id,
                strategy="semantic"
            )
            
            logger.info(f"Content chunked into {len(chunks)} semantic chunks")
            
            # Prepare to store chunks in the database and vector store
            stored_chunk_count = 0
            processed_chunks = []
            
            # Process each chunk: generate embeddings and store in Qdrant
            for chunk in chunks:
                try:
                    # Generate embedding for the chunk using Cohere
                    response = self.cohere_client.embed(
                        texts=[chunk.text],
                        model=COHERE_CONFIG["model"]
                    )
                    
                    embedding_vector = response.embeddings[0]
                    
                    # Prepare payload for Qdrant
                    payload = {
                        "content_id": chunk.content_id,
                        "text": chunk.text,
                        "title": title,
                        "section": section or "",
                        "source_file": source_file,
                        "chunk_order": chunk.chunk_order,
                        "metadata": chunk.metadata or {},
                        "created_at": chunk.created_at or datetime.utcnow().isoformat()
                    }
                    
                    # Store in Qdrant vector database
                    self.qdrant_client.upsert(
                        collection_name=self.collection_name,
                        points=[
                            {
                                "id": chunk.id,
                                "vector": embedding_vector,
                                "payload": payload
                            }
                        ]
                    )
                    
                    processed_chunks.append({
                        "chunk_id": chunk.id,
                        "chunk_order": chunk.chunk_order,
                        "size": len(chunk.text)
                    })
                    
                    stored_chunk_count += 1
                    
                except Exception as e:
                    logger.error(f"Error processing chunk {chunk.id}: {str(e)}")
                    raise EmbeddingGenerationException(
                        f"Error processing chunk {chunk.id}: {str(e)}",
                        "CHUNK_PROCESSING_ERROR"
                    )
            
            logger.info(f"Successfully ingested {stored_chunk_count} chunks for content ID {content_id}")
            
            return {
                "status": "completed",
                "indexed_chunks": stored_chunk_count,
                "content_id": content_id,
                "processing_time": "TBD",  # Would be calculated in real implementation
                "details": {
                    "chunks_created": len(chunks),
                    "chunks_stored": {
                        "qdrant": stored_chunk_count,
                        # Note: In a real implementation, we would also store in PostgreSQL
                        "neon": 0  # Placeholder - would be actual count when DB integration is complete
                    }
                },
                "processed_chunks": processed_chunks
            }
            
        except IngestionException:
            # Re-raise ingestion exceptions
            raise
        except Exception as e:
            logger.error(f"Error during content ingestion: {str(e)}")
            raise IngestionException(
                f"Error during content ingestion: {str(e)}",
                "INGESTION_ERROR"
            )
    
    async def validate_ingestion_data(
        self,
        content: str,
        title: str,
        source_file: str
    ) -> bool:
        """
        Validate ingestion data before processing.
        
        Args:
            content: Content to validate
            title: Title to validate
            source_file: Source file to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        if not content or not title or not source_file:
            return False
        
        if len(content.strip()) < 10:  # Minimum content length
            return False
        
        if len(title.strip()) < 1:
            return False
        
        if len(source_file.strip()) < 1:
            return False
        
        return True