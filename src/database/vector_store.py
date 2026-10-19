"""
Wrapper LanceDB pour l'Exocortex et la Télémétrie Cognitive.
Gère l'indexation vectorielle k-NN locale et multilingue via le modèle d'embedding bge-m3 (1024 dim),
avec exclusion mutuelle stricte en VRAM (keep_alive=0).
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import lancedb
import pyarrow as pa
from pydantic import BaseModel, Field

from src.config import settings
from src.llm.ollama_client import llm_client

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

    def get_embedding(self, text: str) -> List[float]:
        """
        Génère un vecteur d'embedding 1024-dim réel via bge-m3.
        Lève une RuntimeError si le modèle d'embedding est injoignable (interdiction des vecteurs SHA-256 factices).
        """
        clean_text = re.sub(r"\s+", " ", text).strip()[:2048]
        vec = llm_client.generate_embeddings(
            text=clean_text,
            model=settings.MODEL_EMBEDDING,
            keep_alive=0,
        )
        if not vec or len(vec) != EMBEDDING_DIM:
            raise RuntimeError(
                f"Échec critique d'embedding : dimension reçue {len(vec) if vec else 0} != {EMBEDDING_DIM}. "
                f"Vérifiez qu'Ollama est actif et que '{settings.MODEL_EMBEDDING}' est installé."
            )
        return [float(x) for x in vec]

    def index_concept_file(self, file_path: Path) -> bool:
        """Lit, parse le frontmatter et vectorise une note Markdown de 02_Concepts/."""
        if not file_path.exists() or file_path.suffix.lower() != ".md":
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            # Extraction YAML simple
            m_yaml = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw_text, re.DOTALL)
            frontmatter: Dict[str, Any] = {}
            body_content = raw_text

            if m_yaml:
                yaml_block = m_yaml.group(1)
                body_content = m_yaml.group(2).strip()
                for line in yaml_block.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        frontmatter[k.strip()] = v.strip().strip("'\"")

            doc_id = frontmatter.get("id") or file_path.stem
            title = frontmatter.get("title") or file_path.stem.replace("-", " ").title()
            topic = frontmatter.get("semantic_topic") or "General"
            created_at = frontmatter.get("created_at") or ""
            tags = frontmatter.get("tags") or "[]"

            # Texte à vectoriser : Titre + Sujet + Résumé / Contenu
            text_to_embed = f"Titre: {title}\nSujet: {topic}\nContenu:\n{body_content[:1500]}"
            vector = self.get_embedding(text_to_embed)

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

            # Suppression de l'ancienne version si existante puis ajout
            try:
                self._table.delete(f'id = "{doc_id}"')
            except Exception:
                pass

            self._table.add([record])
            logger.info("Note '%s' indexée avec succès dans LanceDB.", file_path.name)
            return True
        except Exception as exc:
            logger.error("Échec d'indexation de la note '%s' : %s", file_path.name, exc)
            return False

    def sync_all_concepts(self, concepts_dir: Optional[Path] = None) -> int:
        """Parcourt 02_Concepts/ et synchronise toutes les notes Markdown dans LanceDB."""
        target_dir = concepts_dir or settings.CONCEPTS_DIR
        if not target_dir.exists():
            return 0

        indexed_count = 0
        for md_file in target_dir.glob("*.md"):
            if self.index_concept_file(md_file):
                indexed_count += 1

        # Purge de la mémoire VRAM après le batch d'embeddings
        llm_client.unload_model(settings.MODEL_EMBEDDING)
        logger.info("Synchronisation LanceDB achevée : %d notes indexées.", indexed_count)
        return indexed_count

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

