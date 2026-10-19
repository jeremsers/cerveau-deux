# CHANGELOG & PATCH D'INTÉGRATION CHIRURGICAL — v0.1.1

**Date :** 20 Octobre 2026
**Version cible :** `v0.1.1` (Verrouillage VRAM Windows 11 à 12.8 Go, Provisioning GGUF actif, Éradication du Thrashing VRAM en boucle, Fix Cloud SOTA & Débridage Takeout)
**Référence parente :** `tech specs/CHANGELOG & PLAN DE REDRESSEMENT ARCHITECTURAL — v0.1.md`

---

## 1. AUDIT D'INTÉGRATION POST-v0.1 (6 FAILLES CRITIQUES IDENTIFIÉES)

Bien que la version `v0.1` ait éradiqué les simulations statiques de la `v0.0` (suppression de `hashlib.sha256`, ajout de `DistilledConceptSchema`, vraie synthèse LLM en Passe 2 et taxonomie émergente), l'inspection du code source réel a mis en évidence **6 failles d'intégration critiques** qui dégradent l'exécution sur Windows 11 (RTX 4070 Ti Super 16 Go VRAM) :

1. **Seuil VRAM Windows 11 erroné (`14.5 Go` au lieu de `12.8 Go`) et variables Ollama absentes :**
   - Dans `src/config.py` (ligne 83) et `.env.example` (ligne 25), `FULL_DUAL_MODEL_VRAM_GB` est resté figé à `14.5`. Or, Windows 11 (DWM + processus système) consomme ~2 Go de VRAM au repos : sur une carte de 16 Go, la VRAM libre réelle plafonne autour de 13.5–14.0 Go. Conséquence : `check_and_select_model()` déclasse **systématiquement** le modèle architecte `gemma4:26b-a4b` vers le `12b`.
   - `start_exocortex.bat` ne configure pas les variables d'environnement indispensables (`OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_MAX_LOADED_MODELS=1`) permettant au modèle 26B MoE de tenir dans le budget VRAM sans basculer en RAM système (*Sysmem Fallback*).

2. **Code mort sur le provisioning GGUF (`ensure_local_gguf_models()`) :**
   - La méthode `ensure_local_gguf_models()` a été implémentée dans `src/llm/ollama_client.py` (ligne 143), mais **elle n'est appelée par aucun point d'entrée** (`run_exocortex.py`, `start_exocortex.bat`, `night_consolidator.py`, `takeout_ingestor.py`).
   - De plus, le `Modelfile` généré ne borne pas `PARAMETER num_ctx 8192`, exposant la VRAM à une allocation de contexte par défaut excessive.

3. **Thrashing catastrophique du SSD et de la VRAM dans les boucles (`keep_alive=0` unitaire) :**
   - Dans `src/consolidators/night_consolidator.py` (lignes 201, 259, 503, 584, 614) et `src/ingestors/takeout_ingestor.py` (ligne 883), les appels LLM situés **à l'intérieur des boucles `for`** passent systématiquement `keep_alive=0`.
   - Conséquence matérielle : à chaque itération de la boucle, Ollama charge 7.2 Go (ou 14 Go) depuis le SSD vers la VRAM, traite 1 seul élément, purge totalement la VRAM, puis recharge le modèle à l'itération suivante.
   - Règle d'ingénierie : passer `keep_alive="5m"` pendant toutes les itérations d'un même batch, et exécuter `llm_client.unload_model(...)` **une seule fois en sortie de boucle**.

4. **Crash `AttributeError` et `TypeError` sur le mode Cloud API (`takeout_ingestor.py`) :**
   - Ligne 863 : appel à `llm_client.is_cloud_available()` qui **n'existe pas** dans la classe `HybridLLMClient` (`src/llm/ollama_client.py`).
   - Ligne 867 : appel à `llm_client.generate_cloud_sota(..., system_prompt=...)` alors que la signature réelle dans `ollama_client.py` (ligne 526) attend `system=...` et supporte nativement `response_model=DistilledConceptSchema`.

5. **Contamination temporelle par `datetime.now()` résiduel dans YouTube et Google Search (`takeout_ingestor.py`) :**
   - Si le fallback `datetime.now()` a bien été retiré des parseurs Gemini, il est resté présent dans `parse_youtube_export()` (lignes 352, 382, 386) et `parse_google_search_export()` (lignes 413, 435, 439), faussant la chronologie si une date d'archive n'est pas reconnue.

