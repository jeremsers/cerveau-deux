"""
Moteur GraphRAG Hybride Multi-Sauts pour l'Exocortex et la Télémétrie Cognitive.
Combine la recherche vectorielle k-NN (Hop 0) avec une traversée de graphe (Hop 1)
sur les [[wikilinks]] d'Obsidian et les sessions épisodiques SQLite.
Garantit une exclusion VRAM stricte (0 Mo résiduel) via déchargement immédiat de bge-m3.
"""

from __future__ import annotations

import logging
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.config import settings
from src.database.db_manager import DBManager
from src.database.vector_store import VectorStore, vector_store
from src.llm.ollama_client import llm_client
from src.utils.markdown_io import ParsedConceptNote, parse_concept_file

logger = logging.getLogger("Exocortex.GraphRAG")


# ==============================================================================
# UTILITAIRE D'EXTRACTION DE WIKILINKS
# ==============================================================================

def extract_wikilinks(text: str) -> List[str]:
    """
    Extrait la liste dédupliquée et ordonnée de toutes les cibles de wikilinks
    présentes dans le texte. Gère les formats :
    - [[Cible]]
    - [[Cible|Alias]]
    - [[Cible#Section]]
    - [[Cible#Section|Alias]]
    """
    if not text:
        return []

    # Regex capturant la cible avant une éventuelle ancre # ou un alias |
    pattern = r"\[\[([^\]|\r\n#]+)(?:#[^\]|\r\n]+)?(?:\|[^\]\r\n]+)?\]\]"
    matches = re.findall(pattern, text)
    seen: Set[str] = set()
    results: List[str] = []

    for m in matches:
        target = m.strip()
        if target and target.lower() not in seen:
            seen.add(target.lower())
            results.append(target)

    return results


# ==============================================================================
# MOTEUR GRAPHRAG HYBRIDE
# ==============================================================================

