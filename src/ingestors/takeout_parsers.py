"""
Module de parsers déterministes pour Google Takeout (Gemini HTML/JSON, YouTube, Google Search).
Isole la logique bas niveau de découpage HTML/JSON et de reconstruction chronologique des sessions.
"""

from __future__ import annotations

import html
import json
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from pydantic import BaseModel, Field

from src.config import settings
from src.database.db_manager import HistoricalFootprintRecord

logger = logging.getLogger("Exocortex.TakeoutParsers")


# ==============================================================================
# MODÈLES DE TOURS ET SESSIONS
# ==============================================================================

class ParsedTurn(BaseModel):
    """Représente un tour d'échange individuel extrait d'un export."""
    session_id: Optional[str] = None
    timestamp: datetime
    user_prompt: str
    ai_response: str = ""
    user_char_count: int = 0
    url: Optional[str] = None


class ReconstructedSession(BaseModel):
    """Représente une session Gemini reconstituée et chronologiquement ordonnée."""
    session_id: str
    timestamp_start: datetime
    timestamp_end: datetime
    turns: List[ParsedTurn]
    turn_count: int
    user_char_count: int
    summary: str


# ==============================================================================
# NETTOYAGE ET CALCUL DE DURÉE RÉALISTE
# ==============================================================================

def sanitize_turn_text(text: str, max_turn_chars: int = 3500) -> str:
    """
    Purge les dumps d'interfaces copiés-collés (menus HTML/DOM), les tracebacks répétitifs
    et les espaces insécables multiples avant envoi au LLM.
    """
    if not text:
        return ""
    cleaned = re.sub(r"(?:[\t \xa0]{4,}\n){3,}", "\n[Dump d'interface UI omis]\n", text)
    lines = cleaned.splitlines()
    if len(lines) > 35:
        filtered_lines: List[str] = []
        log_streak = 0
        for line in lines:
            is_log_line = any(
                pat in line
                for pat in ["Traceback", "File \"", "at FluentMigrator", "sqlalchemy.exc", "ggml_", "llama_model_loader", "   at "]
            )
            if is_log_line:
                log_streak += 1
                if log_streak <= 6:
                    filtered_lines.append(line)
                elif log_streak == 7:
                    filtered_lines.append("... [Stacktrace / Log technique tronqué pour lisibilité] ...")
            else:
                log_streak = 0
                filtered_lines.append(line)
        cleaned = "\n".join(filtered_lines)

    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    if len(cleaned) > max_turn_chars:
        cleaned = cleaned[:max_turn_chars] + "\n...[Contenu long tronqué]..."
    return cleaned


def compute_realistic_session_duration_min(turns: List[ParsedTurn], max_gap_min: int = 15) -> int:
    """
    Calcule le temps réel investi dans une session en additionnant les intervalles
    entre deux échanges consécutifs, plafonnés à `max_gap_min` (15 min) par tour,
    plus 3 minutes de lecture/rédaction de base pour le premier tour.
    """
    if not turns:
        return 0
    total_sec = 180.0
    max_gap_sec = max_gap_min * 60.0
    for i in range(1, len(turns)):
        delta_sec = max(0.0, (turns[i].timestamp - turns[i - 1].timestamp).total_seconds())
        total_sec += min(delta_sec, max_gap_sec)
    return max(5, int(round(total_sec / 60.0)))


# ==============================================================================
# UTILITAIRE DE PARSING DE DATES MULTI-FORMATS
# ==============================================================================

FRENCH_MONTH_MAP = {
    "janv": "Jan", "févr": "Feb", "fevr": "Feb", "mars": "Mar", "avr": "Apr",
    "mai": "May", "juin": "Jun", "juil": "Jul", "août": "Aug", "aout": "Aug",
    "sept": "Sep", "oct": "Oct", "nov": "Nov", "déc": "Dec", "dec": "Dec",
}

def parse_date_flexible(raw_date: str) -> Optional[datetime]:
    """Parse de manière robuste une date Takeout (français, anglais, ISO 8601)."""
    if not raw_date:
        return None
    s = raw_date.strip()

    # Remplacement des mois français
    for fr, en in FRENCH_MONTH_MAP.items():
        s = re.sub(rf"\b{fr}\.?", en, s, flags=re.IGNORECASE)

    # Nettoyage des suffixes de fuseau horaire textuels (CEST, CET, UTC, etc.)
    s_cleaned = re.sub(r"\s+[A-Z]{3,4}$", "", s).strip()

    formats = [
        "%d %b %Y, %H:%M:%S",
        "%d %b %Y %H:%M:%S",
        "%d %B %Y, %H:%M:%S",
        "%b %d, %Y, %I:%M:%S %p",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s_cleaned, fmt)
        except ValueError:
            pass

    try:
        from dateutil import parser
        return parser.parse(s)
    except Exception:
        return None


