"""
Suite de vérification v0.5.7 — Lot 7 : inférence, VRAM et performance (audit C1 à C12).
"""

from __future__ import annotations

import json
import multiprocessing
import os
import sys
import time
import unittest.mock as mock
from datetime import datetime, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest

from src.config import settings
from src.llm import ollama_client as oc
from src.llm.ollama_client import HardwareProbe, HybridLLMClient, VRAMBusyError, llm_client


class _Resp:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status_code = status

    def json(self):
        return self._payload

    def raise_for_status(self):
        pass


def _client_capturing(monkeypatch, capabilities=None):
    """Client dont les appels HTTP sont capturés ; /api/show renvoie les capacités données."""
    client = HybridLLMClient()
    sent = []

    def fake_post(url, json=None, timeout=None):
        sent.append((url, json))
        if url.endswith("/api/show"):
            return _Resp({"capabilities": capabilities or []})
        if url.endswith("/api/chat"):
            return _Resp({"message": {"content": '{"ok": true}'}})
        return _Resp({})

    monkeypatch.setattr(client._session, "post", fake_post)
    monkeypatch.setattr(client, "is_alive", lambda timeout=0.5: True)
    monkeypatch.setattr(client, "check_and_select_model", lambda m: m)
    return client, sent


# ==============================================================================
# C1 — Configuration du serveur Ollama
# ==============================================================================

def test_c1_server_env_is_read_from_the_ollama_process():
    def proc(pid, name, cmdline, env):
        p = mock.MagicMock()
        p.info = {"pid": pid, "name": name, "cmdline": cmdline}
        p.environ.return_value = env
        return p

    good = {"OLLAMA_FLASH_ATTENTION": "1", "OLLAMA_KV_CACHE_TYPE": "q8_0", "OLLAMA_MAX_LOADED_MODELS": "1", "OLLAMA_NUM_PARALLEL": "1"}
    with mock.patch("psutil.process_iter", return_value=[proc(1, "python.exe", ["x"], {}), proc(42, "ollama.exe", ["ollama", "serve"], good)]):
        assert llm_client.check_ollama_server_config() == {"found": True, "missing": {}, "pid": 42}
    with mock.patch("psutil.process_iter", return_value=[proc(42, "ollama.exe", ["ollama", "serve"], {"OLLAMA_FLASH_ATTENTION": "1"})]):
        report = llm_client.check_ollama_server_config()
    assert report["missing"]["OLLAMA_KV_CACHE_TYPE"] == "q8_0"
    bat = (_ROOT / "start_exocortex.bat").read_text(encoding="cp1252")
    assert "\nset OLLAMA_" not in bat.replace("\r\n", "\n")


# ==============================================================================
# C2 / C4 — num_ctx constant, thinking explicite
# ==============================================================================

class _Answer(oc.BaseModel):
    ok: bool


def test_c2_every_request_sends_the_same_num_ctx(monkeypatch):
    client, sent = _client_capturing(monkeypatch)
    image = settings.SYSTEM_BUFFER_DIR / "c2.webp"
    image.parent.mkdir(parents=True, exist_ok=True)
    image.write_bytes(b"x")

    client.generate_text("p", model="m")
    client.generate_vision("p", image, model="m")
    client.generate_structured("p", _Answer, model="m", enable_thinking=False)
    ctxs = [payload["options"]["num_ctx"] for url, payload in sent if url.endswith("/api/chat")]
    assert ctxs == [settings.OLLAMA_NUM_CTX] * 3


def test_c4_thinking_requested_explicitly_when_supported(monkeypatch):
    client, sent = _client_capturing(monkeypatch, capabilities=["completion", "thinking"])
    client.generate_structured("p", _Answer, model="m", enable_thinking=True)
    assert [p.get("think") for u, p in sent if u.endswith("/api/chat")] == [True]

    client, sent = _client_capturing(monkeypatch, capabilities=["completion"])
    client.generate_structured("p", _Answer, model="m", enable_thinking=True)
    assert [p.get("think") for u, p in sent if u.endswith("/api/chat")] == [None]


