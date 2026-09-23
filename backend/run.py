#!/usr/bin/env python
"""
Quick start script for the Onion Quality Grading API.
Run this instead of manually typing uvicorn commands.
"""

import subprocess
import sys
import os

def main():
    # Check if virtual environment exists
    venv_path = os.path.join(os.path.dirname(__file__), 'venv')
    if not os.path.exists(venv_path):
        print("❌ Virtual environment not found.")
        print("\nCreate one with:")
        print("  python -m venv venv")
        print("  source venv/bin/activate  # or venv\\Scripts\\activate on Windows")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if .env exists
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        print("⚠️  .env file not found. Using default configuration.")
        print("\nFor production, copy env.example to .env and configure it.\n")
    
    print("🚀 Starting Onion Quality Grading API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 API stopped.")

if __name__ == "__main__":
    main()