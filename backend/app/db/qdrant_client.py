import os
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv

load_dotenv()

class QdrantClientManager:
    """
    Manager class for Qdrant client connection and operations.
    Handles vector database operations for the RAG system.
    """
    
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.client: Optional[QdrantClient] = None
        self.collection_name = "textbook_chunks"
    
    def connect(self) -> QdrantClient:
        """
        Creates and returns a Qdrant client connection.
        """
        if self.qdrant_api_key:
            self.client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                prefer_grpc=True
            )
        else:
            self.client = QdrantClient(url=self.qdrant_url)
        
        self._ensure_collection_exists()
        return self.client
    
    def _ensure_collection_exists(self):
        """
        Ensures the required collection exists in Qdrant.
        """
        if not self.client:
            raise RuntimeError("Qdrant client not initialized")
        
        # Check if collection exists
        collections = self.client.get_collections()
        collection_exists = any(col.name == self.collection_name for col in collections.collections)
        
        if not collection_exists:
            # Create collection with vector configuration appropriate for embeddings
            # Using 1536 dimensions as that's typical for many embedding models
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
            print(f"Created collection: {self.collection_name}")
    
    def get_client(self) -> QdrantClient:
        """
        Returns the Qdrant client, connecting if necessary.
        """
        if not self.client:
            return self.connect()
        return self.client


# Global instance for the application
qdrant_client_manager = QdrantClientManager()