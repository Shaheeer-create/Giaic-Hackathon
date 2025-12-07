import re
import html
from typing import List, Optional
import trafilatura
from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    """
    Clean and normalize text content for the RAG system.
    
    Args:
        text: Raw text content to clean
        
    Returns:
        Cleaned and normalized text
    """
    if not text:
        return ""
    
    # Unescape HTML entities
    text = html.unescape(text)
    
    # Remove HTML tags if present (using BeautifulSoup for safety)
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove extra newlines and normalize them
    text = re.sub(r'\n+', '\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_text_from_document(content: str, content_type: str = "text") -> str:
    """
    Extract clean text from various document formats.
    
    Args:
        content: Raw document content
        content_type: Type of content ('text', 'html', 'markdown', etc.)
        
    Returns:
        Extracted clean text
    """
    if content_type.lower() == "html":
        # Use trafilatura for extracting text from HTML content
        try:
            text = trafilatura.extract(content, include_comments=False, include_tables=True)
            if text:
                return clean_text(text)
        except Exception:
            # Fallback to basic HTML cleaning if trafilatura fails
            pass
    
    # For other types, just clean the text
    return clean_text(content)


def normalize_content(content: str) -> str:
    """
    Normalize content to ensure consistency.
    
    Args:
        content: Content to normalize
        
    Returns:
        Normalized content
    """
    # Clean the text
    cleaned = clean_text(content)
    
    # Additional normalization steps can be added here
    # For example: standardizing terminology, fixing common typos, etc.
    
    return cleaned


def validate_content(content: str, min_length: int = 10) -> bool:
    """
    Validate content meets minimum requirements.
    
    Args:
        content: Content to validate
        min_length: Minimum character length required
        
    Returns:
        True if content is valid, False otherwise
    """
    if not content or len(content.strip()) < min_length:
        return False
    
    return True


def split_sentences(text: str) -> List[str]:
    """
    Split text into sentences while preserving context.
    
    Args:
        text: Text to split into sentences
        
    Returns:
        List of sentences
    """
    # Simple sentence splitting using regex
    # This can be enhanced with more sophisticated NLP techniques
    sentences = re.split(r'[.!?]+\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences