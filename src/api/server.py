"""
Serveur API REST FastAPI & Command Center Web Exocortex (v0.5.0 - EXO-014).
Fournit les points de terminaison pour la télémétrie cognitive, le GraphRAG hybride,
le studio Kanban SOTA et l'orchestration système.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.config import AUTHORIZED_SEMANTIC_TOPICS, normalize_to_macro_topic, settings
from src.consolidators.drive_compiler import DriveCompiler
from src.consolidators.kanban_engine import _slugify, kanban_engine
from src.consolidators.night_consolidator import NightConsolidator
from src.database.db_manager import DBManager, ProjectRecord
from src.database.graph_rag import HybridGraphRAG, extract_wikilinks
from src.llm.ollama_client import HardwareProbe, llm_client
from src.utils.markdown_io import parse_concept_file

logger = logging.getLogger("Exocortex.API")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


# ==============================================================================
# MODÈLES PYDANTIC POUR LES REQUÊTES
# ==============================================================================

class ProjectCreateRequest(BaseModel):
    project_id: str = Field(..., description="Slug unique du projet (ex: homelab-media)")
    name: str = Field(..., description="Nom complet d'affichage")
    prefix: str = Field(..., description="Préfixe des identifiants de tickets (ex: HLAB)")
    repo_path: Optional[str] = Field(None, description="Chemin absolu vers le dépôt local")
    description: Optional[str] = Field("", description="Description architecturale du projet")


class TaskCreateRequest(BaseModel):
    project_id: str = Field("exocortex", description="Identifiant du projet parent")
    title: str = Field(..., description="Titre concis de la tâche ou de l'idée")
    component_tag: Optional[str] = Field("general", description="Sous-module ou composant")
    summary_pitch: Optional[str] = Field("", description="Expression du besoin ou pitch")
    priority: Optional[int] = Field(2, ge=1, le=4, description="Priorité (1=urgent, 4=optionnel)")
    complexity: Optional[str] = Field("M", description="Complexité estimée (S, M, L, XL)")
    initial_status: Optional[str] = Field("radar", description="Statut initial")


class TaskStatusUpdateRequest(BaseModel):
    status: str = Field(..., description="Nouveau statut Kanban")


class SpecIngestRequest(BaseModel):
    raw_markdown: str = Field(..., description="Contenu Markdown de la spécification")
    target_task_id: Optional[str] = Field(None, description="Task ID ciblé (optionnel)")


# ==============================================================================
# APPLICATION FASTAPI
# ==============================================================================

app = FastAPI(
    title="Exocortex Cognitive Command Center API",
    version="0.5.0",
    description="API REST unifiée pour l'Exocortex, la télémétrie cognitive, le GraphRAG et le Kanban SOTA.",
)

# Configuration CORS pour dev local et UI intégrées
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_read_db() -> DBManager:
    return DBManager(read_only=True)


# ==============================================================================
# 1. SYSTÈME, VRAM & PROACTIVITÉ
# ==============================================================================

@app.get("/api/system/status")
def get_system_status() -> Dict[str, Any]:
    """Retourne la VRAM live, le statut d'Ollama, le bootloader et l'état du DriftGuard."""
    free_gb, total_gb = HardwareProbe.get_vram_info()
    used_gb = round(max(0.0, total_gb - free_gb), 2)
    alive = llm_client.is_alive()

    # Chargement Bootloader
    bootloader_content = ""
    if settings.BOOTLOADER_PATH.exists():
        try:
            bootloader_content = settings.BOOTLOADER_PATH.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            logger.warning("Échec lecture bootloader : %s", exc)

    # Chargement Drift state
    drift_state: Dict[str, Any] = {"drift_detected": False, "mode": "STABLE"}
    if settings.DRIFT_STATE_PATH.exists():
        try:
            drift_state = json.loads(settings.DRIFT_STATE_PATH.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("Échec lecture drift_state : %s", exc)

    return {
        "vram": {
            "free_gb": free_gb,
            "total_gb": total_gb,
            "used_gb": used_gb,
        },
        "ollama_alive": alive,
        "bootloader_content": bootloader_content,
        "drift_state": drift_state,
    }


@app.post("/api/system/trigger-consolidate")
def trigger_consolidate(background_tasks: BackgroundTasks) -> Dict[str, str]:
    """Déclenche la consolidation nocturne en arrière-plan."""
    def _run() -> None:
        try:
            NightConsolidator().consolidate()
        except Exception as exc:
            logger.error("Erreur lors de la consolidation en arrière-plan : %s", exc)

    background_tasks.add_task(_run)
    return {
        "status": "triggered",
        "message": "Consolidation nocturne démarrée en tâche de fond.",
    }


@app.post("/api/system/trigger-drive-compile")
def trigger_drive_compile() -> Dict[str, Any]:
    """Déclenche la compilation des méga-documents Google Drive."""
    try:
        compiler = DriveCompiler()
        files = compiler.compile_all()
        return {
            "status": "success",
            "files": files,
        }
    except Exception as exc:
        logger.error("Échec compilation Google Drive : %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


# ==============================================================================
# 2. TÉLÉMÉTRIE & ANALYTIQUE (READ-ONLY)
# ==============================================================================

@app.get("/api/telemetry/kpis")
def get_telemetry_kpis() -> Dict[str, Any]:
    """Retourne les métriques macro consolidées de l'activité cognitive."""
    return _get_read_db().fetch_macro_kpis()


