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
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Permet l'exécution directe : python src/ingestors/takeout_ingestor.py
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pydantic import BaseModel, Field
from tqdm import tqdm

from src.config import AUTHORIZED_SEMANTIC_TOPICS, normalize_to_macro_topic, settings
from src.database.db_manager import (
    ChatMessageRecord,
    ChatSessionRecord,
    DailyMetricRecord,
    DBManager,
    HistoricalFootprintRecord,
)
from src.database.vector_store import vector_store
from src.consolidators.drive_compiler import DriveCompiler
from src.llm.ollama_client import llm_client
from src.llm.prompts import (
    PROMPT_COGNITIVE_PROFILING_SYSTEM,
    PROMPT_COGNITIVE_PROFILING_USER,
    PROMPT_SESSION_DISTILLATION_SYSTEM,
    PROMPT_SESSION_DISTILLATION_USER,
    PROMPT_STRICT_TAXONOMY_RULE,
    SYSTEM_PROMPT_ANTI_WIKIPEDIA,
)

logger = logging.getLogger("Exocortex.TakeoutIngestor")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


# ==============================================================================
# STRUCTURES INTERNES TYPÉES & SCHÉMA PYDANTIC V2 DE DISTILLATION
# ==============================================================================

class DistilledConceptSchema(BaseModel):
    """Schéma de sortie structuré Pydantic v2 pour la distillation LLM d'une session."""
    is_worth_indexing: bool = Field(description="False si la session n'est que du bruit ou un test trivial sans conclusion.")
    concept_title: str = Field(description="Titre conceptuel précis et canonique (ex: 'Configuration Serveur Plex & Riven sous Docker'). Jamais une phrase de prompt.")
    slug: str = Field(description="Slug kebab-case propre (ex: 'configuration-plex-riven-docker')")
    semantic_topic: str = Field(description="Exactement l'une des 15 macro-catégories autorisées de la liste stricte.")
    is_new_topic: bool = Field(default=False, description="Désormais déprécié, toujours False.")
    new_topic_description: Optional[str] = Field(default=None, description="Description si nouveau topic.")
    tags: List[str] = Field(default_factory=list, description="3 à 6 tags techniques libres en minuscules kebab-case.")
    summary_1_line: str = Field(description="Résumé dense en une seule phrase de la conclusion ou de l'architecture.")
    synthesized_markdown_body: str = Field(
        description="Synthèse structurée en Markdown (sections ### Contexte, ### Arbitrages & Architecture, ### Conclusions & Commandes Clés). Zéro intro Wikipédia."
    )
    related_concepts: List[str] = Field(default_factory=list, description="2 à 3 titres de concepts connexes pour le maillage Obsidian")


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


def ensure_strict_taxonomy_file() -> None:
    """Écrit ou écrase Taxonomie_Tags.md avec la liste stricte et fermée des 16 macro-catégories."""
    settings.TAXONOMIE_TAGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Taxonomie Maîtresse des Tags (Liste Fermée)",
        "",
        "Liste stricte des 16 `semantic_topic` autorisés pour le coffre Exocortex :",
        "",
    ]
    for topic, desc in AUTHORIZED_SEMANTIC_TOPICS.items():
        lines.append(f"- **`{topic}`** : {desc}")
    lines.append("")
    settings.TAXONOMIE_TAGS_PATH.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Taxonomie maîtresse à 16 macro-catégories validée dans %s", settings.TAXONOMIE_TAGS_PATH.name)


def register_new_taxonomy_tag(tag_name: str, description: Optional[str] = None) -> bool:
    """Déprécié en v0.1.2 : la taxonomie est fermée à 16 macro-catégories."""
    macro = normalize_to_macro_topic(tag_name)
    logger.debug("Tentative d'enregistrement de '%s' remappée vers la macro-catégorie '%s'", tag_name, macro)
    return False


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

        # 3. Création des ReconstructedSession pour chaque sous-session
        for sub_idx, sub_turns in enumerate(sub_sessions, 1):
            t_count = len(sub_turns)
            total_chars = sum(t.user_char_count for t in sub_turns)
            start_time = sub_turns[0].timestamp
            end_time = sub_turns[-1].timestamp
            first_prompt = sub_turns[0].user_prompt
            summary_clean = re.sub(r"\s+", " ", first_prompt)[:160].strip()

            # ID de session univoque
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

            # Règle anti-bruit : si moins de 3 tours OU moins de 250 caractères -> bruit
            if t_count < min_turns or total_chars < min_user_chars:
                noise_sessions.append(sess_obj)
            else:
                reconstructed.append(sess_obj)

    # Tri final chronologique des sessions
    reconstructed.sort(key=lambda s: s.timestamp_start)
    noise_sessions.sort(key=lambda s: s.timestamp_start)
    logger.info(
        "Sessionisation achevée : %d sessions qualifiées retenues (%d micro-sessions bruitées archivées).",
        len(reconstructed),
        len(noise_sessions),
    )
    return reconstructed, noise_sessions


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