# ==============================================================================
# C3 — Défragmenteur sans rechargement du 26B à chaque paire
# ==============================================================================

def test_c3_defragmenter_keeps_model_loaded_between_pairs(exo_env, monkeypatch):
    import pandas as pd

    from src.consolidators.graph_defragmenter import ConceptMergeSchema, GraphDefragmenter
    from src.utils.markdown_io import ConceptFrontmatter, ParsedConceptNote, write_concept_file

    rows = []
    for i in range(3):
        path = exo_env.concepts_dir / f"rag-{i}.md"
        fm = ConceptFrontmatter(id=f"r{i}", title=f"Pipeline RAG {i}", created_at="2026-10-01", updated_at="2026-10-01")
        write_concept_file(ParsedConceptNote(frontmatter=fm, title_h1=fm.title, body="Corps."), path)
        rows.append({"slug": path.stem, "title": fm.title, "semantic_topic": "IA", "tags": "rag", "file_path": str(path), "vector": [1.0, 0.0 + i * 0.001]})
    vs = mock.MagicMock()
    vs._table.to_pandas.return_value = pd.DataFrame(rows)
    calls = []

    def fake_structured(prompt, **kwargs):
        calls.append(kwargs.get("keep_alive"))
        return ConceptMergeSchema(should_merge=False, canonical_title="x", canonical_slug="x",
                                  merged_summary_1_line="x", merged_markdown_body="x")

    monkeypatch.setattr(llm_client, "is_alive", mock.MagicMock(return_value=True))
    monkeypatch.setattr(llm_client, "generate_structured", fake_structured)
    GraphDefragmenter(db_manager=exo_env.db, vector_store=vs).run_defragmentation_cycle()
    assert len(calls) == 3 and set(calls) == {"5m"}
    assert llm_client.unload_model.call_count >= 1  # déchargement unique en sortie


# ==============================================================================
# C5 — Vision absente du modèle
# ==============================================================================

def test_c5_screenshots_released_when_model_has_no_vision(exo_env, monkeypatch):
    from src.consolidators.night_consolidator import NightConsolidator
    from src.database.db_manager import RawActivityRecord

    img = settings.SCREEN_STAGING_DIR / "screen_c5.webp"
    img.write_bytes(b"webp")
    exo_env.db.insert_raw_activities_batch([RawActivityRecord(
        timestamp_start=datetime(2026, 10, 3, 9), timestamp_end=datetime(2026, 10, 3, 9, 5), duration_sec=300,
        executable="code.exe", window_title="a.py", screenshot_path=str(img.resolve()))])
    monkeypatch.setattr(llm_client, "force_clear_vram", mock.MagicMock(return_value=16.0))
    monkeypatch.setattr(HardwareProbe, "get_vram_info", staticmethod(lambda: (16.0, 16.0)))
    monkeypatch.setattr(llm_client, "supports", lambda model, cap: False if cap == "vision" else None)
    vision = mock.MagicMock()
    monkeypatch.setattr(llm_client, "generate_vision", vision)

    NightConsolidator(db_manager=exo_env.db).run_pass_1_vision_and_tagging()
    vision.assert_not_called()
    assert not img.exists()
    assert exo_env.db.get_unprocessed_raw_activities() == []


# ==============================================================================
# C6 — Repli prudent de la sonde GPU
# ==============================================================================

def test_c6_probe_fallback_abstains(monkeypatch):
    import builtins

    real_import = builtins.__import__

    def no_pynvml(name, *args, **kwargs):
        if name == "pynvml":
            raise ImportError("absent")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", no_pynvml)
    with mock.patch("subprocess.run", side_effect=FileNotFoundError("nvidia-smi")):
        assert HardwareProbe.get_vram_info() == (0.0, 0.0)
        monkeypatch.setattr(settings, "VRAM_ASSUME_FREE_GB", 16.0)
        assert HardwareProbe.get_vram_info() == (16.0, 16.0)


