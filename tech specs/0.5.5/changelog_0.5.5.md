---
task_id: "EXO-019"
project_id: "exocortex"
component_tag: "metrics-accuracy"
title: "v0.5.5 — Audit Lot 5 : Exactitude des Métriques et du Coffre"
status: "done"
---
# EXO-019 — v0.5.5 — Audit Lot 5 : Exactitude des Métriques et du Coffre

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif du Patch
Cinquième lot de l'audit du 24/10/2026 : rendre les chiffres fidèles à la réalité (fuseaux, inactivité, tunnels, estimations) et le coffre stable dans le temps (enrichissement idempotent, taxonomie, liens). Corrige A5, A9, A12, A13, A14, B17 et B18.

### 1.2 Corrections

1. **A12 — Fuseaux horaires (`takeout_parsers.py`, `db_manager.py`)**
   - Toutes les dates en base sont en **heure locale naïve** (`LOCAL_TIMEZONE`, défaut `Europe/Paris`), comme celles du démon. Les exports JSON (`…Z`) et les dates suffixées `UTC`/`GMT` sont convertis ; les dates HTML (CET/CEST ou sans suffixe) restent locales. Nouvelle fonction `parse_date_pair` (heure locale + heure littérale), `parse_date_flexible` renvoie l'heure locale.
   - Choix assumé par rapport à l'audit (qui proposait de stocker en UTC) : stocker en heure locale évite de migrer toute la télémétrie du démon et donne directement la bonne heure pour la heatmap circadienne.
   - Identifiants synthétiques (`synth_…`, suffixe de sous-session) dérivés de l'heure **littérale** de l'export : une réingestion retrouve les mêmes sessions au lieu de créer des doublons.
   - Empreintes JSON déjà stockées en UTC brut : migrées à la réingestion (`legacy_timestamp`), en conservant id, cluster, topic et rattachement, sans doublon.

2. **A5 — Inactivité et tunnels**
   - Démon : au-delà de `IDLE_SPLIT_THRESHOLD_SEC` (5 min) sans saisie, la fenêtre est close à l'instant de la dernière saisie ; seuil de `IDLE_SPLIT_MEDIA_THRESHOLD_SEC` (60 min) pour une fenêtre média (lecture vidéo sans clavier). Un écran verrouillé (`hwnd = 0`) ne produit plus d'activité « Idle ». Détection média factorisée (`is_media_window`).
   - Tunnels (`compute_focus_tunnels`, partagé depuis v0.5.4) : un trou de plus de 120 s entre deux activités rompt toujours le tunnel ; les interruptions sont tolérées sur leur **cumul** (≤ 120 s, trous compris) si l'activité revient ensuite au topic. Les interruptions non absorbées ouvrent le tunnel suivant.

3. **A13 — Enrichissement réellement idempotent (`markdown_io.py`)**
   - Minutes par date tenues dans le frontmatter (`screen_time_by_date`) ; le total est recalculé (temps hors écran + somme par date). Pour une fiche antérieure, la durée de la date est relue dans sa ligne de télémétrie.
   - Section de la date balisée (`<!-- exo:session AAAA-MM-JJ -->` … `<!-- /exo:session … -->`) et remplacée en bloc ; les sous-titres `###` du LLM sont rétrogradés en `####`. Les sections héritées sans balises sont remplacées jusqu'à la section « Session du » suivante.
   - Callouts `[!abstract]` écrits par le LLM retirés (`strip_llm_callouts`, aussi appliqué aux nouvelles fiches nocturnes) ; le parseur repère le callout de télémétrie par son en-tête « Généalogie », sinon le dernier callout. La consigne du prompt système qui incitait le LLM à écrire ce callout est corrigée.

4. **A9 — Valeurs estimées signalées**
   - `daily_metrics.is_estimated` (migration v3, qui marque aussi les lignes cold start existantes) ; le cold start Takeout écrit `is_estimated=1`. Le contrat `DailyKpis` expose `is_estimated` ; l'interface web affiche « (estimé) », Streamlit précise que les heures de chat sont un forfait.
   - `fetch_macro_kpis` : `chat_hours_is_estimated`, ratio lecture/écriture à `None` sans donnée (au lieu de 0,4 inventé).
   - Topic absent compté `Non_Classe` (archéologie) et `A_Trier` (frontmatter), plus `Dev_et_Architecture_Tech` d'office.
   - Mémos vocaux : `time_is_estimated: true` et mention « forfait mémo vocal, non mesuré ».

