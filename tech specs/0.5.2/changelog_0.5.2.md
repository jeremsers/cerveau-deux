---
task_id: "EXO-016"
project_id: "exocortex"
component_tag: "security-network"
title: "v0.5.2 — Audit Lot 2 : Fermeture de l'Exposition Réseau & Confidentialité"
status: "done"
---
# EXO-016 — v0.5.2 — Audit Lot 2 : Fermeture de l'Exposition Réseau & Confidentialité

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif du Patch
Deuxième lot de l'audit du 24/10/2026. Modèle de menace retenu : une page web ouverte dans le navigateur de l'utilisateur, pendant que les services locaux tournent, ne doit ni lire les données de l'Exocortex, ni en écrire, ni injecter du code dans l'interface. Corrige D1, D2, D4, D5, D6, D7, E6, ainsi que les deux affirmations erronées du README relevées en G1 (lecture seule, aucune donnée transmise).

### 1.2 Corrections

1. **D1 — API 8500 (`src/api/server.py`)**
   - CORS : `allow_origins="*"` + `allow_credentials=True` remplacés par la liste `WEB_GUI_CORS_ORIGINS` (ports de dev 4321 et 5173 sur localhost/127.0.0.1), sans credentials, méthodes et en-têtes explicites.
   - `TrustedHostMiddleware` (`WEB_GUI_ALLOWED_HOSTS`, défaut `127.0.0.1,localhost`) : bloque le DNS rebinding.
   - Jeton local (`src/utils/local_auth.py`) exigé dans l'en-tête `X-Exocortex-Token` pour toute méthode d'écriture sur `/api/*` et pour les GET à effet de bord (`context-pack`, `coder-prompt`). Un en-tête personnalisé impose un pré-vol CORS, refusé aux origines tierces : une page web ne peut plus émettre ces requêtes.
   - Nouvelle route `GET /api/auth/token` : remet le jeton à l'interface servie par le serveur (même origine, `Sec-Fetch-Site`) ou à une origine de dev autorisée ; 403 sinon.
   - Le jeton est stocké dans `_System_Buffer/api_token` (créé au premier usage, hors Git) ou fourni par `EXOCORTEX_API_TOKEN`.

2. **D2 — XSS stocké (`src/web_gui/app.js`, `index.html`)**
   - Fonction `esc()` appliquée à toute donnée interpolée dans un gabarit HTML : messages de chat, résumés, titres de fenêtres, URL, tâches Kanban, empreintes, résultats GraphRAG, toasts, info-bulles du Gantt.
   - Markdown (bootloader, concepts, specs) rendu via `renderMarkdownSafe()` : `DOMPurify.sanitize(marked.parse(...))`.
   - Tous les `onclick`/`onchange` inline générés sont remplacés par des attributs `data-action` traités par délégation (`bindDelegatedActions`). Les identifiants interpolés dans les URL passent par `encodeURIComponent`.
   - Content-Security-Policy posée par le serveur : `script-src 'self' https://cdn.plot.ly https://cdn.jsdelivr.net` (aucun script inline), `connect-src 'self'`, `object-src 'none'`, `frame-ancestors 'none'`, plus `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`.
   - La configuration Tailwind inline est déplacée dans `src/web_gui/tailwind.config.js`.

3. **D5 — Bibliothèques tierces**
   - Plotly 2.32.0, Marked 12.0.2 et DOMPurify 3.1.6 (nouveau) chargés en version exacte avec `integrity="sha384-…"` et `crossorigin="anonymous"`.
   - Tailwind Play 3.4.16 servi en local (`src/web_gui/vendor/tailwindcss-play-3.4.16.js`, licence MIT) : `cdn.tailwindcss.com` n'envoie pas d'en-tête CORS, ce qui rend SRI impossible (vérifié dans Chrome : le script était bloqué).

4. **D4 — Récepteur 8502 (`browser_telemetry_receiver.py`) et extension**
   - CORS : l'origine n'est renvoyée que pour une origine d'extension (`chrome-extension://`, `moz-extension://`) ; pré-vol d'une autre origine → 403.
   - `GET /auth/token` remet le jeton `browser_receiver` uniquement à une origine d'extension (ou à un client local sans `Origin`) ; tout `POST` exige `X-Exocortex-Token`.
   - Corps borné (`BROWSER_RECEIVER_MAX_BODY_BYTES`, 512 Ko → 413), `Content-Type: application/json` obligatoire (415).
   - Une URL d'onglet n'est rattachée qu'à une fenêtre de navigateur (`is_browser_executable`) : plus de rattachement à VS Code par course.
   - Extension 0.5.2 (`background.js`) : récupère le jeton, l'envoie à chaque `POST`, le renouvelle une fois sur 401.

5. **E6 — Périmètre du content script (`manifest.json`)**
   - `<all_urls>` retiré : le script n'est injecté que sur Gemini, Claude et ChatGPT. Conséquence : les onglets ordinaires ne remontent plus leur `<h1>`, seulement URL et titre.

