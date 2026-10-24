"""
Suite de tests de vérification pour la version v0.3.0 :
EXO-010 — Proactivité Exécutive, Context Bootloader & Garde-Fou Rabbit Hole.
1. Génération du Context Bootloader (00_BOOTLOADER_DEMAIN.md) et fallback hors-ligne.
2. Extraction et injection dédupliquée des Open Loops en statut 'radar' dans le Kanban.
3. Garde-fou temps réel DriftGuard (zapping/hyper_fragmentation et dérive passive media_hole).
4. Cooldown strict de 60 minutes entre les alertes attentionnelles.
5. Intégration dans le Dashboard Streamlit.
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

from src.config import settings
from src.consolidators.night_consolidator import (
    ExecutiveBootloaderSchema,
    NightConsolidator,
    OpenLoopItem,
)
from src.daemons.telemetry_daemon import DriftGuard
from src.database.db_manager import (
    DailyMetricRecord,
    DBManager,
    KanbanTaskRecord,
    RawActivityRecord,
)


# ==============================================================================
# FIXTURES DE TEST
# ==============================================================================

@pytest.fixture
def v030_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Prépare un environnement isolé avec base SQLite, coffre Obsidian et buffers."""
    vault_root = tmp_path / "Vault_Data"
    meta_dir = vault_root / "00_Meta"
    concepts_dir = vault_root / "02_Concepts"
    specs_dir = vault_root / "03_Kanban_Specs"
    buffer_dir = vault_root / "_System_Buffer"

    for d in [meta_dir, concepts_dir, specs_dir, buffer_dir]:
        d.mkdir(parents=True, exist_ok=True)

    db_file = buffer_dir / "telemetry.db"
    db = DBManager(db_path=db_file)
    db.init_db()

    # Redirection dynamique de settings
    monkeypatch.setattr(settings, "VAULT_ROOT", vault_root)
    monkeypatch.setattr(type(settings), "META_DIR", property(lambda self: meta_dir))
    monkeypatch.setattr(type(settings), "CONCEPTS_DIR", property(lambda self: concepts_dir))
    monkeypatch.setattr(type(settings), "KANBAN_SPECS_DIR", property(lambda self: specs_dir))
    monkeypatch.setattr(type(settings), "SYSTEM_BUFFER_DIR", property(lambda self: buffer_dir))
    monkeypatch.setattr(type(settings), "BOOTLOADER_PATH", property(lambda self: meta_dir / "00_BOOTLOADER_DEMAIN.md"))
    monkeypatch.setattr(type(settings), "DRIFT_STATE_PATH", property(lambda self: buffer_dir / "drift_state.json"))

    return db, vault_root, meta_dir, concepts_dir, buffer_dir


# ==============================================================================
# TEST 1 : GÉNÉRATION DU CONTEXT BOOTLOADER ET OPEN LOOPS VERS KANBAN
# ==============================================================================

