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

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logger = logging.getLogger("Exocortex.Launcher")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def run_init_models() -> None:
    """Provisionne les modèles GGUF locaux de ./models/ dans Ollama avec limitation num_ctx."""
    logger.info("=== Initialisation & Provisioning des Modèles GGUF Locaux ===")
    from src.llm.ollama_client import llm_client

    status = llm_client.ensure_local_gguf_models()
    logger.info("Statut du provisioning des modèles : %s", status)


def run_ingest_takeout(limit: Optional[int] = None) -> None:
    """Lance l'ingestion complète des archives Google Takeout (Module 1)."""
    logger.info("=== Lancement de l'Ingestion Google Takeout ===")
    from src.ingestors.takeout_ingestor import TakeoutIngestor

    ingestor = TakeoutIngestor()
    result = ingestor.run(max_distill_sessions=limit)
    logger.info("Ingestion Takeout achevée avec succès : %s", result)


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
    from src.llm.ollama_client import llm_client

    if llm_client.is_alive():
        llm_client.ensure_local_gguf_models()

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


def run_kanban_status(project_id: Optional[str] = None) -> None:
    """Affiche dans le terminal le tableau récapitulatif du Kanban et régénère AGENT_QUEUE.md."""
    logger.info("=== État Exécutif du Kanban & File Agent (Module 7) ===")
    from src.consolidators.kanban_engine import kanban_engine

    kanban_engine.sync_existing_tech_specs()
    manifest_path = kanban_engine.compile_agent_queue_manifest()

    projects = kanban_engine.db.get_projects()
    if project_id:
        projects = [p for p in projects if p["project_id"] == project_id]
        if not projects:
            print(f"Aucun projet trouvé avec l'identifiant '{project_id}'.")
            return

    print("\n=======================================================")
    print("=== ÉTAT EXÉCUTIF DU KANBAN MULTI-PROJETS ===")
    print("=======================================================\n")

    for p in projects:
        pid = p["project_id"]
        pname = p["name"]
        tasks = kanban_engine.db.get_kanban_tasks(project_id=pid)

        radar_c = sum(1 for t in tasks if t["status"] == "radar")
        needs_spec_c = sum(1 for t in tasks if t["status"] == "needs_spec")
        ready_c = sum(1 for t in tasks if t["status"] == "ready_for_agent")
        in_prog_c = sum(1 for t in tasks if t["status"] == "in_progress")
        done_c = sum(1 for t in tasks if t["status"] == "done")
        icebox_c = sum(1 for t in tasks if t["status"] == "icebox")

        print(f"📁 PROJET : {pname} [{pid}]")
        print(f"   📡 Radar: {radar_c} | 📝 Spec: {needs_spec_c} | 🎯 Ready: {ready_c} | ⚙️ En cours: {in_prog_c} | ✅ Done: {done_c} | 🧊 Frigo: {icebox_c}")

        active = [t for t in tasks if t["status"] in ("in_progress", "ready_for_agent")]
        if active:
            print("   --- File Active ---")
            for t in active:
                icon = "⚙️" if t["status"] == "in_progress" else "🎯"
                print(f"   {icon} [{t['task_id']}] (P{t['priority']} | {t['complexity']}) {t['title']} ({t['component_tag']})")
        print()

    print(f"Manifeste d'exécution synchronisé : {manifest_path}\n")


def run_next_task(project_id: Optional[str] = None) -> None:
    """
    Sélectionne la tâche ready_for_agent la plus prioritaire,
    la passe en in_progress, actualise AGENT_QUEUE.md et imprime le prompt de l'agent sur stdout.
    """
    from src.consolidators.kanban_engine import kanban_engine

    tasks = kanban_engine.db.get_kanban_tasks(project_id=project_id, statuses=["ready_for_agent"])
    if not tasks:
        print(f"Aucune tâche prête dans la file{' pour le projet ' + project_id if project_id else ''}.")
        return

    # Tri par priorité croissante (P1 avant P4), puis updated_at ASC
    tasks.sort(key=lambda x: (x["priority"], x["updated_at"]))
    next_task = tasks[0]
    tid = next_task["task_id"]

    kanban_engine.db.update_kanban_task_status(tid, "in_progress")
    kanban_engine.compile_agent_queue_manifest()

    print(f"\n🚀 [TASK DÉPILÉE] : {tid} — {next_task['title']} (P{next_task['priority']} | {next_task['complexity']})")
    if next_task.get("spec_file_path"):
        print(f"📄 Spécification : {next_task['spec_file_path']}\n")
    print("=" * 60)
    print("=== PROMPT D'EXÉCUTION POUR L'AGENT CODEUR ===")
    print("=" * 60)
    coder_prompt = kanban_engine.extract_coder_prompt_from_spec(tid)
    print(coder_prompt)
    print("=" * 60 + "\n")


