# Construction Contract Analyzer

A beginner-friendly web application for analyzing construction contracts. Upload a PDF contract (including scanned documents), and the app will extract clauses, classify them as General or Particular Conditions, identify risks, extract time frames, and provide a comparison view.

## Features

- 📄 **PDF Upload**: Upload construction contract PDFs (supports both regular and scanned PDFs with OCR)
- 🔍 **Text Extraction**: Extracts text from PDFs without modification
- 📋 **Clause Splitting**: Automatically splits contracts into individual clauses
- 🏷️ **Classification**: Identifies General Conditions vs Particular Conditions
- ⚠️ **Risk Analysis**: Highlights risks on the Employer
- ⏱️ **Time Frame Extraction**: Identifies deadlines, durations, and dates
- 📊 **Comparison View**: Side-by-side comparison of General vs Particular Conditions
- 🔎 **Search**: Search clauses by number, title, or content

## Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Simple, file-based database
- **pdfplumber** - PDF text extraction
- **pytesseract** - OCR for scanned PDFs
- **pdf2image** - Convert PDF pages to images for OCR

### Frontend
- **React 18** - UI library
- **Vite** - Fast build tool
- **Axios** - HTTP client

## Prerequisites

Before you begin, make sure you have:

1. **Python 3.8 or higher** installed
   - Check: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/

2. **Node.js 16 or higher** installed
   - Check: `node --version`
   - Download: https://nodejs.org/

3. **Tesseract OCR** (for scanned PDF support)
   - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr` (Debian/Ubuntu) or `sudo yum install tesseract` (RHEL/CentOS)

## Installation & Setup

### Step 1: Clone or Navigate to the Project

```bash
cd "AAA Contracts app"
```

### Step 2: Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a Python virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   
   # macOS/Linux
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # Windows (Command Prompt)
   venv\Scripts\activate.bat
   
   # macOS/Linux
   source venv/bin/activate
   ```
   
   You should see `(venv)` in your terminal prompt.

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - FastAPI and Uvicorn (web server)
   - SQLAlchemy (database)
   - pdfplumber, pytesseract, pdf2image (PDF/OCR tools)
   - And other required packages

5. **Note about OCR (Tesseract):**
   - Make sure Tesseract is installed and in your system PATH
   - On Windows, you may need to add the Tesseract installation directory to your PATH
   - If you get OCR errors, you can still use the app with regular (non-scanned) PDFs

### Step 3: Frontend Setup

1. **Open a new terminal window** and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
   
   This will install React, Vite, Axios, and other frontend dependencies.

## Running the Application

### Step 1: Start the Backend Server

1. **Activate your virtual environment** (if not already active):
   ```bash
   cd backend
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```
   
   You should see output like:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

3. **The backend is now running on http://localhost:8000**
   - API docs available at: http://localhost:8000/docs

### Step 2: Start the Frontend Development Server

1. **Open a new terminal window** (keep the backend running)

2. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

3. **Start the Vite development server:**
   ```bash
   npm run dev
   ```
   
   You should see output like:
   ```
   VITE v5.0.8  ready in 500 ms
   ➜  Local:   http://localhost:5173/
   ```

4. **The frontend is now running on http://localhost:5173**

### Step 3: Open the Application

Open your web browser and go to:
```
http://localhost:5173
```

You should see the Construction Contract Analyzer interface!

## Using the Application

### Uploading a Contract

1. **Click the "Browse Files" button** or **drag and drop a PDF file** into the upload area
2. **Select your construction contract PDF**
3. **Wait for processing** - The app will:
   - Extract text (using OCR if needed for scanned PDFs)
   - Split the contract into clauses
   - Classify clauses (General/Particular)
   - Analyze risks and time frames
4. **Once complete**, you'll see the clauses appear in the list

### Navigating the Interface

- **All Clauses**: View all extracted clauses
- **General Conditions**: Filter to show only General Conditions
- **Particular Conditions**: Filter to show only Particular Conditions
- **Comparison**: Side-by-side comparison of General vs Particular Conditions
- **Risks on Employer**: View all clauses that contain employer risks
- **Time Frames & Deadlines**: View all clauses with time-related information

