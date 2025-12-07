from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # Application settings
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    log_level: str = "INFO"
    
    # External service URLs
    gemini_api_key: Optional[str] = None
    cohere_api_key: Optional[str] = None
    qdrant_url: Optional[str] = None
    qdrant_api_key: Optional[str] = None
    neon_database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# Create a single instance of settings
settings = Settings()