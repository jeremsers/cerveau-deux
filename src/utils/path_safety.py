"""
Garde-fous de confinement des chemins (v0.5.1).
Toute écriture ou lecture dont le chemin dérive d'une entrée externe (requête HTTP, sortie LLM,
frontmatter) doit passer par resolve_within() pour garantir qu'elle reste sous son dossier racine.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Iterable, Optional


class UnsafePathError(ValueError):
    """Levée lorsqu'un chemin résolu sort de son dossier racine autorisé."""


def safe_slug(text: str, max_len: int = 80, fallback: str = "note") -> str:
    """Slug kebab-case ASCII strict : aucun séparateur de chemin, aucun '..' possible."""
    norm = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9_]+", "-", norm.lower()).strip("-_")
    return slug[:max_len].strip("-_") or fallback


def is_within(path: Path, root: Path) -> bool:
    """Vrai si `path`, une fois résolu, est `root` ou l'un de ses descendants."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def resolve_within(root: Path, *parts: str) -> Path:
    """
    Construit root / parts et vérifie que le résultat résolu reste sous root.
    Rejette aussi les composants contenant un séparateur (/, \\) ou valant '..'.
    """
    for part in parts:
        if not part or part in (".", "..") or "/" in part or "\\" in part or "\x00" in part:
            raise UnsafePathError(f"Composant de chemin refusé : {part!r}")
    candidate = root.joinpath(*parts)
    if not is_within(candidate, root):
        raise UnsafePathError(f"Chemin hors du dossier autorisé : {candidate}")
    return candidate


def is_under_any(path: Path, roots: Iterable[Path]) -> Optional[Path]:
    """Retourne la racine contenant `path`, ou None si aucune ne la contient."""
    for root in roots:
        if is_within(path, root):
            return root
    return None