6. **Bridage silencieux à 10 sessions, mauvais modèle de distillation et oubli d'indexation LanceDB (`takeout_ingestor.py`) :**
   - Ligne 831 : `top_sessions = sorted(...)[:10]` bride en dur la distillation aux 10 plus grosses sessions et ignore le reste de l'archive.
   - Ligne 882 : la distillation locale appelle `settings.MODEL_FAST_VISION` (`gemma4:12b`) au lieu de `settings.MODEL_HEAVY_SYNTHESIS` (`gemma4:26b-a4b`).
   - Fin de `takeout_ingestor.py` : aucune synchronisation vectorielle (`vector_store.sync_all_concepts()`) ni compilation Drive (`DriveCompiler().compile_all()`) n'est exécutée après la création des fiches dans `02_Concepts/`.

---

## 2. SPÉCIFICATIONS TECHNIQUES DES CORRECTIFS (PLAN D'EXÉCUTION v0.1.1)

### Correctif 1 : `src/config.py` et `.env.example` (Budget VRAM Windows 11 & Paramètre de Batch Takeout)

1. Dans `src/config.py`, abaisser la valeur par défaut de `FULL_DUAL_MODEL_VRAM_GB` à `12.8` et ajouter `TAKEOUT_MAX_DISTILL_SESSIONS` (par défaut `0` = sans limite, ou configurable via `.env`) :
```python
    # --- Contraintes Matérielles VRAM (RTX 4070 Ti Super 16 Go sous Windows 11) ---
    MIN_FREE_VRAM_GB: float = Field(
        default_factory=lambda: float(os.getenv("MIN_FREE_VRAM_GB", "8.0"))
    )
    FULL_DUAL_MODEL_VRAM_GB: float = Field(
        default_factory=lambda: float(os.getenv("FULL_DUAL_MODEL_VRAM_GB", "12.8"))
    )
    TAKEOUT_MAX_DISTILL_SESSIONS: int = Field(
        default_factory=lambda: int(os.getenv("TAKEOUT_MAX_DISTILL_SESSIONS", "0"))  # 0 = Toutes les sessions qualifiées
    )
```

2. Dans `.env.example`, aligner `FULL_DUAL_MODEL_VRAM_GB=12.8`, documenter `TAKEOUT_MAX_DISTILL_SESSIONS=0` et documenter les variables d'optimisation Ollama (`OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`).

---

### Correctif 2 : `src/llm/ollama_client.py` (Méthode Cloud, `Modelfile` optimisé VRAM & Typage `keep_alive`)

1. **Ajout de `is_cloud_available()` dans `HybridLLMClient` :**
```python
    def is_cloud_available(self) -> bool:
        """Vérifie si une clé API Gemini Cloud SOTA valide est configurée dans l'environnement."""
        return bool(settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY.strip()) > 5)
```

2. **Optimisation du `Modelfile` dans `ensure_local_gguf_models()` :**
   Ajouter `PARAMETER num_ctx 8192` dans `modelfile_content` pour garantir que le cache KV (quantifié en `q8_0`) du modèle `gemma4:26b-a4b` ne dépasse jamais les 16 Go de VRAM de la RTX 4070 Ti Super :
```python
            modelfile_content = (
                f'FROM "{gguf_path.resolve().as_posix()}"\n'
                'PARAMETER num_ctx 8192\n'
                'TEMPLATE """{{ if .System }}<start_of_turn>system\n'
                '{{ .System }}<end_of_turn>\n'
                '{{ end }}{{ if .Prompt }}<start_of_turn>user\n'
                '{{ .Prompt }}<end_of_turn>\n'
                '{{ end }}<start_of_turn>model\n'
                '{{ .Response }}<end_of_turn>\n'
                '"""\n'
                'PARAMETER stop "<start_of_turn>"\n'
                'PARAMETER stop "<end_of_turn>"\n'
            )
```

3. **Support de `keep_alive: Union[int, str] = 0` :**
   Mettre à jour la signature des méthodes `generate_text()`, `generate_vision()`, `generate_structured()` et `generate_embeddings()` pour accepter `keep_alive: Union[int, str] = 0` (permettant de passer `"5m"` ou `300` lors des traitements par lots et `0` pour une purge immédiate).

---

### Correctif 3 : `src/consolidators/night_consolidator.py` (Fin du Thrashing VRAM & Provisioning Pré-Consolidation)

1. **Dans `consolidate()` :** Appeler `llm_client.ensure_local_gguf_models()` au début du cycle nocturne pour garantir que `gemma4:12b` et `gemma4:26b-a4b` sont bien provisionnés dans Ollama avant la Passe 1.
2. **Dans `run_pass_1_vision_and_tagging()` :**
   - Lors de la boucle sur `screenshot_activities` (ligne 197), passer `keep_alive="5m"` à `llm_client.generate_vision(...)`.
   - Lors de la boucle sur `signatures` (ligne 254), passer `keep_alive="5m"` à `llm_client.generate_structured(...)`.
   - Conserver l'appel final `llm_client.unload_model(settings.MODEL_FAST_VISION)` en fin de Passe 1 (ligne 295) pour libérer 100 % de la VRAM avant la Passe 2.
