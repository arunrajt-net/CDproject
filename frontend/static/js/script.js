/**
 * Mini SQL Compiler - Client-side Controller & UI Interactivity
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const sqlInput = document.getElementById("sqlInput");
  const lineNumbers = document.getElementById("lineNumbers");
  const compileBtn = document.getElementById("compileBtn");
  const clearBtn = document.getElementById("clearBtn");
  const resetBtn = document.getElementById("resetBtn");
  const exampleSelect = document.getElementById("exampleQuerySelect");

  const statusPill = document.getElementById("compilerStatusPill");
  const statusText = document.getElementById("compilerStatusText");

  // Pipeline Indicators
  const stageLexical = document.getElementById("stageLexical");
  const statusLexical = document.getElementById("statusLexical");
  const stageSyntax = document.getElementById("stageSyntax");
  const statusSyntax = document.getElementById("statusSyntax");
  const stageSemantic = document.getElementById("stageSemantic");
  const statusSemantic = document.getElementById("statusSemantic");
  const metricTokens = document.getElementById("metricTokens");
  const metricDuration = document.getElementById("metricDuration");

  // Output containers
  const treeOutput = document.getElementById("treeOutput");
  const tokensTableBody = document.getElementById("tokensTableBody");
  const tokenStreamCount = document.getElementById("tokenStreamCount");
  const astOutput = document.getElementById("astOutput");
  const semanticContainer = document.getElementById("semanticContainer");
  const semanticBadge = document.getElementById("semanticBadge");
  const symbolTableBody = document.getElementById("symbolTableBody");
  const errorsContainer = document.getElementById("errorsContainer");
  const errorBadge = document.getElementById("errorBadge");

  // Tabs
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabPanes = document.querySelectorAll(".tab-pane");

  // Schema Modal
  const schemaModal = document.getElementById("schemaModal");
  const schemaModalBtn = document.getElementById("schemaModalBtn");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const modalSchemaContent = document.getElementById("modalSchemaContent");

  const DEFAULT_SAMPLE_SQL = "SELECT name, age FROM students WHERE age > 18 ORDER BY age DESC;";

  const EXAMPLES = {
    "val_1": "SELECT * FROM students;",
    "val_2": "SELECT name, age FROM students WHERE age > 18;",
    "val_3": "SELECT name, marks FROM students WHERE marks >= 80 AND department = 'CSE' ORDER BY marks DESC;",
    "val_4": "SELECT DISTINCT department FROM employees WHERE salary > 40000.0;",
    "inv_1": "SELECT FROM students;",
    "inv_2": "SELECT name students;",
    "inv_3": "SELECT salary FROM students;",
    "inv_4": "SELECT name FROM students WHERE age = 'twenty';",
    "inv_5": "SELECT name FROM students @;"
  };

  // --------------------------------------------------------------------------
  // Line Numbers Synchronization
  // --------------------------------------------------------------------------
  function updateLineNumbers() {
    const lines = sqlInput.value.split("\n").length;
    let nums = "";
    for (let i = 1; i <= lines; i++) {
      nums += i + "\n";
    }
    lineNumbers.textContent = nums;
  }

  sqlInput.addEventListener("input", updateLineNumbers);
  sqlInput.addEventListener("scroll", () => {
    lineNumbers.scrollTop = sqlInput.scrollTop;
  });

  // Shortcut Ctrl+Enter / Cmd+Enter
  sqlInput.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      runCompilation();
    }
  });

  // --------------------------------------------------------------------------
  // Tab Switching
  // --------------------------------------------------------------------------
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-tab");
      tabButtons.forEach(b => b.classList.remove("active"));
      tabPanes.forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(targetId).classList.add("active");
    });
  });

  function switchToTab(tabId) {
    tabButtons.forEach(b => {
      if (b.getAttribute("data-tab") === tabId) {
        b.classList.add("active");
      } else {
        b.classList.remove("active");
      }
    });
    tabPanes.forEach(p => {
      if (p.id === tabId) {
        p.classList.add("active");
      } else {
        p.classList.remove("active");
      }
    });
  }

  // --------------------------------------------------------------------------
  // Example Selection & Reset
  // --------------------------------------------------------------------------
  exampleSelect.addEventListener("change", (e) => {
    const val = e.target.value;
    if (EXAMPLES[val]) {
      sqlInput.value = EXAMPLES[val];
      updateLineNumbers();
      runCompilation();
    }
  });

  clearBtn.addEventListener("click", () => {
    sqlInput.value = "";
    updateLineNumbers();
    sqlInput.focus();
  });

  resetBtn.addEventListener("click", () => {
    sqlInput.value = DEFAULT_SAMPLE_SQL;
    updateLineNumbers();
    exampleSelect.selectedIndex = 0;
    runCompilation();
  });

  compileBtn.addEventListener("click", runCompilation);

  // --------------------------------------------------------------------------
  // Copy Buttons
  // --------------------------------------------------------------------------
  document.getElementById("copyTreeBtn").addEventListener("click", () => {
    copyTextToClipboard(treeOutput.textContent, "Parse Tree copied!");
  });

  document.getElementById("copyJsonBtn").addEventListener("click", () => {
    copyTextToClipboard(astOutput.textContent, "AST JSON copied!");
  });

  function copyTextToClipboard(text, msg) {
    navigator.clipboard.writeText(text).then(() => {
      alert(msg);
    }).catch(() => {
      // Fallback
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      alert(msg);
    });
  }

  // --------------------------------------------------------------------------
  // Schema Modal
  // --------------------------------------------------------------------------
  schemaModalBtn.addEventListener("click", () => {
    schemaModal.classList.remove("hidden");
  });

  closeModalBtn.addEventListener("click", () => {
    schemaModal.classList.add("hidden");
  });

  schemaModal.addEventListener("click", (e) => {
    if (e.target === schemaModal) {
      schemaModal.classList.add("hidden");
    }
  });

  // --------------------------------------------------------------------------
  // Compilation Controller
  // --------------------------------------------------------------------------
  async function runCompilation() {
    const query = sqlInput.value.trim();
    if (!query) {
      alert("Please enter a SQL query to compile.");
      return;
    }

    // Set compiling state
    setCompilerStatus("compiling", "Compiling...");
    resetPipelineDisplay();

    try {
      const response = await fetch("/api/compile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query })
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const result = await response.json();
      renderCompilationResult(result);
    } catch (err) {
      console.error("Compilation error:", err);
      setCompilerStatus("error", "Network / Server Error");
      alert("Error communicating with compiler backend: " + err.message);
    }
  }

  function setCompilerStatus(type, text) {
    statusPill.className = "status-pill status-" + type;
    statusText.textContent = text;
  }

  function resetPipelineDisplay() {
    [stageLexical, stageSyntax, stageSemantic].forEach(stage => {
      stage.className = "stage-item";
    });
    statusLexical.textContent = "WAITING";
    statusSyntax.textContent = "WAITING";
    statusSemantic.textContent = "WAITING";
    metricTokens.textContent = "...";
    metricDuration.textContent = "...";
  }

  function updateStageStatus(stageEl, statusEl, status) {
    stageEl.className = "stage-item";
    if (status === "PASSED") {
      stageEl.classList.add("stage-passed");
      statusEl.textContent = "PASSED";
    } else if (status === "FAILED") {
      stageEl.classList.add("stage-failed");
      statusEl.textContent = "FAILED";
    } else if (status === "SKIPPED") {
      stageEl.classList.add("stage-skipped");
      statusEl.textContent = "SKIPPED";
    } else {
      statusEl.textContent = "IDLE";
    }
  }

  // --------------------------------------------------------------------------
  // Result Rendering
  // --------------------------------------------------------------------------
  function renderCompilationResult(res) {
    // 1. Overall Status
    if (res.success) {
      setCompilerStatus("ready", "Compiled Successfully");
    } else {
      setCompilerStatus("error", "Compilation Failed");
    }

    // 2. Pipeline metrics & stages
    const phases = res.phases || {};
    updateStageStatus(stageLexical, statusLexical, phases.lexical);
    updateStageStatus(stageSyntax, statusSyntax, phases.syntax);
    updateStageStatus(stageSemantic, statusSemantic, phases.semantic);

    metricTokens.textContent = res.token_count !== undefined ? res.token_count : res.tokens.length;
    metricDuration.textContent = `${res.duration_ms || 0} ms`;

    // 3. Render Tokens
    renderTokensTable(res.tokens);

    // 4. Render Parse Tree (CST)
    if (res.parse_tree_text) {
      treeOutput.textContent = res.parse_tree_text;
    } else {
      treeOutput.textContent = res.errors && res.errors.length > 0
        ? `[Parse tree construction aborted due to errors in ${res.errors[0].error_type}]`
        : "No parse tree generated.";
    }

    // 5. Render AST & JSON
    if (res.ast_json) {
      astOutput.textContent = JSON.stringify(res.ast_json, null, 2);
    } else {
      astOutput.textContent = "No AST available.";
    }

    // 6. Render Semantic Validation
    renderSemanticReport(res.semantic_analysis, phases.semantic);

    // 7. Render Symbol Table
    if (res.symbol_table && res.symbol_table.length > 0) {
      renderSymbolTable(res.symbol_table);
    }

    // 8. Render Errors & Diagnostics
    renderErrors(res.errors || []);

    // If there were errors, switch view to Diagnostics tab automatically
    if (!res.success && res.errors && res.errors.length > 0) {
      switchToTab("tabErrors");
    } else {
      switchToTab("tabTree");
    }
  }

  function renderTokensTable(tokens) {
    if (!tokens || tokens.length === 0) {
      tokensTableBody.innerHTML = '<tr><td colspan="6" class="empty-state">No tokens generated.</td></tr>';
      tokenStreamCount.textContent = "0 tokens generated";
      return;
    }

    const filtered = tokens.filter(t => t.type !== "EOF");
    tokenStreamCount.textContent = `${filtered.length} tokens generated`;

    let html = "";
    filtered.forEach((tok, idx) => {
      const literal = tok.literal_value !== undefined && tok.literal_value !== null ? tok.literal_value : "-";
      html += `
        <tr>
          <td>${idx + 1}</td>
          <td><span class="tok-badge tok-${tok.type}">${tok.type}</span></td>
          <td><code>${escapeHtml(tok.lexeme)}</code></td>
          <td><code>${escapeHtml(String(literal))}</code></td>
          <td>${tok.line}</td>
          <td>${tok.column}</td>
        </tr>
      `;
    });
    tokensTableBody.innerHTML = html;
  }

  function renderSemanticReport(report, phaseStatus) {
    if (phaseStatus === "PASSED" && report && report.verifications) {
      semanticBadge.className = "badge badge-success";
      semanticBadge.textContent = "All Validations Passed";

      let html = "";
      report.verifications.forEach(v => {
        html += `
          <div class="semantic-item">
            <div class="semantic-item-left">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#10b981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              <div>
                <div class="semantic-check-title">${escapeHtml(v.check)}: <code>${escapeHtml(v.target)}</code></div>
                <div class="semantic-check-detail">${escapeHtml(v.detail)}</div>
              </div>
            </div>
            <span class="badge badge-success">VALID</span>
          </div>
        `;
      });
      semanticContainer.innerHTML = html;
    } else if (phaseStatus === "FAILED") {
      semanticBadge.className = "badge badge-error";
      semanticBadge.textContent = "Validation Failed";
      semanticContainer.innerHTML = '<div class="empty-state" style="color:var(--accent-rose);">Semantic analysis failed. See Diagnostics tab for details.</div>';
    } else {
      semanticBadge.className = "badge badge-neutral";
      semanticBadge.textContent = "Skipped / Pending";
      semanticContainer.innerHTML = '<div class="empty-state">Semantic analysis skipped due to syntax/lexical failure.</div>';
    }
  }

  function renderSymbolTable(symbols) {
    let html = "";
    symbols.forEach(sym => {
      const pkBadge = sym.primary_key ? '<span class="badge badge-neutral" style="color:var(--accent-amber)">Primary Key</span>' : '-';
      const nullableText = sym.nullable ? 'YES' : 'NO';
      html += `
        <tr>
          <td><strong>${escapeHtml(sym.table_name)}</strong></td>
          <td><code>${escapeHtml(sym.column_name)}</code></td>
          <td><span class="badge badge-neutral">${escapeHtml(sym.data_type)}</span></td>
          <td>${nullableText}</td>
          <td>${pkBadge}</td>
        </tr>
      `;
    });
    symbolTableBody.innerHTML = html;
  }

  function renderErrors(errors) {
    if (!errors || errors.length === 0) {
      errorBadge.classList.add("hidden");
      errorsContainer.innerHTML = `
        <div class="success-callout">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          <span>No compiler errors detected. All phases passed successfully.</span>
        </div>
      `;
      return;
    }

    errorBadge.textContent = errors.length;
    errorBadge.classList.remove("hidden");

    let html = "";
    errors.forEach(err => {
      html += `
        <div class="error-card">
          <div class="error-card-header">
            <span class="error-type-tag">${escapeHtml(err.error_type)}</span>
            <span class="error-loc-tag">Line ${err.line}, Column ${err.column}</span>
          </div>
          <div class="error-card-msg">${escapeHtml(err.message)}</div>
          ${err.suggestion ? `
            <div class="error-card-suggestion">
              <strong>Suggestion:</strong> ${escapeHtml(err.suggestion)}
            </div>
          ` : ""}
        </div>
      `;
    });
    errorsContainer.innerHTML = html;
  }

  function escapeHtml(text) {
    if (!text) return "";
    return text.toString()
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Load Schema for Modal Dialog
  async function loadInitialSchema() {
    try {
      const resp = await fetch("/api/schema");
      if (resp.ok) {
        const data = await resp.json();
        let modalHtml = '<div style="display:flex; flex-direction:column; gap:16px;">';
        for (const [tbl, cols] of Object.entries(data.tables)) {
          modalHtml += `
            <div style="background:var(--bg-input); padding:12px; border-radius:6px; border:1px solid var(--border-subtle);">
              <h4 style="color:var(--accent-cyan); font-family:var(--font-mono); margin-bottom:8px;">Table: ${escapeHtml(tbl)}</h4>
              <ul style="list-style:none; padding-left:0; font-size:0.82rem; font-family:var(--font-mono); color:var(--text-muted);">
                ${cols.map(c => `<li>&bull; <strong>${escapeHtml(c.column_name)}</strong>: ${escapeHtml(c.data_type)} ${c.primary_key ? '(PK)' : ''}</li>`).join('')}
              </ul>
            </div>
          `;
        }
        modalHtml += '</div>';
        modalSchemaContent.innerHTML = modalHtml;
        if (data.all_symbols) {
          renderSymbolTable(data.all_symbols);
        }
      }
    } catch (e) {
      console.warn("Could not pre-load schema modal:", e);
    }
  }

  // Initial Boot
  updateLineNumbers();
  loadInitialSchema();
  runCompilation();
});
