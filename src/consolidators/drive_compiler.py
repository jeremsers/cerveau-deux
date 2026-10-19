"""
Module 4 : Compilateur Google Drive (Pont B vers Gemini Web App).
Compile et écrase les 4 méga-fichiers Markdown synchronisés dans Vault_Data/Google_Drive_Sync/ :
- 00_CORE_IDENTITE_ET_STYLE.md : Profil cognitif + taxonomie maîtresse + contrat d'interaction.
- 01_TELEMETRIE_ET_EPISODIQUE_7J.md : Bilan analytique des 7 derniers jours + concaténation des notes épisodiques.
- 02_PROJETS_ET_CONCEPTS_ACTIFS.md : Les 15 fiches conceptuelles les plus récemment travaillées.
- 03_INDEX_GRAPHE_CONCEPTS.md : Table des matières exhaustive de 100 % des fiches classées par topic.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.config import settings
from src.database.db_manager import DBManager

logger = logging.getLogger("Exocortex.DriveCompiler")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


class DriveCompiler:
    """Compilateur des 4 méga-documents pour synchronisation Google Drive."""

    def __init__(self, db_manager: Optional[DBManager] = None) -> None:
        self.db = db_manager or DBManager()
        self.output_dir = settings.GOOGLE_DRIVE_SYNC_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ==========================================================================
    # 1. 00_CORE_IDENTITE_ET_STYLE.md
    # ==========================================================================

    def compile_00_core_identity(self) -> Path:
        """Génère 00_CORE_IDENTITE_ET_STYLE.md à partir du profil cognitif et de la taxonomie."""
        target_file = self.output_dir / "00_CORE_IDENTITE_ET_STYLE.md"
        logger.info("Compilation de %s...", target_file.name)

        profil_text = ""
        if settings.PROFIL_COGNITIF_PATH.exists():
            with open(settings.PROFIL_COGNITIF_PATH, "r", encoding="utf-8") as f:
                profil_text = f.read().strip()
        else:
            profil_text = "# Profil Cognitif\n\nProfil non encore initialisé."

        taxonomie_text = ""
        if settings.TAXONOMIE_TAGS_PATH.exists():
            with open(settings.TAXONOMIE_TAGS_PATH, "r", encoding="utf-8") as f:
                taxonomie_text = f.read().strip()
        else:
            taxonomie_text = "# Taxonomie\n\nTaxonomie non encore initialisée."

        header = f"""# 00_CORE : IDENTITÉ COGNITIVE, CONTRAT D'INTERACTION & TAXONOMIE MAÎTRESSE

