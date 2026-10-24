"""
Suite de vérification v0.5.5 — Lot 5 de l'audit : exactitude des métriques et du coffre.
A12 (fuseaux), A5 (inactivité et tunnels), A13 (enrichissement idempotent), A9 (valeurs estimées),
B17 (taxonomie par mots entiers), A14 (capture live par rang), B18 (wikilinks résolubles).
"""

from __future__ import annotations

import json
import sys
import unittest.mock as mock
from datetime import date, datetime, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest

from src.config import normalize_to_macro_topic, settings
from src.database.db_manager import DBManager, HistoricalFootprintRecord
from src.ingestors.takeout_parsers import ParsedTurn, parse_date_pair, sessionize_gemini_turns
from src.utils.cognitive_metrics import compute_focus_tunnels
from src.utils.markdown_io import (
    ConceptFrontmatter,
    ParsedConceptNote,
    parse_concept_file,
    parse_concept_string,
    serialize_concept_note,
    write_concept_file,
)


# ==============================================================================
# A12 — Fuseaux horaires
# ==============================================================================

def test_a12_same_instant_from_html_and_json(monkeypatch):
    monkeypatch.setattr(settings, "LOCAL_TIMEZONE", "Europe/Paris")
    html_local, html_literal = parse_date_pair("1 oct. 2026, 14:30:00 CEST")
    json_local, json_literal = parse_date_pair("2026-10-01T12:30:00.000Z")
    assert html_local == json_local == datetime(2026, 10, 1, 14, 30)
    assert json_literal == datetime(2026, 10, 1, 12, 30)  # heure littérale conservée pour les identifiants
    assert parse_date_pair("1 janv. 2026, 09:00:00 UTC")[0] == datetime(2026, 1, 1, 10, 0)  # hiver : UTC+1


def test_a12_synthetic_session_ids_are_stable_across_conversion():
    turns = [
        ParsedTurn(timestamp=datetime(2026, 10, 1, 14, 30) + timedelta(minutes=i), user_prompt="x" * 120,
                   user_char_count=120, source_timestamp=datetime(2026, 10, 1, 12, 30) + timedelta(minutes=i))
        for i in range(3)
    ]
    sessions, _ = sessionize_gemini_turns(turns)
    assert sessions[0].session_id == "synth_20261001_123000"  # identifiant d'avant v0.5.5
    assert sessions[0].timestamp_start == datetime(2026, 10, 1, 14, 30)  # mais heure locale stockée


def test_a12_reingestion_migrates_utc_footprints_without_duplicates(exo_env):
    db = exo_env.db
    # Ligne stockée par une version antérieure : heure UTC brute, déjà en cluster et classée
    db.insert_historical_footprints_batch([HistoricalFootprintRecord(
        source="google_search", timestamp=datetime(2026, 10, 1, 12, 30), title_or_query="lancedb ivf",
        cluster_id="cluster_x", semantic_topic="IA_et_LLM_Local")])
    db.insert_historical_footprints_batch([HistoricalFootprintRecord(
        source="google_search", timestamp=datetime(2026, 10, 1, 14, 30), title_or_query="lancedb ivf",
        legacy_timestamp=datetime(2026, 10, 1, 12, 30))])
    with db.get_connection() as conn:
        rows = conn.execute("SELECT timestamp, cluster_id, semantic_topic FROM historical_footprints;").fetchall()
    assert [tuple(r) for r in rows] == [("2026-10-01 14:30:00", "cluster_x", "IA_et_LLM_Local")]


# ==============================================================================
# A5 — Inactivité et tunnels
# ==============================================================================

def _act(start: datetime, minutes: float, topic: str, exe: str = "code.exe"):
    return {"timestamp_start": start, "timestamp_end": start + timedelta(minutes=minutes),
            "duration_sec": int(minutes * 60), "semantic_topic": topic, "executable": exe, "window_title": exe}