# ==============================================================================
# PARSEURS GEMINI (HTML & JSON)
# ==============================================================================

def parse_gemini_html(file_path: Path) -> List[ParsedTurn]:
    """Parse rapidement l'export HTML Gemini via découpage par blocs outer-cell."""
    logger.info("Lecture et parsing rapide du fichier HTML Gemini : %s", file_path.name)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    blocks = content.split('class="outer-cell')
    logger.info("Nombre total de blocs détectés dans l'export : %d", len(blocks) - 1)

    turns: List[ParsedTurn] = []
    last_valid_dt: Optional[datetime] = None
    for block in blocks[1:]:
        if "Prompt" not in block:
            continue

        # Extraction du conteneur principal
        m_body = re.search(
            r'<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">(.*?)</div>',
            block,
            re.DOTALL,
        )
        if not m_body:
            continue
        body_html = m_body.group(1)

        # Extraction du prompt utilisateur
        m_prompt = re.search(r"Prompt\s*[:\xa0]\s*(.*?)(?:<br\s*/?>)", body_html, re.DOTALL | re.IGNORECASE)
        if not m_prompt:
            continue
        user_prompt = html.unescape(m_prompt.group(1)).strip()
        if not user_prompt:
            continue

        # Extraction de la date (jamais datetime.now() pour ne pas polluer l'historique)
        rest = body_html[m_prompt.end():]
        m_date = re.search(r"^(.*?)(?:<br\s*/?>)", rest.strip(), re.DOTALL)
        date_str = m_date.group(1).strip() if m_date else ""
        parsed_dt = parse_date_flexible(date_str)
        if not parsed_dt:
            if last_valid_dt:
                parsed_dt = last_valid_dt
            else:
                continue
        last_valid_dt = parsed_dt

        # Extraction de la réponse IA
        response_html = rest[m_date.end():].strip() if m_date else ""
        response_text = re.sub(r"<[^>]+>", " ", response_html)
        response_text = html.unescape(re.sub(r"\s+", " ", response_text)).strip()

        # Extraction de l'URL et du session_id Gemini
        m_url = re.search(r"https://gemini\.google\.com/app/([a-zA-Z0-9_-]+)", block)
        session_id = m_url.group(1) if m_url else None
        url = m_url.group(0) if m_url else None

        turns.append(
            ParsedTurn(
                session_id=session_id,
                timestamp=parsed_dt,
                user_prompt=user_prompt,
                ai_response=response_text,
                user_char_count=len(user_prompt),
                url=url,
            )
        )

    logger.info("Extraction terminée : %d tours d'échange valides récupérés.", len(turns))
    return turns


def parse_gemini_json(file_path: Path) -> List[ParsedTurn]:
    """Parse un export JSON Gemini (MyActivity.json ou conversations.json)."""
    logger.info("Parsing du fichier JSON Gemini : %s", file_path.name)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    turns: List[ParsedTurn] = []
    last_valid_dt: Optional[datetime] = None
    items = data if isinstance(data, list) else data.get("conversations", [])

    for item in items:
        title = item.get("title", "")
        # En format Google Takeout MyActivity, le titre commence souvent par "Prompt :"
        user_prompt = ""
        if title.startswith("Prompt :") or title.startswith("Prompt\xa0:"):
            user_prompt = title.split(":", 1)[1].strip()
        elif "prompt" in item:
            user_prompt = item["prompt"]

        if not user_prompt:
            continue

        time_str = item.get("time", "")
        parsed_dt = parse_date_flexible(time_str)
        if not parsed_dt:
            if last_valid_dt:
                parsed_dt = last_valid_dt
            else:
                continue
        last_valid_dt = parsed_dt

        url = item.get("titleUrl")
        session_id = None
        if url:
            m = re.search(r"gemini\.google\.com/app/([a-zA-Z0-9_-]+)", url)
            if m:
                session_id = m.group(1)

        turns.append(
            ParsedTurn(
                session_id=session_id,
                timestamp=parsed_dt,
                user_prompt=user_prompt,
                ai_response=item.get("response", ""),
                user_char_count=len(user_prompt),
                url=url,
            )
        )

    logger.info("Extraction JSON terminée : %d tours récupérés.", len(turns))
    return turns


