# CHANGELOG & SPÉCIFICATIONS D'ARCHITECTURE — v0.1.3 (Multi-Pass VRAM Queue, Préservation du Thinking & Déduplication SQLite)

**Date :** 21 Octobre 2026  
**Version cible :** `v0.1.3`  
**Références parentes :** `tech specs/CHANGELOG_V0.1.2_QOL.md`, `log-takeout-post-qol_2.md`, `allies_2.md`

---

## 1. DIAGNOSTIC TECHNIQUE POST-RUN v0.1.2

L'analyse des logs d'exécution de la v0.1.2 (`log-takeout-post-qol_2.md`) et des notes générées (`allies_2.md`) a permis de valider la qualité d'assainissement (427/480 sessions désormais validées au standard SOTA), tout en mettant en évidence **4 anomalies mécaniques** sur les 53 sessions restantes :

1. **Ping-Pong VRAM & Fuite Fantôme lors des Retries Unitaires (`00:20:47`) :**
   - Dans la v0.1.2, lorsqu'une session échouait aux Essais 1 et 2 sur `gemma4:26b-a4b`, le client déchargeait immédiatement le 26B (14 Go), chargeait `gemma4:12b` (7,2 Go) pour une seule session, puis rechargeait le 26B à la session suivante (14 cycles complets SSD <-> VRAM).
   - À `00:20:47`, une erreur HTTP 500 sur `gemma4:12b` lors de l'Essai 3 a interrompu le flux avant le déchargement du 12B, laissant `6.58 Go` de VRAM libre. Les 49 sessions suivantes ont alors été rejetées instantanément en cascade par la sonde VRAM (`6.58 Go < 8.0 Go`).
2. **Conflit entre le Mode *Thinking* de Gemma 4 et le plafond `num_predict: 2500` :**
   - Les erreurs `Expecting value: line 1 column 1 (char 0)` surviennent lorsque le bloc de réflexion interne (`<|thought|>`) consomme l'intégralité des 2500 tokens alloués ou entre en conflit avec la grammaire GBNF avant d'émettre l'accolade `{`.
   - Les erreurs `Unterminated string starting at: line 7 column 32 (char 450)` et les deux fins de phrases coupées dans `allies_2.md` surviennent lorsque `num_predict: 2500` coupe la génération au milieu du champ `synthesized_markdown_body`.
3. **Réécriture aveugle d'une Fiche Réussie par une Fiche `#A_Trier` :**
   - Lors du second run (`00:29`), certaines sessions qui avaient pourtant réussi au premier run (mais dont le fichier `.md` avait été considéré à tort comme incomplet ou retraité) ou qui ont échoué à cause du blocage VRAM ont vu leur fiche écrasée par un placeholder `#A_Trier`. Une règle d'or doit être appliquée : **un fichier déjà distillé avec succès ne doit jamais pouvoir être écrasé par un fallback `#A_Trier`**.
4. **Accumulation de Doublons dans `historical_footprints` et `chat_sessions` :**
   - `historical_footprints` est passé de `73 154` à `146 308` entrées et `chat_sessions` de `480` à `1 021` (car les 541 `noise_sessions` ont été insérées dans `chat_sessions` lors du run suivant), faussant le Burst Clustering (`4 410` -> `7 031` -> `9 089` clusters).

---

## 2. SPÉCIFICATIONS TECHNIQUES DES 5 CHANTIERS (v0.1.3)

### Chantier 1 : Architecture de Distillation par Files d'Attente Séquentielles (3 Vagues Batch — Zéro Ping-Pong VRAM)

Dans `src/ingestors/takeout_ingestor.py` (`initialize_meta_and_concepts`) et `src/llm/ollama_client.py` :
1. **Suppression du changement de modèle inline dans `generate_structured()` :**
   - `generate_structured()` ne doit **jamais** basculer tout seul de `26b` vers `12b` au milieu d'une boucle. Il exécute uniquement la requête sur le modèle explicitement demandé pour la vague en cours.
2. **Orchestration en 3 Vagues Séquentielles (`Multi-Pass Queue`) dans `takeout_ingestor.py` :**
   - **Vague 1 — Modèle `gemma4:26b-a4b` (Verrouillé en VRAM, Prompt Complet, Thinking ACTIF, `num_predict=8192`) :**
     - On vérifie la VRAM **une seule fois** au début de la Vague 1 (et si `free_vram < 8.0 Go`, on appelle d'abord `llm_client.unload_all_models()` pour purger tout modèle fantôme d'Ollama avant de revérifier !).
     - On itère sur `vague1_queue`. Si une session réussit -> écriture immédiate de la fiche `.md` et mise à jour SQLite (`distillation_status="success"`).
     - Si une session échoue -> **aucun retry immédiat**, on l'ajoute simplement à `vague2_queue` et on passe à la session suivante en gardant le 26B chaud en VRAM.
   - **Vague 2 — Modèle `gemma4:26b-a4b` (Toujours en VRAM, Prompt Condensé `6000 chars`, Thinking DÉSACTIVÉ `think=False`, `num_predict=4096`) :**
     - Si `vague2_queue` n'est pas vide, on traite toutes les sessions de `vague2_queue` sur le 26B déjà chargé, mais avec `think=False` et un prompt condensé + consigne stricte de concision (300-450 mots max).
     - Si une session échoue encore -> ajout dans `vague3_queue`.
     - À la fin de la Vague 2 -> **déchargement unique** de `gemma4:26b-a4b`.
   - **Vague 3 — Modèle `gemma4:12b` (Chargé une seule fois en VRAM, `think=False`, `num_predict=4096`) :**
     - Si `vague3_queue` n'est pas vide, on charge `gemma4:12b` une seule fois et on traite le reliquat.
     - Seules les sessions qui échouent à l'issue de la Vague 3 sont placées en quarantaine `#A_Trier` (`distillation_status="failed_fallback"`).
     - À la fin de la Vague 3 -> **déchargement unique** de `gemma4:12b`.