def scan_and_upgrade_existing_concepts(db: DBManager) -> Set[str]:
    """
    Scanne tous les fichiers Markdown existants dans Vault_Data/02_Concepts/ :
    - Détecte et purge les faux succès (fallbacks heuristiques v0.1.1) du disque et de LanceDB.
    - Assainit les fiches réussies sur place :
        * Retrait des blocs de requêtes/vidéos corrélées YouTube/Search.
        * Remapping déterministe vers les 15 macro-catégories maîtresses (+ insertion de l'ancien topic dans tags).
        * Ajout de session_id et distillation_status: "success" dans le frontmatter.
        * Synchronisation des statuts en base SQLite.
    - Retourne l'ensemble des session_id complétées pour le mode Delta (Skip instantané).
    """
    ensure_strict_taxonomy_file()

    completed_session_ids: Set[str] = set()
    # Ajout des sessions déjà marquées success ou misc_noise dans SQLite
    completed_session_ids.update(db.get_completed_session_ids_from_db())

    concept_files = sorted(list(settings.CONCEPTS_DIR.glob("*.md")))
    if not concept_files:
        logger.info("Aucune fiche existante trouvée dans %s.", settings.CONCEPTS_DIR)
        return completed_session_ids

    purged_fallbacks = 0
    upgraded_notes = 0

    with tqdm(total=len(concept_files), desc="Assainissement Notes Existantes", unit="note") as pbar:
        for fpath in concept_files:
            if fpath.name.startswith("all-") or fpath.name.startswith("all_"):
                pbar.update(1)
                continue

            try:
                content = fpath.read_text(encoding="utf-8")
            except Exception as exc:
                logger.warning("Erreur lecture %s : %s", fpath.name, exc)
                pbar.update(1)
                continue

            # Extraction de session_id
            m_sid = re.search(r'session_id:\s*["\']?([^"\'\n\r]+)["\']?', content)
            if m_sid:
                extracted_sid = m_sid.group(1).strip()
            else:
                m_body_sid = re.search(r'Session Gemini [^\w]*([a-zA-Z0-9_-]+)', content)
                extracted_sid = m_body_sid.group(1).strip() if m_body_sid else None

            # Découpe du corps Markdown avant le bloc de télémétrie final de l'Exocortex (v0.1.3 Hotfix)
            if "> - **Temps estimé sur ce sujet :**" in content:
                body_before_abstract = content.split("> - **Temps estimé sur ce sujet :**")[0]
                if "> [!abstract]-" in body_before_abstract:
                    body_before_abstract = body_before_abstract.rsplit("> [!abstract]-", 1)[0]
            elif "> [!abstract]-" in content:
                body_before_abstract = content.rsplit("> [!abstract]-", 1)[0]
            else:
                body_before_abstract = content

            body_before_abstract = body_before_abstract.strip()
            non_empty_lines = [l.strip() for l in body_before_abstract.splitlines() if l.strip()]
            last_line = non_empty_lines[-1] if non_empty_lines else ""

            is_truncated = False
            if last_line:
                valid_endings = ('.', '!', '?', ')', '*', '`', '|', ':', '"', '»', ']', '}', '>')
                if (
                    last_line.endswith("pour assimiler la structure")
                    or last_line.endswith("pour s'assurer que le")
                ):
                    is_truncated = True
                elif not last_line.endswith(valid_endings):
                    # Si la note fait plus de 500 caractères et possède une section de conclusion,
                    # ne pas la rejeter si la dernière ligne est un tableau ou une puce/texte sans point final
                    has_conclusion = bool(re.search(r"###\s*(?:Conclusions?|Synthèse|Bilan|Commandes\s*Clés)", body_before_abstract, re.IGNORECASE))
                    is_table_or_bullet = last_line.startswith(("|", "*", "-", ">"))
                    if len(body_before_abstract) > 500 and (has_conclusion or is_table_or_bullet):
                        is_truncated = False
                    else:
                        is_truncated = True

            # Détection des 5 critères de fallback dégradé ou troncature
            is_fallback = (
                is_truncated
                or "takeout_coldstart" in content
                or ("### Problématique & Contexte" in content and "- Session composée de" in content)
                or bool(re.search(r'semantic_topic:\s*["\']?A_Trier["\']?', content))
                or bool(re.search(r'distillation_status:\s*["\']?failed_fallback["\']?', content))
            )

            if is_fallback:
                if is_truncated:
                    logger.warning("Fiche tronquée détectée et purgée : %s (dernière ligne : '%s')", fpath.name, last_line[-40:])
                # 1. Purge disque et LanceDB
                try:
                    fpath.unlink()
                except Exception as exc:
                    logger.warning("Impossible de supprimer %s : %s", fpath.name, exc)
                vector_store.delete_by_slug(fpath.stem)
                purged_fallbacks += 1
                # Réinitialisation SQLite pour permettre la re-distillation
                if extracted_sid:
                    db.update_session_distillation_metadata(
                        session_id=extracted_sid,
                        topics_list=[],
                        notes_list=[],
                        distillation_status="pending",
                    )
                # Ne pas ajouter extracted_sid à completed_session_ids -> sera re-distillé
            else:
                # 2. Fiche réussie -> In-Place Upgrade
                if extracted_sid:
                    completed_session_ids.add(extracted_sid)

                # Parsing YAML frontmatter
                m_yaml = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
                if m_yaml:
                    yaml_raw = m_yaml.group(1)
                    body_raw = m_yaml.group(2)
                else:
                    yaml_raw = ""
                    body_raw = content

                # Extraction / remapping du semantic_topic
                m_topic = re.search(r'semantic_topic:\s*["\']?([^"\'\n\r]+)["\']?', yaml_raw)
                raw_topic = m_topic.group(1).strip() if m_topic else "Dev_et_Architecture_Tech"
                macro_topic = normalize_to_macro_topic(raw_topic)

                # Extraction / mise à jour des tags
                m_tags = re.search(r'tags:\s*(\[.*?\])', yaml_raw)
                tags_list: List[str] = []
                if m_tags:
                    try:
                        tags_list = json.loads(m_tags.group(1))
                    except Exception:
                        tags_list = []

                if raw_topic != macro_topic:
                    legacy_tag = raw_topic.lower()
                    if legacy_tag not in [t.lower() for t in tags_list]:
                        tags_list.append(legacy_tag)

                # Construction du nouveau frontmatter
                lines_yaml = yaml_raw.splitlines()
                new_yaml_lines = []
                has_sid = False
                has_status = False

                for line in lines_yaml:
                    if line.strip().startswith("semantic_topic:"):
                        new_yaml_lines.append(f'semantic_topic: "{macro_topic}"')
                    elif line.strip().startswith("tags:"):
                        new_yaml_lines.append(f"tags: {json.dumps(tags_list, ensure_ascii=False)}")
                    elif line.strip().startswith("session_id:"):
                        has_sid = True
                        new_yaml_lines.append(line)
                    elif line.strip().startswith("distillation_status:"):
                        has_status = True
                        new_yaml_lines.append('distillation_status: "success"')
                    else:
                        new_yaml_lines.append(line)

                if not has_sid and extracted_sid:
                    new_yaml_lines.append(f'session_id: "{extracted_sid}"')
                if not has_status:
                    new_yaml_lines.append('distillation_status: "success"')

                # Nettoyage du corps Markdown
                # a. Retrait du bloc Requêtes et vidéos corrélées
                clean_body = re.sub(
                    r'>\s*-\s*\*\*Requêtes et vidéos corrélées\s*:\*\*.*?(?=>\s*-\s*\*\*Connexions sémantiques|\Z)',
                    '',
                    body_raw,
                    flags=re.DOTALL,
                )
                # b. Séparation du bloc officiel de télémétrie et suppression des blocs abstract internes/doublons du LLM
                if "> - **Temps estimé sur ce sujet :**" in clean_body:
                    parts = clean_body.split("> - **Temps estimé sur ce sujet :**", 1)
                    pre_telemetry = parts[0]
                    telemetry_part = "> - **Temps estimé sur ce sujet :**" + parts[1]
                    if "> [!abstract]-" in pre_telemetry:
                        pre_telemetry = pre_telemetry.rsplit("> [!abstract]-", 1)[0]
                    # Suppression de tout bloc abstract interne
                    clean_main = re.sub(r'>\s*\[!abstract\]-[^\n]*\n(?:>[^\n]*\n)*', '', pre_telemetry).strip()
                    clean_body = f"{clean_main}\n\n> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)\n{telemetry_part.strip()}"
                else:
                    # S'il n'y a pas le bloc de télémétrie officiel, on supprime tout abstract interne résiduel
                    clean_body = re.sub(r'>\s*\[!abstract\]-[^\n]*\n(?:>[^\n]*\n)*', '', clean_body).strip()

                new_file_content = f"---\n{chr(10).join(new_yaml_lines).strip()}\n---\n\n{clean_body.strip()}\n"
                try:
                    fpath.write_text(new_file_content, encoding="utf-8")
                    upgraded_notes += 1
                except Exception as exc:
                    logger.warning("Erreur écriture mise à niveau %s : %s", fpath.name, exc)

                # Mise à jour en base SQLite
                if extracted_sid:
                    db.update_session_distillation_metadata(
                        session_id=extracted_sid,
                        topics_list=[macro_topic],
                        notes_list=[fpath.stem],
                        distillation_status="success",
                    )

            pbar.update(1)

    # Intégration des sessions rejetées (bruit consolidé) pour éviter de les re-distiller
    with db.get_connection() as conn:
        cur = conn.execute("SELECT session_id FROM chat_sessions WHERE distillation_status = 'misc_noise';")
        for row in cur.fetchall():
            completed_session_ids.add(row[0])

    logger.info(
        "Assainissement terminé : %d fallbacks purgés, %d fiches assainies sur place, %d sessions complètes en mémoire.",
        purged_fallbacks,
        upgraded_notes,
        len(completed_session_ids),
    )
    return completed_session_ids


