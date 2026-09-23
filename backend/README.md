# Onion Quality Grading API

Backend API for the Onion Quality Grading System (SIH 26031)

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL
- Virtual environment

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp env.example .env
# Edit .env with your configuration
```

4. Setup database:
```bash
# Create database
psql -U postgres
CREATE DATABASE onion_sih;
\q

# Run migrations (after alembic is configured)
alembic upgrade head
```

### Running the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── batch.py      # Batch management
│   │   └── analysis.py   # Image analysis & reports
│   ├── models/           # Database models
│   │   ├── user.py
│   │   └── batch.py
│   ├── schemas/          # Pydantic schemas
│   │   ├── user.py
│   │   └── batch.py
│   ├── services/         # Business logic
│   │   ├── auth.py       # Authentication service
│   │   ├── inference.py  # AI inference (mock)
│   │   └── report.py     # PDF generation
│   ├── database.py       # Database connection
│   └── main.py           # FastAPI app
├── requirements.txt
├── env.example
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/me` - Get current user info

### Batches
- `GET /api/batches/` - List batches
- `GET /api/batches/{batch_id}` - Get batch details
- `DELETE /api/batches/{batch_id}` - Delete batch

### Analysis
- `POST /api/analysis/upload` - Upload image and analyze
- `GET /api/analysis/report/{batch_id}` - Generate PDF report

## Mock Mode

Currently, the inference service is in **mock mode** and returns random detection results for testing purposes.

Once you have a trained YOLOv8 model:

1. Uncomment `ultralytics` in `requirements.txt`
2. Update `app/services/inference.py`:
   - Implement `load_model()` method
   - Replace `_generate_mock_detections()` with actual YOLOv8 inference

## Database Migrations

To create and run migrations:

```bash
# Initialize alembic (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Security Notes

- Change `SECRET_KEY` in `.env` before deployment
- Use environment variables for sensitive data
- Never commit `.env` file to version control
- Configure CORS origins properly for production

## Next Steps

- [ ] Configure database migrations with Alembic
- [ ] Integrate S3/MinIO for image storage
- [ ] Replace mock inference with actual YOLOv8 model
- [ ] Add comprehensive error handling
- [ ] Add logging
- [ ] Write unit tests
- [ ] Deploy to production server