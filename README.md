# 🧠 Exocortex & Télémétrie Cognitive

Architecture d'hippocampe artificiel local et de quantification cognitive pour Windows 11, optimisée pour GPU **NVIDIA RTX 4070 Ti Super (16 Go VRAM)**. Version courante : **0.5.7**.

Le système observe l'activité de l'utilisateur sans keylogging, consolide la mémoire par cycles de sommeil paradoxal bi-modèle (Gemma 4 12B/26B et BGE-M3 via Ollama), indexe les concepts dans une base vectorielle embarquée (**LanceDB**), et relie ce coffre aux outils du quotidien : injection pré-prompt par raccourci global, synchronisation Google Drive pour Gemini Web, serveur MCP pour les agents, Kanban de spécifications, Command Center web.

---

## 📐 Architecture

```
  Activité OS ──► Démon de télémétrie (Win32, 0 Mo VRAM) ──┐
  Navigateur  ──► Extension MV3 ──► Récepteur 127.0.0.1:8502 ┤
  Mémos audio ──► voice_inbox/                               ├──► SQLite WAL (7 tables)
  Google Takeout ──► Ingesteur (Gemini, Search, YouTube) ────┘          │
                                                                       ▼
                     Consolidation nocturne (verrou VRAM unique, un modèle à la fois)
                     Passe 0 vocal · Passe 1 vision + classification (12B)
                     Métriques & tunnels · Passe 2 journaux + fiches (26B/12B)
                     Passe 3 index LanceDB (bge-m3) · Défragmenteur (Sommeil Profond)
                                                                       │
            ┌────────────────────────────┬─────────────────────────────┼────────────────────────┐
            ▼                            ▼                             ▼                        ▼
   Coffre Obsidian (Vault_Data)   Google_Drive_Sync (4 docs)   Command Center Web :8500   Serveur MCP (stdio)
   01_Episodique · 02_Concepts    → Gemini Web App             (+ Streamlit secondaire)   → agents codeurs
   03_Kanban_Specs                                              Kanban · GraphRAG
            ▲
   Injecteur Hippocampe (Ctrl+Alt+Espace) : k-NN LanceDB + wikilinks + télémétrie SQLite
```

### Invariants
- **0 Mo VRAM au repos, un seul modèle à la fois** : déchargement `keep_alive=0` et verrou VRAM **inter-processus** (`_System_Buffer/vram.lock`) partagé par la nuit, l'ingestion, l'API, l'injecteur et le MCP. Sous 8 Go libres (jeu lancé), la nuit tourne en mode CPU et les synthèses LLM sont reportées.
- **Démon sans inférence** : `GetLastInputInfo` pour l'intensité de saisie, dwell time de 20 s, fenêtre close après 5 min sans saisie (60 min en lecture média), écran verrouillé ignoré, capture `.webp` différée après 180 s (dHash anti-doublon).
- **Coffre sans pollution** : historiques YouTube/Search en base uniquement ; corps de fiches sans paraphrase encyclopédique ; télémétrie isolée dans le callout `> [!abstract]-` ; écritures atomiques.
- **Aucune perte silencieuse** : migrations SQLite versionnées (`PRAGMA user_version`), fiches douteuses déplacées dans `02_Concepts/_Quarantine/`, fusions archivées dans `_Archive_Merged/`.

---

## 📁 Arborescence

```text
cerveau-deux/
├── run_exocortex.py                 # Point d'entrée CLI unifié
├── start_exocortex.bat              # Démons silencieux + Command Center Web
├── start_web_center.bat             # Command Center Web seul
├── stop_exocortex.bat               # Arrêt propre (démons, serveur web, Streamlit)
├── requirements.txt · .env.example
├── browser_extension/               # Extension Chrome/Edge MV3 (onglets actifs, chats IA)
├── src/
│   ├── config.py                    # Réglages Pydantic, taxonomie fermée, vocabulaires partagés
│   ├── api/server.py                # API FastAPI + service du Command Center
│   ├── web_gui/                     # Interface web (index.html, app.js, vendor/)
│   ├── dashboard/app.py             # Dashboard Streamlit (interface secondaire)
│   ├── consolidators/               # night_consolidator, drive_compiler, vault_doctor,
│   │                                #   graph_defragmenter, kanban_engine
│   ├── daemons/                     # telemetry_daemon, browser_telemetry_receiver,
│   │                                #   git_ide_probe, hippocampus_hotkey
│   ├── database/                    # db_manager (SQLite), vector_store (LanceDB), graph_rag
│   ├── ingestors/                   # takeout_ingestor, takeout_parsers, voice_ingestor
│   ├── llm/                         # ollama_client (sonde VRAM, verrou, Gemini), prompts
│   ├── mcp/exocortex_mcp_server.py  # 5 outils MCP (FastMCP ou JSON-RPC autonome)
│   └── utils/                       # markdown_io, episodic_journal, cognitive_metrics, privacy,
│                                    #   local_auth, path_safety, atomic_io, lifecycle
├── tests/                           # Suites de vérification hermétiques (v0.1.2 → v0.5.7)
├── tech specs/                      # Spécifications et changelogs par version
└── Vault_Data/                      # Coffre Obsidian et données persistantes (hors Git)
    ├── 00_Meta/                     # Profil_Cognitif.md, Taxonomie_Tags.md, bootloader, registre du bruit
    ├── 01_Episodique/               # Journaux quotidiens (sections télémétrie et sessions IA)
    ├── 02_Concepts/                 # Fiches atomiques, _Archive_Merged/, _Quarantine/
    ├── 03_Kanban_Specs/             # Specs par projet et AGENT_QUEUE.md
    ├── Google_Drive_Sync/           # 4 méga-documents pour Gemini Web
    └── _System_Buffer/              # telemetry.db, lancedb_store, screen_staging, voice_inbox, jetons
```

