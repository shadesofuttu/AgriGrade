# Quick Start Guide

**Get the Onion Quality Grading System running in 5 minutes!**

---

## Prerequisites

- Python 3.10+ installed
- Flutter SDK installed
- PostgreSQL installed (optional for now - mock mode works without DB)
- Android Studio / Xcode (for mobile testing)

---

## Backend Setup (2 minutes)

### Option 1: Quick Start (Without Database)

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the server
python run.py
```

Backend will start at http://localhost:8000

**Note**: The app works in mock mode without a database. For full functionality, see "With Database" below.

### Option 2: With Database

```bash
# After steps 1-4 above:

# 5. Create PostgreSQL database
psql -U postgres
CREATE DATABASE onion_sih;
\q

# 6. Configure environment
cp env.example .env
# Edit .env and set your DATABASE_URL

# 7. Create tables (manually for now)
psql -U postgres -d onion_sih
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR NOT NULL,
    role VARCHAR DEFAULT 'inspector',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE batches (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_url VARCHAR,
    image_count INTEGER DEFAULT 1,
    total_onions INTEGER DEFAULT 0,
    grade_a_count INTEGER DEFAULT 0,
    urs_count INTEGER DEFAULT 0,
    damaged_count INTEGER DEFAULT 0,
    rotten_count INTEGER DEFAULT 0,
    sprouted_count INTEGER DEFAULT 0,
    grade_a_percentage FLOAT DEFAULT 0,
    urs_percentage FLOAT DEFAULT 0,
    damaged_percentage FLOAT DEFAULT 0,
    rotten_percentage FLOAT DEFAULT 0,
    sprouted_percentage FLOAT DEFAULT 0,
    ai_confidence FLOAT DEFAULT 0,
    model_version VARCHAR DEFAULT 'v1.0',
    detections JSONB
);
\q

# 8. Run the server
python run.py
```

---

## Frontend Setup (1 minute)

Open a **new terminal** (keep backend running):

```bash
# 1. Install dependencies
flutter pub get

# 2. Check connected devices
flutter devices

# 3. Run the app
flutter run

# Or run on specific device
flutter run -d <device-id>
```

---

## Test the App

### 1. Register
- Open the app
- Click "Don't have an account? Register"
- Fill in details:
  - Full Name: John Doe
  - Username: inspector1
  - Email: john@example.com
  - Password: password123
- Click "Register"

### 2. Analyze Onions
- Click "Capture Image" or "Upload Image"
- Select any image (doesn't have to be onions - mock mode)
- Click "Analyze Image"
- View results!

### 3. Check History
- Navigate to "History" tab
- See all your analyzed batches
- Click on any batch for details
- Download PDF report

---

## API Testing (Optional)

Open http://localhost:8000/docs in your browser to test API endpoints via Swagger UI.

**Try this:**
1. Click on `POST /api/auth/register`
2. Click "Try it out"
3. Fill in user details
4. Click "Execute"
5. Copy the response
6. Now try `POST /api/auth/login` with username/password
7. Copy the `access_token`
8. Click "Authorize" button at top
9. Paste token in format: `Bearer <your_token>`
10. Now try other endpoints!

---

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in run.py or run manually:
uvicorn app.main:app --reload --port 8001
```

**Import errors:**
```bash
# Make sure you're in virtual environment
# You should see (venv) in your terminal
pip install -r requirements.txt
```

**CORS errors:**
- Check `backend/app/main.py` CORS configuration
- Add your frontend URL to allowed origins

### Frontend Issues

**Connection refused:**
- Make sure backend is running
- Check `lib/utils/constants.dart` - update `baseUrl` if needed
- If testing on physical device, use your computer's IP:
  ```dart
  static const String baseUrl = 'http://192.168.1.100:8000';
  ```

**Camera permission denied:**
- Android: Check `android/app/src/main/AndroidManifest.xml`
- iOS: Check `ios/Runner/Info.plist`

**Packages not found:**
```bash
flutter clean
flutter pub get
```

---

## What's Working Now

✅ User registration and login
✅ JWT authentication
✅ Image upload (camera or gallery)
✅ Mock AI analysis (random quality distribution)
✅ Quality visualization with charts
✅ PDF report generation
✅ Batch history
✅ Batch deletion

## What Needs Real Data

🚧 Actual onion detection (needs YOLOv8 model)
🚧 Real defect classification (needs trained model)
🚧 Accurate confidence scores (needs model output)

---

## Next Steps After Testing

1. **Collect onion images** - Start taking photos at procurement centers
2. **Label the dataset** - Use Roboflow to annotate onions
3. **Train YOLOv8** - Train model on labeled data
4. **Integrate model** - Replace mock inference with real model
5. **Deploy** - Host backend on cloud, distribute app

---

## Quick Commands Reference

### Backend
```bash
# Start
cd backend && python run.py

# Stop
Ctrl+C

# View logs
# They appear in terminal
```

### Frontend
```bash
# Start
flutter run

# Hot reload
# Press 'r' in terminal

# Hot restart
# Press 'R' in terminal

# Stop
Ctrl+C or press 'q'
```

---

## Need Help?

Check these files:
- **Backend README**: `backend/README.md`
- **Implementation Status**: `IMPLEMENTATION_STATUS.md`
- **Main README**: `README.md`
- **API Docs**: http://localhost:8000/docs (when running)

---

**Happy Testing! 🧅**