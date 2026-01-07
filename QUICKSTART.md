# Quick Start Guide

## Fast Setup (5 minutes)

### 1. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on: **http://localhost:8000**

### 2. Frontend Setup (new terminal)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: **http://localhost:5173**

### 3. Open Browser
Go to: **http://localhost:5173**

Upload a PDF contract and start analyzing!

---

**Note**: For scanned PDFs, install Tesseract OCR:
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- macOS: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

The app works with regular PDFs even without OCR.
