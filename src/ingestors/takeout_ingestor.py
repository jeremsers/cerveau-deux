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
    PROMPT_COGNITIVE_PROFILING_SYSTEM,
    PROMPT_COGNITIVE_PROFILING_USER,
    PROMPT_SESSION_DISTILLATION_SYSTEM,
    PROMPT_SESSION_DISTILLATION_USER,
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
    semantic_topic: str = Field(description="Tag de la taxonomie existante ou nouveau tag Domaine_SousDomaine")
    is_new_topic: bool = Field(default=False, description="True si semantic_topic est une nouvelle catégorie absente de la liste")
    new_topic_description: Optional[str] = Field(default=None, description="Description en 1 phrase si nouveau topic")
    tags: List[str] = Field(description="3 à 5 sous-tags techniques en minuscule")
    summary_1_line: str = Field(description="Résumé dense en une seule phrase de la conclusion ou de l'architecture.")
    synthesized_markdown_body: str = Field(
        description="Synthèse structurée en Markdown (sections ### Contexte, ### Arbitrages & Architecture, ### Conclusions & Commandes Clés). Zéro intro Wikipédia."
    )
    related_concepts: List[str] = Field(description="2 à 3 titres de concepts connexes pour le maillage Obsidian")


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
    # 1. Suppression des séquences d'espaces/tabulations de scraping UI (ex: SillyTavern sliders)
    cleaned = re.sub(r"(?:[\t \xa0]{4,}\n){3,}", "\n[Dump d'interface UI omis]\n", text)
    # 2. Compression des logs d'erreurs ou stacktraces de plus de 15 lignes consécutives
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
    total_sec = 180.0  # 3 min de base pour l'ouverture de session
    max_gap_sec = max_gap_min * 60.0
    for i in range(1, len(turns)):
        delta_sec = max(0.0, (turns[i].timestamp - turns[i - 1].timestamp).total_seconds())
        total_sec += min(delta_sec, max_gap_sec)
    return max(5, int(round(total_sec / 60.0)))


