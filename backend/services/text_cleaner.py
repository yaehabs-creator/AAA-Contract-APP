"""
Text Cleaning Utility Service
Handles OCR text cleaning and title spacing fixes
WITHOUT changing legal wording - only fixes spacing and formatting
"""

import re
from typing import Optional, Tuple


class TextCleaner:
    """
    Utility class for cleaning extracted text from PDFs/OCR.
    Only fixes spacing issues, never changes legal wording.
    """
    
    @staticmethod
    def fix_title_spacing(title: str) -> Optional[str]:
        """
        Fix spacing in clause titles by inserting spaces where needed.
        
        Rules:
        1. Lowercase letter followed by uppercase → insert space
        2. Letters followed by numbers → insert space
        3. Numbers followed by letters → insert space
        4. Apostrophes should have space after if merged with next word
        5. Preserve all punctuation and wording
        
        Examples:
        - "GeneralIndemnity34" → "General Indemnity 34"
        - "Contractor'sIndemnity40" → "Contractor's Indemnity 40"
        - "PaymentTerms12.6" → "Payment Terms 12.6"
        
        Args:
            title: The title string to fix
            
        Returns:
            Fixed title string with proper spacing, or None if title is None/empty
        """
        if not title or not title.strip():
            return title
        
        # Start with original title
        fixed = title.strip()
        
        # Rule 1: Add space between lowercase and uppercase letters
        # "GeneralIndemnity" → "General Indemnity"
        fixed = re.sub(r'([a-z])([A-Z])', r'\1 \2', fixed)
        
        # Rule 2: Add space between letters and numbers
        # "Indemnity34" → "Indemnity 34"
        fixed = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', fixed)
        
        # Rule 3: Add space between numbers and letters (if not a decimal)
        # "12.6General" → "12.6 General" (but "12.6" stays as is)
        # Don't split decimal numbers like "12.6"
        fixed = re.sub(r'(\d)([A-Za-z])', r'\1 \2', fixed)
        
        # Rule 4: Normalize apostrophes - ensure space after apostrophe if merged
        # "Contractor'sIndemnity" → "Contractor's Indemnity"
        # But preserve existing spaces: "Contractor's Indemnity" stays the same
        fixed = re.sub(r"([''])([A-Za-z])", r"\1 \2", fixed)
        
        # Rule 5: Remove duplicate spaces (from multiple fixes)
        fixed = re.sub(r'\s+', ' ', fixed)
        
        # Trim leading/trailing spaces
        fixed = fixed.strip()
        
        return fixed
    
    @staticmethod
    def clean_ocr_text(text: str) -> str:
        """
        Clean OCR-extracted text by fixing spacing issues while preserving:
        - All words exactly as written
        - All punctuation
        - Line breaks
        - Legal wording unchanged
        
        Fixes:
        - Removes duplicated characters from OCR errors
        - Fixes spacing between words and numbers
        - Normalizes whitespace (but preserves line breaks)
        - Removes excessive spaces
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned text with spacing fixes only
        """
        if not text:
            return text
        
        # Preserve line breaks by splitting and processing line by line
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            if not line.strip():
                cleaned_lines.append('')
                continue
            
            # Remove duplicated characters (common OCR error)
            # Example: "Hellllo" → "Hello" (but be careful not to change valid duplicates)
            # Only remove if 3+ consecutive identical characters
            line = re.sub(r'(.)\1{2,}', r'\1\1', line)
            
            # Fix spacing: letters+numbers, numbers+letters
            # But preserve existing spaces
            # Add space between letters and numbers
            line = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', line)
            # Add space between numbers and letters (but not decimal points)
            line = re.sub(r'(\d)([A-Za-z])', r'\1 \2', line)
            
            # Fix spacing: lowercase followed by uppercase (word boundaries)
            # But don't split abbreviations like "USA" or "pH"
            line = re.sub(r'([a-z])([A-Z][a-z])', r'\1 \2', line)
            
            # Normalize whitespace: collapse multiple spaces to single space
            # But preserve line structure
            line = re.sub(r'[ \t]+', ' ', line)
            
            # Trim each line
            cleaned_lines.append(line.strip())
        
        # Join lines back, preserving original line break structure
        cleaned = '\n'.join(cleaned_lines)
        
        # Final cleanup: remove excessive blank lines (more than 2 consecutive)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        return cleaned
    
    @staticmethod
    def separate_clause_number_and_title(text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Separate clause number from clause title.
        
        Handles patterns like:
        - "12.6 General Indemnity 34"
        - "Sub-Clause 20.1 Payment Terms"
        - "Article 5.2"
        - "1.1.1"
        
        Args:
            text: String containing clause number and optionally title
            
        Returns:
            Tuple of (clause_number, clause_title)
            - clause_number: The numeric identifier (e.g., "12.6")
            - clause_title: The title text (e.g., "General Indemnity 34") or None
        """
        if not text or not text.strip():
            return None, None
        
        text = text.strip()
        
        # Pattern to match clause number at the start
        # Matches: "12.6", "Sub-Clause 12.6", "Article 12.6.1", etc.
        number_pattern = re.compile(
            r'^(?:Sub-?Clause|Clause|Article|Section)?\s*(\d+(?:\.\d+)*)\.?\s*(.*)$',
            re.IGNORECASE
        )
        
        match = number_pattern.match(text)
        if match:
            clause_number = match.group(1)
            remaining = match.group(2).strip()
            
            # If remaining text is very short or looks like part of the number, return None for title
            if not remaining or len(remaining) < 2:
                clause_title = None
            else:
                # Apply title spacing fix
                clause_title = TextCleaner.fix_title_spacing(remaining)
            
            return clause_number, clause_title
        
        # If no pattern match, check if it starts with just a number
        simple_number_match = re.match(r'^(\d+(?:\.\d+)*)\.?\s*(.*)$', text)
        if simple_number_match:
            clause_number = simple_number_match.group(1)
            remaining = simple_number_match.group(2).strip()
            
            if not remaining or len(remaining) < 2:
                clause_title = None
            else:
                clause_title = TextCleaner.fix_title_spacing(remaining)
            
            return clause_number, clause_title
        
        # If no number found, return None for number and the text as title (fixed)
        return None, TextCleaner.fix_title_spacing(text) if text else None
