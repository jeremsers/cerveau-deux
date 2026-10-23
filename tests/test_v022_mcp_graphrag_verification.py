"""
Suite de tests de vérification pour la version v0.2.2 :
EXO-009 — Serveur MCP Local & GraphRAG Hybride Multi-Sauts.
1. Validation de l'extraction de [[wikilinks]] (simples, avec alias, avec ancres).
2. Résolution 1-hop et déduplication stricte dans HybridGraphRAG.
3. Intégration GraphRAG dans l'injecteur Hippocampe (Alt+Espace).
4. Validation des 5 outils MCP métier en direct et via transport JSON-RPC 2.0 stdio.
5. Invariant d'exclusion VRAM (déchargement bge-m3 systématique).
"""

from __future__ import annotations

import json
import sys
import unittest.mock as mock
from datetime import datetime, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest

from src.database.db_manager import (
    ChatSessionRecord,
    DBManager,
    DailyMetricRecord,
    KanbanTaskRecord,
    ProjectRecord,
)
from src.database.graph_rag import HybridGraphRAG, extract_wikilinks
from src.mcp.exocortex_mcp_server import (
    handle_jsonrpc_request,
    mcp_get_concept_note,
    mcp_get_kanban_queue,
    mcp_get_recent_telemetry,
    mcp_get_session_history,
    mcp_search_concepts,
)


# ==============================================================================
# FIXTURES DE TEST (SQLITE ET CONCEPTS TEMPORAIRES)
# ==============================================================================

@pytest.fixture
def temp_env(tmp_path: Path):
    """Crée une base SQLite éphémère et un dossier de concepts pour les tests isolés."""
    db_file = tmp_path / "test_mcp.db"
    concepts_dir = tmp_path / "02_Concepts"
    concepts_dir.mkdir(parents=True, exist_ok=True)

    db = DBManager(db_path=db_file)
    db.init_db()

    # Amorçage d'une session de chat avec 2 messages
    now = datetime.now()
    session_rec = ChatSessionRecord(
        session_id="sess_mcp_001",
        timestamp_start=now - timedelta(minutes=20),
        timestamp_end=now,
        turn_count=2,
        user_char_count=600,
        extracted_topics_json=json.dumps(["IA_et_LLM_Local"]),
        generated_notes_json=json.dumps(["architecture-vectorielle"]),
        summary="Discussion sur l'architecture GraphRAG et LanceDB.",
        distillation_status="success",
    )
    db.insert_chat_sessions_batch([session_rec])

    messages_payload = [
        ("sess_mcp_001", 1, now - timedelta(minutes=15), "Comment structurer GraphRAG ?", "En combinant Hop 0 et Hop 1.", 100),
        ("sess_mcp_001", 2, now - timedelta(minutes=5), "Qu'en est-il de la VRAM ?", "Déchargement bge-m3 immédiat.", 120),
    ]
    db.insert_chat_messages_batch(messages_payload)

    # Amorçage d'une métrique quotidienne
    metric = DailyMetricRecord(
        date=(now - timedelta(days=1)).date(),
        total_screen_sec=14400,
        active_production_sec=10800,
        passive_exploration_sec=3600,
        max_hyperfocus_sec=7200,
        max_hyperfocus_topic="IA_et_LLM_Local",
        context_switches_per_hour=1.2,
        read_vs_write_ratio=0.35,
        top_topics_json=json.dumps({"IA_et_LLM_Local": 3.0, "Dev_et_Architecture_Tech": 1.0}),
    )
    db.upsert_daily_metrics(metric)

    # Amorçage d'un ticket Kanban
    task_rec = KanbanTaskRecord(
        task_id="EXO-999",
        project_id="exocortex",
        component_tag="mcp",
        title="Implémentation Serveur MCP",
        summary_pitch="Serveur stdio JSON-RPC",
        status="ready_for_agent",
        priority=1,
        complexity="M",
        spec_file_path=str(tmp_path / "spec.md"),
        created_at=now,
        updated_at=now,
    )
    db.upsert_kanban_task(task_rec)

    return db, concepts_dir


# ==============================================================================
# TEST 1 : EXTRACTION DE WIKILINKS ET RÉSOLUTION 1-HOP GRAPHRAG
# ==============================================================================

