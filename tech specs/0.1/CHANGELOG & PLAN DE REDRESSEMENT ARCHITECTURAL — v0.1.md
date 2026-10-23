# CHANGELOG & PLAN DE REDRESSEMENT ARCHITECTURAL — v0.1

**Date :** 19 Octobre 2026
**Version cible :** `v0.1.0` (Éradication des simulations v0.0, Intégration GGUF locale, Taxonomie Émergente & Distillation LLM réelle)
**Référence de base :** `tech specs/SPECIFICATIONS_TECHNIQUES_V0.md`

---

## 1. AUDIT POST-MORTEM DE LA VERSION INITIALE (v0.0)

L'inspection du code source livré en `v0.0` a révélé 8 défaillances critiques où la logique métier a été simulée par du formatage statique :

1. **Crash fatal au lancement CLI (`run_exocortex.py`) :** La fonction `run_daemon()` appelle `daemon.run()` (ligne 40) alors que `TelemetryDaemon` implémente `run_loop()`.
2. **Absence totale d'inférence LLM dans `takeout_ingestor.py` :** Le prompt `PROMPT_ATOMIC_CONCEPT_DISTILLATION` est importé mais jamais appelé. Le script utilise une boucle `for` qui coupe les réponses de l'IA à 250 caractères (`ai_snippet[:250]`), utilise les 50 premiers caractères du 1er prompt comme titre de note, et force le topic `Data_Engineering` par défaut.
3. **Coquille vide en Passe 2 de `night_consolidator.py` :** La méthode `run_pass_2_synthesis()` sélectionne un modèle LLM mais ne l'appelle jamais. Elle écrit une chaîne f-string statique (*"Synthèse structurée des arbitrages techniques..."*) et force les liens `[[IA_Agentique_et_RAG]], [[Data_Engineering]]`.
4. **Vecteurs aléatoires silencieux dans `vector_store.py` :** En cas d'indisponibilité d'Ollama ou du modèle `bge-m3`, `get_embedding()` génère un vecteur factice à partir d'un hash cryptographique `hashlib.sha256` répété sur 1024 dimensions, détruisant la pertinence sémantique de LanceDB.
5. **Calcul temporel aberrant (`total_time_invested_min`) :** Calculé par différence brute `timestamp_end - timestamp_start` sur une session entière (produisant jusqu'à 371 670 minutes soit 258 jours sur un fil repris plusieurs mois plus tard) et corrompu par le fallback `datetime.now()` dans `parse_date_flexible()`.
6. **Filtre anti-bruit défaillant (`takeout_ingestor.py`) :** Ligne 408, utilisation de `and` (`if t_count < min_turns and total_chars < min_user_chars`) au lieu de `or`, laissant passer des sessions d'un seul tour contenant un copier-coller de logs.
7. **Pollution par dumps bruts :** Aucune purge pré-inférence des tracebacks SQL, logs de tenseurs ou copier-coller d'interfaces HTML/DOM (ex: 900 lignes de menus SillyTavern).
8. **Carcan taxonomique fermé :** Interdiction de créer de nouvelles catégories sémantiques et écrasement systématique vers `IA_Agentique_et_RAG` via `heuristic_fallback_classification()`.

---

## 2. INTÉGRATION DES MODÈLES GGUF LOCAUX (`./models/`)

Deux modèles quantisés au format `.gguf` sont désormais présents dans le répertoire `./models/` :
- **Modèle Rapide (Passe 1 & Classification) :** `gemma-4-12b-it-Q4_K_M.gguf`
- **Modèle Lourd MoE (Passe 2 & Distillation) :** `gemma-4-26b-a4b-it-UD-IQ4_NL.gguf`

### 2.1. Mises à jour de `src/config.py` et `.env.example`
Ajouter dans `Settings` (`src/config.py`) la gestion du dossier `MODELS_DIR` et du backend d'inférence (`ollama` ou `llama_server`) :

```python
    # --- Répertoire des Modèles GGUF Locaux ---
    MODELS_DIR: Path = Field(
        default_factory=lambda: Path(os.getenv("MODELS_DIR", "./models")).resolve()
    )
    LLM_BACKEND: str = Field(
        default_factory=lambda: os.getenv("LLM_BACKEND", "ollama").lower() # "ollama" ou "llama_server"
    )
    GGUF_FAST_FILENAME: str = Field(
        default_factory=lambda: os.getenv("GGUF_FAST_FILENAME", "gemma-4-12b-it-Q4_K_M.gguf")
    )
    GGUF_HEAVY_FILENAME: str = Field(
        default_factory=lambda: os.getenv("GGUF_HEAVY_FILENAME", "gemma-4-26b-a4b-it-UD-IQ4_NL.gguf")
    )

2.2. Provisioning Automatique Ollama (Modelfile) ou llama-server

Créer un script utilitaire ou une méthode d'initialisation dans src/llm/ollama_client.py (ensure_local_gguf_models()) permettant d'enregistrer automatiquement les fichiers .gguf du dossier ./models/ dans Ollama sous les alias gemma4:12b et gemma4:26b-a4b (ou d'interroger LLAMA_SERVER_BASE_URL en compatibilité OpenAI /v1/chat/completions avec --override-tensor "blk\.(2[0-9]|[3-9][0-9])\.ffn_.*_exps\.weight=CPU").
3. SPÉCIFICATIONS DES CORRECTIONS PAR FICHIER (PLAN D'EXÉCUTION)
Correctif A : run_exocortex.py (Fix Crash Daemon)

Remplacer la fonction run_daemon() (lignes 34-41) par :
Python

def run_daemon() -> None:
    """Lance le démon de télémétrie Windows en temps réel (0 Mo VRAM, < 2% CPU)."""
    logger.info("=== Lancement du Démon de Télémétrie Temps Réel ===")
    from src.daemons.telemetry_daemon import TelemetryDaemon

    daemon = TelemetryDaemon()
    daemon.run_loop()

Correctif B : src/database/vector_store.py (Suppression du Hash SHA-256 Factice)

Un index vectoriel ne doit jamais stocker de bruit cryptographique. Remplacer get_embedding() (lignes 88-117) pour qu'elle lève une exception explicite ou retourne None sans corrompre la table LanceDB :
Python

    def get_embedding(self, text: str) -> List[float]:
        """
        Génère un vecteur d'embedding 1024-dim réel via bge-m3.
        Lève une RuntimeError si le modèle d'embedding est injoignable (interdiction des vecteurs SHA-256 factices).
        """
        clean_text = re.sub(r"\s+", " ", text).strip()[:2048]
        vec = llm_client.generate_embeddings(
            text=clean_text,
            model=settings.MODEL_EMBEDDING,
            keep_alive=0,
        )
        if not vec or len(vec) != EMBEDDING_DIM:
            raise RuntimeError(
                f"Échec critique d'embedding : dimension reçue {len(vec) if vec else 0} != {EMBEDDING_DIM}. "
                f"Vérifiez qu'Ollama est actif et que '{settings.MODEL_EMBEDDING}' est installé."
            )
        return [float(x) for x in vec]

Correctif C : src/llm/prompts.py (Taxonomie Dynamique & Schémas de Distillation)

Remplacer les prompts de classification et de distillation pour autoriser l'émergence contrôlée de nouveaux semantic_topic et imposer une sortie structurée Pydantic :
Python

PROMPT_DYNAMIC_TAXONOMY_RULE = """RÈGLE DE TAXONOMIE DYNAMIQUE ÉMERGENTE :
1. Consulte en priorité la liste des `semantic_topic` existants fournie ci-dessous.
2. Si le sujet correspond clairement à une catégorie existante (pertinence >= 80%), utilise son nom exact.
3. Si et seulement si le sujet traite d'un domaine distinct non couvert par la liste actuelle, CRÉE un nouveau tag canonique au format strict `Domaine_SousDomaine` en PascalCase_Snake (ex: `HomeLab_MediaServer`, `Roleplay_LLM`, `Psychologie_PNL`, `Suisse_DroitFiscal`) et passe le booléen `is_new_topic` à `true` avec une courte description.
4. Il est STRICTEMENT INTERDIT d'utiliser un tag fourre-tout par défaut comme `Data_Engineering` ou `IA_Agentique_et_RAG` pour des sujets qui n'en relèvent pas.
"""

Correctif D : src/ingestors/takeout_ingestor.py (Nettoyage, Calcul Temporel, Distillation LLM)
1. Nettoyage pré-LLM des dumps et logs (clean_noisy_text)

Ajouter cette fonction avant la sessionisation et la distillation :
Python

def sanitize_turn_text(text: str, max_turn_chars: int = 3500) -> str:
    """
    Purge les dumps d'interfaces copiés-collés (menus HTML/DOM), les tracebacks répétitifs
    et les espaces insécables multiples avant envoi au LLM.
    """
    if not text:
        return ""
    # 1. Suppression des séquences d'espaces/tabulations de scraping UI (ex: SillyTavern sliders)
    cleaned = re.sub(r"(?:[\t \xa0]{4,}\n){3,}", "\n[Dump d'interface UI omis]\n", text)
    # 2. Compression des logs d'erreurs ou stacktraces de plus de 15 lignes consécutives
    lines = cleaned.splitlines()
    if len(lines) > 35:
        filtered_lines: List[str] = []
        log_streak = 0
        for line in lines:
            is_log_line = any(
                pat in line
                for pat in ["Traceback", "File \"", "at FluentMigrator", "sqlalchemy.exc", "ggml_", "llama_model_loader", "   at "]
            )
            if is_log_line:
                log_streak += 1
                if log_streak <= 6:
                    filtered_lines.append(line)
                elif log_streak == 7:
                    filtered_lines.append("... [Stacktrace / Log technique tronqué pour lisibilité] ...")
            else:
                log_streak = 0
                filtered_lines.append(line)
        cleaned = "\n".join(filtered_lines)

    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    if len(cleaned) > max_turn_chars:
        cleaned = cleaned[:max_turn_chars] + "\n...[Contenu long tronqué]..."
    return cleaned

2. Calcul mathématique réel du temps investi (compute_realistic_session_duration_min)

Ne jamais faire timestamp_end - timestamp_start sur toute la session. Additionner les écarts inter-tours plafonnés :
Python

def compute_realistic_session_duration_min(turns: List[ParsedTurn], max_gap_min: int = 15) -> int:
    """
    Calcule le temps réel investi dans une session en additionnant les intervalles
    entre deux échanges consécutifs, plafonnés à `max_gap_min` (15 min) par tour,
    plus 3 minutes de lecture/rédaction de base pour le premier tour.
    """
    if not turns:
        return 0
    total_sec = 180.0  # 3 min de base pour l'ouverture de session
    max_gap_sec = max_gap_min * 60.0
    for i in range(1, len(turns)):
        delta_sec = max(0.0, (turns[i].timestamp - turns[i - 1].timestamp).total_seconds())
        total_sec += min(delta_sec, max_gap_sec)
    return max(5, int(round(total_sec / 60.0)))

3. Correction du filtre de bruit et des dates (Lignes 155 & 408)

    Dans parse_gemini_html et parse_gemini_json : si parse_date_flexible(date_str) retourne None, ignorer le tour ou utiliser le timestamp du tour précédent, jamais datetime.now() (qui contamine la date du jour avec de vieilles archives).

    Ligne 408 de sessionize_gemini_turns :

Python

# Règle anti-bruit stricte : rejeter si moins de 3 tours OU moins de 250 caractères utilisateur
if t_count < min_turns or total_chars < min_user_chars:
    filtered_out_noise += 1
    continue

4. Remplacement de initialize_meta_and_concepts par une vraie distillation LLM structurée

Définir le modèle Pydantic de sortie et appeler llm_client.generate_structured (ou generate_cloud_sota selon settings.TAKEOUT_MODE) :
Python

class DistilledConceptSchema(BaseModel):
    is_worth_indexing: bool = Field(description="False si la session n'est que du bruit ou un test trivial sans conclusion.")
    concept_title: str = Field(description="Titre conceptuel précis et canonique (ex: 'Configuration Serveur Plex & Riven sous Docker'). Jamais une phrase de prompt.")
    slug: str = Field(description="Slug kebab-case propre (ex: 'configuration-plex-riven-docker')")
    semantic_topic: str = Field(description="Tag de la taxonomie existante ou nouveau tag Domaine_SousDomaine")
    is_new_topic: bool = Field(default=False, description="True si semantic_topic est une nouvelle catégorie absente de la liste")
    new_topic_description: Optional[str] = Field(default=None, description="Description en 1 phrase si nouveau topic")
    tags: List[str] = Field(description="3 à 5 sous-tags techniques en minuscule")
    summary_1_line: str = Field(description="Résumé dense en une seule phrase de la conclusion ou de l'architecture.")
    synthesized_markdown_body: str = Field(
        description="Synthèse structurée en Markdown (sections ### Contexte, ### Arbitrages & Architecture, ### Conclusions & Commandes Clés). Zéro intro Wikipédia."
    )
    related_concepts: List[str] = Field(description="2 à 3 titres de concepts connexes pour le maillage Obsidian")

Lorsqu'une session est distillée :

    Si res.is_new_topic est True, ajouter automatiquement - **{res.semantic_topic}** : {res.new_topic_description} dans Vault_Data/00_Meta/Taxonomie_Tags.md.

    Mettre à jour extracted_topics_json et generated_notes_json dans la table SQLite chat_sessions pour que le Dashboard Streamlit et hippocampus_hotkey.py affichent les vraies statistiques.

Correctif E : src/consolidators/night_consolidator.py (Taxonomie Émergente & Vraie Passe 2)

    Évolution de WindowClassification (Ligne 48) :

Python

class WindowClassification(BaseModel):
    semantic_topic: str = Field(description="Topic existant dans Taxonomie_Tags.md OU nouveau tag Domaine_SousDomaine si aucun ne correspond.")
    is_new_topic: bool = Field(default=False, description="True si un nouveau topic a dû être créé.")
    new_topic_description: Optional[str] = Field(default=None, description="Description courte si nouveau topic.")
    cognitive_mode: str = Field(description="production, exploration, chat_ia, gaming, media")
    confidence: float = Field(default=0.9)

    Enregistrement dynamique des nouveaux topics : Si res.is_new_topic est True et res.confidence >= 0.75 avec un format valide ^[A-Za-z0-9]+_[A-Za-z0-9_]+$, ajouter le topic à self.allowed_tags et l'écrire dans Taxonomie_Tags.md au lieu de l'écraser avec heuristic_fallback_classification().

    Correction de consolidate() sur les dates vides (Ligne 559) :
    Supprimer if not dates_to_process: dates_to_process = [datetime.now().date()] ou interdire à run_pass_2_synthesis() de générer un fichier 01_Episodique/YYYY-MM-DD.md lorsque metric.total_screen_sec == 0.

    Vraie synthèse LLM dans run_pass_2_synthesis() (Lignes 436-520) :

        Récupérer les activités réelles du jour (self.db.get_activities_for_date(target_date)), extraire les window_title et ocr_snippet (qui contiennent les résumés visuels de la Passe 1).

        Appeler llm_client.generate_text() avec effective_model (gemma4:26b-a4b ou fallback 12b) et SYSTEM_PROMPT_ANTI_WIKIPEDIA pour rédiger :

            La section ## 3. Synthèse des Tunnels de Concentration du journal épisodique YYYY-MM-DD.md basée sur les fenêtres réellement consultées ce jour-là.

            Le corps analytique réel des fiches 02_Concepts/{slug}.md ayant dépassé 45 minutes de focus, à partir des titres de fenêtres, résumés visuels .webp et sessions chat du jour.

4. CRITÈRES D'ACCEPTATION & VALIDATION (DEFINITION OF DONE v0.1)

    [x] Aucun fichier dans Vault_Data/ ne contient de données fictives de test (suppression de toute donnée seedée du 2026-10-19).

    [x] python run_exocortex.py --daemon démarre run_loop() sans lever d'AttributeError.

    [x] vector_store.py ne contient plus aucune référence à hashlib.sha256.

    [x] takeout_ingestor.py nettoie les dumps HTML/logs, calcule total_time_invested_min par somme d'intervalles plafonnés à 15 min, appelle réellement le LLM avec DistilledConceptSchema, et met à jour chat_sessions.extracted_topics_json.

    [x] night_consolidator.py appelle réellement le LLM en Passe 2 pour synthétiser les notes épisodiques et conceptuelles, et enrichit dynamiquement Taxonomie_Tags.md lorsqu'un nouveau sujet émerge.

---

## 5. JOURNAL D'EXÉCUTION & LIVRABLES TECHNIQUES v0.1

### A. Intégration des Modèles GGUF Locaux & Détection Hardware
- **`src/config.py`** : Définition de `MODELS_DIR`, `LLM_BACKEND` (`"ollama"` / `"llama_server"`), `GGUF_FAST_FILENAME`, `GGUF_HEAVY_FILENAME` et propriétés de résolution insensible à la casse `GGUF_FAST_PATH` (`gemma-4-12b-it-Q4_K_M.gguf`) et `GGUF_HEAVY_PATH` (`gemma-4-26B-A4B-it-UD-IQ4_NL.gguf`).
- **`.env.example`** : Documentation des clés de configuration pour les backends d'inférence locale (`OLLAMA_BASE_URL`, `LLM_BACKEND`, `LLAMA_SERVER_BASE_URL`).
- **`src/llm/ollama_client.py`** :
  - Implémentation de `ensure_local_gguf_models()` : vérifie la présence des modèles dans Ollama, génère les `Modelfile` dynamiques pointant vers les chemins GGUF réels, et exécute la création automatique via l'API REST Ollama (ou fallback CLI `ollama create`).
  - Implémentation du support OpenAI-compatible `/chat/completions` avec fallback si `LLM_BACKEND == "llama_server"`.
  - Sonde matérielle VRAM (`HardwareProbe`) et déchargement systématique de la mémoire via `keep_alive=0`.

### B. Correctifs d'Exécution & Sécurité Vectorielle
- **`run_exocortex.py`** : Correction du crash CLI `run_daemon()` en appelant la méthode réelle `daemon.run_loop()`.
- **`src/database/vector_store.py`** : Éradication définitive de toute simulation par `hashlib.sha256`. Levée d'une exception stricte `RuntimeError` si Ollama ou `bge-m3` est inaccessible ou si la dimension vectorielle est différente de 1024.

### C. Refonte Sémantique du Module 1 (Takeout Ingestor)
- **`src/llm/prompts.py`** : Ajout des prompts stricts `PROMPT_DYNAMIC_TAXONOMY_RULE`, `PROMPT_SESSION_DISTILLATION_SYSTEM`, `PROMPT_SESSION_DISTILLATION_USER`, `PROMPT_NIGHT_DAY_SYNTHESIS_SYSTEM` et `PROMPT_NIGHT_CONCEPT_SYNTHESIS_SYSTEM`.
- **`src/database/db_manager.py`** : Implémentation de `update_session_distillation_metadata()` pour synchroniser `extracted_topics_json`, `generated_notes_json` et le résumé analytique.
- **`src/ingestors/takeout_ingestor.py`** :
  - `sanitize_turn_text()` : Compression et assainissement des dumps DOM/UI et des stacktraces > 6 lignes.
  - Parsing de dates corrigé : élimination stricte du fallback erroné `datetime.now()`.
  - Calcul réaliste du temps de focus : `compute_realistic_session_duration_min()` avec plafond des intervalles inactifs à 15 minutes.
  - Distillation structurée via `DistilledConceptSchema` Pydantic v2 avec extraction des topics émergents.
  - Fonction `register_new_taxonomy_tag()` enregistrant automatiquement les nouveaux tags qualifiés dans `Taxonomie_Tags.md`.

### D. Consolidation Nocturne & Taxonomie Émergente (Module 3)
- **`src/consolidators/night_consolidator.py`** :
  - `WindowClassification` enrichi avec `is_new_topic` et `new_topic_description`.
  - Enregistrement dynamique des nouveaux tags dans `Taxonomie_Tags.md` en Passe 1 (seuil de confiance >= 0.75).
  - Repli heuristique par défaut basculé sur `A_Trier` au lieu de `IA_Agentique_et_RAG`.
  - `run_pass_2_synthesis()` : Vraie synthèse LLM basée sur les activités réelles, fenêtres et résumés visuels .webp de la journée. Remplacement des liens hardcodés par des connexions sémantiques dynamiques.
  - Arrêt gracieux et sécurisé de `consolidate()` si aucune activité n'est présente, sans création de notes factices.

### E. Assainissement du Coffre & Scaffold Git
- Éradication de toutes les fausses données de test seedées du 2026-10-19 (`01_Episodique/2026-10-19.md`, fiches concepts factices et entrées de test SQLite).
- `.gitignore` configuré pour exclure le contenu des buffers, caches, modèles et archives tout en conservant l'arborescence complète du coffre via `.gitkeep`.
- Synchronisation réussie des méga-documents Google Drive (`00_CORE`, `01_TELEMETRIE_7J`, `02_CONCEPTS_ACTIFS`, `03_INDEX_GRAPHE`).