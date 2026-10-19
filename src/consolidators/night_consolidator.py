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

from src.config import settings
from src.database.db_manager import (
    DailyMetricRecord,
    DBManager,
    HistoricalFootprintRecord,
    RawActivityRecord,
)
from src.database.vector_store import vector_store
from src.consolidators.drive_compiler import DriveCompiler
from src.ingestors.takeout_ingestor import register_new_taxonomy_tag
from src.llm.ollama_client import HardwareProbe, VRAMInsufficientError, llm_client
from src.llm.prompts import (
    SYSTEM_PROMPT_ANTI_WIKIPEDIA,
    PROMPT_DYNAMIC_TAXONOMY_RULE,
    PROMPT_NIGHT_DAY_SYNTHESIS_SYSTEM,
    PROMPT_NIGHT_CONCEPT_SYNTHESIS_SYSTEM,
)

logger = logging.getLogger("Exocortex.NightConsolidator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


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


# ==============================================================================
# CHARGEMENT ET PARSING DE LA TAXONOMIE FERMÉE
# ==============================================================================

def load_authorized_taxonomy() -> Tuple[List[str], Dict[str, str]]:
    """
    Lit et extrait la liste fermée des tags autorisés depuis Vault_Data/00_Meta/Taxonomie_Tags.md.
    Retourne (liste_des_tags, dictionnaire_tag_description).
    """
    tax_path = settings.TAXONOMIE_TAGS_PATH
    if not tax_path.exists():
        logger.warning("Fichier de taxonomie introuvable (%s). Utilisation de tags par défaut.", tax_path)
        default_tags = [
            "IA_Agentique_et_RAG",
            "LLM_Local_et_Hardware",
            "Prompt_Engineering_et_Suno",
            "Dev_Web_et_Stack_Astro",
            "Chefferie_Projet_et_UX",
            "Freelance_et_Acquisition",
            "Philo_Droit_et_Morale",
            "Metaphysique_et_Physique",
            "Sociologie_et_Politique",
            "Linguistique_et_Culture_Web",
            "MMORPG_Theorycraft",
            "Gaming_Solo_et_Modding",
            "Webtoons_Manga_et_Anime",
            "Analyse_Musicale_et_MAO",
            "Nutrition_Volume_Eating",
            "Sante_et_Admin_Perso",
            "Introspection_et_Neuroatypie",
        ]
        return default_tags, {t: "Topic cognitif standard" for t in default_tags}

    with open(tax_path, "r", encoding="utf-8") as f:
        content = f.read()

    tags: List[str] = []
    descriptions: Dict[str, str] = {}

    for line in content.splitlines():
        # Match lignes comme: - `IA_Agentique_et_RAG` : Exocortex, Obsidian...
        m = re.search(r"-\s*[`\*]{1,2}([A-Za-z0-9_]+)[`\*]{1,2}\s*:\s*(.*)", line)
        if m:
            tag = m.group(1).strip()
            desc = m.group(2).strip()
            tags.append(tag)
            descriptions[tag] = desc

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
        return "Dev_Web_et_Stack_Astro", "production"
    if any(k in text for k in ["ollama", "lancedb", "exocortex", "obsidian", "rag", "embedding"]):
        return "IA_Agentique_et_RAG", "production"
    if any(k in text for k in ["gemini", "chatgpt", "claude.ai", "sillytavern"]):
        return "IA_Agentique_et_RAG", "chat_ia"
    if any(k in text for k in ["wow.exe", "world of warcraft", "warcraft", "guild wars", "lost ark"]):
        return "MMORPG_Theorycraft", "gaming"
    if any(k in text for k in ["minecraft", "skyrim", "cheat engine", "yuzu", "steam"]):
        return "Gaming_Solo_et_Modding", "gaming"
    if any(k in text for k in ["youtube", "stremio", "plex", "netflix", "crunchyroll", "anime", "webtoon", "asura", "reaper"]):
        return "Webtoons_Manga_et_Anime", "media"
    if any(k in text for k in ["suno", "spotify", "fl studio", "maschine", "k-pop", "nmixx"]):
        return "Analyse_Musicale_et_MAO", "media"
    if any(k in text for k in ["calorie", "myfitnesspal", "recette", "repas", "volume eating"]):
        return "Nutrition_Volume_Eating", "exploration"
    if any(k in text for k in ["droit", "jurisprudence", "loi", "philo", "spinoza", "camus"]):
        return "Philo_Droit_et_Morale", "exploration"

    # Repli par défaut sur A_Trier pour éviter de polluer les tags nobles
    fallback_tag = "A_Trier" if allowed_tags and "A_Trier" in allowed_tags else "A_Trier"
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
        free_gb, total_gb = HardwareProbe.get_vram_info()
        logger.info("VRAM disponible avant Passe 1 : %.2f Go / %.2f Go", free_gb, total_gb)

        if free_gb < settings.MIN_FREE_VRAM_GB:
            raise VRAMInsufficientError(f"VRAM insuffisante ({free_gb:.2f} Go < {settings.MIN_FREE_VRAM_GB} Go). Batch différé.")

        # 1. Traitement des captures d'écran différées
        screenshot_activities = self.db.get_unprocessed_activities_with_screenshots(limit=50)
        logger.info("Nombre d'activités avec capture d'écran à analyser : %d", len(screenshot_activities))

        for act in screenshot_activities:
            act_id = act["id"]
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
                        keep_alive=0,
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

            # Mise à jour de la base de données
            self.db.update_activity_visual_summary(act_id, visual_summary)

        # 2. Classification sémantique des activités brutes (processed = 0)
        unprocessed = self.db.get_unprocessed_raw_activities(limit=500)
        logger.info("Activités brutes à classifier : %d", len(unprocessed))

        if not unprocessed:
            logger.info("Aucune activité brute en attente de classification.")
            llm_client.unload_model(settings.MODEL_FAST_VISION)
            return 0

        # Regroupement par signature unique (executable, window_title, ocr_snippet) pour minimiser les appels
        signatures: Dict[Tuple[str, str, Optional[str]], List[int]] = {}
        for row in unprocessed:
            sig = (row["executable"], row["window_title"], row["ocr_snippet"])
            signatures.setdefault(sig, []).append(row["id"])

        logger.info("Signatures uniques identifiées : %d", len(signatures))
        updates: List[Tuple[int, str, str]] = []

        is_ollama_ready = llm_client.is_alive()

        for (exe, title, ocr), row_ids in signatures.items():
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
                    f"{PROMPT_DYNAMIC_TAXONOMY_RULE}\n"
                    "Modes cognitifs autorisés : 'production', 'exploration', 'chat_ia', 'gaming', 'media'.\n"
                    "Assigne le semantic_topic exact et le cognitive_mode le plus pertinent."
                )
                try:
                    res = llm_client.generate_structured(
                        prompt=prompt,
                        response_model=WindowClassification,
                        system="Tu es un classificateur de télémétrie strict. Réponds uniquement en JSON valide conforme au schéma.",
                        model=settings.MODEL_FAST_VISION,
                        keep_alive=0,
                    )
                    # Enregistrement dynamique des nouveaux topics émergents
                    if res.is_new_topic and res.confidence >= 0.75:
                        clean_tag = res.semantic_topic.strip()
                        if re.match(r"^[A-Za-z0-9]+_[A-Za-z0-9_]+$", clean_tag):
                            if clean_tag not in self.allowed_tags:
                                desc = res.new_topic_description or "Topic émergent issu de l'activité écran"
                                if register_new_taxonomy_tag(clean_tag, desc):
                                    self.allowed_tags.append(clean_tag)
                                    self.tag_descriptions[clean_tag] = desc
                                    chosen_topic = clean_tag
                            else:
                                chosen_topic = clean_tag

                    if not chosen_topic:
                        if res.semantic_topic in self.allowed_tags:
                            chosen_topic = res.semantic_topic
                        else:
                            chosen_topic, _ = heuristic_fallback_classification(exe, title, ocr, self.allowed_tags)
                    chosen_mode = res.cognitive_mode
                except Exception as exc:
                    logger.debug("Repli heuristique pour [%s] '%s' (%s)", exe, title, exc)
                    chosen_topic, chosen_mode = heuristic_fallback_classification(exe, title, ocr, self.allowed_tags)
            else:
                chosen_topic, chosen_mode = heuristic_fallback_classification(exe, title, ocr, self.allowed_tags)

            for rid in row_ids:
                updates.append((rid, chosen_topic, chosen_mode))

        # Application de la mise à jour par lots dans SQLite
        if updates:
            self.db.mark_raw_activities_processed(updates)
            logger.info("%d enregistrements d'activité classifiés et marqués processed=1.", len(updates))

        # 3. Purge explicite de la VRAM (keep_alive=0)
        llm_client.unload_model(settings.MODEL_FAST_VISION)
        logger.info("--- FIN PASSE 1 : VRAM PURGÉE ---")
        return len(updates)

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

        # --- Algorithme de Tunnels d'Hyperfocus ---
        # Fusion des blocs partageant le même topic avec tolérance < 120s d'interruption
        sorted_acts = sorted(
            activities,
            key=lambda x: datetime.strptime(x["timestamp_start"], "%Y-%m-%d %H:%M:%S")
            if isinstance(x["timestamp_start"], str)
            else x["timestamp_start"],
        )

        max_hyperfocus_sec = 0
        max_hyperfocus_topic: Optional[str] = None
        current_tunnel_topic: Optional[str] = None
        current_tunnel_duration = 0
        current_tunnel_interruption_sec = 0
        context_switch_events = 0

        for idx, act in enumerate(sorted_acts):
            topic = act.get("semantic_topic") or "Non_Classe"
            duration = act["duration_sec"]

            if current_tunnel_topic is None:
                current_tunnel_topic = topic
                current_tunnel_duration = duration
                continue

            if topic == current_tunnel_topic:
                # Même sujet : le tunnel continue (on réintègre l'interruption tolérée)
                current_tunnel_duration += duration + current_tunnel_interruption_sec
                current_tunnel_interruption_sec = 0
            else:
                # Sujet différent : vérifier si c'est une micro-interruption tolérée (< 120s)
                if duration < 120 and (idx + 1 < len(sorted_acts)) and (sorted_acts[idx + 1].get("semantic_topic") == current_tunnel_topic):
                    current_tunnel_interruption_sec += duration
                    continue

                # Rupture effective du tunnel
                if current_tunnel_duration > max_hyperfocus_sec:
                    max_hyperfocus_sec = current_tunnel_duration
                    max_hyperfocus_topic = current_tunnel_topic

                context_switch_events += 1
                current_tunnel_topic = topic
                current_tunnel_duration = duration
                current_tunnel_interruption_sec = 0

        if current_tunnel_duration > max_hyperfocus_sec:
            max_hyperfocus_sec = current_tunnel_duration
            max_hyperfocus_topic = current_tunnel_topic

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

    # ==========================================================================
    # PASSE 2 : SYNTHÈSE ÉPISODIQUE & FICHES CONCEPTS (GEMMA 4:26B OU 12B)
    # ==========================================================================

    def run_pass_2_synthesis(self, target_date: date, metric: DailyMetricRecord) -> None:
        """
        Passe 2 :
        1. Rédige le journal épisodique 01_Episodique/YYYY-MM-DD.md avec synthèse LLM des tunnels réels.
        2. Pour tout sujet ayant cumulé >= 45 minutes dans la journée, crée ou enrichit la fiche dans 02_Concepts/.
        3. Purge la VRAM en fin de passe.
        """
        if metric.total_screen_sec == 0:
            logger.info("Temps d'écran total nul pour le %s. Aucune note épisodique ou conceptuelle générée.", target_date.isoformat())
            return

        logger.info("--- DÉBUT PASSE 2 : SYNTHÈSE ÉPISODIQUE & CONCEPTS ---")
        free_gb, _ = HardwareProbe.get_vram_info()

        # Choix du modèle selon la VRAM libre
        target_model = settings.MODEL_HEAVY_SYNTHESIS if free_gb >= settings.FULL_DUAL_MODEL_VRAM_GB else settings.MODEL_FAST_VISION
        effective_model = llm_client.check_and_select_model(target_model)
        logger.info("Modèle sélectionné pour la synthèse : %s (VRAM libre: %.2f Go)", effective_model, free_gb)

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
        if llm_client.is_alive():
            try:
                section_3_content = llm_client.generate_text(
                    prompt=synthesis_prompt,
                    system=PROMPT_NIGHT_DAY_SYNTHESIS_SYSTEM,
                    model=effective_model,
                    keep_alive=0,
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

        # 3. Distillation ou enrichissement des fiches conceptuelles (seuil >= 45 min = 2700s)
        for topic_name, duration_secs in top_topics_dict.items():
            if duration_secs < 2700:  # Seuil strict de 45 minutes
                continue

            slug = re.sub(r"[\s_]+", "-", topic_name.lower()).strip("-")
            concept_file = settings.CONCEPTS_DIR / f"{slug}.md"
            duration_fmt = f"{duration_secs // 3600}h{(duration_secs % 3600) // 60:02d}"

            topic_items = topic_activities.get(topic_name, [])
            topic_context_str = "\n".join(topic_items[:12])

            if concept_file.exists():
                with open(concept_file, "r", encoding="utf-8") as cf:
                    existing_text = cf.read()

                m_updated = re.sub(r'updated_at:\s*"[^"]*"', f'updated_at: "{date_str}"', existing_text)
                m_time = re.search(r'total_time_invested_min:\s*(\d+)', m_updated)
                if m_time:
                    prev_time = int(m_time.group(1))
                    new_time = prev_time + (duration_secs // 60)
                    m_updated = re.sub(r'total_time_invested_min:\s*\d+', f'total_time_invested_min: {new_time}', m_updated)

                new_source_line = f">   - Activité écran du `{date_str}` ({duration_fmt})\n"
                if "> - **Sources épisodiques :**\n" in m_updated:
                    m_updated = m_updated.replace("> - **Sources épisodiques :**\n", f"> - **Sources épisodiques :**\n{new_source_line}")

                if llm_client.is_alive() and topic_context_str:
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
                            keep_alive=0,
                        )
                        if enrich_text.strip():
                            if "> [!abstract]- Généalogie & Télémétrie" in m_updated:
                                parts = m_updated.split("> [!abstract]- Généalogie & Télémétrie")
                                m_updated = f"{parts[0].rstrip()}\n\n{enrich_text.strip()}\n\n> [!abstract]- Généalogie & Télémétrie{parts[1]}"
                            else:
                                m_updated = f"{m_updated.rstrip()}\n\n{enrich_text.strip()}\n"
                    except Exception as exc:
                        logger.warning("Erreur enrichissement concept %s : %s", slug, exc)

                with open(concept_file, "w", encoding="utf-8") as cf:
                    cf.write(m_updated)
                logger.info("Fiche conceptuelle enrichie : %s (+%s)", concept_file.name, duration_fmt)
            else:
                concept_id = datetime.now().strftime("%Y%m%d%H%M")
                synthesized_body = ""
                if llm_client.is_alive() and topic_context_str:
                    concept_prompt = (
                        f"L'utilisateur a passé {duration_fmt} de concentration continue sur le sujet '{topic_name}' le {date_str}.\n"
                        f"Fenêtres, outils et activités associées :\n{topic_context_str}\n\n"
                        "Rédige le corps analytique d'une note conceptuelle (2 à 3 sections Markdown avec sous-titres : "
                        "### Contexte & Problématique, ### Choix Techniques & Implémentation, ### Arbitrages & Prochaines Étapes). "
                        "Zéro paraphrase Wikipédia, uniquement du contenu ancré dans l'activité réelle."
                    )
                    try:
                        synthesized_body = llm_client.generate_text(
                            prompt=concept_prompt,
                            system=PROMPT_NIGHT_CONCEPT_SYNTHESIS_SYSTEM,
                            model=effective_model,
                            keep_alive=0,
                        )
                    except Exception as exc:
                        logger.warning("Erreur génération corps concept %s : %s", slug, exc)

                if not synthesized_body.strip():
                    synthesized_body = (
                        f"### Contexte & Investigations\n"
                        f"Session d'hyperfocus de {duration_fmt} consacrée à {topic_name.replace('_', ' ')}.\n\n"
                        f"### Activités & Traces Notables\n"
                        + "\n".join([f"- {it}" for it in topic_items[:6]])
                    )

                # Connexions sémantiques dynamiques
                related_tags = [t for t in self.allowed_tags if t != topic_name][:2]
                related_links_str = ", ".join([f"[[{t}]]" for t in related_tags]) if related_tags else f"[[{topic_name}]]"

                new_concept = f"""---
id: "{concept_id}"
title: "{topic_name.replace('_', ' ')}"
type: "concept"
origin: ["screen_telemetry"]
semantic_topic: "{topic_name}"
tags: ["{topic_name.lower()}", "screen_telemetry"]
created_at: "{date_str}"
updated_at: "{date_str}"
total_time_invested_min: {duration_secs // 60}
summary_1_line: "Synthèse et développement des réflexions sur {topic_name.replace('_', ' ')}."
---

# {topic_name.replace('_', ' ')}

{synthesized_body.strip()}

> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)
> - **Temps cumulé sur ce sujet :** {duration_fmt}
> - **Sources épisodiques :**
>   - Activité écran du `{date_str}` ({duration_fmt})
> - **Connexions sémantiques :** {related_links_str}
"""
                with open(concept_file, "w", encoding="utf-8") as cf:
                    cf.write(new_concept)
                logger.info("Nouvelle fiche conceptuelle créée via synthèse LLM : %s", concept_file.name)

        # Purge de la VRAM après la synthèse
        llm_client.unload_model(effective_model)
        logger.info("--- FIN PASSE 2 : VRAM PURGÉE ---")

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

        # Passe 1 : Vision & Tagging
        classified_count = self.run_pass_1_vision_and_tagging()

        # Identification des dates à traiter
        dates_to_process = self.db.get_distinct_activity_dates(processed_only=True)
        if target_date and target_date not in dates_to_process:
            dates_to_process.append(target_date)
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

        # Pour chaque date : agrégation SQLite & Passe 2
        for d in dates_to_process:
            metric = self.calculate_daily_metrics_for_date(d)
            self.run_pass_2_synthesis(d, metric)

        # Passe 3 : Vectorisation LanceDB
        vector_count = self.run_pass_3_vector_indexing()

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

