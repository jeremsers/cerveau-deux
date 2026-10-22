# CHANGELOG — VERSION v0.1.4 (CONSOLIDATION SÉMANTIQUE, ANTI-COLLISION & DASHBOARD 100 %)

**Projet :** Exocortex & Télémétrie Cognitive  
**Date :** 21 Octobre 2026  
**Environnement Matériel :** Windows 11 Pro, GPU NVIDIA GeForce RTX 4070 Ti Super (16 Go VRAM), CPU Intel Core i7-14700KF, 64 Go RAM DDR5.

---

## 1. Contexte & Objectifs de la v0.1.4

Après la validation à 100 % du Cold Start en v0.1.3-hotfix (480 fiches conceptuelles valides dans `Vault_Data/02_Concepts/`, 6 649 messages préservés dans `chat_messages`, 73 153 empreintes dédupliquées dans `historical_footprints`, et 253 journaux épisodiques reconstitués), la version **v0.1.4** parachève l'architecture logicielle :
1. **Résolution sémantique atomique en Passe 2** : Élimination définitive des méga-notes fourre-tout nommées d'après les 16 macro-catégories (ex: `ia-et-llm-local.md`) au profit de véritables fiches atomiques spécifiques aux travaux observés.
2. **Exclusion mutuelle stricte VRAM en consolidation** : Recherche préalable de correspondances sur fiches existantes réalisée à 100 % sur CPU (aucun appel à `vector_store.search` / modèle `bge-m3` pendant que Gemma 4 26B ou 12B réside en mémoire GPU).
3. **Verrouillage anti-collision multi-sessions** : Protection contre l'écrasement silencieux de notes traitant du même sujet à des dates distinctes dans l'ingestor Takeout et déduplication rigoureuse de la clé primaire LanceDB par slug canonique.
4. **Finalisation à 100 % du Dashboard Streamlit** : Correction des requêtes SQL d'agrégation d'hyperfocus et implémentation de l'**Onglet 5 — Explorateur Épistémique & Empreintes** (Moteur de recherche plein texte Gemini et Archéologie des 73k empreintes).

---

## 2. Détail des Lots Implémentés

### Lot 1 : Alignement Paramétrique & Nettoyage du Code Mort
- **`src/config.py` & `.env.example`** :
  - `INACTIVITY_SESSION_THRESHOLD_MIN` ajusté à **45 minutes** par défaut (au lieu de 120), correspondant exactement à la granularité cognitive validée lors du Cold Start.
  - Exposition explicite de `PROLONGED_SESSION_THRESHOLD_SEC=180` dans `.env.example` pour la capture visuelle `.webp` du démon Win32.
- **`src/consolidators/night_consolidator.py`** :
  - Suppression définitive du couplage obsolète `from src.ingestors.takeout_ingestor import register_new_taxonomy_tag`.

### Lot 2 : Verrouillage Anti-Collision des Slugs et Clés Primaires LanceDB
- **`src/database/vector_store.py`** :
  - La suppression préalable dans LanceDB utilise désormais le slug canonique : `slug = '{safe_slug}' OR id = '{safe_id}'`.
  - Le `doc_id` PyArrow intègre le stem du fichier : `f"{raw_id}_{file_path.stem[:32]}"`, éliminant tout risque d'écrasement si deux notes sont créées la même minute (`YYYYMMDDHHMM`).
- **`src/ingestors/takeout_ingestor.py`** :
  - Dans `save_distilled_concept_note()`, vérification de la concordance du `session_id` si le fichier `CONCEPTS_DIR / f"{slug}.md"` existe déjà sur le disque.
  - En cas de session distincte, le slug est automatiquement suffixé (`{slug}-{created_date_str}-{short_sid}`), garantissant zéro écrasement silencieux.