class HybridGraphRAG:
    """
    Moteur de recherche hybride combinant similarité sémantique vectorielle (Hop 0),
    traversée de liens de graphe Obsidian (Hop 1) et enrichissement épisodique SQLite.
    """

    def __init__(
        self,
        db_manager: Optional[DBManager] = None,
        store: Optional[VectorStore] = None,
        concepts_dir: Optional[Path] = None,
    ) -> None:
        self.db = db_manager or DBManager(read_only=True)
        self.vector_store = store or vector_store
        self.concepts_dir = concepts_dir or settings.CONCEPTS_DIR
        self._concept_index: Dict[str, Path] = {}
        self._concept_metadata: Dict[str, Dict[str, Any]] = {}
        self._last_index_scan = 0.0

    def refresh_index(self, force: bool = False) -> int:
        """
        Construit ou actualise l'index en mémoire des fiches conceptuelles de settings.CONCEPTS_DIR
        pour résoudre instantanément les wikilinks sans I/O disque répétées.
        """
        target_dir = self.concepts_dir or settings.CONCEPTS_DIR
        if not target_dir.exists():
            self._concept_index = {}
            self._concept_metadata = {}
            return 0

        # Vérification simple de modification pour éviter de réindexer inutilement
        try:
            latest_mtime = max(
                (f.stat().st_mtime for f in target_dir.glob("*.md")),
                default=0.0,
            )
        except Exception:
            latest_mtime = 0.0

        if not force and self._concept_index and latest_mtime <= self._last_index_scan:
            return len(self._concept_index)

        index_map: Dict[str, Path] = {}
        meta_map: Dict[str, Dict[str, Any]] = {}

        for p in target_dir.glob("*.md"):
            if p.name.startswith("all-") or p.name.startswith("."):
                continue

            slug = p.stem.strip()
            index_map[slug.lower()] = p

            try:
                note = parse_concept_file(p)
                title = note.frontmatter.title.strip() if note.frontmatter.title else slug
                index_map[title.lower()] = p

                meta_map[slug.lower()] = {
                    "slug": slug,
                    "title": title,
                    "semantic_topic": note.frontmatter.semantic_topic,
                    "session_id": note.frontmatter.session_id,
                    "tags": note.frontmatter.tags,
                    "summary": note.frontmatter.summary_1_line,
                    "file_path": p,
                }
            except Exception as exc:
                logger.debug("Erreur lecture pré-index pour %s : %s", p.name, exc)
                meta_map[slug.lower()] = {
                    "slug": slug,
                    "title": slug.replace("-", " ").title(),
                    "semantic_topic": "General",
                    "session_id": None,
                    "tags": [],
                    "summary": "",
                    "file_path": p,
                }

        self._concept_index = index_map
        self._concept_metadata = meta_map
        self._last_index_scan = latest_mtime
        return len(self._concept_index)

    def resolve_wikilink_to_path(self, target: str) -> Optional[Path]:
        """
        Résout une cible de wikilink vers son chemin de fichier réel dans le coffre.
        Recherche par titre insensible à la casse, slug exact, ou variantes tirets/espaces.
        """
        if not self._concept_index:
            self.refresh_index()

        cleaned = target.strip()
        cleaned_lower = cleaned.lower()

        # 1. Correspondance directe (slug ou title)
        if cleaned_lower in self._concept_index:
            p = self._concept_index[cleaned_lower]
            if p.exists():
                return p

        # 2. Variante : remplacement des espaces par des tirets
        slug_hyphen = re.sub(r"[\s_]+", "-", cleaned_lower)
        if slug_hyphen in self._concept_index:
            p = self._concept_index[slug_hyphen]
            if p.exists():
                return p

        # 3. Variante : remplacement des tirets par des espaces
        slug_space = cleaned_lower.replace("-", " ")
        if slug_space in self._concept_index:
            p = self._concept_index[slug_space]
            if p.exists():
                return p

        # 4. Repli direct sur le système de fichiers si non présent dans l'index
        target_dir = self.concepts_dir or settings.CONCEPTS_DIR
        candidate = target_dir / f"{slug_hyphen}.md"
        if candidate.exists():
            self._concept_index[cleaned_lower] = candidate
            return candidate

        return None

    def _compute_lexical_overlap(self, query_tokens: Set[str], text: str) -> float:
        """Calcule un ratio simple de recouvrement lexical CPU entre la requête et un texte."""
        if not query_tokens or not text:
            return 0.0
        text_tokens = set(re.findall(r"\b\w{3,}\b", text.lower()))
        if not text_tokens:
            return 0.0
        common = query_tokens.intersection(text_tokens)
        return len(common) / math.sqrt(len(query_tokens) * len(text_tokens))

    def search_hybrid(
        self,
        query: str,
        top_k: int = 3,
        neighbor_k: int = 3,
        topic_filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Recherche GraphRAG hybride multi-sauts :
        1. Hop 0 : Recherche vectorielle sémantique k-NN (déchargement VRAM immédiat).
        2. Hop 1 : Traversée des [[wikilinks]] des fiches Hop 0 résolues via l'index RAM.
        3. Déduplication stricte : aucun nœud primaire ne peut apparaître dans les voisins liés.
        4. Traversée Épisodique : récupération SQLite des résumés de sessions rattachées.
        """
        self.refresh_index()

        query_clean = query.strip()
        query_tokens = set(re.findall(r"\b\w{3,}\b", query_clean.lower()))

        # ----------------------------------------------------------------------
        # 1. ANCRAGE VECTORIEL (HOP 0)
        # ----------------------------------------------------------------------
        raw_vector_results: List[Dict[str, Any]] = []
        try:
            # On demande un peu plus si un filtre par topic est actif
            search_limit = top_k * 3 if topic_filter else top_k
            if self.vector_store and self.vector_store.count() > 0:
                raw_vector_results = self.vector_store.search(query_clean, top_k=search_limit)
        except Exception as exc:
            logger.warning("Échec de la recherche vectorielle LanceDB : %s", exc)
        finally:
            # Exclusion VRAM stricte garantie (0 Mo résiduel)
            try:
                llm_client.unload_model(settings.MODEL_EMBEDDING)
            except Exception:
                pass

        # Filtrage optionnel par topic
        primary_results = []
        for r in raw_vector_results:
            if topic_filter:
                r_topic = str(r.get("semantic_topic") or "").lower()
                if r_topic != topic_filter.strip().lower():
                    continue
            primary_results.append(r)
            if len(primary_results) >= top_k:
                break

        # Fallback de recherche lexicale CPU si LanceDB est vide ou hors-ligne
        if not primary_results and self._concept_metadata:
            scored_candidates = []
            for meta in self._concept_metadata.values():
                if topic_filter and str(meta.get("semantic_topic", "")).lower() != topic_filter.strip().lower():
                    continue
                content_sample = f"{meta['title']} {meta.get('summary', '')} {' '.join(meta.get('tags', []))}"
                score = self._compute_lexical_overlap(query_tokens, content_sample)
                if score > 0.05:
                    scored_candidates.append((score, meta))

            scored_candidates.sort(key=lambda x: x[0], reverse=True)
            for sc, meta in scored_candidates[:top_k]:
                p = meta["file_path"]
                try:
                    note = parse_concept_file(p)
                    content = note.body
                except Exception:
                    content = ""
                primary_results.append({
                    "id": meta["slug"],
                    "title": meta["title"],
                    "slug": meta["slug"],
                    "semantic_topic": meta["semantic_topic"],
                    "file_path": str(p.resolve()),
                    "content": content,
                    "score": 1.0 - sc,  # pseudo distance
                })

        # Assemblage des nœuds primaires (Hop 0)
        primary_nodes: List[Dict[str, Any]] = []
        primary_slugs: Set[str] = set()
        primary_paths: Set[str] = set()
        extracted_hop0_wikilinks: List[Tuple[str, float]] = []  # (target, parent_score)

        for r in primary_results:
            slug = r.get("slug") or Path(r.get("file_path", "")).stem
            norm_slug = slug.strip().lower()
            if norm_slug in primary_slugs:
                continue
            primary_slugs.add(norm_slug)

            fpath_str = r.get("file_path")
            fpath = Path(fpath_str) if fpath_str else self.resolve_wikilink_to_path(slug)
            if fpath and fpath.exists():
                primary_paths.add(str(fpath.resolve()).lower())

            # Chargement de la note complète
            note_obj: Optional[ParsedConceptNote] = None
            if fpath and fpath.exists():
                try:
                    note_obj = parse_concept_file(fpath)
                except Exception:
                    pass

            dist = float(r.get("score", 1.0))
            sim_pct = max(0, min(100, int((1.0 - (dist / 2.0)) * 100))) if dist <= 2.0 else 50

            title = note_obj.frontmatter.title if (note_obj and note_obj.frontmatter.title) else (r.get("title") or slug)
            topic = note_obj.frontmatter.semantic_topic if note_obj else (r.get("semantic_topic") or "General")
            session_id = note_obj.frontmatter.session_id if note_obj else None
            body_content = note_obj.body if note_obj else r.get("content", "")

            # Extraction des wikilinks Hop 1 depuis le corps et la télémétrie
            raw_links: List[str] = []
            if note_obj:
                raw_links.extend(extract_wikilinks(note_obj.body))
                telemetry_str = "\n".join(note_obj.telemetry_lines)
                raw_links.extend(extract_wikilinks(telemetry_str))
            else:
                raw_links.extend(extract_wikilinks(body_content))

            for link_target in raw_links:
                extracted_hop0_wikilinks.append((link_target, sim_pct / 100.0))

            primary_nodes.append({
                "slug": slug,
                "title": title,
                "semantic_topic": topic,
                "session_id": session_id,
                "file_path": str(fpath.resolve()) if fpath else "",
                "similarity_pct": sim_pct,
                "excerpt": body_content[:600].strip(),
                "hop": 0,
            })

        # ----------------------------------------------------------------------
        # 2. TRAVERSÉE DES WIKILINKS (HOP 1 - GRAPH OBSIDIAN)
        # ----------------------------------------------------------------------
        candidate_neighbors: Dict[str, Dict[str, Any]] = {}

        for target_str, parent_weight in extracted_hop0_wikilinks:
            resolved_p = self.resolve_wikilink_to_path(target_str)
            if not resolved_p or not resolved_p.exists():
                continue

            resolved_path_norm = str(resolved_p.resolve()).lower()
            resolved_slug_norm = resolved_p.stem.strip().lower()

            # DÉDUPLICATION STRICTE : Un nœud présent dans Hop 0 ne doit jamais être dans Hop 1
            if resolved_slug_norm in primary_slugs or resolved_path_norm in primary_paths:
                continue

            if resolved_slug_norm in candidate_neighbors:
                # Renforcement du score si pointé par plusieurs parents de Hop 0
                candidate_neighbors[resolved_slug_norm]["score"] += (parent_weight * 0.3)
                continue

            # Parsing de la note voisine
            try:
                neighbor_note = parse_concept_file(resolved_p)
                nb_title = neighbor_note.frontmatter.title or resolved_p.stem.replace("-", " ").title()
                nb_topic = neighbor_note.frontmatter.semantic_topic
                nb_body = neighbor_note.body
                nb_session_id = neighbor_note.frontmatter.session_id
            except Exception:
                nb_title = resolved_p.stem.replace("-", " ").title()
                nb_topic = "General"
                nb_body = ""
                nb_session_id = None

            # Score hybride : parent_weight + recouvrement lexical direct avec la requête
            lexical_score = self._compute_lexical_overlap(query_tokens, f"{nb_title} {nb_body[:500]}")
            total_neighbor_score = (parent_weight * 0.5) + (lexical_score * 0.5)

            candidate_neighbors[resolved_slug_norm] = {
                "slug": resolved_p.stem,
                "title": nb_title,
                "semantic_topic": nb_topic,
                "session_id": nb_session_id,
                "file_path": str(resolved_p.resolve()),
                "score": total_neighbor_score,
                "excerpt": nb_body[:400].strip(),
                "hop": 1,
            }

        sorted_neighbors = sorted(
            candidate_neighbors.values(),
            key=lambda x: x["score"],
            reverse=True,
        )
        linked_neighbors = sorted_neighbors[:neighbor_k]

        # ----------------------------------------------------------------------
        # 3. TRAVERSÉE ÉPISODIQUE SQLITE
        # ----------------------------------------------------------------------
        episodic_traces: List[Dict[str, Any]] = []
        seen_sessions: Set[str] = set()

        # Collecte des session_id des nœuds Hop 0 et Hop 1
        all_sids = [
            n["session_id"] for n in (primary_nodes + linked_neighbors) if n.get("session_id")
        ]

        for sid in all_sids:
            if not sid or sid in seen_sessions:
                continue
            seen_sessions.add(sid)

            sess_record = self.db.get_chat_session_by_id(sid)
            if sess_record:
                episodic_traces.append({
                    "session_id": sid,
                    "timestamp_start": str(sess_record.get("timestamp_start", "")),
                    "turn_count": sess_record.get("turn_count", 0),
                    "user_char_count": sess_record.get("user_char_count", 0),
                    "summary": sess_record.get("summary", ""),
                    "distillation_status": sess_record.get("distillation_status", "success"),
                })

        return {
            "query": query,
            "primary_nodes": primary_nodes,
            "linked_neighbors": linked_neighbors,
            "episodic_traces": episodic_traces,
        }

