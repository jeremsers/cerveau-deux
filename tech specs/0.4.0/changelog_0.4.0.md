---
task_id: "EXO-012"
project_id: "exocortex"
component_tag: "deep-sleep-consolidator"
title: "v0.4.0 — Sommeil Profond (Défragmentation du Graphe, Contradictions & Sas Vocal)"
status: "ready_for_agent"
---
# EXO-012 — v0.4.0 — Sommeil Profond (Défragmentation du Graphe, Contradictions & Sas Vocal)

## 1. CHANGELOG & SPÉCIFICATIONS TECHNIQUES

### 1.1 Objectif Architectural
Doter l'Exocortex d'un cycle de **Sommeil Profond** capable de :
1. **Capturer la pensée hors-clavier** via un sas d'ingestion de mémos vocaux (`voice_ingestor.py`) sans jamais polluer la VRAM d'Ollama.
2. **Lutter contre l'entropie du coffre Obsidian** en fusionnant les fiches redondantes (`graph_defragmenter.py`) et en réécrivant automatiquement les `[[wikilinks]]` dans tout le coffre.
3. **Tracer l'évolution des arbitrages techniques** en annotant les anciennes fiches lorsqu'une décision récente les contredit ou les remplace.

### 1.2 Chantier 1 : Sas d'Ingestion Vocale Isolé (`src/ingestors/voice_ingestor.py`)
- **Dossier surveillé :** `Vault_Data/_System_Buffer/voice_inbox/` (synchronisable avec le téléphone via Google Drive ou Syncthing). Formats acceptés : `.m4a`, `.mp3`, `.ogg`, `.wav`, `.flac`.
- **Isolation Mémoire Stricte :** Pour éviter que le runtime C++ `ctranslate2` de `faster-whisper` ne garde des handles CUDA bloqués sous Windows 11 :
  - Soit la transcription tourne sur CPU en quantification `int8` (`device="cpu", compute_type="int8"`), soit dans un sous-processus isolé qui se termine avant la Passe 1.
- **Flux de Traitement :**
  1. Transcrit l'audio en texte horodaté (avec date de création issue du mtime du fichier ou du nom `YYYYMMDD_HHMMSS`).
  2. Crée une session dans `chat_sessions` (`session_id="voice_YYYYMMDD_HHMMSS"`) et `chat_messages`.
  3. Distille la réflexion en fiche atomique dans `02_Concepts/` (`origin: ["voice_memo"]`) via le pipeline structuré existant.
  4. Déplace le fichier audio traité dans `Vault_Data/_System_Buffer/voice_inbox/processed/`.

### 1.3 Chantier 2 : Défragmenteur Sémantique & Réécriture des Wikilinks (`src/consolidators/graph_defragmenter.py`)
- **Détection des Doublons (Double Garde-Fou) :**
  1. Charge tous les vecteurs de la table LanceDB `concepts` et calcule la similarité cosinus par paires **au sein du même `semantic_topic`**.
  2. Filtre les paires ayant `cosine_similarity >= 0.88` **ET** partageant au moins 1 token significatif hors stopwords dans leur titre/tags.
- **Fusion & Validation LLM (26B) :**
  - Soumet la paire candidate au modèle lourd avec un schéma Pydantic `ConceptMergeSchema` (`should_merge: bool`, `canonical_title: str`, `canonical_slug: str`, `merged_summary_1_line: str`, `merged_markdown_body: str`, `contradiction_detected: bool`, `contradiction_explanation: Optional[str]`).
  - Si `should_merge == True` :
    - Additionne les `total_time_invested_min`, fusionne les listes `tags`, `origin` et `telemetry_lines` (sources épisodiques).
    - Écrit la fiche canonique via `write_concept_file()`.
    - Déplace les anciennes fiches fusionnées dans `Vault_Data/02_Concepts/_Archive_Merged/` (zéro perte de données) et supprime leurs anciens slugs de LanceDB.
    - **Mise à jour globale des `[[wikilinks]]` :** Parcourt `01_Episodique/` et `02_Concepts/` pour remplacer `[[Ancien Titre]]` et `[[ancien-slug]]` par `[[Nouveau Titre]]`.

