from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# TODO: Need to implement connection retry logic
# TODO: Add better error handling for connection failures
# TODO: Consider adding connection timeout settings

load_dotenv()

# Database URL from environment variable
# Started with SQLite, moved to PostgreSQL for better concurrency
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create engine with connection pooling
# Had to tweak these values after some performance issues
# Still not sure if these are optimal values
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,  # Might need to adjust based on load
    max_overflow=10,  # Learned about this the hard way
    pool_timeout=30,  # Had timeout issues in production
    pool_recycle=1800,  # Connections were dying after 30 mins
    echo=False  # Set to True when debugging SQL issues
)

# Create session factory
# This took a while to get right - session management is tricky
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
# Using this for all our database models
Base = declarative_base()

def get_db():
    """Get database session
    Had to add proper session cleanup after memory leaks
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database
    This was a pain to debug - had issues with table creation
    and migrations
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        # TODO: Add proper error handling and logging
        raise 