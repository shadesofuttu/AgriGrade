from fastapi import APIRouter
from app.database import engine, Base
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/init-db")
def initialize_database():
    """
    Manually initialize database tables.
    Call this if tables weren't created on startup.
    """
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return {
            "status": "success",
            "message": "Database tables created",
            "tables": ["users", "batches"]
        }
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
