---
task_id: "EXO-010"
project_id: "exocortex"
component_tag: "executive-proactivity"
title: "v0.3.0 — Proactivité Exécutive, Context Bootloader & Garde-Fou Rabbit Hole"
status: "ready_for_agent"
---
# EXO-010 — v0.3.0 — Proactivité Exécutive, Context Bootloader & Garde-Fou Rabbit Hole

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif Architectural
Supprimer les deux principaux facteurs de friction d'un profil HPI/AuDHD à hyperfocus :
1. **L'inertie d'amorçage au réveil** (coût cognitif de rechargement de la pile mentale après une coupure) via un **Context Bootloader** généré en fin de consolidation nocturne.
2. **La perte des intentions implicites** ("il faudrait tester X") via un **Extracteur d'Open Loops** rattaché directement au `KanbanEngine` existant (statut `radar`).
3. **La dérive attentionnelle temps réel** (zapping frénétique ou bascule prolongée vers du média non planifié) via un **Détecteur statistique 0-VRAM** dans `telemetry_daemon.py`.

### 1.2 Chantier 1 : Le « Context Bootloader » & Extracteur d'Open Loops (`src/consolidators/night_consolidator.py`)
En fin de **Passe 2** (pendant que `gemma4:26b-a4b` ou `12b` est déjà chargé en VRAM, donc **0 rechargement VRAM supplémentaire**), ajouter l'étape `generate_executive_bootloader(target_date, metric)` :
- **Entrées :** Les dernières activités de la journée (dernières 2 heures actives), les fiches conceptuelles créées ou modifiées le jour même, et les tâches `in_progress` du `KanbanEngine`.
- **Schéma Pydantic `ExecutiveBootloaderSchema` :**
  - `last_active_state: str` : Où l'utilisateur s'est arrêté (heure, exécutable, fichier/sujet exact).
  - `immediate_next_steps: List[str]` : 3 à 5 actions concrètes et atomiques pour reprendre en < 2 minutes sans réfléchir.
  - `detected_open_loops: List[OpenLoopItem]` : Intentions, bugs en suspens ou pistes évoquées (`title`, `component_tag`, `summary_pitch`, `priority`).
- **Sorties :**
  1. Écriture de `Vault_Data/00_Meta/00_BOOTLOADER_DEMAIN.md` contenant le point d'arrêt, la checklist de redémarrage rapide et les liens `[[wikilinks]]` vers les fiches actives.
  2. Injection idempotente des `detected_open_loops` dans la table SQLite `kanban_tasks` via `kanban_engine.create_task(..., initial_status="radar")` (avec déduplication sur le titre normalisé pour ne jamais créer deux fois le même ticket).

### 1.3 Chantier 2 : Garde-Fou Temps Réel Anti-Dérive / Rabbit Hole (`src/daemons/telemetry_daemon.py`)
Ajouter dans `TelemetryDaemon` un analyseur glissant purement statistique en RAM (`DriftGuard`, **0 Mo VRAM, 0 requête LLM**) :
- Conserve une fenêtre glissante `collections.deque` des événements et changements de fenêtre sur les **90 dernières minutes**.
- Détecte 2 patterns de dérive :
  1. **`hyper_fragmentation` (Zapping) :** Plus de `DRIFT_MAX_SWITCHES_30MIN` (défaut : `25` changements de contexte en 30 minutes avec durée moyenne < 45s).
  2. **`unplanned_media_hole` (Dérive Passive) :** Plus de `DRIFT_MAX_PASSIVE_MIN` (défaut : `90` minutes cumulées d'exécutables ou titres classés heuristiquement en `media`/`exploration` passive sans input clavier significatif `input_intensity < 0.15` après un tunnel de `production`).
- **Action non-intrusive :** Enregistre l'alerte d'état dans `Vault_Data/_System_Buffer/drift_state.json` (lu par le Dashboard) et émet un double bip discret (`winsound.Beep(600, 120)`) avec un *cooldown* strict de 60 minutes entre deux alertes pour ne jamais harceler l'utilisateur.

### 1.4 Chantier 3 : Affichage Exécutif en Haut du Dashboard (`src/dashboard/app.py`)
Dans `render_dashboard()`, juste sous le bandeau des 5 KPIs macro :
- Si `00_BOOTLOADER_DEMAIN.md` existe, afficher un expander mis en valeur `🚀 Context Bootloader — Reprise Rapide & État Mental` (ouvert par défaut si aucune activité de production n'a encore eu lieu aujourd'hui, replié sinon).
- Si `drift_state.json` signale une dérive récente (< 60 min), afficher un bandeau d'avertissement sobre avec le diagnostic statistique.

---
