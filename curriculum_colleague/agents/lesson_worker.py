"""
Lesson Plan Architect Worker Agent (WK-L).
Designs comprehensive, practical lesson plans engineered specifically
for public school teachers facing crowded classrooms (40+ students).
"""

from typing import Dict, Any, List


class LessonPlanWorkerAgent:
    def __init__(self):
        self.role = "Lesson Plan Architect Worker"
        self.avatar_tag = "WK"

    def draft_lesson_plan(self, grounded_data: Dict[str, Any], class_size: int = 45, duration_min: int = 45, corrective_feedback: List[str] = None) -> Dict[str, Any]:
        """
        Drafts a lesson plan addressing large class sizes, zero-cost supplies, and clear outcomes.
        Incorporates corrective feedback if provided by the Reviewer Agent.
        """
        topic = grounded_data.get("topic", "General Topic")
        subtopic = grounded_data.get("subtopic", "Core Concepts")
        code = grounded_data.get("standard_code", "GEN-01")
        outcomes = grounded_data.get("learning_outcomes", [])
        concepts = grounded_data.get("key_concepts", [])
        sources = grounded_data.get("verified_sources", [])
        misconceptions = grounded_data.get("common_misconceptions", [])

        # Crowded classroom specific strategies
        classroom_logistics = {
            "seating_arrangement": "Standard dual-desk rows arranged into 'Shoulder Partners' (pairs) and 'Pod of 4' (turn-around desks) for instant peer-checking without moving furniture.",
            "noise_and_attention_cues": "Teacher call-and-response rhythm: 'Eyes on me in 3... 2... 1 (Pencils down, eyes front)'. Avoids shouting over 40+ learners.",
            "low_resource_supplies": [
                "Chalkboard / Whiteboard + Chalk/Markers",
                "Learner Standard Exercise Books & Pens",
                "1 Printable Dual-Side Activity Sheet per pair (Paper-Saver: 1 A4 split into 2 half-sheets = only 23 copies for 45 kids)"
            ],
            "rapid_formative_checks_for_large_group": "Choral response & Finger Voting (Hold up 1, 2, 3, or 4 fingers against the chest to signal option choice simultaneously)."
        }

        # Time breakdown tailored to 45 or 50 minutes
        timeline = [
            {
                "phase": "Phase 1: Hook & Rapid Retrieval",
                "time": "5 mins",
                "teacher_action": "Write provocative 'Brain Starter' question on chalkboard left panel. Ask learners to think for 60 seconds individually.",
                "learner_action": "Whisper answer to shoulder partner for 60 seconds; teacher calls on 2 random pairs using name popsicle sticks / roll call."
            },
            {
                "phase": "Phase 2: Direct Instruction & Board Notes",
                "time": "15 mins",
                "teacher_action": f"Teach core concepts ({', '.join(concepts[:4])}). Explicitly tackle common misconception: '{misconceptions[0] if misconceptions else 'Key conceptual traps'}'. Sketch clear 3-column diagram on board.",
                "learner_action": "Copy structured board summary directly into exercise books. Point to parts with partner as teacher speaks."
            },
            {
                "phase": "Phase 3: Guided Practice (Think-Pair-Share)",
                "time": "10 mins",
                "teacher_action": "Walk center aisle to spot-check comprehension. Address any widespread error to the whole room.",
                "learner_action": "Work in pairs of two to discuss application questions. Compare notes and highlight key vocabulary."
            },
            {
                "phase": "Phase 4: Independent / Paired Formative Matching Check",
                "time": "10 mins",
                "teacher_action": "Direct class to the Matching Exercise on the board or half-sheet handout. Start silent work timer.",
                "learner_action": "Complete matching exercise individually or with partner in exercise books. Swap books for immediate peer-marking."
            },
            {
                "phase": "Phase 5: Consolidation & Exit Ticket",
                "time": "5 mins",
                "teacher_action": "Conduct choral confirmation of matching answers (Call: 'Term 1 is...' Class responds: 'Match B!'). Record overall class confidence level.",
                "learner_action": "Pack books, hand in exit slips or show thumbs up/neutral/down as dismiss signal."
            }
        ]

        board_layout = {
            "left_column": "DATE & KEY VOCABULARY:\n" + "\n".join([f"- {c}" for c in concepts[:6]]),
            "middle_column": f"LESSON SUMMARY & DIAGRAM:\nTopic: {topic}\nOutcomes:\n" + "\n".join([f"1. {o}" for o in outcomes[:2]]),
            "right_column": "CLASSWORK / MATCHING EXERCISE:\n(Refer to Half-Sheet or Board Grid)"
        }

        differentiation = {
            "struggling_learners": "Provide sentence starters for explanations and a pre-printed vocabulary word bank with simplified definitions.",
            "fast_finishers": "Challenge Prompt: Write a 3-sentence explanation predicting what happens to the system if one key variable is removed."
        }

        lesson_plan = {
            "lesson_title": f"{topic}: {subtopic}",
            "standard_code": code,
            "target_grade": "Grade 7",
            "class_size": class_size,
            "duration": f"{duration_min} minutes",
            "learning_outcomes": outcomes,
            "key_concepts": concepts,
            "verified_sources": sources,
            "common_misconceptions": misconceptions,
            "classroom_logistics": classroom_logistics,
            "timeline": timeline,
            "board_layout": board_layout,
            "differentiation": differentiation,
            "notes": "Specifically formatted for public school classrooms with high learner counts."
        }

        if corrective_feedback:
            lesson_plan["revision_history"] = corrective_feedback

        return lesson_plan
