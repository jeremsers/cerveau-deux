"""
Sonde Contextuelle Git & IDE (Module 2 - v0.3.5 / EXO-011).
Inspecte l'état des dépôts locaux lors de l'utilisation d'un IDE ou d'un terminal
avec un cache TTL de 30 secondes pour garantir une charge CPU < 0.5% (0 Mo VRAM).
Fournit également l'utilitaire sanitize_url pour l'épuration des paramètres de tracking.
"""

from __future__ import annotations

import logging
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import psutil

logger = logging.getLogger("Exocortex.GitIDEProbe")

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Exécutables d'IDE et de terminaux sous surveillance
IDE_TERMINAL_EXECUTABLES = {
    "code.exe",
    "pycharm64.exe",
    "windowsterminal.exe",
    "powershell.exe",
    "cmd.exe",
    "cursor.exe",
    "windsurf.exe",
}

# Paramètres de tracking URL à épurer
TRACKING_QUERY_PARAMS = {
    "gclid",
    "fbclid",
    "igshid",
    "mc_eid",
    "msclkid",
    "_ga",
    "_gl",
    "ref",
    "ref_src",
}


def sanitize_url(raw_url: str) -> str:
    """
    Supprime les paramètres de tracking (utm_*, gclid, fbclid, etc.)
    et les fragments inutiles d'une URL tout en préservant le reste des query params.
    """
    if not raw_url:
        return ""

    raw_url = raw_url.strip()
    try:
        parsed = urlparse(raw_url)
        if not parsed.scheme and not parsed.netloc:
            # URL relative ou fragment brut
            return raw_url

        query_items = parse_qsl(parsed.query, keep_blank_values=False)
        clean_items = [
            (k, v)
            for k, v in query_items
            if not k.lower().startswith("utm_") and k.lower() not in TRACKING_QUERY_PARAMS
        ]
        clean_query = urlencode(clean_items)

        cleaned = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            clean_query,
            "",  # Suppression du fragment
        ))
        return cleaned.rstrip("?")
    except Exception as exc:
        logger.debug("Erreur lors de la sanitization de l'URL '%s' : %s", raw_url, exc)
        return raw_url


class GitIDEProbe:
    """
    Sonde passive non-bloquante pour environnements de développement.
    Extrait le dépôt actif, la branche courante et le différentiel git (+X/-Y)
    avec mise en cache TTL pour minimiser les sous-processus Win32.
    """

    def __init__(self, cache_ttl: float = 30.0) -> None:
        self.cache_ttl = cache_ttl
        # Cache : repo_path_str -> (timestamp, formatted_info)
        self._cache: Dict[str, Tuple[float, str]] = {}

    def is_ide_or_terminal(self, executable: str) -> bool:
        """Vérifie si l'exécutable correspond à un éditeur de code ou terminal."""
        exe_low = executable.lower()
        if exe_low in IDE_TERMINAL_EXECUTABLES:
            return True
        for target in IDE_TERMINAL_EXECUTABLES:
            if target.replace(".exe", "") in exe_low:
                return True
        return False

    def probe_active_ide(
        self,
        pid: int,
        executable: str,
        window_title: str,
        known_projects: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[str]:
        """
        Détermine si l'application active est un IDE/terminal lié à un dépôt Git
        et retourne la chaîne formatée 'git:{repo_name}:{branch} (+{insertions}/-{deletions})'.
        """
        if not self.is_ide_or_terminal(executable):
            return None

        target_repo = self._resolve_repo_path(pid, window_title, known_projects or [])
        if not target_repo:
            return None

        repo_key = str(target_repo.resolve())
        now = time.time()

        # Consultation du cache TTL
        if repo_key in self._cache:
            cached_ts, cached_val = self._cache[repo_key]
            if (now - cached_ts) < self.cache_ttl:
                return cached_val

        # Exécution de git sous-jacente avec timeout strict 0.5s
        formatted_info = self._query_git_state(target_repo)
        if formatted_info:
            self._cache[repo_key] = (now, formatted_info)
            return formatted_info

        return None

    def _resolve_repo_path(
        self,
        pid: int,
        window_title: str,
        known_projects: List[Dict[str, Any]],
    ) -> Optional[Path]:
        """Tente de résoudre le répertoire racine du dépôt Git actif."""
        title_low = window_title.lower()

        # 1. Correspondance avec la liste des projets connus (base SQLite)
        for proj in known_projects:
            rpath_str = proj.get("repo_path")
            if not rpath_str:
                continue
            rpath = Path(rpath_str)
            pname = proj.get("name", "")
            if rpath.name.lower() in title_low or (pname and pname.lower() in title_low):
                if (rpath / ".git").exists():
                    return rpath

        # 2. Inspection du CWD du processus Win32 via psutil
        if pid > 0 and psutil.pid_exists(pid):
            try:
                proc = psutil.Process(pid)
                cwd = Path(proc.cwd())
                curr: Optional[Path] = cwd
                while curr and curr != curr.parent:
                    if (curr / ".git").exists():
                        return curr
                    curr = curr.parent
            except (psutil.NoSuchProcess, psutil.AccessDenied, Exception):
                pass

        # 3. Correspondance avec le projet local de travail courant (_PROJECT_ROOT)
        if (_PROJECT_ROOT / ".git").exists():
            root_name = _PROJECT_ROOT.name.lower()
            if root_name in title_low:
                return _PROJECT_ROOT

        return None

    def _query_git_state(self, repo_dir: Path) -> Optional[str]:
        """Interroge git rev-parse et git diff --shortstat sans fenêtre console."""
        creationflags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
        repo_name = repo_dir.name

        try:
            # 1. Branche courante
            branch_cmd = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=str(repo_dir),
                capture_output=True,
                text=True,
                timeout=0.5,
                creationflags=creationflags,
            )
            branch = branch_cmd.stdout.strip() or "unknown"
            if branch == "HEAD":
                # Tête détachée : récupérer le hash court
                commit_cmd = subprocess.run(
                    ["git", "rev-parse", "--short", "HEAD"],
                    cwd=str(repo_dir),
                    capture_output=True,
                    text=True,
                    timeout=0.5,
                    creationflags=creationflags,
                )
                branch = commit_cmd.stdout.strip() or "detached"

            # 2. Statut des modifications locales
            diff_cmd = subprocess.run(
                ["git", "diff", "--shortstat"],
                cwd=str(repo_dir),
                capture_output=True,
                text=True,
                timeout=0.5,
                creationflags=creationflags,
            )
            diff_out = diff_cmd.stdout.strip()
            insertions = 0
            deletions = 0
            if diff_out:
                ins_match = re.search(r"(\d+)\s+insertion", diff_out)
                del_match = re.search(r"(\d+)\s+deletion", diff_out)
                if ins_match:
                    insertions = int(ins_match.group(1))
                if del_match:
                    deletions = int(del_match.group(1))

            return f"git:{repo_name}:{branch} (+{insertions}/-{deletions})"

        except subprocess.TimeoutExpired:
            logger.debug("Timeout lors de l'exécution git sur %s", repo_dir)
            return f"git:{repo_name}:unknown (+0/-0)"
        except Exception as exc:
            logger.debug("Erreur git sur %s : %s", repo_dir, exc)
            return None

