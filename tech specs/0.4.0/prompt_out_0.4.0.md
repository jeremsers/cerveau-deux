L'implémentation complète de la spécification EXO-012 (v0.4.0 — Sommeil Profond : Défragmentation du Graphe, Contradictions & Sas Vocal) est achevée avec 100 % de tests validés (34/34 tests passés) et zéro régression.

Invariants et Contraintes Respectés
Zéro Perte de Données : Aucun appel unlink() n'est effectué sur les notes fusionnées. Toute note consolidée est déplacée de manière sécurisée dans Vault_Data/02_Concepts/_Archive_Merged/.
Idempotence des Callouts d'Évolution : L'injection du callout > [!warning] Évolution d'Arbitrage vérifie la présence préalable du lien vers la fiche cible et du mot-clé avant toute écriture pour éviter toute duplication.
Intégrité des Wikilinks : La réécriture de graphe rewrite_vault_wikilinks prend en charge de façon transparente les formes [[Titre]], [[slug]] et [[slug|Alias]] sans altérer l'alias d'affichage.
Récapitulatif des Composants Implémentés

Configuration Centrale (src/config.py) :

Ajout des répertoires du sas vocal et d'archivage : VOICE_INBOX_DIR (_System_Buffer/voice_inbox), VOICE_PROCESSED_DIR (processed/), et CONCEPTS_ARCHIVE_MERGED_DIR (02_Concepts/_Archive_Merged).
Intégration dans ensure_directories().

Sas d'Ingestion Vocale Isolé (src/ingestors/voice_ingestor.py) :

VoiceIngestor :
Formats supportés : .m4a, .mp3, .ogg, .wav, .flac.
Transcription isolée sans pollution CUDA (support CPU int8 via faster_whisper ou transcripteur injecté pour les tests).
Persistance de la session audio dans SQLite (chat_sessions avec turn_count=1, chat_messages avec turn_index=0).
Distillation et création de la fiche dans 02_Concepts/ (origin: ["voice_memo"], frontmatter complet et callout de généalogie).
Déplacement automatique du fichier audio source dans processed/.

Défragmenteur Sémantique & Évolution d'Arbitrage (src/consolidators/graph_defragmenter.py) :

cosine_similarity(v1, v2) : calcul vectoriel en pur Python/math standard (0 Mo VRAM).
Schéma structuré Pydantic ConceptMergeSchema.
find_merge_and_contradiction_candidates :
Regroupement intra-topic sémantique sur la table LanceDB concepts.
Double filtre : similarité cosinus 
≥
0.88
≥0.88 ET partage d'au moins 1 token significatif hors stopwords.
Détection des contradictions potentielles pour 
0.78
≤
cos_sim
<
0.88
0.78≤cos_sim<0.88.
merge_concepts_pair :
Cumul de total_time_invested_min et fusion des tags/origines.
Sauvegarde de la fiche canonique unifiée.
Déplacement sécurisé des anciennes fiches dans _Archive_Merged/ et mise à jour de LanceDB.
Réécriture automatique des [[wikilinks]] dans 01_Episodique/ et 02_Concepts/.
annotate_contradiction :
Injection du callout > [!warning] Évolution d'Arbitrage en tête de l'ancienne note avec idempotence garantie.

Orchestrateur CLI (run_exocortex.py) :

Ajout des commandes CLI --ingest-voice et --defrag-graph.

Suite de Tests de Vérification (tests/test_v040_deep_sleep_verification.py) :

test_cosine_similarity_pure_python : validation géométrique de la similarité cosinus.
test_graph_defragmenter_merge_and_wikilink_rewrite : validation du cumul de temps, archivage sans unlink() et réécriture des wikilinks (avec gestion des alias).
test_contradiction_callout_injection_idempotence : validation de l'injection et de l'idempotence du callout d'évolution d'arbitrage.
test_voice_ingestor_pipeline : validation du pipeline mémo vocal, persistance SQLite et archivage dans processed/.
Résultat Global des Tests
powershell
======================= 34 passed, 4 warnings in 19.92s =======================
tests/test_v012_verification.py (1 test)          PASSED                  [  2%]
tests/test_v013_verification.py (1 test)          PASSED                  [  5%]
tests/test_v014_verification.py (7 tests)         PASSED                  [ 26%]
tests/test_v020_kanban_verification.py (4 tests)  PASSED                  [ 38%]
tests/test_v021_refactoring_verification.py (5)   PASSED                  [ 52%]
tests/test_v022_mcp_graphrag_verification.py (6)  PASSED                  [ 70%]
tests/test_v030_proactivity_verification.py (3)   PASSED                  [ 79%]
tests/test_v035_passive_sensors_verification.py (3) PASSED                [ 88%]
tests/test_v040_deep_sleep_verification.py (4)    PASSED                  [100%]