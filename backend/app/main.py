from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, batch, analysis
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Onion Quality Grading API",
    description="AI-powered onion quality assessment system for procurement centers",
    version="1.0.0"
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(batch.router, prefix="/api/batches", tags=["Batches"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])

@app.get("/")
async def root():
    return {
        "message": "Onion Quality Grading API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}