"""
Suite de vérification v0.5.1 — Lot 1 de l'audit : arrêter les pertes de données.
Rejoue les reproductions de l'audit (A1, A2, A3, A4, A6, A7, A8, D3) sur coffre et base temporaires.
"""

from __future__ import annotations

import os
import sys
import time
import unittest.mock as mock
from datetime import datetime, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest
from fastapi.testclient import TestClient

from src.config import settings
from src.consolidators.graph_defragmenter import ConceptMergeSchema, GraphDefragmenter
from src.consolidators.kanban_engine import build_project_record, kanban_engine
from src.consolidators.night_consolidator import NightConsolidator
from src.consolidators.vault_doctor import scan_and_upgrade_existing_concepts
from src.database.db_manager import (
    ChatMessageRecord,
    ChatSessionRecord,
    DBManager,
    KanbanTaskRecord,
    ProjectRecord,
    RawActivityRecord,
)
from src.llm.ollama_client import HardwareProbe, llm_client
from src.utils.markdown_io import ConceptFrontmatter, ParsedConceptNote, parse_concept_file, write_concept_file


def _write_note(path: Path, origin, session_id=None, topic="Dev_et_Architecture_Tech", body="Corps complet et valide.", **extra) -> Path:
    fm = ConceptFrontmatter(
        id=path.stem,
        title=path.stem.replace("-", " ").title(),
        origin=origin,
        semantic_topic=topic,
        session_id=session_id,
        created_at="2026-10-01",
        updated_at="2026-10-01",
        total_time_invested_min=30,
        **extra,
    )
    write_concept_file(ParsedConceptNote(frontmatter=fm, title_h1=fm.title, body=body, telemetry_lines=[]), path)
    return path


# ==============================================================================
# A1 — Le démarrage n'efface plus les sessions courtes (vocal, live)
# ==============================================================================

def test_a1_restart_keeps_short_live_and_voice_sessions(exo_env):
    db = exo_env.db
    db.upsert_live_chat_turn("claude", "claude_live1", "Question courte ?", "Réponse.")
    db.insert_chat_sessions_batch([
        ChatSessionRecord(
            session_id="voice_20261001_120000_memo",
            timestamp_start=datetime(2026, 10, 1, 12),
            timestamp_end=datetime(2026, 10, 1, 12),
            turn_count=1,
            user_char_count=900,
            summary="Mémo",
            distillation_status="success",
        )
    ])

    DBManager(db_path=db.db_path)  # simple redémarrage d'un processus

    assert db.get_chat_session_by_id("claude_live1") is not None
    assert db.get_chat_session_by_id("voice_20261001_120000_memo") is not None

    db.upsert_live_chat_turn("claude", "claude_live1", "Deuxième question ?", "Deuxième réponse.")
    assert db.get_chat_session_by_id("claude_live1")["turn_count"] == 2


def test_a1_orphan_messages_rebuild_their_session(exo_env):
    db = exo_env.db
    db.insert_chat_messages_batch([
        ChatMessageRecord(session_id="live_orphan", turn_index=0, timestamp=datetime(2026, 10, 2, 9),
                          user_prompt="Premier tour", ai_response="R1", user_char_count=12),
        ChatMessageRecord(session_id="voice_20261002_100000_x", turn_index=0, timestamp=datetime(2026, 10, 2, 10),
                          user_prompt="Transcription vocale", ai_response="", user_char_count=20),
    ])

    # Migration v2 : la session vocale orpheline est reconstruite au prochain démarrage
    with db.get_connection() as conn:
        conn.execute("PRAGMA user_version = 1;")
    DBManager(db_path=db.db_path)
    voice = db.get_chat_session_by_id("voice_20261002_100000_x")
    assert voice is not None and voice["turn_count"] == 1

    # Session live : reconstruite à partir des messages existants au tour suivant
    db.upsert_live_chat_turn("claude", "live_orphan", "Second tour", "R2")
    live = db.get_chat_session_by_id("live_orphan")
    assert live["turn_count"] == 2
    assert live["user_char_count"] == 12 + len("Second tour")


def test_a1_footprint_dedup_runs_once(exo_env):
    with exo_env.db.get_connection() as conn:
        assert conn.execute("PRAGMA user_version;").fetchone()[0] >= 2


# ==============================================================================
# A2 — Mettre à jour un projet ne supprime plus ses tâches
# ==============================================================================

