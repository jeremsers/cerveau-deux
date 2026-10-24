"""
Module 3 : Le Consolidateur Nocturne Bi-Modèle (Le Sommeil Paradoxal).
Exécuté la nuit pour consolider les journées d'activité :
- Passe 1 (gemma4:12b) : Analyse visuelle des captures .webp, classification sémantique SQLite, purge VRAM.
- Agrégation Analytique : Calcul des tunnels d'hyperfocus, fragmentation et bilan daily_metrics.
- Passe 2 (gemma4:26b-a4b ou fallback 12b) : Rédaction de 01_Episodique/YYYY-MM-DD.md et des fiches 02_Concepts/.
- Passe 3 (bge-m3) : Vectorisation et indexation k-NN dans LanceDB, purge VRAM finale.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pydantic import BaseModel, Field
from tqdm import tqdm

from src.config import AUTHORIZED_SEMANTIC_TOPICS, normalize_to_macro_topic, settings
from src.database.db_manager import (
    DailyMetricRecord,
    DBManager,
    HistoricalFootprintRecord,
    RawActivityRecord,
)
from src.database.vector_store import vector_store
from src.consolidators.drive_compiler import DriveCompiler
from src.llm.ollama_client import HardwareProbe, VRAMInsufficientError, llm_client
from src.llm.prompts import (
    SYSTEM_PROMPT_ANTI_WIKIPEDIA,
    PROMPT_STRICT_TAXONOMY_RULE,
    PROMPT_DYNAMIC_TAXONOMY_RULE,
    PROMPT_NIGHT_DAY_SYNTHESIS_SYSTEM,
    PROMPT_NIGHT_CONCEPT_SYNTHESIS_SYSTEM,
)
from src.utils.cognitive_metrics import compute_focus_tunnels
from src.utils.markdown_io import (
    ConceptFrontmatter,
    ParsedConceptNote,
    parse_concept_file,
    parse_concept_string,
    strip_llm_callouts,
    write_concept_file,
)

logger = logging.getLogger("Exocortex.NightConsolidator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

BM25_STOPWORDS: Set[str] = {
    # Mots fonctionnels français
    "pour", "dans", "avec", "cette", "sans", "plus", "tout", "faire", "comme", "mais",
    "nous", "vous", "leur", "elle", "ceux", "celui", "celle", "autres", "aussi", "bien",
    "apres", "avant", "entre", "sous", "vers", "chez", "meme", "alors", "donc", "ainsi",
    "encore", "depuis", "pendant", "tous", "toute", "toutes", "quel", "quelle", "quels",
    "quelles", "mode", "types", "type", "base", "haut", "vaut", "sujet", "travaux",
    "session", "sessions", "journee", "activite", "activites", "synthese", "recherche",
    "note", "notes", "concept", "concepts", "fichier", "document", "page", "fenetre",
    # Mots fonctionnels anglais
    "with", "from", "that", "this", "what", "which", "when", "where", "there", "their",
    "about", "into", "over", "after", "before", "between", "under", "through", "during",
    # Artefacts OS et navigateurs
    "chrome", "firefox", "edge", "google", "youtube", "visual", "studio", "code",
    "apercu", "visuel", "http", "https", "blob", "com", "org", "net", "localhost",
    "html", "json", "yaml", "markdown", "window",
    # Termes techniques génériques ubiquitaires
    "python", "script", "projet", "analyse", "optimisation", "configuration",
    "architecture", "systeme", "test", "tests", "erreur", "serveur", "client", "donnees",
    "creation", "developpement", "implementation", "fonction", "module", "debug",
    "exec", "run", "log", "logs", "data", "file", "project", "analysis"
}


# ==============================================================================
# MODÈLE DE CLASSIFICATION STRUCTURÉE PYDANTIC
# ==============================================================================

class WindowClassification(BaseModel):
    """Classification d'une fenêtre d'activité selon la taxonomie fermée ou émergente."""
    semantic_topic: str = Field(description="Topic existant dans Taxonomie_Tags.md OU nouveau tag Domaine_SousDomaine si aucun ne correspond.")
    is_new_topic: bool = Field(default=False, description="True si un nouveau topic a dû être créé.")
    new_topic_description: Optional[str] = Field(default=None, description="Description courte si nouveau topic.")
    cognitive_mode: str = Field(description="Mode cognitif : production, exploration, chat_ia, gaming, media")
    confidence: float = Field(default=0.9, description="Score de confiance entre 0.0 et 1.0")


class NightConceptSynthesisSchema(BaseModel):
    """Schéma structuré pour la création d'une fiche conceptuelle issue de la télémétrie nocturne."""
    concept_title: str = Field(description="Titre conceptuel précis et canonique du sujet travaillé (ex: 'Optimisation Pipeline RAG LanceDB'). Jamais le nom générique de la macro-catégorie.")
    slug: str = Field(description="Slug kebab-case spécifique au sujet (ex: 'optimisation-pipeline-rag-lancedb').")
    tags: List[str] = Field(default_factory=list, description="3 à 6 tags techniques libres en kebab-case.")
    summary_1_line: str = Field(description="Résumé dense en une phrase des travaux et arbitrages réalisés.")
    synthesized_markdown_body: str = Field(description="Corps analytique structuré en Markdown (### Contexte & Problématique, ### Choix Techniques & Implémentation, ### Arbitrages & Prochaines Étapes). Zéro intro Wikipédia.")
    related_concepts: List[str] = Field(default_factory=list, description="2 à 3 titres de concepts connexes.")


class OpenLoopItem(BaseModel):
    """Intention, bug ou piste de travail non résolue détectée pour injection Kanban."""
    title: str = Field(description="Titre concis de l'intention ou du sujet non résolu")
    component_tag: str = Field(default="general", description="Sous-module ou tag technique")
    summary_pitch: str = Field(default="", description="Description courte du problème ou de la piste")
    priority: int = Field(default=2, description="Priorité estimée (1 = urgent, 2 = normal, 3 = basse)")
    complexity: str = Field(default="M", description="Complexité estimée (XS, S, M, L, XL)")


class ExecutiveBootloaderSchema(BaseModel):
    """Schéma Pydantic du Context Bootloader pour la reprise rapide au réveil."""
    last_active_state: str = Field(description="Où l'utilisateur s'est arrêté (heure, exécutable, fichier/sujet exact)")
    immediate_next_steps: List[str] = Field(description="3 à 5 actions concrètes et atomiques pour reprendre en < 2 minutes")
    detected_open_loops: List[OpenLoopItem] = Field(default_factory=list, description="Intentions, bugs ou pistes en suspens détectés")


PROMPT_BOOTLOADER_SYSTEM = """Tu es l'Ingénieur Système et Stratège Cognitif de l'Exocortex.
Ta mission est d'éliminer totalement la friction d'amorçage mental de l'utilisateur pour sa prochaine session de travail.
En analysant les dernières activités de la journée, les notes conceptuelles créées/enrichies et les tâches Kanban en cours :
1. Identifie avec précision où l'utilisateur s'est arrêté (fichier, outil, ligne ou problème exact).
2. Fournis 3 à 5 actions immédiatement exécutables (< 2 minutes) pour reprendre sans hésitation.
3. Détecte les intentions en suspens (Open Loops) : bugs constatés, idées émises non traitées, pistes de refactoring."""


# ==============================================================================
# CHARGEMENT ET PARSING DE LA TAXONOMIE FERMÉE
# ==============================================================================

