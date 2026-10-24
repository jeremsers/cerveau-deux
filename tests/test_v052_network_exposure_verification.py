"""
Suite de vérification v0.5.2 — Lot 2 de l'audit : fermer l'exposition réseau.
D1 (CORS, Host, jeton API), D2 (CSP, échappement), D4 (récepteur 8502), D5 (SRI),
D6 (export Drive), D7 (liste noire), E6 (périmètre du content script).
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest
from fastapi.testclient import TestClient

from src.config import settings
from src.consolidators.drive_compiler import PRIVATE_TOPICS_LABEL, DriveCompiler
from src.daemons.browser_telemetry_receiver import BrowserTelemetryServer
from src.daemons.telemetry_daemon import WindowSessionState
from src.database.db_manager import DailyMetricRecord, KanbanTaskRecord
from src.utils.local_auth import TOKEN_HEADER, get_local_token
from src.utils.markdown_io import ConceptFrontmatter, ParsedConceptNote, write_concept_file
from src.utils.privacy import contains_secret_disclosure, is_sensitive_window

WEB_GUI = _ROOT / "src" / "web_gui"
EVIL = "https://evil.example"


@pytest.fixture
def api(exo_env):
    from src.api.server import app

    exo_env.db.upsert_kanban_task(KanbanTaskRecord(task_id="EXO-900", project_id="exocortex", title="Cible"))
    return TestClient(app, base_url="http://127.0.0.1")


# ==============================================================================
# D1 — API 8500
# ==============================================================================

def test_d1_foreign_origin_cannot_read_or_write(api):
    res = api.get("/api/kanban/tasks", headers={"Origin": EVIL})
    assert res.status_code == 200
    assert "access-control-allow-origin" not in res.headers
    assert "access-control-allow-credentials" not in res.headers

    preflight = api.options(
        "/api/kanban/tasks/EXO-900",
        headers={"Origin": EVIL, "Access-Control-Request-Method": "DELETE",
                 "Access-Control-Request-Headers": TOKEN_HEADER},
    )
    assert preflight.headers.get("access-control-allow-origin") != EVIL

    # Requête « simple » sans jeton (ce qu'une page tierce peut émettre sans pré-vol) : refusée
    assert api.delete("/api/kanban/tasks/EXO-900").status_code == 401
    assert api.post("/api/system/trigger-consolidate").status_code == 401
    assert api.get("/api/kanban/tasks/EXO-900/coder-prompt?mark_in_progress=true").status_code == 401

    token = api.get("/api/auth/token").json()["token"]
    assert api.delete("/api/kanban/tasks/EXO-900", headers={TOKEN_HEADER: token}).status_code == 200


def test_d1_token_endpoint_and_host_check(api):
    assert api.get("/api/auth/token", headers={"Sec-Fetch-Site": "cross-site", "Origin": EVIL}).status_code == 403
    assert api.get("/api/auth/token", headers={"Sec-Fetch-Site": "same-origin"}).json()["token"] == get_local_token("api")

    dev = "http://localhost:5173"
    res = api.get("/api/auth/token", headers={"Sec-Fetch-Site": "same-site", "Origin": dev})
    assert res.status_code == 200 and res.headers.get("access-control-allow-origin") == dev

    # DNS rebinding : un Host étranger est rejeté
    rebinding = TestClient(api.app, base_url="http://attacker.example")
    assert rebinding.get("/api/telemetry/dates").status_code == 400


# ==============================================================================
# D2 / D5 — CSP, échappement, intégrité des bibliothèques
# ==============================================================================

def test_d2_csp_and_security_headers(api):
    for path in ("/", "/api/telemetry/dates"):
        headers = api.get(path).headers
        csp = headers["content-security-policy"]
        assert "script-src 'self'" in csp and "'unsafe-inline'" not in csp.split("script-src")[1].split(";")[0]
        assert headers["x-content-type-options"] == "nosniff"
        assert headers["x-frame-options"] == "DENY"


def test_d2_no_inline_handlers_and_markdown_sanitized():
    app_js = (WEB_GUI / "app.js").read_text(encoding="utf-8")
    index = (WEB_GUI / "index.html").read_text(encoding="utf-8")
    assert not re.search(r"""\son(click|change|input|load|error)\s*=\s*["']""", app_js + index)
    assert not re.search(r"<script(?![^>]*\bsrc=)[^>]*>", index), "aucun script inline autorisé par la CSP"
    assert "DOMPurify.sanitize(marked.parse(" in app_js
    assert "${m.user_prompt}" not in app_js and "${esc(m.user_prompt)}" in app_js


