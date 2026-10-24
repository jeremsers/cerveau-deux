# 🧠 Exocortex & Télémétrie Cognitive

Architecture d'hippocampe artificiel local et de quantification cognitive temps réel pour Windows 11, optimisée pour GPU **NVIDIA RTX 4070 Ti Super (16 Go VRAM)**.

Le système observe l'activité de l'utilisateur sans keylogging, consolide la mémoire par cycles de sommeil paradoxal bi-modèle (Gemma 4 & BGE-M3), indexe les concepts dans une base vectorielle embarquée (**LanceDB**), et établit un pont bidirectionnel avec l'interface Gemini Web App (via synchronisation Google Drive et injection pré-prompt globale `Alt + Espace`).

---

## 📐 Invariants d'Ingénierie & Architecture Système

```
                                  +--------------------------------------------------+
                                  |                 UTILISATEUR                      |
                                  +--------------------------------------------------+
                                       |                                         |
                       [Activité OS]   |                                         | [Alt + Espace]
                                       v                                         v
               +----------------------------------+             +----------------------------------+
               |  Module 2 : Telemetry Daemon     |             | Module 5 : Hippocampus Injector  |
               |  (Win32, 0 Mo VRAM, < 2% CPU)    |             | (pynput, LanceDB k-NN top_k=5)   |
               +----------------------------------+             +----------------------------------+
                                       |                                         |
                                       v                                         v
               +----------------------------------+             +----------------------------------+
               |     SQLite WAL (telemetry.db)    | <---------- | Gemini Web App (Input Prompt)    |
               | (raw_activity, daily_metrics...) |             +----------------------------------+
               +----------------------------------+
                                       |
                     [Traitement Nocturne Différé]
                                       v
               +-----------------------------------------------------------------+
               |              Module 3 : Night Consolidator                      |
               |  - Passe 1 (gemma4:12b) : Vision .webp + Classification         |
               |  - Analytique : Détection Tunnels d'Hyperfocus & Métriques      |
               |  - Passe 2 (gemma4:26b-a4b) : Synthèse Épisodique & Concepts     |
               |  - Passe 3 (bge-m3) : Vectorisation & Indexation LanceDB        |
               +-----------------------------------------------------------------+
                                       |
                       +---------------+---------------+
                       |                               |
                       v                               v
       +-------------------------------+   +-------------------------------------+
       |   Coffre Markdown (Vault)     |   | Module 4 : Drive Compiler           |
       | 01_Episodique/ / 02_Concepts/ |   | 4 Méga-fichiers (Google Drive Sync) |
       +-------------------------------+   +-------------------------------------+
                       |
                       v
       +-----------------------------------------------+
       | Module 6 : Dashboard Streamlit "Bandeur de Stats" |
       | (Timeline Gantt, Treemap, Archéologie, Circadien)|
       +-----------------------------------------------+
```

### 1. Zéro Empreinte Temps Réel (0 Mo VRAM, CPU < 2%)
- Le démon de télémétrie (`telemetry_daemon.py`) n'exécute **aucune inférence locale** pendant la session de travail.
- Utilise l'API Windows native (`GetLastInputInfo`) pour quantifier l'intensité motrice sans enregistrer les frappes.
- Seuil d'engagement (*Dwell Time*) : les fenêtres quittées en moins de 20 secondes sont ignorées.
- Capture d'écran différée en `.webp` (qualité 75) uniquement après 180s de concentration continue sur un même écran avec filtre de redondance perceptuel (`dHash` 64-bit).

### 2. Sommeil Paradoxal en 3 Passes VRAM Mutuellement Exclusives
- Les modèles ne cohabitent jamais en VRAM (`HardwareProbe` via NVML / `nvidia-smi` avec déchargement forcé `keep_alive=0`) :
  - **Passe 1 (`gemma4:12b`)** : Analyse visuelle des captures `.webp`, extraction du résumé visuel, suppression immédiate des `.webp` et classification sémantique fermée.
  - **Calcul Analytique** : Détection des tunnels d'hyperfocus (tolérance micro-interruptions < 120s) et calcul de la fragmentation (`context_switches_per_hour`).
  - **Passe 2 (`gemma4:26b-a4b` ou fallback `12b`)** : Rédaction du journal `01_Episodique/YYYY-MM-DD.md` et mise à jour chirurgicale des fiches `02_Concepts/` pour les sujets cumulant $\ge 45$ min de focus.
  - **Passe 3 (`bge-m3`)** : Vectorisation et indexation k-NN dans LanceDB (`_System_Buffer/lancedb_store/`).

### 3. Non-Pollution du Coffre & Séparation Épistémique
- Les historiques YouTube et Google Search alimentent `historical_footprints` mais ne créent jamais de fiches autonomes dans `02_Concepts/`.
- Les notes Markdown ne contiennent aucune paraphrase encyclopédique Wikipédia : uniquement la substance intellectuelle et les arbitrages de l'utilisateur. La télémétrie et le graphe sont isolés dans des callouts Obsidian repliables (`> [!abstract]-`).