def load_authorized_taxonomy() -> Tuple[List[str], Dict[str, str]]:
    """
    Lit et extrait la liste fermée des tags autorisés depuis Vault_Data/00_Meta/Taxonomie_Tags.md.
    Retourne (liste_des_tags, dictionnaire_tag_description).
    """
    tags = list(AUTHORIZED_SEMANTIC_TOPICS.keys())
    descriptions = dict(AUTHORIZED_SEMANTIC_TOPICS)
    logger.info("Taxonomie chargée : %d topics autorisés identifiés.", len(tags))
    return tags, descriptions


def heuristic_fallback_classification(
    executable: str,
    window_title: str,
    ocr_snippet: Optional[str] = None,
    allowed_tags: Optional[List[str]] = None,
) -> Tuple[str, str]:
    """
    Classifieur heuristique déterministe ultra-rapide utilisé si Ollama est hors ligne
    ou pour amorcer les correspondances évidentes sans consommation VRAM.
    """
    text = f"{executable} {window_title} {ocr_snippet or ''}".lower()

    if any(k in text for k in ["code.exe", "visual studio", "terminal", "powershell", "astro", "react", "typescript", "git", "github", "npm"]):
        return "Dev_et_Architecture_Tech", "production"
    if any(k in text for k in ["ollama", "lancedb", "exocortex", "obsidian", "rag", "embedding"]):
        return "IA_et_LLM_Local", "production"
    if any(k in text for k in ["gemini", "chatgpt", "claude.ai", "sillytavern"]):
        return "IA_et_LLM_Local", "chat_ia"
    if any(k in text for k in ["wow.exe", "world of warcraft", "warcraft", "guild wars", "lost ark"]):
        return "MMORPG_et_Esport", "gaming"
    if any(k in text for k in ["minecraft", "skyrim", "cheat engine", "yuzu", "steam"]):
        return "Gaming_et_GameDesign", "gaming"
    if any(k in text for k in ["youtube", "stremio", "plex", "netflix", "crunchyroll", "anime", "webtoon", "asura", "reaper"]):
        return "Musique_MAO_et_Culture_Pop", "media"
    if any(k in text for k in ["suno", "spotify", "fl studio", "maschine", "k-pop", "nmixx"]):
        return "Musique_MAO_et_Culture_Pop", "media"
    if any(k in text for k in ["calorie", "myfitnesspal", "recette", "repas", "volume eating"]):
        return "Nutrition_et_Cuisine", "exploration"
    if any(k in text for k in ["droit", "jurisprudence", "loi", "philo", "spinoza", "camus"]):
        return "Philo_et_Epistemologie", "exploration"

    # Repli par défaut sur A_Trier pour éviter de polluer les tags nobles
    fallback_tag = "A_Trier"
    mode = "production" if any(k in executable.lower() for k in ["code", "devenv", "notepad"]) else "exploration"
    return fallback_tag, mode


# ==============================================================================
# LE CONSOLIDATEUR NOCTURNE
# ==============================================================================