3. **Dans `run_pass_2_synthesis()` :**
   - Passer `keep_alive="5m"` lors de l'appel `llm_client.generate_text(...)` pour le journal épisodique (ligne 503) et dans la boucle des fiches `02_Concepts/` (lignes 584 et 614).
   - Conserver l'appel final `llm_client.unload_model(effective_model)` en sortie de Passe 2 (ligne 659).
4. **Dans `src/database/vector_store.py` (`get_embedding` et `sync_all_concepts`) :**
   - Ajouter un paramètre `keep_alive: Union[int, str] = 0` à `get_embedding(self, text: str, keep_alive: Union[int, str] = 0)`.
   - Dans `index_concept_file()`, passer `keep_alive="5m"` pour que `sync_all_concepts()` vectorise toutes les notes du coffre sans décharger/recharger `bge-m3` à chaque fichier, puis décharger `bge-m3` une seule fois à la fin de `sync_all_concepts()`.

---

### Correctif 4 : `src/ingestors/takeout_ingestor.py` (Dates strictes, Modèle 26B, Débridage & Indexation Vectorielle)

1. **Suppression totale de `datetime.now()` dans `parse_youtube_export()` et `parse_google_search_export()` :**
   Utiliser exactement la même mécanique `last_valid_dt` que dans `parse_gemini_html()` : si `parse_date_flexible()` retourne `None`, utiliser `last_valid_dt` s'il existe, sinon faire `continue` (ignorer l'entrée corrompue).
2. **Débridage de la sélection des sessions dans `initialize_meta_and_concepts()` :**
   - Ajouter le paramètre `max_distill_sessions: Optional[int] = None` à `initialize_meta_and_concepts()` et `TakeoutIngestor.run()`.
   - Sélectionner toutes les sessions qualifiées (`turn_count >= settings.MIN_TURNS_THRESHOLD and user_char_count >= settings.MIN_USER_CHARS_THRESHOLD`). Si `limit = max_distill_sessions or settings.TAKEOUT_MAX_DISTILL_SESSIONS` est `> 0`, tronquer à `[:limit]`, sinon traiter **100 % des sessions qualifiées**.
3. **Correction de l'appel Cloud SOTA et Passage au Modèle 26B en Local :**
   - En mode `cloud_api` :
     ```python
     if settings.TAKEOUT_MODE == "cloud_api" and llm_client.is_cloud_available():
         try:
             distilled = llm_client.generate_cloud_sota(
                 prompt=user_prompt,
                 system=PROMPT_SESSION_DISTILLATION_SYSTEM,
                 response_model=DistilledConceptSchema,
             )
         except Exception as exc:
             logger.warning("Échec de distillation Cloud SOTA pour session %s : %s", sess.session_id, exc)
     ```
   - En mode local (`llm_client.is_alive()`) :
     - Appeler `llm_client.ensure_local_gguf_models()` avant la boucle de distillation.
     - Utiliser `model=settings.MODEL_HEAVY_SYNTHESIS` (`gemma4:26b-a4b`, avec repli automatique sur `12b` géré par `check_and_select_model` si VRAM < 12.8 Go) et `keep_alive="5m"` pendant la boucle.
     - En sortie de boucle, décharger explicitement le modèle (`llm_client.unload_all_models()`).
4. **Synchronisation LanceDB & Google Drive en fin d'ingestion (`TakeoutIngestor.run()`) :**
   - Après `initialize_meta_and_concepts()`, appeler `vector_store.sync_all_concepts()` et `DriveCompiler(self.db).compile_all()` pour que le coffre, la base vectorielle et Google Drive soient immédiatement opérationnels après le Cold Start.

---

### Correctif 5 : `run_exocortex.py` et `start_exocortex.bat` (Orchestration CLI & Variables d'Environnement Ollama)

1. **Dans `run_exocortex.py` :**
   - Ajouter `--init-models` (appelle `llm_client.ensure_local_gguf_models()`) et `--ingest-takeout` (appelle `TakeoutIngestor().run(max_distill_sessions=args.limit)` avec argument optionnel `--limit`).
   - Appeler `llm_client.ensure_local_gguf_models()` au démarrage de `run_consolidate()`.
2. **Dans `start_exocortex.bat` :**
   - Exporter `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_MAX_LOADED_MODELS=1` et `OLLAMA_NUM_PARALLEL=1`.
   - Exécuter `python run_exocortex.py --init-models` en étape `[0/3]` avant de lancer les démons et Streamlit.

---

## 3. CRITÈRES D'ACCEPTATION (DEFINITION OF DONE v0.1.1)