---

## 📁 Arborescence du Projet

```text
cerveau-deux/
├── .env                              # Clés API, chemins et modèles configurés
├── requirements.txt                  # Dépendances Python typées et figées
├── run_exocortex.py                  # Point d'entrée CLI unifié
├── start_exocortex.bat               # Lanceur silencieux Windows (pythonw + Streamlit)
├── stop_exocortex.bat                # Arrêt propre des démons d'arrière-plan
├── SPECIFICATIONS_TECHNIQUES.md     # Spécifications d'architecture
├── src/
│   ├── config.py                     # Configuration Pydantic v2 & validation d'environnement
│   ├── consolidators/
│   │   ├── drive_compiler.py         # Module 4 : Générateur des 4 méga-fichiers Google Drive
│   │   └── night_consolidator.py     # Module 3 : Sommeil paradoxal en 3 passes VRAM
│   ├── daemons/
│   │   ├── hippocampus_hotkey.py     # Module 5 : Injecteur pré-prompt Alt+Espace (LanceDB + SQLite)
│   │   └── telemetry_daemon.py       # Module 2 : Capteur Win32 bas niveau (0 Mo VRAM)
│   ├── dashboard/
│   │   └── app.py                    # Module 6 : Tableau de bord Streamlit "Bandeur de Stats"
│   ├── database/
│   │   ├── db_manager.py             # SQLite WAL haute performance (4 tables relationnelles)
│   │   └── vector_store.py           # Base vectorielle LanceDB + wrapper BGE-M3
│   ├── ingestors/
│   │   └── takeout_ingestor.py       # Module 1 : Parseur Takeout Gemini, Search & YouTube
│   └── llm/
│       ├── ollama_client.py          # Client hybride Ollama/Google GenAI + sonde VRAM
│       └── prompts.py                # Prompts système anti-Wikipédia et gabarits Markdown
└── Vault_Data/                       # Coffre Obsidian & Données persistantes
    ├── 00_Meta/                      # Profil_Cognitif.md & Taxonomie_Tags.md
    ├── 01_Episodique/                # Journaux quotidiens YYYY-MM-DD.md
    ├── 02_Concepts/                  # Fiches conceptuelles atomiques
    ├── Google_Drive_Sync/            # 4 méga-fichiers synchronisés vers Gemini Web App
    └── _System_Buffer/               # telemetry.db (SQLite WAL), lancedb_store, screen_staging
```

---

## 🚀 Installation & Configuration

### 1. Prérequis Système
- **OS :** Windows 10 ou 11 (64-bit).
- **Python :** 3.11+.
- **GPU Recommandé :** NVIDIA RTX 4070 Ti Super (16 Go VRAM) ou équivalent avec pilote NVIDIA récent.
- **Ollama :** Installé localement avec les modèles :
  ```bash
  ollama pull gemma4:12b
  ollama pull gemma4:26b-a4b
  ollama pull bge-m3
  ```

### 2. Installation des Dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration (`.env`)
Copiez `.env.example` en `.env` et adaptez les variables si nécessaire :
```ini
VAULT_ROOT=./Vault_Data
OLLAMA_BASE_URL=http://localhost:11434
MODEL_FAST_VISION=gemma4:12b
MODEL_HEAVY_SYNTHESIS=gemma4:26b-a4b
MODEL_EMBEDDING=bge-m3
MIN_FREE_VRAM_GB=8.0
FULL_DUAL_MODEL_VRAM_GB=14.5
GEMINI_API_KEY=votre_cle_optionnelle
GEMINI_MODEL=gemini-2.5-flash
```

---

## 🕹️ Utilisation Quotidienne

### 1. Démarrage en 1 Clic (Recommandé)
Double-cliquez sur `start_exocortex.bat` :
- Lance le démon de télémétrie silencieusement en arrière-plan (`pythonw.exe`).
- Lance le listener global `Alt + Espace` silencieusement (`pythonw.exe`).
- Ouvre automatiquement le tableau de bord Streamlit dans votre navigateur.

Pour arrêter tous les démons d'arrière-plan à tout moment :
Double-cliquez sur `stop_exocortex.bat`.

---

### 2. Pilote CLI (`run_exocortex.py`)

| Commande | Action |
|---|---|
| `python run_exocortex.py --daemon` | Démarre la capture de télémétrie Windows en direct. |
| `python run_exocortex.py --consolidate` | Déclenche manuellement la consolidation nocturne en 3 passes VRAM. |
| `python run_exocortex.py --consolidate --date YYYY-MM-DD` | Consolide rétroactivement une date précise. |
| `python run_exocortex.py --compile-drive` | Génère les 4 méga-documents dans `Vault_Data/Google_Drive_Sync/`. |
| `python run_exocortex.py --hotkey` | Démarre l'injecteur pré-prompt `Alt + Espace`. |
| `python run_exocortex.py --dashboard` | Ouvre le dashboard Streamlit "Bandeur de Stats". |
| `python run_exocortex.py --all` | Démarre l'écosystème complet (démons de fond + dashboard). |

