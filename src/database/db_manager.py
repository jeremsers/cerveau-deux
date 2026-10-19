"""
Couche de persistance SQLite pour le système 'Exocortex & Télémétrie Cognitive'.
Configure le moteur SQLite en mode WAL, initialise les 4 tables relationnelles
et fournit des méthodes optimisées d'insertion et d'analyse par lots.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pydantic import BaseModel, Field

from src.config import settings


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


# ==============================================================================
# GESTIONNAIRE DE BASE DE DONNÉES SQLITE
# ==============================================================================

class DBManager:
    """Gestionnaire de persistance SQLite thread-safe configuré en mode WAL haute performance."""

    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = db_path or settings.DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Fournit une connexion SQLite configurée avec WAL, timeouts et row_factory."""
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
                    summary TEXT NOT NULL
                );
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_chat_date ON chat_sessions(timestamp_start);")

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
                user_char_count, extracted_topics_json, generated_notes_json, summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
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
            )
            for s in sessions
        ]
        with self.get_connection() as conn:
            conn.executemany(sql, payload)
        return len(sessions)

    def insert_historical_footprints_batch(self, footprints: List[HistoricalFootprintRecord]) -> int:
        """Insère un lot d'empreintes Search/YouTube dans historical_footprints."""
        if not footprints:
            return 0
        sql = """
            INSERT INTO historical_footprints (
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
            for table in ["raw_activity", "daily_metrics", "chat_sessions", "historical_footprints"]:
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

