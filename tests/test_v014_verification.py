"""
Suite de tests de validation pour la version v0.1.4.
Vérifie la conformité des 5 lots de la spécification :
1. Paramètres de configuration (INACTIVITY_SESSION_THRESHOLD_MIN == 45, PROLONGED_SESSION_THRESHOLD_SEC).
2. Verrouillage anti-collision des slugs et des identifiants dans LanceDB et Takeout Ingestor.
3. Passe 2 du NightConsolidator (NightConceptSynthesisSchema, recherche CPU pure, zéro import déprécié).
4. Moteur de recherche et requêtes SQLite du Dashboard Streamlit (KPIS décorrélés, Volet A & B).
"""

from __future__ import annotations

import json
import os
import re
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pytest

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.config import settings, AUTHORIZED_SEMANTIC_TOPICS
from src.database.db_manager import DBManager
from src.database.vector_store import VectorStore
from src.ingestors.takeout_ingestor import (
    DistilledConceptSchema,
    ParsedTurn,
    ReconstructedSession,
    save_distilled_concept_note,
)
from src.consolidators.night_consolidator import (
    NightConsolidator,
    NightConceptSynthesisSchema,
)
from src.dashboard.app import (
    load_macro_kpis,
    load_chat_search_results,
    load_messages_for_session,
    load_footprints_summary,
    load_top_channels_and_domains,
    load_burst_clusters_summary,
    search_historical_footprints,
)


def test_lot1_config_parameters():
    """Vérifie l'alignement des paramètres dans src/config.py et .env.example."""
    # 1. Valeur par défaut dans config
    assert settings.INACTIVITY_SESSION_THRESHOLD_MIN == 45, (
        f"INACTIVITY_SESSION_THRESHOLD_MIN attendu à 45, obtenu: {settings.INACTIVITY_SESSION_THRESHOLD_MIN}"
    )

    # 2. Vérification de .env.example
    env_example_path = _ROOT / ".env.example"
    assert env_example_path.exists(), ".env.example introuvable"
    env_content = env_example_path.read_text(encoding="utf-8")

    assert "INACTIVITY_SESSION_THRESHOLD_MIN=45" in env_content, (
        "INACTIVITY_SESSION_THRESHOLD_MIN=45 non trouvé dans .env.example"
    )
    assert "PROLONGED_SESSION_THRESHOLD_SEC=180" in env_content, (
        "PROLONGED_SESSION_THRESHOLD_SEC=180 non trouvé dans .env.example"
    )


