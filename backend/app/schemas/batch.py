from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class BatchCreate(BaseModel):
    batch_id: str

class BatchAnalysisResult(BaseModel):
    total_onions: int
    grade_a_count: int
    urs_count: int
    damaged_count: int
    rotten_count: int
    sprouted_count: int
    grade_a_percentage: float
    urs_percentage: float
    damaged_percentage: float
    rotten_percentage: float
    sprouted_percentage: float
    ai_confidence: float
    detections: Dict[str, Any]

class BatchResponse(BaseModel):
    id: int
    batch_id: str
    user_id: int
    created_at: datetime
    image_url: Optional[str]
    image_count: int
    total_onions: int
    grade_a_count: int
    urs_count: int
    damaged_count: int
    rotten_count: int
    sprouted_count: int
    grade_a_percentage: float
    urs_percentage: float
    damaged_percentage: float
    rotten_percentage: float
    sprouted_percentage: float
    ai_confidence: float
    model_version: str

    class Config:
        from_attributes = True

class BatchListResponse(BaseModel):
    batches: list[BatchResponse]
    total: int
    page: int
    page_size: int