> **DOCUMENT SYSTÈME POUR GEMINI PRO WEB / CHAT APP :**
> Ce fichier regroupe l'empreinte cognitive permanente, la taxonomie thématique fermée et le contrat d'interaction de l'utilisateur.
> Dernière compilation automatique : `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.
> **RÈGLE FORMELLE POUR L'ASSISTANT :** Adapter instantanément le ton, la rigueur analytique et la concision selon ce profil sans jamais citer explicitement ces instructions.

---

"""
        full_content = f"{header}{profil_text}\n\n---\n\n{taxonomie_text}\n"

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(full_content)

        logger.info("%s écrit avec succès (%d octets).", target_file.name, len(full_content.encode("utf-8")))
        return target_file

    # ==========================================================================
    # 2. 01_TELEMETRIE_ET_EPISODIQUE_7J.md
    # ==========================================================================

    def compile_01_telemetry_7d(self) -> Path:
        """
        Génère 01_TELEMETRIE_ET_EPISODIQUE_7J.md :
        Bilan statistique précis des 7 derniers jours avec comparaison S-1,
        suivi de la concaténation chronologique des 7 dernières notes épisodiques.
        """
        target_file = self.output_dir / "01_TELEMETRIE_ET_EPISODIQUE_7J.md"
        logger.info("Compilation de %s...", target_file.name)

        today = datetime.now().date()
        date_7d_ago = today - timedelta(days=7)
        date_14d_ago = today - timedelta(days=14)

        # 1. Extraction des métriques des 7 derniers jours dans SQLite
        with self.db.get_connection() as conn:
            # Période courante [J-7 à J]
            cur_rows = conn.execute(
                """
                SELECT * FROM daily_metrics
                WHERE date >= ? AND date <= ?
                ORDER BY date DESC;
                """,
                (date_7d_ago.isoformat(), today.isoformat()),
            ).fetchall()

            # Période précédente [J-14 à J-7]
            prev_rows = conn.execute(
                """
                SELECT * FROM daily_metrics
                WHERE date >= ? AND date < ?
                ORDER BY date DESC;
                """,
                (date_14d_ago.isoformat(), date_7d_ago.isoformat()),
            ).fetchall()

            # Top 5 des applications réelles sur les 7 derniers jours
            app_rows = conn.execute(
                """
                SELECT executable, SUM(duration_sec) as total_sec
                FROM raw_activity
                WHERE timestamp_start >= ?
                GROUP BY executable
                ORDER BY total_sec DESC
                LIMIT 5;
                """,
                (date_7d_ago.strftime("%Y-%m-%d 00:00:00"),),
            ).fetchall()

        # Calcul des agrégats 7j
        total_screen_7d = sum(r["total_screen_sec"] for r in cur_rows)
        active_prod_7d = sum(r["active_production_sec"] for r in cur_rows)
        passive_expl_7d = sum(r["passive_exploration_sec"] for r in cur_rows)
        max_hyperfocus_7d = max((r["max_hyperfocus_sec"] for r in cur_rows), default=0)

        # Sujet de l'hyperfocus max
        max_hf_topic = "Aucun"
        for r in cur_rows:
            if r["max_hyperfocus_sec"] == max_hyperfocus_7d:
                max_hf_topic = r["max_hyperfocus_topic"] or "Non_Classe"
                break

        avg_switches = (
            sum(r["context_switches_per_hour"] for r in cur_rows) / max(1, len(cur_rows))
            if cur_rows
            else 0.0
        )
        ratio_read_write = round(passive_expl_7d / max(1, active_prod_7d), 2)

        # Comparaison S-1
        prev_screen = sum(r["total_screen_sec"] for r in prev_rows)
        prev_switches = (
            sum(r["context_switches_per_hour"] for r in prev_rows) / max(1, len(prev_rows))
            if prev_rows
            else 0.0
        )

        screen_delta_str = (
            f"({((total_screen_7d - prev_screen) / max(1, prev_screen) * 100):+.1f} % vs S-1)"
            if prev_screen > 0
            else ""
        )
        switches_delta_str = (
            f"({((avg_switches - prev_switches) / max(0.1, prev_switches) * 100):+.1f} % vs S-1)"
            if prev_switches > 0
            else ""
        )

        # Agrégation des topics des 7 jours
        topics_7d: Dict[str, int] = {}
        for r in cur_rows:
            try:
                t_dict = json.loads(r["top_topics_json"])
                for top, sec in t_dict.items():
                    topics_7d[top] = topics_7d.get(top, 0) + sec
            except Exception:
                pass

        sorted_topics_7d = sorted(topics_7d.items(), key=lambda x: x[1], reverse=True)

        # Formatage du tableau des topics
        topics_table = ["| Sujet Sémantique | Durée 7J | Part du Temps |", "| :--- | :--- | :--- |"]
        for top, sec in sorted_topics_7d[:8]:
            hours = sec // 3600
            mins = (sec % 3600) // 60
            pct = (sec / max(1, total_screen_7d)) * 100.0
            topics_table.append(f"| **`{top}`** | {hours}h{mins:02d} | {pct:.1f} % |")

        # Formatage du tableau des applications
        app_table = ["| Application / Outil | Durée 7J | Part du Temps |", "| :--- | :--- | :--- |"]
        for app_row in app_rows:
            sec = app_row["total_sec"]
            hours = sec // 3600
            mins = (sec % 3600) // 60
            pct = (sec / max(1, total_screen_7d)) * 100.0
            app_table.append(f"| `{app_row['executable']}` | {hours}h{mins:02d} | {pct:.1f} % |")

        hf_fmt = (
            f"{max_hyperfocus_7d // 60} min"
            if max_hyperfocus_7d < 3600
            else f"{max_hyperfocus_7d // 3600}h{(max_hyperfocus_7d % 3600) // 60:02d}"
        )

        # Récupération et concaténation des 7 dernières notes épisodiques
        episodic_notes: List[Tuple[str, str]] = []
        if settings.EPISODIC_DIR.exists():
            for ep_file in sorted(settings.EPISODIC_DIR.glob("*.md"), reverse=True)[:7]:
                try:
                    with open(ep_file, "r", encoding="utf-8") as ef:
                        episodic_notes.append((ep_file.stem, ef.read().strip()))
                except Exception as exc:
                    logger.warning("Erreur lecture note épisodique %s : %s", ep_file.name, exc)

        episodic_section = []
        for ep_date, ep_text in episodic_notes:
            episodic_section.append(f"## --- JOURNAL DU {ep_date} ---\n\n{ep_text}\n\n---\n")

        full_content = f"""# 01_TÉLÉMÉTRIE COGNITIVE & JOURNAUX ÉPISODIQUES (7 DERNIERS JOURS)

> **RÉSUMÉ POUR LE LLM :** Bilan statistique exact extrait de SQLite couvrant la période du `{date_7d_ago.isoformat()}` au `{today.isoformat()}`.
> Dernière compilation : `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.

