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
from src.llm.ollama_client import VRAMInsufficientError, llm_client
from src.llm.prompts import (
    PROFILE_SPLIT_MARKER,
    PROMPT_BURST_CLUSTER_SYSTEM,
    PROMPT_BURST_CLUSTER_USER,
    PROMPT_COGNITIVE_PROFILING_SYSTEM,
    PROMPT_COGNITIVE_PROFILING_USER,
    PROMPT_SESSION_DISTILLATION_SYSTEM,
    PROMPT_SESSION_DISTILLATION_USER,
    PROMPT_STRICT_TAXONOMY_RULE,
    SYSTEM_PROMPT_ANTI_WIKIPEDIA,
)

logger = logging.getLogger("Exocortex.TakeoutIngestor")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

# Marqueur du profil cognitif par défaut : tant qu'il est présent, le profil peut être remplacé
# automatiquement (mode cloud_api) ou par --import-profile (v0.5.3, B15).
PROFILE_TEMPLATE_MARKER = "<!-- exocortex:profil-gabarit -->"
_LEGACY_PROFILE_TEMPLATE_SIGNATURE = "- Rigueur technique absolue, orientation systèmes et architectures locales robustes."

# Nombre de rafales classées par appel au 12B (B11)
BURST_LLM_BATCH_SIZE = 15


def _allowed_taxonomy_block() -> str:
    return "\n".join(f"- `{k}` : {v}" for k, v in AUTHORIZED_SEMANTIC_TOPICS.items() if k != "A_Trier")


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


