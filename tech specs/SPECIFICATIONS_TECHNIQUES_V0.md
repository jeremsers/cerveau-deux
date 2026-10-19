# SPÉCIFICATIONS TECHNIQUES : Système "Exocortex & Télémétrie Cognitive" (v1.0)

## 1. Vision & Objectifs du Système

Construire un système local automatisé sous Windows agissant à la fois comme :

1. **Un Hippocampe Artificiel (Exocortex) :** Une base de connaissances en fichiers Markdown (`.md`) et vecteurs locaux (LanceDB) qui ne nécessite aucune maintenance manuelle ni consultation visuelle dans Obsidian, mais qui alimente automatiquement une application web de LLM (Gemini Web App) via Google Drive et le presse-papier système.
2. **Une Plateforme de Télémétrie Cognitive (Quantified Self) :** Un système de suivi temporel et sémantique haute précision stocké dans SQLite, mesurant le temps réel passé par sujet/intention (trans-applications), les tunnels d'hyperfocus, le taux de fragmentation de l'attention (*context-switching*) et le ratio exploration/production.

---

## 2. Contraintes Matérielles & Architecture Bi-Modèle (Dual-Gemma 4)

- **OS :** Windows 11 (64-bit) | **GPU :** NVIDIA RTX 4070 Ti Super (16 Go VRAM).
- **Règle d'exclusion mutuelle en VRAM :** Il est strictement interdit de charger deux modèles simultanément en VRAM. Le client `src/llm/ollama_client.py` doit orchestrer un passage de témoin séquentiel en utilisant systématiquement le paramètre `keep_alive=0` lors du dernier appel d'un batch pour purger la mémoire vidéo avant de charger le modèle suivant.
- **Sonde matérielle pré-inférence (`pynvml`) :** Avant tout appel LLM, `ollama_client.py` vérifie la VRAM libre réelle :
  - Si `VRAM_libre < 8 Go` (session Gaming/3D active) : différer le batch (`sleep` / report).
  - Si `8 Go <= VRAM_libre < 14.5 Go` : forcer l'utilisation exclusive de `gemma4:12b`.
  - Si `VRAM_libre >= 14.5 Go` : autoriser l'architecture bi-modèle complète.

- **Répartition des Modèles (via Ollama `http://localhost:11434`) :**
  1. **Modèle Rapide & Multimodal (`MODEL_FAST_VISION = "gemma4:12b"`) :**
     - Empreinte : ~7,2 Go VRAM.
     - Rôle : Analyse directe des captures d'écran (`.webp`) prises lors des sessions prolongées (>3 min), extraction visuelle de schémas/code, et classification JSON rapide des lignes de `raw_activity` dans SQLite.
  2. **Modèle Architecte Haute Précision (`MODEL_HEAVY_SYNTHESIS = "gemma4:26b-a4b"`) :**
     - Architecture : Mixture-of-Experts (26B paramètres totaux, 4B actifs par token, ~14,2 Go VRAM, >110 tok/s).
     - Rôle : Exécuté uniquement en mode texte pur (après déchargement du 12B) pour le minage approfondi de l'archive Google Takeout (`takeout_ingestor.py`), la rédaction du `Profil_Cognitif.md`, la synthèse des fiches conceptuelles (`02_Concepts/`) et le bilan épisodique quotidien.
  3. **Modèle d'Embeddings (`MODEL_EMBEDDING = "bge-m3"`) :**
     - Empreinte : ~1,2 Go VRAM.
     - Rôle : Vectorisation multilingue (1024 dim) dans **LanceDB**, exécutée en fin de pipeline et lors du raccourci `Alt+Space` (`hippocampus_hotkey.py`).

### Optimisation VRAM Chirurgicale par Override-Tensor (`llama-server` / GGUF)

Pour éviter que le modèle `gemma4:26b-a4b` ne sature les 16 Go de VRAM lors des grands contextes de consolidation, le client LLM peut s'interfacer avec une instance `llama-server` (compatible API OpenAI sur port local) lancée avec un déchargement sélectif des tenseurs FFN sur CPU tout en maintenant 100 % des couches d'attention et du cache KV sur le GPU (`-ngl 99`) :