def compile_misc_noise_archive(
    noise_sessions: List[ReconstructedSession],
    llm_rejected_sessions: List[ReconstructedSession],
    archive_path: Optional[Path] = None,
) -> Path:
    """
    Compile un registre exhaustif et dense de toutes les micro-sessions (< 3 tours ou < 250 car.)
    et des sessions rejetées par le LLM (is_worth_indexing=False) dans 00_Meta/00_MISC_ET_BRUIT_ARCHIVE.md.
    """
    out_path = archive_path or settings.MISC_ARCHIVE_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    for s in noise_sessions:
        entries.append((s, "Micro-session"))
    for s in llm_rejected_sessions:
        entries.append((s, "Rejeté par LLM"))

    # Tri antéchronologique strict
    entries.sort(key=lambda item: item[0].timestamp_start, reverse=True)

    count_noise = len(noise_sessions)
    count_llm = len(llm_rejected_sessions)
    total = len(entries)

    lines = [
        "# Registre Consolidé du Bruit & Micro-Sessions",
        "",
        "Archive exhaustive et antéchronologique des micro-sessions (< 3 tours ou < 250 caractères) "
        "et des requêtes déclarées triviales par le LLM (`is_worth_indexing=False`).",
        "",
        "| Statut | Total |",
        "|---|---|",
        f"| Micro-sessions (< 3 tours) | {count_noise} |",
        f"| Rejetées par LLM (Triviales) | {count_llm} |",
        f"| **Total archivé** | **{total}** |",
        "",
        "---",
        "",
        "## Chronologie Exhaustive du Bruit",
        "",
    ]

    for s, origin in entries:
        dt_str = s.timestamp_start.strftime("%Y-%m-%d %H:%M")
        first_q = sanitize_turn_text(s.turns[0].user_prompt)[:140].replace("\n", " ").strip()
        first_r = sanitize_turn_text(s.turns[0].ai_response)[:160].replace("\n", " ").strip() if s.turns[0].ai_response else "N/A"
        line = f"- **[{dt_str}]** (`{s.session_id}` | {s.turn_count}t, {s.user_char_count}c | *{origin}*) — **Q:** {first_q} ➔ **R:** {first_r}"
        lines.append(line)

    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Registre du bruit compilé dans %s (%d sessions archivées).", out_path.name, total)
    return out_path


