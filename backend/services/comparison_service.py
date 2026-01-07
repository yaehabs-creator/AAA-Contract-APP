"""
Comparison Service
Creates comparison views between General and Particular Conditions
"""

from typing import List, Dict, Any
from models import Clause


class ComparisonService:
    """
    Generates comparison between General and Particular Conditions.
    Matches clauses by topic/keywords and highlights differences.
    """
    
    def generate_comparison(self) -> List[Dict[str, Any]]:
        """
        Generate comparison table between General and Particular Conditions.
        
        Returns:
            List of comparison entries, each containing:
            - topic: the topic/keyword
            - general_clause: General Condition info (if found)
            - particular_clause: Particular Condition info (if found)
            - comment: differences or extra risks
        """
        # Get all General and Particular clauses
        all_clauses = Clause.get_all()
        general_clauses = [c for c in all_clauses if c.get("clause_type") == "General Condition"]
        particular_clauses = [c for c in all_clauses if c.get("clause_type") == "Particular Condition"]
        
        # Topic keywords for matching
        topics = {
            "time": ["time", "completion", "delay", "extension", "deadline"],
            "payment": ["payment", "price", "cost", "expense", "compensation"],
            "variations": ["variation", "change", "modification", "alteration"],
            "defects": ["defect", "liability", "warranty", "guarantee"],
            "claims": ["claim", "dispute", "entitlement"],
            "termination": ["termination", "terminate", "cancel"],
            "indemnity": ["indemnity", "indemnify"],
        }
        
        comparisons = []
        
        # For each topic, try to find matching clauses
        for topic_name, keywords in topics.items():
            general_match = self._find_clause_by_keywords(general_clauses, keywords)
            particular_match = self._find_clause_by_keywords(particular_clauses, keywords)
            
            if general_match or particular_match:
                comment = self._generate_comment(general_match, particular_match)
                
                comparisons.append({
                    "topic": topic_name.title(),
                    "general_clause": {
                        "clause_number": general_match.get("clause_number") if general_match else None,
                        "clause_title": general_match.get("clause_title") if general_match else None,
                        "summary": general_match.get("analysis_summary", "")[:150] + "..." if general_match and general_match.get("analysis_summary") else None,
                    } if general_match else None,
                    "particular_clause": {
                        "clause_number": particular_match.get("clause_number") if particular_match else None,
                        "clause_title": particular_match.get("clause_title") if particular_match else None,
                        "summary": particular_match.get("analysis_summary", "")[:150] + "..." if particular_match and particular_match.get("analysis_summary") else None,
                    } if particular_match else None,
                    "comment": comment,
                })
        
        # Also add unmatched clauses
        matched_particular_ids = {
            self._find_clause_by_keywords(particular_clauses, topics[topic]).get("id")
            for topic in topics
            if self._find_clause_by_keywords(particular_clauses, topics[topic])
        }
        
        unmatched_particular = [
            c for c in particular_clauses
            if c.get("id") not in matched_particular_ids
        ]
        
        for clause in unmatched_particular[:10]:  # Limit to 10 unmatched
            comparisons.append({
                "topic": clause.get("clause_title") or f"Clause {clause.get('clause_number')}",
                "general_clause": None,
                "particular_clause": {
                    "clause_number": clause.get("clause_number"),
                    "clause_title": clause.get("clause_title"),
                    "summary": clause.get("analysis_summary", "")[:150] + "..." if clause.get("analysis_summary") else None,
                },
                "comment": "This is a Particular Condition with no matching General Condition. Review for additional risks.",
            })
        
        return comparisons
    
    def _find_clause_by_keywords(
        self,
        clauses: List[Dict[str, Any]],
        keywords: List[str]
    ) -> Dict[str, Any]:
        """Find the first clause that contains any of the keywords"""
        text_to_search = ""
        for clause in clauses:
            text_to_search = (
                (clause.get("clause_title") or "") + " " +
                (clause.get("analysis_summary") or "") + " " +
                (clause.get("full_text_original", "")[:500] or "")
            ).lower()
            
            if any(keyword in text_to_search for keyword in keywords):
                return clause
        
        return None
    
    def _generate_comment(
        self,
        general_clause: Dict[str, Any],
        particular_clause: Dict[str, Any]
    ) -> str:
        """Generate a comment about differences between General and Particular clauses"""
        if not general_clause and not particular_clause:
            return ""
        
        if not particular_clause:
            return "Only General Condition exists. Review if Particular Condition needed."
        
        if not general_clause:
            return "Only Particular Condition exists. This may add extra obligations."
        
        # Check for differences
        comments = []
        
        # Check time frames
        general_times = general_clause.get("time_frames_raw") or ""
        particular_times = particular_clause.get("time_frames_raw") or ""
        if particular_times and general_times != particular_times:
            comments.append("Time frames differ from General Condition.")
        elif particular_times and not general_times:
            comments.append("Particular Condition adds time frames.")
        
        # Check risks
        particular_risks = particular_clause.get("risks_on_employer") or ""
        general_risks = general_clause.get("risks_on_employer") or ""
        if particular_risks and len(particular_risks) > len(general_risks or ""):
            comments.append("Particular Condition may add extra risks for Employer.")
        
        if not comments:
            return "Similar to General Condition. Review for subtle differences."
        
        return " ".join(comments)
