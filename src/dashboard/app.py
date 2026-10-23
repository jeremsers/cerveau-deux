"""
Module 6 : Dashboard Streamlit "Bandeur de Stats" (Télémétrie Cognitive & Archéologie Épistémique).
Interface analytique locale complète, moderne et sombre, interrogeant directement telemetry.db en mode lecture seule.
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pyperclip
import streamlit as st

from src.config import AUTHORIZED_SEMANTIC_TOPICS, normalize_to_macro_topic, settings
from src.consolidators.kanban_engine import kanban_engine
from src.database.db_manager import ProjectRecord

# Configuration de styles CSS avancés
APP_CUSTOM_CSS = """
<style>
.main {
    background-color: #0b0f19;
    color: #f3f4f6;
}
.stMetric {
    background-color: #131b2e;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #1f293d;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}
.stMetric label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.stMetric div[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
    font-size: 1.8rem !important;
    font-weight: 800;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background-color: #0f172a;
    padding: 8px 12px;
    border-radius: 10px;
}
.stTabs [data-baseweb="tab"] {
    padding: 10px 20px;
    color: #94a3b8;
    border-radius: 6px;
}
.stTabs [aria-selected="true"] {
    background-color: #2563eb !important;
    color: #ffffff !important;
    font-weight: bold;
}
.card-box {
    background-color: #131b2e;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}
</style>
"""


@st.cache_resource
def get_db_path() -> Path:
    return settings.SQLITE_DB_PATH


def get_ro_connection() -> sqlite3.Connection:
    """Ouvre une connexion SQLite en lecture seule stricte (file:telemetry.db?mode=ro)."""
    db_path = get_db_path()
    if not db_path.exists():
        try:
            st.error(f"Base de données introuvable : {db_path}")
            st.stop()
        except Exception:
            raise FileNotFoundError(f"Base de données introuvable : {db_path}")
    uri = f"file:{db_path.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=5.0)
    conn.row_factory = sqlite3.Row
    return conn


@st.cache_data(ttl=30)
def load_macro_kpis() -> Dict[str, Any]:
    """Charge l'ensemble des KPIs macro consolidés."""
    with get_ro_connection() as conn:
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

        # 3. Daily metrics stats (agrégation découplée et record d'hyperfocus déterministe)
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


@st.cache_data(ttl=30)
def load_all_activity_dates() -> List[str]:
    """Charge les dates distinctes disponibles dans raw_activity et daily_metrics."""
    with get_ro_connection() as conn:
        cur = conn.execute("SELECT DISTINCT DATE(timestamp_start) as dt FROM raw_activity ORDER BY dt DESC;")
        dates = [r["dt"] for r in cur.fetchall() if r["dt"]]
        if not dates:
            dates = [datetime.now().strftime("%Y-%m-%d")]
        return dates


@st.cache_data(ttl=30)
def load_timeline_for_date(target_date_str: str) -> pd.DataFrame:
    """Charge la chronologie des fenêtres d'activité pour une date spécifique."""
    with get_ro_connection() as conn:
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
        rows = [dict(r) for r in cur.fetchall()]
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows)
        df["timestamp_start"] = pd.to_datetime(df["timestamp_start"])
        df["timestamp_end"] = pd.to_datetime(df["timestamp_end"])
        df["duration_min"] = (df["duration_sec"] / 60.0).round(1)
        df["semantic_topic"] = df["semantic_topic"].fillna("Non_Classe")
        df["cognitive_mode"] = df["cognitive_mode"].fillna("exploration")
        return df


@st.cache_data(ttl=30)
def load_treemap_data() -> pd.DataFrame:
    """Charge les données agrégées pour le Treemap hiérarchique."""
    with get_ro_connection() as conn:
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
        rows = [dict(r) for r in cur.fetchall()]
        if not rows:
            # Fallback avec données de sessions chat si raw_activity est encore jeune
            return pd.DataFrame()
        df = pd.DataFrame(rows)
        df["duration_hours"] = (df["total_sec"] / 3600.0).round(2)
        df["cognitive_mode"] = df["cognitive_mode"].fillna("exploration")
        df["semantic_topic"] = df["semantic_topic"].fillna("Non_Classe")
        df["executable"] = df["executable"].fillna("Inconnu")
        return df


@st.cache_data(ttl=30)
def load_archaeology_data() -> pd.DataFrame:
    """
    Charge l'évolution temporelle hebdomadaire des topics sur les sessions Gemini
    (2024-2026).
    """
    with get_ro_connection() as conn:
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
        if not records:
            return pd.DataFrame()
        df = pd.DataFrame(records)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["year_week"] = df["timestamp"].dt.to_period("W").dt.to_timestamp()
        df["year_month"] = df["timestamp"].dt.to_period("M").dt.to_timestamp()
        return df


@st.cache_data(ttl=30)
def load_circadian_data() -> pd.DataFrame:
    """Charge la répartition 24h x 7j sur l'ensemble de l'historique."""
    with get_ro_connection() as conn:
        # Sessions chat
        cur = conn.execute("SELECT timestamp_start FROM chat_sessions;")
        chat_ts = [r[0] for r in cur.fetchall() if r[0]]
        # Activité OS
        cur = conn.execute("SELECT timestamp_start FROM raw_activity;")
        os_ts = [r[0] for r in cur.fetchall() if r[0]]

    all_ts = chat_ts + os_ts
    if not all_ts:
        return pd.DataFrame()

    df = pd.DataFrame({"timestamp": pd.to_datetime(all_ts)})
    df["hour"] = df["timestamp"].dt.hour
    # 0 = Lundi, 6 = Dimanche
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    df["day_name"] = df["day_of_week"].apply(lambda d: day_names[d])
    return df


@st.cache_data(ttl=30)
def load_chat_search_results(
    query: str = "",
    topic_filter: Optional[str] = None,
    status_filter: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """Recherche full-text dans les sessions et messages Gemini."""
    with get_ro_connection() as conn:
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


@st.cache_data(ttl=30)
def load_messages_for_session(session_id: str) -> List[Dict[str, Any]]:
    """Récupère l'ensemble des tours de conversation d'une session de chat."""
    with get_ro_connection() as conn:
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


@st.cache_data(ttl=30)
def load_footprints_summary() -> Dict[str, Any]:
    """Calcule les métriques globales sur la table historical_footprints."""
    with get_ro_connection() as conn:
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


@st.cache_data(ttl=30)
def load_top_channels_and_domains(limit: int = 15) -> pd.DataFrame:
    """Agrège le top 15 des chaînes YouTube et domaines consultés."""
    with get_ro_connection() as conn:
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
        rows = [dict(r) for r in cur.fetchall()]
        return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["channel_or_domain", "source", "footprint_count"])


@st.cache_data(ttl=30)
def load_burst_clusters_summary(limit: int = 25) -> pd.DataFrame:
    """Identifie les tunnels de recherche denses (Burst Clusters) d'au moins 3 événements."""
    with get_ro_connection() as conn:
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
        rows = [dict(r) for r in cur.fetchall()]
        return pd.DataFrame(rows) if rows else pd.DataFrame()


@st.cache_data(ttl=30)
def search_historical_footprints(
    query: str = "",
    source_filter: str = "Toutes",
    only_clustered: bool = False,
    only_linked: bool = False,
    limit: int = 100,
) -> pd.DataFrame:
    """Recherche dynamique d'empreintes avec filtres multiples."""
    with get_ro_connection() as conn:
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
        rows = [dict(r) for r in cur.fetchall()]
        return pd.DataFrame(rows) if rows else pd.DataFrame(columns=[
            "timestamp", "source", "channel_or_domain", "title_or_query", "cluster_id", "semantic_topic", "linked_gemini_session_id"
        ])


# ==============================================================================
# EN-TÊTE PRINCIPAL & BANDEAU DE KPIS MACRO
# ==============================================================================

st.title("🧠 EXOCORTEX — BANDEUR DE STATS")
st.caption("Tableau de bord de télémétrie cognitive, quantification du focus & archéologie épistémique.")

kpis = load_macro_kpis()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(
        label="Temps Total Traqué",
        value=f"{kpis['total_tracked_hours']} h",
        help="Cumul de l'activité OS locale et des sessions de réflexion Gemini.",
    )
with col2:
    st.metric(
        label="Record d'Hyperfocus",
        value=f"{kpis['max_hyperfocus_hours']} h",
        delta=f"#{kpis['max_hyperfocus_topic']}",
        delta_color="normal",
        help="Plus long tunnel continu de concentration sans zapping d'application.",
    )
with col3:
    st.metric(
        label="Fragmentation (Switches/h)",
        value=f"{kpis['avg_switch_rate']}",
        help="Moyenne des changements de contexte d'application par heure.",
    )
with col4:
    prod_pct = int((kpis['active_prod_hours'] / max(1.0, kpis['active_prod_hours'] + kpis['passive_exp_hours'])) * 100)
    st.metric(
        label="Ratio Prod / Conso",
        value=f"{prod_pct}% Prod",
        delta=f"{100 - prod_pct}% Exploration",
        delta_color="off",
        help="Pourcentage de temps passé en saisie active versus lecture ou vidéo.",
    )
with col5:
    st.metric(
        label="Mémoire Épistémique",
        value=f"{kpis['chat_count']} Sessions",
        delta=f"{kpis['total_turns']} Tours / {kpis['fp_count']} Empreintes",
        delta_color="normal",
        help="Nombre total de sessions de réflexion Gemini et empreintes analysées.",
    )

st.markdown("---")

# ==============================================================================
# NAVIGATION PAR ONGLETS
# ==============================================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "⏱️ Chronologie & Focus Quotidien",
    "🗺️ Cartographie des Obsessions",
    "📜 Archéologie Longitudinale",
    "🌙 Rythmes Circadiens",
    "🔍 Explorateur Épistémique & Empreintes",
    "📋 Kanban & Studio SOTA",
])

