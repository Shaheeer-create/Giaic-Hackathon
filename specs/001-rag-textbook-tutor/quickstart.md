# Quickstart Guide: RAG Backend System for Physical AI & Humanoid Robotics Textbook Tutor

## Overview
This guide provides instructions to set up, configure, and run the RAG backend system that powers the AI tutor for the Physical AI & Humanoid Robotics textbook.

## Prerequisites
- Python 3.10 or higher
- pip package manager
- Access to Qdrant vector database (cloud or local instance)
- Access to Neon PostgreSQL database
- Google Generative AI API key for Gemini models
- Cohere API key for embeddings

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Initialize with uv if available, or use pip
pip install uv  # if not already installed
uv pip install -r requirements.txt

# Or directly with pip
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Copy the example environment file and configure your API keys:

```bash
cp .env.example .env
```

Edit `.env` file with your specific configuration:
```bash
# Google Generative AI (Gemini)
GEMINI_API_KEY=your-gemini-api-key-here

# Cohere for embeddings
COHERE_API_KEY=your-cohere-api-key-here

# Qdrant vector database
QDRANT_URL=your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key

# Neon PostgreSQL database
NEON_DATABASE_URL=your-neon-database-url

# Application settings
ENVIRONMENT=development  # or production
LOG_LEVEL=INFO
```

### 5. Initialize the Application
The application follows this initialization order (as specified):
1. FastAPI application startup
2. Neon PostgreSQL connection
3. Qdrant client initialization
4. Gemini model configuration

## Running the Application

### Development Mode
```bash
# Run with auto-reload for development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
# Run with uvicorn in production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The application will be available at `http://localhost:8000`

## API Endpoints

### 1. Query Endpoint
- **POST** `/query`
- Submit questions about the textbook content
- Example:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain humanoid locomotion principles",
    "user_id": "user-123",
    "confidence_threshold": 0.7
  }'
```

### 2. Ingestion Endpoint
- **POST** `/ingest`
- Add textbook content to the index
- Example:
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Humanoid locomotion involves...",
    "title": "Principles of Humanoid Locomotion",
    "source_file": "chapter5.md",
    "section": "Chapter 5: Locomotion Control"
  }'
```

### 3. Health Check
- **GET** `/health`
- Check if the application is running and all services are connected

## Development Guidelines

### Project Structure
```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/                   # Configuration and settings
│   │   ├── config.py
│   │   └── settings.py
│   ├── api/                    # API routes and dependencies
│   │   ├── routes.py
│   │   └── dependencies.py
│   ├── rag/                    # RAG pipeline implementation
│   │   ├── ingestion.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   ├── generator.py
│   │   └── pipeline.py
│   ├── agents/                 # Tutor agent implementation
│   │   ├── tutor_agent.py
│   │   └── tools.py
│   ├── db/                     # Database connections and models
│   │   ├── neon.py
│   │   └── models.py
│   └── utils/                  # Utility functions
│       ├── chunking.py
│       └── text_cleaner.py
├── tests/                      # Test suite
├── pyproject.toml              # Project dependencies
└── README.md
```

### Key Components

1. **RAG Pipeline**: Located in `rag/` directory, handles ingestion, embedding, retrieval, and generation
2. **Tutor Agent**: Located in `agents/` directory, orchestrates the response generation process
3. **Database Layer**: Located in `db/` directory, manages connections to Qdrant and Neon PostgreSQL

### Testing
Run the test suite:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_query.py

# Run with coverage
pytest --cov=app
```

## Troubleshooting

### Common Issues

**Qdrant Connection Issues**
- Verify your Qdrant URL and API key in the environment variables
- Check that the Qdrant service is running

**API Key Issues**
- Ensure your Gemini and Cohere API keys are valid and properly set
- Check for any usage limits on your API accounts

**Database Connection Issues**
- Verify your Neon PostgreSQL connection string
- Ensure the database is accessible from your network

## Deployment

For production deployment, ensure:
1. Environment variables are securely configured
2. Proper logging and monitoring are set up
3. Database connections are properly managed
4. API keys are secured and not exposed in client code

## Next Steps

1. Start the application using the instructions above
2. Ingest some initial textbook content using the `/ingest` endpoint
3. Test querying the system with the `/query` endpoint
4. Review the logs to ensure proper operation
5. Consult the data model and API contracts for detailed specifications