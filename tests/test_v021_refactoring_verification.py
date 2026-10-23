"""
Tests de vérification et de non-régression pour le Patch v0.2.1 :
Consolidation Architecturale, Vault IO PyYAML, Idempotence Nocturne BM25,
Durcissement Démons Win32 et Découplage Modulaire.
"""

import sys
from datetime import datetime
from pathlib import Path
import unittest.mock as mock

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest
import yaml

from src.config import settings
from src.database.db_manager import DBManager
from src.utils.markdown_io import (
    ConceptFrontmatter,
    ParsedConceptNote,
    parse_concept_string,
    parse_concept_file,
    serialize_concept_note,
    write_concept_file,
)


# ==============================================================================
# CHANTIER 1 : VALIDATION DE MARKDOWN_IO (ROUND-TRIP & CARACTÈRES SPÉCIAUX)
# ==============================================================================

def test_markdown_io_roundtrip_with_special_characters(tmp_path: Path):
    """
    Vérifie que markdown_io gère impeccablement les titres et résumés contenant
    des deux-points, des guillemets, des apostrophes et des caractères accentués
    sans aucune corruption du YAML frontmatter.
    """
    raw_md = """---
id: "202610231200"
title: "Architecture: "Patterns" & Sys: Micro-Services (v2)"
type: "concept"
origin:
  - "gemini_takeout"
semantic_topic: "Dev_et_Architecture_Tech"
tags:
  - "patterns:advanced"
  - "micro-services"
  - "c++"
session_id: "sess_spec_chars_123"
distillation_status: "success"
created_at: "2026-10-23"
updated_at: "2026-10-23"
total_time_invested_min: 75
summary_1_line: "Analyse des patterns: CQRS, Event-Sourcing & "Outbox Pattern"."
---

# Architecture: "Patterns" & Sys: Micro-Services (v2)

### Problématique & Contexte
L'architecture distribuée nécessite une résilience accrue face aux pannes réseau.

### Arbitrages Techniques & Solutions
- Adoption du pattern Outbox transactionnel.
- Séparation des flux de lecture et d'écriture via CQRS.

> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)
> - **Temps estimé sur ce sujet :** 1h15
> - **Sources épisodiques :**
>   - Session Gemini `sess_spec_chars_123` du 2026-10-23 (4 échanges, 1200 chars écrits)
> - **Connexions sémantiques suggérées :** [[Event-Driven Architecture]], [[PostgreSQL WAL]]
"""

    note = parse_concept_string(raw_md)
    assert note.frontmatter.id == "202610231200"
    assert "Patterns" in note.frontmatter.title
    assert note.frontmatter.semantic_topic == "Dev_et_Architecture_Tech"
    assert note.frontmatter.total_time_invested_min == 75
    assert "Outbox Pattern" in note.frontmatter.summary_1_line
    assert len(note.frontmatter.tags) == 3

    # Sérialisation et écriture sur disque
    target_file = tmp_path / "test-special-chars.md"
    written_path = write_concept_file(note, target_file)
    assert written_path.exists()

    # Relecture depuis le fichier
    reloaded_note = parse_concept_file(written_path)
    assert reloaded_note.frontmatter.id == note.frontmatter.id
    assert reloaded_note.frontmatter.title == note.frontmatter.title
    assert reloaded_note.frontmatter.summary_1_line == note.frontmatter.summary_1_line
    assert reloaded_note.frontmatter.total_time_invested_min == 75
    assert reloaded_note.title_h1 == note.title_h1
    assert "Adoption du pattern Outbox" in reloaded_note.body
    assert len(reloaded_note.telemetry_lines) >= 4


# ==============================================================================
# CHANTIER 1 (SUITE) : IDEMPOTENCE STRICTE DE L'ENRICHISSEMENT NOCTURNE
# ==============================================================================

