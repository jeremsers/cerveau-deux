"""
Suite de vérification v0.5.6 — Lot 6 de l'audit : démons, robustesse et dette.
E1/E2 (injecteur), E3 (DriftGuard), E4 (arrêt propre), E5 (sonde Git/IDE), A10 (journal unique),
G6 (écriture atomique), G3 (interface principale), F1/F3 (suite hermétique).
"""

from __future__ import annotations

import json
import os
import sys
import threading
import time
import unittest.mock as mock
from datetime import date, datetime, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest

from src.config import settings


# ==============================================================================
# F1 / F3 — Suite hermétique
# ==============================================================================

def test_f1_session_never_points_to_real_vault():
    real_vault = (_ROOT / "Vault_Data").resolve()
    assert not settings.VAULT_ROOT.resolve().is_relative_to(real_vault)
    assert not settings.DB_PATH.resolve().is_relative_to(real_vault)
    assert settings.OLLAMA_BASE_URL.endswith(":9") or os.environ.get("EXOCORTEX_TEST_OLLAMA_URL")
    assert settings.GEMINI_API_KEY is None


def test_f3_no_suite_relies_on_personal_volumes():
    frozen = ("73153", "73 153", "392", ">= 476", "== 480", "6649")
    for test_file in (_ROOT / "tests").glob("test_v01*.py"):
        content = test_file.read_text(encoding="utf-8")
        for value in frozen:
            assert value not in content, f"{test_file.name} dépend encore d'un volume personnel ({value})"


# ==============================================================================
# E1 / E2 — Injecteur Hippocampe
# ==============================================================================

def test_e1_hotkey_is_configurable_and_not_alt_space():
    assert settings.HIPPOCAMPUS_HOTKEY == "<ctrl>+<alt>+<space>"
    src = (_ROOT / "src" / "daemons" / "hippocampus_hotkey.py").read_text(encoding="utf-8")
    assert 'hotkey_str = "<alt>+<space>"' not in src and "settings.HIPPOCAMPUS_HOTKEY" in src


def test_e2_hook_callback_returns_immediately(exo_env):
    import src.daemons.hippocampus_hotkey as hh

    injector = hh.HippocampusInjector(db_manager=exo_env.db, graph_rag=mock.MagicMock())
    release = threading.Event()

    def slow_copy():
        release.wait(5)
        return ""

    with mock.patch.object(hh, "simulate_select_and_copy", side_effect=slow_copy), \
         mock.patch.object(hh.winsound, "MessageBeep"):
        t0 = time.perf_counter()
        worker = injector.on_hotkey_triggered()
        elapsed = time.perf_counter() - t0
        assert worker is not None and elapsed < 0.1  # le hook clavier rend la main tout de suite
        assert injector.is_processing
        assert injector.on_hotkey_triggered() is None  # activation ignorée pendant le traitement
        release.set()
        worker.join(5)
    assert not injector.is_processing


# ==============================================================================
# E3 — DriftGuard : dérive média seulement après un tunnel de production
# ==============================================================================

def _feed_media(guard, start: datetime, blocks: int = 10):
    alert = None
    for i in range(blocks):
        res = guard.record_switch(start + timedelta(minutes=10 * i), "chrome.exe", "Documentaire - YouTube", 600, 0.05)
        alert = alert or res
    return alert


def test_e3_media_hole_requires_prior_production(tmp_path):
    from src.daemons.telemetry_daemon import DriftGuard

    now = datetime(2026, 10, 24, 21, 0)
    evening = DriftGuard(state_path=tmp_path / "a.json", max_passive_min=90)
    assert _feed_media(evening, now) is None  # soirée film sans travail préalable : pas de dérive

    after_work = DriftGuard(state_path=tmp_path / "b.json", max_passive_min=90)
    after_work.record_switch(now - timedelta(minutes=1), "code.exe", "main.py", 45 * 60, 0.8)
    alert = _feed_media(after_work, now)
    assert alert is not None and alert["drift_type"] == "unplanned_media_hole"


# ==============================================================================
# E4 — Arrêt propre
# ==============================================================================

