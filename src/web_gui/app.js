/**
 * Exocortex Cognitive Command Center - Frontend Application Logic (v0.5.2).
 * Cyber-Dark Single Page Application (SPA).
 */

// =============================================================================
// ÉTAT GLOBAL DE L'APPLICATION
// =============================================================================
const state = {
  currentView: "timeline",
  activeProjectId: "exocortex",
  projects: [],
  selectedDate: null,
  dates: [],
  loadedViews: new Set(),
  modalRawMarkdown: "",
  epistemicSubTab: "chats",
};

// =============================================================================
// UTILITAIRES API REST & PRESSE-PAPIER
// =============================================================================

// Jeton local exigé par l'API pour les écritures et routes sensibles (v0.5.2, D1)
let apiToken = null;

async function fetchApiToken() {
  const res = await fetch("/api/auth/token", { headers: { Accept: "application/json" } });
  if (!res.ok) throw new Error(`Jeton local refusé (HTTP ${res.status})`);
  apiToken = (await res.json()).token;
  return apiToken;
}

async function apiRequest(endpoint, options = {}) {
  try {
    const send = async () =>
      fetch(endpoint, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "X-Exocortex-Token": apiToken || (await fetchApiToken()),
          ...options.headers,
        },
      });
    let res = await send();
    if (res.status === 401) {
      // Jeton régénéré côté serveur : on le relit une fois
      await fetchApiToken();
      res = await send();
    }
    if (!res.ok) {
      const errData = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(errData.detail || `Erreur HTTP ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error(`[API Error] ${endpoint}:`, err);
    throw err;
  }
}

const apiGet = (url) => apiRequest(url, { method: "GET" });
const apiPost = (url, body) => apiRequest(url, { method: "POST", body: JSON.stringify(body) });
const apiPatch = (url, body) => apiRequest(url, { method: "PATCH", body: JSON.stringify(body) });
const apiDelete = (url) => apiRequest(url, { method: "DELETE" });

/**
 * Échappe toute donnée insérée dans un gabarit HTML (v0.5.2, D2) : chats, titres de fenêtres,
 * URL et fiches proviennent de sources externes et ne doivent jamais être interprétés.
 */
function esc(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;")
    .replace(/`/g, "&#96;");
}

/** Rend du Markdown en HTML assaini (DOMPurify) ; repli en texte brut si une bibliothèque manque. */
function renderMarkdownSafe(container, markdown) {
  if (typeof marked !== "undefined" && typeof DOMPurify !== "undefined") {
    container.innerHTML = DOMPurify.sanitize(marked.parse(markdown || ""));
  } else {
    container.textContent = markdown || "";
  }
}

async function copyToClipboard(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    await navigator.clipboard.writeText(text);
  } else {
    // Fallback document.execCommand
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
  }
}

