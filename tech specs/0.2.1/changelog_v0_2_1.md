---
task_id: "EXO-008"
project_id: "exocortex"
component_tag: "core-refactoring"
title: "Consolidation Architecturale v0.2.1 : Vault IO PyYAML, Idempotence Nocturne BM25, Démons Win32 & Découplage Modulaire"
status: "ready_for_agent"
---
# EXO-008 — Consolidation Architecturale v0.2.1 : Vault IO PyYAML, Idempotence Nocturne BM25, Démons Win32 & Découplage Modulaire

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1. Contexte & Objectifs du Patch `v0.2.1`
Avec l'achèvement de la `v0.2.0-core` (Module 7 Kanban), l'ensemble des 7 modules fonctionnels de l'Exocortex est en place. Avant toute nouvelle itération fonctionnelle, la version **`v0.2.1`** a pour unique objectif d'éradiquer la dette technique accumulée lors des patchs `v0.1.1` à `v0.2.0`, de verrouiller l'intégrité des données du coffre Obsidian (`Vault_Data/`) et de garantir une idempotence mathématique stricte sur tous les traitements.

---

### 1.2. Chantier 1 : Unification du Parsing Markdown/YAML (`src/utils/markdown_io.py`)
**Problème identifié :**  
Les modules `vector_store.py`, `drive_compiler.py`, `night_consolidator.py` et `takeout_ingestor.py` lisent et modifient les notes Markdown via des expressions régulières fragiles (`re.match`, `line.split(":", 1)`). Un caractère `:` dans un titre ou un résumé corrompt le frontmatter YAML. Par ailleurs, relancer `night_consolidator.py` sur une même date incrémente indéfiniment `total_time_invested_min` et duplique les sections `### Session du YYYY-MM-DD`.

**Architecture cible :**
1. Créer le package `src/utils/` avec `src/utils/__init__.py` et `src/utils/markdown_io.py`.
2. Implémenter dans `src/utils/markdown_io.py` :
   - Un modèle Pydantic v2 `ConceptFrontmatter` avec validation et normalisation automatique (`normalize_to_macro_topic` sur `semantic_topic`) :
     - `id: str`
     - `title: str`
     - `type: str = "concept"`
     - `origin: List[str] = Field(default_factory=lambda: ["gemini_takeout"])`
     - `semantic_topic: str = "Dev_et_Architecture_Tech"`
     - `tags: List[str] = Field(default_factory=list)`
     - `session_id: Optional[str] = None`
     - `distillation_status: str = "success"`
     - `created_at: str`
     - `updated_at: str`
     - `total_time_invested_min: int = 0`
     - `summary_1_line: str = ""`
   - Un modèle `ParsedConceptNote` contenant :
     - `frontmatter: ConceptFrontmatter`
     - `title_h1: str`
     - `body: str` (le corps analytique pur, **sans** le titre H1 et **sans** le callout de télémétrie)
     - `telemetry_lines: List[str]` (les lignes du bloc `> [!abstract]- Généalogie & Télémétrie`)
     - `file_path: Optional[Path] = None`
   - Les fonctions `parse_concept_file(file_path: Path) -> ParsedConceptNote` et `parse_concept_string(raw_text: str, file_path: Optional[Path] = None) -> ParsedConceptNote` utilisant exclusivement `yaml.safe_load()` pour le bloc YAML (avec repli gracieux de réparation si un ancien fichier a des guillemets mal échappés).
   - La fonction `serialize_concept_note(note: ParsedConceptNote) -> str` et `write_concept_file(note: ParsedConceptNote, target_path: Path) -> None` utilisant `yaml.safe_dump(..., sort_keys=False, allow_unicode=True)` et reconstruisant proprement le fichier selon le contrat exact de l'Exocortex.
   - Une méthode d'enrichissement **100 % idempotente** sur `ParsedConceptNote` :
     `append_or_replace_daily_session(date_str: str, duration_min: int, duration_fmt: str, enrichment_markdown: str, related_links: Optional[List[str]] = None) -> bool` :
     - Vérifie si la source `Activité écran du \`{date_str}\`` ou la section `### Session du {date_str}` existe déjà dans la note.
     - Si elle existe déjà : remplace le contenu de la sous-section `### Session du {date_str}` par le nouveau texte, **sans** additionner une seconde fois `duration_min` à `total_time_invested_min` (ou ajuste uniquement le delta si la durée a changé).
     - Si elle n'existe pas : ajoute `duration_min` à `total_time_invested_min`, insère la ligne de source dans `telemetry_lines`, et insère la section `### Session du {date_str}` juste avant le callout final.
3. Remplacer tous les parsings manuels par regex dans `src/database/vector_store.py`, `src/consolidators/drive_compiler.py`, `src/consolidators/night_consolidator.py` et `src/ingestors/takeout_ingestor.py` par les appels à `markdown_io`.

---