# ==============================================================================
# C7 — Purge limitée aux modèles de l'Exocortex
# ==============================================================================

def test_c7_force_clear_spares_external_models(monkeypatch):
    client = HybridLLMClient()
    monkeypatch.setattr(client, "is_alive", lambda timeout=0.5: True)
    monkeypatch.setattr(client._session, "get", lambda url, timeout=None: _Resp(
        {"models": [{"name": "llama3:8b"}, {"name": f"{settings.MODEL_FAST_VISION}"}]}))
    unloaded = []
    monkeypatch.setattr(client, "unload_model", lambda m: unloaded.append(m) or True)
    monkeypatch.setattr(oc.time, "sleep", lambda s: None)
    monkeypatch.setattr(HardwareProbe, "get_vram_info", staticmethod(lambda: (10.0, 16.0)))
    client.force_clear_vram()
    assert "llama3:8b" not in unloaded and settings.MODEL_FAST_VISION in unloaded


# ==============================================================================
# C8 — Verrou VRAM inter-processus
# ==============================================================================

def _hold_lock(lock_path: str, ready, release) -> None:
    lock = oc.InterProcessVRAMLock(Path(lock_path))
    lock.acquire(timeout=5)
    ready.set()
    release.wait(10)
    lock.release()


def test_c8_lock_excludes_other_processes(tmp_path):
    lock_path = tmp_path / "vram.lock"
    ctx = multiprocessing.get_context("spawn")
    ready, release = ctx.Event(), ctx.Event()
    child = ctx.Process(target=_hold_lock, args=(str(lock_path), ready, release))
    child.start()
    try:
        assert ready.wait(30), "le processus enfant n'a pas obtenu le verrou"
        mine = oc.InterProcessVRAMLock(lock_path)
        t0 = time.monotonic()
        with pytest.raises(VRAMBusyError):
            mine.acquire(timeout=0.5)
        assert time.monotonic() - t0 >= 0.5
        release.set()
        child.join(10)
        mine.acquire(timeout=5)  # libéré par l'autre processus
        mine.acquire(timeout=0)  # réentrant dans le même processus
        mine.release()
        mine.release()
    finally:
        release.set()
        child.join(5)


def test_c8_every_gpu_call_takes_the_lock():
    for name in ("generate_text", "generate_vision", "generate_structured", "generate_embeddings", "force_clear_vram"):
        assert getattr(HybridLLMClient, name).__wrapped__  # décoré par _with_vram_lock


# ==============================================================================
# C9 — Provisioning par la CLI
# ==============================================================================

def test_c9_cli_is_the_primary_provisioning_path(tmp_path, monkeypatch):
    client = HybridLLMClient()
    modelfile = tmp_path / "Modelfile"
    modelfile.write_text("FROM x", encoding="utf-8")
    posted = []
    monkeypatch.setattr(client._session, "post", lambda url, json=None, timeout=None: posted.append(url) or _Resp({}))

    with mock.patch.object(oc.shutil, "which", return_value="C:/ollama.exe"), \
         mock.patch.object(oc.subprocess, "run", return_value=mock.MagicMock(returncode=0, stderr="")) as run:
        assert client._create_ollama_model("gemma4:12b", modelfile, "FROM x") is True
    assert run.call_args.args[0][:3] == ["C:/ollama.exe", "create", "gemma4:12b"] and posted == []

    with mock.patch.object(oc.shutil, "which", return_value=None):
        assert client._create_ollama_model("gemma4:12b", modelfile, "FROM x") is True
    assert posted and posted[0].endswith("/api/create")


# ==============================================================================
# C10 — Seuils VRAM à source unique
# ==============================================================================

