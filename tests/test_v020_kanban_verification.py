"""
Suite de tests de validation pour la version v0.2.0-core.
Vérifie la conformité intégrale du Module 7 : Kanban Exécutif & Pont Cloud SOTA :
1. CRUD de projets dynamiques et génération d'identifiants séquentiels (TEST-001, TEST-002).
2. Indexation idempotente des spécifications historiques de 'tech specs/' en tâches terminées (done).
3. Cycle de vie complet : radar -> needs_spec -> Context-Pack SOTA -> attachement de spec -> ready_for_agent -> in_progress -> done.
4. Commandes CLI d'orchestration pour l'agent codeur (--kanban-status, --next-task, --complete-task).
"""

from __future__ import annotations

import io
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pytest

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.config import settings
from src.database.db_manager import DBManager, KanbanTaskRecord, ProjectRecord
from src.consolidators.kanban_engine import kanban_engine
from run_exocortex import run_complete_task, run_kanban_status, run_next_task


def test_project_crud_and_id_generation():
    """
    Vérifie la création dynamique d'un projet dans la table projects,
    et la génération séquentielle et déterministe de ses identifiants de tickets.
    """
    db = kanban_engine.db

    # 1. Vérification du projet racine exocortex
    exo_proj = db.get_project_by_id("exocortex")
    assert exo_proj is not None, "Le projet 'exocortex' doit être amorcé par défaut."
    assert exo_proj["prefix"] == "EXO"

    # 2. Création d'un nouveau projet dynamique
    test_pid = "test-project-v020"
    test_proj = ProjectRecord(
        project_id=test_pid,
        name="Test Projet Kanban",
        prefix="TST",
        repo_path=str(_ROOT),
        description="Projet éphémère pour les tests automatisés v0.2.0.",
    )
    db.upsert_project(test_proj)

    fetched = db.get_project_by_id(test_pid)
    assert fetched is not None
    assert fetched["name"] == "Test Projet Kanban"
    assert fetched["prefix"] == "TST"

    try:
        # 3. Génération du premier ID
        id_1 = db.generate_next_task_id(test_pid)
        assert id_1 == "TST-001", f"Attendu 'TST-001', obtenu '{id_1}'"

        # Insertion de la première tâche
        task_1 = KanbanTaskRecord(
            task_id=id_1,
            project_id=test_pid,
            component_tag="core",
            title="Première tâche de test",
            status="radar",
        )
        db.upsert_kanban_task(task_1)

        # 4. Génération du deuxième ID
        id_2 = db.generate_next_task_id(test_pid)
        assert id_2 == "TST-002", f"Attendu 'TST-002', obtenu '{id_2}'"

        # Insertion de la deuxième tâche
        task_2 = KanbanTaskRecord(
            task_id=id_2,
            project_id=test_pid,
            component_tag="core",
            title="Deuxième tâche de test",
            status="radar",
        )
        db.upsert_kanban_task(task_2)

        # 5. Récupération et vérification
        tasks = db.get_kanban_tasks(project_id=test_pid)
        assert len(tasks) == 2
        task_ids = [t["task_id"] for t in tasks]
        assert "TST-001" in task_ids
        assert "TST-002" in task_ids

    finally:
        # Nettoyage
        db.delete_kanban_task("TST-001")
        db.delete_kanban_task("TST-002")
        with db.get_connection() as conn:
            conn.execute("DELETE FROM projects WHERE project_id = ?;", (test_pid,))


def test_sync_existing_tech_specs():
    """
    Vérifie l'indexation automatique des fichiers historiques du dossier 'tech specs/'
    dans la colonne 'done' du projet 'exocortex', ainsi que son idempotence stricte.
    """
    db = kanban_engine.db

    # 1. Exécution de la synchronisation
    count_synced = kanban_engine.sync_existing_tech_specs()
    assert isinstance(count_synced, int)

    # 2. Vérification de la présence des specs historiques
    done_tasks = db.get_kanban_tasks(project_id="exocortex", statuses=["done"])
    assert len(done_tasks) >= 5, f"Au moins 5 specs historiques attendues, trouvées : {len(done_tasks)}"

    # Vérification des métadonnées
    for t in done_tasks:
        assert t["component_tag"] == "core-architecture"
        assert t["status"] == "done"
        assert t["spec_file_path"] is not None
        assert Path(t["spec_file_path"]).exists()

    # 3. Vérification de l'idempotence (deuxième exécution ne doit rien rajouter)
    count_second_run = kanban_engine.sync_existing_tech_specs()
    assert count_second_run == 0, f"La deuxième synchronisation doit être sans effet (0), obtenu : {count_second_run}"


