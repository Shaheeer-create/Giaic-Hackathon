import os
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # Import Base from the models module

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("NEON_DATABASE_URL")

if not DATABASE_URL:
    # Fallback to a local SQLite database for development
    DATABASE_URL = "sqlite:///./textbook_tutor.db"
    print("NEON_DATABASE_URL not set, using local SQLite database for development")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency for FastAPI to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database tables
    """
    Base.metadata.create_all(bind=engine)


# Initialize database tables when module is imported
init_db()