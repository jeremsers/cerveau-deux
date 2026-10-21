# CHANGELOG & SPÉCIFICATIONS D'ARCHITECTURE — v0.1.2 (QoL, Delta Engine & Taxonomie Stricte)

**Date :** 20 Octobre 2026
**Version cible :** `v0.1.2` (Idempotence & Rattrapage Delta, Grammaire JSON GBNF, Taxonomie à 2 Niveaux, Granularité SQLite `chat_messages`, Cold Start Épisodique, Registre `Misc` & Télémétrie CLI `tqdm`)
**Références parentes :** `tech specs/CHANGELOG_V0.1.1.md`, `qol 0.1.2.md`

---

## 1. DIAGNOSTIC POST-RUN COMPLET (480 SESSIONS — v0.1.1)

L'exécution intégrale du pipeline d'ingestion sur les archives Google Takeout (6 649 tours Gemini, 44 896 vidéos YouTube, 28 258 requêtes Search) a généré **479 fiches conceptuelles** en 3h53. L'inspection du corpus généré (`all_2.md`) et des logs (`log-takeout_2.md`) a révélé **10 axes d'amélioration architecturale et de Qualité de Vie (QoL)** :

1. **Absence d'Idempotence et de Mode Delta (Reprise / Nouveau Takeout) :** Relancer `--ingest-takeout` écrase et recalcule les 480 sessions depuis zéro (~4h de GPU). Le système doit détecter les sessions déjà distillées avec succès pour ne traiter que le delta.
2. **Détection et Rattrapage des 87 "Faux Succès" (Fallback Heuristique) :** Lorsqu'une erreur JSON ou HTTP 500 survient, le fallback de la v0.1.1 générait une fiche dégradée (portant les signatures `"takeout_coldstart"` dans `tags` et `### Problématique & Contexte` / `- Session composée de` dans le corps) ET lui assignait parfois un tag valide par mots-clés (ex: `#Chefferie_Projet_et_UX`), polluant les vraies catégories au lieu de l'isoler dans `#A_Trier`.
3. **Échecs de Parsing JSON (~18% des sessions) & Erreurs HTTP 500 Ollama :**
   - `ollama_client.py` passait `"format": "json"` au lieu du schéma JSON Pydantic complet `"format": response_model.model_json_schema()`, privant `llama.cpp` du décodage contraint par grammaire GBNF (causant des `Field required: related_concepts` ou `Unterminated string`).
   - Les sessions très longues ou multi-sujets provoquaient des erreurs `500 Internal Server Error` sur Ollama faute de mécanisme de _retry_ avec réduction adaptative de la fenêtre de texte.
4. **Inflation Taxonomique incontrôlée (+90 `semantic_topic` créés) :** La création libre de `semantic_topic` a généré des dizaines de doublons quasi-synonymes (`Marketing_Conversion_et_Ads`, `Marketing_Digital_et_Strategie`, `Marketing_Performance_et_Data`, etc.), fragmentant les statistiques du Dashboard.
5. **Pollution des Fiches Concepts par YouTube & Google Search :** La jointure temporelle `[-60 min ; +30 min]` injecte des vidéos YouTube et recherches Google totalement hors-sujet dans le bloc `> [!abstract]-` des fiches conceptuelles. Ces données doivent être strictement réservées au Dashboard analytique (Module 6).
6. **Perte des Sessions jugées comme "Bruit" (< 3 tours ou `is_worth_indexing=False`) :** Les 541 micro-sessions filtrées et les sessions rejetées par le LLM disparaissaient sans laisser de trace consultable dans le coffre.
7. **Absence de Granularité des Messages en Base (`chat_messages`) :** Seul le résumé de session était stocké dans SQLite ; le contenu exact tour par tour n'était pas persisté dans `telemetry.db`.
8. **Absence de Cold Start sur les Journaux Épisodiques (`01_Episodique/`) :** Le dossier `01_Episodique/` et la table `daily_metrics` restaient vides après l'ingestion Takeout au lieu de reconstituer l'historique quotidien à partir des sessions passées.
9. **Exécution à l'aveugle dans le Terminal :** Absence de barre de progression temps réel (`X/480 | % | ETA | Succès | Fallback | Skipped`) lors des opérations longues.

