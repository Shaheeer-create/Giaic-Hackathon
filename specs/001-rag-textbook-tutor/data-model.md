# Data Model: RAG Backend System for Physical AI & Humanoid Robotics Textbook Tutor

## Entity Relationships Overview

The system has a simple but effective data model to support RAG functionality. The primary entities are related to managing textbook content, retrieval, and queries.

## Core Entities

### Query
**Description**: A question submitted by a user that requires an answer based on textbook content

**Fields**:
- `id` (string): Unique identifier for the query
- `question` (string): The actual question text from the user
- `timestamp` (datetime): When the query was submitted
- `user_id` (string, optional): Identifier for the user who submitted the query
- `confidence_threshold` (float): Minimum confidence score required for results

**Relationships**:
- One-to-many with QueryResponse (one query can generate multiple responses over time)
- One-to-many with RetrievedContext (one query can retrieve multiple contexts)

### Textbook Content
**Description**: The indexed Physical AI & Humanoid Robotics textbook material that has been processed into chunks with embeddings

**Fields**:
- `id` (string): Unique identifier for the content unit
- `title` (string): Title of the content section/chapter
- `content` (string): The actual text content
- `source_file` (string): Original source file name
- `page_number` (integer, optional): Page number if applicable
- `section` (string, optional): Section identifier within the textbook
- `metadata` (json): Additional metadata about the content
- `created_at` (datetime): When the content was indexed
- `updated_at` (datetime): When the content was last updated

**Relationships**:
- One-to-many with DocumentChunk (one content unit can be split into multiple chunks)

### Document Chunk
**Description**: A segment of the textbook content that has been semantically divided for efficient storage and retrieval

**Fields**:
- `id` (string): Unique identifier for the chunk
- `content_id` (string): Reference to the parent Textbook Content
- `text` (string): The chunked text content
- `embedding_vector` (array): Vector representation for similarity search
- `chunk_order` (integer): Position of this chunk in the original content
- `semantic_boundary` (boolean): Whether this chunk ends at a semantic boundary
- `metadata` (json): Additional metadata about the chunk
- `created_at` (datetime): When the chunk was created

**Relationships**:
- Many-to-one with Textbook Content (multiple chunks can belong to one content unit)

### Retrieved Context
**Description**: Relevant textbook passages retrieved based on similarity to a user query

**Fields**:
- `id` (string): Unique identifier for the retrieval result
- `query_id` (string): Reference to the query that triggered this retrieval
- `chunk_id` (string): Reference to the retrieved document chunk
- `similarity_score` (float): Score indicating how similar the chunk is to the query
- `rank` (integer): Position in the relevance ranking
- `retrieved_at` (datetime): When the context was retrieved

**Relationships**:
- Many-to-one with Query (many retrieved contexts can result from one query)
- Many-to-one with Document Chunk (each retrieved context references one chunk)

### Generated Answer
**Description**: The response created by the Gemini model based on the retrieved context

**Fields**:
- `id` (string): Unique identifier for the generated answer
- `query_id` (string): Reference to the original query
- `retrieved_context_ids` (array): References to the contexts used to generate the answer
- `answer_text` (string): The generated answer text
- `confidence_score` (float): Confidence in the accuracy of the answer
- `source_chunks` (array): IDs of the chunks that informed the answer
- `generated_at` (datetime): When the answer was generated
- `metadata` (json): Additional generation metadata

**Relationships**:
- Many-to-one with Query (multiple answers can be generated over time for one query)
- Many-to-many with Retrieved Context (answer is based on multiple retrieved contexts)

### Embedding
**Description**: Numerical representation of text content used for semantic similarity search in the vector database

**Fields**:
- `id` (string): Unique identifier for the embedding
- `chunk_id` (string): Reference to the document chunk
- `vector_data` (array): The actual embedding vector
- `model_used` (string): The embedding model used (Cohere model name)
- `created_at` (datetime): When the embedding was generated

**Relationships**:
- One-to-one with Document Chunk (each chunk has one corresponding embedding)

### Confidence Metadata
**Description**: Information that indicates the reliability and relevance of the generated answer

**Fields**:
- `id` (string): Unique identifier for the confidence metadata
- `answer_id` (string): Reference to the generated answer
- `overall_confidence` (float): Overall confidence in the answer
- `context_relevance` (float): How relevant the retrieved context was
- `coverage_score` (float): How much of the question is addressed by the context
- `warning_flags` (array): Any flags indicating potential issues with the answer
- `calculated_at` (datetime): When the confidence metrics were calculated

**Relationships**:
- One-to-one with Generated Answer (each answer has one confidence metadata record)

## Validation Rules

### Query Validation
- Question must be non-empty and contain at least 3 characters
- User ID must follow proper format if provided
- Confidence threshold must be between 0 and 1

### Textbook Content Validation
- Content must be non-empty
- Title must be provided
- Source file must be specified
- Metadata must follow proper JSON format

### Document Chunk Validation
- Text must be non-empty
- Content ID must reference existing Textbook Content
- Chunk order must be a non-negative integer
- Embedding vector must be properly formatted

### Retrieved Context Validation
- Query ID and chunk ID must exist
- Similarity score must be between 0 and 1
- Rank must be a positive integer

## State Transitions (if applicable)

### Query Lifecycle
1. **Submitted**: Query received by the system
2. **Processing**: Retrieval and generation in progress
3. **Completed**: Answer generated and returned
4. **Failed**: Query could not be processed (no relevant context found)

### Content Lifecycle
1. **Ingesting**: Content being loaded and processed
2. **Chunking**: Content being divided into semantic chunks
3. **Embedding**: Embeddings being generated for chunks
4. **Indexed**: Content fully processed and retrievable
5. **Updated**: When original content is modified

## Indexes and Performance Considerations

### Required Indexes
- Query: Index on timestamp for chronological queries
- Document Chunk: Index on content_id for efficient retrieval
- Retrieved Context: Index on query_id for query result retrieval
- Embedding: Vector index for similarity search (handled by Qdrant)

### Performance Notes
- Embeddings will be stored in Qdrant for efficient vector similarity search
- Textbook content metadata will be stored in PostgreSQL for efficient querying
- Connection pooling should be configured for high-concurrency scenarios