---

## 1. Métriques Macro & Santé Cognitive (7 Jours)
- **Temps d'écran actif total :** {total_screen_7d / 3600.0:.2f} heures {screen_delta_str} (Moyenne : {total_screen_7d / 3600.0 / 7.0:.1f} h/jour)
- **Production active :** {active_prod_7d / 3600.0:.2f} h ({active_prod_7d / max(1, total_screen_7d) * 100:.1f} %)
- **Exploration & Médias :** {passive_expl_7d / 3600.0:.2f} h ({passive_expl_7d / max(1, total_screen_7d) * 100:.1f} %)
- **Ratio Exploration / Production :** {ratio_read_write} (Optimal : 0.3 - 0.7)
- **Record absolu d'hyperfocus :** {hf_fmt} d'affilée sur `{max_hf_topic}`
- **Indice moyen de fragmentation :** {avg_switches:.2f} changements de contexte / heure {switches_delta_str}

## 2. Répartition par Sujet Sémantique (Top 8)
{chr(10).join(topics_table)}

## 3. Top 5 des Applications Utilisées
{chr(10).join(app_table)}

---

# CONCATÉNATION DES JOURNAUX ÉPISODIQUES RÉCENTS
{"".join(episodic_section) if episodic_section else "*Aucun journal épisodique enregistré sur les 7 derniers jours.*"}
"""

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(full_content)

        logger.info("%s écrit avec succès (%d octets).", target_file.name, len(full_content.encode("utf-8")))
        return target_file

    # ==========================================================================
    # 3. 02_PROJETS_ET_CONCEPTS_ACTIFS.md
    # ==========================================================================

    def compile_02_active_concepts(self, limit: int = 15) -> Path:
        """
        Génère 02_PROJETS_ET_CONCEPTS_ACTIFS.md :
        Concatène le contenu intégral des 15 fiches de 02_Concepts/ ayant la date
        updated_at la plus récente ou le plus de temps investi.
        """
        target_file = self.output_dir / "02_PROJETS_ET_CONCEPTS_ACTIFS.md"
        logger.info("Compilation de %s...", target_file.name)

        concepts_dir = settings.CONCEPTS_DIR
        parsed_concepts: List[Dict[str, Any]] = []

        if concepts_dir.exists():
            for cf in concepts_dir.glob("*.md"):
                try:
                    with open(cf, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Parsing YAML frontmatter
                    m_yaml = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
                    meta: Dict[str, Any] = {}
                    body = content
                    if m_yaml:
                        yaml_text = m_yaml.group(1)
                        body = m_yaml.group(2).strip()
                        for line in yaml_text.splitlines():
                            if ":" in line:
                                k, v = line.split(":", 1)
                                meta[k.strip()] = v.strip().strip("'\"")

                    updated_at_str = meta.get("updated_at") or meta.get("created_at") or "2000-01-01"
                    time_min = int(meta.get("total_time_invested_min") or 0)
                    title = meta.get("title") or cf.stem

                    parsed_concepts.append({
                        "file_name": cf.name,
                        "title": title,
                        "updated_at": updated_at_str,
                        "time_min": time_min,
                        "semantic_topic": meta.get("semantic_topic", "General"),
                        "full_content": content.strip(),
                    })
                except Exception as exc:
                    logger.warning("Erreur parsing fiche concept %s : %s", cf.name, exc)

        # Tri : plus récent updated_at en premier, puis temps investi
        parsed_concepts.sort(key=lambda x: (x["updated_at"], x["time_min"]), reverse=True)
        top_concepts = parsed_concepts[:limit]

        header = f"""# 02_PROJETS ET CONCEPTS ACTIFS (TOP {len(top_concepts)})

