"""
Filtre de confidentialité commun au démon Win32 et au récepteur navigateur (v0.5.2, D7).
Remplace la recherche par sous-chaînes ("login" écartait login_flow.ts, "bank" écartait "Bankai")
par une correspondance en mots entiers sur des marques et marqueurs ciblés, et une
correspondance par domaine sur les URL.
"""

from __future__ import annotations

import re
import unicodedata
from functools import lru_cache
from typing import Iterable, Optional, Tuple
from urllib.parse import urlparse

from src.config import settings


def _fold(text: str) -> str:
    """Minuscules sans accents, pour une comparaison insensible à la casse et aux diacritiques."""
    norm = unicodedata.normalize("NFKD", text or "")
    return "".join(c for c in norm if not unicodedata.combining(c)).lower()


@lru_cache(maxsize=8)
def _compile_terms(terms: Tuple[str, ...]) -> Optional[re.Pattern]:
    folded = sorted({_fold(t).strip() for t in terms if t and t.strip()}, key=len, reverse=True)
    if not folded:
        return None
    # Bornes de mot : ni lettre, ni chiffre, ni '_' de part et d'autre du terme
    alternation = "|".join(re.escape(t) for t in folded)
    return re.compile(rf"(?<![\w])(?:{alternation})(?![\w])")


def contains_sensitive_term(*texts: Optional[str]) -> bool:
    """Vrai si l'un des textes contient un terme de TITLE_BLACKLIST en mot entier."""
    pattern = _compile_terms(tuple(settings.TITLE_BLACKLIST))
    if pattern is None:
        return False
    return any(text and pattern.search(_fold(text)) for text in texts)


# Divulgation de secret dans un texte libre (tour de chat) : on vise la valeur, pas le sujet.
# "Voici mon mot de passe root : X" est rejeté ; "comment hacher un password avec argon2" ne l'est pas.
_SECRET_DISCLOSURE_PATTERNS = [
    re.compile(r"(?<![\w])(?:mot de passe|mdp|password|passwd|passphrase|pin)(?![\w])[^\n:=]{0,25}[:=]\s*\S{4,}"),
    re.compile(r"(?<![\w])(?:sk-[a-z0-9_-]{20,}|ghp_[a-z0-9]{30,}|akia[0-9a-z]{16}|xox[baprs]-[a-z0-9-]{10,})"),
    re.compile(r"-----begin [a-z ]*private key-----"),
]


def contains_secret_disclosure(*texts: Optional[str]) -> bool:
    """Vrai si un texte semble contenir la valeur d'un secret (mot de passe, clé d'API, clé privée)."""
    return any(text and any(p.search(_fold(text)) for p in _SECRET_DISCLOSURE_PATTERNS) for text in texts)


def is_sensitive_url(url: Optional[str], domains: Optional[Iterable[str]] = None) -> bool:
    """Vrai si le nom d'hôte de l'URL est un domaine sensible ou l'un de ses sous-domaines."""
    if not url:
        return False
    candidate = url if "://" in url else f"https://{url}"
    host = (urlparse(candidate).hostname or "").lower().rstrip(".")
    if not host:
        return False
    for domain in domains if domains is not None else settings.SENSITIVE_DOMAINS:
        d = domain.lower().strip().lstrip(".")
        if d and (host == d or host.endswith(f".{d}")):
            return True
    return False


def is_blacklisted_executable(executable: Optional[str]) -> bool:
    """Correspondance exacte (insensible à la casse) sur le nom de l'exécutable."""
    exe = (executable or "").strip().lower()
    return bool(exe) and exe in {e.lower() for e in settings.EXE_BLACKLIST}


def is_browser_executable(executable: Optional[str]) -> bool:
    exe = (executable or "").lower()
    return any(name in exe for name in settings.BROWSER_EXECUTABLES)


def is_sensitive_window(executable: Optional[str], window_title: Optional[str], url: Optional[str] = None) -> bool:
    """Décision unique d'exclusion d'une fenêtre ou d'un onglet de la télémétrie."""
    return (
        is_blacklisted_executable(executable)
        or contains_sensitive_term(window_title)
        or is_sensitive_url(url)
    )