from src.ingestors.takeout_parsers import (
    FRENCH_MONTH_MAP,
    ParsedTurn,
    ReconstructedSession,
    compute_realistic_session_duration_min,
    parse_date_flexible,
    parse_gemini_html,
    parse_gemini_json,
    parse_google_search_export,
    parse_youtube_export,
    sanitize_turn_text,
    sessionize_gemini_turns,
)
from src.consolidators.vault_doctor import (
    VaultDoctor,
    ensure_strict_taxonomy_file,
    register_new_taxonomy_tag,
    scan_and_upgrade_existing_concepts,
)
from src.utils.episodic_journal import SECTION_AI_SESSIONS, write_journal_section
from src.utils.markdown_io import (
    ConceptFrontmatter,
    ParsedConceptNote,
    parse_concept_file,
    parse_concept_string,
    write_concept_file,
)


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
            "4. Copiez-collez l'intégralité du prompt ci-dessous dans la zone de texte.\n"
            "5. Enregistrez la réponse de Gemini dans un fichier texte, puis importez-la :\n"
            "   python run_exocortex.py --import-profile <chemin_du_fichier>\n\n"
            "--------------------------- DÉBUT DU PROMPT À COPIER ---------------------------\n"
        )
        f.write(PROMPT_COGNITIVE_PROFILING_SYSTEM.format(allowed_taxonomy=_allowed_taxonomy_block()))
        f.write(
            "\n\nTu trouveras en pièce jointe le document '00_USER_PROMPTS_ONLY.md' contenant l'historique complet.\n"
            "Analyse l'intégralité de ces prompts et rédige le contenu complet de '00_Meta/Profil_Cognitif.md', "
            "en Markdown, commençant par le titre '# Profil Cognitif & Empreinte Intellectuelle'.\n"
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


class BurstTopicItem(BaseModel):
    cluster_id: str = Field(description="Identifiant exact de la rafale")
    semantic_topic: str = Field(description="L'une des macro-catégories autorisées")


class BurstBatchClassification(BaseModel):
    clusters: List[BurstTopicItem] = Field(default_factory=list)


def heuristic_burst_topic(queries: List[str], min_votes: int = 2) -> Optional[str]:
    """
    Repli CPU sans LLM (B11) : chaque mot des requêtes vote pour une macro-catégorie via
    normalize_to_macro_topic ; la catégorie majoritaire est retenue si elle réunit min_votes voix.
    """
    votes: Dict[str, int] = {}
    for q in queries:
        for word in set(re.findall(r"[a-zA-ZÀ-ÿ0-9][\wÀ-ÿ'-]{2,}", q.lower())):
            topic = normalize_to_macro_topic(word)
            if topic != "A_Trier":
                votes[topic] = votes.get(topic, 0) + 1
    if not votes:
        return None
    best, count = max(votes.items(), key=lambda kv: kv[1])
    return best if count >= min_votes else None


def classify_burst_clusters(db: DBManager, min_events: int = settings.SEARCH_BURST_MIN_EVENTS) -> int:
    """
    Attribue un semantic_topic aux rafales Search/YouTube qui n'en ont pas (v0.5.3, B11) :
    lots de BURST_LLM_BATCH_SIZE rafales par appel au 12B, puis repli heuristique pour les
    rafales non résolues (Ollama hors ligne, VRAM insuffisante, réponse invalide).
    Retourne le nombre de rafales classées.
    """
    clusters = db.get_untopiced_burst_clusters(min_events=min_events)
    if not clusters:
        return 0
    logger.info("Classification thématique de %d rafale(s) Search/YouTube...", len(clusters))

    resolved: Dict[str, str] = {}
    if llm_client.is_alive():
        allowed = _allowed_taxonomy_block()
        try:
            for start in range(0, len(clusters), BURST_LLM_BATCH_SIZE):
                batch = clusters[start:start + BURST_LLM_BATCH_SIZE]
                block = "\n".join(
                    f"- `{c['cluster_id']}` : " + " | ".join((c["queries"] or "").split(" || ")[:12])[:900]
                    for c in batch
                )
                try:
                    res = llm_client.generate_structured(
                        prompt=PROMPT_BURST_CLUSTER_USER.format(allowed_taxonomy=allowed, clusters_block=block),
                        response_model=BurstBatchClassification,
                        system=PROMPT_BURST_CLUSTER_SYSTEM,
                        model=settings.MODEL_FAST_VISION,
                        keep_alive="5m",
                        enable_thinking=False,
                        num_predict=2048,
                    )
                except VRAMInsufficientError:
                    raise
                except Exception as exc:
                    logger.warning("Échec de classification LLM d'un lot de rafales : %s", exc)
                    continue
                batch_ids = {c["cluster_id"] for c in batch}
                for item in res.clusters:
                    if item.cluster_id in batch_ids:
                        resolved[item.cluster_id] = normalize_to_macro_topic(item.semantic_topic)
        except VRAMInsufficientError as exc:
            logger.warning("VRAM insuffisante pour classer les rafales au 12B (%s) : repli heuristique.", exc)
        finally:
            llm_client.unload_model(settings.MODEL_FAST_VISION)

    classified = 0
    for c in clusters:
        topic = resolved.get(c["cluster_id"])
        if not topic or topic == "A_Trier":
            topic = heuristic_burst_topic((c["queries"] or "").split(" || "))
        if topic:
            db.set_cluster_topic(c["cluster_id"], topic)
            classified += 1
    logger.info("%d rafale(s) classée(s) sur %d.", classified, len(clusters))
    return classified


# ==============================================================================
# PROFIL COGNITIF (v0.5.3, B15)
# ==============================================================================

def is_profile_template(path: Optional[Path] = None) -> bool:
    """Vrai si le profil est absent ou encore le gabarit par défaut (remplaçable automatiquement)."""
    target = path or settings.PROFIL_COGNITIF_PATH
    if not target.exists():
        return True
    content = target.read_text(encoding="utf-8", errors="replace")
    return PROFILE_TEMPLATE_MARKER in content or _LEGACY_PROFILE_TEMPLATE_SIGNATURE in content


def extract_profile_from_reply(reply: str) -> str:
    """
    Extrait le profil d'une réponse Gemini : partie précédant ===SPLIT_LIVRABLE=== (anciennes
    consignes à deux livrables), en-tête « SECTION 1 » et blocs ```markdown retirés.
    """
    text = reply.strip()
    if PROFILE_SPLIT_MARKER in text:
        text = text.split(PROFILE_SPLIT_MARKER, 1)[0].strip()
    text = re.sub(r"^```(?:markdown|md)?\s*\n", "", text)
    text = re.sub(r"\n```\s*$", "", text)
    text = re.sub(r"^#\s*SECTION\s*1\s*:[^\n]*\n", "", text, flags=re.IGNORECASE).strip()
    if not text.startswith("#"):
        text = f"# Profil Cognitif & Empreinte Intellectuelle\n\n{text}"
    return text


def import_cognitive_profile(reply: str, target: Optional[Path] = None) -> Path:
    """Écrit le profil extrait d'une réponse Gemini dans 00_Meta/Profil_Cognitif.md (la taxonomie reste fermée)."""
    profile = extract_profile_from_reply(reply)
    if len(profile) < 200:
        raise ValueError("Profil trop court ou vide : vérifiez le fichier importé.")
    out = target or settings.PROFIL_COGNITIF_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(profile + "\n", encoding="utf-8")
    logger.info("Profil cognitif importé dans %s (%d caractères).", out, len(profile))
    return out


def generate_cognitive_profile_cloud(user_prompts_file: Path, max_chars: int = 3_000_000) -> Optional[Path]:
    """
    Mode cloud_api : produit automatiquement le profil via Gemini à partir de 00_USER_PROMPTS_ONLY.md,
    uniquement si le profil est encore le gabarit (un profil importé ou écrit à la main n'est jamais écrasé).
    """
    if settings.TAKEOUT_MODE != "cloud_api" or not llm_client.is_cloud_available():
        return None
    if not is_profile_template() or not user_prompts_file.exists():
        return None
    prompts_content = user_prompts_file.read_text(encoding="utf-8", errors="replace")[:max_chars]
    try:
        reply = llm_client.generate_cloud_sota(
            prompt=PROMPT_COGNITIVE_PROFILING_USER.format(prompts_content=prompts_content),
            system=PROMPT_COGNITIVE_PROFILING_SYSTEM.format(allowed_taxonomy=_allowed_taxonomy_block()),
        )
        return import_cognitive_profile(str(reply))
    except Exception as exc:
        logger.warning("Profil cognitif cloud non généré : %s", exc)
        return None


# ==============================================================================
# PASSE 2 & 3 : PROFILAGE ET DISTILLATION DES PREMIÈRES NOTES ATOMIQUES
# ==============================================================================


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
                        # Ratios production/exploration et lecture/écriture fixés : estimation (A9)
                        is_estimated=True,
                    )
                )

            # Section « sessions IA » du journal unique (A10) : la section télémétrie écrite par la
            # consolidation nocturne pour la même date est conservée, et inversement.
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

            ai_section = f"""## Sessions IA (Gemini)
- **Temps total de réflexion / dialogue IA (estimé) :** {total_duration_fmt}
- **Nombre de sessions cognitives :** {len(day_sessions)}
- **Session d'hyperfocus maximale :** {max_hf_fmt} (`{max_topic}`)

### Répartition Thématique
| Macro-Catégorie | Sessions | Temps Estimé |
|---|---|---|
{table_md}

### Sessions Cognitives Réalisées
{sessions_md}"""
            write_journal_section(
                d_str,
                SECTION_AI_SESSIONS,
                ai_section,
                frontmatter_updates={
                    "total_reflection_min": total_duration_min,
                    "sessions_count": len(day_sessions),
                    "top_topics": [t[0] for t in sorted_topics],
                },
                source="takeout_cold_start",
            )
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
                note_parsed = parse_concept_file(existing_f)
                if (
                    note_parsed.frontmatter.session_id == sess.session_id
                    and note_parsed.frontmatter.distillation_status == "success"
                ):
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
            existing_note = parse_concept_file(concept_file)
            existing_sid = existing_note.frontmatter.session_id
            if existing_sid and existing_sid != sess.session_id:
                # Collision de slug entre deux sessions distinctes
                short_sid = re.sub(r"[^a-zA-Z0-9]", "", sess.session_id)[:6].lower()
                slug = f"{slug}-{created_date_str}-{short_sid}"
                concept_file = settings.CONCEPTS_DIR / f"{slug}.md"
                logger.info("Anti-collision slug activée : renommage en '%s.md' pour session %s.", slug, sess.session_id)
        except Exception as exc:
            logger.warning("Erreur vérification collision slug pour %s : %s", concept_file.name, exc)

    concept_id = sess.timestamp_start.strftime("%Y%m%d%H%M")
    related_md = ", ".join([f"[[{rc}]]" for rc in related_list]) if related_list else "—"

    fm = ConceptFrontmatter(
        id=concept_id,
        title=clean_title,
        type="concept",
        origin=["gemini_takeout"],
        semantic_topic=macro_topic,
        tags=tags_list,
        session_id=sess.session_id,
        distillation_status=dist_status,
        created_at=created_date_str,
        updated_at=updated_date_str,
        total_time_invested_min=duration_min,
        summary_1_line=summary_1l,
    )
    telemetry_lines = [
        "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)",
        f"> - **Temps estimé sur ce sujet :** {duration_fmt}",
        "> - **Sources épisodiques :**",
        f">   - Session Gemini `{sess.session_id}` du {created_date_str} ({sess.turn_count} échanges, {sess.user_char_count} chars écrits)",
        f"> - **Connexions sémantiques suggérées :** {related_md}",
    ]
    parsed_note = ParsedConceptNote(
        frontmatter=fm,
        title_h1=clean_title,
        body=body_md,
        telemetry_lines=telemetry_lines,
        file_path=concept_file,
    )
    write_concept_file(parsed_note, concept_file)

    db.update_session_distillation_metadata(
        session_id=sess.session_id,
        topics_list=[macro_topic],
        notes_list=[slug],
        summary=summary_1l,
        distillation_status=dist_status,
    )
    return True, dist_status


