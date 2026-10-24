"""
Récepteur Télémétrique Local HTTP (Module 2 - v0.3.5 / EXO-011).
Serveur HTTP léger (ThreadingHTTPServer) écoutant exclusivement sur 127.0.0.1:8502 (ou port dynamique).
Reçoit la télémétrie des onglets actifs et les échanges avec les LLMs (Gemini, Claude, ChatGPT)
depuis l'extension navigateur sans aucun surcoût VRAM (0 Mo VRAM).
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, Optional, Tuple

from src.config import settings
from src.daemons.git_ide_probe import sanitize_url
from src.database.db_manager import DBManager
from src.utils.local_auth import TOKEN_HEADER, get_local_token, token_matches
from src.utils.privacy import (
    contains_secret_disclosure,
    contains_sensitive_term,
    is_browser_executable,
    is_sensitive_url,
)

logger = logging.getLogger("Exocortex.BrowserReceiver")


EXTENSION_ORIGIN_PREFIXES = ("chrome-extension://", "moz-extension://", "extension://")


def is_payload_blacklisted(*texts: Optional[str], urls: Tuple[Optional[str], ...] = ()) -> bool:
    """
    Vrai si l'une des URL appartient à un domaine sensible, ou si l'un des textes contient un terme
    de la liste noire en mot entier (navigation privée, gestionnaires de secrets, banques) — v0.5.2, D7.
    """
    return any(is_sensitive_url(u) for u in urls) or contains_sensitive_term(*texts)


def _is_extension_origin(origin: Optional[str]) -> bool:
    return bool(origin) and origin.startswith(EXTENSION_ORIGIN_PREFIXES)


class BrowserTelemetryRequestHandler(BaseHTTPRequestHandler):
    """Gestionnaire de requêtes HTTP pour le pont d'extension navigateur."""

    server: "BrowserTelemetryServer"  # Type hint pour l'instance parente

    def log_message(self, format: str, *args: Any) -> None:
        """Délègue les logs HTTP au logger standard sans polluer stdout."""
        logger.debug("%s - " + format, self.address_string(), *args)

    def _send_cors_headers(self) -> None:
        """
        En-têtes CORS réservés à l'extension (v0.5.2, D4) : l'origine n'est renvoyée que si elle
        est une origine d'extension. Une page web ne peut donc ni lire les réponses ni passer le
        pré-vol qu'impose l'en-tête X-Exocortex-Token.
        """
        origin = self.headers.get("Origin")
        if _is_extension_origin(origin):
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
            self.send_header("Access-Control-Allow-Headers", f"Content-Type, {TOKEN_HEADER}")
            self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self) -> None:
        """Gère les requêtes préliminaires CORS (preflight)."""
        self.send_response(HTTPStatus.NO_CONTENT if _is_extension_origin(self.headers.get("Origin")) else HTTPStatus.FORBIDDEN)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        """GET /auth/token : remet le jeton partagé à l'extension (origine d'extension uniquement)."""
        if self.path != "/auth/token":
            self._send_json_error(HTTPStatus.NOT_FOUND, f"Route inconnue : {self.path}")
            return
        origin = self.headers.get("Origin")
        # Une page web envoie toujours son Origin sur un fetch cross-origin : seule l'extension
        # (origine chrome-extension://) ou un client local sans navigateur obtient le jeton.
        if origin and not _is_extension_origin(origin):
            self._send_json_error(HTTPStatus.FORBIDDEN, "Origine non autorisée")
            return
        self._send_json_response(HTTPStatus.OK, {"token": get_local_token("browser_receiver"), "header": TOKEN_HEADER})

    def do_POST(self) -> None:
        """Traite les flux /telemetry/tab et /telemetry/chat_turn."""
        if not token_matches("browser_receiver", self.headers.get(TOKEN_HEADER)):
            self._send_json_error(HTTPStatus.UNAUTHORIZED, "Jeton local manquant ou invalide")
            return

        if "application/json" not in (self.headers.get("Content-Type") or "").lower():
            self._send_json_error(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "Content-Type application/json requis")
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            content_length = 0
        if content_length <= 0:
            self._send_json_error(HTTPStatus.BAD_REQUEST, "Payload vide")
            return
        if content_length > settings.BROWSER_RECEIVER_MAX_BODY_BYTES:
            self._send_json_error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "Payload trop volumineux")
            return

        try:
            raw_body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(raw_body)
        except Exception as exc:
            logger.debug("Erreur décodage JSON payload : %s", exc)
            self._send_json_error(HTTPStatus.BAD_REQUEST, f"JSON invalide : {exc}")
            return

        if self.path == "/telemetry/tab":
            self._handle_tab_telemetry(data)
        elif self.path == "/telemetry/chat_turn":
            self._handle_chat_turn(data)
        else:
            self._send_json_error(HTTPStatus.NOT_FOUND, f"Route inconnue : {self.path}")

    def _handle_tab_telemetry(self, data: Dict[str, Any]) -> None:
        """
        Gère POST /telemetry/tab :
        Payload : {"url": str, "title": str, "h1": Optional[str], "domain": Optional[str]}
        """
        url = str(data.get("url") or "").strip()
        title = str(data.get("title") or "").strip()
        h1 = str(data.get("h1") or "").strip()
        domain = str(data.get("domain") or "").strip()

        # Invariant 1 : Filtrage strict de confidentialité (204 No Content sans toucher SQLite ni RAM)
        if is_payload_blacklisted(title, h1, urls=(url, domain)):
            logger.info("Onglet rejeté par la blacklist de confidentialité : %s", domain or url[:30])
            self.send_response(HTTPStatus.NO_CONTENT)
            self._send_cors_headers()
            self.end_headers()
            return

        clean_url = sanitize_url(url)

        # Mise à jour en RAM de l'état du démon de télémétrie s'il est rattaché
        server = self.server
        tab_info = {
            "url": clean_url,
            "title": title,
            "h1": h1,
            "domain": domain,
            "timestamp": datetime.now(),
        }
        server.last_tab_telemetry = tab_info

        # L'URL n'est rattachée qu'à une fenêtre de navigateur (jamais à VS Code ou autre, D4)
        daemon = server.daemon
        if daemon and daemon.current_state and is_browser_executable(daemon.current_state.executable):
            daemon.current_state.url_or_path = clean_url
            if h1:
                daemon.current_state.ocr_snippet = h1[:200]

        logger.debug("Onglet reçu et épuré : %s (%s)", clean_url, title[:40])
        self._send_json_response(HTTPStatus.OK, {"status": "ok", "url": clean_url})

    def _handle_chat_turn(self, data: Dict[str, Any]) -> None:
        """
        Gère POST /telemetry/chat_turn :
        Payload : {"platform": str, "session_id": str, "user_prompt": str, "ai_response": str, "url": Optional[str]}
        """
        platform = str(data.get("platform") or "web").strip().lower()
        session_id = str(data.get("session_id") or "").strip()
        user_prompt = str(data.get("user_prompt") or "").strip()
        ai_response = str(data.get("ai_response") or "").strip()
        url = str(data.get("url") or "").strip()

        if not session_id or not user_prompt:
            self._send_json_error(HTTPStatus.BAD_REQUEST, "session_id et user_prompt obligatoires")
            return

        # Invariant 1 : Filtrage strict de confidentialité (204 No Content)
        if is_payload_blacklisted(user_prompt, ai_response, urls=(url,)) or contains_secret_disclosure(user_prompt):
            logger.info("Tour de chat IA rejeté par la blacklist de confidentialité (session: %s)", session_id)
            self.send_response(HTTPStatus.NO_CONTENT)
            self._send_cors_headers()
            self.end_headers()
            return

        # Persistance idempotente dans SQLite
        db = self.server.db
        try:
            result = db.upsert_live_chat_turn(
                platform=platform,
                session_id=session_id,
                user_prompt=user_prompt,
                ai_response=ai_response,
            )
            logger.info(
                "Tour de chat capturé en direct [%s] session '%s' (turn=%s, status=%s)",
                platform,
                session_id,
                result.get("turn_index"),
                result.get("status"),
            )
            self._send_json_response(HTTPStatus.OK, {"status": "ok", "result": result})
        except Exception as exc:
            logger.error("Erreur ingestion tour de chat : %s", exc)
            self._send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"Erreur base de données : {exc}")

    def _send_json_response(self, status: HTTPStatus, body_dict: Dict[str, Any]) -> None:
        """Envoie une réponse JSON avec entêtes CORS."""
        resp_bytes = json.dumps(body_dict, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.end_headers()
        self.wfile.write(resp_bytes)

    def _send_json_error(self, status: HTTPStatus, message: str) -> None:
        """Envoie un message d'erreur JSON avec entêtes CORS."""
        self._send_json_response(status, {"error": message, "status": status.value})


class BrowserTelemetryServer(ThreadingHTTPServer):
    """
    Serveur HTTP multithread dédié à la réception de la télémétrie navigateur.
    Écoute exclusivement sur le loopback 127.0.0.1.
    """

    def __init__(
        self,
        db_manager: Optional[DBManager] = None,
        daemon: Optional[Any] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> None:
        bind_host = host or settings.BROWSER_RECEIVER_HOST or "127.0.0.1"
        bind_port = port if port is not None else settings.BROWSER_RECEIVER_PORT

        super().__init__((bind_host, bind_port), BrowserTelemetryRequestHandler)

        self.db = db_manager or DBManager()
        self.daemon = daemon
        self.last_tab_telemetry: Optional[Dict[str, Any]] = None
        self._thread: Optional[threading.Thread] = None

    @property
    def port(self) -> int:
        """Retourne le port réel assigné au socket (utile pour les ports éphémères)."""
        return self.server_address[1]

    @property
    def base_url(self) -> str:
        """Retourne l'URL de base du serveur."""
        return f"http://127.0.0.1:{self.port}"

    def start(self) -> None:
        """Démarre le serveur dans un thread d'arrière-plan autonome."""
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(
            target=self.serve_forever,
            name="Exocortex-BrowserReceiver",
            daemon=True,
        )
        self._thread.start()
        logger.info("Serveur récepteur navigateur démarré sur %s", self.base_url)

    def stop(self) -> None:
        """Arrête proprement le serveur HTTP et libère le socket."""
        try:
            self.shutdown()
            self.server_close()
        except Exception as exc:
            logger.debug("Erreur lors de l'arrêt du serveur récepteur : %s", exc)
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        logger.info("Serveur récepteur navigateur arrêté.")

    def __enter__(self) -> "BrowserTelemetryServer":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()

