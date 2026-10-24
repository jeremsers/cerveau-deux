---
task_id: "EXO-014"
project_id: "exocortex"
component_tag: "web-gui-fastapi"
title: "v0.5.0 — Exocortex Web Command Center (API FastAPI + GUI Web Moderne)"
status: "ready_for_agent"
---
# EXO-014 — v0.5.0 — Exocortex Web Command Center (API FastAPI + GUI Web Moderne)

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif Architectural
Remplacer l'interface monolithique Streamlit (`src/dashboard/app.py`, qui ré-exécute tout le script à chaque clic) par une véritable application Web réactive, fluide et maîtrisée :
1. **Un Backend REST & Temps Réel (`src/api/server.py` sous FastAPI / Uvicorn)** exposant en JSON l'intégralité des moteurs de l'Exocortex (`DBManager`, `KanbanEngine`, `HybridGraphRAG`, `HardwareProbe`, `DriftGuard`, `Bootloader`).
2. **Un Frontend Web Moderne (`src/web_gui/`)** servi directement par FastAPI sur `[http://127.0.0.1:8500](http://127.0.0.1:8500)`, offrant une navigation instantanée sans rechargement (SPA), un thème Cyber-Dark sur-mesure (Tailwind CSS), des graphiques interactifs (Plotly.js / Chart), un explorateur GraphRAG visuel et un studio Kanban interactif avec copie 1-clic native (`navigator.clipboard`).

### 1.2 Chantier 1 : Backend API FastAPI (`src/api/server.py`)
Créer `src/api/server.py` exposant les routes REST JSON suivantes (avec CORS activé pour le dev local sur `localhost:4321` / `localhost:5173`) :
- **Système, VRAM & Proactivité :**
  - `GET /api/system/status` : Retourne la VRAM libre/totale (`HardwareProbe.get_vram_info()`), le statut d'Ollama (`llm_client.is_alive()`), le contenu de `00_BOOTLOADER_DEMAIN.md` et l'état temps réel du `DriftGuard` (`drift_state.json`).
  - `POST /api/system/trigger-consolidate` : Lance `NightConsolidator().consolidate()` en tâche de fond (`BackgroundTasks`) et retourne le statut.
  - `POST /api/system/trigger-drive-compile` : Exécute `DriveCompiler().compile_all()` et retourne les fichiers générés.
- **Télémétrie & Analytique (Lecture Seule `DBManager(read_only=True)`) :**
  - `GET /api/telemetry/kpis` : Retourne `fetch_macro_kpis()`.
  - `GET /api/telemetry/dates` : Retourne `fetch_all_activity_dates()`.
  - `GET /api/telemetry/timeline?date=YYYY-MM-DD` : Retourne `fetch_timeline_for_date(date)`.
  - `GET /api/telemetry/treemap` : Retourne `fetch_treemap_data()`.
  - `GET /api/telemetry/archaeology` : Retourne `fetch_archaeology_sessions()` + calcul des archétypes cognitifs (*Pilier Fondamental*, *Passion Éphémère*, *Sujet Émergent*).
  - `GET /api/telemetry/circadian` : Retourne la matrice `7j x 24h` et les compteurs par quadrant horaire.
- **Explorateur Épistémique, Empreintes & GraphRAG :**
  - `GET /api/epistemic/chats?q=&topic=&status=&limit=50` : Retourne `search_chat_sessions()`.
  - `GET /api/epistemic/chats/{session_id}/messages` : Retourne `fetch_messages_for_session(session_id)`.
  - `GET /api/epistemic/footprints/summary` : Retourne `fetch_footprints_summary()`, `fetch_top_channels_and_domains()` et `fetch_burst_clusters_summary()`.
  - `GET /api/epistemic/footprints/search?q=&source=&clustered=false&linked=false` : Retourne `search_footprints()`.
  - `GET /api/graphrag/search?q=&top_k=5&topic=` : Exécute `HybridGraphRAG().search_hybrid()` et retourne les nœuds primaires (Hop 0), les voisins `[[wikilinks]]` (Hop 1) et les arêtes `{source, target}` pour le rendu visuel du graphe.
  - `GET /api/concepts/{slug}` : Lit et retourne via `parse_concept_file()` le frontmatter, le corps Markdown et la télémétrie d'une fiche de `02_Concepts/`.
