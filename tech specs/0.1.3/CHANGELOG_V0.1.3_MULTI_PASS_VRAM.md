# CHANGELOG & RAPPORT D'INGÉNIERIE SYSTÈME — v0.1.3

**Date :** 21 Octobre 2026  
**Version :** `v0.1.3` (Multi-Pass VRAM Queue, Préservation du Thinking, Auto-Heal JSON & Déduplication SQLite)  
**Plateforme & Matériel :** Windows 11 Pro, NVIDIA GeForce RTX 4070 Ti Super (16 Go VRAM)  
**Références :** `tech specs/changelog-v1.0.3.md`, `log-takeout-post-qol_2.md`, `allies_2.md`

---

## 1. Synthèse Exécutive des Problèmes Traités

L'analyse approfondie du run de production v0.1.2 (`log-takeout-post-qol_2.md`) et des fiches générées a mis en lumière 4 dysfonctionnements critiques :

1. **Thrashing VRAM / Ping-Pong Inutile (00:20:47) :**  
   Lorsqu'une session échouait sur `gemma4:26b-a4b`, `generate_structured` déchargeait immédiatement le modèle 26B (14 Go), chargeait `gemma4:12b` (7,2 Go) pour une tentative unitaire, puis rechargeait le 26B à la session suivante. À `00:20:47`, un crash HTTP 500 sur le 12B a laissé le modèle en VRAM (6,58 Go libres < seuil de 8,0 Go), provoquant le rejet immédiat en cascade des 49 dernières sessions en 3 secondes.
2. **Conflit entre Mode Thinking (`<|thought|>`) et Plafond `num_predict: 2500` :**  
   Les tokens de raisonnement interne de Gemma 4 combinés au corps Markdown saturaient le quota de 2500 tokens, générant des erreurs `Unterminated string` et coupant des phrases au milieu (notamment dans `neuroplasticite-acquisition-langues-complexes-adulte.md` et `optimisation-cpu-affinite-p-e-cores-smt.md`).
3. **Écrasement d'une Note Valide par un Fallback `#A_Trier` :**  
   Lors de re-runs partiels, une session déjà distillée avec succès risquait d'être écrasée par une note de quarantaine suite à un incident de sonde VRAM.
4. **Inflation et Doublons SQLite :**  
   La table `historical_footprints` accumulait des doublons à chaque exécution (passant de 73 154 à 146 308 puis 219 462 entrées), et `chat_sessions` contenait 541 micro-sessions bruitées.

---

## 2. Détail des 5 Chantiers Déployés

### Chantier 1 : Architecture de Distillation par File d'Attente Séquentielle (3 Vagues Batch)
- **Suppression du changement de modèle inline :**  
  Dans `src/llm/ollama_client.py`, `generate_structured` n'effectue plus aucune bascule de modèle à chaud lorsque `allow_model_switch_fallback=False`.
