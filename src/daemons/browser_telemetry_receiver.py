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

logger = logging.getLogger("Exocortex.BrowserReceiver")


def is_payload_blacklisted(*texts: Optional[str]) -> bool:
    """
    Vérifie si l'un des textes fournis contient un terme de la liste noire de confidentialité
    (titres interdits, mots de passe, gestionnaires de secrets, établissements bancaires).
    """
    for t in texts:
        if not t:
            continue
        t_low = t.lower()
        for b_title in settings.TITLE_BLACKLIST:
            if b_title.lower() in t_low:
                return True
        for b_exe in settings.EXE_BLACKLIST:
            clean_exe = b_exe.lower().replace(".exe", "")
            if clean_exe in t_low:
                return True
    return False


class BrowserTelemetryRequestHandler(BaseHTTPRequestHandler):
    """Gestionnaire de requêtes HTTP pour le pont d'extension navigateur."""

    server: "BrowserTelemetryServer"  # Type hint pour l'instance parente

    def log_message(self, format: str, *args: Any) -> None:
        """Délègue les logs HTTP au logger standard sans polluer stdout."""
        logger.debug("%s - " + format, self.address_string(), *args)

    def _send_cors_headers(self) -> None:
        """Injecte les entêtes CORS pour autoriser les requêtes cross-origin de l'extension."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self) -> None:
        """Gère les requêtes préliminaires CORS (preflight)."""
        self.send_response(HTTPStatus.NO_CONTENT)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self) -> None:
        """Traite les flux /telemetry/tab et /telemetry/chat_turn."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            self._send_json_error(HTTPStatus.BAD_REQUEST, "Payload vide")
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
        if is_payload_blacklisted(url, title, h1, domain):
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

        daemon = server.daemon
        if daemon and daemon.current_state:
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
        if is_payload_blacklisted(user_prompt, ai_response, url):
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

