from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Get database URL and handle Render's postgres:// format
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/onion_sih")

# Render provides postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    logger.info("Converted database URL from postgres:// to postgresql://")

# Production-ready connection pool configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=5,           # Number of persistent connections
    max_overflow=10,       # Additional connections when pool is full
    pool_pre_ping=True,    # Verify connections before using
    pool_recycle=3600,     # Recycle connections after 1 hour
    echo=False             # Set to True for SQL query logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger.info(f"Database engine configured with pool_size=5, max_overflow=10")

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()