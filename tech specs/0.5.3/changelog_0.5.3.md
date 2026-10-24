---
task_id: "EXO-017"
project_id: "exocortex"
component_tag: "pipeline-restoration"
title: "v0.5.3 — Audit Lot 3 : Rétablissement des Fonctions Annoncées mais Inertes"
status: "done"
---
# EXO-017 — v0.5.3 — Audit Lot 3 : Rétablissement des Fonctions Annoncées mais Inertes

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif du Patch
Troisième lot de l'audit du 24/10/2026 : faire réellement tourner des étapes annoncées depuis v0.0 à v0.4.0 mais qui ne s'exécutaient pas, et empêcher qu'un manque de VRAM ou un Ollama éteint fasse échouer tout un pipeline. Corrige B11, B12, B13, B14, B15, B16 et A11.

### 1.2 Corrections

1. **B12 — Distillation des mémos vocaux (`voice_ingestor.py`)**
   - L'appel à `llm_client.generate()` (méthode inexistante, erreur avalée) est remplacé par `generate_structured` avec le nouveau schéma `VoiceMemoSchema` (titre, topic, tags, résumé, corps) et les prompts `PROMPT_VOICE_MEMO_SYSTEM/USER` (taxonomie fermée complète, plus une liste partielle de 9 catégories).
   - Topic normalisé par `normalize_to_macro_topic`. Sans LLM, la fiche est classée `A_Trier` au lieu de `Dev_et_Architecture_Tech` d'office.
   - La transcription brute est conservée sous la synthèse ; la session vocale reçoit topic, fiche liée et résumé (`update_session_distillation_metadata`).

2. **B13 — Report propre quand la VRAM manque (`takeout_ingestor.py`)**
   - `VRAMInsufficientError` est importée ; sous 8 Go libres avant la Vague 1, la distillation est **reportée** (sessions laissées `pending`, reprises au run suivant par le mode Delta) au lieu de lever une `NameError`. Registre du bruit et journaux cold start sont tout de même produits.
   - `initialize_meta_and_concepts` retourne un rapport (`distilled_success`, `quarantined`, `llm_noise`, `deferred_sessions`), repris dans le résultat de `TakeoutIngestor.run()`.

3. **B14 — Mode `cloud_api` indépendant d'Ollama**
   - Nouvelle « Vague 0 » : en `TAKEOUT_MODE=cloud_api` avec une clé Gemini, toutes les sessions passent d'abord par Gemini, sans condition sur Ollama ni sur la VRAM. Seules les sessions en échec retombent sur les vagues locales (ou restent `pending` si Ollama est éteint).
   - Construction du prompt factorisée (`_build_distillation_prompt`) pour les quatre vagues.

