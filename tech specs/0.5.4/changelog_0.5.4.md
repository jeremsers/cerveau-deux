---
task_id: "EXO-018"
project_id: "exocortex"
component_tag: "interface-contracts"
title: "v0.5.4 — Audit Lot 4 : Réconciliation Backend ↔ Interfaces & Tests de Contrat"
status: "done"
---
# EXO-018 — v0.5.4 — Audit Lot 4 : Réconciliation Backend ↔ Interfaces & Tests de Contrat

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif du Patch
Quatrième lot de l'audit du 24/10/2026. Les interfaces (web, Streamlit, MCP) lisaient des clés, des modes et des statuts que le backend n'écrivait pas : KPIs du jour à 0 après chaque nuit, pastille DriftGuard toujours « STABLE », modes cognitifs inventés, filtres fictifs, libellés figés. Ce lot instaure des sources uniques et des tests de contrat. Corrige B1 à B10 et F2.

### 1.2 Sources uniques

- **Vocabulaires (`src/config.py`)** : `COGNITIVE_MODES` (production, exploration, chat_ia, gaming, media, non_classe, avec libellés et couleurs), `DISTILLATION_STATUSES` (success, pending, misc_noise, failed_fallback), `normalize_cognitive_mode()` (NULL ou inconnu → `non_classe`).
- **Calculs partagés (`src/utils/cognitive_metrics.py`, nouveau)** : `compute_focus_tunnels` (tunnels d'hyperfocus), `build_daily_kpis` + modèle `DailyKpis`, `compute_drift_status` + modèle `DriftStatus`, `diagnose_circadian` (profil déduit des données, seuil de dominance explicite à 40 %).
- **Nouvelle route `GET /api/meta/vocabulary`** : modes, statuts et topics servis aux interfaces.

### 1.3 Corrections

1. **B1 — KPIs du jour** : `/api/telemetry/timeline` renvoie toujours un `DailyKpis` (mêmes clés que la journée soit consolidée ou non, champ `is_consolidated`). `total_active_sec` et `total_deep_work_sec` viennent de `daily_metrics` quand la journée est consolidée ; les KPIs ne retombent plus à 0 après la nuit.
2. **B2 — Modes cognitifs** : `app.js` n'utilise plus `Deep_Work/Execution/Communication/Passive/Noise` ; Gantt, table, treemap et donut prennent libellés et couleurs du vocabulaire. Les activités non classées s'affichent « Non classé » (plus « Deep_Work » côté web, plus « exploration » côté Streamlit). Le score d'alignement = production active / total.
3. **B3 — DriftGuard** : `/api/system/status` renvoie un `DriftStatus` stable dont le booléen `active` (alerte de moins d'une heure) est calculé côté serveur ; la pastille web lit `drift_state.active` et affiche le diagnostic en info-bulle. Streamlit utilise la même fonction.
4. **B4 — `url_or_path`** : ajouté (avec `id`) au SELECT de `fetch_timeline_for_date` ; visible dans la table et le Gantt web.
5. **B5 — Filtres de l'explorateur web** : statuts et topics remplis depuis `/api/meta/vocabulary` (`skipped` fictif supprimé, `misc_noise` et `failed_fallback` ajoutés ; le filtre de topic est enfin alimenté).
6. **B6 — Treemap web** : nœuds identifiés par `ids` hiérarchiques (`m:mode|t:topic|e:exe`) et parents par id, `branchvalues: "total"`.
7. **B7 — Une seule définition des tunnels** : la consolidation nocturne, l'API (cartes de tunnels, compteur) et Streamlit appellent `compute_focus_tunnels` ; l'API ne liste plus chaque fenêtre de 30 min comme un tunnel.
8. **B8 — Bootloader Streamlit** : déplié si la production **du jour** est nulle (`load_today_production_sec`), et non plus la production cumulée de toute la base.
9. **B9 — Libellés figés** : « Hyperfocus Crépusculaire & Nocturne », « Chronotype du Loup », « 690 sessions », « 6 649 messages », « 480 sessions », « 73 153 / 73k empreintes » remplacés par des valeurs lues en base et par `diagnose_circadian` (champ `diagnosis` de `/api/telemetry/circadian`).
10. **B10 — Serveur MCP** : table unique `build_tool_functions()` utilisée par FastMCP (`add_tool` avec les noms et descriptions de `MCP_TOOLS_SPEC`) et par la boucle JSON-RPC autonome ; anciens noms `mcp_*` acceptés en alias. `serverInfo.version` = `__version__`. `mcp>=1.2,<2` ajouté à `requirements.txt` (le chemin `mcp.server.fastmcp` n'existe plus en 2.x).

### 1.4 Fichiers modifiés
`src/__init__.py`, `src/config.py`, `src/utils/cognitive_metrics.py` (nouveau), `src/api/server.py`, `src/database/db_manager.py`, `src/consolidators/night_consolidator.py`, `src/dashboard/app.py`, `src/web_gui/app.js`, `src/web_gui/index.html`, `src/mcp/exocortex_mcp_server.py`, `requirements.txt`, `start_web_center.bat`, `tests/test_v054_contracts_verification.py` (nouveau).

## 2. VÉRIFICATION

Suite `tests/test_v054_contracts_verification.py` (14 tests de contrat, F2) :
- **B1** : même jeu de clés `DailyKpis` avant et après consolidation ; après la nuit, 91 min d'activité, 50 min de production, 2 tunnels ; toute clé `metric.*` lue par `app.js` existe dans le contrat.
- **B4** : `url_or_path` et `id` présents dans les événements.
- **B7** : tunnel le plus long identique côté API et `daily_metrics` (50 min) ; Streamlit utilise la fonction partagée.
- **B2/B5** : vocabulaire servi = vocabulaire de la config ; aucun mode hérité ni `skipped` dans le front ; les modes et statuts écrits par le backend (code et prompts) appartiennent au vocabulaire.
- **B3** : contrat `DriftStatus`, alerte active à 5 min, inactive à 2 h ; `app.js` lit `drift.active`.
- **B6/B8/B9** : treemap à `ids`, bootloader sur la production du jour, aucun libellé figé, diagnostic « Profil matinal » sur des données matinales.
- **B10** : noms identiques entre `tools/list`, la table et les paramètres des fonctions ; alias hérités ; version ; enregistrement FastMCP vérifié avec le SDK `mcp` 1.30 installé dans un dossier isolé (test ignoré si `mcp` est absent) ; épinglage dans `requirements.txt`.

Résultats (coffre temporaire) : **87 passed, 1 skipped** (FastMCP, `mcp` non installé dans l'environnement par défaut ; **passé** avec `mcp` 1.30). Les 5 échecs préexistants de v0.1.2–v0.1.4 sont inchangés (F1, lot 6).

Vérification d'interface : dashboard Streamlit exécuté avec `streamlit.testing.v1.AppTest` sur un coffre temporaire — aucune exception, alerte DriftGuard affichée par la logique partagée.

## 3. POINTS D'ATTENTION
- `pip install -r requirements.txt` installe désormais `mcp` 1.x : le serveur MCP passe alors par FastMCP, avec les mêmes noms d'outils qu'auparavant en mode autonome.
- Les journées déjà consolidées gardent leur `max_hyperfocus_sec` historique ; il est recalculé avec la définition unique à leur prochaine consolidation.
- Streamlit affiche des avertissements de dépréciation `use_container_width` (préexistants, sans effet fonctionnel).
