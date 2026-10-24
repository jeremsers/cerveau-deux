---
task_id: "EXO-020"
project_id: "exocortex"
component_tag: "daemons-robustness"
title: "v0.5.6 — Audit Lot 6 : Démons, Robustesse, Suite de Tests Hermétique"
status: "done"
---
# EXO-020 — v0.5.6 — Audit Lot 6 : Démons, Robustesse, Suite de Tests Hermétique

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif du Patch
Sixième lot de l'audit du 24/10/2026 : fiabiliser les démons Windows, unifier le journal épisodique, rendre les écritures atomiques, trancher l'interface principale et — surtout — rendre la suite de tests entièrement hermétique, pour qu'elle ne puisse plus jamais lire ni modifier le coffre et la base réels. Corrige E1 à E5, A10, G6, G3, F1 et F3. (Le verrou VRAM inter-processus C8, prévu par l'audit dans ce lot, est traité avec les autres constats d'inférence au lot 7.)

### 1.2 Corrections

1. **E1 — Raccourci configurable** : `HIPPOCAMPUS_HOTKEY` (syntaxe pynput), défaut `<ctrl>+<alt>+<space>`. Alt+Espace ouvrait le menu système de la fenêtre et était souvent capté par PowerToys Run.
2. **E2 — Travail hors du hook clavier** : `on_hotkey_triggered` ne fait plus que déléguer à un thread dédié (`_process_hotkey`) et rend la main immédiatement ; un verrou non bloquant ignore les activations pendant un traitement. Windows ne retire plus silencieusement le hook pour lenteur (`LowLevelHooksTimeout`).
3. **E3 — DriftGuard** : l'alerte « dérive média » exige un tunnel de production préalable (`DRIFT_MIN_PRODUCTION_TUNNEL_MIN`, 30 min de saisie active hors média avant la séquence passive), conformément à la spec v0.3.0. L'historique est allongé (`max_passive_min + DRIFT_PRODUCTION_LOOKBACK_MIN`) : avec 90 min de média dans une fenêtre de 90 min, la condition était impossible à observer. Une soirée film sans travail préalable ne déclenche plus d'alerte.
4. **E4 — Arrêt propre** : nouveau module `src/utils/lifecycle.py`. `stop_exocortex.bat` appelle `python run_exocortex.py --stop` : un fichier-signal (`_System_Buffer/stop_daemons.flag`) demande aux démons de sauvegarder la fenêtre en cours puis de sortir ; les processus restants (serveur web, Streamlit, démons bloqués) sont ensuite arrêtés. Plus de `wmic`. Sous Windows, `Stop-Process -Force` ne délivrait aucun signal : la fenêtre en cours était perdue. `--all` demande aussi l'arrêt propre à la sortie.
5. **E5 — Résolution du dépôt Git** : `extract_ide_workspace` lit le nom du workspace dans le titre (VS Code, Cursor, Windsurf, VSCodium, JetBrains) ; correspondance **exacte** avec les projets connus, puis index des `workspaceStorage/*/workspace.json` des IDE de la famille VS Code ; le répertoire courant du processus n'est plus utilisé que pour les terminaux. Les correspondances par sous-chaîne du titre sont supprimées (un projet « api » ne capte plus « api-gateway »).
6. **A10 — Journal épisodique unique** : `src/utils/episodic_journal.py`. Un journal est composé de sections balisées remplacées séparément : `telemetrie` (consolidation nocturne) et `sessions_ia` (cold start Takeout) ; frontmatter fusionné, liste `sources`. Les journaux antérieurs sont convertis à la lecture. La nuit consolide toute date sans section télémétrie : un journal cold start ne bloque plus son jour, et le journal nocturne n'efface plus les sessions Gemini.
7. **G6 — Écriture atomique** : `src/utils/atomic_io.atomic_write_text` (fichier temporaire, `fsync`, `os.replace`) pour les fiches (`write_concept_file`), les journaux, le bootloader, `AGENT_QUEUE.md` et les specs Kanban. Une interruption laisse l'ancienne version intacte au lieu d'une note tronquée.
8. **G3 — Interface principale** : conformément à la spec v0.5.0 (remplacement de Streamlit), `start_exocortex.bat` et `run_exocortex.py --all` lancent le Command Center Web. Streamlit reste disponible (`--dashboard`) comme interface secondaire, adossée depuis v0.5.4 aux mêmes requêtes et contrats.
9. **F1 / F3 — Suite hermétique**
   - `tests/conftest.py` redirige `VAULT_ROOT`, `TAKEOUT_DIR`, `MODELS_DIR`, Ollama (port fermé) et la clé Gemini **avant tout import de `src`** : aucun test, ni singleton créé à l'import, ne peut atteindre les données réelles ou un modèle. `pytest_sessionstart` arrête la suite si la configuration pointe malgré tout vers `Vault_Data`.
   - Suites v0.1.2, v0.1.3 et v0.1.4 réécrites sur des données synthétiques (export Takeout HTML généré, fiches créées par le test) avec des invariants relatifs à la place des volumes personnels (392 fiches, 480 sessions, 73 153 empreintes, 6 649 messages). v0.1.3 ne dépend plus de deux fiches précises du coffre réel (F3).
   - Corrigé au passage : nom `Optional` non défini dans le test v0.2.0, et retrait par le Vault Doctor des empreintes corrélées présentes dans le bloc de télémétrie (pas seulement dans le corps), révélé par la réécriture de v0.1.2.
   - Le test v0.3.0 de dérive média est aligné sur la spec (tunnel de production préalable).