def test_bootloader_generation_and_open_loops_to_kanban(v030_env):
    """
    Vérifie que generate_executive_bootloader :
    - Produit 00_BOOTLOADER_DEMAIN.md avec dernier état, checklist et fiches actives.
    - Injecte les Open Loops en statut 'radar' dans kanban_tasks.
    - Applique une déduplication stricte lors d'une seconde exécution (idempotence).
    """
    db, vault_root, meta_dir, concepts_dir, buffer_dir = v030_env

    target_date = date(2026, 10, 24)
    now = datetime(2026, 10, 24, 18, 30, 0)

    # 1. Amorçage de données d'activité dans SQLite
    act1 = RawActivityRecord(
        timestamp_start=now - timedelta(minutes=45),
        timestamp_end=now - timedelta(minutes=20),
        duration_sec=1500,
        executable="code.exe",
        window_title="graph_rag.py - cerveau-deux",
        active_input=True,
        input_intensity=0.85,
        semantic_topic="Dev_et_Architecture_Tech",
        cognitive_mode="production",
        processed=True,
    )
    act2 = RawActivityRecord(
        timestamp_start=now - timedelta(minutes=20),
        timestamp_end=now,
        duration_sec=1200,
        executable="code.exe",
        window_title="exocortex_mcp_server.py - cerveau-deux",
        active_input=True,
        input_intensity=0.75,
        semantic_topic="Dev_et_Architecture_Tech",
        cognitive_mode="production",
        processed=True,
    )
    db.insert_raw_activities_batch([act1, act2])

    # 2. Amorçage d'une fiche conceptuelle active du jour
    note_path = concepts_dir / "serveur-mcp-graphrag.md"
    note_path.write_text("""---
id: "concept_mcp"
title: "Serveur MCP & GraphRAG"
semantic_topic: "Dev_et_Architecture_Tech"
created_at: "2026-10-24"
updated_at: "2026-10-24"
total_time_invested_min: 45
summary_1_line: "Architecture serveur MCP et GraphRAG."
---

# Serveur MCP & GraphRAG
Détail de l'architecture.
""", encoding="utf-8")

    # 3. Métrique quotidienne
    metric = DailyMetricRecord(
        date=target_date,
        total_screen_sec=10800,
        active_production_sec=8000,
        passive_exploration_sec=2800,
        max_hyperfocus_sec=3600,
        max_hyperfocus_topic="Dev_et_Architecture_Tech",
        context_switches_per_hour=1.5,
        read_vs_write_ratio=0.35,
        top_topics_json=json.dumps({"Dev_et_Architecture_Tech": 8000}),
    )

    consolidator = NightConsolidator(db_manager=db)

    # Mock du retour LLM structuré
    mock_llm_response = ExecutiveBootloaderSchema(
        last_active_state="Arrêt sur l'implémentation du protocole stdio dans exocortex_mcp_server.py.",
        immediate_next_steps=[
            "Tester la commande JSON-RPC tools/list sur sys.stdin",
            "Vérifier le déchargement immédiat de bge-m3",
            "Ajouter l'option CLI --mcp-server dans run_exocortex.py",
        ],
        detected_open_loops=[
            OpenLoopItem(
                title="Support du transport SSE pour Cursor",
                component_tag="mcp",
                summary_pitch="Étudier la faisabilité d'un transport SSE en local pour Cursor.",
                priority=2,
                complexity="M",
            ),
            OpenLoopItem(
                title="Optimisation indexation IVF-PQ LanceDB",
                component_tag="database",
                summary_pitch="Créer l'index IVF-PQ à partir de 256 fiches.",
                priority=3,
                complexity="S",
            ),
        ],
    )

    from src.llm.ollama_client import llm_client
    with mock.patch.object(llm_client, "is_alive", return_value=True), \
         mock.patch.object(llm_client, "generate_structured", return_value=mock_llm_response):

        bootloader_path = consolidator.generate_executive_bootloader(
            target_date=target_date,
            metric=metric,
            effective_model="gemma4:26b-a4b",
        )

        assert bootloader_path.exists()
        content = bootloader_path.read_text(encoding="utf-8")

        # Vérification de la structure du fichier
        assert "# 🚀 Context Bootloader" in content
        assert "exocortex_mcp_server.py" in content
        assert "- [ ] Tester la commande JSON-RPC tools/list" in content
        assert "[[Serveur MCP & GraphRAG]]" in content

        # Vérification de l'injection dans le Kanban en statut 'radar'
        tasks = consolidator.db.get_kanban_tasks(project_id="exocortex", statuses=["radar"])
        titles = [t["title"] for t in tasks]
        assert "Support du transport SSE pour Cursor" in titles
        assert "Optimisation indexation IVF-PQ LanceDB" in titles

        # 4. TEST D'IDEMPOTENCE STRICTE (Rejeu) : aucun doublon ne doit être créé
        consolidator.generate_executive_bootloader(
            target_date=target_date,
            metric=metric,
            effective_model="gemma4:26b-a4b",
        )
        tasks_after = consolidator.db.get_kanban_tasks(project_id="exocortex", statuses=["radar"])
        assert len(tasks_after) == len(tasks), "L'injection d'Open Loops doit être strictement idempotente !"


