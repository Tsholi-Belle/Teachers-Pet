"""
Tests for Curriculum Colleague multi-agent engine:
1. Verifies grounding against official database (anti-hallucination)
2. Tests Reviewer rejection of unverified sources
3. Tests Self-Correction loop
4. Tests matching exercise outcome alignment
"""

import sys
import os

# Add root project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from curriculum_colleague.workflow import CurriculumColleagueWorkflow
from curriculum_colleague.verification.fact_checker import FactChecker


def test_standard_workflow():
    print("Testing standard workflow...")
    events = []
    wf = CurriculumColleagueWorkflow(on_event=lambda e: events.append(e))
    bundle = wf.run(
        user_goal="Grade 7 Natural Sciences: Photosynthesis and Food Chains for 45 students in public school",
        force_correction_demo=False
    )
    assert bundle["metadata"]["verification_score"] >= 80
    assert bundle["metadata"]["standard_code"] == "NS-G7-T1-01"
    assert len(bundle["exercise"]["column_a"]) >= 4
    assert bundle["verification_audit"]["can_deliver"] is True
    print("Standard workflow PASSED! Verification score:", bundle["metadata"]["verification_score"])


def test_self_correction_workflow():
    print("\nTesting self-correction loop trigger...")
    events = []
    wf = CurriculumColleagueWorkflow(on_event=lambda e: events.append(e))
    bundle = wf.run(
        user_goal="Grade 7 Natural Sciences: Photosynthesis and Food Chains for 45 students in public school",
        force_correction_demo=True
    )
    # Check that self correction happened
    correction_events = [e for e in events if e["stage"] == "05 Correct"]
    assert len(correction_events) >= 2
    assert bundle["metadata"]["verification_score"] >= 80
    assert bundle["verification_audit"]["can_deliver"] is True
    print("Self-correction workflow PASSED! Verified that problems were flagged, corrected, and delivered.")


def test_anti_hallucination_check():
    print("\nTesting anti-hallucination check...")
    checker = FactChecker()
    fake_plan = {
        "standard_code": "",  # missing code
        "learning_outcomes": ["Only one outcome"],
        "verified_sources": ["http://unknown blog/fake-facts"],
        "matching_exercises": [{"term": "A", "match": "B"}, {"term": "A", "match": "Duplicate"}]  # duplicate term
    }
    audit = checker.verify_lesson_plan(fake_plan)
    assert audit["passed"] is False
    assert len(audit["violations"]) >= 3
    print("Anti-hallucination check PASSED! Flagged violations successfully:", audit["violations"])


if __name__ == "__main__":
    test_standard_workflow()
    test_self_correction_workflow()
    test_anti_hallucination_check()
    print("\nALL UNIT & INTEGRATION TESTS PASSED PERFECTLY!")
