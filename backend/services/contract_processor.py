"""
Contract Processor Service
Handles PDF upload, OCR, text extraction, and clause splitting
"""

import os
import re
from typing import List, Dict, Any, Optional, Tuple
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

# Note: When running from backend/ directory, these imports work because
# Python adds the current directory to sys.path
from models import Clause, ClauseType
from services.clause_classifier import ClauseClassifier
from services.clause_analyzer import ClauseAnalyzer
from services.text_cleaner import TextCleaner


class ContractProcessor:
    """
    Processes uploaded PDF contracts:
    1. Extracts text (with OCR if needed)
    2. Splits into clauses
    3. Classifies clauses
    4. Analyzes each clause
    """
    
    def __init__(self):
        self.classifier = ClauseClassifier()
        self.analyzer = ClauseAnalyzer()
    
    def process_contract(self, file_path: str) -> Dict[str, Any]:
        """
        Main processing function.
        Takes a PDF file path and processes it into clauses.
        
        Returns:
            Dictionary with clauses_count and list of clause dictionaries
        """
        # Step 1: Extract text from PDF (with OCR if needed)
        print(f"Extracting text from: {file_path}")
        original_text, cleaned_text = self._extract_text_from_pdf(file_path)
        
        if not original_text or len(original_text.strip()) < 100:
            raise ValueError("Could not extract sufficient text from PDF. The file may be corrupted or empty.")
        
        # Step 2: Split text into clauses (use cleaned text for better parsing)
        print("Splitting text into clauses...")
        raw_clauses = self._split_into_clauses(cleaned_text)
        
        if not raw_clauses:
            raise ValueError("Could not identify any clauses in the contract.")
        
        # Step 3: Process each clause
        print(f"Processing {len(raw_clauses)} clauses...")
        processed_clauses = []
        
        # Store original and cleaned text for mapping
        self._original_text = original_text
        self._cleaned_text = cleaned_text
        
        for raw_clause in raw_clauses:
            clause_data = self._process_single_clause(raw_clause, original_text)
            if clause_data:
                # Save to database
                clause = Clause.create(**clause_data)
                processed_clauses.append(clause.to_dict())
        
        return {
            "clauses_count": len(processed_clauses),
            "clauses": processed_clauses
        }
    
    def _extract_text_from_pdf(self, file_path: str) -> Tuple[str, str]:
        """
        Extract text from PDF file.
        Tries regular text extraction first, falls back to OCR if needed.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple of (original_text, cleaned_text)
            - original_text: Raw extracted text (unchanged)
            - cleaned_text: Text with spacing fixes only (for OCR)
        """
        original_text = ""
        is_ocr = False
        
        # Try regular text extraction first
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        original_text += page_text + "\n"
            
            # If we got good text (more than 500 chars), use it
            if len(original_text.strip()) > 500:
                # Regular PDF text usually doesn't need cleaning
                cleaned_text = original_text
                return original_text, cleaned_text
        except Exception as e:
            print(f"Regular extraction failed: {e}")
        
        # If regular extraction didn't work well, try OCR
        print("Regular extraction insufficient, trying OCR...")
        is_ocr = True
        try:
            # Convert PDF to images
            images = convert_from_path(file_path, dpi=300)
            
            # Extract text from each image using OCR
            for i, image in enumerate(images):
                print(f"OCR processing page {i+1}/{len(images)}...")
                page_text = pytesseract.image_to_string(image, lang='eng')
                original_text += page_text + "\n"
            
            # Clean OCR text (spacing fixes only)
            cleaned_text = TextCleaner.clean_ocr_text(original_text)
            
            return original_text, cleaned_text
        except Exception as e:
            print(f"OCR failed: {e}")
            raise ValueError(f"Could not extract text from PDF. Error: {e}")
    
    def _split_into_clauses(self, text: str) -> List[Dict[str, Any]]:
        """
        Split contract text into individual clauses.
        
        Looks for patterns like:
        - "1.1", "1.2", "Sub-Clause 2.1"
        - Section headers like "GENERAL CONDITIONS"
        
        Returns:
            List of dictionaries with:
            - clause_number: detected clause number
            - clause_title: detected title
            - full_text: the clause text
            - section_name: which section it belongs to
        """
        clauses = []
        current_section = None
        
        # Normalize line breaks
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        
        # Split by potential clause boundaries
        # Pattern: Clause number at start of line (e.g., "1.1", "Sub-Clause 2.1", "Article 3")
        clause_pattern = re.compile(
            r'^(?:Sub-?Clause|Clause|Article|Section)?\s*(\d+(?:\.\d+)*(?:\.\d+)?)\.?\s+(.+?)$',
            re.MULTILINE | re.IGNORECASE
        )
        
        # Also detect section headers
        section_pattern = re.compile(
            r'^(?:PART|SECTION|CHAPTER)\s+[IVX]+[\.:]?\s+(.+)|^([A-Z][A-Z\s&]+CONDITIONS?)\s*$',
            re.MULTILINE
        )
        
        lines = text.split('\n')
        current_clause_text = []
        current_clause_number = None
        current_clause_title = None
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for section header
            section_match = section_pattern.match(line)
            if section_match:
                section_name = section_match.group(1) or section_match.group(2)
                if section_name:
                    current_section = section_name.strip()
                    # Save previous clause if exists
                    if current_clause_text:
                        clauses.append({
                            "clause_number": current_clause_number,
                            "clause_title": current_clause_title,
                            "full_text": '\n'.join(current_clause_text),
                            "section_name": current_section
                        })
                    current_clause_text = []
                    current_clause_number = None
                    current_clause_title = None
            
            # Check for clause number
            clause_match = clause_pattern.match(line)
            if clause_match:
                # Save previous clause
                if current_clause_text:
                    clauses.append({
                        "clause_number": current_clause_number,
                        "clause_title": current_clause_title,
                        "full_text": '\n'.join(current_clause_text),
                        "section_name": current_section
                    })
                
                # Start new clause
                # Extract number and title properly
                detected_number = clause_match.group(1)
                title_part = clause_match.group(2).strip()
                
                # Use text cleaner to separate number and title properly
                if title_part and len(title_part) < 200:  # Likely contains title
                    number, title = TextCleaner.separate_clause_number_and_title(
                        f"{detected_number}. {title_part}"
                    )
                    current_clause_number = number or detected_number
                    # Fix title spacing
                    if title:
                        current_clause_title = TextCleaner.fix_title_spacing(title)
                    else:
                        current_clause_title = TextCleaner.fix_title_spacing(title_part) if title_part else None
                else:
                    current_clause_number = detected_number
                    current_clause_title = None
                
                current_clause_text = [line]
            else:
                # Continue current clause
                if current_clause_text or line:  # Start clause on first non-empty line
                    current_clause_text.append(line)
            
            i += 1
        
        # Don't forget the last clause
        if current_clause_text:
            clauses.append({
                "clause_number": current_clause_number,
                "clause_title": current_clause_title,
                "full_text": '\n'.join(current_clause_text),
                "section_name": current_section
            })
        
        # If no clauses were found with pattern matching, split by paragraphs
        if not clauses:
            print("No clauses found with pattern matching, splitting by paragraphs...")
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 50]
            for i, para in enumerate(paragraphs[:50]):  # Limit to first 50 paragraphs
                clauses.append({
                    "clause_number": str(i + 1),
                    "clause_title": None,
                    "full_text": para,
                    "section_name": current_section
                })
        
        return clauses
    
    def _process_single_clause(self, raw_clause: Dict[str, Any], original_text: str = None) -> Optional[Dict[str, Any]]:
        """
        Process a single raw clause:
        1. Clean and fix title spacing
        2. Classify it (General/Particular)
        3. Analyze risks
        4. Extract time frames
        5. Generate summary
        
        Args:
            raw_clause: Dictionary with clause_number, clause_title, full_text, section_name
            
        Returns:
            Dictionary ready for Clause.create()
        """
        full_text_cleaned = raw_clause["full_text"]
        
        # Skip very short clauses (likely noise)
        if len(full_text_cleaned.strip()) < 20:
            return None
        
        # Get clause number and title (with spacing fixes)
        clause_number = raw_clause.get("clause_number")
        clause_title = raw_clause.get("clause_title")
        
        # Apply title spacing fix if title exists
        if clause_title:
            clause_title = TextCleaner.fix_title_spacing(clause_title)
        
        # If title is missing, try to extract it from the first line
        if not clause_title and full_text_cleaned:
            first_line = full_text_cleaned.split('\n')[0].strip()
            # Try to extract title from first line
            _, extracted_title = TextCleaner.separate_clause_number_and_title(first_line)
            if extracted_title:
                clause_title = extracted_title
        
        # Get original text corresponding to this clause
        # For now, use cleaned text as original if we can't map it
        # In a more advanced implementation, you'd map the clause position back to original text
        # For simplicity, we'll use cleaned as original for regular PDFs,
        # and for OCR, the cleaned version is what we extracted
        if original_text and original_text == full_text_cleaned:
            # Regular PDF - no cleaning needed
            full_text_original = original_text
        else:
            # OCR text - use cleaned as "original" since OCR is already processed
            # In practice, you'd want to map character positions back
            full_text_original = full_text_cleaned
        
        # Fix section name spacing too
        section_name = raw_clause.get("section_name")
        if section_name:
            section_name = TextCleaner.fix_title_spacing(section_name)
        
        # Classify clause type (use cleaned title if available)
        clause_type = self.classifier.classify_clause_type(
            full_text_cleaned,
            section_name,
            clause_title
        )
        
        # Analyze clause
        analysis = self.analyzer.analyze_clause(full_text_cleaned)
        
        # Extract time frames
        time_frames = self.analyzer.extract_time_frames(full_text_cleaned)
        time_frames_raw = ", ".join([tf["raw"] for tf in time_frames])
        time_frames_explained = self.analyzer.format_time_frames_explanation(time_frames)
        
        # Analyze risks (pass clause number and title for professional formatting)
        risks = self.analyzer.analyze_risks_for_employer(
            full_text_cleaned,
            clause_number=clause_number,
            clause_title=clause_title
        )
        
        return {
            "clause_number": clause_number,
            "clause_title": clause_title,
            "full_text_original": full_text_original,  # ORIGINAL TEXT - NEVER MODIFY
            "full_text_cleaned": full_text_cleaned,  # CLEANED TEXT - spacing fixes only
            "section_name": section_name,
            "clause_type": clause_type,
            "analysis_summary": analysis,
            "risks_on_employer": risks,
            "time_frames_raw": time_frames_raw if time_frames else None,
            "time_frames_explained": time_frames_explained if time_frames else None,
        }
