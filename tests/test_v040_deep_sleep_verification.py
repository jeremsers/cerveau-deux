"""
Suite de tests de vérification pour la version v0.4.0 :
EXO-012 — Sommeil Profond : Défragmentation du Graphe, Contradictions & Sas Vocal.
1. Calcul pur Python de la similarité cosinus (cosine_similarity).
2. Défragmentation et fusion de fiches (merge_concepts_pair) :
   - Cumul du temps total investi.
   - Archivage sécurisé dans _Archive_Merged/ (Zéro Perte, aucun unlink()).
   - Réécriture exhaustive des [[wikilinks]] dans 01_Episodique/ et 02_Concepts/.
3. Traçage des évolutions d'arbitrage (annotate_contradiction) :
   - Injection du callout Obsidian '> [!warning] Évolution d'Arbitrage'.
   - Idempotence stricte (aucun doublon sur appels répétés).
4. Pipeline d'ingestion des mémos vocaux (VoiceIngestor) :
   - Transcription isolée sans VRAM.
   - Ingestion SQLite (chat_sessions, chat_messages).
   - Génération de note conceptuelle et archivage du fichier audio dans processed/.
"""

from __future__ import annotations

import json
import os
import sys
import unittest.mock as mock
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest

from src.config import settings
from src.consolidators.graph_defragmenter import (
    ConceptMergeSchema,
    GraphDefragmenter,
    cosine_similarity,
)
from src.database.db_manager import DBManager
from src.ingestors.voice_ingestor import VoiceIngestor
from src.utils.markdown_io import (
    ConceptFrontmatter,
    ParsedConceptNote,
    parse_concept_file,
    write_concept_file,
)


# ==============================================================================
# FIXTURES DE TEST
# ==============================================================================