def test_lot2_slug_anti_collision_takeout(exo_env):
    """Vérifie que deux sessions distinctes avec le même slug ne s'écrasent jamais."""
    created_files: List[Path] = []
    test_slug = "test-collision-v014-concept"
    original_file = settings.CONCEPTS_DIR / f"{test_slug}.md"

    try:
        # 1. Écriture d'une première note issue d'une session A
        sess_a = ReconstructedSession(
            session_id="session_aaa_111",
            timestamp_start=datetime(2025, 1, 10, 14, 0, 0),
            timestamp_end=datetime(2025, 1, 10, 14, 30, 0),
            turns=[
                ParsedTurn(
                    turn_index=0,
                    timestamp=datetime(2025, 1, 10, 14, 0, 0),
                    user_prompt="Question A",
                    ai_response="Reponse A",
                    user_char_count=10,
                )
            ],
            turn_count=1,
            user_char_count=10,
            summary="Session A Summary",
        )
        schema_a = DistilledConceptSchema(
            concept_title="Test Concept A",
            slug=test_slug,
            semantic_topic="Dev_et_Architecture_Tech",
            tags=["dev", "test"],
            summary_1_line="Concept original de la session A",
            synthesized_markdown_body="### Contexte\nCorps original de la session A.",
            is_worth_indexing=True,
            related_concepts=[],
        )

        db = exo_env.db
        ok_a, status_a = save_distilled_concept_note(sess_a, schema_a, db)
        assert ok_a is True
        assert status_a == "success"
        assert original_file.exists()
        created_files.append(original_file)

        content_a = original_file.read_text(encoding="utf-8")
        assert "session_aaa_111" in content_a
        assert "Concept original de la session A" in content_a

        # 2. Tentative d'écriture d'une session B avec le MÊME slug
        sess_b = ReconstructedSession(
            session_id="session_bbb_222",
            timestamp_start=datetime(2025, 2, 20, 10, 0, 0),
            timestamp_end=datetime(2025, 2, 20, 10, 45, 0),
            turns=[
                ParsedTurn(
                    turn_index=0,
                    timestamp=datetime(2025, 2, 20, 10, 0, 0),
                    user_prompt="Question B",
                    ai_response="Reponse B",
                    user_char_count=10,
                )
            ],
            turn_count=1,
            user_char_count=10,
            summary="Session B Summary",
        )
        schema_b = DistilledConceptSchema(
            concept_title="Test Concept B",
            slug=test_slug,  # Collision volontaire !
            semantic_topic="Dev_et_Architecture_Tech",
            tags=["dev", "collision"],
            summary_1_line="Concept concurrent de la session B",
            synthesized_markdown_body="### Contexte\nCorps concurrent de la session B.",
            is_worth_indexing=True,
            related_concepts=[],
        )

        ok_b, status_b = save_distilled_concept_note(sess_b, schema_b, db)
        assert ok_b is True
        assert status_b == "success"

        # Le slug attendu pour la session B est f"{test_slug}-2025-02-20-sessio"
        file_b = settings.CONCEPTS_DIR / f"{test_slug}-2025-02-20-sessio.md"
        assert file_b.exists(), f"Fiche B introuvable à {file_b}"
        created_files.append(file_b)

        # 3. Vérifier que la note A est intacte (aucun écrasement silencieux)
        content_a_after = original_file.read_text(encoding="utf-8")
        assert "session_aaa_111" in content_a_after
        assert "Concept original de la session A" in content_a_after

        # 4. Vérifier que la note B contient ses propres métadonnées
        content_b = file_b.read_text(encoding="utf-8")
        assert "session_bbb_222" in content_b
        assert "Concept concurrent de la session B" in content_b

    finally:
        # Nettoyage des fichiers de test
        for p in created_files:
            if p.exists():
                try:
                    p.unlink()
                except Exception:
                    pass


def test_lot2_lancedb_vector_store_slug_key():
    """Vérifie que la clé primaire de suppression LanceDB utilise bien le slug canonique."""
    vstore_code = (_ROOT / "src" / "database" / "vector_store.py").read_text(encoding="utf-8")
    assert "slug = '{safe_slug}'" in vstore_code or 'slug = \\\'{safe_slug}\\\'' in vstore_code, (
        "vector_store.py ne cible pas slug = '{safe_slug}' pour la suppression idempotente"
    )
    assert 'f"{raw_id}_{file_path.stem[:32]}"' in vstore_code, (
        "vector_store.py n'inclut pas le slug dans le doc_id pour garantir l'unicité de clé"
    )


def test_lot3_night_consolidator_schema_and_purity(exo_env):
    """Vérifie la Passe 2 du NightConsolidator (Schéma Pydantic & Absence d'import déprécié)."""
    # 1. Vérification de l'absence d'import circulaire / déprécié
    night_code = (_ROOT / "src" / "consolidators" / "night_consolidator.py").read_text(encoding="utf-8")
    assert "register_new_taxonomy_tag" not in night_code, (
        "L'import déprécié register_new_taxonomy_tag est encore présent dans night_consolidator.py"
    )

    # 2. Validation du schéma NightConceptSynthesisSchema
    schema_instance = NightConceptSynthesisSchema(
        concept_title="Optimisation Pipeline RAG LanceDB",
        slug="optimisation-pipeline-rag-lancedb",
        tags=["rag", "lancedb", "vram"],
        summary_1_line="Optimisation des flux vectoriels locaux et exclusion VRAM.",
        synthesized_markdown_body="### Contexte & Problématique\nÉviter le thrashing VRAM.",
        related_concepts=["LanceDB Architecture", "VRAM Management"],
    )
    assert schema_instance.concept_title == "Optimisation Pipeline RAG LanceDB"
    assert schema_instance.slug == "optimisation-pipeline-rag-lancedb"
    assert len(schema_instance.tags) == 3

    # 3. Vérification de la méthode CPU-only
    consolidator = NightConsolidator(db_manager=exo_env.db)
    assert hasattr(consolidator, "_find_matching_existing_concept_cpu"), (
        "Méthode _find_matching_existing_concept_cpu manquante sur NightConsolidator"
    )


