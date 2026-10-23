"""
Serveur MCP (Model Context Protocol) local stdio pour l'Exocortex et la Télémétrie Cognitive.
Expose les 5 outils d'interrogation de contexte pour les agents codeurs et clients LLM :
1. search_exocortex_concepts (ou mcp_search_concepts)
2. get_concept_note (ou mcp_get_concept_note)
3. get_recent_episodic_telemetry (ou mcp_get_recent_telemetry)
4. get_session_history (ou mcp_get_session_history)
5. get_active_kanban_queue (ou mcp_get_kanban_queue)

Garantit :
- 0 Mo VRAM permanente (déchargement bge-m3 immédiat).
- Pureté totale du flux stdio : AUCUN log ni print sur sys.stdout (réservé au transport JSON-RPC 2.0).
- Fallback autonome JSON-RPC 2.0 stdio complet si la bibliothèque externe 'mcp' n'est pas installée.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# Configuration impérative de logging UNIQUEMENT sur stderr
logger = logging.getLogger("Exocortex.MCPServer")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

from src.config import settings
from src.database.db_manager import DBManager
from src.database.graph_rag import HybridGraphRAG
from src.utils.markdown_io import parse_concept_file


# ==============================================================================
# 5 FONCTIONS D'OUTILS MÉTIER PURES
# ==============================================================================

def mcp_search_concepts(
    query: str,
    topic: Optional[str] = None,
    top_k: int = 5,
    include_graph_neighbors: bool = True,
    db_manager: Optional[DBManager] = None,
) -> Dict[str, Any]:
    """
    Recherche des notes conceptuelles via HybridGraphRAG :
    - Hop 0 : Recherche vectorielle LanceDB k-NN.
    - Hop 1 : Traversée des liens [[wikilinks]] d'Obsidian (si include_graph_neighbors=True).
    - Traces épisodiques rattachées issues de SQLite.
    """
    db = db_manager or DBManager(read_only=True)
    rag = HybridGraphRAG(db_manager=db)
    neighbor_limit = top_k if include_graph_neighbors else 0
    return rag.search_hybrid(
        query=query,
        top_k=top_k,
        neighbor_k=neighbor_limit,
        topic_filter=topic,
    )


def mcp_get_concept_note(
    slug_or_title: str,
    concepts_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Lit et retourne l'intégralité du contenu, du frontmatter et de la télémétrie
    d'une note conceptuelle du coffre Obsidian.
    """
    target_dir = concepts_dir or settings.CONCEPTS_DIR
    rag = HybridGraphRAG(concepts_dir=target_dir)
    resolved_path = rag.resolve_wikilink_to_path(slug_or_title)

    if not resolved_path or not resolved_path.exists():
        return {
            "found": False,
            "error": f"Fiche conceptuelle '{slug_or_title}' introuvable dans {target_dir}.",
        }

    try:
        note = parse_concept_file(resolved_path)
        return {
            "found": True,
            "slug": resolved_path.stem,
            "file_path": str(resolved_path.resolve()),
            "frontmatter": note.frontmatter.model_dump(),
            "title_h1": note.title_h1,
            "body": note.body,
            "telemetry_lines": note.telemetry_lines,
        }
    except Exception as exc:
        logger.error("Erreur lecture note %s : %s", resolved_path.name, exc)
        return {
            "found": False,
            "error": f"Erreur lors du parsing de la note '{resolved_path.name}' : {exc}",
        }