@pytest.fixture
def v040_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Prépare un environnement isolé avec base SQLite et arborescence Vault."""
    vault_root = tmp_path / "Vault_Data"
    concepts_dir = vault_root / "02_Concepts"
    archive_merged_dir = concepts_dir / "_Archive_Merged"
    episodic_dir = vault_root / "01_Episodique"
    buffer_dir = vault_root / "_System_Buffer"
    voice_inbox = buffer_dir / "voice_inbox"
    voice_processed = voice_inbox / "processed"

    for d in [concepts_dir, archive_merged_dir, episodic_dir, buffer_dir, voice_inbox, voice_processed]:
        d.mkdir(parents=True, exist_ok=True)

    db_file = buffer_dir / "telemetry.db"
    db = DBManager(db_path=db_file)
    db.init_db()

    # Redirection dynamique de settings
    monkeypatch.setattr(settings, "VAULT_ROOT", vault_root)
    monkeypatch.setattr(type(settings), "CONCEPTS_DIR", property(lambda self: concepts_dir))
    monkeypatch.setattr(type(settings), "CONCEPTS_ARCHIVE_MERGED_DIR", property(lambda self: archive_merged_dir))
    monkeypatch.setattr(type(settings), "EPISODIC_DIR", property(lambda self: episodic_dir))
    monkeypatch.setattr(type(settings), "SYSTEM_BUFFER_DIR", property(lambda self: buffer_dir))
    monkeypatch.setattr(type(settings), "VOICE_INBOX_DIR", property(lambda self: voice_inbox))
    monkeypatch.setattr(type(settings), "VOICE_PROCESSED_DIR", property(lambda self: voice_processed))

    return db, vault_root, concepts_dir, archive_merged_dir, episodic_dir, voice_inbox, voice_processed


# ==============================================================================
# TEST 1 : SIMILARITÉ COSINUS EN PUR PYTHON (0 MO VRAM)
# ==============================================================================

def test_cosine_similarity_pure_python():
    """Valide les propriétés géométriques de la similarité cosinus standard."""
    # Vecteurs identiques
    v1 = [1.0, 2.0, 3.0]
    assert pytest.approx(cosine_similarity(v1, v1), 1e-6) == 1.0

    # Vecteurs orthogonaux
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0

    # Vecteurs opposés
    assert pytest.approx(cosine_similarity([1.0, 0.0], [-1.0, 0.0]), 1e-6) == -1.0

    # Cas limites (vides, dimensions inégales ou normes nulles)
    assert cosine_similarity([], []) == 0.0
    assert cosine_similarity([1.0], [1.0, 2.0]) == 0.0
    assert cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


# ==============================================================================
# TEST 2 : FUSION DE FICHES, ARCHIVAGE SÉCURISÉ & RÉÉCRITURE DES WIKILINKS
# ==============================================================================

def test_graph_defragmenter_merge_and_wikilink_rewrite(v040_env):
    """
    Crée 2 fiches conceptuelles redondantes A et B et un journal épisodique référençant A.
    Exécute merge_concepts_pair et vérifie :
    1. Le cumul exact du temps total investi et la fusion des tags.
    2. Le déplacement des anciennes fiches dans _Archive_Merged/ (zéro unlink()).
    3. La réécriture exhaustive des wikilinks [[A]], [[slug-a]] et [[slug-a|alias]] dans le journal épisodique.
    """
    db, vault_root, concepts_dir, archive_merged_dir, episodic_dir, _, _ = v040_env

    # 1. Fiche A (Ancienne)
    note_a_path = concepts_dir / "note-a-architecture.md"
    note_a = ParsedConceptNote(
        frontmatter=ConceptFrontmatter(
            id="note-a-architecture",
            title="Architecture Microservices (v1)",
            type="concept",
            origin=["gemini_takeout"],
            semantic_topic="Dev_et_Architecture_Tech",
            tags=["architecture", "backend"],
            created_at="2026-10-15",
            updated_at="2026-10-15",
            total_time_invested_min=45,
            summary_1_line="Architecture microservices initiale.",
        ),
        title_h1="Architecture Microservices (v1)",
        body="## Contenu initial\nDescription des services indépendants.",
        telemetry_lines=[
            "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)",
            "> - **Temps cumulé sur ce sujet :** 45m",
            "> - **Sources épisodiques :**",
            ">   - Activité écran du `2026-10-15` (45m)",
        ],
        file_path=note_a_path,
    )
    write_concept_file(note_a, note_a_path)

    # 2. Fiche B (Plus récente)
    note_b_path = concepts_dir / "note-b-cqrs-patterns.md"
    note_b = ParsedConceptNote(
        frontmatter=ConceptFrontmatter(
            id="note-b-cqrs-patterns",
            title="Microservices & Pattern CQRS",
            type="concept",
            origin=["screen_telemetry"],
            semantic_topic="Dev_et_Architecture_Tech",
            tags=["architecture", "cqrs", "event-sourcing"],
            created_at="2026-10-22",
            updated_at="2026-10-22",
            total_time_invested_min=30,
            summary_1_line="Pattern CQRS appliqué aux microservices.",
        ),
        title_h1="Microservices & Pattern CQRS",
        body="## Contenu CQRS\nSéparation commande et requête.",
        telemetry_lines=[
            "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)",
            "> - **Temps cumulé sur ce sujet :** 30m",
            "> - **Sources épisodiques :**",
            ">   - Activité écran du `2026-10-22` (30m)",
        ],
        file_path=note_b_path,
    )
    write_concept_file(note_b, note_b_path)

    # 3. Journal épisodique référençant la Fiche A sous plusieurs formes
    episodic_file = episodic_dir / "2026-10-23.md"
    episodic_file.write_text("""# Journal du 2026-10-23