def test_d5_cdn_scripts_are_pinned_with_sri():
    index = (WEB_GUI / "index.html").read_text(encoding="utf-8")
    external = re.findall(r"<script[^>]*src=\"(https://[^\"]+)\"[^>]*>", index)
    assert len(external) == 3  # Plotly, Marked, DOMPurify ; Tailwind est servi en local
    assert (WEB_GUI / "vendor" / "tailwindcss-play-3.4.16.js").exists()
    for tag in re.findall(r"<script[^>]*src=\"https://[^>]*>", index):
        assert 'integrity="sha384-' in tag and 'crossorigin="anonymous"' in tag
        assert re.search(r"(@\d+\.\d+\.\d+|-\d+\.\d+\.\d+|/\d+\.\d+\.\d+)", tag), tag


# ==============================================================================
# D4 / E6 — Récepteur 8502 et extension
# ==============================================================================

def _request(url, data=None, headers=None, method="GET"):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as err:
        return err.code, dict(err.headers), err.read()


def test_d4_receiver_requires_extension_token(exo_env):
    class Daemon:
        current_state = WindowSessionState("Code.exe", "main.py - Visual Studio Code", 1)

    daemon = Daemon()
    with BrowserTelemetryServer(db_manager=exo_env.db, daemon=daemon, host="127.0.0.1", port=0) as srv:
        base = srv.base_url
        tab = json.dumps({"url": "https://example.org/x", "title": "Exemple"}).encode()

        status, _, _ = _request(f"{base}/telemetry/tab", tab, {"Content-Type": "application/json"}, "POST")
        assert status == 401

        status, headers, _ = _request(f"{base}/telemetry/tab", headers={"Origin": EVIL}, method="OPTIONS")
        assert status == 403 and "Access-Control-Allow-Origin" not in headers
        assert _request(f"{base}/auth/token", headers={"Origin": EVIL})[0] == 403

        ext = "chrome-extension://abcdef"
        status, _, body = _request(f"{base}/auth/token", headers={"Origin": ext})
        token = json.loads(body)["token"]
        auth = {"Content-Type": "application/json", TOKEN_HEADER: token, "Origin": ext}

        status, headers, _ = _request(f"{base}/telemetry/tab", tab, auth, "POST")
        assert status == 200 and headers.get("Access-Control-Allow-Origin") == ext
        # L'URL n'est jamais rattachée à une fenêtre qui n'est pas un navigateur
        assert daemon.current_state.url_or_path is None

        assert _request(f"{base}/telemetry/tab", tab, {**auth, "Content-Type": "text/plain"}, "POST")[0] == 415
        big = json.dumps({"url": "https://x.org", "title": "x" * (settings.BROWSER_RECEIVER_MAX_BODY_BYTES + 1)}).encode()
        assert _request(f"{base}/telemetry/tab", big, auth, "POST")[0] == 413

        forged = json.dumps({"session_id": "s", "user_prompt": "<img src=x onerror=alert(1)>", "ai_response": "r"}).encode()
        assert _request(f"{base}/telemetry/chat_turn", forged, {"Content-Type": "application/json"}, "POST")[0] == 401