def _build_distillation_prompt(
    sess: ReconstructedSession,
    allowed_topics_str: str,
    max_user_chars: int,
    max_ai_chars: int,
    max_total_chars: int,
) -> str:
    """Construit le prompt de distillation d'une session (taille adaptée à chaque vague)."""
    clean_turns_text: List[str] = []
    for t in sess.turns:
        u_clean = sanitize_turn_text(t.user_prompt, max_turn_chars=max_user_chars)
        a_clean = sanitize_turn_text(t.ai_response, max_turn_chars=max_ai_chars)
        clean_turns_text.append(f"### Utilisateur :\n{u_clean}\n\n### Assistant :\n{a_clean}")
    session_text = "\n\n---\n\n".join(clean_turns_text)[:max_total_chars]
    return PROMPT_SESSION_DISTILLATION_USER.format(allowed_taxonomy=allowed_topics_str, session_text=session_text)


def initialize_meta_and_concepts(
    sessions: List[ReconstructedSession],
    noise_sessions: List[ReconstructedSession],
    db: DBManager,
    max_distill_sessions: Optional[int] = None,
) -> Dict[str, int]:
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
                f"{PROFILE_TEMPLATE_MARKER}\n"
                "> Gabarit par défaut : remplacez-le via `python run_exocortex.py --import-profile <fichier>` "
                "(mode web_manual) ou laissez le mode cloud_api le générer.\n\n"
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

    ok_count = 0
    misc_count = 0
    a_trier_count = 0
    llm_rejected_sessions: List[ReconstructedSession] = []
    deferred_sessions: List[ReconstructedSession] = []

    def _record(st: str, sess: ReconstructedSession) -> None:
        nonlocal ok_count, misc_count
        if st == "success":
            ok_count += 1
        elif st == "misc_noise":
            misc_count += 1
            llm_rejected_sessions.append(sess)

    vague1_queue: List[ReconstructedSession] = list(sessions_to_distill)
    vague2_queue: List[ReconstructedSession] = []
    vague3_queue: List[ReconstructedSession] = []

    # ==========================================================================
    # VAGUE 0 (mode cloud_api) : Gemini Cloud, indépendante d'Ollama et de la VRAM (B14)
    # ==========================================================================
    if vague1_queue and settings.TAKEOUT_MODE == "cloud_api" and llm_client.is_cloud_available():
        logger.info("--- DISTILLATION CLOUD SOTA (%s) [%d sessions] ---", settings.GEMINI_MODEL, len(vague1_queue))
        local_fallback: List[ReconstructedSession] = []
        with tqdm(total=len(vague1_queue), desc="Distillation Cloud SOTA", unit="sess") as pbar:
            for sess in vague1_queue:
                try:
                    distilled_cloud = llm_client.generate_cloud_sota(
                        prompt=_build_distillation_prompt(sess, allowed_topics_str, 2500, 3500, 20000),
                        system=PROMPT_SESSION_DISTILLATION_SYSTEM,
                        response_model=DistilledConceptSchema,
                    )
                    _, st = save_distilled_concept_note(sess, distilled_cloud, db, allow_quarantine=False)
                    _record(st, sess)
                except Exception as exc:
                    logger.warning("Échec Cloud SOTA pour %s : %s. Repli local.", sess.session_id, exc)
                    local_fallback.append(sess)
                pbar.update(1)
        vague1_queue = local_fallback

    if vague1_queue and llm_client.is_alive():
        llm_client.ensure_local_gguf_models()
    elif vague1_queue:
        logger.warning("Ollama hors ligne : %d session(s) restent en attente (pending) pour un prochain run.", len(vague1_queue))
        deferred_sessions.extend(vague1_queue)
        vague1_queue = []

    # ==========================================================================
    # VAGUE 1 : gemma4:26b-a4b (Thinking ACTIF, num_predict=8192, Prompt Complet)
    # ==========================================================================
    if vague1_queue and llm_client.is_alive():
        free_gb = llm_client.force_clear_vram()
        min_strict = getattr(settings, "VRAM_STRICT_ABORT_FREE_GB", 8.0)
        if free_gb < min_strict:
            # Report sans interrompre le pipeline (B13) : les sessions restent 'pending' et seront
            # reprises au prochain run grâce au mode Delta ; bruit et journaux sont tout de même produits.
            logger.error(
                "VRAM insuffisante avant Vague 1 (%.2f Go < %.2f Go). Distillation de %d session(s) reportée.",
                free_gb, min_strict, len(vague1_queue),
            )
            deferred_sessions.extend(vague1_queue)
            vague1_queue = []

    if vague1_queue and llm_client.is_alive():
        logger.info("--- DÉMARRAGE VAGUE 1 : gemma4:26b-a4b (Thinking ACTIF, num_predict=8192) [%d sessions] ---", len(vague1_queue))
        with tqdm(total=len(vague1_queue), desc="Distillation Vague 1 (26B Thinking)", unit="sess") as pbar:
            for sess in vague1_queue:
                user_prompt = _build_distillation_prompt(sess, allowed_topics_str, 2500, 3500, 20000)

                distilled: Optional[DistilledConceptSchema] = None
                if llm_client.is_alive():
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
                    _record(st, sess)

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
                user_prompt = _build_distillation_prompt(sess, allowed_topics_str, 800, 1000, 6000)

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
                    _record(st, sess)

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
                user_prompt = _build_distillation_prompt(sess, allowed_topics_str, 800, 1000, 6000)

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
                    _record(st, sess)
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
    if deferred_sessions:
        logger.warning(
            "%d session(s) reportée(s) (Ollama hors ligne ou VRAM insuffisante) : elles restent 'pending' "
            "et seront distillées au prochain run.",
            len(deferred_sessions),
        )

    # 4. Compilation du registre consolidé du bruit (00_Meta/00_MISC_ET_BRUIT_ARCHIVE.md)
    compile_misc_noise_archive(noise_sessions, llm_rejected_sessions)

    # 5. Cold Start Épisodique Rétroactif (01_Episodique/YYYY-MM-DD.md & daily_metrics)
    generate_cold_start_episodic_journals(sessions, db)

    return {
        "distilled_success": ok_count,
        "quarantined": a_trier_count,
        "llm_noise": misc_count,
        "deferred_sessions": len(deferred_sessions),
    }


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

        # 6. Burst Clustering sur les traces restantes, puis topic de chaque rafale (B11)
        burst_count = perform_burst_clustering(self.db)
        bursts_topiced = classify_burst_clusters(self.db)

        # 7. Génération des fichiers de staging
        user_prompts_file, batch_files, web_prompt_file = generate_staging_files(qualified_sessions)

        # 7b. Mode cloud_api : profil cognitif automatique tant que le profil est le gabarit (B15)
        settings.ensure_directories()
        profile_path = generate_cognitive_profile_cloud(user_prompts_file)

        # 8. Initialisation de 00_Meta, assainissement existant, distillation Delta et Cold Start épisodique
        distillation_report = initialize_meta_and_concepts(
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
            "burst_clusters_topiced": bursts_topiced,
            "cognitive_profile_generated": bool(profile_path),
            "distillation": distillation_report,
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