def test_append_or_replace_daily_session_idempotence():
    """
    Vérifie l'idempotence stricte de ParsedConceptNote.append_or_replace_daily_session.
    Exécuter 3 fois l'enrichissement pour une même date ne doit compter le temps
    qu'une seule fois et ne créer qu'une unique sous-section Markdown.
    """
    fm = ConceptFrontmatter(
        id="202610200000",
        title="LanceDB & Vector Search",
        semantic_topic="IA_et_LLM_Local",
        tags=["lancedb", "vectors"],
        created_at="2026-10-20",
        updated_at="2026-10-20",
        total_time_invested_min=30,
        summary_1_line="Indexation vectorielle locale.",
    )
    body = "### Synthèse Initiale\nIntroduction aux index vectoriels IVF-PQ."
    telemetry = [
        "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)",
        "> - **Temps estimé sur ce sujet :** 30 min",
        "> - **Sources épisodiques :**",
        ">   - Activité écran du `2026-10-20` (30 min)",
        "> - **Connexions sémantiques suggérées :** [[Exocortex]]",
    ]
    note = ParsedConceptNote(
        frontmatter=fm,
        title_h1="LanceDB & Vector Search",
        body=body,
        telemetry_lines=telemetry,
    )

    # 1. Premier enrichissement du 2026-10-23 (45 min)
    mod1 = note.append_or_replace_daily_session(
        date_str="2026-10-23",
        duration_min=45,
        duration_fmt="45 min",
        enrichment_markdown="**Activités clés :** Optimisation des requêtes k-NN.",
        related_links=["[[PyArrow]]"],
    )
    assert mod1 is True
    assert note.frontmatter.total_time_invested_min == 75
    assert note.frontmatter.updated_at == "2026-10-23"
    assert note.body.count("### Session du 2026-10-23") == 1
    assert "Optimisation des requêtes k-NN" in note.body
    assert any("2026-10-23" in l for l in note.telemetry_lines)

    # 2. Deuxième enrichissement le même jour (redémarrage du consolidateur)
    mod2 = note.append_or_replace_daily_session(
        date_str="2026-10-23",
        duration_min=45,
        duration_fmt="45 min",
        enrichment_markdown="**Activités clés :** Optimisation des requêtes k-NN et benchmarks.",
        related_links=["[[PyArrow]]"],
    )
    assert mod2 is True
    # Le temps NE DOIT PAS être cumulé deux fois !
    assert note.frontmatter.total_time_invested_min == 75, "Le temps cumulé ne doit pas doubler lors d'une ré-exécution !"
    assert note.body.count("### Session du 2026-10-23") == 1, "Il ne doit y avoir qu'une seule section pour cette date !"
    assert "benchmarks" in note.body

    # 3. Troisième enrichissement identique (rejeu complet)
    mod3 = note.append_or_replace_daily_session(
        date_str="2026-10-23",
        duration_min=45,
        duration_fmt="45 min",
        enrichment_markdown="**Activités clés :** Optimisation des requêtes k-NN et benchmarks.",
    )
    assert note.frontmatter.total_time_invested_min == 75
    assert note.body.count("### Session du 2026-10-23") == 1


# ==============================================================================
# CHANTIER 2 : SÉLECTIVITÉ DU MATCHER CPU BM25
# ==============================================================================

def test_bm25_cpu_matcher_selectivity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """
    Vérifie la robustesse du matcher BM25 / IDF :
    - Rejette les correspondances basées sur des stopwords ou du vocabulaire technique générique
      ('python', 'code', 'script', 'donnees', 'analyse', 'projet').
    - Accepte avec précision les fiches partageant des mots-clés techniques distinctifs ('lancedb', 'pyarrow').
    - Exige au moins 2 termes discriminants dans (title + slug + tags).
    """
    from src.consolidators.night_consolidator import NightConsolidator

    # Création d'un mock du dossier de concepts avec 3 fiches
    concepts_dir = tmp_path / "concepts"
    concepts_dir.mkdir(parents=True, exist_ok=True)

    note_lancedb = concepts_dir / "lancedb-vector-storage-pyarrow.md"
    note_lancedb.write_text("""---
id: "202610100000"
title: "LanceDB Vector Storage & PyArrow"
semantic_topic: "IA_et_LLM_Local"
tags: ["lancedb", "pyarrow", "embeddings"]
created_at: "2026-10-10"
updated_at: "2026-10-10"
total_time_invested_min: 60
summary_1_line: "Moteur vectoriel basé sur Arrow."
---

# LanceDB Vector Storage & PyArrow
Contenu d'architecture vectorielle.
""", encoding="utf-8")

    note_generic_python = concepts_dir / "optimisation-python-script-code.md"
    note_generic_python.write_text("""---
id: "202610100001"
title: "Optimisation de Code et Scripts Python"
semantic_topic: "Dev_et_Architecture_Tech"
tags: ["python", "script", "code", "donnees"]
created_at: "2026-10-10"
updated_at: "2026-10-10"
total_time_invested_min: 40
summary_1_line: "Bonnes pratiques de scripts et optimisation de code."
---

# Optimisation de Code et Scripts Python
Généralités de code Python.
""", encoding="utf-8")

    monkeypatch.setattr(type(settings), "CONCEPTS_DIR", property(lambda self: concepts_dir))
    consolidator = NightConsolidator()

    # CAS 1 : Bruit générique -> Doit impérativement être REJETÉ (None)
    # Bien que contenant "python", "code", "script", "donnees", "optimisation"
    generic_items = [
        "Écriture de scripts Python pour l'analyse de données",
        "Optimisation du code et tests d'architecture du projet",
        "Configuration des fichiers de tests et du système",
    ]
    match_generic = consolidator._find_matching_existing_concept_cpu(
        topic_name="Dev_et_Architecture_Tech",
        topic_items=generic_items,
    )
    assert match_generic is None, f"Le bruit générique ne doit jamais matcher ! Obtenu : {match_generic}"

    # CAS 2 : Termes discriminants spécifiques -> Doit impérativement MATCHER
    specific_items = [
        "Benchmark des index vectoriels LanceDB sous Windows 11",
        "Intégration du format de table PyArrow pour la persistance locale",
    ]
    match_specific = consolidator._find_matching_existing_concept_cpu(
        topic_name="IA_et_LLM_Local",
        topic_items=specific_items,
    )
    assert match_specific is not None, "Les termes techniques discriminants (lancedb, pyarrow) doivent matcher !"
    assert match_specific.name == note_lancedb.name