- **Regex Modèle Dense (couches 20+) :** `--override-tensor "blk\.(2[0-9]|[3-9][0-9])\.ffn_.*=CPU"`

- **Regex Modèle MoE (Experts FFN couches 20+) :** `--override-tensor "blk\.(2[0-9]|[3-9][0-9])\.ffn_.*_exps\.weight=CPU"`
Cette configuration abaisse l'empreinte VRAM du modèle 26B de ~14,2 Go à ~8,5 Go sans dégrader la vitesse d'évaluation du contexte sur la RTX 4070 Ti Super.

---

## 3. Arborescence Cible du Projet & des Données

### 3.1. Dépôt du Code Source (`exocortex-engine/`)

```text
exocortex-engine/
├── .env.example
├── requirements.txt
├── SPECIFICATIONS_TECHNIQUES.md
├── src/
│   ├── config.py                  # Chemins, seuils temporels, blacklist d'exécutables
│   ├── database/
│   │   ├── db_manager.py          # Connexion SQLite WAL, création tables, requêtes analytiques
│   │   └── vector_store.py        # Wrapper LanceDB (indexation bge-m3 + recherche k-NN)
│   ├── llm/
│   │   ├── ollama_client.py       # Client HTTP avec sorties structurées JSON (Pydantic)
│   │   └── prompts.py             # Prompts système stricts (anti-Wikipédia, profilage, tagging)
│   ├── ingestors/
│   │   └── takeout_ingestor.py    # Module 1 : Parsing Google Takeout Gemini + Cold Start
│   ├── daemons/
│   │   ├── telemetry_daemon.py    # Module 2 : Surveillance Win32 + OCR CPU + DHash
│   │   └── hippocampus_hotkey.py  # Module 5 : Raccourci Alt+Space -> Injection Presse-papier
│   ├── consolidators/
│   │   ├── night_consolidator.py  # Module 3 : Classification LLM, Notes Épisodiques, Concepts
│   │   └── drive_compiler.py      # Module 4 : Compilation des 4 Méga-Fichiers vers Google Drive
│   └── dashboard/
│       └── app.py                 # Module 6 : Interface Streamlit de statistiques & Dataviz
```

### 3.2. Arborescence du Stockage Local (`Vault_Data/`)

```text
Vault_Data/
├── 00_Meta/
│   ├── Profil_Cognitif.md         # Empreinte cognitive, style, préférences d'interaction
│   └── Taxonomie_Tags.md          # Liste fermée des semantic_topics autorisés (JSON/YAML)
├── 01_Episodique/
│   └── YYYY-MM-DD.md              # Journaux quotidiens générés automatiquement
├── 02_Concepts/
│   └── [slug-du-concept].md       # Fiches atomiques distillées avec Frontmatter YAML
├── _System_Buffer/                # Dossier technique hors indexation Markdown
│   ├── telemetry.db               # Base SQLite maîtresse (conservée indéfiniment)
│   └── lancedb_store/             # Index vectoriel LanceDB
└── Google_Drive_Sync/             # Dossier synchronisé par Google Drive for Desktop
    ├── 00_CORE_IDENTITE_ET_STYLE.md
    ├── 01_TELEMETRIE_ET_EPISODIQUE_7J.md
    ├── 02_PROJETS_ET_CONCEPTS_ACTIFS.md
    └── 03_INDEX_GRAPHE_CONCEPTS.md
```

---

## 4. Schéma de la Base de Données SQLite (`telemetry.db`)

Le gestionnaire `db_manager.py` doit initialiser exactement ce schéma avec `PRAGMA journal_mode=WAL;` et `PRAGMA synchronous=NORMAL;` :