@app.get("/api/telemetry/dates")
def get_telemetry_dates() -> List[str]:
    """Retourne la liste des dates (YYYY-MM-DD) disposant de données de télémétrie."""
    return _get_read_db().fetch_all_activity_dates()


@app.get("/api/telemetry/timeline")
def get_telemetry_timeline(date_str: Optional[str] = Query(None, alias="date")) -> Dict[str, Any]:
    """Retourne les événements de télémétrie, tunnels d'hyperfocus et métriques journalières pour une date donnée."""
    db = _get_read_db()
    if not date_str:
        all_dates = db.fetch_all_activity_dates()
        target_str = all_dates[0] if all_dates else date.today().isoformat()
    else:
        try:
            # Valide le format de date
            _ = date.fromisoformat(date_str)
            target_str = date_str
        except ValueError:
            raise HTTPException(status_code=400, detail="Format de date invalide (attendu: YYYY-MM-DD)")

    events = db.fetch_timeline_for_date(target_str)

    # Récupération ou calcul des métriques journalières
    daily_metric: Dict[str, Any] = {}
    with db.get_ro_connection() as conn:
        cur = conn.execute("SELECT * FROM daily_metrics WHERE date = ?;", (target_str,))
        row = cur.fetchone()
        if row:
            daily_metric = dict(row)

    # Extraction des tunnels d'hyperfocus (durée >= 30 min / 1800 s)
    focus_tunnels: List[Dict[str, Any]] = []
    for ev in events:
        dur = ev.get("duration_sec") or 0
        if dur >= 1800:
            focus_tunnels.append({
                "start_time": ev.get("timestamp_start"),
                "end_time": ev.get("timestamp_end"),
                "duration_sec": dur,
                "executable": ev.get("executable"),
                "top_window_title": ev.get("window_title"),
            })

    if not daily_metric:
        total_active = sum(e.get("duration_sec") or 0 for e in events)
        total_deep = sum(e.get("duration_sec") or 0 for e in events if e.get("cognitive_mode") == "Deep_Work")
        chat_turns = 0
        with db.get_ro_connection() as conn:
            cur = conn.execute("SELECT SUM(turn_count) FROM chat_sessions WHERE DATE(timestamp_start) = ?;", (target_str,))
            r = cur.fetchone()
            if r and r[0]:
                chat_turns = r[0]

        daily_metric = {
            "total_active_sec": total_active,
            "total_deep_work_sec": total_deep,
            "hyperfocus_tunnel_count": len(focus_tunnels),
            "total_chat_turns": chat_turns,
        }

    return {
        "date": target_str,
        "events": events,
        "daily_metric": daily_metric,
        "focus_tunnels": focus_tunnels,
    }


@app.get("/api/telemetry/treemap")
def get_telemetry_treemap() -> List[Dict[str, Any]]:
    """Retourne les données d'agrégation hiérarchique pour le Treemap cognitif."""
    return _get_read_db().fetch_treemap_data()