### 1.4 Chantier 3 : Détection des Contradictions & Évolution d'Arbitrage
Lorsque deux fiches sont proches (`0.78 <= cosine_similarity < 0.88`) ou que `should_merge == False` mais `contradiction_detected == True` (ex: passage d'un outil A à un outil B plus récent) :
- Le défragmenteur n'écrase pas l'ancienne fiche mais injecte en haut de son corps Markdown (via `markdown_io.py`) un callout Obsidian idempotent :
  ```markdown
  > [!warning] Évolution d'Arbitrage (Mis à jour le YYYY-MM-DD)
  > Ce choix architectural a évolué dans la note plus récente [[Nouvelle Fiche]] : *[contradiction_explanation]*.
  ```

---

## 2. PROMPT D'EXÉCUTION POUR L'AGENT CODEUR

Tu es un Ingénieur Système Senior Python. Implémente la spécification **EXO-012 (v0.4.0 — Sommeil Profond : Défragmentation du Graphe, Contradictions & Sas Vocal)**.

### Invariants & Contraintes Strictes
1. **Zéro Perte de Données :** Aucune note fusionnée ne doit être supprimée par `unlink()` sans avoir été préalablement déplacée dans `Vault_Data/02_Concepts/_Archive_Merged/`.
2. **Idempotence des Callouts d'Évolution :** Si une fiche contient déjà un bloc `> [!warning] Évolution d'Arbitrage` pointant vers la même fiche cible, ne jamais le dupliquer.
3. **Intégrité des Wikilinks :** La réécriture des `[[wikilinks]]` après fusion doit gérer les formats `[[Titre]]`, `[[slug]]` et `[[slug|Alias]]`.

### Étapes d'Implémentation
1. **Mettre à jour `src/config.py` :**
   - Ajouter `VOICE_INBOX_DIR` (`self.SYSTEM_BUFFER_DIR / "voice_inbox"`), `VOICE_PROCESSED_DIR` (`self.VOICE_INBOX_DIR / "processed"`), et `CONCEPTS_ARCHIVE_MERGED_DIR` (`self.CONCEPTS_DIR / "_Archive_Merged"`). Les inclure dans `ensure_directories()`.
2. **Créer `src/ingestors/voice_ingestor.py` :**
   - Implémenter `VoiceIngestor` capable de transcrire les fichiers audio (via `faster_whisper` en mode `cpu`/`int8` s'il est installé, ou un transcripteur injectable pour les tests), d'enregistrer la session dans `chat_sessions`/`chat_messages`, de générer la fiche conceptuelle et d'archiver l'audio dans `processed/`.
3. **Créer `src/consolidators/graph_defragmenter.py` :**
   - Implémenter `cosine_similarity(v1: List[float], v2: List[float]) -> float` en pur Python/`math` (sans dépendance lourde obligatoire).
   - Implémenter `GraphDefragmenter` avec :
     - `find_merge_and_contradiction_candidates(similarity_threshold: float = 0.88, contradiction_min_sim: float = 0.78)`
     - `merge_concepts_pair(note_a_path: Path, note_b_path: Path, merge_decision: ConceptMergeSchema) -> Path`
     - `annotate_contradiction(older_note_path: Path, newer_note_title: str, explanation: str, date_str: str) -> None`
     - `rewrite_vault_wikilinks(old_targets: List[str], new_target: str) -> int`
4. **Mettre à jour `run_exocortex.py` :**
   - Ajouter `--ingest-voice` et `--defrag-graph` dans l'orchestrateur CLI.
5. **Créer `tests/test_v040_deep_sleep_verification.py` :**
   - `test_graph_defragmenter_merge_and_wikilink_rewrite` : Crée 2 fiches redondantes A et B + un journal épisodique pointant vers `[[A]]`, exécute `merge_concepts_pair`, et vérifie que : (1) la fiche fusionnée cumule les `total_time_invested_min`, (2) les anciennes fiches sont dans `_Archive_Merged/`, et (3) le journal épisodique pointe désormais vers la nouvelle fiche.
   - `test_contradiction_callout_injection_idempotence` : Vérifie l'ajout du callout `> [!warning] Évolution d'Arbitrage` en haut de l'ancienne note et son idempotence en cas de double appel.
   - `test_voice_ingestor_pipeline` : Simule un fichier mémo dans `voice_inbox/` avec un transcripteur mocké et vérifie l'insertion SQLite, la création de la note dans `02_Concepts/` et le déplacement dans `processed/`.
   - Exécuter `pytest tests/ -v`.
```