```sql
-- 1. Activité brute capturée en temps réel par le démon CPU
CREATE TABLE IF NOT EXISTS raw_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_start DATETIME NOT NULL,
    timestamp_end DATETIME NOT NULL,
    duration_sec INTEGER NOT NULL,
    executable TEXT NOT NULL,              -- ex: 'firefox.exe', 'Code.exe'
    window_title TEXT NOT NULL,            -- Titre complet de la fenêtre Win32
    url_or_path TEXT,                      -- Extrait du titre ou de la barre d'adresse si dispo
    ocr_snippet TEXT,                      -- Mots-clés extraits par OCR CPU (max 500 chars)
    active_input BOOLEAN DEFAULT 1,        -- 1 = Activité clavier/souris détectée, 0 = Passif (vidéo/lecture)
    input_intensity REAL DEFAULT 0.0,      -- Score normalisé d'actions/minute (sans keylogging du contenu)
    semantic_topic TEXT,                   -- Assigné par night_consolidator (ex: 'Architecture_RAG')
    cognitive_mode TEXT,                   -- Assigné par night_consolidator ('exploration', 'production', 'chat_ia', 'gaming', 'media')
    processed BOOLEAN DEFAULT 0            -- 0 = Brut, 1 = Classifié par le LLM local
);

CREATE INDEX IF NOT EXISTS idx_raw_ts ON raw_activity(timestamp_start);
CREATE INDEX IF NOT EXISTS idx_raw_topic ON raw_activity(semantic_topic);
CREATE INDEX IF NOT EXISTS idx_raw_processed ON raw_activity(processed);

-- 2. Métriques quotidiennes agrégées (Calculées chaque soir)
CREATE TABLE IF NOT EXISTS daily_metrics (
    date DATE PRIMARY KEY,
    total_screen_sec INTEGER NOT NULL,
    active_production_sec INTEGER NOT NULL,
    passive_exploration_sec INTEGER NOT NULL,
    max_hyperfocus_sec INTEGER NOT NULL,       -- Plus longue séquence continue sur le même semantic_topic
    max_hyperfocus_topic TEXT,
    context_switches_per_hour REAL NOT NULL,   -- Nombre de changements de semantic_topic / heure active
    read_vs_write_ratio REAL NOT NULL,         -- Ratio (exploration + media) / production
    top_topics_json TEXT NOT NULL              -- JSON: {"topic_A": 7200, "topic_B": 3400} (en secondes)
);

-- 3. Historique des conversations IA (Alimenté par Google Takeout + sessions futures)
CREATE TABLE IF NOT EXISTS chat_sessions (
    session_id TEXT PRIMARY KEY,
    timestamp_start DATETIME NOT NULL,
    timestamp_end DATETIME NOT NULL,
    turn_count INTEGER NOT NULL,
    user_char_count INTEGER NOT NULL,          -- Volume écrit par l'utilisateur (mesure d'engagement)
    extracted_topics_json TEXT NOT NULL,       -- JSON array des sujets détectés
    generated_notes_json TEXT NOT NULL,        -- JSON array des chemins de fichiers .md créés
    summary TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_chat_date ON chat_sessions(timestamp_start);
```

---

## 5. Spécifications Détaillées des 6 Modules

### MODULE 1 : `takeout_ingestor.py` (Cold Start Hybride : Python Local + Cloud SOTA)

- **Objectif :** Exploiter la fenêtre de contexte massive (1M+ tokens) d'un modèle Cloud SOTA pour l'analyse globale de l'archive Google Takeout Gemini, tout en générant les statistiques exactes en local.
- **Architecture en 3 passes :**
  1. **Passe 1 — Parsing Déterministe & Injection SQLite (CPU Local) :**
     - Parser le fichier Takeout (`.json` ou `.html`), reconstruire les sessions (seuil d'inactivité : 120 min) et filtrer le bruit (`< 3 tours` et `< 250 caractères` utilisateur).
     - Insérer immédiatement toutes les métriques temporelles et volumétriques dans la table `chat_sessions` de `telemetry.db`.
     - Générer dans `_System_Buffer/takeout_staging/` :
       - `00_USER_PROMPTS_ONLY.md` : Concaténation chronologique de 100 % des messages écrits par l'utilisateur (sans les longs pavés de réponse de l'IA), permettant de faire tenir 1 à 2 ans de pensée pure dans une seule fenêtre de contexte Cloud (< 200k tokens).
       - `01_FULL_SESSIONS_BATCH_[N].md` : Les sessions complètes découpées en lots de ~400k tokens.
  2. **Passe 2 — Profilage Global & Taxonomie Maîtresse (Cloud SOTA) :**
     - Le script doit proposer deux modes via `.env` (`TAKEOUT_MODE="web_manual"` ou `"cloud_api"`) :
       - **Mode `web_manual` (0 €) :** Génère les fichiers de staging accompagnés d'un fichier `PROMPT_A_COPIER_DANS_GEMINI_WEB.txt` que l'utilisateur glisse avec `00_USER_PROMPTS_ONLY.md` dans son interface Gemini Pro pour obtenir d'un bloc son `Profil_Cognitif.md` et sa `Taxonomie_Tags.md`.
       - **Mode `cloud_api` (Automatisé via SDK `google-genai`) :** Envoie automatiquement `00_USER_PROMPTS_ONLY.md` au modèle Cloud SOTA pour générer `00_Meta/Profil_Cognitif.md` et `00_Meta/Taxonomie_Tags.md`.
  3. **Passe 3 — Distillation Atomique des Concepts (`02_Concepts/`) :**
     - Utilise la `Taxonomie_Tags.md` générée en Passe 2 comme contrainte stricte.
     - Extrait les fiches de concepts atomiques (`02_Concepts/[slug].md`) soit par appels API Cloud SOTA (modèle Flash/Pro en batch JSON structuré), soit en fallback local nocturne sur `gemma4:26b-a4b`, puis les indexe dans **LanceDB** avec `bge-m3`.