---

### Chantier 2 : Préservation du Mode *Thinking* en Vague 1 + Réparation Chirurgicale JSON (`ollama_client.py`)

Dans `src/llm/ollama_client.py` :
1. **Paramètres du `Modelfile` et d'inférence :**
   - Configurer `PARAMETER num_ctx 16384` dans `ensure_local_gguf_models()`.
   - Ajouter le paramètre `enable_thinking: bool = True` et `num_predict: int = 8192` à `generate_structured()`.
   - Lorsque `enable_thinking=False` (Vagues 2 et 3), passer `"think": False` dans le payload JSON d'Ollama `/api/chat` (et ajouter `/no_think` ou la consigne de réponse directe dans le system prompt).
2. **Nettoyage des balises `<|thought|>` et Auto-Réparation des Chaînes Tronquées (`repair_truncated_json`) :**
   - Avant `json.loads()`, supprimer tout bloc `<|thought|>...<|/thought|>` ou `<think>...</think>` éventuellement présent en tête de `raw_content`.
   - Créer une fonction `repair_truncated_json(raw_json: str) -> Optional[str]` :
     - Si `raw_json` commence bien par `{` et contient `"synthesized_markdown_body": "` mais s'arrête brutalement sans fermer la chaîne ni l'objet JSON (erreur `Unterminated string starting at: line 7`), couper proprement à la dernière fin de phrase valide (`.`, `\n`) de `synthesized_markdown_body`, refermer les guillemets et compléter avec `", "related_concepts": []}`.
     - Tester également dans le prompt de distillation l'exigence explicite : *"Le champ synthesized_markdown_body doit être synthétique, dense et complet (entre 250 et 450 mots maximum, ne jamais laisser une phrase inachevée)."*

---

### Chantier 3 : Purge Préventive des Modèles Fantômes en VRAM (`unload_all_known_models`)

Dans `src/llm/ollama_client.py` :
1. Créer la méthode `force_clear_vram(self) -> float` qui :
   - Interroge `GET http://localhost:11434/api/ps` pour lister tous les modèles actuellement chargés en VRAM par le démon Ollama (même si un script précédent a crashé).
   - Envoie `keep_alive: 0` sur chacun des modèles listés dans `/api/ps` (ainsi que sur `gemma4:26b-a4b`, `gemma4:12b` et `bge-m3`).
   - Attend `1.0s` et retourne `get_vram_free_gb()`.
2. Dans `check_and_select_model()`, si `free_vram < 8.0 Go`, appeler automatiquement `force_clear_vram()` une fois avant de déclarer que la VRAM est saturée par un jeu 3D ! Cela rend physiquement impossible le bug en cascade de `00:20:47`.

---

### Chantier 4 : Déduplication SQLite (`historical_footprints` & `chat_sessions`)

Dans `src/database/db_manager.py` et `src/ingestors/takeout_ingestor.py` :
1. **Déduplication de `historical_footprints` :**
   - Dans `init_db()`, supprimer les doublons existants dans `historical_footprints` via :
     ```sql
     DELETE FROM historical_footprints
     WHERE id NOT IN (
         SELECT MIN(id) FROM historical_footprints
         GROUP BY source, timestamp, title_or_query
     );
     CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_footprint
     ON historical_footprints(source, timestamp, title_or_query);
     ```
   - Remplacer `INSERT INTO historical_footprints` par `INSERT OR IGNORE INTO historical_footprints` dans `insert_historical_footprints_batch()`.
2. **Nettoyage de `chat_sessions` :**
   - Ne stocker dans `chat_sessions` que les **480 sessions qualifiées** (ou marquer explicitement `distillation_status = 'micro_noise'` pour les 541 micro-sessions et les exclure du comptage des sessions à distiller).
   - Dans `scan_and_upgrade_existing_concepts()`, reconstruire `completed_session_ids` **uniquement** à partir des fichiers `.md` réellement présents et valides sur le disque dans `02_Concepts/` (+ les sessions marquées `llm_noise`), afin qu'une session dont le fichier `.md` est en `#A_Trier` ne soit jamais sautée par erreur.
   - **Protection anti-écrasement :** Si un fichier valide existe déjà pour un `session_id`, interdire formellement de le remplacer par une fiche `#A_Trier`.

---

### Chantier 5 : Réparation des 2 Notes Tronquées de la v0.1.2

Dans `scan_and_upgrade_existing_concepts()` :
- Ajouter une vérification de fin de texte sur les notes existantes : si le corps Markdown juste avant `> [!abstract]-` se termine par un mot de liaison suspendu (ex: `"pour assimiler la structure"`, `"pour s'assurer que le"`, ou absence de ponctuation finale `.`, `)`, `*`, `` ` ``, `|`, `>`), marquer automatiquement cette fiche comme `incomplete_truncated` (la purger) pour qu'elle soit régénérée proprement en Vague 1 avec `num_predict=8192` !