### Lot 3 : Refonte de la Passe 2 du NightConsolidator (Structuration Pydantic & Matcher CPU)
- **`src/consolidators/night_consolidator.py`** :
  - Introduction du schéma Pydantic `NightConceptSynthesisSchema` : `concept_title`, `slug`, `tags`, `summary_1_line`, `synthesized_markdown_body`, `related_concepts`.
  - Implémentation du matcher lexical CPU pur `_find_matching_existing_concept_cpu(topic_name, topic_items)` garantissant le respect de l'exclusion mutuelle VRAM (zéro chargement de `bge-m3` pendant l'inférence LLM).
  - Si une note existante correspond, enrichissement chirurgical de la note existante avec une section `### Session du {date_str} ({duration_fmt})` et incrémentation de `total_time_invested_min`.
  - Si aucune note ne correspond, génération structurée d'une note conceptuelle atomique (ex: `optimisation-pipeline-rag-lancedb.md`) classée sous `semantic_topic`, avec protection anti-collision sur le slug.

### Lot 4 : Dashboard Streamlit "Bandeur de Stats" (100 %)
- **`src/dashboard/app.py`** :
  - **Correction SQL `load_macro_kpis()`** : Découplage strict entre la requête d'agrégation (`AVG(context_switches_per_hour), AVG(read_vs_write_ratio)`) et la requête déterministe récupérant le record d'hyperfocus (`SELECT max_hyperfocus_sec, max_hyperfocus_topic FROM daily_metrics WHERE max_hyperfocus_sec IS NOT NULL ORDER BY max_hyperfocus_sec DESC LIMIT 1;`).
  - **Onglet 5 — 🔍 Explorateur Épistémique & Empreintes** :
    - **Volet A (Recherche Gemini)** : Moteur plein texte interrogeant `chat_messages` (`user_prompt`, `ai_response`) et `chat_sessions` (`summary`), filtres par macro-catégorie et statut de distillation, affichage des métadonnées, aperçu direct des fiches conceptuelles associées depuis `Vault_Data/02_Concepts/`, et expander des tours de conversation complets.
    - **Volet B (Archéologie des Empreintes & Burst Clusters)** : 5 KPIs globaux (73 153 empreintes, 44k YouTube, 28k Search, Burst Clusters, Liées à Gemini), graphique horizontal Plotly du Top 15 des chaînes et domaines les plus consultés, tableau des Burst Clusters denses (tunnels $\ge 3$ événements en 45 min), et explorateur tabulaire paginé avec recherche multi-critères.
  - Encapsulation propre de l'UI dans `render_dashboard()` pour permettre l'importation propre et silencieuse des fonctions de requêtes dans les suites de tests sans alertes `ScriptRunContext`.

### Lot 5 : Suite de Tests de Validation Automatisée
- **`tests/test_v014_verification.py`** :
  - `test_lot1_config_parameters` : Validation de `INACTIVITY_SESSION_THRESHOLD_MIN == 45` et `PROLONGED_SESSION_THRESHOLD_SEC == 180`.
  - `test_lot2_slug_anti_collision_takeout` : Validation de la préservation de la note originale et génération d'une note suffixée sans écrasement.
  - `test_lot2_lancedb_vector_store_slug_key` : Validation de la suppression LanceDB par slug et de l'unicité du `doc_id`.
  - `test_lot3_night_consolidator_schema_and_purity` : Validation du schéma `NightConceptSynthesisSchema`, absence d'import obsolète, et présence de la méthode CPU.
  - `test_lot4_dashboard_macro_kpis_sqlite` : Validation des KPIs macro sans erreur de syntaxe SQL.
  - `test_lot4_dashboard_tab5_chat_search` : Validation des requêtes de recherche de sessions et messages Gemini.
  - `test_lot4_dashboard_tab5_footprints` : Validation de l'agrégation des 73k empreintes, du top 15 et des clusters.

---

## 3. Résultats des Tests & Statut d'Exécution

```text
============================= test session starts =============================
platform win32 -- Python 3.11.4, pytest-8.3.5, pluggy-1.5.0
rootdir: C:\Users\Jijax\projets\cerveau-deux
collected 7 items

tests\test_v014_verification.py .......                                  [100%]
======================== 7 passed in 4.45s ========================
```

Le script `test_v013_verification.py` s'exécute également avec succès (0 régression sur le Mode Delta, les invariants VRAM, la déduplication SQLite ou l'assainissement in-place).

