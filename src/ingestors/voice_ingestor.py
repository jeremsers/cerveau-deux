"""
Module 9 : Sas d'Ingestion Vocale Isolé (v0.4.0 / EXO-012).
Scanne Vault_Data/_System_Buffer/voice_inbox/ pour ingérer les mémos audio (.m4a, .mp3, .ogg, .wav, .flac),
les transcrire (via faster-whisper sur CPU int8 ou transcripteur injecté sans toucher à la VRAM CUDA),
persister la session dans SQLite (chat_sessions / chat_messages),
générer la fiche conceptuelle atomique dans 02_Concepts/ (origin: ["voice_memo"]),
et archiver le fichier source dans processed/.
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pydantic import BaseModel, Field

from src.config import AUTHORIZED_SEMANTIC_TOPICS, normalize_to_macro_topic, settings
from src.database.db_manager import ChatMessageRecord, ChatSessionRecord, DBManager
from src.llm.ollama_client import llm_client
from src.llm.prompts import PROMPT_VOICE_MEMO_SYSTEM, PROMPT_VOICE_MEMO_USER
from src.utils.markdown_io import (
    ConceptFrontmatter,
    ParsedConceptNote,
    write_concept_file,
)

logger = logging.getLogger("Exocortex.VoiceIngestor")

SUPPORTED_AUDIO_EXTENSIONS = {".m4a", ".mp3", ".ogg", ".wav", ".flac"}


class VoiceMemoSchema(BaseModel):
    """Sortie structurée de la distillation d'un mémo vocal (v0.5.3, B12)."""
    concept_title: str = Field(description="Titre conceptuel précis, jamais le début de la transcription.")
    semantic_topic: str = Field(description="Exactement l'une des macro-catégories autorisées.")
    tags: List[str] = Field(default_factory=list, description="2 à 5 tags en kebab-case.")
    summary_1_line: str = Field(description="Résumé dense en une phrase.")
    synthesized_markdown_body: str = Field(description="Corps Markdown structuré : idées, décisions, actions.")


def _allowed_taxonomy_block() -> str:
    return "\n".join(f"- `{k}` : {v}" for k, v in AUTHORIZED_SEMANTIC_TOPICS.items() if k != "A_Trier")


