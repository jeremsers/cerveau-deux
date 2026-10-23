PS C:\Users\Jijax\projets\cerveau-deux> python run_exocortex.py --ingest-takeout
2026-10-20 17:41:45,904 [INFO] Exocortex.Launcher: === Lancement de l'Ingestion Google Takeout ===
2026-10-20 17:41:47,811 [INFO] Exocortex.VectorStore: Table vectorielle LanceDB 'concepts' chargée avec succès.
2026-10-20 17:41:47,816 [INFO] Exocortex.TakeoutIngestor: === LANCEMENT DU MODULE 1 (TAKEOUT INGESTOR) ===
2026-10-20 17:41:47,816 [INFO] Exocortex.TakeoutIngestor: Fichiers Takeout détectés : Gemini=2, YouTube=2, Search=1
2026-10-20 17:41:47,820 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique YouTube : historique-recherche-youtube.html
2026-10-20 17:41:47,853 [INFO] Exocortex.TakeoutIngestor: Extraction YouTube terminée : 0 empreintes trouvées.
2026-10-20 17:41:47,855 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique YouTube : historique-vues-youtube.html
2026-10-20 17:41:49,338 [INFO] Exocortex.TakeoutIngestor: Extraction YouTube terminée : 44896 empreintes trouvées.
2026-10-20 17:41:49,731 [INFO] Exocortex.TakeoutIngestor: Parsing de l'historique Google Search : historique-google-search.html
2026-10-20 17:41:50,864 [INFO] Exocortex.TakeoutIngestor: Extraction Google Search terminée : 28258 requêtes trouvées.
2026-10-20 17:41:51,126 [INFO] Exocortex.TakeoutIngestor: Lecture et parsing rapide du fichier HTML Gemini : gemini_gems_data.html
2026-10-20 17:41:51,126 [INFO] Exocortex.TakeoutIngestor: Nombre total de blocs détectés dans l'export : 0
2026-10-20 17:41:51,126 [INFO] Exocortex.TakeoutIngestor: Extraction terminée : 0 tours d'échange valides récupérés.
2026-10-20 17:41:51,126 [INFO] Exocortex.TakeoutIngestor: Lecture et parsing rapide du fichier HTML Gemini : historique-gemini.html
2026-10-20 17:41:51,319 [INFO] Exocortex.TakeoutIngestor: Nombre total de blocs détectés dans l'export : 7264
2026-10-20 17:41:53,002 [INFO] Exocortex.TakeoutIngestor: Extraction terminée : 6649 tours d'échange valides récupérés.
2026-10-20 17:41:53,023 [INFO] Exocortex.TakeoutIngestor: Démarrage de la sessionisation sur 6649 tours...
2026-10-20 17:41:53,035 [INFO] Exocortex.TakeoutIngestor: Sessionisation achevée : 480 sessions qualifiées retenues (541 sous-sessions bruitées écartées).
2026-10-20 17:41:53,047 [INFO] Exocortex.TakeoutIngestor: Exécution de la jointure temporelle Search/YouTube sur 480 sessions...
2026-10-20 17:41:55,708 [INFO] Exocortex.TakeoutIngestor: Jointure temporelle achevée : 4093 empreintes rattachées aux sessions Gemini.
2026-10-20 17:41:55,708 [INFO] Exocortex.TakeoutIngestor: Recherche des tunnels d'exploration (Burst Clustering) hors sessions Gemini...
2026-10-20 17:41:56,765 [INFO] Exocortex.TakeoutIngestor: Burst Clustering terminé : 4410 clusters denses formés.
2026-10-20 17:41:56,784 [INFO] Exocortex.TakeoutIngestor: Génération des fichiers de staging dans : C:\Users\Jijax\projets\cerveau-deux\Vault_Data\_System_Buffer\takeout_staging
2026-10-20 17:41:56,820 [INFO] Exocortex.TakeoutIngestor: Fichier 00_USER_PROMPTS_ONLY.md écrit (5828 prompts au total).
2026-10-20 17:41:56,900 [INFO] Exocortex.TakeoutIngestor: 15 fichier(s) de lots complets généré(s).
2026-10-20 17:41:56,900 [INFO] Exocortex.TakeoutIngestor: Consignes web prêtes dans : PROMPT_A_COPIER_DANS_GEMINI_WEB.txt
2026-10-20 17:41:57,456 [INFO] Exocortex.LLM: Modèle Ollama 'gemma4:12b' déjà disponible.
2026-10-20 17:41:57,456 [INFO] Exocortex.LLM: Modèle Ollama 'gemma4:26b-a4b' déjà disponible.
2026-10-20 17:41:57,539 [INFO] Exocortex.LLM: VRAM GPU : 14.61 Go libres / 15.99 Go totales
2026-10-20 17:42:32,548 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : contournement-api-trakt-riven-jellyseerr-webhooks.md (#HomeLab_MediaServer)
2026-10-20 17:42:59,554 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-debogage-sillytavern-koboldcpp.md (#LLM_Local_et_Hardware)
2026-10-20 17:43:29,012 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 733)). Tentative d'extraction manuelle...
2026-10-20 17:43:29,013 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session b84de84534d1836a_s03_20260915 : Unterminated string starting at: line 16 column 32 (char 733)
2026-10-20 17:43:29,014 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : du-coup-jai-des-valeurs-a-adapter-pour-le-contexte.md (#A_Trier)
2026-10-20 17:43:47,908 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : deploiement-stack-debrid-windows.md (#HomeLab_MediaServer)
2026-10-20 17:44:09,026 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-local-llm-roleplay-qwen-sillytavern.md (#LLM_Local_et_Hardware)
2026-10-20 17:44:33,439 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Expecting value: line 1 column 1 (char 0)). Tentative d'extraction manuelle...
2026-10-20 17:44:33,439 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 15517b9f1e91b0f1 : Expecting value: line 1 column 1 (char 0)
2026-10-20 17:44:33,440 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : origins-anima-after-losing-a-player-combat-gain-20.md (#A_Trier)
2026-10-20 17:45:06,824 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Cuisine_Equipement_Technique`
2026-10-20 17:45:06,824 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrages-equipement-cuisine-riz-glace.md (#Cuisine_Equipement_Technique)
2026-10-20 17:45:36,089 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 715)). Tentative d'extraction manuelle...
2026-10-20 17:45:36,089 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 66c6295487c3e470_s01_20260301 : Unterminated string starting at: line 16 column 32 (char 715)
2026-10-20 17:45:36,089 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : je-mapprete-a-lancer-ma-toute-premiere-campagne-go.md (#A_Trier)
2026-10-20 17:45:58,024 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-representation-autisme-sheldon-cooper.md (#Introspection_et_Neuroatypie)
2026-10-20 17:46:35,778 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 816)). Tentative d'extraction manuelle...
2026-10-20 17:46:35,779 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 0934ff6c7fb95a1c_s22_20260225 : Unterminated string starting at: line 16 column 32 (char 816)
2026-10-20 17:46:35,780 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : bon-jai-redesigner-les-lp-et-la-frontpage-avec-not.md (#A_Trier)
2026-10-20 17:47:08,011 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 37 column 32 (char 3486)). Tentative d'extraction manuelle...
2026-10-20 17:47:08,011 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 0934ff6c7fb95a1c_s12_20260208 : Unterminated string starting at: line 37 column 32 (char 3486)
2026-10-20 17:47:08,011 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : jai-peur-qua-120-chf-prix-ferme-voulu-par-le-clien.md (#A_Trier)
2026-10-20 17:47:28,544 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-lp-double-conversion-astro-scss.md (#Dev_Web_et_Stack_Astro)
2026-10-20 17:47:48,084 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : navigation-mdph-diagnostic-differentiel-tsa-trauma.md (#Introspection_et_Neuroatypie)
2026-10-20 17:48:16,032 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : methodologie-veille-tech-juridique.md (#Productivité_Veille_Informationnelle)
2026-10-20 17:48:38,486 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : phenomenologie-retro-acronymes-etymologie.md (#Linguistique_et_Culture_Web)
2026-10-20 17:49:14,529 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Marketing_Conversion_et_Ads`
2026-10-20 17:49:14,529 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : conversion-froide-tracking-transaction-offre-crise.md (#Marketing_Conversion_et_Ads)
2026-10-20 17:49:47,677 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Expecting value: line 1 column 1 (char 0)). Tentative d'extraction manuelle...
2026-10-20 17:49:47,677 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 0934ff6c7fb95a1c_s13_20260209 : Expecting value: line 1 column 1 (char 0)
2026-10-20 17:49:47,678 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : bon-on-va-partir-sur-une-petite-session-templating.md (#A_Trier)
2026-10-20 17:50:07,028 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : framework-documentation-portfolio-projets-digitaux.md (#Chefferie_Projet_et_UX)
2026-10-20 17:50:38,598 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-ecart-type-discours-politique.md (#Sociologie_et_Politique)
2026-10-20 17:51:03,541 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-philosophique-credit-social-despotisme-eclaire.md (#Philo_Droit_et_Morale)
2026-10-20 17:51:26,876 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Culture_Kpop_et_Industrie_Media`
2026-10-20 17:51:26,876 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-comparative-ceremonies-kpop.md (#Culture_Kpop_et_Industrie_Media)
2026-10-20 17:51:59,921 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : deconstruction-meritocratie-richesse-relative.md (#Sociologie_et_Politique)
2026-10-20 17:52:30,518 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : absurdisme-neuroatypie-ideologies.md (#Philo_Droit_et_Morale)
2026-10-20 17:52:54,100 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : configuration-stripe-copywriting-tunnel-vente-pnl.md (#Freelance_et_Acquisition)
2026-10-20 17:53:27,578 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Neurosciences_Esthetiques`
2026-10-20 17:53:27,579 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : neuro-acoustique-saturation-cognitive-hpi-tdah.md (#Neurosciences_Esthetiques)
2026-10-20 17:53:50,183 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-critique-systemes-teleologie-hegemonie-cybernétique.md (#Sociologie_et_Politique)
2026-10-20 17:54:10,144 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-llm-inhibition-raisonnement-experts.md (#IA_Agentique_et_RAG)
2026-10-20 17:54:44,026 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sociologie_Culture_Web`
2026-10-20 17:54:44,027 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-meta-ragebait-dynamiques-meute-numerique.md (#Sociologie_Culture_Web)
2026-10-20 17:55:16,105 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dialectique-simulation-confrontation-ideologique.md (#Sociologie_et_Politique)
2026-10-20 17:55:46,774 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sociologie_Religion_et_Pratique`
2026-10-20 17:55:46,775 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : derive-pratique-religieuse-mecanisation-gamification.md (#Sociologie_Religion_et_Pratique)
2026-10-20 17:56:15,811 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Esport_Analyse_et_Psychologie`
2026-10-20 17:56:15,812 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : epistemologie-analyse-esport-biais-cognitifs.md (#Esport_Analyse_et_Psychologie)
2026-10-20 17:56:45,291 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-dossier-mdph-aah-rsdae.md (#Sante_et_Admin_Perso)
2026-10-20 17:57:13,701 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : neurodivergence-facteur-g-double-empathie-homophilie.md (#Introspection_et_Neuroatypie)
2026-10-20 17:57:50,855 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Sociologie_Esport`
2026-10-20 17:57:50,856 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-systemique-sous-representation-esport.md (#Gaming_Sociologie_Esport)
2026-10-20 17:58:22,736 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Philo_Epistemologie_et_Ontologie`
2026-10-20 17:58:22,736 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : epistemologie-constructivisme-isomorphisme-verite.md (#Philo_Epistemologie_et_Ontologie)
2026-10-20 17:58:47,926 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-identification-politique-narratif-avant-poste.md (#Sociologie_et_Politique)
2026-10-20 17:59:14,550 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : monotropisme-inertie-autistique-cliff-edge.md (#Introspection_et_Neuroatypie)
2026-10-20 17:59:35,127 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : conflit-integration-neuroatypie-burnout-salariat.md (#Introspection_et_Neuroatypie)
2026-10-20 18:00:00,164 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Philosophie_Identitaire_et_Sociale`
2026-10-20 18:00:00,165 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : friction-phenomenologique-vs-existentialisme-agentivite.md (#Philosophie_Identitaire_et_Sociale)
2026-10-20 18:00:24,911 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session b0b0d3efc9f6a3ca_s01_20251015 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 18:00:24,912 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : tu-crois-quon-pourrait-travailler-ensemble-a-forma.md (#Chefferie_Projet_et_UX)
2026-10-20 18:00:46,248 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : mecanismes-profil-pda-hpi-autisme.md (#Introspection_et_Neuroatypie)
2026-10-20 18:01:09,179 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : workflow-hybride-maschine-ableton-architecture-drop.md (#Analyse_Musicale_et_MAO)
2026-10-20 18:01:48,365 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 15 column 32 (char 743)). Tentative d'extraction manuelle...
2026-10-20 18:01:48,365 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session f0da8c7048b8ddda_s01_20260201 : Unterminated string starting at: line 15 column 32 (char 743)
2026-10-20 18:01:48,366 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : je-suis-tomber-sur-un-message-intéressant-nicholas.md (#A_Trier)
2026-10-20 18:02:19,729 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Histoire_SystemesComplexes`
2026-10-20 18:02:19,730 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dynamiques-historiques-causalite-complexite.md (#Histoire_SystemesComplexes)
2026-10-20 18:02:54,964 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : absurdisme-artisanat-revolte-teleologie.md (#Philo_Droit_et_Morale)
2026-10-20 18:03:27,330 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-conversion-acquisition-services-locaux.md (#Freelance_et_Acquisition)
2026-10-20 18:03:52,324 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-formation-rfpe-vs-aah-mdph.md (#Sante_et_Admin_Perso)
2026-10-20 18:04:13,222 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : homonationalisme-respectabilite-alienation-sociopolitique.md (#Sociologie_et_Politique)
2026-10-20 18:04:41,726 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dynamique-regulation-cognitive-hpi-autisme-interet.md (#Introspection_et_Neuroatypie)
2026-10-20 18:05:14,538 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 97bf529a8cd6131a : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 18:05:14,539 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-je-viens-avoir-une-idee-de-scenario-en-creant-u.md (#Prompt_Engineering_et_Suno)
2026-10-20 18:05:47,652 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-trajectoire-taylor-swift-soft-fascisme.md (#Sociologie_et_Politique)
2026-10-20 18:06:24,953 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 632)). Tentative d'extraction manuelle...
2026-10-20 18:06:24,953 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 3790d98514e3439e_s09_20260227 : Unterminated string starting at: line 16 column 32 (char 632)
2026-10-20 18:06:24,954 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : attention-repasse-au-format-slide-car-tout-le-form.md (#A_Trier)
2026-10-20 18:07:04,906 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 657)). Tentative d'extraction manuelle...
2026-10-20 18:07:04,906 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session c520289736dfdd22 : Unterminated string starting at: line 16 column 32 (char 657)
2026-10-20 18:07:04,907 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : is-ff-xvi-as-lengthy-in-cinematics-as-the-first-ho.md (#A_Trier)
2026-10-20 18:07:42,893 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 665)). Tentative d'extraction manuelle...
2026-10-20 18:07:42,893 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 3c47522650838ef1_s02_20251207 : Unterminated string starting at: line 16 column 32 (char 665)
2026-10-20 18:07:42,893 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : faut-il-separer-lhomme-de-lartiste.md (#A_Trier)
2026-10-20 18:08:14,649 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Epistemologie_et_Expertise`
2026-10-20 18:08:14,649 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : deconstruction-expertise-boite-noire-desacralisation.md (#Epistemologie_et_Expertise)
2026-10-20 18:08:52,040 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-dysfonctionnements-cancel-culture.md (#Sociologie_et_Politique)
2026-10-20 18:09:22,267 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : violation-inegalite-bell-realisme-non-localite-hasard.md (#Metaphysique_et_Physique)
2026-10-20 18:10:00,494 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Business_Strategie_IA`
2026-10-20 18:10:00,496 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : methodologie-veille-cadrage-ia-rse.md (#Business_Strategie_IA)
2026-10-20 18:10:24,283 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
synthesized_markdown_body
  Field required [type=missing, input_value={'is_worth_indexing': Tru...rie_Musicale_Asie_Est']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 18:10:24,284 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 52938d3663558d07 : 1 validation error for DistilledConceptSchema
synthesized_markdown_body
  Field required [type=missing, input_value={'is_worth_indexing': Tru...rie_Musicale_Asie_Est']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 18:10:24,285 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : i-was-wondering-are-music-show-in-korea-more-mains.md (#A_Trier)
2026-10-20 18:10:46,719 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : critique-meritocratie-efficience-theorie-cuilleres.md (#Sociologie_et_Politique)
2026-10-20 18:11:23,628 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-hardware-local-assistants-multimodaux.md (#LLM_Local_et_Hardware)
2026-10-20 18:12:01,730 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 852)). Tentative d'extraction manuelle...
2026-10-20 18:12:01,730 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 88ffd2664b40ec7a : Unterminated string starting at: line 16 column 32 (char 852)
2026-10-20 18:12:01,731 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : white-supremacy-collapses-instantly-when-you-reali.md (#Philo_Droit_et_Morale)
2026-10-20 18:12:20,267 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-veille-technologique-chef-projet-digital.md (#Chefferie_Projet_et_UX)
2026-10-20 18:12:51,356 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : probabilites-impossibilite-physique-inegalites-bell.md (#Metaphysique_et_Physique)
2026-10-20 18:13:12,085 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
synthesized_markdown_body
  Field required [type=missing, input_value={'is_worth_indexing': Tru...iltyTavern & Samplers']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 18:13:12,085 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session b84de84534d1836a_s01_20260910 : 1 validation error for DistilledConceptSchema
synthesized_markdown_body
  Field required [type=missing, input_value={'is_worth_indexing': Tru...iltyTavern & Samplers']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 18:13:12,086 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ive-dabbled-with-sillytavern-and-an-open-source-mo.md (#A_Trier)
2026-10-20 18:13:35,010 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : deconstruction-sauts-logiques-esoterisme-sociologie.md (#Sociologie_et_Politique)
2026-10-20 18:14:05,809 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Infrastructure_et_Streaming`
2026-10-20 18:14:05,810 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-pc-handheld-apollo-artemis-steam-input.md (#Gaming_Infrastructure_et_Streaming)
2026-10-20 18:14:33,445 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session eaa75ffc557bb1aa_s02_20261018 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 18:14:33,446 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : 1-le-probleme-cest-que-je-trouve-personnellement-q.md (#Sante_et_Admin_Perso)
2026-10-20 18:15:02,394 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Data_Engineering_Automation`
2026-10-20 18:15:02,395 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-decouplage-extraction-assets-excel-api.md (#Data_Engineering_Automation)
2026-10-20 18:15:25,808 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : audit-pivot-google-ads-niche-rupture.md (#Freelance_et_Acquisition)
2026-10-20 18:15:51,379 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : deconstruction-geoïsme-droits-naturels-monocausalité.md (#Philo_Droit_et_Morale)
2026-10-20 18:16:20,402 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `IA_Theorie_et_Cognition`
2026-10-20 18:16:20,403 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ontologie-emergence-topologie-espace-latent.md (#IA_Theorie_et_Cognition)
2026-10-20 18:16:48,724 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...ent pour l'entreprise "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 18:16:48,724 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session a1e79c5cce2aab87_s01_20260318 : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...ent pour l'entreprise "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 18:16:48,724 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : forces-persuasion-du-client-avec-presentation-de-l.md (#Business_Strategie_IA)
2026-10-20 18:17:19,500 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Data_AnalysePolitique`
2026-10-20 18:17:19,501 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : framework-influence-politique-engagement-algorithmique.md (#Data_AnalysePolitique)
2026-10-20 18:17:43,277 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : prismes-geopolitiques-chine-usa-autonomie-europe.md (#Sociologie_et_Politique)
2026-10-20 18:18:13,621 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-positionnement-producteur-vs-cm.md (#Freelance_et_Acquisition)
2026-10-20 18:18:48,338 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 76ab18281b446c6f_s02_20260216 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 18:18:48,339 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ya-peut-etre-une-confusion-quand-je-parle-des-gran.md (#A_Trier)
2026-10-20 18:19:17,360 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Marketing_Digital_et_Strategie`
2026-10-20 18:19:17,361 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-strategie-marketing-paradigme-ia.md (#Marketing_Digital_et_Strategie)
2026-10-20 18:19:50,973 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Media_Webnovels_et_LitRPG`
2026-10-20 18:19:50,974 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : profil-consommation-narrative-world-building-power-fantasy.md (#Media_Webnovels_et_LitRPG)
2026-10-20 18:20:23,278 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : positionnement-portfolio-profil-hybride-droit-dev-gestion-projet.md (#Freelance_et_Acquisition)
2026-10-20 18:20:51,445 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : sociologie-queerbaiting-normalisation-recuperation.md (#Sociologie_et_Politique)
2026-10-20 18:21:18,679 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : modelisation-vectorielle-identification-genre-male-gaze.md (#Sociologie_et_Politique)
2026-10-20 18:21:57,299 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_SystemOptimization`
2026-10-20 18:21:57,300 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : diagnostic-resolution-micro-stutters-memory-drivers.md (#Hardware_SystemOptimization)
2026-10-20 18:22:20,642 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : profilage-neurocognitif-dyssynchronie-hypervigilance.md (#Introspection_et_Neuroatypie)
2026-10-20 18:22:54,496 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : profil-double-exceptionnalite-hpi-tsa.md (#Introspection_et_Neuroatypie)
2026-10-20 18:23:32,262 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sociologie_Fandom_et_Subcultures`
2026-10-20 18:23:32,262 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dualite-shipping-culture-simulation-performance.md (#Sociologie_Fandom_et_Subcultures)
2026-10-20 18:24:02,027 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : sociologie-domination-dissonance-parasociale-numerique.md (#Sociologie_et_Politique)
2026-10-20 18:24:30,614 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-production-musicale-kanye-west.md (#Analyse_Musicale_et_MAO)
2026-10-20 18:24:54,268 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : declin-exigence-fracture-cognitive-automatisation.md (#Sociologie_Cognition_Numérique)
2026-10-20 18:25:22,091 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-consommation-derives-cannabinoïdes-protocoles-tolerance.md (#Sante_Pharmacologie_Cannabinoïdes)
2026-10-20 18:25:58,540 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Culture_et_Sociologie_Musicale`
2026-10-20 18:25:58,542 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dichotomie-identitaire-economie-caricature-rap.md (#Culture_et_Sociologie_Musicale)
2026-10-20 18:26:26,317 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Marketing_Performance_et_Data`
2026-10-20 18:26:26,318 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-tracking-ga4-google-ads-micro-budget.md (#Marketing_Performance_et_Data)
2026-10-20 18:26:49,067 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : atrophie-pensee-dominante-exclusion-debat.md (#Sociologie_et_Politique)
2026-10-20 18:27:20,147 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-conversion-design-triage-therapeute.md (#Chefferie_Projet_et_UX)
2026-10-20 18:27:45,977 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Lifestyle_Vaporisation`
2026-10-20 18:27:45,978 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparatif-vaporisateurs-architecture-oem-vs-proprietaire.md (#Lifestyle_Vaporisation)
2026-10-20 18:28:08,223 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-clinique-masking-epuisement-neuroatypique.md (#Introspection_et_Neuroatypie)
2026-10-20 18:28:32,469 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : epicurisme-moderne-resistance-absurde.md (#Philo_Droit_et_Morale)
2026-10-20 18:29:03,200 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : acceleration-richesse-verrou-metapolitique.md (#Sociologie_et_Politique)
2026-10-20 18:29:38,457 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Design_et_Psychologie`
2026-10-20 18:29:38,458 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-agencie-systemique-profilage-joueur.md (#Gaming_Design_et_Psychologie)
2026-10-20 18:30:00,945 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-absurdisme-lucidite-revolte-collective.md (#Philo_Droit_et_Morale)
2026-10-20 18:30:34,447 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-deploiement-iteratif-kpi-chatbot-rag.md (#Chefferie_Projet_et_UX)
2026-10-20 18:31:04,831 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparaison-philosophie-combat-wow-gw2.md (#MMORPG_Theorycraft)
2026-10-20 18:31:31,205 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 9b38b9556f3aabe5 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 18:31:31,206 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-parlons-conscience-deja-pour-commencer-je-veux.md (#A_Trier)
2026-10-20 18:32:06,027 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-organoleptique-pates-fermentees-coreennes.md (#Gastronomie_Fermentation_et_Sensorialité)
2026-10-20 18:32:40,493 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_GameDesign_Cognitif`
2026-10-20 18:32:40,493 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : typologie-complexite-gameplay-cpu-vs-ram.md (#Gaming_GameDesign_Cognitif)
2026-10-20 18:33:13,444 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : neurobiologie-focalisation-interne-monotropisme.md (#Introspection_et_Neuroatypie)
2026-10-20 18:33:49,366 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : mecanismes-derive-semantique-brainrot.md (#Linguistique_et_Culture_Web)
2026-10-20 18:34:19,918 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ingenierie-soutenance-portfolio-chef-projet-digital.md (#Chefferie_Projet_et_UX)
2026-10-20 18:34:43,495 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...boss (souvent de type '}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 18:34:43,495 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 6762c417e899baef : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...boss (souvent de type '}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 18:34:43,496 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : httpswwwnexusmodscomeldenringmods4709-im-looking-f.md (#A_Trier)
2026-10-20 18:35:14,794 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : profil-esthetique-densite-ancre-vocale-liberation.md (#Analyse_Musicale_et_MAO)
2026-10-20 18:35:57,525 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 829)). Tentative d'extraction manuelle...
2026-10-20 18:35:57,525 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 80780af833b4898c : Unterminated string starting at: line 16 column 32 (char 829)
2026-10-20 18:35:57,526 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-je-suis-tombé-sur-ce-tweet-genuine-questions-be.md (#A_Trier)
2026-10-20 18:36:23,757 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : impasse-camusienne-ethique-violence-decoloniale.md (#Philo_Droit_et_Morale)
2026-10-20 18:36:57,174 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : determinisme-pensee-systemique-critique-individualisme.md (#Sociologie_et_Politique)
2026-10-20 18:37:31,818 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Marketing_Strategie_et_Performance`
2026-10-20 18:37:31,818 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : plan-marketing-digital-hyatt-regency-paris-etoile.md (#Marketing_Strategie_et_Performance)
2026-10-20 18:38:08,915 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Economie_Politique_et_Ideologie`
2026-10-20 18:38:08,916 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : deconstruction-trilemme-economique-neutralite-institutionnelle.md (#Economie_Politique_et_Ideologie)
2026-10-20 18:38:32,747 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparaison-modeles-socio-economiques-chine-usa.md (#Sociologie_et_Politique)
2026-10-20 18:39:05,556 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Admin_Gestion_Litige`
2026-10-20 18:39:05,557 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-recadrage-litige-administratif.md (#Admin_Gestion_Litige)
2026-10-20 18:39:35,448 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-theorie-esprit-masking-ados2.md (#Introspection_et_Neuroatypie)
2026-10-20 18:40:12,787 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-performative-male-transition-cognitive.md (#Sociologie_et_Politique)
2026-10-20 18:40:41,475 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Sociologie_Medecine`
2026-10-20 18:40:41,475 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : genese-protocoles-alternatifs-lyme-covid.md (#Sante_Sociologie_Medecine)
2026-10-20 18:41:13,941 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-narrative-romance-vs-relation-webtoons.md (#Webtoons_Manga_et_Anime)
2026-10-20 18:41:48,093 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-metaphysique-observateur-4d-individualisme-ouvert.md (#Metaphysique_et_Physique)
2026-10-20 18:42:30,071 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 757)). Tentative d'extraction manuelle...
2026-10-20 18:42:30,071 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session d25b9f810a755bf6 : Unterminated string starting at: line 16 column 32 (char 757)
2026-10-20 18:42:30,072 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : cristallisation.md (#A_Trier)
2026-10-20 18:43:11,391 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `MMORPG_GuildManagement`
2026-10-20 18:43:11,392 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-recrutement-filtrage-semantique-mmorpg.md (#MMORPG_GuildManagement)
2026-10-20 18:43:32,087 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 64039d3d83ed303b : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 18:43:32,088 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : cest-quoi-la-culture-du-plein.md (#Linguistique_et_Culture_Web)
2026-10-20 18:43:56,526 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : neuroatypie-travail-subsistance-propre.md (#Introspection_et_Neuroatypie)
2026-10-20 18:44:29,113 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Marketing_Strategie_et_ROI`
2026-10-20 18:44:29,113 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-marketing-roi-planification-editoriale.md (#Marketing_Strategie_et_ROI)
2026-10-20 18:44:55,306 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : methodologie-cadrage-us-tickets-api-contracts.md (#Chefferie_Projet_et_UX)
2026-10-20 18:45:34,059 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 24413b0b7f201835_s42_20261016 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 18:45:34,060 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : quid-du-he-10.md (#A_Trier)
2026-10-20 18:46:11,583 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : psychologie-soumission-dissonance-integrite.md (#Sociologie_et_Politique)
2026-10-20 18:46:42,920 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Handheld_Ecosystem`
2026-10-20 18:46:42,922 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-ecosysteme-gaming-portable-micro-sessions.md (#Gaming_Handheld_Ecosystem)
2026-10-20 18:47:12,715 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Neuroatypie_Admin_France`
2026-10-20 18:47:12,715 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : articulation-ema-cra-strategie-mdph-autisme.md (#Neuroatypie_Admin_France)
2026-10-20 18:47:48,706 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : cout-energetique-lucidite-dogmatisme-cognitif.md (#Philo_Droit_et_Morale)
2026-10-20 18:48:27,485 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Culture_Pop_et_Narratologie`
2026-10-20 18:48:27,485 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-vectorielle-resilience-narrative-sitcoms.md (#Culture_Pop_et_Narratologie)
2026-10-20 18:49:08,887 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-systemique-vs-consommation-politique-epistemologie.md (#Sociologie_et_Politique)
2026-10-20 18:49:36,609 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : paradoxes-sociopolitiques-droits-trans-coalitions-politiques.md (#Sociologie_et_Politique)
2026-10-20 18:50:14,365 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 705)). Tentative d'extraction manuelle...
2026-10-20 18:50:14,365 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 24413b0b7f201835_s24_20260908 : Unterminated string starting at: line 16 column 32 (char 705)
2026-10-20 18:50:14,366 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : jai-potentiellemnt-acces-a-de-la-cali-canda-et-de.md (#A_Trier)
2026-10-20 18:50:42,846 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Culture_Pop_et_Analyse_Narrative`
2026-10-20 18:50:42,847 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-vectorielle-narration-empathie-systeme-chaos.md (#Culture_Pop_et_Analyse_Narrative)
2026-10-20 18:51:02,595 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 8f17d824af6c8d8f : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 18:51:02,595 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-je-veux-que-tu-maide-a-preparer-des-prompts-pou.md (#Prompt_Engineering_et_Suno)
2026-10-20 18:51:32,259 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `GameDesign_Systems`
2026-10-20 18:51:32,260 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-scoring-simplification-moba-tactile.md (#GameDesign_Systems)
2026-10-20 18:52:00,895 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : spinozisme-absurde-dialectique-droit-soft-law.md (#Philo_Droit_et_Morale)
2026-10-20 18:52:32,373 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-hardware-gpu-desktop-vs-arm-ia-locale.md (#LLM_Local_et_Hardware)
2026-10-20 18:52:59,084 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : transition-diagnostique-hpi-tsa-communication.md (#Introspection_et_Neuroatypie)
2026-10-20 18:53:34,285 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Data_Privacy_Mechanics`
2026-10-20 18:53:34,285 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-systemique-privacy-asymetrie-pouvoir-espace-latent.md (#Data_Privacy_Mechanics)
2026-10-20 18:54:10,456 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 766)). Tentative d'extraction manuelle...
2026-10-20 18:54:10,457 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 500cc93f69efff33_s02_20260108 : Unterminated string starting at: line 16 column 32 (char 766)
2026-10-20 18:54:10,458 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : jai-limpression-quon-sort-un-peu-des-chiffres-de-n.md (#A_Trier)
2026-10-20 18:54:44,763 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Neurosciences_et_Cognition_Musicale`
2026-10-20 18:54:44,764 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : neuro-architecture-evolution-musicale-taste-freeze.md (#Neurosciences_et_Cognition_Musicale)
2026-10-20 18:55:21,826 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-semantique-recrutement-guilde-mmorpg.md (#MMORPG_Theorycraft)
2026-10-20 18:55:55,556 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 738)). Tentative d'extraction manuelle...
2026-10-20 18:55:55,556 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 0934ff6c7fb95a1c_s20_20260224 : Unterminated string starting at: line 16 column 32 (char 738)
2026-10-20 18:55:55,557 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : jm-ai-toujours-pas-acces-alors-que-jai-fait-un-pai.md (#Sante_et_Admin_Perso)
2026-10-20 18:56:28,908 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-volume-alimentaire-batch-cooking-500kcal.md (#Nutrition_Volume_Eating)
2026-10-20 18:56:54,850 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : asymetries-sociologiques-epistemologiques-transidentite-bon-sens.md (#Sociologie_et_Politique)
2026-10-20 18:57:20,249 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ontologie-temps-b-theorie-vs-phenomenologie-localite.md (#Metaphysique_et_Physique)
2026-10-20 18:57:42,107 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dynamiques-transmisogynie-scrutin-mtf.md (#Sociologie_et_Politique)
2026-10-20 18:58:20,930 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 714)). Tentative d'extraction manuelle...
2026-10-20 18:58:20,930 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 0625db95dd409dba : Unterminated string starting at: line 16 column 32 (char 714)
2026-10-20 18:58:20,931 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : je-realise-un-guide-sur-la-pnl-et-je-dois-faire-un.md (#A_Trier)
2026-10-20 18:58:51,148 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-clinique-marqueurs-neurodivergence.md (#Introspection_et_Neuroatypie)
2026-10-20 18:59:11,535 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : definition-personas-green-futur-b2b-b2c.md (#Chefferie_Projet_et_UX)
2026-10-20 18:59:32,337 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 90ceffc7f4d02bb4 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 18:59:32,337 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : si-tu-te-rapelle-de-certaines-de-nos-dsicussiosn-j.md (#A_Trier)
2026-10-20 19:00:09,430 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 780)). Tentative d'extraction manuelle...
2026-10-20 19:00:09,430 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 5e31d98ef112df15 : Unterminated string starting at: line 16 column 32 (char 780)
2026-10-20 19:00:09,431 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : aide-moi-a-creer-le-script-dun-accompagnement-audi.md (#Marketing_Digital_et_Strategie)
2026-10-20 19:00:30,947 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Hardware_et_Peripheriques`
2026-10-20 19:00:30,948 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-materiel-ayn-thor-vs-azeron-cyborg-2.md (#Gaming_Hardware_et_Peripheriques)
2026-10-20 19:01:05,650 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Marketing_Digital_et_Acquisition`
2026-10-20 19:01:05,651 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-gtm-conversion-astro-jamstack.md (#Marketing_Digital_et_Acquisition)
2026-10-20 19:01:39,478 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Design_Psychologie_Perception`
2026-10-20 19:01:39,478 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : psychophysique-couleur-valence-arousal-ux.md (#Design_Psychologie_Perception)
2026-10-20 19:02:04,886 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 906b56167afcda7b_s01_20261017 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 19:02:04,887 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : est-ce-quavec-hermes-agent-je-suis-censé-pouvoir-g.md (#A_Trier)
2026-10-20 19:02:33,822 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-perte-poids-charge-mentale-picard-overnight-oats.md (#Nutrition_Volume_Eating)
2026-10-20 19:03:00,909 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Carriere_et_Formation_Pro`
2026-10-20 19:03:00,909 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : negociation-administrative-stage-international-pmsmp.md (#Carriere_et_Formation_Pro)
2026-10-20 19:03:24,908 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : validation-diagnostic-tsa-commission-audhd-hpi.md (#Introspection_et_Neuroatypie)
2026-10-20 19:03:51,927 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Esthetique_et_Cognition_Linguistique`
2026-10-20 19:03:51,928 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-cognitive-rime-esthetique-resolution-semantique.md (#Esthetique_et_Cognition_Linguistique)
2026-10-20 19:04:25,215 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : conception-personas-ux-chatbot-ia.md (#Chefferie_Projet_et_UX)
2026-10-20 19:04:49,714 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
synthesized_markdown_body
  Field required [type=missing, input_value={'is_worth_indexing': Tru...ité des Réseaux P2P']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 19:04:49,715 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session b35ecf5567d6c1e1 : 1 validation error for DistilledConceptSchema
synthesized_markdown_body
  Field required [type=missing, input_value={'is_worth_indexing': Tru...ité des Réseaux P2P']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 19:04:49,716 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : bonjour-depuis-deux-jours-il-nest-plus-possible-de.md (#A_Trier)
2026-10-20 19:05:25,904 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-communication-diagnostic-tsa-mdph-aah.md (#Introspection_et_Neuroatypie)
2026-10-20 19:06:03,050 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Expecting property name enclosed in double quotes: line 16 column 2197 (char 2828)). Tentative d'extraction manuelle...
2026-10-20 19:06:03,050 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session c214de50f2d82668_s01_20260924 : Expecting property name enclosed in double quotes: line 16 column 2197 (char 2828)
2026-10-20 19:06:03,051 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : prevalence-et-comorbodité-des-tsas-par-rapport-a-l.md (#A_Trier)
2026-10-20 19:06:28,585 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Droit_Administratif_et_Formation`
2026-10-20 19:06:28,585 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-administratif-stage-formation-vs-pmsmp-suisse.md (#Droit_Administratif_et_Formation)
2026-10-20 19:06:57,088 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...struction du biais de "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 19:06:57,089 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session fe1bbab80fff2038 : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...struction du biais de "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 19:06:57,090 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : parle-moi-en-détail-du-projet-de-planification-éco.md (#Chefferie_Projet_et_UX)
2026-10-20 19:07:14,637 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session b5bb17c263e90034 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 19:07:14,638 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-mais-en-gros-cest-pas-vriament-du-cloud-rap-la.md (#A_Trier)
2026-10-20 19:07:40,110 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Cannabis_Pharmacologie`
2026-10-20 19:07:40,110 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-consommation-cannabis-synergies-cbg-cbd-thc.md (#Sante_Cannabis_Pharmacologie)
2026-10-20 19:08:16,717 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Cuisine_Technique`
2026-10-20 19:08:16,718 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : substitutions-culinaires-proprietes-riz.md (#Cuisine_Technique)
2026-10-20 19:08:41,231 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : decryptage-interaction-administrative-ema-anxiete.md (#Sante_et_Admin_Perso)
2026-10-20 19:09:11,335 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : emergence-qualia-intersubjectivite-philosophique.md (#Metaphysique_et_Physique)
2026-10-20 19:09:49,459 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-section-offre-high-ticket-investissement.md (#Chefferie_Projet_et_UX)
2026-10-20 19:10:16,631 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparaison-politique-socio-economique-asie-europe.md (#Sociologie_et_Politique)
2026-10-20 19:10:43,847 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ux-strategie-conversion-sante-mentale.md (#Chefferie_Projet_et_UX)
2026-10-20 19:11:15,214 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_System_Optimization`
2026-10-20 19:11:15,214 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : diagnostic-bottleneck-cpu-optimisation-micro-stutters.md (#Hardware_System_Optimization)
2026-10-20 19:11:43,724 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-macro-recrutement-mmo.md (#MMORPG_Theorycraft)
2026-10-20 19:12:13,261 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-demographique-deconstruction-subversion-migratoire.md (#Sociologie_et_Politique)
2026-10-20 19:12:38,988 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-design-ui-ux-niche-coaching.md (#Chefferie_Projet_et_UX)
2026-10-20 19:13:05,522 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 57b5f07f67116dc3 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 19:13:05,522 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dou-pensent-tu-que-la-fascination-pour-les-femboys.md (#Philo_Droit_et_Morale)
2026-10-20 19:13:30,667 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : processus-diagnostic-tsa-anamnese-restitution.md (#Introspection_et_Neuroatypie)
2026-10-20 19:14:05,953 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 15 column 32 (char 733)). Tentative d'extraction manuelle...
2026-10-20 19:14:05,953 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 500cc93f69efff33_s01_20260106 : Unterminated string starting at: line 15 column 32 (char 733)
2026-10-20 19:14:05,954 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : avec-15k-de-budgets-on-ne-peut-avoir-quaussi-peu-d.md (#A_Trier)
2026-10-20 19:14:37,703 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session c56c502deb85abdb : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 19:14:37,704 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : jhabite-dans-un-pays-où-les-parents-choisissent-lé.md (#A_Trier)
2026-10-20 19:15:15,656 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 632)). Tentative d'extraction manuelle...
2026-10-20 19:15:15,656 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 3790d98514e3439e_s10_20260305 : Unterminated string starting at: line 16 column 32 (char 632)
2026-10-20 19:15:15,657 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : je-preferes-que-tu-me-genre-des-slides-directement.md (#A_Trier)
2026-10-20 19:15:52,483 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Business_Ops_Automation`
2026-10-20 19:15:52,484 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-tripwire-automatisation-livraison.md (#Business_Ops_Automation)
2026-10-20 19:16:19,868 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-volume-batch-cooking-500kcal.md (#Nutrition_Volume_Eating)
2026-10-20 19:16:52,797 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `IA_Risques_et_Societe`
2026-10-20 19:16:52,799 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-risques-existentiels-scenarios-post-humanite-ia.md (#IA_Risques_et_Societe)
2026-10-20 19:17:30,117 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : reintegration-benevolat-competences-visibilite-passive.md (#Introspection_et_Neuroatypie)
2026-10-20 19:18:00,665 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `IA_Image_Generation`
2026-10-20 19:18:00,665 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : prompt-engineering-echelle-perspective-photorealisme.md (#IA_Image_Generation)
2026-10-20 19:18:29,093 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Marketing_Strategie_Client`
2026-10-20 19:18:29,094 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : segmentation-personas-marketing-b2b-b2c.md (#Marketing_Strategie_Client)
2026-10-20 19:18:55,572 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ingenierie-soutenance-orale-narration-strategique.md (#Chefferie_Projet_et_UX)
2026-10-20 19:19:18,046 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...na systématique (ex: "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 19:19:18,046 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 00e0a27c9543c861 : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...na systématique (ex: "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 19:19:18,048 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : est-ce-que-le-parallel-agentic-work-est-la-norme-e.md (#A_Trier)
2026-10-20 19:19:48,302 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Economie_Politique`
2026-10-20 19:19:48,303 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : deconstruction-paradigmes-economiques-inegalites-capital-ruissellement.md (#Economie_Politique)
2026-10-20 19:20:21,499 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dysfonction-executive-paradoxe-liberte-audhd.md (#Introspection_et_Neuroatypie)
2026-10-20 19:21:00,410 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : epistemologie-feminisme-verite-situee-expertise.md (#Sociologie_et_Politique)
2026-10-20 19:21:40,618 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 695)). Tentative d'extraction manuelle...
2026-10-20 19:21:40,618 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session cc82553ae929d49e_s03_20261018 : Unterminated string starting at: line 16 column 32 (char 695)
2026-10-20 19:21:40,619 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-cest-bon-jai-trouver-mon-projet-ça-va-etre-daut.md (#Chefferie_Projet_et_UX)
2026-10-20 19:22:20,016 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `IA_Cognition_et_Neurosciences`
2026-10-20 19:22:20,017 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : paradigmes-ia-symbolisme-connexionnisme-espace-latent.md (#IA_Cognition_et_Neurosciences)
2026-10-20 19:22:53,958 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Marketing_Digital_et_Analytics`
2026-10-20 19:22:53,959 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-tracking-ga4-google-ads-diagnostic.md (#Marketing_Digital_et_Analytics)
2026-10-20 19:23:15,406 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : determinisme-vs-indeterminisme-interaction-quantique.md (#Metaphysique_et_Physique)
2026-10-20 19:23:48,435 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : mutation-marche-hardware-ia-vs-consumer.md (#LLM_Local_et_Hardware)
2026-10-20 19:24:20,097 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Vaping_Extraction`
2026-10-20 19:24:20,098 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-extraction-dynamique-vaping.md (#Sante_Vaping_Extraction)
2026-10-20 19:24:45,421 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : epistemologie-droit-normatif-vs-sociologie-empirique.md (#Philo_Droit_et_Morale)
2026-10-20 19:25:02,722 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru... immédiat, expansion "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 19:25:02,723 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session f8d4de2191898fe5 : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru... immédiat, expansion "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 19:25:02,724 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-lets-say-the-infinite-universe-theory-is-true-d.md (#A_Trier)
2026-10-20 19:25:44,203 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 668)). Tentative d'extraction manuelle...
2026-10-20 19:25:44,203 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 78e36f02b157b3ec : Unterminated string starting at: line 16 column 32 (char 668)
2026-10-20 19:25:44,204 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : a-quel-point-un-regime-low-fodmap-est-il-vraiment.md (#A_Trier)
2026-10-20 19:26:12,982 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : deconstruction-isomorphisme-effort-souffrance.md (#Philo_Droit_et_Morale)
2026-10-20 19:26:50,265 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Finance_Gestion_Patrimoniale`
2026-10-20 19:26:50,266 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-patrimoniale-demembrement-sci-donation-partage.md (#Finance_Gestion_Patrimoniale)
2026-10-20 19:27:21,891 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 3 column 20 (char 50)). Tentative d'extraction manuelle...
2026-10-20 19:27:21,891 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 3790d98514e3439e_s02_20260128 : Unterminated string starting at: line 3 column 20 (char 50)
2026-10-20 19:27:21,892 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-adapter-a-ma-sheet-la-formule-donne-ça-pour-le.md (#A_Trier)
2026-10-20 19:27:55,118 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Dev_Cloud_Storage`
2026-10-20 19:27:55,118 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : distribution-fichiers-payants-cloudflare-r2-vercel.md (#Dev_Cloud_Storage)
2026-10-20 19:28:25,722 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-acquisition-vs-conversion.md (#Freelance_et_Acquisition)
2026-10-20 19:28:52,110 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Infrastructure_Email_et_DNS`
2026-10-20 19:28:52,111 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : configuration-authentification-email-brevo-infomaniak.md (#Infrastructure_Email_et_DNS)
2026-10-20 19:29:13,116 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : erosion-agency-charge-cognitive-healer-mplus.md (#MMORPG_Theorycraft)
2026-10-20 19:29:50,510 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Loisirs_JDR_Tabletop`
2026-10-20 19:29:50,511 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparatif-systemes-jdr-initiation-familiale.md (#Loisirs_JDR_Tabletop)
2026-10-20 19:30:29,511 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : modelisation-cognitive-espace-latent-esthetique-complexite.md (#Introspection_et_Neuroatypie)
2026-10-20 19:30:57,960 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : profilage-architecture-cognitive-architecte-vs-executant.md (#Introspection_et_Neuroatypie)
2026-10-20 19:31:27,287 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-camus-federalisme-fait-accompli-coexistence.md (#Sociologie_et_Politique)
2026-10-20 19:31:58,634 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Entrepreneuriat_Gestion_Startup`
2026-10-20 19:31:58,635 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : standardisation-selection-agence-marketing-rfp-scoring.md (#Entrepreneuriat_Gestion_Startup)
2026-10-20 19:32:30,150 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : modelisation-consommation-gestion-stock-cannabis.md (#Sante_et_Admin_Perso)
2026-10-20 19:32:54,590 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : gestion-urgence-dentaire-progression-infection.md (#Sante_et_Admin_Perso)
2026-10-20 19:33:26,708 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Carriere_Formation_et_Strategie`
2026-10-20 19:33:26,709 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-montée-compétences-data-financement-france-travail.md (#Carriere_Formation_et_Strategie)
2026-10-20 19:33:58,041 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : modelisation-neurobiologique-save-scumming-hpi-tsa.md (#Introspection_et_Neuroatypie)
2026-10-20 19:34:27,112 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Theorycraft_et_Sociologie`
2026-10-20 19:34:27,113 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : deconstruction-difficult-reception-fear-hunger.md (#Gaming_Theorycraft_et_Sociologie)
2026-10-20 19:35:01,983 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 3835e55d835bfc7c_s01_20260910 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 19:35:01,984 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : jai-envie-dacquerir-une-streaming-box-genre-apple.md (#Gaming_Infrastructure_et_Streaming)
2026-10-20 19:35:35,950 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-demarche-mdph-aah-gestion-surcharge-tsa.md (#Introspection_et_Neuroatypie)
2026-10-20 19:35:57,241 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...des utilisateurs (ex: "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 19:35:57,242 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 0934ff6c7fb95a1c_s01_20260202 : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...des utilisateurs (ex: "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 19:35:57,243 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-demain-je-commence-mon-stage-pour-une-entrepris.md (#Chefferie_Projet_et_UX)
2026-10-20 19:36:20,024 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-pedanterie-linguistique-insultes-esprit.md (#Linguistique_et_Culture_Web)
2026-10-20 19:36:45,295 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 3474819659a51a32 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 19:36:45,296 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : is-there-a-gacha-component-to-where-winds-meet.md (#A_Trier)
2026-10-20 19:37:19,305 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : consommation-horreur-dread-vs-shock.md (#Introspection_et_Neuroatypie)
2026-10-20 19:37:50,703 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-soutenance-roadmap-arbitrages.md (#Chefferie_Projet_et_UX)
2026-10-20 19:38:21,002 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : methodologies-fast-forward-moteurs-emulation.md (#Gaming_Solo_et_Modding)
2026-10-20 19:38:55,004 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : chainement-audio-meditation-eq-compression.md (#Analyse_Musicale_et_MAO)
2026-10-20 19:39:32,376 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : taxonomie-consommation-narrative-fast-food-vs-gourmet.md (#Webtoons_Manga_et_Anime)
2026-10-20 19:40:04,815 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Neurosciences_et_Cognition`
2026-10-20 19:40:04,815 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-bande-passante-cognitive-accélération-media.md (#Neurosciences_et_Cognition)
2026-10-20 19:40:40,950 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 786)). Tentative d'extraction manuelle...
2026-10-20 19:40:40,950 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 3790d98514e3439e_s03_20260128 : Unterminated string starting at: line 16 column 32 (char 786)
2026-10-20 19:40:40,951 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : il-me-faudrait-combien-idealmeent-en-budget-market.md (#Marketing_Conversion_et_Ads)
2026-10-20 19:41:14,461 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 623)). Tentative d'extraction manuelle...
2026-10-20 19:41:14,462 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 9140f4c4e251214d_s03_20251126 : Unterminated string starting at: line 16 column 32 (char 623)
2026-10-20 19:41:14,463 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-un-prompt-suno-pour-de-lhyperpop-jersey-kpop-re.md (#Prompt_Engineering_et_Suno)
2026-10-20 19:41:46,189 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Marketing_Conversion_Automation`
2026-10-20 19:41:46,189 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-conversion-automatisation-funnels-pnl.md (#Marketing_Conversion_Automation)
2026-10-20 19:42:18,015 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...d réseau ne peut pas "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 19:42:18,016 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 4f39e8da039fad66 : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...d réseau ne peut pas "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 19:42:18,017 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : wifi-5-suffisant-pour-du-cloud-local-via-apollo-ar.md (#LLM_Local_et_Hardware)
2026-10-20 19:42:59,409 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Expecting value: line 1 column 1 (char 0)). Tentative d'extraction manuelle...
2026-10-20 19:42:59,409 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 24413b0b7f201835_s18_20260901 : Expecting value: line 1 column 1 (char 0)
2026-10-20 19:42:59,410 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : jai-recup-un-adaptateur-et-un-mini-bubbler-du-coup.md (#A_Trier)
2026-10-20 19:43:34,668 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Gestion_Habitudes`
2026-10-20 19:43:34,668 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : gestion-transition-consommation-remplacement-sas.md (#Sante_Gestion_Habitudes)
2026-10-20 19:44:05,423 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-r2-vercel-conversion-segmentee.md (#Dev_Web_et_Stack_Astro)
2026-10-20 19:44:30,739 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-optimisation-dossier-mdph-aah-hpi-autisme.md (#Sante_et_Admin_Perso)
2026-10-20 19:45:09,091 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `GameDesign_MOBA_Macro`
2026-10-20 19:45:09,092 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : conception-simulateur-moba-macro-tactile.md (#GameDesign_MOBA_Macro)
2026-10-20 19:45:46,669 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 788)). Tentative d'extraction manuelle...
2026-10-20 19:45:46,669 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 0934ff6c7fb95a1c_s09_20260204 : Unterminated string starting at: line 16 column 32 (char 788)
2026-10-20 19:45:46,670 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comment-me-conseilles-tu-de-gerer-le-hsoting-des-f.md (#A_Trier)
2026-10-20 19:46:20,407 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Business_Strategie_Coaching`
2026-10-20 19:46:20,407 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-pricing-tunnel-vente-coaching.md (#Business_Strategie_Coaching)
2026-10-20 19:46:49,795 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_SystemTroubleshooting`
2026-10-20 19:46:49,796 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : diagnostic-micro-gels-systeme-latence-dpc.md (#Hardware_SystemTroubleshooting)
2026-10-20 19:47:18,168 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : workflow-mixx-pop-suno-genre-switch.md (#Prompt_Engineering_et_Suno)
2026-10-20 19:47:55,005 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_PC_Troubleshooting`
2026-10-20 19:47:55,006 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : diagnostic-throttling-vrm-instabilite-ram.md (#Hardware_PC_Troubleshooting)
2026-10-20 19:48:30,540 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `MMORPG_Dev_Tools`
2026-10-20 19:48:30,540 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : tracking-performances-mplus-warcraft-logs-api.md (#MMORPG_Dev_Tools)
2026-10-20 19:48:48,319 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 5507d571ad00a429_s03_20260416 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 19:48:48,319 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : au-niveau-de-lanalyse-bilan-personnel-pour-la-slid.md (#Chefferie_Projet_et_UX)
2026-10-20 19:49:15,257 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 662)). Tentative d'extraction manuelle...
2026-10-20 19:49:15,257 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session b826e37a3ce5ab5c : Unterminated string starting at: line 16 column 32 (char 662)
2026-10-20 19:49:15,258 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : peut-tu-me-faire-un-tableur-mettant-en-relation-le.md (#A_Trier)
2026-10-20 19:49:45,785 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dynamiques-friction-cognitive-dependance-comportementale.md (#Introspection_et_Neuroatypie)
2026-10-20 19:50:19,554 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Marketing_Growth_Strategy`
2026-10-20 19:50:19,554 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-marketing-digital-roi-hotel-luxe.md (#Marketing_Growth_Strategy)
2026-10-20 19:50:54,676 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Psychologie_Psychometrie`
2026-10-20 19:50:54,677 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : deconstruction-biais-mesure-qi-facteurs-environnementaux.md (#Psychologie_Psychometrie)
2026-10-20 19:51:20,122 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : pipeline-recherche-transformation-pedagogique.md (#Prompt_Engineering_et_Suno)
2026-10-20 19:51:56,103 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 775)). Tentative d'extraction manuelle...
2026-10-20 19:51:56,103 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 24413b0b7f201835_s28_20260913 : Unterminated string starting at: line 16 column 32 (char 775)
2026-10-20 19:51:56,104 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : quid-du-arizer-go-srt.md (#A_Trier)
2026-10-20 19:52:33,031 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 15 column 32 (char 725)). Tentative d'extraction manuelle...
2026-10-20 19:52:33,031 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 05cebac9a4454fa6 : Unterminated string starting at: line 15 column 32 (char 725)
2026-10-20 19:52:33,032 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : pourquoi-un-sirop-a-la-maison-ne-donne-jamais-vrai.md (#Culture_Kpop_et_Industrie_Media)
2026-10-20 19:52:55,185 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 61a39dc3fea08429_s02_20260109 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 19:52:55,186 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comment-je-pourrais-adapter-lintitulé-au-format-fr.md (#Freelance_et_Acquisition)
2026-10-20 19:53:24,076 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : methodologie-pitch-deck-alignement-strategique-technique.md (#Chefferie_Projet_et_UX)
2026-10-20 19:53:53,504 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_DataAnalysis`
2026-10-20 19:53:53,505 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-statistique-impact-nerfs-lol.md (#Gaming_DataAnalysis)
2026-10-20 19:54:19,457 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dissonance-ideaux-individuels-regulation-sociale.md (#Sociologie_et_Politique)
2026-10-20 19:54:51,898 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Simulation_Engine`
2026-10-20 19:54:51,900 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-simulateur-degats-lol-meraki.md (#Gaming_Simulation_Engine)
2026-10-20 19:55:22,172 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : upgrade-intel-lga1700-preservation-ddr4.md (#LLM_Local_et_Hardware)
2026-10-20 19:55:48,068 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ingenierie-paroles-suno-digicore-breakcore.md (#Prompt_Engineering_et_Suno)
2026-10-20 19:56:31,041 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 744)). Tentative d'extraction manuelle...
2026-10-20 19:56:31,041 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 24413b0b7f201835_s01_20260810 : Unterminated string starting at: line 16 column 32 (char 744)
2026-10-20 19:56:31,042 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-on-va-commencer-mon-journal-de-vaping-dans-cett.md (#Sante_Vaping_Extraction)
2026-10-20 19:56:53,127 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : plausibilite-logique-anxiete-simulation-tsa.md (#Introspection_et_Neuroatypie)
2026-10-20 19:57:16,026 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : workflow-mao-maschine-koii-time-stretching.md (#Analyse_Musicale_et_MAO)
2026-10-20 19:57:47,096 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Culture_Tech_et_IA`
2026-10-20 19:57:47,096 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : poweruserslop-esthetique-competence-complexite.md (#Culture_Tech_et_IA)
2026-10-20 19:58:22,953 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `SoftSkills_Communication_Pro`
2026-10-20 19:58:22,953 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : protocole-communication-email-etudiant-administration.md (#SoftSkills_Communication_Pro)
2026-10-20 19:59:02,363 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparaison-evolution-pokemon-digimon.md (#Webtoons_Manga_et_Anime)
2026-10-20 19:59:28,197 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
synthesized_markdown_body
  Field required [type=missing, input_value={'is_worth_indexing': Tru...n Media via Arr-Stack']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 19:59:28,197 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 7b59d8d3da4143bb_s01_20260830 : 1 validation error for DistilledConceptSchema
synthesized_markdown_body
  Field required [type=missing, input_value={'is_worth_indexing': Tru...n Media via Arr-Stack']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 19:59:28,198 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : stremio-est-il-toujours-la-meilleur-solution-pour.md (#A_Trier)
2026-10-20 20:00:07,614 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Systemic_et_IA`
2026-10-20 20:00:07,614 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : paradigme-observateur-4d-lecture-jdr-ia.md (#Gaming_Systemic_et_IA)
2026-10-20 20:00:39,981 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `GameDev_Incremental_Engine`
2026-10-20 20:00:39,982 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-moteur-jeu-incremental-3d-headless.md (#GameDev_Incremental_Engine)
2026-10-20 20:01:17,705 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gestion_Projet_Tech`
2026-10-20 20:01:17,706 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : cadrage-budget-recrutement-app-mobile.md (#Gestion_Projet_Tech)
2026-10-20 20:01:40,970 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : gestion-parcours-mdph-coordination-medicale.md (#Sante_et_Admin_Perso)
2026-10-20 20:02:20,667 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Freelance_Positionnement_IA`
2026-10-20 20:02:20,668 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : micro-entrepreneuriat-post-llm-orchestration.md (#Freelance_Positionnement_IA)
2026-10-20 20:02:48,472 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Lifestyle_Vaping_Hardware`
2026-10-20 20:02:48,472 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparaison-kroma-z-geekvape-z-nano-effet-puff.md (#Lifestyle_Vaping_Hardware)
2026-10-20 20:03:21,867 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-forensique-copypastas-obfuscation-traduction.md (#Linguistique_et_Culture_Web)
2026-10-20 20:03:42,151 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session fc40a0f2cccecc6b : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 20:03:42,152 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : how-hard-owuld-it-be-to-make-a-device-similar-to-t.md (#A_Trier)
2026-10-20 20:04:07,696 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Dev_DataViz_Interactive`
2026-10-20 20:04:07,697 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : visualisation-interactive-systemes-complexes-html-js.md (#Dev_DataViz_Interactive)
2026-10-20 20:04:47,387 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Neurobiologie_Substances`
2026-10-20 20:04:47,388 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : neurobiologie-tolerance-sevrage-cannabinoide.md (#Sante_Neurobiologie_Substances)
2026-10-20 20:05:08,548 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : taxonomy-manhwa-consumption-fast-food-vs-gourmet.md (#Webtoons_Manga_et_Anime)
2026-10-20 20:05:41,386 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Cognition_Apprentissage_Langues`
2026-10-20 20:05:41,387 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : neuroplasticite-apprentissage-langues-neuroatypique.md (#Cognition_Apprentissage_Langues)
2026-10-20 20:06:15,441 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : gw2-gear-optimization-celestial-vs-specialized.md (#MMORPG_Theorycraft)
2026-10-20 20:06:44,013 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-ergonomie-conversationnelle-psychometrie-llm.md (#IA_LLM_Psychométrie_et_Style)
2026-10-20 20:07:07,969 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : transition-hm-mm-sondage-roster.md (#MMORPG_Theorycraft)
2026-10-20 20:07:39,790 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 15 column 32 (char 687)). Tentative d'extraction manuelle...
2026-10-20 20:07:39,790 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 141940775be9a621 : Unterminated string starting at: line 15 column 32 (char 687)
2026-10-20 20:07:39,791 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : quel-diff-entre-i206-et-i208.md (#A_Trier)
2026-10-20 20:08:06,122 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Community_Management`
2026-10-20 20:08:06,123 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-recrutement-guilde-social-midcore.md (#Gaming_Community_Management)
2026-10-20 20:08:34,630 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Handheld_Hardware`
2026-10-20 20:08:34,631 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-ergonomie-dual-screen-retroid-ayn.md (#Gaming_Handheld_Hardware)
2026-10-20 20:09:06,296 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-hardware-strategie-business-llm.md (#LLM_Local_et_Hardware)
2026-10-20 20:09:34,197 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Industry_Theory`
2026-10-20 20:09:34,198 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-divergence-moba-pc-vs-mobile.md (#Gaming_Industry_Theory)
2026-10-20 20:10:12,868 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Economie_Logistique_et_Finance`
2026-10-20 20:10:12,869 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ingenierie-dissolution-capital-flux-30-jours.md (#Economie_Logistique_et_Finance)
2026-10-20 20:10:52,034 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 16 column 32 (char 746)). Tentative d'extraction manuelle...
2026-10-20 20:10:52,034 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 620d8e0295db2c39 : Unterminated string starting at: line 16 column 32 (char 746)
2026-10-20 20:10:52,035 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : how-to-check-whether-smthyperthreading-is-on-or-of.md (#A_Trier)
2026-10-20 20:11:20,690 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_RemoteAccess`
2026-10-20 20:11:20,690 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-remote-wol-windows-autologin.md (#Hardware_RemoteAccess)
2026-10-20 20:11:53,042 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Epidemiologie_et_Causalite`
2026-10-20 20:11:53,043 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : distinction-causalite-directe-facteur-risque.md (#Sante_Epidemiologie_et_Causalite)
2026-10-20 20:12:18,866 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : aphantasie-dissociation-spatiale-visuelle.md (#Introspection_et_Neuroatypie)
2026-10-20 20:12:50,767 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-ia-sovereine-eco-conçue-rag-chainlit.md (#IA_Agentique_et_RAG)
2026-10-20 20:13:26,686 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 15 column 32 (char 753)). Tentative d'extraction manuelle...
2026-10-20 20:13:26,686 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 9db78a9846f8d553_s03_20261004 : Unterminated string starting at: line 15 column 32 (char 753)
2026-10-20 20:13:26,687 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : is-garden-map-farming-owrth.md (#A_Trier)
2026-10-20 20:13:51,249 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparative-socio-economics-us-states-resilience.md (#Sociologie_et_Politique)
2026-10-20 20:14:18,737 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Maintenance_Electromenagers`
2026-10-20 20:14:18,737 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : reparation-manchette-lave-linge.md (#Maintenance_Electromenagers)
2026-10-20 20:14:46,958 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Emulation_Performance`
2026-10-20 20:14:46,958 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-fluidite-lsfg-mobile-pc-emulation-switch.md (#Gaming_Emulation_Performance)
2026-10-20 20:15:16,436 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Nutrition_GestionSensorielle`
2026-10-20 20:15:16,436 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-culinaire-gestion-aversions-sensorielles.md (#Nutrition_GestionSensorielle)
2026-10-20 20:15:39,174 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sport_Strategie_et_Tactique`
2026-10-20 20:15:39,174 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-complexite-strategique-kinball-foot-us.md (#Sport_Strategie_et_Tactique)
2026-10-20 20:16:08,167 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : benchmark-selection-outils-gestion-projet-hello-hercule.md (#Chefferie_Projet_et_UX)
2026-10-20 20:16:34,310 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_Networking`
2026-10-20 20:16:34,311 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : depannage-routeur-5g-meteor-dns-cloud-ui.md (#Hardware_Networking)
2026-10-20 20:17:07,255 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Usage_Vaporisation_Cannabis`
2026-10-20 20:17:07,256 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-vaporisation-resine-valorisation-avb.md (#Usage_Vaporisation_Cannabis)
2026-10-20 20:17:36,915 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : critique-sociologique-achat-comptant.md (#Sociologie_et_Politique)
2026-10-20 20:18:01,027 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : prompt-engineering-coach-entrepreneurial-realiste.md (#Prompt_Engineering_et_Suno)
2026-10-20 20:18:34,242 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : theorie-extreme-centre-tripartition-politique.md (#Sociologie_et_Politique)
2026-10-20 20:18:54,415 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-linguistique-agentivite-invisibilisation-agresseur.md (#Linguistique_et_Culture_Web)
2026-10-20 20:19:30,918 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Expecting value: line 19 column 28 (char 2853)). Tentative d'extraction manuelle...
2026-10-20 20:19:30,918 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 179c4b27f756e97a_s01_20260330 : Expecting value: line 19 column 28 (char 2853)
2026-10-20 20:19:30,919 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : la-oslution-que-tu-porpose-est-uniquement-le-masqu.md (#A_Trier)
2026-10-20 20:19:53,300 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 0b1375f48429a389 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 20:19:53,309 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : quel-est-la-meilleure-manière-de-retirer-la-viande.md (#A_Trier)
2026-10-20 20:20:22,598 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Cuisine_Equipement_et_Techniques`
2026-10-20 20:20:22,598 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-cuisson-riz-multicuiseur-vs-rice-cooker.md (#Cuisine_Equipement_et_Techniques)
2026-10-20 20:20:52,064 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-dualite-narrative-erikson-sanderson.md (#Culture_Littéraire_et_Fantasy)
2026-10-20 20:21:11,510 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : meta-prompting-rag-sota-generation.md (#IA_Agentique_et_RAG)
2026-10-20 20:21:37,153 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-autocrafting-refined-storage-litematica.md (#Gaming_Solo_et_Modding)
2026-10-20 20:22:01,594 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-consommation-cannabinoïdes-dose-materiel-cbd-thc.md (#Sante_Pharmacologie_Cannabinoïdes)
2026-10-20 20:22:30,463 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : developpement-plugins-midi-logiques-workflow-ableton-move.md (#Analyse_Musicale_et_MAO)
2026-10-20 20:22:46,499 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...de la texture sonore ("}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 20:22:46,499 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 9140f4c4e251214d_s04_20251127 : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...de la texture sonore ("}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 20:22:46,500 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-on-retourne-sur-de-la-kpop-en-coreen-hangeul-av.md (#Sante_et_Admin_Perso)
2026-10-20 20:23:20,575 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Expecting value: line 9 column 25 (char 424)). Tentative d'extraction manuelle...
2026-10-20 20:23:20,575 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session ff14a41f15afb390_s02_20260105 : Expecting value: line 9 column 25 (char 424)
2026-10-20 20:23:20,576 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ou-se-situent-les-civ-pre-colombienne-sur-la-grand.md (#A_Trier)
2026-10-20 20:23:49,850 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : dissonance-narrative-clip-free-bird.md (#Analyse_Musicale_et_MAO)
2026-10-20 20:24:14,581 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_Maintenance_PC`
2026-10-20 20:24:14,582 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : diagnostic-resolution-throttling-vrm.md (#Hardware_Maintenance_PC)
2026-10-20 20:24:38,951 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : physiologie-rgo-micro-aspiration.md (#Sante_et_Admin_Perso)
2026-10-20 20:25:03,333 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Handheld_et_Hardware`
2026-10-20 20:25:03,334 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : gaming-pc-arm-emulation-vs-streaming.md (#Gaming_Handheld_et_Hardware)
2026-10-20 20:25:38,295 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_PC_et_Troubleshooting`
2026-10-20 20:25:38,296 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-upgrade-cpu-intel-vs-amd-am4-x3d.md (#Hardware_PC_et_Troubleshooting)
2026-10-20 20:26:09,769 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-incremental-tech-abstraction-industrielle.md (#GameDesign_Systems)
2026-10-20 20:26:36,771 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-financement-formation-rfft-rqth-agefiph.md (#Sante_et_Admin_Perso)
2026-10-20 20:27:10,599 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Cuisine_Technique_et_Chimie`
2026-10-20 20:27:10,600 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-texture-emulsion-gnocchi-pates.md (#Cuisine_Technique_et_Chimie)
2026-10-20 20:27:41,091 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Finance_Gestion_Patrimoine`
2026-10-20 20:27:41,091 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : modelisation-independance-financiere-rente-3m.md (#Finance_Gestion_Patrimoine)
2026-10-20 20:28:04,209 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparatif-samplers-hardware-workflow-chromatique.md (#Analyse_Musicale_et_MAO)
2026-10-20 20:28:34,429 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Informatique_Recuperation_Donnees`
2026-10-20 20:28:34,430 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : recuperation-donnees-sage-50-suisse-panne-materielle.md (#Informatique_Recuperation_Donnees)
2026-10-20 20:29:00,207 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 6041411ab410da2d : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 20:29:00,207 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : je-veux-faire-du-riz-a-sushi-pour-ce-soir-avec-mon.md (#A_Trier)
2026-10-20 20:29:19,234 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparaison-paradigmes-progression-fluidite-mmorpg.md (#MMORPG_Theorycraft)
2026-10-20 20:29:42,343 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_ActualPlay_Culture`
2026-10-20 20:29:42,344 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : genealogie-terminologie-actual-play-francophone.md (#Gaming_ActualPlay_Culture)
2026-10-20 20:30:06,741 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : plan-recrutement-structuration-equipe-mvp-hello-hercule.md (#Chefferie_Projet_et_UX)
2026-10-20 20:30:31,556 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Finance_Immobilier_Patrimoine`
2026-10-20 20:30:31,557 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-placement-vs-achat-immobilier-hcsf.md (#Finance_Immobilier_Patrimoine)
2026-10-20 20:30:58,297 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ethique-oisivete-dividende-technologique.md (#Philo_Droit_et_Morale)
2026-10-20 20:31:24,415 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `IA_Video_Generation`
2026-10-20 20:31:24,415 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : prompt-engineering-asmr-textures-rupture-veo.md (#IA_Video_Generation)
2026-10-20 20:31:52,134 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : workflow-production-hyperpop-digicore-maschine-mk2.md (#Analyse_Musicale_et_MAO)
2026-10-20 20:32:17,867 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Animaux_Comportement_et_Soins`
2026-10-20 20:32:17,867 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : gestion-cohabitation-felines-chaton-orphelin-apathie-adulte.md (#Animaux_Comportement_et_Soins)
2026-10-20 20:32:39,350 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
synthesized_markdown_body
  Field required [type=missing, input_value={'is_worth_indexing': Tru...aturation sensorielle']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 20:32:39,350 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 6c6f327764688e3b_s02_20260212 : 1 validation error for DistilledConceptSchema
synthesized_markdown_body
  Field required [type=missing, input_value={'is_worth_indexing': Tru...aturation sensorielle']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 20:32:39,351 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : jai-fait-une-marinade-pour-les-hauts-de-cuisse-pap.md (#A_Trier)
2026-10-20 20:33:04,201 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Input_Mechanics`
2026-10-20 20:33:04,202 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-input-mapping-manette-tactile.md (#Gaming_Input_Mechanics)
2026-10-20 20:33:37,131 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Economie_Finances_Personnelles`
2026-10-20 20:33:37,131 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-socio-economique-pouvoir-achat-psychologie-rarete.md (#Economie_Finances_Personnelles)
2026-10-20 20:34:02,958 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_GameDesign`
2026-10-20 20:34:02,959 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-game-design-agence-narration-systemique.md (#Gaming_GameDesign)
2026-10-20 20:34:37,239 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Psychologie_Etats_Conscience`
2026-10-20 20:34:37,240 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : mecanique-cognitive-shifting-dissociation.md (#Psychologie_Etats_Conscience)
2026-10-20 20:35:14,114 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : physique-vaporisation-protocoles-extraction-cbg-cbd.md (#Lifestyle_Vaporisation)
2026-10-20 20:35:39,379 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-absence-integration-memes-statiques.md (#Linguistique_et_Culture_Web)
2026-10-20 20:36:07,220 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Cannabis_Vape`
2026-10-20 20:36:07,220 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : protocoles-vaporisation-cbd-thc-gestion-avb.md (#Sante_Cannabis_Vape)
2026-10-20 20:36:28,159 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `GameDev_Architecture_et_Pipeline`
2026-10-20 20:36:28,160 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-data-driven-pipeline-assets-unity-collection-game.md (#GameDev_Architecture_et_Pipeline)
2026-10-20 20:36:55,941 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 3790d98514e3439e_s11_20260305 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 20:36:55,942 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : je-souhaiterais-rajouter-deux-slides-une-premiere.md (#Marketing_Conversion_et_Ads)
2026-10-20 20:37:30,073 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Unterminated string starting at: line 15 column 32 (char 827)). Tentative d'extraction manuelle...
2026-10-20 20:37:30,073 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 5c19ab409346282d : Unterminated string starting at: line 15 column 32 (char 827)
2026-10-20 20:37:30,074 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : tu-peux-retrouver-la-discussion-dans-laquelle-nous.md (#Psychologie_Etats_Conscience)
2026-10-20 20:38:00,034 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ethique-audace-externalisation-couts-sociaux.md (#Sociologie_et_Politique)
2026-10-20 20:38:29,729 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_Optimisation_Professionnelle`
2026-10-20 20:38:29,730 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-materiel-pc-sage-50.md (#Hardware_Optimisation_Professionnelle)
2026-10-20 20:39:00,221 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Habitat_Maintenance_et_Parasites`
2026-10-20 20:39:00,221 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : diagnostic-traitement-infestation-vrillettes.md (#Habitat_Maintenance_et_Parasites)
2026-10-20 20:39:32,430 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-systemique-dilemme-escargot-mortel.md (#Logique_Modélisation_Systémique)
2026-10-20 20:39:57,520 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `HomeLab_Infrastructure`
2026-10-20 20:39:57,520 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-energetique-pc-vs-mini-pc-n100-serveur.md (#HomeLab_Infrastructure)
2026-10-20 20:40:30,832 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-hybride-chatbot-ecommerce-chainlit-rag-api.md (#IA_Agentique_et_RAG)
2026-10-20 20:40:52,382 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : mixage-vocal-meditation-traitement-signal.md (#Analyse_Musicale_et_MAO)
2026-10-20 20:41:26,015 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-couch-lock-thc-cbd-cbn.md (#Santé_CannabisPharmacologie)
2026-10-20 20:41:52,264 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Epistemologie_Expertise`
2026-10-20 20:41:52,265 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : epistemologie-expertise-theorique-vs-pratique.md (#Epistemologie_Expertise)
2026-10-20 20:42:23,567 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_AutoBattler_Strategy`
2026-10-20 20:42:23,568 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : tft-decision-matrix-set-17.md (#Gaming_AutoBattler_Strategy)
2026-10-20 20:42:55,739 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-musicologique-sociologique-trot-coreen.md (#Analyse_Musicale_et_MAO)
2026-10-20 20:43:20,410 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-archetypes-semiotique-looksmaxxing.md (#Linguistique_et_Culture_Web)
2026-10-20 20:43:51,974 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Dev_Mobile_et_CrossPlatform`
2026-10-20 20:43:51,974 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-pwa-react-native-flutter.md (#Dev_Mobile_et_CrossPlatform)
2026-10-20 20:44:21,629 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Logique_Algorithmique`
2026-10-20 20:44:21,629 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : algorithme-mesure-temporelle-sabliers-4-7.md (#Logique_Algorithmique)
2026-10-20 20:44:53,829 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Incremental_Theorycraft`
2026-10-20 20:44:53,830 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-progression-farming-trimps.md (#Gaming_Incremental_Theorycraft)
2026-10-20 20:45:20,018 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Prompt_Engineering_MetaCognition`
2026-10-20 20:45:20,019 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : protocole-oscillation-dialectique-construction-crash-test.md (#Prompt_Engineering_MetaCognition)
2026-10-20 20:45:45,468 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_Maintenance_et_Troubleshooting`
2026-10-20 20:45:45,468 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : diagnostic-panne-ecran-noir-ventilateurs-100.md (#Hardware_Maintenance_et_Troubleshooting)
2026-10-20 20:46:12,098 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `DIY_Menuiserie_Structure`
2026-10-20 20:46:12,099 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-structurelle-plateau-bureau-assis-debout.md (#DIY_Menuiserie_Structure)
2026-10-20 20:46:38,506 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : taxonomie-narrative-connoisseur-manga.md (#Webtoons_Manga_et_Anime)
2026-10-20 20:46:58,227 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : framework-presentation-bilan-competences-chef-projet.md (#Chefferie_Projet_et_UX)
2026-10-20 20:47:27,194 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...ion d'une approche de "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 20:47:27,194 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 9c7eed1b336ac46d : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...ion d'une approche de "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 20:47:27,195 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : est-ce-quil-est-pertinent-de-creer-une-sorte-de-pe.md (#A_Trier)
2026-10-20 20:47:52,550 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_BoardGames`
2026-10-20 20:47:52,551 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-comparative-jeux-plateau-feeling-jdr-strategie.md (#Gaming_BoardGames)
2026-10-20 20:48:19,436 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-streaming-moonlight-reseau-stockage.md (#HomeLab_MediaServer)
2026-10-20 20:48:51,776 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : protocole-soins-post-extraction-dentaire.md (#Sante_et_Admin_Perso)
2026-10-20 20:49:15,073 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Cuisine_Science_et_Technique`
2026-10-20 20:49:15,074 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-culinaire-equilibre-organoleptique-physique-textures.md (#Cuisine_Science_et_Technique)
2026-10-20 20:49:42,052 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `OS_Windows_Optimization`
2026-10-20 20:49:42,052 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : diagnostic-charge-cpu-telemetrie-windows.md (#OS_Windows_Optimization)
2026-10-20 20:50:11,735 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Nutrition_SensoryScience`
2026-10-20 20:50:11,736 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : physiologie-chimie-transition-zero-sucre.md (#Nutrition_SensoryScience)
2026-10-20 20:50:33,788 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : methodologie-description-symptomes-visuels-aura-migraineuse.md (#Sante_et_Admin_Perso)
2026-10-20 20:51:01,755 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-handheld-android-snapdragon-8-gen-2-vs-3.md (#Gaming_Handheld_Hardware)
2026-10-20 20:51:33,708 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-vaporisation-fleur-vs-resine.md (#Lifestyle_Vaporisation)
2026-10-20 20:51:56,845 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : unification-domotique-synology-home-assistant.md (#HomeLab_MediaServer)
2026-10-20 20:52:18,083 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-organoleptique-fonctionnelle-konjac.md (#Nutrition_Volume_Eating)
2026-10-20 20:52:38,383 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...vation/culpabilité (*"}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 20:52:38,384 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 9995eb046939d6cd_s05_20250822 : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...vation/culpabilité (*"}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 20:52:38,385 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : donne-moi-des-idees-pour-des-sauces-hypocaloriques.md (#A_Trier)
2026-10-20 20:53:15,667 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Dev_Web_Accessibility`
2026-10-20 20:53:15,668 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : accessibilite-web-alt-text-aria-mat-icon.md (#Dev_Web_Accessibility)
2026-10-20 20:53:38,635 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 7a3ea9720e660e52 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 20:53:38,636 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : how-come-blackpink-is-so-low-in-the-awards-ranking.md (#A_Trier)
2026-10-20 20:54:05,545 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `DevOps_Cloud_Infrastructure`
2026-10-20 20:54:05,546 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-distribution-cloudflare-r2-vercel-astro.md (#DevOps_Cloud_Infrastructure)
2026-10-20 20:54:24,823 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 1dd395ddff1e5f11 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 20:54:24,824 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ok-be-careful-no-spoiler-except-yes-or-no-is-there.md (#A_Trier)
2026-10-20 20:54:53,410 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : protocole-expulsion-protection-mineurs-droit-francais.md (#Philo_Droit_et_Morale)
2026-10-20 20:55:15,433 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-framerate-modding-ips-yuzu.md (#Gaming_Solo_et_Modding)
2026-10-20 20:55:45,825 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Pharmacologie`
2026-10-20 20:55:45,826 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : protocole-vaporisation-hybride-modulation-pharmacologique.md (#Sante_Pharmacologie)
2026-10-20 20:56:11,055 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : securisation-administrative-aah-gestion-anxiete.md (#Sante_et_Admin_Perso)
2026-10-20 20:56:34,894 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 0934ff6c7fb95a1c_s25_20260301 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 20:56:34,895 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : je-veux-que-tu-me-fasses-deux-documents-un-pour-la.md (#A_Trier)
2026-10-20 20:57:03,264 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Loisirs_Vaping_DIY`
2026-10-20 20:57:03,264 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-additifs-refroidissement-ws23-ws3-diy.md (#Loisirs_Vaping_DIY)
2026-10-20 20:57:27,446 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Maison_Gestion_Energie`
2026-10-20 20:57:27,447 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-consommation-chauffage-cet.md (#Maison_Gestion_Energie)
2026-10-20 20:58:05,539 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategie-mdph-rsdae-aah-tsa.md (#Sante_et_Admin_Perso)
2026-10-20 20:58:30,440 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Lifestyle_Vapotage_Technique`
2026-10-20 20:58:30,441 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-rendu-aromatique-puffs-vs-rechargeables.md (#Lifestyle_Vapotage_Technique)
2026-10-20 20:59:00,790 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : gouvernance-technologique-determinisme-latent-manifeste.md (#Sociologie_et_Politique)
2026-10-20 20:59:30,216 [INFO] Exocortex.TakeoutIngestor: Session 32b24dda52d886c3 considérée comme bruit par la distillation.
2026-10-20 20:59:53,023 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : workflow-wordpress-git-deployment-php-debug.md (#Dev_Web_et_Stack_Astro)
2026-10-20 21:00:20,295 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_DRM_ReverseEngineering`
2026-10-20 21:00:20,295 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : denuvo-bypass-steam-session-management.md (#Gaming_DRM_ReverseEngineering)
2026-10-20 21:00:39,730 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-structurelle-socialisme-sud-americain-vs-social-democratie.md (#Sociologie_et_Politique)
2026-10-20 21:01:10,721 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Design_et_Analyse`
2026-10-20 21:01:10,722 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-design-boucle-tactique-sociale-checklist.md (#Gaming_Design_et_Analyse)
2026-10-20 21:01:44,596 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Art_Design_Sensoriel`
2026-10-20 21:01:44,597 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-olfactive-composition-ombre-fusion-profils.md (#Art_Design_Sensoriel)
2026-10-20 21:02:32,978 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Expecting value: line 1 column 1 (char 0)). Tentative d'extraction manuelle...
2026-10-20 21:02:32,978 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 2fe191d379e02dd9_s07_20260923 : Expecting value: line 1 column 1 (char 0)
2026-10-20 21:02:32,979 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ça-représente-quoi-2000-baht-en-proportion-du-sala.md (#Neuroatypie_Admin_France)
2026-10-20 21:02:54,757 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Cuisine_Electromenager`
2026-10-20 21:02:54,758 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparatif-cuiseurs-riz-strategie-achat.md (#Cuisine_Electromenager)
2026-10-20 21:03:21,105 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-ninja-creami-slushy-gestion-metabolique.md (#Nutrition_Volume_Eating)
2026-10-20 21:03:55,517 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : souverainete-cloud-conformite-rgaa-standards-operationnels.md (#Droit_et_Conformite_Numérique)
2026-10-20 21:04:22,269 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Cybersecurite_Piracy_et_Infrastructure`
2026-10-20 21:04:22,270 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : mutation-ddl-infrastructures-infostealers.md (#Cybersecurite_Piracy_et_Infrastructure)
2026-10-20 21:04:46,099 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Immobilier_Gestion_Locative`
2026-10-20 21:04:46,100 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-annonce-airbnb-praz-de-lys.md (#Immobilier_Gestion_Locative)
2026-10-20 21:05:20,171 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (Expecting value: line 1 column 1 (char 0)). Tentative d'extraction manuelle...
2026-10-20 21:05:20,171 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 8d3170b6dd647014 : Expecting value: line 1 column 1 (char 0)
2026-10-20 21:05:20,172 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : est-ce-quen-matiere-de-eliquide-les-arome-concentr.md (#Sante_Cannabis_Vape)
2026-10-20 21:05:47,043 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Audio_HiFi_Hardware`
2026-10-20 21:05:47,043 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : selection-hifi-fiio-ft1-rap-optimisation.md (#Audio_HiFi_Hardware)
2026-10-20 21:06:15,914 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : planet-crafter-midgame-analysis-flooding-design.md (#Gaming_Solo_et_Modding)
2026-10-20 21:06:41,266 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Carriere_Formation_Professionnelle`
2026-10-20 21:06:41,267 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : parcours-certification-animation-direction-loisirs.md (#Carriere_Formation_Professionnelle)
2026-10-20 21:07:02,468 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 87baf2d9a4d00a9c : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 21:07:02,468 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : est-ce-quen-faisant-chauffer-du-cheese-whiz-genre.md (#A_Trier)
2026-10-20 21:07:25,074 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Competitive_Theory`
2026-10-20 21:07:25,074 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-comparative-competitivite-mobile-pc-console.md (#Gaming_Competitive_Theory)
2026-10-20 21:07:45,536 [WARNING] Exocortex.LLM: Échec du parsing initial JSON (1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...ich Text Editing** à "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing). Tentative d'extraction manuelle...
2026-10-20 21:07:45,536 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session f54f6d284ac0ca54 : 1 validation error for DistilledConceptSchema
related_concepts
  Field required [type=missing, input_value={'is_worth_indexing': Tru...ich Text Editing** à "}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
2026-10-20 21:07:45,537 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : salut-toi-est-ce-quon-peut-qualifier-de-wysiwyg-un.md (#A_Trier)
2026-10-20 21:08:04,147 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 8cc95c9714f6e74a : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 21:08:04,147 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : fais-moi-un-son-sur-kc-vs-kcb-en-lec.md (#A_Trier)
2026-10-20 21:08:30,738 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Pharmacologie_Substances`
2026-10-20 21:08:30,738 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-vaporisation-densite-saturation-cb1.md (#Sante_Pharmacologie_Substances)
2026-10-20 21:08:58,500 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_PC_Optimization`
2026-10-20 21:08:58,500 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : diagnostic-bridage-intel-i5-13400f-asus-h610m-a.md (#Hardware_PC_Optimization)
2026-10-20 21:09:22,223 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Cuisine_Technique_et_Gastronomie`
2026-10-20 21:09:22,224 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : techniques-preparation-riz-gohan-sumeshi.md (#Cuisine_Technique_et_Gastronomie)
2026-10-20 21:09:51,595 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : evolution-technique-visuelle-martial-peak-ink-clan.md (#Webtoons_Manga_et_Anime)
2026-10-20 21:10:21,413 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Product_Management_Compliance`
2026-10-20 21:10:21,417 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : cadrage-mvp-barelyx-legal-ux-api.md (#Product_Management_Compliance)
2026-10-20 21:10:46,353 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Hardware_Audio_et_Ergonomie`
2026-10-20 21:10:46,354 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : solutions-ecoute-position-allongee.md (#Hardware_Audio_et_Ergonomie)
2026-10-20 21:11:13,507 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : gestion-cannabinoïdes-semi-synthetiques-maintenance-fenix-mini.md (#Sante_Cannabinoïdes_et_Vaporisation)
2026-10-20 21:11:32,137 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-omeprazole-reflux-biliaires.md (#Sante_et_Admin_Perso)
2026-10-20 21:12:09,732 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-surcouche-graphique-3d-low-poly-trimps.md (#Gaming_Solo_et_Modding)
2026-10-20 21:12:41,742 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Biologie_Physiologie_Humaine`
2026-10-20 21:12:41,743 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : physiologie-etats-conscience-reflexes.md (#Biologie_Physiologie_Humaine)
2026-10-20 21:13:06,282 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-structure-narrative-comedie-meta.md (#Culture_Pop_et_Narratologie)
2026-10-20 21:13:33,846 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `PopCulture_AnalyseNarrative`
2026-10-20 21:13:33,847 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-echec-narratif-leonard-tbbt.md (#PopCulture_AnalyseNarrative)
2026-10-20 21:13:57,501 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gestion_Perso_et_Logistique`
2026-10-20 21:13:57,501 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-consommation-modelisation-autonomie-stock.md (#Gestion_Perso_et_Logistique)
2026-10-20 21:14:19,453 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `IA_ComputerVision`
2026-10-20 21:14:19,453 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : pipeline-clips-twitch-reconnaissance-faciale.md (#IA_ComputerVision)
2026-10-20 21:14:48,179 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : methodologie-apprentissage-jeux-strategie-systemiques.md (#Gaming_Solo_et_Modding)
2026-10-20 21:15:11,938 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session fb3bd2c1048ef3a4_s02_20260816 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 21:15:11,939 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : pour-le-coup-par-contre-je-trouve-que-amy.md (#A_Trier)
2026-10-20 21:15:39,756 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Education_Carriere_Academique`
2026-10-20 21:15:39,756 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : comparaison-parcours-logopedie-geneve-vs-psychomotricite-france.md (#Education_Carriere_Academique)
2026-10-20 21:16:10,990 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : protocole-cicatrisation-post-extraction-dentaire.md (#Sante_et_Admin_Perso)
2026-10-20 21:16:39,279 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Physique_Vapotage`
2026-10-20 21:16:39,279 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : thermodynamique-chimie-vaporisation.md (#Sante_Physique_Vapotage)
2026-10-20 21:17:06,484 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-base-breeding-ranching-palworld-soralite.md (#Gaming_Solo_et_Modding)
2026-10-20 21:17:45,505 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 3aaf918cd374c2c0 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 21:17:45,506 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : est-ce-que-le-recours-à-la-force-publique-après-ex.md (#A_Trier)
2026-10-20 21:18:03,643 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-nutritionnelle-ninja-creami.md (#Nutrition_Volume_Eating)
2026-10-20 21:18:21,640 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Business_Automation_NoCode`
2026-10-20 21:18:21,641 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : automatisation-stripe-brevo-make-workflow.md (#Business_Automation_NoCode)
2026-10-20 21:18:43,177 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-consommation-protocoles-vaporisation-cannabinoïdes.md (#Sante_Pharmacologie_Substances)
2026-10-20 21:19:24,969 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Pharmacologie_Usage`
2026-10-20 21:19:24,970 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-vaporisation-stacking-modulation-cbd-thc.md (#Sante_Pharmacologie_Usage)
2026-10-20 21:19:48,566 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `DevOps_Networking`
2026-10-20 21:19:48,567 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : exposition-services-locaux-tunneling-cgnat-5g.md (#DevOps_Networking)
2026-10-20 21:20:18,515 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Physique_Speculative_et_Ingenierie`
2026-10-20 21:20:18,516 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : applications-indestructibilite-sphere-vs-cone.md (#Physique_Speculative_et_Ingenierie)
2026-10-20 21:20:37,434 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : selection-groovebox-nomade-drafting-rapide.md (#Analyse_Musicale_et_MAO)
2026-10-20 21:21:03,398 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ux-design-psychologie-page-livraison-cocon.md (#Chefferie_Projet_et_UX)
2026-10-20 21:21:20,226 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : diagnostic-comportement-cohabitation-felines.md (#Animaux_Comportement_et_Soins)
2026-10-20 21:21:36,829 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 4bbc88702e728581 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 21:21:36,830 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : javais-un-coach-qui-mavait-parler-dune-ressource-p.md (#Neuroatypie_Admin_France)
2026-10-20 21:22:00,886 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : inertie-sommeil-apnee-sahs.md (#Sante_et_Admin_Perso)
2026-10-20 21:22:28,382 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : guild-wars-2-gold-farming-accessibility-builds-dps.md (#MMORPG_Theorycraft)
2026-10-20 21:22:56,801 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Science_Astronomie_et_Exploration`
2026-10-20 21:22:56,801 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-habitabilite-echelles-colonisation-spatiale.md (#Science_Astronomie_et_Exploration)
2026-10-20 21:23:26,920 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gastronomie_Technique`
2026-10-20 21:23:26,920 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ingenierie-culinaire-frangipane-deglacage.md (#Gastronomie_Technique)
2026-10-20 21:23:59,795 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-alignements-moraux-anime.md (#Webtoons_Manga_et_Anime)
2026-10-20 21:24:26,056 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Droit_Indemnisation_Corporelle`
2026-10-20 21:24:26,056 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : indemnisation-prejudice-corporel-loi-badinter-accident-travail.md (#Droit_Indemnisation_Corporelle)
2026-10-20 21:24:49,481 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Dev_Infrastructure_et_Backend`
2026-10-20 21:24:49,482 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : arbitrage-architecture-server-vs-serverless.md (#Dev_Infrastructure_et_Backend)
2026-10-20 21:25:14,502 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : protocole-recuperation-post-extraction-dentaire.md (#Sante_et_Admin_Perso)
2026-10-20 21:25:33,512 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-conversion-page-vitrine-reassurance.md (#Dev_Web_et_Stack_Astro)
2026-10-20 21:25:56,154 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : optimisation-progression-gestion-compte-gw2.md (#MMORPG_Theorycraft)
2026-10-20 21:26:25,375 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Media_Animation_Adulte`
2026-10-20 21:26:25,375 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : taxonomie-animation-adulte-charge-cognitive.md (#Media_Animation_Adulte)
2026-10-20 21:26:57,140 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Management_and_Strategy`
2026-10-20 21:26:57,141 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : strategies-engagement-jeux-gestion-4x.md (#Gaming_Management_and_Strategy)
2026-10-20 21:27:30,609 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Sante_Gestion_Substances`
2026-10-20 21:27:30,610 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : protocole-sevrage-programme-optimisation-consommation.md (#Sante_Gestion_Substances)
2026-10-20 21:27:57,195 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : archetypes-rm-top-sartorialisme.md (#Culture_Kpop_et_Sémiotique)
2026-10-20 21:28:20,507 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Mecanique_Moto_Mini`
2026-10-20 21:28:20,508 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : maintenance-mecanique-ressort-lanceur-piwi-gazelle.md (#Mecanique_Moto_Mini)
2026-10-20 21:28:50,109 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : workflow-production-hyperpop-digicore-optimisation.md (#Analyse_Musicale_et_MAO)
2026-10-20 21:29:23,438 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_GameDesign_et_Culture_Doujin`
2026-10-20 21:29:23,439 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-ecosysteme-touhou-danmaku-doujin-jrpg.md (#Gaming_GameDesign_et_Culture_Doujin)
2026-10-20 21:29:41,852 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Automation_NoCode_Fintech`
2026-10-20 21:29:41,852 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : integration-stripe-make-routage-metadata-litiges.md (#Automation_NoCode_Fintech)
2026-10-20 21:30:06,948 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 66c6295487c3e470_s11_20260323 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 21:30:06,948 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : je-peux-setup-un-evenement-ga4-pour-quand-les-pers.md (#Sante_et_Admin_Perso)
2026-10-20 21:30:26,882 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gastronomie_Sciences_Sensorielles`
2026-10-20 21:30:26,882 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-sensorielle-biochimique-scarpetta-beurre.md (#Gastronomie_Sciences_Sensorielles)
2026-10-20 21:30:57,642 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Gaming_Coop_et_Survie`
2026-10-20 21:30:57,643 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : analyse-comparative-jeux-survie-evolutions-enshrouded.md (#Gaming_Coop_et_Survie)
2026-10-20 21:31:23,872 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : evolution-qi-biais-mesure-neuroatypie.md (#Introspection_et_Neuroatypie)
2026-10-20 21:31:50,862 [WARNING] Exocortex.TakeoutIngestor: Échec de distillation locale pour session 39ddd2a984b69b45 : 500 Server Error: Internal Server Error for url: http://localhost:11434/api/chat
2026-10-20 21:31:50,862 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : on-est-daccords-que-cette-adresse-mail-plocrtehfrg.md (#A_Trier)
2026-10-20 21:32:21,229 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : product-ownership-competences-user-stories-cycle-en-v.md (#Chefferie_Projet_et_UX)
2026-10-20 21:32:54,228 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Education_Droit_et_Carriere`
2026-10-20 21:32:54,228 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : mecanique-ects-reactivation-profil-juridique.md (#Education_Droit_et_Carriere)
2026-10-20 21:33:19,896 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Cuisine_Technique_et_Fusion`
2026-10-20 21:33:19,897 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : ingenierie-textures-nems-jjajang-tteokbokki.md (#Cuisine_Technique_et_Fusion)
2026-10-20 21:33:40,328 [INFO] Exocortex.TakeoutIngestor: Nouveau tag taxonomique enregistré dans Taxonomie_Tags.md : `Dev_Backend_Architecture`
2026-10-20 21:33:40,329 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : architecture-api-graphql-nestjs-pwa.md (#Dev_Backend_Architecture)
2026-10-20 21:34:02,988 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : suivi-glycemique-titration-metformine-lantus.md (#Sante_et_Admin_Perso)
2026-10-20 21:34:29,055 [INFO] Exocortex.TakeoutIngestor: Fiche conceptuelle distillée créée : preparation-rendez-vous-medical-ema.md (#Sante_et_Admin_Perso)
2026-10-20 21:34:29,073 [INFO] Exocortex.LLM: Modèle 'gemma4:12b' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-20 21:34:29,085 [INFO] Exocortex.LLM: Modèle 'gemma4:26b-a4b' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-20 21:34:29,949 [INFO] Exocortex.LLM: Modèle 'bge-m3' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-20 21:34:30,450 [INFO] Exocortex.TakeoutIngestor: Distillation LLM achevée : 479 fiches conceptuelles créées dans 02_Concepts/.
2026-10-20 21:34:30,450 [INFO] Exocortex.TakeoutIngestor: --- SYNCHRONISATION VECTORIELLE LANCEDB ---
2026-10-20 21:34:33,888 [INFO] Exocortex.VectorStore: Note '1-le-probleme-cest-que-je-trouve-personnellement-q.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:33,928 [INFO] Exocortex.VectorStore: Note 'a-quel-point-un-regime-low-fodmap-est-il-vraiment.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:33,967 [INFO] Exocortex.VectorStore: Note 'absurdisme-artisanat-revolte-teleologie.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,007 [INFO] Exocortex.VectorStore: Note 'absurdisme-neuroatypie-ideologies.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,046 [INFO] Exocortex.VectorStore: Note 'acceleration-richesse-verrou-metapolitique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,097 [INFO] Exocortex.VectorStore: Note 'accessibilite-web-alt-text-aria-mat-icon.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,143 [INFO] Exocortex.VectorStore: Note 'aide-moi-a-creer-le-script-dun-accompagnement-audi.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,195 [INFO] Exocortex.VectorStore: Note 'algorithme-mesure-temporelle-sabliers-4-7.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,241 [INFO] Exocortex.VectorStore: Note 'analyse-absence-integration-memes-statiques.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,282 [INFO] Exocortex.VectorStore: Note 'analyse-agencie-systemique-profilage-joueur.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,328 [INFO] Exocortex.VectorStore: Note 'analyse-alignements-moraux-anime.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,373 [INFO] Exocortex.VectorStore: Note 'analyse-archetypes-semiotique-looksmaxxing.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,414 [INFO] Exocortex.VectorStore: Note 'analyse-camus-federalisme-fait-accompli-coexistence.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,455 [INFO] Exocortex.VectorStore: Note 'analyse-clinique-marqueurs-neurodivergence.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,495 [INFO] Exocortex.VectorStore: Note 'analyse-clinique-masking-epuisement-neuroatypique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,536 [INFO] Exocortex.VectorStore: Note 'analyse-cognitive-rime-esthetique-resolution-semantique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,576 [INFO] Exocortex.VectorStore: Note 'analyse-comparative-ceremonies-kpop.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,617 [INFO] Exocortex.VectorStore: Note 'analyse-comparative-competitivite-mobile-pc-console.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,664 [INFO] Exocortex.VectorStore: Note 'analyse-comparative-jeux-plateau-feeling-jdr-strategie.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,707 [INFO] Exocortex.VectorStore: Note 'analyse-comparative-jeux-survie-evolutions-enshrouded.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,752 [INFO] Exocortex.VectorStore: Note 'analyse-complexite-strategique-kinball-foot-us.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,798 [INFO] Exocortex.VectorStore: Note 'analyse-consommation-modelisation-autonomie-stock.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,844 [INFO] Exocortex.VectorStore: Note 'analyse-consommation-protocoles-vaporisation-cannabinoïdes.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,884 [INFO] Exocortex.VectorStore: Note 'analyse-critique-systemes-teleologie-hegemonie-cybernétique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,923 [INFO] Exocortex.VectorStore: Note 'analyse-demographique-deconstruction-subversion-migratoire.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:34,969 [INFO] Exocortex.VectorStore: Note 'analyse-design-boucle-tactique-sociale-checklist.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,017 [INFO] Exocortex.VectorStore: Note 'analyse-divergence-moba-pc-vs-mobile.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,062 [INFO] Exocortex.VectorStore: Note 'analyse-dualite-narrative-erikson-sanderson.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,103 [INFO] Exocortex.VectorStore: Note 'analyse-ecart-type-discours-politique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,148 [INFO] Exocortex.VectorStore: Note 'analyse-echec-narratif-leonard-tbbt.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,194 [INFO] Exocortex.VectorStore: Note 'analyse-ecosysteme-touhou-danmaku-doujin-jrpg.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,243 [INFO] Exocortex.VectorStore: Note 'analyse-ergonomie-conversationnelle-psychometrie-llm.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,289 [INFO] Exocortex.VectorStore: Note 'analyse-forensique-copypastas-obfuscation-traduction.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,335 [INFO] Exocortex.VectorStore: Note 'analyse-game-design-agence-narration-systemique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,380 [INFO] Exocortex.VectorStore: Note 'analyse-habitabilite-echelles-colonisation-spatiale.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,421 [INFO] Exocortex.VectorStore: Note 'analyse-identification-politique-narratif-avant-poste.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,466 [INFO] Exocortex.VectorStore: Note 'analyse-linguistique-agentivite-invisibilisation-agresseur.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,506 [INFO] Exocortex.VectorStore: Note 'analyse-meta-ragebait-dynamiques-meute-numerique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,553 [INFO] Exocortex.VectorStore: Note 'analyse-musicologique-sociologique-trot-coreen.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,598 [INFO] Exocortex.VectorStore: Note 'analyse-narrative-romance-vs-relation-webtoons.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,643 [INFO] Exocortex.VectorStore: Note 'analyse-organoleptique-pates-fermentees-coreennes.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,684 [INFO] Exocortex.VectorStore: Note 'analyse-pedanterie-linguistique-insultes-esprit.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,726 [INFO] Exocortex.VectorStore: Note 'analyse-performative-male-transition-cognitive.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,772 [INFO] Exocortex.VectorStore: Note 'analyse-philosophique-credit-social-despotisme-eclaire.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,811 [INFO] Exocortex.VectorStore: Note 'analyse-representation-autisme-sheldon-cooper.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,856 [INFO] Exocortex.VectorStore: Note 'analyse-risques-existentiels-scenarios-post-humanite-ia.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,903 [INFO] Exocortex.VectorStore: Note 'analyse-sensorielle-biochimique-scarpetta-beurre.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,950 [INFO] Exocortex.VectorStore: Note 'analyse-socio-economique-pouvoir-achat-psychologie-rarete.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:35,991 [INFO] Exocortex.VectorStore: Note 'analyse-statistique-impact-nerfs-lol.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,031 [INFO] Exocortex.VectorStore: Note 'analyse-strategie-marketing-paradigme-ia.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,077 [INFO] Exocortex.VectorStore: Note 'analyse-structure-narrative-comedie-meta.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,122 [INFO] Exocortex.VectorStore: Note 'analyse-structurelle-socialisme-sud-americain-vs-social-democratie.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,169 [INFO] Exocortex.VectorStore: Note 'analyse-systemique-dilemme-escargot-mortel.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,209 [INFO] Exocortex.VectorStore: Note 'analyse-systemique-privacy-asymetrie-pouvoir-espace-latent.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,257 [INFO] Exocortex.VectorStore: Note 'analyse-systemique-sous-representation-esport.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,301 [INFO] Exocortex.VectorStore: Note 'analyse-systemique-vs-consommation-politique-epistemologie.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,346 [INFO] Exocortex.VectorStore: Note 'analyse-theorie-esprit-masking-ados2.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,387 [INFO] Exocortex.VectorStore: Note 'analyse-trajectoire-taylor-swift-soft-fascisme.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,429 [INFO] Exocortex.VectorStore: Note 'analyse-vectorielle-narration-empathie-systeme-chaos.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,475 [INFO] Exocortex.VectorStore: Note 'analyse-vectorielle-resilience-narrative-sitcoms.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,521 [INFO] Exocortex.VectorStore: Note 'aphantasie-dissociation-spatiale-visuelle.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,568 [INFO] Exocortex.VectorStore: Note 'applications-indestructibilite-sphere-vs-cone.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,613 [INFO] Exocortex.VectorStore: Note 'arbitrage-acquisition-vs-conversion.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,654 [INFO] Exocortex.VectorStore: Note 'arbitrage-administratif-stage-formation-vs-pmsmp-suisse.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,700 [INFO] Exocortex.VectorStore: Note 'arbitrage-architecture-server-vs-serverless.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,746 [INFO] Exocortex.VectorStore: Note 'arbitrage-energetique-pc-vs-mini-pc-n100-serveur.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,791 [INFO] Exocortex.VectorStore: Note 'arbitrage-ergonomie-dual-screen-retroid-ayn.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,838 [INFO] Exocortex.VectorStore: Note 'arbitrage-formation-rfpe-vs-aah-mdph.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,884 [INFO] Exocortex.VectorStore: Note 'arbitrage-handheld-android-snapdragon-8-gen-2-vs-3.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,927 [INFO] Exocortex.VectorStore: Note 'arbitrage-hardware-gpu-desktop-vs-arm-ia-locale.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:36,972 [INFO] Exocortex.VectorStore: Note 'arbitrage-materiel-ayn-thor-vs-azeron-cyborg-2.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,019 [INFO] Exocortex.VectorStore: Note 'arbitrage-materiel-pc-sage-50.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,064 [INFO] Exocortex.VectorStore: Note 'arbitrage-ninja-creami-slushy-gestion-metabolique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,109 [INFO] Exocortex.VectorStore: Note 'arbitrage-placement-vs-achat-immobilier-hcsf.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,155 [INFO] Exocortex.VectorStore: Note 'arbitrage-positionnement-producteur-vs-cm.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,203 [INFO] Exocortex.VectorStore: Note 'arbitrage-pwa-react-native-flutter.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,250 [INFO] Exocortex.VectorStore: Note 'arbitrage-upgrade-cpu-intel-vs-amd-am4-x3d.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,291 [INFO] Exocortex.VectorStore: Note 'arbitrages-equipement-cuisine-riz-glace.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,337 [INFO] Exocortex.VectorStore: Note 'archetypes-rm-top-sartorialisme.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,378 [INFO] Exocortex.VectorStore: Note 'architecture-absurdisme-lucidite-revolte-collective.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,425 [INFO] Exocortex.VectorStore: Note 'architecture-api-graphql-nestjs-pwa.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,471 [INFO] Exocortex.VectorStore: Note 'architecture-base-breeding-ranching-palworld-soralite.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,519 [INFO] Exocortex.VectorStore: Note 'architecture-conversion-acquisition-services-locaux.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,559 [INFO] Exocortex.VectorStore: Note 'architecture-conversion-automatisation-funnels-pnl.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,599 [INFO] Exocortex.VectorStore: Note 'architecture-conversion-design-triage-therapeute.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,644 [INFO] Exocortex.VectorStore: Note 'architecture-conversion-page-vitrine-reassurance.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,691 [INFO] Exocortex.VectorStore: Note 'architecture-data-driven-pipeline-assets-unity-collection-game.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,731 [INFO] Exocortex.VectorStore: Note 'architecture-decouplage-extraction-assets-excel-api.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,778 [INFO] Exocortex.VectorStore: Note 'architecture-distribution-cloudflare-r2-vercel-astro.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,817 [INFO] Exocortex.VectorStore: Note 'architecture-dysfonctionnements-cancel-culture.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,864 [INFO] Exocortex.VectorStore: Note 'architecture-hybride-chatbot-ecommerce-chainlit-rag-api.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,909 [INFO] Exocortex.VectorStore: Note 'architecture-ia-sovereine-eco-conçue-rag-chainlit.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:37,957 [INFO] Exocortex.VectorStore: Note 'architecture-incremental-tech-abstraction-industrielle.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,001 [INFO] Exocortex.VectorStore: Note 'architecture-llm-inhibition-raisonnement-experts.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,045 [INFO] Exocortex.VectorStore: Note 'architecture-lp-double-conversion-astro-scss.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,090 [INFO] Exocortex.VectorStore: Note 'architecture-metaphysique-observateur-4d-individualisme-ouvert.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,135 [INFO] Exocortex.VectorStore: Note 'architecture-moteur-jeu-incremental-3d-headless.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,188 [INFO] Exocortex.VectorStore: Note 'architecture-olfactive-composition-ombre-fusion-profils.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,236 [INFO] Exocortex.VectorStore: Note 'architecture-organoleptique-fonctionnelle-konjac.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,285 [INFO] Exocortex.VectorStore: Note 'architecture-production-musicale-kanye-west.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,338 [INFO] Exocortex.VectorStore: Note 'architecture-r2-vercel-conversion-segmentee.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,382 [INFO] Exocortex.VectorStore: Note 'architecture-scoring-simplification-moba-tactile.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,428 [INFO] Exocortex.VectorStore: Note 'architecture-section-offre-high-ticket-investissement.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,473 [INFO] Exocortex.VectorStore: Note 'architecture-simulateur-degats-lol-meraki.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,527 [INFO] Exocortex.VectorStore: Note 'architecture-surcouche-graphique-3d-low-poly-trimps.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,570 [INFO] Exocortex.VectorStore: Note 'architecture-tracking-ga4-google-ads-diagnostic.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,619 [INFO] Exocortex.VectorStore: Note 'architecture-tracking-ga4-google-ads-micro-budget.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,665 [INFO] Exocortex.VectorStore: Note 'articulation-ema-cra-strategie-mdph-autisme.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,714 [INFO] Exocortex.VectorStore: Note 'asymetries-sociologiques-epistemologiques-transidentite-bon-sens.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,757 [INFO] Exocortex.VectorStore: Note 'atrophie-pensee-dominante-exclusion-debat.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,808 [INFO] Exocortex.VectorStore: Note 'attention-repasse-au-format-slide-car-tout-le-form.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,858 [INFO] Exocortex.VectorStore: Note 'au-niveau-de-lanalyse-bilan-personnel-pour-la-slid.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,909 [INFO] Exocortex.VectorStore: Note 'audit-pivot-google-ads-niche-rupture.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:38,959 [INFO] Exocortex.VectorStore: Note 'automatisation-stripe-brevo-make-workflow.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,002 [INFO] Exocortex.VectorStore: Note 'avec-15k-de-budgets-on-ne-peut-avoir-quaussi-peu-d.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,053 [INFO] Exocortex.VectorStore: Note 'benchmark-selection-outils-gestion-projet-hello-hercule.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,098 [INFO] Exocortex.VectorStore: Note 'bon-jai-redesigner-les-lp-et-la-frontpage-avec-not.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,142 [INFO] Exocortex.VectorStore: Note 'bon-on-va-partir-sur-une-petite-session-templating.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,188 [INFO] Exocortex.VectorStore: Note 'bonjour-depuis-deux-jours-il-nest-plus-possible-de.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,232 [INFO] Exocortex.VectorStore: Note 'cadrage-budget-recrutement-app-mobile.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,283 [INFO] Exocortex.VectorStore: Note 'cadrage-mvp-barelyx-legal-ux-api.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,333 [INFO] Exocortex.VectorStore: Note 'cest-quoi-la-culture-du-plein.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,388 [INFO] Exocortex.VectorStore: Note 'chainement-audio-meditation-eq-compression.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,433 [INFO] Exocortex.VectorStore: Note 'comment-je-pourrais-adapter-lintitulé-au-format-fr.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,486 [INFO] Exocortex.VectorStore: Note 'comment-me-conseilles-tu-de-gerer-le-hsoting-des-f.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,535 [INFO] Exocortex.VectorStore: Note 'comparaison-evolution-pokemon-digimon.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,586 [INFO] Exocortex.VectorStore: Note 'comparaison-kroma-z-geekvape-z-nano-effet-puff.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,633 [INFO] Exocortex.VectorStore: Note 'comparaison-modeles-socio-economiques-chine-usa.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,690 [INFO] Exocortex.VectorStore: Note 'comparaison-paradigmes-progression-fluidite-mmorpg.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,740 [INFO] Exocortex.VectorStore: Note 'comparaison-parcours-logopedie-geneve-vs-psychomotricite-france.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,787 [INFO] Exocortex.VectorStore: Note 'comparaison-philosophie-combat-wow-gw2.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,833 [INFO] Exocortex.VectorStore: Note 'comparaison-politique-socio-economique-asie-europe.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,888 [INFO] Exocortex.VectorStore: Note 'comparatif-cuiseurs-riz-strategie-achat.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,939 [INFO] Exocortex.VectorStore: Note 'comparatif-samplers-hardware-workflow-chromatique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:39,990 [INFO] Exocortex.VectorStore: Note 'comparatif-systemes-jdr-initiation-familiale.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,043 [INFO] Exocortex.VectorStore: Note 'comparatif-vaporisateurs-architecture-oem-vs-proprietaire.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,094 [INFO] Exocortex.VectorStore: Note 'comparative-socio-economics-us-states-resilience.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,146 [INFO] Exocortex.VectorStore: Note 'conception-personas-ux-chatbot-ia.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,193 [INFO] Exocortex.VectorStore: Note 'conception-simulateur-moba-macro-tactile.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,240 [INFO] Exocortex.VectorStore: Note 'configuration-authentification-email-brevo-infomaniak.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,286 [INFO] Exocortex.VectorStore: Note 'configuration-stripe-copywriting-tunnel-vente-pnl.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,338 [INFO] Exocortex.VectorStore: Note 'conflit-integration-neuroatypie-burnout-salariat.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,384 [INFO] Exocortex.VectorStore: Note 'consommation-horreur-dread-vs-shock.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,432 [INFO] Exocortex.VectorStore: Note 'contournement-api-trakt-riven-jellyseerr-webhooks.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,478 [INFO] Exocortex.VectorStore: Note 'conversion-froide-tracking-transaction-offre-crise.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,532 [INFO] Exocortex.VectorStore: Note 'cout-energetique-lucidite-dogmatisme-cognitif.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,577 [INFO] Exocortex.VectorStore: Note 'cristallisation.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,630 [INFO] Exocortex.VectorStore: Note 'critique-meritocratie-efficience-theorie-cuilleres.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,681 [INFO] Exocortex.VectorStore: Note 'critique-sociologique-achat-comptant.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,727 [INFO] Exocortex.VectorStore: Note 'declin-exigence-fracture-cognitive-automatisation.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,769 [INFO] Exocortex.VectorStore: Note 'deconstruction-biais-mesure-qi-facteurs-environnementaux.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,827 [INFO] Exocortex.VectorStore: Note 'deconstruction-difficult-reception-fear-hunger.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,879 [INFO] Exocortex.VectorStore: Note 'deconstruction-expertise-boite-noire-desacralisation.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,932 [INFO] Exocortex.VectorStore: Note 'deconstruction-geoïsme-droits-naturels-monocausalité.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:40,979 [INFO] Exocortex.VectorStore: Note 'deconstruction-isomorphisme-effort-souffrance.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,027 [INFO] Exocortex.VectorStore: Note 'deconstruction-meritocratie-richesse-relative.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,084 [INFO] Exocortex.VectorStore: Note 'deconstruction-paradigmes-economiques-inegalites-capital-ruissellement.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,143 [INFO] Exocortex.VectorStore: Note 'deconstruction-sauts-logiques-esoterisme-sociologie.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,193 [INFO] Exocortex.VectorStore: Note 'deconstruction-trilemme-economique-neutralite-institutionnelle.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,269 [INFO] Exocortex.VectorStore: Note 'decryptage-interaction-administrative-ema-anxiete.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,333 [INFO] Exocortex.VectorStore: Note 'definition-personas-green-futur-b2b-b2c.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,400 [INFO] Exocortex.VectorStore: Note 'denuvo-bypass-steam-session-management.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,464 [INFO] Exocortex.VectorStore: Note 'depannage-routeur-5g-meteor-dns-cloud-ui.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,524 [INFO] Exocortex.VectorStore: Note 'deploiement-stack-debrid-windows.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,585 [INFO] Exocortex.VectorStore: Note 'derive-pratique-religieuse-mecanisation-gamification.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,649 [INFO] Exocortex.VectorStore: Note 'determinisme-pensee-systemique-critique-individualisme.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,705 [INFO] Exocortex.VectorStore: Note 'determinisme-vs-indeterminisme-interaction-quantique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,757 [INFO] Exocortex.VectorStore: Note 'developpement-plugins-midi-logiques-workflow-ableton-move.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,830 [INFO] Exocortex.VectorStore: Note 'diagnostic-bottleneck-cpu-optimisation-micro-stutters.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,897 [INFO] Exocortex.VectorStore: Note 'diagnostic-bridage-intel-i5-13400f-asus-h610m-a.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:41,955 [INFO] Exocortex.VectorStore: Note 'diagnostic-charge-cpu-telemetrie-windows.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,027 [INFO] Exocortex.VectorStore: Note 'diagnostic-comportement-cohabitation-felines.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,090 [INFO] Exocortex.VectorStore: Note 'diagnostic-micro-gels-systeme-latence-dpc.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,156 [INFO] Exocortex.VectorStore: Note 'diagnostic-panne-ecran-noir-ventilateurs-100.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,220 [INFO] Exocortex.VectorStore: Note 'diagnostic-resolution-micro-stutters-memory-drivers.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,286 [INFO] Exocortex.VectorStore: Note 'diagnostic-resolution-throttling-vrm.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,348 [INFO] Exocortex.VectorStore: Note 'diagnostic-throttling-vrm-instabilite-ram.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,422 [INFO] Exocortex.VectorStore: Note 'diagnostic-traitement-infestation-vrillettes.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,492 [INFO] Exocortex.VectorStore: Note 'dialectique-simulation-confrontation-ideologique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,553 [INFO] Exocortex.VectorStore: Note 'dichotomie-identitaire-economie-caricature-rap.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,621 [INFO] Exocortex.VectorStore: Note 'dissonance-ideaux-individuels-regulation-sociale.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,692 [INFO] Exocortex.VectorStore: Note 'dissonance-narrative-clip-free-bird.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,761 [INFO] Exocortex.VectorStore: Note 'distinction-causalite-directe-facteur-risque.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,832 [INFO] Exocortex.VectorStore: Note 'distribution-fichiers-payants-cloudflare-r2-vercel.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,898 [INFO] Exocortex.VectorStore: Note 'donne-moi-des-idees-pour-des-sauces-hypocaloriques.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:42,972 [INFO] Exocortex.VectorStore: Note 'dou-pensent-tu-que-la-fascination-pour-les-femboys.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,030 [INFO] Exocortex.VectorStore: Note 'du-coup-jai-des-valeurs-a-adapter-pour-le-contexte.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,100 [INFO] Exocortex.VectorStore: Note 'dualite-shipping-culture-simulation-performance.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,175 [INFO] Exocortex.VectorStore: Note 'dynamique-regulation-cognitive-hpi-autisme-interet.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,242 [INFO] Exocortex.VectorStore: Note 'dynamiques-friction-cognitive-dependance-comportementale.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,298 [INFO] Exocortex.VectorStore: Note 'dynamiques-historiques-causalite-complexite.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,375 [INFO] Exocortex.VectorStore: Note 'dynamiques-transmisogynie-scrutin-mtf.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,446 [INFO] Exocortex.VectorStore: Note 'dysfonction-executive-paradoxe-liberte-audhd.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,513 [INFO] Exocortex.VectorStore: Note 'emergence-qualia-intersubjectivite-philosophique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,581 [INFO] Exocortex.VectorStore: Note 'epicurisme-moderne-resistance-absurde.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,650 [INFO] Exocortex.VectorStore: Note 'epistemologie-analyse-esport-biais-cognitifs.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,725 [INFO] Exocortex.VectorStore: Note 'epistemologie-constructivisme-isomorphisme-verite.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,791 [INFO] Exocortex.VectorStore: Note 'epistemologie-droit-normatif-vs-sociologie-empirique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,867 [INFO] Exocortex.VectorStore: Note 'epistemologie-expertise-theorique-vs-pratique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:43,923 [INFO] Exocortex.VectorStore: Note 'epistemologie-feminisme-verite-situee-expertise.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,003 [INFO] Exocortex.VectorStore: Note 'erosion-agency-charge-cognitive-healer-mplus.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,064 [INFO] Exocortex.VectorStore: Note 'est-ce-quavec-hermes-agent-je-suis-censé-pouvoir-g.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,150 [INFO] Exocortex.VectorStore: Note 'est-ce-que-le-parallel-agentic-work-est-la-norme-e.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,223 [INFO] Exocortex.VectorStore: Note 'est-ce-que-le-recours-à-la-force-publique-après-ex.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,302 [INFO] Exocortex.VectorStore: Note 'est-ce-quen-faisant-chauffer-du-cheese-whiz-genre.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,379 [INFO] Exocortex.VectorStore: Note 'est-ce-quen-matiere-de-eliquide-les-arome-concentr.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,452 [INFO] Exocortex.VectorStore: Note 'est-ce-quil-est-pertinent-de-creer-une-sorte-de-pe.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,525 [INFO] Exocortex.VectorStore: Note 'ethique-audace-externalisation-couts-sociaux.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,598 [INFO] Exocortex.VectorStore: Note 'ethique-oisivete-dividende-technologique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,670 [INFO] Exocortex.VectorStore: Note 'evolution-qi-biais-mesure-neuroatypie.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,743 [INFO] Exocortex.VectorStore: Note 'evolution-technique-visuelle-martial-peak-ink-clan.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,815 [INFO] Exocortex.VectorStore: Note 'exposition-services-locaux-tunneling-cgnat-5g.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,886 [INFO] Exocortex.VectorStore: Note 'fais-moi-un-son-sur-kc-vs-kcb-en-lec.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:44,956 [INFO] Exocortex.VectorStore: Note 'faut-il-separer-lhomme-de-lartiste.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,027 [INFO] Exocortex.VectorStore: Note 'forces-persuasion-du-client-avec-presentation-de-l.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,093 [INFO] Exocortex.VectorStore: Note 'framework-documentation-portfolio-projets-digitaux.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,193 [INFO] Exocortex.VectorStore: Note 'framework-influence-politique-engagement-algorithmique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,268 [INFO] Exocortex.VectorStore: Note 'framework-presentation-bilan-competences-chef-projet.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,335 [INFO] Exocortex.VectorStore: Note 'friction-phenomenologique-vs-existentialisme-agentivite.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,407 [INFO] Exocortex.VectorStore: Note 'gaming-pc-arm-emulation-vs-streaming.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,482 [INFO] Exocortex.VectorStore: Note 'genealogie-terminologie-actual-play-francophone.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,554 [INFO] Exocortex.VectorStore: Note 'genese-protocoles-alternatifs-lyme-covid.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,630 [INFO] Exocortex.VectorStore: Note 'gestion-cannabinoïdes-semi-synthetiques-maintenance-fenix-mini.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,708 [INFO] Exocortex.VectorStore: Note 'gestion-cohabitation-felines-chaton-orphelin-apathie-adulte.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,778 [INFO] Exocortex.VectorStore: Note 'gestion-parcours-mdph-coordination-medicale.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,847 [INFO] Exocortex.VectorStore: Note 'gestion-transition-consommation-remplacement-sas.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:45,926 [INFO] Exocortex.VectorStore: Note 'gestion-urgence-dentaire-progression-infection.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,001 [INFO] Exocortex.VectorStore: Note 'gouvernance-technologique-determinisme-latent-manifeste.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,074 [INFO] Exocortex.VectorStore: Note 'guild-wars-2-gold-farming-accessibility-builds-dps.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,148 [INFO] Exocortex.VectorStore: Note 'gw2-gear-optimization-celestial-vs-specialized.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,214 [INFO] Exocortex.VectorStore: Note 'homonationalisme-respectabilite-alienation-sociopolitique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,286 [INFO] Exocortex.VectorStore: Note 'how-come-blackpink-is-so-low-in-the-awards-ranking.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,374 [INFO] Exocortex.VectorStore: Note 'how-hard-owuld-it-be-to-make-a-device-similar-to-t.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,446 [INFO] Exocortex.VectorStore: Note 'how-to-check-whether-smthyperthreading-is-on-or-of.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,519 [INFO] Exocortex.VectorStore: Note 'httpswwwnexusmodscomeldenringmods4709-im-looking-f.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,592 [INFO] Exocortex.VectorStore: Note 'i-was-wondering-are-music-show-in-korea-more-mains.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,659 [INFO] Exocortex.VectorStore: Note 'il-me-faudrait-combien-idealmeent-en-budget-market.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,731 [INFO] Exocortex.VectorStore: Note 'impasse-camusienne-ethique-violence-decoloniale.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,801 [INFO] Exocortex.VectorStore: Note 'indemnisation-prejudice-corporel-loi-badinter-accident-travail.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,882 [INFO] Exocortex.VectorStore: Note 'inertie-sommeil-apnee-sahs.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:46,954 [INFO] Exocortex.VectorStore: Note 'ingenierie-culinaire-frangipane-deglacage.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,027 [INFO] Exocortex.VectorStore: Note 'ingenierie-dissolution-capital-flux-30-jours.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,095 [INFO] Exocortex.VectorStore: Note 'ingenierie-paroles-suno-digicore-breakcore.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,174 [INFO] Exocortex.VectorStore: Note 'ingenierie-soutenance-orale-narration-strategique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,244 [INFO] Exocortex.VectorStore: Note 'ingenierie-soutenance-portfolio-chef-projet-digital.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,320 [INFO] Exocortex.VectorStore: Note 'ingenierie-textures-nems-jjajang-tteokbokki.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,392 [INFO] Exocortex.VectorStore: Note 'integration-stripe-make-routage-metadata-litiges.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,464 [INFO] Exocortex.VectorStore: Note 'is-ff-xvi-as-lengthy-in-cinematics-as-the-first-ho.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,534 [INFO] Exocortex.VectorStore: Note 'is-garden-map-farming-owrth.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,588 [INFO] Exocortex.VectorStore: Note 'is-there-a-gacha-component-to-where-winds-meet.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,672 [INFO] Exocortex.VectorStore: Note 'ive-dabbled-with-sillytavern-and-an-open-source-mo.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,739 [INFO] Exocortex.VectorStore: Note 'jai-envie-dacquerir-une-streaming-box-genre-apple.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,807 [INFO] Exocortex.VectorStore: Note 'jai-fait-une-marinade-pour-les-hauts-de-cuisse-pap.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,877 [INFO] Exocortex.VectorStore: Note 'jai-limpression-quon-sort-un-peu-des-chiffres-de-n.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:47,953 [INFO] Exocortex.VectorStore: Note 'jai-peur-qua-120-chf-prix-ferme-voulu-par-le-clien.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,023 [INFO] Exocortex.VectorStore: Note 'jai-potentiellemnt-acces-a-de-la-cali-canda-et-de.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,095 [INFO] Exocortex.VectorStore: Note 'jai-recup-un-adaptateur-et-un-mini-bubbler-du-coup.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,175 [INFO] Exocortex.VectorStore: Note 'javais-un-coach-qui-mavait-parler-dune-ressource-p.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,239 [INFO] Exocortex.VectorStore: Note 'je-mapprete-a-lancer-ma-toute-premiere-campagne-go.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,298 [INFO] Exocortex.VectorStore: Note 'je-peux-setup-un-evenement-ga4-pour-quand-les-pers.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,377 [INFO] Exocortex.VectorStore: Note 'je-preferes-que-tu-me-genre-des-slides-directement.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,444 [INFO] Exocortex.VectorStore: Note 'je-realise-un-guide-sur-la-pnl-et-je-dois-faire-un.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,515 [INFO] Exocortex.VectorStore: Note 'je-souhaiterais-rajouter-deux-slides-une-premiere.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,595 [INFO] Exocortex.VectorStore: Note 'je-suis-tomber-sur-un-message-intéressant-nicholas.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,664 [INFO] Exocortex.VectorStore: Note 'je-veux-faire-du-riz-a-sushi-pour-ce-soir-avec-mon.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,733 [INFO] Exocortex.VectorStore: Note 'je-veux-que-tu-me-fasses-deux-documents-un-pour-la.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,798 [INFO] Exocortex.VectorStore: Note 'jhabite-dans-un-pays-où-les-parents-choisissent-lé.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,870 [INFO] Exocortex.VectorStore: Note 'jm-ai-toujours-pas-acces-alors-que-jai-fait-un-pai.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:48,942 [INFO] Exocortex.VectorStore: Note 'la-oslution-que-tu-porpose-est-uniquement-le-masqu.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,012 [INFO] Exocortex.VectorStore: Note 'maintenance-mecanique-ressort-lanceur-piwi-gazelle.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,084 [INFO] Exocortex.VectorStore: Note 'mecanique-cognitive-shifting-dissociation.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,161 [INFO] Exocortex.VectorStore: Note 'mecanique-ects-reactivation-profil-juridique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,226 [INFO] Exocortex.VectorStore: Note 'mecanismes-derive-semantique-brainrot.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,300 [INFO] Exocortex.VectorStore: Note 'mecanismes-profil-pda-hpi-autisme.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,378 [INFO] Exocortex.VectorStore: Note 'meta-prompting-rag-sota-generation.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,448 [INFO] Exocortex.VectorStore: Note 'methodologie-apprentissage-jeux-strategie-systemiques.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,521 [INFO] Exocortex.VectorStore: Note 'methodologie-cadrage-us-tickets-api-contracts.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,597 [INFO] Exocortex.VectorStore: Note 'methodologie-description-symptomes-visuels-aura-migraineuse.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,665 [INFO] Exocortex.VectorStore: Note 'methodologie-pitch-deck-alignement-strategique-technique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,731 [INFO] Exocortex.VectorStore: Note 'methodologie-veille-cadrage-ia-rse.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,806 [INFO] Exocortex.VectorStore: Note 'methodologie-veille-tech-juridique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,866 [INFO] Exocortex.VectorStore: Note 'methodologies-fast-forward-moteurs-emulation.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:49,949 [INFO] Exocortex.VectorStore: Note 'micro-entrepreneuriat-post-llm-orchestration.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,022 [INFO] Exocortex.VectorStore: Note 'mixage-vocal-meditation-traitement-signal.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,096 [INFO] Exocortex.VectorStore: Note 'modelisation-cognitive-espace-latent-esthetique-complexite.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,181 [INFO] Exocortex.VectorStore: Note 'modelisation-consommation-gestion-stock-cannabis.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,256 [INFO] Exocortex.VectorStore: Note 'modelisation-independance-financiere-rente-3m.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,326 [INFO] Exocortex.VectorStore: Note 'modelisation-neurobiologique-save-scumming-hpi-tsa.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,394 [INFO] Exocortex.VectorStore: Note 'modelisation-vectorielle-identification-genre-male-gaze.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,460 [INFO] Exocortex.VectorStore: Note 'monotropisme-inertie-autistique-cliff-edge.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,532 [INFO] Exocortex.VectorStore: Note 'mutation-ddl-infrastructures-infostealers.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,601 [INFO] Exocortex.VectorStore: Note 'mutation-marche-hardware-ia-vs-consumer.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,667 [INFO] Exocortex.VectorStore: Note 'navigation-mdph-diagnostic-differentiel-tsa-trauma.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,733 [INFO] Exocortex.VectorStore: Note 'negociation-administrative-stage-international-pmsmp.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,804 [INFO] Exocortex.VectorStore: Note 'neuro-acoustique-saturation-cognitive-hpi-tdah.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,875 [INFO] Exocortex.VectorStore: Note 'neuro-architecture-evolution-musicale-taste-freeze.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:50,941 [INFO] Exocortex.VectorStore: Note 'neuroatypie-travail-subsistance-propre.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,014 [INFO] Exocortex.VectorStore: Note 'neurobiologie-focalisation-interne-monotropisme.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,090 [INFO] Exocortex.VectorStore: Note 'neurobiologie-tolerance-sevrage-cannabinoide.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,164 [INFO] Exocortex.VectorStore: Note 'neurodivergence-facteur-g-double-empathie-homophilie.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,241 [INFO] Exocortex.VectorStore: Note 'neuroplasticite-apprentissage-langues-neuroatypique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,312 [INFO] Exocortex.VectorStore: Note 'ok-adapter-a-ma-sheet-la-formule-donne-ça-pour-le.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,385 [INFO] Exocortex.VectorStore: Note 'ok-be-careful-no-spoiler-except-yes-or-no-is-there.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,454 [INFO] Exocortex.VectorStore: Note 'ok-cest-bon-jai-trouver-mon-projet-ça-va-etre-daut.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,523 [INFO] Exocortex.VectorStore: Note 'ok-demain-je-commence-mon-stage-pour-une-entrepris.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,593 [INFO] Exocortex.VectorStore: Note 'ok-je-suis-tombé-sur-ce-tweet-genuine-questions-be.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,654 [INFO] Exocortex.VectorStore: Note 'ok-je-veux-que-tu-maide-a-preparer-des-prompts-pou.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,733 [INFO] Exocortex.VectorStore: Note 'ok-je-viens-avoir-une-idee-de-scenario-en-creant-u.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,800 [INFO] Exocortex.VectorStore: Note 'ok-lets-say-the-infinite-universe-theory-is-true-d.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,865 [INFO] Exocortex.VectorStore: Note 'ok-mais-en-gros-cest-pas-vriament-du-cloud-rap-la.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:51,936 [INFO] Exocortex.VectorStore: Note 'ok-on-retourne-sur-de-la-kpop-en-coreen-hangeul-av.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,005 [INFO] Exocortex.VectorStore: Note 'ok-on-va-commencer-mon-journal-de-vaping-dans-cett.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,070 [INFO] Exocortex.VectorStore: Note 'ok-parlons-conscience-deja-pour-commencer-je-veux.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,143 [INFO] Exocortex.VectorStore: Note 'ok-un-prompt-suno-pour-de-lhyperpop-jersey-kpop-re.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,225 [INFO] Exocortex.VectorStore: Note 'on-est-daccords-que-cette-adresse-mail-plocrtehfrg.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,292 [INFO] Exocortex.VectorStore: Note 'ontologie-emergence-topologie-espace-latent.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,372 [INFO] Exocortex.VectorStore: Note 'ontologie-temps-b-theorie-vs-phenomenologie-localite.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,454 [INFO] Exocortex.VectorStore: Note 'optimisation-additifs-refroidissement-ws23-ws3-diy.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,521 [INFO] Exocortex.VectorStore: Note 'optimisation-annonce-airbnb-praz-de-lys.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,596 [INFO] Exocortex.VectorStore: Note 'optimisation-autocrafting-refined-storage-litematica.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,662 [INFO] Exocortex.VectorStore: Note 'optimisation-bande-passante-cognitive-accélération-media.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,735 [INFO] Exocortex.VectorStore: Note 'optimisation-consommation-cannabinoïdes-dose-materiel-cbd-thc.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,808 [INFO] Exocortex.VectorStore: Note 'optimisation-consommation-cannabis-synergies-cbg-cbd-thc.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,883 [INFO] Exocortex.VectorStore: Note 'optimisation-consommation-chauffage-cet.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:52,949 [INFO] Exocortex.VectorStore: Note 'optimisation-consommation-derives-cannabinoïdes-protocoles-tolerance.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,024 [INFO] Exocortex.VectorStore: Note 'optimisation-couch-lock-thc-cbd-cbn.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,099 [INFO] Exocortex.VectorStore: Note 'optimisation-cuisson-riz-multicuiseur-vs-rice-cooker.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,172 [INFO] Exocortex.VectorStore: Note 'optimisation-culinaire-equilibre-organoleptique-physique-textures.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,246 [INFO] Exocortex.VectorStore: Note 'optimisation-culinaire-gestion-aversions-sensorielles.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,319 [INFO] Exocortex.VectorStore: Note 'optimisation-debogage-sillytavern-koboldcpp.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,399 [INFO] Exocortex.VectorStore: Note 'optimisation-demarche-mdph-aah-gestion-surcharge-tsa.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,471 [INFO] Exocortex.VectorStore: Note 'optimisation-ecosysteme-gaming-portable-micro-sessions.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,549 [INFO] Exocortex.VectorStore: Note 'optimisation-extraction-dynamique-vaping.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,620 [INFO] Exocortex.VectorStore: Note 'optimisation-financement-formation-rfft-rqth-agefiph.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,693 [INFO] Exocortex.VectorStore: Note 'optimisation-fluidite-lsfg-mobile-pc-emulation-switch.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,757 [INFO] Exocortex.VectorStore: Note 'optimisation-framerate-modding-ips-yuzu.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,845 [INFO] Exocortex.VectorStore: Note 'optimisation-hardware-local-assistants-multimodaux.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,920 [INFO] Exocortex.VectorStore: Note 'optimisation-hardware-strategie-business-llm.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:53,994 [INFO] Exocortex.VectorStore: Note 'optimisation-input-mapping-manette-tactile.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,069 [INFO] Exocortex.VectorStore: Note 'optimisation-local-llm-roleplay-qwen-sillytavern.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,134 [INFO] Exocortex.VectorStore: Note 'optimisation-macro-recrutement-mmo.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,195 [INFO] Exocortex.VectorStore: Note 'optimisation-nutritionnelle-ninja-creami.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,272 [INFO] Exocortex.VectorStore: Note 'optimisation-omeprazole-reflux-biliaires.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,344 [INFO] Exocortex.VectorStore: Note 'optimisation-patrimoniale-demembrement-sci-donation-partage.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,420 [INFO] Exocortex.VectorStore: Note 'optimisation-pc-handheld-apollo-artemis-steam-input.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,495 [INFO] Exocortex.VectorStore: Note 'optimisation-progression-farming-trimps.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,575 [INFO] Exocortex.VectorStore: Note 'optimisation-progression-gestion-compte-gw2.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,657 [INFO] Exocortex.VectorStore: Note 'optimisation-remote-wol-windows-autologin.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,728 [INFO] Exocortex.VectorStore: Note 'optimisation-rendu-aromatique-puffs-vs-rechargeables.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,802 [INFO] Exocortex.VectorStore: Note 'optimisation-semantique-recrutement-guilde-mmorpg.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,875 [INFO] Exocortex.VectorStore: Note 'optimisation-streaming-moonlight-reseau-stockage.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:54,948 [INFO] Exocortex.VectorStore: Note 'optimisation-structurelle-plateau-bureau-assis-debout.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,031 [INFO] Exocortex.VectorStore: Note 'optimisation-texture-emulsion-gnocchi-pates.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,108 [INFO] Exocortex.VectorStore: Note 'optimisation-vaporisation-densite-saturation-cb1.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,194 [INFO] Exocortex.VectorStore: Note 'optimisation-vaporisation-fleur-vs-resine.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,266 [INFO] Exocortex.VectorStore: Note 'optimisation-vaporisation-resine-valorisation-avb.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,355 [INFO] Exocortex.VectorStore: Note 'optimisation-vaporisation-stacking-modulation-cbd-thc.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,422 [INFO] Exocortex.VectorStore: Note 'optimisation-volume-alimentaire-batch-cooking-500kcal.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,495 [INFO] Exocortex.VectorStore: Note 'optimisation-volume-batch-cooking-500kcal.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,568 [INFO] Exocortex.VectorStore: Note 'origins-anima-after-losing-a-player-combat-gain-20.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,638 [INFO] Exocortex.VectorStore: Note 'ou-se-situent-les-civ-pre-colombienne-sur-la-grand.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,713 [INFO] Exocortex.VectorStore: Note 'paradigme-observateur-4d-lecture-jdr-ia.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,784 [INFO] Exocortex.VectorStore: Note 'paradigmes-ia-symbolisme-connexionnisme-espace-latent.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,858 [INFO] Exocortex.VectorStore: Note 'paradoxes-sociopolitiques-droits-trans-coalitions-politiques.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:55,929 [INFO] Exocortex.VectorStore: Note 'parcours-certification-animation-direction-loisirs.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,009 [INFO] Exocortex.VectorStore: Note 'parle-moi-en-détail-du-projet-de-planification-éco.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,073 [INFO] Exocortex.VectorStore: Note 'peut-tu-me-faire-un-tableur-mettant-en-relation-le.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,148 [INFO] Exocortex.VectorStore: Note 'phenomenologie-retro-acronymes-etymologie.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,219 [INFO] Exocortex.VectorStore: Note 'physiologie-chimie-transition-zero-sucre.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,295 [INFO] Exocortex.VectorStore: Note 'physiologie-etats-conscience-reflexes.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,371 [INFO] Exocortex.VectorStore: Note 'physiologie-rgo-micro-aspiration.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,446 [INFO] Exocortex.VectorStore: Note 'physique-vaporisation-protocoles-extraction-cbg-cbd.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,511 [INFO] Exocortex.VectorStore: Note 'pipeline-clips-twitch-reconnaissance-faciale.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,596 [INFO] Exocortex.VectorStore: Note 'pipeline-recherche-transformation-pedagogique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,665 [INFO] Exocortex.VectorStore: Note 'plan-marketing-digital-hyatt-regency-paris-etoile.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,740 [INFO] Exocortex.VectorStore: Note 'plan-recrutement-structuration-equipe-mvp-hello-hercule.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,812 [INFO] Exocortex.VectorStore: Note 'planet-crafter-midgame-analysis-flooding-design.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,884 [INFO] Exocortex.VectorStore: Note 'plausibilite-logique-anxiete-simulation-tsa.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:56,954 [INFO] Exocortex.VectorStore: Note 'positionnement-portfolio-profil-hybride-droit-dev-gestion-projet.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,025 [INFO] Exocortex.VectorStore: Note 'pour-le-coup-par-contre-je-trouve-que-amy.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,097 [INFO] Exocortex.VectorStore: Note 'pourquoi-un-sirop-a-la-maison-ne-donne-jamais-vrai.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,175 [INFO] Exocortex.VectorStore: Note 'poweruserslop-esthetique-competence-complexite.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,249 [INFO] Exocortex.VectorStore: Note 'preparation-rendez-vous-medical-ema.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,313 [INFO] Exocortex.VectorStore: Note 'prevalence-et-comorbodité-des-tsas-par-rapport-a-l.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,392 [INFO] Exocortex.VectorStore: Note 'prismes-geopolitiques-chine-usa-autonomie-europe.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,459 [INFO] Exocortex.VectorStore: Note 'probabilites-impossibilite-physique-inegalites-bell.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,521 [INFO] Exocortex.VectorStore: Note 'processus-diagnostic-tsa-anamnese-restitution.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,606 [INFO] Exocortex.VectorStore: Note 'product-ownership-competences-user-stories-cycle-en-v.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,677 [INFO] Exocortex.VectorStore: Note 'profil-consommation-narrative-world-building-power-fantasy.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,746 [INFO] Exocortex.VectorStore: Note 'profil-double-exceptionnalite-hpi-tsa.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,819 [INFO] Exocortex.VectorStore: Note 'profil-esthetique-densite-ancre-vocale-liberation.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,896 [INFO] Exocortex.VectorStore: Note 'profilage-architecture-cognitive-architecte-vs-executant.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:57,961 [INFO] Exocortex.VectorStore: Note 'profilage-neurocognitif-dyssynchronie-hypervigilance.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,046 [INFO] Exocortex.VectorStore: Note 'prompt-engineering-asmr-textures-rupture-veo.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,125 [INFO] Exocortex.VectorStore: Note 'prompt-engineering-coach-entrepreneurial-realiste.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,194 [INFO] Exocortex.VectorStore: Note 'prompt-engineering-echelle-perspective-photorealisme.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,271 [INFO] Exocortex.VectorStore: Note 'protocole-cicatrisation-post-extraction-dentaire.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,340 [INFO] Exocortex.VectorStore: Note 'protocole-communication-email-etudiant-administration.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,413 [INFO] Exocortex.VectorStore: Note 'protocole-expulsion-protection-mineurs-droit-francais.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,487 [INFO] Exocortex.VectorStore: Note 'protocole-oscillation-dialectique-construction-crash-test.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,553 [INFO] Exocortex.VectorStore: Note 'protocole-recuperation-post-extraction-dentaire.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,644 [INFO] Exocortex.VectorStore: Note 'protocole-sevrage-programme-optimisation-consommation.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,726 [INFO] Exocortex.VectorStore: Note 'protocole-soins-post-extraction-dentaire.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,802 [INFO] Exocortex.VectorStore: Note 'protocole-vaporisation-hybride-modulation-pharmacologique.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,885 [INFO] Exocortex.VectorStore: Note 'protocoles-vaporisation-cbd-thc-gestion-avb.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:58,955 [INFO] Exocortex.VectorStore: Note 'psychologie-soumission-dissonance-integrite.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,033 [INFO] Exocortex.VectorStore: Note 'psychophysique-couleur-valence-arousal-ux.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,105 [INFO] Exocortex.VectorStore: Note 'quel-diff-entre-i206-et-i208.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,180 [INFO] Exocortex.VectorStore: Note 'quel-est-la-meilleure-manière-de-retirer-la-viande.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,250 [INFO] Exocortex.VectorStore: Note 'quid-du-arizer-go-srt.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,317 [INFO] Exocortex.VectorStore: Note 'quid-du-he-10.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,393 [INFO] Exocortex.VectorStore: Note 'recuperation-donnees-sage-50-suisse-panne-materielle.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,464 [INFO] Exocortex.VectorStore: Note 'reintegration-benevolat-competences-visibilite-passive.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,540 [INFO] Exocortex.VectorStore: Note 'reparation-manchette-lave-linge.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,622 [INFO] Exocortex.VectorStore: Note 'salut-toi-est-ce-quon-peut-qualifier-de-wysiwyg-un.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,695 [INFO] Exocortex.VectorStore: Note 'securisation-administrative-aah-gestion-anxiete.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,783 [INFO] Exocortex.VectorStore: Note 'segmentation-personas-marketing-b2b-b2c.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,857 [INFO] Exocortex.VectorStore: Note 'selection-groovebox-nomade-drafting-rapide.md' indexée avec succès dans LanceDB.
2026-10-20 21:34:59,934 [INFO] Exocortex.VectorStore: Note 'selection-hifi-fiio-ft1-rap-optimisation.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,003 [INFO] Exocortex.VectorStore: Note 'si-tu-te-rapelle-de-certaines-de-nos-dsicussiosn-j.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,066 [INFO] Exocortex.VectorStore: Note 'sociologie-domination-dissonance-parasociale-numerique.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,144 [INFO] Exocortex.VectorStore: Note 'sociologie-queerbaiting-normalisation-recuperation.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,218 [INFO] Exocortex.VectorStore: Note 'solutions-ecoute-position-allongee.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,295 [INFO] Exocortex.VectorStore: Note 'souverainete-cloud-conformite-rgaa-standards-operationnels.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,363 [INFO] Exocortex.VectorStore: Note 'spinozisme-absurde-dialectique-droit-soft-law.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,442 [INFO] Exocortex.VectorStore: Note 'standardisation-selection-agence-marketing-rfp-scoring.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,515 [INFO] Exocortex.VectorStore: Note 'strategie-communication-diagnostic-tsa-mdph-aah.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,589 [INFO] Exocortex.VectorStore: Note 'strategie-deploiement-iteratif-kpi-chatbot-rag.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,651 [INFO] Exocortex.VectorStore: Note 'strategie-design-ui-ux-niche-coaching.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,736 [INFO] Exocortex.VectorStore: Note 'strategie-dossier-mdph-aah-rsdae.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,807 [INFO] Exocortex.VectorStore: Note 'strategie-gtm-conversion-astro-jamstack.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,870 [INFO] Exocortex.VectorStore: Note 'strategie-marketing-digital-roi-hotel-luxe.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:00,954 [INFO] Exocortex.VectorStore: Note 'strategie-marketing-roi-planification-editoriale.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,038 [INFO] Exocortex.VectorStore: Note 'strategie-mdph-rsdae-aah-tsa.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,106 [INFO] Exocortex.VectorStore: Note 'strategie-montée-compétences-data-financement-france-travail.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,180 [INFO] Exocortex.VectorStore: Note 'strategie-optimisation-dossier-mdph-aah-hpi-autisme.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,248 [INFO] Exocortex.VectorStore: Note 'strategie-perte-poids-charge-mentale-picard-overnight-oats.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,320 [INFO] Exocortex.VectorStore: Note 'strategie-pricing-tunnel-vente-coaching.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,387 [INFO] Exocortex.VectorStore: Note 'strategie-recadrage-litige-administratif.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,459 [INFO] Exocortex.VectorStore: Note 'strategie-recrutement-filtrage-semantique-mmorpg.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,536 [INFO] Exocortex.VectorStore: Note 'strategie-recrutement-guilde-social-midcore.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,608 [INFO] Exocortex.VectorStore: Note 'strategie-soutenance-roadmap-arbitrages.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,684 [INFO] Exocortex.VectorStore: Note 'strategie-tripwire-automatisation-livraison.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,755 [INFO] Exocortex.VectorStore: Note 'strategie-veille-technologique-chef-projet-digital.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,827 [INFO] Exocortex.VectorStore: Note 'strategies-engagement-jeux-gestion-4x.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,897 [INFO] Exocortex.VectorStore: Note 'stremio-est-il-toujours-la-meilleur-solution-pour.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:01,972 [INFO] Exocortex.VectorStore: Note 'substitutions-culinaires-proprietes-riz.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,058 [INFO] Exocortex.VectorStore: Note 'suivi-glycemique-titration-metformine-lantus.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,137 [INFO] Exocortex.VectorStore: Note 'taxonomie-animation-adulte-charge-cognitive.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,205 [INFO] Exocortex.VectorStore: Note 'taxonomie-consommation-narrative-fast-food-vs-gourmet.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,276 [INFO] Exocortex.VectorStore: Note 'taxonomie-narrative-connoisseur-manga.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,356 [INFO] Exocortex.VectorStore: Note 'taxonomy-manhwa-consumption-fast-food-vs-gourmet.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,438 [INFO] Exocortex.VectorStore: Note 'techniques-preparation-riz-gohan-sumeshi.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,520 [INFO] Exocortex.VectorStore: Note 'tft-decision-matrix-set-17.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,593 [INFO] Exocortex.VectorStore: Note 'theorie-extreme-centre-tripartition-politique.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,665 [INFO] Exocortex.VectorStore: Note 'thermodynamique-chimie-vaporisation.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,750 [INFO] Exocortex.VectorStore: Note 'tracking-performances-mplus-warcraft-logs-api.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,816 [INFO] Exocortex.VectorStore: Note 'transition-diagnostique-hpi-tsa-communication.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,889 [INFO] Exocortex.VectorStore: Note 'transition-hm-mm-sondage-roster.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:02,965 [INFO] Exocortex.VectorStore: Note 'tu-crois-quon-pourrait-travailler-ensemble-a-forma.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,040 [INFO] Exocortex.VectorStore: Note 'tu-peux-retrouver-la-discussion-dans-laquelle-nous.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,121 [INFO] Exocortex.VectorStore: Note 'typologie-complexite-gameplay-cpu-vs-ram.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,191 [INFO] Exocortex.VectorStore: Note 'unification-domotique-synology-home-assistant.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,258 [INFO] Exocortex.VectorStore: Note 'upgrade-intel-lga1700-preservation-ddr4.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,332 [INFO] Exocortex.VectorStore: Note 'ux-design-psychologie-page-livraison-cocon.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,403 [INFO] Exocortex.VectorStore: Note 'ux-strategie-conversion-sante-mentale.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,477 [INFO] Exocortex.VectorStore: Note 'validation-diagnostic-tsa-commission-audhd-hpi.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,548 [INFO] Exocortex.VectorStore: Note 'violation-inegalite-bell-realisme-non-localite-hasard.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,624 [INFO] Exocortex.VectorStore: Note 'visualisation-interactive-systemes-complexes-html-js.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,690 [INFO] Exocortex.VectorStore: Note 'white-supremacy-collapses-instantly-when-you-reali.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,763 [INFO] Exocortex.VectorStore: Note 'wifi-5-suffisant-pour-du-cloud-local-via-apollo-ar.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:03,974 [INFO] Exocortex.VectorStore: Note 'workflow-mixx-pop-suno-genre-switch.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:04,056 [INFO] Exocortex.VectorStore: Note 'workflow-production-hyperpop-digicore-maschine-mk2.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:04,131 [INFO] Exocortex.VectorStore: Note 'workflow-production-hyperpop-digicore-optimisation.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:04,202 [INFO] Exocortex.VectorStore: Note 'workflow-wordpress-git-deployment-php-debug.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:04,263 [INFO] Exocortex.VectorStore: Note 'ya-peut-etre-une-confusion-quand-je-parle-des-gran.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:04,344 [INFO] Exocortex.VectorStore: Note 'ça-représente-quoi-2000-baht-en-proportion-du-sala.md' indexée avec succès dans LanceDB.
2026-10-20 21:35:04,359 [INFO] Exocortex.LLM: Modèle 'bge-m3' déchargé avec succès de la VRAM (keep_alive=0).
2026-10-20 21:35:04,359 [INFO] Exocortex.VectorStore: Synchronisation LanceDB achevée : 479 notes indexées.
2026-10-20 21:35:04,359 [INFO] Exocortex.TakeoutIngestor: --- COMPILATION DES MÉGA-FICHIERS GOOGLE DRIVE ---
2026-10-20 21:35:04,359 [INFO] Exocortex.DriveCompiler: === DÉBUT COMPILATION DES 4 MÉGA-DOCUMENTS GOOGLE DRIVE ===
2026-10-20 21:35:04,359 [INFO] Exocortex.DriveCompiler: Compilation de 00_CORE_IDENTITE_ET_STYLE.md...
2026-10-20 21:35:04,360 [INFO] Exocortex.DriveCompiler: 00_CORE_IDENTITE_ET_STYLE.md écrit avec succès (36196 octets).
2026-10-20 21:35:04,360 [INFO] Exocortex.DriveCompiler: Compilation de 01_TELEMETRIE_ET_EPISODIQUE_7J.md...
2026-10-20 21:35:04,360 [INFO] Exocortex.DriveCompiler: 01_TELEMETRIE_ET_EPISODIQUE_7J.md écrit avec succès (1030 octets).
2026-10-20 21:35:04,360 [INFO] Exocortex.DriveCompiler: Compilation de 02_PROJETS_ET_CONCEPTS_ACTIFS.md...
2026-10-20 21:35:04,399 [INFO] Exocortex.DriveCompiler: 02_PROJETS_ET_CONCEPTS_ACTIFS.md écrit avec succès (15 concepts inclus).
2026-10-20 21:35:04,410 [INFO] Exocortex.DriveCompiler: Compilation de 03_INDEX_GRAPHE_CONCEPTS.md...
2026-10-20 21:35:04,443 [INFO] Exocortex.DriveCompiler: 03_INDEX_GRAPHE_CONCEPTS.md écrit avec succès (479 notes indexées au total).
2026-10-20 21:35:04,443 [INFO] Exocortex.DriveCompiler: === FIN DE COMPILATION GOOGLE DRIVE AVEC SUCCÈS ===
2026-10-20 21:35:04,541 [INFO] Exocortex.TakeoutIngestor: === FIN DU MODULE 1 AVEC SUCCÈS ===
2026-10-20 21:35:04,541 [INFO] Exocortex.TakeoutIngestor: Statistiques SQLite finales : {'raw_activity': 0, 'daily_metrics': 0, 'chat_sessions': 480, 'historical_footprints': 73154}      
2026-10-20 21:35:04,558 [INFO] Exocortex.Launcher: Ingestion Takeout achevée avec succès : {'sessions_count': 480, 'linked_footprints': 4093, 'burst_clusters': 4410, 'staging_prompts_file': 'C:\\Users\\Jijax\\projets\\cerveau-deux\\Vault_Data\\_System_Buffer\\takeout_staging\\00_USER_PROMPTS_ONLY.md', 'staging_batches_count': 15, 'web_prompt_file': 'C:\\Users\\Jijax\\projets\\cerveau-deux\\Vault_Data\\_System_Buffer\\takeout_staging\\PROMPT_A_COPIER_DANS_GEMINI_WEB.txt', 'indexed_concepts_count': 479, 'drive_files': {'00_CORE': 'C:\\Users\\Jijax\\projets\': 'C:\\Users\\Jijax\\projets\\cerveau-deux\\Vault_Da\cerveau-deux\\Vault_Data\\Google_Drive_Sync\\00_CORE_IDENTITE_ET_STYLE.md', '01_TELEMETRIE_7J': 'C:\\Users\\Jijax\\projets\\cerveau-deux\\Vault_Data\\Google_Drive_Sync\\01_TELEMETRIE_ET_t_staging\\PROMPT_A_COPIER_DANS_GEMINI_WEB.txt', 'indEPISODIQUE_7J.md', '02_CONCEPTS_ACTIFS': 'C:\\Users\\Jijax\\projets\\cerveau-deux\\Vault_Data\\Google_Drive_Sync\\02_PROJETS_ET_CONCEPTS_ACTIFS.md', '03_INDEX_GRAPHE': 'C:\\Users\\Jijax\\s\\Jijax\\projets\\cerveau-deux\\Vault_Data\\Google_Dprojets\\cerveau-deux\\Vault_Data\\Google_Drive_Sync\\03_INDEX_GRAPHE_CONCEPTS.md'}, 'db_stats': {'raw_activity': 0, 'daily_metrics': 0, 'chat_sessions': 480, 'historical_footprints': 731GRAPHE': 'C:\\Users\\Jijax\\projets\\cerveau-deux\\Va54}}