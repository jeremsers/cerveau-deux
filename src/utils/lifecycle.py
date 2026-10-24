"""
Arrêt propre des processus Exocortex sous Windows (v0.5.6, E4).
Sous Windows, Stop-Process / TerminateProcess ne délivre aucun signal : le gestionnaire SIGTERM du
démon ne s'exécute pas et la fenêtre en cours est perdue. L'arrêt passe donc d'abord par un
fichier-signal surveillé par les démons (sauvegarde puis sortie), puis par un arrêt forcé des
seuls processus encore vivants.
"""

from __future__ import annotations

import logging
import os
import time
from typing import List

import psutil

from src.config import settings

logger = logging.getLogger("Exocortex.Lifecycle")

# Motifs de ligne de commande des processus de l'Exocortex
EXOCORTEX_PROCESS_MARKERS = (
    "src.daemons.telemetry_daemon",
    "src.daemons.hippocampus_hotkey",
    "src.api.server",
    "run_exocortex.py --web",
    "run_exocortex.py --all",
    "run_exocortex.py --daemon",
    "run_exocortex.py --hotkey",
    "run_exocortex.py --dashboard",
    "dashboard/app.py",
    "dashboard\\app.py",
)


def stop_requested() -> bool:
    return settings.STOP_FLAG_PATH.exists()


def clear_stop_flag() -> None:
    settings.STOP_FLAG_PATH.unlink(missing_ok=True)


def request_stop() -> None:
    settings.STOP_FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
    settings.STOP_FLAG_PATH.write_text(str(time.time()), encoding="utf-8")


def find_exocortex_processes() -> List[psutil.Process]:
    """Processus Python de l'Exocortex en cours d'exécution (hors processus courant)."""
    me = os.getpid()
    found: List[psutil.Process] = []
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if proc.info["pid"] == me or "python" not in (proc.info["name"] or "").lower():
                continue
            cmdline = " ".join(proc.info["cmdline"] or [])
            if any(marker in cmdline for marker in EXOCORTEX_PROCESS_MARKERS):
                found.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found


def _is_daemon(proc: psutil.Process) -> bool:
    try:
        cmdline = " ".join(proc.cmdline())
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False
    return any(m in cmdline for m in ("telemetry_daemon", "hippocampus_hotkey", "--daemon", "--hotkey"))


def stop_all(grace_sec: float = 10.0) -> int:
    """
    Demande l'arrêt propre (fichier-signal), attend au plus grace_sec que les démons sauvegardent
    leur fenêtre en cours et sortent, puis arrête de force les processus restants (Streamlit,
    serveur web, démons bloqués). Retourne le nombre de processus arrêtés de force.
    """
    request_stop()
    deadline = time.time() + grace_sec
    remaining = find_exocortex_processes()
    # Seuls les démons surveillent le signal ; le serveur web et Streamlit sont arrêtés ensuite
    while any(_is_daemon(p) for p in remaining) and time.time() < deadline:
        time.sleep(0.5)
        remaining = [p for p in remaining if p.is_running()]
    forced = 0
    for proc in remaining:
        try:
            if proc.is_running():
                proc.terminate()
                forced += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    psutil.wait_procs(remaining, timeout=5)
    clear_stop_flag()
    logger.info("Arrêt de l'Exocortex : %d processus arrêté(s) de force après l'arrêt propre des démons.", forced)
    return forced
