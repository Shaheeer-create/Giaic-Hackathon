import re
from typing import List, Dict, Any
from dataclasses import dataclass
import uuid
from .text_cleaner import clean_text, split_sentences


@dataclass
class DocumentChunk:
    """
    Data class representing a semantic chunk of a document.
    """
    id: str
    content_id: str
    text: str
    chunk_order: int
    semantic_boundary: bool = True
    metadata: Dict[str, Any] = None
    created_at: str = None


def semantic_chunking(content: str, content_id: str, max_chunk_size: int = 1000, overlap: int = 100) -> List[DocumentChunk]:
    """
    Split content into semantically meaningful chunks.
    
    Args:
        content: The content to be chunked
        content_id: ID of the parent content
        max_chunk_size: Maximum size of each chunk (in characters)
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of DocumentChunk objects
    """
    # Clean the content
    cleaned_content = clean_text(content)
    
    # Split content into sentences to preserve semantic boundaries
    sentences = split_sentences(cleaned_content)
    
    chunks = []
    current_chunk = ""
    current_chunk_size = 0
    chunk_order = 0
    
    for i, sentence in enumerate(sentences):
        # Check if adding the current sentence would exceed max_chunk_size
        if current_chunk_size + len(sentence) > max_chunk_size and current_chunk:
            # Save the current chunk
            chunk_id = str(uuid.uuid4())
            chunk = DocumentChunk(
                id=chunk_id,
                content_id=content_id,
                text=current_chunk.strip(),
                chunk_order=chunk_order,
                semantic_boundary=True
            )
            chunks.append(chunk)
            
            # Start a new chunk with overlap from the previous one
            if overlap > 0:
                # Find the last 'overlap' characters from the current chunk
                overlap_text = current_chunk[-overlap:]
                current_chunk = overlap_text + " " + sentence + " "
            else:
                current_chunk = sentence + " "
            
            current_chunk_size = len(current_chunk)
            chunk_order += 1
        else:
            # Add the sentence to the current chunk
            current_chunk += sentence + " "
            current_chunk_size = len(current_chunk)
    
    # Add the last chunk if it has content
    if current_chunk.strip():
        chunk_id = str(uuid.uuid4())
        chunk = DocumentChunk(
            id=chunk_id,
            content_id=content_id,
            text=current_chunk.strip(),
            chunk_order=chunk_order,
            semantic_boundary=True
        )
        chunks.append(chunk)
    
    return chunks


def paragraph_chunking(content: str, content_id: str, max_chunk_size: int = 2000) -> List[DocumentChunk]:
    """
    Split content into paragraph-based chunks.
    
    Args:
        content: The content to be chunked
        content_id: ID of the parent content
        max_chunk_size: Maximum size of each chunk (in characters)
        
    Returns:
        List of DocumentChunk objects
    """
    # Split content into paragraphs
    paragraphs = re.split(r'\n\s*\n', content)
    
    chunks = []
    chunk_order = 0
    
    i = 0
    while i < len(paragraphs):
        current_chunk = ""
        
        # Add paragraphs to the current chunk until we reach the size limit
        while i < len(paragraphs):
            paragraph = paragraphs[i].strip()
            if not paragraph:
                i += 1
                continue
                
            # Check if adding this paragraph would exceed the size limit
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + "\n\n"
                i += 1
            else:
                # If the current chunk has content, save it
                if current_chunk.strip():
                    chunk_id = str(uuid.uuid4())
                    chunk = DocumentChunk(
                        id=chunk_id,
                        content_id=content_id,
                        text=current_chunk.strip(),
                        chunk_order=chunk_order,
                        semantic_boundary=True
                    )
                    chunks.append(chunk)
                    chunk_order += 1
                    current_chunk = ""  # Start a new chunk
                    # Don't increment i, as we need to try adding the current paragraph to the new chunk
                else:
                    # The paragraph is too large for the chunk size, split it further
                    # For now, we'll add the large paragraph to a new chunk
                    chunk_id = str(uuid.uuid4())
                    chunk = DocumentChunk(
                        id=chunk_id,
                        content_id=content_id,
                        text=paragraph,
                        chunk_order=chunk_order,
                        semantic_boundary=True
                    )
                    chunks.append(chunk)
                    chunk_order += 1
                    i += 1
                    current_chunk = ""
                    break  # Move to the next iteration
        
        # Add the last chunk if it has content
        if current_chunk.strip():
            chunk_id = str(uuid.uuid4())
            chunk = DocumentChunk(
                id=chunk_id,
                content_id=content_id,
                text=current_chunk.strip(),
                chunk_order=chunk_order,
                semantic_boundary=True
            )
            chunks.append(chunk)
            chunk_order += 1
    
    return chunks


def chunk_content(content: str, content_id: str, strategy: str = "semantic") -> List[DocumentChunk]:
    """
    Main function to chunk content using the specified strategy.
    
    Args:
        content: The content to be chunked
        content_id: ID of the parent content
        strategy: The chunking strategy to use ("semantic" or "paragraph")
        
    Returns:
        List of DocumentChunk objects
    """
    if strategy == "semantic":
        return semantic_chunking(content, content_id)
    elif strategy == "paragraph":
        return paragraph_chunking(content, content_id)
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")