def generate_cold_start_episodic_journals(sessions: List[ReconstructedSession], db: DBManager) -> int:
    """
    Génère les journaux quotidiens rétroactifs 01_Episodique/YYYY-MM-DD.md
    et peuple daily_metrics à partir de l'historique Takeout (sessions Gemini).
    """
    settings.EPISODIC_DIR.mkdir(parents=True, exist_ok=True)

    # Récupération de l'état des sessions depuis SQLite pour obtenir les notes et topics associés
    session_meta_map: Dict[str, Dict[str, Any]] = {}
    with db.get_connection() as conn:
        cur = conn.execute("SELECT session_id, extracted_topics_json, generated_notes_json, summary, distillation_status FROM chat_sessions;")
        for row in cur.fetchall():
            session_meta_map[row["session_id"]] = {
                "topics": json.loads(row["extracted_topics_json"]) if row["extracted_topics_json"] else [],
                "notes": json.loads(row["generated_notes_json"]) if row["generated_notes_json"] else [],
                "summary": row["summary"] or "",
                "status": row["distillation_status"] or "pending",
            }

    # Regroupement des sessions par date YYYY-MM-DD
    by_date: Dict[str, List[ReconstructedSession]] = {}
    for s in sessions:
        d_str = s.timestamp_start.strftime("%Y-%m-%d")
        by_date.setdefault(d_str, []).append(s)

    sorted_dates = sorted(by_date.keys())
    generated_count = 0

    with tqdm(total=len(sorted_dates), desc="Génération Journaux Épisodiques", unit="jour") as pbar:
        for d_str in sorted_dates:
            day_sessions = sorted(by_date[d_str], key=lambda s: s.timestamp_start)

            total_duration_min = sum(compute_realistic_session_duration_min(s.turns) for s in day_sessions)
            total_duration_sec = total_duration_min * 60

            max_sess = max(day_sessions, key=lambda s: compute_realistic_session_duration_min(s.turns))
            max_hf_min = compute_realistic_session_duration_min(max_sess.turns)
            max_hf_sec = max_hf_min * 60
            max_meta = session_meta_map.get(max_sess.session_id, {})
            max_topic = (max_meta.get("topics") or ["General"])[0]

            topic_seconds: Dict[str, int] = {}
            topic_session_counts: Dict[str, int] = {}
            for s in day_sessions:
                dur_sec = compute_realistic_session_duration_min(s.turns) * 60
                meta = session_meta_map.get(s.session_id, {})
                t_list = meta.get("topics") or ["General"]
                primary_t = normalize_to_macro_topic(t_list[0])
                topic_seconds[primary_t] = topic_seconds.get(primary_t, 0) + dur_sec
                topic_session_counts[primary_t] = topic_session_counts.get(primary_t, 0) + 1

            sorted_topics = sorted(topic_seconds.items(), key=lambda x: x[1], reverse=True)

            # Mise à jour SQLite daily_metrics si aucune activité OS présente
            day_obj = datetime.strptime(d_str, "%Y-%m-%d").date()
            with db.get_connection() as conn:
                cur = conn.execute("SELECT total_screen_sec FROM daily_metrics WHERE date = ?;", (d_str,))
                existing_m = cur.fetchone()

            if not existing_m or existing_m["total_screen_sec"] == 0:
                top_topics_clean = {k: v for k, v in sorted_topics}
                db.upsert_daily_metrics(
                    DailyMetricRecord(
                        date=day_obj,
                        total_screen_sec=total_duration_sec,
                        active_production_sec=int(total_duration_sec * 0.7),
                        passive_exploration_sec=int(total_duration_sec * 0.3),
                        max_hyperfocus_sec=max_hf_sec,
                        max_hyperfocus_topic=max_topic,
                        context_switches_per_hour=round(len(day_sessions) / max(1.0, total_duration_sec / 3600.0), 2),
                        read_vs_write_ratio=0.4,
                        top_topics_json=json.dumps(top_topics_clean, ensure_ascii=False),
                    )
                )

            # Génération de la note 01_Episodique/YYYY-MM-DD.md
            episodic_file = settings.EPISODIC_DIR / f"{d_str}.md"
            should_write = True
            if episodic_file.exists():
                try:
                    f_content = episodic_file.read_text(encoding="utf-8")
                    if 'origin: "takeout_cold_start"' not in f_content and 'origin: takeout_cold_start' not in f_content:
                        should_write = False
                except Exception:
                    should_write = True

            if should_write:
                total_duration_fmt = f"{total_duration_min // 60}h{total_duration_min % 60:02d}" if total_duration_min >= 60 else f"{total_duration_min} min"
                max_hf_fmt = f"{max_hf_min // 60}h{max_hf_min % 60:02d}" if max_hf_min >= 60 else f"{max_hf_min} min"

                table_rows = []
                for top_name, top_sec in sorted_topics:
                    cnt = topic_session_counts.get(top_name, 1)
                    t_min = top_sec // 60
                    table_rows.append(f"| `{top_name}` | {cnt} | {t_min} min |")
                table_md = "\n".join(table_rows) if table_rows else "| `General` | 1 | 0 min |"

                sessions_md_lines = []
                for s in day_sessions:
                    s_hm = s.timestamp_start.strftime("%H:%M")
                    e_hm = s.timestamp_end.strftime("%H:%M")
                    s_dur = compute_realistic_session_duration_min(s.turns)
                    s_meta = session_meta_map.get(s.session_id, {})
                    s_notes = s_meta.get("notes") or []
                    s_summary = s_meta.get("summary") or s.summary

                    if s_notes:
                        note_slug = s_notes[0]
                        link_target = f"[[{note_slug}]]"
                        sessions_md_lines.append(f"- **{s_hm} - {e_hm}** ({s.turn_count} tours, {s_dur} min) — {link_target} : *{s_summary}*")
                    else:
                        sessions_md_lines.append(f"- **{s_hm} - {e_hm}** ({s.turn_count} tours, {s_dur} min) — `{s.session_id}` : *{s_summary}*")

                sessions_md = "\n".join(sessions_md_lines)
                topics_header_json = json.dumps([t[0] for t in sorted_topics], ensure_ascii=False)

                ep_content = f"""---
id: "{d_str.replace('-', '')}"
date: "{d_str}"
type: "episodic_journal"
origin: "takeout_cold_start"
total_reflection_min: {total_duration_min}
sessions_count: {len(day_sessions)}
top_topics: {topics_header_json}
---

# Journal Épisodique — {d_str}

## 1. Vue d'Ensemble & Télémétrie
- **Temps total de réflexion / dialogue IA :** {total_duration_fmt}
- **Nombre de sessions cognitives :** {len(day_sessions)}
- **Session d'hyperfocus maximale :** {max_hf_fmt} (`{max_topic}`)

### Répartition Thématique
| Macro-Catégorie | Sessions | Temps Estimé |
|---|---|---|
{table_md}

## 2. Sessions Cognitives Réalisées
{sessions_md}
"""
                episodic_file.write_text(ep_content, encoding="utf-8")
                generated_count += 1

            pbar.update(1)

    logger.info("Cold Start Épisodique achevé : %d journaux quotidiens rédigés dans 01_Episodique/.", generated_count)
    return generated_count