Aujourd'hui, reprise des travaux sur [[Architecture Microservices (v1)]].
Voir également [[note-a-architecture|alias v1]] et [[note-b-cqrs-patterns]] pour les patterns.
""", encoding="utf-8")

    # Mock du vector store pour éviter le chargement CUDA de bge-m3
    mock_vs = mock.MagicMock()
    defragmenter = GraphDefragmenter(db_manager=db, vector_store=mock_vs)

    merge_decision = ConceptMergeSchema(
        should_merge=True,
        canonical_title="Architecture Microservices & Patterns CQRS",
        canonical_slug="architecture-microservices-cqrs-canonique",
        merged_summary_1_line="Synthèse complète unifiée de l'architecture microservices et du pattern CQRS.",
        merged_markdown_body="## 1. Vue d'Ensemble\nArchitecture consolidée.",
        contradiction_detected=False,
    )

    merged_path = defragmenter.merge_concepts_pair(note_a_path, note_b_path, merge_decision)

    # --- Vérification 1 : Propriétés de la note canonique fusionnée ---
    assert merged_path.exists()
    canonical_note = parse_concept_file(merged_path)
    assert canonical_note.frontmatter.title == "Architecture Microservices & Patterns CQRS"
    # Cumul du temps investi (45 + 30 = 75 minutes)
    assert canonical_note.frontmatter.total_time_invested_min == 75
    # Fusion des tags sans doublons
    assert set(canonical_note.frontmatter.tags) == {"architecture", "backend", "cqrs", "event-sourcing"}
    # Date de création la plus ancienne conservée
    assert canonical_note.frontmatter.created_at == "2026-10-15"

    # --- Vérification 2 : Archivage sécurisé dans _Archive_Merged/ (Zéro Perte) ---
    assert (archive_merged_dir / "note-a-architecture.md").exists()
    assert (archive_merged_dir / "note-b-cqrs-patterns.md").exists()
    assert not note_a_path.exists()
    assert not note_b_path.exists()

    # --- Vérification 3 : Réécriture globale des wikilinks dans le journal épisodique ---
    rewritten_episodic = episodic_file.read_text(encoding="utf-8")
    assert "[[Architecture Microservices & Patterns CQRS]]" in rewritten_episodic
    assert "[[Architecture Microservices & Patterns CQRS|alias v1]]" in rewritten_episodic
    # Les anciens liens doivent avoir disparu
    assert "[[Architecture Microservices (v1)]]" not in rewritten_episodic
    assert "[[note-a-architecture|alias v1]]" not in rewritten_episodic
    assert "[[note-b-cqrs-patterns]]" not in rewritten_episodic


# ==============================================================================
# TEST 3 : TRAÇAGE DES CONTRADICTIONS & IDEMPOTENCE DU CALLOUT
# ==============================================================================

def test_contradiction_callout_injection_idempotence(v040_env):
    """
    Vérifie l'injection d'un callout Obsidian '> [!warning] Évolution d'Arbitrage'
    en haut du corps Markdown de l'ancienne note lorsqu'une contradiction est détectée,
    et garantit une idempotence stricte en cas de double exécution.
    """
    db, vault_root, concepts_dir, _, _, _, _ = v040_env

    older_note_file = concepts_dir / "choix-chromadb.md"
    note = ParsedConceptNote(
        frontmatter=ConceptFrontmatter(
            id="choix-chromadb",
            title="Choix Base Vectorielle ChromaDB",
            type="concept",
            semantic_topic="Dev_et_Architecture_Tech",
            created_at="2026-08-10",
            updated_at="2026-08-10",
            total_time_invested_min=30,
            summary_1_line="Utilisation initiale de ChromaDB.",
        ),
        title_h1="Choix Base Vectorielle ChromaDB",
        body="## Contexte\nChromaDB est retenu pour les embeddings.",
        telemetry_lines=[],
        file_path=older_note_file,
    )
    write_concept_file(note, older_note_file)

    defragmenter = GraphDefragmenter(db_manager=db, vector_store=mock.MagicMock())

    # 1. Première annotation de contradiction
    defragmenter.annotate_contradiction(
        older_note_path=older_note_file,
        newer_note_title="Migration vers LanceDB Embarqué",
        explanation="Abandon de ChromaDB au profit de LanceDB pour éliminer la surcharge RAM.",
        date_str="2026-10-24",
    )

    parsed_1 = parse_concept_file(older_note_file)
    assert "> [!warning] Évolution d'Arbitrage (Mis à jour le 2026-10-24)" in parsed_1.body
    assert "[[Migration vers LanceDB Embarqué]]" in parsed_1.body
    assert "Abandon de ChromaDB au profit de LanceDB" in parsed_1.body
    assert parsed_1.frontmatter.updated_at == "2026-10-24"

    # 2. Deuxième appel identique (Test d'idempotence stricte)
    defragmenter.annotate_contradiction(
        older_note_path=older_note_file,
        newer_note_title="Migration vers LanceDB Embarqué",
        explanation="Abandon de ChromaDB au profit de LanceDB pour éliminer la surcharge RAM.",
        date_str="2026-10-24",
    )

    parsed_2 = parse_concept_file(older_note_file)
    # Le callout ne doit apparaître qu'une seule et unique fois
    count_callouts = parsed_2.body.count("[!warning] Évolution d'Arbitrage")
    assert count_callouts == 1


# ==============================================================================
# TEST 4 : PIPELINE D'INGESTION DES MÉMOS VOCAUX (VOICE_INGESTOR)
# ==============================================================================

def test_voice_ingestor_pipeline(v040_env):
    """
    Simule la présence d'un mémo audio dans voice_inbox/ avec transcripteur mocké.
    Vérifie :
    1. L'ingestion dans SQLite (chat_sessions avec turn_count=1, chat_messages).
    2. La création de la fiche conceptuelle atomique dans 02_Concepts/ avec origin: ["voice_memo"].
    3. L'archivage physique du fichier audio dans processed/.
    """
    db, vault_root, concepts_dir, _, _, voice_inbox, voice_processed = v040_env

    # 1. Création d'un faux fichier audio mémo
    audio_file = voice_inbox / "20261024_163000_reflexion_event_driven.m4a"
    audio_file.write_bytes(b"FAKE_AUDIO_DATA_FOR_TESTING")

    # Mock du transcripteur (0 Mo VRAM)
    def mock_transcriber(path: Path) -> str:
        return (
            "Réflexion sur les bus d'événements asynchrones. "
            "Il est impératif de séparer la capture de télémétrie de l'indexation vectorielle "
            "pour garantir une réactivité maximale."
        )

    ingestor = VoiceIngestor(
        db_manager=db,
        inbox_dir=voice_inbox,
        processed_dir=voice_processed,
        transcriber=mock_transcriber,
    )

    result = ingestor.run()
    assert result["processed_count"] == 1
    assert len(result["created_notes"]) == 1

    created_note_path = result["created_notes"][0]
    assert created_note_path.exists()

    # 2. Vérification de la note conceptuelle
    note = parse_concept_file(created_note_path)
    assert "voice_memo" in note.frontmatter.origin
    assert "vocal" in note.frontmatter.tags
    assert "bus d'événements asynchrones" in note.body
    assert "20261024_163000_reflexion_event_driven.m4a" in "\n".join(note.telemetry_lines)

    # 3. Vérification de l'enregistrement SQLite
    session_id = note.frontmatter.session_id
    assert session_id is not None
    session_db = db.get_chat_session_by_id(session_id)
    assert session_db is not None
    assert session_db["turn_count"] == 1

    messages_db = db.fetch_messages_for_session(session_id)
    assert len(messages_db) == 1
    assert messages_db[0]["turn_index"] == 0
    assert "bus d'événements asynchrones" in messages_db[0]["user_prompt"]

    # 4. Vérification du déplacement du fichier audio dans processed/
    assert not audio_file.exists()
    assert (voice_processed / audio_file.name).exists()

