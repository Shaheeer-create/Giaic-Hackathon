from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import cohere
import numpy as np
from ..db.qdrant_client import qdrant_client_manager
from ..core.config import COHERE_CONFIG, QDRANT_CONFIG, RAG_CONFIG
from ..utils.exceptions import ExternalServiceException
from ..utils.logging import get_logger
import uuid

logger = get_logger(__name__)


class RetrievalService:
    """
    Service for retrieving relevant context from the vector database.
    """

    def __init__(self):
        self.qdrant_client = qdrant_client_manager.get_client()
        self.collection_name = QDRANT_CONFIG["collection_name"]

        api_key = COHERE_CONFIG["api_key"]
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.cohere_client = cohere.Client(api_key)

    async def retrieve_context(
        self,
        query_text: str,
        top_k: int = 5,
        similarity_threshold: float = 0.7,
        include_metadata: bool = True,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context for the given query text.

        Args:
            query_text: The query text to find similar content for
            top_k: Number of top results to retrieve
            similarity_threshold: Minimum similarity score for results
            include_metadata: Whether to include metadata in results
            filters: Optional filters to apply to the search

        Returns:
            List of context chunks with similarity scores
        """
        try:
            # Generate embedding for the query text using Cohere
            response = self.cohere_client.embed(
                texts=[query_text],
                model=COHERE_CONFIG["model"]
            )

            query_embedding = response.embeddings[0]

            # Prepare filters for Qdrant
            qdrant_filters = None
            if filters:
                qdrant_filters = self._build_qdrant_filter(filters)

            # Search in Qdrant for similar vectors
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=similarity_threshold,
                query_filter=qdrant_filters
            )

            # Format results into context chunks
            context_chunks = []
            for i, result in enumerate(search_results):
                if result.score >= similarity_threshold:
                    context_chunk = {
                        "id": result.id,
                        "text": result.payload.get("text", ""),
                        "similarity_score": result.score,
                        "section": result.payload.get("section", ""),
                        "source_file": result.payload.get("source_file", ""),
                        "chunk_order": result.payload.get("chunk_order", 0),
                        "rank": i + 1
                    }

                    if include_metadata:
                        context_chunk["metadata"] = result.payload.get("metadata", {})

                    context_chunks.append(context_chunk)

            logger.info(f"Retrieved {len(context_chunks)} relevant chunks for query")
            return context_chunks

        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise ExternalServiceException(
                f"Error retrieving context from vector database: {str(e)}",
                "RETRIEVAL_ERROR"
            )

    async def retrieve_context_by_content_id(
        self,
        content_id: str,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all chunks associated with a specific content ID.

        Args:
            content_id: ID of the content to retrieve chunks for
            top_k: Maximum number of chunks to retrieve

        Returns:
            List of context chunks associated with the content ID
        """
        try:
            # Search in Qdrant for records with the content_id
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_filter=Filter(
                    must=[
                        FieldCondition(
                            key="content_id",
                            match=MatchValue(value=content_id)
                        )
                    ]
                ),
                limit=top_k
            )

            # Format results into context chunks
            context_chunks = []
            for i, result in enumerate(search_results):
                context_chunk = {
                    "id": result.id,
                    "text": result.payload.get("text", ""),
                    "similarity_score": result.score if hasattr(result, 'score') else 1.0,
                    "section": result.payload.get("section", ""),
                    "source_file": result.payload.get("source_file", ""),
                    "chunk_order": result.payload.get("chunk_order", 0),
                    "rank": i + 1,
                    "metadata": result.payload.get("metadata", {})
                }
                context_chunks.append(context_chunk)

            logger.info(f"Retrieved {len(context_chunks)} chunks for content ID {content_id}")
            return context_chunks

        except Exception as e:
            logger.error(f"Error retrieving context by content ID: {str(e)}")
            raise ExternalServiceException(
                f"Error retrieving content from vector database: {str(e)}",
                "RETRIEVAL_ERROR"
            )

    async def check_content_exists(self, content_id: str) -> bool:
        """
        Check if content with the given ID exists in the vector database.

        Args:
            content_id: ID of the content to check

        Returns:
            True if content exists, False otherwise
        """
        try:
            # Count points with the specified content_id
            count = self.qdrant_client.count(
                collection_name=self.collection_name,
                count_filter=Filter(
                    must=[
                        FieldCondition(
                            key="content_id",
                            match=MatchValue(value=content_id)
                        )
                    ]
                )
            )

            return count.count > 0
        except Exception as e:
            logger.error(f"Error checking content existence: {str(e)}")
            return False

    def _build_qdrant_filter(self, filters: Dict[str, Any]) -> Filter:
        """
        Build Qdrant filter from simple filter dictionary.

        Args:
            filters: Dictionary of field-value pairs to filter by

        Returns:
            Qdrant Filter object
        """
        conditions = []
        for field, value in filters.items():
            conditions.append(
                FieldCondition(
                    key=field,
                    match=MatchValue(value=value)
                )
            )
        return Filter(must=conditions) if conditions else None

    async def rerank_results(
        self,
        query_text: str,
        results: List[Dict[str, Any]],
        top_n: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank the retrieved results using Cohere's rerank functionality.

        Args:
            query_text: The original query text
            results: List of retrieved results to rerank
            top_n: Number of top results to return after reranking

        Returns:
            Reranked list of results
        """
        if not results:
            return []

        # Extract the text from results for reranking
        texts = [result["text"] for result in results]

        try:
            # Use Cohere's rerank functionality
            response = self.cohere_client.rerank(
                query=query_text,
                documents=texts,
                top_n=top_n or len(texts),
                model="rerank-english-v2.0"  # Using a suitable rerank model
            )

            # Map the reranked results back to our original format
            reranked_results = []
            for idx, item in enumerate(response.results):
                original_result = results[item.index]
                original_result["rerank_score"] = item.relevance_score
                original_result["rank"] = idx + 1  # Update rank based on reranking
                reranked_results.append(original_result)

            return reranked_results

        except Exception as e:
            logger.warning(f"Error during reranking, returning original order: {str(e)}")
            # If reranking fails, return original order with original scores
            for i, result in enumerate(results):
                result["rank"] = i + 1
            return results

    async def enhanced_retrieve_context(
        self,
        query_text: str,
        top_k: int = 5,
        similarity_threshold: float = 0.7,
        use_reranking: bool = True,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Enhanced retrieval with reranking and additional filtering options.

        Args:
            query_text: The query text to find similar content for
            top_k: Number of top results to retrieve
            similarity_threshold: Minimum similarity score for results
            use_reranking: Whether to apply reranking after initial retrieval
            filters: Optional filters to apply to the search

        Returns:
            List of context chunks with similarity scores, potentially reranked
        """
        # First, retrieve results using vector similarity
        results = await self.retrieve_context(
            query_text=query_text,
            top_k=top_k * 2,  # Retrieve more initially for reranking
            similarity_threshold=similarity_threshold * 0.8,  # Lower threshold initially
            include_metadata=True,
            filters=filters
        )

        if use_reranking and results:
            # Apply reranking to improve relevance
            results = await self.rerank_results(
                query_text=query_text,
                results=results,
                top_n=top_k
            )
        else:
            # If not reranking, just limit to top_k
            results = results[:top_k]

        # Apply final similarity threshold filtering
        results = [r for r in results if r["similarity_score"] >= similarity_threshold]

        logger.info(f"Enhanced retrieval returned {len(results)} results for query")
        return results