---
task_id: "EXO-015"
project_id: "exocortex"
component_tag: "data-integrity"
title: "v0.5.1 — Audit Lot 1 : Arrêt des Pertes de Données Silencieuses"
status: "done"
---
# EXO-015 — v0.5.1 — Audit Lot 1 : Arrêt des Pertes de Données Silencieuses

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif du Patch
Premier lot de remédiation de l'audit de conformité du 24/10/2026. Il neutralise les mécanismes qui supprimaient ou écrasaient des données sans prévenir : le nettoyage au démarrage (A1), la mise à jour d'un projet (A2), la réingestion Takeout (A3), les fuites de captures (A4), le Vault Doctor (A6), la fusion du défragmenteur (A7, A8) et les chemins contrôlés par les requêtes HTTP (D3). Aucune refonte : chaque correctif est local.

### 1.2 Corrections

1. **A1 — Le démarrage n'efface plus les sessions courtes (`src/database/db_manager.py`)**
   - Le `DELETE FROM chat_sessions WHERE turn_count < 3 OR user_char_count < 250` exécuté à chaque `DBManager()` est supprimé. Le filtrage des micro-sessions ne se fait plus qu'à l'ingestion Takeout, qui n'insère déjà que les sessions qualifiées.
   - Nouvelles migrations versionnées par `PRAGMA user_version` (`_apply_migrations`) :
     - **v1** : déduplication des empreintes et index unique (v0.1.3), désormais exécutés une seule fois par base et non plus à chaque démarrage.
     - **v2** : reconstruction des sessions vocales (`voice_*`) effacées par l'ancien nettoyage, à partir de leurs messages restés orphelins.
   - `upsert_live_chat_turn` : si la session parente a disparu mais que des messages existent, elle est recréée avec le bon nombre de tours, le bon volume de caractères et l'horodatage du premier tour (au lieu de repartir à 1 tour).

2. **A2 — Mettre à jour un projet ne supprime plus ses tâches**
   - `upsert_project` passe de `INSERT OR REPLACE` (suppression puis réinsertion, qui déclenchait `ON DELETE CASCADE`) à `INSERT … ON CONFLICT(project_id) DO UPDATE`. La date de création est conservée.
   - Nouvelle méthode `create_project` qui refuse un slug existant.
   - API : `POST /api/kanban/projects` crée uniquement (409 si le slug existe) ; nouvelle route `PUT /api/kanban/projects/{project_id}` pour la mise à jour. Streamlit refuse également un slug existant.

3. **A3 — La réingestion Takeout préserve statuts et résumés**
   - `insert_chat_sessions_batch` utilise `ON CONFLICT(session_id) DO UPDATE` limité aux colonnes temporelles et volumétriques (`timestamp_start`, `timestamp_end`, `turn_count`, `user_char_count`). Le statut `misc_noise`, le résumé du 26B, les topics et les notes générées survivent à une réingestion ; les sessions triviales ne repartent plus au LLM.

4. **A4 — Fin des fuites de captures `.webp`**
   - Démon (`telemetry_daemon.py`) : la capture remplacée toutes les 180 s est supprimée ; une capture rattachée à une fenêtre écartée (durée inférieure au dwell time) l'est aussi.
   - Passe 1 (`night_consolidator.py`) : les captures sont analysées par lots de 50 jusqu'à épuisement (méthode `_analyze_activity_screenshot`), et la classification ignore toute activité dont la capture n'a pas encore été lue (`get_unprocessed_raw_activities(exclude_pending_screenshots=True)`). Une activité n'est donc plus jamais marquée traitée avant la vision.
   - Nouvelle purge `purge_orphan_screenshots()` en fin de Passe 1 : supprime les captures du staging qu'aucune activité ne référence et plus anciennes que `SCREEN_ORPHAN_MAX_AGE_HOURS` (24 h par défaut, pour épargner la fenêtre que le démon tient encore en mémoire).
   - `update_activity_visual_summary` n'ajoute plus de suffixe vide à `ocr_snippet` quand l'image a disparu.

