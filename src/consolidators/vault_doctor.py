"""
Module de maintenance et d'audit du coffre Obsidian (Vault Doctor).
Centralise l'intégrité taxonomique, la détection de troncatures, la purge des fallbacks
et la mise à niveau in-place des notes conceptuelles de 02_Concepts/.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml
from tqdm import tqdm

from src.config import AUTHORIZED_SEMANTIC_TOPICS, normalize_to_macro_topic, settings
from src.database.db_manager import DBManager
from src.database.vector_store import vector_store
from src.utils.markdown_io import (
    ConceptFrontmatter,
    ParsedConceptNote,
    parse_concept_file,
    parse_concept_string,
    write_concept_file,
)

logger = logging.getLogger("Exocortex.VaultDoctor")


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


def scan_and_upgrade_existing_concepts(db: DBManager) -> Set[str]:
    """
    Scanne les fiches issues du Takeout Gemini (origin gemini_takeout + session_id) dans Vault_Data/02_Concepts/ :
    - Détecte les faux succès (fallbacks heuristiques v0.1.1, troncatures) et les déplace dans
      02_Concepts/_Quarantine/ (jamais de suppression définitive), puis les retire de LanceDB.
    - Assainit les fiches réussies sur place :
        * Retrait des blocs de requêtes/vidéos corrélées YouTube/Search.
        * Remapping déterministe vers les 16 macro-catégories maîtresses (+ insertion de l'ancien topic dans tags).
        * Ajout de session_id et distillation_status: "success" dans le frontmatter.
        * Synchronisation des statuts en base SQLite.
    - Les fiches vocales, nocturnes, manuelles et fusionnées sont laissées intactes.
    - Retourne l'ensemble des session_id complétées pour le mode Delta (Skip instantané).
    """
    doctor = VaultDoctor(db_manager=db)
    return doctor.scan_and_upgrade_existing_concepts()


class VaultDoctor:
    """Gestionnaire d'intégrité, d'assainissement et de réparation du coffre Obsidian."""

    def __init__(self, db_manager: Optional[DBManager] = None) -> None:
        self.db = db_manager or DBManager()

    def ensure_taxonomy(self) -> None:
        """Assure la présence du fichier de taxonomie fermé."""
        ensure_strict_taxonomy_file()

    def scan_and_upgrade_existing_concepts(self) -> Set[str]:
        """
        Implémentation complète de l'assainissement in-place et de la purge des fallbacks.
        """
        self.ensure_taxonomy()

        completed_session_ids: Set[str] = set()
        completed_session_ids.update(self.db.get_completed_session_ids_from_db())

        concept_files = sorted(list(settings.CONCEPTS_DIR.glob("*.md")))
        if not concept_files:
            logger.info("Aucune fiche existante trouvée dans %s.", settings.CONCEPTS_DIR)
            return completed_session_ids

        purged_fallbacks = 0
        upgraded_notes = 0
        skipped_foreign = 0

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

                raw_fm = _read_raw_frontmatter(content)

                # Fiches fusionnées par le défragmenteur : leurs sessions sources restent terminées (A8)
                merged_sids = _as_str_list(raw_fm.get("session_ids"))
                if merged_sids or raw_fm.get("merged_from"):
                    for sid in merged_sids:
                        completed_session_ids.add(sid)
                        self.db.update_session_distillation_metadata(
                            session_id=sid,
                            topics_list=[normalize_to_macro_topic(str(raw_fm.get("semantic_topic") or ""))],
                            notes_list=[fpath.stem],
                            distillation_status="success",
                        )
                    pbar.update(1)
                    continue

                # Extraction de session_id
                m_sid = re.search(r'session_id:\s*["\']?([^"\'\n\r]+)["\']?', content)
                if m_sid:
                    extracted_sid = m_sid.group(1).strip()
                else:
                    m_body_sid = re.search(r'Session Gemini [^\w]*([a-zA-Z0-9_-]+)', content)
                    extracted_sid = m_body_sid.group(1).strip() if m_body_sid else None

                # Périmètre strict (A6) : seules les fiches issues du Takeout Gemini, rattachées à une
                # session, relèvent du Vault Doctor. Notes vocales, nocturnes ou manuelles ne sont ni
                # purgées ni réécrites (le défaut ConceptFrontmatter.origin ne compte pas : on lit le YAML brut).
                if "gemini_takeout" not in _as_str_list(raw_fm.get("origin")) or not extracted_sid:
                    if extracted_sid:
                        completed_session_ids.add(extracted_sid)
                    skipped_foreign += 1
                    pbar.update(1)
                    continue

                # Découpe du corps Markdown avant le bloc de télémétrie final de l'Exocortex
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
                        has_conclusion = bool(re.search(r"###\s*(?:Conclusions?|Synthèse|Bilan|Commandes\s*Clés)", body_before_abstract, re.IGNORECASE))
                        is_table_or_bullet = last_line.startswith(("|", "*", "-", ">"))
                        if len(body_before_abstract) > 500 and (has_conclusion or is_table_or_bullet):
                            is_truncated = False
                        else:
                            is_truncated = True

                # Détection des critères de fallback dégradé ou troncature
                is_fallback = (
                    is_truncated
                    or "takeout_coldstart" in content
                    or ("### Problématique & Contexte" in content and "- Session composée de" in content)
                    or bool(re.search(r'semantic_topic:\s*["\']?A_Trier["\']?', content))
                    or bool(re.search(r'distillation_status:\s*["\']?failed_fallback["\']?', content))
                )

                if is_fallback:
                    if is_truncated:
                        logger.warning("Fiche tronquée détectée et mise en quarantaine : %s (dernière ligne : '%s')", fpath.name, last_line[-40:])
                    try:
                        quarantined = move_to_quarantine(fpath)
                        logger.info("Fiche déplacée en quarantaine : %s", quarantined)
                    except Exception as exc:
                        logger.warning("Impossible de mettre %s en quarantaine : %s", fpath.name, exc)
                        pbar.update(1)
                        continue
                    vector_store.delete_by_slug(fpath.stem)
                    purged_fallbacks += 1
                    if extracted_sid:
                        self.db.update_session_distillation_metadata(
                            session_id=extracted_sid,
                            topics_list=[],
                            notes_list=[],
                            distillation_status="pending",
                        )
                else:
                    if extracted_sid:
                        completed_session_ids.add(extracted_sid)

                    # Utilisation de markdown_io pour normaliser et assainir proprement
                    try:
                        note = parse_concept_string(content, file_path=fpath)
                        fm = note.frontmatter
                        raw_topic = fm.semantic_topic
                        macro_topic = normalize_to_macro_topic(raw_topic)
                        fm.semantic_topic = macro_topic

                        if raw_topic != macro_topic:
                            legacy_tag = raw_topic.lower()
                            if legacy_tag not in [t.lower() for t in fm.tags]:
                                fm.tags.append(legacy_tag)

                        if extracted_sid and not fm.session_id:
                            fm.session_id = extracted_sid
                        fm.distillation_status = "success"

                        # Nettoyage du corps des empreintes résiduelles
                        clean_body = re.sub(
                            r'>\s*-\s*\*\*Requêtes et vidéos corrélées\s*:\*\*.*?(?=>\s*-\s*\*\*Connexions sémantiques|\Z)',
                            '',
                            note.body,
                            flags=re.DOTALL,
                        ).strip()
                        # Suppression de callout abstract résiduel dans le corps
                        clean_body = re.sub(r'>\s*\[!abstract\]-[^\n]*\n(?:>[^\n]*\n)*', '', clean_body).strip()
                        note.body = clean_body
                        # Les empreintes corrélées se trouvent aussi dans le bloc de télémétrie (v0.5.6)
                        note.telemetry_lines = [
                            line for line in note.telemetry_lines
                            if not re.search(r"Requêtes et vidéos corrélées|\[youtube\]|\[google_search\]", line)
                        ]

                        write_concept_file(note, fpath)
                        upgraded_notes += 1

                        if extracted_sid:
                            self.db.update_session_distillation_metadata(
                                session_id=extracted_sid,
                                topics_list=[macro_topic],
                                notes_list=[fpath.stem],
                                distillation_status="success",
                            )
                    except Exception as exc:
                        logger.warning("Erreur mise à niveau note %s : %s", fpath.name, exc)

                pbar.update(1)

        # Intégration des sessions rejetées (bruit consolidé)
        with self.db.get_connection() as conn:
            cur = conn.execute("SELECT session_id FROM chat_sessions WHERE distillation_status = 'misc_noise';")
            for row in cur.fetchall():
                completed_session_ids.add(row[0])

        logger.info(
            "Assainissement terminé : %d fallbacks en quarantaine, %d fiches assainies sur place, "
            "%d fiches hors périmètre Takeout ignorées, %d sessions complètes en mémoire.",
            purged_fallbacks,
            upgraded_notes,
            skipped_foreign,
            len(completed_session_ids),
        )
        return completed_session_ids


def _read_raw_frontmatter(content: str) -> Dict[str, Any]:
    """Lit le frontmatter YAML tel qu'écrit sur disque, sans valeurs par défaut du modèle."""
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", content, re.DOTALL)
    if not match:
        return {}
    try:
        loaded = yaml.safe_load(match.group(1))
        return loaded if isinstance(loaded, dict) else {}
    except yaml.YAMLError:
        return {}


def _as_str_list(value: Any) -> List[str]:
    """Normalise un champ YAML scalaire ou liste en liste de chaînes non vides."""
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(v).strip() for v in value if str(v).strip()]
    return [s.strip() for s in str(value).strip("[]").replace('"', "").replace("'", "").split(",") if s.strip()]


def move_to_quarantine(fpath: Path) -> Path:
    """Déplace une fiche dans 02_Concepts/_Quarantine/ (jamais de suppression définitive)."""
    quarantine_dir = settings.CONCEPTS_QUARANTINE_DIR
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    dest = quarantine_dir / fpath.name
    if dest.exists():
        dest = quarantine_dir / f"{fpath.stem}_{datetime.now().strftime('%Y%m%d%H%M%S')}{fpath.suffix}"
    shutil.move(str(fpath), str(dest))
    return dest