// =============================================================================
// SYSTÈME DE TOAST NOTIFICATIONS
// =============================================================================

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  const bgColors = {
    info: "bg-cyber-800 border-cyber-cyan text-slate-100",
    success: "bg-emerald-950/90 border-emerald-500 text-emerald-200",
    error: "bg-rose-950/90 border-rose-500 text-rose-200",
    warning: "bg-amber-950/90 border-amber-500 text-amber-200",
  };

  const icons = {
    info: "ℹ️",
    success: "✅",
    error: "❌",
    warning: "⚠️",
  };

  toast.className = `toast px-4 py-2.5 rounded-lg border text-xs font-medium shadow-xl flex items-center gap-2.5 max-w-sm ${bgColors[type] || bgColors.info}`;
  toast.innerHTML = `
    <span>${icons[type] || "ℹ️"}</span>
    <span class="flex-1">${esc(message)}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(0.5rem)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// =============================================================================
// MODALE POLYVALENTE MARKDOWN
// =============================================================================

function openMarkdownModal(title, markdownContent) {
  state.modalRawMarkdown = markdownContent;
  const modal = document.getElementById("modal-markdown");
  const modalTitle = document.getElementById("modal-markdown-title");
  const modalBody = document.getElementById("modal-markdown-body");

  if (modalTitle) modalTitle.innerHTML = `<span>📄</span> <span>${esc(title)}</span>`;
  if (modalBody) renderMarkdownSafe(modalBody, markdownContent);

  if (modal) modal.classList.remove("hidden");
}

function closeMarkdownModal() {
  const modal = document.getElementById("modal-markdown");
  if (modal) modal.classList.add("hidden");
}

// =============================================================================
// BANDEAU GLOBAL & STATUT SYSTÈME LIVE
// =============================================================================

async function updateSystemStatus() {
  try {
    const data = await apiGet("/api/system/status");

    // VRAM
    const vramVal = document.getElementById("vram-val");
    if (vramVal && data.vram) {
      vramVal.innerText = `${data.vram.used_gb} / ${data.vram.total_gb} Go`;
    }

    // Ollama
    const ollamaDot = document.getElementById("ollama-dot");
    const ollamaVal = document.getElementById("ollama-val");
    if (ollamaVal && ollamaDot) {
      if (data.ollama_alive) {
        ollamaDot.className = "w-2 h-2 rounded-full bg-emerald-400";
        ollamaVal.innerText = "Actif";
        ollamaVal.className = "font-semibold text-emerald-400";
      } else {
        ollamaDot.className = "w-2 h-2 rounded-full bg-rose-400";
        ollamaVal.innerText = "Hors-ligne";
        ollamaVal.className = "font-semibold text-rose-400";
      }
    }

    // DriftGuard
    const driftDot = document.getElementById("drift-dot");
    const driftVal = document.getElementById("drift-val");
    if (driftVal && driftDot) {
      if (data.drift_state && data.drift_state.drift_detected) {
        driftDot.className = "w-2 h-2 rounded-full bg-amber-400 pulse-glow";
        driftVal.innerText = "DRIFT DÉTECTÉ";
        driftVal.className = "font-semibold text-amber-400";
      } else {
        driftDot.className = "w-2 h-2 rounded-full bg-emerald-400";
        driftVal.innerText = "STABLE";
        driftVal.className = "font-semibold text-emerald-400";
      }
    }

    // Sauvegarde Bootloader pour ouverture instantanée
    state.bootloaderContent = data.bootloader_content || "# Context Bootloader\n\nAucun bootloader actif.";
  } catch (err) {
    console.warn("Impossible de rafraîchir le statut système :", err);
  }
}

// =============================================================================
// NAVIGATION PAR ONGLETS (SPA)
// =============================================================================

function switchView(viewName) {
  state.currentView = viewName;

  // Mise à jour de l'apparence des onglets
  document.querySelectorAll(".nav-tab").forEach((tab) => {
    if (tab.dataset.view === viewName) {
      tab.className = "nav-tab active px-3.5 py-1.5 rounded-md text-xs font-medium transition flex items-center gap-2 text-slate-100 bg-cyber-blue/30 border border-cyber-blue/50 text-cyber-cyan";
    } else {
      tab.className = "nav-tab px-3.5 py-1.5 rounded-md text-xs font-medium transition flex items-center gap-2 text-slate-400 hover:text-slate-200 hover:bg-cyber-800";
    }
  });

  // Affichage du bon conteneur
  document.querySelectorAll(".view-panel").forEach((panel) => {
    if (panel.id === `view-${viewName}`) {
      panel.classList.remove("hidden");
    } else {
      panel.classList.add("hidden");
    }
  });

  // Chargement paresseux des données
  if (!state.loadedViews.has(viewName)) {
    state.loadedViews.add(viewName);
    loadViewData(viewName);
  }
}

function loadViewData(viewName) {
  switch (viewName) {
    case "timeline":
      initTimelineView();
      break;
    case "carto":
      loadCartographyView();
      break;
    case "archaeology":
      loadArchaeologyView();
      break;
    case "circadian":
      loadCircadianView();
      break;
    case "epistemic":
      loadEpistemicView();
      break;
    case "kanban":
      initKanbanView();
      break;
  }
}

// =============================================================================
// VUE 1 : CHRONOLOGIE & TUNNELS D'HYPERFOCUS
// =============================================================================

async function initTimelineView() {
  try {
    const dates = await apiGet("/api/telemetry/dates");
    state.dates = dates;

    const select = document.getElementById("timeline-date-select");
    if (!select) return;

    select.innerHTML = "";
    if (!dates || dates.length === 0) {
      select.innerHTML = `<option value="">Aucune date disponible</option>`;
      return;
    }

    dates.forEach((d, idx) => {
      const opt = document.createElement("option");
      opt.value = d;
      opt.innerText = idx === 0 ? `${d} (Dernière activité)` : d;
      select.appendChild(opt);
    });

    state.selectedDate = dates[0];
    await loadTimelineForDate(state.selectedDate);
  } catch (err) {
    showToast("Échec chargement des dates de chronologie", "error");
  }
}

async function loadTimelineForDate(dateStr) {
  if (!dateStr) return;
  try {
    const data = await apiGet(`/api/telemetry/timeline?date=${encodeURIComponent(dateStr)}`);
    const events = data.events || [];
    const metric = data.daily_metric || {};

    // 1. KPIs Journaliers
    const totalSec = metric.total_active_sec || 0;
    const hrs = Math.floor(totalSec / 3600);
    const mins = Math.floor((totalSec % 3600) / 60);
    document.getElementById("kpi-total-time").innerText = `${hrs}h ${mins}m`;
    document.getElementById("kpi-tunnels-count").innerText = metric.hyperfocus_tunnel_count || 0;
    document.getElementById("kpi-gemini-turns").innerText = metric.total_chat_turns || 0;

    const focusRatio = totalSec > 0 ? Math.round(((metric.total_deep_work_sec || 0) / totalSec) * 100) : 0;
    document.getElementById("kpi-focus-ratio").innerText = `${focusRatio}%`;

    // 2. Tunnels d'Hyperfocus
    const tunnelsList = document.getElementById("tunnels-list");
    const tunnelsBadge = document.getElementById("tunnels-badge");
    const tunnels = data.focus_tunnels || [];
    tunnelsBadge.innerText = tunnels.length;
    tunnelsList.innerHTML = "";

    if (tunnels.length === 0) {
      tunnelsList.innerHTML = `<p class="text-xs text-slate-500 italic">Aucun tunnel ≥ 30 min identifié ce jour.</p>`;
    } else {
      tunnels.forEach((t) => {
        const durMin = Math.round((t.duration_sec || 0) / 60);
        const card = document.createElement("div");
        card.className = "p-2.5 rounded-lg bg-cyber-900 border border-cyber-700/80 space-y-1 text-xs";
        card.innerHTML = `
          <div class="flex items-center justify-between">
            <span class="font-bold text-emerald-400">🔥 ${durMin} min</span>
            <span class="text-[10px] font-mono text-slate-400">${esc(t.start_time?.slice(11, 16) || "")} - ${esc(t.end_time?.slice(11, 16) || "")}</span>
          </div>
          <div class="font-semibold text-slate-200">${esc(t.executable || "App")}</div>
          <div class="text-[11px] text-slate-400 truncate">${esc(t.top_window_title || "Sans titre")}</div>
        `;
        tunnelsList.appendChild(card);
      });
    }

    // 3. Diagramme de Gantt Plotly
    renderGanttChart(events);

    // 4. Table des Activités Détaillées
    renderActivityTable(events);
  } catch (err) {
    showToast(`Erreur chargement chronologie (${dateStr})`, "error");
  }
}

function renderGanttChart(events) {
  const container = document.getElementById("gantt-chart-container");
  if (!container) return;

  if (!events || events.length === 0) {
    container.innerHTML = `<div class="h-full flex items-center justify-center text-slate-500 text-xs italic">Aucune donnée d'activité pour ce jour.</div>`;
    return;
  }

  // Couleurs par mode cognitif
  const modeColors = {
    Deep_Work: "#38bdf8",
    Execution: "#10b981",
    Communication: "#8b5cf6",
    Passive: "#f59e0b",
    Noise: "#64748b",
  };

  const traces = [];
  const groupedByMode = {};

  events.forEach((ev) => {
    const mode = ev.cognitive_mode || "Deep_Work";
    if (!groupedByMode[mode]) {
      groupedByMode[mode] = { x0: [], x1: [], y: [], text: [] };
    }
    groupedByMode[mode].x0.push(ev.timestamp_start);
    groupedByMode[mode].x1.push(ev.timestamp_end);
    groupedByMode[mode].y.push(ev.executable || "Autre");
    groupedByMode[mode].text.push(`${esc(ev.window_title || "")}<br>${esc(ev.url_or_path || "")}`);
  });

  Object.keys(groupedByMode).forEach((mode) => {
    const g = groupedByMode[mode];
    traces.push({
      type: "bar",
      orientation: "h",
      name: mode,
      base: g.x0,
      x: g.x1.map((end, i) => new Date(end) - new Date(g.x0[i])),
      y: g.y,
      marker: { color: modeColors[mode] || "#3b82f6" },
      hoverinfo: "text",
      hovertext: g.text,
    });
  });

  const layout = {
    barmode: "stack",
    template: "plotly_dark",
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { l: 90, r: 20, t: 10, b: 30 },
    height: 310,
    xaxis: {
      type: "date",
      gridcolor: "#1f293d",
      tickformat: "%H:%M",
    },
    yaxis: {
      automargin: true,
      gridcolor: "#1f293d",
      tickfont: { size: 10 },
    },
    legend: {
      orientation: "h",
      y: 1.15,
      x: 0,
      font: { size: 10 },
    },
  };

  Plotly.newPlot("gantt-chart-container", traces, layout, { responsive: true, displayModeBar: false });
}

function renderActivityTable(events) {
  const tbody = document.getElementById("timeline-table-body");
  if (!tbody) return;

  window._allTimelineEvents = events;
  filterAndRenderTimelineTable();
}