5. **A6 — Le Vault Doctor reste dans son périmètre et ne supprime plus rien (`vault_doctor.py`)**
   - Seules les fiches dont le frontmatter **brut** contient `origin: gemini_takeout` et un `session_id` sont examinées (le défaut `origin=["gemini_takeout"]` du modèle Pydantic n'est plus pris en compte). Notes vocales, nocturnes, manuelles et fusionnées ne sont ni purgées ni réécrites.
   - Les fiches tronquées ou en fallback sont déplacées dans `02_Concepts/_Quarantine/` (`move_to_quarantine`) au lieu d'être supprimées par `unlink()`.
   - Nouveau chemin `settings.CONCEPTS_QUARANTINE_DIR`, créé par `ensure_directories()` et exclu de la réécriture des wikilinks.

6. **A7 — La fusion ne peut plus écraser une note tierce ni écrire hors de `02_Concepts/` (`graph_defragmenter.py`)**
   - `_resolve_canonical_target` : le slug proposé par le LLM est slugifié strictement (`safe_slug`), le chemin résolu doit rester sous `02_Concepts/` (`resolve_within`), et une note existante hors de la paire fusionnée n'est jamais écrasée (suffixe `-2`, `-3`…).

7. **A8 — La fusion conserve l'information et les sessions sources**
   - Le prompt de décision reçoit les corps complets des deux fiches (jusqu'à 12 000 caractères chacune, contre 1 500) avec la consigne de ne perdre aucun fait.
   - La fiche fusionnée porte `session_ids` (union des sessions sources) et `merged_from` dans son frontmatter. Le Vault Doctor les reconnaît : les sessions fusionnées restent « terminées » en mode Delta et ne sont plus redistillées puis refusionnées.

8. **D3 — Chemins contrôlés par la requête**
   - Nouveau module `src/utils/path_safety.py` (`safe_slug`, `resolve_within`, `is_within`, `is_under_any`).
   - `GET /api/concepts/{slug}` : refuse `..`, `/` et `\` (400) ; le chemin résolu doit rester sous `02_Concepts/`.
   - Projets : `build_project_record` (dans `kanban_engine.py`) slugifie `project_id`, valide le préfixe (`^[A-Z0-9]{1,8}$`) et le dépôt (`validate_repo_path`).
   - `repo_path` doit être un dossier absolu existant contenant `.git` et, si la variable `KANBAN_ALLOWED_REPO_ROOTS` est définie (racines séparées par `;`), situé sous l'une d'elles. Le context-pack revalide le dépôt avant d'en lister l'arborescence.
   - `attach_spec_to_task` écrit la spec sous `03_Kanban_Specs/<slug-projet>/`, chemin vérifié par `resolve_within`.
   - `KanbanEngine.create_task` refuse un projet inconnu (404 côté API) au lieu d'échouer sur la clé étrangère.

### 1.3 Divers
- Version centralisée dans `src/__init__.py` (`__version__ = "0.5.1"`), lue par l'API FastAPI ; bandeau web et `start_web_center.bat` mis à jour.
- Nouveaux réglages (`src/config.py`) : `KANBAN_ALLOWED_REPO_ROOTS`, `SCREEN_ORPHAN_MAX_AGE_HOURS`, propriété `CONCEPTS_QUARANTINE_DIR`.
- Nouveau `tests/conftest.py` : fixture `exo_env` qui isole complètement un test (coffre, SQLite et LanceDB sous `tmp_path`, singletons `kanban_engine` et `vector_store` redirigés, Ollama simulé hors ligne).

### 1.4 Fichiers modifiés
`src/__init__.py`, `src/config.py`, `src/utils/path_safety.py` (nouveau), `src/database/db_manager.py`, `src/consolidators/vault_doctor.py`, `src/consolidators/graph_defragmenter.py`, `src/consolidators/kanban_engine.py`, `src/consolidators/night_consolidator.py`, `src/daemons/telemetry_daemon.py`, `src/api/server.py`, `src/dashboard/app.py`, `src/web_gui/index.html`, `start_web_center.bat`, `tests/conftest.py` (nouveau), `tests/test_v051_data_loss_verification.py` (nouveau).

## 2. VÉRIFICATION

Suite `tests/test_v051_data_loss_verification.py` (14 tests), qui rejoue les reproductions de l'audit :

| Test | Constat |
| --- | --- |
| `test_a1_restart_keeps_short_live_and_voice_sessions` | A1 : 2 sessions courtes intactes après redémarrage, tour suivant à 2 |
| `test_a1_orphan_messages_rebuild_their_session` | A1 : migration v2 (vocal) et reconstruction live |
| `test_a1_footprint_dedup_runs_once` | A1 : `user_version` ≥ 2 |
| `test_a2_project_update_keeps_tasks` | A2 : 3 tâches → 3 après renommage ; doublon refusé |
| `test_a3_reingestion_preserves_status_and_summary` | A3 : `misc_noise` et résumé 26B préservés |
| `test_a4_pass1_analyzes_every_screenshot_and_purges_orphans` | A4 : 60 captures analysées (> 50), orphelins purgés, capture récente épargnée |
| `test_a4_daemon_deletes_replaced_screenshot` | A4 : la capture remplacée est supprimée |
| `test_a4_unprocessed_query_skips_pending_screenshots` | A4 : pas de marquage avant vision |
| `test_a6_vault_doctor_scope_and_quarantine` | A6 : notes vocale, nocturne et manuelle intactes ; fiche Takeout tronquée en quarantaine |
| `test_a7_a8_merge_is_confined_and_keeps_session_ids` | A7 : `budget-2027` non écrasée, `../01_Episodique/…` confiné ; A8 : `session_ids` reconnus |
| `test_a8_merge_prompt_receives_full_bodies` | A8 : un détail placé après 1 500 caractères atteint le prompt |
| `test_d3_api_rejects_path_traversal_and_invalid_projects` | D3 : `..%5C…` refusé, slug assaini, dépôt non Git refusé, 409, 404, PUT |
| `test_d3_spec_written_inside_kanban_dir` | D3 : spec d'un projet hérité `../../…` confinée |
| `test_d3_repo_path_must_be_git_repo` | D3 : `.git` exigé |

Résultats (pytest lancé avec `VAULT_ROOT` pointant vers un coffre temporaire) :
- `test_v051` + suites hermétiques v0.2.0 → v0.4.1 : **42 passed**.
- Suites v0.1.2, v0.1.3, v0.1.4 et v0.5.0 : 5 échecs **identiques avant et après ce lot**. Ils viennent des volumes personnels codés en dur dans ces tests (constat F1), traités au lot 6 (v0.5.6).

## 3. POINTS D'ATTENTION
- Les fiches précédemment mises en quarantaine n'existent pas : celles supprimées par les versions antérieures du Vault Doctor ne sont pas récupérables par ce patch.
- Les sessions live effacées avant ce patch sont reconstruites au prochain tour capturé dans la même conversation ; les sessions vocales le sont dès le premier démarrage (migration v2).
- Un projet dont `repo_path` n'est pas un dépôt Git reste enregistré, mais son arborescence n'est plus incluse dans le context-pack (message explicite à la place).