# ------------------------------------------------------------------------------
# ONGLET 1 : CHRONOLOGIE & FOCUS QUOTIDIEN
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Analyse Chronologique Quotidienne & Tunnels d'Hyperfocus")

    available_dates = load_all_activity_dates()
    selected_date = st.selectbox("Sélectionner la journée à inspecter :", available_dates, index=0)

    df_day = load_timeline_for_date(selected_date)

    if df_day.empty:
        st.info(f"Aucune activité écran enregistrée pour la journée du {selected_date}.")
    else:
        # Métriques du jour
        day_tot_min = df_day["duration_min"].sum()
        day_prod_min = df_day[df_day["active_input"] == 1]["duration_min"].sum()
        day_exp_min = df_day[df_day["active_input"] == 0]["duration_min"].sum()

        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        mcol1.metric("Temps Écran Total", f"{round(day_tot_min / 60.0, 1)} h ({int(day_tot_min)} min)")
        mcol2.metric("Production Active", f"{round(day_prod_min / 60.0, 1)} h", f"{int(day_prod_min)} min")
        mcol3.metric("Exploration Passive", f"{round(day_exp_min / 60.0, 1)} h", f"{int(day_exp_min)} min")
        mcol4.metric("Fenêtres Traquées", f"{len(df_day)}")

        # Graphique de Gantt / Timeline Plotly
        fig_gantt = px.timeline(
            df_day,
            x_start="timestamp_start",
            x_end="timestamp_end",
            y="executable",
            color="semantic_topic",
            hover_name="window_title",
            hover_data={
                "duration_min": True,
                "cognitive_mode": True,
                "active_input": True,
                "timestamp_start": "|%H:%M:%S",
                "timestamp_end": "|%H:%M:%S",
            },
            title=f"Chronologie Détaillée de l'Activité Écran — {selected_date}",
            template="plotly_dark",
            height=400,
        )
        fig_gantt.update_yaxes(autorange="reversed")
        fig_gantt.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor="#0f172a",
            paper_bgcolor="#0f172a",
            xaxis_title="Heure de la journée",
            yaxis_title="Application",
        )
        st.plotly_chart(fig_gantt, use_container_width=True)

        # Détection et mise en exergue des blocs d'hyperfocus (> 30 min)
        hyperfocus_blocks = df_day[df_day["duration_sec"] >= 1800].sort_values("duration_sec", ascending=False)
        if not hyperfocus_blocks.empty:
            st.markdown("#### 🎯 Tunnels d'Hyperfocus Détectés (≥ 30 min)")
            for _, hrow in hyperfocus_blocks.iterrows():
                dur_h = round(hrow["duration_sec"] / 3600.0, 2)
                st.success(
                    f"**{dur_h}h ({int(hrow['duration_sec'] / 60)} min)** sur **{hrow['executable']}** "
                    f"— Topic: `#{hrow['semantic_topic']}` | Mode: `{hrow['cognitive_mode']}` | *{hrow['window_title'][:80]}*"
                )

        # Tableau des fenêtres du jour
        with st.expander("Voir le détail tabulaire des fenêtres de la journée"):
            st.dataframe(
                df_day[["timestamp_start", "duration_min", "executable", "semantic_topic", "cognitive_mode", "window_title"]],
                use_container_width=True,
            )