def test_e6_content_script_limited_to_ai_platforms():
    manifest = json.loads((_ROOT / "browser_extension" / "manifest.json").read_text(encoding="utf-8"))
    matches = [m for cs in manifest["content_scripts"] for m in cs["matches"]]
    assert "<all_urls>" not in matches
    assert all(any(d in m for d in ("gemini.google.com", "claude.ai", "chatgpt.com", "chat.openai.com")) for m in matches)


# ==============================================================================
# D7 — Liste noire en mots entiers et par domaine
# ==============================================================================

@pytest.mark.parametrize("exe,title,url,expected", [
    ("Code.exe", "login_flow.ts - cerveau-deux - Visual Studio Code", None, False),
    ("chrome.exe", "Problème de connexion au serveur Ollama - Google Chrome", None, False),
    ("chrome.exe", "Bankai - Bleach Wiki - Google Chrome", None, False),
    ("Code.exe", "password_policy.py - Visual Studio Code", None, False),
    ("chrome.exe", "Mon compte — Boursorama - Google Chrome", None, True),
    ("msedge.exe", "Nouvel onglet - [InPrivate] - Microsoft Edge", None, True),
    ("chrome.exe", "Connexion", "https://accounts.google.com/signin", True),
    ("chrome.exe", "Espace client", "https://clients.boursobank.com/", True),
    ("KeePassXC.exe", "Base.kdbx", None, True),
])
def test_d7_blacklist_samples(exe, title, url, expected):
    assert is_sensitive_window(exe, title, url) is expected


def test_d7_chat_secret_disclosure():
    assert contains_secret_disclosure("Voici mon mot de passe root : SuperSecret123!")
    assert contains_secret_disclosure("ma clé sk-abcdefghijklmnopqrstuvwxyz123456")
    assert not contains_secret_disclosure("Comment hacher un password avec argon2 ?")


# ==============================================================================
# D6 — Catégories sensibles absentes de l'export Drive
# ==============================================================================

def test_d6_drive_export_excludes_sensitive_topics(exo_env):
    cdir = exo_env.concepts_dir
    for slug, topic in [("suivi-traitement", "Sante_et_Pharmacologie"), ("pipeline-rag", "IA_et_LLM_Local")]:
        fm = ConceptFrontmatter(id=slug, title=slug, semantic_topic=topic, created_at="2026-10-20",
                                updated_at="2026-10-20", summary_1_line=f"résumé {slug}")
        write_concept_file(ParsedConceptNote(frontmatter=fm, title_h1=slug, body=f"Corps {slug}"), cdir / f"{slug}.md")
    settings.TAXONOMIE_TAGS_PATH.write_text(
        "- **`Sante_et_Pharmacologie`** : pharmacologie\n- **`IA_et_LLM_Local`** : LLM\n", encoding="utf-8")
    from datetime import date
    exo_env.db.upsert_daily_metrics(DailyMetricRecord(
        date=date.today(), total_screen_sec=3600, active_production_sec=1800, passive_exploration_sec=1800,
        max_hyperfocus_sec=1800, max_hyperfocus_topic="Sante_et_Pharmacologie", context_switches_per_hour=1.0,
        read_vs_write_ratio=1.0, top_topics_json=json.dumps({"Sante_et_Pharmacologie": 1800, "IA_et_LLM_Local": 1800}),
    ))

    files = DriveCompiler(db_manager=exo_env.db).compile_all()
    exported = "\n".join(Path(p).read_text(encoding="utf-8") for p in files.values())

    assert "suivi-traitement" not in exported and "pipeline-rag" in exported
    assert "pharmacologie" not in exported
    assert PRIVATE_TOPICS_LABEL in exported
    assert "Sante_et_Pharmacologie" not in exported.replace(
        "les catégories suivantes ne sont jamais exportées vers Drive : `Admin_Finance_et_Droit`, "
        "`Introspection_et_Neuroatypie`, `Sante_et_Pharmacologie`", "")
