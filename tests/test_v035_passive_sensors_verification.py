"""
Suite de tests de vérification pour la version v0.3.5 :
EXO-011 — Enrichissement des Capteurs Passifs : Sonde Git/IDE & Connecteur Navigateur Temps Réel.
1. Sonde Contextuelle Git & IDE (GitIDEProbe) : extraction repo/branche/diff et cache TTL 30s.
2. Nettoyage d'URL (sanitize_url) : suppression des paramètres de tracking et fragments.
3. Récepteur Télémétrique Local HTTP (BrowserTelemetryServer) : /telemetry/tab, CORS et filtrage blacklist (204).
4. Ingestion Live IA (/telemetry/chat_turn) et idempotence stricte dans SQLite (chat_sessions / chat_messages).
"""

from __future__ import annotations

import json
import os
import re
import sys
import unittest.mock as mock
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pytest

from src.config import settings
from src.daemons.browser_telemetry_receiver import (
    BrowserTelemetryServer,
    is_payload_blacklisted,
)
from src.daemons.git_ide_probe import GitIDEProbe, sanitize_url
from src.daemons.telemetry_daemon import WindowSessionState
from src.database.db_manager import DBManager


# ==============================================================================
# TEST 1 : SONDE GIT/IDE, FORMATAGE ET FONCTIONNEMENT DU CACHE TTL 30S
# ==============================================================================

def test_git_ide_probe_formatting_and_cache():
    """
    Vérifie que :
    - sanitize_url supprime proprement les paramètres de tracking (utm_*, gclid, etc.) et fragments.
    - GitIDEProbe extrait le statut git (branche, insertions, suppressions) sur le dépôt courant.
    - Le cache TTL de 30 secondes évite toute exécution superflue de sous-processus git.
    - Les exécutables non-IDE sont immédiatement ignorés.
    """
    # 1. Validation de sanitize_url
    raw_url = "https://docs.python.org/3/library/re.html?utm_source=twitter&utm_medium=social&gclid=12345&id=42#re-syntax"
    clean = sanitize_url(raw_url)
    assert clean == "https://docs.python.org/3/library/re.html?id=42"
    assert "utm_" not in clean
    assert "gclid" not in clean
    assert "#" not in clean

    clean_plain = sanitize_url("https://github.com/astral-sh/uv?utm_campaign=launch")
    assert clean_plain == "https://github.com/astral-sh/uv"

    # 2. Validation de GitIDEProbe sur le dépôt actif
    probe = GitIDEProbe(cache_ttl=30.0)

    # Exécutable hors cible -> None
    assert probe.probe_active_ide(pid=os.getpid(), executable="notepad.exe", window_title="Notes") is None

    # Exécutable cible (VS Code) sur le projet courant
    known_projects = [
        {
            "project_id": "exocortex",
            "name": "cerveau-deux",
            "repo_path": str(_ROOT),
        }
    ]
    window_title = f"git_ide_probe.py - {_ROOT.name} - Visual Studio Code"

    result = probe.probe_active_ide(
        pid=os.getpid(),
        executable="code.exe",
        window_title=window_title,
        known_projects=known_projects,
    )

    assert result is not None
    assert result.startswith(f"git:{_ROOT.name}:")
    assert re.search(r"\(\+\d+/-\d+\)$", result)

    # 3. Validation du cache TTL (30 secondes)
    # Si on appelle immédiatement à nouveau en mockant subprocess.run pour lever une exception,
    # le probe DOIT retourner la valeur en cache sans exécuter git.
    with mock.patch("subprocess.run", side_effect=RuntimeError("Ne doit pas être appelé (cache actif)")):
        cached_result = probe.probe_active_ide(
            pid=os.getpid(),
            executable="code.exe",
            window_title=window_title,
            known_projects=known_projects,
        )
        assert cached_result == result


EXTENSION_ORIGIN = "chrome-extension://dummy-extension-id"


def _extension_headers(base_url: str) -> dict:
    """En-têtes envoyés par l'extension depuis v0.5.2 : jeton local obtenu via GET /auth/token."""
    req = urllib.request.Request(f"{base_url}/auth/token", headers={"Origin": EXTENSION_ORIGIN})
    with urllib.request.urlopen(req) as resp:
        token = json.loads(resp.read().decode("utf-8"))["token"]
    return {"Content-Type": "application/json", "Origin": EXTENSION_ORIGIN, "X-Exocortex-Token": token}


# ==============================================================================
# TEST 2 : RÉCEPTEUR HTTP LOCAL, TAB TELEMETRY ET FILTRAGE STRICT BLACKLIST
# ==============================================================================