def test_a2_project_update_keeps_tasks(exo_env):
    db = exo_env.db
    db.create_project(ProjectRecord(project_id="homelab", name="Homelab", prefix="HLAB"))
    for i in range(3):
        db.upsert_kanban_task(KanbanTaskRecord(task_id=f"HLAB-00{i + 1}", project_id="homelab", title=f"T{i}"))

    db.upsert_project(ProjectRecord(project_id="homelab", name="Homelab renommé", prefix="HLAB"))

    assert db.get_project_by_id("homelab")["name"] == "Homelab renommé"
    assert len(db.get_kanban_tasks(project_id="homelab")) == 3
    with pytest.raises(ValueError):
        db.create_project(ProjectRecord(project_id="homelab", name="Doublon", prefix="DUP"))


# ==============================================================================
# A3 — La réingestion Takeout préserve statuts et résumés LLM
# ==============================================================================

def test_a3_reingestion_preserves_status_and_summary(exo_env):
    db = exo_env.db

    def rec(sid: str, turns: int) -> ChatSessionRecord:
        return ChatSessionRecord(session_id=sid, timestamp_start=datetime(2026, 9, 1, 10),
                                 timestamp_end=datetime(2026, 9, 1, 11), turn_count=turns,
                                 user_char_count=800, summary="premier prompt brut")

    db.insert_chat_sessions_batch([rec("sess_noise", 4), rec("sess_ok", 5)])
    db.update_session_distillation_metadata("sess_noise", [], [], distillation_status="misc_noise")
    db.update_session_distillation_metadata("sess_ok", ["IA_et_LLM_Local"], ["note-ok"], summary="Résumé du 26B")

    db.insert_chat_sessions_batch([rec("sess_noise", 4), rec("sess_ok", 7)])

    noise = db.get_chat_session_by_id("sess_noise")
    ok = db.get_chat_session_by_id("sess_ok")
    assert noise["distillation_status"] == "misc_noise"
    assert ok["distillation_status"] == "success"
    assert ok["summary"] == "Résumé du 26B"
    assert ok["turn_count"] == 7  # colonnes volumétriques mises à jour
    assert {"sess_noise", "sess_ok"} <= db.get_completed_session_ids_from_db()


# ==============================================================================
# A4 — Captures : aucune activité marquée traitée avant la vision, orphelins purgés
# ==============================================================================

def test_a4_pass1_analyzes_every_screenshot_and_purges_orphans(exo_env, monkeypatch):
    db = exo_env.db
    staging = settings.SCREEN_STAGING_DIR
    activities = []
    for i in range(60):
        img = staging / f"screen_{i:03d}.webp"
        img.write_bytes(b"webp")
        activities.append(RawActivityRecord(
            timestamp_start=datetime(2026, 10, 3, 9) + timedelta(minutes=i),
            timestamp_end=datetime(2026, 10, 3, 9) + timedelta(minutes=i, seconds=50),
            duration_sec=50, executable="code.exe", window_title=f"fichier_{i}.py",
            screenshot_path=str(img.resolve()),
        ))
    db.insert_raw_activities_batch(activities)

    orphan = staging / "screen_orphan.webp"
    orphan.write_bytes(b"old")
    old = time.time() - 48 * 3600
    os.utime(orphan, (old, old))
    recent_orphan = staging / "screen_current_window.webp"
    recent_orphan.write_bytes(b"new")

    monkeypatch.setattr(llm_client, "force_clear_vram", mock.MagicMock(return_value=16.0))
    monkeypatch.setattr(HardwareProbe, "get_vram_info", staticmethod(lambda: (16.0, 16.0)))
    monkeypatch.setattr(llm_client, "generate_vision", mock.MagicMock(return_value="Éditeur de code ouvert."))

    NightConsolidator(db_manager=db).run_pass_1_vision_and_tagging()

    assert llm_client.generate_vision.call_count == 60
    assert not any(p.name.startswith("screen_0") for p in staging.glob("*.webp"))
    assert not orphan.exists()
    assert recent_orphan.exists()  # capture récente : peut appartenir à la fenêtre en cours du démon
    assert db.get_unprocessed_raw_activities() == []


def test_a4_daemon_deletes_replaced_screenshot(exo_env):
    from PIL import Image

    import src.daemons.telemetry_daemon as td

    daemon = td.TelemetryDaemon(db_manager=exo_env.db)
    old_capture = settings.SCREEN_STAGING_DIR / "screen_old.webp"
    old_capture.write_bytes(b"old")
    daemon.current_state = td.WindowSessionState("code.exe", "main.py", 1)
    daemon.current_state.screenshot_path = str(old_capture.resolve())

    with mock.patch.object(td.win32gui, "GetWindowRect", return_value=(0, 0, 300, 300)), \
         mock.patch("mss.mss", side_effect=RuntimeError("pas d'écran")), \
         mock.patch.object(td.ImageGrab, "grab", return_value=Image.new("RGB", (300, 300), "white")):
        new_capture = daemon.capture_window_webp(1)

    assert new_capture is not None and new_capture.exists()
    assert not old_capture.exists()
    assert daemon.current_state.screenshot_path == str(new_capture.resolve())