@app.get("/api/telemetry/archaeology")
def get_telemetry_archaeology() -> Dict[str, Any]:
    """Retourne les sessions archéologiques et calcule les archétypes cognitifs."""
    db = _get_read_db()
    sessions = db.fetch_archaeology_sessions()
    if not sessions:
        return {
            "total_sessions": 0,
            "archetypes": [],
            "monthly_series": [],
            "topics": [],
        }

    now_dt = datetime.now()
    topic_sessions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    monthly_agg: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for s in sessions:
        top = s["topic"]
        topic_sessions[top].append(s)
        ts = s["timestamp"]
        dt = now_dt
        if isinstance(ts, str):
            try:
                dt = datetime.fromisoformat(ts)
            except Exception:
                pass
        elif isinstance(ts, datetime):
            dt = ts
        ym = dt.strftime("%Y-%m")
        monthly_agg[ym][top] += 1

    archetypes_list: List[Dict[str, Any]] = []
    for top, s_list in topic_sessions.items():
        dt_list = []
        for s in s_list:
            ts = s["timestamp"]
            cur_dt = now_dt
            if isinstance(ts, str):
                try:
                    cur_dt = datetime.fromisoformat(ts)
                except Exception:
                    pass
            elif isinstance(ts, datetime):
                cur_dt = ts
            dt_list.append(cur_dt)

        min_d = min(dt_list)
        max_d = max(dt_list)
        span_days = max(1, (max_d - min_d).days)
        count = len(s_list)
        total_chars = sum(s.get("chars", 0) for s in s_list)
        recency_days = (now_dt - max_d).days

        if span_days > 180 and count >= 15:
            archetype = "🏛️ Pilier Fondamental"
        elif span_days < 45 and count >= 5:
            archetype = "⚡ Passion Éphémère (Burst)"
        elif recency_days < 30 and span_days < 60:
            archetype = "🌱 Sujet Émergent"
        else:
            archetype = "🔄 Intérêt Intermittent"

        archetypes_list.append({
            "topic": top,
            "archetype": archetype,
            "session_count": count,
            "first_focus": min_d.strftime("%Y-%m-%d"),
            "last_focus": max_d.strftime("%Y-%m-%d"),
            "span_days": span_days,
            "total_chars": int(total_chars),
        })

    archetypes_list.sort(key=lambda x: x["session_count"], reverse=True)

    all_months = sorted(monthly_agg.keys())
    all_topics = sorted(topic_sessions.keys())
    monthly_series: List[Dict[str, Any]] = []
    for m in all_months:
        row: Dict[str, Any] = {"month": m}
        for t in all_topics:
            row[t] = monthly_agg[m].get(t, 0)
        monthly_series.append(row)

    return {
        "total_sessions": len(sessions),
        "archetypes": archetypes_list,
        "monthly_series": monthly_series,
        "topics": all_topics,
    }


@app.get("/api/telemetry/circadian")
def get_telemetry_circadian() -> Dict[str, Any]:
    """Retourne la matrice 7j x 24h et les quadrants horaires pour l'analyse circadienne."""
    db = _get_read_db()
    timestamps = db.fetch_circadian_timestamps()
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    # Matrice 7 x 24
    matrix: List[List[int]] = [[0 for _ in range(24)] for _ in range(7)]
    quadrants = {
        "Nuit Profonde (00h - 06h)": 0,
        "Matinée (06h - 12h)": 0,
        "Après-Midi (12h - 18h)": 0,
        "Soirée & Crépuscule (18h - 00h)": 0,
    }

    for ts_str in timestamps:
        try:
            # Traite format ISO classique ou avec espace
            clean_ts = ts_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean_ts)
        except Exception:
            continue

        weekday = dt.weekday()  # Lundi = 0, Dimanche = 6
        hour = dt.hour
        matrix[weekday][hour] += 1

        if 0 <= hour < 6:
            quadrants["Nuit Profonde (00h - 06h)"] += 1
        elif 6 <= hour < 12:
            quadrants["Matinée (06h - 12h)"] += 1
        elif 12 <= hour < 18:
            quadrants["Après-Midi (12h - 18h)"] += 1
        else:
            quadrants["Soirée & Crépuscule (18h - 00h)"] += 1

    return {
        "days": days,
        "hours": list(range(24)),
        "matrix": matrix,
        "quadrants": quadrants,
        "total_events": len(timestamps),
    }


# ==============================================================================
# 3. EXPLORATEUR ÉPISTÉMIQUE & EMPREINTES
# ==============================================================================

