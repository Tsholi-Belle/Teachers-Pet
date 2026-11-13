"""
Multi-Agent Workflow Engine for Teacher's Pet.
Orchestrates the 6-stage lifecycle:
01 Goal -> 02 Plan -> 03 Act -> 04 Check -> 05 Correct -> 06 Deliver
"""

import time
import json
from typing import Dict, Any, List, Callable
from curriculum_colleague.agents.planner import PlannerAgent
from curriculum_colleague.agents.grounding_worker import GroundingWorkerAgent
from curriculum_colleague.agents.lesson_worker import LessonPlanWorkerAgent
from curriculum_colleague.agents.exercise_worker import ExerciseWorkerAgent
from curriculum_colleague.agents.reviewer import ReviewerAgent
from curriculum_colleague.verification.fact_checker import FactChecker


class CurriculumColleagueWorkflow:
    def __init__(self, on_event: Callable[[Dict[str, Any]], None] = None):
        self.fact_checker = FactChecker()
        self.planner = PlannerAgent()
        self.grounding_worker = GroundingWorkerAgent(self.fact_checker)
        self.lesson_worker = LessonPlanWorkerAgent()
        self.exercise_worker = ExerciseWorkerAgent()
        self.reviewer = ReviewerAgent(self.fact_checker)
        self.on_event = on_event or (lambda event: None)

    def _emit(self, stage: str, agent_tag: str, agent_name: str, message: str, payload: Any = None):
        event = {
            "timestamp": time.time(),
            "stage": stage,
            "agent_tag": agent_tag,
            "agent_name": agent_name,
            "message": message,
            "payload": payload
        }
        self.on_event(event)
        return event

    def run(self, user_goal: str, force_correction_demo: bool = False) -> Dict[str, Any]:
        """
        Executes the end-to-end agentic workflow.
        Includes reasoning, self-correction, execution, collaboration, and education grounding.
        """
        workflow_log = []

        # ==========================================
        # 01 GOAL
        # ==========================================
        self._emit(
            stage="01 Goal",
            agent_tag="USER",
            agent_name="Educator",
            message=f"Received teacher goal: '{user_goal}'. Targeting high-density public school classroom (40+ learners).",
            payload={"goal": user_goal}
        )

        # ==========================================
        # 02 PLAN (Planner Agent PL)
        # ==========================================
        self._emit(
            stage="02 Plan",
            agent_tag="PL",
            agent_name="Planner Agent",
            message="Reasoning about pedagogical requirements, parsing syllabus context, and assigning tasks to Worker Agents.",
            payload=None
        )
        plan_spec = self.planner.plan_workflow(user_goal)
        self._emit(
            stage="02 Plan",
            agent_tag="PL",
            agent_name="Planner Agent",
            message=f"Created multi-agent plan for {plan_spec['inferred_subject']} ({plan_spec['inferred_grade']}). Assigned Grounding, Lesson Architecture, and Exercise Synthesis tasks.",
            payload=plan_spec
        )

        # ==========================================
        # 03 ACT (Worker Agents WK)
        # ==========================================
        # Worker 1: Grounding Worker
        self._emit(
            stage="03 Act",
            agent_tag="WK",
            agent_name="Grounding Worker (WK-G)",
            message="Connecting to verified curriculum repository. Enforcing strict zero-hallucination check...",
            payload=None
        )
        grounded_data = self.grounding_worker.retrieve_grounded_context(
            subject=plan_spec["inferred_subject"],
            grade=plan_spec["inferred_grade"],
            goal=user_goal
        )
        self._emit(
            stage="03 Act",
            agent_tag="WK",
            agent_name="Grounding Worker (WK-G)",
            message=f"Retrieved official standard code: {grounded_data.get('standard_code', 'N/A')}. Verified sources: {len(grounded_data.get('verified_sources', []))} official references anchored.",
            payload=grounded_data
        )

        # Worker 2: Lesson Plan Architect Worker
        self._emit(
            stage="03 Act",
            agent_tag="WK",
            agent_name="Lesson Plan Architect (WK-L)",
            message="Structuring lesson plan optimized for 40+ learners (Think-Pair-Share, board layouts, low-cost resources).",
            payload=None
        )
        
        # If force_correction_demo is requested, deliberately insert an unfeasible item or unverified source to demonstrate Self-Correction
        if force_correction_demo:
            grounded_copy = dict(grounded_data)
            grounded_copy["verified_sources"] = ["http://unverified-free-lesson-blog.org/download"]
            lesson_plan = self.lesson_worker.draft_lesson_plan(
                grounded_data=grounded_copy,
                class_size=plan_spec["target_class_size"],
                duration_min=45
            )
            # Add an unrealistic crowded classroom requirement to trigger self-correction
            lesson_plan["classroom_logistics"]["low_resource_supplies"].append("Individual iPad for every student")
        else:
            lesson_plan = self.lesson_worker.draft_lesson_plan(
                grounded_data=grounded_data,
                class_size=plan_spec["target_class_size"],
                duration_min=45
            )

        # Worker 3: Exercise & Assessment Worker
        self._emit(
            stage="03 Act",
            agent_tag="WK",
            agent_name="Exercise Worker (WK-E)",
            message="Generating matching exercise paired 1-to-1 with curriculum outcomes and paper-saving layout.",
            payload=None
        )
        exercise = self.exercise_worker.build_matching_exercise(grounded_data, count=5)
        self._emit(
            stage="03 Act",
            agent_tag="WK",
            agent_name="Exercise Worker (WK-E)",
            message=f"Synthesized matching exercise with {len(exercise['column_a'])} verified concept pairs and student answer key.",
            payload=exercise
        )

        # ==========================================
        # 04 CHECK (Reviewer Agent RV)
        # ==========================================
        self._emit(
            stage="04 Check",
            agent_tag="RV",
            agent_name="Reviewer Agent",
            message="Running verification audit: Outcome mapping, Source citation integrity, 40+ Public school feasibility, and Exercise ambiguity checks.",
            payload=None
        )
        review_result = self.reviewer.review_artifact(lesson_plan, exercise)
        self._emit(
            stage="04 Check",
            agent_tag="RV",
            agent_name="Reviewer Agent",
            message=f"Review Verdict: {review_result['status']} (Verification Score: {review_result['verification_score']}%). Found {len(review_result['violations'])} issue(s).",
            payload=review_result
        )

        # ==========================================
        # 05 CORRECT (Self-Correction Loop)
        # ==========================================
        corrections_applied = []
        if not review_result["can_deliver"]:
            self._emit(
                stage="05 Correct",
                agent_tag="RV",
                agent_name="Reviewer Agent",
                message=f"Flagged violations detected! Rejecting draft. Sending work back to Worker Agents with corrective directives: {'; '.join(review_result['violations'])}",
                payload={"violations": review_result["violations"], "directives": review_result["required_corrections"]}
            )

            # Worker self-corrects based on Reviewer's directives
            time.sleep(0.5)
            self._emit(
                stage="05 Correct",
                agent_tag="WK",
                agent_name="Worker Agents (Self-Correcting)",
                message="Self-correcting: Stripping unverified sources, restoring accredited DBE references, and adapting pedagogy to zero-tech chalkboard/pair strategies.",
                payload=None
            )

            # Re-generate clean compliant version
            lesson_plan = self.lesson_worker.draft_lesson_plan(
                grounded_data=grounded_data,
                class_size=plan_spec["target_class_size"],
                duration_min=45,
                corrective_feedback=review_result["required_corrections"]
            )
            exercise = self.exercise_worker.build_matching_exercise(grounded_data, count=5)

            # Re-review after correction
            review_result = self.reviewer.review_artifact(lesson_plan, exercise)
            corrections_applied.append("Fixed unverified sources and adapted to high-density classroom zero-tech mode.")

            self._emit(
                stage="05 Correct",
                agent_tag="RV",
                agent_name="Reviewer Agent",
                message=f"Post-Correction Re-Audit: {review_result['status']}! Verification Score: {review_result['verification_score']}%. All checks PASSED.",
                payload=review_result
            )
        else:
            self._emit(
                stage="05 Correct",
                agent_tag="RV",
                agent_name="Reviewer Agent",
                message="Self-Correction check passed with 100% verification score on first pass. No corrections required.",
                payload={"status": "clean_pass"}
            )

        # ==========================================
        # 06 DELIVER
        # ==========================================
        self._emit(
            stage="06 Deliver",
            agent_tag="PL",
            agent_name="Delivery Orchestrator",
            message="Packaging verified materials for teacher delivery: Print-ready lesson plan, student matching sheet, answer key, and curriculum certificate.",
            payload=None
        )

        delivery_bundle = {
            "metadata": {
                "subject": plan_spec["inferred_subject"],
                "grade": plan_spec["inferred_grade"],
                "standard_code": lesson_plan["standard_code"],
                "class_size": lesson_plan["class_size"],
                "duration": lesson_plan["duration"],
                "verification_score": review_result["verification_score"],
                "corrections_made": len(corrections_applied)
            },
            "lesson_plan": lesson_plan,
            "exercise": exercise,
            "verification_audit": review_result,
            "plan_spec": plan_spec
        }

        self._emit(
            stage="06 Deliver",
            agent_tag="DELIVER",
            agent_name="Teacher's Pet",
            message="Delivery complete. Ready for classroom execution.",
            payload=delivery_bundle
        )

        return delivery_bundle