def mcp_get_recent_telemetry(
    days: int = 7,
    db_manager: Optional[DBManager] = None,
) -> Dict[str, Any]:
    """
    Retourne la télémétrie cognitive des N derniers jours :
    - Métriques d'écran quotidiennes (temps actif, hyperfocus, switches).
    - Distribution temporelle par topic sémantique.
    """
    db = db_manager or DBManager(read_only=True)
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    daily_metrics_list: List[Dict[str, Any]] = []
    with db.get_ro_connection() as conn:
        cursor = conn.execute(
            """
            SELECT date, total_screen_sec, active_production_sec, passive_exploration_sec,
                   max_hyperfocus_sec, max_hyperfocus_topic, context_switches_per_hour,
                   read_vs_write_ratio, top_topics_json
            FROM daily_metrics
            WHERE date >= ?
            ORDER BY date DESC;
            """,
            (cutoff_date,),
        )
        for row in cursor.fetchall():
            try:
                top_topics = json.loads(row["top_topics_json"])
            except Exception:
                top_topics = {}

            daily_metrics_list.append({
                "date": str(row["date"]),
                "total_screen_hours": round(row["total_screen_sec"] / 3600.0, 2),
                "active_prod_hours": round(row["active_production_sec"] / 3600.0, 2),
                "passive_expl_hours": round(row["passive_exploration_sec"] / 3600.0, 2),
                "max_hyperfocus_hours": round(row["max_hyperfocus_sec"] / 3600.0, 2),
                "max_hyperfocus_topic": row["max_hyperfocus_topic"],
                "context_switches_per_hour": round(row["context_switches_per_hour"], 2),
                "read_vs_write_ratio": round(row["read_vs_write_ratio"], 2),
                "top_topics": top_topics,
            })

    total_screen_h = sum(m["total_screen_hours"] for m in daily_metrics_list)
    total_active_h = sum(m["active_prod_hours"] for m in daily_metrics_list)

    return {
        "days": days,
        "from_date": cutoff_date,
        "days_recorded": len(daily_metrics_list),
        "total_screen_hours": round(total_screen_h, 2),
        "total_active_hours": round(total_active_h, 2),
        "metrics": daily_metrics_list,
    }


def mcp_get_session_history(
    session_id: str,
    db_manager: Optional[DBManager] = None,
) -> Dict[str, Any]:
    """
    Retourne les métadonnées et la transcription complète des échanges (chat_messages)
    pour une session Gemini donnée.
    """
    db = db_manager or DBManager(read_only=True)
    session_meta = db.get_chat_session_by_id(session_id)
    if not session_meta:
        return {
            "found": False,
            "error": f"Session Gemini '{session_id}' introuvable dans la base SQLite.",
        }

    messages = db.fetch_messages_for_session(session_id)
    return {
        "found": True,
        "session_id": session_id,
        "metadata": {
            "timestamp_start": str(session_meta.get("timestamp_start", "")),
            "timestamp_end": str(session_meta.get("timestamp_end", "")),
            "turn_count": session_meta.get("turn_count", 0),
            "user_char_count": session_meta.get("user_char_count", 0),
            "summary": session_meta.get("summary", ""),
            "distillation_status": session_meta.get("distillation_status", "success"),
            "extracted_topics": session_meta.get("extracted_topics_json", "[]"),
        },
        "turns": messages,
    }


def mcp_get_kanban_queue(
    project_id: str = "exocortex",
    db_manager: Optional[DBManager] = None,
) -> Dict[str, Any]:
    """
    Retourne la file d'attente d'exécution Kanban :
    - Tâches prêtes pour l'agent (ready_for_agent)
    - Tâches en cours (in_progress)
    - Tâches en attente de spécification (needs_spec)
    """
    db = db_manager or DBManager(read_only=True)
    tasks = db.get_kanban_tasks(
        project_id=project_id,
        statuses=["ready_for_agent", "in_progress", "needs_spec", "radar"],
    )

    ready = [t for t in tasks if t.get("status") == "ready_for_agent"]
    in_prog = [t for t in tasks if t.get("status") == "in_progress"]
    needs_sp = [t for t in tasks if t.get("status") == "needs_spec"]
    radar = [t for t in tasks if t.get("status") == "radar"]

    return {
        "project_id": project_id,
        "total_active_count": len(tasks),
        "ready_for_agent_count": len(ready),
        "in_progress_count": len(in_prog),
        "ready_for_agent": ready,
        "in_progress": in_prog,
        "needs_spec": needs_sp,
        "radar": radar,
    }


# Alias pour conformité aux spécifications fonctionnelles
search_exocortex_concepts = mcp_search_concepts
get_concept_note = mcp_get_concept_note
get_recent_episodic_telemetry = mcp_get_recent_telemetry
get_session_history = mcp_get_session_history
get_active_kanban_queue = mcp_get_kanban_queue


# ==============================================================================
# SCHÉMAS DES OUTILS MCP POUR JSON-RPC tools/list
# ==============================================================================

