"""
Jetons locaux d'authentification (v0.5.2, D1/D4).
Un jeton aléatoire par service est conservé dans _System_Buffer/ (hors dépôt Git). Une page web
tierce ne peut ni le lire (aucun en-tête CORS ne l'y autorise) ni envoyer l'en-tête qui le porte
sans pré-vol CORS, lui-même refusé.
"""

from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import Optional

from src.config import settings

TOKEN_HEADER = "X-Exocortex-Token"


def _token_path(service: str) -> Path:
    return settings.SYSTEM_BUFFER_DIR / f"{service}_token"


def get_local_token(service: str) -> str:
    """
    Retourne le jeton du service ('api' ou 'browser_receiver').
    Priorité : variable EXOCORTEX_<SERVICE>_TOKEN, puis fichier, sinon création.
    """
    env_value = os.getenv(f"EXOCORTEX_{service.upper()}_TOKEN", "").strip()
    if env_value:
        return env_value
    path = _token_path(service)
    try:
        existing = path.read_text(encoding="utf-8").strip()
        if existing:
            return existing
    except FileNotFoundError:
        pass
    token = secrets.token_urlsafe(32)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(token, encoding="utf-8")
    return token


def token_matches(service: str, provided: Optional[str]) -> bool:
    """Comparaison à temps constant du jeton fourni avec le jeton attendu."""
    return bool(provided) and secrets.compare_digest(provided.strip(), get_local_token(service))
