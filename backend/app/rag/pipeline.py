from typing import Dict, Any, List
from ..rag.ingestion import IngestionService
from ..rag.retriever import RetrievalService
from ..rag.generator import GenerationService
from ..agents.tutor_agent import TutorAgent
from ..utils.exceptions import NoRelevantContentException
from ..utils.logging import get_logger

logger = get_logger(__name__)


class PipelineOrchestrator:
    """
    Orchestrates the complete RAG pipeline from ingestion to answer generation.
    """
    
    def __init__(self):
        self.ingestion_service = IngestionService()
        self.retrieval_service = RetrievalService()
        self.generation_service = GenerationService()
        self.tutor_agent = TutorAgent()
    
    async def process_query(
        self,
        question: str,
        user_id: str = None,
        confidence_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Process a query through the complete RAG pipeline.
        
        Args:
            question: The question to answer
            user_id: Optional user identifier
            confidence_threshold: Minimum confidence required for answer
            
        Returns:
            Dictionary containing the answer and metadata
        """
        logger.info(f"Starting RAG pipeline for query from user {user_id}: {question}")
        
        try:
            # Step 1: Retrieve relevant context
            context_chunks = await self.retrieval_service.retrieve_context(
                query_text=question,
                top_k=5,
                similarity_threshold=confidence_threshold
            )
            
            # Step 2: If no context found, return appropriate response
            if not context_chunks:
                logger.warning(f"No relevant context found for query: {question}")
                raise NoRelevantContentException(
                    "No relevant textbook content found to answer the question",
                    "NO_RELEVANT_CONTENT"
                )
            
            # Step 3: Generate answer based on context
            result = await self.generation_service.generate_answer(
                question=question,
                context_chunks=context_chunks,
                confidence_threshold=confidence_threshold
            )
            
            logger.info(f"RAG pipeline completed successfully for query: {question}")
            return result
            
        except NoRelevantContentException:
            # Re-raise the exception to be handled by the calling endpoint
            raise
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            raise e
    
    async def ingest_and_index(
        self,
        content: str,
        title: str,
        source_file: str,
        section: str = None,
        page_number: int = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Ingest content and index it in the RAG system.
        
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
        logger.info(f"Starting ingestion pipeline for: {title} from {source_file}")
        
        try:
            result = await self.ingestion_service.ingest_content(
                content=content,
                title=title,
                source_file=source_file,
                section=section,
                page_number=page_number,
                metadata=metadata
            )
            
            logger.info(f"Ingestion pipeline completed for: {title}")
            return result
            
        except Exception as e:
            logger.error(f"Error in ingestion pipeline: {str(e)}")
            raise e
    
    async def process_query_with_enhanced_retrieval(
        self,
        question: str,
        user_id: str = None,
        confidence_threshold: float = 0.7,
        use_reranking: bool = True
    ) -> Dict[str, Any]:
        """
        Process a query with enhanced retrieval capabilities.
        
        Args:
            question: The question to answer
            user_id: Optional user identifier
            confidence_threshold: Minimum confidence required for answer
            use_reranking: Whether to use reranking for better results
            
        Returns:
            Dictionary containing the answer and metadata
        """
        logger.info(f"Starting enhanced RAG pipeline for query: {question}")
        
        try:
            # Step 1: Retrieve relevant context with enhanced capabilities
            context_chunks = await self.retrieval_service.enhanced_retrieve_context(
                query_text=question,
                top_k=5,
                similarity_threshold=confidence_threshold,
                use_reranking=use_reranking
            )
            
            # Step 2: If no context found, return appropriate response
            if not context_chunks:
                logger.warning(f"No relevant context found for query: {question}")
                raise NoRelevantContentException(
                    "No relevant textbook content found to answer the question",
                    "NO_RELEVANT_CONTENT"
                )
            
            # Step 3: Generate answer based on context
            result = await self.generation_service.generate_answer(
                question=question,
                context_chunks=context_chunks,
                confidence_threshold=confidence_threshold
            )
            
            logger.info(f"Enhanced RAG pipeline completed for query: {question}")
            return result
            
        except NoRelevantContentException:
            # Re-raise the exception to be handled by the calling endpoint
            raise
        except Exception as e:
            logger.error(f"Error in enhanced RAG pipeline: {str(e)}")
            raise e