Le patch de stabilisation EXO-013 (v0.4.1 — Hotfix Intégration, Isolation VRAM Sommeil Profond & Fix Filtres UI) a été implémenté et validé avec 100 % de succès (37/37 tests passés).

Détail des Corrections Appliquées

Isolation VRAM & Auto-Fusion Interdite (src/consolidators/graph_defragmenter.py) :

find_merge_and_contradiction_candidates() : ignore immédiatement toute paire candidate où path_a.resolve() == path_b.resolve() ou rec_a["slug"] == rec_b["slug"].
merge_concepts_pair() : lève explicitement une ValueError si l'on tente de fusionner une fiche avec elle-même. Accepte le paramètre defer_vector_sync: bool = False qui supprime les anciens slugs de LanceDB sans jamais solliciter l'embedding bge-m3.
run_defragmentation_cycle() : passe defer_vector_sync=True, collecte les fiches fusionnées, décharge le modèle de synthèse lourd (MODEL_HEAVY_SYNTHESIS) à la sortie de la boucle LLM, indexe ensuite les notes fusionnées dans LanceDB via vector_store, puis décharge MODEL_EMBEDDING.

Optimisation & Intégration du Cycle Nocturne (src/consolidators/night_consolidator.py) :

run_pass_2_synthesis() : ajout du paramètre run_bootloader: bool = True pour n'appeler generate_executive_bootloader() que lorsque run_bootloader=True.
consolidate() :
Lance automatiquement VoiceIngestor(db_manager=self.db).run() en Passe 0 si des mémos sont présents dans voice_inbox/.
Si target_date est spécifié, ne traite que [target_date]. Sinon, filtre pour ne traiter que les dates n'ayant pas encore de fichier journal 01_Episodique/YYYY-MM-DD.md plus la date la plus récente max_date.
Passe run_bootloader=(d == max(dates_to_process)) pour garantir que le Bootloader ne reflète que la date la plus récente sans être écrasé.

Alignement UI & Résumé Live Chat (src/dashboard/app.py & src/database/db_manager.py) :

Dans db_manager.py (upsert_live_chat_turn) : initialise summary avec clean_prompt[:140] lors de la création de la session live pour éviter les intitulés vides dans l'Explorateur Épistémique.
Dans app.py : options de statut mises à jour avec les vraies valeurs SQLite (["Tous", "success", "pending", "misc_noise", "failed_fallback"]) et suppression de la fonction morte get_ro_connection().

Nettoyage Résiduel (src/ingestors/takeout_ingestor.py) :

Utilisation de parse_concept_file() dans save_distilled_concept_note() pour la vérification anti-écrasement et anti-collision de slug.

Nouvelle Suite de Vérification (tests/test_v041_hotfix_verification.py) :

test_defragmenter_no_self_merge_and_vram_isolation : auto-fusions bloquées et ordre strict d'exclusion VRAM validé.
test_night_consolidator_bootloader_only_on_latest_date : vérification que le Bootloader porte la date la plus récente.
test_live_chat_turn_initializes_summary : validation de l'initialisation du summary au premier tour de chat.
Résultats des Tests
powershell
======================= 37 passed, 4 warnings in 26.42s =======================
tests/test_v012_verification.py (1 test)          PASSED                  [  2%]
tests/test_v013_verification.py (1 test)          PASSED                  [  5%]
tests/test_v014_verification.py (7 tests)         PASSED                  [ 24%]
tests/test_v020_kanban_verification.py (4 tests)  PASSED                  [ 35%]
tests/test_v021_refactoring_verification.py (5)   PASSED                  [ 48%]
tests/test_v022_mcp_graphrag_verification.py (6)  PASSED                  [ 64%]
tests/test_v030_proactivity_verification.py (3)   PASSED                  [ 72%]
tests/test_v035_passive_sensors_verification.py (3) PASSED                [ 81%]
tests/test_v040_deep_sleep_verification.py (4)    PASSED                  [ 91%]
tests/test_v041_hotfix_verification.py (3)        PASSED                  [100%]