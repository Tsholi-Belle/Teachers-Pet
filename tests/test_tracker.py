"""
Unit tests for Annual Curriculum Scope & Accountability Tracker.
"""

import sys
import os

# Add root project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from curriculum_colleague.tracker.scope_tracker import ScopeTracker


def test_preset_and_pacing():
    print("Testing pre-seeded ATP loading and accountability pacing...")
    tracker = ScopeTracker()
    scope = tracker.load_preset("caps_ns_g7")
    assert scope["subject"] == "Natural Sciences"
    assert "Term 1" in scope["terms"]

    # In preset, weeks 1 to 4 are completed
    # If current week is 4, 4 completed vs 4 expected -> ON_TRACK
    acc_week4 = tracker.calculate_accountability(term_name="Term 1", current_week=4)
    assert acc_week4["health_status"] == "ON_TRACK"
    assert acc_week4["pacing_delta_weeks"] >= 0
    print("Week 4 pacing test PASSED (On Track):", acc_week4["health_label"])

    # If current week is 5, 4 completed vs 5 expected -> SLIGHT_DELAY (-1 week)
    acc_week5 = tracker.calculate_accountability(term_name="Term 1", current_week=5)
    assert acc_week5["health_status"] == "SLIGHT_DELAY"
    assert acc_week5["pacing_delta_weeks"] == -1
    print("Week 5 pacing test PASSED (1 Week Behind):", acc_week5["health_label"])

    # If current week is 8, 4 completed vs 8 expected -> CRITICAL_LAG (-4 weeks)
    acc_week8 = tracker.calculate_accountability(term_name="Term 1", current_week=8)
    assert acc_week8["health_status"] == "CRITICAL_LAG"
    assert acc_week8["pacing_delta_weeks"] <= -2
    print("Week 8 pacing test PASSED (Critical Lag):", acc_week8["health_label"])


def test_status_update():
    print("\nTesting objective status update...")
    tracker = ScopeTracker()
    tracker.load_preset("caps_ns_g7")

    # Mark week 5 as completed
    res = tracker.update_objective_status("t1_w5", completed=True, notes="Taught with 3-panel chalkboard.")
    assert res["status"] == "success"
    assert res["objective"]["completed"] is True

    # Re-calculate week 5 pacing: now 5 completed vs 5 expected -> ON_TRACK
    acc = tracker.calculate_accountability(term_name="Term 1", current_week=5)
    assert acc["health_status"] == "ON_TRACK"
    print("Status update test PASSED! Pacing successfully restored to ON_TRACK.")


def test_csv_upload_parsing():
    print("\nTesting CSV scope upload parsing...")
    tracker = ScopeTracker()
    csv_content = """Term,Week,Topic,Objectives,Hours,Completed
Term 1,1,Fractions Introduction,Identify numerator and denominator,4.5,true
Term 1,2,Equivalent Fractions,Simplify fractions using LCD,4.5,false
Term 2,1,Geometry of 2D Shapes,Classify triangles by sides and angles,4.5,false
"""
    result = tracker.upload_scope(csv_content, file_format="csv")
    assert result["status"] == "success"
    parsed_scope = result["scope"]
    assert "Term 1" in parsed_scope["terms"]
    assert len(parsed_scope["terms"]["Term 1"]["weeks"]) == 2
    assert parsed_scope["terms"]["Term 1"]["weeks"][0]["completed"] is True
    print("CSV scope parsing test PASSED! Loaded", len(parsed_scope["terms"]), "terms.")


if __name__ == "__main__":
    test_preset_and_pacing()
    test_status_update()
    test_csv_upload_parsing()
    print("\nALL TRACKER TESTS PASSED PERFECTLY!")
