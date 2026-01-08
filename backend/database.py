"""
Database configuration and initialization
Uses SQLite for simplicity and beginner-friendly setup
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file path
SQLALCHEMY_DATABASE_URL = "sqlite:///./contract_analyzer.db"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def init_db():
    """
    Initialize the database by creating all tables.
    This should be called on application startup.
    """
    from models import Clause  # Import here to avoid circular imports
    Base.metadata.drop_all(bind=engine)  # Drop all existing tables
    Base.metadata.create_all(bind=engine)  # Create tables with current schema

def get_db():
    """
    Dependency function to get database session.
    Yields a database session and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
