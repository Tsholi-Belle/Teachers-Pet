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
    launchBtn.innerHTML = `Agents Collaborating...`;

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
      launchBtn.innerHTML = `Run Teacher's Pet`;
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
        launchBtn.innerHTML = `Run Teacher's Pet`;
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
            <span style="color: #94a3b8"><strong>Learners:</strong> ${escapeHtml(t.learner_action)}</span>
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
          <strong>Public School Classroom Adaptation:</strong><br>
          • <strong>Seating:</strong> ${escapeHtml(plan.classroom_logistics.seating_arrangement)}<br>
          • <strong>Attention Cue:</strong> ${escapeHtml(plan.classroom_logistics.noise_and_attention_cues)}<br>
          • <strong>Rapid Feedback:</strong> ${escapeHtml(plan.classroom_logistics.rapid_formative_checks_for_large_group)}
        </div>

        <div class="section-block">
          <h4>Verified Learning Outcomes</h4>
          <ul class="outcomes-list">
            ${plan.learning_outcomes.map(o => `<li>${escapeHtml(o)}</li>`).join("")}
          </ul>
        </div>

        <div class="section-block">
          <h4>Large-Class Instructional Timeline</h4>
          <table class="timeline-table">
            <thead>
              <tr><th>Phase</th><th>Timing</th><th>Classroom Actions</th></tr>
            </thead>
            <tbody>${timelineRows}</tbody>
          </table>
        </div>

        <div class="section-block">
          <h4>3-Panel Chalkboard Layout (Zero-Cost Public School Strategy)</h4>
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
          <h4>Differentiation for Diverse Pacing</h4>
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
          <strong>School Budget Note:</strong> ${escapeHtml(exercise.paper_saver_guidance)}<br>
          <strong>Peer Checking:</strong> ${escapeHtml(exercise.peer_marking_protocol)}
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
          <strong>Rapid Class-wide Choral Correction:</strong><br>
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
            <span class="pacing-badge ${checks.curriculum_grounding ? 'on-track' : 'critical'}">${checks.curriculum_grounding ? "PASS" : "FAIL"}</span>
            <div>
              <strong>Official Curriculum Standard Code:</strong>
              <span style="color: #94a3b8">Anchored to authorized standard <code>${escapeHtml(plan.standard_code)}</code></span>
            </div>
          </div>
          <div class="check-item">
            <span class="pacing-badge ${checks.source_verification ? 'on-track' : 'critical'}">${checks.source_verification ? "PASS" : "FAIL"}</span>
            <div>
              <strong>Strict Source Whitelist:</strong>
              <span style="color: #94a3b8">Zero unverified links or blogs. Citing: <em>${plan.verified_sources.join(", ")}</em></span>
            </div>
          </div>
          <div class="check-item">
            <span class="pacing-badge ${checks.crowded_class_40plus ? 'on-track' : 'critical'}">${checks.crowded_class_40plus ? "PASS" : "FAIL"}</span>
            <div>
              <strong>Public School Feasibility:</strong>
              <span style="color: #94a3b8">Enforces zero-cost supplies, pair-work, chalkboard layouts, and paper-saving formats.</span>
            </div>
          </div>
          <div class="check-item">
            <span class="pacing-badge ${checks.exercise_integrity ? 'on-track' : 'critical'}">${checks.exercise_integrity ? "PASS" : "FAIL"}</span>
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

  // =========================================================
  // Scope & Accountability Tracker Logic
  // =========================================================
  let currentActiveTerm = "Term 1";
  let activeScopeData = null;

  function initScopeTracker() {
    // 1. View Navigation
    document.querySelectorAll(".nav-pill-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".nav-pill-btn").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".app-view").forEach(v => v.style.display = "none");

        btn.classList.add("active");
        const targetView = document.getElementById(btn.dataset.view);
        if (targetView) targetView.style.display = "block";

        if (btn.dataset.view === "tracker-view") {
          fetchScopeAndRender();
        }
      });
    });

    // 2. Week Select Listener
    const currentWeekSelect = document.getElementById("currentWeekSelect");
    if (currentWeekSelect) {
      currentWeekSelect.addEventListener("change", () => {
        updateAccountability(currentActiveTerm, parseInt(currentWeekSelect.value));
      });
    }

    // 3. Term Tabs
    document.querySelectorAll(".term-tab-btn").forEach(tab => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".term-tab-btn").forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        currentActiveTerm = tab.dataset.term;
        renderCurrentTermObjectives();
        const currentWeek = parseInt(document.getElementById("currentWeekSelect").value || "4");
        updateAccountability(currentActiveTerm, currentWeek);
      });
    });

    // 4. Upload Drawer Controls
    const toggleUploadBtn = document.getElementById("toggleUploadBtn");
    const uploadDrawer = document.getElementById("uploadDrawer");
    const cancelUploadBtn = document.getElementById("cancelUploadBtn");
    const submitScopeUploadBtn = document.getElementById("submitScopeUploadBtn");
    const browseFileBtn = document.getElementById("browseFileBtn");
    const scopeFileInput = document.getElementById("scopeFileInput");
    const dropZone = document.getElementById("dropZone");
    const scopePasteInput = document.getElementById("scopePasteInput");
    const presetScopeSelect = document.getElementById("presetScopeSelect");

    if (toggleUploadBtn && uploadDrawer) {
      toggleUploadBtn.addEventListener("click", () => {
        uploadDrawer.style.display = uploadDrawer.style.display === "none" ? "block" : "none";
      });
    }

    if (cancelUploadBtn && uploadDrawer) {
      cancelUploadBtn.addEventListener("click", () => {
        uploadDrawer.style.display = "none";
      });
    }

    if (browseFileBtn && scopeFileInput) {
      browseFileBtn.addEventListener("click", () => scopeFileInput.click());
      scopeFileInput.addEventListener("change", handleFileUpload);
    }

    if (dropZone) {
      dropZone.addEventListener("dragover", e => { e.preventDefault(); dropZone.classList.add("dragover"); });
      dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
      dropZone.addEventListener("drop", e => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
          readFileAndUpload(e.dataTransfer.files[0]);
        }
      });
    }

    if (submitScopeUploadBtn) {
      submitScopeUploadBtn.addEventListener("click", async () => {
        const text = scopePasteInput.value.trim();
        if (!text) {
          alert("Please paste scope text or upload a JSON/CSV file.");
          return;
        }
        await uploadScopeContent(text, text.startsWith("{") ? "json" : "text");
        uploadDrawer.style.display = "none";
        scopePasteInput.value = "";
      });
    }

    if (presetScopeSelect) {
      presetScopeSelect.addEventListener("change", async () => {
        const presetId = presetScopeSelect.value;
        try {
          const res = await fetch("/api/scope/preset", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ preset_id: presetId })
          });
          const data = await res.json();
          if (data.status === "success") {
            activeScopeData = data.scope;
            updateScopeUI();
          }
        } catch (err) {
          console.error("Failed to load preset:", err);
        }
      });
    }

    // Initial load
    fetchScopeAndRender();
  }

  function handleFileUpload(e) {
    if (e.target.files && e.target.files[0]) {
      readFileAndUpload(e.target.files[0]);
    }
  }

  function readFileAndUpload(file) {
    const reader = new FileReader();
    const format = file.name.endsWith(".json") ? "json" : file.name.endsWith(".csv") ? "csv" : "text";
    reader.onload = async event => {
      const content = event.target.result;
      await uploadScopeContent(content, format);
      const uploadDrawer = document.getElementById("uploadDrawer");
      if (uploadDrawer) uploadDrawer.style.display = "none";
    };
    reader.readAsText(file);
  }

  async function uploadScopeContent(content, format) {
    try {
      const res = await fetch("/api/scope/upload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content, format })
      });
      const data = await res.json();
      if (data.status === "success") {
        alert("Curriculum Scope loaded successfully!");
        activeScopeData = data.scope;
        updateScopeUI();
      } else {
        alert("Upload error: " + data.message);
      }
    } catch (err) {
      alert("Failed to upload scope: " + err.message);
    }
  }

  async function fetchScopeAndRender() {
    try {
      const res = await fetch("/api/scope");
      const data = await res.json();
      if (data.status === "success") {
        activeScopeData = data.scope;
        updateScopeUI();
      }
    } catch (err) {
      console.error("Error fetching scope:", err);
    }
  }

  function updateScopeUI() {
    if (!activeScopeData) return;
    const titleDisplay = document.getElementById("scopeTitleDisplay");
    if (titleDisplay) {
      titleDisplay.textContent = `Loaded: ${activeScopeData.title || "Annual Teaching Plan"} (${activeScopeData.academic_year || "2026"})`;
    }

    // Update term progress pills
    const terms = activeScopeData.terms || {};
    ["Term 1", "Term 2", "Term 3", "Term 4"].forEach((tName, i) => {
      const pill = document.getElementById(`t${i+1}Progress`);
      if (pill && terms[tName]) {
        const weeks = terms[tName].weeks || [];
        const completed = weeks.filter(w => w.completed).length;
        pill.textContent = `${completed}/${weeks.length}`;
      }
    });

    renderCurrentTermObjectives();
    const currentWeek = parseInt(document.getElementById("currentWeekSelect").value || "4");
    updateAccountability(currentActiveTerm, currentWeek);
  }

  function renderCurrentTermObjectives() {
    if (!activeScopeData) return;
    const termData = (activeScopeData.terms || {})[currentActiveTerm];
    const nameDisplay = document.getElementById("currentTermNameDisplay");
    const container = document.getElementById("objectivesList");
    if (!container) return;

    if (!termData) {
      container.innerHTML = `<p class="helper-text">No objectives found for ${currentActiveTerm}.</p>`;
      return;
    }

    if (nameDisplay) {
      nameDisplay.textContent = `${currentActiveTerm}: ${termData.name || "Curriculum Focus"}`;
    }

    const weeks = termData.weeks || [];
    container.innerHTML = weeks.map(item => {
      const isCompleted = item.completed;
      return `
        <div class="objective-item-card ${isCompleted ? 'completed' : ''}" id="obj-row-${item.id}">
          <div>
            <input type="checkbox" class="objective-checkbox" data-id="${item.id}" ${isCompleted ? 'checked' : ''}>
          </div>
          <div class="obj-week-col">
            <span class="obj-week-num">Week ${item.week}</span>
            <span class="obj-topic-name">${escapeHtml(item.topic)}</span>
          </div>
          <div class="obj-bullets">
            ${(item.objectives || []).map(o => `<div>• ${escapeHtml(o)}</div>`).join("")}
          </div>
          <div class="obj-hours-tag">
            ${item.hours_allocated || 3.5}h
          </div>
          <div class="obj-actions-col">
            <button class="btn-draft-lesson" data-topic="${escapeHtml(item.topic)}" data-objs="${escapeHtml((item.objectives || []).join('; '))}">
              Draft Lesson
            </button>
            ${isCompleted && item.date_completed ? `<span class="obj-completed-date">Done: ${item.date_completed}</span>` : ''}
          </div>
        </div>
      `;
    }).join("");

    // Attach checkbox listeners
    container.querySelectorAll(".objective-checkbox").forEach(box => {
      box.addEventListener("change", async () => {
        const objId = box.dataset.id;
        const checked = box.checked;
        await toggleObjectiveStatus(objId, checked);
      });
    });

    // Attach Draft Lesson shortcut listeners
    container.querySelectorAll(".btn-draft-lesson").forEach(btn => {
      btn.addEventListener("click", () => {
        const topic = btn.dataset.topic;
        const objs = btn.dataset.objs;
        const goalStr = `${activeScopeData.grade || 'Grade 7'} ${activeScopeData.subject || 'Natural Sciences'}: ${topic} (${objs}) for 45 students in public school`;

        // Transfer to Generator View
        document.querySelector('.nav-pill-btn[data-view="generator-view"]').click();
        goalInput.value = goalStr;
        goalInput.scrollIntoView({ behavior: 'smooth' });
        goalInput.focus();
      });
    });
  }

  async function toggleObjectiveStatus(objId, completed) {
    try {
      const res = await fetch("/api/scope/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: objId, completed: completed })
      });
      const data = await res.json();
      if (data.status === "success") {
        fetchScopeAndRender();
      }
    } catch (err) {
      console.error("Failed to update status:", err);
    }
  }

  async function updateAccountability(termName, currentWeek) {
    try {
      const res = await fetch(`/api/scope/accountability?term=${encodeURIComponent(termName)}&week=${currentWeek}`);
      const data = await res.json();
      if (data.status === "success") {
        const rep = data.report;
        renderAccountabilityReport(rep);
      }
    } catch (err) {
      console.error("Failed to fetch accountability report:", err);
    }
  }

  function renderAccountabilityReport(rep) {
    const badge = document.getElementById("pacingHealthBadge");
    const badgeText = document.getElementById("pacingHealthText");
    const deltaText = document.getElementById("pacingDeltaText");
    const advisoryBox = document.getElementById("plannerAdvisoryBox");
    const progressBar = document.getElementById("scopeProgressBar");
    const progressPercentLabel = document.getElementById("progressPercentLabel");
    const progressCountLabel = document.getElementById("progressCountLabel");
    const trackerNavBadge = document.getElementById("trackerNavBadge");

    if (progressBar) progressBar.style.width = `${rep.completion_percentage}%`;
    if (progressPercentLabel) progressPercentLabel.textContent = `${rep.completion_percentage}% Scope Covered`;
    if (progressCountLabel) progressCountLabel.textContent = `${rep.completed_count} of ${rep.total_weeks} Weeks Completed`;

    if (badge && badgeText && deltaText) {
      badge.className = "pacing-health-badge";
      if (rep.health_status === "ON_TRACK") {
        badge.classList.add("badge-on-track");
        const iconSpan = badge.querySelector(".badge-icon");
        if (iconSpan) iconSpan.textContent = "";
        badgeText.textContent = "On Track & Pacing Well";
        deltaText.textContent = `${rep.pacing_delta_weeks >= 0 ? '+' : ''}${rep.pacing_delta_weeks} weeks ahead of expected ATP`;
        if (trackerNavBadge) {
          trackerNavBadge.className = "pacing-badge on-track";
          trackerNavBadge.textContent = `${rep.term} • On Track`;
        }
      } else if (rep.health_status === "SLIGHT_DELAY") {
        badge.classList.add("badge-slight-delay");
        const iconSpan = badge.querySelector(".badge-icon");
        if (iconSpan) iconSpan.textContent = "";
        badgeText.textContent = "1 Week Behind Schedule";
        deltaText.textContent = "1 week behind expected Department scope";
        if (trackerNavBadge) {
          trackerNavBadge.className = "pacing-badge delayed";
          trackerNavBadge.textContent = `${rep.term} • 1 Wk Behind`;
        }
      } else {
        badge.classList.add("badge-critical-lag");
        const iconSpan = badge.querySelector(".badge-icon");
        if (iconSpan) iconSpan.textContent = "";
        badgeText.textContent = `${Math.abs(rep.pacing_delta_weeks)} Weeks Behind Schedule`;
        deltaText.textContent = `Critical lag: ${Math.abs(rep.pacing_delta_weeks)} weeks behind Department ATP`;
        if (trackerNavBadge) {
          trackerNavBadge.className = "pacing-badge critical";
          trackerNavBadge.textContent = `${rep.term} • ${Math.abs(rep.pacing_delta_weeks)} Wks Behind`;
        }
      }
    }

    if (advisoryBox) {
      advisoryBox.textContent = rep.planner_advisory;
    }
  }

  // Initialize Scope Tracker
  initScopeTracker();
});
