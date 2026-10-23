L'implémentation de la spécification EXO-011 (v0.3.5 — Enrichissement des Capteurs Passifs : Sonde Git/IDE & Connecteur Navigateur Temps Réel) est achevée avec 100 % de succès et zéro régression (30/30 tests passés).

Invariants et Contraintes Respectés
Confidentialité & Blacklist : Tout événement entrant (URL, titre de page, <h1>, prompt ou réponse LLM) contenant un mot issu de settings.TITLE_BLACKLIST ou settings.EXE_BLACKLIST (mots de passe, secrets, banques, bitwarden, etc.) est immédiatement rejeté avec le code HTTP 204 No Content, sans aucun impact sur SQLite ni sur la RAM.
Performance Démon (< 2% CPU / 0 Mo VRAM) : La sonde Git met en cache ses résultats avec un TTL de 30 secondes par chemin de dépôt, évitant les sous-processus git répétés lors du cycle de polling (2s).
Sécurité Réseau : Le serveur HTTP écoute exclusivement sur le loopback strict 127.0.0.1:8502.
Récapitulatif des Fichiers et Modifications

Sonde Git & IDE (src/daemons/git_ide_probe.py) :

sanitize_url(raw_url: str) -> str : épure les query params de tracking (utm_*, gclid, fbclid, igshid, msclkid, etc.) ainsi que les fragments (#...).
GitIDEProbe :
Identifie si la fenêtre active appartient à un IDE ou terminal (code.exe, pycharm64.exe, windowsterminal.exe, cursor.exe, windsurf.exe, etc.).
Résout le dépôt Git via known_projects, l'inspection du cwd du processus (psutil.Process(pid).cwd()) ou le projet local.
Interroge git rev-parse --abbrev-ref HEAD et git diff --shortstat (timeout 0.5s, sans fenêtre console CREATE_NO_WINDOW).
Met en cache les métadonnées pendant 30 secondes et formate sous la forme : git:{repo_name}:{branch} (+{insertions}/-{deletions}).

Persistance Idempotente des Tours IA (src/database/db_manager.py) :

upsert_live_chat_turn(platform, session_id, user_prompt, ai_response, timestamp) :
Déduplique strictement sur le couple (session_id, user_prompt).
Si un message avec le même prompt existe déjà, met à jour la réponse IA si celle-ci a été complétée, sans incrémenter turn_count.
Si c'est un nouveau tour, insère le message (turn_index = len(messages)) et met à jour turn_count et timestamp_end dans chat_sessions.

Récepteur HTTP Télémétrique Local (src/daemons/browser_telemetry_receiver.py) :

BrowserTelemetryServer basé sur ThreadingHTTPServer (thread d'arrière-plan daemon=True) :
OPTIONS : gestion complète des en-têtes CORS (Access-Control-Allow-Origin: *).
POST /telemetry/tab : validation blacklist, nettoyage via sanitize_url, mise à jour en RAM de current_state.url_or_path et ocr_snippet (<h1>).
POST /telemetry/chat_turn : validation blacklist, persistance idempotente via db.upsert_live_chat_turn.

Démon de Télémétrie (src/daemons/telemetry_daemon.py) :

Ajout de url_or_path et ocr_snippet sur WindowSessionState et transmission dans flush_current_window() vers raw_activity.
Interrogation de GitIDEProbe lors des sessions sur IDE/Terminal.
Rattachement automatique du dernier onglet navigateur reçu en mémoire.
Lancement et arrêt propre de BrowserTelemetryServer dans run_loop().

WebExtension Manifest V3 (browser_extension/) :

manifest.json : déclaration Manifest V3 pour Chrome/Edge/Brave.
background.js : écoute de chrome.tabs.onActivated et chrome.tabs.onUpdated, transmission HTTP non-bloquante avec débouce.
content_script.js : extraction du <h1> et observation via MutationObserver des paires de questions/réponses sur Gemini Web, Claude.ai et ChatGPT.

Suite de Vérification (tests/test_v035_passive_sensors_verification.py) :

test_git_ide_probe_formatting_and_cache : validation du format git:{repo}:{branch} (+X/-Y) et non-réexécution sous cache 30s.
test_browser_receiver_tab_and_blacklist : validation de POST /telemetry/tab, en-têtes CORS et rejet immédiat (204) sur bitwarden.
test_live_chat_turn_ingestion_idempotence : validation de l'idempotence stricte sur double envoi et incrémentation sur nouveau tour.
Validation des Tests
powershell
======================= 30 passed, 4 warnings in 19.39s =======================
tests/test_v012_verification.py (1 test)          PASSED                  [  3%]
tests/test_v013_verification.py (1 test)          PASSED                  [  6%]
tests/test_v014_verification.py (7 tests)         PASSED                  [ 30%]
tests/test_v020_kanban_verification.py (4 tests)  PASSED                  [ 43%]
tests/test_v021_refactoring_verification.py (5)   PASSED                  [ 60%]
tests/test_v022_mcp_graphrag_verification.py (6)  PASSED                  [ 80%]
tests/test_v030_proactivity_verification.py (3)   PASSED                  [ 90%]
tests/test_v035_passive_sensors_verification.py (3) PASSED                [100%]