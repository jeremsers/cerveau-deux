---
task_id: "EXO-021"
project_id: "exocortex"
component_tag: "inference-vram"
title: "v0.5.7 — Audit Lot 7 : Inférence, VRAM & Performance, Dépendances et Documentation"
status: "done"
---
# EXO-021 — v0.5.7 — Audit Lot 7 : Inférence, VRAM & Performance, Dépendances et Documentation

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif du Patch
Dernier lot de remédiation de l'audit du 24/10/2026. Les six lots proposés par l'audit ne couvraient pas les constats d'inférence C1 à C12 ni l'essentiel de la dette documentaire ; ce lot les traite, avec le verrou VRAM inter-processus (C8) et la documentation (G1, G2), les dépendances (G4) et la configuration (G5). Après ce lot, **tous les constats identifiés de l'audit ont un correctif**.

### 1.2 Vérifications faites sur la machine (constats « à vérifier »)
Lecture seule, sans charger de modèle :
- **Serveur Ollama 0.40.6 (PID 13648)** : les quatre variables `OLLAMA_FLASH_ATTENTION`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_NUM_PARALLEL=1` sont bien vues par le serveur. C1 n'avait donc pas d'effet ici, mais les `set` du `.bat` restaient trompeurs.
- **C5 confirmé** : `gemma4:12b` déclare `completion, tools, thinking`, **sans `vision`**. La Passe 1 vision n'a jamais pu lire les captures.
- **C4** : `gemma4:12b` et `gemma4:26b-a4b` déclarent `thinking`.
- **C2 confirmé** : les modèles installés ont été créés avec `num_ctx 8192`, alors que la distillation envoyait 16384 et les autres appels rien : chaque alternance forçait un rechargement.

### 1.3 Corrections

1. **C1 — Configuration du serveur Ollama** : `HybridLLMClient.check_ollama_server_config()` lit l'environnement du **processus serveur** Ollama (psutil) et indique la marche à suivre (`setx` puis redémarrage) s'il manque une variable. Appelée par `--init-models` (donc à chaque `start_exocortex.bat`). Les `set OLLAMA_*` sans effet sont retirés du `.bat` et remplacés par les instructions.
2. **C2 — `num_ctx` unique** : `OLLAMA_NUM_CTX` (16384) envoyé par `generate_text`, `generate_vision` et `generate_structured`, et écrit dans les Modelfiles générés.
3. **C3 — Défragmenteur** : `keep_alive="5m"` pendant la boucle d'évaluation des paires (le 26B n'est plus déchargé puis rechargé à chaque paire) ; déchargement unique en sortie, comme le prévoyait v0.4.1.
4. **C4 — Mode thinking** : `think: true` envoyé explicitement en Vague 1 quand Ollama déclare la capacité `thinking` du modèle (`/api/show`, mis en cache).
5. **C5 — Vision** : si le modèle ne déclare pas la capacité `vision`, la Passe 1 libère les captures sans les envoyer au modèle et l'indique dans le journal (au lieu d'appels inutiles et de captures accumulées). La classification par signatures continue normalement.
6. **C6 — Sonde GPU** : sans pynvml ni nvidia-smi, la VRAM est supposée nulle (`VRAM_ASSUME_FREE_GB = 0`, abstention) au lieu de 16 Go ; réglable pour une machine sans outils NVIDIA.
7. **C7 — Purge ciblée** : `force_clear_vram` ne décharge que les modèles de l'Exocortex (12B, 26B, bge-m3) ; un modèle chargé par un autre outil sur le même serveur Ollama n'est plus éjecté.
8. **C8 — Verrou VRAM inter-processus** : `InterProcessVRAMLock` (`_System_Buffer/vram.lock`, `msvcrt.locking` sous Windows, `flock` ailleurs), réentrant dans un processus. Chaque appel GPU (`generate_*`, embeddings, purge) le prend ; la consolidation nocturne, l'ingestion Takeout et le défragmenteur le détiennent pour toute leur durée. Les appels interactifs attendent peu : injecteur 3 s (injection annulée avec un son d'erreur), API GraphRAG 5 s (HTTP 503), context-pack 5 s, MCP 10 s. Si le GPU reste pris, la nuit bascule en mode CPU et l'ingestion reporte la distillation locale.
9. **C9 — Provisioning** : `ollama create -f Modelfile` (CLI) est la voie principale ; `/api/create` au format historique n'est qu'un repli si la CLI est absente du PATH.
10. **C10 — Seuils à source unique** : `VRAM_STRICT_ABORT_FREE_GB` et `VRAM_REASONING_MIN_FREE_GB` sont les seuls réglages ; `MIN_FREE_VRAM_GB` et `FULL_DUAL_MODEL_VRAM_GB` deviennent des alias en lecture (les anciennes variables d'environnement restent honorées en repli).
11. **C11 — Indexation LanceDB incrémentale** : seules les fiches nouvelles ou modifiées (empreinte sha1) sont ré-embarquées ; les fiches disparues sont retirées ; les fichiers `all-*` sont exclus ; la table est compactée (`optimize`) après modification. État dans `_System_Buffer/lancedb_store_sync_state.json` ; la première nuit après la mise à jour réindexe tout une fois.
12. **C12 — GraphRAG partagé** : l'API et le serveur MCP réutilisent une instance `HybridGraphRAG` entre requêtes ; l'index est invalidé sur changement de date de modification **ou** du nombre de fiches (une suppression est détectée), et indexe les `aliases`.
13. **G4 — `requirements.txt`** : retrait de rapidocr-onnxruntime, imagehash, beautifulsoup4, lxml, python-dotenv, pydantic-settings, rich et du doublon pynvml (nvidia-ml-py fournit le module) ; ajout de pandas, tzdata (zoneinfo sous Windows), pytest et httpx ; faster-whisper documenté comme optionnel.
14. **G5 — `.env.example`** : toutes les variables lues par le code sont documentées avec leur valeur par défaut (VRAM, verrou, fuseau, inactivité, confidentialité, DriftGuard, raccourci, ports, CORS, jetons, Kanban).
15. **G1 — README** réécrit : architecture actuelle, arborescence réelle, toutes les commandes CLI, configuration du serveur Ollama, extension, Command Center, tests hermétiques, confidentialité.
16. **G2 — Documentation fonctionnelle** : passages inexacts corrigés (`gc.collect` et cache CUDA, arrêt sur `<|thought|>`, bip 1200 Hz, arrêt de Streamlit par `stop.bat`, « 5 tables », lecture seule du dashboard, chronotype figé, Alt+Espace, volumes personnels) et nouvelle section 13 sur les modules v0.2 → v0.5.7.

### 1.4 Fichiers modifiés
`src/__init__.py`, `src/config.py`, `src/llm/ollama_client.py`, `src/consolidators/night_consolidator.py`, `src/consolidators/graph_defragmenter.py`, `src/consolidators/kanban_engine.py`, `src/ingestors/takeout_ingestor.py`, `src/database/vector_store.py`, `src/database/graph_rag.py`, `src/api/server.py`, `src/mcp/exocortex_mcp_server.py`, `src/daemons/hippocampus_hotkey.py`, `run_exocortex.py`, `start_exocortex.bat`, `start_web_center.bat`, `src/web_gui/index.html`, `requirements.txt`, `.env.example`, `README.md`, `tech specs/DOCUMENTATION_FONCTIONNELLE_ET_TECHNIQUE.md`, `tests/test_v013_verification.py`, `tests/test_v057_inference_vram_verification.py` (nouveau).

## 2. VÉRIFICATION

Suite `tests/test_v057_inference_vram_verification.py` (13 tests) :
- **C1** : environnement du serveur lu depuis le bon processus, variables manquantes signalées ; plus de `set OLLAMA_*` dans le `.bat`.
- **C2/C4** : même `num_ctx` sur les trois types de requêtes ; `think: true` seulement si le modèle déclare `thinking`.
- **C3** : `keep_alive="5m"` à chaque paire évaluée.
- **C5** : modèle sans vision → aucun appel vision, capture supprimée, activité classée.
- **C6** : repli à 0 Go, ou à la valeur configurée.
- **C7** : un modèle externe (`llama3:8b`) n'est pas déchargé.
- **C8** : un **second processus réel** détient le verrou ; le premier échoue proprement après le délai, puis l'obtient une fois libéré ; réentrance vérifiée ; toutes les méthodes GPU sont protégées.
- **C9** : CLI utilisée en priorité, REST seulement sans CLI.
- **C10** : alias cohérents, ancien nom d'environnement honoré.
- **C11** : 3 fiches indexées, 0 au second passage, 1 après modification, fiche supprimée retirée, `all-*` ignoré.
- **C12** : une seule instance GraphRAG pour 3 requêtes ; suppression d'une fiche détectée par l'index.

Résultats : **161 passed, 1 skipped** avec `python -m pytest tests` (le test sauté vérifie FastMCP et passe quand le SDK `mcp` 1.x est installé). Aucun fichier de `Vault_Data/` modifié par la suite.

Vérification navigateur (Chrome headless, coffre temporaire) : KPIs du jour non nuls après consolidation (1 h 30, 2 tunnels, 56 % de production), statuts du filtre servis par l'API, activité non classée affichée « Non classé », aucune erreur console ni violation CSP.

## 3. POINTS D'ATTENTION
- **Vision** : avec les modèles actuels, la Passe 1 n'analyse plus les captures (elle ne le faisait déjà pas en pratique). Pour la rétablir, fournir un modèle Ollama déclarant `vision` (GGUF avec projecteur multimodal) via `MODEL_FAST_VISION`.
- La première synchronisation LanceDB après cette version réindexe tout le coffre une fois, puis seulement le delta.
- Pendant une consolidation, l'injecteur peut refuser une injection (son d'erreur) et la recherche GraphRAG du Command Center répondre 503 : c'est le verrou VRAM qui protège la carte.
- `pip install -r requirements.txt` ne réinstalle plus les paquets retirés ; ils peuvent être désinstallés s'ils ne servent pas à d'autres projets.