def test_a4_unprocessed_query_skips_pending_screenshots(exo_env):
    db = exo_env.db
    db.insert_raw_activities_batch([
        RawActivityRecord(timestamp_start=datetime(2026, 10, 3, 9), timestamp_end=datetime(2026, 10, 3, 9, 5),
                          duration_sec=300, executable="code.exe", window_title="a", screenshot_path="x.webp"),
        RawActivityRecord(timestamp_start=datetime(2026, 10, 3, 10), timestamp_end=datetime(2026, 10, 3, 10, 5),
                          duration_sec=300, executable="code.exe", window_title="b"),
    ])
    rows = db.get_unprocessed_raw_activities(exclude_pending_screenshots=True)
    assert [r["window_title"] for r in rows] == ["b"]


# ==============================================================================
# A6 — Le Vault Doctor ne touche qu'aux fiches Takeout, et met en quarantaine
# ==============================================================================

def test_a6_vault_doctor_scope_and_quarantine(exo_env):
    cdir = exo_env.concepts_dir
    truncated = "### Contexte\nUne phrase coupée en plein milieu sans ponctuation finale et sans"
    voice = _write_note(cdir / "memo-vocal-court.md", ["voice_memo"], "voice_x", body="Court")
    night = _write_note(cdir / "non-classe-20261001.md", ["screen_telemetry"], topic="Non_Classe", body=truncated)
    manual = cdir / "note-manuelle.md"
    manual.write_text("# Ma note\n\nIdées en vrac sans ponctuation", encoding="utf-8")
    takeout_bad = _write_note(cdir / "takeout-tronquee.md", ["gemini_takeout"], "sess_trunc", body=truncated)
    takeout_ok = _write_note(cdir / "takeout-valide.md", ["gemini_takeout"], "sess_valid", body="### Conclusions\nTout est clair.")
    manual_before = manual.read_text(encoding="utf-8")

    completed = scan_and_upgrade_existing_concepts(exo_env.db)

    assert voice.exists() and night.exists() and manual.exists() and takeout_ok.exists()
    assert manual.read_text(encoding="utf-8") == manual_before  # jamais réécrite
    assert not takeout_bad.exists()
    assert (settings.CONCEPTS_QUARANTINE_DIR / "takeout-tronquee.md").exists()
    assert "sess_valid" in completed and "sess_trunc" not in completed


# ==============================================================================
# A7 / A8 — Fusion : slug confiné, aucune note tierce écrasée, sessions conservées
# ==============================================================================

def test_a7_a8_merge_is_confined_and_keeps_session_ids(exo_env):
    cdir = exo_env.concepts_dir
    a = _write_note(cdir / "note-a.md", ["gemini_takeout"], "sess_a", body="### A\nDétail A.")
    b = _write_note(cdir / "note-b.md", ["gemini_takeout"], "sess_b", body="### B\nDétail B.")
    third = _write_note(cdir / "budget-2027.md", ["manual"], body="Budget important.")
    journal = exo_env.episodic_dir / "2026-10-01.md"
    journal.write_text("journal original", encoding="utf-8")

    defrag = GraphDefragmenter(db_manager=exo_env.db, vector_store=mock.MagicMock())

    def decision(slug: str) -> ConceptMergeSchema:
        return ConceptMergeSchema(should_merge=True, canonical_title="Fusion", canonical_slug=slug,
                                  merged_summary_1_line="r", merged_markdown_body="Corps fusionné.")

    target = defrag.merge_concepts_pair(a, b, decision("budget-2027"))
    assert target.parent.resolve() == cdir.resolve()
    assert target.name == "budget-2027-2.md"
    assert parse_concept_file(third).body == "Budget important."

    c = _write_note(cdir / "note-c.md", ["gemini_takeout"], "sess_c")
    d = _write_note(cdir / "note-d.md", ["gemini_takeout"], "sess_d")
    target2 = defrag.merge_concepts_pair(c, d, decision("../01_Episodique/2026-10-01"))
    assert target2.parent.resolve() == cdir.resolve()
    assert journal.read_text(encoding="utf-8") == "journal original"

    merged = parse_concept_file(target)
    assert merged.frontmatter.model_extra["session_ids"] == ["sess_a", "sess_b"]

    completed = scan_and_upgrade_existing_concepts(exo_env.db)
    assert {"sess_a", "sess_b", "sess_c", "sess_d"} <= completed