### Viewing Clause Details

1. **Click on any clause** in the list to see full details
2. **The detail panel shows**:
   - Original clause text (unchanged from the contract)
   - Analysis summary
   - Risks on employer (if any)
   - Time frames and deadlines (if any)

### Searching

- Use the search bar at the top to search by:
  - Clause number
  - Clause title
  - Clause content
  - Analysis summary

## Project Structure

```
AAA Contracts app/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── database.py                # Database configuration
│   ├── models.py                  # Database models (Clause)
│   ├── requirements.txt           # Python dependencies
│   ├── services/
│   │   ├── contract_processor.py  # PDF processing and clause extraction
│   │   ├── clause_classifier.py   # Classify General vs Particular
│   │   ├── clause_analyzer.py     # Analyze risks, time frames, summaries
│   │   └── comparison_service.py  # Generate comparison views
│   └── uploads/                   # Temporary PDF storage (auto-created)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Main React component
│   │   ├── main.jsx               # React entry point
│   │   ├── components/            # React components
│   │   │   ├── UploadSection.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   ├── TabNavigation.jsx
│   │   │   ├── ClauseList.jsx
│   │   │   ├── ClauseDetail.jsx
│   │   │   └── ComparisonView.jsx
│   │   └── services/
│   │       └── api.js             # API client
│   ├── package.json               # Node.js dependencies
│   └── vite.config.js             # Vite configuration
│
└── README.md                      # This file
```

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError` or `No module named 'fastapi'`
- **Solution**: Make sure you activated the virtual environment and ran `pip install -r requirements.txt`

**Problem**: `pytesseract.pytesseract.TesseractNotFoundError`
- **Solution**: 
  - Install Tesseract OCR (see Prerequisites)
  - Add Tesseract to your system PATH
  - The app will still work for regular (non-scanned) PDFs

**Problem**: Port 8000 already in use
- **Solution**: 
  - Stop the other process using port 8000, OR
  - Run with a different port: `uvicorn main:app --reload --port 8001`
  - Update `frontend/src/services/api.js` to use the new port

**Problem**: Database errors
- **Solution**: Delete `contract_analyzer.db` and restart the backend (it will recreate the database)

### Frontend Issues

**Problem**: `npm install` fails
- **Solution**: 
  - Make sure Node.js is installed: `node --version`
  - Try deleting `node_modules` and `package-lock.json`, then run `npm install` again

**Problem**: Can't connect to backend
- **Solution**: 
  - Make sure the backend is running on http://localhost:8000
  - Check that CORS is enabled (already configured in `backend/main.py`)
  - Check browser console for error messages

**Problem**: Port 5173 already in use
- **Solution**: Vite will automatically use the next available port, or you can specify: `npm run dev -- --port 3000`

### PDF Processing Issues

**Problem**: "Could not extract sufficient text from PDF"
- **Solution**: 
  - The PDF might be corrupted or encrypted
  - Try a different PDF file
  - For scanned PDFs, make sure Tesseract OCR is installed

**Problem**: No clauses found
- **Solution**: 
  - The PDF might not have recognizable clause patterns
  - The app uses heuristics to split clauses - some contracts may need manual adjustment
  - Check the extracted text in the database or logs

## Development Notes

### Database

- The database file `contract_analyzer.db` is created automatically in the `backend/` directory
- To reset the database, delete this file and restart the backend
- All clause data is stored in the `clauses` table

### Code Organization

- **Backend**: Well-commented Python code using FastAPI best practices
- **Frontend**: React components with clear separation of concerns
- **Services**: Business logic separated into service modules for easy maintenance

### Extending the Application

The code is structured to make it easy to:
- Add new clause classification rules (in `clause_classifier.py`)
- Improve time frame extraction (in `clause_analyzer.py`)
- Add new risk detection patterns (in `clause_analyzer.py`)
- Customize the UI (React components in `frontend/src/components/`)

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the code comments (code is well-documented)
3. Check the API documentation at http://localhost:8000/docs when the backend is running

---

**Happy Contract Analyzing!** 📋✨