class NightConsolidator:
    """Orchestrateur des 3 passes de consolidation nocturne (Sommeil Paradoxal)."""

    def __init__(self, db_manager: Optional[DBManager] = None) -> None:
        self.db = db_manager or DBManager()
        settings.ensure_directories()
        self.allowed_tags, self.tag_descriptions = load_authorized_taxonomy()
        # Mode CPU (B16) : activé quand la VRAM manque, aucune inférence GPU pendant la nuit
        self.cpu_only: bool = False
        # Dates dont au moins une activité a été classée par la dernière Passe 1 (A11)
        self.last_classified_dates: Set[date] = set()

    @property
    def pending_llm_dates_path(self) -> Path:
        """Dates consolidées en mode CPU, à re-synthétiser par LLM au prochain run (B16)."""
        return settings.SYSTEM_BUFFER_DIR / "pending_llm_dates.json"

    def _load_pending_llm_dates(self) -> Set[date]:
        try:
            raw = json.loads(self.pending_llm_dates_path.read_text(encoding="utf-8"))
            return {datetime.strptime(d, "%Y-%m-%d").date() for d in raw}
        except (FileNotFoundError, ValueError, TypeError):
            return set()

    def _save_pending_llm_dates(self, dates: Set[date]) -> None:
        if dates:
            self.pending_llm_dates_path.write_text(
                json.dumps(sorted(d.isoformat() for d in dates)), encoding="utf-8"
            )
        else:
            self.pending_llm_dates_path.unlink(missing_ok=True)

    # ==========================================================================
    # PASSE 1 : VISION & TAGGING (GEMMA 4:12B)
    # ==========================================================================

    def run_pass_1_vision_and_tagging(self) -> int:
        """
        Passe 1 :
        1. Résumé visuel des captures .webp via modèle rapide et suppression des images du disque.
        2. Classification thématique structurée des activités raw_activity et footprints non traitées.
        3. Purge immédiate de la VRAM (keep_alive=0).
        """
        logger.info("--- DÉBUT PASSE 1 : VISION & TAGGING (gemma4:12b) ---")
        self.last_classified_dates = set()
        llm_client.force_clear_vram()
        free_gb, total_gb = HardwareProbe.get_vram_info()
        logger.info("VRAM disponible avant Passe 1 : %.2f Go / %.2f Go", free_gb, total_gb)

        if free_gb < settings.MIN_FREE_VRAM_GB:
            # Mode CPU (B16) : la nuit n'est plus abandonnée. Classification heuristique, métriques,
            # journaux et compilation Drive sont produits ; vision et synthèses LLM sont reportées.
            logger.warning(
                "VRAM insuffisante (%.2f Go < %.2f Go) : consolidation en mode CPU, synthèses LLM reportées.",
                free_gb, settings.MIN_FREE_VRAM_GB,
            )
            self.cpu_only = True

        # 1. Traitement des captures d'écran différées, par lots jusqu'à épuisement (A4) :
        #    aucune activité n'est marquée traitée tant que sa capture n'a pas été lue.
        seen_screenshot_ids: Set[int] = set()
        while not self.cpu_only:
            screenshot_activities = [
                a for a in self.db.get_unprocessed_activities_with_screenshots(limit=50)
                if a["id"] not in seen_screenshot_ids
            ]
            if not screenshot_activities:
                break
            logger.info("Lot d'activités avec capture d'écran à analyser : %d", len(screenshot_activities))
            for act in tqdm(screenshot_activities, desc="Consolidation Nocturne (Captures)", unit="img"):
                seen_screenshot_ids.add(act["id"])
                self._analyze_activity_screenshot(act)

        # 2. Classification sémantique des activités brutes (processed = 0), par lots de 500
        #    jusqu'à épuisement (A11) : une journée chargée n'est plus figée avec une part Non_Classe.
        is_ollama_ready = not self.cpu_only and llm_client.is_alive()
        total_classified = 0
        while True:
            unprocessed = self.db.get_unprocessed_raw_activities(limit=500, exclude_pending_screenshots=True)
            if not unprocessed:
                break
            logger.info("Lot d'activités brutes à classifier : %d", len(unprocessed))
            classified = self._classify_activity_batch(unprocessed, is_ollama_ready)
            if classified == 0:
                break
            total_classified += classified
            for row in unprocessed:
                ts = row["timestamp_start"]
                self.last_classified_dates.add(
                    (datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") if isinstance(ts, str) else ts).date()
                )

        if total_classified == 0:
            logger.info("Aucune activité brute en attente de classification.")

        # 3. Purge explicite de la VRAM (keep_alive=0)
        llm_client.unload_model(settings.MODEL_FAST_VISION)
        self.purge_orphan_screenshots()
        logger.info("--- FIN PASSE 1 : VRAM PURGÉE ---")
        return total_classified

    def _classify_activity_batch(self, unprocessed: List[Dict[str, Any]], is_ollama_ready: bool) -> int:
        """Classe un lot d'activités par signature unique et les marque processed=1."""
        # Regroupement par signature unique (executable, window_title, ocr_snippet) pour minimiser les appels
        signatures: Dict[Tuple[str, str, Optional[str]], List[int]] = {}
        for row in unprocessed:
            sig = (row["executable"], row["window_title"], row["ocr_snippet"])
            signatures.setdefault(sig, []).append(row["id"])

        logger.info("Signatures uniques identifiées : %d", len(signatures))
        updates: List[Tuple[int, str, str]] = []

        for (exe, title, ocr), row_ids in tqdm(signatures.items(), desc="Consolidation Nocturne (Signatures)", unit="sig"):
            chosen_topic = None
            chosen_mode = None

            if is_ollama_ready:
                taxonomy_list = "\n".join([f"- `{t}` : {self.tag_descriptions.get(t, '')}" for t in self.allowed_tags])
                prompt = (
                    f"Voici une activité capturée sur le bureau Windows :\n"
                    f"- Exécutable : {exe}\n"
                    f"- Titre de la fenêtre : {title}\n"
                    f"- Extrait visuel/OCR : {ocr or 'Aucun'}\n\n"
                    f"Taxonomie actuelle autorisée pour semantic_topic :\n{taxonomy_list}\n\n"
                    f"{PROMPT_STRICT_TAXONOMY_RULE}\n"
                    "Modes cognitifs autorisés : 'production', 'exploration', 'chat_ia', 'gaming', 'media'.\n"
                    "Assigne le semantic_topic exact et le cognitive_mode le plus pertinent."
                )
                try:
                    res = llm_client.generate_structured(
                        prompt=prompt,
                        response_model=WindowClassification,
                        system="Tu es un classificateur de télémétrie strict. Réponds uniquement en JSON valide conforme au schéma.",
                        model=settings.MODEL_FAST_VISION,
                        keep_alive="5m",
                        enable_thinking=False,
                        num_predict=2048,
                    )
                    chosen_topic = normalize_to_macro_topic(res.semantic_topic)
                    chosen_mode = res.cognitive_mode
                except Exception as exc:
                    logger.debug("Repli heuristique pour [%s] '%s' (%s)", exe, title, exc)
                    chosen_topic, chosen_mode = heuristic_fallback_classification(exe, title, ocr, self.allowed_tags)
            else:
                chosen_topic, chosen_mode = heuristic_fallback_classification(exe, title, ocr, self.allowed_tags)

            chosen_topic = normalize_to_macro_topic(chosen_topic or "A_Trier")
            for rid in row_ids:
                updates.append((rid, chosen_topic, chosen_mode))

        # Application de la mise à jour par lots dans SQLite
        if updates:
            self.db.mark_raw_activities_processed(updates)
            logger.info("%d enregistrements d'activité classifiés et marqués processed=1.", len(updates))
        return len(updates)

    def _analyze_activity_screenshot(self, act: Dict[str, Any]) -> None:
        """Résume une capture par le modèle de vision, supprime le fichier et libère screenshot_path."""
        img_path = Path(act["screenshot_path"])
        visual_summary = ""

        if img_path.exists():
            prompt = (
                "Analyse cette capture d'écran de l'utilisateur en une seule phrase dense et factuelle : "
                "identifie l'application, le projet, le code ou le contenu textuel affiché. Zéro bavardage."
            )
            try:
                visual_summary = llm_client.generate_vision(
                    prompt=prompt,
                    image_path=img_path,
                    model=settings.MODEL_FAST_VISION,
                    keep_alive="5m",
                )
            except Exception as exc:
                logger.warning("Échec vision pour %s : %s", img_path.name, exc)
                visual_summary = f"Capture d'écran sur {act.get('executable', 'application')}"

            # Suppression physique du fichier .webp pour respecter le budget disque
            try:
                img_path.unlink()
                logger.debug("Image temporaire supprimée du disque : %s", img_path.name)
            except Exception as exc:
                logger.warning("Impossible de supprimer %s : %s", img_path, exc)

        self.db.update_activity_visual_summary(act["id"], visual_summary)

    def purge_orphan_screenshots(self) -> int:
        """
        Supprime du staging les captures .webp qu'aucune activité ne référence plus (A4).
        Seules les captures plus anciennes que SCREEN_ORPHAN_MAX_AGE_HOURS sont visées, pour ne
        pas toucher la capture de la fenêtre que le démon tient encore en mémoire.
        """
        staging = settings.SCREEN_STAGING_DIR
        if not staging.exists():
            return 0
        referenced = {os.path.normcase(str(Path(p).resolve())) for p in self.db.get_referenced_screenshot_paths()}
        cutoff = datetime.now().timestamp() - settings.SCREEN_ORPHAN_MAX_AGE_HOURS * 3600
        purged = 0
        for img in staging.glob("*.webp"):
            try:
                if os.path.normcase(str(img.resolve())) in referenced or img.stat().st_mtime > cutoff:
                    continue
                img.unlink()
                purged += 1
            except Exception as exc:
                logger.debug("Purge capture orpheline impossible %s : %s", img.name, exc)
        if purged:
            logger.info("%d capture(s) orpheline(s) supprimée(s) du staging.", purged)
        return purged

    # ==========================================================================
    # CALCUL ANALYTIQUE DES TUNNELS D'HYPERFOCUS ET DAILY_METRICS
    # ==========================================================================

    def calculate_daily_metrics_for_date(self, target_date: date) -> DailyMetricRecord:
        """
        Calcule les métriques d'attention pour une journée complète :
        - Tunnels d'hyperfocus (tolérance micro-interruptions < 120s sur un autre exécutable/topic).
        - Ratios de concentration, fragmentation de l'attention et répartition temporelle par sujet.
        """
        activities = self.db.get_activities_for_date(target_date)
        if not activities:
            return DailyMetricRecord(
                date=target_date,
                total_screen_sec=0,
                active_production_sec=0,
                passive_exploration_sec=0,
                max_hyperfocus_sec=0,
                max_hyperfocus_topic=None,
                context_switches_per_hour=0.0,
                read_vs_write_ratio=0.0,
                top_topics_json="{}",
            )

        total_screen_sec = sum(a["duration_sec"] for a in activities)
        active_production_sec = sum(
            a["duration_sec"]
            for a in activities
            if a.get("cognitive_mode") == "production" and a.get("active_input")
        )
        passive_exploration_sec = sum(
            a["duration_sec"]
            for a in activities
            if a.get("cognitive_mode") in ("exploration", "media") or not a.get("active_input")
        )

        # Répartition par sujet
        topic_durations: Dict[str, int] = {}
        for a in activities:
            top = a.get("semantic_topic") or "Non_Classe"
            topic_durations[top] = topic_durations.get(top, 0) + a["duration_sec"]

        # Tri décroissant des sujets
        sorted_topics = dict(sorted(topic_durations.items(), key=lambda x: x[1], reverse=True))

        # --- Tunnels d'Hyperfocus : définition unique partagée avec l'API et Streamlit (B7) ---
        tunnels = compute_focus_tunnels(activities)
        best_tunnel = max(tunnels, key=lambda t: t.duration_sec, default=None)
        max_hyperfocus_sec = best_tunnel.duration_sec if best_tunnel else 0
        max_hyperfocus_topic: Optional[str] = best_tunnel.topic if best_tunnel else None
        context_switch_events = max(0, len(tunnels) - 1)

        # Calcul du taux de switch horaire et du ratio lecture/écriture
        active_hours = max(0.1, total_screen_sec / 3600.0)
        context_switches_per_hour = round(context_switch_events / active_hours, 2)
        read_vs_write_ratio = round(passive_exploration_sec / max(1, active_production_sec), 2)

        metric = DailyMetricRecord(
            date=target_date,
            total_screen_sec=total_screen_sec,
            active_production_sec=active_production_sec,
            passive_exploration_sec=passive_exploration_sec,
            max_hyperfocus_sec=max_hyperfocus_sec,
            max_hyperfocus_topic=max_hyperfocus_topic,
            context_switches_per_hour=context_switches_per_hour,
            read_vs_write_ratio=read_vs_write_ratio,
            top_topics_json=json.dumps(sorted_topics, ensure_ascii=False),
        )
        self.db.upsert_daily_metrics(metric)
        logger.info(
            "Bilan métrique du %s : Écran=%.1f h | Prod=%.1f h | Hyperfocus max=%d min (%s) | Switches/h=%.1f",
            target_date.isoformat(),
            total_screen_sec / 3600.0,
            active_production_sec / 3600.0,
            max_hyperfocus_sec // 60,
            max_hyperfocus_topic,
            context_switches_per_hour,
        )
        return metric

    def _find_matching_existing_concept_cpu(self, topic_name: str, topic_items: List[str]) -> Optional[Path]:
        """
        Recherche purement CPU (0 Mo VRAM, BM25 / IDF) d'une note conceptuelle existante appartenant
        à topic_name et présentant un fort recouvrement lexical hautement distinctif avec les fenêtres
        et activités actives du jour.
        """
        if not topic_items or not settings.CONCEPTS_DIR.exists():
            return None

        # 1. Extraction et tokenisation des termes de la journée
        raw_text = " ".join(topic_items).lower()
        all_query_tokens = [t.lower() for t in re.findall(r"\b[a-zA-Z0-9À-ÿ_-]{3,}\b", raw_text)]
        query_kws = [t for t in all_query_tokens if t not in BM25_STOPWORDS]
        if not query_kws:
            return None

        query_kw_set = set(query_kws)
        if len(query_kw_set) < 2:
            return None

        norm_target_topic = normalize_to_macro_topic(topic_name)
        generic_slug = re.sub(r"[\s_]+", "-", topic_name.lower()).strip("-")

        # 2. Collecte des notes du coffre et calcul de l'IDF
        all_concept_files = [
            f for f in settings.CONCEPTS_DIR.glob("*.md")
            if not f.name.startswith("all-") and not f.name.startswith("all_")
        ]
        if not all_concept_files:
            return None

        N = len(all_concept_files)
        doc_freq: Dict[str, int] = {kw: 0 for kw in query_kw_set}
        candidate_notes: List[Tuple[Path, ParsedConceptNote, Dict[str, float], float, Set[str]]] = []

        for fpath in all_concept_files:
            try:
                file_text = fpath.read_text(encoding="utf-8", errors="replace")
                file_lower = file_text.lower()

                # Mise à jour document frequency pour calcul de l'IDF
                for kw in query_kw_set:
                    if kw in file_lower:
                        doc_freq[kw] += 1

                # Vérification éligibilité du candidat (même topic sémantique)
                if fpath.stem == generic_slug:
                    continue

                note = parse_concept_string(file_text, file_path=fpath)
                if note.frontmatter.semantic_topic != norm_target_topic:
                    continue

                # Extraction des tokens pondérés du candidat
                title_slug_text = f"{note.frontmatter.title} {fpath.stem.replace('-', ' ')}".lower()
                title_slug_tokens = [t for t in re.findall(r"\b[a-zA-Z0-9À-ÿ_-]{3,}\b", title_slug_text) if t not in BM25_STOPWORDS]

                tags_text = " ".join(note.frontmatter.tags).lower()
                tag_tokens = [t for t in re.findall(r"\b[a-zA-Z0-9À-ÿ_-]{3,}\b", tags_text) if t not in BM25_STOPWORDS]

                summary_body_text = f"{note.frontmatter.summary_1_line} {note.body[:1500]}".lower()
                summary_tokens = [t for t in re.findall(r"\b[a-zA-Z0-9À-ÿ_-]{3,}\b", summary_body_text) if t not in BM25_STOPWORDS]

                # Règle stricte : au moins 2 mots-clés spécifiques dans (title + slug + tags)
                key_tokens = set(title_slug_tokens) | set(tag_tokens)
                matching_kws = query_kw_set.intersection(key_tokens)
                if len(matching_kws) < 2:
                    continue

                # Calcul des fréquences pondérées : title x3, tags x2, summary x1
                tf_weighted: Dict[str, float] = {}
                for t in title_slug_tokens:
                    tf_weighted[t] = tf_weighted.get(t, 0.0) + 3.0
                for t in tag_tokens:
                    tf_weighted[t] = tf_weighted.get(t, 0.0) + 2.0
                for t in summary_tokens:
                    tf_weighted[t] = tf_weighted.get(t, 0.0) + 1.0

                doc_len = sum(tf_weighted.values())
                candidate_notes.append((fpath, note, tf_weighted, doc_len, matching_kws))
            except Exception as exc:
                logger.debug("Erreur analyse candidat BM25 %s : %s", fpath.name, exc)
                continue

        if not candidate_notes:
            return None

        # 3. Calcul BM25 Robertson-Spärck Jones
        avgdl = sum(c[3] for c in candidate_notes) / max(1, len(candidate_notes))
        k1 = 1.5
        b = 0.75

        best_match: Optional[Path] = None
        best_score = 0.0

        for fpath, note, tf_dict, doc_len, matching_kws in candidate_notes:
            score = 0.0
            for kw in query_kw_set:
                tf = tf_dict.get(kw, 0.0)
                if tf <= 0.0:
                    continue
                nt = doc_freq.get(kw, 0)
                idf = math.log(1.0 + (N - nt + 0.5) / (nt + 0.5))
                denom = tf + k1 * (1.0 - b + b * (doc_len / max(1.0, avgdl)))
                term_score = idf * ((tf * (k1 + 1.0)) / max(1e-6, denom))
                score += term_score

            if score > best_score:
                best_score = score
                best_match = fpath

        # Seuil strict de pertinence BM25
        if best_match and best_score >= 2.0:
            logger.info(
                "Correspondance conceptuelle BM25 retenue pour topic '%s' : %s (score BM25: %.2f)",
                topic_name,
                best_match.name,
                best_score,
            )
            return best_match

        return None

    # ==========================================================================
    # PASSE 2 : SYNTHÈSE ÉPISODIQUE & FICHES CONCEPTS (GEMMA 4:26B OU 12B)
    # ==========================================================================

    def run_pass_2_synthesis(self, target_date: date, metric: DailyMetricRecord, run_bootloader: bool = True) -> None:
        """
        Passe 2 :
        1. Rédige le journal épisodique 01_Episodique/YYYY-MM-DD.md avec synthèse LLM des tunnels réels.
        2. Pour tout sujet ayant cumulé >= 45 minutes dans la journée, crée ou enrichit la fiche dans 02_Concepts/.
        3. Génère le Bootloader si run_bootloader=True.
        4. Purge la VRAM en fin de passe.
        """
        if metric.total_screen_sec == 0:
            logger.info("Temps d'écran total nul pour le %s. Aucune note épisodique ou conceptuelle générée.", target_date.isoformat())
            return

        logger.info("--- DÉBUT PASSE 2 : SYNTHÈSE ÉPISODIQUE & CONCEPTS ---")
        effective_model: Optional[str] = None
        if not self.cpu_only and llm_client.is_alive():
            llm_client.force_clear_vram()
            free_gb, _ = HardwareProbe.get_vram_info()

            # Choix du modèle selon la VRAM libre
            target_model = settings.MODEL_HEAVY_SYNTHESIS if free_gb >= settings.FULL_DUAL_MODEL_VRAM_GB else settings.MODEL_FAST_VISION
            try:
                effective_model = llm_client.check_and_select_model(target_model)
                logger.info("Modèle sélectionné pour la synthèse : %s (VRAM libre: %.2f Go)", effective_model, free_gb)
            except VRAMInsufficientError as exc:
                logger.warning("VRAM insuffisante pour la Passe 2 (%s) : bascule en mode CPU.", exc)
                self.cpu_only = True
        llm_ready = effective_model is not None

        # 1. Extraction et structuration des activités réelles du jour
        date_str = target_date.strftime("%Y-%m-%d")
        activities = self.db.get_activities_for_date(target_date)

        topic_activities: Dict[str, List[str]] = {}
        for act in activities:
            top = act.get("semantic_topic") or "Non_Classe"
            exe = act.get("executable") or ""
            title = act.get("window_title") or ""
            ocr = act.get("ocr_snippet") or ""
            line = f"- [{exe}] {title}"
            if ocr:
                line += f" (Aperçu visuel : {ocr[:120]})"
            if line not in topic_activities.setdefault(top, []):
                topic_activities[top].append(line)

        # Préparation du tableau des topics pour le journal
        top_topics_dict = json.loads(metric.top_topics_json)
        topics_table_lines = [
            "| Sujet Sémantique | Durée Cumulée | Part du Temps |",
            "| :--- | :--- | :--- |",
        ]
        for top_name, top_secs in top_topics_dict.items():
            hours = top_secs // 3600
            mins = (top_secs % 3600) // 60
            pct = (top_secs / max(1, metric.total_screen_sec)) * 100.0
            topics_table_lines.append(f"| **`{top_name}`** | {hours}h{mins:02d} | {pct:.1f} % |")

        topics_table = "\n".join(topics_table_lines)
        hyperfocus_fmt = f"{metric.max_hyperfocus_sec // 60} min" if metric.max_hyperfocus_sec < 3600 else f"{metric.max_hyperfocus_sec // 3600}h{(metric.max_hyperfocus_sec % 3600) // 60:02d}"

        # 2. Synthèse LLM de la Section 3 du Journal Épisodique
        activities_summary_lines: List[str] = []
        for top_name, items in topic_activities.items():
            activities_summary_lines.append(f"### Sujet : {top_name}")
            for item in items[:6]:
                activities_summary_lines.append(item)
        activities_text = "\n".join(activities_summary_lines)

        synthesis_prompt = (
            f"Voici les données d'activité réelles de la journée du {date_str} :\n"
            f"- Temps d'écran total : {metric.total_screen_sec / 3600.0:.2f} h\n"
            f"- Production active : {metric.active_production_sec / 3600.0:.2f} h\n"
            f"- Exploration / passif : {metric.passive_exploration_sec / 3600.0:.2f} h\n"
            f"- Tunnel d'hyperfocus max : {hyperfocus_fmt} sur `{metric.max_hyperfocus_topic or 'Non défini'}`\n"
            f"- Changements de contexte par heure : {metric.context_switches_per_hour}\n\n"
            f"Activités et fenêtres réelles consultées par sujet :\n{activities_text}\n\n"
            "Rédige une analyse synthétique dense, factuelle et sans complaisance (2 à 3 paragraphes) des tunnels de concentration "
            "de la journée, des transitions de focus, des outils et des réalisations concrètes observées. "
            "Zéro verbiage encyclopédique. Ne décris que la dynamique de travail réelle de l'utilisateur."
        )

        section_3_content = ""
        if llm_ready:
            try:
                section_3_content = llm_client.generate_text(
                    prompt=synthesis_prompt,
                    system=PROMPT_NIGHT_DAY_SYNTHESIS_SYSTEM,
                    model=effective_model,
                    keep_alive="5m",
                )
            except Exception as exc:
                logger.warning("Erreur lors de la synthèse LLM du journal épisodique : %s", exc)

        if not section_3_content.strip():
            section_3_content = (
                f"Journée marquée par une concentration principale sur `{metric.max_hyperfocus_topic or 'les projets en cours'}` "
                f"avec un hyperfocus continu de {hyperfocus_fmt} et {metric.context_switches_per_hour} changements de contexte par heure."
            )

        episodic_file = settings.EPISODIC_DIR / f"{date_str}.md"
        episodic_content = f"""---
date: "{date_str}"
total_screen_hours: {metric.total_screen_sec / 3600.0:.2f}
active_production_hours: {metric.active_production_sec / 3600.0:.2f}
passive_exploration_hours: {metric.passive_exploration_sec / 3600.0:.2f}
max_hyperfocus_min: {metric.max_hyperfocus_sec // 60}
max_hyperfocus_topic: "{metric.max_hyperfocus_topic or 'None'}"
context_switches_per_hour: {metric.context_switches_per_hour}
read_vs_write_ratio: {metric.read_vs_write_ratio}
---

# Journal Épisodique & Télémétrie Cognitive : {date_str}

## 1. Métriques Clés d'Attention & Focus
- **Temps d'écran actif total :** {metric.total_screen_sec / 3600.0:.2f} heures
- **Production active :** {metric.active_production_sec / 3600.0:.2f} h vs **Exploration passive :** {metric.passive_exploration_sec / 3600.0:.2f} h
- **Tunnel d'hyperfocus maximal :** {hyperfocus_fmt} sur `{metric.max_hyperfocus_topic or 'Non défini'}`
- **Fragmentation de l'attention :** {metric.context_switches_per_hour} changements de contexte / heure
- **Ratio Exploration / Production :** {metric.read_vs_write_ratio}

## 2. Répartition du Temps par Sujet
{topics_table}

## 3. Synthèse des Tunnels de Concentration
{section_3_content.strip()}
"""
        with open(episodic_file, "w", encoding="utf-8") as f:
            f.write(episodic_content)
        logger.info("Journal épisodique généré : %s", episodic_file.name)

        # 3. Distillation ou enrichissement des fiches conceptuelles atomiques (seuil >= 45 min = 2700s)
        for topic_name, duration_secs in top_topics_dict.items():
            if duration_secs < 2700:  # Seuil strict de 45 minutes
                continue
            # Jamais de fiche pour une part non classée (A11)
            if topic_name in ("Non_Classe", "A_Trier") or normalize_to_macro_topic(topic_name) == "A_Trier":
                continue
            # Mode CPU (B16) : fiches reportées à la prochaine nuit avec GPU (date marquée à enrichir)
            if self.cpu_only:
                continue

            duration_fmt = f"{duration_secs // 3600}h{(duration_secs % 3600) // 60:02d}"
            topic_items = topic_activities.get(topic_name, [])
            topic_context_str = "\n".join(topic_items[:12])

            # Recherche préalable CPU d'une fiche conceptuelle atomique existante (Exclusion mutuelle VRAM)
            matched_file = self._find_matching_existing_concept_cpu(topic_name, topic_items)

            if matched_file and matched_file.exists():
                concept_file = matched_file
                note = parse_concept_file(concept_file)

                enrich_text = ""
                if llm_ready and topic_context_str:
                    enrich_prompt = (
                        f"L'utilisateur a passé {duration_fmt} de travail supplémentaire sur le sujet '{topic_name}' le {date_str}.\n"
                        f"Fenêtres et activités récentes :\n{topic_context_str}\n\n"
                        f"Rédige un court paragraphe d'enrichissement factuel (avec un sous-titre `### Session du {date_str}`) "
                        "détaillant les nouveaux arbitrages, implémentations ou tests observés. Zéro intro générale encyclopédique."
                    )
                    try:
                        enrich_text = llm_client.generate_text(
                            prompt=enrich_prompt,
                            system=PROMPT_NIGHT_CONCEPT_SYNTHESIS_SYSTEM,
                            model=effective_model,
                            keep_alive="5m",
                        )
                    except Exception as exc:
                        logger.warning("Erreur enrichissement concept %s : %s", concept_file.name, exc)

                if not enrich_text.strip():
                    enrich_text = (
                        f"### Session du {date_str}\n\n"
                        f"Poursuite des développements ({duration_fmt}) observée le {date_str}.\n"
                        + "\n".join([f"- {it}" for it in topic_items[:6]])
                    )

                note.append_or_replace_daily_session(
                    date_str=date_str,
                    duration_min=duration_secs // 60,
                    duration_fmt=duration_fmt,
                    enrichment_markdown=enrich_text.strip(),
                )
                write_concept_file(note, concept_file)
                logger.info("Fiche conceptuelle enrichie (idempotente) : %s (+%s)", concept_file.name, duration_fmt)
            else:
                # Génération d'une nouvelle fiche conceptuelle ATOMIQUE (et non du nom de la macro-catégorie)
                concept_id = datetime.now().strftime("%Y%m%d%H%M")
                generic_slug = re.sub(r"[\s_]+", "-", topic_name.lower()).strip("-")

                distilled: Optional[NightConceptSynthesisSchema] = None
                if llm_ready and topic_context_str:
                    concept_prompt = (
                        f"L'utilisateur a passé {duration_fmt} de concentration continue sur des activités rattachées au macro-domaine '{topic_name}' le {date_str}.\n"
                        f"Traces, fenêtres et outils observés :\n{topic_context_str}\n\n"
                        "Génère une fiche conceptuelle ATOMIQUE et PRÉCISE modélisant le cœur technique ou conceptuel de ces travaux. "
                        "Le titre et le slug doivent refléter l'objet spécifique du travail (ex: 'Optimisation Pipeline RAG LanceDB' -> 'optimisation-pipeline-rag-lancedb'), "
                        "et JAMAIS le nom générique de la macro-catégorie.\n"
                        "Rédige un corps dense en Markdown (### Contexte & Problématique, ### Choix Techniques & Implémentation, ### Arbitrages & Prochaines Étapes). "
                        "Zéro paraphrase encyclopédique Wikipédia."
                    )
                    try:
                        distilled = llm_client.generate_structured(
                            prompt=concept_prompt,
                            response_model=NightConceptSynthesisSchema,
                            system=PROMPT_NIGHT_CONCEPT_SYNTHESIS_SYSTEM,
                            model=effective_model,
                            keep_alive="5m",
                        )
                    except Exception as exc:
                        logger.warning("Erreur génération structurée concept nocturne pour %s : %s", topic_name, exc)

                if distilled and distilled.concept_title and distilled.synthesized_markdown_body:
                    title = distilled.concept_title.strip()
                    raw_slug = re.sub(r"[^a-z0-9_-]+", "-", (distilled.slug or "").lower()).strip("-")
                    slug = raw_slug if raw_slug and raw_slug != generic_slug else re.sub(r"[^a-z0-9_-]+", "-", title.lower()).strip("-")
                    if not slug or slug == generic_slug:
                        slug = f"{generic_slug}-{date_str.replace('-', '')}"
                    tags = [re.sub(r"[^a-z0-9_-]+", "-", t.lower()).strip("-") for t in (distilled.tags or []) if t]
                    if generic_slug not in tags:
                        tags.insert(0, generic_slug)
                    if "screen_telemetry" not in tags:
                        tags.append("screen_telemetry")
                    summary_1_line = distilled.summary_1_line.strip()
                    synthesized_body = strip_llm_callouts(distilled.synthesized_markdown_body)
                    related_links = [f"[[{rc.strip()}]]" for rc in (distilled.related_concepts or []) if rc.strip()]
                    related_links_str = ", ".join(related_links) if related_links else f"#{topic_name}"
                else:
                    title = f"{topic_name.replace('_', ' ')} - Travaux du {date_str}"
                    slug = f"{generic_slug}-{date_str.replace('-', '')}"
                    tags = [generic_slug, "screen_telemetry"]
                    summary_1_line = f"Synthèse et développements techniques sur {topic_name.replace('_', ' ')} observés le {date_str}."
                    synthesized_body = (
                        f"### Contexte & Investigations\n"
                        f"Session d'hyperfocus de {duration_fmt} consacrée à {topic_name.replace('_', ' ')}.\n\n"
                        f"### Activités & Traces Notables\n"
                        + "\n".join([f"- {it}" for it in topic_items[:8]])
                    )
                    related_tags = [t for t in self.allowed_tags if t != topic_name][:2]
                    # Catégories : ce ne sont pas des fichiers, donc des tags et non des wikilinks (B18)
                    related_links_str = ", ".join([f"#{t}" for t in related_tags]) if related_tags else f"#{topic_name}"

                # Sécurisation anti-collision sur le slug
                concept_file = settings.CONCEPTS_DIR / f"{slug}.md"
                if concept_file.exists():
                    slug = f"{slug}-{date_str.replace('-', '')}"
                    concept_file = settings.CONCEPTS_DIR / f"{slug}.md"
                if concept_file.exists():
                    slug = f"{slug}-{datetime.now().strftime('%H%M%S')}"
                    concept_file = settings.CONCEPTS_DIR / f"{slug}.md"

                fm = ConceptFrontmatter(
                    id=concept_id,
                    title=title,
                    type="concept",
                    origin=["screen_telemetry"],
                    semantic_topic=topic_name,
                    tags=tags,
                    created_at=date_str,
                    updated_at=date_str,
                    total_time_invested_min=duration_secs // 60,
                    summary_1_line=summary_1_line,
                )
                telemetry_lines = [
                    "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)",
                    f"> - **Temps cumulé sur ce sujet :** {duration_fmt}",
                    "> - **Sources épisodiques :**",
                    f">   - Activité écran du `{date_str}` ({duration_fmt})",
                    f"> - **Connexions sémantiques :** {related_links_str}",
                ]
                new_note = ParsedConceptNote(
                    frontmatter=fm,
                    title_h1=title,
                    body=synthesized_body,
                    telemetry_lines=telemetry_lines,
                    file_path=concept_file,
                )
                write_concept_file(new_note, concept_file)
                logger.info("Nouvelle fiche conceptuelle atomique créée via synthèse LLM : %s", concept_file.name)

        # Génération du Context Bootloader et extraction des Open Loops (Module 8 - v0.3.0)
        if run_bootloader:
            try:
                self.generate_executive_bootloader(target_date, metric, effective_model)
            except Exception as exc:
                logger.warning("Erreur lors de la génération du Context Bootloader : %s", exc)

        # Purge de la VRAM après la synthèse
        if effective_model:
            llm_client.unload_model(effective_model)
        logger.info("--- FIN PASSE 2 : VRAM PURGÉE ---")

    def generate_executive_bootloader(
        self,
        target_date: date,
        metric: DailyMetricRecord,
        effective_model: Optional[str],
    ) -> Path:
        """
        Génère Vault_Data/00_Meta/00_BOOTLOADER_DEMAIN.md pour supprimer l'inertie d'amorçage matinale
        et injecte de manière idempotente les Open Loops détectés dans le Kanban (statut 'radar').
        """
        date_str = target_date.strftime("%Y-%m-%d")
        logger.info("--- Génération du Context Bootloader & Extraction des Open Loops (%s) ---", date_str)

        activities = self.db.get_activities_for_date(target_date)
        recent_activities = activities[-15:] if activities else []

        # Fiches conceptuelles créées ou mises à jour aujourd'hui
        active_concepts: List[str] = []
        for cf in settings.CONCEPTS_DIR.glob("*.md"):
            if cf.name.startswith("all-") or cf.name.startswith("."):
                continue
            try:
                note = parse_concept_file(cf)
                if note.frontmatter.updated_at == date_str or note.frontmatter.created_at == date_str:
                    c_title = note.frontmatter.title or cf.stem
                    active_concepts.append(f"[[{c_title}]]")
            except Exception:
                pass

        # Tâches Kanban en cours
        from src.consolidators.kanban_engine import KanbanEngine
        kanban = KanbanEngine(db_manager=self.db)
        kanban_tasks = kanban.db.get_kanban_tasks(project_id="exocortex", statuses=["in_progress", "ready_for_agent"])
        in_prog_tasks = [t for t in kanban_tasks if t.get("status") == "in_progress"]
        ready_tasks = [t for t in kanban_tasks if t.get("status") == "ready_for_agent"]

        recent_act_text_lines = []
        for act in recent_activities:
            exe = act.get("executable") or ""
            title = act.get("window_title") or ""
            dur = act.get("duration_sec", 0)
            recent_act_text_lines.append(f"- [{exe}] {title} ({dur}s)")
        recent_act_str = "\n".join(recent_act_text_lines) if recent_act_text_lines else "(Aucune activité détaillée enregistrée)"

        bootloader_data: Optional[ExecutiveBootloaderSchema] = None
        if effective_model and llm_client.is_alive() and (recent_activities or in_prog_tasks or active_concepts):
            bootloader_prompt = (
                f"Données de fin de journée pour le {date_str} :\n"
                f"- Temps d'écran total : {metric.total_screen_sec / 3600.0:.2f} h (Prod: {metric.active_production_sec / 3600.0:.2f} h)\n"
                f"- Hyperfocus max : {metric.max_hyperfocus_topic or 'N/A'}\n"
                f"- Dernières activités enregistrées (parcours terminal) :\n{recent_act_str}\n\n"
                f"- Fiches actives du jour : {', '.join(active_concepts) if active_concepts else 'Aucune'}\n"
                f"- Tâches Kanban en cours : {', '.join([t['title'] for t in in_prog_tasks]) if in_prog_tasks else 'Aucune'}\n\n"
                "Remplis le schéma structuré ExecutiveBootloaderSchema :\n"
                "1. Où l'utilisateur s'est arrêté exactement.\n"
                "2. 3 à 5 prochaines étapes concrètes et atomiques pour démarrer demain en < 2 min.\n"
                "3. Détecte les Open Loops (questions non résolues, bugs vus dans les logs/titres, refactorings indispensables)."
            )
            try:
                bootloader_data = llm_client.generate_structured(
                    prompt=bootloader_prompt,
                    response_model=ExecutiveBootloaderSchema,
                    system=PROMPT_BOOTLOADER_SYSTEM,
                    model=effective_model,
                    keep_alive="5m",
                )
            except Exception as exc:
                logger.warning("Erreur lors de la génération LLM du Bootloader : %s", exc)

        # Repli déterministe si Ollama indisponible ou échec
        if not bootloader_data or not bootloader_data.last_active_state:
            last_act = recent_activities[-1] if recent_activities else {}
            last_exe = last_act.get("executable", "Environnement de dev")
            last_title = last_act.get("window_title", "Session de travail")
            fallback_state = f"Arrêt de session sur [{last_exe}] '{last_title}'."

            fallback_steps = []
            if in_prog_tasks:
                for t in in_prog_tasks[:3]:
                    fallback_steps.append(f"Reprendre la tâche en cours [{t['task_id']}] : {t['title']}")
            if len(fallback_steps) < 3 and ready_tasks:
                for t in ready_tasks[: 3 - len(fallback_steps)]:
                    fallback_steps.append(f"Amorcer la tâche prête [{t['task_id']}] : {t['title']}")
            while len(fallback_steps) < 3:
                fallback_steps.append("Vérifier les tests de non-régression et consulter le tableau de bord.")

            bootloader_data = ExecutiveBootloaderSchema(
                last_active_state=fallback_state,
                immediate_next_steps=fallback_steps[:5],
                detected_open_loops=[],
            )

        # Écriture du fichier 00_BOOTLOADER_DEMAIN.md
        bootloader_file = settings.BOOTLOADER_PATH
        bootloader_file.parent.mkdir(parents=True, exist_ok=True)

        steps_checklist = "\n".join([f"- [ ] {step.strip()}" for step in bootloader_data.immediate_next_steps])
        concepts_block = "\n".join([f"- {c}" for c in active_concepts]) if active_concepts else "- Aucune fiche conceptuelle modifiée aujourd'hui."

        kanban_lines = []
        for t in in_prog_tasks:
            kanban_lines.append(f"- ⚙️ **[{t['task_id']}]** {t['title']} (P{t.get('priority', 2)} | {t.get('complexity', 'M')})")
        for t in ready_tasks[:3]:
            kanban_lines.append(f"- 🎯 **[{t['task_id']}]** {t['title']} (P{t.get('priority', 2)} | {t.get('complexity', 'M')})")
        kanban_block = "\n".join(kanban_lines) if kanban_lines else "- Aucune tâche en cours ou prête dans le Kanban."

        content = f"""# 🚀 Context Bootloader — Reprise Rapide & État Mental

> **Date de consolidation :** `{date_str}`
> **Bilan d'Attention :** {metric.total_screen_sec / 3600.0:.2f} h écran ({metric.active_production_sec / 3600.0:.2f} h prod) | Hyperfocus : `{metric.max_hyperfocus_topic or 'N/A'}`

## 1. Dernier Point d'Arrêt
{bootloader_data.last_active_state.strip()}

## 2. Checklist de Redémarrage Immédiat (< 2 min)
{steps_checklist}

## 3. Fiches Conceptuelles Actives
{concepts_block}

## 4. Tâches Kanban Prioritaires
{kanban_block}
"""
        bootloader_file.write_text(content, encoding="utf-8")
        logger.info("Context Bootloader généré avec succès : %s", bootloader_file.name)

        # Injection dédupliquée des Open Loops dans le Kanban (statut 'radar')
        if bootloader_data.detected_open_loops:
            existing_tasks = kanban.db.get_kanban_tasks(project_id="exocortex")
            existing_titles = {t["title"].strip().lower() for t in existing_tasks if t.get("title")}

            created_loops = 0
            for loop in bootloader_data.detected_open_loops:
                loop_title_norm = loop.title.strip().lower()
                if loop_title_norm in existing_titles:
                    continue
                kanban.create_task(
                    project_id="exocortex",
                    title=loop.title.strip(),
                    component_tag=loop.component_tag.strip() or "open-loop",
                    summary_pitch=loop.summary_pitch.strip() or "Intention en suspens détectée lors de la consolidation nocturne.",
                    priority=loop.priority,
                    complexity=loop.complexity,
                    initial_status="radar",
                )
                existing_titles.add(loop_title_norm)
                created_loops += 1

            if created_loops > 0:
                logger.info("%d Open Loop(s) injecté(s) dans le Kanban en statut 'radar'.", created_loops)

        return bootloader_file

    # ==========================================================================
    # PASSE 3 : INDEXATION VECTORIELLE LANCEDB (BGE-M3)
    # ==========================================================================

    def run_pass_3_vector_indexing(self) -> int:
        """
        Passe 3 :
        Synchronise l'ensemble des notes de 02_Concepts/ dans LanceDB via vector_store,
        puis décharge bge-m3 de la VRAM.
        """
        logger.info("--- DÉBUT PASSE 3 : INDEXATION VECTORIELLE LANCEDB (bge-m3) ---")
        indexed_count = vector_store.sync_all_concepts()
        llm_client.unload_model(settings.MODEL_EMBEDDING)
        logger.info("--- FIN PASSE 3 : LANCEDB À JOUR (%d NOTES) & VRAM PURGÉE ---", indexed_count)
        return indexed_count

    # ==========================================================================
    # ORCHESTRATEUR PRINCIPAL
    # ==========================================================================

    def consolidate(self, target_date: Optional[date] = None) -> Dict[str, Any]:
        """Exécute les 3 passes complètes de consolidation nocturne."""
        logger.info("============================================================")
        logger.info("=== DÉCLENCHEMENT DU SOMMEIL PARADOXAL (CONSOLIDATION) ===")
        logger.info("============================================================")

        # 0. Provisioning automatique des modèles GGUF locaux dans Ollama
        if llm_client.is_alive():
            llm_client.ensure_local_gguf_models()

        # Passe 0 : Ingestion des mémos vocaux en attente dans voice_inbox/ (v0.4.1)
        try:
            from src.ingestors.voice_ingestor import VoiceIngestor
            v_ingestor = VoiceIngestor(db_manager=self.db)
            v_res = v_ingestor.run()
            if v_res.get("processed_count", 0) > 0:
                logger.info("Passe 0 : %d mémo(s) vocal/vocaux ingéré(s).", v_res["processed_count"])
        except Exception as v_exc:
            logger.warning("Avertissement Passe 0 Ingestion Vocale : %s", v_exc)

        # Passe 1 : Vision & Tagging
        classified_count = self.run_pass_1_vision_and_tagging()

        # Identification des dates à traiter
        pending_llm_dates = self._load_pending_llm_dates()
        if target_date:
            dates_to_process = [target_date]
        else:
            all_dates = sorted(self.db.get_distinct_activity_dates(processed_only=True))
            if all_dates:
                max_date = max(all_dates)
                # Dates sans journal, date la plus récente, toute date dont une activité vient d'être
                # classée (A11) et dates consolidées en mode CPU à enrichir par LLM (B16)
                known = set(all_dates)
                dates_to_process = sorted(
                    {
                        d for d in all_dates
                        if not (settings.EPISODIC_DIR / f"{d.isoformat()}.md").exists() or d == max_date
                    }
                    | (set(getattr(self, "last_classified_dates", set())) & known)
                    | (pending_llm_dates & known if not self.cpu_only and llm_client.is_alive() else set())
                )
            else:
                dates_to_process = []

        if not dates_to_process:
            logger.info("Aucune date avec activité à consolider. Arrêt du Sommeil Paradoxal.")
            return {
                "classified_activities": classified_count,
                "processed_dates": [],
                "indexed_concepts_count": 0,
                "drive_files": {},
                "db_stats": self.db.get_database_stats(),
            }

        logger.info("Journées à agréger et synthétiser : %s", [d.isoformat() for d in dates_to_process])

        # Pour chaque date : agrégation SQLite & Passe 2 (Bootloader sur la date la plus récente uniquement)
        max_target_date = max(dates_to_process) if dates_to_process else None
        for d in tqdm(dates_to_process, desc="Consolidation Nocturne (Journaux)", unit="jour"):
            metric = self.calculate_daily_metrics_for_date(d)
            should_run_bootloader = (d == max_target_date)
            self.run_pass_2_synthesis(d, metric, run_bootloader=should_run_bootloader)

        # Suivi des dates à enrichir (B16) : ajoutées en mode CPU, retirées une fois synthétisées par LLM
        if self.cpu_only or not llm_client.is_alive():
            self._save_pending_llm_dates(pending_llm_dates | set(dates_to_process))
        else:
            self._save_pending_llm_dates(pending_llm_dates - set(dates_to_process))

        # Passe 3 : Vectorisation LanceDB (bge-m3, reportée en mode CPU : la synchronisation est complète au run suivant)
        vector_count = 0 if self.cpu_only else self.run_pass_3_vector_indexing()

        # Module 4 : Compilation des méga-documents Google Drive
        logger.info("--- DÉBUT COMPILATION MÉGA-FICHIERS GOOGLE DRIVE ---")
        drive_compiler = DriveCompiler(self.db)
        drive_files = drive_compiler.compile_all()
        logger.info("--- FIN COMPILATION GOOGLE DRIVE (%d FICHIERS) ---", len(drive_files))

        db_stats = self.db.get_database_stats()
        logger.info("=== SOMMEIL PARADOXAL TERMINÉ AVEC SUCCÈS ===")
        logger.info("Statistiques SQLite : %s", db_stats)

        return {
            "classified_activities": classified_count,
            "processed_dates": [d.isoformat() for d in dates_to_process],
            "indexed_concepts_count": vector_count,
            "drive_files": {k: str(v) for k, v in drive_files.items()},
            "db_stats": db_stats,
            "cpu_only": self.cpu_only,
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exocortex Night Consolidator")
    parser.add_argument("--date", type=str, default=None, help="Date spécifique à consolider (YYYY-MM-DD).")
    args = parser.parse_args()

    target_dt = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else None
    consolidator = NightConsolidator()
    res = consolidator.consolidate(target_date=target_dt)
    print("\n" + "=" * 60)
    print("RÉSULTAT DE LA CONSOLIDATION NOCTURNE :")
    for k, v in res.items():
        print(f"  - {k} : {v}")
    print("=" * 60)

