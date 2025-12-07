# Agent Context: RAG Backend System for Physical AI & Humanoid Robotics Textbook Tutor

## Project Overview
- **Feature**: RAG Backend System (Gemini-Based Agents) for Physical AI & Humanoid Robotics textbook tutor
- **Branch**: 001-rag-textbook-tutor
- **Technology Stack**: Python 3.10+, FastAPI, Agents SDK, Google Generative AI, Qdrant, Cohere, Neon PostgreSQL
- **Project Type**: Web application (backend API service)

## Key Technologies
- **Framework**: FastAPI, Agents SDK, google-generativeai, qdrant-client, cohere, trafilatura, psycopg2-binary, python-dotenv
- **Database**: Qdrant (vector database), Neon PostgreSQL (metadata and session storage)
- **Target Platform**: Linux server (backend service)

## Project Structure
```
backend/
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── settings.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   └── dependencies.py
│   │
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   ├── generator.py
│   │   └── pipeline.py
│   │
│   ├── agents/
│   │   ├── tutor_agent.py
│   │   └── tools.py
│   │
│   ├── db/
│   │   ├── neon.py
│   │   └── models.py
│   │
│   └── utils/
│       ├── chunking.py
│       └── text_cleaner.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
│
├── pyproject.toml
├── README.md
└── .env.example
```

## API Endpoints
- **POST /query**: Accepts user questions and returns Gemini-generated answers based on textbook content
- **POST /ingest**: Accepts textbook content for indexing in the RAG system

## Key Requirements
- No hallucinations allowed - answers must be grounded in indexed content only
- Must refuse to answer when no relevant context is found
- Response time should not exceed 10 seconds
- Support for 200 concurrent queries
- Follow exact folder structure specified in requirements

## Important Files
- Specification: specs/001-rag-textbook-tutor/spec.md
- Implementation Plan: specs/001-rag-textbook-tutor/plan.md
- Data Model: specs/001-rag-textbook-tutor/data-model.md
- API Contracts: specs/001-rag-textbook-tutor/contracts/
- Research Summary: specs/001-rag-textbook-tutor/research.md
- Quickstart Guide: specs/001-rag-textbook-tutor/quickstart.md