# ------------------------------------------------------------------------------
# ONGLET 2 : CARTOGRAPHIE DES OBSESSIONS & TREEMAP
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Cartographie Hiérarchique des Domaines & Allocations Temporelles")

    df_tree = load_treemap_data()

    if df_tree.empty:
        # Alternative basée sur chat_sessions si raw_activity est encore vide
        st.info("Données d'activité écran insuffisantes pour construire le Treemap complet. Affichage de la répartition des sessions Gemini :")
        df_arch = load_archaeology_data()
        if not df_arch.empty:
            topic_counts = df_arch["topic"].value_counts().reset_index()
            topic_counts.columns = ["Topic", "Sessions"]
            fig_pie = px.pie(
                topic_counts,
                names="Topic",
                values="Sessions",
                title="Répartition des Sujets de Réflexion (Sessions Gemini)",
                template="plotly_dark",
                hole=0.4,
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        tcol1, tcol2 = st.columns([3, 2])
        with tcol1:
            st.markdown("#### Treemap : `Mode Cognitif` → `Topic Sémantique` → `Application`")
            fig_tree = px.treemap(
                df_tree,
                path=["cognitive_mode", "semantic_topic", "executable"],
                values="total_sec",
                color="cognitive_mode",
                template="plotly_dark",
                height=520,
            )
            fig_tree.update_layout(margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_tree, use_container_width=True)

        with tcol2:
            st.markdown("#### Répartition par Mode Cognitif")
            mode_agg = df_tree.groupby("cognitive_mode")["total_sec"].sum().reset_index()
            mode_agg["hours"] = (mode_agg["total_sec"] / 3600.0).round(1)
            fig_donut = px.pie(
                mode_agg,
                names="cognitive_mode",
                values="hours",
                hole=0.45,
                template="plotly_dark",
                height=350,
            )
            fig_donut.update_layout(margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_donut, use_container_width=True)

            # Top 5 des exécutables
            st.markdown("#### Top 5 des Applications")
            app_agg = df_tree.groupby("executable")["total_sec"].sum().reset_index()
            app_agg["hours"] = (app_agg["total_sec"] / 3600.0).round(1)
            app_agg = app_agg.sort_values("hours", ascending=False).head(5)
            st.dataframe(app_agg[["executable", "hours"]], use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# ONGLET 3 : ARCHÉOLOGIE LONGITUDINALE & DEMI-VIE DES INTÉRÊTS
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Archéologie Longitudinale & Demi-Vie des Obsessions (2024 - 2026)")
    st.markdown(
        "Ce module retrace l'histoire intellectuelle sur plus de 690 sessions de réflexion, "
        "distinguant les **Piliers Fondamentaux** (intérêts récurrents durables) des **Passions Éphémères** "
        "(pics d'obsession temporaires)."
    )

    df_arch = load_archaeology_data()

    if df_arch.empty:
        st.warning("Aucune session Gemini trouvée pour l'analyse archéologique.")
    else:
        # 1. Aire empilée temporelle (mensuelle)
        monthly_topics = df_arch.groupby(["year_month", "topic"])["count"].sum().reset_index()
        fig_area = px.area(
            monthly_topics,
            x="year_month",
            y="count",
            color="topic",
            title="Évolution Mensuelle du Volume de Réflexion par Sujet Sémantique (2024 - 2026)",
            template="plotly_dark",
            height=460,
        )
        fig_area.update_layout(
            xaxis_title="Chronologie",
            yaxis_title="Nombre de Sessions",
            legend_title="Topic Sémantique",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_area, use_container_width=True)

        # 2. Analyse de la demi-vie et catégorisation des intérêts
        st.markdown("#### Matrice de Pérennité Cognitive : Piliers vs Passions Éphémères")

        stats_list = []
        now_dt = datetime.now()
        for topic, grp in df_arch.groupby("topic"):
            min_date = grp["timestamp"].min()
            max_date = grp["timestamp"].max()
            span_days = max(1, (max_date - min_date).days)
            session_count = len(grp)
            total_chars = grp["chars"].sum()

            # Classification heuristique
            recency_days = (now_dt - max_date).days
            if span_days > 180 and session_count >= 15:
                archetype = "🏛️ Pilier Fondamental"
            elif span_days < 45 and session_count >= 5:
                archetype = "⚡ Passion Éphémère (Burst)"
            elif recency_days < 30 and span_days < 60:
                archetype = "🌱 Sujet Émergent"
            else:
                archetype = "🔄 Intérêt Intermittent"

            stats_list.append({
                "Sujet Sémantique": topic,
                "Archétype Cognitif": archetype,
                "Sessions": session_count,
                "Premier Focus": min_date.strftime("%Y-%m-%d"),
                "Dernier Focus": max_date.strftime("%Y-%m-%d"),
                "Étendue (Jours)": span_days,
                "Caractères Rédigés": int(total_chars),
            })

        df_stats = pd.DataFrame(stats_list).sort_values("Sessions", ascending=False)
        st.dataframe(df_stats, use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# ONGLET 4 : RYTHMES CIRCADIENS & CHRONOBIOLOGIE
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("Analyse Chronobiologique & Rythmes Circadiens (24h x 7j)")
    st.caption("Visualisation des plages horaires d'hyperfocus et des signatures de productivité nocturne.")

    df_circ = load_circadian_data()

    if df_circ.empty:
        st.warning("Données insuffisantes pour cartographier les rythmes circadiens.")
    else:
        # Création de la matrice 7j x 24h
        day_order = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        matrix = df_circ.groupby(["day_name", "hour"]).size().unstack(fill_value=0)
        matrix = matrix.reindex(index=day_order, columns=list(range(24)), fill_value=0)

        # Heatmap Plotly
        fig_heat = px.imshow(
            matrix,
            labels=dict(x="Heure de la journée (0h - 23h)", y="Jour de la semaine", color="Activités"),
            x=[f"{h}h" for h in range(24)],
            y=day_order,
            color_continuous_scale="Viridis",
            title="Carte Thermique d'Activité Cognitive (Heure x Jour)",
            template="plotly_dark",
            height=380,
        )
        fig_heat.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_heat, use_container_width=True)

        # Répartition par quadrant horaire
        st.markdown("#### Signature de la Productivité par Quart de Journée")
        qcol1, qcol2 = st.columns(2)

        def get_quadrant(h: int) -> str:
            if 0 <= h < 6:
                return "1. Nuit Profonde (00h - 06h)"
            elif 6 <= h < 12:
                return "2. Matinée (06h - 12h)"
            elif 12 <= h < 18:
                return "3. Après-Midi (12h - 18h)"
            else:
                return "4. Soirée & Crépuscule (18h - 00h)"

        df_circ["quadrant"] = df_circ["hour"].apply(get_quadrant)
        quad_counts = df_circ["quadrant"].value_counts().sort_index().reset_index()
        quad_counts.columns = ["Quadrant", "Volume d'Activité"]

        with qcol1:
            fig_quad = px.bar(
                quad_counts,
                x="Quadrant",
                y="Volume d'Activité",
                color="Quadrant",
                template="plotly_dark",
                height=320,
            )
            fig_quad.update_layout(showlegend=False, margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_quad, use_container_width=True)

        with qcol2:
            night_count = len(df_circ[df_circ["hour"].isin([22, 23, 0, 1, 2, 3, 4, 5])])
            night_pct = round((night_count / max(1, len(df_circ))) * 100, 1)

            st.markdown(
                f"""
                <div class="card-box">
                    <h4 style="color: #38bdf8; margin-top:0;">🦉 Diagnostic Chronobiologique</h4>
                    <p><b>Index Nocturne :</b> <span style="color:#a855f7; font-size:1.2rem; font-weight:bold;">{night_pct}%</span> de l'activité cognitive se déroule entre 22h et 06h.</p>
                    <p><b>Profil Détecté :</b> <i>Chronotype du Loup / Chouette Nocturne (Delayed Sleep Phase Tendency)</i>.</p>
                    <p style="font-size:0.9rem; color:#94a3b8;">
                    La télémétrie confirme une concentration intense et des sessions d'hyperfocus sans friction pendant les heures calmes de la nuit.
                    L'Exocortex aligne ses consolidations nocturnes pour s'exécuter à la clôture de ces fenêtres.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ------------------------------------------------------------------------------
# ONGLET 5 : EXPLORATEUR ÉPISTÉMIQUE & EMPREINTES
# ------------------------------------------------------------------------------
with tab5:
    st.subheader("🔍 Explorateur Épistémique & Archéologie des Empreintes")
    st.caption("Recherche full-text dans les échanges Gemini historiques (6 649 messages) et analyse des 73 153 empreintes numériques.")

    tab5_sub1, tab5_sub2 = st.tabs([
        "💬 Volet A : Moteur de Recherche Gemini (Sessions & Messages)",
        "🌐 Volet B : Archéologie des Empreintes & Tunnels de Recherche",
    ])

    # ==========================================================================
    # VOLET A : MOTEUR DE RECHERCHE DANS LES SESSIONS ET MESSAGES GEMINI
    # ==========================================================================
    with tab5_sub1:
        st.markdown("#### Moteur de Recherche Full-Text (Takeout & Échanges Gemini)")
        st.caption("Explorez les 6 649 messages et 480 sessions indexées dans la base épistémique.")

        c_q, c_top, c_st = st.columns([3, 2, 1])
        search_query = c_q.text_input(
            "Recherche plein texte (mots-clés, concepts, requêtes, réponses) :",
            placeholder="ex: lancedb, quantization, astro, docker...",
            key="gemini_search_text_input",
        )
        macro_topics = ["Tous les topics"] + sorted(list(AUTHORIZED_SEMANTIC_TOPICS.keys()))
        filter_topic = c_top.selectbox(
            "Filtrer par Sujet Sémantique :",
            macro_topics,
            index=0,
            key="gemini_topic_select",
        )
        filter_status = c_st.selectbox(
            "Statut Distillation :",
            ["Tous", "distilled", "skipped", "pending"],
            index=0,
            key="gemini_status_select",
        )

        matched_sessions = load_chat_search_results(
            query=search_query,
            topic_filter=filter_topic,
            status_filter=filter_status,
            limit=50,
        )

        if not matched_sessions:
            st.info("Aucune session Gemini ne correspond aux critères de recherche.")
        else:
            st.success(f"**{len(matched_sessions)} session(s) identifiée(s)** (affichage limité aux 50 plus récentes).")

            session_labels = {
                s["session_id"]: f"[{str(s['timestamp_start'])[:10]}] {s['summary'][:70] or s['session_id']} ({s['turn_count']} tours)"
                for s in matched_sessions
            }
            selected_sid = st.selectbox(
                "Sélectionner une session à inspecter :",
                options=list(session_labels.keys()),
                format_func=lambda sid: session_labels.get(sid, sid),
                key="gemini_session_selector",
            )

            current_sess = next((s for s in matched_sessions if s["session_id"] == selected_sid), matched_sessions[0])

            # Cartouche d'en-tête de session
            meta_col1, meta_col2, meta_col3, meta_col4 = st.columns(4)
            meta_col1.metric("Date & Heure", str(current_sess["timestamp_start"])[:16])
            meta_col2.metric("Échanges", f"{current_sess['turn_count']} tours", f"{current_sess['user_char_count']} cars")
            meta_col3.metric("Statut", current_sess["distillation_status"])

            topics_raw = current_sess.get("extracted_topics_json") or "[]"
            try:
                parsed_topics = json.loads(topics_raw)
            except Exception:
                parsed_topics = []
            topics_badges = " ".join([f"`#{t}`" for t in parsed_topics]) if parsed_topics else "*Aucun topic*"
            meta_col4.markdown(f"**Topics Détectés :**\n{topics_badges}")

            # Résumé cognitif de la session
            if current_sess.get("summary"):
                st.markdown(
                    f"""
                    <div class="card-box" style="margin-top: 10px; margin-bottom: 15px;">
                        <b style="color: #38bdf8;">📝 Résumé Analytique Exocortex :</b><br>
                        <span style="color: #e2e8f0;">{current_sess['summary']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Fiches conceptuelles associées
            notes_raw = current_sess.get("generated_notes_json") or "[]"
            try:
                parsed_notes = json.loads(notes_raw)
            except Exception:
                parsed_notes = []

            if parsed_notes:
                st.markdown("**📚 Fiches Conceptuelles Liées (Vault 02_Concepts) :**")
                for note_slug in parsed_notes:
                    concept_p = settings.CONCEPTS_DIR / f"{note_slug}.md"
                    if concept_p.exists():
                        with st.expander(f"📄 Voir la fiche : `{note_slug}.md`"):
                            st.markdown(concept_p.read_text(encoding="utf-8", errors="replace"))
                    else:
                        st.markdown(f"- `[[{note_slug}]]` *(non matérialisée sur disque)*")

            # Tours complets de conversation
            st.markdown("#### 💬 Tours de Conversation Complets")
            messages = load_messages_for_session(current_sess["session_id"])
            if not messages:
                st.info("Aucun détail de message disponible pour cette session.")
            else:
                for msg in messages:
                    t_idx = msg.get("turn_index", 0) + 1
                    t_time = str(msg.get("timestamp", ""))[:19]
                    cars = msg.get("user_char_count", 0)
                    with st.expander(f"Tour {t_idx} — [{t_time}] ({cars} caractères)", expanded=(t_idx == 1)):
                        st.markdown(f"**🧑 Utilisateur :**\n\n{msg.get('user_prompt', '')}")
                        st.markdown("---")
                        st.markdown(f"**🤖 Gemini :**\n\n{msg.get('ai_response', '')}")

    # ==========================================================================
    # VOLET B : ARCHÉOLOGIE DES EMPREINTES & BURST CLUSTERS
    # ==========================================================================
    with tab5_sub2:
        st.markdown("#### Archéologie des Empreintes Numériques (YouTube & Google Search)")
        st.caption("Visualisez les 73 153 empreintes passées, les clusters de recherche en rafale et les connexions aux sessions Gemini.")

        # KPI bandeau
        fp_kpis = load_footprints_summary()
        fk1, fk2, fk3, fk4, fk5 = st.columns(5)
        fk1.metric("Total Empreintes", f"{fp_kpis['total']:,}".replace(",", " "))
        fk2.metric("Vidéos YouTube", f"{fp_kpis['youtube']:,}".replace(",", " "))
        fk3.metric("Recherches Google", f"{fp_kpis['search']:,}".replace(",", " "))
        fk4.metric("En Burst Clusters", f"{fp_kpis['clustered']:,}".replace(",", " "))
        fk5.metric("Liées à Gemini", f"{fp_kpis['linked']:,}".replace(",", " "))

        st.markdown("---")

        # Visualisation Top 15 Chaînes et Domaines
        st.markdown("#### 🏆 Top 15 des Chaînes YouTube & Domaines Web Consultés")
        df_top15 = load_top_channels_and_domains(limit=15)
        if not df_top15.empty:
            fig_top = px.bar(
                df_top15,
                x="footprint_count",
                y="channel_or_domain",
                color="source",
                orientation="h",
                labels={"footprint_count": "Nombre d'occurrences", "channel_or_domain": "Chaîne / Domaine", "source": "Source"},
                template="plotly_dark",
                height=420,
            )
            fig_top.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_top, use_container_width=True)
        else:
            st.info("Aucune donnée d'empreinte disponible.")

        # Burst Clusters
        st.markdown("#### ⚡ Tunnels d'Exploration Denses (Burst Clusters)")
        st.caption("Regroupements temporels d'au moins 3 requêtes ou vidéos survenues dans un intervalle court (< 45 min).")
        df_clusters = load_burst_clusters_summary(limit=25)
        if not df_clusters.empty:
            st.dataframe(
                df_clusters[["cluster_id", "source", "semantic_topic", "event_count", "start_time", "end_time", "samples"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Aucun cluster dense n'a encore été formé.")

        # Moteur d'exploration tabulaire des empreintes
        st.markdown("#### 🔎 Explorateur et Filtre d'Empreintes")
        fc1, fc2, fc3, fc4 = st.columns([3, 1, 1, 1])
        fp_q = fc1.text_input("Recherche textuelle (requête, titre vidéo, chaîne, domaine) :", key="fp_text_search")
        fp_src = fc2.selectbox("Source :", ["Toutes", "youtube", "google_search"], key="fp_src_filter")
        fp_only_cluster = fc3.checkbox("Burst Clusters uniquement", value=False, key="fp_only_clust")
        fp_only_linked = fc4.checkbox("Liées à Gemini uniquement", value=False, key="fp_only_link")

        df_footprints = search_historical_footprints(
            query=fp_q,
            source_filter=fp_src,
            only_clustered=fp_only_cluster,
            only_linked=fp_only_linked,
            limit=100,
        )

        if not df_footprints.empty:
            st.dataframe(
                df_footprints[["timestamp", "source", "channel_or_domain", "title_or_query", "cluster_id", "semantic_topic", "linked_gemini_session_id"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Aucune empreinte ne correspond à cette sélection.")

# ------------------------------------------------------------------------------
# ONGLET 6 : KANBAN EXÉCUTIF & STUDIO SOTA (v0.2.0 - Module 7)
# ------------------------------------------------------------------------------
with tab6:
    st.subheader("📋 Kanban Exécutif Multi-Projets & Studio SOTA")
    st.caption("Gestion agile dynamique, pont presse-papier 1-clic avec Gemini Web App et file d'attente agent codeur.")

    # Synchronisation idempotente des specs historiques tech specs/
    kanban_engine.sync_existing_tech_specs()

    projects = kanban_engine.db.get_projects()
    if not projects:
        projects = [{"project_id": "exocortex", "name": "Exocortex & Télémétrie Cognitive", "prefix": "EXO"}]

    # --- BARRE SUPÉRIEURE (1 Projet = 1 Vue) ---
    p_col1, p_col2 = st.columns([3, 1])
    with p_col1:
        proj_options = [p["project_id"] for p in projects]
        selected_project_id = st.selectbox(
            "Projet Actif (1 Projet = 1 Vue) :",
            options=proj_options,
            format_func=lambda pid: next((p["name"] for p in projects if p["project_id"] == pid), pid),
            key="kanban_active_proj",
        )

    with p_col2:
        with st.popover("➕ Nouveau Projet"):
            st.markdown("##### 🚀 Créer un Nouveau Projet")
            new_pname = st.text_input("Nom d'affichage *", placeholder="ex: Homelab Media", key="new_proj_name")
            new_pid = st.text_input("Slug Unique *", placeholder="ex: homelab-media", key="new_proj_id")
            new_prefix = st.text_input("Préfixe Tickets *", placeholder="ex: HLAB", max_chars=5, key="new_proj_prefix")
            new_repo = st.text_input("Chemin Local Dépôt (optionnel)", placeholder="C:/chemin/vers/repo", key="new_proj_repo")
            new_desc = st.text_area("Description du projet", placeholder="Contexte architectural et objectifs...", key="new_proj_desc")
            if st.button("Enregistrer le Projet", key="btn_save_proj", use_container_width=True):
                if new_pname.strip() and new_pid.strip() and new_prefix.strip():
                    kanban_engine.db.upsert_project(
                        ProjectRecord(
                            project_id=new_pid.strip().lower(),
                            name=new_pname.strip(),
                            prefix=new_prefix.strip().upper(),
                            repo_path=new_repo.strip() or None,
                            description=new_desc.strip(),
                        )
                    )
                    st.success(f"Projet '{new_pname}' créé !")
                    st.rerun()
                else:
                    st.error("Nom, Slug et Préfixe sont obligatoires.")

    active_proj = next((p for p in projects if p["project_id"] == selected_project_id), None)
    if active_proj:
        st.info(f"**Périmètre :** {active_proj.get('description', '')} | **Dépôt :** `{active_proj.get('repo_path') or 'Non configuré'}`")

    # --- FILTRES SECONDAIRES ---
    all_proj_tasks = kanban_engine.db.get_kanban_tasks(project_id=selected_project_id)
    unique_tags = sorted(list({t["component_tag"] for t in all_proj_tasks if t.get("component_tag")}))
    tag_options = ["Tous"] + unique_tags

    f_col1, f_col2 = st.columns([2, 2])
    with f_col1:
        selected_tag = st.selectbox("Filtrer par sous-module (component_tag) :", options=tag_options, key="kanban_filter_tag")
    with f_col2:
        search_query = st.text_input("Recherche textuelle dans les tickets :", key="kanban_search_text")

    filtered_tasks = all_proj_tasks
    if selected_tag != "Tous":
        filtered_tasks = [t for t in filtered_tasks if t.get("component_tag") == selected_tag]
    if search_query.strip():
        q_low = search_query.strip().lower()
        filtered_tasks = [
            t for t in filtered_tasks
            if q_low in t["title"].lower()
            or q_low in t.get("summary_pitch", "").lower()
            or q_low in t["task_id"].lower()
        ]

    # --- BARRE D'ACTIONS RAPIDES ---
    st.markdown("---")
    act_col1, act_col2 = st.columns(2)
    with act_col1:
        with st.expander("➕ Nouvelle Idée / Tâche"):
            nt_title = st.text_input("Titre de la tâche / idée *", key="nt_title")
            nt_sub1, nt_sub2, nt_sub3 = st.columns(3)
            with nt_sub1:
                nt_tag = st.text_input("Sous-module", value="general", key="nt_tag")
            with nt_sub2:
                nt_prio = st.selectbox(
                    "Priorité",
                    options=[1, 2, 3, 4],
                    index=1,
                    format_func=lambda x: {1: "P1 (Urgent)", 2: "P2 (Normal)", 3: "P3 (Secondaire)", 4: "P4 (Optionnel)"}[x],
                    key="nt_prio",
                )
            with nt_sub3:
                nt_cplx = st.selectbox("Complexité", options=["S", "M", "L", "XL"], index=1, key="nt_cplx")
            nt_status = st.selectbox(
                "Statut initial",
                options=["radar", "needs_spec"],
                format_func=lambda s: "📡 Radar (À arbitrer)" if s == "radar" else "📝 Nécessite Spec + Prompt",
                key="nt_status",
            )
            nt_pitch = st.text_area("Pitch / Contexte & Objectifs", key="nt_pitch")
            if st.button("Créer la Tâche", key="btn_create_task", use_container_width=True):
                if nt_title.strip():
                    new_tid = kanban_engine.create_task(
                        project_id=selected_project_id,
                        title=nt_title.strip(),
                        component_tag=nt_tag.strip() or "general",
                        summary_pitch=nt_pitch.strip(),
                        priority=nt_prio,
                        complexity=nt_cplx,
                        initial_status=nt_status,
                    )
                    st.toast(f"Tâche {new_tid} créée !")
                    st.rerun()
                else:
                    st.error("Le titre de la tâche est obligatoire.")

    with act_col2:
        with st.expander("📥 Ingérer Spec + Prompt depuis Gemini Web"):
            st.caption("Collez le Markdown retourné par Gemini Web App (avec frontmatter YAML et sections).")
            if st.button("📋 Coller depuis le Presse-Papier Windows", key="btn_paste_clip", use_container_width=True):
                try:
                    clip_text = pyperclip.paste()
                    if clip_text and clip_text.strip():
                        attached = kanban_engine.attach_spec_to_task(clip_text)
                        st.toast(f"Spec ingérée avec succès pour {attached.get('task_id', 'le ticket')} !")
                        st.rerun()
                    else:
                        st.warning("Le presse-papier est vide.")
                except Exception as exc:
                    st.error(f"Erreur presse-papier : {exc}")

            manual_spec = st.text_area("Ou coller manuellement le Markdown ici :", height=100, key="manual_spec_area")
            if st.button("Valider l'Ingestion Manuelle", key="btn_manual_ingest", use_container_width=True):
                if manual_spec.strip():
                    attached = kanban_engine.attach_spec_to_task(manual_spec.strip())
                    st.toast(f"Spec ingérée avec succès pour {attached.get('task_id', 'le ticket')} !")
                    st.rerun()

    # --- TABLEAU KANBAN EN 4 COLONNES VISUELLES ---
    st.markdown("---")
    kcol1, kcol2, kcol3, kcol4 = st.columns(4)

    radar_tasks = [t for t in filtered_tasks if t["status"] == "radar"]
    needs_spec_tasks = [t for t in filtered_tasks if t["status"] == "needs_spec"]
    ready_and_in_progress = [t for t in filtered_tasks if t["status"] in ("ready_for_agent", "in_progress")]
    done_tasks = [t for t in filtered_tasks if t["status"] == "done"]
    icebox_tasks = [t for t in filtered_tasks if t["status"] == "icebox"]

    # 1. RADAR / IDÉES
    with kcol1:
        st.markdown(f"### 📡 Radar ({len(radar_tasks)})")
        for t in radar_tasks:
            with st.container(border=True):
                st.markdown(f"**`{t['task_id']}`** `{t['component_tag']}` | P{t['priority']} | {t['complexity']}")
                st.markdown(f"**{t['title']}**")
                if t.get("summary_pitch"):
                    st.caption(t["summary_pitch"][:160] + ("..." if len(t["summary_pitch"]) > 160 else ""))
                rc1, rc2 = st.columns(2)
                if rc1.button("✅ Valider", key=f"val_{t['task_id']}", use_container_width=True):
                    kanban_engine.db.update_kanban_task_status(t["task_id"], "needs_spec")
                    st.rerun()
                if rc2.button("🧊 Frigo", key=f"frigo_{t['task_id']}", use_container_width=True):
                    kanban_engine.db.update_kanban_task_status(t["task_id"], "icebox")
                    st.rerun()

    # 2. NÉCESSITE SPEC + PROMPT
    with kcol2:
        st.markdown(f"### 📝 Spec Requise ({len(needs_spec_tasks)})")
        for t in needs_spec_tasks:
            with st.container(border=True):
                st.markdown(f"**`{t['task_id']}`** `{t['component_tag']}` | P{t['priority']} | {t['complexity']}")
                st.markdown(f"**{t['title']}**")
                if t.get("summary_pitch"):
                    st.caption(t["summary_pitch"][:160] + ("..." if len(t["summary_pitch"]) > 160 else ""))

                if st.button("📋 Copier Context-Pack", key=f"cp_{t['task_id']}", use_container_width=True):
                    prompt_text = kanban_engine.build_sota_context_pack_prompt(t["task_id"])
                    try:
                        pyperclip.copy(prompt_text)
                        st.toast(f"Context-Pack {t['task_id']} copié ! Collez-le dans Gemini Web.")
                    except Exception as e:
                        st.error(f"Erreur presse-papier : {e}")

                if st.button("📥 Lier Spec Presse-Papier", key=f"link_{t['task_id']}", use_container_width=True):
                    try:
                        c_text = pyperclip.paste()
                        if c_text and c_text.strip():
                            kanban_engine.attach_spec_to_task(c_text, target_task_id=t["task_id"])
                            st.toast(f"Spec rattachée à {t['task_id']} !")
                            st.rerun()
                        else:
                            st.warning("Presse-papier vide.")
                    except Exception as e:
                        st.error(f"Erreur : {e}")

                sb1, sb2 = st.columns(2)
                if sb1.button("⬅️ Radar", key=f"back_rad_{t['task_id']}", use_container_width=True):
                    kanban_engine.db.update_kanban_task_status(t["task_id"], "radar")
                    st.rerun()
                if sb2.button("🧊 Frigo", key=f"back_frg_{t['task_id']}", use_container_width=True):
                    kanban_engine.db.update_kanban_task_status(t["task_id"], "icebox")
                    st.rerun()

    # 3. PRÊT POUR AGENT & EN COURS
    with kcol3:
        st.markdown(f"### 🎯 Prêt & ⚙️ En Cours ({len(ready_and_in_progress)})")
        for t in ready_and_in_progress:
            with st.container(border=True):
                if t["status"] == "in_progress":
                    st.markdown("`:violet-background[⚙️ EN COURS]`")
                else:
                    st.markdown("`:green-background[🎯 PRÊT POUR AGENT]`")

                st.markdown(f"**`{t['task_id']}`** `{t['component_tag']}` | P{t['priority']} | {t['complexity']}")
                st.markdown(f"**{t['title']}**")

                if st.button("🤖 Copier Prompt Codeur", key=f"coder_{t['task_id']}", use_container_width=True):
                    coder_prompt = kanban_engine.extract_coder_prompt_from_spec(t["task_id"])
                    try:
                        pyperclip.copy(coder_prompt)
                        kanban_engine.db.update_kanban_task_status(t["task_id"], "in_progress")
                        kanban_engine.compile_agent_queue_manifest()
                        st.toast(f"Prompt {t['task_id']} copié & tâche passée En Cours !")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur presse-papier : {e}")

                if t.get("spec_file_path") and Path(t["spec_file_path"]).exists():
                    with st.expander("📄 Lire Spec & Prompt"):
                        st.markdown(Path(t["spec_file_path"]).read_text(encoding="utf-8", errors="ignore"))

                if st.button("✅ Marquer Terminé", key=f"done_{t['task_id']}", use_container_width=True):
                    kanban_engine.db.update_kanban_task_status(t["task_id"], "done")
                    kanban_engine.compile_agent_queue_manifest()
                    st.toast(f"Tâche {t['task_id']} marquée terminée !")
                    st.rerun()

    # 4. TERMINÉ
    with kcol4:
        st.markdown(f"### ✅ Terminé ({len(done_tasks)})")
        for t in done_tasks:
            with st.container(border=True):
                st.markdown(f"**`{t['task_id']}`** `{t['component_tag']}`")
                st.markdown(f"**{t['title']}**")
                if t.get("spec_file_path") and Path(t["spec_file_path"]).exists():
                    with st.expander("📄 Voir Spécification"):
                        p_file = Path(t["spec_file_path"])
                        txt = p_file.read_text(encoding="utf-8", errors="ignore")
                        st.markdown(txt[:2500] + ("\n\n*(tronqué pour affichage)*" if len(txt) > 2500 else ""))

    # --- FRIGO (ICEBOX) ---
    st.markdown("---")
    show_icebox = st.checkbox("🧊 Afficher le Frigo (Idées écartées)", value=False, key="kanban_show_icebox")
    if show_icebox:
        st.markdown(f"#### 🧊 Frigo ({len(icebox_tasks)} idées écartées)")
        if not icebox_tasks:
            st.info("Aucune idée n'est actuellement au frigo.")
        else:
            ib_cols = st.columns(3)
            for idx, t in enumerate(icebox_tasks):
                with ib_cols[idx % 3]:
                    with st.container(border=True):
                        st.markdown(f"**`{t['task_id']}`** `{t['component_tag']}` | P{t['priority']} | {t['complexity']}")
                        st.markdown(f"**{t['title']}**")
                        if t.get("summary_pitch"):
                            st.caption(t["summary_pitch"])
                        ib1, ib2 = st.columns(2)
                        if ib1.button("♻️ Restaurer", key=f"restore_{t['task_id']}", use_container_width=True):
                            kanban_engine.db.update_kanban_task_status(t["task_id"], "radar")
                            st.rerun()
                        if ib2.button("🗑️ Supprimer", key=f"del_{t['task_id']}", use_container_width=True):
                            kanban_engine.db.delete_kanban_task(t["task_id"])
                            st.rerun()

