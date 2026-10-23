---
task_id: "EXO-009"
project_id: "exocortex"
component_tag: "mcp-and-graphrag"
title: "v0.2.2 — Serveur MCP Local & GraphRAG Hybride Multi-Sauts"
status: "ready_for_agent"
---
# EXO-009 — v0.2.2 — Serveur MCP Local & GraphRAG Hybride Multi-Sauts

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif Architectural
Transformer l'Exocortex d'un système à injection manuelle (`Alt+Espace`) en une infrastructure interrogeable nativement par n'importe quel agent codeur ou client LLM (Claude Code, Cursor, Cline, Windsurf) via le protocole **MCP (Model Context Protocol)**, tout en enrichissant la recherche vectorielle k-NN d'une traversée de graphe à 1 saut (**GraphRAG Hybride**) sur les `[[wikilinks]]` et les sessions SQLite.

### 1.2 Chantier 1 : Moteur GraphRAG Hybride Multi-Sauts (`src/database/graph_rag.py`)
Actuellement, `vector_store.search(query, top_k=5)` ne retourne que les voisins vectoriels directs. Or, deux notes peuvent être architecturalement liées (ex: une décision de schéma SQL et un composant UI) sans partager le même vocabulaire.
- Créer `src/database/graph_rag.py` contenant la classe `HybridGraphRAG` :
  1. **Ancrage Vectoriel (Hop 0) :** Interroge `vector_store.search(query, top_k=primary_k)` (défaut `primary_k=3`) et décharge immédiatement `bge-m3` (`0 Mo VRAM` résiduelle).
  2. **Traversée des Wikilinks (Hop 1 - Graphe Obsidian) :** Pour chaque note de Hop 0, parse le fichier via `parse_concept_file()` et extrait tous les liens `[[Titre ou Slug]]` présents dans `body` et dans `telemetry_lines` (champ `Connexions sémantiques`).
  3. **Résolution & Scoring CPU des Voisins :** Résout chaque wikilink vers son fichier `.md` dans `02_Concepts/` (correspondance exacte de `slug` ou de `title` insensible à la casse). Attribue un score de pertinence hybride combinant la proximité du parent (Hop 0) et le recouvrement lexical BM25 avec la requête.
  4. **Traversée Épisodique SQLite :** Récupère via `DBManager(read_only=True)` les résumés des sessions Gemini (`chat_sessions`) rattachées aux `session_id` des notes de Hop 0.
  5. **Assemblage Structuré :** Retourne un dictionnaire typé `GraphRAGResult` distinguant les `primary_nodes` (Hop 0), les `linked_neighbors` (Hop 1, max `neighbor_k=3`) et les `episodic_traces`.
- **Intégration dans `hippocampus_hotkey.py` :** Mettre à jour `HippocampusInjector.build_enriched_payload()` pour utiliser `HybridGraphRAG` et inclure une sous-section `### Connexions de Graphe (1-Hop Wikilinks)` dans `<contexte_hippocampe_local>`.

### 1.3 Chantier 2 : Serveur MCP Standard (`src/mcp/exocortex_mcp_server.py`)
Créer un serveur MCP conforme au standard JSON-RPC 2.0 `stdio` (compatible avec le SDK officiel `mcp` (`FastMCP`) ET disposant d'une boucle JSON-RPC `stdio` native sans dépendance externe bloquante si le package `mcp` n'est pas installé) exposant 5 outils en lecture seule (`0 Mo VRAM` permanente) :
1. `search_exocortex_concepts(query: str, topic: Optional[str] = None, top_k: int = 5, include_graph_neighbors: bool = True)` : Exécute la recherche `HybridGraphRAG`, filtre optionnellement par `semantic_topic`, et retourne les notes complètes avec leurs voisins 1-hop.
2. `get_concept_note(slug_or_title: str)` : Lit et retourne le frontmatter et le corps complet d'une fiche de `02_Concepts/`.
3. `get_recent_episodic_telemetry(days: int = 7)` : Retourne les métriques quotidiennes (`daily_metrics`), le temps par topic et les synthèses épisodiques des `N` derniers jours.
4. `get_session_history(session_id: str)` : Retourne les métadonnées et l'intégralité des échanges (`chat_messages`) d'une session Gemini historique.
5. `get_active_kanban_queue(project_id: str = "exocortex")` : Retourne les tâches `in_progress` et `ready_for_agent` avec leurs chemins de spécifications techniques.

### 1.4 Intégration CLI (`run_exocortex.py`)
Ajouter l'argument `--mcp-server` dans `run_exocortex.py` pour lancer le serveur MCP sur `stdio` (avec redirection stricte de tous les `logging` vers `sys.stderr` pour ne jamais corrompre le flux JSON-RPC sur `sys.stdout`).

---