# ==============================================================================
# CHANTIER 3 : DÉCOUPAGE MODULAIRE & RÉTROCOMPATIBILITÉ DES IMPORTS
# ==============================================================================

def test_modular_imports_backward_compatibility():
    """
    Vérifie que la séparation en modules spécialisés conserve une rétrocompatibilité
    stricte à 100 % sur tous les imports historiques.
    """
    # 1. Imports depuis le nouveau module takeout_parsers
    from src.ingestors.takeout_parsers import (
        ParsedTurn,
        ReconstructedSession,
        FRENCH_MONTH_MAP,
        parse_date_flexible,
        sanitize_turn_text,
        compute_realistic_session_duration_min,
        parse_gemini_html,
        parse_gemini_json,
        parse_youtube_export,
        parse_google_search_export,
        sessionize_gemini_turns,
    )
    assert ParsedTurn is not None
    assert callable(compute_realistic_session_duration_min)
    assert callable(sessionize_gemini_turns)

    # 2. Imports depuis le nouveau consolidateur vault_doctor
    from src.consolidators.vault_doctor import (
        VaultDoctor,
        ensure_strict_taxonomy_file,
        scan_and_upgrade_existing_concepts,
    )
    assert VaultDoctor is not None
    assert callable(scan_and_upgrade_existing_concepts)

    # 3. Rétrocompatibilité totale depuis takeout_ingestor
    import src.ingestors.takeout_ingestor as ti
    assert hasattr(ti, "ParsedTurn")
    assert hasattr(ti, "ReconstructedSession")
    assert hasattr(ti, "parse_date_flexible")
    assert hasattr(ti, "sanitize_turn_text")
    assert hasattr(ti, "compute_realistic_session_duration_min")
    assert hasattr(ti, "ensure_strict_taxonomy_file")
    assert hasattr(ti, "scan_and_upgrade_existing_concepts")
    assert hasattr(ti, "VaultDoctor")
    assert hasattr(ti, "save_distilled_concept_note")


# ==============================================================================
# CHANTIER 5 : ISOLATION DU DASHBOARD & REQUÊTES DBMANAGER
# ==============================================================================

def test_dashboard_import_no_streamlit_side_effects():
    """
    Vérifie que l'import de src.dashboard.app ne déclenche pas le rendu Streamlit
    hors contexte web et que les fonctions analytiques fonctionnent en lecture seule.
    """
    # L'import ne doit lever aucune exception de contexte Streamlit manquant
    import src.dashboard.app as app

    # Vérification de la présence des fonctions d'API analytiques historiques
    assert callable(app.load_macro_kpis)
    assert callable(app.load_chat_search_results)
    assert callable(app.load_messages_for_session)
    assert callable(app.load_footprints_summary)
    assert callable(app.load_top_channels_and_domains)
    assert callable(app.load_burst_clusters_summary)
    assert callable(app.search_historical_footprints)

    # Test d'exécution de load_macro_kpis via DBManager(read_only=True)
    kpis = app.load_macro_kpis()
    assert isinstance(kpis, dict)
    assert "chat_count" in kpis
    assert "total_turns" in kpis
    assert "fp_count" in kpis