### 1.3. Chantier 2 : Pertinence du Matcher CPU BM25 & Idempotence dans `night_consolidator.py`
**Problème identifié :**  
Dans `src/consolidators/night_consolidator.py`, la méthode `_find_matching_existing_concept_cpu()` compte simplement le nombre de mots de $\ge 4$ lettres en commun ($\ge 3$ mots). Trois termes génériques comme `script`, `code`, `fichier` suffisent à fusionner deux sujets totalement étrangers.

**Architecture cible :**
1. Remplacer l'heuristique naïve de `_find_matching_existing_concept_cpu(self, topic_name: str, topic_items: List[str]) -> Optional[Path]` par un algorithme **BM25 / TF-IDF pondéré en pur Python/math** (0 Mo VRAM, < 20 ms CPU) :
   - Filtrer d'abord les notes de `02_Concepts/` ayant `frontmatter.semantic_topic == topic_name` (via `parse_concept_file`).
   - Construire pour chaque note candidate un corpus pondéré : les tokens du `title` et du `slug` ont un poids $\times 3$, les `tags` ont un poids $\times 2$, et `summary_1_line` a un poids $\times 1$.
   - Calculer l'Inverse Document Frequency ($\text{IDF}(t) = \ln\left(1 + \frac{N - n_t + 0.5}{n_t + 0.5}\right)$) sur l'ensemble des notes du coffre pour pénaliser les mots ubiquitaires (`python`, `configuration`, `analyse`, `optimisation`, `architecture`, `systeme`, `projet`, `donnees`, `creation`).
   - Exiger à la fois :
     - Au moins **2 tokens distinctifs** (à fort IDF) présents directement dans l'union `(title + slug + tags)` de la fiche candidate.
     - Un score de similarité normalisé strict avant d'autoriser la fusion. Sinon, retourner `None` pour forcer la création d'une nouvelle fiche conceptuelle atomique propre.
2. Utiliser `ParsedConceptNote.append_or_replace_daily_session(...)` en Passe 2 pour garantir qu'exécuter `--consolidate --date YYYY-MM-DD` 5 fois d'affilée produit **exactement** le même fichier Markdown et le même `total_time_invested_min`.

---

### 1.4. Chantier 3 : Découpage de `takeout_ingestor.py` & Isolation du `VaultDoctor`
**Problème identifié :**  
`src/ingestors/takeout_ingestor.py` dépasse 1 700 lignes et mélange le parsing bas niveau (HTML/JSON), la maintenance/réparation du coffre (`scan_and_upgrade_existing_concepts`) et l'orchestration LLM.

**Architecture cible :**
1. Créer `src/ingestors/takeout_parsers.py` :
   - Y déplacer `ParsedTurn`, `ReconstructedSession`, `FRENCH_MONTH_MAP`, `parse_date_flexible()`, `sanitize_turn_text()`, `compute_realistic_session_duration_min()`, `parse_gemini_html()`, `parse_gemini_json()`, `parse_youtube_export()`, `parse_google_search_export()`, et `sessionize_gemini_turns()`.
2. Créer `src/consolidators/vault_doctor.py` :
   - Y déplacer et moderniser (avec `markdown_io`) la fonction `scan_and_upgrade_existing_concepts(db: DBManager) -> Set[str]` ainsi que `ensure_strict_taxonomy_file()`.
   - Exposer une classe `VaultDoctor` permettant d'auditer, réparer et normaliser les notes de `02_Concepts/`.
3. Conserver les ré-exports (`from src.ingestors.takeout_parsers import ...` et `from src.consolidators.vault_doctor import ...`) dans `src/ingestors/takeout_ingestor.py` pour garantir **100 % de rétrocompatibilité** avec les suites de tests existantes (`test_v012`, `test_v013`, `test_v014`).

---

### 1.5. Chantier 4 : Durcissement des Démons Win32 (`hippocampus_hotkey.py` & `telemetry_daemon.py`)
**Problème identifié :**
1. Dans `src/daemons/hippocampus_hotkey.py`, `simulate_select_and_copy()` fait un `time.sleep(0.05)` aveugle après `Ctrl+C` et écrase définitivement le presse-papier précédent de l'utilisateur. Si le navigateur met 90 ms à copier, `pyperclip.paste()` lit l'ancien presse-papier.
2. Dans `src/daemons/telemetry_daemon.py`, `capture_window_webp()` utilise `PIL.ImageGrab.grab(bbox=...)` sans gérer les écrans multiples à coordonnées négatives ni le DPI Awareness sous Windows 11, alors que `mss` est déjà installé dans `requirements.txt`.

