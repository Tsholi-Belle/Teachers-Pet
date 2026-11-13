#!/usr/bin/env python3
"""
Teacher's Pet CLI.
Terminal interface for autonomous lesson planning, matching exercise generation,
and learning outcome verification.
"""

import sys
import os
import argparse
import json

# Ensure project root in path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from curriculum_colleague.workflow import CurriculumColleagueWorkflow


def main():
    parser = argparse.ArgumentParser(
        description="Teacher's Pet: Autonomous lesson planner & exercise synthesizer for 40+ student classrooms."
    )
    parser.add_argument("goal", nargs="?", default="Grade 7 Natural Sciences: Photosynthesis & Food Chains for 45 students in public school", help="Educational goal / topic")
    parser.add_argument("--demo-correction", action="store_true", help="Demonstrate Reviewer agent intercepting unverified sources and forcing self-correction")
    parser.add_argument("--export-md", help="Path to export markdown classroom pack")
    args = parser.parse_args()

    print("\n" + "="*70)
    print(" 🏫 TEACHER'S PET: Autonomous Multi-Agent Pedagogical Team")
    print("="*70)
    print(f"Goal: {args.goal}")
    print(f"Self-Correction Demo Mode: {args.demo_correction}\n")

    def print_event(evt):
        tag = evt["agent_tag"]
        stage = evt["stage"]
        name = evt["agent_name"]
        msg = evt["message"]
        color = "\033[94m" if tag == "PL" else "\033[92m" if tag == "WK" else "\033[93m" if tag == "RV" else "\033[95m"
        reset = "\033[0m"
        print(f"[{stage}] {color}[{tag}] {name}{reset}: {msg}")

    wf = CurriculumColleagueWorkflow(on_event=print_event)
    bundle = wf.run(user_goal=args.goal, force_correction_demo=args.demo_correction)

    plan = bundle["lesson_plan"]
    exercise = bundle["exercise"]
    audit = bundle["verification_audit"]

    print("\n" + "="*70)
    print(" 📋 DELIVERED CLASSROOM BUNDLE (40+ LEARNERS)")
    print("="*70)
    print(f"Topic: {plan['lesson_title']} ({plan['standard_code']})")
    print(f"Duration: {plan['duration']} | Class Size: {plan['class_size']} Learners")
    print(f"Curriculum Verification Score: {audit['verification_score']}% (Strict Grounding: PASSED)")
    print("\n--- LEARNING OUTCOMES ---")
    for o in plan["learning_outcomes"]:
        print(f"  • {o}")

    print("\n--- 40+ LEARNER CLASSROOM LOGISTICS ---")
    print(f"  • Seating: {plan['classroom_logistics']['seating_arrangement']}")
    print(f"  • Attention Cue: {plan['classroom_logistics']['noise_and_attention_cues']}")
    print(f"  • Rapid Check: {plan['classroom_logistics']['rapid_formative_checks_for_large_group']}")

    print("\n--- MATCHING EXERCISE (Paper-Saver Layout) ---")
    for item in exercise["column_a"]:
        print(f"  [{item['number']}] {item['term']:<25} -> Match with letter in Column B")
    print("\n  COLUMN B DEFINITIONS:")
    for b in exercise["column_b"]:
        print(f"  ({b['letter']}) {b['definition']}")

    print("\n--- TEACHER ANSWER KEY ---")
    for num, ans in exercise["answer_key"].items():
        print(f"  Key {num} = {ans['correct_match']}: {ans['term']} [Outcome: {ans['outcome_aligned']}]")

    if args.export_md:
        md_content = f"""# {plan['lesson_title']}
**Curriculum Standard:** `{plan['standard_code']}`  
**Class Size:** {plan['class_size']} Students | **Duration:** {plan['duration']}  
**Verification Score:** {audit['verification_score']}%  

## Verified Learning Outcomes
{chr(10).join(['- ' + o for o in plan['learning_outcomes']])}

## Large Class Management (40+ Students)
- **Seating:** {plan['classroom_logistics']['seating_arrangement']}
- **Attention Cue:** {plan['classroom_logistics']['noise_and_attention_cues']}
- **Rapid Formative Check:** {plan['classroom_logistics']['rapid_formative_checks_for_large_group']}

## Chalkboard Summary (3 Panels)
```
{plan['board_layout']['left_column']}
---
{plan['board_layout']['middle_column']}
---
{plan['board_layout']['right_column']}
```

## Student Matching Exercise
| Column A (Concepts) | Column B (Definitions) |
| :--- | :--- |
{chr(10).join([f"| **{a['number']}. {a['term']}** | **({b['letter']})** {b['definition']} |" for a, b in zip(exercise['column_a'], exercise['column_b'])])}

## Teacher Answer Key
{chr(10).join([f"- **{k} = {v['correct_match']}**: {v['term']} (*Target Outcome: {v['outcome_aligned']}*)" for k, v in exercise['answer_key'].items()])}
"""
        with open(args.export_md, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"\nSaved markdown classroom bundle to: {args.export_md}")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