def save_distilled_concept_note(
    sess: ReconstructedSession,
    distilled: Optional[DistilledConceptSchema],
    db: DBManager,
    allow_quarantine: bool = False,
) -> Tuple[bool, str]:
    """
    Écrit la note conceptuelle Markdown et met à jour SQLite chat_sessions.
    Retourne (success: bool, status: 'success' | 'misc_noise' | 'failed_fallback' | 'skipped').
    Applique une protection stricte anti-écrasement : ne remplace jamais une note existante valide par #A_Trier.
    """
    duration_min = compute_realistic_session_duration_min(sess.turns)
    duration_fmt = f"{duration_min // 60}h{duration_min % 60:02d}" if duration_min >= 60 else f"{duration_min} min"

    if distilled and not distilled.is_worth_indexing:
        db.update_session_distillation_metadata(
            session_id=sess.session_id,
            topics_list=[],
            notes_list=[],
            summary=sess.summary,
            distillation_status="misc_noise",
        )
        return False, "misc_noise"

    if not distilled:
        if not allow_quarantine:
            return False, "failed"

        # Protection anti-écrasement : si une note valide existe déjà sur disque, ne jamais l'écraser par #A_Trier
        for existing_f in settings.CONCEPTS_DIR.glob("*.md"):
            try:
                txt = existing_f.read_text(encoding="utf-8", errors="replace")
                if f'session_id: "{sess.session_id}"' in txt and 'distillation_status: "success"' in txt:
                    logger.info("Protection anti-écrasement activée : note valide %s préservée pour %s.", existing_f.name, sess.session_id)
                    return True, "skipped"
            except Exception:
                pass

        first_user = sanitize_turn_text(sess.turns[0].user_prompt)[:100]
        clean_title = re.sub(r"[^\w\s-]", "", first_user).strip().title() or f"Session-{sess.session_id}"
        slug = f"a-trier-{sess.session_id.lower()}"
        macro_topic = "A_Trier"
        tags_list = ["a-trier", "failed-fallback"]
        summary_1l = sess.summary[:140] if sess.summary else first_user
        body_md = (
            f"### Problématique & Contexte\n{first_user}\n\n"
            f"### Arbitrages Techniques & Solutions\n"
            f"- Session en quarantaine technique après échec de distillation.\n"
            f"- {sess.turn_count} échanges techniques sauvegardés dans SQLite (`chat_messages`)."
        )
        related_list: List[str] = []
        dist_status = "failed_fallback"
    else:
        clean_title = distilled.concept_title
        slug = distilled.slug
        macro_topic = normalize_to_macro_topic(distilled.semantic_topic)
        tags_list = distilled.tags or []
        if macro_topic != distilled.semantic_topic and distilled.semantic_topic.lower() not in [t.lower() for t in tags_list]:
            tags_list.append(distilled.semantic_topic.lower())
        summary_1l = distilled.summary_1_line
        raw_body_md = distilled.synthesized_markdown_body
        body_md = re.sub(r'>\s*\[!abstract\]-[^\n]*\n(?:>[^\n]*\n)*', '', raw_body_md).strip()
        related_list = distilled.related_concepts or []
        dist_status = "success"

    created_date_str = sess.timestamp_start.strftime("%Y-%m-%d")
    updated_date_str = sess.timestamp_end.strftime("%Y-%m-%d")

    concept_file = settings.CONCEPTS_DIR / f"{slug}.md"
    if dist_status == "success" and concept_file.exists():
        try:
            existing_content = concept_file.read_text(encoding="utf-8", errors="replace")
            m_sid = re.search(r'session_id:\s*["\']?([^"\'\n\r]+)["\']?', existing_content)
            existing_sid = m_sid.group(1).strip() if m_sid else None
            if existing_sid and existing_sid != sess.session_id:
                # Collision de slug entre deux sessions distinctes
                short_sid = re.sub(r"[^a-zA-Z0-9]", "", sess.session_id)[:6].lower()
                slug = f"{slug}-{created_date_str}-{short_sid}"
                concept_file = settings.CONCEPTS_DIR / f"{slug}.md"
                logger.info("Anti-collision slug activée : renommage en '%s.md' pour session %s.", slug, sess.session_id)
        except Exception as exc:
            logger.warning("Erreur vérification collision slug pour %s : %s", concept_file.name, exc)

    concept_id = sess.timestamp_start.strftime("%Y%m%d%H%M")
    related_md = ", ".join([f"[[{rc}]]" for rc in related_list]) if related_list else "[[Exocortex]]"
    tags_json = json.dumps(tags_list, ensure_ascii=False)
    summary_clean = summary_1l.replace('"', "'")

    note_content = f"""---
id: "{concept_id}"
title: "{clean_title}"
type: "concept"
origin: ["gemini_takeout"]
semantic_topic: "{macro_topic}"
tags: {tags_json}
session_id: "{sess.session_id}"
distillation_status: "{dist_status}"
created_at: "{created_date_str}"
updated_at: "{updated_date_str}"
total_time_invested_min: {duration_min}
summary_1_line: "{summary_clean}"
---

# {clean_title}

{body_md}

> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)
> - **Temps estimé sur ce sujet :** {duration_fmt}
> - **Sources épisodiques :**
>   - Session Gemini `{sess.session_id}` du {created_date_str} ({sess.turn_count} échanges, {sess.user_char_count} chars écrits)
> - **Connexions sémantiques suggérées :** {related_md}
"""
    concept_file.write_text(note_content, encoding="utf-8")

    db.update_session_distillation_metadata(
        session_id=sess.session_id,
        topics_list=[macro_topic],
        notes_list=[slug],
        summary=summary_1l,
        distillation_status=dist_status,
    )
    return True, dist_status