**Architecture cible :**
1. **Dans `src/daemons/hippocampus_hotkey.py` :**
   - Avant `Ctrl+A` / `Ctrl+C`, sauvegarder le contenu actuel du presse-papier (`previous_clipboard = pyperclip.paste()`) et placer une sentinelle vide `pyperclip.copy("")`.
   - Après l'envoi de `Ctrl+C`, effectuer une boucle de polling rapide (`max_wait_ms = 350`, pas de `15 ms`) attendant que `pyperclip.paste()` devienne non vide.
   - Si rien n'a été capturé après 350 ms, restaurer `previous_clipboard` et annuler proprement.
   - Après `simulate_paste_payload(enriched_payload)` et un court délai de collage (`120 ms`), restaurer `previous_clipboard` dans le presse-papier afin que le raccourci `Alt+Espace` soit non-destructif pour le presse-papier de travail de l'utilisateur (tout en gardant une option ou un comportement sûr). *Note : laisser le payload enrichi dans le presse-papier uniquement si le collage automatique échoue.*
2. **Dans `src/daemons/telemetry_daemon.py` :**
   - Activer le DPI Awareness Windows 11 au démarrage du module (`ctypes.windll.shcore.SetProcessDpiAwareness(2)` ou `ctypes.windll.user32.SetProcessDPIAware()`) dans un bloc `try/except`.
   - Dans `capture_window_webp()`, utiliser `mss.mss()` en priorité pour capturer la boîte englobante `{"left": left, "top": top, "width": width, "height": height}` et convertir en `PIL.Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")`, avec repli automatique sur `ImageGrab.grab(bbox=..., all_screens=True)` en cas d'exception.

---

### 1.6. Chantier 5 : Rapatriement des Requêtes Analytiques SQLite & Modularisation de `app.py`
**Problème identifié :**  
`src/dashboard/app.py` contient 1 300 lignes et exécute des dizaines de requêtes SQL brutes directement dans le fichier d'interface. De plus, l'exécution du code Streamlit au niveau module (hors fonction) complique l'importation propre lors des tests.

**Architecture cible :**
1. Ajouter dans `src/database/db_manager.py` (ou via un helper read-only `get_ro_connection()`) les méthodes analytiques typées consommées par le Dashboard :
   - `fetch_macro_kpis() -> Dict[str, Any]`
   - `fetch_all_activity_dates() -> List[str]`
   - `fetch_timeline_for_date(target_date_str: str) -> List[Dict[str, Any]]`
   - `fetch_treemap_data() -> List[Dict[str, Any]]`
   - `fetch_archaeology_sessions() -> List[Dict[str, Any]]`
   - `fetch_circadian_timestamps() -> List[str]`
   - `search_chat_sessions(query: str, topic_filter: Optional[str], status_filter: Optional[str], limit: int) -> List[Dict[str, Any]]`
   - `fetch_messages_for_session(session_id: str) -> List[Dict[str, Any]]`
   - `fetch_footprints_summary() -> Dict[str, Any]`
   - `fetch_top_channels_and_domains(limit: int) -> List[Dict[str, Any]]`
   - `fetch_burst_clusters_summary(limit: int) -> List[Dict[str, Any]]`
   - `search_footprints(query: str, source_filter: str, only_clustered: bool, only_linked: bool, limit: int) -> List[Dict[str, Any]]`
2. Dans `src/dashboard/app.py` :
   - Les fonctions historiques (`load_macro_kpis`, `load_chat_search_results`, `load_messages_for_session`, `load_footprints_summary`, `load_top_channels_and_domains`, `load_burst_clusters_summary`, `search_historical_footprints`) restent présentes avec **exactement les mêmes signatures et types de retour** (DataFrames / Dicts) pour ne casser aucun test de `test_v014_verification.py`, mais délèguent désormais leurs requêtes SQL à `DBManager(read_only=True)`.
   - Encapsuler le rendu visuel des onglets dans une fonction `render_dashboard()` appelée uniquement lorsque le script est exécuté par Streamlit ou en `__main__`, évitant ainsi d'exécuter `st.title`, `st.tabs` et les rendus graphiques lorsqu'un test unitaire importe simplement `from src.dashboard.app import load_macro_kpis`.

---

### 1.7. Chantier 6 : Suite de Tests de Non-Régression `tests/test_v021_refactoring_verification.py`
Créer une suite de tests complète `tests/test_v021_refactoring_verification.py` vérifiant :
1. Le cycle complet `parse_concept_string` $\rightarrow$ modification $\rightarrow$ `serialize_concept_note` via `PyYAML`, y compris avec des deux-points `:` et des guillemets dans le titre et le résumé.
2. L'idempotence stricte de `append_or_replace_daily_session()` : appeler 3 fois l'enrichissement pour la journée `2026-10-23` (60 min) n'ajoute que `60` minutes au total et ne crée qu'une seule section `### Session du 2026-10-23`.
3. La précision du matcher CPU BM25 (`_find_matching_existing_concept_cpu`) : ne matche pas sur des mots génériques (`python`, `code`, `script`), mais matche avec précision sur des termes techniques spécifiques (`lancedb`, `bge-m3`, `pyarrow`).
4. Le découpage modulaire (`takeout_parsers.py`, `vault_doctor.py`) et la rétrocompatibilité des imports dans `takeout_ingestor.py`.
5. L'exécution à 100 % au vert de toute la suite : `test_v012`, `test_v013`, `test_v014`, `test_v020` et `test_v021`.

---