function filterAndRenderTimelineTable() {
  const tbody = document.getElementById("timeline-table-body");
  const filterInput = document.getElementById("timeline-search-filter");
  const q = (filterInput?.value || "").toLowerCase().trim();
  const events = window._allTimelineEvents || [];

  const filtered = q
    ? events.filter(
        (e) =>
          (e.executable || "").toLowerCase().includes(q) ||
          (e.window_title || "").toLowerCase().includes(q) ||
          (e.url_or_path || "").toLowerCase().includes(q) ||
          (e.cognitive_mode || "").toLowerCase().includes(q)
      )
    : events;

  tbody.innerHTML = "";
  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" class="py-4 text-center text-slate-500 italic">Aucune activité correspondante.</td></tr>`;
    return;
  }

  // Affichage des 100 premières lignes
  filtered.slice(0, 100).forEach((ev) => {
    const tr = document.createElement("tr");
    tr.className = "hover:bg-cyber-800/40 transition";
    const startH = (ev.timestamp_start || "").slice(11, 19);
    const durSec = ev.duration_sec || 0;
    const durStr = durSec > 60 ? `${Math.floor(durSec / 60)}m ${durSec % 60}s` : `${durSec}s`;

    let contextHtml = `<div class="truncate max-w-md font-sans text-slate-200" title="${esc(ev.window_title)}">${esc(ev.window_title || "Sans titre")}</div>`;
    if (ev.url_or_path) {
      contextHtml += `<div class="text-[10px] text-cyber-cyan truncate max-w-md font-mono" title="${esc(ev.url_or_path)}">${esc(ev.url_or_path)}</div>`;
    }

    tr.innerHTML = `
      <td class="py-2 px-3 text-slate-400">${esc(startH)}</td>
      <td class="py-2 px-3 text-slate-300 font-semibold">${esc(durStr)}</td>
      <td class="py-2 px-3 text-slate-100 font-semibold">${esc(ev.executable || "App")}</td>
      <td class="py-2 px-3">${contextHtml}</td>
      <td class="py-2 px-3"><span class="px-2 py-0.5 rounded text-[10px] bg-cyber-800 border border-cyber-700 text-slate-300">${esc(ev.cognitive_mode || "Deep_Work")}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

// =============================================================================
// VUE 2 : CARTOGRAPHIE & GRAPHRAG VISUEL
// =============================================================================

async function loadCartographyView() {
  try {
    const [treemapData, topicsList] = await Promise.all([
      apiGet("/api/telemetry/treemap"),
      apiGet("/api/telemetry/archaeology").then((d) => d.topics || []),
    ]);

    // Remplissage du select topic GraphRAG
    const ragTopicSelect = document.getElementById("graphrag-topic-filter");
    if (ragTopicSelect) {
      ragTopicSelect.innerHTML = `<option value="">Tous les Topics</option>`;
      topicsList.forEach((t) => {
        const opt = document.createElement("option");
        opt.value = t;
        opt.innerText = t;
        ragTopicSelect.appendChild(opt);
      });
    }

    // 1. Plotly Treemap
    renderTreemapChart(treemapData);

    // 2. Plotly Donut des Modes Cognitifs
    renderDonutChart(treemapData);
  } catch (err) {
    showToast("Échec chargement cartographie cognitive", "error");
  }
}

function renderTreemapChart(data) {
  const container = document.getElementById("treemap-chart-container");
  if (!container || !data || data.length === 0) return;

  const labels = [];
  const parents = [];
  const values = [];

  // Groupement par Mode -> Topic -> Executable
  const modesSet = new Set();
  const topicsMap = {};
  const execs = [];

  data.forEach((row) => {
    const mode = row.cognitive_mode || "Deep_Work";
    const topic = row.semantic_topic || "Général";
    const exec = row.executable || "App";
    const sec = row.total_sec || 0;

    modesSet.add(mode);
    const topicKey = `${mode}__${topic}`;
    topicsMap[topicKey] = (topicsMap[topicKey] || 0) + sec;
    execs.push({ id: `${topicKey}__${exec}`, label: exec, parent: topicKey, val: sec });
  });

  // Niveau 1 : Modes
  modesSet.forEach((m) => {
    labels.push(m);
    parents.push("");
    values.push(0);
  });

  // Niveau 2 : Topics
  Object.keys(topicsMap).forEach((tk) => {
    const [mode, top] = tk.split("__");
    labels.push(top);
    parents.push(mode);
    values.push(topicsMap[tk]);
  });

  // Niveau 3 : Exécutables
  execs.forEach((e) => {
    labels.push(e.label);
    parents.push(e.parent.split("__")[1]);
    values.push(e.val);
  });

  const trace = {
    type: "treemap",
    labels: labels,
    parents: parents,
    values: values,
    textinfo: "label+value",
    marker: { line: { width: 1, color: "#1e293b" } },
  };

  const layout = {
    template: "plotly_dark",
    paper_bgcolor: "transparent",
    margin: { l: 0, r: 0, t: 0, b: 0 },
    height: 380,
  };

  Plotly.newPlot("treemap-chart-container", [trace], layout, { responsive: true, displayModeBar: false });
}

function renderDonutChart(data) {
  const container = document.getElementById("donut-chart-container");
  if (!container || !data) return;

  const modeTotals = {};
  data.forEach((row) => {
    const m = row.cognitive_mode || "Deep_Work";
    modeTotals[m] = (modeTotals[m] || 0) + (row.total_sec || 0);
  });

  const trace = {
    type: "pie",
    labels: Object.keys(modeTotals),
    values: Object.values(modeTotals),
    hole: 0.5,
    marker: {
      colors: ["#38bdf8", "#10b981", "#8b5cf6", "#f59e0b", "#64748b"],
    },
    textinfo: "percent",
  };

  const layout = {
    template: "plotly_dark",
    paper_bgcolor: "transparent",
    showlegend: true,
    legend: { orientation: "h", y: -0.1 },
    margin: { l: 10, r: 10, t: 10, b: 10 },
    height: 380,
  };

  Plotly.newPlot("donut-chart-container", [trace], layout, { responsive: true, displayModeBar: false });
}

// Recherche GraphRAG
async function runGraphRAGSearch() {
  const input = document.getElementById("graphrag-input-query");
  const topicSel = document.getElementById("graphrag-topic-filter");
  const q = (input?.value || "").trim();
  if (!q) {
    showToast("Veuillez saisir une requête de recherche.", "warning");
    return;
  }

  const topicParam = topicSel?.value ? `&topic=${encodeURIComponent(topicSel.value)}` : "";
  const resultsContainer = document.getElementById("graphrag-results-container");
  const hop0Container = document.getElementById("graphrag-hop0-cards");
  const hop1Container = document.getElementById("graphrag-hop1-cards");
  const statsSpan = document.getElementById("graphrag-stats");
  const vizContainer = document.getElementById("graphrag-network-viz");

  try {
    showToast("Recherche GraphRAG multi-sauts en cours...", "info");
    const data = await apiGet(`/api/graphrag/search?q=${encodeURIComponent(q)}${topicParam}`);

    resultsContainer.classList.remove("hidden");
    hop0Container.innerHTML = "";
    hop1Container.innerHTML = "";
    vizContainer.innerHTML = "";

    const hop0 = data.primary_nodes || [];
    const hop1 = data.linked_neighbors || [];

    statsSpan.innerText = `${hop0.length} nœuds Hop 0 (k-NN) | ${hop1.length} voisins Hop 1 (Wikilinks)`;

    // Rendu Cartes Hop 0
    if (hop0.length === 0) {
      hop0Container.innerHTML = `<p class="text-xs text-slate-500 italic">Aucune note Hop 0 correspondante.</p>`;
    } else {
      hop0.forEach((n) => {
        const card = document.createElement("div");
        card.className = "cyber-card p-3 space-y-1.5 cursor-pointer hover:border-cyber-cyan transition";
        card.innerHTML = `
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-100 text-xs">${esc(n.title)}</span>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-cyber-cyan/20 text-cyber-cyan">${esc(n.similarity_pct)}% sim</span>
          </div>
          <div class="text-[10px] font-mono text-purple-300">#${esc(n.semantic_topic)}</div>
          <p class="text-[11px] text-slate-400 line-clamp-3 leading-relaxed">${esc(n.excerpt)}</p>
        `;
        card.onclick = () => loadAndOpenConcept(n.slug);
        hop0Container.appendChild(card);
      });
    }

    // Rendu Cartes Hop 1
    if (hop1.length === 0) {
      hop1Container.innerHTML = `<p class="text-xs text-slate-500 italic">Aucun rebond Hop 1 détecté.</p>`;
    } else {
      hop1.forEach((n) => {
        const card = document.createElement("div");
        card.className = "cyber-card p-3 space-y-1.5 cursor-pointer hover:border-purple-400 transition";
        card.innerHTML = `
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-100 text-xs">${esc(n.title)}</span>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300">Score: ${esc(n.score)}</span>
          </div>
          <div class="text-[10px] font-mono text-purple-300">#${esc(n.semantic_topic)}</div>
          <p class="text-[11px] text-slate-400 line-clamp-3 leading-relaxed">${esc(n.excerpt)}</p>
        `;
        card.onclick = () => loadAndOpenConcept(n.slug);
        hop1Container.appendChild(card);
      });
    }

    // Topologie Visuelle Rapide (Bulles de Nœuds)
    (data.nodes || []).forEach((nd) => {
      const bubble = document.createElement("div");
      const isHop0 = nd.type === "primary";
      bubble.className = `px-3 py-1.5 rounded-full text-xs font-mono flex items-center gap-1.5 cursor-pointer border ${
        isHop0 ? "bg-cyber-cyan/10 border-cyber-cyan/50 text-cyber-cyan hover:bg-cyber-cyan/20" : "bg-purple-900/30 border-purple-500/50 text-purple-300 hover:bg-purple-900/50"
      }`;
      bubble.innerHTML = `<span>${isHop0 ? "🎯" : "🔗"}</span> <span>${esc(nd.label)}</span>`;
      bubble.onclick = () => loadAndOpenConcept(nd.id);
      vizContainer.appendChild(bubble);
    });

    showToast("Recherche GraphRAG terminée.", "success");
  } catch (err) {
    showToast(`Erreur GraphRAG : ${err.message}`, "error");
  }
}

async function loadAndOpenConcept(slug) {
  try {
    const data = await apiGet(`/api/concepts/${encodeURIComponent(slug)}`);
    openMarkdownModal(`Concept : ${data.title} (${slug}.md)`, data.raw_markdown);
  } catch (err) {
    showToast(`Impossible d'ouvrir le concept '${slug}' : ${err.message}`, "error");
  }
}

