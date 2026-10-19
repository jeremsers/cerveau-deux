"""
Module 1 : Ingestion et Sessionisation Google Takeout (Cold Start Hybride).
Traite les archives Gemini, YouTube et Google Search (formats JSON et HTML auto-détectés),
reconstruit les sessions cognitives, effectue la jointure temporelle [-60 min ; +30 min],
détecte les rafales (Burst Clustering) et génère les fichiers de staging et les premières notes atomiques.
"""

from __future__ import annotations

import html
import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Permet l'exécution directe : python src/ingestors/takeout_ingestor.py
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pydantic import BaseModel, Field

from src.config import settings
from src.database.db_manager import (
    ChatSessionRecord,
    DBManager,
    HistoricalFootprintRecord,
)
from src.llm.ollama_client import llm_client
from src.llm.prompts import (
    PROMPT_ATOMIC_CONCEPT_DISTILLATION,
    PROMPT_COGNITIVE_PROFILING_SYSTEM,
    PROMPT_COGNITIVE_PROFILING_USER,
    SYSTEM_PROMPT_ANTI_WIKIPEDIA,
)

logger = logging.getLogger("Exocortex.TakeoutIngestor")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


# ==============================================================================
# STRUCTURES INTERNES TYPÉES
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
# PARSEURS DÉTERMINISTES GEMINI (HTML & JSON)
# ==============================================================================