5. **B17 — Taxonomie par mots entiers (`config.py`)**
   - `normalize_to_macro_topic` découpe le tag en mots (`_`, `-`, espaces, CamelCase, accents ignorés) ; un mot-clé correspond à un mot entier, une racine d'au moins 5 lettres aussi en préfixe, les expressions (« volume eating », « guild wars ») comme expressions. « Psychotherapie », « Storage_Strategy », « Research_Notes », « Enjeux_Climatiques » ne sont plus mal classés.

6. **A14 — Capture live par rang de tour**
   - L'extension (0.5.5) envoie `turn_index` ; `upsert_live_chat_turn` déduplique sur (session, rang) : deux « continue » sont deux tours. Une réponse complétée met à jour le tour existant. Sans `turn_index` (extension antérieure), repli sur l'ancien comportement. Les compteurs de session sont recalculés depuis `chat_messages`.

7. **B18 — Wikilinks résolubles**
   - Chaque fiche écrite reçoit son titre dans `aliases` : les liens `[[Titre]]` (fusions, connexions suggérées, évolutions d'arbitrage) sont résolus par Obsidian, sans casser le contrat de réécriture de v0.4.0.
   - Les liens vers des noms de catégories (qui ne sont pas des fichiers) deviennent des tags `#Categorie` ; le lien fictif `[[Exocortex]]` par défaut est supprimé.

### 1.3 Fichiers modifiés
`src/__init__.py`, `src/config.py`, `src/ingestors/takeout_parsers.py`, `src/ingestors/takeout_ingestor.py`, `src/ingestors/voice_ingestor.py`, `src/database/db_manager.py`, `src/daemons/telemetry_daemon.py`, `src/daemons/browser_telemetry_receiver.py`, `src/utils/cognitive_metrics.py`, `src/utils/markdown_io.py`, `src/consolidators/night_consolidator.py`, `src/llm/prompts.py`, `src/dashboard/app.py`, `src/web_gui/app.js`, `src/web_gui/index.html`, `browser_extension/content_script.js`, `browser_extension/manifest.json`, `start_web_center.bat`, `tests/test_v055_metrics_accuracy_verification.py` (nouveau).

## 2. VÉRIFICATION

Suite `tests/test_v055_metrics_accuracy_verification.py` (31 tests) :
- **A12** : le même instant lu 14:30 en HTML et 12:30Z en JSON donne 14:30 local ; conversion d'hiver (UTC+1) ; identifiant `synth_20261001_123000` inchangé ; empreinte UTC migrée sans doublon, cluster et topic conservés.
- **A5** : deux sessions à 11 h d'écart = deux tunnels ; Slack 1 min + Mail 1 min absorbés (tunnel de 62 min) ; 2 min 30 d'interruption rompent le tunnel ; démon : 8 h sans saisie → 10 min enregistrées ; écran verrouillé → aucune activité « Idle ».
- **A13** : 145 puis 190 min → total 55 + 190 ; « Arbitrages » présent une seule fois ; fiche héritée réajustée (200 − 145 + 190) ; un callout LLM n'emporte plus la section « Choix Techniques ».
- **A9** : journée cold start `is_estimated` dans l'API, heures de chat marquées estimées, topic par défaut `A_Trier`, aucune session sans topic comptée « Dev » ; migration v3 sur une base héritée.
- **B17** : 16 cas, dont les 6 de l'audit.
- **A14** : « continue » ×2 → 3 tours, réponse complétée mise à jour ; repli sans rang.
- **B18** : alias du titre écrit une seule fois ; liens de catégories devenus des tags.

Résultats (coffre temporaire) : **118 passed, 1 skipped** sur les suites hermétiques v0.2.0 → v0.5.5 ; les 5 échecs préexistants de v0.1.2–v0.1.4 sont inchangés (F1, lot 6).

## 3. POINTS D'ATTENTION
- **Extension à recharger** (0.5.5) pour bénéficier de la déduplication par rang.
- Réingérer le Takeout après cette version convertit en heure locale les dates des exports JSON déjà importés (sessions et empreintes), sans doublon.
- Les fiches existantes reçoivent `aliases` et `screen_time_by_date` à leur prochaine réécriture seulement.
- Le temps sans saisie de plus de 5 min n'est plus compté : les durées et tunnels des nouvelles journées seront plus courts que ceux d'avant cette version.
