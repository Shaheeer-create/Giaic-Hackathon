# Research Summary: RAG Backend System (Gemini-Based Agents) for Physical AI & Humanoid Robotics Textbook Tutor

## Overview
This document captures the research and decisions made during planning for the RAG backend system, addressing all technical unknowns and establishing the foundation for implementation.

## Technology Stack Decisions

### Backend Framework
- **Decision**: FastAPI
- **Rationale**: High-performance, easy to use, excellent for API development with built-in async support and automatic OpenAPI documentation generation
- **Alternatives considered**: Flask (simpler but less performant), Django (overkill for API-only backend)

### LLM Integration
- **Decision**: Google Generative AI (Gemini models)
- **Rationale**: Specified in requirements, excellent for generating grounded responses from context
- **Alternatives considered**: OpenAI API (different cost structure), Hugging Face models (self-hosted alternative)

### Vector Database
- **Decision**: Qdrant
- **Rationale**: High-performance vector database with good Python SDK, designed specifically for similarity search
- **Alternatives considered**: Pinecone (managed but vendor-locked), Weaviate (alternative open-source), FAISS (Facebook AI Similarity Search)

### Relational Database
- **Decision**: Neon PostgreSQL
- **Rationale**: Serverless PostgreSQL with git-like branching, excellent for metadata and session storage
- **Alternatives considered**: Traditional PostgreSQL (requires more setup), SQLite (simpler but limited), MongoDB (document-based)

### Embeddings Provider
- **Decision**: Cohere
- **Rationale**: High-quality embeddings specifically for retrieval tasks, good performance
- **Alternatives considered**: OpenAI embeddings (vendor lock-in), Sentence Transformers (self-hosted option)

### Text Processing
- **Decision**: Trafilatura
- **Rationale**: Excellent for extracting clean text from various document formats, particularly good for academic content
- **Alternatives considered**: BeautifulSoup (more general purpose), PDFMiner (PDF-specific)

## Architecture Considerations

### RAG Pipeline Design
- **Decision**: Separate ingestion and retrieval pipelines with clear separation of concerns
- **Rationale**: Allows independent scaling of indexing and querying capabilities
- **Implementation**: Dedicated modules for ingestion, embeddings, retrieval, and generation

### Agent Design
- **Decision**: Tutor Agent that orchestrates the RAG process using Gemini models
- **Rationale**: Allows for more sophisticated reasoning and response generation while maintaining grounding in textbook content
- **Constraints**: Must refuse answers when no relevant context is found

### API Design
- **Decision**: REST API with POST endpoints for query and ingestion
- **Rationale**: Simple, well-understood, supports the required functionality
- **Endpoints**: /query for questions, /ingest for content indexing

## Performance and Scalability

### Response Time Requirements
- **Decision**: 10-second maximum response time for query processing
- **Rationale**: Balances thorough retrieval and generation with user experience expectations
- **Optimization approach**: Efficient vector search, optimized context injection

### Concurrency Handling
- **Decision**: Support for 200 concurrent queries
- **Rationale**: Based on specification requirements, allows for reasonable load handling
- **Implementation**: Async processing where possible, connection pooling

## Security and Reliability

### Content Integrity
- **Decision**: Strict grounding requirement - no answers without textbook content
- **Rationale**: Prevents hallucinations and maintains educational value
- **Implementation**: Validation in generator module to check for retrieved context

### Error Handling
- **Decision**: Graceful degradation with clear error messages
- **Rationale**: Maintains user trust and provides debugging information
- **Implementation**: Comprehensive exception handling with meaningful error responses

## Development Approach

### Folder Structure
- **Decision**: Follow exact structure specified in requirements
- **Rationale**: Ensures consistency and meets architectural requirements
- **Structure**: Dedicated directories for core, api, rag, agents, db, utils

### Testing Strategy
- **Decision**: Unit, integration, and contract tests
- **Rationale**: Ensures quality at all levels of the system
- **Implementation**: pytest framework with appropriate test types for each module