- [x] `FULL_DUAL_MODEL_VRAM_GB` vaut `12.8` dans `src/config.py` et `.env.example`.
- [x] `start_exocortex.bat` exporte `OLLAMA_FLASH_ATTENTION=1` et `OLLAMA_KV_CACHE_TYPE=q8_0`, et exécute `python run_exocortex.py --init-models`.
- [x] `run_exocortex.py` supporte `--init-models` et `--ingest-takeout [--limit N]`.
- [x] `HybridLLMClient.is_cloud_available()` existe et `generate_cloud_sota()` est appelé avec les bons arguments (`system=...`, `response_model=DistilledConceptSchema`).
- [x] Aucun appel `datetime.now()` ne subsiste comme fallback de parsing de date dans `parse_youtube_export()` et `parse_google_search_export()`.
- [x] Aucun appel LLM ou embedding situé dans une boucle `for` (`night_consolidator.py`, `takeout_ingestor.py`, `vector_store.py`) n'utilise `keep_alive=0` à chaque itération : ils utilisent `keep_alive="5m"` en boucle puis `unload_model()` en sortie de boucle.

---

## 4. JOURNAL D'EXÉCUTION DU PATCH v0.1.1

### A. Configuration & Budget VRAM Windows 11 (`src/config.py`, `.env.example`, `.env`)
- `FULL_DUAL_MODEL_VRAM_GB` abaissé de `14.5` à `12.8` Go pour correspondre à l'empreinte réelle de Windows 11 au repos (~2 Go VRAM réservés).
- Ajout de `TAKEOUT_MAX_DISTILL_SESSIONS: int` (par défaut `0` = toutes les sessions qualifiées).
- Documentation des variables système d'optimisation Ollama (`OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_NUM_PARALLEL=1`).

### B. Moteur d'Inférence & Modelfile (`src/llm/ollama_client.py`)
- Ajout de la méthode `is_cloud_available()` dans `HybridLLMClient`.
- Injection de `PARAMETER num_ctx 8192` dans la génération dynamique des `Modelfile` pour borner le cache KV de `gemma4:26b-a4b`.
- Typage et gestion assouplis de `keep_alive: Union[int, str] = 0` dans `generate_text()`, `generate_vision()`, `generate_structured()` et `generate_embeddings()` pour autoriser la persistance temporaire pendant les batches (`"5m"`).

### C. Éradication du Thrashing VRAM & Déchargement de Fin de Boucle (`vector_store.py`, `night_consolidator.py`)
- `src/database/vector_store.py` : `get_embedding()` et `index_concept_file()` acceptent `keep_alive: Union[int, str] = 0`. `sync_all_concepts()` vectorise en boucle avec `keep_alive="5m"`, puis décharge `bge-m3` une seule fois en sortie.
- `src/consolidators/night_consolidator.py` :
  - Appel de `ensure_local_gguf_models()` dès le début de `consolidate()`.
  - Passe 1 : `generate_vision()` et `generate_structured()` utilisent `keep_alive="5m"` en boucle, purge VRAM unique en fin de Passe 1.
  - Passe 2 : `generate_text()` utilise `keep_alive="5m"` pour le journal épisodique et les fiches concepts, purge VRAM unique en fin de Passe 2.

### D. Fiabilisation du Module 1 (`src/ingestors/takeout_ingestor.py`)
- Éradication totale de `datetime.now()` dans `parse_youtube_export()` et `parse_google_search_export()` au profit d'un mécanisme strict `last_valid_dt`.
- `initialize_meta_and_concepts()` et `TakeoutIngestor.run()` acceptent `max_distill_sessions: Optional[int] = None`.
- Débridage de la sélection par taille au profit de l'ensemble des sessions qualifiées (ou bornage paramétrable).
- Correction du mode Cloud SOTA : appel avec `system=PROMPT_SESSION_DISTILLATION_SYSTEM` et `response_model=DistilledConceptSchema`.
- Mode local : passage au modèle lourd `settings.MODEL_HEAVY_SYNTHESIS` avec `keep_alive="5m"` et déchargement global `llm_client.unload_all_models()` en sortie de boucle.
- Synchronisation LanceDB (`vector_store.sync_all_concepts()`) et Google Drive (`DriveCompiler.compile_all()`) déclenchées en fin d'ingestion.

### E. Orchestration CLI & Scripts Windows (`run_exocortex.py`, `start_exocortex.bat`)
- `run_exocortex.py` : ajout des commandes `--init-models` et `--ingest-takeout` avec argument optionnel `--limit`.
- `start_exocortex.bat` : export des variables VRAM Ollama et exécution de l'étape `[0/3] Provisioning des modeles GGUF locaux dans Ollama...`.