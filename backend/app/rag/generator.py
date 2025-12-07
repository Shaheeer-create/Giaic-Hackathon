from typing import List, Dict, Any
from ..agents.tutor_agent import TutorAgent
from ..utils.exceptions import NoRelevantContentException
from ..utils.logging import get_logger

logger = get_logger(__name__)


class GenerationService:
    """
    Service for generating answers using the Tutor Agent.
    """
    
    def __init__(self):
        self.tutor_agent = TutorAgent()
    
    async def generate_answer(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        confidence_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate an answer based on the question and context chunks.
        
        Args:
            question: The question to answer
            context_chunks: List of context chunks to use for answer generation
            confidence_threshold: Minimum confidence score required for a valid answer
            
        Returns:
            Dictionary containing the generated answer and metadata
        """
        # Check if we have any context chunks
        if not context_chunks:
            logger.warning("No context chunks provided for answer generation")
            raise NoRelevantContentException(
                "No relevant content found to answer the question",
                "NO_RELEVANT_CONTENT"
            )
        
        # Generate the answer using the Tutor Agent
        try:
            result = await self.tutor_agent.generate_answer(
                question=question,
                context_chunks=context_chunks,
                confidence_threshold=confidence_threshold
            )
            
            # Validate that the answer is properly grounded in the context
            is_grounded = await self.tutor_agent.validate_answer_grounding(
                question=question,
                answer=result["answer"],
                context_chunks=context_chunks
            )
            
            if not is_grounded:
                logger.warning("Generated answer is not properly grounded in the provided context")
                # Return an error response instead
                raise NoRelevantContentException(
                    "Could not generate a properly grounded answer from the provided context",
                    "NO_GROUNDED_ANSWER"
                )
            
            logger.info(f"Successfully generated answer with confidence {result.get('confidence_score', 0)}")
            return result
            
        except NoRelevantContentException:
            # Re-raise NoRelevantContentException as-is
            raise
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise e  # Re-raise other exceptions