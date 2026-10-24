"""
Calculs cognitifs partagés par la consolidation nocturne, l'API web et le dashboard Streamlit
(v0.5.4, B1/B3/B7/B9) : une seule définition des tunnels d'hyperfocus, de l'état du DriftGuard,
des KPIs journaliers et du diagnostic circadien, pour que les trois interfaces affichent les
mêmes chiffres.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional

from pydantic import BaseModel, Field

from src.config import normalize_cognitive_mode

UNCLASSIFIED_TOPIC = "Non_Classe"
MICRO_INTERRUPTION_TOLERANCE_SEC = 120
HYPERFOCUS_TUNNEL_MIN_SEC = 1800
DRIFT_ALERT_ACTIVE_WINDOW_SEC = 3600


def _as_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value).replace("Z", "+00:00")).replace(tzinfo=None)


# ==============================================================================
# TUNNELS D'HYPERFOCUS (B7)
# ==============================================================================

class FocusTunnel(BaseModel):
    """Bloc de concentration continu sur un même semantic_topic."""
    topic: str
    start_time: str
    end_time: str
    duration_sec: int
    executable: str = Field(description="Exécutable dominant du tunnel")
    top_window_title: str = Field(description="Fenêtre la plus longue du tunnel")
    activity_count: int


def compute_focus_tunnels(
    activities: Iterable[Dict[str, Any]],
    tolerance_sec: int = MICRO_INTERRUPTION_TOLERANCE_SEC,
) -> List[FocusTunnel]:
    """
    Fusionne les activités consécutives d'un même topic en tunnels. Une interruption de moins de
    tolerance_sec sur un autre topic est absorbée si l'activité suivante revient au topic du tunnel.
    """
    sorted_acts = sorted(activities, key=lambda a: _as_datetime(a["timestamp_start"]))
    tunnels: List[FocusTunnel] = []
    current: Optional[Dict[str, Any]] = None
    pending_interruption = 0

    def close(t: Dict[str, Any]) -> None:
        exe = max(t["exe_secs"].items(), key=lambda kv: kv[1])[0] if t["exe_secs"] else ""
        tunnels.append(FocusTunnel(
            topic=t["topic"],
            start_time=t["start"].strftime("%Y-%m-%d %H:%M:%S"),
            end_time=t["end"].strftime("%Y-%m-%d %H:%M:%S"),
            duration_sec=t["duration"],
            executable=exe,
            top_window_title=t["top_title"][1],
            activity_count=t["count"],
        ))

    def start(act: Dict[str, Any], topic: str) -> Dict[str, Any]:
        dur = int(act.get("duration_sec") or 0)
        return {
            "topic": topic,
            "start": _as_datetime(act["timestamp_start"]),
            "end": _as_datetime(act["timestamp_end"]),
            "duration": dur,
            "exe_secs": {act.get("executable") or "": dur},
            "top_title": (dur, act.get("window_title") or ""),
            "count": 1,
        }

    for idx, act in enumerate(sorted_acts):
        topic = act.get("semantic_topic") or UNCLASSIFIED_TOPIC
        dur = int(act.get("duration_sec") or 0)

        if current is None:
            current = start(act, topic)
            continue

        if topic == current["topic"]:
            current["duration"] += dur + pending_interruption
            pending_interruption = 0
            current["end"] = _as_datetime(act["timestamp_end"])
            exe = act.get("executable") or ""
            current["exe_secs"][exe] = current["exe_secs"].get(exe, 0) + dur
            if dur > current["top_title"][0]:
                current["top_title"] = (dur, act.get("window_title") or "")
            current["count"] += 1
            continue

        next_topic = (sorted_acts[idx + 1].get("semantic_topic") or UNCLASSIFIED_TOPIC) if idx + 1 < len(sorted_acts) else None
        if dur < tolerance_sec and next_topic == current["topic"]:
            pending_interruption += dur
            continue

        close(current)
        current = start(act, topic)
        pending_interruption = 0

    if current is not None:
        close(current)
    return tunnels


# ==============================================================================
# KPIs JOURNALIERS (B1)
# ==============================================================================

class DailyKpis(BaseModel):
    """Contrat unique des KPIs du jour renvoyés par /api/telemetry/timeline."""
    date: str
    is_consolidated: bool = Field(description="Vrai si une ligne daily_metrics existe pour cette date")
    total_active_sec: int
    total_deep_work_sec: int = Field(description="Production active (mode production avec saisie)")
    hyperfocus_tunnel_count: int
    max_hyperfocus_sec: int
    max_hyperfocus_topic: Optional[str] = None
    total_chat_turns: int
    context_switches_per_hour: float


def build_daily_kpis(
    date_str: str,
    events: List[Dict[str, Any]],
    tunnels: List[FocusTunnel],
    chat_turns: int,
    daily_metric_row: Optional[Dict[str, Any]] = None,
) -> DailyKpis:
    """Construit les KPIs du jour, que la journée soit consolidée (daily_metrics) ou non."""
    long_tunnels = [t for t in tunnels if t.duration_sec >= HYPERFOCUS_TUNNEL_MIN_SEC]
    best = max(tunnels, key=lambda t: t.duration_sec, default=None)
    if daily_metric_row:
        return DailyKpis(
            date=date_str,
            is_consolidated=True,
            total_active_sec=int(daily_metric_row.get("total_screen_sec") or 0),
            total_deep_work_sec=int(daily_metric_row.get("active_production_sec") or 0),
            hyperfocus_tunnel_count=len(long_tunnels),
            max_hyperfocus_sec=int(daily_metric_row.get("max_hyperfocus_sec") or 0),
            max_hyperfocus_topic=daily_metric_row.get("max_hyperfocus_topic"),
            total_chat_turns=chat_turns,
            context_switches_per_hour=float(daily_metric_row.get("context_switches_per_hour") or 0.0),
        )
    total = sum(int(e.get("duration_sec") or 0) for e in events)
    deep = sum(
        int(e.get("duration_sec") or 0) for e in events
        if normalize_cognitive_mode(e.get("cognitive_mode")) == "production" and e.get("active_input")
    )
    hours = max(0.1, total / 3600.0)
    return DailyKpis(
        date=date_str,
        is_consolidated=False,
        total_active_sec=total,
        total_deep_work_sec=deep,
        hyperfocus_tunnel_count=len(long_tunnels),
        max_hyperfocus_sec=best.duration_sec if best else 0,
        max_hyperfocus_topic=best.topic if best else None,
        total_chat_turns=chat_turns,
        context_switches_per_hour=round(max(0, len(tunnels) - 1) / hours, 2),
    )


# ==============================================================================
# ÉTAT DU DRIFTGUARD (B3)
# ==============================================================================

class DriftStatus(BaseModel):
    """État stable du DriftGuard : `active` vaut vrai si une alerte date de moins d'une heure."""
    active: bool = False
    drift_type: Optional[str] = None
    diagnostic: Optional[str] = None
    severity: Optional[str] = None
    detected_at: Optional[str] = None
    cooldown_until: Optional[str] = None


