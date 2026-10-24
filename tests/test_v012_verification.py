"""
Suite de validation v0.1.2, rendue hermétique en v0.5.6 (audit F1).
Vérifie les mêmes chantiers qu'à l'origine, mais sur un export Takeout synthétique et des fiches
créées par le test, avec des invariants relatifs au lieu des volumes personnels de l'utilisateur :
1. Taxonomie fermée à 16 macro-catégories
2. Client LLM et génération structurée
3. Persistance SQLite (chat_messages, distillation_status)
4. Assainissement in-place des fiches Takeout
5. Registre du bruit 00_MISC_ET_BRUIT_ARCHIVE.md
6. Cold Start Épisodique rétroactif 01_Episodique/*.md et daily_metrics
7. LanceDB delete_by_slug
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.config import AUTHORIZED_SEMANTIC_TOPICS, normalize_to_macro_topic, settings
from src.database.vector_store import VectorStore
from src.ingestors.takeout_ingestor import (
    TakeoutIngestor,
    compile_misc_noise_archive,
    generate_cold_start_episodic_journals,
    parse_gemini_html,
    scan_and_upgrade_existing_concepts,
    sessionize_gemini_turns,
)


def write_gemini_html_export(path: Path, days: int = 3, turns_per_day: int = 4, noise_days: int = 1) -> int:
    """Écrit un export HTML Gemini minimal au format MyActivity ; retourne le nombre de tours."""
    blocks = []
    count = 0
    for d in range(days + noise_days):
        n_turns = turns_per_day if d < days else 1  # dernier(s) jour(s) : micro-session bruitée
        for t in range(n_turns):
            ts = datetime(2026, 3, 2 + d, 10, 0) + timedelta(minutes=5 * t)
            date_txt = ts.strftime("%d %b %Y, %H:%M:%S CET").replace("Mar", "mars")
            prompt = f"Question détaillée {d}-{t} sur l'architecture du pipeline vectoriel local " * 2
            blocks.append(
                '<div class="outer-cell mdl-cell"><div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">'
                f"Prompt : {prompt}<br>{date_txt}<br><p>Réponse argumentée {d}-{t}.</p></div>"
                f'<a href="https://gemini.google.com/app/sess{d:02d}">lien</a></div>'
            )
            count += 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("<html><body>" + "".join(blocks) + "</body></html>", encoding="utf-8")
    return count


def test_v012_chantier1_taxonomy():
    assert len(AUTHORIZED_SEMANTIC_TOPICS) == 16
    assert "IA_et_LLM_Local" in AUTHORIZED_SEMANTIC_TOPICS and "A_Trier" in AUTHORIZED_SEMANTIC_TOPICS
    assert normalize_to_macro_topic("IA_Agentique_et_RAG") == "IA_et_LLM_Local"
    assert normalize_to_macro_topic("Philo_Droit_et_Morale") == "Philo_et_Epistemologie"
    assert normalize_to_macro_topic("Nutrition_Volume_Eating") == "Nutrition_et_Cuisine"


def test_v012_chantier2_llm_client():
    from src.llm.ollama_client import HybridLLMClient, llm_client

    assert isinstance(llm_client, HybridLLMClient)
    assert callable(llm_client.generate_structured)


def test_v012_chantier3_sqlite_schema(exo_env):
    with exo_env.db.get_connection() as conn:
        cs_cols = [r["name"] for r in conn.execute("PRAGMA table_info(chat_sessions);").fetchall()]
        cm_cols = [r["name"] for r in conn.execute("PRAGMA table_info(chat_messages);").fetchall()]
    assert "distillation_status" in cs_cols
    assert {"session_id", "turn_index", "user_prompt", "ai_response", "user_char_count"} <= set(cm_cols)


def test_v012_chantier4_in_place_sanitization(exo_env):
    cdir = exo_env.concepts_dir
    for i in range(5):
        (cdir / f"fiche-legacy-{i}.md").write_text(
            "---\n"
            f'id: "legacy{i}"\ntitle: "Fiche {i}"\norigin: ["gemini_takeout"]\n'
            'semantic_topic: "IA_Agentique_et_RAG"\ncreated_at: "2025-01-01"\nupdated_at: "2025-01-01"\n'
            "---\n"
            f"# Fiche {i}\n\n### Contexte\nArbitrage complet et conclu.\n\n"
            "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)\n"
            "> - **Temps estimé sur ce sujet :** 20 min\n"
            f"> - **Sources épisodiques :**\n>   - Session Gemini `sid_{i}` du 2025-01-01\n"
            "> - **Requêtes et vidéos corrélées :** [youtube] vidéo, [google_search] requête\n"
            "> - **Connexions sémantiques suggérées :** —\n",
            encoding="utf-8",
        )

    completed = scan_and_upgrade_existing_concepts(exo_env.db)

    notes = list(cdir.glob("*.md"))
    assert len(notes) == 5
    for fpath in notes:
        content = fpath.read_text(encoding="utf-8")
        assert "Requêtes et vidéos corrélées" not in content and "[youtube]" not in content
        topic = re.search(r'semantic_topic:\s*"?([^"\n]+)"?', content).group(1)
        assert topic in AUTHORIZED_SEMANTIC_TOPICS
        assert "session_id:" in content
    assert {f"sid_{i}" for i in range(5)} <= completed


def test_v012_chantiers5_6_parsing_noise_registry_and_cold_start(exo_env):
    export = settings.TAKEOUT_DIR / "Gemini" / "MonActivite_gemini.html"
    n_turns = write_gemini_html_export(export, days=3, turns_per_day=4, noise_days=1)

    files = TakeoutIngestor(db_manager=exo_env.db).discover_files()
    assert files["gemini"] == [export]

    turns = parse_gemini_html(export)
    assert len(turns) == n_turns
    qualified, noise = sessionize_gemini_turns(turns)
    assert len(qualified) == 3 and len(noise) == 1

    messages = [
        (s.session_id, i, t.timestamp, t.user_prompt, t.ai_response, t.user_char_count)
        for s in qualified + noise for i, t in enumerate(s.turns, 1)
    ]
    assert exo_env.db.insert_chat_messages_batch(messages) == n_turns

    misc_path = compile_misc_noise_archive(noise, [])
    assert "# Registre Consolidé du Bruit & Micro-Sessions" in misc_path.read_text(encoding="utf-8")

    generated = generate_cold_start_episodic_journals(qualified, exo_env.db)
    assert generated == len({s.timestamp_start.date() for s in qualified}) == 3
    with exo_env.db.get_connection() as conn:
        assert conn.execute("SELECT COUNT(*) FROM daily_metrics;").fetchone()[0] == 3


def test_v012_chantier7_lancedb_delete_by_slug(tmp_path):
    vs = VectorStore(store_dir=tmp_path / "lancedb")
    assert vs.delete_by_slug("non-existent-test-slug") is True
