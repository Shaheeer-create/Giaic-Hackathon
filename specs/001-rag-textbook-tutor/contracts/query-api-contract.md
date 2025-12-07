# OpenAPI Contract: Query Endpoint

## POST /query

### Description
Accepts a user question about the Physical AI & Humanoid Robotics textbook and returns a generated answer based on retrieved textbook content.

### Request

#### Path
`POST /query`

#### Headers
- `Content-Type: application/json`
- `Accept: application/json`

#### Body
```json
{
  "question": "string (required) - The question about the textbook content",
  "user_id": "string (optional) - Identifier for the user asking the question",
  "confidence_threshold": "number (optional, default: 0.7) - Minimum confidence score required for results"
}
```

#### Example Request
```json
{
  "question": "Explain the principles of humanoid locomotion in Physical AI",
  "user_id": "user-12345",
  "confidence_threshold": 0.75
}
```

### Response

#### Success Response (200 OK)
```json
{
  "answer": "string - The generated answer based on textbook content",
  "confidence_score": "number - Confidence in the accuracy of the answer (0-1)",
  "referenced_chunks": [
    {
      "chunk_id": "string - ID of the textbook chunk used",
      "content_preview": "string - Brief preview of the content used",
      "similarity_score": "number - How similar this chunk is to the query (0-1)",
      "section": "string - Section of the textbook this chunk belongs to"
    }
  ],
  "query_id": "string - Unique identifier for this query",
  "metadata": {
    "processing_time": "number - Time taken to process the query in milliseconds",
    "total_chunks_retrieved": "number - Total number of chunks considered",
    "model_used": "string - The model used for generation"
  }
}
```

#### Example Success Response
```json
{
  "answer": "Humanoid locomotion in Physical AI involves the control of bipedal walking using principles of dynamics and control theory. The key aspects include maintaining balance through zero-moment point (ZMP) control and using inverted pendulum models to understand walking patterns...",
  "confidence_score": 0.85,
  "referenced_chunks": [
    {
      "chunk_id": "ch-001-phys-ai-locomotion",
      "content_preview": "Humanoid locomotion involves the control of bipedal walking patterns using dynamics and control theory...",
      "similarity_score": 0.92,
      "section": "Chapter 5: Locomotion Control"
    }
  ],
  "query_id": "query-abc123def456",
  "metadata": {
    "processing_time": 2450,
    "total_chunks_retrieved": 5,
    "model_used": "gemini-pro"
  }
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

#### No Content Found Response (404 Not Found)
```json
{
  "error": {
    "code": "NO_RELEVANT_CONTENT",
    "message": "No relevant textbook content found to answer the question",
    "suggestion": "string - Suggested alternative action if applicable"
  }
}
```

#### Server Error Response (500 Internal Server Error)
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An internal error occurred while processing the query"
  }
}
```

### Implementation Notes
- Must validate that the question is not empty and contains at least 3 meaningful characters
- Must ensure answers are grounded only in indexed textbook content
- Must return appropriate error when no relevant content is found
- Processing time should not exceed 10 seconds as per specification