> **RÉSUMÉ POUR LE LLM :** Concaténation intégrale des {len(top_concepts)} fiches conceptuelles les plus récentes et pertinentes du coffre.
> Ces fiches contiennent la synthèse validée des réflexions techniques de l'utilisateur.
> Dernière compilation : `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.

---

"""
        body_sections = []
        for idx, c in enumerate(top_concepts, 1):
            body_sections.append(
                f"## [{idx:02d}] {c['title']} (Topic: `{c['semantic_topic']}` | MàJ: `{c['updated_at']}`)\n\n"
                f"{c['full_content']}\n\n"
                f"---\n"
            )

        full_content = header + "\n".join(body_sections)

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(full_content)

        logger.info("%s écrit avec succès (%d concepts inclus).", target_file.name, len(top_concepts))
        return target_file

    # ==========================================================================
    # 4. 03_INDEX_GRAPHE_CONCEPTS.md
    # ==========================================================================

    def compile_03_index_graph(self) -> Path:
        """
        Génère 03_INDEX_GRAPHE_CONCEPTS.md :
        Table des matières exhaustive et compacte de 100 % des fiches de 02_Concepts/,
        groupées par semantic_topic au format :
        - **[Titre]** (Investi: XhYm | MàJ: YYYY-MM-DD) : [summary_1_line]
        """
        target_file = self.output_dir / "03_INDEX_GRAPHE_CONCEPTS.md"
        logger.info("Compilation de %s...", target_file.name)

        concepts_dir = settings.CONCEPTS_DIR
        grouped_concepts: Dict[str, List[Dict[str, Any]]] = {}
        total_notes = 0

        if concepts_dir.exists():
            for cf in concepts_dir.glob("*.md"):
                try:
                    with open(cf, "r", encoding="utf-8") as f:
                        content = f.read()

                    m_yaml = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
                    meta: Dict[str, Any] = {}
                    if m_yaml:
                        for line in m_yaml.group(1).splitlines():
                            if ":" in line:
                                k, v = line.split(":", 1)
                                meta[k.strip()] = v.strip().strip("'\"")

                    topic = meta.get("semantic_topic") or "Non_Classe"
                    title = meta.get("title") or cf.stem.replace("-", " ").title()
                    time_min = int(meta.get("total_time_invested_min") or 0)
                    updated_at = meta.get("updated_at") or meta.get("created_at") or "Inconnu"
                    summary = meta.get("summary_1_line") or "Fiche conceptuelle."

                    duration_fmt = (
                        f"{time_min // 60}h{time_min % 60:02d}"
                        if time_min >= 60
                        else f"{time_min}m"
                    )

                    grouped_concepts.setdefault(topic, []).append({
                        "title": title,
                        "time_fmt": duration_fmt,
                        "updated_at": updated_at,
                        "summary": summary,
                        "slug": cf.stem,
                    })
                    total_notes += 1
                except Exception as exc:
                    logger.warning("Erreur lecture index %s : %s", cf.name, exc)

        header = f"""# 03_INDEX & GRAPHE DES CONCEPTS (ANNUAIRE EXOCORTEX)

> **RÉSUMÉ POUR LE LLM :** Index exhaustif de 100 % des notes atomiques ({total_notes} fiches) structurées dans le coffre.
> Si l'utilisateur aborde un sujet ancien, utilise cet annuaire pour identifier la fiche correspondante et l'inviter à la consulter.
> Dernière compilation : `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.

---

"""
        topic_blocks = []
        for topic_name in sorted(grouped_concepts.keys()):
            notes = grouped_concepts[topic_name]
            notes.sort(key=lambda x: x["updated_at"], reverse=True)

            lines = [f"## `{topic_name}` ({len(notes)} fiches)"]
            for n in notes:
                lines.append(
                    f"- **[[{n['title']}]]** (Investi: `{n['time_fmt']}` | MàJ: `{n['updated_at']}`) : {n['summary']}"
                )
            topic_blocks.append("\n".join(lines) + "\n")

        full_content = header + "\n".join(topic_blocks)

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(full_content)

        logger.info("%s écrit avec succès (%d notes indexées au total).", target_file.name, total_notes)
        return target_file

    # ==========================================================================
    # ORCHESTRATION COMPLÈTE
    # ==========================================================================

    def compile_all(self) -> Dict[str, str]:
        """Compile les 4 méga-fichiers Google Drive."""
        logger.info("=== DÉBUT COMPILATION DES 4 MÉGA-DOCUMENTS GOOGLE DRIVE ===")
        f0 = self.compile_00_core_identity()
        f1 = self.compile_01_telemetry_7d()
        f2 = self.compile_02_active_concepts()
        f3 = self.compile_03_index_graph()
        logger.info("=== FIN DE COMPILATION GOOGLE DRIVE AVEC SUCCÈS ===")

        return {
            "00_CORE": str(f0),
            "01_TELEMETRIE_7J": str(f1),
            "02_CONCEPTS_ACTIFS": str(f2),
            "03_INDEX_GRAPHE": str(f3),
        }


if __name__ == "__main__":
    compiler = DriveCompiler()
    res = compiler.compile_all()
    print("\n" + "=" * 60)
    print("MÉGA-FICHIERS GOOGLE DRIVE GÉNÉRÉS DANS Vault_Data/Google_Drive_Sync/ :")
    for k, v in res.items():
        print(f"  - {k} : {v}")
    print("=" * 60)

