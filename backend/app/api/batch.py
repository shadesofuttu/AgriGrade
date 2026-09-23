from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.batch import Batch
from app.schemas.batch import BatchResponse, BatchListResponse
from app.services.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=BatchListResponse)
async def get_batches(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get list of batches for current user.
    """
    # Query batches for current user
    batches = db.query(Batch).filter(
        Batch.user_id == current_user.id
    ).order_by(Batch.created_at.desc()).offset(skip).limit(limit).all()
    
    total = db.query(Batch).filter(Batch.user_id == current_user.id).count()
    
    return {
        "batches": batches,
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit
    }

@router.get("/{batch_id}", response_model=BatchResponse)
async def get_batch(
    batch_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get specific batch by batch_id.
    """
    batch = db.query(Batch).filter(
        Batch.batch_id == batch_id,
        Batch.user_id == current_user.id
    ).first()
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found"
        )
    
    return batch

@router.delete("/{batch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_batch(
    batch_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a batch.
    """
    batch = db.query(Batch).filter(
        Batch.batch_id == batch_id,
        Batch.user_id == current_user.id
    ).first()
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found"
        )
    
    db.delete(batch)
    db.commit()
    
    return None