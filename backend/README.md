# RAG Backend System for Physical AI & Humanoid Robotics Textbook Tutor

This is a backend Retrieval-Augmented Generation (RAG) system that enables an AI tutor for the Physical AI & Humanoid Robotics textbook. The system indexes textbook content, retrieves relevant context based on user queries, and generates grounded answers using Gemini models.

## Features

- Index textbook content with semantic chunking
- Retrieve relevant textbook passages based on user queries
- Generate grounded answers using Gemini models
- Refuse to answer when no relevant content exists
- API endpoints for querying and content ingestion

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.10+
- **Vector Database**: Qdrant
- **Relational Database**: Neon PostgreSQL
- **AI Models**: Google Generative AI (Gemini)
- **Embeddings**: Cohere
- **Testing**: pytest

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install uv  # if not already installed
   uv pip install -r requirements.txt
   # Or directly with pip: pip install -e .
   ```
4. Set up environment variables by copying .env.example:
   ```bash
   cp .env.example .env
   ```
5. Edit .env file with your specific configuration

## Running the Application

### Development Mode
```bash
# Run with auto-reload for development
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
# Run with uvicorn in production mode
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Query Endpoint
- **POST** `/query`
- Submit questions about the textbook content

### Ingestion Endpoint
- **POST** `/ingest`
- Add textbook content to the index

### Health Check
- **GET** `/health`
- Check if the application is running and all services are connected