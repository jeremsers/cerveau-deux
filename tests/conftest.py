"""
Fixtures partagées des suites de vérification (v0.5.1+).

Barrière d'hermétisme (v0.5.6, F1) : AVANT tout import de `src`, le coffre, le dossier Takeout,
Ollama et la clé Gemini sont redirigés vers des valeurs de test. `src.config` lisant ces variables
à l'import (et le fichier .env ne remplaçant jamais une variable déjà définie), aucun test ne
peut plus lire ni modifier le vrai coffre, la vraie base, ni appeler un modèle réel — y compris
les singletons créés à l'import (kanban_engine, vector_store).

`exo_env` isole en plus chaque test dans son propre coffre sous tmp_path.
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest.mock as mock
from dataclasses import dataclass
from pathlib import Path

_SESSION_SANDBOX = Path(tempfile.mkdtemp(prefix="exocortex-tests-"))
os.environ["VAULT_ROOT"] = str(_SESSION_SANDBOX / "Vault_Data")
os.environ["TAKEOUT_DIR"] = str(_SESSION_SANDBOX / "takeout_raw")
os.environ["MODELS_DIR"] = str(_SESSION_SANDBOX / "models")
os.environ["OLLAMA_BASE_URL"] = os.environ.get("EXOCORTEX_TEST_OLLAMA_URL", "http://127.0.0.1:9")
os.environ["LLM_BACKEND"] = "ollama"
os.environ["GEMINI_API_KEY"] = ""
os.environ["TAKEOUT_MODE"] = "web_manual"

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest

from src.config import settings
from src.database.db_manager import DBManager


_REAL_VAULT = (_ROOT / "Vault_Data").resolve()


def pytest_sessionstart(session: pytest.Session) -> None:
    """Garde-fou : refuse de lancer la suite si la configuration pointe vers le vrai coffre."""
    from src.config import settings

    if settings.VAULT_ROOT.resolve() == _REAL_VAULT or settings.DB_PATH.resolve().is_relative_to(_REAL_VAULT):
        pytest.exit("Suite de tests pointée vers le vrai coffre Vault_Data : arrêt (F1).", returncode=2)


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