def initialize_meta_and_concepts(
    sessions: List[ReconstructedSession],
    noise_sessions: List[ReconstructedSession],
    db: DBManager,
    max_distill_sessions: Optional[int] = None,
) -> None:
    """
    Initialise 00_Meta/, assainit l'existant, distille les sessions restantes via l'architecture
    à 3 vagues séquentielles (Multi-Pass VRAM Queue : 26B Thinking -> 26B No-Think -> 12B Fallback),
    compile le registre du bruit et reconstitue les journaux épisodiques.
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

    # 1. Validation de la taxonomie maîtresse fermée
    ensure_strict_taxonomy_file()

    # 2. Scanner d'Assainissement & Mode Delta (Skip des ~392 fiches déjà réussies)
    completed_session_ids = scan_and_upgrade_existing_concepts(db)

    # Préparation de la liste taxonomique pour le prompt LLM
    allowed_topics_str = "\n".join([f"- `{k}` : {v}" for k, v in AUTHORIZED_SEMANTIC_TOPICS.items() if k != "A_Trier"])

    # Sélection des sessions qualifiées
    qualified_sessions = sorted(
        [s for s in sessions if s.turn_count >= settings.MIN_TURNS_THRESHOLD and s.user_char_count >= settings.MIN_USER_CHARS_THRESHOLD],
        key=lambda s: s.user_char_count,
        reverse=True,
    )
    limit = max_distill_sessions if max_distill_sessions is not None else settings.TAKEOUT_MAX_DISTILL_SESSIONS
    target_sessions = qualified_sessions[:limit] if limit and limit > 0 else qualified_sessions

    # Filtrage Delta : seules les sessions non complétées (ou purgées) sont distillées
    sessions_to_distill = [s for s in target_sessions if s.session_id not in completed_session_ids]
    logger.info(
        "Plan de distillation LLM : %d sessions à traiter (%d déjà complétées ignorées via Mode Delta).",
        len(sessions_to_distill),
        len(completed_session_ids),
    )

    if sessions_to_distill and llm_client.is_alive():
        llm_client.ensure_local_gguf_models()

    ok_count = 0
    misc_count = 0
    a_trier_count = 0
    llm_rejected_sessions: List[ReconstructedSession] = []

    vague1_queue: List[ReconstructedSession] = list(sessions_to_distill)
    vague2_queue: List[ReconstructedSession] = []
    vague3_queue: List[ReconstructedSession] = []

    # ==========================================================================
    # VAGUE 1 : gemma4:26b-a4b (Thinking ACTIF, num_predict=8192, Prompt Complet)
    # ==========================================================================
    if vague1_queue and llm_client.is_alive():
        logger.info("--- DÉMARRAGE VAGUE 1 : gemma4:26b-a4b (Thinking ACTIF, num_predict=8192) [%d sessions] ---", len(vague1_queue))
        free_gb = llm_client.force_clear_vram()
        min_strict = getattr(settings, "VRAM_STRICT_ABORT_FREE_GB", 8.0)
        if free_gb < min_strict:
            logger.error("VRAM insuffisante avant Vague 1 (%.2f Go < %.2f Go). Report.", free_gb, min_strict)
            raise VRAMInsufficientError(f"VRAM insuffisante ({free_gb:.2f} Go < {min_strict} Go)")

        with tqdm(total=len(vague1_queue), desc="Distillation Vague 1 (26B Thinking)", unit="sess") as pbar:
            for sess in vague1_queue:
                clean_turns_text: List[str] = []
                for t in sess.turns:
                    u_clean = sanitize_turn_text(t.user_prompt, max_turn_chars=2500)
                    a_clean = sanitize_turn_text(t.ai_response, max_turn_chars=3500)
                    clean_turns_text.append(f"### Utilisateur :\n{u_clean}\n\n### Assistant :\n{a_clean}")
                session_text = "\n\n---\n\n".join(clean_turns_text)[:20000]

                user_prompt = PROMPT_SESSION_DISTILLATION_USER.format(
                    allowed_taxonomy=allowed_topics_str,
                    session_text=session_text,
                )

                distilled: Optional[DistilledConceptSchema] = None
                if settings.TAKEOUT_MODE == "cloud_api" and llm_client.is_cloud_available():
                    try:
                        distilled = llm_client.generate_cloud_sota(
                            prompt=user_prompt,
                            system=PROMPT_SESSION_DISTILLATION_SYSTEM,
                            response_model=DistilledConceptSchema,
                        )
                    except Exception as exc:
                        logger.warning("Échec Cloud SOTA pour %s : %s", sess.session_id, exc)

                if not distilled and llm_client.is_alive():
                    try:
                        distilled = llm_client.generate_structured(
                            prompt=user_prompt,
                            response_model=DistilledConceptSchema,
                            system=PROMPT_SESSION_DISTILLATION_SYSTEM,
                            model=settings.MODEL_HEAVY_SYNTHESIS,
                            keep_alive="30m",
                            enable_thinking=True,
                            num_predict=8192,
                            allow_model_switch_fallback=False,
                        )
                    except Exception as exc:
                        logger.warning("Échec Vague 1 pour session %s (%s). Mise en file d'attente Vague 2.", sess.session_id, exc)
                        vague2_queue.append(sess)
                        pbar.set_postfix({"ok": ok_count, "v2_pending": len(vague2_queue)})
                        pbar.update(1)
                        continue

                if distilled:
                    _, st = save_distilled_concept_note(sess, distilled, db, allow_quarantine=False)
                    if st == "success":
                        ok_count += 1
                    elif st == "misc_noise":
                        misc_count += 1
                        llm_rejected_sessions.append(sess)

                pbar.set_postfix({"ok": ok_count, "v2_pending": len(vague2_queue)})
                pbar.update(1)

    # ==========================================================================
    # VAGUE 2 : gemma4:26b-a4b (Toujours en VRAM, Prompt Condensé, think=False, num_predict=4096)
    # ==========================================================================
    if vague2_queue and llm_client.is_alive():
        logger.info("--- DÉMARRAGE VAGUE 2 : gemma4:26b-a4b (Prompt Condensé, think=False, num_predict=4096) [%d sessions] ---", len(vague2_queue))
        condensed_system_prompt = (
            PROMPT_SESSION_DISTILLATION_SYSTEM
            + "\n\nCONSIGNE STRICTE : Le champ synthesized_markdown_body doit être direct, dense et faire entre 250 et 400 mots maximum. Réponds immédiatement en JSON."
        )

        with tqdm(total=len(vague2_queue), desc="Distillation Vague 2 (26B No-Think)", unit="sess") as pbar:
            for sess in vague2_queue:
                clean_turns_text = []
                for t in sess.turns:
                    u_clean = sanitize_turn_text(t.user_prompt, max_turn_chars=800)
                    a_clean = sanitize_turn_text(t.ai_response, max_turn_chars=1000)
                    clean_turns_text.append(f"### Utilisateur :\n{u_clean}\n\n### Assistant :\n{a_clean}")
                session_text = "\n\n---\n\n".join(clean_turns_text)[:6000]

                user_prompt = PROMPT_SESSION_DISTILLATION_USER.format(
                    allowed_taxonomy=allowed_topics_str,
                    session_text=session_text,
                )

                distilled = None
                try:
                    distilled = llm_client.generate_structured(
                        prompt=user_prompt,
                        response_model=DistilledConceptSchema,
                        system=condensed_system_prompt,
                        model=settings.MODEL_HEAVY_SYNTHESIS,
                        keep_alive="30m",
                        enable_thinking=False,
                        num_predict=4096,
                        allow_model_switch_fallback=False,
                    )
                except Exception as exc:
                    logger.warning("Échec Vague 2 pour session %s (%s). Mise en file d'attente Vague 3 (12B).", sess.session_id, exc)
                    vague3_queue.append(sess)
                    pbar.set_postfix({"ok": ok_count, "v3_pending": len(vague3_queue)})
                    pbar.update(1)
                    continue

                if distilled:
                    _, st = save_distilled_concept_note(sess, distilled, db, allow_quarantine=False)
                    if st == "success":
                        ok_count += 1
                    elif st == "misc_noise":
                        misc_count += 1
                        llm_rejected_sessions.append(sess)

                pbar.set_postfix({"ok": ok_count, "v3_pending": len(vague3_queue)})
                pbar.update(1)

    # Déchargement UNIQUE du 26B à la fin de la Vague 2
    if llm_client.is_alive():
        llm_client.unload_model(settings.MODEL_HEAVY_SYNTHESIS)
        time.sleep(1.0)

    # ==========================================================================
    # VAGUE 3 : gemma4:12b (Chargé UNE seule fois, think=False, num_predict=4096)
    # ==========================================================================
    if vague3_queue and llm_client.is_alive():
        logger.info("--- DÉMARRAGE VAGUE 3 : gemma4:12b (Repli final, think=False, num_predict=4096) [%d sessions] ---", len(vague3_queue))
        condensed_system_prompt = (
            PROMPT_SESSION_DISTILLATION_SYSTEM
            + "\n\nCONSIGNE STRICTE : Le champ synthesized_markdown_body doit être direct, dense et faire entre 250 et 400 mots maximum. Réponds immédiatement en JSON."
        )

        with tqdm(total=len(vague3_queue), desc="Distillation Vague 3 (12B Fallback)", unit="sess") as pbar:
            for sess in vague3_queue:
                clean_turns_text = []
                for t in sess.turns:
                    u_clean = sanitize_turn_text(t.user_prompt, max_turn_chars=800)
                    a_clean = sanitize_turn_text(t.ai_response, max_turn_chars=1000)
                    clean_turns_text.append(f"### Utilisateur :\n{u_clean}\n\n### Assistant :\n{a_clean}")
                session_text = "\n\n---\n\n".join(clean_turns_text)[:6000]

                user_prompt = PROMPT_SESSION_DISTILLATION_USER.format(
                    allowed_taxonomy=allowed_topics_str,
                    session_text=session_text,
                )

                distilled = None
                try:
                    distilled = llm_client.generate_structured(
                        prompt=user_prompt,
                        response_model=DistilledConceptSchema,
                        system=condensed_system_prompt,
                        model=settings.MODEL_FAST_VISION,  # gemma4:12b
                        keep_alive="30m",
                        enable_thinking=False,
                        num_predict=4096,
                        allow_model_switch_fallback=False,
                    )
                except Exception as exc:
                    logger.error("Échec définitif Vague 3 pour session %s (%s). Quarantaine #A_Trier.", sess.session_id, exc)

                if distilled:
                    _, st = save_distilled_concept_note(sess, distilled, db, allow_quarantine=False)
                    if st == "success":
                        ok_count += 1
                    elif st == "misc_noise":
                        misc_count += 1
                        llm_rejected_sessions.append(sess)
                else:
                    # Échec définitif -> Sauvegarde en quarantaine avec protection anti-écrasement
                    _, st = save_distilled_concept_note(sess, None, db, allow_quarantine=True)
                    if st == "failed_fallback":
                        a_trier_count += 1

                pbar.set_postfix({"ok": ok_count, "a_trier": a_trier_count})
                pbar.update(1)

        # Déchargement UNIQUE du 12B à la fin de la Vague 3
        llm_client.unload_model(settings.MODEL_FAST_VISION)
        time.sleep(1.0)

    # Déchargement complet de la VRAM après la distillation
    llm_client.unload_all_models()
    logger.info("Distillation LLM achevée : %d réussies, %d en quarantaine, %d bruit LLM.", ok_count, a_trier_count, misc_count)

    # 4. Compilation du registre consolidé du bruit (00_Meta/00_MISC_ET_BRUIT_ARCHIVE.md)
    compile_misc_noise_archive(noise_sessions, llm_rejected_sessions)

    # 5. Cold Start Épisodique Rétroactif (01_Episodique/YYYY-MM-DD.md & daily_metrics)
    generate_cold_start_episodic_journals(sessions, db)


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

    def run(self, max_distill_sessions: Optional[int] = None) -> Dict[str, Any]:
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

        qualified_sessions, noise_sessions = sessionize_gemini_turns(gemini_turns)
        all_sessions = qualified_sessions + noise_sessions

        # 3b. Insertion exhaustive de tous les messages individuels dans chat_messages
        all_chat_messages: List[Tuple[str, int, datetime, str, str, int]] = []
        for sess in all_sessions:
            for turn_idx, turn in enumerate(sess.turns, 1):
                all_chat_messages.append((
                    sess.session_id,
                    turn_idx,
                    turn.timestamp,
                    turn.user_prompt,
                    turn.ai_response,
                    turn.user_char_count,
                ))
        if all_chat_messages:
            self.db.insert_chat_messages_batch(all_chat_messages)
            logger.info("Table chat_messages synchronisée : %d messages insérés.", len(all_chat_messages))

        # 4. Injection SQLite des sessions qualifiées uniquement (v0.1.3 : 480 sessions)
        session_records = [
            ChatSessionRecord(
                session_id=s.session_id,
                timestamp_start=s.timestamp_start,
                timestamp_end=s.timestamp_end,
                turn_count=s.turn_count,
                user_char_count=s.user_char_count,
                summary=s.summary,
                distillation_status="pending",
            )
            for s in qualified_sessions
        ]
        self.db.insert_chat_sessions_batch(session_records)

        # 5. Jointure temporelle [-60 min ; +30 min] (sur les sessions qualifiées)
        linked_count = perform_temporal_join(qualified_sessions, self.db)

        # 6. Burst Clustering sur les traces restantes
        burst_count = perform_burst_clustering(self.db)

        # 7. Génération des fichiers de staging
        user_prompts_file, batch_files, web_prompt_file = generate_staging_files(qualified_sessions)

        # 8. Initialisation de 00_Meta, assainissement existant, distillation Delta et Cold Start épisodique
        initialize_meta_and_concepts(
            qualified_sessions,
            noise_sessions,
            self.db,
            max_distill_sessions=max_distill_sessions,
        )

        # 9. Synchronisation Vectorielle LanceDB & Compilation Google Drive
        logger.info("--- SYNCHRONISATION VECTORIELLE LANCEDB ---")
        indexed_concepts = vector_store.sync_all_concepts()

        logger.info("--- COMPILATION DES MÉGA-FICHIERS GOOGLE DRIVE ---")
        drive_compiler = DriveCompiler(self.db)
        drive_files = drive_compiler.compile_all()

        db_stats = self.db.get_database_stats()
        logger.info("=== FIN DU MODULE 1 AVEC SUCCÈS ===")
        logger.info("Statistiques SQLite finales : %s", db_stats)

        return {
            "sessions_count": len(qualified_sessions),
            "noise_sessions_count": len(noise_sessions),
            "linked_footprints": linked_count,
            "burst_clusters": burst_count,
            "staging_prompts_file": str(user_prompts_file),
            "staging_batches_count": len(batch_files),
            "web_prompt_file": str(web_prompt_file),
            "indexed_concepts_count": indexed_concepts,
            "drive_files": {k: str(v) for k, v in drive_files.items()},
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