Base SQLite (`_System_Buffer/telemetry.db`) : `raw_activity`, `daily_metrics`, `chat_sessions`, `chat_messages`, `historical_footprints`, `projects`, `kanban_tasks`.

---

## 🚀 Installation & Configuration

### 1. Prérequis
- Windows 10/11 64 bits, Python 3.11+, pilote NVIDIA récent.
- [Ollama](https://ollama.com) avec les modèles `gemma4:12b`, `gemma4:26b-a4b` et `bge-m3` (les deux Gemma peuvent être provisionnés depuis des GGUF locaux de `models/` par `--init-models`).

### 2. Dépendances
```bash
pip install -r requirements.txt
```
`faster-whisper` (transcription des mémos vocaux) est optionnel, voir la fin de `requirements.txt`.

### 3. Serveur Ollama (une fois)
Le budget VRAM du 26B suppose un cache KV quantifié. Ces variables doivent être vues par le **serveur** Ollama : définissez-les au niveau utilisateur puis redémarrez Ollama.
```bat
setx OLLAMA_FLASH_ATTENTION 1
setx OLLAMA_KV_CACHE_TYPE q8_0
setx OLLAMA_MAX_LOADED_MODELS 1
setx OLLAMA_NUM_PARALLEL 1
```
`python run_exocortex.py --init-models` vérifie l'environnement réel du processus serveur et prévient s'il manque une variable.

### 4. Fichier `.env`
Copiez `.env.example` en `.env`. Toutes les variables y sont documentées ; les principales :
```ini
VAULT_ROOT=./Vault_Data
OLLAMA_BASE_URL=http://localhost:11434
MODEL_FAST_VISION=gemma4:12b
MODEL_HEAVY_SYNTHESIS=gemma4:26b-a4b
MODEL_EMBEDDING=bge-m3
VRAM_STRICT_ABORT_FREE_GB=8.0      # sous ce seuil, aucune inférence (mode CPU la nuit)
VRAM_REASONING_MIN_FREE_GB=12.8    # sous ce seuil, le 26B est remplacé par le 12B
OLLAMA_NUM_CTX=16384
TAKEOUT_MODE=web_manual            # ou cloud_api avec GEMINI_API_KEY
HIPPOCAMPUS_HOTKEY=<ctrl>+<alt>+<space>
```

### 5. Extension navigateur
Chargez `browser_extension/` comme extension non empaquetée (`chrome://extensions`, mode développeur). Elle n'est injectée que sur Gemini, Claude et ChatGPT ; elle s'authentifie auprès du récepteur local avec un jeton obtenu automatiquement.

---

## 🕹️ Utilisation

### Démarrage en 1 clic
`start_exocortex.bat` vérifie Ollama, démarre le démon de télémétrie et l'injecteur en arrière-plan (`pythonw`), puis ouvre le **Command Center** sur `http://127.0.0.1:8500`. `stop_exocortex.bat` arrête tout proprement : les démons sauvegardent la fenêtre en cours avant de sortir.

### Commandes (`run_exocortex.py`)

| Commande | Action |
|---|---|
| `--init-models` | Vérifie la configuration du serveur Ollama et provisionne les modèles GGUF locaux. |
| `--ingest-takeout [--limit N]` | Ingestion complète Google Takeout (sessions, empreintes, rafales, distillation Delta, journaux). |
| `--import-profile FICHIER` | Importe le profil cognitif renvoyé par Gemini Web (mode `web_manual`). |
| `--daemon` | Démon de télémétrie Win32 (et récepteur de l'extension sur 8502). |
| `--consolidate [--date AAAA-MM-JJ]` | Consolidation nocturne (Passes 0 à 3, Drive). |
| `--ingest-voice` | Transcrit et distille les mémos de `_System_Buffer/voice_inbox/`. |
| `--defrag-graph` | Sommeil Profond : fusions et évolutions d'arbitrage entre fiches proches. |
| `--compile-drive` | Régénère les 4 méga-documents de `Google_Drive_Sync/`. |
| `--hotkey` | Injecteur Hippocampe (raccourci `HIPPOCAMPUS_HOTKEY`). |
| `--web [--port --host]` | Command Center Web (interface principale). |
| `--dashboard` | Dashboard Streamlit (interface secondaire, mêmes requêtes et contrats). |
| `--all` | Démons d'arrière-plan + Command Center au premier plan. |
| `--stop` | Arrêt propre de tous les processus Exocortex. |
| `--mcp-server` | Serveur MCP stdio (5 outils : recherche, fiche, télémétrie, session, file Kanban). |
| `--kanban-status` · `--next-task` · `--complete-task ID` | Pilotage du Kanban et de `AGENT_QUEUE.md`. |

### Injecteur Hippocampe
Dans n'importe quelle zone de saisie, tapez votre prompt puis **Ctrl+Alt+Espace** : le texte est capturé, enrichi d'un bloc `<contexte_hippocampe_local>` (fiches proches par k-NN, voisins par wikilinks, heures investies) et réinjecté. Si une consolidation détient le GPU, l'injection est annulée au bout de 3 s plutôt que de bloquer. Test sans clavier :
```bash
python -m src.daemons.hippocampus_hotkey --test "Comment optimiser mon pipeline RAG avec LanceDB ?"
```

### Google Takeout
Placez les exports dans `takeout_raw/` (HTML ou JSON ; les dates JSON en UTC sont converties en heure locale). En mode `web_manual`, suivez `_System_Buffer/takeout_staging/PROMPT_A_COPIER_DANS_GEMINI_WEB.txt` puis importez la réponse avec `--import-profile`. En mode `cloud_api`, distillation et profil passent par Gemini, même Ollama éteint.

### Command Center Web
Six vues : chronologie et tunnels d'hyperfocus, cartographie et GraphRAG, archéologie longitudinale, rythmes circadiens, explorateur épistémique (chats, empreintes, rafales), studio Kanban. Les modes cognitifs, statuts et topics affichés sont servis par l'API (`/api/meta/vocabulary`) ; les valeurs estimées (journées issues du cold start Takeout) sont signalées.

### Google Drive (Pont B)
`00_CORE_IDENTITE_ET_STYLE.md`, `01_TELEMETRIE_ET_EPISODIQUE_7J.md`, `02_PROJETS_ET_CONCEPTS_ACTIFS.md`, `03_INDEX_GRAPHE_CONCEPTS.md` sont compilés chaque nuit. Les catégories de `DRIVE_EXCLUDED_TOPICS` n'y figurent jamais.

---

## 🧪 Tests
```bash
python -m pytest tests
```
La suite est **hermétique** : `tests/conftest.py` redirige coffre, base, Takeout, Ollama et clé Gemini vers des valeurs de test avant tout import, et refuse de démarrer si la configuration pointe vers `Vault_Data`. Aucun test ne lit ni ne modifie vos données.

---

## 🔒 Confidentialité & Sécurité
- **Liste noire ciblée :** fenêtres et onglets de navigation privée, gestionnaires de mots de passe, banques et administrations sont exclus de la télémétrie. La correspondance se fait en mots entiers sur des marques et marqueurs précis, et par domaine sur les URL (`TITLE_BLACKLIST`, `SENSITIVE_DOMAINS`, extensibles via `TITLE_BLACKLIST_EXTRA` et `SENSITIVE_DOMAINS_EXTRA`). Un tour de chat qui divulgue un mot de passe ou une clé d'API est rejeté.
- **Stockage local :** la base SQLite, les vecteurs LanceDB et les notes Markdown restent sur votre machine.
- **Ce qui peut sortir de la machine :**
  - les 4 méga-documents de `Vault_Data/Google_Drive_Sync/`, si ce dossier est synchronisé avec Google Drive puis lu par Gemini Web. Les catégories de `DRIVE_EXCLUDED_TOPICS` (par défaut `Sante_et_Pharmacologie`, `Introspection_et_Neuroatypie`, `Admin_Finance_et_Droit`) n'y figurent jamais ;
  - les sessions envoyées à l'API Gemini si vous activez le mode `TAKEOUT_MODE=cloud_api` avec votre clé ;
  - les fichiers de staging Takeout que vous copiez vous-même dans Gemini Web (mode `web_manual`).
- **Services locaux protégés :** l'API du Command Center (8500) et le récepteur de l'extension (8502) n'écoutent que sur `127.0.0.1`, refusent les origines web tierces (CORS restreint, contrôle de l'en-tête `Host`) et exigent un jeton local (`_System_Buffer/*_token`) pour toute écriture. L'interface web applique une Content-Security-Policy et échappe tout contenu affiché.
