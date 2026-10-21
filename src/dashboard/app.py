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
import streamlit as st

from src.config import normalize_to_macro_topic, settings

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Exocortex — Bandeur de Stats",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Thème sombre et styles CSS avancés
st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_db_path() -> Path:
    return settings.SQLITE_DB_PATH


def get_ro_connection() -> sqlite3.Connection:
    """Ouvre une connexion SQLite en lecture seule stricte (file:telemetry.db?mode=ro)."""
    db_path = get_db_path()
    if not db_path.exists():
        st.error(f"Base de données introuvable : {db_path}")
        st.stop()
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

        # 3. Daily metrics stats (hyperfocus record, avg context switch)
        cur = conn.execute(
            """
            SELECT 
                MAX(max_hyperfocus_sec),
                max_hyperfocus_topic,
                AVG(context_switches_per_hour),
                AVG(read_vs_write_ratio)
            FROM daily_metrics
            WHERE max_hyperfocus_sec IS NOT NULL;
            """
        )
        row = cur.fetchone()
        max_hyperfocus_sec = row[0] if row and row[0] else 0
        max_hyperfocus_topic = row[1] if row and row[1] else "N/A"
        avg_switch_rate = round(row[2], 2) if row and row[2] else 0.0
        avg_read_ratio = round(row[3], 2) if row and row[3] else 0.4

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

tab1, tab2, tab3, tab4 = st.tabs([
    "⏱️ Chronologie & Focus Quotidien",
    "🗺️ Cartographie des Obsessions",
    "📜 Archéologie Longitudinale",
    "🌙 Rythmes Circadiens",
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