MCP_TOOLS_SPEC = [
    {
        "name": "search_exocortex_concepts",
        "description": "Recherche sémantique vectorielle k-NN et traversée de graphe 1-hop Obsidian dans la base de connaissances Exocortex.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Expression de recherche, question technique ou concept à explorer",
                },
                "topic": {
                    "type": "string",
                    "description": "Filtre optionnel sur une macro-catégorie sémantique (ex: Dev_et_Architecture_Tech, IA_et_LLM_Local)",
                },
                "top_k": {
                    "type": "integer",
                    "description": "Nombre de nœuds primaires k-NN à retourner (défaut: 5)",
                    "default": 5,
                },
                "include_graph_neighbors": {
                    "type": "boolean",
                    "description": "Si vrai, traverse et retourne les notes voisines liées par [[wikilinks]] (Hop 1)",
                    "default": True,
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_concept_note",
        "description": "Lit et retourne le contenu complet (frontmatter, Markdown, télémétrie) d'une fiche conceptuelle par son titre ou slug.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug_or_title": {
                    "type": "string",
                    "description": "Slug de fichier ou titre exact de la fiche conceptuelle",
                },
            },
            "required": ["slug_or_title"],
        },
    },
    {
        "name": "get_recent_episodic_telemetry",
        "description": "Extrait le journal d'activité cognitive et les métriques de travail sur les N derniers jours (temps actif, hyperfocus, switches).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "description": "Nombre de jours d'historique à analyser (défaut: 7)",
                    "default": 7,
                },
            },
        },
    },
    {
        "name": "get_session_history",
        "description": "Récupère les métadonnées et la liste exhaustive de tous les échanges (prompts et réponses) d'une session Gemini archivée.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Identifiant unique de la session Gemini",
                },
            },
            "required": ["session_id"],
        },
    },
    {
        "name": "get_active_kanban_queue",
        "description": "Consulte la file d'attente d'orchestration Kanban de l'Exocortex pour identifier les prochaines tâches prêtes pour l'agent.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Identifiant du projet (défaut: exocortex)",
                    "default": "exocortex",
                },
            },
        },
    },
]


# ==============================================================================
# GESTIONNAIRE JSON-RPC 2.0 AUTONOME (FALLBACK SANS DÉPENDANCE MCP)
# ==============================================================================

def handle_jsonrpc_request(
    request: Dict[str, Any],
    db_manager: Optional[DBManager] = None,
    concepts_dir: Optional[Path] = None,
) -> Optional[Dict[str, Any]]:
    """
    Traite une requête JSON-RPC 2.0 unitaire conforme au standard Model Context Protocol.
    Prend en charge : initialize, ping, notifications/initialized, tools/list, tools/call.
    Retourne un dictionnaire de réponse JSON-RPC 2.0 ou None pour les notifications.
    """
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params") or {}

    # 1. Traitement des notifications (aucune réponse requise si req_id est None)
    if method == "notifications/initialized":
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": False,
                    },
                },
                "serverInfo": {
                    "name": "Exocortex",
                    "version": "0.2.2",
                },
            },
        }

    if method == "ping":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {},
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": MCP_TOOLS_SPEC,
            },
        }

    if method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments") or {}

        try:
            if tool_name in ("search_exocortex_concepts", "mcp_search_concepts"):
                tool_result = mcp_search_concepts(
                    query=arguments.get("query", ""),
                    topic=arguments.get("topic"),
                    top_k=int(arguments.get("top_k", 5)),
                    include_graph_neighbors=bool(arguments.get("include_graph_neighbors", True)),
                    db_manager=db_manager,
                )
            elif tool_name in ("get_concept_note", "mcp_get_concept_note"):
                tool_result = mcp_get_concept_note(
                    slug_or_title=arguments.get("slug_or_title", ""),
                    concepts_dir=concepts_dir,
                )
            elif tool_name in ("get_recent_episodic_telemetry", "mcp_get_recent_telemetry"):
                tool_result = mcp_get_recent_telemetry(
                    days=int(arguments.get("days", 7)),
                    db_manager=db_manager,
                )
            elif tool_name in ("get_session_history", "mcp_get_session_history"):
                tool_result = mcp_get_session_history(
                    session_id=arguments.get("session_id", ""),
                    db_manager=db_manager,
                )
            elif tool_name in ("get_active_kanban_queue", "mcp_get_kanban_queue"):
                tool_result = mcp_get_kanban_queue(
                    project_id=arguments.get("project_id", "exocortex"),
                    db_manager=db_manager,
                )
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Outil MCP inconnu : '{tool_name}'",
                    },
                }

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(tool_result, ensure_ascii=False, indent=2),
                        }
                    ],
                },
            }
        except Exception as exc:
            logger.error("Erreur lors de l'appel de l'outil %s : %s", tool_name, exc, exc_info=True)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32603,
                    "message": f"Erreur interne lors de l'exécution de '{tool_name}' : {exc}",
                },
            }

    # Méthode non gérée
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": -32601,
            "message": f"Méthode JSON-RPC non supportée : '{method}'",
        },
    }