// =============================================================================
// VUE 3 : ARCHÉOLOGIE LONGITUDINALE
// =============================================================================

async function loadArchaeologyView() {
  try {
    const data = await apiGet("/api/telemetry/archaeology");
    window._archaeologyData = data;

    // 1. Plotly Stacked Area Chart
    renderArchaeologyAreaChart(data);

    // 2. Matrice de Pérennité Cognitive
    filterAndRenderArchaeologyTable();
  } catch (err) {
    showToast("Échec chargement archéologie cognitive", "error");
  }
}

function renderArchaeologyAreaChart(data) {
  const container = document.getElementById("archaeology-area-chart");
  if (!container || !data || !data.monthly_series) return;

  const series = data.monthly_series;
  const topics = data.topics || [];

  const months = series.map((s) => s.month);
  const traces = [];

  topics.forEach((topic) => {
    traces.push({
      x: months,
      y: series.map((s) => s[topic] || 0),
      name: topic,
      stackgroup: "one",
      type: "scatter",
      mode: "none",
    });
  });

  const layout = {
    template: "plotly_dark",
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { l: 40, r: 20, t: 20, b: 40 },
    height: 380,
    xaxis: { gridcolor: "#1f293d", tickangle: -45 },
    yaxis: { gridcolor: "#1f293d" },
    legend: { orientation: "h", y: -0.25 },
  };

  Plotly.newPlot("archaeology-area-chart", traces, layout, { responsive: true, displayModeBar: false });
}

