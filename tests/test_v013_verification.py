"""
Suite de validation v0.1.3, rendue hermétique en v0.5.6 (audit F1, F3).
Mêmes chantiers qu'à l'origine, sans dépendre ni modifier le coffre réel : l'état d'entrée
(doublons, notes tronquées, note valide) est construit par le test.
1. Déduplication SQLite des empreintes et ingestion des seules sessions qualifiées
2. Auto-réparation JSON et support du thinking
3. Paramètres VRAM, Modelfile num_ctx et purge active
4. Notes tronquées de la v0.1.2 mises en quarantaine
5. Protection anti-écrasement par #A_Trier
"""

from __future__ import annotations

import inspect
import json
import re
import sys
from datetime import datetime
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.config import settings
from src.database.db_manager import DBManager, HistoricalFootprintRecord
from src.ingestors.takeout_ingestor import (
    ParsedTurn,
    ReconstructedSession,
    TakeoutIngestor,
    save_distilled_concept_note,
    scan_and_upgrade_existing_concepts,
)
from src.llm.ollama_client import HybridLLMClient, llm_client, repair_truncated_json
from tests.test_v012_verification import write_gemini_html_export


def test_v013_chantier1_dedup_and_qualified_sessions_only(exo_env):
    db = exo_env.db
    fp = HistoricalFootprintRecord(source="youtube", timestamp=datetime(2026, 3, 1, 20), title_or_query="Vidéo")
    db.insert_historical_footprints_batch([fp, fp, fp])
    with db.get_connection() as conn:
        assert conn.execute("SELECT COUNT(*) FROM historical_footprints;").fetchone()[0] == 1
        indexes = [r["name"] for r in conn.execute("PRAGMA index_list('historical_footprints');").fetchall()]
    assert "idx_unique_footprint" in indexes

    n_turns = write_gemini_html_export(settings.TAKEOUT_DIR / "MonActivite_gemini.html", days=3, turns_per_day=4, noise_days=2)
    result = TakeoutIngestor(db_manager=db).run()

    assert result["sessions_count"] == 3 and result["noise_sessions_count"] == 2
    with db.get_connection() as conn:
        # Takeout : seules les sessions qualifiées entrent dans chat_sessions...
        assert conn.execute("SELECT COUNT(*) FROM chat_sessions;").fetchone()[0] == 3
        assert conn.execute(
            "SELECT COUNT(*) FROM chat_sessions WHERE turn_count < 3 OR user_char_count < 250;"
        ).fetchone()[0] == 0
        # ... mais chat_messages conserve l'intégralité des tours, bruit compris
        assert conn.execute("SELECT COUNT(*) FROM chat_messages;").fetchone()[0] == n_turns


def test_v013_chantier2_repair_truncated_json():
    raw_with_thought = (
        "<|thought|>\nRéflexion.\n<|/thought|>\n"
        '{"concept_title": "Optimisation CPU", "slug": "optimisation-cpu", "semantic_topic": "HomeLab_et_Hardware", '
        '"tags": ["cpu"], "summary_1_line": "S.", "synthesized_markdown_body": "### Contexte\\nContention.", '
        '"is_worth_indexing": true, "related_concepts": []}'
    )
    assert json.loads(repair_truncated_json(raw_with_thought))["concept_title"] == "Optimisation CPU"

    raw_truncated_body = (
        '{"concept_title": "Neuroplasticité Adulte", "slug": "neuroplasticite-adulte", '
        '"semantic_topic": "Introspection_et_Neuroatypie", "tags": ["langues"], "summary_1_line": "S.", '
        '"synthesized_markdown_body": "### Contexte\\nL\'adulte dispose de capacités logiques solides. '
        "Exploiter la capacité de déconstruction pour assimiler la structure"
    )
    data_b = json.loads(repair_truncated_json(raw_truncated_body))
    assert data_b["concept_title"] == "Neuroplasticité Adulte"
    assert data_b["synthesized_markdown_body"].endswith("solides.")

    raw_think_tag = (
        "<think>Réflexion</think>"
        '{"concept_title": "Titre C", "slug": "titre-c", "semantic_topic": "IA_et_LLM_Local", "tags": [], '
        '"summary_1_line": "S1", "synthesized_markdown_body": "Body C.", "is_worth_indexing": true, "related_concepts": []}'
    )
    assert json.loads(repair_truncated_json(raw_think_tag))["concept_title"] == "Titre C"


def test_v013_chantier3_vram_parameters():
    assert settings.VRAM_STRICT_ABORT_FREE_GB == 8.0
    assert settings.VRAM_REASONING_MIN_FREE_GB == 12.8
    assert settings.MODEL_REASONING == settings.MODEL_HEAVY_SYNTHESIS
    assert "num_ctx 16384" in inspect.getsource(HybridLLMClient.ensure_local_gguf_models)

    sig = inspect.signature(HybridLLMClient.generate_structured)
    assert sig.parameters["enable_thinking"].default is True
    assert sig.parameters["num_predict"].default == 8192
    assert sig.parameters["allow_model_switch_fallback"].default is False
    assert hasattr(llm_client, "force_clear_vram")


def _takeout_note(path: Path, sid: str, body: str) -> None:
    path.write_text(
        "---\n"
        f'id: "{path.stem}"\ntitle: "{path.stem}"\norigin: ["gemini_takeout"]\nsession_id: "{sid}"\n'
        'semantic_topic: "IA_et_LLM_Local"\ndistillation_status: "success"\ncreated_at: "2025-01-01"\nupdated_at: "2025-01-01"\n'
        f"---\n# {path.stem}\n\n{body}\n\n"
        "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)\n> - **Temps estimé sur ce sujet :** 20 min\n",
        encoding="utf-8",
    )


def test_v013_chantiers4_5_truncated_notes_and_anti_overwrite(exo_env):
    cdir = exo_env.concepts_dir
    langues = cdir / "neuroplasticite-acquisition-langues-complexes-adulte.md"
    cpu = cdir / "optimisation-cpu-affinite-p-e-cores-smt.md"
    valide = cdir / "pipeline-rag-valide.md"
    _takeout_note(langues, "sid_langues", "### Contexte\nExploiter la capacité de déconstruction pour assimiler la structure")
    _takeout_note(cpu, "sid_cpu", "### Contexte\nVérifier l'affinité des cœurs pour s'assurer que le")
    _takeout_note(valide, "sid_valide", "### Conclusions\nArchitecture validée et documentée.")

    completed = scan_and_upgrade_existing_concepts(exo_env.db)

    assert not langues.exists() and not cpu.exists()
    assert (settings.CONCEPTS_QUARANTINE_DIR / langues.name).exists()
    assert (settings.CONCEPTS_QUARANTINE_DIR / cpu.name).exists()
    assert valide.exists() and "sid_valide" in completed

    now_dt = datetime.now()
    dummy = ReconstructedSession(
        session_id="sid_valide",
        turns=[ParsedTurn(session_id="sid_valide", timestamp=now_dt, user_prompt="Question", ai_response="R", user_char_count=50)],
        timestamp_start=now_dt, timestamp_end=now_dt, turn_count=1, user_char_count=50, summary="Test",
    )
    _, status = save_distilled_concept_note(dummy, None, exo_env.db, allow_quarantine=True)
    assert status == "skipped"
    after = valide.read_text(encoding="utf-8")
    assert "# A_Trier" not in after and 'distillation_status: "success"' in after