def test_bootloader_offline_fallback(v030_env):
    """Vérifie le repli déterministe propre du Bootloader si Ollama est hors-ligne."""
    db, vault_root, meta_dir, concepts_dir, buffer_dir = v030_env

    target_date = date(2026, 10, 24)
    metric = DailyMetricRecord(
        date=target_date,
        total_screen_sec=7200,
        active_production_sec=5000,
        passive_exploration_sec=2200,
        max_hyperfocus_sec=2400,
        max_hyperfocus_topic="HomeLab_et_Hardware",
        context_switches_per_hour=1.0,
        read_vs_write_ratio=0.4,
        top_topics_json="{}",
    )

    consolidator = NightConsolidator(db_manager=db)

    from src.llm.ollama_client import llm_client
    with mock.patch.object(llm_client, "is_alive", return_value=False):
        bootloader_path = consolidator.generate_executive_bootloader(
            target_date=target_date,
            metric=metric,
            effective_model="gemma4:12b",
        )

        assert bootloader_path.exists()
        content = bootloader_path.read_text(encoding="utf-8")
        assert "# 🚀 Context Bootloader" in content
        assert "- [ ]" in content


# ==============================================================================
# TEST 2 : GARDE-FOU TEMPS RÉEL (DRIFTGUARD - ZAPPING & DÉRIVE PASSIVE)
# ==============================================================================

def test_drift_guard_zapping_and_passive_detection(tmp_path: Path):
    """
    Vérifie les deux règles du DriftGuard :
    1. hyper_fragmentation : >= 25 switches en 30 min avec durée moyenne < 45s.
    2. unplanned_media_hole : >= 90 min de média passif sans saisie active.
    3. Cooldown de 60 minutes entre alertes.
    """
    state_file = tmp_path / "drift_state.json"
    guard = DriftGuard(
        state_path=state_file,
        max_switches_30min=25,
        max_passive_min=90,
        cooldown_min=60,
    )

    now = datetime(2026, 10, 24, 15, 0, 0)

    # --------------------------------------------------------------------------
    # Cas 1 : Simulation de zapping intense (30 switches rapides en 10 minutes)
    # --------------------------------------------------------------------------
    alert = None
    for i in range(30):
        t = now + timedelta(seconds=i * 20)
        res = guard.record_switch(
            timestamp=t,
            executable="chrome.exe" if i % 2 == 0 else "code.exe",
            window_title=f"Page de recherche ou fichier {i}",
            duration_sec=15,  # < 45s
            input_intensity=0.5,
        )
        if res:
            alert = res

    assert alert is not None, "Une alerte de zapping aurait dû se déclencher !"
    assert alert["active_alert"] is True
    assert alert["drift_type"] == "hyper_fragmentation"
    assert "Dispersion attentionnelle" in alert["diagnostic"]
    assert state_file.exists()

    state_json = json.loads(state_file.read_text(encoding="utf-8"))
    assert state_json["drift_type"] == "hyper_fragmentation"

    # --------------------------------------------------------------------------
    # Cas 2 : Vérification du cooldown de 60 minutes
    # --------------------------------------------------------------------------
    subsequent_res = guard.record_switch(
        timestamp=now + timedelta(minutes=15),
        executable="chrome.exe",
        window_title="Zapping supplémentaire pendant le cooldown",
        duration_sec=10,
        input_intensity=0.5,
    )
    assert subsequent_res is None, "Aucune nouvelle alerte ne doit être émise pendant le cooldown !"

    # --------------------------------------------------------------------------
    # Cas 3 : Simulation de dérive passive média (95 minutes sur YouTube sans input)
    # --------------------------------------------------------------------------
    media_state_file = tmp_path / "media_drift_state.json"
    media_guard = DriftGuard(
        state_path=media_state_file,
        max_switches_30min=25,
        max_passive_min=90,
        cooldown_min=60,
    )

    media_alert = None
    # Spec v0.3.0 (rétablie en v0.5.6, audit E3) : la dérive média suit un tunnel de production
    media_guard.record_switch(
        timestamp=now - timedelta(minutes=1),
        executable="code.exe",
        window_title="night_consolidator.py - Visual Studio Code",
        duration_sec=45 * 60,
        input_intensity=0.8,
    )
    # 10 blocs de 10 minutes sur YouTube avec input_intensity = 0.05 (< 0.15)
    for i in range(10):
        t = now + timedelta(minutes=i * 10)
        res = media_guard.record_switch(
            timestamp=t,
            executable="chrome.exe",
            window_title="Documentaire long - YouTube",
            duration_sec=600,
            input_intensity=0.05,
        )
        if res:
            media_alert = res

    assert media_alert is not None, "Une alerte de trou média passif aurait dû se déclencher !"
    assert media_alert["drift_type"] == "unplanned_media_hole"
    assert media_state_file.exists()
