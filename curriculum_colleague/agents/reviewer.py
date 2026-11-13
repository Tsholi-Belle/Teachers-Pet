"""
Reviewer Agent (RV).
Tests the complete output against educational goals, verifies grounding against official curricula,
flags problems, and sends work back to worker agents to be fixed in the Self-Correction loop.
"""

from typing import Dict, Any, List
from curriculum_colleague.verification.fact_checker import FactChecker


class ReviewerAgent:
    def __init__(self, fact_checker: FactChecker = None):
        self.role = "Reviewer Agent"
        self.avatar_tag = "RV"
        self.checker = fact_checker or FactChecker()

    def review_artifact(self, lesson_plan: Dict[str, Any], exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs comprehensive evaluation.
        Combines lesson plan data with matching exercise data and executes verification audit.
        """
        combined = dict(lesson_plan)
        combined["matching_exercises"] = exercise.get("matching_items", [])

        audit = self.checker.verify_lesson_plan(combined)

        # Additional pedagogical review checks
        pedagogy_notes = []
        
        # Check alignment between outcomes and exercise
        outcomes = lesson_plan.get("learning_outcomes", [])
        matched_outcomes = set()
        for item in exercise.get("column_a", []):
            if item.get("outcome_aligned"):
                matched_outcomes.add(item["outcome_aligned"])

        if len(matched_outcomes) < len(outcomes) and len(outcomes) > 0:
            pedagogy_notes.append(f"Exercise covers {len(matched_outcomes)} of {len(outcomes)} stated outcomes. Recommend covering all key outcomes.")

        # Check pacing for large classes
        timeline = lesson_plan.get("timeline", [])
        total_minutes = sum([int(t["time"].split()[0]) for t in timeline if "mins" in t.get("time", "")])
        if total_minutes > 50:
            audit["violations"].append(f"Timeline exceeds standard class period ({total_minutes} mins > 50 mins).")
            audit["required_fixes"].append("Compress direct instruction or guided practice to fit within standard 45-50 min period.")
            audit["verification_score"] -= 10
            audit["passed"] = False

        review_verdict = {
            "reviewer_agent": self.role,
            "status": "APPROVED" if audit["passed"] else "NEEDS_REVISION",
            "verification_score": audit["verification_score"],
            "checks": {
                "curriculum_grounding": audit["grounding_check"]["passed"],
                "source_verification": audit["source_check"]["passed"],
                "crowded_class_40plus": audit["crowded_classroom_check"]["passed"],
                "exercise_integrity": audit["exercise_check"]["passed"],
                "pedagogy_alignment": len(audit["violations"]) == 0
            },
            "violations": audit["violations"],
            "required_corrections": audit["required_fixes"],
            "pedagogy_notes": pedagogy_notes,
            "can_deliver": audit["passed"]
        }
        return review_verdict
