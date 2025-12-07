# OpenAPI Contract: Ingest Endpoint

## POST /ingest

### Description
Accepts textbook content for indexing in the RAG system. Processes the content through cleaning, chunking, and embedding before storing in the vector database.

### Request

#### Path
`POST /ingest`

#### Headers
- `Content-Type: application/json`
- `Accept: application/json`

#### Body
```json
{
  "content": "string (required) - The textbook content to be indexed",
  "title": "string (required) - Title or heading of the content being indexed",
  "source_file": "string (required) - Original source file name or identifier",
  "section": "string (optional) - Section or chapter identifier within the textbook",
  "page_number": "integer (optional) - Page number if applicable",
  "metadata": "object (optional) - Additional metadata about the content"
}
```

#### Example Request
```json
{
  "content": "Humanoid locomotion involves the control of bipedal walking patterns using dynamics and control theory. The key aspects include maintaining balance through zero-moment point (ZMP) control and using inverted pendulum models to understand walking patterns...",
  "title": "Principles of Humanoid Locomotion",
  "source_file": "chapter5_locomotion.md",
  "section": "Chapter 5: Locomotion Control",
  "page_number": 125,
  "metadata": {
    "author": "Textbook Author",
    "last_updated": "2024-12-01"
  }
}
```

### Response

#### Success Response (200 OK)
```json
{
  "status": "string - Status of the ingestion process",
  "indexed_chunks": "integer - Number of content chunks successfully indexed",
  "content_id": "string - Unique identifier for the indexed content",
  "processing_time": "number - Time taken to process and index the content in milliseconds",
  "details": {
    "chunks_created": "integer - Number of text chunks created during processing",
    "embeddings_generated": "integer - Number of embeddings created",
    "chunks_stored": {
      "qdrant": "integer - Number of chunks stored in vector database",
      "neon": "integer - Number of metadata records stored in PostgreSQL"
    }
  },
  "warnings": [
    "string - Any warnings during the ingestion process"
  ]
}
```

#### Example Success Response
```json
{
  "status": "completed",
  "indexed_chunks": 3,
  "content_id": "content-xyz789abc123",
  "processing_time": 32500,
  "details": {
    "chunks_created": 3,
    "embeddings_generated": 3,
    "chunks_stored": {
      "qdrant": 3,
      "neon": 3
    }
  },
  "warnings": []
}
```

#### Error Response (400 Bad Request)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "string - Description of the validation error",
    "details": {
      "field": "string - Field with the error",
      "reason": "string - Why the field is invalid"
    }
  }
}
```

#### Processing Error Response (500 Internal Server Error)
```json
{
  "error": {
    "code": "INGESTION_ERROR",
    "message": "An error occurred during content ingestion",
    "details": {
      "stage": "string - Stage of ingestion where error occurred (e.g., 'cleaning', 'chunking', 'embedding', 'storage')",
      "reason": "string - Detailed reason for the error"
    }
  }
}
```

### Implementation Notes
- Content must be cleaned and normalized before processing
- Text should be chunked semantically to preserve meaning and context
- Embeddings must be generated using the specified embedding model
- Both vector data and metadata must be stored appropriately
- Processing should complete within 5 minutes per chapter as specified
- Must handle large content appropriately with streaming if necessary