---

## 2. SPÉCIFICATIONS TECHNIQUES DES 10 CORRECTIFS (v0.1.2)

### Correctif 1 : Taxonomie Stricte à 2 Niveaux (15 Macro-Catégories Fermées + `tags` Granulaires Libres)

Dans `src/config.py`, `src/llm/prompts.py`, `src/ingestors/takeout_ingestor.py` et `src/consolidators/night_consolidator.py` :

1. **Niveau 1 — `semantic_topic` (Liste Fermée Canonique de 16 Macro-Catégories) :**
   Il est désormais **strictement interdit** de créer de nouveaux `semantic_topic` à la volée. Toute activité ou fiche conceptuelle doit appartenir à l'une de ces **16 catégories maîtresses** :
   - `IA_et_LLM_Local` : Architectures RAG, modèles locaux, quantification GGUF, VRAM, agents IA, prompt engineering.
   - `Dev_et_Architecture_Tech` : Développement web (Astro, React, TS), backend, API, scripts Python, bases de données, cloud, CSS/A11y.
   - `HomeLab_et_Hardware` : Serveurs domestiques (Plex, Riven, Debrid, Docker), réseau/DNS, montage/dépannage PC, périphériques et consoles handheld.
   - `Chefferie_Projet_et_Produit` : Gestion de projet digital, Product Ownership, cadrage MVP, UX/UI design, soutenances, méthodologie agile.
   - `Marketing_et_Acquisition` : Google Ads, GA4, GTM, SEO/SEA, tunnels de vente, copywriting, Stripe/Make/Brevo, CRO.
   - `Freelance_et_Carriere` : Positionnement freelance, tarification, formations (OpenClassrooms, France Travail), stratégie professionnelle.
   - `Admin_Finance_et_Droit` : Démarches MDPH/AAH/RSDAE, droit français/suisse, fiscalité, immobilier, gestion patrimoniale, litiges.
   - `Introspection_et_Neuroatypie` : Fonctionnement HPI/TSA/TDAH/AuDHD, masking, monotropisme, bilans cliniques (ADOS-2, EMA, CRA), métacognition.
   - `Sante_et_Pharmacologie` : Suivi médical, dentaire, sommeil/apnée, pharmacologie, vaporisation, gestion de la tolérance et réduction des risques.
   - `Nutrition_et_Cuisine` : Volume eating, batch cooking, science culinaire, cuiseurs à riz, Ninja Creami, glycémie et équipements de cuisine.
   - `Philo_et_Epistemologie` : Absurdisme (Camus), spinozisme, épistémologie, éthique, logique formelle, métaphysique et physique théorique.
   - `Sociologie_et_Geopolitique` : Analyse systémique des sociétés, économie politique, géopolitique, mouvements sociaux, démographie et débats idéologiques.
   - `Gaming_et_GameDesign` : Jeux solo, RPG, modding, émulation, analyse de game design, jeux incrémentaux et jeux de plateau/JDR.
   - `MMORPG_et_Esport` : World of Warcraft (Mythic+, raid, guildes), Guild Wars 2, League of Legends, TFT, theorycrafting et scène esport.
   - `Musique_MAO_et_Culture_Pop` : Production musicale (Maschine, Ableton, VST), Suno AI, K-Pop, rap, webtoons, mangas, animes, séries et linguistique web.
   - `A_Trier` : Catégorie de quarantaine exclusivement réservée aux échecs techniques de distillation en attente de retraitement.

2. **Niveau 2 — `tags` (Granularité Fine & Émergente) :**
   Le champ `tags: List[str]` (3 à 6 tags en `kebab-case`) porte toute la précision granulaire (ex: `["riven", "jellyseerr", "plex-watchlist", "docker"]`).