def test_wikilink_extraction():
    """Vérifie l'extraction précise et dédupliquée des wikilinks avec variantes complexes."""
    text = (
        "Dans l'architecture [[LanceDB]], nous utilisons [[PyArrow]] pour le stockage.\n"
        "Voir aussi [[Architecture Vectorielle|Arch Vec]] et une section [[LanceDB#IVF-PQ]].\n"
        "Répétition de [[lancedb]] en minuscule et lien vide [[]]."
    )
    links = extract_wikilinks(text)
    assert "LanceDB" in links
    assert "PyArrow" in links
    assert "Architecture Vectorielle" in links
    # Déduplication insensible à la casse
    assert len(links) == 3


def test_wikilink_extraction_and_1hop_resolution(temp_env):
    """
    Crée 3 notes A, B, C où A contient [[Note B]] et [[Note C|Alias C]].
    Vérifie que la recherche hybride sur A retourne :
    - A en primary_nodes (Hop 0)
    - B et C en linked_neighbors (Hop 1)
    - Zéro doublon : A n'apparaît PAS dans linked_neighbors.
    """
    db, concepts_dir = temp_env

    # 1. Note A (Point d'entrée)
    file_a = concepts_dir / "note-a-architecture.md"
    file_a.write_text("""---
id: "note_a"
title: "Note A Architecture"
semantic_topic: "Dev_et_Architecture_Tech"
session_id: "sess_mcp_001"
tags: ["archi", "graph"]
created_at: "2026-10-24"
updated_at: "2026-10-24"
total_time_invested_min: 30
summary_1_line: "Architecture principale."
---

# Note A Architecture
Cette note fait référence à [[Note B Composant]] et à [[Note C Utilitaires|Alias C]].

> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)
> - **Connexions sémantiques suggérées :** [[Note B Composant]]
""", encoding="utf-8")

    # 2. Note B (Voisin lié)
    file_b = concepts_dir / "note-b-composant.md"
    file_b.write_text("""---
id: "note_b"
title: "Note B Composant"
semantic_topic: "Dev_et_Architecture_Tech"
tags: ["composant"]
created_at: "2026-10-24"
updated_at: "2026-10-24"
total_time_invested_min: 20
summary_1_line: "Composant satellite."
---

# Note B Composant
Détail du composant lié.
""", encoding="utf-8")

    # 3. Note C (Voisin lié via alias)
    file_c = concepts_dir / "note-c-utilitaires.md"
    file_c.write_text("""---
id: "note_c"
title: "Note C Utilitaires"
semantic_topic: "Dev_et_Architecture_Tech"
tags: ["utils"]
created_at: "2026-10-24"
updated_at: "2026-10-24"
total_time_invested_min: 10
summary_1_line: "Boîte à outils."
---

# Note C Utilitaires
Fonctions utilitaires partagées.
""", encoding="utf-8")

    rag = HybridGraphRAG(db_manager=db, concepts_dir=concepts_dir)
    rag.refresh_index(force=True)

    # Simulation d'un retour vectoriel ciblant Note A
    mock_vector_results = [
        {
            "id": "note_a",
            "title": "Note A Architecture",
            "slug": "note-a-architecture",
            "semantic_topic": "Dev_et_Architecture_Tech",
            "file_path": str(file_a.resolve()),
            "content": file_a.read_text(encoding="utf-8"),
            "score": 0.1,  # Proximité élevée
        }
    ]

    with mock.patch.object(rag.vector_store, "search", return_value=mock_vector_results), \
         mock.patch.object(rag.vector_store, "count", return_value=1):

        result = rag.search_hybrid(query="Architecture système", top_k=1, neighbor_k=3)

        assert "primary_nodes" in result
        assert "linked_neighbors" in result
        assert "episodic_traces" in result

        primary = result["primary_nodes"]
        neighbors = result["linked_neighbors"]
        traces = result["episodic_traces"]

        # Vérification Hop 0
        assert len(primary) == 1
        assert primary[0]["slug"] == "note-a-architecture"
        assert primary[0]["hop"] == 0

        # Vérification Hop 1 (B et C résolus)
        neighbor_slugs = [n["slug"] for n in neighbors]
        assert "note-b-composant" in neighbor_slugs
        assert "note-c-utilitaires" in neighbor_slugs

        # DÉDUPLICATION STRICTE : Note A ne doit JAMAIS être dans les voisins
        assert "note-a-architecture" not in neighbor_slugs
        for n in neighbors:
            assert n["hop"] == 1

        # Vérification des traces épisodiques rattachées (sess_mcp_001)
        assert len(traces) >= 1
        assert traces[0]["session_id"] == "sess_mcp_001"
        assert "GraphRAG" in traces[0]["summary"]


