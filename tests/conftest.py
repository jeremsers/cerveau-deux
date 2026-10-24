"""
Fixtures partagées des suites de vérification (v0.5.1+).
`exo_env` isole complètement un test : coffre, base SQLite et LanceDB sous tmp_path,
singletons (kanban_engine, vector_store) redirigés, Ollama considéré hors ligne.
"""

from __future__ import annotations

import sys
import unittest.mock as mock
from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest

from src.config import settings
from src.database.db_manager import DBManager


@dataclass
class ExoEnv:
    db: DBManager
    vault_root: Path
    tmp_path: Path

    @property
    def concepts_dir(self) -> Path:
        return settings.CONCEPTS_DIR

    @property
    def episodic_dir(self) -> Path:
        return settings.EPISODIC_DIR


@pytest.fixture
def exo_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ExoEnv:
    """Coffre et base temporaires ; aucune écriture possible dans les données réelles."""
    vault_root = tmp_path / "Vault_Data"
    monkeypatch.setattr(settings, "VAULT_ROOT", vault_root)
    monkeypatch.setattr(settings, "TAKEOUT_DIR", tmp_path / "takeout_raw")
    settings.ensure_directories()

    db = DBManager(db_path=settings.DB_PATH)

    from src.consolidators.kanban_engine import kanban_engine
    from src.database.vector_store import vector_store
    from src.llm.ollama_client import llm_client

    monkeypatch.setattr(kanban_engine, "db", db)
    for method in ("delete_by_slug", "index_concept_file"):
        monkeypatch.setattr(vector_store, method, mock.MagicMock(return_value=True))
    monkeypatch.setattr(vector_store, "sync_all_concepts", mock.MagicMock(return_value=0))
    monkeypatch.setattr(llm_client, "is_alive", mock.MagicMock(return_value=False))
    monkeypatch.setattr(llm_client, "unload_model", mock.MagicMock(return_value=True))
    monkeypatch.setattr(llm_client, "unload_all_models", mock.MagicMock(return_value=None))

    return ExoEnv(db=db, vault_root=vault_root, tmp_path=tmp_path)
