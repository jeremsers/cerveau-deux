"""
Module 10 : Défragmenteur Sémantique, Contradictions & Réécriture de Graphe (v0.4.0 / EXO-012).
Exécute le Sommeil Profond pour lutter contre l'entropie du coffre Obsidian :
1. Détection des doublons sémantiques au sein du même semantic_topic (cosine similarity >= 0.88 + tokens partagés).
2. Fusion déterministe / LLM (26B) avec cumul des temps investis et réécriture globale des [[wikilinks]].
3. Archivage systématique dans 02_Concepts/_Archive_Merged/ (zéro perte de données, aucun unlink()).
4. Traçage des évolutions d'arbitrage via callouts Obsidian idempotents (> [!warning] Évolution d'Arbitrage).
"""

from __future__ import annotations

import json
import logging
import math
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from pydantic import BaseModel, Field

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.config import settings
from src.database.db_manager import DBManager
from src.database.vector_store import VectorStore
from src.llm.ollama_client import VRAMBusyError, llm_client
from src.utils.markdown_io import (
    ConceptFrontmatter,
    ParsedConceptNote,
    parse_concept_file,
    write_concept_file,
)
from src.utils.path_safety import resolve_within, safe_slug

logger = logging.getLogger("Exocortex.GraphDefragmenter")

# Taille maximale de chaque corps de fiche transmis au LLM pour une décision de fusion :
# assez pour contenir une fiche complète, borné pour tenir dans num_ctx.
MERGE_PROMPT_BODY_MAX_CHARS = 12000


def _collect_session_ids(note: ParsedConceptNote) -> Set[str]:
    """Rassemble session_id et session_ids (fiche déjà fusionnée) d'une note."""
    ids: Set[str] = set()
    if note.frontmatter.session_id:
        ids.add(str(note.frontmatter.session_id).strip())
    extra = (note.frontmatter.model_extra or {}).get("session_ids") or []
    if isinstance(extra, str):
        extra = [extra]
    ids.update(str(s).strip() for s in extra if str(s).strip())
    return ids

STOPWORDS_SIGNIFICANT = {
    "le", "la", "les", "un", "une", "des", "du", "de", "d", "l", "en", "et", "ou",
    "a", "dans", "par", "pour", "sur", "avec", "sans", "sous", "ce", "cet", "cette",
    "ces", "mon", "ton", "son", "notre", "votre", "leur", "the", "a", "an", "and",
    "or", "in", "on", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "concept", "note", "fiche", "session"
}


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """
    Calcule la similarité cosinus entre deux vecteurs en pur Python (0 Mo VRAM, math standard).
    Retourne une valeur normalisée dans [-1.0, 1.0].
    """
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0

    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot_product / (norm_a * norm_b)


class ConceptMergeSchema(BaseModel):
    """Schéma de décision pour la fusion ou l'arbitrage de contradictions entre 2 fiches."""
    should_merge: bool = Field(description="Vrai si les deux notes sont redondantes et doivent être fusionnées en une seule.")
    canonical_title: str = Field(description="Titre canonique unifié de la fiche résultante.")
    canonical_slug: str = Field(description="Slug kebab-case de la fiche résultante (sans extension .md).")
    merged_summary_1_line: str = Field(description="Résumé d'une seule phrase englobant l'intégralité du nouveau concept.")
    merged_markdown_body: str = Field(description="Corps Markdown unifié et analytique de la fiche fusionnée.")
    contradiction_detected: bool = Field(default=False, description="Vrai si la note la plus récente remplace ou contredit un choix de la note ancienne.")
    contradiction_explanation: Optional[str] = Field(default=None, description="Explication concise du changement d'arbitrage architectural ou technique.")