# ==============================================================================
# PARSEURS MULTI-TAKEOUT (YOUTUBE & RECHERCHE GOOGLE)
# ==============================================================================

def parse_youtube_export(file_path: Path) -> List[HistoricalFootprintRecord]:
    """Parse l'historique YouTube (HTML ou JSON)."""
    logger.info("Parsing de l'historique YouTube : %s", file_path.name)
    footprints: List[HistoricalFootprintRecord] = []
    last_valid_dt: Optional[datetime] = None

    if file_path.suffix.lower() == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        items = data if isinstance(data, list) else []
        for item in items:
            title = item.get("title", "")
            title_clean = re.sub(r"^A regardé\s+", "", title).strip()
            url = item.get("titleUrl")
            time_str = item.get("time", "")
            dt = parse_date_flexible(time_str)
            if not dt:
                if last_valid_dt:
                    dt = last_valid_dt
                else:
                    continue
            last_valid_dt = dt
            channel = None
            subtitles = item.get("subtitles", [])
            if subtitles and isinstance(subtitles, list):
                channel = subtitles[0].get("name")
            footprints.append(
                HistoricalFootprintRecord(
                    source="youtube",
                    timestamp=dt,
                    title_or_query=title_clean,
                    url=url,
                    channel_or_domain=channel,
                )
            )
    else:
        # Parsing HTML YouTube
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        blocks = content.split('class="outer-cell')
        for b in blocks[1:]:
            m_link = re.search(r'<a href="([^"]*watch\?v=[^"]*)">([^<]+)</a>', b)
            if not m_link:
                continue
            url = m_link.group(1)
            title = html.unescape(m_link.group(2)).strip()
            # Chaîne
            m_channel = re.search(r'<a href="[^"]*channel/[^"]*">([^<]+)</a>', b)
            channel = html.unescape(m_channel.group(1)).strip() if m_channel else None
            # Date
            m_date = re.search(r"<br/?>\s*(\d{1,2}\s+[\w\.]+\s+\d{4},\s+\d{2}:\d{2}:\d{2}\s+[A-Za-z0-9_]+)", b)
            dt = parse_date_flexible(m_date.group(1)) if m_date else None
            if not dt:
                if last_valid_dt:
                    dt = last_valid_dt
                else:
                    continue
            last_valid_dt = dt
            footprints.append(
                HistoricalFootprintRecord(
                    source="youtube",
                    timestamp=dt,
                    title_or_query=title,
                    url=url,
                    channel_or_domain=channel,
                )
            )

    logger.info("Extraction YouTube terminée : %d empreintes trouvées.", len(footprints))
    return footprints


def parse_google_search_export(file_path: Path) -> List[HistoricalFootprintRecord]:
    """Parse l'historique Google Search (HTML ou JSON)."""
    logger.info("Parsing de l'historique Google Search : %s", file_path.name)
    footprints: List[HistoricalFootprintRecord] = []
    last_valid_dt: Optional[datetime] = None

    if file_path.suffix.lower() == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        items = data if isinstance(data, list) else []
        for item in items:
            title = item.get("title", "")
            query = re.sub(r"^(Vous avez recherché|Recherche|Recherché)\s*:\s*", "", title, flags=re.IGNORECASE).strip()
            if not query:
                continue
            url = item.get("titleUrl")
            time_str = item.get("time", "")
            dt = parse_date_flexible(time_str)
            if not dt:
                if last_valid_dt:
                    dt = last_valid_dt
                else:
                    continue
            last_valid_dt = dt
            footprints.append(
                HistoricalFootprintRecord(
                    source="google_search",
                    timestamp=dt,
                    title_or_query=query,
                    url=url,
                )
            )
    else:
        # Parsing HTML Google Search
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        blocks = content.split('class="outer-cell')
        for b in blocks[1:]:
            m_query = re.search(r'(?:recherché\s+|Recherche\s*:\s*).*?<a[^>]*>([^<]+)</a>', b, re.IGNORECASE)
            if not m_query:
                continue
            query = html.unescape(m_query.group(1)).strip()
            m_url = re.search(r'<a href="([^"]+)"', b)
            url = m_url.group(1) if m_url else None
            m_date = re.search(r"<br/?>\s*(\d{1,2}\s+[\w\.]+\s+\d{4},\s+\d{2}:\d{2}:\d{2}\s+[A-Za-z0-9_]+)", b)
            dt = parse_date_flexible(m_date.group(1)) if m_date else None
            if not dt:
                if last_valid_dt:
                    dt = last_valid_dt
                else:
                    continue
            last_valid_dt = dt
            footprints.append(
                HistoricalFootprintRecord(
                    source="google_search",
                    timestamp=dt,
                    title_or_query=query,
                    url=url,
                )
            )

    logger.info("Extraction Google Search terminée : %d requêtes trouvées.", len(footprints))
    return footprints


