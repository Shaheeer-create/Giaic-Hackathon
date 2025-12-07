import cohere
from typing import List
from ..core.config import COHERE_CONFIG
from ..utils.exceptions import EmbeddingGenerationException
from ..utils.logging import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """
    Service for generating embeddings using Cohere.
    """
    
    def __init__(self):
        api_key = COHERE_CONFIG["api_key"]
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")
        
        self.cohere_client = cohere.Client(api_key)
        self.model = COHERE_CONFIG["model"]
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to generate embeddings for
            
        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        if not texts:
            raise EmbeddingGenerationException(
                "No texts provided for embedding generation",
                "NO_TEXTS_FOR_EMBEDDING"
            )
        
        try:
            response = self.cohere_client.embed(
                texts=texts,
                model=self.model
            )
            
            if not response or not response.embeddings:
                raise EmbeddingGenerationException(
                    "Cohere API returned empty embeddings",
                    "EMPTY_EMBEDDINGS"
                )
            
            return response.embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise EmbeddingGenerationException(
                f"Error generating embeddings: {str(e)}",
                "EMBEDDING_GENERATION_ERROR"
            )
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text string to generate embedding for
            
        Returns:
            Embedding vector (list of floats)
        """
        embeddings = await self.generate_embeddings([text])
        return embeddings[0] if embeddings else []
    
    async def validate_embedding_model(self) -> bool:
        """
        Validate that the embedding model is accessible.
        
        Returns:
            True if model is accessible, False otherwise
        """
        try:
            # Test with a simple text
            test_embedding = await self.generate_embedding("test")
            return len(test_embedding) > 0
        except:
            return False