@app.get("/api/epistemic/chats")
def search_chats(
    q: str = Query("", description="Terme de recherche full-text"),
    topic: Optional[str] = Query(None, description="Filtre par sujet sémantique"),
    status: Optional[str] = Query(None, description="Filtre par statut de distillation"),
    limit: int = Query(50, ge=1, le=200, description="Nombre maximum de sessions"),
) -> List[Dict[str, Any]]:
    """Recherche full-text dans les sessions et messages Gemini."""
    db = _get_read_db()
    return db.search_chat_sessions(
        query=q,
        topic_filter=topic,
        status_filter=status,
        limit=limit,
    )


@app.get("/api/epistemic/chats/{session_id}/messages")
def get_chat_messages(session_id: str) -> List[Dict[str, Any]]:
    """Retourne la liste ordonnée des messages d'une session de chat."""
    db = _get_read_db()
    return db.fetch_messages_for_session(session_id)


@app.get("/api/epistemic/footprints/summary")
def get_footprints_summary() -> Dict[str, Any]:
    """Retourne les métriques globales, top chaînes/domaines et burst clusters."""
    db = _get_read_db()
    kpis = db.fetch_footprints_summary()
    top15 = db.fetch_top_channels_and_domains(limit=15)
    bursts = db.fetch_burst_clusters_summary(limit=25)
    return {
        "kpis": kpis,
        "top_channels_and_domains": top15,
        "burst_clusters": bursts,
    }


@app.get("/api/epistemic/footprints/search")
def search_footprints(
    q: str = Query("", description="Recherche textuelle dans le titre ou domaine"),
    source: Optional[str] = Query("Toutes", description="Filtre par source ('youtube', 'google_search', 'Toutes')"),
    clustered: bool = Query(False, description="Filtrer uniquement les empreintes en burst clusters"),
    linked: bool = Query(False, description="Filtrer uniquement les empreintes liées à Gemini"),
    limit: int = Query(100, ge=1, le=500, description="Nombre de résultats maximum"),
) -> List[Dict[str, Any]]:
    """Recherche dynamique dans les empreintes numériques."""
    db = _get_read_db()
    return db.search_footprints(
        query=q,
        source_filter=source or "Toutes",
        only_clustered=clustered,
        only_linked=linked,
        limit=limit,
    )


# ==============================================================================
# 4. GRAPHRAG HYBRIDE & CONCEPTS OBSIDIAN
# ==============================================================================

@app.get("/api/graphrag/search")
def search_graphrag(
    q: str = Query(..., description="Requête sémantique ou conceptuelle"),
    top_k: int = Query(5, ge=1, le=20, description="Nombre de nœuds Hop 0"),
    neighbor_k: int = Query(3, ge=1, le=10, description="Nombre de voisins Hop 1"),
    topic: Optional[str] = Query(None, description="Filtre par topic sémantique"),
) -> Dict[str, Any]:
    """
    Exécute la recherche GraphRAG hybride multi-sauts et formate les nœuds et arêtes
    pour la visualisation de graphe interactive.
    """
    rag = HybridGraphRAG()
    results = rag.search_hybrid(
        query=q,
        top_k=top_k,
        neighbor_k=neighbor_k,
        topic_filter=topic,
    )

    primary_nodes = results.get("primary_nodes", [])
    linked_neighbors = results.get("linked_neighbors", [])
    episodic_traces = results.get("episodic_traces", [])

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    seen_node_ids = set()

    for p in primary_nodes:
        nid = p["slug"]
        if nid not in seen_node_ids:
            seen_node_ids.add(nid)
            nodes.append({
                "id": nid,
                "label": p["title"],
                "type": "primary",
                "hop": 0,
                "topic": p["semantic_topic"],
                "similarity_pct": p.get("similarity_pct", 100),
                "file_path": p.get("file_path", ""),
                "excerpt": p.get("excerpt", ""),
            })

    for nb in linked_neighbors:
        nid = nb["slug"]
        if nid not in seen_node_ids:
            seen_node_ids.add(nid)
            nodes.append({
                "id": nid,
                "label": nb["title"],
                "type": "neighbor",
                "hop": 1,
                "topic": nb["semantic_topic"],
                "score": round(float(nb.get("score", 0.0)), 2),
                "file_path": nb.get("file_path", ""),
                "excerpt": nb.get("excerpt", ""),
            })

    # Construction des arêtes à partir des wikilinks réels
    for p in primary_nodes:
        p_slug = p["slug"]
        p_fpath = Path(p.get("file_path", ""))
        if p_fpath.exists():
            try:
                parsed = parse_concept_file(p_fpath)
                wikilinks = extract_wikilinks(parsed.body + "\n" + "\n".join(parsed.telemetry_lines))
                for target in wikilinks:
                    target_slug = _slugify(target)
                    for n in nodes:
                        if n["id"] == target_slug or n["label"].strip().lower() == target.strip().lower():
                            if p_slug != n["id"]:
                                edges.append({
                                    "source": p_slug,
                                    "target": n["id"],
                                    "relation": "wikilink",
                                })
            except Exception:
                pass

    # Si aucune arête trouvée, lier les voisins au premier nœud primaire
    if not edges and primary_nodes and linked_neighbors:
        hub = primary_nodes[0]["slug"]
        for nb in linked_neighbors:
            if hub != nb["slug"]:
                edges.append({
                    "source": hub,
                    "target": nb["slug"],
                    "relation": "wikilink",
                })

    return {
        "query": q,
        "primary_nodes": primary_nodes,
        "linked_neighbors": linked_neighbors,
        "episodic_traces": episodic_traces,
        "nodes": nodes,
        "edges": edges,
    }


