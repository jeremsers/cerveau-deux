---
task_id: "EXO-013"
project_id: "exocortex"
component_tag: "core-stabilization"
title: "v0.4.1 — Hotfix Intégration, Isolation VRAM Sommeil Profond & Fix Filtres UI"
status: "ready_for_agent"
---
# EXO-013 — v0.4.1 — Hotfix Intégration, Isolation VRAM Sommeil Profond & Fix Filtres UI

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif du Patch
Corriger 6 anomalies d'intégration identifiées lors de l'audit complet de la `v0.4.0` afin de garantir l'exclusion mutuelle VRAM en Sommeil Profond, d'éviter le recalcul redondant des journées passées dans `NightConsolidator`, et d'aligner les filtres du Dashboard avec les statuts SQLite réels.

### 1.2 Liste des Corrections Chirurgicales
1. **Exclusion Mutuelle VRAM dans `GraphDefragmenter` (`src/consolidators/graph_defragmenter.py`) :**
   - Interdire toute paire candidate où `path_a.resolve() == path_b.resolve()` ou `rec_a["slug"] == rec_b["slug"]`.
   - Dans `merge_concepts_pair()`, ajouter un paramètre `defer_vector_sync: bool = False`. Lorsqu'il est appelé depuis `run_defragmentation_cycle()`, ne **jamais** charger `bge-m3` pendant que `gemma4:26b-a4b` est en VRAM.
   - À la fin de `run_defragmentation_cycle()`, décharger explicitement `settings.MODEL_HEAVY_SYNTHESIS` (`llm_client.unload_model(...)`), puis synchroniser les nouvelles fiches fusionnées dans LanceDB et décharger `settings.MODEL_EMBEDDING`.
2. **Optimisation & Intégration du Cycle Nocturne (`src/consolidators/night_consolidator.py`) :**
   - Au début de `consolidate()`, exécuter automatiquement `VoiceIngestor(db_manager=self.db).run()` (Passe 0) si des fichiers audio sont présents dans `settings.VOICE_INBOX_DIR`.
   - Dans `consolidate()`, si `target_date` est fourni, ne traiter **que** `[target_date]`. Sinon, ne traiter que les dates ayant eu de nouvelles activités ou n'ayant pas encore de fichier journal `01_Episodique/YYYY-MM-DD.md` (plus la date la plus récente), afin de ne jamais recalculer tout l'historique ni écraser `00_BOOTLOADER_DEMAIN.md` avec une date ancienne.
   - N'exécuter `generate_executive_bootloader()` **qu'une seule fois**, sur la date la plus récente (`max(dates_to_process)`).
3. **Alignement des Statuts UI & Résumé Live Chat (`src/dashboard/app.py` & `src/database/db_manager.py`) :**
   - Dans `src/dashboard/app.py`, remplacer les options du filtre `Statut Distillation` par `["Tous", "success", "pending", "misc_noise", "failed_fallback"]` et supprimer la fonction morte `get_ro_connection()`.
   - Dans `src/database/db_manager.py` (`upsert_live_chat_turn`), initialiser `summary` avec `clean_prompt[:140]` lors de la création d'une nouvelle session live pour éviter les intitulés vides dans l'Explorateur Épistémique.
4. **Nettoyage résiduel (`src/ingestors/takeout_ingestor.py`) :**
   - Utiliser `parse_concept_file()` dans `save_distilled_concept_note()` pour vérifier la protection anti-écrasement et l'anti-collision de slug au lieu de regex manuelles.

---