def _slugify(text: str) -> str:
    """Transforme un titre en slug kebab-case propre et sûr pour le système de fichiers."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text[:60] or "memo-vocal"


class VoiceIngestor:
    """Ingesteur de mémos vocaux avec isolation stricte de la mémoire VRAM."""

    def __init__(
        self,
        db_manager: Optional[DBManager] = None,
        inbox_dir: Optional[Path] = None,
        processed_dir: Optional[Path] = None,
        transcriber: Optional[Callable[[Path], str]] = None,
    ) -> None:
        self.db = db_manager or DBManager()
        self.inbox_dir = inbox_dir or settings.VOICE_INBOX_DIR
        self.processed_dir = processed_dir or settings.VOICE_PROCESSED_DIR
        self.transcriber = transcriber

        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def extract_file_datetime(self, audio_path: Path) -> datetime:
        """
        Extrait la date et l'heure du mémo vocal à partir du nom de fichier
        (ex: 20261024_143000 ou 2026-10-24) ou de la date de modification du fichier.
        """
        stem = audio_path.stem
        # Pattern 1 : YYYYMMDD_HHMMSS ou YYYYMMDD-HHMMSS
        m1 = re.search(r"(\d{4})(\d{2})(\d{2})[_-](\d{2})(\d{2})(\d{2})", stem)
        if m1:
            try:
                y, m, d, h, mi, s = map(int, m1.groups())
                return datetime(y, m, d, h, mi, s)
            except ValueError:
                pass

        # Pattern 2 : YYYY-MM-DD
        m2 = re.search(r"(\d{4})[-_](\d{2})[-_](\d{2})", stem)
        if m2:
            try:
                y, m, d = map(int, m2.groups())
                return datetime(y, m, d, 12, 0, 0)
            except ValueError:
                pass

        # Fallback : date mtime du fichier
        try:
            return datetime.fromtimestamp(audio_path.stat().st_mtime)
        except Exception:
            return datetime.now()

    def transcribe_audio(self, audio_path: Path) -> str:
        """Transcrit un mémo audio (0 Mo VRAM - CPU int8 ou transcripteur injecté)."""
        if self.transcriber is not None:
            return self.transcriber(audio_path)

        # Inférence CPU int8 via faster-whisper si disponible
        try:
            from faster_whisper import WhisperModel

            logger.info("Transcription CPU int8 via faster_whisper pour : %s", audio_path.name)
            model = WhisperModel("base", device="cpu", compute_type="int8")
            segments, _ = model.transcribe(str(audio_path), beam_size=5)
            text = " ".join([segment.text for segment in segments]).strip()
            return text
        except ImportError:
            logger.warning(
                "faster-whisper n'est pas installé. Fallback déterministe pour %s.",
                audio_path.name,
            )
            return f"(Transcription audio non disponible pour {audio_path.name})"
        except Exception as exc:
            logger.error("Erreur de transcription audio pour %s : %s", audio_path.name, exc)
            return f"(Échec de transcription pour {audio_path.name} : {exc})"

    def distill_memo(
        self,
        transcription: str,
        audio_name: str,
        dt: datetime,
    ) -> Tuple[str, str, str, str, List[str]]:
        """
        Détermine le titre, le sujet, le résumé, le corps et les tags de la note (v0.5.3, B12).
        Distillation structurée par le 12B (VoiceMemoSchema) si Ollama répond ; sinon repli
        heuristique classé A_Trier (et non plus Dev_et_Architecture_Tech d'office).
        La transcription brute est toujours conservée en fin de corps.
        """
        clean_text = transcription.strip()
        date_str = dt.strftime("%Y-%m-%d")
        transcript_section = f"## Transcription brute\n\n{clean_text}\n"

        # Repli heuristique
        first_line = re.sub(r"^[^\w]+", "", clean_text.split("\n")[0]).strip()
        raw_title = first_line[:60].strip() or f"Note Vocale du {date_str}"
        title = raw_title if raw_title.startswith(("Note Vocale", "Réflexion")) else f"Réflexion Vocale : {raw_title}"
        topic = "A_Trier"
        summary_1_line = clean_text[:120].replace("\n", " ").strip()
        tags = ["vocal", "reflexion"]
        body = transcript_section

        if llm_client.is_alive() and len(clean_text) > 40:
            try:
                distilled = llm_client.generate_structured(
                    prompt=PROMPT_VOICE_MEMO_USER.format(
                        allowed_taxonomy=_allowed_taxonomy_block(),
                        date_str=date_str,
                        transcription=clean_text[:12000],
                    ),
                    response_model=VoiceMemoSchema,
                    system=PROMPT_VOICE_MEMO_SYSTEM,
                    model=settings.MODEL_FAST_VISION,
                    enable_thinking=False,
                    num_predict=4096,
                )
                title = distilled.concept_title.strip() or title
                topic = normalize_to_macro_topic(distilled.semantic_topic)
                summary_1_line = distilled.summary_1_line.strip() or summary_1_line
                tags = ["vocal"] + [_slugify(t) for t in distilled.tags if t.strip()][:6]
                synthesized = re.sub(r">\s*\[!abstract\][^\n]*\n(?:>[^\n]*\n?)*", "", distilled.synthesized_markdown_body).strip()
                body = f"{synthesized}\n\n{transcript_section}" if synthesized else transcript_section
            except Exception as llm_exc:
                logger.warning("Distillation LLM du mémo vocal %s impossible (%s) : repli A_Trier.", audio_name, llm_exc)

        return title, topic, summary_1_line, body, tags

    def process_file(self, audio_path: Path) -> Optional[Path]:
        """Traite un fichier audio unique de bout en bout."""
        if audio_path.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:
            return None

        logger.info("Traitement du mémo vocal : %s", audio_path.name)
        dt = self.extract_file_datetime(audio_path)
        date_str = dt.strftime("%Y-%m-%d")
        ts_str = dt.strftime("%Y-%m-%d %H:%M:%S")

        session_id = f"voice_{dt.strftime('%Y%m%d_%H%M%S')}_{_slugify(audio_path.stem)[:16]}"

        # 1. Transcription (0 Mo VRAM)
        transcription = self.transcribe_audio(audio_path)
        u_chars = len(transcription)

        # 2. Persistance dans SQLite (chat_sessions & chat_messages)
        session_rec = ChatSessionRecord(
            session_id=session_id,
            timestamp_start=dt,
            timestamp_end=dt,
            turn_count=1,
            user_char_count=u_chars,
            extracted_topics_json="[]",
            generated_notes_json="[]",
            summary=transcription[:200],
            distillation_status="success",
        )
        self.db.insert_chat_sessions_batch([session_rec])

        message_rec = ChatMessageRecord(
            session_id=session_id,
            turn_index=0,
            timestamp=dt,
            user_prompt=transcription,
            ai_response="",
            user_char_count=u_chars,
        )
        self.db.insert_chat_messages_batch([message_rec])

        # 3. Distillation en note conceptuelle
        title, topic, summary_1_line, body, tags = self.distill_memo(transcription, audio_path.name, dt)
        slug = _slugify(title)
        concept_file = settings.CONCEPTS_DIR / f"{slug}.md"

        # Gestion collision de nom de fichier
        counter = 2
        while concept_file.exists():
            concept_file = settings.CONCEPTS_DIR / f"{slug}-{counter}.md"
            counter += 1

        fm = ConceptFrontmatter(
            id=concept_file.stem,
            title=title,
            type="concept",
            origin=["voice_memo"],
            semantic_topic=topic,
            tags=tags,
            session_id=session_id,
            created_at=date_str,
            updated_at=date_str,
            total_time_invested_min=15,
            summary_1_line=summary_1_line,
            # Forfait de 15 min par mémo, pas une mesure (A9)
            time_is_estimated=True,
        )

        telemetry_lines = [
            "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)",
            "> - **Temps estimé sur ce sujet :** 15m (forfait mémo vocal, non mesuré)",
            "> - **Sources épisodiques :**",
            f">   - Mémo vocal `{audio_path.name}` ({dt.strftime('%Y-%m-%d %H:%M')})",
            "> - **Connexions sémantiques :**",
        ]

        note = ParsedConceptNote(
            frontmatter=fm,
            title_h1=title,
            body=body,
            telemetry_lines=telemetry_lines,
            file_path=concept_file,
        )
        write_concept_file(note, concept_file)
        logger.info("Fiche conceptuelle créée pour mémo vocal : %s (%s)", concept_file.name, topic)

        # Rattachement de la fiche et du topic à la session vocale (Explorateur épistémique)
        self.db.update_session_distillation_metadata(
            session_id=session_id,
            topics_list=[topic],
            notes_list=[concept_file.stem],
            summary=summary_1_line,
            distillation_status="success",
        )

        # 4. Archivage du fichier audio dans processed/
        target_processed = self.processed_dir / audio_path.name
        if target_processed.exists():
            target_processed = self.processed_dir / f"{audio_path.stem}_{datetime.now().strftime('%Y%m%d%H%M%S')}{audio_path.suffix}"

        try:
            shutil.move(str(audio_path), str(target_processed))
            logger.info("Mémo vocal archivé dans : %s", target_processed.name)
        except Exception as exc:
            logger.warning("Échec déplacement mémo vocal %s : %s", audio_path.name, exc)

        return concept_file

    def run(self) -> Dict[str, Any]:
        """Parcourt le dossier voice_inbox/ et traite tous les mémos vocaux en attente."""
        created_notes: List[Path] = []
        errors: List[str] = []

        if not self.inbox_dir.exists():
            return {"processed_count": 0, "created_notes": [], "errors": []}

        audio_files = [
            f for f in sorted(self.inbox_dir.iterdir())
            if f.is_file() and f.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
        ]

        logger.info("%d mémo(s) vocal/vocaux trouvé(s) dans %s", len(audio_files), self.inbox_dir)

        for audio_file in audio_files:
            try:
                res = self.process_file(audio_file)
                if res:
                    created_notes.append(res)
            except Exception as exc:
                logger.error("Erreur traitement %s : %s", audio_file.name, exc)
                errors.append(f"{audio_file.name}: {exc}")

        return {
            "processed_count": len(created_notes),
            "created_notes": created_notes,
            "errors": errors,
        }

