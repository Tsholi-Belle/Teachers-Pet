"""
Planner Agent (PL).
Turns the high-level educational goal into an actionable multi-agent plan,
assigns worker tasks, and coordinates the execution and self-correction cycle.
"""

from typing import Dict, Any, List


class PlannerAgent:
    def __init__(self):
        self.role = "Planner Agent"
        self.avatar_tag = "PL"

    def plan_workflow(self, user_goal: str) -> Dict[str, Any]:
        """
        Takes an outcome-oriented teacher goal, reasons about subject, grade,
        class size constraints (40+ public school kids), and produces execution steps.
        """
        # Parse key entities from prompt
        goal_lower = user_goal.lower()
        
        # Detect Grade
        grade = "Grade 7"
        for g in ["grade 6", "grade 7", "grade 8", "grade 9", "middle school", "primary"]:
            if g in goal_lower:
                grade = g.title()
                break

        # Detect Subject
        subject = "Natural Sciences"
        if any(s in goal_lower for s in ["math", "algebra", "fraction", "fractional"]):
            subject = "Mathematics"
        elif any(s in goal_lower for s in ["english", "speech", "grammar", "language"]):
            subject = "English First Additional Language"
        elif any(s in goal_lower for s in ["science", "photosynthesis", "plant", "ecosystem", "biology", "atom"]):
            subject = "Natural Sciences"

        # Detect Class Size & Public School Context
        class_size = 45
        if "40" in goal_lower or "45" in goal_lower or "50" in goal_lower:
            class_size = 45

        plan_spec = {
            "goal": user_goal,
            "inferred_subject": subject,
            "inferred_grade": grade,
            "target_class_size": class_size,
            "pedagogical_context": "Public school classroom with 40+ learners; chalk-and-talk friendly, low-resource, cooperative pairs.",
            "steps": [
                {
                    "step_id": 1,
                    "agent": "Grounding Worker (WK-G)",
                    "action": "Query verified curriculum registry for accredited standard codes, approved outcomes, and vetted textbooks. Reject any unverified assertions.",
                    "status": "ready"
                },
                {
                    "step_id": 2,
                    "agent": "Lesson Plan Architect (WK-L)",
                    "action": "Draft structured lesson plan with 40+ student management protocols, time breakdown, chalkboard layout, and tiered differentiation.",
                    "status": "waiting"
                },
                {
                    "step_id": 3,
                    "agent": "Exercise & Assessment Worker (WK-E)",
                    "action": "Build matching exercises with 1-to-1 unambiguous definitions, quick-check exit tickets, and master answer keys.",
                    "status": "waiting"
                },
                {
                    "step_id": 4,
                    "agent": "Reviewer Agent (RV)",
                    "action": "Execute 5-point verification audit: check outcome alignment, source validity, crowded-classroom feasibility, and exercise accuracy.",
                    "status": "waiting"
                },
                {
                    "step_id": 5,
                    "agent": "Self-Correction Loop",
                    "action": "If any issues or unverified items are flagged, send specific corrective directives back to workers until fully verified.",
                    "status": "waiting"
                },
                {
                    "step_id": 6,
                    "agent": "Delivery Orchestrator",
                    "action": "Compile and publish print-ready Teacher Lesson Plan, Student Activity Sheet, and Curriculum Verification Audit Certificate.",
                    "status": "waiting"
                }
            ]
        }
        return plan_spec
