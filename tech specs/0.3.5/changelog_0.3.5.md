---
task_id: "EXO-011"
project_id: "exocortex"
component_tag: "passive-sensors"
title: "v0.3.5 — Enrichissement des Capteurs Passifs (Sonde Git/IDE & Connecteur Navigateur Temps Réel)"
status: "ready_for_agent"
---
# EXO-011 — v0.3.5 — Enrichissement des Capteurs Passifs (Sonde Git/IDE & Connecteur Navigateur Temps Réel)

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif Architectural
Actuellement, la colonne `url_or_path` de `raw_activity` reste à `None`, et les conversations IA nécessitent encore des exports Google Takeout manuels. Cette version enrichit la télémétrie passive à **0 Mo VRAM** via deux capteurs :
1. **Une Sonde Contextuelle Git & IDE** dans `telemetry_daemon.py` qui inspecte l'état des dépôts locaux lorsque l'utilisateur travaille dans VS Code, PyCharm ou Windows Terminal.
2. **Un Récepteur HTTP Local (`127.0.0.1:8502`) + WebExtension Manifest V3** qui renseigne l'URL active et capture au fil de l'eau les nouveaux échanges sur Gemini Web App, Claude et ChatGPT directement dans `chat_sessions` et `chat_messages`.

### 1.2 Chantier 1 : Sonde Contextuelle Git & IDE (`src/daemons/git_ide_probe.py`)
Lorsque l'exécutable au premier plan appartient à `{"code.exe", "pycharm64.exe", "windowsterminal.exe", "powershell.exe", "cmd.exe", "cursor.exe", "windsurf.exe"}` :
- Identifier le dépôt Git actif :
  - Soit en faisant correspondre le nom du dossier/projet présent dans `window_title` (ex: `fichier.py - mon-projet - Visual Studio Code`) avec les `repo_path` enregistrés dans la table SQLite `projects` ou le répertoire courant.
  - Soit en inspectant `psutil.Process(pid).cwd()`.
- Exécuter avec un cache TTL de 30 secondes (pour garantir `< 0.5% CPU`) `git rev-parse --abbrev-ref HEAD` et `git diff --shortstat` (timeout strict 0.5s, `CREATE_NO_WINDOW` sous Windows).
- Formater `url_or_path` sous la forme : `git:{repo_name}:{branch} (+{insertions}/-{deletions})`.

### 1.3 Chantier 2 : Récepteur Télémétrique Local (`127.0.0.1:8502`) & Ingestion Live IA
- Créer `src/daemons/browser_telemetry_receiver.py` utilisant `http.server.ThreadingHTTPServer` de la bibliothèque standard Python (exécuté dans un thread `daemon=True` au sein de `TelemetryDaemon`) écoutant exclusivement sur `127.0.0.1:8502` :
  - **`POST /telemetry/tab` :** Reçoit `{"url": str, "title": str, "h1": str, "domain": str}`.
    - Filtre l'URL et le titre via `TelemetryDaemon.is_blacklisted()`.
    - Si valide, met à jour en RAM `current_state.url_or_path = url` (en retirant les query params de tracking `utm_*`, `fbclid`, etc.) et enrichit `ocr_snippet` avec le `<h1>`.
  - **`POST /telemetry/chat_turn` :** Reçoit `{"platform": "gemini"|"claude"|"chatgpt", "session_id": str, "user_prompt": str, "ai_response": str, "url": str}`.
    - Calcule un identifiant de session stable et insère/met à jour de manière idempotente la session dans `chat_sessions` et le tour dans `chat_messages` (déduplication par hash ou couple `(session_id, user_prompt)`).
- Créer dans `browser_extension/` les 3 fichiers prêts à charger dans Chrome/Edge/Brave (`manifest.json` Manifest V3, `background.js`, `content_script.js`) avec gestion CORS (`Access-Control-Allow-Origin: *`).

---

## 2. PROMPT D'EXÉCUTION POUR L'AGENT CODEUR

Tu es un Ingénieur Système Senior Python & WebExtension. Implémente la spécification **EXO-011 (v0.3.5 — Enrichissement des Capteurs Passifs : Sonde Git/IDE & Connecteur Navigateur Temps Réel)**.

### Invariants & Contraintes Strictes
1. **Confidentialité & Blacklist :** Toute URL ou titre contenant un mot de `settings.TITLE_BLACKLIST` doit être rejeté immédiatement avec un code `204 No Content` sans jamais toucher SQLite ni la RAM.
2. **Performance Démon (< 2% CPU) :** La sonde Git doit mettre en cache son résultat par `repo_path` pendant 30 secondes afin de ne jamais спамmer de sous-processus `git` à chaque tick de 2 secondes.
3. **Sécurité Réseau :** Le serveur HTTP ne doit écouter que sur `127.0.0.1` (loopback strict).

### Étapes d'Implémentation
1. **Créer `src/daemons/git_ide_probe.py` :**
   - Implémenter `GitIDEProbe` avec `probe_active_ide(pid: int, executable: str, window_title: str, known_projects: List[Dict[str, Any]]) -> Optional[str]`.
   - Implémenter `sanitize_url(raw_url: str) -> str` qui supprime les paramètres de tracking (`utm_source`, `utm_medium`, `utm_campaign`, `gclid`, `fbclid`) et les fragments inutiles.
2. **Créer `src/daemons/browser_telemetry_receiver.py` :**
   - Implémenter `BrowserTelemetryServer` (basé sur `ThreadingHTTPServer`) exposant `POST /telemetry/tab`, `POST /telemetry/chat_turn` et `OPTIONS` (CORS).
   - Implémenter la persistance live des tours de chat IA dans `DBManager` via une nouvelle méthode `upsert_live_chat_turn(platform: str, session_id: str, user_prompt: str, ai_response: str, timestamp: Optional[datetime] = None) -> Dict[str, Any]`.
3. **Mettre à jour `src/daemons/telemetry_daemon.py` :**
   - Ajouter `url_or_path: Optional[str] = None` dans `WindowSessionState` et le transmettre à `RawActivityRecord` dans `flush_current_window()`.
   - Appeler `GitIDEProbe` lors des sessions sur IDE/Terminal.
   - Démarrer optionnellement `BrowserTelemetryServer` dans `run_loop()`.
4. **Créer l'extension navigateur dans `browser_extension/` :**
   - Générer `manifest.json` (Manifest V3), `background.js` et `content_script.js` (envoi de l'onglet actif et capture des échanges IA).
5. **Créer `tests/test_v035_passive_sensors_verification.py` :**
   - `test_git_ide_probe_formatting_and_cache` : Vérifie l'extraction du repo/branche/diff sur le dépôt local courant et le fonctionnement du cache 30s.
   - `test_browser_receiver_tab_and_blacklist` : Lance `BrowserTelemetryServer` sur un port éphémère, envoie un `POST /telemetry/tab` valide puis un `POST` contenant `"bitwarden"` et vérifie le filtrage strict.
   - `test_live_chat_turn_ingestion_idempotence` : Envoie deux fois le même tour via `POST /telemetry/chat_turn` et vérifie qu'aucun doublon n'est créé dans `chat_messages` et que `turn_count` est exact dans `chat_sessions`.
   - Exécuter `pytest tests/ -v`.
```

---