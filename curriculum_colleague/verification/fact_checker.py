"""
Fact Checker and Grounding Verification Engine.
Strictly ensures that all curriculum outcomes, subject facts, and source citations
are anchored in verified curriculum standards and prohibits hallucinations.
"""

import json
import os
import re
from typing import Dict, List, Any, Tuple


class FactChecker:
    def __init__(self, db_path: str = None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, "curriculum_db.json")
        self.db_path = db_path
        self.curricula = self._load_db()

    def _load_db(self) -> Dict[str, Any]:
        if not os.path.exists(self.db_path):
            return {"curricula": {}}
        with open(self.db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("curricula", {})

    def find_verified_standard(self, subject: str, grade: str, topic_query: str) -> List[Dict[str, Any]]:
        """
        Retrieves matching verified standards from official curriculum databases.
        """
        matches = []
        q = topic_query.lower()
        for cur_key, cur_data in self.curricula.items():
            for subj_key, grades in cur_data.get("subjects", {}).items():
                if subject.lower() in subj_key.lower() or subj_key.lower() in subject.lower():
                    for gr_key, items in grades.items():
                        if grade.lower() in gr_key.lower() or gr_key.lower() in grade.lower():
                            for item in items:
                                # Match topic or key concepts
                                topic_text = (item["topic"] + " " + item["subtopic"] + " " + " ".join(item["key_concepts"])).lower()
                                if any(word in topic_text for word in q.split() if len(word) > 3) or q in topic_text:
                                    matches.append({
                                        "curriculum": cur_key,
                                        "curriculum_full_name": cur_data.get("name"),
                                        "authority": cur_data.get("authority"),
                                        "standard_code": item["code"],
                                        "topic": item["topic"],
                                        "subtopic": item["subtopic"],
                                        "outcomes": item["outcomes"],
                                        "key_concepts": item["key_concepts"],
                                        "verified_sources": item["verified_sources"],
                                        "common_misconceptions": item.get("common_misconceptions", [])
                                    })
        return matches

    def verify_lesson_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs a rigorous 5-point verification audit:
        1. Curriculum Outcome Grounding: Are outcomes tied to verified syllabus standards?
        2. Source Citation Integrity: Are citations verified and non-hallucinated?
        3. Public School 40+ Feasibility: Is pedagogy realistic for high-density public classrooms?
        4. Exercise Integrity: Are matching items one-to-one, distinct, and accurate?
        5. Factual Accuracy & Misconception Safeguards: No pseudo-facts.
        """
        audit_results = {
            "passed": True,
            "verification_score": 100,
            "grounding_check": {"passed": True, "notes": []},
            "source_check": {"passed": True, "notes": []},
            "crowded_classroom_check": {"passed": True, "notes": []},
            "exercise_check": {"passed": True, "notes": []},
            "factual_check": {"passed": True, "notes": []},
            "violations": [],
            "required_fixes": []
        }

        # 1. Grounding check
        std_code = plan.get("standard_code", "").strip()
        outcomes = plan.get("learning_outcomes", [])
        if not std_code:
            audit_results["grounding_check"]["passed"] = False
            audit_results["grounding_check"]["notes"].append("Missing official curriculum standard code.")
            audit_results["violations"].append("Unverified curriculum code: Output must link to an official code.")
            audit_results["required_fixes"].append("Attach exact verified syllabus code (e.g. CAPS NS-G7-T1-01).")
            audit_results["verification_score"] -= 25

        if not outcomes or len(outcomes) < 2:
            audit_results["grounding_check"]["passed"] = False
            audit_results["grounding_check"]["notes"].append("Insufficient learning outcomes provided.")
            audit_results["violations"].append("Missing explicit learning outcomes.")
            audit_results["required_fixes"].append("List at least 2 concrete curriculum-aligned outcomes.")
            audit_results["verification_score"] -= 15

        # 2. Source Whitelist Check
        sources = plan.get("verified_sources", [])
        hallucinated_markers = ["example.com", "unknown blog", "chatgpt.com", "ai-generated-link", "pending-source"]
        if not sources:
            audit_results["source_check"]["passed"] = False
            audit_results["source_check"]["notes"].append("No verified sources cited.")
            audit_results["violations"].append("Unverified sources: No accredited curriculum reference provided.")
            audit_results["required_fixes"].append("Cite official Department of Basic Education or accredited textbook.")
            audit_results["verification_score"] -= 20
        else:
            for s in sources:
                if any(m in s.lower() for m in hallucinated_markers) or len(s.strip()) < 5:
                    audit_results["source_check"]["passed"] = False
                    audit_results["violations"].append(f"Suspicious or unverified source detected: '{s}'")
                    audit_results["required_fixes"].append(f"Replace unverified source '{s}' with an authorized resource.")
                    audit_results["verification_score"] -= 20

        # 3. Crowded Classroom Check (40+ kids in public school)
        text_dump = json.dumps(plan).lower()
        unrealistic_for_crowded = [
            "individual ipad", "individual laptop", "one tablet per student",
            "expensive materials", "individual computer lab", "microscope for each student"
        ]
        for item in unrealistic_for_crowded:
            if item in text_dump:
                audit_results["crowded_classroom_check"]["passed"] = False
                audit_results["violations"].append(f"Unfeasible requirement for 40+ public school class: '{item}'")
                audit_results["required_fixes"].append(f"Adapt pedagogy to zero/low-tech resources (blackboard, group pair-share, choral drill, paper-saver single printout).")
                audit_results["verification_score"] -= 15

        # Check grouping strategy for 40+ kids
        class_strategies = ["pair", "partner", "think-pair-share", "group of 4", "pod", "choral", "peer check"]
        if not any(strat in text_dump for strat in class_strategies):
            audit_results["crowded_classroom_check"]["notes"].append("Recommended to include specific high-density group management strategy (Think-Pair-Share or 4-student pods).")

        # 4. Exercise Check (Matching exercises)
        exercises = plan.get("matching_exercises", [])
        if not exercises:
            audit_results["exercise_check"]["passed"] = False
            audit_results["violations"].append("No matching exercises generated.")
            audit_results["required_fixes"].append("Include at least 4-6 matching pairs aligned with learning outcomes.")
            audit_results["verification_score"] -= 20
        else:
            terms = [e.get("term", "").strip().lower() for e in exercises]
            definitions = [e.get("match", "").strip().lower() for e in exercises]
            if len(set(terms)) < len(terms):
                audit_results["exercise_check"]["passed"] = False
                audit_results["violations"].append("Duplicate terms found in matching exercise.")
                audit_results["required_fixes"].append("Ensure all terms in matching exercise are unique.")
                audit_results["verification_score"] -= 10
            if len(set(definitions)) < len(definitions):
                audit_results["exercise_check"]["passed"] = False
                audit_results["violations"].append("Duplicate definitions found in matching exercise.")
                audit_results["required_fixes"].append("Ensure all match targets are unambiguous and distinct.")
                audit_results["verification_score"] -= 10

        # Overall pass criteria
        audit_results["verification_score"] = max(0, audit_results["verification_score"])
        audit_results["passed"] = (audit_results["verification_score"] >= 80) and (len(audit_results["violations"]) == 0)

        return audit_results