def register_new_taxonomy_tag(tag_name: str, description: Optional[str] = None) -> bool:
    """
    Ajoute proprement un nouveau topic validé au format strict Domaine_SousDomaine dans Taxonomie_Tags.md.
    """
    if not tag_name or not re.match(r"^[A-Za-z0-9]+_[A-Za-z0-9_]+$", tag_name):
        return False
    tax_path = settings.TAXONOMIE_TAGS_PATH
    if not tax_path.exists():
        return False

    content = tax_path.read_text(encoding="utf-8")
    if f"`{tag_name}`" in content or f"**{tag_name}**" in content:
        return False

    desc_text = description or "Sujet émergent qualifié par distillation"
    new_entry = f"\n- `{tag_name}` : {desc_text}\n"

    with open(tax_path, "a", encoding="utf-8") as f:
        f.write(new_entry)
    logger.info("Nouveau tag taxonomique enregistré dans %s : `%s`", tax_path.name, tag_name)
    return True


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

            # Règle anti-bruit stricte : ignorer si moins de 3 tours OU moins de 250 caractères
            if t_count < min_turns or total_chars < min_user_chars:
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

    # Lecture et extraction de la taxonomie maîtresse
    allowed_topics_list: List[str] = []
    if settings.TAXONOMIE_TAGS_PATH.exists():
        with open(settings.TAXONOMIE_TAGS_PATH, "r", encoding="utf-8") as f:
            for line in f:
                m_tag = re.search(r"-\s*`?([A-Za-z0-9]+_[A-Za-z0-9_]+)`?", line)
                if m_tag:
                    allowed_topics_list.append(m_tag.group(1))

    if not allowed_topics_list:
        allowed_topics_list = [
            "Dev_Web_et_Stack_Astro", "IA_Agentique_et_RAG", "LLM_Local_et_Hardware",
            "Chefferie_Projet_et_UX", "Freelance_et_Acquisition", "Gaming_Solo_et_Modding",
            "MMORPG_Theorycraft", "Webtoons_Manga_et_Anime", "Analyse_Musicale_et_MAO",
            "Nutrition_Volume_Eating", "Sante_et_Admin_Perso", "Introspection_et_Neuroatypie",
        ]
    allowed_topics_str = "\n".join([f"- `{t}`" for t in allowed_topics_list])

    # Sélection des sessions les plus qualifiées pour la distillation initiale
    top_sessions = sorted(
        [s for s in sessions if s.turn_count >= 3 and s.user_char_count >= 300],
        key=lambda s: s.user_char_count,
        reverse=True,
    )[:10]

    created_notes_count = 0
    for sess in top_sessions:
        # Récupération des empreintes corrélées à cette session
        footprints = db.get_footprints_for_session(sess.session_id)
        footprints_md = ""
        if footprints:
            footprints_md = "> - **Requêtes et vidéos corrélées :**\n"
            for fp in footprints[:8]:
                footprints_md += f">   - [{fp['source']}] {fp['title_or_query']}\n"

        # Calcul mathématique réaliste du temps investi
        duration_min = compute_realistic_session_duration_min(sess.turns)
        duration_fmt = f"{duration_min // 60}h{duration_min % 60:02d}" if duration_min >= 60 else f"{duration_min} min"

        # Nettoyage et assainissement des tours pour le LLM
        clean_turns_text: List[str] = []
        for t in sess.turns:
            u_clean = sanitize_turn_text(t.user_prompt, max_turn_chars=1500)
            a_clean = sanitize_turn_text(t.ai_response, max_turn_chars=2000)
            clean_turns_text.append(f"### Utilisateur :\n{u_clean}\n\n### Assistant :\n{a_clean}")
        session_text = "\n\n---\n\n".join(clean_turns_text)[:12000]

        # Appel LLM structuré pour distillation réelle
        distilled: Optional[DistilledConceptSchema] = None
        user_prompt = PROMPT_SESSION_DISTILLATION_USER.format(
            allowed_taxonomy=allowed_topics_str,
            session_text=session_text,
        )

        # 1. Tentative Cloud SOTA si configuré
        if settings.TAKEOUT_MODE == "cloud_api" and llm_client.is_cloud_available():
            try:
                cloud_raw = llm_client.generate_cloud_sota(
                    prompt=user_prompt,
                    system_prompt=PROMPT_SESSION_DISTILLATION_SYSTEM,
                )
                m_json = re.search(r"\{.*\}", cloud_raw, re.DOTALL)
                if m_json:
                    distilled = DistilledConceptSchema.model_validate(json.loads(m_json.group(0)))
            except Exception as exc:
                logger.warning("Échec de distillation Cloud SOTA pour session %s : %s", sess.session_id, exc)

        # 2. Tentative LLM Local (Ollama ou llama_server)
        if not distilled and llm_client.is_alive():
            try:
                distilled = llm_client.generate_structured(
                    prompt=user_prompt,
                    response_model=DistilledConceptSchema,
                    system=PROMPT_SESSION_DISTILLATION_SYSTEM,
                    model=settings.MODEL_FAST_VISION,
                    keep_alive=0,
                )
            except Exception as exc:
                logger.warning("Échec de distillation locale pour session %s : %s", sess.session_id, exc)

        # 3. Repli heuristique si le LLM est inaccessible
        if not distilled:
            first_user = sanitize_turn_text(sess.turns[0].user_prompt)[:100]
            clean_title = re.sub(r"[^\w\s-]", "", first_user).strip().title()
            slug = re.sub(r"[\s_]+", "-", clean_title.lower())[:50].strip("-") or f"session-{sess.session_id}"
            
            # Détection de topic par mots-clés
            matched_topic = "A_Trier"
            text_low = (sess.summary + " " + first_user).lower()
            for cand in allowed_topics_list:
                cand_kws = cand.lower().split("_")
                if any(kw in text_low for kw in cand_kws if len(kw) > 3):
                    matched_topic = cand
                    break

            distilled = DistilledConceptSchema(
                is_worth_indexing=True,
                concept_title=clean_title,
                slug=slug,
                semantic_topic=matched_topic,
                is_new_topic=False,
                tags=[matched_topic.lower(), "takeout_coldstart"],
                summary_1_line=sess.summary[:140],
                synthesized_markdown_body=(
                    f"### Problématique & Contexte\n{first_user}\n\n"
                    f"### Arbitrages Techniques & Solutions\n"
                    f"- Session composée de {sess.turn_count} échanges techniques.\n"
                    f"- Conclusion principale : {sanitize_turn_text(sess.turns[-1].ai_response)[:400]}..."
                ),
                related_concepts=[matched_topic],
            )

        if not distilled.is_worth_indexing:
            logger.info("Session %s considérée comme bruit par la distillation.", sess.session_id)
            continue

        # Gestion de la taxonomie dynamique émergente
        if distilled.is_new_topic and distilled.semantic_topic:
            register_new_taxonomy_tag(distilled.semantic_topic, distilled.new_topic_description)
            if distilled.semantic_topic not in allowed_topics_list:
                allowed_topics_list.append(distilled.semantic_topic)

        # Sauvegarde de la note dans 02_Concepts/
        concept_file = settings.CONCEPTS_DIR / f"{distilled.slug}.md"
        created_date_str = sess.timestamp_start.strftime("%Y-%m-%d")
        updated_date_str = sess.timestamp_end.strftime("%Y-%m-%d")
        concept_id = sess.timestamp_start.strftime("%Y%m%d%H%M")

        related_md = ", ".join([f"[[{rc}]]" for rc in distilled.related_concepts]) if distilled.related_concepts else "[[Exocortex]]"
        tags_json = json.dumps(distilled.tags, ensure_ascii=False)

        note_content = f"""---
id: "{concept_id}"
title: "{distilled.concept_title}"
type: "concept"
origin: ["gemini_takeout"]
semantic_topic: "{distilled.semantic_topic}"
tags: {tags_json}
created_at: "{created_date_str}"
updated_at: "{updated_date_str}"
total_time_invested_min: {duration_min}
summary_1_line: "{distilled.summary_1_line.replace('"', "'")}"
---

# {distilled.concept_title}

{distilled.synthesized_markdown_body}

> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)
> - **Temps estimé sur ce sujet :** {duration_fmt}
> - **Sources épisodiques :**
>   - Session Gemini `{sess.session_id}` du {created_date_str} ({sess.turn_count} échanges, {sess.user_char_count} chars écrits)
{footprints_md}> - **Connexions sémantiques suggérées :** {related_md}
"""
        with open(concept_file, "w", encoding="utf-8") as f:
            f.write(note_content)
        created_notes_count += 1
        logger.info("Fiche conceptuelle distillée créée : %s (#%s)", concept_file.name, distilled.semantic_topic)

        # Mise à jour des métadonnées dans SQLite (chat_sessions)
        db.update_session_distillation_metadata(
            session_id=sess.session_id,
            topics_list=[distilled.semantic_topic],
            notes_list=[distilled.slug],
            summary=distilled.summary_1_line,
        )

    logger.info("Distillation LLM achevée : %d fiches conceptuelles créées dans 02_Concepts/.", created_notes_count)


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
