"""
Orchestrateur Principal de l'Exocortex & Télémétrie Cognitive.
Point d'entrée unique pour piloter l'ensemble des modules du système :
- Démon de télémétrie temps réel Win32 (Module 2)
- Consolidateur nocturne bi-modèle (Module 3)
- Compilateur Google Drive (Module 4)
- Injecteur de contexte local Alt+Espace (Module 5)
- Dashboard analytique Streamlit "Bandeur de Stats" (Module 6)
"""

from __future__ import annotations

import argparse
import logging
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.config import settings

logger = logging.getLogger("Exocortex.Launcher")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def run_daemon() -> None:
    """Lance le démon de télémétrie Windows en temps réel (0 Mo VRAM, < 2% CPU)."""
    logger.info("=== Lancement du Démon de Télémétrie Temps Réel ===")
    from src.daemons.telemetry_daemon import TelemetryDaemon

    daemon = TelemetryDaemon()
    daemon.run_loop()


def run_consolidate(date_str: Optional[str] = None) -> None:
    """Lance le consolidateur nocturne (Sommeil paradoxal en 3 passes VRAM)."""
    logger.info("=== Lancement du Consolidateur Nocturne ===")
    from src.consolidators.night_consolidator import NightConsolidator

    target_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    consolidator = NightConsolidator()
    res = consolidator.consolidate(target_date=target_date)
    logger.info("Consolidation terminée avec succès : %s", res)


def run_compile_drive() -> None:
    """Compile et synchronise les 4 méga-documents Google Drive."""
    logger.info("=== Lancement du Compilateur Google Drive ===")
    from src.consolidators.drive_compiler import DriveCompiler

    compiler = DriveCompiler()
    generated = compiler.compile_all()
    for name, path in generated.items():
        p = Path(path)
        logger.info("Fichier synchronisé : %s (%d octets)", p.name, p.stat().st_size)


def run_hotkey() -> None:
    """Lance le listener global Alt+Espace (Injecteur Hippocampe)."""
    logger.info("=== Lancement de l'Injecteur Hippocampe (Alt+Espace) ===")
    from src.daemons.hippocampus_hotkey import HippocampusInjector

    injector = HippocampusInjector()
    injector.run_daemon()


def run_dashboard() -> None:
    """Lance le serveur Streamlit du Dashboard 'Bandeur de Stats'."""
    dashboard_script = _PROJECT_ROOT / "src" / "dashboard" / "app.py"
    logger.info("=== Lancement du Dashboard Streamlit 'Bandeur de Stats' ===")
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(dashboard_script),
        "--server.headless=false",
        "--theme.base=dark",
    ]
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        logger.info("Arrêt du Dashboard Streamlit.")


def run_all() -> None:
    """
    Lance l'ensemble de l'écosystème Exocortex :
    1. Démon de télémétrie (processus séparé)
    2. Démon de hotkey Alt+Espace (processus séparé)
    3. Dashboard Streamlit (au premier plan)
    Gère l'arrêt propre de tous les processus fils lors d'un Ctrl+C.
    """
    logger.info("============================================================")
    logger.info("=== DÉMARRAGE DE LA SUITE COMPLÈTE EXOCORTEX & TÉLÉMÉTRIE ===")
    logger.info("============================================================")

    processes: List[subprocess.Popen] = []

    # 1. Démon de télémétrie
    telemetry_cmd = [sys.executable, "-m", "src.daemons.telemetry_daemon"]
    p_telemetry = subprocess.Popen(telemetry_cmd, cwd=str(_PROJECT_ROOT))
    processes.append(p_telemetry)
    logger.info("Démon de télémétrie démarré (PID %d).", p_telemetry.pid)

    # 2. Démon Hotkey
    hotkey_cmd = [sys.executable, "-m", "src.daemons.hippocampus_hotkey"]
    p_hotkey = subprocess.Popen(hotkey_cmd, cwd=str(_PROJECT_ROOT))
    processes.append(p_hotkey)
    logger.info("Injecteur Alt+Espace démarré (PID %d).", p_hotkey.pid)

    # 3. Dashboard Streamlit (premier plan)
    dashboard_script = _PROJECT_ROOT / "src" / "dashboard" / "app.py"
    dashboard_cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(dashboard_script),
        "--server.headless=false",
        "--theme.base=dark",
    ]

    try:
        logger.info("Lancement du Dashboard Streamlit...")
        subprocess.run(dashboard_cmd, cwd=str(_PROJECT_ROOT))
    except KeyboardInterrupt:
        logger.info("Interruption détectée, arrêt propre des démons...")
    finally:
        for p in processes:
            try:
                p.terminate()
                p.wait(timeout=3)
            except Exception:
                p.kill()
        logger.info("Tous les démons Exocortex ont été arrêtés.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exocortex & Télémétrie Cognitive — Orchestrateur Principal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation :
  python run_exocortex.py --daemon            # Démarre le démon de capture d'activité temps réel
  python run_exocortex.py --consolidate       # Exécute la consolidation nocturne bi-modèle
  python run_exocortex.py --compile-drive     # Met à jour les 4 méga-fichiers Google Drive Sync
  python run_exocortex.py --hotkey            # Démarre l'écoute du raccourci global Alt+Espace
  python run_exocortex.py --dashboard         # Ouvre le dashboard Streamlit 'Bandeur de Stats'
  python run_exocortex.py --all               # Lance démons de fond + dashboard au premier plan
        """,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--daemon", action="store_true", help="Lance le démon de télémétrie temps réel Win32.")
    group.add_argument("--consolidate", action="store_true", help="Lance la consolidation nocturne bi-modèle.")
    group.add_argument("--compile-drive", action="store_true", help="Compile les 4 méga-documents Google Drive.")
    group.add_argument("--hotkey", action="store_true", help="Lance le démon de raccourci global Alt+Espace.")
    group.add_argument("--dashboard", action="store_true", help="Lance le dashboard analytique Streamlit.")
    group.add_argument("--all", action="store_true", help="Lance tous les démons d'arrière-plan et le dashboard.")

    parser.add_argument("--date", type=str, default=None, help="Date optionnelle pour la consolidation (YYYY-MM-DD).")

    args = parser.parse_args()

    # S'assure que l'arborescence et la base sont prêtes
    settings.ensure_directories()

    if args.daemon:
        run_daemon()
    elif args.consolidate:
        run_consolidate(args.date)
    elif args.compile_drive:
        run_compile_drive()
    elif args.hotkey:
        run_hotkey()
    elif args.dashboard:
        run_dashboard()
    elif args.all:
        run_all()


if __name__ == "__main__":
    main()