- **Orchestration en 3 Vagues Séquentielles dans `src/ingestors/takeout_ingestor.py` (`initialize_meta_and_concepts`) :**
  - **Vague 1 (`gemma4:26b-a4b`) :** Modèle verrouillé en VRAM, Thinking actif (`enable_thinking=True`), `num_predict=8192`, prompt complet (jusqu'à 20 000 caractères). Si échec, mise en file d'attente dans `vague2_queue` sans bascule immédiate.
  - **Vague 2 (`gemma4:26b-a4b`) :** Modèle conservé chaud en VRAM, Thinking désactivé (`think=False`), `num_predict=4096`, prompt condensé (6 000 caractères max) avec consigne stricte de concision (250-400 mots). Si échec, mise en file d'attente dans `vague3_queue`. Déchargement unique du 26B à la fin de la Vague 2.
  - **Vague 3 (`gemma4:12b`) :** Chargé une seule fois pour traiter le reliquat avec `think=False` et `num_predict=4096`. Seules les sessions échouant à l'issue de la Vague 3 sont placées en quarantaine `#A_Trier`. Déchargement unique du 12B en fin de passe.

### Chantier 2 : Préservation du Thinking & Auto-Heal JSON (`repair_truncated_json`)
- **Nettoyage des balises `<|thought|>` et `<think>` :**  
  Purge systématique des blocs de réflexion avant le parsing JSON.
- **Réparation chirurgicale des chaînes tronquées :**  
  Si le JSON est coupé dans `synthesized_markdown_body`, la fonction `repair_truncated_json` coupe proprement à la dernière ponctuation terminale valide (`.`, `!`, `?`, `\n`), referme les guillemets et complète avec `", "related_concepts": []}`.
- **Support natif `think: False` :**  
  Passage de `"think": False` dans le payload d'Ollama `/api/chat` en Vagues 2 et 3.
- **Contexte 16K :**  
  `PARAMETER num_ctx 16384` configuré dans le template `Modelfile` d'Ollama (`ensure_local_gguf_models`).

### Chantier 3 : Purge Préventive des Modèles Fantômes en VRAM (`force_clear_vram`)
- **Méthode `HybridLLMClient.force_clear_vram()` :**  
  Interroge `/api/ps` d'Ollama et décharge immédiatement tous les modèles résidents avec `keep_alive=0`.
- **Sonde `check_and_select_model()` durcie :**  
  Si la VRAM libre est inférieure au seuil strict de 8,0 Go, exécute automatiquement une purge active préventive avant de lever toute exception.
- **Intégration Consolidation Nocturne :**  
  Passe 1 et Passe 2 de `night_consolidator.py` appellent systématiquement `force_clear_vram()` avant inspection de la VRAM. Passe 1 utilise `enable_thinking=False, num_predict=2048`.

### Chantier 4 : Déduplication SQLite & Protection Anti-Écrasement
- **Index Unique et Déduplication native :**  
  Dans `init_db()`, exécution d'une requête de déduplication par `(source, timestamp, title_or_query)` et création de l'index unique `idx_unique_footprint`. Remplacement par `INSERT OR IGNORE` dans `insert_historical_footprints_batch()`. Le volume d'empreintes est assaini à 73 153 entrées uniques (28 257 Google Search + 44 896 YouTube).
- **Assainissement de `chat_sessions` :**  
  Suppression des micro-sessions (< 3 tours ou < 250 caractères) de `chat_sessions`. Exactement 480 sessions qualifiées sont conservées. Les 6 649 messages individuels restent intégralement préservés dans `chat_messages`.
- **Protection Anti-Écrasement dans `save_distilled_concept_note` :**  
  Interdiction formelle de remplacer une fiche existante valide par une fiche `#A_Trier`.

### Chantier 5 : Détection et Purge Chirurgicale des Notes Tronquées
- **Vérification de fin de texte dans `scan_and_upgrade_existing_concepts` :**  
  Détecte les notes dont le corps Markdown avant `> [!abstract]-` se termine par des fragments suspendus (ex: `"pour assimiler la structure"`, `"pour s'assurer que le"`, ou absence de ponctuation finale valide).
- **Résultat de la purge :**  
  54 notes dégradées ou tronquées ont été purgées du disque et de LanceDB (dont les deux fichiers identifiés dans `allies_2.md`), laissant 407 fiches valides avec 100% de conformité de ponctuation et de taxonomie.

---

## 3. Matrice de Validation Technique

| Composant | Test / Critère | Résultat v0.1.3 |
|---|---|---|
| `historical_footprints` | Déduplication exacte (73 153 lignes uniques, index unique) | **CONFORME (100%)** |
| `chat_sessions` | Exclusion des 541 micro-sessions (exactement 480 sessions) | **CONFORME (100%)** |
| `chat_messages` | Préservation fine de tous les tours d'échange (>= 6649 messages) | **CONFORME (100%)** |
| `repair_truncated_json` | Auto-réparation des balises `<|thought|>` et corps Markdown tronqués | **CONFORME (100%)** |
| `ollama_client.py` | Modelfile 16K, `enable_thinking=True`, `num_predict=8192`, `force_clear_vram` | **CONFORME (100%)** |
| `takeout_ingestor.py` | Multi-Pass VRAM Queue (3 vagues séquentielles, zéro ping-pong) | **CONFORME (100%)** |
| `save_distilled_concept_note` | Protection anti-écrasement des fiches valides par `#A_Trier` | **CONFORME (100%)** |
| `night_consolidator.py` | Purge VRAM préventive avant Passe 1 et 2, `enable_thinking=False` Passe 1 | **CONFORME (100%)** |
| `tests/test_v013_verification.py` | Validation automatisée end-to-end de tous les chantiers | **SUCCÈS TOTAL (Exit 0)** |

