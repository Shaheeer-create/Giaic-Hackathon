import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from ..core.config import GEMINI_CONFIG
from ..utils.exceptions import ExternalServiceException
from ..utils.logging import get_logger
from .tools import AgentTools

logger = get_logger(__name__)

class TutorAgent:
    """
    Agent that orchestrates the RAG process using Gemini models.
    Handles query processing, context injection, and answer generation.
    """

    def __init__(self):
        api_key = GEMINI_CONFIG["api_key"]
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GEMINI_CONFIG["model"])
        self.tools = AgentTools()

    async def generate_answer(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        confidence_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate an answer based on the question and retrieved context.

        Args:
            question: The user's question
            context_chunks: List of context chunks retrieved from the knowledge base
            confidence_threshold: Minimum confidence required for a valid answer

        Returns:
            Dictionary containing the answer and metadata
        """
        if not context_chunks:
            raise ExternalServiceException(
                "No relevant context provided for answer generation",
                "NO_CONTEXT_PROVIDED"
            )

        # Construct the prompt with context
        context_text = self._format_context(context_chunks)
        prompt = self._construct_prompt(question, context_text)

        try:
            # Generate content using Gemini
            response = await self.model.generate_content_async(prompt)

            if not response or not response.text:
                raise ExternalServiceException(
                    "Gemini model did not return a valid response",
                    "INVALID_MODEL_RESPONSE"
                )

            answer_text = response.text.strip()

            # Calculate a confidence score based on how well the response addresses the question
            confidence_score = self._calculate_confidence_score(
                question, answer_text, context_chunks
            )

            # Check if the confidence score meets the threshold
            if confidence_score < confidence_threshold:
                logger.warning(
                    f"Generated answer confidence ({confidence_score}) below threshold ({confidence_threshold})"
                )
                return {
                    "answer": "I couldn't find sufficient relevant information to answer your question.",
                    "confidence_score": confidence_score,
                    "referenced_chunks": [],
                    "model_used": GEMINI_CONFIG["model"],
                    "warning": f"Confidence score {confidence_score} is below the required threshold of {confidence_threshold}"
                }

            # Get the chunk IDs that were used to generate the answer
            referenced_chunk_ids = [chunk["id"] for chunk in context_chunks]

            return {
                "answer": answer_text,
                "confidence_score": confidence_score,
                "referenced_chunks": [
                    {
                        "chunk_id": chunk["id"],
                        "content_preview": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"],
                        "similarity_score": chunk.get("similarity_score", 0.0),
                        "section": chunk.get("section", "")
                    }
                    for chunk in context_chunks
                ],
                "model_used": GEMINI_CONFIG["model"],
                "confidence_score": confidence_score
            }

        except Exception as e:
            logger.error(f"Error generating answer with Gemini: {str(e)}")
            raise ExternalServiceException(
                f"Error communicating with Gemini API: {str(e)}",
                "GEMINI_API_ERROR"
            )

    def _construct_prompt(self, question: str, context: str) -> str:
        """
        Construct the prompt for the Gemini model.

        Args:
            question: The user's question
            context: Formatted context to provide to the model

        Returns:
            Formatted prompt string
        """
        return f"""
        You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
        Answer the user's question based ONLY on the provided context.
        Do not use any external knowledge.
        If the context does not contain information to answer the question,
        clearly state that you don't have enough information.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

    def _format_context(self, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Format the context chunks into a string for the prompt.

        Args:
            context_chunks: List of context chunks retrieved from the knowledge base

        Returns:
            Formatted context string
        """
        formatted_contexts = []
        for chunk in context_chunks:
            chunk_text = chunk["text"].strip()
            if chunk_text:
                formatted_contexts.append(chunk_text)

        return "\n\n".join(formatted_contexts)

    def _calculate_confidence_score(
        self,
        question: str,
        answer: str,
        context_chunks: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate a basic confidence score based on relevance measures.

        Args:
            question: The original question
            answer: The generated answer
            context_chunks: The context chunks used to generate the answer

        Returns:
            Confidence score between 0 and 1
        """
        # This is a simplified confidence calculation
        # In a real implementation, you'd want more sophisticated measures

        # Ensure the answer is relevant to the question
        question_lower = question.lower()
        answer_lower = answer.lower()

        # Check if answer contains relevant terms from the question
        question_terms = set(question_lower.split())
        answer_terms = set(answer_lower.split())
        common_terms = question_terms.intersection(answer_terms)

        # Calculate score based on term overlap and context utilization
        term_overlap_score = len(common_terms) / len(question_terms) if question_terms else 0

        # Consider the number of context chunks used (more chunks = higher confidence)
        chunk_utilization_score = min(len(context_chunks) / 5.0, 1.0)  # Cap at 1.0

        # Combine scores (this is a simplified approach)
        confidence_score = (term_overlap_score * 0.6) + (chunk_utilization_score * 0.4)

        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, confidence_score))

    async def validate_answer_grounding(
        self,
        question: str,
        answer: str,
        context_chunks: List[Dict[str, Any]]
    ) -> bool:
        """
        Validate that the answer is properly grounded in the provided context.

        Args:
            question: The original question
            answer: The generated answer
            context_chunks: The context chunks used to generate the answer

        Returns:
            True if the answer is properly grounded, False otherwise
        """
        # In a real implementation, this would involve more sophisticated checks
        # For now, we'll just ensure that an answer was generated and we have context
        return bool(answer and context_chunks and len(answer.strip()) > 10)

    async def get_content_clarification(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]]
    ) -> str:
        """
        Use tools to get clarification about the question or content when needed.

        Args:
            question: The original question
            context_chunks: Context chunks retrieved

        Returns:
            Clarification about the question or relevant content
        """
        # Use the tools to get more information if needed
        search_result = await self.tools.search_textbook_content(
            query=question,
            top_k=3
        )

        if search_result.success and search_result.data:
            # Return the most relevant content based on the question
            relevant_content = search_result.data[0]["text"] if search_result.data else ""
            return f"Relevant content found: {relevant_content[:200]}..."
        else:
            return "No additional content found to clarify this question."