class GraphDefragmenter:
    """Gestionnaire de défragmentation sémantique et d'évolution d'arbitrage du coffre Obsidian."""

    def __init__(
        self,
        db_manager: Optional[DBManager] = None,
        vector_store: Optional[VectorStore] = None,
    ) -> None:
        self.db = db_manager or DBManager()
        self.vector_store = vector_store or VectorStore()
        settings.ensure_directories()

    def find_merge_and_contradiction_candidates(
        self,
        similarity_threshold: float = 0.88,
        contradiction_min_sim: float = 0.78,
    ) -> List[Dict[str, Any]]:
        """
        Scanne la base vectorielle LanceDB pour détecter les paires candidates au sein du même semantic_topic :
        - merge_candidate : cos_sim >= similarity_threshold ET au moins 1 token partagé hors stopwords.
        - contradiction_candidate : contradiction_min_sim <= cos_sim < similarity_threshold.
        """
        candidates: List[Dict[str, Any]] = []

        try:
            tbl = self.vector_store._table
            df = tbl.to_pandas()
        except Exception as exc:
            logger.warning("Impossible de lire les vecteurs LanceDB : %s", exc)
            return candidates

        if df.empty or len(df) < 2:
            return candidates

        # Regroupement par macro-catégorie sémantique
        grouped = df.groupby("semantic_topic")

        for topic, group in grouped:
            records = group.to_dict("records")
            n = len(records)
            for i in range(n):
                for j in range(i + 1, n):
                    rec_a = records[i]
                    rec_b = records[j]

                    vec_a = rec_a.get("vector")
                    vec_b = rec_b.get("vector")
                    if vec_a is None or vec_b is None:
                        continue

                    # Conversion éventuelle numpy -> list
                    if hasattr(vec_a, "tolist"):
                        vec_a = vec_a.tolist()
                    if hasattr(vec_b, "tolist"):
                        vec_b = vec_b.tolist()

                    sim = cosine_similarity(vec_a, vec_b)

                    path_a = Path(rec_a["file_path"]) if rec_a.get("file_path") else settings.CONCEPTS_DIR / f"{rec_a['slug']}.md"
                    path_b = Path(rec_b["file_path"]) if rec_b.get("file_path") else settings.CONCEPTS_DIR / f"{rec_b['slug']}.md"

                    # Interdiction stricte de l'auto-fusion ou comparaison de la même note
                    if rec_a.get("slug") == rec_b.get("slug") or path_a.resolve() == path_b.resolve():
                        continue

                    # Extraction des tokens pour le garde-fou
                    title_a = str(rec_a.get("title") or "")
                    title_b = str(rec_b.get("title") or "")
                    tags_a = str(rec_a.get("tags") or "")
                    tags_b = str(rec_b.get("tags") or "")

                    tokens_a = {
                        t for t in re.findall(r"\b[a-zA-Z0-9À-ÿ_-]{3,}\b", f"{title_a} {tags_a}".lower())
                        if t not in STOPWORDS_SIGNIFICANT
                    }
                    tokens_b = {
                        t for t in re.findall(r"\b[a-zA-Z0-9À-ÿ_-]{3,}\b", f"{title_b} {tags_b}".lower())
                        if t not in STOPWORDS_SIGNIFICANT
                    }
                    shared_tokens = tokens_a & tokens_b

                    if sim >= similarity_threshold and len(shared_tokens) >= 1:
                        candidates.append({
                            "type": "merge_candidate",
                            "note_a": path_a,
                            "note_b": path_b,
                            "similarity": round(sim, 4),
                            "topic": str(topic),
                            "shared_tokens": list(shared_tokens),
                        })
                    elif contradiction_min_sim <= sim < similarity_threshold:
                        candidates.append({
                            "type": "contradiction_candidate",
                            "note_a": path_a,
                            "note_b": path_b,
                            "similarity": round(sim, 4),
                            "topic": str(topic),
                            "shared_tokens": list(shared_tokens),
                        })

        logger.info("%d paire(s) candidate(s) identifiée(s) pour le Sommeil Profond.", len(candidates))
        return candidates

    def merge_concepts_pair(
        self,
        note_a_path: Path,
        note_b_path: Path,
        merge_decision: ConceptMergeSchema,
        defer_vector_sync: bool = False,
    ) -> Path:
        """
        Fusionne 2 notes de concepts selon la décision validée :
        1. Parse et cumule total_time_invested_min, fusionne tags, origin et telemetry_lines.
        2. Écrit la note canonique dans 02_Concepts/<canonical_slug>.md.
        3. Déplace sans unlink() les anciennes notes dans 02_Concepts/_Archive_Merged/ (Zéro Perte).
        4. Nettoie LanceDB des anciens slugs et indexe la nouvelle note (ou reporte si defer_vector_sync=True).
        5. Réécrit tous les [[wikilinks]] pointant vers les anciennes cibles dans tout le coffre.
        """
        if note_a_path.resolve() == note_b_path.resolve():
            raise ValueError(f"Impossible de fusionner une fiche avec elle-même : {note_a_path}")

        if not note_a_path.exists() or not note_b_path.exists():
            raise FileNotFoundError(f"L'une des notes à fusionner est introuvable : {note_a_path} / {note_b_path}")

        note_a = parse_concept_file(note_a_path)
        note_b = parse_concept_file(note_b_path)

        # 1. Cumul du temps et métadonnées
        total_time = (note_a.frontmatter.total_time_invested_min or 0) + (note_b.frontmatter.total_time_invested_min or 0)
        merged_tags = sorted(list(set(note_a.frontmatter.tags) | set(note_b.frontmatter.tags)))
        merged_origins = sorted(list(set(note_a.frontmatter.origin) | set(note_b.frontmatter.origin)))

        # Dates
        created_candidates = [d for d in [note_a.frontmatter.created_at, note_b.frontmatter.created_at] if d]
        earliest_created = min(created_candidates) if created_candidates else datetime.now().strftime("%Y-%m-%d")
        updated_at = datetime.now().strftime("%Y-%m-%d")

        # Fusion des lignes de télémétrie épisodiques
        telemetry_lines: List[str] = [
            "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)",
            f"> - **Temps cumulé sur ce sujet :** {total_time}m",
            "> - **Sources épisodiques :**",
        ]

        seen_sources: Set[str] = set()
        for note in [note_a, note_b]:
            for line in note.telemetry_lines:
                if line.startswith(">   - ") and line not in seen_sources:
                    telemetry_lines.append(line)
                    seen_sources.add(line)

        telemetry_lines.append(
            f"> - **Fiches sources fusionnées :** [[{note_a.frontmatter.title}]] et [[{note_b.frontmatter.title}]]"
        )

        # 2. Construction de la note canonique (slug issu du LLM : slugifié et confiné, A7)
        target_path = self._resolve_canonical_target(merge_decision, note_a_path, note_b_path)
        canonical_slug = target_path.stem

        # Sessions sources conservées pour le mode Delta du Takeout (A8)
        merged_session_ids = sorted(_collect_session_ids(note_a) | _collect_session_ids(note_b))
        merged_from = sorted({note_a_path.stem, note_b_path.stem})

        fm = ConceptFrontmatter(
            id=canonical_slug,
            title=merge_decision.canonical_title,
            type="concept",
            origin=merged_origins,
            semantic_topic=note_a.frontmatter.semantic_topic or note_b.frontmatter.semantic_topic,
            tags=merged_tags,
            created_at=earliest_created,
            updated_at=updated_at,
            total_time_invested_min=total_time,
            summary_1_line=merge_decision.merged_summary_1_line,
            session_ids=merged_session_ids,
            merged_from=merged_from,
        )

        canonical_note = ParsedConceptNote(
            frontmatter=fm,
            title_h1=merge_decision.canonical_title,
            body=merge_decision.merged_markdown_body,
            telemetry_lines=telemetry_lines,
            file_path=target_path,
        )

        # 3. Sauvegarde et archivage Zéro Perte (Invariant 1)
        archive_dir = settings.CONCEPTS_ARCHIVE_MERGED_DIR
        archive_dir.mkdir(parents=True, exist_ok=True)

        # Si l'un des anciens fichiers a le même chemin que target_path, on fait une copie de sécurité dans _Archive_Merged
        for old_path in [note_a_path, note_b_path]:
            if old_path.resolve() == target_path.resolve():
                backup_path = archive_dir / f"{old_path.stem}_premerge_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
                shutil.copy2(str(old_path), str(backup_path))
                logger.info("Copie de sauvegarde de la note cible avant écrasement : %s", backup_path.name)

        # Écriture de la nouvelle fiche canonique
        write_concept_file(canonical_note, target_path)
        logger.info("Fiche canonique fusionnée écrite : %s (%s)", target_path.name, canonical_note.frontmatter.title)

        # Déplacement des anciens fichiers dans _Archive_Merged sans unlink()
        for old_path in [note_a_path, note_b_path]:
            if old_path.resolve() != target_path.resolve() and old_path.exists():
                archive_dest = archive_dir / old_path.name
                if archive_dest.exists():
                    archive_dest = archive_dir / f"{old_path.stem}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
                shutil.move(str(old_path), str(archive_dest))
                logger.info("Ancienne note archivée dans _Archive_Merged : %s -> %s", old_path.name, archive_dest.name)

        # 4. Nettoyage et synchronisation LanceDB (sans chargement bge-m3 si defer_vector_sync=True)
        try:
            self.vector_store.delete_by_slug(note_a_path.stem)
            self.vector_store.delete_by_slug(note_b_path.stem)
            if not defer_vector_sync:
                self.vector_store.index_concept_file(target_path)
        except Exception as v_exc:
            logger.warning("Avertissement synchronisation LanceDB lors de la fusion : %s", v_exc)

        # 5. Réécriture globale des wikilinks dans le coffre (Invariant 3)
        old_targets = [
            note_a.frontmatter.title,
            note_a_path.stem,
            note_b.frontmatter.title,
            note_b_path.stem,
        ]
        self.rewrite_vault_wikilinks(old_targets=old_targets, new_target=merge_decision.canonical_title)

        return target_path

    def _resolve_canonical_target(
        self,
        merge_decision: ConceptMergeSchema,
        note_a_path: Path,
        note_b_path: Path,
    ) -> Path:
        """
        Détermine le chemin de la fiche fusionnée à partir du slug proposé par le LLM (A7) :
        - slugification stricte (aucun '/', '\\' ni '..' possible) ;
        - chemin résolu obligatoirement sous 02_Concepts/ ;
        - une note existante hors de la paire n'est jamais écrasée : suffixe -2, -3, ...
        """
        concepts_dir = settings.CONCEPTS_DIR
        pair = {note_a_path.resolve(), note_b_path.resolve()}
        base_slug = safe_slug(
            merge_decision.canonical_slug or merge_decision.canonical_title,
            fallback=note_a_path.stem,
        )
        candidate_slug = base_slug
        counter = 2
        while True:
            target = resolve_within(concepts_dir, f"{candidate_slug}.md")
            if not target.exists() or target.resolve() in pair:
                return target
            candidate_slug = f"{base_slug}-{counter}"
            counter += 1

    def annotate_contradiction(
        self,
        older_note_path: Path,
        newer_note_title: str,
        explanation: str,
        date_str: str,
    ) -> None:
        """
        Injecte un callout Obsidian '> [!warning] Évolution d'Arbitrage' en haut du corps
        de l'ancienne note lorsqu'une décision plus récente contredit ou remplace un choix (Chantier 3).
        Invariant 2 : Idempotence stricte (ne duplique jamais si le callout pointe déjà vers la même fiche).
        """
        if not older_note_path.exists():
            return

        note = parse_concept_file(older_note_path)

        # Invariant 2 : Idempotence stricte
        target_link = f"[[{newer_note_title}]]"
        if target_link in note.body and "[!warning] Évolution d'Arbitrage" in note.body:
            logger.info("Callout d'évolution déjà présent dans %s vers %s. Ignoré.", older_note_path.name, newer_note_title)
            return

        callout = (
            f"> [!warning] Évolution d'Arbitrage (Mis à jour le {date_str})\n"
            f"> Ce choix architectural a évolué dans la note plus récente {target_link} : *{explanation.strip()}*."
        )

        note.body = f"{callout}\n\n{note.body.lstrip()}"
        note.frontmatter.updated_at = date_str

        write_concept_file(note, older_note_path)
        logger.info("Callout d'évolution d'arbitrage injecté dans : %s -> %s", older_note_path.name, newer_note_title)

    def rewrite_vault_wikilinks(self, old_targets: List[str], new_target: str) -> int:
        """
        Parcourt récursivement 01_Episodique/ et 02_Concepts/ (hors _Archive_Merged/)
        pour réécrire tous les liens wikilinks pointant vers les anciennes cibles.
        Gère les formes [[Titre]], [[slug]], et [[slug|Alias]] (Invariant 3).
        Retourne le nombre de fichiers modifiés.
        """
        clean_new = new_target.strip()
        if not clean_new:
            return 0

        # Filtre les anciennes cibles uniques et distinctes de new_target
        valid_olds = {
            t.strip()
            for t in old_targets
            if t and t.strip() and t.strip().lower() != clean_new.lower()
        }

        if not valid_olds:
            return 0

        updated_files_count = 0
        search_dirs = [settings.EPISODIC_DIR, settings.CONCEPTS_DIR]

        for s_dir in search_dirs:
            if not s_dir.exists():
                continue

            for md_file in s_dir.rglob("*.md"):
                # Exclure les dossiers d'archivage (fusions) et de quarantaine (Vault Doctor)
                if "_Archive_Merged" in md_file.parts or "_Quarantine" in md_file.parts:
                    continue

                try:
                    content = md_file.read_text(encoding="utf-8")
                    modified = False

                    for old in valid_olds:
                        pattern = re.compile(rf"\[\[{re.escape(old)}(\|[^\]]+)?\]\]", re.IGNORECASE)

                        def _replacer(m: re.Match) -> str:
                            alias = m.group(1) or ""
                            return f"[[{clean_new}{alias}]]"

                        new_content, count = pattern.subn(_replacer, content)
                        if count > 0:
                            content = new_content
                            modified = True

                    if modified:
                        md_file.write_text(content, encoding="utf-8")
                        updated_files_count += 1
                        logger.debug("Wikilinks mis à jour dans : %s", md_file.name)
                except Exception as exc:
                    logger.debug("Erreur lecture/écriture wikilinks %s : %s", md_file.name, exc)

        logger.info("%d fichier(s) mis à jour avec le nouveau wikilink [[%s]].", updated_files_count, clean_new)
        return updated_files_count

    def run_defragmentation_cycle(self) -> Dict[str, Any]:
        """Cycle de Sommeil Profond sous une session VRAM unique (C8) : aucun autre processus ne charge de modèle entre deux paires."""
        try:
            with llm_client.vram_session():
                return self._run_defragmentation_cycle()
        except VRAMBusyError as exc:
            logger.warning("Sommeil Profond reporté : %s", exc)
            return {"candidates_found": 0, "merges_done": 0, "contradictions_done": 0, "deferred": True}

    def _run_defragmentation_cycle(self) -> Dict[str, Any]:
        """
        Cycle autonome de Sommeil Profond :
        1. Trouve les candidats à la fusion et aux contradictions.
        2. Pour chaque candidat, demande la décision au modèle 26B (ou applique le schéma).
        3. Exécute les fusions ou les annotations de contradiction.
        """
        logger.info("=== DÉBUT CYCLE DE SOMMEIL PROFOND (DÉFRAGMENTATION DU GRAPHE) ===")
        candidates = self.find_merge_and_contradiction_candidates()

        merges_done = 0
        contradictions_done = 0
        merged_paths: List[Path] = []
        today_str = datetime.now().strftime("%Y-%m-%d")

        for cand in candidates:
            path_a: Path = cand["note_a"]
            path_b: Path = cand["note_b"]
            if not path_a.exists() or not path_b.exists():
                continue

            # Détermination de l'ancienneté relative
            note_a = parse_concept_file(path_a)
            note_b = parse_concept_file(path_b)
            older_path, newer_path = (path_a, path_b) if (note_a.frontmatter.created_at <= note_b.frontmatter.created_at) else (path_b, path_a)
            newer_title = parse_concept_file(newer_path).frontmatter.title

            if cand["type"] == "merge_candidate":
                # Évaluation LLM ou fusion directe
                decision = None
                if llm_client.is_alive():
                    prompt = (
                        f"Évalue ces deux fiches conceptuelles pour fusion ou contradiction :\n\n"
                        f"--- FICHE A ({path_a.name}) ---\n{note_a.frontmatter.title}\n{note_a.body[:MERGE_PROMPT_BODY_MAX_CHARS]}\n\n"
                        f"--- FICHE B ({path_b.name}) ---\n{note_b.frontmatter.title}\n{note_b.body[:MERGE_PROMPT_BODY_MAX_CHARS]}\n\n"
                        "Si tu fusionnes, merged_markdown_body doit conserver TOUS les faits, commandes et arbitrages "
                        "des deux fiches (aucune perte d'information).\n"
                        "Remplis le schéma ConceptMergeSchema :\n"
                        "- should_merge : vrai si elles traitent du même concept et sont redondantes.\n"
                        "- contradiction_detected : vrai si l'une remplace l'autre suite à un arbitrage technique."
                    )
                    try:
                        decision = llm_client.generate_structured(
                            prompt=prompt,
                            response_model=ConceptMergeSchema,
                            model=settings.MODEL_HEAVY_SYNTHESIS,
                            keep_alive="5m",  # 26B gardé entre deux paires (C3), déchargé une fois en sortie
                        )
                    except Exception as llm_exc:
                        logger.warning("Échec évaluation LLM pour fusion : %s", llm_exc)

                if decision and decision.should_merge:
                    target_p = self.merge_concepts_pair(path_a, path_b, decision, defer_vector_sync=True)
                    merged_paths.append(target_p)
                    merges_done += 1
                elif decision and decision.contradiction_detected and decision.contradiction_explanation:
                    self.annotate_contradiction(
                        older_note_path=older_path,
                        newer_note_title=newer_title,
                        explanation=decision.contradiction_explanation,
                        date_str=today_str,
                    )
                    contradictions_done += 1

            elif cand["type"] == "contradiction_candidate":
                # Vérification de contradiction
                if llm_client.is_alive():
                    prompt = (
                        f"Y a-t-il une contradiction ou une évolution d'arbitrage entre ces deux choix ?\n\n"
                        f"Choix 1 ({older_path.name}) : {parse_concept_file(older_path).body[:MERGE_PROMPT_BODY_MAX_CHARS // 2]}\n\n"
                        f"Choix 2 récent ({newer_path.name}) : {parse_concept_file(newer_path).body[:MERGE_PROMPT_BODY_MAX_CHARS // 2]}\n\n"
                        "Remplis ConceptMergeSchema (should_merge=False si fiches distinctes mais contradictoires)."
                    )
                    try:
                        dec = llm_client.generate_structured(
                            prompt=prompt,
                            response_model=ConceptMergeSchema,
                            model=settings.MODEL_HEAVY_SYNTHESIS,
                            keep_alive="5m",  # 26B gardé entre deux paires (C3), déchargé une fois en sortie
                        )
                        if dec and dec.contradiction_detected and dec.contradiction_explanation:
                            self.annotate_contradiction(
                                older_note_path=older_path,
                                newer_note_title=newer_title,
                                explanation=dec.contradiction_explanation,
                                date_str=today_str,
                            )
                            contradictions_done += 1
                    except Exception as exc:
                        logger.debug("Erreur analyse contradiction : %s", exc)

        # Exclusion mutuelle VRAM : déchargement du modèle 26B avant indexation bge-m3
        llm_client.unload_model(settings.MODEL_HEAVY_SYNTHESIS)

        # Indexation vectorielle différée des fiches fusionnées
        if merged_paths:
            logger.info("Synchronisation vectorielle différée de %d fiche(s) fusionnée(s)...", len(merged_paths))
            for p in merged_paths:
                try:
                    self.vector_store.index_concept_file(p)
                except Exception as idx_exc:
                    logger.warning("Erreur indexation vectorielle post-fusion pour %s : %s", p.name, idx_exc)

            llm_client.unload_model(settings.MODEL_EMBEDDING)

        logger.info(
            "=== FIN CYCLE DE SOMMEIL PROFOND : %d fusion(s), %d contradiction(s) annotée(s) ===",
            merges_done,
            contradictions_done,
        )
        return {
            "candidates_found": len(candidates),
            "merges_done": merges_done,
            "contradictions_done": contradictions_done,
        }