- **Kanban Exécutif & Studio SOTA (`KanbanEngine`) :**
  - `GET /api/kanban/projects` & `POST /api/kanban/projects` : Liste et crée des projets (`ProjectRecord`).
  - `GET /api/kanban/tasks?project_id=exocortex` & `POST /api/kanban/tasks` : Liste et crée des tickets Kanban.
  - `PATCH /api/kanban/tasks/{task_id}/status` : Change le statut d'un ticket (`radar`, `needs_spec`, `ready_for_agent`, `in_progress`, `done`, `icebox`) et recompile `AGENT_QUEUE.md`.
  - `DELETE /api/kanban/tasks/{task_id}` : Supprime un ticket.
  - `GET /api/kanban/tasks/{task_id}/context-pack` : Génère et retourne `build_sota_context_pack_prompt(task_id)`.
  - `GET /api/kanban/tasks/{task_id}/coder-prompt` : Retourne `extract_coder_prompt_from_spec(task_id)` et passe optionnellement le ticket en `in_progress`.
  - `POST /api/kanban/specs/ingest` : Reçoit `{"raw_markdown": str, "target_task_id": Optional[str]}` et exécute `attach_spec_to_task()`.

### 1.3 Chantier 2 : Interface Web Réactive (`src/web_gui/`)
Servie à la racine `GET /` par FastAPI (`StaticFiles`), l'interface Web (`index.html`, `app.js`, `styles.css`) utilise une architecture modulaire propre (Tailwind CSS + Plotly.js + Marked.js pour le rendu Markdown) et propose 6 vues instantanées :
1. **Bandeau Global Temps Réel :** Jauge VRAM live, statut Ollama, alerte `DriftGuard` si active, et tiroir dépliable **🚀 Context Bootloader** (avec rendu Markdown et cases à cocher interactives).
2. **Vue 1 — Chronologie & Tunnels d'Hyperfocus :** Sélecteur de date, KPIs journaliers, diagramme de Gantt interactif Plotly, cartes des tunnels $\ge 30$ min et table filtrable incluant `url_or_path` (infos Git/URL).
3. **Vue 2 — Cartographie & GraphRAG Visuel :** Treemap Plotly (`Mode -> Topic -> Exécutable`), Donut des modes cognitifs, et barre de test live `HybridGraphRAG` affichant les fiches Hop 0 et les rebonds Hop 1 `[[wikilinks]]`.
4. **Vue 3 — Archéologie Longitudinale (2024-2026) :** Aire empilée mensuelle Plotly et matrice filtrable des Piliers Fondamentaux vs Passions Éphémères.
5. **Vue 4 — Rythmes Circadiens :** Heatmap 24h x 7j, histogramme des 4 quadrants horaires et carte de diagnostic chronobiologique.
6. **Vue 5 — Explorateur Épistémique (Chats & Empreintes) :** Recherche full-text instantanée (debounce 250ms) dans les sessions/messages Gemini + modale de lecture des fiches `02_Concepts/` liées + explorateur des 73k empreintes et Burst Clusters.
7. **Vue 6 — Studio Kanban SOTA :** Board 4 colonnes (`Radar`, `Spec Requise`, `Prêt & En Cours`, `Terminé`) + `Frigo`, changement de colonne en 1 clic ou glisser-déposer, boutons `📋 Copier Context-Pack` et `🤖 Copier Prompt Codeur` utilisant `navigator.clipboard.writeText()`, et modale d'ingestion directe des specs Markdown.

### 1.4 Intégration CLI & Lanceurs (`run_exocortex.py`, `requirements.txt`, `start_exocortex.bat`)
- Ajouter `fastapi>=0.110.0` et `uvicorn>=0.29.0` dans `requirements.txt`.
- Ajouter `--web` (port par défaut `8500`) dans `run_exocortex.py` pour démarrer le serveur FastAPI/Uvicorn et ouvrir automatiquement le navigateur.

---