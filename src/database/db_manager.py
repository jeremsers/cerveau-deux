"""
Couche de persistance SQLite pour le système 'Exocortex & Télémétrie Cognitive'.
Configure le moteur SQLite en mode WAL, initialise les 4 tables relationnelles
et fournit des méthodes optimisées d'insertion et d'analyse par lots.
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, Union

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pydantic import BaseModel, Field

from src.config import normalize_to_macro_topic, settings


# ==============================================================================
# MODÈLES PYDANTIC V2 POUR LES ENREGISTREMENTS SQLITE
# ==============================================================================

class RawActivityRecord(BaseModel):
    """Représente une tranche d'activité brute capturée sur l'OS Win32."""
    id: Optional[int] = None
    timestamp_start: datetime
    timestamp_end: datetime
    duration_sec: int
    executable: str
    window_title: str
    url_or_path: Optional[str] = None
    ocr_snippet: Optional[str] = None
    screenshot_path: Optional[str] = None
    active_input: bool = True
    input_intensity: float = 0.0
    semantic_topic: Optional[str] = None
    cognitive_mode: Optional[str] = None
    processed: bool = False


class DailyMetricRecord(BaseModel):
    """Représente le bilan cognitif et d'attention agrégé d'une journée."""
    date: date
    total_screen_sec: int
    active_production_sec: int
    passive_exploration_sec: int
    max_hyperfocus_sec: int
    max_hyperfocus_topic: Optional[str] = None
    context_switches_per_hour: float
    read_vs_write_ratio: float
    top_topics_json: str  # Dict serialisé en JSON : {"topic": secondes}


class ChatSessionRecord(BaseModel):
    """Représente une session de conversation IA (Gemini Takeout ou future)."""
    session_id: str
    timestamp_start: datetime
    timestamp_end: datetime
    turn_count: int
    user_char_count: int
    extracted_topics_json: str = "[]"
    generated_notes_json: str = "[]"
    summary: str = ""
    distillation_status: str = "pending"


class ChatMessageRecord(BaseModel):
    """Représente un message/tour individuel dans une session de chat."""
    id: Optional[int] = None
    session_id: str
    turn_index: int
    timestamp: datetime
    user_prompt: str
    ai_response: str
    user_char_count: int


class HistoricalFootprintRecord(BaseModel):
    """Représente une empreinte de recherche Google ou de visionnage YouTube."""
    id: Optional[int] = None
    source: str  # 'youtube' | 'google_search'
    timestamp: datetime
    title_or_query: str
    url: Optional[str] = None
    channel_or_domain: Optional[str] = None
    cluster_id: Optional[str] = None
    semantic_topic: Optional[str] = None
    linked_gemini_session_id: Optional[str] = None


class ProjectRecord(BaseModel):
    """Projet suivi dans le Kanban Exocortex (1 Projet = 1 Vue)."""
    project_id: str
    name: str
    prefix: str
    repo_path: Optional[str] = None
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.now)


class KanbanTaskRecord(BaseModel):
    """Tâche ou idée du Kanban exécutif."""
    task_id: str
    project_id: str
    component_tag: str = "general"
    title: str
    summary_pitch: str = ""
    status: str = "radar"  # 'radar', 'needs_spec', 'ready_for_agent', 'in_progress', 'done', 'icebox'
    priority: int = 2      # 1 (Urgent), 2 (Normal), 3 (Secondaire), 4 (Optionnel)
    complexity: str = "M"  # 'S', 'M', 'L', 'XL'
    spec_file_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ==============================================================================
# GESTIONNAIRE DE BASE DE DONNÉES SQLITE
# ==============================================================================

class DBManager:
    """Gestionnaire de persistance SQLite thread-safe configuré en mode WAL haute performance."""

    def __init__(self, db_path: Optional[Path] = None, read_only: bool = False) -> None:
        self.db_path = db_path or settings.DB_PATH
        self.read_only = read_only
        if not self.read_only:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.init_db()

    @contextmanager
    def get_ro_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Fournit une connexion SQLite sécurisée en lecture seule stricte (mode=ro)."""
        uri = f"{self.db_path.resolve().as_uri()}?mode=ro"
        conn = sqlite3.connect(
            uri,
            uri=True,
            timeout=15.0,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA busy_timeout=5000;")
            yield conn
        finally:
            conn.close()

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Fournit une connexion SQLite configurée avec WAL, timeouts et row_factory."""
        if self.read_only:
            with self.get_ro_connection() as conn:
                yield conn
            return

        conn = sqlite3.connect(
            str(self.db_path),
            timeout=10.0,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        conn.row_factory = sqlite3.Row
        try:
            # Optimisations PRAGMA
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA busy_timeout=5000;")
            conn.execute("PRAGMA foreign_keys=ON;")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_db(self) -> None:
        """Crée l'intégralité des 4 tables et des index si non existants."""
        with self.get_connection() as conn:
            # 1. Table raw_activity
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS raw_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp_start DATETIME NOT NULL,
                    timestamp_end DATETIME NOT NULL,
                    duration_sec INTEGER NOT NULL,
                    executable TEXT NOT NULL,
                    window_title TEXT NOT NULL,
                    url_or_path TEXT,
                    ocr_snippet TEXT,
                    screenshot_path TEXT,
                    active_input BOOLEAN DEFAULT 1,
                    input_intensity REAL DEFAULT 0.0,
                    semantic_topic TEXT,
                    cognitive_mode TEXT,
                    processed BOOLEAN DEFAULT 0
                );
                """
            )
            # Migration automatique si la table existait sans la colonne screenshot_path
            cursor = conn.execute("PRAGMA table_info(raw_activity);")
            columns = [row[1] for row in cursor.fetchall()]
            if "screenshot_path" not in columns:
                conn.execute("ALTER TABLE raw_activity ADD COLUMN screenshot_path TEXT;")

            conn.execute("CREATE INDEX IF NOT EXISTS idx_raw_ts ON raw_activity(timestamp_start);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_raw_topic ON raw_activity(semantic_topic);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_raw_processed ON raw_activity(processed);")

            # 2. Table daily_metrics
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_metrics (
                    date DATE PRIMARY KEY,
                    total_screen_sec INTEGER NOT NULL,
                    active_production_sec INTEGER NOT NULL,
                    passive_exploration_sec INTEGER NOT NULL,
                    max_hyperfocus_sec INTEGER NOT NULL,
                    max_hyperfocus_topic TEXT,
                    context_switches_per_hour REAL NOT NULL,
                    read_vs_write_ratio REAL NOT NULL,
                    top_topics_json TEXT NOT NULL
                );
                """
            )

            # 3. Table chat_sessions
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    session_id TEXT PRIMARY KEY,
                    timestamp_start DATETIME NOT NULL,
                    timestamp_end DATETIME NOT NULL,
                    turn_count INTEGER NOT NULL,
                    user_char_count INTEGER NOT NULL,
                    extracted_topics_json TEXT NOT NULL,
                    generated_notes_json TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    distillation_status TEXT DEFAULT 'pending'
                );
                """
            )
            # Migration automatique si la table existait sans la colonne distillation_status
            cursor_cs = conn.execute("PRAGMA table_info(chat_sessions);")
            cs_columns = [row[1] for row in cursor_cs.fetchall()]
            if "distillation_status" not in cs_columns:
                conn.execute("ALTER TABLE chat_sessions ADD COLUMN distillation_status TEXT DEFAULT 'pending';")

            conn.execute("CREATE INDEX IF NOT EXISTS idx_chat_date ON chat_sessions(timestamp_start);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_chat_status ON chat_sessions(distillation_status);")

            # 3b. Table chat_messages (Granularité fine des échanges Takeout / LLM)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    turn_index INTEGER NOT NULL,
                    timestamp DATETIME NOT NULL,
                    user_prompt TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    user_char_count INTEGER NOT NULL,
                    UNIQUE(session_id, turn_index)
                );
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_msg_session ON chat_messages(session_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_msg_ts ON chat_messages(timestamp);")

            # 4. Table historical_footprints
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS historical_footprints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    title_or_query TEXT NOT NULL,
                    url TEXT,
                    channel_or_domain TEXT,
                    cluster_id TEXT,
                    semantic_topic TEXT,
                    linked_gemini_session_id TEXT
                );
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_hist_ts ON historical_footprints(timestamp);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_hist_session ON historical_footprints(linked_gemini_session_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_hist_cluster ON historical_footprints(cluster_id);")

            # Déduplication et contrainte d'unicité v0.1.3
            conn.execute(
                """
                DELETE FROM historical_footprints
                WHERE id NOT IN (
                    SELECT MIN(id) FROM historical_footprints
                    GROUP BY source, timestamp, title_or_query
                );
                """
            )
            conn.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_footprint
                ON historical_footprints(source, timestamp, title_or_query);
                """
            )

            # Nettoyage des micro-sessions bruitées de chat_sessions (v0.1.3)
            conn.execute(
                """
                DELETE FROM chat_sessions
                WHERE turn_count < 3 OR user_char_count < 250;
                """
            )

            # 5. Tables Kanban & Multi-Projets (v0.2.0 - Module 7)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS projects (
                    project_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    prefix TEXT NOT NULL,
                    repo_path TEXT,
                    description TEXT NOT NULL,
                    created_at DATETIME NOT NULL
                );
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS kanban_tasks (
                    task_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    component_tag TEXT NOT NULL DEFAULT 'general',
                    title TEXT NOT NULL,
                    summary_pitch TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'radar',
                    priority INTEGER NOT NULL DEFAULT 2,
                    complexity TEXT NOT NULL DEFAULT 'M',
                    spec_file_path TEXT,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE
                );
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kanban_proj_status ON kanban_tasks(project_id, status);")

            # Amorçage idempotent du projet exocortex
            conn.execute(
                """
                INSERT OR IGNORE INTO projects (project_id, name, prefix, repo_path, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    "exocortex",
                    "Exocortex & Télémétrie Cognitive",
                    "EXO",
                    str(_PROJECT_ROOT),
                    "Second cerveau automatisé Obsidian, démon Win32, consolidation nocturne bi-modèle, LanceDB et Dashboard Streamlit.",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )

    # ==========================================================================
    # INSERTIONS PAR LOTS (BATCH OPERATIONS)
    # ==========================================================================

    def insert_chat_sessions_batch(self, sessions: List[ChatSessionRecord]) -> int:
        """Insère ou remplace un lot de sessions Gemini dans chat_sessions."""
        if not sessions:
            return 0
        sql = """
            INSERT OR REPLACE INTO chat_sessions (
                session_id, timestamp_start, timestamp_end, turn_count,
                user_char_count, extracted_topics_json, generated_notes_json, summary,
                distillation_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        payload = [
            (
                s.session_id,
                s.timestamp_start.strftime("%Y-%m-%d %H:%M:%S"),
                s.timestamp_end.strftime("%Y-%m-%d %H:%M:%S"),
                s.turn_count,
                s.user_char_count,
                s.extracted_topics_json,
                s.generated_notes_json,
                s.summary,
                s.distillation_status,
            )
            for s in sessions
        ]
        with self.get_connection() as conn:
            conn.executemany(sql, payload)
        return len(sessions)

    def update_session_distillation_metadata(
        self,
        session_id: str,
        topics_list: List[str],
        notes_list: List[str],
        summary: Optional[str] = None,
        distillation_status: str = "success",
    ) -> bool:
        """
        Met à jour les métadonnées de distillation post-LLM d'une session Gemini :
        topics extraits, fiches conceptuelles générées, résumé et statut de distillation.
        """
        topics_json = json.dumps(topics_list, ensure_ascii=False)
        notes_json = json.dumps(notes_list, ensure_ascii=False)

        with self.get_connection() as conn:
            if summary:
                conn.execute(
                    """
                    UPDATE chat_sessions
                    SET extracted_topics_json = ?, generated_notes_json = ?, summary = ?, distillation_status = ?
                    WHERE session_id = ?;
                    """,
                    (topics_json, notes_json, summary, distillation_status, session_id),
                )
            else:
                conn.execute(
                    """
                    UPDATE chat_sessions
                    SET extracted_topics_json = ?, generated_notes_json = ?, distillation_status = ?
                    WHERE session_id = ?;
                    """,
                    (topics_json, notes_json, distillation_status, session_id),
                )
        return True

    def insert_chat_messages_batch(
        self,
        messages: List[Union[ChatMessageRecord, Tuple[str, int, Union[datetime, str], str, str, int], Dict[str, Any]]],
    ) -> int:
        """Insère ou remplace un lot de messages/tours de conversation dans chat_messages."""
        if not messages:
            return 0
        sql = """
            INSERT OR REPLACE INTO chat_messages (
                session_id, turn_index, timestamp, user_prompt, ai_response, user_char_count
            ) VALUES (?, ?, ?, ?, ?, ?);
        """
        payload = []
        for m in messages:
            if isinstance(m, ChatMessageRecord):
                ts = m.timestamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(m.timestamp, datetime) else str(m.timestamp)
                payload.append((m.session_id, m.turn_index, ts, m.user_prompt, m.ai_response, m.user_char_count))
            elif isinstance(m, tuple):
                ts = m[2].strftime("%Y-%m-%d %H:%M:%S") if isinstance(m[2], datetime) else str(m[2])
                payload.append((m[0], m[1], ts, m[3], m[4], m[5]))
            elif isinstance(m, dict):
                ts_val = m["timestamp"]
                ts = ts_val.strftime("%Y-%m-%d %H:%M:%S") if isinstance(ts_val, datetime) else str(ts_val)
                payload.append((m["session_id"], m["turn_index"], ts, m["user_prompt"], m["ai_response"], m["user_char_count"]))
        with self.get_connection() as conn:
            conn.executemany(sql, payload)
        return len(payload)

    def upsert_live_chat_turn(
        self,
        platform: str,
        session_id: str,
        user_prompt: str,
        ai_response: str,
        timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Insère ou met à jour de façon idempotente un tour de conversation capturé en direct
        par le récepteur d'extension navigateur (v0.3.5 / EXO-011).

        Déduplique sur le couple (session_id, user_prompt) :
        - Si un message avec le même user_prompt existe déjà dans la session, met à jour
          la réponse IA si elle a évolué, sans incrémenter turn_count.
        - Sinon, ajoute le nouveau tour (turn_index = len(messages)) et incrémente turn_count
          dans chat_sessions.
        """
        now_dt = timestamp or datetime.now()
        ts_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")

        clean_prompt = user_prompt.strip()
        clean_response = ai_response.strip()
        u_chars = len(clean_prompt)

        with self.get_connection() as conn:
            # 1. Vérifier si la session existe
            cur_sess = conn.execute(
                "SELECT session_id, turn_count, user_char_count FROM chat_sessions WHERE session_id = ?;",
                (session_id,),
            )
            sess_row = cur_sess.fetchone()

            # 2. Récupérer les messages existants pour cette session
            cur_msgs = conn.execute(
                "SELECT turn_index, user_prompt, ai_response FROM chat_messages WHERE session_id = ? ORDER BY turn_index ASC;",
                (session_id,),
            )
            existing_msgs = cur_msgs.fetchall()

            # 3. Déduplication par prompt
            for row in existing_msgs:
                t_idx, existing_prompt, existing_ai = row[0], row[1], row[2]
                if existing_prompt.strip() == clean_prompt:
                    if existing_ai.strip() != clean_response and clean_response:
                        conn.execute(
                            "UPDATE chat_messages SET ai_response = ? WHERE session_id = ? AND turn_index = ?;",
                            (clean_response, session_id, t_idx),
                        )
                        conn.execute(
                            "UPDATE chat_sessions SET timestamp_end = ? WHERE session_id = ?;",
                            (ts_str, session_id),
                        )
                        return {
                            "session_id": session_id,
                            "turn_index": t_idx,
                            "status": "updated",
                            "is_new": False,
                        }
                    return {
                        "session_id": session_id,
                        "turn_index": t_idx,
                        "status": "duplicate",
                        "is_new": False,
                    }

            # 4. Nouveau tour de conversation
            new_turn_index = len(existing_msgs)
            conn.execute(
                """
                INSERT INTO chat_messages (
                    session_id, turn_index, timestamp, user_prompt, ai_response, user_char_count
                ) VALUES (?, ?, ?, ?, ?, ?);
                """,
                (session_id, new_turn_index, ts_str, clean_prompt, clean_response, u_chars),
            )

            # 5. Création ou mise à jour de la session parent
            if not sess_row:
                initial_summary = clean_prompt[:140]
                conn.execute(
                    """
                    INSERT INTO chat_sessions (
                        session_id, timestamp_start, timestamp_end, turn_count,
                        user_char_count, extracted_topics_json, generated_notes_json,
                        summary, distillation_status
                    ) VALUES (?, ?, ?, 1, ?, '[]', '[]', ?, 'pending');
                    """,
                    (session_id, ts_str, ts_str, u_chars, initial_summary),
                )
            else:
                conn.execute(
                    """
                    UPDATE chat_sessions
                    SET timestamp_end = ?,
                        turn_count = turn_count + 1,
                        user_char_count = user_char_count + ?
                    WHERE session_id = ?;
                    """,
                    (ts_str, u_chars, session_id),
                )

        return {
            "session_id": session_id,
            "turn_index": new_turn_index,
            "status": "created",
            "is_new": True,
        }

    def get_completed_session_ids_from_db(self) -> Set[str]:
        """Retourne l'ensemble des session_id déjà traitées avec succès ou bruit consolidé."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT session_id FROM chat_sessions
                WHERE distillation_status IN ('success', 'misc_noise');
                """
            )
            return {row[0] for row in cursor.fetchall()}

    def insert_historical_footprints_batch(self, footprints: List[HistoricalFootprintRecord]) -> int:
        """Insère un lot d'empreintes Search/YouTube dans historical_footprints avec déduplication native."""
        if not footprints:
            return 0
        sql = """
            INSERT OR IGNORE INTO historical_footprints (
                source, timestamp, title_or_query, url, channel_or_domain,
                cluster_id, semantic_topic, linked_gemini_session_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        payload = [
            (
                f.source,
                f.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                f.title_or_query,
                f.url,
                f.channel_or_domain,
                f.cluster_id,
                f.semantic_topic,
                f.linked_gemini_session_id,
            )
            for f in footprints
        ]
        with self.get_connection() as conn:
            conn.executemany(sql, payload)
        return len(footprints)

    def insert_raw_activities_batch(self, activities: List[RawActivityRecord]) -> int:
        """Insère un lot d'activités OS brutes dans raw_activity."""
        if not activities:
            return 0
        sql = """
            INSERT INTO raw_activity (
                timestamp_start, timestamp_end, duration_sec, executable,
                window_title, url_or_path, ocr_snippet, screenshot_path, active_input,
                input_intensity, semantic_topic, cognitive_mode, processed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        payload = [
            (
                a.timestamp_start.strftime("%Y-%m-%d %H:%M:%S"),
                a.timestamp_end.strftime("%Y-%m-%d %H:%M:%S"),
                a.duration_sec,
                a.executable,
                a.window_title,
                a.url_or_path,
                a.ocr_snippet,
                a.screenshot_path,
                1 if a.active_input else 0,
                a.input_intensity,
                a.semantic_topic,
                a.cognitive_mode,
                1 if a.processed else 0,
            )
            for a in activities
        ]
        with self.get_connection() as conn:
            conn.executemany(sql, payload)
        return len(activities)

    def upsert_daily_metrics(self, metric: DailyMetricRecord) -> None:
        """Insère ou met à jour le bilan quotidien dans daily_metrics."""
        sql = """
            INSERT OR REPLACE INTO daily_metrics (
                date, total_screen_sec, active_production_sec, passive_exploration_sec,
                max_hyperfocus_sec, max_hyperfocus_topic, context_switches_per_hour,
                read_vs_write_ratio, top_topics_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        with self.get_connection() as conn:
            conn.execute(
                sql,
                (
                    metric.date.isoformat(),
                    metric.total_screen_sec,
                    metric.active_production_sec,
                    metric.passive_exploration_sec,
                    metric.max_hyperfocus_sec,
                    metric.max_hyperfocus_topic,
                    metric.context_switches_per_hour,
                    metric.read_vs_write_ratio,
                    metric.top_topics_json,
                ),
            )

    # ==========================================================================
    # MÉTHODES DE REQUÊTAGE ET MISES À JOUR
    # ==========================================================================

    def get_chat_sessions(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Récupère les sessions de chat filtrées optionnellement par date."""
        query = "SELECT * FROM chat_sessions"
        params: List[Any] = []
        conditions: List[str] = []

        if start_date:
            conditions.append("timestamp_start >= ?")
            params.append(start_date.strftime("%Y-%m-%d %H:%M:%S"))
        if end_date:
            conditions.append("timestamp_end <= ?")
            params.append(end_date.strftime("%Y-%m-%d %H:%M:%S"))

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY timestamp_start ASC;"

        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_chat_session_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une session par son ID unique."""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM chat_sessions WHERE session_id = ?;", (session_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_unlinked_footprints(self) -> List[Dict[str, Any]]:
        """Récupère toutes les empreintes non rattachées à une session Gemini."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM historical_footprints WHERE linked_gemini_session_id IS NULL ORDER BY timestamp ASC;"
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_footprints_by_timerange(self, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        """Récupère les empreintes Search/YouTube comprises dans un intervalle temporel donné."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM historical_footprints
                WHERE timestamp >= ? AND timestamp <= ?
                ORDER BY timestamp ASC;
                """,
                (start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S")),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_footprints_for_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Récupère toutes les empreintes corrélées à une session Gemini spécifique."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM historical_footprints
                WHERE linked_gemini_session_id = ?
                ORDER BY timestamp ASC;
                """,
                (session_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def link_footprints_batch(self, links: List[Tuple[int, str]]) -> int:
        """Associe par lots des empreintes à un session_id Gemini (jointure temporelle)."""
        if not links:
            return 0
        sql = "UPDATE historical_footprints SET linked_gemini_session_id = ? WHERE id = ?;"
        payload = [(session_id, footprint_id) for footprint_id, session_id in links]
        with self.get_connection() as conn:
            conn.executemany(sql, payload)
        return len(links)

    def update_footprint_clusters_batch(
        self, clusters: List[Tuple[int, str, Optional[str]]]
    ) -> int:
        """Met à jour le cluster_id et le semantic_topic optionnel d'un lot d'empreintes."""
        if not clusters:
            return 0
        sql = "UPDATE historical_footprints SET cluster_id = ?, semantic_topic = ? WHERE id = ?;"
        payload = [(cid, topic, fid) for fid, cid, topic in clusters]
        with self.get_connection() as conn:
            conn.executemany(sql, payload)
        return len(clusters)

    def get_dense_clusters(self, min_events: int = 5) -> List[Dict[str, Any]]:
        """Agrège et retourne les clusters d'empreintes contenant au moins min_events éléments."""
        query = """
            SELECT cluster_id, COUNT(*) as event_count,
                   MIN(timestamp) as start_time, MAX(timestamp) as end_time,
                   GROUP_CONCAT(title_or_query, ' || ') as concatenated_queries,
                   semantic_topic
            FROM historical_footprints
            WHERE cluster_id IS NOT NULL
            GROUP BY cluster_id
            HAVING event_count >= ?
            ORDER BY start_time ASC;
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (min_events,))
            return [dict(row) for row in cursor.fetchall()]

    def get_unprocessed_raw_activities(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """Récupère les entrées brutes de télémétrie non encore traitées par le LLM."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM raw_activity
                WHERE processed = 0
                ORDER BY timestamp_start ASC
                LIMIT ?;
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def mark_raw_activities_processed(self, updates: List[Tuple[int, str, str]]) -> int:
        """Met à jour le semantic_topic, le cognitive_mode et processed=1 pour un lot d'activités."""
        if not updates:
            return 0
        sql = """
            UPDATE raw_activity
            SET semantic_topic = ?, cognitive_mode = ?, processed = 1
            WHERE id = ?;
        """
        payload = [(topic, mode, row_id) for row_id, topic, mode in updates]
        with self.get_connection() as conn:
            conn.executemany(sql, payload)
        return len(updates)

    def get_unprocessed_activities_with_screenshots(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupère les activités non traitées possédant une capture d'écran sauvegardée."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM raw_activity
                WHERE processed = 0 AND screenshot_path IS NOT NULL AND screenshot_path != ''
                ORDER BY timestamp_start ASC
                LIMIT ?;
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def update_activity_visual_summary(self, activity_id: int, visual_summary: str) -> None:
        """Met à jour l'ocr_snippet avec le résumé visuel et efface le screenshot_path."""
        sql = """
            UPDATE raw_activity
            SET ocr_snippet = CASE 
                WHEN ocr_snippet IS NULL OR ocr_snippet = '' THEN ?
                ELSE ocr_snippet || ' | [Visuel] ' || ?
            END,
            screenshot_path = NULL
            WHERE id = ?;
        """
        with self.get_connection() as conn:
            conn.execute(sql, (visual_summary, visual_summary, activity_id))

    def get_distinct_activity_dates(self, processed_only: bool = True) -> List[date]:
        """Retourne la liste des dates uniques présentes dans raw_activity."""
        where_clause = "WHERE processed = 1" if processed_only else ""
        query = f"""
            SELECT DISTINCT DATE(timestamp_start) as act_date
            FROM raw_activity
            {where_clause}
            ORDER BY act_date ASC;
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query)
            dates = []
            for row in cursor.fetchall():
                val = row["act_date"]
                if val:
                    dates.append(datetime.strptime(val, "%Y-%m-%d").date())
            return dates

    def get_activities_for_date(self, target_date: date) -> List[Dict[str, Any]]:
        """Récupère toutes les activités ordonnées pour une journée donnée."""
        start_str = target_date.strftime("%Y-%m-%d 00:00:00")
        end_str = target_date.strftime("%Y-%m-%d 23:59:59")
        query = """
            SELECT * FROM raw_activity
            WHERE timestamp_start >= ? AND timestamp_start <= ?
            ORDER BY timestamp_start ASC;
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (start_str, end_str))
            return [dict(row) for row in cursor.fetchall()]

    def get_database_stats(self) -> Dict[str, int]:
        """Retourne un dictionnaire récapitulatif du nombre d'enregistrements par table."""
        with self.get_connection() as conn:
            stats = {}
            for table in [
                "raw_activity",
                "daily_metrics",
                "chat_sessions",
                "historical_footprints",
                "chat_messages",
                "projects",
                "kanban_tasks",
            ]:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table};")
                stats[table] = cursor.fetchone()[0]
            return stats

    def get_topic_telemetry_stats(self, topic: str) -> Dict[str, Any]:
        """
        Calcule les statistiques cumulées d'investissement et d'antériorité pour un semantic_topic :
        - Temps total d'activité OS traqué (minutes / heures)
        - Nombre de sessions de réflexion Gemini associées
        - Nombre d'empreintes de recherche et vidéo associées
        - Date et heure de dernière activité observée
        - Exécutable dominant
        """
        stats: Dict[str, Any] = {
            "topic": topic,
            "total_os_seconds": 0,
            "total_os_hours": 0.0,
            "chat_sessions_count": 0,
            "footprints_count": 0,
            "last_active": None,
            "dominant_app": None,
        }
        with self.get_connection() as conn:
            # 1. raw_activity
            cur = conn.execute(
                """
                SELECT 
                    COALESCE(SUM(duration_sec), 0) AS total_sec,
                    MAX(timestamp_start) AS max_ts
                FROM raw_activity
                WHERE semantic_topic = ?;
                """,
                (topic,),
            )
            row = cur.fetchone()
            if row:
                stats["total_os_seconds"] = int(row["total_sec"])
                stats["total_os_hours"] = round(row["total_sec"] / 3600.0, 1)
                stats["last_active"] = row["max_ts"]

            # Exécutable dominant
            cur = conn.execute(
                """
                SELECT executable, SUM(duration_sec) AS dur
                FROM raw_activity
                WHERE semantic_topic = ?
                GROUP BY executable
                ORDER BY dur DESC
                LIMIT 1;
                """,
                (topic,),
            )
            top_app = cur.fetchone()
            if top_app:
                stats["dominant_app"] = top_app["executable"]

            # 2. chat_sessions
            cur = conn.execute(
                """
                SELECT 
                    COUNT(*) AS count,
                    MAX(timestamp_end) AS max_ts
                FROM chat_sessions
                WHERE extracted_topics_json LIKE ?;
                """,
                (f"%{topic}%",),
            )
            chat_row = cur.fetchone()
            if chat_row:
                stats["chat_sessions_count"] = int(chat_row["count"])
                chat_max = chat_row["max_ts"]
                if chat_max and (not stats["last_active"] or chat_max > stats["last_active"]):
                    stats["last_active"] = chat_max

            # 3. historical_footprints
            cur = conn.execute(
                """
                SELECT 
                    COUNT(*) AS count,
                    MAX(timestamp) AS max_ts
                FROM historical_footprints
                WHERE semantic_topic = ?;
                """,
                (topic,),
            )
            fp_row = cur.fetchone()
            if fp_row:
                stats["footprints_count"] = int(fp_row["count"])
                fp_max = fp_row["max_ts"]
                if fp_max and (not stats["last_active"] or fp_max > stats["last_active"]):
                    stats["last_active"] = fp_max

        return stats

    # ==========================================================================
    # MÉTHODES DU MODULE 7 : KANBAN EXÉCUTIF & MULTI-PROJETS (v0.2.0)
    # ==========================================================================

    def get_projects(self) -> List[Dict[str, Any]]:
        """Retourne tous les projets suivis, ordonnés par date de création croissante."""
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM projects ORDER BY created_at ASC;")
            return [dict(row) for row in cur.fetchall()]

    def get_project_by_id(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Récupère un projet spécifique par son project_id."""
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM projects WHERE project_id = ?;", (project_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def upsert_project(self, project: ProjectRecord) -> None:
        """Insère ou met à jour un projet."""
        created_str = (
            project.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(project.created_at, datetime)
            else str(project.created_at)
        )
        sql = """
            INSERT OR REPLACE INTO projects (project_id, name, prefix, repo_path, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        with self.get_connection() as conn:
            conn.execute(
                sql,
                (
                    project.project_id,
                    project.name,
                    project.prefix,
                    project.repo_path,
                    project.description,
                    created_str,
                ),
            )

    def generate_next_task_id(self, project_id: str) -> str:
        """
        Génère le prochain identifiant déterministe séquentiel pour un projet (ex: EXO-001, EXO-002).
        Analyse les IDs existants pour ce préfixe et incrémente le numéro maximal.
        """
        proj = self.get_project_by_id(project_id)
        prefix = proj["prefix"].strip().upper() if proj and proj.get("prefix") else project_id.upper()[:4]

        pattern = f"{prefix}-%"
        with self.get_connection() as conn:
            cur = conn.execute(
                "SELECT task_id FROM kanban_tasks WHERE project_id = ? OR task_id LIKE ?;",
                (project_id, pattern),
            )
            rows = cur.fetchall()

        max_num = 0
        for row in rows:
            tid = str(row["task_id"]).strip()
            match = re.match(rf"^{re.escape(prefix)}-(\d+)$", tid)
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num

        return f"{prefix}-{max_num + 1:03d}"

    def upsert_kanban_task(self, task: KanbanTaskRecord) -> str:
        """Insère ou remplace une tâche Kanban et retourne son task_id."""
        created_str = (
            task.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(task.created_at, datetime)
            else str(task.created_at)
        )
        updated_str = (
            task.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(task.updated_at, datetime)
            else str(task.updated_at)
        )
        sql = """
            INSERT OR REPLACE INTO kanban_tasks (
                task_id, project_id, component_tag, title, summary_pitch,
                status, priority, complexity, spec_file_path, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        with self.get_connection() as conn:
            conn.execute(
                sql,
                (
                    task.task_id,
                    task.project_id,
                    task.component_tag,
                    task.title,
                    task.summary_pitch,
                    task.status,
                    task.priority,
                    task.complexity,
                    task.spec_file_path,
                    created_str,
                    updated_str,
                ),
            )
        return task.task_id

    def update_kanban_task_status(
        self, task_id: str, new_status: str, spec_file_path: Optional[str] = None
    ) -> bool:
        """Met à jour le statut d'une tâche, sa date de mise à jour, et optionnellement son chemin de spec."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            if spec_file_path is not None:
                cur = conn.execute(
                    """
                    UPDATE kanban_tasks
                    SET status = ?, spec_file_path = ?, updated_at = ?
                    WHERE task_id = ?;
                    """,
                    (new_status, spec_file_path, now_str, task_id),
                )
            else:
                cur = conn.execute(
                    """
                    UPDATE kanban_tasks
                    SET status = ?, updated_at = ?
                    WHERE task_id = ?;
                    """,
                    (new_status, now_str, task_id),
                )
            return cur.rowcount > 0

    def update_kanban_task_details(
        self,
        task_id: str,
        title: str,
        component_tag: str,
        summary_pitch: str,
        priority: int,
        complexity: str,
    ) -> bool:
        """Met à jour les métadonnées descriptives d'une tâche."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                UPDATE kanban_tasks
                SET title = ?, component_tag = ?, summary_pitch = ?, priority = ?, complexity = ?, updated_at = ?
                WHERE task_id = ?;
                """,
                (title, component_tag, summary_pitch, priority, complexity, now_str, task_id),
            )
            return cur.rowcount > 0

    def delete_kanban_task(self, task_id: str) -> bool:
        """Supprime définitivement une tâche Kanban."""
        with self.get_connection() as conn:
            cur = conn.execute("DELETE FROM kanban_tasks WHERE task_id = ?;", (task_id,))
            return cur.rowcount > 0

    def get_kanban_tasks(
        self, project_id: Optional[str] = None, statuses: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Récupère les tâches Kanban filtrées par projet et/ou statuts,
        triées par priorité croissante (P1 en premier), puis par updated_at DESC.
        """
        clauses = []
        params: List[Any] = []
        if project_id:
            clauses.append("project_id = ?")
            params.append(project_id)
        if statuses:
            placeholders = ",".join("?" for _ in statuses)
            clauses.append(f"status IN ({placeholders})")
            params.extend(statuses)

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"""
            SELECT * FROM kanban_tasks
            {where_sql}
            ORDER BY priority ASC, updated_at DESC;
        """
        with self.get_connection() as conn:
            cur = conn.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]

    def get_kanban_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une tâche Kanban par son task_id."""
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM kanban_tasks WHERE task_id = ?;", (task_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    # ==========================================================================
    # MÉTHODES ANALYTIQUES CONSOLIDÉES POUR LE DASHBOARD (READ-ONLY)
    # ==========================================================================

    def fetch_macro_kpis(self) -> Dict[str, Any]:
        """Charge l'ensemble des KPIs macro consolidés."""
        with self.get_ro_connection() as conn:
            # 1. Total chat sessions & turns
            cur = conn.execute("SELECT COUNT(*), SUM(turn_count), SUM(user_char_count) FROM chat_sessions;")
            chat_count, total_turns, total_chars = cur.fetchone()
            chat_count = chat_count or 0
            total_turns = total_turns or 0
            total_chars = total_chars or 0

            # Heures estimées Gemini (10 min par session en moyenne)
            chat_hours = round((chat_count * 10) / 60.0, 1)

            # 2. Total raw activity
            cur = conn.execute(
                """
                SELECT 
                    COUNT(*),
                    COALESCE(SUM(duration_sec), 0),
                    COALESCE(SUM(CASE WHEN active_input = 1 THEN duration_sec ELSE 0 END), 0),
                    COALESCE(SUM(CASE WHEN active_input = 0 THEN duration_sec ELSE 0 END), 0)
                FROM raw_activity;
                """
            )
            raw_count, total_os_sec, active_prod_sec, passive_exp_sec = cur.fetchone()
            total_os_sec = total_os_sec or 0
            active_prod_sec = active_prod_sec or 0
            passive_exp_sec = passive_exp_sec or 0
            os_hours = round(total_os_sec / 3600.0, 1)

            # 3. Daily metrics stats
            cur = conn.execute(
                """
                SELECT 
                    AVG(context_switches_per_hour),
                    AVG(read_vs_write_ratio)
                FROM daily_metrics;
                """
            )
            row_avg = cur.fetchone()
            avg_switch_rate = round(row_avg[0], 2) if row_avg and row_avg[0] is not None else 0.0
            avg_read_ratio = round(row_avg[1], 2) if row_avg and row_avg[1] is not None else 0.4

            cur = conn.execute(
                """
                SELECT max_hyperfocus_sec, max_hyperfocus_topic
                FROM daily_metrics
                WHERE max_hyperfocus_sec IS NOT NULL
                ORDER BY max_hyperfocus_sec DESC
                LIMIT 1;
                """
            )
            row_hf = cur.fetchone()
            max_hyperfocus_sec = row_hf[0] if row_hf and row_hf[0] else 0
            max_hyperfocus_topic = row_hf[1] if row_hf and row_hf[1] else "N/A"

            # 4. Footprints count
            cur = conn.execute("SELECT COUNT(*) FROM historical_footprints;")
            fp_count = cur.fetchone()[0] or 0

        return {
            "chat_count": chat_count,
            "chat_hours": chat_hours,
            "total_turns": total_turns,
            "total_chars": total_chars,
            "raw_count": raw_count,
            "os_hours": os_hours,
            "total_tracked_hours": round(chat_hours + os_hours, 1),
            "active_prod_hours": round(active_prod_sec / 3600.0, 1),
            "passive_exp_hours": round(passive_exp_sec / 3600.0, 1),
            "max_hyperfocus_hours": round(max_hyperfocus_sec / 3600.0, 2),
            "max_hyperfocus_topic": max_hyperfocus_topic,
            "avg_switch_rate": avg_switch_rate,
            "avg_read_ratio": avg_read_ratio,
            "fp_count": fp_count,
        }

    def fetch_all_activity_dates(self) -> List[str]:
        """Charge les dates distinctes disponibles dans raw_activity."""
        with self.get_ro_connection() as conn:
            cur = conn.execute("SELECT DISTINCT DATE(timestamp_start) as dt FROM raw_activity ORDER BY dt DESC;")
            dates = [r["dt"] for r in cur.fetchall() if r["dt"]]
            if not dates:
                dates = [datetime.now().strftime("%Y-%m-%d")]
            return dates

    def fetch_timeline_for_date(self, target_date_str: str) -> List[Dict[str, Any]]:
        """Charge la chronologie brute des fenêtres d'activité pour une date spécifique."""
        with self.get_ro_connection() as conn:
            cur = conn.execute(
                """
                SELECT 
                    timestamp_start, timestamp_end, duration_sec, executable,
                    window_title, active_input, input_intensity, semantic_topic, cognitive_mode
                FROM raw_activity
                WHERE DATE(timestamp_start) = ?
                ORDER BY timestamp_start ASC;
                """,
                (target_date_str,),
            )
            return [dict(r) for r in cur.fetchall()]

    def fetch_treemap_data(self) -> List[Dict[str, Any]]:
        """Charge les données agrégées pour le Treemap hiérarchique."""
        with self.get_ro_connection() as conn:
            cur = conn.execute(
                """
                SELECT 
                    cognitive_mode, semantic_topic, executable,
                    SUM(duration_sec) as total_sec,
                    COUNT(*) as event_count
                FROM raw_activity
                GROUP BY cognitive_mode, semantic_topic, executable
                ORDER BY total_sec DESC;
                """
            )
            return [dict(r) for r in cur.fetchall()]

    def fetch_archaeology_sessions(self) -> List[Dict[str, Any]]:
        """Charge les sessions Gemini pour l'analyse archéologique temporelle."""
        with self.get_ro_connection() as conn:
            cur = conn.execute(
                """
                SELECT timestamp_start, extracted_topics_json, turn_count, user_char_count
                FROM chat_sessions
                ORDER BY timestamp_start ASC;
                """
            )
            records = []
            for r in cur.fetchall():
                ts = r["timestamp_start"]
                topics_raw = r["extracted_topics_json"]
                try:
                    topics = json.loads(topics_raw) if topics_raw else []
                except Exception:
                    topics = []
                if not topics:
                    topics = ["Dev_et_Architecture_Tech"]
                for top in topics:
                    records.append({
                        "timestamp": ts,
                        "topic": normalize_to_macro_topic(top),
                        "turns": r["turn_count"],
                        "chars": r["user_char_count"],
                        "count": 1,
                    })
            return records

    def fetch_circadian_timestamps(self) -> List[str]:
        """Charge la liste de tous les horodatages disponibles pour l'analyse circadienne."""
        with self.get_ro_connection() as conn:
            cur = conn.execute("SELECT timestamp_start FROM chat_sessions;")
            chat_ts = [r[0] for r in cur.fetchall() if r[0]]
            cur = conn.execute("SELECT timestamp_start FROM raw_activity;")
            os_ts = [r[0] for r in cur.fetchall() if r[0]]
        return [str(ts) for ts in (chat_ts + os_ts)]

    def search_chat_sessions(
        self,
        query: str = "",
        topic_filter: Optional[str] = None,
        status_filter: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Recherche full-text dans les sessions et messages Gemini."""
        with self.get_ro_connection() as conn:
            params: List[Any] = []
            conditions = []

            if query.strip():
                q_like = f"%{query.strip()}%"
                conditions.append(
                    "(cs.session_id IN (SELECT session_id FROM chat_messages WHERE user_prompt LIKE ? OR ai_response LIKE ?) OR cs.summary LIKE ?)"
                )
                params.extend([q_like, q_like, q_like])

            if topic_filter and topic_filter != "Tous les topics":
                conditions.append("cs.extracted_topics_json LIKE ?")
                params.append(f"%{topic_filter}%")

            if status_filter and status_filter != "Tous":
                conditions.append("cs.distillation_status = ?")
                params.append(status_filter)

            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            sql = f"""
                SELECT cs.session_id, cs.timestamp_start, cs.timestamp_end, cs.turn_count,
                       cs.user_char_count, cs.extracted_topics_json, cs.generated_notes_json,
                       cs.summary, cs.distillation_status
                FROM chat_sessions cs
                {where_clause}
                ORDER BY cs.timestamp_start DESC
                LIMIT {limit};
            """
            cur = conn.execute(sql, params)
            return [dict(r) for r in cur.fetchall()]

    def fetch_messages_for_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Récupère l'ensemble des tours de conversation d'une session de chat."""
        with self.get_ro_connection() as conn:
            cur = conn.execute(
                """
                SELECT id, turn_index, timestamp, user_prompt, ai_response, user_char_count
                FROM chat_messages
                WHERE session_id = ?
                ORDER BY turn_index ASC;
                """,
                (session_id,),
            )
            return [dict(r) for r in cur.fetchall()]

    def fetch_footprints_summary(self) -> Dict[str, Any]:
        """Calcule les métriques globales sur la table historical_footprints."""
        with self.get_ro_connection() as conn:
            cur = conn.execute(
                """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN source = 'youtube' THEN 1 ELSE 0 END) as youtube_count,
                    SUM(CASE WHEN source = 'google_search' THEN 1 ELSE 0 END) as search_count,
                    SUM(CASE WHEN cluster_id IS NOT NULL AND cluster_id != '' THEN 1 ELSE 0 END) as clustered_count,
                    SUM(CASE WHEN linked_gemini_session_id IS NOT NULL AND linked_gemini_session_id != '' THEN 1 ELSE 0 END) as linked_count
                FROM historical_footprints;
                """
            )
            r = cur.fetchone()
            return {
                "total": r["total"] or 0,
                "youtube": r["youtube_count"] or 0,
                "search": r["search_count"] or 0,
                "clustered": r["clustered_count"] or 0,
                "linked": r["linked_count"] or 0,
            }

    def fetch_top_channels_and_domains(self, limit: int = 15) -> List[Dict[str, Any]]:
        """Agrège le top des chaînes YouTube et domaines consultés."""
        with self.get_ro_connection() as conn:
            cur = conn.execute(
                f"""
                SELECT channel_or_domain, source, COUNT(*) as footprint_count
                FROM historical_footprints
                WHERE channel_or_domain IS NOT NULL AND channel_or_domain != ''
                GROUP BY channel_or_domain, source
                ORDER BY footprint_count DESC
                LIMIT {limit};
                """
            )
            return [dict(r) for r in cur.fetchall()]

    def fetch_burst_clusters_summary(self, limit: int = 25) -> List[Dict[str, Any]]:
        """Identifie les tunnels de recherche denses (Burst Clusters) d'au moins 3 événements."""
        with self.get_ro_connection() as conn:
            cur = conn.execute(
                f"""
                SELECT 
                    cluster_id,
                    source,
                    semantic_topic,
                    COUNT(*) as event_count,
                    MIN(timestamp) as start_time,
                    MAX(timestamp) as end_time,
                    GROUP_CONCAT(title_or_query, ' ➔ ') as samples
                FROM historical_footprints
                WHERE cluster_id IS NOT NULL AND cluster_id != ''
                GROUP BY cluster_id, source, semantic_topic
                HAVING event_count >= 3
                ORDER BY event_count DESC, start_time DESC
                LIMIT {limit};
                """
            )
            return [dict(r) for r in cur.fetchall()]

    def search_footprints(
        self,
        query: str = "",
        source_filter: str = "Toutes",
        only_clustered: bool = False,
        only_linked: bool = False,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Recherche dynamique d'empreintes avec filtres multiples."""
        with self.get_ro_connection() as conn:
            conditions = []
            params = []
            if query.strip():
                conditions.append("(title_or_query LIKE ? OR channel_or_domain LIKE ?)")
                params.extend([f"%{query.strip()}%", f"%{query.strip()}%"])
            if source_filter and source_filter != "Toutes":
                conditions.append("source = ?")
                params.append(source_filter)
            if only_clustered:
                conditions.append("cluster_id IS NOT NULL AND cluster_id != ''")
            if only_linked:
                conditions.append("linked_gemini_session_id IS NOT NULL AND linked_gemini_session_id != ''")

            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            cur = conn.execute(
                f"""
                SELECT timestamp, source, channel_or_domain, title_or_query, cluster_id, semantic_topic, linked_gemini_session_id
                FROM historical_footprints
                {where_clause}
                ORDER BY timestamp DESC
                LIMIT {limit};
                """,
                params,
            )
            return [dict(r) for r in cur.fetchall()]

