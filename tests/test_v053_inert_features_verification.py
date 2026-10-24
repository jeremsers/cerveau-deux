"""
Suite de vérification v0.5.3 — Lot 3 de l'audit : rétablir les fonctions annoncées mais inertes.
B11 (topic des rafales), B12 (distillation vocale), B13/B14 (report et voie cloud de la distillation
Takeout), B15 (profil cognitif), A11 (classification exhaustive), B16 (mode CPU nocturne).
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

import src.ingestors.takeout_ingestor as ti
from src.config import settings
from src.consolidators.night_consolidator import NightConsolidator
from src.database.db_manager import ChatSessionRecord, HistoricalFootprintRecord, RawActivityRecord
from src.ingestors.takeout_parsers import ParsedTurn, ReconstructedSession
from src.ingestors.voice_ingestor import VoiceIngestor, VoiceMemoSchema
from src.llm.ollama_client import HardwareProbe, llm_client
from src.utils.markdown_io import parse_concept_file


def _session(sid: str, start: datetime, turns: int = 4) -> ReconstructedSession:
    parsed = [
        ParsedTurn(session_id=sid, timestamp=start + timedelta(minutes=5 * i),
                   user_prompt=f"Question technique détaillée numéro {i} sur l'architecture du pipeline " * 3,
                   ai_response="Réponse argumentée.", user_char_count=200)
        for i in range(turns)
    ]
    return ReconstructedSession(session_id=sid, timestamp_start=start, timestamp_end=parsed[-1].timestamp,
                                turns=parsed, turn_count=turns, user_char_count=200 * turns, summary="premier prompt")


def _distilled(title: str = "Pipeline RAG local") -> ti.DistilledConceptSchema:
    return ti.DistilledConceptSchema(
        is_worth_indexing=True, concept_title=title, slug=title.lower().replace(" ", "-"),
        semantic_topic="IA_et_LLM_Local", tags=["rag"], summary_1_line="Résumé.",
        synthesized_markdown_body="### Contexte\nCorps complet.", related_concepts=[],
    )


# ==============================================================================
# B12 — Distillation vocale
# ==============================================================================

def test_b12_voice_memo_is_distilled_with_structured_output(exo_env, monkeypatch):
    inbox = settings.VOICE_INBOX_DIR
    (inbox / "20261020_183000_memo.m4a").write_bytes(b"audio")
    transcription = "Bon alors pour les vacances d'été il faut que je fixe un budget de deux mille euros maximum et réserver avant mars."

    structured = mock.MagicMock(return_value=VoiceMemoSchema(
        concept_title="Budget Vacances d'Été 2027", semantic_topic="Admin_Finance_et_Droit",
        tags=["budget", "vacances"], summary_1_line="Plafond de 2 000 € et réservation avant mars.",
        synthesized_markdown_body="### Décisions\n- Budget plafonné à 2 000 €.",
    ))
    monkeypatch.setattr(llm_client, "is_alive", mock.MagicMock(return_value=True))
    monkeypatch.setattr(llm_client, "generate_structured", structured)
    assert not hasattr(llm_client, "generate")  # la méthode appelée avant v0.5.3 n'a jamais existé

    res = VoiceIngestor(db_manager=exo_env.db, transcriber=lambda p: transcription).run()
    assert res["processed_count"] == 1 and not res["errors"]

    note = parse_concept_file(res["created_notes"][0])
    assert note.frontmatter.title == "Budget Vacances d'Été 2027"
    assert note.frontmatter.semantic_topic == "Admin_Finance_et_Droit"
    assert "Budget plafonné" in note.body and transcription in note.body

    sess = exo_env.db.get_chat_session_by_id(next(iter(
        r["session_id"] for r in exo_env.db.get_chat_sessions() if r["session_id"].startswith("voice_")
    )))
    assert json.loads(sess["generated_notes_json"]) == [note.file_path.stem]


def test_b12_voice_memo_offline_is_quarantined_not_dev(exo_env):
    (settings.VOICE_INBOX_DIR / "20261021_090000_idee.m4a").write_bytes(b"audio")
    res = VoiceIngestor(db_manager=exo_env.db, transcriber=lambda p: "Idée en vrac sur le jardin et les tomates cerises.").run()
    note = parse_concept_file(res["created_notes"][0])
    assert note.frontmatter.semantic_topic == "A_Trier"


# ==============================================================================
# B13 / B14 — Distillation Takeout : report sans erreur, voie cloud indépendante d'Ollama
# ==============================================================================

def test_b13_low_vram_defers_distillation_without_crash(exo_env, monkeypatch):
    sessions = [_session("sess_a", datetime(2026, 10, 5, 10)), _session("sess_b", datetime(2026, 10, 5, 15))]
    exo_env.db.insert_chat_sessions_batch([
        ChatSessionRecord(session_id=s.session_id, timestamp_start=s.timestamp_start, timestamp_end=s.timestamp_end,
                          turn_count=s.turn_count, user_char_count=s.user_char_count, summary=s.summary)
        for s in sessions
    ])
    monkeypatch.setattr(llm_client, "is_alive", mock.MagicMock(return_value=True))
    monkeypatch.setattr(llm_client, "ensure_local_gguf_models", mock.MagicMock(return_value={}))
    monkeypatch.setattr(llm_client, "force_clear_vram", mock.MagicMock(return_value=5.0))
    structured = mock.MagicMock()
    monkeypatch.setattr(llm_client, "generate_structured", structured)

    report = ti.initialize_meta_and_concepts(sessions, [], exo_env.db)

    assert report["deferred_sessions"] == 2
    structured.assert_not_called()
    assert exo_env.db.get_chat_session_by_id("sess_a")["distillation_status"] == "pending"
    assert (settings.EPISODIC_DIR / "2026-10-05.md").exists()  # la suite du pipeline a tourné


def test_b14_cloud_mode_works_with_ollama_off(exo_env, monkeypatch):
    sess = _session("sess_cloud", datetime(2026, 10, 6, 9))
    exo_env.db.insert_chat_sessions_batch([ChatSessionRecord(
        session_id=sess.session_id, timestamp_start=sess.timestamp_start, timestamp_end=sess.timestamp_end,
        turn_count=sess.turn_count, user_char_count=sess.user_char_count, summary=sess.summary)])
    monkeypatch.setattr(settings, "TAKEOUT_MODE", "cloud_api")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "cle-de-test-123")
    cloud = mock.MagicMock(return_value=_distilled("Pipeline Cloud"))
    monkeypatch.setattr(llm_client, "generate_cloud_sota", cloud)

    report = ti.initialize_meta_and_concepts([sess], [], exo_env.db)

    assert cloud.call_count == 1 and report["distilled_success"] == 1
    assert (settings.CONCEPTS_DIR / "pipeline-cloud.md").exists()
    assert exo_env.db.get_chat_session_by_id("sess_cloud")["distillation_status"] == "success"


# ==============================================================================
# B11 — Topic des rafales Search / YouTube
# ==============================================================================

def _insert_burst(db, start: datetime, queries):
    db.insert_historical_footprints_batch([
        HistoricalFootprintRecord(source="google_search", timestamp=start + timedelta(minutes=i), title_or_query=q)
        for i, q in enumerate(queries)
    ])


def test_b11_bursts_receive_a_topic(exo_env, monkeypatch):
    db = exo_env.db
    _insert_burst(db, datetime(2026, 9, 1, 20), ["docker compose plex", "riven debrid", "plex docker gpu",
                                                  "homelab nas", "docker volumes plex"])
    _insert_burst(db, datetime(2026, 9, 3, 20), ["recette volume eating", "ninja creami recette", "riz cuiseur",
                                                  "batch cooking poulet", "recette protéinée"])
    assert ti.perform_burst_clustering(db) == 2

    # LLM : seule la première rafale est résolue ; la seconde passe par le repli heuristique
    def fake_structured(prompt, response_model, **kwargs):
        first = db.get_untopiced_burst_clusters()[0]["cluster_id"]
        return response_model(clusters=[{"cluster_id": first, "semantic_topic": "HomeLab_et_Hardware"}])

    monkeypatch.setattr(llm_client, "is_alive", mock.MagicMock(return_value=True))
    monkeypatch.setattr(llm_client, "generate_structured", fake_structured)
    assert ti.classify_burst_clusters(db) == 2

    with db.get_connection() as conn:
        topics = dict(conn.execute(
            "SELECT cluster_id, MAX(semantic_topic) FROM historical_footprints GROUP BY cluster_id").fetchall())
    assert sorted(topics.values()) == ["HomeLab_et_Hardware", "Nutrition_et_Cuisine"]
    assert db.get_topic_telemetry_stats("HomeLab_et_Hardware")["footprints_count"] == 5

    # Re-clustering : les topics attribués ne sont pas effacés
    ti.perform_burst_clustering(db)
    assert db.get_untopiced_burst_clusters() == []


# ==============================================================================
# B15 — Profil cognitif
# ==============================================================================

PROFILE_REPLY = "# SECTION 1 : Profil_Cognitif.md\n# Profil Cognitif\n\n" + ("Raisonnement systémique et itératif. " * 20) + \
    "\n\n===SPLIT_LIVRABLE===\n\n# SECTION 2 : Taxonomie_Tags.md\n- `Rust_BasNiveau`"


def test_b15_import_profile_keeps_closed_taxonomy(exo_env):
    ti.ensure_strict_taxonomy_file()
    taxonomy_before = settings.TAXONOMIE_TAGS_PATH.read_text(encoding="utf-8")
    out = ti.import_cognitive_profile(PROFILE_REPLY)
    content = out.read_text(encoding="utf-8")
    assert content.startswith("# Profil Cognitif") and "Raisonnement systémique" in content
    assert "Rust_BasNiveau" not in content and "SPLIT_LIVRABLE" not in content
    assert settings.TAXONOMIE_TAGS_PATH.read_text(encoding="utf-8") == taxonomy_before
    with pytest.raises(ValueError):
        ti.import_cognitive_profile("trop court")


def test_b15_cloud_profile_replaces_template_only(exo_env, monkeypatch, tmp_path):
    prompts_file = tmp_path / "00_USER_PROMPTS_ONLY.md"
    prompts_file.write_text("prompts", encoding="utf-8")
    monkeypatch.setattr(settings, "TAKEOUT_MODE", "cloud_api")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "cle-de-test-123")
    cloud = mock.MagicMock(return_value=PROFILE_REPLY)
    monkeypatch.setattr(llm_client, "generate_cloud_sota", cloud)

    assert ti.generate_cognitive_profile_cloud(prompts_file) is not None
    assert "{allowed_taxonomy}" not in cloud.call_args.kwargs["system"]
    # Un profil réel n'est jamais écrasé
    assert ti.generate_cognitive_profile_cloud(prompts_file) is None
    assert cloud.call_count == 1


# ==============================================================================
# A11 — Classification exhaustive et reconsolidation des dates modifiées
# ==============================================================================

def _activities(day: date, n: int, title: str = "main.py - Visual Studio Code"):
    base = datetime.combine(day, datetime.min.time()).replace(hour=8)
    return [RawActivityRecord(timestamp_start=base + timedelta(seconds=30 * i),
                              timestamp_end=base + timedelta(seconds=30 * i + 25), duration_sec=25,
                              executable="code.exe", window_title=f"{title} {i % 7}") for i in range(n)]


def test_a11_pass1_classifies_until_exhaustion(exo_env, monkeypatch):
    db = exo_env.db
    db.insert_raw_activities_batch(_activities(date(2026, 10, 1), 1200))
    monkeypatch.setattr(llm_client, "force_clear_vram", mock.MagicMock(return_value=16.0))
    monkeypatch.setattr(HardwareProbe, "get_vram_info", staticmethod(lambda: (16.0, 16.0)))

    nc = NightConsolidator(db_manager=db)
    assert nc.run_pass_1_vision_and_tagging() == 1200
    assert db.get_unprocessed_raw_activities() == []
    assert nc.last_classified_dates == {date(2026, 10, 1)}


def test_a11_dates_with_new_activities_are_reconsolidated(exo_env, monkeypatch):
    db = exo_env.db
    monkeypatch.setattr(llm_client, "force_clear_vram", mock.MagicMock(return_value=16.0))
    monkeypatch.setattr(HardwareProbe, "get_vram_info", staticmethod(lambda: (16.0, 16.0)))
    nc = NightConsolidator(db_manager=db)
    with mock.patch.object(nc, "run_pass_3_vector_indexing", return_value=0):
        db.insert_raw_activities_batch(_activities(date(2026, 10, 1), 10) + _activities(date(2026, 10, 2), 10))
        nc.consolidate()
        assert (settings.EPISODIC_DIR / "2026-10-01.md").exists()

        # Nouvelles activités arrivées tardivement pour le 01/10 (journal existant, pas la date max)
        db.insert_raw_activities_batch(_activities(date(2026, 10, 1), 200))
        res = nc.consolidate()
    assert "2026-10-01" in res["processed_dates"]
    with db.get_connection() as conn:
        total = conn.execute("SELECT total_screen_sec FROM daily_metrics WHERE date = '2026-10-01';").fetchone()[0]
    assert total == 210 * 25


def test_a11_no_concept_note_for_unclassified_share(exo_env, monkeypatch):
    db = exo_env.db
    db.insert_raw_activities_batch([RawActivityRecord(
        timestamp_start=datetime(2026, 10, 3, 9), timestamp_end=datetime(2026, 10, 3, 11), duration_sec=7200,
        executable="mystery.exe", window_title="Fenêtre inconnue", semantic_topic="A_Trier",
        cognitive_mode="exploration", processed=True)])
    nc = NightConsolidator(db_manager=db)
    nc.run_pass_2_synthesis(date(2026, 10, 3), nc.calculate_daily_metrics_for_date(date(2026, 10, 3)), run_bootloader=False)
    assert list(settings.CONCEPTS_DIR.glob("*.md")) == []


# ==============================================================================
# B16 — Mode CPU quand la VRAM manque
# ==============================================================================

def test_b16_low_vram_night_runs_in_cpu_mode(exo_env, monkeypatch):
    db = exo_env.db
    db.insert_raw_activities_batch(_activities(date(2026, 10, 4), 20))
    monkeypatch.setattr(llm_client, "is_alive", mock.MagicMock(return_value=True))
    monkeypatch.setattr(llm_client, "ensure_local_gguf_models", mock.MagicMock(return_value={}))
    monkeypatch.setattr(llm_client, "force_clear_vram", mock.MagicMock(return_value=4.0))
    monkeypatch.setattr(HardwareProbe, "get_vram_info", staticmethod(lambda: (4.0, 16.0)))
    for name in ("generate_structured", "generate_text", "generate_vision"):
        monkeypatch.setattr(llm_client, name, mock.MagicMock(side_effect=AssertionError(f"{name} appelé en mode CPU")))

    nc = NightConsolidator(db_manager=db)
    res = nc.consolidate()

    assert res["cpu_only"] is True
    assert res["classified_activities"] == 20
    assert "2026-10-04" in res["processed_dates"]
    assert (settings.EPISODIC_DIR / "2026-10-04.md").exists()
    with db.get_connection() as conn:
        assert conn.execute("SELECT COUNT(*) FROM daily_metrics;").fetchone()[0] == 1
    assert json.loads(nc.pending_llm_dates_path.read_text(encoding="utf-8")) == ["2026-10-04"]
    assert res["drive_files"]

    # Nuit suivante avec GPU libre : la date est re-synthétisée puis retirée de la liste
    nc2 = NightConsolidator(db_manager=db)
    monkeypatch.setattr(llm_client, "force_clear_vram", mock.MagicMock(return_value=16.0))
    monkeypatch.setattr(HardwareProbe, "get_vram_info", staticmethod(lambda: (16.0, 16.0)))
    monkeypatch.setattr(llm_client, "check_and_select_model", mock.MagicMock(return_value=settings.MODEL_FAST_VISION))
    monkeypatch.setattr(llm_client, "generate_text", mock.MagicMock(return_value="Synthèse LLM du 04/10."))
    monkeypatch.setattr(llm_client, "generate_structured", mock.MagicMock(side_effect=RuntimeError("hors sujet")))
    with mock.patch.object(nc2, "run_pass_3_vector_indexing", return_value=0):
        res2 = nc2.consolidate()
    assert "2026-10-04" in res2["processed_dates"]
    assert "Synthèse LLM du 04/10." in (settings.EPISODIC_DIR / "2026-10-04.md").read_text(encoding="utf-8")
    assert not nc2.pending_llm_dates_path.exists()
