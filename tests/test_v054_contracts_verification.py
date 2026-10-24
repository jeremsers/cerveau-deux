"""
Suite de vérification v0.5.4 — Lot 4 de l'audit : réconcilier backend et interfaces.
Tests de contrat (F2) entre les réponses de l'API, app.js, Streamlit et le serveur MCP :
B1 (KPIs), B2 (modes), B3 (drift), B4 (url_or_path), B5 (filtres), B6 (treemap),
B7 (tunnels), B8 (bootloader), B9 (libellés figés), B10 (outils MCP).
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest
from fastapi.testclient import TestClient

from src import __version__
from src.config import COGNITIVE_MODES, DISTILLATION_STATUSES, settings
from src.consolidators.night_consolidator import NightConsolidator
from src.database.db_manager import RawActivityRecord
from src.mcp.exocortex_mcp_server import (
    MCP_TOOLS_SPEC,
    build_tool_functions,
    handle_jsonrpc_request,
)
from src.utils.cognitive_metrics import DailyKpis, DriftStatus, compute_drift_status

WEB = _ROOT / "src" / "web_gui"
APP_JS = (WEB / "app.js").read_text(encoding="utf-8")
INDEX_HTML = (WEB / "index.html").read_text(encoding="utf-8")
STREAMLIT = (_ROOT / "src" / "dashboard" / "app.py").read_text(encoding="utf-8")


@pytest.fixture
def api(exo_env):
    from src.api.server import app

    return TestClient(app, base_url="http://127.0.0.1")


def _day(db, day: date):
    """Journée type : un tunnel de 50 min (code), une coupure de 1 min, un tunnel de 40 min (navigateur)."""
    base = datetime.combine(day, datetime.min.time()).replace(hour=9)
    rows = []
    t = base
    for exe, title, topic, mode, minutes, active in [
        ("code.exe", "server.py", "Dev_et_Architecture_Tech", "production", 25, True),
        ("code.exe", "app.js", "Dev_et_Architecture_Tech", "production", 25, True),
        ("slack.exe", "Slack", "Freelance_et_Carriere", "exploration", 1, False),
        ("chrome.exe", "Docs LanceDB", "IA_et_LLM_Local", "exploration", 40, False),
    ]:
        rows.append(RawActivityRecord(
            timestamp_start=t, timestamp_end=t + timedelta(minutes=minutes), duration_sec=minutes * 60,
            executable=exe, window_title=title, semantic_topic=topic, cognitive_mode=mode,
            active_input=active, processed=True, url_or_path="https://lancedb.github.io" if exe == "chrome.exe" else None,
        ))
        t += timedelta(minutes=minutes)
    db.insert_raw_activities_batch(rows)


# ==============================================================================
# B1 / B4 / B7 — Contrat de /api/telemetry/timeline
# ==============================================================================

def test_b1_daily_kpis_contract_before_and_after_consolidation(api, exo_env):
    _day(exo_env.db, date(2026, 10, 10))
    before = api.get("/api/telemetry/timeline?date=2026-10-10").json()["daily_metric"]

    NightConsolidator(db_manager=exo_env.db).calculate_daily_metrics_for_date(date(2026, 10, 10))
    after = api.get("/api/telemetry/timeline?date=2026-10-10").json()["daily_metric"]

    expected = set(DailyKpis.model_fields)
    assert set(before) == set(after) == expected
    assert before["is_consolidated"] is False and after["is_consolidated"] is True
    # Avant v0.5.4, ces KPIs tombaient à 0 dès qu'une ligne daily_metrics existait
    assert after["total_active_sec"] == 91 * 60
    assert after["total_deep_work_sec"] == 50 * 60
    assert after["hyperfocus_tunnel_count"] == 2

    used_by_front = set(re.findall(r"\bmetric\.(\w+)", APP_JS))
    assert used_by_front and used_by_front <= expected, used_by_front - expected


def test_b4_events_expose_url_or_path(api, exo_env):
    _day(exo_env.db, date(2026, 10, 11))
    events = api.get("/api/telemetry/timeline?date=2026-10-11").json()["events"]
    assert all("url_or_path" in e and "id" in e for e in events)
    assert any(e["url_or_path"] == "https://lancedb.github.io" for e in events)


def test_b7_single_tunnel_definition(api, exo_env):
    db = exo_env.db
    _day(db, date(2026, 10, 12))
    metric = NightConsolidator(db_manager=db).calculate_daily_metrics_for_date(date(2026, 10, 12))
    data = api.get("/api/telemetry/timeline?date=2026-10-12").json()
    longest = max(t["duration_sec"] for t in data["focus_tunnels"])
    assert longest == metric.max_hyperfocus_sec == 50 * 60
    assert {t["topic"] for t in data["focus_tunnels"]} == {"Dev_et_Architecture_Tech", "IA_et_LLM_Local"}
    assert "compute_focus_tunnels" in STREAMLIT


# ==============================================================================
# B2 / B5 — Vocabulaires servis par l'API
# ==============================================================================

def test_b2_b5_vocabulary_is_the_single_source(api):
    vocab = api.get("/api/meta/vocabulary").json()
    assert [m["key"] for m in vocab["cognitive_modes"]] == list(COGNITIVE_MODES)
    assert [s["key"] for s in vocab["distillation_statuses"]] == list(DISTILLATION_STATUSES)

    # Le front n'utilise plus l'ancien vocabulaire inventé, ni le statut fictif « skipped »
    for legacy in ("Deep_Work", "Execution", "Communication", "Passive", '"Noise"'):
        assert legacy not in APP_JS, legacy
    assert 'value="skipped"' not in INDEX_HTML
    assert "/api/meta/vocabulary" in APP_JS


def test_b2_modes_written_by_backend_are_in_vocabulary():
    src = (_ROOT / "src" / "consolidators" / "night_consolidator.py").read_text(encoding="utf-8")
    written = set(re.findall(r'return "[A-Za-z_]+", "(\w+)"', src))
    allowed_in_prompt = set(re.findall(r"'(\w+)'", re.search(r"Modes cognitifs autorisés : ([^\n]+)", src).group(1)))
    assert written and written <= set(COGNITIVE_MODES)
    assert allowed_in_prompt <= set(COGNITIVE_MODES)


def test_b5_statuses_written_by_backend_are_in_vocabulary():
    written = set()
    for py in (_ROOT / "src").rglob("*.py"):
        written |= set(re.findall(r'distillation_status\s*=\s*"(\w+)"', py.read_text(encoding="utf-8")))
        written |= set(re.findall(r'dist_status\s*=\s*"(\w+)"', py.read_text(encoding="utf-8")))
    assert written and written <= set(DISTILLATION_STATUSES), written - set(DISTILLATION_STATUSES)


# ==============================================================================
# B3 — État du DriftGuard
# ==============================================================================

def test_b3_drift_state_contract(api):
    now = datetime.now()
    settings.DRIFT_STATE_PATH.write_text(json.dumps({
        "active_alert": True, "drift_type": "hyper_fragmentation", "severity": "warning",
        "detected_at": (now - timedelta(minutes=5)).isoformat(), "diagnostic": "Zapping.",
    }), encoding="utf-8")
    drift = api.get("/api/system/status").json()["drift_state"]
    assert set(drift) == set(DriftStatus.model_fields) and drift["active"] is True
    assert "drift_state || {}" in APP_JS and "drift.active" in APP_JS and "drift_detected" not in APP_JS

    old = compute_drift_status({"active_alert": True, "detected_at": (now - timedelta(hours=2)).isoformat()}, now)
    assert old.active is False


# ==============================================================================
# B6 / B8 / B9 — Treemap, bootloader Streamlit, libellés figés
# ==============================================================================

def test_b6_treemap_uses_ids():
    block = APP_JS[APP_JS.index("function renderTreemapChart"):APP_JS.index("function renderDonutChart")]
    assert "ids:" in block and "parents: all.map((n) => n.parent)" in block


def test_b8_bootloader_expands_on_today_production():
    assert "expand_bootloader = load_today_production_sec() == 0" in STREAMLIT


def test_b9_no_hardcoded_profile_or_volumes(api, exo_env):
    for frozen in ("Hyperfocus Crépusculaire", "Chronotype du Loup", "690 sessions", "73 153", "6 649", "73k"):
        assert frozen not in INDEX_HTML and frozen not in STREAMLIT, frozen
    _day(exo_env.db, date(2026, 10, 13))
    diagnosis = api.get("/api/telemetry/circadian").json()["diagnosis"]
    assert diagnosis["label"] == "Profil matinal"  # 91 min entre 9 h et 10 h 31


# ==============================================================================
# B10 — Serveur MCP : une seule table d'outils
# ==============================================================================

def test_b10_mcp_single_tool_table():
    names = [spec["name"] for spec in MCP_TOOLS_SPEC]
    functions = build_tool_functions()
    assert list(functions) == names

    import inspect
    for spec in MCP_TOOLS_SPEC:
        params = set(inspect.signature(functions[spec["name"]]).parameters)
        assert params == set(spec["inputSchema"]["properties"]), spec["name"]

    init = handle_jsonrpc_request({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    assert init["result"]["serverInfo"]["version"] == __version__
    listed = handle_jsonrpc_request({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    assert [t["name"] for t in listed["result"]["tools"]] == names


def test_b10_jsonrpc_call_and_legacy_alias(exo_env):
    for name in ("get_active_kanban_queue", "mcp_get_kanban_queue"):
        res = handle_jsonrpc_request(
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": name, "arguments": {"project_id": "exocortex", "ignored": 1}}},
            db_manager=exo_env.db,
        )
        assert json.loads(res["result"]["content"][0]["text"])["project_id"] == "exocortex"


def test_b10_fastmcp_registers_same_names():
    fastmcp = pytest.importorskip("mcp.server.fastmcp")
    import asyncio

    app = fastmcp.FastMCP("Exocortex")
    functions = build_tool_functions()
    for spec in MCP_TOOLS_SPEC:
        app.add_tool(functions[spec["name"]], name=spec["name"], description=spec["description"])
    tools = asyncio.run(app.list_tools())
    assert sorted(t.name for t in tools) == sorted(spec["name"] for spec in MCP_TOOLS_SPEC)


def test_b10_mcp_pinned_in_requirements():
    reqs = (_ROOT / "requirements.txt").read_text(encoding="utf-8")
    assert re.search(r"^mcp>=1\.\d+,<2$", reqs, re.MULTILINE)