def run_mcp_stdio_server(
    db_manager: Optional[DBManager] = None,
    concepts_dir: Optional[Path] = None,
) -> None:
    """
    Boucle principale du serveur MCP sur stdio.
    Lit les requêtes JSON-RPC 2.0 ligne par ligne sur sys.stdin et écrit
    exclusivement les réponses sur sys.stdout, tout en garantissant 0 print/log parasite.
    """
    logger.info("Démarrage du Serveur MCP Exocortex v0.2.2 sur stdio...")

    # Vérification et initialisation de FastMCP si disponible
    try:
        from mcp.server.fastmcp import FastMCP  # type: ignore

        mcp_app = FastMCP("Exocortex")

        @mcp_app.tool()
        def search_concepts_tool(query: str, topic: Optional[str] = None, top_k: int = 5, include_graph_neighbors: bool = True) -> str:
            res = mcp_search_concepts(query, topic, top_k, include_graph_neighbors, db_manager)
            return json.dumps(res, ensure_ascii=False, indent=2)

        @mcp_app.tool()
        def get_concept_note_tool(slug_or_title: str) -> str:
            res = mcp_get_concept_note(slug_or_title, concepts_dir)
            return json.dumps(res, ensure_ascii=False, indent=2)

        @mcp_app.tool()
        def get_recent_telemetry_tool(days: int = 7) -> str:
            res = mcp_get_recent_telemetry(days, db_manager)
            return json.dumps(res, ensure_ascii=False, indent=2)

        @mcp_app.tool()
        def get_session_history_tool(session_id: str) -> str:
            res = mcp_get_session_history(session_id, db_manager)
            return json.dumps(res, ensure_ascii=False, indent=2)

        @mcp_app.tool()
        def get_active_kanban_queue_tool(project_id: str = "exocortex") -> str:
            res = mcp_get_kanban_queue(project_id, db_manager)
            return json.dumps(res, ensure_ascii=False, indent=2)

        logger.info("Bibliothèque officielle 'mcp' détectée : exécution via FastMCP.")
        mcp_app.run(transport="stdio")
        return
    except ImportError:
        logger.info("Bibliothèque 'mcp' non installée : activation du moteur autonome JSON-RPC 2.0 stdio.")

    # Boucle de transport JSON-RPC native autonome
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break  # Fin de flux (client fermé)

            clean_line = line.strip()
            if not clean_line:
                continue

            # Support basique du cadrage Content-Length si envoyé
            if clean_line.lower().startswith("content-length:"):
                # Lecture de la ligne vide séparatrice
                sys.stdin.readline()
                length = int(clean_line.split(":", 1)[1].strip())
                body_raw = sys.stdin.read(length)
                request_data = json.loads(body_raw)
            else:
                request_data = json.loads(clean_line)

            response = handle_jsonrpc_request(request_data, db_manager=db_manager, concepts_dir=concepts_dir)
            if response is not None:
                encoded = json.dumps(response, ensure_ascii=False)
                sys.stdout.write(encoded + "\n")
                sys.stdout.flush()
        except (KeyboardInterrupt, SystemExit):
            break
        except Exception as exc:
            logger.error("Erreur de boucle stdio MCP : %s", exc, exc_info=True)


if __name__ == "__main__":
    run_mcp_stdio_server()