def test_a5_tunnels_break_on_long_gaps():
    t0 = datetime(2026, 10, 1, 9)
    tunnels = compute_focus_tunnels([_act(t0, 60, "Dev"), _act(t0 + timedelta(hours=11), 60, "Dev")])
    assert [t.duration_sec for t in tunnels] == [3600, 3600]


def test_a5_cumulated_micro_interruptions_are_tolerated():
    t0 = datetime(2026, 10, 1, 9)
    acts = [_act(t0, 30, "Dev"), _act(t0 + timedelta(minutes=30), 1, "Com", "slack.exe"),
            _act(t0 + timedelta(minutes=31), 1, "Com", "outlook.exe"), _act(t0 + timedelta(minutes=32), 30, "Dev")]
    tunnels = compute_focus_tunnels(acts)
    assert len(tunnels) == 1 and tunnels[0].duration_sec == 62 * 60

    acts_long = [_act(t0, 30, "Dev"), _act(t0 + timedelta(minutes=30), 2.5, "Com", "slack.exe"),
                 _act(t0 + timedelta(minutes=32.5), 30, "Dev")]
    assert [t.topic for t in compute_focus_tunnels(acts_long)] == ["Dev", "Com", "Dev"]


def test_a5_daemon_splits_on_idle_and_ignores_locked_screen(exo_env):
    import src.daemons.telemetry_daemon as td

    daemon = td.TelemetryDaemon(db_manager=exo_env.db)
    now = datetime.now()
    state = td.WindowSessionState("Code.exe", "main.py", 42)
    state.timestamp_start = now - timedelta(hours=8)
    state.timestamp_last_seen = now
    daemon.current_state = state

    # 8 h de fenêtre, mais dernière saisie 10 min après l'ouverture
    with mock.patch.object(daemon, "get_foreground_window_info", return_value=(42, "Code.exe", "main.py")), \
         mock.patch.object(td, "get_user_idle_seconds", return_value=8 * 3600 - 600):
        daemon.step()
    with exo_env.db.get_connection() as conn:
        rows = conn.execute("SELECT duration_sec FROM raw_activity;").fetchall()
    assert len(rows) == 1 and 590 <= rows[0][0] <= 610
    assert daemon.current_state is None

    # Écran verrouillé : aucune activité « Idle »
    with mock.patch.object(daemon, "get_foreground_window_info", return_value=(0, "Idle", "")):
        daemon.step()
    with exo_env.db.get_connection() as conn:
        assert conn.execute("SELECT COUNT(*) FROM raw_activity WHERE executable = 'Idle';").fetchone()[0] == 0


# ==============================================================================
# A13 — Enrichissement réellement idempotent
# ==============================================================================

def _note(total: int = 55, telemetry=None, body: str = "### Contexte\nTravaux.") -> ParsedConceptNote:
    fm = ConceptFrontmatter(id="n", title="Pipeline RAG", created_at="2026-09-01", updated_at="2026-09-01",
                            total_time_invested_min=total)
    return ParsedConceptNote(frontmatter=fm, title_h1="Pipeline RAG", body=body, telemetry_lines=telemetry or [])


def test_a13_duration_change_readjusts_total_and_no_duplicate_sections():
    note = _note()
    llm = "### Session du 2026-10-01\n\nAvancée.\n\n### Arbitrages\n- Choix IVF."
    note.append_or_replace_daily_session("2026-10-01", 145, "2h25", llm)
    note.append_or_replace_daily_session("2026-10-01", 190, "3h10", llm)
    assert note.frontmatter.total_time_invested_min == 55 + 190
    assert note.body.count("Arbitrages") == 1 and note.body.count("### Session du 2026-10-01") == 1

    roundtrip = parse_concept_string(serialize_concept_note(note))
    assert roundtrip.frontmatter.total_time_invested_min == 245
    assert roundtrip.frontmatter.model_extra["screen_time_by_date"] == {"2026-10-01": 190}