@app.get("/api/concepts/{slug}")
def get_concept_by_slug(slug: str) -> Dict[str, Any]:
    """Lit et parse une fiche conceptuelle du coffre Obsidian 02_Concepts/."""
    clean_slug = slug[:-3] if slug.endswith(".md") else slug
    target_path = settings.CONCEPTS_DIR / f"{clean_slug}.md"

    if not target_path.exists():
        # Recherche insensible à la casse
        found: Optional[Path] = None
        target_lower = f"{clean_slug.lower()}.md"
        for p in settings.CONCEPTS_DIR.glob("*.md"):
            if p.name.lower() == target_lower:
                found = p
                break
        if not found:
            raise HTTPException(status_code=404, detail=f"Fiche conceptuelle '{slug}' introuvable.")
        target_path = found

    try:
        parsed = parse_concept_file(target_path)
        raw_md = target_path.read_text(encoding="utf-8", errors="replace")
        return {
            "slug": target_path.stem,
            "title": parsed.title_h1 or parsed.frontmatter.title,
            "frontmatter": parsed.frontmatter.model_dump(),
            "body": parsed.body,
            "telemetry_lines": parsed.telemetry_lines,
            "raw_markdown": raw_md,
        }
    except Exception as exc:
        logger.error("Erreur lors de la lecture du concept %s : %s", target_path, exc)
        raise HTTPException(status_code=500, detail=f"Erreur de lecture : {exc}")


# ==============================================================================
# 5. KANBAN EXÉCUTIF & STUDIO SOTA (KanbanEngine)
# ==============================================================================

@app.get("/api/kanban/projects")
def get_kanban_projects() -> List[Dict[str, Any]]:
    """Retourne la liste des projets configurés dans le Kanban."""
    projects = kanban_engine.db.get_projects()
    if not projects:
        return [{"project_id": "exocortex", "name": "Exocortex & Télémétrie Cognitive", "prefix": "EXO"}]
    return projects


@app.post("/api/kanban/projects")
def create_kanban_project(req: ProjectCreateRequest) -> Dict[str, Any]:
    """Crée ou met à jour un projet Kanban."""
    record = ProjectRecord(
        project_id=req.project_id.strip().lower(),
        name=req.name.strip(),
        prefix=req.prefix.strip().upper(),
        repo_path=req.repo_path.strip() if req.repo_path else None,
        description=req.description.strip() if req.description else "",
    )
    kanban_engine.db.upsert_project(record)
    saved = kanban_engine.db.get_project_by_id(record.project_id)
    return saved or {}


@app.get("/api/kanban/tasks")
def get_kanban_tasks(
    project_id: Optional[str] = Query("exocortex", description="ID du projet filtré"),
    tag: Optional[str] = Query(None, description="Sous-module / composant"),
    q: Optional[str] = Query(None, description="Recherche textuelle dans les tickets"),
) -> List[Dict[str, Any]]:
    """Retourne la liste filtrée des tâches Kanban."""
    tasks = kanban_engine.db.get_kanban_tasks(project_id=project_id)
    if tag and tag != "Tous":
        tasks = [t for t in tasks if t.get("component_tag") == tag]
    if q and q.strip():
        q_low = q.strip().lower()
        tasks = [
            t for t in tasks
            if q_low in t["title"].lower()
            or q_low in t.get("summary_pitch", "").lower()
            or q_low in t["task_id"].lower()
        ]
    return tasks