@pytest.fixture
def seeded_dashboard(exo_env):
    """Base temporaire semée (v0.5.6, F1) : invariants relatifs au lieu des volumes personnels."""
    import streamlit as st
    from src.database.db_manager import ChatMessageRecord, ChatSessionRecord, HistoricalFootprintRecord

    db = exo_env.db
    sessions = [
        ChatSessionRecord(session_id=f"s{i}", timestamp_start=datetime(2026, 1, 1 + i, 10),
                          timestamp_end=datetime(2026, 1, 1 + i, 11), turn_count=4, user_char_count=900,
                          extracted_topics_json='["IA_et_LLM_Local"]', summary=f"Session Python {i}",
                          distillation_status="success")
        for i in range(3)
    ]
    db.insert_chat_sessions_batch(sessions)
    db.insert_chat_messages_batch([
        ChatMessageRecord(session_id=s.session_id, turn_index=t, timestamp=s.timestamp_start,
                          user_prompt=f"Question Python {t}", ai_response="R", user_char_count=225)
        for s in sessions for t in range(4)
    ])
    db.insert_historical_footprints_batch(
        [HistoricalFootprintRecord(source="youtube", timestamp=datetime(2026, 1, 1, 20, i), title_or_query=f"Vidéo {i}",
                                   channel_or_domain="Chaîne A", cluster_id="cluster_a") for i in range(4)]
        + [HistoricalFootprintRecord(source="google_search", timestamp=datetime(2026, 1, 2, 9, i), title_or_query=f"requête {i}",
                                     channel_or_domain="google.com") for i in range(3)]
    )
    st.cache_data.clear()
    st.cache_resource.clear()
    yield db
    st.cache_data.clear()
    st.cache_resource.clear()


def test_lot4_dashboard_macro_kpis_sqlite(seeded_dashboard):
    """Vérifie que load_macro_kpis() s'exécute sans erreur SQL et reflète la base."""
    kpis = load_macro_kpis()
    required_keys = [
        "chat_count", "chat_hours", "total_turns", "total_chars", "raw_count", "os_hours",
        "total_tracked_hours", "active_prod_hours", "passive_exp_hours", "max_hyperfocus_hours",
        "max_hyperfocus_topic", "avg_switch_rate", "avg_read_ratio", "fp_count",
    ]
    for rk in required_keys:
        assert rk in kpis, f"Clé manquante dans load_macro_kpis() : {rk}"
    assert kpis["chat_count"] == 3 and kpis["total_turns"] == 12
    assert kpis["fp_count"] == 7
    assert kpis["max_hyperfocus_hours"] >= 0.0
    assert isinstance(kpis["max_hyperfocus_topic"], str)


def test_lot4_dashboard_tab5_chat_search(seeded_dashboard):
    """Vérifie le moteur de recherche full-text du Volet A (chat_messages & chat_sessions)."""
    all_res = load_chat_search_results(limit=10)
    assert len(all_res) == 3
    sess = all_res[0]
    assert {"session_id", "summary", "distillation_status"} <= set(sess)
    assert len(load_messages_for_session(sess["session_id"])) == 4
    assert len(load_chat_search_results(topic_filter="IA_et_LLM_Local", limit=10)) == 3
    assert len(load_chat_search_results(query="Python", limit=10)) == 3
    assert load_chat_search_results(query="introuvable-xyz", limit=10) == []


def test_lot4_dashboard_tab5_footprints(seeded_dashboard):
    """Vérifie les requêtes d'agrégation et de recherche du Volet B (historical_footprints)."""
    fp_summary = load_footprints_summary()
    assert fp_summary["youtube"] == 4 and fp_summary["search"] == 3
    assert fp_summary["youtube"] + fp_summary["search"] == fp_summary["total"]

    df_top = load_top_channels_and_domains(limit=15)
    assert {"channel_or_domain", "footprint_count"} <= set(df_top.columns)
    assert df_top.iloc[0]["channel_or_domain"] == "Chaîne A" and len(df_top) <= 15

    df_clusters = load_burst_clusters_summary(limit=10)
    assert list(df_clusters["cluster_id"]) == ["cluster_a"]

    df_search = search_historical_footprints(source_filter="youtube", limit=20)
    assert len(df_search) == 4 and (df_search["source"] == "youtube").all()


def run_checks():
    """Exécute la suite v0.1.4 via pytest (les tests reposent désormais sur des fixtures hermétiques)."""
    raise SystemExit(pytest.main([__file__, "-q"]))


if __name__ == "__main__":
    run_checks()