def compute_drift_status(raw_state: Optional[Dict[str, Any]], now: Optional[datetime] = None) -> DriftStatus:
    """Interprète drift_state.json (écrit par le démon) en un objet stable pour les interfaces."""
    if not raw_state or not raw_state.get("active_alert"):
        return DriftStatus()
    now = now or datetime.now()
    active = False
    detected = raw_state.get("detected_at")
    if detected:
        try:
            active = (now - _as_datetime(detected)) < timedelta(seconds=DRIFT_ALERT_ACTIVE_WINDOW_SEC)
        except ValueError:
            active = False
    return DriftStatus(
        active=active,
        drift_type=raw_state.get("drift_type"),
        diagnostic=raw_state.get("diagnostic"),
        severity=raw_state.get("severity"),
        detected_at=detected,
        cooldown_until=raw_state.get("cooldown_until"),
    )


# ==============================================================================
# DIAGNOSTIC CIRCADIEN (B9)
# ==============================================================================

CIRCADIAN_PROFILES = {
    "Nuit Profonde (00h - 06h)": ("Profil nocturne", "L'activité se concentre entre minuit et 6 h."),
    "Matinée (06h - 12h)": ("Profil matinal", "L'activité se concentre entre 6 h et midi."),
    "Après-Midi (12h - 18h)": ("Profil diurne", "L'activité se concentre entre midi et 18 h."),
    "Soirée & Crépuscule (18h - 00h)": ("Profil crépusculaire", "L'activité se concentre entre 18 h et minuit."),
}
CIRCADIAN_DOMINANCE_THRESHOLD = 0.40


def diagnose_circadian(quadrants: Dict[str, int]) -> Dict[str, Any]:
    """
    Déduit le profil des données au lieu d'un libellé figé : un quadrant est dit dominant s'il
    réunit au moins 40 % des horodatages ; sinon le profil est « réparti ».
    """
    total = sum(quadrants.values())
    if total == 0:
        return {"label": "Données insuffisantes", "description": "Aucun horodatage à analyser.", "dominant_share": 0.0}
    dominant, count = max(quadrants.items(), key=lambda kv: kv[1])
    share = count / total
    if share >= CIRCADIAN_DOMINANCE_THRESHOLD and dominant in CIRCADIAN_PROFILES:
        label, description = CIRCADIAN_PROFILES[dominant]
    else:
        label, description = "Profil réparti", "Aucune plage horaire ne réunit 40 % de l'activité."
    return {"label": label, "description": f"{description} ({share:.0%} des horodatages).", "dominant_share": round(share, 3)}