def test_e4_daemon_stops_gracefully_and_saves_current_window(exo_env):
    import src.daemons.telemetry_daemon as td
    from src.utils.lifecycle import request_stop, stop_requested

    request_stop()  # signal résiduel d'une session précédente : effacé au démarrage
    daemon = td.TelemetryDaemon(db_manager=exo_env.db)
    state = td.WindowSessionState("code.exe", "main.py", 7)
    state.timestamp_start = datetime.now() - timedelta(minutes=10)
    daemon.current_state = state

    with mock.patch.object(daemon, "step"):
        loop = threading.Thread(target=daemon.run_loop, kwargs={"interval_sec": 0.05, "enable_browser_receiver": False})
        loop.start()
        time.sleep(0.3)
        assert loop.is_alive() and not stop_requested()
        request_stop()
        loop.join(5)
    assert not loop.is_alive()
    with exo_env.db.get_connection() as conn:
        assert conn.execute("SELECT COUNT(*) FROM raw_activity WHERE window_title = 'main.py';").fetchone()[0] == 1


def test_e4_stop_script_no_longer_uses_wmic():
    stop_bat = (_ROOT / "stop_exocortex.bat").read_text(encoding="utf-8")
    commands = "\n".join(line for line in stop_bat.splitlines() if not line.strip().startswith("::"))
    assert "wmic" not in commands.lower() and "run_exocortex.py --stop" in commands
    from src.utils.lifecycle import EXOCORTEX_PROCESS_MARKERS, stop_all

    assert any("dashboard" in m for m in EXOCORTEX_PROCESS_MARKERS)  # Streamlit visé
    assert any("server" in m or "--web" in m for m in EXOCORTEX_PROCESS_MARKERS)  # serveur web visé
    with mock.patch("src.utils.lifecycle.find_exocortex_processes", return_value=[]):
        assert stop_all(grace_sec=0.1) == 0
    assert not settings.STOP_FLAG_PATH.exists()


# ==============================================================================
# E5 — Résolution du dépôt Git
# ==============================================================================

def _repo(path: Path) -> Path:
    (path / ".git").mkdir(parents=True)
    return path


def test_e5_workspace_exact_match_and_vscode_index(tmp_path, monkeypatch):
    from src.daemons.git_ide_probe import GitIDEProbe

    api_repo = _repo(tmp_path / "api")
    gateway_repo = _repo(tmp_path / "api-gateway")
    probe = GitIDEProbe()
    known = [{"project_id": "api", "name": "API", "repo_path": str(api_repo)}]

    # « api-gateway » ne correspond plus au projet « api » par sous-chaîne
    title = "main.go - api-gateway - Visual Studio Code"
    assert probe._resolve_repo_path(0, title, known, "code.exe") is None

    # Index des workspaces VS Code (workspaceStorage)
    storage = tmp_path / "AppData" / "Code" / "User" / "workspaceStorage" / "abc123"
    storage.mkdir(parents=True)
    (storage / "workspace.json").write_text(json.dumps({"folder": gateway_repo.resolve().as_uri()}), encoding="utf-8")
    monkeypatch.setenv("APPDATA", str(tmp_path / "AppData"))
    assert GitIDEProbe()._resolve_repo_path(0, title, known, "code.exe") == gateway_repo.resolve()

    # Projet connu : correspondance exacte du workspace
    assert probe._resolve_repo_path(0, "app.py - api - Visual Studio Code", known, "code.exe") == api_repo


def test_e5_cwd_used_for_terminals_only(tmp_path):
    from src.daemons.git_ide_probe import GitIDEProbe

    repo = _repo(tmp_path / "depot")
    fake_proc = mock.MagicMock()
    fake_proc.cwd.return_value = str(repo / "src")
    with mock.patch("psutil.pid_exists", return_value=True), mock.patch("psutil.Process", return_value=fake_proc):
        probe = GitIDEProbe()
        assert probe._resolve_repo_path(1234, "PowerShell", [], "powershell.exe") == repo
        assert probe._resolve_repo_path(1234, "Sans titre - Visual Studio Code", [], "code.exe") is None


# ==============================================================================
# A10 — Journal épisodique unique à sections
# ==============================================================================