@app.post("/api/kanban/tasks")
def create_kanban_task(req: TaskCreateRequest) -> Dict[str, Any]:
    """Crée une nouvelle tâche Kanban et met à jour AGENT_QUEUE.md."""
    task_id = kanban_engine.create_task(
        project_id=req.project_id,
        title=req.title,
        component_tag=req.component_tag or "general",
        summary_pitch=req.summary_pitch or "",
        priority=req.priority or 2,
        complexity=req.complexity or "M",
        initial_status=req.initial_status or "radar",
    )
    task = kanban_engine.db.get_kanban_task_by_id(task_id)
    return task or {}


@app.patch("/api/kanban/tasks/{task_id}/status")
def update_kanban_task_status(task_id: str, req: TaskStatusUpdateRequest) -> Dict[str, Any]:
    """Met à jour le statut d'une tâche Kanban et recompile le manifeste."""
    task = kanban_engine.db.get_kanban_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Tâche '{task_id}' introuvable.")

    kanban_engine.db.update_kanban_task_status(task_id=task_id, new_status=req.status)
    kanban_engine.compile_agent_queue_manifest()
    updated = kanban_engine.db.get_kanban_task_by_id(task_id)
    return updated or {}


@app.delete("/api/kanban/tasks/{task_id}")
def delete_kanban_task(task_id: str) -> Dict[str, Any]:
    """Supprime une tâche Kanban et actualise le manifeste."""
    task = kanban_engine.db.get_kanban_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Tâche '{task_id}' introuvable.")

    kanban_engine.db.delete_kanban_task(task_id)
    kanban_engine.compile_agent_queue_manifest()
    return {"status": "deleted", "task_id": task_id}


@app.get("/api/kanban/tasks/{task_id}/context-pack")
def get_task_context_pack(task_id: str) -> Dict[str, Any]:
    """Génère le prompt Context-Pack haute-fidélité pour Gemini Web App."""
    try:
        prompt = kanban_engine.build_sota_context_pack_prompt(task_id)
        return {
            "task_id": task_id,
            "prompt": prompt,
        }
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.get("/api/kanban/tasks/{task_id}/coder-prompt")
def get_task_coder_prompt(
    task_id: str,
    mark_in_progress: bool = Query(False, description="Bascule automatiquement le ticket en 'in_progress'"),
) -> Dict[str, Any]:
    """Extrait chirurgicalement le prompt codeur et bascule optionnellement le statut."""
    task = kanban_engine.db.get_kanban_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Tâche '{task_id}' introuvable.")

    prompt = kanban_engine.extract_coder_prompt_from_spec(task_id)
    if mark_in_progress and task.get("status") != "in_progress":
        kanban_engine.db.update_kanban_task_status(task_id=task_id, new_status="in_progress")
        kanban_engine.compile_agent_queue_manifest()
        task = kanban_engine.db.get_kanban_task_by_id(task_id) or task

    return {
        "task_id": task_id,
        "prompt": prompt,
        "status": task.get("status"),
    }


@app.post("/api/kanban/specs/ingest")
def ingest_kanban_spec(req: SpecIngestRequest) -> Dict[str, Any]:
    """Ingère une spécification Markdown brute et l'attache à une tâche Kanban."""
    try:
        updated_task = kanban_engine.attach_spec_to_task(
            raw_markdown=req.raw_markdown,
            target_task_id=req.target_task_id,
        )
        return updated_task
    except Exception as exc:
        logger.error("Erreur ingestion spec : %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


# ==============================================================================
# 6. SERVEUR DE FICHIERS STATIQUES WEB COMMAND CENTER
# ==============================================================================

web_gui_dir = _PROJECT_ROOT / "src" / "web_gui"
if not web_gui_dir.exists():
    web_gui_dir.mkdir(parents=True, exist_ok=True)

# Monter l'interface Web moderne sur GET / (après toutes les routes /api)
app.mount("/", StaticFiles(directory=str(web_gui_dir), html=True), name="web_gui")