def test_browser_receiver_tab_and_blacklist(tmp_path: Path):
    """
    Lance BrowserTelemetryServer sur un port éphémère (port=0), envoie :
    - Un POST /telemetry/tab valide et vérifie l'enrichissement en RAM.
    - Un POST /telemetry/tab blacklisté ('bitwarden', 'master password') et vérifie le 204 No Content strict.
    - Une requête OPTIONS pour vérifier les en-têtes CORS.
    """
    db_file = tmp_path / "test_browser.db"
    db = DBManager(db_path=db_file)
    db.init_db()

    # Simulation d'un état courant du démon en RAM
    class DummyDaemon:
        def __init__(self):
            self.current_state = WindowSessionState(
                executable="msedge.exe",
                window_title="Documentation Python - Microsoft Edge",
                hwnd=1001,
            )

    dummy_daemon = DummyDaemon()

    with BrowserTelemetryServer(db_manager=db, daemon=dummy_daemon, host="127.0.0.1", port=0) as server:
        base_url = server.base_url

        # 1. Vérification CORS (OPTIONS)
        req_opt = urllib.request.Request(
            f"{base_url}/telemetry/tab",
            headers={"Origin": "chrome-extension://dummy-extension-id"},
            method="OPTIONS",
        )
        with urllib.request.urlopen(req_opt) as resp_opt:
            assert resp_opt.status in (200, 204)
            assert resp_opt.headers.get("Access-Control-Allow-Origin") == "chrome-extension://dummy-extension-id"

        # 2. Requête valide : POST /telemetry/tab
        valid_payload = {
            "url": "https://docs.python.org/3/library/asyncio.html?utm_source=twitter#runners",
            "title": "asyncio — Asynchronous I/O — Python documentation",
            "h1": "asyncio — Asynchronous I/O",
            "domain": "docs.python.org",
        }
        body_bytes = json.dumps(valid_payload).encode("utf-8")
        req_valid = urllib.request.Request(
            f"{base_url}/telemetry/tab",
            data=body_bytes,
            headers=_extension_headers(base_url),
            method="POST",
        )
        with urllib.request.urlopen(req_valid) as resp_valid:
            assert resp_valid.status == 200
            resp_data = json.loads(resp_valid.read().decode("utf-8"))
            assert resp_data.get("status") == "ok"
            assert resp_data.get("url") == "https://docs.python.org/3/library/asyncio.html"

        # Vérification de la mise à jour en RAM de current_state
        assert dummy_daemon.current_state.url_or_path == "https://docs.python.org/3/library/asyncio.html"
        assert dummy_daemon.current_state.ocr_snippet == "asyncio — Asynchronous I/O"

        # 3. Requête blacklistée : POST /telemetry/tab contenant 'bitwarden'
        blacklisted_payload = {
            "url": "https://vault.bitwarden.com/#/vault",
            "title": "Bitwarden Web Vault",
            "h1": "Master Password Credentials",
            "domain": "vault.bitwarden.com",
        }
        req_black = urllib.request.Request(
            f"{base_url}/telemetry/tab",
            data=json.dumps(blacklisted_payload).encode("utf-8"),
            headers=_extension_headers(base_url),
            method="POST",
        )
        with urllib.request.urlopen(req_black) as resp_black:
            # Code 204 No Content strict
            assert resp_black.status == 204

        # Vérification stricte : current_state n'a PAS été écrasé par la requête interdite
        assert dummy_daemon.current_state.url_or_path == "https://docs.python.org/3/library/asyncio.html"


# ==============================================================================
# TEST 3 : INGESTION LIVE TOURS DE CHAT IA & IDEMPOTENCE STRICTE
# ==============================================================================