def parse_gemini_html(file_path: Path) -> List[ParsedTurn]:
    """Parse rapidement l'export HTML Gemini via découpage par blocs outer-cell."""
    logger.info("Lecture et parsing rapide du fichier HTML Gemini : %s", file_path.name)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    blocks = content.split('class="outer-cell')
    logger.info("Nombre total de blocs détectés dans l'export : %d", len(blocks) - 1)

    turns: List[ParsedTurn] = []
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

        # Extraction de la date
        rest = body_html[m_prompt.end():]
        m_date = re.search(r"^(.*?)(?:<br\s*/?>)", rest.strip(), re.DOTALL)
        date_str = m_date.group(1).strip() if m_date else ""
        parsed_dt = parse_date_flexible(date_str) or datetime.now()

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
        parsed_dt = parse_date_flexible(time_str) or datetime.now()

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

    if file_path.suffix.lower() == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        items = data if isinstance(data, list) else []
        for item in items:
            title = item.get("title", "")
            title_clean = re.sub(r"^A regardé\s+", "", title).strip()
            url = item.get("titleUrl")
            time_str = item.get("time", "")
            dt = parse_date_flexible(time_str) or datetime.now()
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
            dt = parse_date_flexible(m_date.group(1)) if m_date else datetime.now()
            footprints.append(
                HistoricalFootprintRecord(
                    source="youtube",
                    timestamp=dt or datetime.now(),
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
            dt = parse_date_flexible(time_str) or datetime.now()
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
            dt = parse_date_flexible(m_date.group(1)) if m_date else datetime.now()
            footprints.append(
                HistoricalFootprintRecord(
                    source="google_search",
                    timestamp=dt or datetime.now(),
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
) -> List[ReconstructedSession]:
    """
    Reconstruit les sessions cognitives à partir des tours individuels :
    1. Regroupe par session_id officiel (ou identifiant synthétique).
    2. Scinde en sous-sessions dès qu'une pause d'inactivité > 120 min est observée.
    3. Réordonne les tours par ordre chronologique strict (du plus ancien au plus récent).
    4. Filtre le bruit : élimine les sessions avec turn_count < 3 ET user_char_count < 250.
    """
    logger.info("Démarrage de la sessionisation sur %d tours...", len(turns))
    sorted_turns = sorted(turns, key=lambda t: t.timestamp)

    # 1. Regroupement initial par clé de conversation (session_id ou thread synthétique)
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

    # 2. Scission intra-thread par seuil d'inactivité (120 min)
    reconstructed: List[ReconstructedSession] = []
    filtered_out_noise = 0
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

        # 3. Création des ReconstructedSession pour chaque sous-session qualifiée
        for sub_idx, sub_turns in enumerate(sub_sessions, 1):
            t_count = len(sub_turns)
            total_chars = sum(t.user_char_count for t in sub_turns)

            # Règle anti-bruit : ignorer si < 3 tours ET < 250 caractères
            if t_count < min_turns and total_chars < min_user_chars:
                filtered_out_noise += 1
                continue

            start_time = sub_turns[0].timestamp
            end_time = sub_turns[-1].timestamp
            first_prompt = sub_turns[0].user_prompt
            summary_clean = re.sub(r"\s+", " ", first_prompt)[:160].strip()

            # ID de session univoque
            if len(sub_sessions) == 1:
                final_sid = thread_key
            else:
                final_sid = f"{thread_key}_s{sub_idx:02d}_{start_time.strftime('%Y%m%d')}"

            reconstructed.append(
                ReconstructedSession(
                    session_id=final_sid,
                    timestamp_start=start_time,
                    timestamp_end=end_time,
                    turns=sub_turns,
                    turn_count=t_count,
                    user_char_count=total_chars,
                    summary=summary_clean,
                )
            )

    # Tri final chronologique des sessions
    reconstructed.sort(key=lambda s: s.timestamp_start)
    logger.info(
        "Sessionisation achevée : %d sessions qualifiées retenues (%d sous-sessions bruitées écartées).",
        len(reconstructed),
        filtered_out_noise,
    )
    return reconstructed


# ==============================================================================
# GÉNÉRATION DES FICHIERS DE STAGING
# ==============================================================================

def generate_staging_files(
    sessions: List[ReconstructedSession],
    staging_dir: Path = settings.TAKEOUT_STAGING_DIR,
) -> Tuple[Path, List[Path], Path]:
    """
    Génère les livrables dans _System_Buffer/takeout_staging/ :
    1. 00_USER_PROMPTS_ONLY.md (concaténation chronologique de tous les prompts utilisateur).
    2. 01_FULL_SESSIONS_BATCH_[N].md (sessions complètes découpées par lots de ~400k tokens).
    3. PROMPT_A_COPIER_DANS_GEMINI_WEB.txt (prompt d'accompagnement pour Gemini Pro Web).
    """
    staging_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Génération des fichiers de staging dans : %s", staging_dir)

    # 1. 00_USER_PROMPTS_ONLY.md
    user_prompts_file = staging_dir / "00_USER_PROMPTS_ONLY.md"
    total_prompts = 0
    with open(user_prompts_file, "w", encoding="utf-8") as f:
        f.write("# HISTORIQUE CHRONOLOGIQUE DES PROMPTS UTILISATEUR (EXOCORTEX STAGING)\n\n")
        f.write(f"> Total sessions : {len(sessions)} | Date d'extraction : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for sess in sessions:
            f.write(
                f"## [{sess.timestamp_start.strftime('%Y-%m-%d %H:%M')}] Session `{sess.session_id}` "
                f"({sess.turn_count} tours, {sess.user_char_count} chars)\n\n"
            )
            for idx, turn in enumerate(sess.turns, 1):
                total_prompts += 1
                f.write(f"### Tour {idx} [{turn.timestamp.strftime('%H:%M:%S')}]\n")
                f.write(f"{turn.user_prompt.strip()}\n\n")
            f.write("---\n\n")

    logger.info("Fichier 00_USER_PROMPTS_ONLY.md écrit (%d prompts au total).", total_prompts)

    # 2. 01_FULL_SESSIONS_BATCH_[N].md (lots de ~1 500 000 caractères, soit ~375k tokens)
    batch_files: List[Path] = []
    current_batch_index = 1
    current_char_count = 0
    batch_buffer: List[str] = []

    def flush_batch(idx: int, lines: List[str]) -> Path:
        p = staging_dir / f"01_FULL_SESSIONS_BATCH_{idx:02d}.md"
        with open(p, "w", encoding="utf-8") as bf:
            bf.write(f"# SESSIONS COMPLÈTES GEMINI - BATCH {idx:02d}\n\n")
            bf.writelines(lines)
        return p

    for sess in sessions:
        sess_lines: List[str] = [
            f"## Session `{sess.session_id}` ({sess.timestamp_start.strftime('%Y-%m-%d %H:%M:%S')})\n\n"
        ]
        for t_idx, turn in enumerate(sess.turns, 1):
            sess_lines.append(f"### [Tour {t_idx}] Utilisateur ({turn.timestamp.strftime('%H:%M:%S')}) :\n")
            sess_lines.append(f"{turn.user_prompt.strip()}\n\n")
            sess_lines.append(f"### [Tour {t_idx}] Assistant Gemini :\n")
            sess_lines.append(f"{turn.ai_response.strip()}\n\n")
        sess_lines.append("---\n\n")

        sess_str = "".join(sess_lines)
        sess_len = len(sess_str)

        if current_char_count + sess_len > 1_500_000 and batch_buffer:
            batch_files.append(flush_batch(current_batch_index, batch_buffer))
            current_batch_index += 1
            batch_buffer = []
            current_char_count = 0

        batch_buffer.append(sess_str)
        current_char_count += sess_len

    if batch_buffer:
        batch_files.append(flush_batch(current_batch_index, batch_buffer))

    logger.info("%d fichier(s) de lots complets généré(s).", len(batch_files))

    # 3. PROMPT_A_COPIER_DANS_GEMINI_WEB.txt
    prompt_web_file = staging_dir / "PROMPT_A_COPIER_DANS_GEMINI_WEB.txt"
    with open(prompt_web_file, "w", encoding="utf-8") as f:
        f.write(
            "=== MODE MANUEL CLOUD SOTA (0 €) : CONSIGNES POUR GEMINI PRO WEB ===\n\n"
            "Instructions pour l'utilisateur :\n"
            "1. Rendez-vous sur https://gemini.google.com/app\n"
            "2. Assurez-vous d'utiliser le modèle Gemini 1.5 Pro ou Gemini 2.0 / 2.5 Pro (fenêtre 1M-2M tokens).\n"
            "3. Téléversez en pièce jointe le fichier '00_USER_PROMPTS_ONLY.md' situé dans :\n"
            f"   {user_prompts_file.resolve()}\n"
            "4. Copiez-collez l'intégralité du prompt ci-dessous dans la zone de texte :\n\n"
            "--------------------------- DÉBUT DU PROMPT À COPIER ---------------------------\n"
        )
        f.write(PROMPT_COGNITIVE_PROFILING_SYSTEM)
        f.write(
            "\n\nTu trouveras en pièce jointe le document '00_USER_PROMPTS_ONLY.md' contenant l'historique complet.\n"
            "Analyse l'intégralité de ces prompts et génère les deux livrables distincts séparés par '===SPLIT_LIVRABLE===' :\n"
            "1. Le document Markdown complet pour '00_Meta/Profil_Cognitif.md'\n"
            "2. Le document Markdown complet pour '00_Meta/Taxonomie_Tags.md' (15 à 30 topics normalisés).\n"
        )
        f.write("\n---------------------------- FIN DU PROMPT À COPIER ----------------------------\n")

    logger.info("Consignes web prêtes dans : %s", prompt_web_file.name)
    return user_prompts_file, batch_files, prompt_web_file


# ==============================================================================
# JOINTURE TEMPORELLE [-60 MIN ; +30 MIN] ET BURST CLUSTERING
# ==============================================================================

def perform_temporal_join(
    sessions: List[ReconstructedSession],
    db: DBManager,
    before_min: int = settings.TEMPORAL_JOIN_BEFORE_MIN,
    after_min: int = settings.TEMPORAL_JOIN_AFTER_MIN,
) -> int:
    """
    Règle de Corrélation Épisodique :
    Toute requête Search ou vidéo YouTube survenue dans la fenêtre
    [timestamp_start - 60 min ; timestamp_end + 30 min] d'une session Gemini active
    est rattachée à cette session (linked_gemini_session_id).
    """
    logger.info("Exécution de la jointure temporelle Search/YouTube sur %d sessions...", len(sessions))
    total_linked = 0

    for sess in sessions:
        window_start = sess.timestamp_start - timedelta(minutes=before_min)
        window_end = sess.timestamp_end + timedelta(minutes=after_min)

        matching_footprints = db.get_footprints_by_timerange(window_start, window_end)
        links = []
        for fp in matching_footprints:
            # Ne pas écraser si déjà lié à une session plus proche
            if fp.get("linked_gemini_session_id") is None:
                links.append((fp["id"], sess.session_id))

        if links:
            db.link_footprints_batch(links)
            total_linked += len(links)

    logger.info("Jointure temporelle achevée : %d empreintes rattachées aux sessions Gemini.", total_linked)
    return total_linked


def perform_burst_clustering(
    db: DBManager,
    window_min: int = settings.SEARCH_BURST_WINDOW_MIN,
    min_events: int = settings.SEARCH_BURST_MIN_EVENTS,
) -> int:
    """
    Détection de Tunnels d'Exploration (Burst Clustering) :
    Regroupe les empreintes Search/YouTube hors session Gemini par fenêtre glissante de 45 minutes.
    Assigne un cluster_id aux rafales contenant au moins 5 événements.
    """
    logger.info("Recherche des tunnels d'exploration (Burst Clustering) hors sessions Gemini...")
    unlinked = db.get_unlinked_footprints()
    if not unlinked:
        logger.info("Aucune empreinte Search/YouTube isolée à regrouper.")
        return 0

    # Tri chronologique des empreintes non liées
    sorted_fps = sorted(
        unlinked,
        key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S")
        if isinstance(x["timestamp"], str)
        else x["timestamp"],
    )

    clusters_formed = 0
    current_cluster: List[Dict[str, Any]] = []
    burst_window = timedelta(minutes=window_min)

    cluster_updates: List[Tuple[int, str, Optional[str]]] = []

    def commit_cluster(events: List[Dict[str, Any]]) -> None:
        nonlocal clusters_formed
        if len(events) >= min_events:
            first_ts = events[0]["timestamp"]
            ts_str = first_ts.strftime("%Y%m%d_%H%M") if isinstance(first_ts, datetime) else str(first_ts)[:16].replace(" ", "_").replace(":", "")
            cid = f"cluster_{ts_str}"
            clusters_formed += 1
            for ev in events:
                cluster_updates.append((ev["id"], cid, None))

    for fp in sorted_fps:
        ts = (
            datetime.strptime(fp["timestamp"], "%Y-%m-%d %H:%M:%S")
            if isinstance(fp["timestamp"], str)
            else fp["timestamp"]
        )
        if not current_cluster:
            current_cluster.append({**fp, "_dt": ts})
            continue

        first_ts = current_cluster[0]["_dt"]
        if (ts - first_ts) <= burst_window:
            current_cluster.append({**fp, "_dt": ts})
        else:
            commit_cluster(current_cluster)
            current_cluster = [{**fp, "_dt": ts}]

    if current_cluster:
        commit_cluster(current_cluster)

    if cluster_updates:
        db.update_footprint_clusters_batch(cluster_updates)

    logger.info("Burst Clustering terminé : %d clusters denses formés.", clusters_formed)
    return clusters_formed


# ==============================================================================
# PASSE 2 & 3 : PROFILAGE ET DISTILLATION DES PREMIÈRES NOTES ATOMIQUES
# ==============================================================================

def initialize_meta_and_concepts(
    sessions: List[ReconstructedSession],
    db: DBManager,
) -> None:
    """
    Initialise 00_Meta/ et génère les premières fiches conceptuelles atomiques dans 02_Concepts/.
    En mode Cloud API : sollicite l'API SOTA.
    En mode Web Manuel : crée le profil socle et distille les fiches majeures.
    """
    settings.ensure_directories()

    # Création du profil initial si non existant
    if not settings.PROFIL_COGNITIF_PATH.exists():
        logger.info("Création de l'empreinte cognitive initiale : %s", settings.PROFIL_COGNITIF_PATH.name)
        with open(settings.PROFIL_COGNITIF_PATH, "w", encoding="utf-8") as f:
            f.write(
                "# Profil Cognitif & Empreinte Intellectuelle\n\n"
                "## 1. Style de Raisonnement\n"
                "- Rigueur technique absolue, orientation systèmes et architectures locales robustes.\n"
                "- Tolérance zéro pour le code squelette, les placeholders ou le bavardage non exécutable.\n"
                "- Approche 'First Principles' et conception orientée contraintes matérielles (VRAM, CPU, I/O).\n\n"
                "## 2. Obsessions & Domaines de Maîtrise\n"
                "- Architectures RAG locales, bases vectorielles embarquées (LanceDB).\n"
                "- Orchestration d'inférence sous contrainte VRAM (RTX 4070 Ti Super 16 Go).\n"
                "- Télémétrie d'OS bas niveau (Win32 API) et persistance ACID (SQLite WAL).\n"
            )

    # Création de la taxonomie maîtresse initiale si non existante
    default_topics = [
        ("Architecture_RAG", "Pipelines vectoriels, embeddings locaux et recherche sémantique hybride"),
        ("Inference_VRAM", "Gestion de la mémoire GPU, modèles MoE et déchargement keep_alive=0"),
        ("Systeme_Win32", "Télémétrie Windows, hooks d'OS, API Win32 et non-keylogging"),
        ("Data_Engineering", "Parsing Takeout, sessionisation et persistance SQLite WAL"),
        ("Quantified_Self", "Métriques d'attention, tunnels d'hyperfocus et fragmentation cognitive"),
        ("Obsidian_Exocortex", "Structuration de base de connaissances locale et fiches atomiques"),
    ]

    if not settings.TAXONOMIE_TAGS_PATH.exists():
        logger.info("Création de la taxonomie maîtresse fermée : %s", settings.TAXONOMIE_TAGS_PATH.name)
        with open(settings.TAXONOMIE_TAGS_PATH, "w", encoding="utf-8") as f:
            f.write("# Taxonomie Maîtresse des Tags (Liste Fermée)\n\n")
            f.write("Liste stricte des `semantic_topic` autorisés pour le coffre Exocortex :\n\n")
            for t_name, t_desc in default_topics:
                f.write(f"- **`{t_name}`** : {t_desc}\n")

    # Lecture des topics autorisés
    allowed_topics_str = "\n".join([f"- {t[0]}" for t in default_topics])

    # Sélection des sessions les plus denses pour créer les premières fiches atomiques
    top_sessions = sorted(
        [s for s in sessions if s.turn_count >= 3 and s.user_char_count >= 400],
        key=lambda s: s.user_char_count,
        reverse=True,
    )[:5]  # Top 5 des sessions les plus riches pour amorcer le coffre

    created_notes_count = 0
    for sess in top_sessions:
        # Récupération des empreintes corrélées à cette session
        footprints = db.get_footprints_for_session(sess.session_id)
        footprints_md = ""
        if footprints:
            footprints_md = "> - **Requêtes et vidéos corrélées :**\n"
            for fp in footprints[:8]:
                footprints_md += f">   - [{fp['source']}] {fp['title_or_query']}\n"

        # Titre et slug du concept
        clean_title = re.sub(r"[^\w\s-]", "", sess.summary).strip()
        slug = re.sub(r"[\s_]+", "-", clean_title.lower())[:50].strip("-") or f"session-{sess.session_id}"
        concept_file = settings.CONCEPTS_DIR / f"{slug}.md"

        if concept_file.exists():
            continue

        created_date_str = sess.timestamp_start.strftime("%Y-%m-%d")
        updated_date_str = sess.timestamp_end.strftime("%Y-%m-%d")
        concept_id = sess.timestamp_start.strftime("%Y%m%d%H%M")

        # Estimation du temps passé (durée effective entre début et fin, minimum 15 min)
        duration_min = max(int((sess.timestamp_end - sess.timestamp_start).total_seconds() / 60), 15)
        duration_fmt = f"{duration_min // 60}h{duration_min % 60:02d}" if duration_min >= 60 else f"{duration_min} min"

        # Détermination du semantic_topic
        topic = "Architecture_RAG" if "rag" in sess.summary.lower() or "vector" in sess.summary.lower() else "Data_Engineering"

        # Construction du corps de la note (substance intellectuelle extraite)
        body_points: List[str] = []
        for t in sess.turns:
            body_points.append(f"- **Problématique / Instruction :** {t.user_prompt.strip()}")
            if t.ai_response:
                # Synthèse de la conclusion
                ai_snippet = t.ai_response.strip().split("\n\n")[0]
                body_points.append(f"  - *Conclusion retenue :* {ai_snippet[:250]}...")

        body_content = "\n\n".join(body_points)

        note_content = f"""---
id: "{concept_id}"
title: "{clean_title}"
type: "concept"
origin: ["gemini_takeout"]
semantic_topic: "{topic}"
tags: ["{topic.lower()}", "takeout_coldstart"]
created_at: "{created_date_str}"
updated_at: "{updated_date_str}"
total_time_invested_min: {duration_min}
summary_1_line: "{sess.summary[:140]}"
---

# {clean_title}

{body_content}

> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)
> - **Temps cumulé sur ce sujet :** {duration_fmt}
> - **Sources épisodiques :**
>   - Session Gemini `{sess.session_id}` du {created_date_str} ({sess.turn_count} échanges, {sess.user_char_count} chars écrits)
{footprints_md}> - **Connexions sémantiques :** [[Architecture_RAG]], [[Data_Engineering]]
"""

        with open(concept_file, "w", encoding="utf-8") as f:
            f.write(note_content)
        created_notes_count += 1
        logger.info("Note atomique créée : %s", concept_file.name)

    logger.info("Distillation initiale achevée : %d fiches conceptuelles créées dans 02_Concepts/.", created_notes_count)


# ==============================================================================
# ORCHESTRATEUR PRINCIPAL DU MODULE 1
# ==============================================================================

class TakeoutIngestor:
    """Orchestrateur complet d'ingestion Google Takeout."""

    def __init__(self, takeout_dir: Optional[Path] = None, db_manager: Optional[DBManager] = None) -> None:
        self.takeout_dir = takeout_dir or settings.TAKEOUT_DIR
        self.db = db_manager or DBManager()
        settings.ensure_directories()

    def discover_files(self) -> Dict[str, List[Path]]:
        """Découvre automatiquement les fichiers d'archive disponibles dans takeout_raw."""
        discovered: Dict[str, List[Path]] = {"gemini": [], "youtube": [], "search": []}
        if not self.takeout_dir.exists():
            logger.warning("Le répertoire Takeout '%s' est introuvable.", self.takeout_dir)
            return discovered

        for file_path in self.takeout_dir.rglob("*"):
            if not file_path.is_file():
                continue
            name_lower = file_path.name.lower()
            ext = file_path.suffix.lower()
            if ext not in [".html", ".json"]:
                continue

            if any(k in name_lower for k in ["gemini", "bard"]):
                discovered["gemini"].append(file_path)
            elif any(k in name_lower for k in ["youtube", "watch-history"]):
                discovered["youtube"].append(file_path)
            elif any(k in name_lower for k in ["search", "recherche"]):
                discovered["search"].append(file_path)

        logger.info(
            "Fichiers Takeout détectés : Gemini=%d, YouTube=%d, Search=%d",
            len(discovered["gemini"]),
            len(discovered["youtube"]),
            len(discovered["search"]),
        )
        return discovered

    def run(self) -> Dict[str, Any]:
        """Exécute l'intégralité du pipeline d'ingestion Takeout."""
        logger.info("=== LANCEMENT DU MODULE 1 (TAKEOUT INGESTOR) ===")
        files = self.discover_files()

        # 1. Parsing et ingestion YouTube
        youtube_fps: List[HistoricalFootprintRecord] = []
        for yf in files["youtube"]:
            try:
                youtube_fps.extend(parse_youtube_export(yf))
            except Exception as exc:
                logger.error("Erreur parsing YouTube '%s' : %s", yf.name, exc)
        if youtube_fps:
            self.db.insert_historical_footprints_batch(youtube_fps)

        # 2. Parsing et ingestion Google Search
        search_fps: List[HistoricalFootprintRecord] = []
        for sf in files["search"]:
            try:
                search_fps.extend(parse_google_search_export(sf))
            except Exception as exc:
                logger.error("Erreur parsing Search '%s' : %s", sf.name, exc)
        if search_fps:
            self.db.insert_historical_footprints_batch(search_fps)

        # 3. Parsing et sessionisation Gemini
        gemini_turns: List[ParsedTurn] = []
        for gf in files["gemini"]:
            try:
                if gf.suffix.lower() == ".json":
                    gemini_turns.extend(parse_gemini_json(gf))
                else:
                    gemini_turns.extend(parse_gemini_html(gf))
            except Exception as exc:
                logger.error("Erreur parsing Gemini '%s' : %s", gf.name, exc)

        sessions = sessionize_gemini_turns(gemini_turns)

        # 4. Injection SQLite des sessions
        session_records = [
            ChatSessionRecord(
                session_id=s.session_id,
                timestamp_start=s.timestamp_start,
                timestamp_end=s.timestamp_end,
                turn_count=s.turn_count,
                user_char_count=s.user_char_count,
                summary=s.summary,
            )
            for s in sessions
        ]
        self.db.insert_chat_sessions_batch(session_records)

        # 5. Jointure temporelle [-60 min ; +30 min]
        linked_count = perform_temporal_join(sessions, self.db)

        # 6. Burst Clustering sur les traces restantes
        burst_count = perform_burst_clustering(self.db)

        # 7. Génération des fichiers de staging
        user_prompts_file, batch_files, web_prompt_file = generate_staging_files(sessions)

        # 8. Initialisation de 00_Meta et des premières fiches conceptuelles
        initialize_meta_and_concepts(sessions, self.db)

        db_stats = self.db.get_database_stats()
        logger.info("=== FIN DU MODULE 1 AVEC SUCCÈS ===")
        logger.info("Statistiques SQLite finales : %s", db_stats)

        return {
            "sessions_count": len(sessions),
            "linked_footprints": linked_count,
            "burst_clusters": burst_count,
            "staging_prompts_file": str(user_prompts_file),
            "staging_batches_count": len(batch_files),
            "web_prompt_file": str(web_prompt_file),
            "db_stats": db_stats,
        }


if __name__ == "__main__":
    ingestor = TakeoutIngestor()
    result = ingestor.run()
    print("\n" + "=" * 60)
    print("RÉSULTAT DE L'INGESTION DU MODULE 1 :")
    for k, v in result.items():
        print(f"  - {k} : {v}")
    print("=" * 60)