4. **B15 — Profil cognitif réellement produit**
   - Prompt de profilage aligné sur la taxonomie fermée : un seul livrable, le profil, situé dans les 16 macro-catégories ; plus de demande de taxonomie de 15 à 30 topics.
   - Nouvelle commande `python run_exocortex.py --import-profile <fichier>` (mode `web_manual`) : extrait le profil de la réponse Gemini (y compris au format à deux livrables `===SPLIT_LIVRABLE===`), refuse un contenu vide, ne touche jamais à `Taxonomie_Tags.md`.
   - Mode `cloud_api` : profil généré automatiquement depuis `00_USER_PROMPTS_ONLY.md` (`generate_cognitive_profile_cloud`), uniquement tant que le profil est le gabarit par défaut (marqueur `<!-- exocortex:profil-gabarit -->` ou signature de l'ancien gabarit). Un profil importé ou écrit à la main n'est jamais écrasé.
   - Consignes `PROMPT_A_COPIER_DANS_GEMINI_WEB.txt` mises à jour (étape d'import).

5. **B11 — Topic des rafales Search/YouTube**
   - `classify_burst_clusters` : rafales sans topic classées par lots de 15 au 12B (`BurstBatchClassification`, prompts `PROMPT_BURST_CLUSTER_*` enfin appelés), puis repli CPU par vote des mots des requêtes (`heuristic_burst_topic`) pour les rafales non résolues. Exécuté dans `TakeoutIngestor.run()` après le clustering.
   - `update_footprint_clusters_batch` ne remet plus le topic à `NULL` lors d'un re-clustering (`COALESCE`). Nouvelles méthodes `get_untopiced_burst_clusters` et `set_cluster_topic`.
   - Effet : le compteur « recherches/vidéos » par topic de l'injecteur (`get_topic_telemetry_stats`) n'est plus bloqué à 0.

6. **A11 — Classification exhaustive et reconsolidation (`night_consolidator.py`)**
   - La Passe 1 classe les activités par lots de 500 **jusqu'à épuisement** (`_classify_activity_batch`), au lieu de 500 par nuit.
   - Les dates dont une activité vient d'être classée (`last_classified_dates`) sont reconsolidées même si leur journal existe déjà.
   - Plus aucune fiche conceptuelle n'est créée pour la part `Non_Classe`/`A_Trier` d'une journée.

7. **B16 — Mode CPU de la consolidation nocturne**
   - Sous 8 Go de VRAM libre (jeu lancé la nuit), la consolidation n'est plus abandonnée : `cpu_only` active la classification heuristique, le calcul des `daily_metrics`, les journaux (synthèse déterministe), le bootloader de repli et la compilation Drive. Vision, synthèses LLM, création de fiches et indexation LanceDB sont reportées.
   - Les captures en attente sont conservées pour la nuit suivante (jamais marquées traitées sans vision).
   - Les dates consolidées sans LLM sont notées dans `_System_Buffer/pending_llm_dates.json` puis re-synthétisées et retirées de la liste à la première nuit où le LLM est disponible. Une `VRAMInsufficientError` levée en Passe 2 bascule aussi en mode CPU.
   - Le résultat de `consolidate()` expose `cpu_only`.

### 1.3 Fichiers modifiés
`src/__init__.py`, `src/llm/prompts.py`, `src/ingestors/takeout_ingestor.py`, `src/ingestors/voice_ingestor.py`, `src/consolidators/night_consolidator.py`, `src/database/db_manager.py`, `run_exocortex.py`, `src/web_gui/index.html`, `start_web_center.bat`, `tests/test_v053_inert_features_verification.py` (nouveau).

## 2. VÉRIFICATION

Suite `tests/test_v053_inert_features_verification.py` (11 tests) :

| Test | Constat |
| --- | --- |
| `test_b12_voice_memo_is_distilled_with_structured_output` | Mémo « budget vacances » classé `Admin_Finance_et_Droit`, titre LLM, transcription conservée, fiche liée à la session |
| `test_b12_voice_memo_offline_is_quarantined_not_dev` | Sans LLM : `A_Trier`, plus `Dev` |
| `test_b13_low_vram_defers_distillation_without_crash` | VRAM 5 Go : aucune exception, 2 sessions reportées `pending`, journaux produits |
| `test_b14_cloud_mode_works_with_ollama_off` | Ollama éteint : 1 appel Gemini, 1 fiche |
| `test_b11_bursts_receive_a_topic` | 2 rafales classées (LLM + repli), topics conservés après re-clustering |
| `test_b15_import_profile_keeps_closed_taxonomy` | Profil importé, second livrable ignoré, taxonomie intacte |
| `test_b15_cloud_profile_replaces_template_only` | Profil cloud généré une fois, jamais réécrit ensuite |
| `test_a11_pass1_classifies_until_exhaustion` | 1 200 activités classées en une nuit |
| `test_a11_dates_with_new_activities_are_reconsolidated` | Journal existant du 01/10 recalculé (210 activités) |
| `test_a11_no_concept_note_for_unclassified_share` | 2 h `A_Trier` → aucune fiche |
| `test_b16_low_vram_night_runs_in_cpu_mode` | VRAM 4 Go : aucune inférence, métriques + journal + Drive produits, date en attente puis enrichie la nuit suivante |

Résultats (coffre temporaire) : **74 passed** sur les suites hermétiques v0.2.0 → v0.5.3 ; les 5 échecs préexistants de v0.1.2–v0.1.4 sont inchangés (F1, lot 6). Commande `--import-profile` testée manuellement (import réussi, fichier absent refusé).

## 3. POINTS D'ATTENTION
- La première ingestion Takeout après cette version classera toutes les rafales existantes : compter environ un appel 12B par lot de 15 rafales.
- Les mémos vocaux déjà ingérés gardent leur ancien topic ; seuls les nouveaux bénéficient de la distillation.
- En mode CPU, la classification heuristique est définitive pour les activités concernées (seule la synthèse est enrichie ensuite).