def test_a10_cold_start_and_night_share_the_journal(exo_env, monkeypatch):
    from src.consolidators.night_consolidator import NightConsolidator
    from src.database.db_manager import RawActivityRecord
    from src.ingestors.takeout_ingestor import generate_cold_start_episodic_journals
    from src.ingestors.takeout_parsers import ParsedTurn, ReconstructedSession
    from src.utils.episodic_journal import SECTION_AI_SESSIONS, SECTION_TELEMETRY, read_journal

    db = exo_env.db
    for day in (date(2026, 10, 5), date(2026, 10, 6)):
        turns = [ParsedTurn(timestamp=datetime.combine(day, datetime.min.time()).replace(hour=20) + timedelta(minutes=5 * i),
                            user_prompt="q" * 100, user_char_count=100) for i in range(4)]
        sess = ReconstructedSession(session_id=f"s_{day}", timestamp_start=turns[0].timestamp, timestamp_end=turns[-1].timestamp,
                                    turns=turns, turn_count=4, user_char_count=400, summary=f"Session du {day}")
        generate_cold_start_episodic_journals([sess], db)
        db.insert_raw_activities_batch([RawActivityRecord(
            timestamp_start=datetime.combine(day, datetime.min.time()).replace(hour=9),
            timestamp_end=datetime.combine(day, datetime.min.time()).replace(hour=10), duration_sec=3600,
            executable="code.exe", window_title="main.py", semantic_topic="Dev_et_Architecture_Tech",
            cognitive_mode="production", processed=True)])

    nc = NightConsolidator(db_manager=db)
    with mock.patch.object(nc, "run_pass_1_vision_and_tagging", return_value=0), \
         mock.patch.object(nc, "run_pass_3_vector_indexing", return_value=0):
        res = nc.consolidate()

    # Le 05/10 (journal cold start existant, pas la date max) est bien consolidé
    assert res["processed_dates"] == ["2026-10-05", "2026-10-06"]
    for day in ("2026-10-05", "2026-10-06"):
        fm, sections = read_journal(day)
        assert set(sections) == {SECTION_TELEMETRY, SECTION_AI_SESSIONS}
        assert f"Session du {day}" in sections[SECTION_AI_SESSIONS]  # sessions Gemini conservées
        assert fm["sessions_count"] == 1 and fm["total_screen_hours"] == 1.0
        assert set(fm["sources"]) == {"takeout_cold_start", "screen_telemetry"}

    # Une réingestion Takeout ne touche pas la section télémétrie
    before = read_journal("2026-10-06")[1][SECTION_TELEMETRY]
    generate_cold_start_episodic_journals([], db)
    assert read_journal("2026-10-06")[1][SECTION_TELEMETRY] == before


def test_a10_legacy_cold_start_journal_is_converted(exo_env):
    from src.utils.episodic_journal import SECTION_AI_SESSIONS, SECTION_TELEMETRY, read_journal, write_journal_section

    (exo_env.episodic_dir / "2025-05-01.md").write_text(
        '---\ndate: "2025-05-01"\norigin: "takeout_cold_start"\nsessions_count: 2\n---\n\n'
        "# Journal Épisodique — 2025-05-01\n\n## 2. Sessions Cognitives Réalisées\n- Session historique\n",
        encoding="utf-8",
    )
    write_journal_section("2025-05-01", SECTION_TELEMETRY, "## Télémétrie\n- 1 h", source="screen_telemetry")
    fm, sections = read_journal("2025-05-01")
    assert "Session historique" in sections[SECTION_AI_SESSIONS]
    assert fm["sessions_count"] == 2 and "origin" not in fm


# ==============================================================================
# G6 — Écriture atomique
# ==============================================================================

def test_g6_interrupted_write_keeps_previous_note(exo_env):
    from src.utils.markdown_io import ConceptFrontmatter, ParsedConceptNote, parse_concept_file, write_concept_file

    path = exo_env.concepts_dir / "note-atomique.md"
    fm = ConceptFrontmatter(id="n", title="Note", created_at="2026-10-01", updated_at="2026-10-01")
    write_concept_file(ParsedConceptNote(frontmatter=fm, title_h1="Note", body="Version 1 complète."), path)

    with mock.patch("src.utils.atomic_io.os.replace", side_effect=OSError("coupure")):
        with pytest.raises(OSError):
            write_concept_file(ParsedConceptNote(frontmatter=fm, title_h1="Note", body="Version 2"), path)

    assert parse_concept_file(path).body == "Version 1 complète."
    assert [p.name for p in exo_env.concepts_dir.iterdir() if p.suffix == ".tmp"] == []


# ==============================================================================
# G3 — Interface principale
# ==============================================================================

def test_g3_launchers_use_the_web_command_center():
    start_bat = (_ROOT / "start_exocortex.bat").read_text(encoding="cp1252")
    assert "run_exocortex.py --web" in start_bat and "streamlit run" not in start_bat
    launcher = (_ROOT / "run_exocortex.py").read_text(encoding="utf-8")
    run_all = launcher[launcher.index("def run_all"):launcher.index("def run_kanban_status")]
    assert "run_web()" in run_all and "streamlit" not in run_all