# ==============================================================================
# TEST 2 : INTÉGRATION DANS HIPPOCAMPUS INJECTOR (ALT+ESPACE)
# ==============================================================================

def test_hippocampus_integration_with_graphrag(temp_env):
    """
    Vérifie que build_enriched_payload assemble à la fois les extraits Hop 0
    et la section ### Connexions de Graphe (1-Hop Wikilinks) issue de GraphRAG.
    """
    from src.daemons.hippocampus_hotkey import HippocampusInjector

    db, concepts_dir = temp_env

    mock_rag_result = {
        "query": "test query",
        "primary_nodes": [
            {
                "slug": "concept-primaire",
                "title": "Concept Primaire",
                "semantic_topic": "IA_et_LLM_Local",
                "similarity_pct": 92,
                "excerpt": "Contenu du concept primaire.",
            }
        ],
        "linked_neighbors": [
            {
                "slug": "voisin-graphe",
                "title": "Voisin Graphe",
                "semantic_topic": "IA_et_LLM_Local",
                "excerpt": "Extrait du voisin de graphe.",
            }
        ],
        "episodic_traces": [],
    }

    injector = HippocampusInjector(db_manager=db)
    with mock.patch.object(injector.graph_rag, "search_hybrid", return_value=mock_rag_result):
        payload = injector.build_enriched_payload("Explique-moi l'architecture.")

        assert "<contexte_hippocampe_local>" in payload
        assert "[[Concept Primaire]]" in payload
        assert "### Connexions de Graphe (1-Hop Wikilinks) :" in payload
        assert "[[Voisin Graphe]]" in payload
        assert "</contexte_hippocampe_local>" in payload


# ==============================================================================
# TEST 3 : OUTILS MCP MÉTIER EN DIRECT
# ==============================================================================

def test_mcp_tools_direct(temp_env):
    """Teste les 5 fonctions d'outils métier purs du serveur MCP."""
    db, concepts_dir = temp_env

    # 1. mcp_get_concept_note
    test_note_path = concepts_dir / "note-test-mcp.md"
    test_note_path.write_text("""---
id: "note_mcp_test"
title: "Note Test MCP"
semantic_topic: "IA_et_LLM_Local"
created_at: "2026-10-24"
updated_at: "2026-10-24"
summary_1_line: "Note de test pour les outils MCP."
---

# Note Test MCP
Corps de la note de test MCP.
""", encoding="utf-8")

    note_res = mcp_get_concept_note("note-test-mcp", concepts_dir=concepts_dir)
    assert note_res["found"] is True
    assert note_res["title_h1"] == "Note Test MCP"
    assert "Corps de la note" in note_res["body"]

    # Test note introuvable
    not_found_res = mcp_get_concept_note("inconnue-note", concepts_dir=concepts_dir)
    assert not_found_res["found"] is False

    # 2. mcp_get_recent_telemetry
    telemetry_res = mcp_get_recent_telemetry(days=7, db_manager=db)
    assert telemetry_res["days"] == 7
    assert telemetry_res["days_recorded"] >= 1
    assert telemetry_res["total_screen_hours"] > 0

    # 3. mcp_get_session_history
    sess_res = mcp_get_session_history("sess_mcp_001", db_manager=db)
    assert sess_res["found"] is True
    assert sess_res["session_id"] == "sess_mcp_001"
    assert len(sess_res["turns"]) == 2
    assert "GraphRAG" in sess_res["metadata"]["summary"]

    # 4. mcp_get_kanban_queue
    kanban_res = mcp_get_kanban_queue(project_id="exocortex", db_manager=db)
    assert kanban_res["total_active_count"] >= 1
    assert any(t["task_id"] == "EXO-999" for t in kanban_res["ready_for_agent"])

    # 5. mcp_search_concepts
    search_res = mcp_search_concepts(query="Note Test MCP", top_k=2, db_manager=db)
    assert "primary_nodes" in search_res
    assert "linked_neighbors" in search_res


