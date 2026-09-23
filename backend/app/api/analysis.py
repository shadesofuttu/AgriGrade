from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.database import get_db
from app.models.user import User
from app.models.batch import Batch
from app.schemas.batch import BatchAnalysisResult, BatchResponse
from app.services.auth import get_current_active_user
from app.services.inference import inference_service
from app.services.report import report_service

router = APIRouter()

@router.post("/upload", response_model=BatchResponse, status_code=status.HTTP_201_CREATED)
async def analyze_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Upload image and perform onion quality analysis.
    """
    try:
        # Log file details for debugging
        print(f"Received file: {file.filename}")
        print(f"Content type: {file.content_type}")
        
        # Validate file exists and has a filename
        if not file or not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        
        # Check file extension (more reliable than content-type on mobile)
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.heic']
        file_ext = file.filename.lower()
        if not any(file_ext.endswith(ext) for ext in allowed_extensions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Validate content type if provided (but don't fail if missing)
        if file.content_type and not file.content_type.startswith('image/'):
            print(f"Warning: Content-Type '{file.content_type}' doesn't start with 'image/', but file extension is valid")
    
        # Read image bytes
        image_bytes = await file.read()
        
        # Run inference (real model if loaded, mock fallback otherwise)
        detections = inference_service.analyze_image(image_bytes)
        grades = inference_service.calculate_grades(detections)
        
        print(f"[Analysis] Total detected: {grades['total_onions']}, Confidence: {grades['ai_confidence']}, Model: {detections['model_version']}")
        
        # Generate batch ID
        batch_id = f"ON-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
        
        # TODO: Upload image to S3 and get URL
        image_url = f"https://placeholder.com/{batch_id}.jpg"
        
        # Create batch record
        batch = Batch(
            batch_id=batch_id,
            user_id=current_user.id,
            image_url=image_url,
            image_count=1,
            total_onions=grades["total_onions"],
            grade_a_count=grades["grade_a_count"],
            urs_count=grades["urs_count"],
            damaged_count=grades["damaged_count"],
            rotten_count=grades["rotten_count"],
            sprouted_count=grades["sprouted_count"],
            grade_a_percentage=grades["grade_a_percentage"],
            urs_percentage=grades["urs_percentage"],
            damaged_percentage=grades["damaged_percentage"],
            rotten_percentage=grades["rotten_percentage"],
            sprouted_percentage=grades["sprouted_percentage"],
            ai_confidence=grades["ai_confidence"],
            model_version=detections["model_version"],
            detections=grades["detections"]
        )
        
        db.add(batch)
        db.commit()
        db.refresh(batch)
        
        return batch
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze image: {str(e)}"
        )

@router.get("/report/{batch_id}")
async def generate_report(
    batch_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate PDF report for a batch.
    """
    # Get batch
    batch = db.query(Batch).filter(
        Batch.batch_id == batch_id,
        Batch.user_id == current_user.id
    ).first()
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found"
        )
    
    # Prepare batch data for report
    batch_data = {
        "batch_id": batch.batch_id,
        "created_at": batch.created_at,
        "inspector_name": current_user.full_name,
        "total_onions": batch.total_onions,
        "grade_a_count": batch.grade_a_count,
        "urs_count": batch.urs_count,
        "damaged_count": batch.damaged_count,
        "rotten_count": batch.rotten_count,
        "sprouted_count": batch.sprouted_count,
        "grade_a_percentage": batch.grade_a_percentage,
        "urs_percentage": batch.urs_percentage,
        "damaged_percentage": batch.damaged_percentage,
        "rotten_percentage": batch.rotten_percentage,
        "sprouted_percentage": batch.sprouted_percentage,
        "ai_confidence": batch.ai_confidence,
        "model_version": batch.model_version
    }
    
    # Generate PDF
    pdf_buffer = report_service.generate_batch_report(batch_data)
    
    # Return as downloadable file
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=onion_report_{batch_id}.pdf"
        }
    )