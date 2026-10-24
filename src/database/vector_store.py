"""
Wrapper LanceDB pour l'Exocortex et la Télémétrie Cognitive.
Gère l'indexation vectorielle k-NN locale et multilingue via le modèle d'embedding bge-m3 (1024 dim),
avec exclusion mutuelle stricte en VRAM (keep_alive=0).
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import lancedb
import pyarrow as pa
from pydantic import BaseModel, Field

from src.config import settings
from src.llm.ollama_client import llm_client
from src.utils.markdown_io import parse_concept_file

logger = logging.getLogger("Exocortex.VectorStore")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

# Dimension vectorielle native de BAAI/bge-m3
EMBEDDING_DIM = 1024


class ConceptDocument(BaseModel):
    """Document conceptuel normalisé pour l'indexation vectorielle."""
    id: str
    title: str
    slug: str
    semantic_topic: str
    tags: str = "[]"  # JSON list
    created_at: str
    file_path: str
    content: str
    vector: Optional[List[float]] = None


class VectorStore:
    """Wrapper LanceDB embarqué haute performance pour le coffre Exocortex."""

    def __init__(self, store_dir: Optional[Path] = None) -> None:
        self.store_dir = store_dir or settings.LANCEDB_DIR
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.table_name = "concepts"
        self._db = lancedb.connect(str(self.store_dir))
        self._table = None
        self._init_table()

    def _get_schema(self) -> pa.Schema:
        """Définit le schéma PyArrow pour la table de documents vectorisés."""
        return pa.schema([
            pa.field("id", pa.string()),
            pa.field("title", pa.string()),
            pa.field("slug", pa.string()),
            pa.field("semantic_topic", pa.string()),
            pa.field("tags", pa.string()),
            pa.field("created_at", pa.string()),
            pa.field("file_path", pa.string()),
            pa.field("content", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), EMBEDDING_DIM)),
        ])

    def _init_table(self) -> None:
        """Ouvre la table existante ou l'initialise avec le schéma adéquat."""
        try:
            if self.table_name in self._db.table_names():
                self._table = self._db.open_table(self.table_name)
                logger.info("Table vectorielle LanceDB '%s' chargée avec succès.", self.table_name)
            else:
                self._table = self._db.create_table(
                    self.table_name,
                    schema=self._get_schema(),
                    mode="create",
                )
                logger.info("Table vectorielle LanceDB '%s' créée avec succès.", self.table_name)
        except Exception as exc:
            logger.error("Erreur d'initialisation de la table LanceDB : %s", exc)
            raise

    def get_embedding(self, text: str, keep_alive: Union[int, str] = 0) -> List[float]:
        """
        Génère un vecteur d'embedding 1024-dim réel via bge-m3.
        Lève une RuntimeError si le modèle d'embedding est injoignable (interdiction des vecteurs SHA-256 factices).
        """
        clean_text = re.sub(r"\s+", " ", text).strip()[:2048]
        vec = llm_client.generate_embeddings(
            text=clean_text,
            model=settings.MODEL_EMBEDDING,
            keep_alive=keep_alive,
        )
        if not vec or len(vec) != EMBEDDING_DIM:
            raise RuntimeError(
                f"Échec critique d'embedding : dimension reçue {len(vec) if vec else 0} != {EMBEDDING_DIM}. "
                f"Vérifiez qu'Ollama est actif et que '{settings.MODEL_EMBEDDING}' est installé."
            )
        return [float(x) for x in vec]

    def index_concept_file(self, file_path: Path, keep_alive: Union[int, str] = 0) -> bool:
        """Lit, parse le frontmatter et vectorise une note Markdown de 02_Concepts/."""
        if not file_path.exists() or file_path.suffix.lower() != ".md":
            return False

        try:
            note = parse_concept_file(file_path)
            fm = note.frontmatter
            body_content = note.body

            raw_id = fm.id
            if raw_id and raw_id != file_path.stem:
                doc_id = f"{raw_id}_{file_path.stem[:32]}"
            else:
                doc_id = file_path.stem

            title = fm.title or file_path.stem.replace("-", " ").title()
            topic = fm.semantic_topic or "General"
            created_at = fm.created_at or ""
            tags = json.dumps(fm.tags, ensure_ascii=False) if isinstance(fm.tags, list) else str(fm.tags)

            # Texte à vectoriser : Titre + Sujet + Résumé / Contenu
            text_to_embed = f"Titre: {title}\nSujet: {topic}\nContenu:\n{body_content[:1500]}"
            vector = self.get_embedding(text_to_embed, keep_alive=keep_alive)

            record = {
                "id": str(doc_id),
                "title": str(title),
                "slug": file_path.stem,
                "semantic_topic": str(topic),
                "tags": str(tags),
                "created_at": str(created_at),
                "file_path": str(file_path.resolve()),
                "content": body_content,
                "vector": vector,
            }

            # Suppression préalable ciblée par slug unique (évite d'écraser une note tierce ayant le même timestamp minute)
            try:
                safe_slug = str(file_path.stem).replace("'", "''")
                self._table.delete(f"slug = '{safe_slug}'")
            except Exception:
                pass

            self._table.add([record])
            logger.debug("Note '%s' indexée avec succès dans LanceDB.", file_path.name)
            return True
        except Exception as exc:
            logger.error("Échec d'indexation de la note '%s' : %s", file_path.name, exc)
            return False

    def delete_by_slug(self, slug: str) -> bool:
        """Supprime une note de la table vectorielle LanceDB par son slug ou son id."""
        try:
            safe_slug = str(slug).replace("'", "''")
            self._table.delete(f"slug = '{safe_slug}' OR id = '{safe_slug}'")
            logger.debug("Document '%s' supprimé de LanceDB.", slug)
            return True
        except Exception as exc:
            logger.warning("Erreur suppression LanceDB pour slug '%s': %s", slug, exc)
            return False

    @property
    def sync_state_path(self) -> Path:
        """Empreintes des fiches déjà indexées (slug -> sha1 du fichier), hors du dossier LanceDB."""
        return self.store_dir.parent / f"{self.store_dir.name}_sync_state.json"

    def _load_sync_state(self) -> Optional[Dict[str, str]]:
        try:
            data = json.loads(self.sync_state_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else None
        except (FileNotFoundError, ValueError):
            return None

    def _indexed_slugs(self) -> set:
        try:
            return set(self._table.to_arrow().column("slug").to_pylist())
        except Exception:
            return set()

    def sync_all_concepts(self, concepts_dir: Optional[Path] = None) -> int:
        """
        Synchronise 02_Concepts/ dans LanceDB de façon incrémentale (v0.5.7, C11) :
        - seules les fiches nouvelles ou modifiées (empreinte sha1 du fichier) sont ré-embarquées,
          au lieu de tout le coffre chaque nuit ;
        - les fiches disparues (fusionnées, mises en quarantaine, supprimées) sont retirées ;
        - les fichiers agrégés `all-*` ne sont pas indexés ;
        - la table est compactée après modification.
        Retourne le nombre de fiches (ré)indexées lors de cet appel.
        """
        from tqdm import tqdm

        target_dir = concepts_dir or settings.CONCEPTS_DIR
        if not target_dir.exists():
            return 0

        md_files = sorted(
            f for f in target_dir.glob("*.md") if not f.name.startswith(("all-", "all_", "."))
        )
        previous = self._load_sync_state()
        state: Dict[str, str] = dict(previous or {})
        on_disk = {f.stem: f for f in md_files}

        # Fiches disparues : retirées de l'index (au premier passage, toute ligne orpheline de la table)
        known = set(state) if previous is not None else self._indexed_slugs()
        removed = [slug for slug in known if slug not in on_disk]
        for slug in removed:
            self.delete_by_slug(slug)
            state.pop(slug, None)

        to_index = []
        for md_file in md_files:
            digest = hashlib.sha1(md_file.read_bytes()).hexdigest()
            if state.get(md_file.stem) != digest:
                to_index.append((md_file, digest))

        indexed_count = 0
        if to_index:
            with tqdm(total=len(to_index), desc="Indexation LanceDB (bge-m3)", unit="note") as pbar:
                for md_file, digest in to_index:
                    if self.index_concept_file(md_file, keep_alive="5m"):
                        state[md_file.stem] = digest
                        indexed_count += 1
                    pbar.update(1)
            # Purge de la mémoire VRAM après le batch d'embeddings
            llm_client.unload_model(settings.MODEL_EMBEDDING)

        if to_index or removed:
            self._compact()
        self.sync_state_path.parent.mkdir(parents=True, exist_ok=True)
        self.sync_state_path.write_text(json.dumps(state, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        logger.info(
            "Synchronisation LanceDB : %d fiche(s) (ré)indexée(s), %d retirée(s), %d inchangée(s).",
            indexed_count, len(removed), len(md_files) - len(to_index),
        )
        return indexed_count

    def _compact(self) -> None:
        """Compacte la table (fragments créés par les delete + add successifs)."""
        try:
            if hasattr(self._table, "optimize"):
                self._table.optimize()
            elif hasattr(self._table, "compact_files"):
                self._table.compact_files()
        except Exception as exc:
            logger.debug("Compaction LanceDB ignorée : %s", exc)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Recherche sémantique k-NN dans LanceDB à partir d'un prompt utilisateur."""
        if self._table is None or self.count() == 0:
            logger.info("Table LanceDB vide ou non initialisée.")
            return []

        query_vector = self.get_embedding(query)
        # Purge de la VRAM après encodage de la requête
        llm_client.unload_model(settings.MODEL_EMBEDDING)

        try:
            results = (
                self._table.search(query_vector)
                .limit(top_k)
                .to_list()
            )
            # Nettoyage des résultats pour l'affichage / injection
            cleaned = []
            for r in results:
                cleaned.append({
                    "id": r.get("id"),
                    "title": r.get("title"),
                    "slug": r.get("slug"),
                    "semantic_topic": r.get("semantic_topic"),
                    "file_path": r.get("file_path"),
                    "content": r.get("content", ""),
                    "score": r.get("_distance", 0.0),
                })
            return cleaned
        except Exception as exc:
            logger.error("Erreur lors de la recherche vectorielle : %s", exc)
            return []

    def count(self) -> int:
        """Retourne le nombre total de documents indexés."""
        try:
            return len(self._table) if self._table is not None else 0
        except Exception:
            return 0


# Instance globale
vector_store = VectorStore()

