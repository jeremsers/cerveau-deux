PS C:\Users\Jijax\projets\cerveau-deux> python run_exocortex.py --ingest-takeout
2026-10-21 01:26:43,316 [INFO] Exocortex.Launcher: === Lancement de l'Ingestion Google Takeout ===
2026-10-21 01:26:45,385 [INFO] Exocortex.VectorStore: Table vectorielle LanceDB 'concepts' chargée avec succès.
2026-10-21 01:26:45,451 [INFO] Exocortex.TakeoutIngestor: === LANCEMENT DU MODULE 1 (TAKEOUT INGESTOR) ===
2026-10-21 01:26:45,456 [INFO] Exocortex.TakeoutIngestor: Fichiers Takeout détectés : Gemini=2, YouTube=2, Search=1
2026-10-21 01:26:45,456 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique YouTube : historique-recherche-youtube.html
2026-10-21 01:26:45,491 [INFO] Exocortex.TakeoutIngestor: Extraction YouTube terminée : 0 empreintes trouvées.
2026-10-21 01:26:45,495 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique YouTube : historique-vues-youtube.html
2026-10-21 01:26:47,099 [INFO] Exocortex.TakeoutIngestor: Extraction YouTube terminée : 44896 empreintes trouvées.
2026-10-21 01:26:47,419 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique Google Search : historique-google-search.html
2026-10-21 01:26:48,637 [INFO] Exocortex.TakeoutIngestor: Extraction Google Search terminée : 28258 requêtes trouvées.
2026-10-21 01:26:48,831 [INFO] Exocortex.TakeoutIngestor: Lecture et parsing rapide du fichier HTML Gemini : gemini_gems_data.html
2026-10-21 01:26:48,835 [INFO] Exocortex.TakeoutIngestor: Nombre total de blocs détectés dans l'export : 0
2026-10-21 01:26:48,836 [INFO] Exocortex.TakeoutIngestor: Extraction terminée : 0 tours d'échange valides récupérés.
2026-10-21 01:26:48,836 [INFO] Exocortex.TakeoutIngestor: Lecture et parsing rapide du fichier HTML Gemini : historique-gemini.html
2026-10-21 01:26:49,076 [INFO] Exocortex.TakeoutIngestor: Nombre total de blocs détectés dans l'export : 7264
2026-10-21 01:26:50,708 [INFO] Exocortex.TakeoutIngestor: Extraction terminée : 6649 tours d'échange valides récupérés.
2026-10-21 01:26:50,728 [INFO] Exocortex.TakeoutIngestor: Démarrage de la sessionisation sur 6649 tours...
2026-10-21 01:26:50,749 [INFO] Exocortex.TakeoutIngestor: Sessionisation achevée : 480 sessions qualifiées retenues (541 micro-sessions bruitées archivées).
2026-10-21 01:26:51,263 [INFO] Exocortex.TakeoutIngestor: Table chat_messages synchronisée : 6649 messages insérés.
2026-10-21 01:26:51,281 [INFO] Exocortex.TakeoutIngestor: Exécution de la jointure temporelle Search/YouTube sur 480 sessions...
2026-10-21 01:26:51,852 [INFO] Exocortex.TakeoutIngestor: Jointure temporelle achevée : 0 empreintes rattachées aux sessions Gemini.
2026-10-21 01:26:51,852 [INFO] Exocortex.TakeoutIngestor: Recherche des tunnels d'exploration (Burst Clustering) hors sessions Gemini...
2026-10-21 01:26:52,956 [INFO] Exocortex.TakeoutIngestor: Burst Clustering terminé : 4410 clusters denses formés.
2026-10-21 01:26:52,968 [INFO] Exocortex.TakeoutIngestor: Génération des fichiers de staging dans : C:\Users\Jijax\projets\cerveau-deux\Vault_Data\_System_Buffer\takeout_staging
2026-10-21 01:26:53,006 [INFO] Exocortex.TakeoutIngestor: Fichier 00_USER_PROMPTS_ONLY.md écrit (5828 prompts au total).
2026-10-21 01:26:53,091 [INFO] Exocortex.TakeoutIngestor: 15 fichier(s) de lots complets généré(s).
2026-10-21 01:26:53,093 [INFO] Exocortex.TakeoutIngestor: Consignes web prêtes dans : PROMPT_A_COPIER_DANS_GEMINI_WEB.txt
2026-10-21 01:26:53,093 [INFO] Exocortex.TakeoutIngestor: Taxonomie maîtresse à 16 macro-catégories validée dans Taxonomie_Tags.md
2026-10-21 01:26:53,093 [INFO] Exocortex.TakeoutIngestor: Taxonomie maîtresse à 16 macro-catégories validée dans Taxonomie_Tags.md
2026-10-21 01:26:55,430 [INFO] Exocortex.TakeoutIngestor: Assainissement terminé : 0 fallbacks purgés, 407 fiches assainies sur place, 407 sessions complètes en mémoire.
2026-10-21 01:26:55,430 [INFO] Exocortex.TakeoutIngestor: Plan de distillation LLM : 73 sessions à traiter (407 déjà complétées ignorées via Mode Delta).
2026-10-21 01:26:56,004 [INFO] Exocortex.LLM: Modèle Ollama 'gemma4:12b' déjà disponible.
2026-10-21 01:26:56,004 [INFO] Exocortex.LLM: Modèle Ollama 'gemma4:26b-a4b' déjà disponible.
2026-10-21 01:26:56,016 [INFO] Exocortex.TakeoutIngestor: --- DÉMARRAGE VAGUE 1 : gemma4:26b-a4b (Thinking ACTIF, num_predict=8192) [73 sessions] ---
2026-10-21 01:26:56,045 [INFO] Exocortex.LLM: Modèle 'gemma4:26b-a4b' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-21 01:26:56,058 [INFO] Exocortex.LLM: Modèle 'bge-m3' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-21 01:26:56,072 [INFO] Exocortex.LLM: Modèle 'gemma4:12b' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-21 01:26:57,126 [INFO] Exocortex.LLM: VRAM GPU après purge active (force_clear_vram) : 14.42 Go libres
Distillation Vague 1 (26B Thinking):   0%|                                                                                                                     | 0/73 [00:00<?, ?sess/s]2026-10-21 01:26:57,202 [INFO] Exocortex.LLM: VRAM GPU : 14.42 Go libres / 15.99 Go totales
Distillation Vague 1 (26B Thinking): 100%|███████████████████████████████████████████████████████████████████████████████████████| 73/73 [39:21<00:00, 32.35s/sess, ok=72, v2_pending=0] 
2026-10-21 02:06:18,727 [INFO] Exocortex.LLM: Modèle 'gemma4:26b-a4b' déchargé avec succès de la VRAM (keep_alive=0).
Traceback (most recent call last):
  File "C:\Users\Jijax\projets\cerveau-deux\run_exocortex.py", line 223, in <module>
    main()
  File "C:\Users\Jijax\projets\cerveau-deux\run_exocortex.py", line 207, in main
    run_ingest_takeout(args.limit)
  File "C:\Users\Jijax\projets\cerveau-deux\run_exocortex.py", line 49, in run_ingest_takeout
    result = ingestor.run(max_distill_sessions=limit)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Jijax\projets\cerveau-deux\src\ingestors\takeout_ingestor.py", line 1684, in run
    initialize_meta_and_concepts(
  File "C:\Users\Jijax\projets\cerveau-deux\src\ingestors\takeout_ingestor.py", line 1490, in initialize_meta_and_concepts
    time.sleep(1.0)
    ^^^^
NameError: name 'time' is not defined
PS C:\Users\Jijax\projets\cerveau-deux> python run_exocortex.py --ingest-takeout
2026-10-21 02:08:11,562 [INFO] Exocortex.Launcher: === Lancement de l'Ingestion Google Takeout ===
2026-10-21 02:08:13,801 [INFO] Exocortex.VectorStore: Table vectorielle LanceDB 'concepts' chargée avec succès.
2026-10-21 02:08:14,168 [INFO] Exocortex.TakeoutIngestor: === LANCEMENT DU MODULE 1 (TAKEOUT INGESTOR) ===
2026-10-21 02:08:14,168 [INFO] Exocortex.TakeoutIngestor: Fichiers Takeout détectés : Gemini=2, YouTube=2, Search=1
2026-10-21 02:08:14,169 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique YouTube : historique-recherche-youtube.html
2026-10-21 02:08:14,203 [INFO] Exocortex.TakeoutIngestor: Extraction YouTube terminée : 0 empreintes trouvées.
2026-10-21 02:08:14,205 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique YouTube : historique-vues-youtube.html
2026-10-21 02:08:15,704 [INFO] Exocortex.TakeoutIngestor: Extraction YouTube terminée : 44896 empreintes trouvées.
2026-10-21 02:08:16,004 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique Google Search : historique-google-search.html
2026-10-21 02:08:17,123 [INFO] Exocortex.TakeoutIngestor: Extraction Google Search terminée : 28258 requêtes trouvées.
2026-10-21 02:08:17,308 [INFO] Exocortex.TakeoutIngestor: Lecture et parsing rapide du fichier HTML Gemini : gemini_gems_data.html
2026-10-21 02:08:17,308 [INFO] Exocortex.TakeoutIngestor: Nombre total de blocs détectés dans l'export : 0
2026-10-21 02:08:17,308 [INFO] Exocortex.TakeoutIngestor: Extraction terminée : 0 tours d'échange valides récupérés.
2026-10-21 02:08:17,308 [INFO] Exocortex.TakeoutIngestor: Lecture et parsing rapide du fichier HTML Gemini : historique-gemini.html
2026-10-21 02:08:17,527 [INFO] Exocortex.TakeoutIngestor: Nombre total de blocs détectés dans l'export : 7264
2026-10-21 02:08:18,971 [INFO] Exocortex.TakeoutIngestor: Extraction terminée : 6649 tours d'échange valides récupérés.
2026-10-21 02:08:18,991 [INFO] Exocortex.TakeoutIngestor: Démarrage de la sessionisation sur 6649 tours...
2026-10-21 02:08:19,006 [INFO] Exocortex.TakeoutIngestor: Sessionisation achevée : 480 sessions qualifiées retenues (541 micro-sessions bruitées archivées).
2026-10-21 02:08:19,530 [INFO] Exocortex.TakeoutIngestor: Table chat_messages synchronisée : 6649 messages insérés.
2026-10-21 02:08:19,545 [INFO] Exocortex.TakeoutIngestor: Exécution de la jointure temporelle Search/YouTube sur 480 sessions...
2026-10-21 02:08:20,123 [INFO] Exocortex.TakeoutIngestor: Jointure temporelle achevée : 0 empreintes rattachées aux sessions Gemini.
2026-10-21 02:08:20,123 [INFO] Exocortex.TakeoutIngestor: Recherche des tunnels d'exploration (Burst Clustering) hors sessions Gemini...
2026-10-21 02:08:21,268 [INFO] Exocortex.TakeoutIngestor: Burst Clustering terminé : 4410 clusters denses formés.
2026-10-21 02:08:21,283 [INFO] Exocortex.TakeoutIngestor: Génération des fichiers de staging dans : C:\Users\Jijax\projets\cerveau-deux\Vault_Data\_System_Buffer\takeout_staging
2026-10-21 02:08:21,316 [INFO] Exocortex.TakeoutIngestor: Fichier 00_USER_PROMPTS_ONLY.md écrit (5828 prompts au total).
2026-10-21 02:08:21,390 [INFO] Exocortex.TakeoutIngestor: 15 fichier(s) de lots complets généré(s).
2026-10-21 02:08:21,390 [INFO] Exocortex.TakeoutIngestor: Consignes web prêtes dans : PROMPT_A_COPIER_DANS_GEMINI_WEB.txt
2026-10-21 02:08:21,390 [INFO] Exocortex.TakeoutIngestor: Taxonomie maîtresse à 16 macro-catégories validée dans Taxonomie_Tags.md
2026-10-21 02:08:21,390 [INFO] Exocortex.TakeoutIngestor: Taxonomie maîtresse à 16 macro-catégories validée dans Taxonomie_Tags.md
Assainissement Notes Existantes:   9%|██████████                                                                                                    | 44/479 [00:00<00:03, 142.48note/s]2026-10-21 02:08:21,738 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : analyse-phishing-obfuscation-contournement-spf-dkim.md (dernière ligne : ' : Obfuscation 
et Contournement SPF/DKIM')
Assainissement Notes Existantes:  24%|██████████████████████████▌                                                                                  | 117/479 [00:01<00:02, 121.26note/s]2026-10-21 02:08:22,504 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : architecture-tunnel-conversion-tripwire-high-ticket.md (dernière ligne : ' Conversion : Du Tripwire au High-Ticket')
Assainissement Notes Existantes:  42%|█████████████████████████████████████████████▋                                                               | 201/479 [00:01<00:02, 130.19note/s]2026-10-21 02:08:23,152 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : emergence-topologie-espace-latent-llm.md (dernière ligne : 'opologie de l'Espace Latent dans les LLM')
Assainissement Notes Existantes:  51%|███████████████████████████████████████████████████████▌                                                     | 244/479 [00:02<00:01, 129.31note/s]2026-10-21 02:08:23,541 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : maitrise-cuisson-sucree-equilibre-conservation.md (dernière ligne : 'ganoleptique et Conservation Alimentaire')
Assainissement Notes Existantes:  63%|████████████████████████████████████████████████████████████████████▉                                         | 300/479 [00:02<00:01, 98.20note/s]2026-10-21 02:08:24,143 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : optimisation-culinaire-gestion-dechets-variation-sensorielle.md (dernière ligne : 's et Stratégies de Variation Sensorielle')
Assainissement Notes Existantes:  65%|███████████████████████████████████████████████████████████████████████▍                                      | 311/479 [00:02<00:01, 95.69note/s]2026-10-21 02:08:24,229 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : optimisation-extraction-resine-avb.md (dernière ligne : 'ction de Résine et Valorisation 
de l'AVB')
Assainissement Notes Existantes:  73%|███████████████████████████████████████████████████████████████████████████████▏                             | 348/479 [00:03<00:01, 108.18note/s]2026-10-21 02:08:24,521 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : optimisation-vaporisation-stacking-modulation-cbd-thc.md (dernière ligne : 'amique de Stacking et Modulation CBD/THC')
Assainissement Notes Existantes:  78%|████████████████████████████████████████████████████████████████████████████████████▋                        | 372/479 [00:03<00:00, 110.08note/s]2026-10-21 02:08:24,784 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : procedures-expulsion-filiation-algerienne.md (dernière ligne : 'sion Locative et de Filiation Algérienne')
Assainissement Notes Existantes:  80%|███████████████████████████████████████████████████████████████████████████████████████▍                     | 384/479 [00:03<00:00, 110.55note/s]2026-10-21 02:08:24,899 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : prompt-engineering-suno-digicore-neurodivergence.md (dernière ligne : 'que Digicore & Narration Neurodivergente')
Assainissement Notes Existantes:  85%|█████████████████████████████████████████████████████████████████████████████████████████████                | 409/479 [00:03<00:00, 106.62note/s]2026-10-21 02:08:25,189 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : strategie-cro-refonte-semantique-jtbd-lift.md (dernière ligne : 'efonte Sémantique : Approche JTBD & LIFT')
Assainissement Notes Existantes:  97%|█████████████████████████████████████████████████████████████████████████████████████████████████████████▎   | 463/479 [00:04<00:00, 116.09note/s]2026-10-21 02:08:25,574 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : typologie-complexite-ludique-cpu-vs-ram.md (dernière ligne : 'a Complexité Ludique : Modèle CPU vs RAM')
2026-10-21 02:08:25,700 [INFO] Exocortex.TakeoutIngestor: Assainissement terminé : 11 fallbacks purgés, 468 fiches assainies sur place, 468 sessions complètes en mémoire.
2026-10-21 02:08:25,700 [INFO] Exocortex.TakeoutIngestor: Plan de distillation LLM : 12 sessions à traiter (468 déjà complétées ignorées via Mode Delta).
2026-10-21 02:08:26,262 [INFO] Exocortex.LLM: Modèle Ollama 'gemma4:12b' déjà disponible.
2026-10-21 02:08:26,262 [INFO] Exocortex.LLM: Modèle Ollama 'gemma4:26b-a4b' déjà disponible.
2026-10-21 02:08:26,273 [INFO] Exocortex.TakeoutIngestor: --- DÉMARRAGE VAGUE 1 : gemma4:26b-a4b (Thinking ACTIF, num_predict=8192) [12 sessions] ---
2026-10-21 02:08:26,300 [INFO] Exocortex.LLM: Modèle 'gemma4:12b' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-21 02:08:26,313 [INFO] Exocortex.LLM: Modèle 'bge-m3' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-21 02:08:26,326 [INFO] Exocortex.LLM: Modèle 'gemma4:26b-a4b' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-21 02:08:27,379 [INFO] Exocortex.LLM: VRAM GPU après purge active (force_clear_vram) : 14.44 Go libres
Distillation Vague 1 (26B Thinking):   0%|                                                                                                                     | 0/12 [00:00<?, ?sess/s]2026-10-21 02:08:27,440 [INFO] Exocortex.LLM: VRAM GPU : 14.44 Go libres / 15.99 Go totales
Distillation Vague 1 (26B Thinking): 100%|███████████████████████████████████████████████████████████████████████████████████████| 12/12 [06:15<00:00, 31.31s/sess, ok=11, v2_pending=0] 
2026-10-21 02:14:43,137 [INFO] Exocortex.LLM: Modèle 'gemma4:26b-a4b' déchargé avec succès de la VRAM (keep_alive=0).
Traceback (most recent call last):
  File "C:\Users\Jijax\projets\cerveau-deux\run_exocortex.py", line 223, in <module>
    main()
  File "C:\Users\Jijax\projets\cerveau-deux\run_exocortex.py", line 207, in main
    run_ingest_takeout(args.limit)
  File "C:\Users\Jijax\projets\cerveau-deux\run_exocortex.py", line 49, in run_ingest_takeout
    result = ingestor.run(max_distill_sessions=limit)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Jijax\projets\cerveau-deux\src\ingestors\takeout_ingestor.py", line 1684, in run
    initialize_meta_and_concepts(
  File "C:\Users\Jijax\projets\cerveau-deux\src\ingestors\takeout_ingestor.py", line 1490, in initialize_meta_and_concepts
    time.sleep(1.0)
    ^^^^
NameError: name 'time' is not defined
PS C:\Users\Jijax\projets\cerveau-deux> python run_exocortex.py --ingest-takeout
2026-10-21 02:15:05,778 [INFO] Exocortex.Launcher: === Lancement de l'Ingestion Google Takeout ===
2026-10-21 02:15:08,122 [INFO] Exocortex.VectorStore: Table vectorielle LanceDB 'concepts' chargée avec succès.
2026-10-21 02:15:08,502 [INFO] Exocortex.TakeoutIngestor: === LANCEMENT DU MODULE 1 (TAKEOUT INGESTOR) ===
2026-10-21 02:15:08,503 [INFO] Exocortex.TakeoutIngestor: Fichiers Takeout détectés : Gemini=2, YouTube=2, Search=1
2026-10-21 02:15:08,503 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique YouTube : historique-recherche-youtube.html
2026-10-21 02:15:08,546 [INFO] Exocortex.TakeoutIngestor: Extraction YouTube terminée : 0 empreintes trouvées.
2026-10-21 02:15:08,549 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique YouTube : historique-vues-youtube.html
2026-10-21 02:15:10,160 [INFO] Exocortex.TakeoutIngestor: Extraction YouTube terminée : 44896 empreintes trouvées.
2026-10-21 02:15:10,467 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique Google Search : historique-google-search.html
2026-10-21 02:15:11,671 [INFO] Exocortex.TakeoutIngestor: Extraction Google Search terminée : 28258 requêtes trouvées.
2026-10-21 02:15:11,867 [INFO] Exocortex.TakeoutIngestor: Lecture et parsing rapide du fichier HTML Gemini : gemini_gems_data.html
2026-10-21 02:15:11,868 [INFO] Exocortex.TakeoutIngestor: Nombre total de blocs détectés dans l'export : 0
2026-10-21 02:15:11,868 [INFO] Exocortex.TakeoutIngestor: Extraction terminée : 0 tours d'échange valides récupérés.
2026-10-21 02:15:11,868 [INFO] Exocortex.TakeoutIngestor: Lecture et parsing rapide du fichier HTML Gemini : historique-gemini.html
2026-10-21 02:15:12,104 [INFO] Exocortex.TakeoutIngestor: Nombre total de blocs détectés dans l'export : 7264
2026-10-21 02:15:13,650 [INFO] Exocortex.TakeoutIngestor: Extraction terminée : 6649 tours d'échange valides récupérés.
2026-10-21 02:15:13,668 [INFO] Exocortex.TakeoutIngestor: Démarrage de la sessionisation sur 6649 tours...
2026-10-21 02:15:13,688 [INFO] Exocortex.TakeoutIngestor: Sessionisation achevée : 480 sessions qualifiées retenues (541 micro-sessions bruitées archivées).
2026-10-21 02:15:14,250 [INFO] Exocortex.TakeoutIngestor: Table chat_messages synchronisée : 6649 messages insérés.
2026-10-21 02:15:14,262 [INFO] Exocortex.TakeoutIngestor: Exécution de la jointure temporelle Search/YouTube sur 480 sessions...
2026-10-21 02:15:14,861 [INFO] Exocortex.TakeoutIngestor: Jointure temporelle achevée : 0 empreintes rattachées aux sessions Gemini.
2026-10-21 02:15:14,861 [INFO] Exocortex.TakeoutIngestor: Recherche des tunnels d'exploration (Burst Clustering) hors sessions Gemini...
2026-10-21 02:15:16,028 [INFO] Exocortex.TakeoutIngestor: Burst Clustering terminé : 4410 clusters denses formés.
2026-10-21 02:15:16,040 [INFO] Exocortex.TakeoutIngestor: Génération des fichiers de staging dans : C:\Users\Jijax\projets\cerveau-deux\Vault_Data\_System_Buffer\takeout_staging
2026-10-21 02:15:16,075 [INFO] Exocortex.TakeoutIngestor: Fichier 00_USER_PROMPTS_ONLY.md écrit (5828 prompts au total).
2026-10-21 02:15:16,156 [INFO] Exocortex.TakeoutIngestor: 15 fichier(s) de lots complets généré(s).
2026-10-21 02:15:16,157 [INFO] Exocortex.TakeoutIngestor: Consignes web prêtes dans : PROMPT_A_COPIER_DANS_GEMINI_WEB.txt
2026-10-21 02:15:16,158 [INFO] Exocortex.TakeoutIngestor: Taxonomie maîtresse à 16 macro-catégories validée dans Taxonomie_Tags.md
2026-10-21 02:15:16,159 [INFO] Exocortex.TakeoutIngestor: Taxonomie maîtresse à 16 macro-catégories validée dans Taxonomie_Tags.md
Assainissement Notes Existantes:   8%|█████████▏                                                                                                    | 40/479 [00:00<00:03, 135.79note/s]2026-10-21 02:15:16,534 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : analyse-phishing-obfuscation-contournement.md (dernière ligne : 'Obfuscation et Contournement de Sécurité')
Assainissement Notes Existantes:  24%|██████████████████████████▍                                                                                  | 116/479 [00:00<00:02, 146.82note/s]2026-10-21 02:15:17,097 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : architecture-tunnel-conversion-tripwire-high-ticket.md (dernière ligne : 'rsion : Stratégie Tripwire & High-Ticket')
Assainissement Notes Existantes:  64%|█████████████████████████████████████████████████████████████████████▋                                       | 306/479 [00:02<00:01, 141.92note/s]2026-10-21 02:15:18,398 [WARNING] Exocortex.TakeoutIngestor: Fiche tronquée détectée et purgée : optimisation-culinaire-strategie-alimentaire-neuroatypie.md (dernière ligne : 'Alimentaires pour Profils Neuroatypiques')
Assainissement Notes Existantes: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████| 479/479 [00:03<00:00, 137.67note/s]
2026-10-21 02:15:19,664 [INFO] Exocortex.TakeoutIngestor: Assainissement terminé : 3 fallbacks purgés, 476 fiches assainies sur place, 476 sessions complètes en mémoire.
2026-10-21 02:15:19,665 [INFO] Exocortex.TakeoutIngestor: Plan de distillation LLM : 4 sessions à traiter (476 déjà complétées ignorées via Mode Delta).
2026-10-21 02:15:20,207 [INFO] Exocortex.LLM: Modèle Ollama 'gemma4:12b' déjà disponible.
2026-10-21 02:15:20,207 [INFO] Exocortex.LLM: Modèle Ollama 'gemma4:26b-a4b' déjà disponible.
2026-10-21 02:15:20,219 [INFO] Exocortex.TakeoutIngestor: --- DÉMARRAGE VAGUE 1 : gemma4:26b-a4b (Thinking ACTIF, num_predict=8192) [4 sessions] ---
2026-10-21 02:15:20,247 [INFO] Exocortex.LLM: Modèle 'bge-m3' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-21 02:15:20,260 [INFO] Exocortex.LLM: Modèle 'gemma4:26b-a4b' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-21 02:15:20,274 [INFO] Exocortex.LLM: Modèle 'gemma4:12b' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-21 02:15:21,337 [INFO] Exocortex.LLM: VRAM GPU après purge active (force_clear_vram) : 14.23 Go libres
Distillation Vague 1 (26B Thinking):   0%|                                                                                                                      | 0/4 [00:00<?, ?sess/s]2026-10-21 02:15:21,400 [INFO] Exocortex.LLM: VRAM GPU : 14.23 Go libres / 15.99 Go totales
Distillation Vague 1 (26B Thinking): 100%|██████████████████████████████████████████████████████████████████████████████████████████| 4/4 [02:29<00:00, 37.43s/sess, ok=3, v2_pending=0]
2026-10-21 02:17:51,086 [INFO] Exocortex.LLM: Modèle 'gemma4:26b-a4b' déchargé avec succès de la VRAM (keep_alive=0).
Traceback (most recent call last):
  File "C:\Users\Jijax\projets\cerveau-deux\run_exocortex.py", line 223, in <module>
    main()
  File "C:\Users\Jijax\projets\cerveau-deux\run_exocortex.py", line 207, in main
    run_ingest_takeout(args.limit)
  File "C:\Users\Jijax\projets\cerveau-deux\run_exocortex.py", line 49, in run_ingest_takeout
    result = ingestor.run(max_distill_sessions=limit)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Jijax\projets\cerveau-deux\src\ingestors\takeout_ingestor.py", line 1684, in run
    initialize_meta_and_concepts(
  File "C:\Users\Jijax\projets\cerveau-deux\src\ingestors\takeout_ingestor.py", line 1490, in initialize_meta_and_concepts
    time.sleep(1.0)
    ^^^^
NameError: name 'time' is not defined