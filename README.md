# Onion Quality Grading System (SIH 26031)

AI-powered mobile application for automated onion quality assessment at procurement centers.

## Project Overview

This project addresses the problem of subjective and inconsistent manual onion quality inspection by providing an AI-powered solution.

## Tech Stack

**Frontend**: Flutter + Provider  
**Backend**: FastAPI + PostgreSQL  
**ML**: YOLOv8 (mock mode - pending dataset)  
**PDF**: ReportLab

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env  # Configure .env
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
flutter pub get
flutter run
```

## Features

✅ User authentication  
✅ Image capture/upload  
✅ AI analysis (mock mode)  
✅ Quality reports with PDF export  
✅ Batch history  

🚧 Real YOLOv8 integration (pending dataset)

## API Endpoints

- `POST /api/auth/login` - Login
- `POST /api/analysis/upload` - Analyze image
- `GET /api/batches/` - List batches
- `GET /api/analysis/report/{batch_id}` - Download PDF

API Docs: http://localhost:8000/docs

## Next Steps

1. Collect & label dataset (200-500 images/class)
2. Train YOLOv8 model
3. Replace mock inference with trained model
4. Setup database migrations
5. Configure S3 storage