6. **D7 — Liste noire (`src/utils/privacy.py`, `config.py`)**
   - Correspondance en **mots entiers**, insensible à la casse et aux accents, sur des marqueurs ciblés (navigation privée, gestionnaires de mots de passe, banques, administrations), au lieu de sous-chaînes. Les termes génériques `login`, `connexion`, `bank`, `password`, `credentials`, `authenticator` sont retirés.
   - Nouvelle liste `SENSITIVE_DOMAINS` (banques, paiement, impots, ameli, CAF, FranceConnect, gestionnaires de mots de passe, pages de connexion Google/Microsoft), appliquée par domaine et sous-domaines aux URL reçues.
   - Exécutables comparés par nom exact (`EXE_BLACKLIST`, enrichi de KeePassXC et Dashlane).
   - Extensions sans modifier le code : `TITLE_BLACKLIST_EXTRA`, `SENSITIVE_DOMAINS_EXTRA`.
   - Tours de chat : rejet sur divulgation de secret (`contains_secret_disclosure` : « mot de passe … : valeur », clés `sk-…`, `ghp_…`, `AKIA…`, clé privée PEM) plutôt que sur la simple mention du mot « mot de passe ».
   - Le démon (`TelemetryDaemon.is_blacklisted`) et le récepteur partagent ce module.

7. **D6 — Export Google Drive (`drive_compiler.py`)**
   - `DRIVE_EXCLUDED_TOPICS` (défaut : `Sante_et_Pharmacologie`, `Introspection_et_Neuroatypie`, `Admin_Finance_et_Droit`) : fiches exclues de `02_PROJETS_ET_CONCEPTS_ACTIFS` et de `03_INDEX_GRAPHE_CONCEPTS` ; noms masqués en « Catégories privées » dans les tableaux de `01_TELEMETRIE` ; lignes nommant ces catégories retirées des journaux et de la taxonomie exportés ; mention explicite dans `00_CORE`.

8. **G1 (partiel) — README**
   - « Lecture seule stricte » du dashboard corrigé (l'onglet Kanban écrit en base).
   - Section confidentialité réécrite : liste noire ciblée, ce qui peut sortir de la machine (Drive, mode `cloud_api`, staging manuel), protection des services locaux. La mise à jour complète du README est prévue au lot 7 (v0.5.7).

### 1.3 Fichiers modifiés
`src/__init__.py`, `src/config.py`, `src/utils/local_auth.py` (nouveau), `src/utils/privacy.py` (nouveau), `src/api/server.py`, `src/daemons/browser_telemetry_receiver.py`, `src/daemons/telemetry_daemon.py`, `src/consolidators/drive_compiler.py`, `src/web_gui/app.js`, `src/web_gui/index.html`, `src/web_gui/tailwind.config.js` (nouveau), `src/web_gui/vendor/tailwindcss-play-3.4.16.js` (nouveau), `browser_extension/manifest.json`, `browser_extension/background.js`, `browser_extension/content_script.js`, `start_web_center.bat`, `README.md`, `tests/test_v052_network_exposure_verification.py` (nouveau), `tests/test_v035_passive_sensors_verification.py`, `tests/test_v050_web_api_verification.py`, `tests/test_v051_data_loss_verification.py`.

## 2. VÉRIFICATION

Suite `tests/test_v052_network_exposure_verification.py` (18 tests) :
- **D1** : origine tierce sans `Access-Control-Allow-Origin` ni credentials ; `DELETE`, consolidation et `coder-prompt?mark_in_progress=true` sans jeton → 401 ; avec jeton → 200 ; jeton refusé en `cross-site` ; origine de dev autorisée ; `Host: attacker.example` → 400.
- **D2/D5** : CSP sans script inline sur `/` et `/api/*` ; aucun handler inline ni script inline dans `app.js`/`index.html` ; Markdown assaini ; 3 scripts CDN épinglés avec SRI, Tailwind local.
- **D4** : `POST` sans jeton → 401 (y compris tour de chat forgé) ; pré-vol et jeton refusés à une origine web ; 415, 413 ; URL non rattachée à VS Code.
- **E6** : plus de `<all_urls>` dans le manifest.
- **D7** : les 9 titres de l'échantillon (dont ceux de l'audit : `login_flow.ts`, « Problème de connexion », « Bankai », « Mon compte — Boursorama ») correctement classés ; divulgation de secret détectée sans bloquer une question sur argon2.
- **D6** : fiche santé absente de l'export, catégorie masquée, taxonomie expurgée.

Tests existants adaptés au nouveau contrat (comportement voulu, pas une régression) : v0.3.5 (l'extension envoie le jeton ; l'en-tête CORS vaut l'origine de l'extension et non plus `*`), v0.5.0 et v0.5.1 (client de test sur `127.0.0.1` avec jeton).

Résultats (coffre temporaire) : **60 passed** sur les suites hermétiques v0.2.0 → v0.5.2. Suites v0.1.2, v0.1.3, v0.1.4 : les 5 mêmes échecs qu'avant le lot (volumes personnels codés en dur, F1, lot 6). v0.5.0 passe.

Vérification navigateur : interface chargée dans Chrome headless sous la CSP. Tailwind appliqué, Gantt Plotly rendu, aucune violation CSP ni erreur d'intégrité ; un titre de fenêtre piégé (`<b onmouseover=…>`) s'affiche échappé.

## 3. POINTS D'ATTENTION
- **Extension à recharger** dans `chrome://extensions` (version 0.5.2) : l'ancienne version, sans jeton, reçoit désormais 401.
- Si le Command Center est lancé avec `--host` autre que `127.0.0.1`/`localhost`, ajouter ce nom à `WEB_GUI_ALLOWED_HOSTS`.
- Un front de dev sur un autre port que 4321/5173 doit être ajouté à `WEB_GUI_CORS_ORIGINS`.
- Supprimer `_System_Buffer/api_token` ou `browser_receiver_token` régénère le jeton ; l'interface et l'extension le relisent automatiquement.
- Pour mettre à jour une bibliothèque CDN, changer la version **et** recalculer l'empreinte `sha384`, sinon le navigateur refuse le script.
