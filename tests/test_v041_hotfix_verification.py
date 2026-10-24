"""
Suite de tests de vérification pour la version v0.4.1 :
EXO-013 — Hotfix Intégration, Isolation VRAM Sommeil Profond & Fix Filtres UI.
1. Interdiction des auto-fusions et isolation VRAM séquentielle en Sommeil Profond (GraphDefragmenter).
2. Exécution du Context Bootloader restreinte à la date la plus récente dans NightConsolidator.
3. Initialisation immédiate du summary dans chat_sessions dès le premier tour live.
"""

from __future__ import annotations

import json
import sys
import unittest.mock as mock
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pandas as pd
import pytest

from src.config import settings
from src.consolidators.graph_defragmenter import (
    ConceptMergeSchema,
    GraphDefragmenter,
)
from src.consolidators.night_consolidator import NightConsolidator
from src.database.db_manager import (
    DailyMetricRecord,
    DBManager,
    RawActivityRecord,
)
from src.llm.ollama_client import llm_client
from src.utils.markdown_io import (
    ConceptFrontmatter,
    ParsedConceptNote,
    write_concept_file,
)


# ==============================================================================
# FIXTURES DE TEST
# ==============================================================================

@pytest.fixture
def v041_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Prépare un environnement isolé avec base SQLite et répertoires Vault."""
    vault_root = tmp_path / "Vault_Data"
    concepts_dir = vault_root / "02_Concepts"
    archive_merged_dir = concepts_dir / "_Archive_Merged"
    episodic_dir = vault_root / "01_Episodique"
    meta_dir = vault_root / "00_Meta"
    buffer_dir = vault_root / "_System_Buffer"
    voice_inbox = buffer_dir / "voice_inbox"
    voice_processed = voice_inbox / "processed"

    for d in [concepts_dir, archive_merged_dir, episodic_dir, meta_dir, buffer_dir, voice_inbox, voice_processed]:
        d.mkdir(parents=True, exist_ok=True)

    db_file = buffer_dir / "telemetry.db"
    db = DBManager(db_path=db_file)
    db.init_db()

    # Redirection dynamique de settings
    monkeypatch.setattr(settings, "VAULT_ROOT", vault_root)
    monkeypatch.setattr(type(settings), "CONCEPTS_DIR", property(lambda self: concepts_dir))
    monkeypatch.setattr(type(settings), "CONCEPTS_ARCHIVE_MERGED_DIR", property(lambda self: archive_merged_dir))
    monkeypatch.setattr(type(settings), "EPISODIC_DIR", property(lambda self: episodic_dir))
    monkeypatch.setattr(type(settings), "META_DIR", property(lambda self: meta_dir))
    monkeypatch.setattr(type(settings), "BOOTLOADER_PATH", property(lambda self: meta_dir / "00_BOOTLOADER_DEMAIN.md"))
    monkeypatch.setattr(type(settings), "SYSTEM_BUFFER_DIR", property(lambda self: buffer_dir))
    monkeypatch.setattr(type(settings), "VOICE_INBOX_DIR", property(lambda self: voice_inbox))
    monkeypatch.setattr(type(settings), "VOICE_PROCESSED_DIR", property(lambda self: voice_processed))

    return db, vault_root, concepts_dir, archive_merged_dir, episodic_dir, meta_dir, buffer_dir


# ==============================================================================
# TEST 1 : GRAPH DEFRAGMENTER - AUTO-FUSION INTERDITE & ISOLATION VRAM
# ==============================================================================

def test_defragmenter_no_self_merge_and_vram_isolation(v041_env):
    """
    Vérifie que :
    1. find_merge_and_contradiction_candidates ignore les paires où slug ou chemin sont identiques.
    2. merge_concepts_pair lève une ValueError en cas de tentative d'auto-fusion.
    3. run_defragmentation_cycle décharge MODEL_HEAVY_SYNTHESIS avant d'indexer dans LanceDB,
       puis décharge MODEL_EMBEDDING à la fin.
    """
    db, vault_root, concepts_dir, archive_merged_dir, _, _, _ = v041_env

    # 1. Création de deux notes pour tester le cycle
    note_a_path = concepts_dir / "note-alpha.md"
    note_a = ParsedConceptNote(
        frontmatter=ConceptFrontmatter(
            id="note-alpha",
            title="Pattern CQRS et Event Sourcing",
            type="concept",
            semantic_topic="Dev_et_Architecture_Tech",
            tags=["cqrs", "architecture"],
            created_at="2026-10-20",
            updated_at="2026-10-20",
            total_time_invested_min=30,
            summary_1_line="Note alpha sur CQRS.",
        ),
        title_h1="Pattern CQRS et Event Sourcing",
        body="Corps note alpha.",
        telemetry_lines=[],
        file_path=note_a_path,
    )
    write_concept_file(note_a, note_a_path)

    note_b_path = concepts_dir / "note-beta.md"
    note_b = ParsedConceptNote(
        frontmatter=ConceptFrontmatter(
            id="note-beta",
            title="Architecture CQRS Avancée",
            type="concept",
            semantic_topic="Dev_et_Architecture_Tech",
            tags=["cqrs", "event-sourcing"],
            created_at="2026-10-22",
            updated_at="2026-10-22",
            total_time_invested_min=45,
            summary_1_line="Note beta sur CQRS.",
        ),
        title_h1="Architecture CQRS Avancée",
        body="Corps note beta.",
        telemetry_lines=[],
        file_path=note_b_path,
    )
    write_concept_file(note_b, note_b_path)

    # 2. Test auto-fusion : merge_concepts_pair doit lever ValueError
    mock_vs = mock.MagicMock()
    defragmenter = GraphDefragmenter(db_manager=db, vector_store=mock_vs)

    dummy_decision = ConceptMergeSchema(
        should_merge=True,
        canonical_title="CQRS Canonique",
        canonical_slug="cqrs-canonique",
        merged_summary_1_line="Synthèse CQRS.",
        merged_markdown_body="Corps fusionné.",
    )

    with pytest.raises(ValueError, match="Impossible de fusionner une fiche avec elle-même"):
        defragmenter.merge_concepts_pair(note_a_path, note_a_path, dummy_decision)

    # 3. Test find_merge_and_contradiction_candidates avec auto-paire simulée
    fake_df = pd.DataFrame([
        {
            "id": "1",
            "title": "Pattern CQRS",
            "slug": "note-alpha",
            "semantic_topic": "Dev_et_Architecture_Tech",
            "tags": "['cqrs']",
            "file_path": str(note_a_path),
            "vector": [1.0, 0.5, 0.2],
        },
        {
            "id": "2",
            "title": "Pattern CQRS Dupliqué",
            "slug": "note-alpha",  # Même slug !
            "semantic_topic": "Dev_et_Architecture_Tech",
            "tags": "['cqrs']",
            "file_path": str(note_a_path),
            "vector": [1.0, 0.5, 0.2],
        },
    ])
    mock_vs._table.to_pandas.return_value = fake_df

    candidates = defragmenter.find_merge_and_contradiction_candidates()
    # L'auto-paire doit être filtrée : 0 candidat
    assert len(candidates) == 0

    # 4. Test de l'isolation VRAM séquentielle dans run_defragmentation_cycle
    # On fournit deux enregistrements distincts
    distinct_df = pd.DataFrame([
        {
            "id": "1",
            "title": "Pattern CQRS et Event Sourcing",
            "slug": "note-alpha",
            "semantic_topic": "Dev_et_Architecture_Tech",
            "tags": "['cqrs']",
            "file_path": str(note_a_path),
            "vector": [1.0, 0.5, 0.2],
        },
        {
            "id": "2",
            "title": "Architecture CQRS Avancée",
            "slug": "note-beta",
            "semantic_topic": "Dev_et_Architecture_Tech",
            "tags": "['cqrs']",
            "file_path": str(note_b_path),
            "vector": [0.99, 0.49, 0.21],
        },
    ])
    mock_vs._table.to_pandas.return_value = distinct_df

    call_order: List[str] = []

    def mock_unload(model_name: str):
        call_order.append(f"unload:{model_name}")

    def mock_index(path: Path):
        call_order.append(f"index:{path.name}")

    mock_vs.index_concept_file.side_effect = mock_index

    with mock.patch.object(llm_client, "is_alive", return_value=True), \
         mock.patch.object(llm_client, "generate_structured", return_value=dummy_decision), \
         mock.patch.object(llm_client, "unload_model", side_effect=mock_unload):

        res = defragmenter.run_defragmentation_cycle()
        assert res["merges_done"] == 1

        # Vérification de l'ordre d'appel strict (Exclusion Mutuelle VRAM)
        # 1. Déchargement du modèle de synthèse lourd (26B)
        # 2. Indexation vectorielle LanceDB (bge-m3)
        # 3. Déchargement du modèle d'embedding (bge-m3)
        heavy_unload = f"unload:{settings.MODEL_HEAVY_SYNTHESIS}"
        embed_unload = f"unload:{settings.MODEL_EMBEDDING}"

        assert heavy_unload in call_order
        assert embed_unload in call_order

        heavy_idx = call_order.index(heavy_unload)
        embed_idx = call_order.index(embed_unload)

        # Vérifie qu'au moins une indexation a eu lieu APRÈS le déchargement du 26B
        index_indices = [i for i, c in enumerate(call_order) if c.startswith("index:")]
        assert len(index_indices) > 0
        for idx in index_indices:
            assert idx > heavy_idx, "L'indexation vectorielle a eu lieu avant le déchargement du modèle lourd !"
            assert idx < embed_idx, "L'indexation vectorielle a eu lieu après le déchargement du modèle d'embedding !"


# ==============================================================================
# TEST 2 : NIGHT CONSOLIDATOR - BOOTLOADER SUR LA DATE LA PLUS RÉCENTE
# ==============================================================================

def test_night_consolidator_bootloader_only_on_latest_date(v041_env):
    """
    Insère des activités sur 2 dates distinctes (2026-04-10 et 2026-04-15).
    Vérifie que :
    - consolidate() produit les 2 journaux épisodiques 2026-04-10.md et 2026-04-15.md.
    - 00_BOOTLOADER_DEMAIN.md n'est généré qu'une seule fois et porte la date la plus récente (2026-04-15).
    """
    db, vault_root, concepts_dir, _, episodic_dir, meta_dir, _ = v041_env

    # 1. Insertion activités date 1 : 2026-04-10
    act_old = RawActivityRecord(
        timestamp_start=datetime(2026, 4, 10, 10, 0, 0),
        timestamp_end=datetime(2026, 4, 10, 11, 0, 0),
        duration_sec=3600,
        executable="code.exe",
        window_title="projet_v01.py - cerveau-deux",
        semantic_topic="Dev_et_Architecture_Tech",
        cognitive_mode="production",
        processed=True,
    )

    # 2. Insertion activités date 2 : 2026-04-15 (plus récente)
    act_recent = RawActivityRecord(
        timestamp_start=datetime(2026, 4, 15, 14, 0, 0),
        timestamp_end=datetime(2026, 4, 15, 16, 0, 0),
        duration_sec=7200,
        executable="code.exe",
        window_title="graph_defragmenter.py - cerveau-deux",
        semantic_topic="Dev_et_Architecture_Tech",
        cognitive_mode="production",
        processed=True,
    )
    db.insert_raw_activities_batch([act_old, act_recent])

    consolidator = NightConsolidator(db_manager=db)

    # Mock de Passe 1 et de l'indexation Passe 3
    with mock.patch.object(consolidator, "run_pass_1_vision_and_tagging", return_value=0), \
         mock.patch.object(consolidator, "run_pass_3_vector_indexing", return_value=0), \
         mock.patch.object(llm_client, "is_alive", return_value=False):

        result = consolidator.consolidate()

        # Les deux dates ont été traitées
        assert (episodic_dir / "2026-04-10.md").exists()
        assert (episodic_dir / "2026-04-15.md").exists()

        # Le Context Bootloader existe et doit porter la date de la session la plus récente
        bootloader_path = settings.BOOTLOADER_PATH
        assert bootloader_path.exists()
        bootloader_text = bootloader_path.read_text(encoding="utf-8")

        assert "`2026-04-15`" in bootloader_text
        assert "2026-04-10" not in bootloader_text


# ==============================================================================
# TEST 3 : LIVE CHAT TURN - INITIALISATION DU SUMMARY DANS CHAT_SESSIONS
# ==============================================================================

def test_live_chat_turn_initializes_summary(v041_env):
    """
    Vérifie que la méthode upsert_live_chat_turn initialise le champ summary
    de chat_sessions avec clean_prompt[:140] dès la création de la session,
    évitant ainsi les intitulés vides dans l'Explorateur Épistémique du Dashboard.
    """
    db, _, _, _, _, _, _ = v041_env

    session_id = "test_live_summary_init"
    prompt_text = "Comment garantir l'isolation stricte de la VRAM lors de la défragmentation sémantique nocturne ?"
    ai_resp = "Il faut décharger le modèle 26B avant de charger le modèle d'embedding bge-m3."

    res = db.upsert_live_chat_turn(
        platform="gemini",
        session_id=session_id,
        user_prompt=prompt_text,
        ai_response=ai_resp,
    )
    assert res["status"] == "created"

    sess = db.get_chat_session_by_id(session_id)
    assert sess is not None
    assert sess["summary"] != ""
    assert sess["summary"] == prompt_text[:140]