def run_complete_task(task_id: str) -> None:
    """Valide la fin de développement d'une tâche, la passe en 'done' et met à jour AGENT_QUEUE.md."""
    from src.consolidators.kanban_engine import kanban_engine

    task = kanban_engine.db.get_kanban_task_by_id(task_id)
    if not task:
        print(f"Tâche '{task_id}' introuvable dans la base de données.")
        return

    kanban_engine.db.update_kanban_task_status(task_id, "done")
    kanban_engine.compile_agent_queue_manifest()
    print(f"✅ Tâche '{task_id}' ({task['title']}) marquée comme terminée avec succès !")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exocortex & Télémétrie Cognitive — Orchestrateur Principal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation :
  python run_exocortex.py --init-models       # Provisionne les modèles GGUF locaux dans Ollama
  python run_exocortex.py --ingest-takeout    # Ingestion complète Takeout (Module 1)
  python run_exocortex.py --daemon            # Démarre le démon de capture d'activité temps réel
  python run_exocortex.py --consolidate       # Exécute la consolidation nocturne bi-modèle
  python run_exocortex.py --compile-drive     # Met à jour les 4 méga-fichiers Google Drive Sync
  python run_exocortex.py --hotkey            # Démarre l'écoute du raccourci global Alt+Espace
  python run_exocortex.py --dashboard         # Ouvre le dashboard Streamlit 'Bandeur de Stats'
  python run_exocortex.py --all               # Lance démons de fond + dashboard au premier plan
  python run_exocortex.py --kanban-status     # Affiche l'état du Kanban et actualise AGENT_QUEUE.md
  python run_exocortex.py --next-task         # Dépile la tâche prête la plus prioritaire
  python run_exocortex.py --complete-task EXO-005  # Marque la tâche EXO-005 comme terminée
        """,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--init-models", action="store_true", help="Provisionne les modèles GGUF locaux dans Ollama.")
    group.add_argument("--ingest-takeout", action="store_true", help="Lance l'ingestion complète des archives Google Takeout.")
    group.add_argument("--daemon", action="store_true", help="Lance le démon de télémétrie temps réel Win32.")
    group.add_argument("--consolidate", action="store_true", help="Lance la consolidation nocturne bi-modèle.")
    group.add_argument("--compile-drive", action="store_true", help="Compile les 4 méga-documents Google Drive.")
    group.add_argument("--hotkey", action="store_true", help="Lance le démon de raccourci global Alt+Espace.")
    group.add_argument("--dashboard", action="store_true", help="Lance le dashboard analytique Streamlit.")
    group.add_argument("--all", action="store_true", help="Lance tous les démons d'arrière-plan et le dashboard.")
    group.add_argument("--kanban-status", action="store_true", help="Affiche l'état des tickets du Kanban et actualise AGENT_QUEUE.md.")
    group.add_argument("--next-task", action="store_true", help="Dépile et affiche la tâche la plus prioritaire prête pour l'agent codeur.")
    group.add_argument("--complete-task", type=str, metavar="TASK_ID", help="Marque une tâche comme terminée.")

    parser.add_argument("--date", type=str, default=None, help="Date optionnelle pour la consolidation (YYYY-MM-DD).")
    parser.add_argument("--limit", type=int, default=None, help="Limite optionnelle de sessions à distiller lors du Takeout.")
    parser.add_argument("--project", type=str, default=None, help="Filtrer par project_id (ex: exocortex).")

    args = parser.parse_args()

    # S'assure que l'arborescence et la base sont prêtes
    settings.ensure_directories()

    if args.init_models:
        run_init_models()
    elif args.ingest_takeout:
        run_ingest_takeout(args.limit)
    elif args.daemon:
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
    elif args.kanban_status:
        run_kanban_status(args.project)
    elif args.next_task:
        run_next_task(args.project)
    elif args.complete_task:
        run_complete_task(args.complete_task)


if __name__ == "__main__":
    main()