function filterAndRenderArchaeologyTable() {
  const tbody = document.getElementById("archaeology-table-body");
  const filterInput = document.getElementById("archaeology-search-filter");
  const q = (filterInput?.value || "").toLowerCase().trim();
  const archetypes = window._archaeologyData?.archetypes || [];

  const filtered = q ? archetypes.filter((a) => a.topic.toLowerCase().includes(q) || a.archetype.toLowerCase().includes(q)) : archetypes;

  tbody.innerHTML = "";
  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="py-4 text-center text-slate-500 italic">Aucun sujet correspondant.</td></tr>`;
    return;
  }

  filtered.forEach((item) => {
    const tr = document.createElement("tr");
    tr.className = "hover:bg-cyber-800/40 transition";

    let badgeClass = "bg-slate-800 text-slate-300 border-slate-700";
    if (item.archetype.includes("Pilier")) badgeClass = "bg-blue-950/80 text-blue-300 border-blue-500/50";
    else if (item.archetype.includes("Passion")) badgeClass = "bg-amber-950/80 text-amber-300 border-amber-500/50";
    else if (item.archetype.includes("Émergent")) badgeClass = "bg-emerald-950/80 text-emerald-300 border-emerald-500/50";

    tr.innerHTML = `
      <td class="py-2.5 px-3 font-semibold text-slate-200">${esc(item.topic)}</td>
      <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded text-[10px] font-sans border ${badgeClass}">${esc(item.archetype)}</span></td>
      <td class="py-2.5 px-3 text-right font-bold text-cyber-cyan">${esc(item.session_count)}</td>
      <td class="py-2.5 px-3 text-slate-400">${esc(item.first_focus)}</td>
      <td class="py-2.5 px-3 text-slate-400">${esc(item.last_focus)}</td>
      <td class="py-2.5 px-3 text-right text-slate-300">${esc(item.span_days)} j</td>
      <td class="py-2.5 px-3 text-right text-slate-400">${item.total_chars.toLocaleString("fr-FR")}</td>
    `;
    tbody.appendChild(tr);
  });
}

// =============================================================================
// VUE 4 : RYTHMES CIRCADIENS & CHRONOBIOLOGIE
// =============================================================================

async function loadCircadianView() {
  try {
    const data = await apiGet("/api/telemetry/circadian");

    document.getElementById("circadian-total-events").innerText = `${(data.total_events || 0).toLocaleString("fr-FR")} horodatages`;

    // 1. Heatmap 24h x 7j
    renderCircadianHeatmap(data);

    // 2. Bar chart des Quadrants
    renderCircadianQuadrants(data.quadrants);
  } catch (err) {
    showToast("Échec chargement rythmes circadiens", "error");
  }
}

function renderCircadianHeatmap(data) {
  const container = document.getElementById("circadian-heatmap");
  if (!container || !data) return;

  const trace = {
    type: "heatmap",
    z: data.matrix,
    x: data.hours.map((h) => `${h}h`),
    y: data.days,
    colorscale: "Viridis",
  };

  const layout = {
    template: "plotly_dark",
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { l: 80, r: 20, t: 10, b: 30 },
    height: 310,
    xaxis: { gridcolor: "#1f293d" },
    yaxis: { gridcolor: "#1f293d" },
  };

  Plotly.newPlot("circadian-heatmap", [trace], layout, { responsive: true, displayModeBar: false });
}

function renderCircadianQuadrants(quadrants) {
  const container = document.getElementById("circadian-quadrants-chart");
  if (!container || !quadrants) return;

  const trace = {
    type: "bar",
    x: Object.keys(quadrants),
    y: Object.values(quadrants),
    marker: {
      color: ["#8b5cf6", "#38bdf8", "#10b981", "#f59e0b"],
    },
  };

  const layout = {
    template: "plotly_dark",
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { l: 40, r: 20, t: 10, b: 40 },
    height: 270,
    xaxis: { gridcolor: "#1f293d", tickfont: { size: 10 } },
    yaxis: { gridcolor: "#1f293d" },
  };

  Plotly.newPlot("circadian-quadrants-chart", [trace], layout, { responsive: true, displayModeBar: false });
}

// =============================================================================
// VUE 5 : EXPLORATEUR ÉPISTÉMIQUE (CHATS & EMPREINTES)
// =============================================================================

function loadEpistemicView() {
  loadEpistemicChats();
  loadEpistemicFootprints();
}

let _chatSearchDebounceTimer = null;
async function loadEpistemicChats() {
  const q = document.getElementById("chats-search-input")?.value || "";
  const topic = document.getElementById("chats-topic-filter")?.value || "";
  const status = document.getElementById("chats-status-filter")?.value || "";

  const container = document.getElementById("chats-list-container");
  if (!container) return;

  try {
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (topic) params.set("topic", topic);
    if (status) params.set("status", status);
    params.set("limit", "50");

    const chats = await apiGet(`/api/epistemic/chats?${params.toString()}`);
    container.innerHTML = "";

    if (chats.length === 0) {
      container.innerHTML = `<p class="text-xs text-slate-500 italic p-4 text-center">Aucune session Gemini ne correspond aux critères.</p>`;
      return;
    }

    chats.forEach((s) => {
      const card = document.createElement("div");
      card.className = "cyber-card p-4 space-y-2.5 transition";

      let topics = [];
      try {
        topics = JSON.parse(s.extracted_topics_json || "[]");
      } catch (e) {}

      let notes = [];
      try {
        notes = JSON.parse(s.generated_notes_json || "[]");
      } catch (e) {}

      const topicsBadges = topics.map((t) => `<span class="px-1.5 py-0.5 rounded bg-cyber-800 text-slate-300 text-[10px] font-mono">#${esc(t)}</span>`).join(" ");

      const notesButtons = notes
        .map((n) => `<button class="text-cyber-cyan hover:underline text-[11px] font-mono mr-2" data-action="open-concept" data-slug="${esc(n)}">[[${esc(n)}]]</button>`)
        .join(" ");

      card.innerHTML = `
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="font-bold text-slate-100 text-xs">${esc((s.timestamp_start || "").slice(0, 16))}</span>
            <span class="px-2 py-0.5 rounded text-[10px] bg-cyber-blue/20 text-cyber-cyan font-mono">${esc(s.turn_count)} tours</span>
            <span class="px-2 py-0.5 rounded text-[10px] bg-cyber-800 text-slate-400 font-mono">${esc(s.user_char_count)} chars</span>
          </div>
          <div>${topicsBadges}</div>
        </div>
        <div class="text-xs text-slate-300 leading-relaxed">${esc(s.summary || "Aucun résumé cognitif")}</div>
        ${notesButtons ? `<div class="pt-1 text-xs"><span class="text-slate-500 text-[11px]">Notes liées : </span>${notesButtons}</div>` : ""}
        <div class="pt-1 flex justify-end">
          <button class="btn-cyber-ghost px-2.5 py-1 rounded text-[11px]" data-action="toggle-chat" data-session-id="${esc(s.session_id)}">
            💬 Voir les échanges
          </button>
        </div>
        <div class="chat-messages hidden space-y-2 pt-2 border-t border-cyber-700/60"></div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    showToast("Échec recherche sessions épistémiques", "error");
  }
}

async function toggleChatMessages(sessionId, btn) {
  const container = btn.closest(".cyber-card")?.querySelector(".chat-messages");
  if (!container) return;

  if (!container.classList.contains("hidden")) {
    container.classList.add("hidden");
    btn.innerText = "💬 Voir les échanges";
    return;
  }

  btn.innerText = "Chargement...";
  try {
    const msgs = await apiGet(`/api/epistemic/chats/${encodeURIComponent(sessionId)}/messages`);
    container.innerHTML = "";

    msgs.forEach((m, idx) => {
      const turnDiv = document.createElement("div");
      turnDiv.className = "p-2.5 rounded bg-cyber-900 border border-cyber-700/60 space-y-1.5 text-xs";
      turnDiv.innerHTML = `
        <div class="font-semibold text-slate-400 flex items-center justify-between">
          <span>Tour ${idx + 1} (${esc(m.user_char_count)} chars)</span>
          <span class="font-mono text-[10px]">${esc((m.timestamp || "").slice(11, 19))}</span>
        </div>
        <div class="text-slate-200 whitespace-pre-wrap"><b class="text-cyber-cyan">Utilisateur:</b> ${esc(m.user_prompt)}</div>
        <div class="text-slate-300 whitespace-pre-wrap border-t border-cyber-700/40 pt-1.5"><b class="text-purple-400">Assistant:</b> ${esc(m.ai_response)}</div>
      `;
      container.appendChild(turnDiv);
    });

    container.classList.remove("hidden");
    btn.innerText = "Fermer les échanges";
  } catch (err) {
    showToast("Impossible de charger les messages", "error");
    btn.innerText = "💬 Voir les échanges";
  }
}

async function loadEpistemicFootprints() {
  try {
    const data = await apiGet("/api/epistemic/footprints/summary");
    const kpis = data.kpis || {};

    document.getElementById("fp-kpi-total").innerText = (kpis.total || 0).toLocaleString("fr-FR");
    document.getElementById("fp-kpi-youtube").innerText = (kpis.youtube || 0).toLocaleString("fr-FR");
    document.getElementById("fp-kpi-search").innerText = (kpis.search || 0).toLocaleString("fr-FR");
    document.getElementById("fp-kpi-clustered").innerText = (kpis.clustered || 0).toLocaleString("fr-FR");
    document.getElementById("fp-kpi-linked").innerText = (kpis.linked || 0).toLocaleString("fr-FR");

    // Top 15 Chaînes & Domaines
    const topList = document.getElementById("top-channels-list");
    if (topList) {
      topList.innerHTML = "";
      (data.top_channels_and_domains || []).forEach((c) => {
        const item = document.createElement("div");
        item.className = "flex items-center justify-between p-2 rounded bg-cyber-900 border border-cyber-700/60";
        item.innerHTML = `
          <span class="text-slate-200 font-semibold truncate max-w-xs">${esc(c.channel_or_domain)}</span>
          <div class="flex items-center gap-2">
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-cyber-800 text-slate-400 font-mono">${esc(c.source)}</span>
            <span class="font-bold text-cyber-cyan font-mono">${esc(c.footprint_count)}</span>
          </div>
        `;
        topList.appendChild(item);
      });
    }

    // Burst Clusters
    const burstList = document.getElementById("burst-clusters-list");
    if (burstList) {
      burstList.innerHTML = "";
      (data.burst_clusters || []).forEach((b) => {
        const item = document.createElement("div");
        item.className = "p-2 rounded bg-cyber-900 border border-cyber-700/60 space-y-1";
        item.innerHTML = `
          <div class="flex items-center justify-between">
            <span class="font-bold text-amber-300 font-mono text-[11px]">${esc(b.cluster_id)}</span>
            <span class="text-emerald-400 font-bold">${esc(b.event_count)} événements</span>
          </div>
          <div class="text-[11px] text-slate-400 truncate">${esc(b.samples || "")}</div>
        `;
        burstList.appendChild(item);
      });
    }

    // Recherche initiale dans les empreintes
    searchFootprintsTable();
  } catch (err) {
    console.warn("Échec chargement empreintes :", err);
  }
}

async function searchFootprintsTable() {
  const q = document.getElementById("fp-search-query")?.value || "";
  const source = document.getElementById("fp-source-filter")?.value || "Toutes";
  const tbody = document.getElementById("fp-table-body");
  if (!tbody) return;

  try {
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (source) params.set("source", source);
    params.set("limit", "100");

    const list = await apiGet(`/api/epistemic/footprints/search?${params.toString()}`);
    tbody.innerHTML = "";

    if (list.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="py-4 text-center text-slate-500 italic">Aucune empreinte correspondante.</td></tr>`;
      return;
    }

    list.forEach((fp) => {
      const tr = document.createElement("tr");
      tr.className = "hover:bg-cyber-800/40 transition";
      tr.innerHTML = `
        <td class="py-2 px-3 text-slate-400">${esc((fp.timestamp || "").slice(0, 16))}</td>
        <td class="py-2 px-3"><span class="px-1.5 py-0.5 rounded text-[10px] bg-cyber-800 text-slate-300">${esc(fp.source)}</span></td>
        <td class="py-2 px-3 text-slate-200 font-semibold">${esc(fp.channel_or_domain || "-")}</td>
        <td class="py-2 px-3 text-slate-100 max-w-sm truncate" title="${esc(fp.title_or_query)}">${esc(fp.title_or_query || "-")}</td>
        <td class="py-2 px-3 text-purple-300">${esc(fp.semantic_topic || "-")}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    showToast("Échec recherche empreintes", "error");
  }
}

// =============================================================================
// VUE 6 : STUDIO KANBAN SOTA
// =============================================================================

async function initKanbanView() {
  try {
    const projects = await apiGet("/api/kanban/projects");
    state.projects = projects;

    const select = document.getElementById("kanban-project-select");
    if (!select) return;

    select.innerHTML = "";
    projects.forEach((p) => {
      const opt = document.createElement("option");
      opt.value = p.project_id;
      opt.innerText = `${p.name} (${p.prefix})`;
      select.appendChild(opt);
    });

    state.activeProjectId = projects[0]?.project_id || "exocortex";
    select.value = state.activeProjectId;

    await loadKanbanTasks();
  } catch (err) {
    showToast("Échec initialisation Kanban", "error");
  }
}

async function loadKanbanTasks() {
  try {
    const pid = state.activeProjectId;
    const tag = document.getElementById("kanban-filter-tag")?.value || "Tous";
    const q = document.getElementById("kanban-search-input")?.value || "";

    const params = new URLSearchParams();
    params.set("project_id", pid);
    if (tag && tag !== "Tous") params.set("tag", tag);
    if (q) params.set("q", q);

    const tasks = await apiGet(`/api/kanban/tasks?${params.toString()}`);
    state.kanbanTasks = tasks;

    // Mise à jour de la liste des tags pour le filtre
    updateKanbanTagsFilter(tasks);

    // Distribution des tâches par colonne
    renderKanbanColumns(tasks);
  } catch (err) {
    showToast("Échec chargement des tâches Kanban", "error");
  }
}

function updateKanbanTagsFilter(tasks) {
  const select = document.getElementById("kanban-filter-tag");
  if (!select) return;

  const currentVal = select.value;
  const tags = new Set();
  tasks.forEach((t) => {
    if (t.component_tag) tags.add(t.component_tag);
  });

  select.innerHTML = `<option value="Tous">Tous les modules</option>`;
  Array.from(tags).sort().forEach((tag) => {
    const opt = document.createElement("option");
    opt.value = tag;
    opt.innerText = tag;
    select.appendChild(opt);
  });
  if (tags.has(currentVal)) select.value = currentVal;
}

function renderKanbanColumns(tasks) {
  const cols = {
    radar: document.querySelector('.kanban-col[data-col-status="radar"]'),
    needs_spec: document.querySelector('.kanban-col[data-col-status="needs_spec"]'),
    ready_or_progress: document.querySelector('.kanban-col[data-col-status="ready_or_progress"]'),
    done: document.querySelector('.kanban-col[data-col-status="done"]'),
  };

  const iceboxContainer = document.getElementById("icebox-cards-list");
  if (iceboxContainer) iceboxContainer.innerHTML = "";

  Object.values(cols).forEach((col) => {
    if (col) {
      const list = col.querySelector(".col-cards-list");
      if (list) list.innerHTML = "";
    }
  });

  const counts = { radar: 0, needs_spec: 0, ready_or_progress: 0, done: 0, icebox: 0 };

  tasks.forEach((task) => {
    const status = task.status;
    let targetColKey = status;
    if (status === "ready_for_agent" || status === "in_progress") {
      targetColKey = "ready_or_progress";
    }

    if (status === "icebox") {
      counts.icebox++;
      if (iceboxContainer) iceboxContainer.appendChild(createKanbanCardElement(task));
      return;
    }

    if (cols[targetColKey]) {
      counts[targetColKey]++;
      const list = cols[targetColKey].querySelector(".col-cards-list");
      if (list) list.appendChild(createKanbanCardElement(task));
    }
  });

  // Mise à jour des compteurs
  Object.keys(counts).forEach((key) => {
    if (cols[key]) {
      const badge = cols[key].querySelector(".col-count");
      if (badge) badge.innerText = counts[key];
    }
  });
}

function createKanbanCardElement(task) {
  const card = document.createElement("div");
  card.className = "kanban-card space-y-2";
  card.id = `card-${task.task_id}`;

  const prioBadges = {
    1: '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">P1</span>',
    2: '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/40">P2</span>',
    3: '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40">P3</span>',
    4: '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-slate-700 text-slate-300">P4</span>',
  };

  let statusBadge = "";
  if (task.status === "in_progress") {
    statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 pulse-glow">EN COURS</span>';
  } else if (task.status === "ready_for_agent") {
    statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-cyber-cyan/20 text-cyber-cyan border border-cyber-cyan/40">PRÊT CODEUR</span>';
  }

  const tid = esc(task.task_id);
  card.innerHTML = `
    <div class="flex items-center justify-between gap-1 text-[11px]">
      <div class="flex items-center gap-1.5 font-mono font-bold text-cyber-cyan">
        <span>${tid}</span>
        ${prioBadges[task.priority] || ""}
        <span class="px-1 py-0.5 rounded text-[10px] bg-cyber-800 text-slate-400 font-sans">${esc(task.complexity)}</span>
      </div>
      <div>${statusBadge}</div>
    </div>

    <div class="font-bold text-xs text-slate-100 leading-tight">${esc(task.title)}</div>
    <div class="text-[10px] text-purple-300 font-mono">#${esc(task.component_tag || "general")}</div>

    ${task.summary_pitch ? `<p class="text-[11px] text-slate-400 line-clamp-2 leading-snug">${esc(task.summary_pitch)}</p>` : ""}

    <!-- Actions 1-Clic SOTA (délégation d'événements : aucun handler inline, CSP v0.5.2) -->
    <div class="pt-2 border-t border-cyber-700/60 flex flex-wrap items-center gap-1.5">
      <button class="btn-cyber-action px-2 py-1 rounded text-[10px] flex items-center gap-1 font-semibold" title="Copier Context-Pack haute-fidélité pour Gemini Web" data-action="copy-context-pack" data-task-id="${tid}">
        <span>📋</span> <span>Context-Pack</span>
      </button>

      <button class="btn-cyber-primary px-2 py-1 rounded text-[10px] flex items-center gap-1 font-semibold" title="Extraire le prompt codeur et basculer en cours" data-action="copy-coder-prompt" data-task-id="${tid}">
        <span>🤖</span> <span>Prompt Codeur</span>
      </button>

      ${task.spec_file_path ? `<button class="btn-cyber-ghost px-2 py-1 rounded text-[10px]" title="Consulter la spec" data-action="view-spec" data-task-id="${tid}">📄 Spec</button>` : ""}

      <!-- Sélecteur rapide de statut -->
      <select class="bg-cyber-900 border border-cyber-700 text-slate-300 text-[10px] rounded px-1.5 py-1 outline-none ml-auto" data-action="change-status" data-task-id="${tid}">
        <option value="radar" ${task.status === "radar" ? "selected" : ""}>Radar</option>
        <option value="needs_spec" ${task.status === "needs_spec" ? "selected" : ""}>Needs Spec</option>
        <option value="ready_for_agent" ${task.status === "ready_for_agent" ? "selected" : ""}>Prêt</option>
        <option value="in_progress" ${task.status === "in_progress" ? "selected" : ""}>En cours</option>
        <option value="done" ${task.status === "done" ? "selected" : ""}>Terminé</option>
        <option value="icebox" ${task.status === "icebox" ? "selected" : ""}>Frigo</option>
      </select>

      <button class="text-slate-500 hover:text-rose-400 text-xs px-1" title="Supprimer la tâche" data-action="delete-task" data-task-id="${tid}">🗑️</button>
    </div>
  `;

  return card;
}

// Actions Métier SOTA
async function copyTaskContextPack(taskId) {
  try {
    const data = await apiGet(`/api/kanban/tasks/${encodeURIComponent(taskId)}/context-pack`);
    await copyToClipboard(data.prompt);
    showToast(`Context-Pack pour ${taskId} copié ! Prêt pour Gemini Web App.`, "success");
  } catch (err) {
    showToast(`Erreur génération Context-Pack : ${err.message}`, "error");
  }
}

async function copyTaskCoderPrompt(taskId) {
  try {
    const data = await apiGet(`/api/kanban/tasks/${encodeURIComponent(taskId)}/coder-prompt?mark_in_progress=true`);
    if (!data.prompt) {
      showToast("Aucune spec ou prompt codeur attaché à ce ticket.", "warning");
      return;
    }
    await copyToClipboard(data.prompt);
    showToast(`Prompt Codeur pour ${taskId} copié ! Ticket passé 'en cours'.`, "success");
    await loadKanbanTasks();
  } catch (err) {
    showToast(`Erreur prompt codeur : ${err.message}`, "error");
  }
}

async function viewTaskSpec(taskId) {
  try {
    const task = state.kanbanTasks.find((t) => t.task_id === taskId);
    if (!task || !task.spec_file_path) {
      showToast("Aucun chemin de spec disponible.", "warning");
      return;
    }
    const coderPromptData = await apiGet(`/api/kanban/tasks/${encodeURIComponent(taskId)}/coder-prompt`);
    openMarkdownModal(`Spécification Technique : ${taskId} - ${task.title}`, coderPromptData.prompt || "# Spécification\n\nContenu non extrait.");
  } catch (err) {
    showToast(`Impossible de lire la spec : ${err.message}`, "error");
  }
}

async function changeTaskStatus(taskId, newStatus) {
  try {
    await apiPatch(`/api/kanban/tasks/${encodeURIComponent(taskId)}/status`, { status: newStatus });
    showToast(`Statut de ${taskId} mis à jour : ${newStatus}`, "info");
    await loadKanbanTasks();
  } catch (err) {
    showToast(`Échec mise à jour du statut : ${err.message}`, "error");
  }
}

async function deleteTask(taskId) {
  if (!confirm(`Confirmer la suppression de la tâche ${taskId} ?`)) return;
  try {
    await apiDelete(`/api/kanban/tasks/${encodeURIComponent(taskId)}`);
    showToast(`Tâche ${taskId} supprimée.`, "info");
    await loadKanbanTasks();
  } catch (err) {
    showToast(`Erreur suppression : ${err.message}`, "error");
  }
}

// =============================================================================
// INITIALISATION DES ÉVÉNEMENTS & DOM LOADED
// =============================================================================

/**
 * Délégation d'événements pour les éléments générés dynamiquement (v0.5.2, D2) :
 * remplace les attributs onclick/onchange inline, interdits par la Content-Security-Policy.
 */
function bindDelegatedActions() {
  document.addEventListener("click", (e) => {
    const el = e.target.closest("[data-action]");
    if (!el || el.tagName === "SELECT") return;
    const { action, taskId, slug, sessionId } = el.dataset;
    switch (action) {
      case "open-concept":
        loadAndOpenConcept(slug);
        break;
      case "toggle-chat":
        toggleChatMessages(sessionId, el);
        break;
      case "copy-context-pack":
        copyTaskContextPack(taskId);
        break;
      case "copy-coder-prompt":
        copyTaskCoderPrompt(taskId);
        break;
      case "view-spec":
        viewTaskSpec(taskId);
        break;
      case "delete-task":
        deleteTask(taskId);
        break;
    }
  });
  document.addEventListener("change", (e) => {
    const el = e.target.closest("[data-action='change-status']");
    if (el) changeTaskStatus(el.dataset.taskId, el.value);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  bindDelegatedActions();

  // 1. Initialisation Bandeau & Statut
  updateSystemStatus();
  setInterval(updateSystemStatus, 10000);

  // 2. Boutons d'Action Rapides Topbar
  document.getElementById("btn-open-bootloader")?.addEventListener("click", () => {
    openMarkdownModal("00_BOOTLOADER_DEMAIN.md — Priorités & Context Bootloader", state.bootloaderContent || "# Bootloader\n\nAucune consigne active.");
  });

  document.getElementById("btn-trigger-consolidate")?.addEventListener("click", async () => {
    try {
      showToast("Lancement de la consolidation nocturne...", "info");
      const res = await apiPost("/api/system/trigger-consolidate", {});
      showToast(res.message, "success");
    } catch (err) {
      showToast(`Erreur déclenchement consolidation : ${err.message}`, "error");
    }
  });

  document.getElementById("btn-trigger-drive")?.addEventListener("click", async () => {
    try {
      showToast("Compilation des méga-documents Google Drive...", "info");
      const res = await apiPost("/api/system/trigger-drive-compile", {});
      showToast("4 méga-documents compilés avec succès dans Vault_Data/Google_Drive_Sync/", "success");
    } catch (err) {
      showToast(`Erreur compilation Drive : ${err.message}`, "error");
    }
  });

  // 3. Navigation par Onglets
  document.querySelectorAll(".nav-tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      switchView(btn.dataset.view);
    });
  });

  // 4. Événements Vue 1 : Chronologie
  document.getElementById("timeline-date-select")?.addEventListener("change", (e) => {
    state.selectedDate = e.target.value;
    loadTimelineForDate(state.selectedDate);
  });
  document.getElementById("btn-refresh-timeline")?.addEventListener("click", () => {
    if (state.selectedDate) loadTimelineForDate(state.selectedDate);
  });
  document.getElementById("timeline-search-filter")?.addEventListener("input", filterAndRenderTimelineTable);

  // 5. Événements Vue 2 : Cartographie & GraphRAG
  document.getElementById("btn-run-graphrag")?.addEventListener("click", runGraphRAGSearch);
  document.getElementById("graphrag-input-query")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") runGraphRAGSearch();
  });

  // 6. Événements Vue 3 : Archéologie
  document.getElementById("archaeology-search-filter")?.addEventListener("input", filterAndRenderArchaeologyTable);

  // 7. Événements Vue 5 : Épistémique
  document.getElementById("epistemic-tab-chats")?.addEventListener("click", () => {
    document.getElementById("epistemic-panel-chats").classList.remove("hidden");
    document.getElementById("epistemic-panel-footprints").classList.add("hidden");
    document.getElementById("epistemic-tab-chats").className = "px-3 py-1 text-xs rounded font-medium bg-cyber-blue/30 text-cyber-cyan border border-cyber-blue/50";
    document.getElementById("epistemic-tab-footprints").className = "px-3 py-1 text-xs rounded font-medium text-slate-400 hover:text-slate-200";
  });
  document.getElementById("epistemic-tab-footprints")?.addEventListener("click", () => {
    document.getElementById("epistemic-panel-chats").classList.add("hidden");
    document.getElementById("epistemic-panel-footprints").classList.remove("hidden");
    document.getElementById("epistemic-tab-footprints").className = "px-3 py-1 text-xs rounded font-medium bg-cyber-blue/30 text-cyber-cyan border border-cyber-blue/50";
    document.getElementById("epistemic-tab-chats").className = "px-3 py-1 text-xs rounded font-medium text-slate-400 hover:text-slate-200";
  });

  document.getElementById("chats-search-input")?.addEventListener("input", () => {
    clearTimeout(_chatSearchDebounceTimer);
    _chatSearchDebounceTimer = setTimeout(loadEpistemicChats, 250);
  });
  document.getElementById("chats-topic-filter")?.addEventListener("change", loadEpistemicChats);
  document.getElementById("chats-status-filter")?.addEventListener("change", loadEpistemicChats);
  document.getElementById("fp-search-query")?.addEventListener("input", searchFootprintsTable);
  document.getElementById("fp-source-filter")?.addEventListener("change", searchFootprintsTable);

  // 8. Événements Vue 6 : Kanban
  document.getElementById("kanban-project-select")?.addEventListener("change", (e) => {
    state.activeProjectId = e.target.value;
    loadKanbanTasks();
  });
  document.getElementById("kanban-filter-tag")?.addEventListener("change", loadKanbanTasks);
  document.getElementById("kanban-search-input")?.addEventListener("input", loadKanbanTasks);

  document.getElementById("btn-toggle-icebox")?.addEventListener("click", () => {
    const sec = document.getElementById("kanban-icebox-section");
    if (sec) sec.classList.toggle("hidden");
  });

  // Modale Nouveau Projet
  document.getElementById("btn-new-project-modal")?.addEventListener("click", () => {
    document.getElementById("modal-new-project")?.classList.remove("hidden");
  });
  document.getElementById("btn-close-modal-proj")?.addEventListener("click", () => {
    document.getElementById("modal-new-project")?.classList.add("hidden");
  });
  document.getElementById("btn-cancel-proj")?.addEventListener("click", () => {
    document.getElementById("modal-new-project")?.classList.add("hidden");
  });
  document.getElementById("btn-save-proj")?.addEventListener("click", async () => {
    const name = document.getElementById("new-proj-name")?.value.trim();
    const pid = document.getElementById("new-proj-id")?.value.trim();
    const prefix = document.getElementById("new-proj-prefix")?.value.trim();
    const repo = document.getElementById("new-proj-repo")?.value.trim();
    const desc = document.getElementById("new-proj-desc")?.value.trim();

    if (!name || !pid || !prefix) {
      showToast("Nom, Slug et Préfixe sont obligatoires.", "warning");
      return;
    }

    try {
      await apiPost("/api/kanban/projects", {
        project_id: pid,
        name: name,
        prefix: prefix,
        repo_path: repo || null,
        description: desc || "",
      });
      showToast(`Projet '${name}' créé !`, "success");
      document.getElementById("modal-new-project")?.classList.add("hidden");
      await initKanbanView();
    } catch (err) {
      showToast(`Échec création projet : ${err.message}`, "error");
    }
  });

  // Modale Nouvelle Tâche
  document.getElementById("btn-new-task-modal")?.addEventListener("click", () => {
    document.getElementById("modal-new-task")?.classList.remove("hidden");
  });
  document.getElementById("btn-close-modal-task")?.addEventListener("click", () => {
    document.getElementById("modal-new-task")?.classList.add("hidden");
  });
  document.getElementById("btn-cancel-task")?.addEventListener("click", () => {
    document.getElementById("modal-new-task")?.classList.add("hidden");
  });
  document.getElementById("btn-save-task")?.addEventListener("click", async () => {
    const title = document.getElementById("new-task-title")?.value.trim();
    const tag = document.getElementById("new-task-tag")?.value.trim();
    const prio = parseInt(document.getElementById("new-task-priority")?.value, 10);
    const cplx = document.getElementById("new-task-complexity")?.value;
    const status = document.getElementById("new-task-status")?.value;
    const pitch = document.getElementById("new-task-pitch")?.value.trim();

    if (!title) {
      showToast("Le titre de la tâche est obligatoire.", "warning");
      return;
    }

    try {
      await apiPost("/api/kanban/tasks", {
        project_id: state.activeProjectId,
        title: title,
        component_tag: tag || "general",
        priority: prio,
        complexity: cplx,
        initial_status: status,
        summary_pitch: pitch,
      });
      showToast("Tâche créée avec succès !", "success");
      document.getElementById("modal-new-task")?.classList.add("hidden");
      document.getElementById("new-task-title").value = "";
      document.getElementById("new-task-pitch").value = "";
      await loadKanbanTasks();
    } catch (err) {
      showToast(`Échec création tâche : ${err.message}`, "error");
    }
  });

  // Modale Ingestion Spec Markdown
  document.getElementById("btn-open-ingest-modal")?.addEventListener("click", () => {
    const taskSelect = document.getElementById("ingest-target-task");
    if (taskSelect) {
      taskSelect.innerHTML = `<option value="">Détection automatique (via frontmatter YAML ou titre H1)</option>`;
      (state.kanbanTasks || []).forEach((t) => {
        const opt = document.createElement("option");
        opt.value = t.task_id;
        opt.innerText = `${t.task_id} — ${t.title}`;
        taskSelect.appendChild(opt);
      });
    }
    document.getElementById("modal-ingest-spec")?.classList.remove("hidden");
  });
  document.getElementById("btn-close-modal-ingest")?.addEventListener("click", () => {
    document.getElementById("modal-ingest-spec")?.classList.add("hidden");
  });
  document.getElementById("btn-cancel-ingest")?.addEventListener("click", () => {
    document.getElementById("modal-ingest-spec")?.classList.add("hidden");
  });
  document.getElementById("btn-submit-ingest")?.addEventListener("click", async () => {
    const targetTaskId = document.getElementById("ingest-target-task")?.value || null;
    const rawMarkdown = document.getElementById("ingest-spec-content")?.value.trim();

    if (!rawMarkdown) {
      showToast("Le contenu de la spec ne peut pas être vide.", "warning");
      return;
    }

    try {
      const updated = await apiPost("/api/kanban/specs/ingest", {
        raw_markdown: rawMarkdown,
        target_task_id: targetTaskId,
      });
      showToast(`Spec ingérée pour ${updated.task_id} ! Statut: ready_for_agent.`, "success");
      document.getElementById("modal-ingest-spec")?.classList.add("hidden");
      document.getElementById("ingest-spec-content").value = "";
      await loadKanbanTasks();
    } catch (err) {
      showToast(`Erreur ingestion spec : ${err.message}`, "error");
    }
  });

  // Fermeture Modale Markdown
  document.getElementById("btn-close-modal-markdown")?.addEventListener("click", closeMarkdownModal);
  document.getElementById("btn-copy-modal-raw")?.addEventListener("click", async () => {
    if (state.modalRawMarkdown) {
      await copyToClipboard(state.modalRawMarkdown);
      showToast("Markdown brut copié dans le presse-papier.", "success");
    }
  });

  // 9. Démarrage Vue par Défaut
  switchView("timeline");
});