def test_a8_merge_prompt_receives_full_bodies(exo_env, monkeypatch):
    cdir = exo_env.concepts_dir
    long_body = "Intro.\n" + ("x" * 2000) + "\nDÉTAIL_CRITIQUE_APRES_1500."
    a = _write_note(cdir / "long-a.md", ["gemini_takeout"], "sa", body=long_body)
    b = _write_note(cdir / "long-b.md", ["gemini_takeout"], "sb", body="Autre.")
    vs = mock.MagicMock()
    vs._table.to_pandas.return_value = __import__("pandas").DataFrame([
        {"slug": "long-a", "title": "Pipeline RAG", "semantic_topic": "IA", "tags": "rag", "file_path": str(a), "vector": [1.0, 0.0]},
        {"slug": "long-b", "title": "Pipeline RAG bis", "semantic_topic": "IA", "tags": "rag", "file_path": str(b), "vector": [1.0, 0.01]},
    ])
    captured = {}

    def fake_structured(prompt, **kwargs):
        captured["prompt"] = prompt
        return ConceptMergeSchema(should_merge=False, canonical_title="x", canonical_slug="x",
                                  merged_summary_1_line="x", merged_markdown_body="x")

    monkeypatch.setattr(llm_client, "is_alive", mock.MagicMock(return_value=True))
    monkeypatch.setattr(llm_client, "generate_structured", fake_structured)
    GraphDefragmenter(db_manager=exo_env.db, vector_store=vs).run_defragmentation_cycle()
    assert "DÉTAIL_CRITIQUE_APRES_1500" in captured["prompt"]


# ==============================================================================
# D3 — Chemins contrôlés par la requête
# ==============================================================================

def test_d3_api_rejects_path_traversal_and_invalid_projects(exo_env, tmp_path):
    from src.api.server import app

    from src.utils.local_auth import TOKEN_HEADER, get_local_token

    client = TestClient(app, base_url="http://127.0.0.1", headers={TOKEN_HEADER: get_local_token("api")})
    (exo_env.episodic_dir / "2026-10-01.md").write_text("secret", encoding="utf-8")
    assert client.get("/api/concepts/..%5C01_Episodique%5C2026-10-01").status_code in (400, 404)
    assert client.get("/api/concepts/..").status_code in (400, 404)

    bad_slug = {"project_id": "../../evil", "name": "Evil", "prefix": "EVL"}
    res = client.post("/api/kanban/projects", json=bad_slug)
    assert res.status_code == 200 and res.json()["project_id"] == "evil"

    not_a_repo = tmp_path / "pas_un_depot"
    not_a_repo.mkdir()
    res = client.post("/api/kanban/projects", json={"project_id": "p2", "name": "P2", "prefix": "P2", "repo_path": str(not_a_repo)})
    assert res.status_code == 400

    assert client.post("/api/kanban/projects", json={"project_id": "evil", "name": "x", "prefix": "EVL"}).status_code == 409
    assert client.post("/api/kanban/tasks", json={"project_id": "inconnu", "title": "t"}).status_code == 404

    res = client.put("/api/kanban/projects/evil", json={"project_id": "evil", "name": "Renommé", "prefix": "EVL"})
    assert res.status_code == 200 and res.json()["name"] == "Renommé"


def test_d3_spec_written_inside_kanban_dir(exo_env):
    db = exo_env.db
    # Projet hérité (créé avant la validation) dont le slug contient une remontée de chemin
    with db.get_connection() as conn:
        conn.execute(
            "INSERT INTO projects VALUES ('../../hors_coffre', 'Legacy', 'LEG', NULL, '', '2026-01-01 00:00:00');"
        )
    db.upsert_kanban_task(KanbanTaskRecord(task_id="LEG-001", project_id="../../hors_coffre", title="Spec"))
    task = kanban_engine.attach_spec_to_task("---\ntask_id: LEG-001\n---\n# Spec", target_task_id="LEG-001")
    spec_path = Path(task["spec_file_path"]).resolve()
    spec_path.relative_to(settings.KANBAN_SPECS_DIR.resolve())


def test_d3_repo_path_must_be_git_repo(tmp_path):
    with pytest.raises(ValueError):
        build_project_record("p", "P", "P", repo_path=str(tmp_path))
    (tmp_path / ".git").mkdir()
    assert build_project_record("p", "P", "P", repo_path=str(tmp_path)).repo_path == str(tmp_path.resolve())