def test_live_chat_turn_ingestion_idempotence(tmp_path: Path):
    """
    Envoie deux fois le même tour de chat IA via POST /telemetry/chat_turn.
    Vérifie :
    - La création initiale dans chat_sessions (turn_count = 1) et chat_messages (turn_index = 0).
    - L'idempotence stricte : aucune duplication lors du second envoi (turn_count reste 1, 1 seul message).
    - L'incrémentation propre lors de l'envoi d'un second tour distinct (turn_count = 2, turn_index = 1).
    - Le rejet immédiat (204 No Content) si le prompt contient un mot de passe ou terme blacklisté.
    """
    db_file = tmp_path / "test_chat_live.db"
    db = DBManager(db_path=db_file)
    db.init_db()

    with BrowserTelemetryServer(db_manager=db, host="127.0.0.1", port=0) as server:
        base_url = server.base_url
        session_id = "gemini_live_session_alpha_1"

        turn_1_payload = {
            "platform": "gemini",
            "session_id": session_id,
            "user_prompt": "Comment concevoir une architecture event-driven en Python ?",
            "ai_response": "Une architecture event-driven repose sur un bus de messages ou Kafka...",
            "url": "https://gemini.google.com/app/session_alpha_1",
        }

        # --- 1er ENVOI DU TOUR 1 ---
        req_1 = urllib.request.Request(
            f"{base_url}/telemetry/chat_turn",
            data=json.dumps(turn_1_payload).encode("utf-8"),
            headers=_extension_headers(base_url),
            method="POST",
        )
        with urllib.request.urlopen(req_1) as resp_1:
            assert resp_1.status == 200
            data_1 = json.loads(resp_1.read().decode("utf-8"))
            assert data_1["result"]["status"] == "created"
            assert data_1["result"]["turn_index"] == 0

        # Vérification en base
        session_db = db.get_chat_session_by_id(session_id)
        assert session_db is not None
        assert session_db["turn_count"] == 1

        messages_db = db.fetch_messages_for_session(session_id)
        assert len(messages_db) == 1
        assert messages_db[0]["turn_index"] == 0
        assert messages_db[0]["user_prompt"] == "Comment concevoir une architecture event-driven en Python ?"

        # --- 2e ENVOI IDENTIQUE DU TOUR 1 (TEST D'IDEMPOTENCE) ---
        req_duplicate = urllib.request.Request(
            f"{base_url}/telemetry/chat_turn",
            data=json.dumps(turn_1_payload).encode("utf-8"),
            headers=_extension_headers(base_url),
            method="POST",
        )
        with urllib.request.urlopen(req_duplicate) as resp_dup:
            assert resp_dup.status == 200
            data_dup = json.loads(resp_dup.read().decode("utf-8"))
            assert data_dup["result"]["status"] == "duplicate"
            assert data_dup["result"]["is_new"] is False

        # Vérification stricte : aucun doublon dans la base
        session_db_after = db.get_chat_session_by_id(session_id)
        assert session_db_after["turn_count"] == 1

        messages_after = db.fetch_messages_for_session(session_id)
        assert len(messages_after) == 1

        # --- 3e ENVOI : UN SECOND TOUR DISTINCT DANS LA MÊME SESSION ---
        turn_2_payload = {
            "platform": "gemini",
            "session_id": session_id,
            "user_prompt": "Quel est le compromis de latence avec Kafka ?",
            "ai_response": "Le compromis principal est l'éventuelle consistance et la surcharge réseau...",
            "url": "https://gemini.google.com/app/session_alpha_1",
        }
        req_2 = urllib.request.Request(
            f"{base_url}/telemetry/chat_turn",
            data=json.dumps(turn_2_payload).encode("utf-8"),
            headers=_extension_headers(base_url),
            method="POST",
        )
        with urllib.request.urlopen(req_2) as resp_2:
            assert resp_2.status == 200
            data_2 = json.loads(resp_2.read().decode("utf-8"))
            assert data_2["result"]["status"] == "created"
            assert data_2["result"]["turn_index"] == 1

        session_db_2 = db.get_chat_session_by_id(session_id)
        assert session_db_2["turn_count"] == 2

        messages_2 = db.fetch_messages_for_session(session_id)
        assert len(messages_2) == 2
        assert messages_2[1]["turn_index"] == 1
        assert messages_2[1]["user_prompt"] == "Quel est le compromis de latence avec Kafka ?"

        # --- 4e ENVOI : TOUR CONTENANT UN MOT DE PASSE (BLACKLIST) ---
        turn_blacklisted = {
            "platform": "gemini",
            "session_id": session_id,
            "user_prompt": "Voici mon mot de passe root : SuperSecret123!",
            "ai_response": "Ne partagez jamais vos mots de passe...",
            "url": "https://gemini.google.com/app/session_alpha_1",
        }
        req_black = urllib.request.Request(
            f"{base_url}/telemetry/chat_turn",
            data=json.dumps(turn_blacklisted).encode("utf-8"),
            headers=_extension_headers(base_url),
            method="POST",
        )
        with urllib.request.urlopen(req_black) as resp_black:
            assert resp_black.status == 204

        # Vérification : le tour rejeté n'a pas été inséré
        session_final = db.get_chat_session_by_id(session_id)
        assert session_final["turn_count"] == 2
        assert len(db.fetch_messages_for_session(session_id)) == 2

