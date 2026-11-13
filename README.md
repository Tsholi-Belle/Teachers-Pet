#  Teacher's Pet

> **Autonomous Multi-Agent Colleague for School Teachers**  
> Tailored specifically for educators in public schools managing overcrowded classes (40+ learners) with limited resources. Autonomously drafts structured lesson plans, builds differentiated matching exercises, and certifies every item against official curriculum learning outcomes with **zero hallucinations or unverified sources**.

[![GitHub Repository](https://img.shields.io/badge/GitHub-Tsholi--Belle%2FTeachers--Pet-blue?logo=github)](https://github.com/Tsholi-Belle/Teachers-Pet)
[![Verification Audit](https://img.shields.io/badge/Grounding%20Audit-100%25%20Verified-emerald)](#-anti-hallucination--zero-unverified-sources-guarantee)
[![Classroom Ready](https://img.shields.io/badge/Classroom%20Size-40%2B%20Learners-pink)](#-purpose-built-for-public-schools-with-40-kids)

---

##  Grounded in the 5 Core Pillars

1. **Reasons**: Rather than reciting a rigid template, the **Planner Agent (`PL`)** dynamically evaluates the teacher's goal, class size constraints (45 learners), and time boundaries to construct an adaptive pedagogical workflow.
2. **Self-Corrects**: The **Reviewer Agent (`RV`)** audits every draft through a 5-point verification engine. If any unverified source, hallucinated curriculum code, or unfeasible high-tech requirement is detected, work is automatically rejected and sent back to workers in the **05 Correct** stage for repair.
3. **Executes**: Completes the multi-step pipeline and produces ready-to-use, print-friendly artifacts (Lesson Plan, Student Matching Activity Sheet, Teacher Answer Key, Verification Certificate).
4. **Collaborates**: Coordinates distinct specialized agent roles:
   - **`PL` Planner Agent**: Decomposes educational outcomes into actionable tasks.
   - **`WK-G` Grounding Worker**: Strictly queries verified curriculum registries (CAPS / NGSS) and whitelisted textbooks.
   - **`WK-L` Lesson Architect Worker**: Structures the 45-minute lesson with 3-panel chalkboard layouts and crowd-management protocols.
   - **`WK-E` Exercise & Assessment Worker**: Synthesizes 1-to-1 concept matching exercises mapped directly to learning outcomes.
   - **`RV` Reviewer Agent**: Checks outputs against verified outcomes, flags violations, and enforces revisions.
5. **Serves Education**: Directly solves the daily workload crisis of public school educators who teach 40+ kids per class without teaching assistants or expensive hardware.

---


##  Anti-Hallucination & Zero-Unverified-Sources Guarantee

Public school teachers face official departmental audits. Fictitious citations or inaccurate concepts damage learning. **Teacher's Pet** enforces:
- **Verified Standard Anchoring**: Every outcome must match an authenticated national curriculum framework (e.g. CAPS Section 3 `NS-G7-T1-01`, NGSS `MS-LS1-6`).
- **Source Whitelist Verification**: All references must cite accredited textbook titles or official department publications (e.g. DBE, Sasol Inzalo, Siyavula). Any unknown URL, blog, or fabricated citation triggers an immediate audit failure.
- **1-to-1 Exercise Validation**: Ensures matching exercise items have unambiguous definitions, no duplicate terms, and explicit outcome mapping.

---

##  Purpose-Built for Public Schools with 40+ Kids

- **Paper-Saver Format**: Formatted for 2-up A5 half-sheets (1 sheet per pair = only 23 photocopies for 45 kids) or direct chalkboard copying.
- **High-Density Seating Protocols**: Uses "Shoulder Partners" (pairs) and "Pods of 4" (turning front desks around) without moving furniture.
- **Rapid Whole-Class Formative Checking**: Choral call-and-response and chest-finger voting to check 45 students in under 90 seconds without marking backlogs.
- **Chalkboard 3-Panel Strategy**: Clear blackboard layouts (Left: Vocabulary, Center: Concept Diagram, Right: Classwork).

---

##  Annual Scope Uploader & Curriculum Accountability Tracker

Public school educators face relentless pressure from departmental audits to complete the syllabus on time despite classroom disruptions, sports days, and high student counts. **Teacher's Pet** integrates an end-to-end Curriculum Scope & Accountability Tracker:

- **Year Scope & Objectives Uploader**:
  - Upload custom school Annual Teaching Plans (ATPs) via **JSON, CSV, or plain text**.
  - One-click Department Presets: Pre-loaded with official **CAPS Grade 7 Natural Sciences ATP (2026)** and **CAPS Grade 8 Mathematics ATP (2026)**.
- **Term-by-Term Objectives Matrix**:
  - Full breakdown across **Term 1, Term 2, Term 3, and Term 4** with weekly pacing targets, expected outcomes, and allocated hours.
  - Interactive completion checkboxes with automatic completion date stamping.
- **Real-Time Pacing & Accountability Engine**:
  - Dynamically calculates syllabus coverage vs. current school calendar week.
  - Pacing Health Badges: **On Track ✅**, **1 Week Behind ⚠️**, or **Critical Lag 🚨**.
  - **Planner Agent (`PL`) Catch-Up Advisories**: When a teacher falls behind schedule, the Planner Agent provides automated consolidation strategies to catch up without sacrificing core learning outcomes.
- **Seamless Lesson Generator Linkage**:
  - Click **"⚡ Draft Lesson"** on any weekly objective in the scope to instantly transfer the exact topic and outcomes into the lesson generator and auto-advance your tracking.

---

##  Pitch Deck & Product Vision

Explore the complete pitch deck detailing the problem statement, solution, and why teachers need this agent:
- 📑 **[Pitch Deck Document (Markdown)](docs/pitch_deck.md)**
- 💻 **[Interactive Pitch Deck (HTML Presentation)](docs/pitch_deck.html)**

---

##  Quickstart Guide

### 1. Web Dashboard (Interactive UI)

Open your browser to: **`(https://teachers-pet-production-0f02b09c.up.railway.app)`**

### 2. Command Line Interface (CLI)
Run directly from terminal:
```bash
# Standard workflow
python3 cli.py "Grade 7 Natural Sciences: Photosynthesis & Food Chains for 45 learners"

# With self-correction demonstration
python3 cli.py --demo-correction

# Export directly to markdown classroom pack
python3 cli.py --export-md sample_lesson.md
```

### 3. Run Automated Tests
```bash
python3 tests/test_agents.py
python3 tests/test_tracker.py
```

---

##  Project Structure

```
Teachers-Pet/
├── app.py                      # Web server & REST API (zero external dependencies)
├── cli.py                      # Interactive CLI tool with colored logging & MD export
├── sample_lesson.md            # Generated verified classroom pack
├── docs/
│   ├── pitch_deck.md           # Full Pitch Deck document
│   └── pitch_deck.html         # Interactive slide presentation
├── curriculum_colleague/
│   ├── workflow.py             # 6-Stage Multi-Agent Orchestrator
│   ├── agents/
│   │   ├── planner.py          # Planner Agent (PL)
│   │   ├── grounding_worker.py # Grounding Worker Agent (WK-G)
│   │   ├── lesson_worker.py    # Lesson Plan Architect Worker (WK-L)
│   │   ├── exercise_worker.py  # Exercise & Assessment Worker (WK-E)
│   │   └── reviewer.py         # Reviewer Agent (RV)
│   └── verification/
│       ├── curriculum_db.json  # Official verified curriculum registry (CAPS, NGSS)
│       └── fact_checker.py     # Anti-hallucination verification auditor
├── static/
│   ├── index.html              # Clean teacher-focused dashboard
│   ├── style.css               # Dark theme & clean print media stylesheet
│   └── app.js                  # Frontend event animation & delivery renderer
└── tests/
    └── test_agents.py          # Unit & integration verification test suite
```

---

##  License
MIT License. Built for educators everywhere.