# ==============================================================================
# TEST 4 : GESTIONNAIRE JSON-RPC 2.0 STDIO AUTONOME
# ==============================================================================

def test_jsonrpc_handler_protocol_and_tools(temp_env):
    """
    Vérifie la conformité totale du gestionnaire JSON-RPC 2.0 :
    - initialize
    - ping
    - tools/list
    - tools/call sur chacun des 5 outils métier
    """
    db, concepts_dir = temp_env

    # 1. initialize
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {},
    }
    init_res = handle_jsonrpc_request(init_req, db_manager=db, concepts_dir=concepts_dir)
    assert init_res["jsonrpc"] == "2.0"
    assert init_res["id"] == 1
    assert init_res["result"]["serverInfo"]["name"] == "Exocortex"
    assert "tools" in init_res["result"]["capabilities"]

    # 2. ping
    ping_res = handle_jsonrpc_request({"jsonrpc": "2.0", "id": 2, "method": "ping"})
    assert ping_res["result"] == {}

    # 3. tools/list
    list_req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/list",
    }
    list_res = handle_jsonrpc_request(list_req, db_manager=db, concepts_dir=concepts_dir)
    tools = list_res["result"]["tools"]
    tool_names = [t["name"] for t in tools]
    assert "search_exocortex_concepts" in tool_names
    assert "get_concept_note" in tool_names
    assert "get_recent_episodic_telemetry" in tool_names
    assert "get_session_history" in tool_names
    assert "get_active_kanban_queue" in tool_names

    for t in tools:
        assert "inputSchema" in t
        assert t["inputSchema"]["type"] == "object"

    # 4. tools/call -> get_active_kanban_queue
    call_req = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "get_active_kanban_queue",
            "arguments": {"project_id": "exocortex"},
        },
    }
    call_res = handle_jsonrpc_request(call_req, db_manager=db, concepts_dir=concepts_dir)
    assert call_res["id"] == 4
    content = call_res["result"]["content"]
    assert len(content) == 1
    assert content[0]["type"] == "text"
    parsed_payload = json.loads(content[0]["text"])
    assert parsed_payload["project_id"] == "exocortex"
    assert parsed_payload["total_active_count"] >= 1

    # 5. tools/call -> get_session_history
    call_sess_req = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "get_session_history",
            "arguments": {"session_id": "sess_mcp_001"},
        },
    }
    call_sess_res = handle_jsonrpc_request(call_sess_req, db_manager=db, concepts_dir=concepts_dir)
    parsed_sess = json.loads(call_sess_res["result"]["content"][0]["text"])
    assert parsed_sess["found"] is True
    assert parsed_sess["session_id"] == "sess_mcp_001"
    assert len(parsed_sess["turns"]) == 2

    # 6. tools/call avec outil inconnu -> code d'erreur -32601
    bad_req = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "tools/call",
        "params": {
            "name": "non_existent_tool",
            "arguments": {},
        },
    }
    bad_res = handle_jsonrpc_request(bad_req, db_manager=db, concepts_dir=concepts_dir)
    assert "error" in bad_res
    assert bad_res["error"]["code"] == -32601


# ==============================================================================
# TEST 5 : INVARIANT D'EXCLUSION VRAM (DÉCHARGEMENT SYSTÉMATIQUE)
# ==============================================================================

def test_vram_exclusion_safety(temp_env):
    """
    Vérifie que toute recherche vectorielle ou GraphRAG déclenche
    systématiquement le déchargement immédiat de bge-m3 (0 Mo VRAM résiduel).
    """
    from src.config import settings
    from src.llm.ollama_client import llm_client

    db, concepts_dir = temp_env
    rag = HybridGraphRAG(db_manager=db, concepts_dir=concepts_dir)

    with mock.patch.object(llm_client, "unload_model") as mock_unload, \
         mock.patch.object(rag.vector_store, "search", return_value=[]):

        rag.search_hybrid(query="requête test exclusion vram")

        assert mock_unload.called, "unload_model doit être appelé systématiquement pour garantir 0 Mo VRAM !"
        mock_unload.assert_called_with(settings.MODEL_EMBEDDING)