def test_c10_single_source_thresholds(monkeypatch):
    assert settings.MIN_FREE_VRAM_GB == settings.VRAM_STRICT_ABORT_FREE_GB == 8.0
    assert settings.FULL_DUAL_MODEL_VRAM_GB == settings.VRAM_REASONING_MIN_FREE_GB == 12.8
    monkeypatch.setenv("MIN_FREE_VRAM_GB", "6.5")  # ancien nom encore honoré
    monkeypatch.delenv("VRAM_STRICT_ABORT_FREE_GB", raising=False)
    from src.config import Settings

    assert Settings().VRAM_STRICT_ABORT_FREE_GB == 6.5


# ==============================================================================
# C11 — Indexation LanceDB incrémentale
# ==============================================================================

def test_c11_vector_sync_is_incremental(tmp_path, monkeypatch):
    from src.database.vector_store import VectorStore
    from src.utils.markdown_io import ConceptFrontmatter, ParsedConceptNote, write_concept_file

    concepts = tmp_path / "concepts"
    for i in range(3):
        fm = ConceptFrontmatter(id=f"n{i}", title=f"Note {i}", created_at="2026-10-01", updated_at="2026-10-01")
        write_concept_file(ParsedConceptNote(frontmatter=fm, title_h1=fm.title, body=f"Corps {i}."), concepts / f"note-{i}.md")
    (concepts / "all-concepts.md").write_text("# Agrégat", encoding="utf-8")

    vs = VectorStore(store_dir=tmp_path / "lancedb")
    embed = mock.MagicMock(return_value=[0.1] * 1024)
    monkeypatch.setattr(vs, "get_embedding", embed)

    assert vs.sync_all_concepts(concepts) == 3 and embed.call_count == 3  # all-* exclu
    assert vs.sync_all_concepts(concepts) == 0 and embed.call_count == 3  # rien n'a changé

    (concepts / "note-1.md").write_text((concepts / "note-1.md").read_text(encoding="utf-8") + "\nAjout.", encoding="utf-8")
    (concepts / "note-2.md").unlink()
    assert vs.sync_all_concepts(concepts) == 1 and embed.call_count == 4
    assert vs._indexed_slugs() == {"note-0", "note-1"}


# ==============================================================================
# C12 — Index GraphRAG partagé entre requêtes
# ==============================================================================

def test_c12_graphrag_index_shared_and_invalidated(exo_env, monkeypatch):
    from fastapi.testclient import TestClient

    import src.api.server as server
    from src.database.graph_rag import HybridGraphRAG
    from src.utils.markdown_io import ConceptFrontmatter, ParsedConceptNote, write_concept_file

    monkeypatch.setattr(server, "_graph_rag_instance", None)
    built = []
    real_init = HybridGraphRAG.__init__

    def counting_init(self, *a, **kw):
        built.append(1)
        real_init(self, *a, **kw)

    monkeypatch.setattr(HybridGraphRAG, "__init__", counting_init)
    monkeypatch.setattr(HybridGraphRAG, "search_hybrid", lambda self, **kw: {"primary_nodes": [], "linked_neighbors": [], "episodic_traces": []})
    client = TestClient(server.app, base_url="http://127.0.0.1")
    for _ in range(3):
        assert client.get("/api/graphrag/search?q=rag").status_code == 200
    assert len(built) == 1

    rag = server._get_graph_rag()
    for i in range(2):
        fm = ConceptFrontmatter(id=f"g{i}", title=f"Graphe {i}", created_at="2026-10-01", updated_at="2026-10-01")
        write_concept_file(ParsedConceptNote(frontmatter=fm, title_h1=fm.title, body="x"), exo_env.concepts_dir / f"graphe-{i}.md")
    rag.refresh_index()
    assert rag.resolve_wikilink_to_path("Graphe 1") is not None
    (exo_env.concepts_dir / "graphe-1.md").unlink()
    rag.refresh_index()
    assert rag.resolve_wikilink_to_path("Graphe 1") is None  # suppression détectée