# ==============================================================================
# ALGORITHME DE SESSIONISATION ET FILTRE ANTI-BRUIT
# ==============================================================================

def sessionize_gemini_turns(
    turns: List[ParsedTurn],
    inactivity_threshold_min: int = settings.INACTIVITY_SESSION_THRESHOLD_MIN,
    min_turns: int = settings.MIN_TURNS_THRESHOLD,
    min_user_chars: int = settings.MIN_USER_CHARS_THRESHOLD,
) -> Tuple[List[ReconstructedSession], List[ReconstructedSession]]:
    """
    Reconstruit les sessions cognitives à partir des tours individuels :
    1. Regroupe par session_id officiel (ou identifiant synthétique).
    2. Scinde en sous-sessions dès qu'une pause d'inactivité > 120 min est observée.
    3. Réordonne les tours par ordre chronologique strict (du plus ancien au plus récent).
    4. Sépare les sessions qualifiées et les micro-sessions bruitées (< 3 tours OU < 250 caractères).
    Retourne (sessions_qualifiees, sessions_bruit).
    """
    logger.info("Démarrage de la sessionisation sur %d tours...", len(turns))
    sorted_turns = sorted(turns, key=lambda t: t.timestamp)

    threads_map: Dict[str, List[ParsedTurn]] = {}
    current_synth_thread: Optional[str] = None
    last_global_ts: Optional[datetime] = None

    for turn in sorted_turns:
        if turn.session_id:
            threads_map.setdefault(turn.session_id, []).append(turn)
        else:
            if (
                last_global_ts is None
                or current_synth_thread is None
                or (turn.timestamp - last_global_ts).total_seconds() > inactivity_threshold_min * 60
            ):
                current_synth_thread = f"synth_{turn.timestamp.strftime('%Y%m%d_%H%M%S')}"
            threads_map.setdefault(current_synth_thread, []).append(turn)
            last_global_ts = turn.timestamp

    reconstructed: List[ReconstructedSession] = []
    noise_sessions: List[ReconstructedSession] = []
    inactivity_delta = timedelta(minutes=inactivity_threshold_min)

    for thread_key, t_list in threads_map.items():
        t_list_sorted = sorted(t_list, key=lambda t: t.timestamp)
        sub_sessions: List[List[ParsedTurn]] = []
        current_sub: List[ParsedTurn] = [t_list_sorted[0]]

        for next_turn in t_list_sorted[1:]:
            prev_turn = current_sub[-1]
            if (next_turn.timestamp - prev_turn.timestamp) > inactivity_delta:
                sub_sessions.append(current_sub)
                current_sub = [next_turn]
            else:
                current_sub.append(next_turn)

        if current_sub:
            sub_sessions.append(current_sub)

        for sub_idx, sub_turns in enumerate(sub_sessions, 1):
            t_count = len(sub_turns)
            total_chars = sum(t.user_char_count for t in sub_turns)
            start_time = sub_turns[0].timestamp
            end_time = sub_turns[-1].timestamp
            first_prompt = sub_turns[0].user_prompt
            summary_clean = re.sub(r"\s+", " ", first_prompt)[:160].strip()

            if len(sub_sessions) == 1:
                final_sid = thread_key
            else:
                final_sid = f"{thread_key}_s{sub_idx:02d}_{start_time.strftime('%Y%m%d')}"

            sess_obj = ReconstructedSession(
                session_id=final_sid,
                timestamp_start=start_time,
                timestamp_end=end_time,
                turns=sub_turns,
                turn_count=t_count,
                user_char_count=total_chars,
                summary=summary_clean,
            )

            if t_count < min_turns or total_chars < min_user_chars:
                noise_sessions.append(sess_obj)
            else:
                reconstructed.append(sess_obj)

    reconstructed.sort(key=lambda s: s.timestamp_start)
    noise_sessions.sort(key=lambda s: s.timestamp_start)
    logger.info(
        "Sessionisation achevée : %d sessions qualifiées retenues (%d micro-sessions bruitées archivées).",
        len(reconstructed),
        len(noise_sessions),
    )
    return reconstructed, noise_sessions