def test_a13_legacy_note_without_per_date_map():
    note = _note(total=200, telemetry=[
        "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)",
        "> - **Sources épisodiques :**",
        ">   - Activité écran du `2026-10-01` (2h25)",
    ], body="### Contexte\nTravaux.\n\n### Session du 2026-10-01\n\nAncien texte.\n\n### Arbitrages\n- Ancien.")
    note.append_or_replace_daily_session("2026-10-01", 190, "3h10", "Nouveau texte.\n\n### Arbitrages\n- Nouveau.")
    assert note.frontmatter.total_time_invested_min == 200 - 145 + 190
    assert "Ancien" not in note.body and note.body.count("Arbitrages") == 1


def test_a13_llm_callout_does_not_swallow_body():
    llm = "Intro.\n\n> [!abstract] Résumé LLM\n> pas à sa place\n\n### Choix Techniques\nIVF-PQ retenu."
    note = _note()
    note.append_or_replace_daily_session("2026-10-02", 30, "30 min", llm)
    parsed = parse_concept_string(serialize_concept_note(note))
    assert "Choix Techniques" in parsed.body and "IVF-PQ retenu" in parsed.body
    assert "Résumé LLM" not in parsed.body
    assert not any("Choix Techniques" in line for line in parsed.telemetry_lines)


# ==============================================================================
# A9 — Valeurs estimées signalées
# ==============================================================================

def test_a9_estimated_values_are_flagged(exo_env):
    from fastapi.testclient import TestClient

    from src.api.server import app
    from src.ingestors.takeout_ingestor import generate_cold_start_episodic_journals
    from src.ingestors.takeout_parsers import ReconstructedSession

    turns = [ParsedTurn(timestamp=datetime(2026, 9, 5, 10) + timedelta(minutes=5 * i), user_prompt="q" * 100,
                        user_char_count=100) for i in range(4)]
    sess = ReconstructedSession(session_id="s1", timestamp_start=turns[0].timestamp, timestamp_end=turns[-1].timestamp,
                                turns=turns, turn_count=4, user_char_count=400, summary="q")
    generate_cold_start_episodic_journals([sess], exo_env.db)

    client = TestClient(app, base_url="http://127.0.0.1")
    kpi = client.get("/api/telemetry/timeline?date=2026-09-05").json()["daily_metric"]
    assert kpi["is_consolidated"] is True and kpi["is_estimated"] is True
    macro = client.get("/api/telemetry/kpis").json()
    assert macro["chat_hours_is_estimated"] is True
    assert ConceptFrontmatter(id="x", title="x", created_at="", updated_at="").semantic_topic == "A_Trier"
    assert all(r["topic"] != "Dev_et_Architecture_Tech" for r in exo_env.db.fetch_archaeology_sessions())


def test_a9_migration_marks_legacy_cold_start_rows(tmp_path):
    db_path = tmp_path / "legacy.db"
    db = DBManager(db_path=db_path)
    with db.get_connection() as conn:
        conn.execute("INSERT INTO daily_metrics VALUES ('2025-01-01', 600, 420, 180, 600, 'IA', 1.0, 0.4, '{}', 0);")
        conn.execute("PRAGMA user_version = 2;")
    DBManager(db_path=db_path)
    with db.get_connection() as conn:
        assert conn.execute("SELECT is_estimated FROM daily_metrics;").fetchone()[0] == 1


# ==============================================================================
# B17 — Taxonomie par mots entiers
# ==============================================================================

