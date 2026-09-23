from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, unique=True, index=True)  # e.g., ON-2026-00124
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Image metadata
    image_url = Column(String)
    image_count = Column(Integer, default=1)
    
    # Analysis results
    total_onions = Column(Integer, default=0)
    grade_a_count = Column(Integer, default=0)
    urs_count = Column(Integer, default=0)
    damaged_count = Column(Integer, default=0)
    rotten_count = Column(Integer, default=0)
    sprouted_count = Column(Integer, default=0)
    
    # Percentages
    grade_a_percentage = Column(Float, default=0.0)
    urs_percentage = Column(Float, default=0.0)
    damaged_percentage = Column(Float, default=0.0)
    rotten_percentage = Column(Float, default=0.0)
    sprouted_percentage = Column(Float, default=0.0)
    
    # AI metadata
    ai_confidence = Column(Float, default=0.0)
    model_version = Column(String, default="v1.0")
    
    # Raw detection data
    detections = Column(JSON)  # Store raw YOLO output
    
    # Relationships
    user = relationship("User", back_populates="batches")