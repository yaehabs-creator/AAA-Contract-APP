"""
Clause Classifier Service
Classifies clauses as General Conditions, Particular Conditions, or Unknown
"""

from typing import Optional
from models import ClauseType


class ClauseClassifier:
    """
    Classifies clauses based on section headers and content.
    Uses heuristics that can be improved over time.
    """
    
    # Keywords that suggest General Conditions
    GENERAL_KEYWORDS = [
        "general condition",
        "standard form",
        "standard contract",
        "default provision",
        "unless otherwise",
        "subject to",
    ]
    
    # Keywords that suggest Particular Conditions
    PARTICULAR_KEYWORDS = [
        "particular condition",
        "special condition",
        "specific to",
        "this contract",
        "project specific",
        "as amended",
    ]
    
    def classify_clause_type(
        self,
        full_text: str,
        section_name: Optional[str] = None,
        clause_title: Optional[str] = None
    ) -> ClauseType:
        """
        Classify a clause as General Condition, Particular Condition, or Unknown.
        
        Logic:
        1. Check section_name first (most reliable)
        2. Check clause_title for keywords
        3. Check full_text for keywords
        4. Default to Unknown
        
        Args:
            full_text: The full text of the clause
            section_name: The section name (e.g., "GENERAL CONDITIONS")
            clause_title: The clause title
            
        Returns:
            ClauseType enum value
        """
        text_lower = full_text.lower()
        
        # Step 1: Check section name
        if section_name:
            section_lower = section_name.lower()
            if "general condition" in section_lower and "particular" not in section_lower:
                return ClauseType.GENERAL
            if "particular condition" in section_lower or "special condition" in section_lower:
                return ClauseType.PARTICULAR
        
        # Step 2: Check clause title
        if clause_title:
            title_lower = clause_title.lower()
            for keyword in self.GENERAL_KEYWORDS:
                if keyword in title_lower:
                    return ClauseType.GENERAL
            for keyword in self.PARTICULAR_KEYWORDS:
                if keyword in title_lower:
                    return ClauseType.PARTICULAR
        
        # Step 3: Check full text for keywords
        general_count = sum(1 for keyword in self.GENERAL_KEYWORDS if keyword in text_lower)
        particular_count = sum(1 for keyword in self.PARTICULAR_KEYWORDS if keyword in text_lower)
        
        if particular_count > general_count and particular_count > 0:
            return ClauseType.PARTICULAR
        if general_count > 0:
            return ClauseType.GENERAL
        
        # Default: Unknown
        return ClauseType.UNKNOWN