3. **Remapping Automatique de l'Existant :**
   Fournir une table de correspondance déterministe `LEGACY_TOPIC_MAPPING` dans `takeout_ingestor.py` qui convertit automatiquement les ~90 anciens topics générés en v0.1.1 vers l'une des 15 catégories maîtresses tout en déplaçant l'ancien topic granulaire dans la liste `tags` de la note !

---

### Correctif 2 : Décodage JSON Contraint par Schéma (GBNF Ollama) & Retry Anti-Erreur 500

Dans `src/llm/ollama_client.py` (`generate_structured`) :

1. **Grammaire JSON Schema native :** Au lieu de `"format": "json"`, passer directement `"format": response_model.model_json_schema()` dans le payload `/api/chat` d'Ollama. Cela force le moteur C++ `llama.cpp` d'Ollama à contraindre chaque token généré selon le schéma exact de `DistilledConceptSchema` (impossible d'omettre `synthesized_markdown_body` ou `related_concepts`, et impossible de laisser une chaîne non fermée).
2. **Options de contexte et de prédiction :** Passer `"options": {"temperature": 0.1, "num_ctx": 12288, "num_predict": 2500}` pour éviter toute troncature de sortie JSON ou dépassement de contexte.
3. **Mécanisme de Retry Adaptatif (Anti-500 & Anti-ValidationError) :**
   Si l'appel à Ollama échoue (HTTP 500 ou `ValidationError`/`JSONDecodeError`), effectuer automatiquement une **seconde tentative (Retry 1)** après `time.sleep(1.5)` en réduisant la taille du prompt de 40 % (troncature centrale ou finale propre) et en passant sur `temperature: 0.2`. Si le Retry 1 sur le 26B échoue encore sur une erreur 500, tenter un **Retry 2 sur `settings.MODEL_FAST_VISION` (`gemma4:12b`)** avant d'abandonner en fallback !

---

### Correctif 3 : Moteur Delta, Détection des 87 "Faux Succès" & Quarantaine Stricte `#A_Trier`

Dans `src/ingestors/takeout_ingestor.py` :

1. **Nouveaux champs dans le Frontmatter YAML des fiches `02_Concepts/` :**
   Ajouter systématiquement dans le YAML de chaque note :
   ```yaml
   session_id: "6741935c6956aa2c"
   distillation_status: "success" # ou "failed_fallback"
   ```

2. Scanner d'État et d'Assainissement Pré-Ingestion (scan_and_sanitize_existing_concepts) :
Avant de lancer la boucle LLM dans initialize_meta_and_concepts() :Parcourir tous les fichiers Vault_Data/02_Concepts/*.md.Extraire le session_id (soit depuis la clé YAML session_id:, soit par regex sur Session Gemini \([^`]+)`` dans le callout final).Détecter si le fichier est un "Faux Succès" (Fallback v0.1.1) via ces 4 critères :"takeout_coldstart" est présent dans la ligne tags: ;OU ### Problématique & Contexte et - Session composée de sont présents dans le corps de la note ;OU semantic_topic == "A_Trier" ;OU distillation_status == "failed_fallback".Action si FAILED_FALLBACK (les ~87 fichiers de ton run précédent) :Supprimer physiquement l'ancien fichier .md mal nommé du disque (cf.unlink()) et supprimer son entrée dans LanceDB.Ne PAS ajouter son session_id à l'ensemble completed_session_ids $\rightarrow$ il sera automatiquement re-distillé par le LLM lors de cette passe !Action si SUCCESS (les ~392 fichiers déjà réussis) :Ajouter son session_id à completed_session_ids $\rightarrow$ le LLM ne sera PAS rappelé dessus (skip instantané).Assainir le fichier sur place (In-Place Upgrade en < 1 ms par fichier) :Supprimer tout bloc > - **Requêtes et vidéos corrélées :** et les lignes >   - [youtube]... / >   - [google_search]... associées.Si son semantic_topic n'est pas dans les 15 catégories fermées, le remapper via LEGACY_TOPIC_MAPPING et ajouter l'ancien topic en minuscule dans tags: [...].Ajouter session_id: "..." et distillation_status: "success" dans son YAML s'ils sont absents.Mettre à jour SQLite (update_session_distillation_metadata).

3. Quarantaine Stricte en cas d'Échec Total :
Si, malgré les retries (26B puis 12B), une session échoue encore à la distillation LLM, le bloc de secours (if not distilled:) doit obligatoirement forcer :

    semantic_topic = "A_Trier" (suppression totale de la devinette par mots-clés qui polluait les autres catégories) ;

    distillation_status = "failed_fallback" dans le YAML ;

    slug = f"a-trier-{sess.session_id.lower()}".

### Correctif 4 : Suppression de YouTube/Search dans les Fiches Concepts

Dans src/ingestors/takeout_ingestor.py :

    Supprimer définitivement la génération et l'insertion de footprints_md (Requêtes et vidéos corrélées) dans le callout > [!abstract]- Généalogie & Télémétrie des notes 02_Concepts/.

    Conserver l'ingestion de YouTube et Google Search dans la table SQLite historical_footprints exclusivement pour les statistiques du Dashboard Streamlit (src/dashboard/app.py).

### Correctif 5 : Registre Consolidé du Bruit & Micro-Sessions (00_Meta/00_MISC_ET_BRUIT_ARCHIVE.md)

Pour garantir zéro perte d'information sur les sessions écartées :

    Sessions courtes (< 3 tours ou < 250 caractères) :
    Dans sessionize_gemini_turns(), au lieu de détruire silencieusement les sous-sessions qui sont sous le seuil (filtered_out_noise), les conserver dans une liste séparée noise_sessions: List[ReconstructedSession] retournée par la fonction :  Tuple[List[ReconstructedSession], List[ReconstructedSession]].

    Sessions rejetées par le LLM (is_worth_indexing == False) :
    Lorsqu'une session qualifiée est jugée triviale par le LLM (not distilled.is_worth_indexing), l'ajouter également à la liste des éléments misc (et marquer son statut distillation_status = "misc_noise" dans SQLite chat_sessions pour ne plus jamais la re-soumettre au LLM aux runs suivants !).

    Compilation du document unique Vault_Data/00_Meta/00_MISC_ET_BRUIT_ARCHIVE.md :
    Générer (et mettre à jour de façon idempotente) ce fichier Markdown structuré par ordre antéchronologique, listant sur une seule ligne dense par session :
    - **[YYYY-MM-DD HH:MM]** (\session_id` | X tours | Y chars | Statut: Micro-session ou Trivial LLM) : Prompt initial : "..." →  Aperçu réponse : "..."`

### Correctif 6 : Granularité Totale du Takeout en Base SQLite (Table chat_messages)

Dans src/database/db_manager.py et src/ingestors/takeout_ingestor.py :

    Créer une nouvelle table SQLite chat_messages dans init_db() :

    ```sql

    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        turn_index INTEGER NOT NULL,
        timestamp DATETIME NOT NULL,
        user_prompt TEXT NOT NULL,
        ai_response TEXT NOT NULL,
        user_char_count INTEGER NOT NULL,
        UNIQUE(session_id, turn_index)
    );
    CREATE INDEX IF NOT EXISTS idx_msg_session ON chat_messages(session_id);

```
2.Ajouter une colonne distillation_status TEXT DEFAULT 'pending' dans la table chat_sessions (via migration ALTER TABLE automatique si absente).
3. Lors de TakeoutIngestor.run(), insérer par lots (INSERT OR REPLACE INTO chat_messages) l'intégralité des échanges découpés par session (y compris les micro-sessions), permettant de requêter ou ré-analyser n'importe quelle conversation depuis SQLite sans jamais relire les fichiers HTML bruts.

### Correctif 7 : Cold Start Épisodique Rétroactif (01_Episodique/YYYY-MM-DD.md & daily_metrics)

Dans src/ingestors/takeout_ingestor.py :
Ajouter une fonction generate_cold_start_episodic_journals(sessions, db) appelée à la fin de l'ingestion Takeout :

    Regrouper toutes les sessions Gemini par date (YYYY-MM-DD).

    Pour chaque date historique possédant au moins une session Gemini :

        Calculer le temps total investi ce jour-là (somme des compute_realistic_session_duration_min), le tunnel d'hyperfocus maximal, les topics abordés (depuis chat_sessions.extracted_topics_json) et les fiches conceptuelles créées ce jour-là ([[Titre ou Slug]]).

        Si daily_metrics n'a pas encore d'entrée d'activité OS (total_screen_sec == 0) pour cette date, insérer ce bilan historique dans daily_metrics.

        Si le fichier Vault_Data/01_Episodique/YYYY-MM-DD.md n'existe pas (ou est issu d'un précédent Cold Start), générer la note épisodique quotidienne structurée récapitulant les sessions Gemini du jour, les sujets explorés et les liens Obsidian vers les fiches 02_Concepts/ générées.

### Correctif 8 : Barres de Progression Temps Réel (tqdm) sur tous les Scripts

Dans src/ingestors/takeout_ingestor.py, src/consolidators/night_consolidator.py et src/database/vector_store.py :

    Utiliser tqdm pour afficher une barre de progression claire dans le terminal sur chaque boucle longue :

        Assainissement existant : Assainissement Notes Existantes: 100%|██████████| 479/479 [00:00<00:00]

        Distillation Takeout : Distillation Takeout:  42%|████▏     | 37/87 [18:20<24:15, 29.1s/sess, Réussis=35, Misc=1, A_Trier=1, Skip_Delta=393]

        Indexation Vectorielle LanceDB : Indexation LanceDB (bge-m3): 100%|██████████| 479/479 [00:28<00:00, 16.8note/s]

        Consolidation Nocturne (Passes 1 & 2) : Barre de progression sur les captures .webp, les signatures de fenêtres et les journaux épisodiques.

    Remplacer logger.info par tqdm.write à l'intérieur des boucles tqdm (ou désactiver le bruit de log par fichier dans vector_store.py) pour que la barre de progression reste propre en bas de l'écran sans être cassée par des centaines de lignes de log.

3. CRITÈRES D'ACCEPTATION (DEFINITION OF DONE v0.1.2)

    [ ] Relancer python run_exocortex.py --ingest-takeout détecte automatiquement les ~392 fiches déjà réussies (Skip_Delta), les assainit sur place (retrait YouTube/Search + remapping vers les 15 catégories fermées) sans rappeler le LLM dessus.

    [ ] Les ~87 fiches qui avaient échoué au run précédent (détectées via "takeout_coldstart", ### Problématique & Contexte ou #A_Trier) sont automatiquement purgées et re-distillées par gemma4:26b-a4b avec le nouveau décodage JSON Schema strict (format: response_model.model_json_schema()) et le retry anti-500.

    [ ] Plus aucun tag semantic_topic hors de la liste fermée des 16 catégories n'existe dans Taxonomie_Tags.md ni dans 02_Concepts/*.md.

    [ ] Plus aucune vidéo YouTube ou recherche Google n'apparaît dans les fichiers 02_Concepts/*.md.

    [ ] Le fichier Vault_Data/00_Meta/00_MISC_ET_BRUIT_ARCHIVE.md compile proprement toutes les micro-sessions et sessions rejetées par le LLM, ligne par ligne.

    [ ] La table chat_messages dans telemetry.db contient les 6 649 tours de conversation, et Vault_Data/01_Episodique/ contient les journaux quotidiens rétroactifs générés depuis l'historique Gemini.

    [ ] Toutes les opérations affichent une barre de progression tqdm claire avec compteurs en direct.
```
