/**
 * Frontend Orchestrator for Teacher's Pet
 * Handles user interactions, stage animations, log rendering, and delivery tabs.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const goalInput = document.getElementById("goalInput");
  const launchBtn = document.getElementById("launchBtn");
  const eventsLog = document.getElementById("eventsLog");
  const logCount = document.getElementById("logCount");
  const demoCorrectionToggle = document.getElementById("demoCorrectionToggle");
  const printBtn = document.getElementById("printBtn");
  const outputFooter = document.getElementById("outputFooter");

  // Summary pills
  const pillCode = document.getElementById("pillCode");
  const pillScore = document.getElementById("pillScore");
  const pillSize = document.getElementById("pillSize");

  // Tab panes
  const lessonTab = document.getElementById("lesson-tab");
  const exerciseTab = document.getElementById("exercise-tab");
  const answersTab = document.getElementById("answers-tab");
  const auditTab = document.getElementById("audit-tab");

  // Stage cards
  const stageCards = {
    "01 Goal": document.getElementById("stage-01"),
    "02 Plan": document.getElementById("stage-02"),
    "03 Act": document.getElementById("stage-03"),
    "04 Check": document.getElementById("stage-04"),
    "05 Correct": document.getElementById("stage-05"),
    "06 Deliver": document.getElementById("stage-06")
  };

  // Preset Buttons
  document.querySelectorAll(".preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      goalInput.value = btn.dataset.goal;
      goalInput.focus();
    });
  });

  // Tab Switching
  document.querySelectorAll(".tab-btn").forEach(tab => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
      
      tab.classList.add("active");
      const targetPane = document.getElementById(tab.dataset.tab);
      if (targetPane) targetPane.classList.add("active");
    });
  });

  // Print button
  printBtn.addEventListener("click", () => {
    window.print();
  });

  // Launch button
  launchBtn.addEventListener("click", async () => {
    const goal = goalInput.value.trim();
    if (!goal) {
      alert("Please enter a teacher goal or select a quick preset.");
      return;
    }

    const forceCorrection = demoCorrectionToggle.checked;
    resetWorkflowUI();
    launchBtn.disabled = true;
    launchBtn.innerHTML = `<span>⏳</span> Agents Collaborating...`;

    try {
      const response = await fetch("/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal, force_correction: forceCorrection })
      });

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        animateEvents(data.events, data.bundle);
      }
    } catch (err) {
      console.error("Execution failed:", err);
      appendLog("System", "SYS", "Execution Error", `Failed: ${err.message}`, "error");
      launchBtn.disabled = false;
      launchBtn.innerHTML = `<span>⚡</span> Run Teacher's Pet`;
    }
  });

  function resetWorkflowUI() {
    eventsLog.innerHTML = "";
    logCount.textContent = "0 events";
    Object.values(stageCards).forEach(card => {
      if (card) card.classList.remove("active", "completed", "error");
    });
    outputFooter.style.display = "none";
  }

  function animateEvents(events, bundle) {
    let index = 0;
    const interval = setInterval(() => {
      if (index >= events.length) {
        clearInterval(interval);
        launchBtn.disabled = false;
        launchBtn.innerHTML = `<span>⚡</span> Run Teacher's Pet`;
        renderDeliveryBundle(bundle);
        return;
      }

      const evt = events[index];
      processEvent(evt);
      index++;
    }, 450); // slight delay to visibly see the agent hand-off and reasoning
  }

  function processEvent(evt) {
    // Highlight corresponding stage
    const currentCard = stageCards[evt.stage];
    if (currentCard) {
      Object.values(stageCards).forEach(c => c.classList.remove("active"));
      currentCard.classList.add("active");

      if (evt.stage === "05 Correct" && evt.agent_tag === "RV" && evt.payload && evt.payload.violations) {
        currentCard.classList.add("error");
      } else {
        currentCard.classList.remove("error");
        currentCard.classList.add("completed");
      }
    }

    // Add log
    appendLog(evt.agent_name, evt.agent_tag, evt.stage, evt.message);
  }

  function appendLog(agentName, agentTag, stage, message) {
    const entry = document.createElement("div");
    let stageClass = "stage-general";
    if (stage.includes("Plan")) stageClass = "stage-plan";
    if (stage.includes("Act")) stageClass = "stage-act";
    if (stage.includes("Check")) stageClass = "stage-check";
    if (stage.includes("Correct")) stageClass = "stage-correct";
    if (stage.includes("Deliver")) stageClass = "stage-deliver";

    entry.className = `log-entry ${stageClass}`;
    entry.innerHTML = `
      <div class="log-header">
        <span class="log-agent">[${agentTag}] ${agentName}</span>
        <span class="log-time">${stage}</span>
      </div>
      <div class="log-msg">${escapeHtml(message)}</div>
    `;

    eventsLog.appendChild(entry);
    eventsLog.scrollTop = eventsLog.scrollHeight;

    const count = eventsLog.querySelectorAll(".log-entry").length;
    logCount.textContent = `${count} events`;
  }

  function renderDeliveryBundle(bundle) {
    const plan = bundle.lesson_plan;
    const exercise = bundle.exercise;
    const audit = bundle.verification_audit;
    const meta = bundle.metadata;

    // Summary pills
    pillCode.textContent = `Standard: ${meta.standard_code}`;
    pillScore.textContent = `Audit Score: ${meta.verification_score}%`;
    pillSize.textContent = `Class: ${meta.class_size} Learners`;
    outputFooter.style.display = "flex";

    // 1. Render Lesson Plan
    renderLessonPlan(plan);

    // 2. Render Matching Exercise
    renderMatchingExercise(exercise);

    // 3. Render Answer Key & Outcome Mapping
    renderAnswerKey(exercise, plan);

    // 4. Render Verification Audit
    renderVerificationAudit(audit, plan);

    // Switch to first tab
    document.querySelector('.tab-btn[data-tab="lesson-tab"]').click();
  }

  function renderLessonPlan(plan) {
    const timelineRows = plan.timeline.map(t => `
      <tr>
        <td class="timeline-phase">${escapeHtml(t.phase)}</td>
        <td class="timeline-time">${escapeHtml(t.time)}</td>
        <td><strong>Teacher:</strong> ${escapeHtml(t.teacher_action)}<br>
            <span style="color: #94a3b8"><strong>Learners (40+):</strong> ${escapeHtml(t.learner_action)}</span>
        </td>
      </tr>
    `).join("");

    lessonTab.innerHTML = `
      <div class="lesson-card">
        <div class="lesson-meta-grid">
          <div class="meta-item"><strong>Title</strong><span>${escapeHtml(plan.lesson_title)}</span></div>
          <div class="meta-item"><strong>Curriculum Code</strong><span>${escapeHtml(plan.standard_code)}</span></div>
          <div class="meta-item"><strong>Duration</strong><span>${escapeHtml(plan.duration)}</span></div>
          <div class="meta-item"><strong>Class Size</strong><span>${escapeHtml(plan.class_size)} Learners</span></div>
        </div>

        <div class="callout-box">
          <strong>🏫 Public School Classroom Adaptation (40+ Kids):</strong><br>
          • <strong>Seating:</strong> ${escapeHtml(plan.classroom_logistics.seating_arrangement)}<br>
          • <strong>Attention Cue:</strong> ${escapeHtml(plan.classroom_logistics.noise_and_attention_cues)}<br>
          • <strong>Rapid Feedback:</strong> ${escapeHtml(plan.classroom_logistics.rapid_formative_checks_for_large_group)}
        </div>

        <div class="section-block">
          <h4>🎯 Verified Learning Outcomes</h4>
          <ul class="outcomes-list">
            ${plan.learning_outcomes.map(o => `<li>${escapeHtml(o)}</li>`).join("")}
          </ul>
        </div>

        <div class="section-block">
          <h4>⏱️ Large-Class Instructional Timeline</h4>
          <table class="timeline-table">
            <thead>
              <tr><th>Phase</th><th>Timing</th><th>Classroom Actions</th></tr>
            </thead>
            <tbody>${timelineRows}</tbody>
          </table>
        </div>

        <div class="section-block">
          <h4>📝 3-Panel Chalkboard Layout (Zero-Cost Public School Strategy)</h4>
          <div class="board-preview-grid">
            <div class="board-col">
              <h5>PANEL 1 (LEFT)</h5>
              <pre>${escapeHtml(plan.board_layout.left_column)}</pre>
            </div>
            <div class="board-col">
              <h5>PANEL 2 (CENTER DIAGRAM)</h5>
              <pre>${escapeHtml(plan.board_layout.middle_column)}</pre>
            </div>
            <div class="board-col">
              <h5>PANEL 3 (EXERCISE)</h5>
              <pre>${escapeHtml(plan.board_layout.right_column)}</pre>
            </div>
          </div>
        </div>

        <div class="section-block">
          <h4>⚖️ Differentiation for Diverse Pacing</h4>
          <p style="font-size: 0.85rem; color: #cbd5e1;">
            • <strong>Struggling Learners:</strong> ${escapeHtml(plan.differentiation.struggling_learners)}<br>
            • <strong>Fast Finishers:</strong> ${escapeHtml(plan.differentiation.fast_finishers)}
          </p>
        </div>
      </div>
    `;
  }

  function renderMatchingExercise(exercise) {
    const colAItems = exercise.column_a.map(i => `
      <div class="matching-item">
        <span class="item-badge">${escapeHtml(i.number)}</span>
        <div><strong>${escapeHtml(i.term)}</strong></div>
      </div>
    `).join("");

    const colBItems = exercise.column_b.map(i => `
      <div class="matching-item">
        <span class="item-badge" style="background: rgba(236, 72, 153, 0.2); color: #f472b6;">${escapeHtml(i.letter)}</span>
        <div>${escapeHtml(i.definition)}</div>
      </div>
    `).join("");

    exerciseTab.innerHTML = `
      <div class="lesson-card">
        <h3>${escapeHtml(exercise.exercise_title)}</h3>
        <p class="panel-sub">Student Activity Sheet • High-Density Paper-Saver Format</p>

        <div class="callout-box" style="border-left-color: #ec4899; background: rgba(236, 72, 153, 0.08);">
          <strong>📄 School Budget Note:</strong> ${escapeHtml(exercise.paper_saver_guidance)}<br>
          <strong>👥 Peer Checking:</strong> ${escapeHtml(exercise.peer_marking_protocol)}
        </div>

        <div class="matching-container">
          <div class="column-card">
            <h5>Column A: Scientific Concepts</h5>
            ${colAItems}
          </div>
          <div class="column-card">
            <h5>Column B: Verified Definitions (Shuffled)</h5>
            ${colBItems}
          </div>
        </div>

        <div style="margin-top: 20px; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 6px; font-size: 0.85rem;">
          <strong>Student Instruction:</strong> Match each number in Column A with its correct letter from Column B. Write your answer into your exercise book in the format: <em>1 - [Letter], 2 - [Letter]...</em>
        </div>
      </div>
    `;
  }

  function renderAnswerKey(exercise, plan) {
    const answerEntries = Object.entries(exercise.answer_key).map(([num, data]) => `
      <div class="matching-item" style="border-left: 3px solid #10b981;">
        <span class="item-badge" style="background: #10b98133; color: #34d399;">${num} = ${data.correct_match}</span>
        <div style="flex: 1;">
          <strong>${escapeHtml(data.term)}</strong> ➔ ${escapeHtml(data.definition)}<br>
          <span style="font-size: 0.74rem; color: #38bdf8;">Verified Learning Outcome Target: "${escapeHtml(data.outcome_aligned)}"</span>
        </div>
      </div>
    `).join("");

    answersTab.innerHTML = `
      <div class="lesson-card">
        <h3>Teacher Master Answer Key & Curriculum Alignment Matrix</h3>
        <p class="panel-sub">Checks each exercise item against official verified learning outcomes.</p>

        <div style="margin-bottom: 16px;">
          ${answerEntries}
        </div>

        <div class="callout-box" style="border-left-color: #10b981; background: rgba(16, 185, 129, 0.08);">
          <strong>🎯 Rapid Class-wide Choral Correction:</strong><br>
          Teacher calls out: <em>"Number 1: Chlorophyll is..."</em> ➔ Whole class responds in unison: <em>"Letter ${exercise.column_a[0].correct_letter}!"</em>. Corrects 45 students in under 90 seconds without marking backlogs.
        </div>
      </div>
    `;
  }

  function renderVerificationAudit(audit, plan) {
    const checks = audit.checks;
    const scoreColor = audit.verification_score >= 90 ? "#10b981" : "#f59e0b";

    auditTab.innerHTML = `
      <div class="audit-card">
        <div class="audit-score-banner" style="border-color: ${scoreColor}">
          <div>
            <h3>Curriculum Grounding & Anti-Hallucination Audit</h3>
            <p style="font-size: 0.84rem; color: #94a3b8;">Automated verification against official Department of Basic Education standards.</p>
          </div>
          <div class="score-text">
            <strong>${audit.verification_score}%</strong>
            <div style="font-size: 0.75rem; text-align: right; color: ${scoreColor}">${audit.status}</div>
          </div>
        </div>

        <div class="section-block">
          <h4>Audit Checkpoints</h4>
          <div class="check-item">
            <span class="icon">${checks.curriculum_grounding ? "✅" : "❌"}</span>
            <div>
              <strong>Official Curriculum Standard Code:</strong>
              <span style="color: #94a3b8">Anchored to authorized standard <code>${escapeHtml(plan.standard_code)}</code></span>
            </div>
          </div>
          <div class="check-item">
            <span class="icon">${checks.source_verification ? "✅" : "❌"}</span>
            <div>
              <strong>Strict Source Whitelist:</strong>
              <span style="color: #94a3b8">Zero unverified links or blogs. Citing: <em>${plan.verified_sources.join(", ")}</em></span>
            </div>
          </div>
          <div class="check-item">
            <span class="icon">${checks.crowded_class_40plus ? "✅" : "❌"}</span>
            <div>
              <strong>40+ Learner Public School Feasibility:</strong>
              <span style="color: #94a3b8">Enforces zero-cost supplies, pair-work, chalkboard layouts, and paper-saving formats.</span>
            </div>
          </div>
          <div class="check-item">
            <span class="icon">${checks.exercise_integrity ? "✅" : "❌"}</span>
            <div>
              <strong>Exercise Structural Integrity:</strong>
              <span style="color: #94a3b8">Checked for zero duplicates, 1-to-1 unambiguous matching keys, and outcome alignment.</span>
            </div>
          </div>
        </div>

        ${audit.violations && audit.violations.length > 0 ? `
          <div class="callout-box" style="border-left-color: #ef4444; background: rgba(239, 68, 68, 0.08); margin-top: 14px;">
            <strong>Violations Flagged & Repaired:</strong>
            <ul style="padding-left: 18px; margin-top: 6px;">
              ${audit.violations.map(v => `<li>${escapeHtml(v)}</li>`).join("")}
            </ul>
          </div>
        ` : `
          <div class="callout-box" style="border-left-color: #10b981; background: rgba(16, 185, 129, 0.08); margin-top: 14px;">
            <strong>Anti-Hallucination Guarantee:</strong> All learning outcomes, concepts, and teacher strategies strictly verified. Zero hallucinated citations or unverified assertions detected.
          </div>
        `}
      </div>
    `;
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
});
