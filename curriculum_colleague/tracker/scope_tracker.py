"""
Annual Curriculum Scope & Accountability Pacing Tracker for Teacher's Pet.
Allows teachers to upload or select their Annual Teaching Plan (ATP),
tracks term-by-term expected objectives, and audits pacing against official deadlines.
"""

import json
import os
import csv
import io
import time
from typing import Dict, Any, List, Optional


class ScopeTracker:
    def __init__(self, storage_path: Optional[str] = None):
        if storage_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            storage_path = os.path.join(base_dir, "active_scope.json")
        self.storage_path = storage_path
        self.current_scope = self._load_storage()

    def _load_storage(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        # Default to pre-seeded CAPS Grade 7 Natural Sciences ATP
        return self.get_preset_scope("caps_ns_g7")

    def save_storage(self) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.current_scope, f, indent=2)

    def get_preset_scope(self, preset_id: str) -> Dict[str, Any]:
        """Returns official pre-seeded Annual Teaching Plans (ATPs)."""
        presets = {
            "caps_ns_g7": {
                "id": "caps_ns_g7",
                "title": "CAPS Natural Sciences Grade 7 Annual Teaching Plan",
                "authority": "Department of Basic Education",
                "grade": "Grade 7",
                "subject": "Natural Sciences",
                "academic_year": "2026",
                "terms": {
                    "Term 1": {
                        "name": "Life and Living (Biosphere & Biodiversity)",
                        "weeks_count": 10,
                        "weeks": [
                            {
                                "week": 1,
                                "id": "t1_w1",
                                "topic": "The Biosphere",
                                "objectives": [
                                    "Define the biosphere and its three components (lithosphere, hydrosphere, atmosphere).",
                                    "Identify requirements for sustaining life on Earth."
                                ],
                                "hours_allocated": 3.5,
                                "completed": True,
                                "date_completed": "2026-01-22",
                                "notes": "Covered via 3-panel chalkboard diagram."
                            },
                            {
                                "week": 2,
                                "id": "t1_w2",
                                "topic": "Biodiversity and Classification",
                                "objectives": [
                                    "Classify organisms into the five kingdoms.",
                                    "Distinguish between vertebrates and invertebrates."
                                ],
                                "hours_allocated": 3.5,
                                "completed": True,
                                "date_completed": "2026-01-29",
                                "notes": "Learners completed paired classification exercise."
                            },
                            {
                                "week": 3,
                                "id": "t1_w3",
                                "topic": "Sexual Reproduction in Angiosperms",
                                "objectives": [
                                    "Identify flower structures: sepals, petals, stamens, and pistil.",
                                    "Describe the process of pollination and fertilization."
                                ],
                                "hours_allocated": 3.5,
                                "completed": True,
                                "date_completed": "2026-02-05",
                                "notes": "Live hibiscus flower observation."
                            },
                            {
                                "week": 4,
                                "id": "t1_w4",
                                "topic": "Photosynthesis and Food Production",
                                "objectives": [
                                    "Explain the process of photosynthesis: chlorophyll, sunlight, CO2, water -> glucose + oxygen.",
                                    "Identify oxygen as the by-product of photosynthesis.",
                                    "Differentiate between photosynthesis and respiration."
                                ],
                                "hours_allocated": 3.5,
                                "completed": True,
                                "date_completed": "2026-02-12",
                                "notes": "Generated and verified with Teacher's Pet."
                            },
                            {
                                "week": 5,
                                "id": "t1_w5",
                                "topic": "Respiration in Living Organisms",
                                "objectives": [
                                    "Explain cellular respiration as energy release from food.",
                                    "Compare inhaled vs exhaled air composition."
                                ],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 6,
                                "id": "t1_w6",
                                "topic": "Ecosystems and Trophic Levels",
                                "objectives": [
                                    "Classify producers, primary, secondary, and tertiary consumers.",
                                    "Explain decomposers and nutrient recycling."
                                ],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 7,
                                "id": "t1_w7",
                                "topic": "Food Chains and Food Webs",
                                "objectives": [
                                    "Construct food chains showing correct arrow direction of energy flow.",
                                    "Analyze impact of disruptions in food webs."
                                ],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 8,
                                "id": "t1_w8",
                                "topic": "Adaptations and Survival",
                                "objectives": [
                                    "Describe structural adaptations of plants (xerophytes, hydrophytes).",
                                    "Describe camouflage and behavioral adaptations in animals."
                                ],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 9,
                                "id": "t1_w9",
                                "topic": "Formal Assessment Preparation & Consolidation",
                                "objectives": [
                                    "Revise Biosphere, Photosynthesis, Respiration, and Ecosystems.",
                                    "Address common diagnostic misconception traps."
                                ],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 10,
                                "id": "t1_w10",
                                "topic": "Term 1 Formal Assessment Task (FAT 1)",
                                "objectives": [
                                    "Administer standardized Term 1 Test (Department moderated).",
                                    "Record marks and compile diagnostic error analysis."
                                ],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            }
                        ]
                    },
                    "Term 2": {
                        "name": "Matter and Materials",
                        "weeks_count": 10,
                        "weeks": [
                            {
                                "week": 1,
                                "id": "t2_w1",
                                "topic": "Properties of Materials",
                                "objectives": ["Distinguish physical properties: strength, flexibility, thermal & electrical conductivity."],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 2,
                                "id": "t2_w2",
                                "topic": "Separating Mixtures",
                                "objectives": ["Demonstrate methods of separating mixtures: filtration, evaporation, distillation, chromatography."],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 3,
                                "id": "t2_w3",
                                "topic": "Acids, Bases, and Neutral Substances",
                                "objectives": ["Identify properties of acids and bases using litmus paper indicators."],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 4,
                                "id": "t2_w4",
                                "topic": "The Periodic Table of Elements",
                                "objectives": ["Interpret symbols and atomic numbers for first 20 elements on the periodic table."],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            }
                        ]
                    },
                    "Term 3": {
                        "name": "Energy and Change",
                        "weeks_count": 10,
                        "weeks": [
                            {
                                "week": 1,
                                "id": "t3_w1",
                                "topic": "Sources of Energy & Heat Transfer",
                                "objectives": ["Explain conduction, convection, and radiation in everyday contexts."],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 2,
                                "id": "t3_w2",
                                "topic": "Insulation and Energy Conservation",
                                "objectives": ["Design an insulated solar cooker or thermos cup model using low-cost recycled materials."],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            }
                        ]
                    },
                    "Term 4": {
                        "name": "Planet Earth and Beyond",
                        "weeks_count": 10,
                        "weeks": [
                            {
                                "week": 1,
                                "id": "t4_w1",
                                "topic": "Relationship of the Sun, Earth, and Moon",
                                "objectives": ["Explain day/night cycles, seasons, and solar/lunar eclipses."],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 2,
                                "id": "t4_w2",
                                "topic": "Historical and Modern Astronomy",
                                "objectives": ["Describe Indigenous knowledge of astronomy (e.g. Pleiades/IsiLimela) alongside modern telescopes (SALT)."],
                                "hours_allocated": 3.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            }
                        ]
                    }
                }
            },
            "caps_math_g8": {
                "id": "caps_math_g8",
                "title": "CAPS Mathematics Grade 8 Annual Teaching Plan",
                "authority": "Department of Basic Education",
                "grade": "Grade 8",
                "subject": "Mathematics",
                "academic_year": "2026",
                "terms": {
                    "Term 1": {
                        "name": "Numbers, Operations & Relationships",
                        "weeks_count": 10,
                        "weeks": [
                            {
                                "week": 1,
                                "id": "m_t1_w1",
                                "topic": "Whole Numbers and Calculations",
                                "objectives": ["Prime factors, LCM and HCF of 3-digit numbers."],
                                "hours_allocated": 4.5,
                                "completed": True,
                                "date_completed": "2026-01-22",
                                "notes": ""
                            },
                            {
                                "week": 2,
                                "id": "m_t1_w2",
                                "topic": "Integers and Signed Numbers",
                                "objectives": ["Add, subtract, multiply, and divide integers with negative signs."],
                                "hours_allocated": 4.5,
                                "completed": True,
                                "date_completed": "2026-01-29",
                                "notes": ""
                            },
                            {
                                "week": 3,
                                "id": "m_t1_w3",
                                "topic": "Exponents and Scientific Notation",
                                "objectives": ["Laws of exponents for integer exponents."],
                                "hours_allocated": 4.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            },
                            {
                                "week": 4,
                                "id": "m_t1_w4",
                                "topic": "Numeric and Geometric Patterns",
                                "objectives": ["Determine general rule Tn = an + c for linear sequences."],
                                "hours_allocated": 4.5,
                                "completed": False,
                                "date_completed": None,
                                "notes": ""
                            }
                        ]
                    }
                }
            }
        }
        return presets.get(preset_id, presets["caps_ns_g7"])

    def load_preset(self, preset_id: str) -> Dict[str, Any]:
        """Sets the active scope to an official department preset."""
        preset = self.get_preset_scope(preset_id)
        self.current_scope = preset
        self.save_storage()
        return self.current_scope

    def upload_scope(self, raw_content: str, file_format: str = "json") -> Dict[str, Any]:
        """
        Parses an uploaded scope from JSON, CSV, or formatted text.
        Converts it into standardized Scope & Term Objectives structure.
        """
        if file_format == "json" or raw_content.strip().startswith("{"):
            try:
                parsed = json.loads(raw_content)
                # Validate structure
                if "terms" not in parsed:
                    raise ValueError("JSON scope must contain a 'terms' key.")
                self.current_scope = parsed
                self.save_storage()
                return {"status": "success", "message": "Uploaded JSON Scope loaded successfully.", "scope": self.current_scope}
            except Exception as e:
                return {"status": "error", "message": f"Failed to parse JSON scope: {str(e)}"}

        elif file_format == "csv" or "\n" in raw_content and ("," in raw_content or "\t" in raw_content):
            try:
                reader = csv.DictReader(io.StringIO(raw_content))
                terms = {}
                for idx, row in enumerate(reader, 1):
                    term_name = row.get("Term", row.get("term", "Term 1")).strip()
                    if term_name not in terms:
                        terms[term_name] = {"name": f"Curriculum Scope {term_name}", "weeks_count": 0, "weeks": []}
                    
                    week_num = int(row.get("Week", row.get("week", len(terms[term_name]["weeks"]) + 1)))
                    topic = row.get("Topic", row.get("topic", f"Topic {week_num}"))
                    objs_raw = row.get("Objectives", row.get("objectives", ""))
                    objectives = [o.strip() for o in objs_raw.split(";") if o.strip()] or [topic]
                    
                    terms[term_name]["weeks"].append({
                        "week": week_num,
                        "id": f"{term_name.lower().replace(' ', '_')}_w{week_num}",
                        "topic": topic,
                        "objectives": objectives,
                        "hours_allocated": float(row.get("Hours", 3.5)),
                        "completed": row.get("Completed", "false").lower() in ["true", "1", "yes"],
                        "date_completed": row.get("DateCompleted", None),
                        "notes": row.get("Notes", "")
                    })
                    terms[term_name]["weeks_count"] = len(terms[term_name]["weeks"])

                self.current_scope = {
                    "id": f"custom_upload_{int(time.time())}",
                    "title": "Teacher Uploaded Annual Curriculum Scope",
                    "authority": "Teacher Custom Upload",
                    "grade": "Uploaded Grade",
                    "subject": "Uploaded Subject",
                    "academic_year": "2026",
                    "terms": terms
                }
                self.save_storage()
                return {"status": "success", "message": "Uploaded CSV Scope converted successfully.", "scope": self.current_scope}
            except Exception as e:
                return {"status": "error", "message": f"Failed to parse CSV scope: {str(e)}"}

        else:
            # Parse text line by line
            lines = [l.strip() for l in raw_content.splitlines() if l.strip()]
            weeks = []
            curr_week = 1
            for l in lines:
                parts = l.split(":", 1) if ":" in l else (f"Week {curr_week}", l)
                topic = parts[0].strip()
                desc = parts[1].strip() if len(parts) > 1 else topic
                weeks.append({
                    "week": curr_week,
                    "id": f"t1_w{curr_week}",
                    "topic": topic,
                    "objectives": [desc],
                    "hours_allocated": 3.5,
                    "completed": False,
                    "date_completed": None,
                    "notes": ""
                })
                curr_week += 1

            self.current_scope = {
                "id": f"text_upload_{int(time.time())}",
                "title": "Teacher Custom Curriculum Scope",
                "authority": "Teacher Custom Text",
                "grade": "Grade 7-9",
                "subject": "General",
                "academic_year": "2026",
                "terms": {
                    "Term 1": {
                        "name": "Custom Syllabus Scope",
                        "weeks_count": len(weeks),
                        "weeks": weeks
                    }
                }
            }
            self.save_storage()
            return {"status": "success", "message": "Uploaded plain text converted to Term 1 scope.", "scope": self.current_scope}

    def update_objective_status(self, objective_id: str, completed: bool, notes: str = "") -> Dict[str, Any]:
        """Toggles or updates the completion status of a specific weekly curriculum objective."""
        found = False
        target_obj = None
        for term_key, term_data in self.current_scope.get("terms", {}).items():
            for item in term_data.get("weeks", []):
                if item["id"] == objective_id:
                    item["completed"] = completed
                    item["date_completed"] = time.strftime("%Y-%m-%d") if completed else None
                    if notes:
                        item["notes"] = notes
                    found = True
                    target_obj = item
                    break
            if found:
                break

        if found:
            self.save_storage()
            return {"status": "success", "objective": target_obj}
        return {"status": "error", "message": f"Objective ID '{objective_id}' not found."}

    def calculate_accountability(self, term_name: str = "Term 1", current_week: int = 5) -> Dict[str, Any]:
        """
        Calculates pacing against the official Annual Scope:
        - Target expected completion by week N
        - Actual completed objectives
        - Pacing Delta (e.g. 0 = on track, -1 = 1 week behind schedule, +1 = ahead)
        - Catch-up advisory from Planner Agent (PL)
        """
        term_data = self.current_scope.get("terms", {}).get(term_name, {})
        if not term_data:
            return {
                "status": "error",
                "message": f"Term '{term_name}' not found in active scope."
            }

        weeks = term_data.get("weeks", [])
        total_weeks = len(weeks)
        if total_weeks == 0:
            return {"status": "empty", "message": "No weeks found in term."}

        # Count completed
        completed_count = sum(1 for w in weeks if w.get("completed", False))
        expected_completed = min(current_week, total_weeks)

        pacing_delta_weeks = completed_count - expected_completed
        completion_percentage = round((completed_count / total_weeks) * 100, 1)

        # Determine health status
        if pacing_delta_weeks >= 0:
            health_status = "ON_TRACK"
            health_label = "On Track & Pacing Well"
            badge_color = "emerald"
            advisory = "You are on schedule with the official curriculum scope! Maintain current pacing and continue formative checks."
        elif pacing_delta_weeks == -1:
            health_status = "SLIGHT_DELAY"
            health_label = "1 Week Behind Schedule"
            badge_color = "amber"
            advisory = "Curriculum pacing alert: 1 week behind official ATP. Recommended Catch-Up Strategy: Consolidate next week's vocabulary with a double-concept 3-panel chalkboard diagram to recover the pacing buffer."
        else:
            health_status = "CRITICAL_LAG"
            health_label = f"{abs(pacing_delta_weeks)} Weeks Behind Schedule"
            badge_color = "red"
            advisory = f"URGENT PACING WARNING: {abs(pacing_delta_weeks)} weeks behind Department ATP. Recommended Catch-Up Strategy: Activate Teacher's Pet Accelerated Paired Modules to combine upcoming subtopics and run high-speed choral formative checks."

        return {
            "term": term_name,
            "current_week": current_week,
            "total_weeks": total_weeks,
            "completed_count": completed_count,
            "expected_completed": expected_completed,
            "pacing_delta_weeks": pacing_delta_weeks,
            "completion_percentage": completion_percentage,
            "health_status": health_status,
            "health_label": health_label,
            "badge_color": badge_color,
            "planner_advisory": advisory,
            "weeks_data": weeks
        }