def test_ticket_lifecycle_and_context_pack():
    """
    Vérifie le cycle de vie complet d'un ticket Kanban :
    radar -> needs_spec -> génération Context-Pack -> retour SOTA (attach_spec) -> ready_for_agent -> in_progress -> done.
    """
    db = kanban_engine.db
    test_title = "Module 7 Test Ticket Lifecycle"
    test_tag = "kanban-engine"
    test_pitch = "Concevoir un pont automatisé entre Gemini Web et l'agent codeur local."

    created_file_path: Optional[Path] = None

    # 1. Création du ticket en 'radar'
    task_id = kanban_engine.create_task(
        project_id="exocortex",
        title=test_title,
        component_tag=test_tag,
        summary_pitch=test_pitch,
        priority=1,
        complexity="M",
        initial_status="radar",
    )
    assert task_id.startswith("EXO-")

    try:
        t_record = db.get_kanban_task_by_id(task_id)
        assert t_record is not None
        assert t_record["status"] == "radar"

        # 2. Arbitrage vers 'needs_spec'
        db.update_kanban_task_status(task_id, "needs_spec")
        t_record = db.get_kanban_task_by_id(task_id)
        assert t_record["status"] == "needs_spec"

        # 3. Génération du prompt Context-Pack SOTA
        prompt = kanban_engine.build_sota_context_pack_prompt(task_id)
        assert "# MISSION D'ARCHITECTURE & SPÉCIFICATION TECHNIQUE" in prompt
        assert task_id in prompt
        assert test_title in prompt
        assert test_pitch in prompt
        assert "## 2. CONTEXTE ARCHITECTURAL DU PROJET" in prompt
        assert "## 4. LIVRABLE ATTENDU (FORMAT STRICT)" in prompt
        assert "## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES" in prompt
        assert "## 2. PROMPT D'EXÉCUTION POUR L'AGENT CODEUR" in prompt

        # 4. Simulation du retour Markdown de Gemini Web App
        mock_gemini_response = f"""```markdown
---
task_id: "{task_id}"
project_id: "exocortex"
component_tag: "{test_tag}"
title: "{test_title}"
status: "ready_for_agent"
---
# {task_id} — {test_title}

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES
Spécifications techniques générées par le Cloud SOTA.
Architecture et fichiers cibles définis.

## 2. PROMPT D'EXÉCUTION POUR L'AGENT CODEUR
Instruction impérative pour l'agent codeur :
1. Implémenter les modules.
2. Lancer la validation pytest.
```"""

        # 5. Attachement de la spécification
        updated_task = kanban_engine.attach_spec_to_task(mock_gemini_response)
        assert updated_task["status"] == "ready_for_agent"
        assert updated_task["spec_file_path"] is not None

        spec_path = Path(updated_task["spec_file_path"])
        created_file_path = spec_path
        assert spec_path.exists(), f"Le fichier physique de spec {spec_path} doit exister."
        assert spec_path.parent == settings.KANBAN_SPECS_DIR / "exocortex"

        # 6. Vérification du manifeste AGENT_QUEUE.md
        queue_path = settings.AGENT_QUEUE_PATH
        assert queue_path.exists()
        queue_content = queue_path.read_text(encoding="utf-8")
        assert task_id in queue_content
        assert test_title in queue_content

        # 7. Extraction chirurgicale du prompt de l'agent codeur
        coder_prompt = kanban_engine.extract_coder_prompt_from_spec(task_id)
        assert "Instruction impérative pour l'agent codeur :" in coder_prompt
        assert "CHANGELOG & SPÉCIFICATIONS TECHNIQUES" not in coder_prompt

        # 8. Progression vers 'in_progress' puis 'done'
        db.update_kanban_task_status(task_id, "in_progress")
        kanban_engine.compile_agent_queue_manifest()
        t_prog = db.get_kanban_task_by_id(task_id)
        assert t_prog["status"] == "in_progress"

        db.update_kanban_task_status(task_id, "done")
        kanban_engine.compile_agent_queue_manifest()
        t_done = db.get_kanban_task_by_id(task_id)
        assert t_done["status"] == "done"

    finally:
        # Nettoyage
        db.delete_kanban_task(task_id)
        kanban_engine.compile_agent_queue_manifest()
        if created_file_path and created_file_path.exists():
            try:
                created_file_path.unlink()
            except Exception:
                pass


def test_cli_commands(capsys):
    """
    Vérifie l'exécution des commandes CLI du Kanban :
    - run_kanban_status
    - run_next_task
    - run_complete_task
    """
    db = kanban_engine.db

    # 1. Test de --kanban-status
    run_kanban_status(project_id="exocortex")
    captured = capsys.readouterr()
    assert "ÉTAT EXÉCUTIF DU KANBAN" in captured.out
    assert "exocortex" in captured.out

    # 2. Création d'une tâche de test prête pour l'agent
    test_tid = kanban_engine.create_task(
        project_id="exocortex",
        title="Tâche CLI Déroulée",
        component_tag="cli-test",
        summary_pitch="Tâche pour vérifier run_next_task et run_complete_task",
        priority=1,
        complexity="S",
        initial_status="ready_for_agent",
    )

    try:
        # 3. Test de --next-task
        run_next_task(project_id="exocortex")
        captured_next = capsys.readouterr()
        assert "[TASK DÉPILÉE]" in captured_next.out
        assert test_tid in captured_next.out

        # Vérification du passage en 'in_progress'
        t_in_prog = db.get_kanban_task_by_id(test_tid)
        assert t_in_prog["status"] == "in_progress"

        # 4. Test de --complete-task
        run_complete_task(test_tid)
        captured_done = capsys.readouterr()
        assert "marquée comme terminée avec succès" in captured_done.out

        # Vérification du passage en 'done'
        t_done = db.get_kanban_task_by_id(test_tid)
        assert t_done["status"] == "done"

    finally:
        # Nettoyage
        db.delete_kanban_task(test_tid)
        kanban_engine.compile_agent_queue_manifest()