---

### 3. L'Injecteur Hippocampe (`Alt + Espace`)
Dans n'importe quelle application (navigateur web sur Gemini, VS Code, invite de commande) :
1. Tapez votre question ou prompt.
2. Appuyez sur `Alt + Espace`.
3. Le système capture votre texte, interroge **LanceDB** (`top_k = 5`), interroge **SQLite** pour récupérer le cumul d'heures investies et l'antériorité du sujet, et réinjecte instantanément votre prompt enrichi d'un bloc `<contexte_hippocampe_local>`.
4. Un signal sonore discret confirme l'injection sans quitter votre fenêtre.

Pour tester l'injecteur en ligne de commande de manière headless :
```bash
python -m src.daemons.hippocampus_hotkey --test "Comment optimiser mon pipeline RAG avec LanceDB ?"
```

---

### 4. Les 4 Méga-Documents Google Drive (`Pont B`)
Situés dans `Vault_Data/Google_Drive_Sync/`, ces 4 fichiers sont compilés automatiquement chaque nuit pour être partagés dans Google Drive et lus par Gemini Web App :
- **`00_CORE_IDENTITE_ET_STYLE.md`** : Profil cognitif, taxonomie maîtresse et contrat d'interaction.
- **`01_TELEMETRIE_ET_EPISODIQUE_7J.md`** : Bilan statistique des 7 derniers jours (temps par topic, record d'hyperfocus, ratio prod/conso) + notes épisodiques.
- **`02_PROJETS_ET_CONCEPTS_ACTIFS.md`** : Concaténation intégrale des 15 concepts les plus récemment travaillés.
- **`03_INDEX_GRAPHE_CONCEPTS.md`** : Table des matières exhaustive de 100% des fiches conceptuelles du coffre classées par topic.

---

### 5. Tableau de Bord "Bandeur de Stats" (Streamlit)
Lit les métriques via des connexions SQLite en lecture seule (`mode=ro`) ; l'onglet Kanban, lui, **écrit** dans la base (création de projets et de tâches) :
- **Bandeau KPIs Macro :** Heures totales traquées, record d'hyperfocus, fréquence de zapping (`switches/h`), ratio prod/conso, volume épistémique.
- **Onglet 1 (Chronologie & Focus Quotidien) :** Diagramme de Gantt interactif Plotly minute par minute et mise en exergue des tunnels d'hyperfocus.
- **Onglet 2 (Cartographie des Obsessions) :** Treemap hiérarchique (`Mode Cognitif` → `Topic Sémantique` → `Application`) et camembert des modes cognitifs.
- **Onglet 3 (Archéologie Longitudinale) :** Aire empilée mensuelle des réflexions depuis 2024 et matrice de catégorisation (*Piliers Fondamentaux* vs *Passions Éphémères*).
- **Onglet 4 (Rythmes Circadiens) :** Heatmap 24h x 7j et diagnostic chronobiologique personnalisé (détection du chronotype nocturne).

---

## 🔒 Confidentialité & Sécurité
- **Liste noire ciblée :** fenêtres et onglets de navigation privée, gestionnaires de mots de passe, banques et administrations sont exclus de la télémétrie. La correspondance se fait en mots entiers sur des marques et marqueurs précis, et par domaine sur les URL (`TITLE_BLACKLIST`, `SENSITIVE_DOMAINS`, extensibles via `TITLE_BLACKLIST_EXTRA` et `SENSITIVE_DOMAINS_EXTRA`). Un tour de chat qui divulgue un mot de passe ou une clé d'API est rejeté.
- **Stockage local :** la base SQLite, les vecteurs LanceDB et les notes Markdown restent sur votre machine.
- **Ce qui peut sortir de la machine :**
  - les 4 méga-documents de `Vault_Data/Google_Drive_Sync/`, si ce dossier est synchronisé avec Google Drive puis lu par Gemini Web. Les catégories de `DRIVE_EXCLUDED_TOPICS` (par défaut `Sante_et_Pharmacologie`, `Introspection_et_Neuroatypie`, `Admin_Finance_et_Droit`) n'y figurent jamais ;
  - les sessions envoyées à l'API Gemini si vous activez le mode `TAKEOUT_MODE=cloud_api` avec votre clé ;
  - les fichiers de staging Takeout que vous copiez vous-même dans Gemini Web (mode `web_manual`).
- **Services locaux protégés :** l'API du Command Center (8500) et le récepteur de l'extension (8502) n'écoutent que sur `127.0.0.1`, refusent les origines web tierces (CORS restreint, contrôle de l'en-tête `Host`) et exigent un jeton local (`_System_Buffer/*_token`) pour toute écriture. L'interface web applique une Content-Security-Policy et échappe tout contenu affiché.
