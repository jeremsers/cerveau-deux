"""
Module 7 : Kanban Exécutif Multi-Projets & Pont Cloud SOTA (v0.2.0-core).
Gère la synchronisation des spécifications techniques, la préparation des prompts
d'architecture SOTA, l'ingestion des specs Markdown et le manifeste d'exécution
de l'agent codeur (AGENT_QUEUE.md).
"""

from __future__ import annotations

import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.config import settings
from src.database.db_manager import DBManager, KanbanTaskRecord


def _slugify(text: str) -> str:
    """Transforme un titre en slug kebab-case propre et sûr pour le système de fichiers."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text[:50] or "task"


def _generate_repo_tree(repo_path: Path, max_depth: int = 4) -> str:
    """
    Génère l'arborescence des fichiers d'un dépôt local en filtrant strictement
    les répertoires parasites et le bruit technique.
    """
    ignored = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        "Vault_Data",
        "models",
        "takeout_raw",
        ".pytest_cache",
        ".idea",
        ".vscode",
        ".mypy_cache",
        ".ruff_cache",
    }
    lines: List[str] = [f"{repo_path.name}/"]

    def walk(current_dir: Path, depth: int, prefix: str = "") -> None:
        if depth > max_depth:
            return
        try:
            entries = sorted(
                list(current_dir.iterdir()),
                key=lambda x: (not x.is_dir(), x.name.lower()),
            )
        except Exception:
            return

        valid_entries = [
            e for e in entries if e.name not in ignored and not e.name.startswith("~")
        ]
        total = len(valid_entries)
        for i, entry in enumerate(valid_entries):
            is_last = i == total - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                sub_prefix = f"{prefix}    " if is_last else f"{prefix}│   "
                walk(entry, depth + 1, sub_prefix)

    walk(repo_path, 1)
    return "\n".join(lines)


class KanbanEngine:
    """Moteur métier pour le suivi multi-projets, la liaison SOTA et l'orchestration de code."""

    def __init__(self, db_manager: Optional[DBManager] = None) -> None:
        self.db = db_manager or DBManager()
        settings.ensure_directories()

    def sync_existing_tech_specs(self) -> int:
        """
        Scanne récursivement le dossier 'tech specs/' et indexe tous les changelogs/specs
        historiques comme tâches 'done' rattachées au projet 'exocortex'.
        Méthode entièrement idempotente : ne crée aucun doublon si la spec est déjà indexée.
        """
        tech_specs_root = _PROJECT_ROOT / "tech specs"
        if not tech_specs_root.exists():
            return 0

        existing_tasks = self.db.get_kanban_tasks(project_id="exocortex")
        indexed_paths = {
            os.path.normcase(os.path.abspath(t["spec_file_path"]))
            for t in existing_tasks
            if t.get("spec_file_path")
        }
        indexed_titles = {
            t["title"].strip().lower() for t in existing_tasks if t.get("title")
        }

        # Découverte récursive de tous les fichiers .md
        md_files: List[Path] = []
        for p in tech_specs_root.rglob("*.md"):
            if not p.is_file() or p.name.startswith("~") or p.name.startswith("."):
                continue
            md_files.append(p)

        # Tri stable par chemin relatif pour reproductibilité des IDs
        md_files.sort(key=lambda p: str(p.relative_to(tech_specs_root)).lower())

        synced_count = 0
        for fpath in md_files:
            norm_path = os.path.normcase(os.path.abspath(fpath))
            if norm_path in indexed_paths:
                continue

            # Extraction du titre du fichier
            title = self._extract_title_from_md(fpath)
            if title.strip().lower() in indexed_titles:
                continue

            # Génération d'un task_id déterministe
            task_id = self.db.generate_next_task_id("exocortex")
            record = KanbanTaskRecord(
                task_id=task_id,
                project_id="exocortex",
                component_tag="core-architecture",
                title=title,
                summary_pitch=f"Spécification technique archivée : {fpath.name}",
                status="done",
                priority=2,
                complexity="L",
                spec_file_path=str(fpath.resolve()),
                created_at=datetime.fromtimestamp(fpath.stat().st_mtime),
                updated_at=datetime.fromtimestamp(fpath.stat().st_mtime),
            )
            self.db.upsert_kanban_task(record)
            indexed_paths.add(norm_path)
            indexed_titles.add(title.strip().lower())
            synced_count += 1

        if synced_count > 0:
            self.compile_agent_queue_manifest()

        return synced_count

    def _extract_title_from_md(self, fpath: Path) -> str:
        """Extrait le premier titre niveau 1 (# ...) d'un Markdown ou génère un fallback propre."""
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    s = line.strip()
                    if s.startswith("# "):
                        title = s[2:].strip()
                        # Nettoie les balises et emojis éventuels si nécessaire
                        return title or fpath.stem
        except Exception:
            pass
        return fpath.stem.replace("_", " ").replace("-", " ").title()

    def create_task(
        self,
        project_id: str,
        title: str,
        component_tag: str = "general",
        summary_pitch: str = "",
        priority: int = 2,
        complexity: str = "M",
        initial_status: str = "radar",
    ) -> str:
        """Crée une nouvelle tâche Kanban dans un projet et actualise le manifeste."""
        task_id = self.db.generate_next_task_id(project_id)
        record = KanbanTaskRecord(
            task_id=task_id,
            project_id=project_id,
            component_tag=component_tag.strip() or "general",
            title=title.strip(),
            summary_pitch=summary_pitch.strip(),
            status=initial_status,
            priority=priority,
            complexity=complexity,
            spec_file_path=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.db.upsert_kanban_task(record)
        self.compile_agent_queue_manifest()
        return task_id

    def build_sota_context_pack_prompt(self, task_id: str) -> str:
        """
        Génère le prompt d'architecture haute-fidélité prêt à être injecté dans Gemini Web App.
        Assemble :
        1. Expression du besoin et métadonnées du ticket.
        2. Arborescence épurée du code source local.
        3. Extraits sémantiques k-NN issus de LanceDB (sans bloquer si hors ligne).
        4. Contrat strict Markdown imposant le format 'Changelog + Prompt Agent Codeur'.
        """
        task = self.db.get_kanban_task_by_id(task_id)
        if not task:
            raise ValueError(f"Tâche '{task_id}' introuvable dans la base de données.")

        project = self.db.get_project_by_id(task["project_id"])
        project_name = project["name"] if project else task["project_id"]
        project_desc = project["description"] if project else ""
        repo_path_str = project.get("repo_path") if project else None

        # 1. Extraction de l'arborescence du dépôt
        repo_tree_str = "(Aucun dépôt local configuré pour ce projet)"
        if repo_path_str:
            repo_p = Path(repo_path_str)
            if repo_p.exists() and repo_p.is_dir():
                repo_tree_str = _generate_repo_tree(repo_p, max_depth=4)

        # 2. Recherche sémantique dans LanceDB (0 Mo VRAM au repos)
        related_concepts_str = "Aucun extrait conceptuel pertinent disponible (Ollama hors-ligne ou base vide)."
        try:
            from src.database.vector_store import vector_store
            from src.llm.ollama_client import llm_client

            if vector_store.count() > 0 and llm_client.is_alive():
                query = f"{task['title']} {task.get('summary_pitch', '')}".strip()
                results = vector_store.search(query, top_k=3)
                if results:
                    snippets = []
                    for r in results:
                        ctitle = r.get("title") or "Concept"
                        snippet = (r.get("content") or "")[:600].strip()
                        snippets.append(f"### [[{ctitle}]]\n{snippet}\n")
                    related_concepts_str = "\n".join(snippets)
                # Déchargement immédiat de l'embedding pour respecter les 0 Mo VRAM
                llm_client.unload_model(settings.MODEL_EMBEDDING)
        except Exception:
            # Fallback gracieux en cas de défaillance
            pass

        # 3. Assemblage du contrat de prompt SOTA
        prompt = f"""# MISSION D'ARCHITECTURE & SPÉCIFICATION TECHNIQUE (PROJET: {project_name})

- **Task ID :** {task['task_id']}
- **Sous-module :** {task['component_tag']}
- **Titre :** {task['title']}
- **Complexité cible :** {task['complexity']} | **Priorité :** P{task['priority']}

## 1. EXPRESSION DU BESOIN & OBJECTIFS
{task['summary_pitch'] or '(Aucun pitch complémentaire fourni)'}

## 2. CONTEXTE ARCHITECTURAL DU PROJET
**Description du projet :** {project_desc}
**Arborescence actuelle du dépôt :**
```text
{repo_tree_str}
```

## 3. MÉMOIRE SÉMANTIQUE & ARBITRAGES LIÉS (EXOCORTEX LANCEDB)
{related_concepts_str}

## 4. LIVRABLE ATTENDU (FORMAT STRICT)
Génère un document Markdown complet et autonome contenant exactement le frontmatter YAML et les deux sections ci-dessous (sans texte parasite autour du bloc ou prêt à être copié) :

```markdown
---
task_id: "{task['task_id']}"
project_id: "{task['project_id']}"
component_tag: "{task['component_tag']}"
title: "{task['title']}"
status: "ready_for_agent"
---
# {task['task_id']} — {task['title']}

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES
(Détaille ici l'architecture, les choix techniques, les structures de données et la liste exacte des fichiers à créer ou modifier)

## 2. PROMPT D'EXÉCUTION POUR L'AGENT CODEUR
(Rédige ici le prompt complet, impératif et autonome que l'agent codeur devra exécuter étape par étape, incluant les tests de vérification)
```
"""
        return prompt.strip()

    def attach_spec_to_task(
        self, raw_markdown: str, target_task_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ingère le livrable Markdown renvoyé par Gemini Web App, le sauvegarde sous
        'Vault_Data/03_Kanban_Specs/{project_id}/{task_id}_{slug}.md', bascule la tâche
        au statut 'ready_for_agent' et met à jour AGENT_QUEUE.md.
        """
        raw = raw_markdown.strip()

        # Nettoyage des triples backticks englobants
        if raw.startswith("```markdown"):
            raw = raw[len("```markdown") :].strip()
            if raw.endswith("```"):
                raw = raw[:-3].strip()
        elif raw.startswith("```"):
            raw = raw[3:].strip()
            if raw.endswith("```"):
                raw = raw[:-3].strip()

        # Extraction de task_id depuis le frontmatter YAML ou le titre H1
        parsed_task_id: Optional[str] = None
        m_yaml = re.search(r'task_id:\s*["\']?([A-Za-z0-9_-]+)["\']?', raw, re.IGNORECASE)
        if m_yaml:
            parsed_task_id = m_yaml.group(1).strip()
        else:
            m_title = re.search(r"^#\s*([A-Za-z0-9_-]+)", raw, re.MULTILINE)
            if m_title:
                parsed_task_id = m_title.group(1).strip()

        # Choix de l'ID effectif
        effective_task_id = target_task_id or parsed_task_id
        task = self.db.get_kanban_task_by_id(effective_task_id) if effective_task_id else None

        if not task:
            # Si le ticket n'existe pas encore, tentative de création à la volée
            m_proj = re.search(r'project_id:\s*["\']?([a-z0-9_-]+)["\']?', raw, re.IGNORECASE)
            project_id = m_proj.group(1).strip() if m_proj else "exocortex"

            m_title_yaml = re.search(r'title:\s*["\']?([^"\n\r]+)["\']?', raw, re.IGNORECASE)
            title = m_title_yaml.group(1).strip() if m_title_yaml else "Nouvelle Spécification"

            m_tag = re.search(r'component_tag:\s*["\']?([^"\n\r]+)["\']?', raw, re.IGNORECASE)
            component_tag = m_tag.group(1).strip() if m_tag else "general"

            effective_task_id = self.create_task(
                project_id=project_id,
                title=title,
                component_tag=component_tag,
                summary_pitch="Spécification ingérée directement depuis le Presse-Papier",
                initial_status="ready_for_agent",
            )
            task = self.db.get_kanban_task_by_id(effective_task_id)

        project_id = task["project_id"]
        title = task["title"]
        slug = _slugify(title)

        # Enregistrement physique du fichier Markdown
        dest_dir = settings.KANBAN_SPECS_DIR / project_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        spec_path = dest_dir / f"{task['task_id']}_{slug}.md"
        spec_path.write_text(raw, encoding="utf-8")

        # Mise à jour en base SQLite
        self.db.update_kanban_task_status(
            task_id=task["task_id"],
            new_status="ready_for_agent",
            spec_file_path=str(spec_path.resolve()),
        )

        self.compile_agent_queue_manifest()
        return self.db.get_kanban_task_by_id(task["task_id"]) or {}

    def extract_coder_prompt_from_spec(self, task_id: str) -> str:
        """
        Extrait chirurgicalement la section '## 2. PROMPT D'EXÉCUTION POUR L'AGENT CODEUR'
        d'une spec Markdown pour injection directe dans la session de code.
        """
        task = self.db.get_kanban_task_by_id(task_id)
        if not task or not task.get("spec_file_path"):
            return ""

        fpath = Path(task["spec_file_path"])
        if not fpath.exists():
            return task.get("summary_pitch", "")

        try:
            content = fpath.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""

        # Détection du marqueur de section
        pattern = re.compile(
            r"##\s*2\.\s*PROMPT\s+D['’]EX[EÉ]CUTION\s+POUR\s+L['’]AGENT\s+CODEUR.*$",
            re.IGNORECASE | re.MULTILINE,
        )
        match = pattern.search(content)
        if match:
            extracted = content[match.end() :].strip()
            return extracted or content

        return content

    def compile_agent_queue_manifest(self) -> Path:
        """
        Génère ou met à jour le fichier manifeste 'Vault_Data/03_Kanban_Specs/AGENT_QUEUE.md'
        listant les tâches 'in_progress' et 'ready_for_agent' par ordre de priorité croissante.
        """
        projects = self.db.get_projects()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines: List[str] = [
            "# 🤖 MANIFESTE D'EXÉCUTION AGENT CODEUR (AGENT_QUEUE.md)",
            f"*Généré automatiquement par le Module 7 (Kanban Exécutif & Studio SOTA)*  ",
            f"*Dernière synchronisation : {now_str}*",
            "",
            "> [!NOTE] Invariants d'Exécution",
            "> - Consommation VRAM Kanban : **0 Mo** (moteur passif SQLite).",
            "> - Pour dépiler la prochaine tâche : `python run_exocortex.py --next-task`.",
            "> - Pour marquer une tâche achevée : `python run_exocortex.py --complete-task <TASK_ID>`.",
            "",
            "---",
            "",
        ]

        total_ready = 0
        total_in_progress = 0

        for p in projects:
            pid = p["project_id"]
            pname = p["name"]

            in_progress = self.db.get_kanban_tasks(project_id=pid, statuses=["in_progress"])
            ready = self.db.get_kanban_tasks(project_id=pid, statuses=["ready_for_agent"])

            # Tri ready par priorité croissante (P1 avant P4), puis updated_at ASC (premier arrivé premier servi)
            ready.sort(key=lambda x: (x["priority"], x["updated_at"]))

            if not in_progress and not ready:
                continue

            lines.append(f"## 📁 Projet : {pname} (`{pid}`)")
            lines.append("")

            # Section En Cours
            if in_progress:
                lines.append("### ⚙️ En Cours de Développement")
                for t in in_progress:
                    total_in_progress += 1
                    spec_link = t.get("spec_file_path") or "Non spécifiée"
                    lines.append(
                        f"- **`{t['task_id']}`** [P{t['priority']} | {t['complexity']}] **{t['title']}** ({t['component_tag']})"
                    )
                    lines.append(f"  - *Spec :* `{spec_link}`")
                    lines.append(f"  - *Terminer :* `python run_exocortex.py --complete-task {t['task_id']}`")
                lines.append("")

            # Section Prêt
            if ready:
                lines.append("### 🎯 Prêt pour Exécution (File d'Attente Prioritaire)")
                for t in ready:
                    total_ready += 1
                    spec_link = t.get("spec_file_path") or "Non spécifiée"
                    lines.append(
                        f"- **`{t['task_id']}`** [P{t['priority']} | {t['complexity']}] **{t['title']}** ({t['component_tag']})"
                    )
                    lines.append(f"  - *Spec :* `{spec_link}`")
                    lines.append(f"  - *Dépiler :* `python run_exocortex.py --next-task --project {pid}`")
                lines.append("")

            lines.append("---")
            lines.append("")

        if total_ready == 0 and total_in_progress == 0:
            lines.append("*(Aucune tâche en cours ni prête pour l'agent codeur pour le moment).*")
            lines.append("")

        manifest_path = settings.AGENT_QUEUE_PATH
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text("\n".join(lines), encoding="utf-8")
        return manifest_path


# Instance singleton au niveau module
kanban_engine = KanbanEngine()

