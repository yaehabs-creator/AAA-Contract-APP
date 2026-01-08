"""
Database models for the Contract Analyzer
Defines the Clause model with all required fields
"""

from sqlalchemy import Column, Integer, String, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import enum
from database import Base, SessionLocal
from typing import Optional, List, Dict, Any

class ClauseType(str, enum.Enum):
    """Enum for clause types"""
    GENERAL = "General Condition"
    PARTICULAR = "Particular Condition"
    UNKNOWN = "Unknown"

class Clause(Base):
    """
    Clause model representing a single clause from a construction contract.
    
    Stores:
    - Original extracted text (unchanged)
    - Classification (General/Particular/Unknown)
    - Analysis results (risks, time frames, summary)
    """
    __tablename__ = "clauses"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Clause identification
    clause_number = Column(String(50), nullable=True, index=True)
    clause_title = Column(String(500), nullable=True)
    section_name = Column(String(200), nullable=True)
    
    # Original text (MUST NOT be modified)
    full_text_original = Column(Text, nullable=False)
    
    # Cleaned text (spacing fixes only, wording unchanged)
    full_text_cleaned = Column(Text, nullable=True)
    
    # Classification
    clause_type = Column(SQLEnum(ClauseType), default=ClauseType.UNKNOWN, index=True)
    
    # Analysis fields
    analysis_summary = Column(Text, nullable=True)
    risks_on_employer = Column(Text, nullable=True)
    time_frames_raw = Column(Text, nullable=True)  # Raw extracted time expressions
    time_frames_explained = Column(Text, nullable=True)  # Human-readable explanation
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert clause to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "clause_number": self.clause_number,
            "clause_title": self.clause_title,
            "section_name": self.section_name,
            "full_text_original": self.full_text_original,
            "full_text_cleaned": self.full_text_cleaned,
            "clause_type": self.clause_type.value if self.clause_type else None,
            "analysis_summary": self.analysis_summary,
            "risks_on_employer": self.risks_on_employer,
            "time_frames_raw": self.time_frames_raw,
            "time_frames_explained": self.time_frames_explained,
        }
    
    @staticmethod
    def create(
        clause_number: Optional[str],
        clause_title: Optional[str],
        full_text_original: str,
        section_name: Optional[str] = None,
        clause_type: ClauseType = ClauseType.UNKNOWN,
        analysis_summary: Optional[str] = None,
        risks_on_employer: Optional[str] = None,
        time_frames_raw: Optional[str] = None,
        time_frames_explained: Optional[str] = None,
        full_text_cleaned: Optional[str] = None,
    ) -> "Clause":
        """Create a new clause in the database"""
        db = SessionLocal()
        try:
            clause = Clause(
                clause_number=clause_number,
                clause_title=clause_title,
                full_text_original=full_text_original,
                full_text_cleaned=full_text_cleaned,
                section_name=section_name,
                clause_type=clause_type,
                analysis_summary=analysis_summary,
                risks_on_employer=risks_on_employer,
                time_frames_raw=time_frames_raw,
                time_frames_explained=time_frames_explained,
            )
            db.add(clause)
            db.commit()
            db.refresh(clause)
            return clause
        finally:
            db.close()
    
    @staticmethod
    def get_all(
        clause_type: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all clauses, optionally filtered by type or search term"""
        db = SessionLocal()
        try:
            query = db.query(Clause)
            
            # Filter by type if provided
            if clause_type:
                try:
                    clause_type_enum = ClauseType(clause_type)
                    query = query.filter(Clause.clause_type == clause_type_enum)
                except ValueError:
                    pass  # Invalid type, ignore filter
            
            # Search filter
            if search_term:
                search = f"%{search_term}%"
                query = query.filter(
                    (Clause.clause_number.like(search)) |
                    (Clause.clause_title.like(search)) |
                    (Clause.full_text_original.like(search)) |
                    (Clause.analysis_summary.like(search)) |
                    (Clause.risks_on_employer.like(search))
                )
            
            clauses = query.all()
            return [clause.to_dict() for clause in clauses]
        finally:
            db.close()
    
    @staticmethod
    def get_by_id(clause_id: int) -> Optional[Dict[str, Any]]:
        """Get a clause by its ID"""
        db = SessionLocal()
        try:
            clause = db.query(Clause).filter(Clause.id == clause_id).first()
            return clause.to_dict() if clause else None
        finally:
            db.close()
    
    @staticmethod
    def get_by_risk() -> List[Dict[str, Any]]:
        """Get all clauses that have risks on employer"""
        db = SessionLocal()
        try:
            clauses = db.query(Clause).filter(
                Clause.risks_on_employer.isnot(None),
                Clause.risks_on_employer != ""
            ).all()
            return [clause.to_dict() for clause in clauses]
        finally:
            db.close()
    
    @staticmethod
    def get_by_time_frames() -> List[Dict[str, Any]]:
        """Get all clauses that contain time frames"""
        db = SessionLocal()
        try:
            clauses = db.query(Clause).filter(
                Clause.time_frames_raw.isnot(None),
                Clause.time_frames_raw != ""
            ).all()
            return [clause.to_dict() for clause in clauses]
        finally:
            db.close()
    
    @staticmethod
    def delete_all():
        """Delete all clauses (useful for testing or reset)"""
        db = SessionLocal()
        try:
            db.query(Clause).delete()
            db.commit()
        finally:
            db.close()
