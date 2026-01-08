"""
Construction Contract Analyzer - FastAPI Backend
Main entry point for the API server
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
import os
import logging
import traceback

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from database import init_db
from models import Clause, ClauseType
from services.contract_processor import ContractProcessor
from services.comparison_service import ComparisonService

# Initialize FastAPI app
app = FastAPI(
    title="Construction Contract Analyzer API",
    description="API for analyzing construction contracts",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Construction Contract Analyzer API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Upload and process contract
@app.post("/api/upload")
async def upload_contract(file: UploadFile = File(...)):
    """
    Upload a PDF contract file and process it into clauses.
    Supports both regular PDFs and scanned PDFs (with OCR).
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save uploaded file temporarily
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process the contract
        processor = ContractProcessor()
        result = processor.process_contract(file_path)
        
        # Clean up temporary file
        os.remove(file_path)
        
        return JSONResponse(content={
            "message": "Contract processed successfully",
            "clauses_count": result["clauses_count"],
            "clauses": result["clauses"]
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing contract: {str(e)}")

# Get all clauses
@app.get("/api/clauses")
async def get_clauses(
    clause_type: Optional[str] = None,
    search: Optional[str] = None
):
    """
    Get all clauses, optionally filtered by type or search term.
    """
    try:
        clauses = Clause.get_all(
            clause_type=clause_type if clause_type else None,
            search_term=search if search else None
        )
        return {"clauses": clauses}
    except Exception as e:
        logger.error(f"Error fetching clauses: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error fetching clauses: {str(e)}")

# Get a single clause by ID
@app.get("/api/clauses/{clause_id}")
async def get_clause(clause_id: int):
    """
    Get a specific clause by its ID.
    """
    try:
        clause = Clause.get_by_id(clause_id)
        if not clause:
            raise HTTPException(status_code=404, detail="Clause not found")
        return {"clause": clause}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching clause: {str(e)}")

# Get comparison view
@app.get("/api/comparison")
async def get_comparison():
    """
    Get the comparison view of General vs Particular Conditions.
    """
    try:
        service = ComparisonService()
        comparison = service.generate_comparison()
        return {"comparison": comparison}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating comparison: {str(e)}")

# Get risks on employer
@app.get("/api/risks")
async def get_risks():
    """
    Get all clauses that have risks on the employer.
    """
    try:
        clauses = Clause.get_by_risk()
        return {"clauses": clauses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching risks: {str(e)}")

# Get time frames
@app.get("/api/time-frames")
async def get_time_frames():
    """
    Get all clauses that contain time frames or deadlines.
    """
    try:
        clauses = Clause.get_by_time_frames()
        return {"clauses": clauses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching time frames: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