@pytest.mark.parametrize("tag,expected", [
    ("Psychotherapie", "Introspection_et_Neuroatypie"),
    ("Therapie_Cognitive", "Sante_et_Pharmacologie"),
    ("Storage_Strategy", "A_Trier"),
    ("Fragmentation_Attention", "A_Trier"),
    ("Research_Notes", "A_Trier"),
    ("Enjeux_Climatiques", "A_Trier"),
    ("HomeLab", "HomeLab_et_Hardware"),
    ("Docker_Compose", "HomeLab_et_Hardware"),
    ("Prompt_Engineering_Avance", "IA_et_LLM_Local"),
    ("api", "Dev_et_Architecture_Tech"),
    ("Volume_Eating", "Nutrition_et_Cuisine"),
    ("Context_Switches", "A_Trier"),
    ("K-Pop", "Musique_MAO_et_Culture_Pop"),
    ("ADOS-2", "Introspection_et_Neuroatypie"),
    ("Santé_Mentale", "Sante_et_Pharmacologie"),
    ("GameDesign", "Gaming_et_GameDesign"),
])
def test_b17_whole_word_normalization(tag, expected):
    assert normalize_to_macro_topic(tag) == expected


# ==============================================================================
# A14 — Capture live dédupliquée par rang de tour
# ==============================================================================

def test_a14_identical_prompts_at_different_ranks_are_distinct(exo_env):
    db = exo_env.db
    db.upsert_live_chat_turn("claude", "c1", "Explique le WAL", "Réponse 1", turn_index=0)
    db.upsert_live_chat_turn("claude", "c1", "continue", "Suite A", turn_index=1)
    db.upsert_live_chat_turn("claude", "c1", "continue", "Suite B", turn_index=2)
    # Réémission du tour 1 avec une réponse complétée : mise à jour, pas de doublon
    res = db.upsert_live_chat_turn("claude", "c1", "continue", "Suite A complétée", turn_index=1)
    assert res["status"] == "updated"

    msgs = db.fetch_messages_for_session("c1")
    assert [m["ai_response"] for m in msgs] == ["Réponse 1", "Suite A complétée", "Suite B"]
    assert db.get_chat_session_by_id("c1")["turn_count"] == 3


def test_a14_legacy_extension_without_rank_still_deduplicates(exo_env):
    db = exo_env.db
    db.upsert_live_chat_turn("gemini", "g1", "Question", "R")
    assert db.upsert_live_chat_turn("gemini", "g1", "Question", "R")["status"] == "duplicate"
    assert db.get_chat_session_by_id("g1")["turn_count"] == 1


# ==============================================================================
# B18 — Wikilinks résolubles dans Obsidian
# ==============================================================================

def test_b18_title_alias_written_for_title_links(exo_env):
    path = exo_env.concepts_dir / "pipeline-rag-lancedb.md"
    fm = ConceptFrontmatter(id="p", title="Pipeline RAG LanceDB", created_at="2026-10-01", updated_at="2026-10-01")
    write_concept_file(ParsedConceptNote(frontmatter=fm, title_h1=fm.title, body="Corps."), path)
    assert parse_concept_file(path).frontmatter.model_extra["aliases"] == ["Pipeline RAG LanceDB"]
    # Réécriture : pas de doublon d'alias
    write_concept_file(parse_concept_file(path), path)
    assert parse_concept_file(path).frontmatter.model_extra["aliases"] == ["Pipeline RAG LanceDB"]


def test_b18_category_links_become_tags(exo_env):
    from src.consolidators.night_consolidator import NightConsolidator
    from src.database.db_manager import RawActivityRecord

    exo_env.db.insert_raw_activities_batch([RawActivityRecord(
        timestamp_start=datetime(2026, 10, 3, 9), timestamp_end=datetime(2026, 10, 3, 10), duration_sec=3600,
        executable="code.exe", window_title="vector_store.py", semantic_topic="IA_et_LLM_Local",
        cognitive_mode="production", processed=True)])
    nc = NightConsolidator(db_manager=exo_env.db)
    nc.run_pass_2_synthesis(date(2026, 10, 3), nc.calculate_daily_metrics_for_date(date(2026, 10, 3)), run_bootloader=False)
    note = parse_concept_file(next(exo_env.concepts_dir.glob("*.md")))
    links = "\n".join(note.telemetry_lines)
    assert "[[IA_et_LLM_Local]]" not in links and "[[Dev_et_Architecture_Tech]]" not in links
    assert "#" in links
