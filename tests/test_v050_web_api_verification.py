"""
Suite de tests de validation d'intégration pour EXO-014 (v0.5.0).
Valide l'API REST FastAPI, le Command Center Web, les moteurs télémétriques,
le GraphRAG hybride et le studio Kanban SOTA.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Generator

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import pytest
from fastapi.testclient import TestClient

from src.api.server import app
from src.config import settings
from src.database.db_manager import DBManager, KanbanTaskRecord, ProjectRecord
from src.utils.markdown_io import ConceptFrontmatter, ParsedConceptNote, write_concept_file


@pytest.fixture(scope="module")
def api_client() -> Generator[TestClient, None, None]:
    """Client de test FastAPI pour les requêtes HTTP in-memory."""
    settings.ensure_directories()
    with TestClient(app) as client:
        yield client


# ==============================================================================
# TEST 1 : SYSTÈME & TÉLÉMÉTRIE COGNITIVE
# ==============================================================================

def test_api_system_and_telemetry_endpoints(api_client: TestClient) -> None:
    """Valide les routes /api/system/* et /api/telemetry/*."""
    # 1. Statut Système (VRAM, Ollama, Drift, Bootloader)
    res_status = api_client.get("/api/system/status")
    assert res_status.status_code == 200
    status_data = res_status.json()
    assert "vram" in status_data
    assert "free_gb" in status_data["vram"]
    assert "total_gb" in status_data["vram"]
    assert "ollama_alive" in status_data
    assert "bootloader_content" in status_data
    assert "drift_state" in status_data

    # 2. KPIs Télémetrie
    res_kpis = api_client.get("/api/telemetry/kpis")
    assert res_kpis.status_code == 200
    kpis_data = res_kpis.json()
    assert isinstance(kpis_data, dict)

    # 3. Liste des Dates
    res_dates = api_client.get("/api/telemetry/dates")
    assert res_dates.status_code == 200
    dates_list = res_dates.json()
    assert isinstance(dates_list, list)

    # 4. Chronologie Journalière
    test_date = dates_list[0] if dates_list else "2026-03-30"
    res_timeline = api_client.get(f"/api/telemetry/timeline?date={test_date}")
    assert res_timeline.status_code == 200
    timeline_data = res_timeline.json()
    assert "events" in timeline_data
    assert "focus_tunnels" in timeline_data
    assert "daily_metric" in timeline_data

    # Test date invalide
    res_bad_date = api_client.get("/api/telemetry/timeline?date=bad-date-format")
    assert res_bad_date.status_code == 400

    # 5. Treemap Hiérarchique
    res_tree = api_client.get("/api/telemetry/treemap")
    assert res_tree.status_code == 200
    tree_data = res_tree.json()
    assert isinstance(tree_data, list)

    # 6. Archéologie Longitudinale
    res_arch = api_client.get("/api/telemetry/archaeology")
    assert res_arch.status_code == 200
    arch_data = res_arch.json()
    assert "archetypes" in arch_data
    assert "monthly_series" in arch_data
    assert "topics" in arch_data

    # 7. Rythmes Circadiens
    res_circ = api_client.get("/api/telemetry/circadian")
    assert res_circ.status_code == 200
    circ_data = res_circ.json()
    assert "days" in circ_data
    assert "hours" in circ_data
    assert "matrix" in circ_data
    assert len(circ_data["days"]) == 7
    assert len(circ_data["hours"]) == 24
    assert len(circ_data["matrix"]) == 7
    assert "quadrants" in circ_data


# ==============================================================================
# TEST 2 : KANBAN MULTI-PROJETS & WORKFLOW SOTA
# ==============================================================================

def test_api_kanban_crud_and_sota_workflow(api_client: TestClient) -> None:
    """Valide le cycle de vie complet des tickets et le pont presse-papier SOTA."""
    test_pid = f"test-proj-{int(datetime.now().timestamp())}"

    try:
        # 1. Création de projet
        res_create_proj = api_client.post(
            "/api/kanban/projects",
            json={
                "project_id": test_pid,
                "name": "Projet Test Web API",
                "prefix": "TPW",
                "repo_path": str(_PROJECT_ROOT),
                "description": "Projet créé par la suite de tests v0.5.0",
            },
        )
        assert res_create_proj.status_code == 200
        proj_data = res_create_proj.json()
        assert proj_data["project_id"] == test_pid

        # 2. Liste des projets
        res_projects = api_client.get("/api/kanban/projects")
        assert res_projects.status_code == 200
        assert any(p["project_id"] == test_pid for p in res_projects.json())

        # 3. Création de tâche
        res_create_task = api_client.post(
            "/api/kanban/tasks",
            json={
                "project_id": test_pid,
                "title": "Implémentation Sonde WebSocket",
                "component_tag": "telemetry",
                "summary_pitch": "Ajouter le support du streaming bidirectionnel",
                "priority": 1,
                "complexity": "M",
                "initial_status": "radar",
            },
        )
        assert res_create_task.status_code == 200
        task_data = res_create_task.json()
        task_id = task_data["task_id"]
        assert task_data["title"] == "Implémentation Sonde WebSocket"
        assert task_data["status"] == "radar"

        # 4. Lecture des tâches filtrées
        res_tasks = api_client.get(f"/api/kanban/tasks?project_id={test_pid}")
        assert res_tasks.status_code == 200
        tasks_list = res_tasks.json()
        assert len(tasks_list) == 1
        assert tasks_list[0]["task_id"] == task_id

        # 5. Génération du Context-Pack SOTA pour Gemini Web
        res_cp = api_client.get(f"/api/kanban/tasks/{task_id}/context-pack")
        assert res_cp.status_code == 200
        cp_data = res_cp.json()
        assert cp_data["task_id"] == task_id
        assert "MISSION D'ARCHITECTURE" in cp_data["prompt"]
        assert task_id in cp_data["prompt"]

        # 6. Ingestion de Spec Markdown retournée par Gemini Web
        mock_spec_md = f"""---
task_id: "{task_id}"
project_id: "{test_pid}"
component_tag: "telemetry"
title: "Implémentation Sonde WebSocket"
status: "ready_for_agent"
---
# {task_id} — Implémentation Sonde WebSocket

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES
Architecture détaillée et structures de données.

## 2. PROMPT D'EXÉCUTION POUR L'AGENT CODEUR
Tu es l'agent codeur. Implémente la sonde WebSocket sans régression.
"""

        res_ingest = api_client.post(
            "/api/kanban/specs/ingest",
            json={
                "raw_markdown": mock_spec_md,
                "target_task_id": task_id,
            },
        )
        assert res_ingest.status_code == 200
        ingested_task = res_ingest.json()
        assert ingested_task["status"] == "ready_for_agent"
        assert ingested_task["spec_file_path"] is not None

        # 7. Extraction du Prompt Codeur & Basculement automatique en 'in_progress'
        res_coder = api_client.get(f"/api/kanban/tasks/{task_id}/coder-prompt?mark_in_progress=true")
        assert res_coder.status_code == 200
        coder_data = res_coder.json()
        assert "Tu es l'agent codeur" in coder_data["prompt"]
        assert coder_data["status"] == "in_progress"

        # 8. Mise à jour de statut en 'done'
        res_patch = api_client.patch(
            f"/api/kanban/tasks/{task_id}/status",
            json={"status": "done"},
        )
        assert res_patch.status_code == 200
        assert res_patch.json()["status"] == "done"

        # 9. Suppression de tâche
        res_del = api_client.delete(f"/api/kanban/tasks/{task_id}")
        assert res_del.status_code == 200
        assert res_del.json()["status"] == "deleted"

        # Vérification que la tâche a bien disparu
        res_tasks_after = api_client.get(f"/api/kanban/tasks?project_id={test_pid}")
        assert len(res_tasks_after.json()) == 0
    finally:
        db = DBManager()
        with db.get_connection() as conn:
            conn.execute("DELETE FROM projects WHERE project_id = ?;", (test_pid,))
        proj_specs_dir = settings.KANBAN_SPECS_DIR / test_pid
        if proj_specs_dir.exists():
            shutil.rmtree(proj_specs_dir, ignore_errors=True)


# ==============================================================================
# TEST 3 : ÉPISTÉMIQUE, GRAPHRAG, CONCEPTS & SERVEUR WEB STATIQUE
# ==============================================================================

def test_api_epistemic_and_static_gui_serving(api_client: TestClient) -> None:
    """Valide l'explorateur épistémique, GraphRAG, lecture de concept et distribution Web."""
    # 1. Sessions & Messages Gemini
    res_chats = api_client.get("/api/epistemic/chats?limit=5")
    assert res_chats.status_code == 200
    chats_list = res_chats.json()
    assert isinstance(chats_list, list)

    if chats_list:
        test_sid = chats_list[0]["session_id"]
        res_msgs = api_client.get(f"/api/epistemic/chats/{test_sid}/messages")
        assert res_msgs.status_code == 200
        assert isinstance(res_msgs.json(), list)

    # 2. Empreintes Numériques (Footprints)
    res_fp_summary = api_client.get("/api/epistemic/footprints/summary")
    assert res_fp_summary.status_code == 200
    fp_data = res_fp_summary.json()
    assert "kpis" in fp_data
    assert "top_channels_and_domains" in fp_data
    assert "burst_clusters" in fp_data

    res_fp_search = api_client.get("/api/epistemic/footprints/search?limit=10")
    assert res_fp_search.status_code == 200
    assert isinstance(res_fp_search.json(), list)

    # 3. GraphRAG Hybride
    res_rag = api_client.get("/api/graphrag/search?q=Python%20FastAPI&top_k=3&neighbor_k=2")
    assert res_rag.status_code == 200
    rag_data = res_rag.json()
    assert "query" in rag_data
    assert "primary_nodes" in rag_data
    assert "linked_neighbors" in rag_data
    assert "nodes" in rag_data
    assert "edges" in rag_data

    # 4. Lecture d'une Fiche Conceptuelle (/api/concepts/{slug})
    test_slug = "concept_test_v050_api"
    test_concept_path = settings.CONCEPTS_DIR / f"{test_slug}.md"
    try:
        note = ParsedConceptNote(
            frontmatter=ConceptFrontmatter(
                id=test_slug,
                title="Concept Test V050 API",
                semantic_topic="Dev_et_Architecture_Tech",
                source_turn_index=1,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
            ),
            title_h1="Concept Test V050 API",
            body="Corps d'analyse conceptuelle reliant [[Architecture]].",
            telemetry_lines=["> - Date : 2026-10-24"],
        )
        write_concept_file(note, test_concept_path)

        res_concept = api_client.get(f"/api/concepts/{test_slug}")
        assert res_concept.status_code == 200
        concept_data = res_concept.json()
        assert concept_data["slug"] == test_slug
        assert concept_data["title"] == "Concept Test V050 API"
        assert "frontmatter" in concept_data
        assert "body" in concept_data
        assert "raw_markdown" in concept_data
    finally:
        if test_concept_path.exists():
            test_concept_path.unlink()

    # Test concept introuvable -> 404
    res_not_found = api_client.get("/api/concepts/non_existent_concept_slug_xyz")
    assert res_not_found.status_code == 404

    # 5. Service Web Statique (Command Center GUI)
    res_root = api_client.get("/")
    assert res_root.status_code == 200
    assert "text/html" in res_root.headers.get("content-type", "").lower()
    assert "EXOCORTEX" in res_root.text

    res_css = api_client.get("/styles.css")
    assert res_css.status_code == 200
    assert "cyber-card" in res_css.text

    res_js = api_client.get("/app.js")
    assert res_js.status_code == 200
    assert "updateSystemStatus" in res_js.text