#### Extension Multi-Takeout (Google Search & YouTube History)

Le Module 1 (`takeout_ingestor.py`) accepte en entrée optionnelle les fichiers `Mon activité` issus de **Google Search** et **YouTube**.

1. **Table SQLite dédiée (`historical_footprints`) :**

   ```sql
   CREATE TABLE IF NOT EXISTS historical_footprints (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       source TEXT NOT NULL,              -- 'youtube' | 'google_search'
       timestamp DATETIME NOT NULL,
       title_or_query TEXT NOT NULL,      -- Titre de la vidéo ou texte de la requête
       url TEXT,
       channel_or_domain TEXT,            -- Nom de la chaîne YT ou domaine cliqué
       cluster_id TEXT,                   -- ID de regroupement si rafale temporelle
       semantic_topic TEXT,               -- Assigné par batch uniquement sur les clusters denses
       linked_gemini_session_id TEXT      -- Clé étrangère si corrélation temporelle (< 120 min)
   );
   CREATE INDEX IF NOT EXISTS idx_hist_ts ON historical_footprints(timestamp);

2.Règle Stricte de Non-Pollution du Coffre :

Il est strictement interdit de générer une note dans 02_Concepts/ à partir d'une entrée YouTube ou Google Search isolée.

Jointure Temporelle Automatique : Toute requête Search ou vidéo YouTube survenue dans une fenêtre de [-60 min ; +30 min] autour d'une session Gemini active est automatiquement rattachée aux métadonnées de cette session (linked_gemini_session_id) et listée dans le bloc > [!abstract]- Sources & Contexte Épisodique de la note générée.

Détection de Tunnels d'Exploration (Burst Clustering) : Les événements Search/YouTube hors session Gemini sont regroupés par fenêtre glissante de 45 minutes. Seuls les clusters contenant >= 5 événements sont envoyés par lots à gemma4:12b pour recevoir un semantic_topic et alimenter les statistiques de daily_metrics (courbes de demi-vie des centres d'intérêt).

### MODULE 2 : `telemetry_daemon.py` (Capteur Temps Réel 0-VRAM)

- **Objectif :** Tourner en tâche de fond sous Windows et alimenter `raw_activity` sans impact sur les performances.
- **Mécanisme de boucle (Polling à 2 secondes) :**
  1. Récupérer le handle de la fenêtre au premier plan via `win32gui.GetForegroundWindow()`, son PID via `win32process.GetWindowThreadProcessId()`, le nom de l'exécutable via `psutil.Process(pid).name()` et le titre via `win32gui.GetWindowText()`.
  2. **Filtre de confidentialité (Blacklist) :** Si l'exécutable ou le titre matche la liste noire définie dans `config.py` (ex: `Bitwarden`, `1Password`, `KeePass`, `InPrivate`, `Navigation privée`, mots-clés bancaires), ignorer totalement le cycle.
  3. **Mesure d'activité physique (Non-Keylogger) :** Utiliser `ctypes.windll.user32.GetLastInputInfo` ou un compteur d'événements global (sans jamais enregistrer quelles touches sont pressées) pour déterminer si l'utilisateur est actif (`active_input = 1`) ou passif devant un flux vidéo/lecture (`active_input = 0`).
  4. **Seuil d'engagement (*Dwell Time*) :** Maintenir l'état en RAM. Si l'utilisateur quitte une fenêtre après `< 20 secondes`, considérer cela comme du bruit de zapping (incrémenter uniquement un compteur de switch en mémoire, ne pas déclencher d'OCR).
  5. **Capture & OCR CPU sélectif :** Si la durée sur une même fenêtre atteint `20 secondes` ET que l'exécutable est un navigateur, un lecteur PDF ou une application bureautique :
     - Capturer uniquement le rectangle de la fenêtre active via `mss`.
     - Calculer un hachage perceptuel rapide (`imagehash.dhash`). Si la distance de Hamming avec la capture précédente est `< 5`, ne pas relancer l'OCR.
     - Exécuter `rapidocr_onnxruntime` (exécuté strictement sur CPU via ONNX Runtime) ou l'API native `winocr` pour extraire les 500 premiers caractères significatifs visibles à l'écran, puis supprimer immédiatement l'image de la RAM (aucune image stockée sur disque).
  6. Au changement de fenêtre (si durée totale `>= 20s`), insérer la ligne consolidée dans `raw_activity`.

### MODULE 3 : `night_consolidator.py` (Le "Sommeil Paradoxal" Nocturne)

- **Déclenchement :** Planificateur de tâches Windows (ex: 03h00 du matin, ou au verrouillage prolongé de la session, ou manuellement).
- **Étape A — Classification Sémantique SQLite :**
  1. Sélectionner toutes les entrées de `raw_activity` où `processed = 0`.
  2. Regrouper par paires uniques `(executable, window_title, ocr_snippet)` pour éviter d'envoyer 50 fois le même titre de fenêtre au LLM.
  3. Fournir au LLM local la liste existante dans `00_Meta/Taxonomie_Tags.md` (pour éviter la prolifération de synonymes) et demander une sortie JSON associant chaque entrée à un `semantic_topic` et un `cognitive_mode`.
  4. Mettre à jour `raw_activity` (`processed = 1`).
- **Étape B — Calcul des Métriques d'Hyperfocus (`daily_metrics`) :**
  1. Parcourir chronologiquement les entrées du jour.
  2. **Algorithme de Tunnel d'Hyperfocus :** Fusionner les blocs consécutifs partageant le même `semantic_topic` (en tolérant des micro-interruptions `< 120 secondes` sur un autre exécutable, comme répondre à un message rapide ou chercher une commande). Identifier la durée maximale (`max_hyperfocus_sec`).
  3. Calculer `context_switches_per_hour` et `read_vs_write_ratio`, puis insérer le bilan dans `daily_metrics`.
- **Étape C — Génération Markdown & Indexation Vectorielle :**
  1. Générer la note `01_Episodique/YYYY-MM-DD.md` contenant le résumé statistique de la journée, la chronologie des tunnels de concentration et la synthèse des sujets explorés.
  2. Si un sujet a accumulé `> 45 minutes` d'exploration active dans la journée, créer ou enrichir la fiche correspondante dans `02_Concepts/` et mettre à jour l'index **LanceDB** via `vector_store.py`.

### MODULE 4 : `drive_compiler.py` (Pont Natif vers Gemini Web App)

- **Objectif :** Contourner l'incapacité des applications web de LLM à parcourir des milliers de petits fichiers locaux en compilant 4 méga-documents synchronisés sur Google Drive.
- **Exécution :** Appelé automatiquement à la fin de `night_consolidator.py`.
- **Fichiers générés dans `Google_Drive_Sync/` :**
  1. `00_CORE_IDENTITE_ET_STYLE.md` : Copie du profil cognitif + instructions système d'interaction (pas de flatterie, rigueur technique, prise en compte de l'historique).
  2. `01_TELEMETRIE_ET_EPISODIQUE_7J.md` : Tableaux Markdown générés depuis SQLite résumant les statistiques des 7 derniers jours (temps par sujet, hyperfocus, dérives) + concaténation des 7 dernières notes épisodiques.
  3. `02_PROJETS_ET_CONCEPTS_ACTIFS.md` : Concaténation complète des 15 notes de `02_Concepts/` ayant été créées ou modifiées le plus récemment.
  4. `03_INDEX_GRAPHE_CONCEPTS.md` : Annuaire ultra-condensé de **toutes** les notes du coffre sous la forme `- **[Titre]** (Tags) : Résumé en 1 ligne`, permettant au LLM web de connaître l'existence de n'importe quelle note ancienne et de la demander si besoin.

### MODULE 5 : `hippocampus_hotkey.py` (Injecteur Pré-Prompt Temps Réel)

- **Objectif :** Permettre d'injecter en moins de 100 ms dans le chat web des souvenirs précis vieux de plusieurs mois via un raccourci clavier.
- **Mécanisme :**
  1. Écoute globale du raccourci `Alt + Espace` (via `keyboard` ou `pynput`).
  2. À l'activation, simule `Ctrl+A` puis `Ctrl+C` dans la zone de saisie active du navigateur pour lire le brouillon de prompt de l'utilisateur via `pyperclip`.
  3. Encode la requête avec `BAAI/bge-m3` et interroge **LanceDB** (`top_k = 5`).
  4. Formate un bloc Markdown structuré contenant le prompt initial suivi d'une section `<contexte_hippocampe_local>` regroupant le contenu intégral des 5 notes les plus pertinentes et les métriques SQLite associées au sujet.
  5. Remplace le contenu du presse-papier et simule `Ctrl+V` (ou copie l'objet fichier `.md` dans le presse-papier Windows `CF_HDROP` pour collage en pièce jointe directe).

### MODULE 6 : `dashboard/app.py` (Interface "Bandeur de Stats")

- **Objectif :** Visualisation locale interactive sur `http://localhost:8501` via **Streamlit** et **Plotly Express**.
- **Vues obligatoires :**
  1. **KPIs en tête :** Temps actif total, Record d'hyperfocus de la semaine, Indice de fragmentation moyen, Ratio Exploration / Production.
  2. **Heatmap Circadienne & Calendaire :** Carte thermique façon GitHub Contributions + distribution horaire des pics de concentration.
  3. **Sankey / Treemap des Obsessions :** Répartition du temps par `semantic_topic` croisé avec les exécutables réels (voir quels outils servent à quels sujets).
  4. **Courbe de Demi-Vie des Intérêts (Historique Gemini + OS) :** Graphique temporel sur 12 mois montrant l'émergence, les pics d'intensité et la mise en veille de chaque centre d'intérêt.
  5. **Inspecteur de "Rabbit Holes" :** Frise chronologique interactive d'une journée permettant de visualiser l'enchaînement exact des sujets minute par minute.

---

## 6. Contrat de Formatage des Notes Markdown (`02_Concepts/`)

Toute note générée ou mise à jour par le système doit impérativement respecter ce gabarit afin de séparer les faits/concepts des métadonnées de traçabilité :

```markdown
---
id: "YYYYMMDDHHMM"
title: "Titre du Concept"
type: "concept"
origin: ["gemini_takeout", "screen_telemetry"]
semantic_topic: "Nom_Du_Topic_Normalise"
tags: ["tag1", "tag2"]
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
total_time_invested_min: 145
summary_1_line: "Résumé dense en une seule phrase pour l'index global."
---

# Titre du Concept

[Corps de la note : uniquement la synthèse structurée des réflexions, architectures, arbitrages techniques et conclusions validées par l'utilisateur. Aucune introduction générique.]

> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)
> - **Temps cumulé sur ce sujet :** 2h25
> - **Sources épisodiques :**
>   - Session Gemini du `YYYY-MM-DD` (14 échanges)
>   - Activité écran du `YYYY-MM-DD` (45 min sur `firefox.exe` / Documentation)
> - **Connexions sémantiques :** [[Concept Connexe A]], [[Concept Connexe B]]
```