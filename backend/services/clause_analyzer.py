"""
Clause Analyzer Service
Analyzes clauses for:
- Time frames and deadlines
- Risks on employer
- General clause summary
"""

import re
from typing import List, Dict, Any


class ClauseAnalyzer:
    """
    Analyzes contract clauses to extract:
    - Time frames and deadlines
    - Employer risks
    - General summaries
    """
    
    # Patterns for time expressions
    TIME_PATTERNS = [
        # Durations: "7 days", "28 days", "14 calendar days"
        (r'\b(\d+)\s+(?:calendar\s+)?(?:business\s+)?(?:working\s+)?days?\b', 'duration', 'days'),
        (r'\b(\d+)\s+weeks?\b', 'duration', 'weeks'),
        (r'\b(\d+)\s+months?\b', 'duration', 'months'),
        (r'\b(\d+)\s+years?\b', 'duration', 'years'),
        # Deadlines: "within X days", "no later than", "at least X days before"
        (r'within\s+(\d+)\s+(?:calendar\s+)?(?:business\s+)?days?\s+(?:of|from|after)', 'deadline', 'days'),
        (r'no\s+later\s+than\s+(\d+)\s+(?:calendar\s+)?(?:business\s+)?days?\s+(?:of|from|after|before)', 'deadline', 'days'),
        (r'at\s+least\s+(\d+)\s+(?:calendar\s+)?(?:business\s+)?days?\s+before', 'deadline', 'days'),
        # Dates: "1 January 2025", "01/01/2025"
        (r'\b(\d{1,2}[\s/-]\d{1,2}[\s/-]\d{2,4})\b', 'date', None),
        (r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', 'date', None),
    ]
    
    # Risk indicators for employer
    RISK_KEYWORDS = [
        # Payment obligations
        ('employer shall pay', 'Payment obligation'),
        ('employer must pay', 'Payment obligation'),
        ('additional payment', 'Additional cost'),
        ('extra payment', 'Additional cost'),
        # Time extensions
        ('extension of time', 'Time extension risk'),
        ('extension to time', 'Time extension risk'),
        ('time extension', 'Time extension risk'),
        ('delay by employer', 'Delay liability'),
        # Claims
        ('contractor may claim', 'Claim entitlement'),
        ('contractor is entitled', 'Claim entitlement'),
        ('contractor shall be entitled', 'Claim entitlement'),
        # Indemnities
        ('indemnify', 'Indemnity obligation'),
        ('indemnity', 'Indemnity obligation'),
        # Warranties
        ('warranty', 'Warranty obligation'),
        ('guarantee', 'Guarantee obligation'),
        # Responsibilities
        ('employer shall provide', 'Provision obligation'),
        ('employer is responsible', 'Responsibility'),
        ('employer\'s risk', 'Risk allocation'),
        ('employer liability', 'Liability'),
    ]
    
    def extract_time_frames(self, clause_text: str) -> List[Dict[str, Any]]:
        """
        Extract all time frames, deadlines, and dates from clause text.
        
        Returns:
            List of dictionaries with:
            - raw: the original text matched
            - type: "duration", "deadline", or "date"
            - value: numeric value if applicable
            - unit: "days", "weeks", "months", "years", or None
            - description: human-readable description
        """
        time_frames = []
        clause_lower = clause_text.lower()
        
        for pattern, time_type, unit in self.TIME_PATTERNS:
            matches = re.finditer(pattern, clause_text, re.IGNORECASE)
            for match in matches:
                raw = match.group(0)
                
                # Avoid duplicates
                if any(tf["raw"] == raw for tf in time_frames):
                    continue
                
                # Extract numeric value if available
                value = None
                if match.groups():
                    try:
                        value = int(match.group(1))
                    except (ValueError, IndexError):
                        pass
                
                # Generate description
                description = self._describe_time_frame(raw, time_type, value, unit)
                
                time_frames.append({
                    "raw": raw,
                    "type": time_type,
                    "value": value,
                    "unit": unit,
                    "description": description
                })
        
        return time_frames
    
    def _describe_time_frame(
        self,
        raw: str,
        time_type: str,
        value: int,
        unit: str
    ) -> str:
        """Generate human-readable description of a time frame"""
        if time_type == "duration":
            if value and unit:
                return f"A period of {value} {unit} (likely for notice, reply, or action)"
            return f"A duration: {raw}"
        elif time_type == "deadline":
            return f"A deadline: {raw}"
        elif time_type == "date":
            return f"A specific date: {raw}"
        return f"Time reference: {raw}"
    
    def format_time_frames_explanation(self, time_frames: List[Dict[str, Any]]) -> str:
        """
        Format time frames into a human-readable explanation.
        
        Returns:
            Multi-line string explaining all time frames in the clause
        """
        if not time_frames:
            return None
        
        explanation = "This clause includes the following time frames:\n"
        for tf in time_frames:
            explanation += f"  - {tf['raw']}: {tf['description']}\n"
        
        return explanation.strip()
    
    def analyze_risks_for_employer(self, clause_text: str) -> Optional[str]:
        """
        Analyze clause text for risks on the employer.
        
        Returns:
            String summary of risks, or None if no significant risks found
        """
        clause_lower = clause_text.lower()
        risks = []
        
        for keyword_phrase, risk_type in self.RISK_KEYWORDS:
            if keyword_phrase in clause_lower:
                # Get context around the keyword (sentence)
                pattern = re.compile(
                    rf'.{{0,100}}{re.escape(keyword_phrase)}.{{0,100}}',
                    re.IGNORECASE | re.DOTALL
                )
                matches = list(pattern.finditer(clause_text))
                
                if matches:
                    context = matches[0].group(0).strip()
                    risks.append(f"Risk ({risk_type}): {context[:200]}...")
        
        if risks:
            # Return summary, avoiding duplicates
            unique_risks = list(dict.fromkeys(risks))  # Preserves order, removes duplicates
            return "\n\n".join(unique_risks[:5])  # Limit to 5 risks
        
        return None
    
    def analyze_clause(self, clause_text: str) -> str:
        """
        Generate a general analysis/summary of the clause.
        
        Identifies:
        - Purpose of the clause
        - Main obligations (Contractor vs Employer)
        - Type of risk (time, cost, quality, legal)
        
        Returns:
            Human-readable summary string
        """
        text_lower = clause_text.lower()
        
        # Identify purpose keywords
        purpose_keywords = {
            'payment': 'This clause deals with payment matters',
            'time': 'This clause addresses time-related obligations',
            'completion': 'This clause covers completion requirements',
            'defect': 'This clause concerns defects and liability',
            'variation': 'This clause handles variations to the contract',
            'claim': 'This clause relates to claims and disputes',
            'termination': 'This clause covers contract termination',
            'indemnity': 'This clause involves indemnity provisions',
            'warranty': 'This clause includes warranty obligations',
        }
        
        purpose = None
        for keyword, desc in purpose_keywords.items():
            if keyword in text_lower:
                purpose = desc
                break
        
        if not purpose:
            purpose = "This clause sets out contractual obligations and requirements."
        
        # Identify parties and obligations
        contractor_obligations = []
        employer_obligations = []
        
        if 'contractor shall' in text_lower or 'contractor must' in text_lower:
            contractor_obligations.append("Contractor has specific obligations")
        if 'contractor may' in text_lower or 'contractor is entitled' in text_lower:
            contractor_obligations.append("Contractor has certain entitlements")
        
        if 'employer shall' in text_lower or 'employer must' in text_lower:
            employer_obligations.append("Employer has specific obligations")
        if 'employer may' in text_lower:
            employer_obligations.append("Employer has certain rights")
        
        # Build summary
        summary = f"{purpose}\n\n"
        
        if contractor_obligations:
            summary += f"Contractor obligations: {', '.join(contractor_obligations)}.\n"
        
        if employer_obligations:
            summary += f"Employer obligations: {', '.join(employer_obligations)}.\n"
        
        # Identify risk types
        risk_types = []
        if any(word in text_lower for word in ['time', 'delay', 'extension', 'deadline']):
            risk_types.append('time')
        if any(word in text_lower for word in ['payment', 'cost', 'price', 'expense']):
            risk_types.append('cost')
        if any(word in text_lower for word in ['defect', 'quality', 'standard', 'comply']):
            risk_types.append('quality')
        if any(word in text_lower for word in ['liability', 'indemnity', 'claim', 'dispute']):
            risk_types.append('legal')
        
        if risk_types:
            summary += f"\nRisk types involved: {', '.join(risk_types)}."
        
        return summary.strip()
