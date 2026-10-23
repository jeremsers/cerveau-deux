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