### 1.3 Fichiers modifiés
`src/__init__.py`, `src/config.py`, `src/utils/lifecycle.py` (nouveau), `src/utils/episodic_journal.py` (nouveau), `src/utils/atomic_io.py` (nouveau), `src/utils/markdown_io.py`, `src/daemons/hippocampus_hotkey.py`, `src/daemons/telemetry_daemon.py`, `src/daemons/git_ide_probe.py`, `src/consolidators/night_consolidator.py`, `src/consolidators/kanban_engine.py`, `src/consolidators/vault_doctor.py`, `src/ingestors/takeout_ingestor.py`, `run_exocortex.py`, `start_exocortex.bat`, `stop_exocortex.bat`, `start_web_center.bat`, `src/web_gui/index.html`, `tests/conftest.py`, `tests/test_v012_verification.py`, `tests/test_v013_verification.py`, `tests/test_v014_verification.py`, `tests/test_v020_kanban_verification.py`, `tests/test_v030_proactivity_verification.py`, `tests/test_v056_daemons_robustness_verification.py` (nouveau).

## 2. VÉRIFICATION

Suite `tests/test_v056_daemons_robustness_verification.py` (13 tests) : hermétisme de la session (F1) et absence de volumes personnels dans les suites v0.1.x (F3) ; raccourci par défaut (E1) ; callback rendu en moins de 100 ms pendant un traitement de 5 s, seconde activation ignorée (E2) ; dérive média refusée sans tunnel préalable, levée après 45 min de production (E3) ; démon arrêté par le signal avec sauvegarde de la fenêtre en cours, signal résiduel ignoré au démarrage, script sans `wmic` (E4) ; workspace exact, index VS Code, `cwd` réservé aux terminaux (E5) ; journaux partagés cold start + nuit, date cold start consolidée, réingestion sans effet sur la télémétrie, conversion d'un journal hérité (A10) ; écriture interrompue sans perte ni fichier temporaire résiduel (G6) ; lanceurs sur le Command Center (G3).

Résultats : **148 passed, 1 skipped** avec un simple `python -m pytest tests`, sans redirection manuelle de l'environnement. **Les 5 échecs historiques de v0.1.2–v0.1.4 ont disparu.** Vérifié après le run : aucun fichier de `Vault_Data/` modifié.

L'arrêt réel (`--stop`) n'a pas été exécuté sur la machine pendant le développement (il aurait arrêté les processus Exocortex en cours) ; il est couvert par les tests unitaires.

## 3. POINTS D'ATTENTION
- **Nouveau raccourci de l'injecteur : Ctrl+Alt+Espace.** Pour revenir à l'ancien : `HIPPOCAMPUS_HOTKEY=<alt>+<space>` dans `.env`.
- `start_exocortex.bat` ouvre désormais `http://127.0.0.1:8500` au lieu du dashboard Streamlit (`python run_exocortex.py --dashboard` pour ce dernier).
- Les journaux existants sont convertis au format à sections à leur prochaine réécriture.
- Pour lancer la suite contre un Ollama réel (tests manuels), définir `EXOCORTEX_TEST_OLLAMA_URL`.
