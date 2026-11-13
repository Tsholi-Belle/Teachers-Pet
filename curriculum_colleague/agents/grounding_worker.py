"""
Grounding Worker Agent (WK-G).
Retrieves verified curriculum standards, syllabus codes, and approved resources.
Strictly disallows unverified sources or ungrounded assertions.
"""

from typing import Dict, Any, List
from curriculum_colleague.verification.fact_checker import FactChecker


class GroundingWorkerAgent:
    def __init__(self, fact_checker: FactChecker = None):
        self.role = "Grounding Worker Agent"
        self.avatar_tag = "WK"
        self.checker = fact_checker or FactChecker()

    def retrieve_grounded_context(self, subject: str, grade: str, goal: str) -> Dict[str, Any]:
        """
        Retrieves official curriculum outcomes and approved sources from the verified registry.
        """
        matches = self.checker.find_verified_standard(subject, grade, goal)
        if not matches:
            # Fallback to general subject lookup in database
            matches = self.checker.find_verified_standard(subject, grade, "")

        if matches:
            standard = matches[0]
            return {
                "status": "grounded_success",
                "curriculum": standard["curriculum"],
                "curriculum_full_name": standard["curriculum_full_name"],
                "authority": standard["authority"],
                "standard_code": standard["standard_code"],
                "topic": standard["topic"],
                "subtopic": standard["subtopic"],
                "learning_outcomes": standard["outcomes"],
                "key_concepts": standard["key_concepts"],
                "verified_sources": standard["verified_sources"],
                "common_misconceptions": standard.get("common_misconceptions", [])
            }
        
        # If no verified standard is found, do NOT fabricate! Explicitly raise unverified warning
        return {
            "status": "unverified_warning",
            "warning": f"No official verified curriculum entry found for {subject} {grade} matching '{goal}'. Hallucination prevention active.",
            "learning_outcomes": [],
            "verified_sources": []
        }
