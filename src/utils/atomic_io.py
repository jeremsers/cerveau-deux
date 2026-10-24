"""
Écriture atomique de fichiers texte (v0.5.6, G6).
Le contenu est écrit dans un fichier temporaire du même dossier puis substitué par os.replace :
une interruption (coupure, crash, arrêt forcé) laisse soit l'ancien fichier intact, soit le
nouveau complet — jamais une note tronquée que le Vault Doctor prendrait ensuite pour un échec.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> Path:
    """Écrit `content` dans `path` de façon atomique et retourne `path`."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="") as tmp:
            tmp.write(content)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise
    return path
