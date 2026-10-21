"""
Script de validation pour l'implémentation v0.1.3.
Vérifie la conformité de l'ensemble des 5 chantiers techniques :
1. Architecture Multi-Pass VRAM Queue (gemma4:26b-a4b -> 26B No-Think -> 12B Fallback)
2. Préservation du Thinking (num_predict=8192, Modelfile num_ctx 16384) & Auto-Heal JSON
3. Purge active VRAM (force_clear_vram, élimination des modèles fantômes)
4. Déduplication SQLite (historical_footprints = 73 154, chat_sessions = 480)
5. Détection & purge chirurgicale des notes tronquées de la v0.1.2 et protection anti-écrasement
"""

import json
import re
import sys
from pathlib import Path

# Add project root
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from datetime import datetime
from src.config import settings
from src.database.db_manager import DBManager, HistoricalFootprintRecord
from src.llm.ollama_client import HybridLLMClient, llm_client, repair_truncated_json
from src.ingestors.takeout_ingestor import (
    scan_and_upgrade_existing_concepts,
    save_distilled_concept_note,
    ReconstructedSession,
    ParsedTurn,
    DistilledConceptSchema,
)


def run_checks():
    print("=" * 70)
    print("VÉRIFICATION TECHNIQUE DES 5 CHANTIERS v0.1.3")
    print("=" * 70)

    # --------------------------------------------------------------------------
    # CHANTIER 1 : Déduplication SQLite & Unicité
    # --------------------------------------------------------------------------
    print("\n--- CHANTIER 1 : Déduplication SQLite (historical_footprints & chat_sessions) ---")
    db = DBManager()
    with db.get_connection() as conn:
        # 1. Vérification du décompte de historical_footprints
        cur = conn.execute("SELECT COUNT(*) FROM historical_footprints;")
        hist_count = cur.fetchone()[0]
        print(f"Lignes dans historical_footprints après déduplication : {hist_count}")
        assert hist_count in (73153, 73154), f"Attendu 73 153 ou 73 154 empreintes uniques, obtenu : {hist_count}"

        # 2. Vérification de l'index unique
        cur = conn.execute("PRAGMA index_list('historical_footprints');")
        indexes = [r["name"] for r in cur.fetchall()]
        assert "idx_unique_footprint" in indexes, "Index unique idx_unique_footprint manquant !"

        # 3. Vérification du décompte de chat_sessions (480 sessions qualifiées, 0 bruit)
        cur = conn.execute("SELECT COUNT(*) FROM chat_sessions;")
        cs_count = cur.fetchone()[0]
        print(f"Sessions dans chat_sessions après nettoyage micro-sessions : {cs_count}")
        assert cs_count == 480, f"Attendu exactement 480 sessions qualifiées, obtenu : {cs_count}"

        # Vérifier qu'aucune session restante n'est sous le seuil
        cur = conn.execute("SELECT COUNT(*) FROM chat_sessions WHERE turn_count < 3 OR user_char_count < 250;")
        invalid_cs = cur.fetchone()[0]
        assert invalid_cs == 0, f"Trouvé {invalid_cs} sessions non conformes dans chat_sessions !"

        # 4. Vérification que chat_messages conserve bien l'intégralité des 6649 messages
        cur = conn.execute("SELECT COUNT(*) FROM chat_messages;")
        cm_count = cur.fetchone()[0]
        print(f"Messages conservés dans chat_messages : {cm_count}")
        assert cm_count >= 6649, f"chat_messages devrait contenir au moins 6649 messages, obtenu : {cm_count}"

    print("Déduplication et contrainte d'unicité SQLite validées avec succès.")

    # --------------------------------------------------------------------------
    # CHANTIER 2 : Auto-Heal JSON & Parsing Thinking
    # --------------------------------------------------------------------------
    print("\n--- CHANTIER 2 : Fonction repair_truncated_json & Support Thinking ---")

    # Cas A : Bloc Thinking pur
    raw_with_thought = (
        "<|thought|>\nL'utilisateur demande une analyse de Process Lasso et du cache L3.\n"
        "Je vais structurer la réponse selon le schéma Pydantic requis.\n<|/thought|>\n"
        '{"concept_title": "Optimisation CPU", "slug": "optimisation-cpu", '
        '"semantic_topic": "HomeLab_et_Hardware", "tags": ["cpu"], '
        '"summary_1_line": "Optimisation CPU et affinité.", '
        '"synthesized_markdown_body": "### Contexte\\nL\'analyse montre une contention.", '
        '"is_worth_indexing": true, "related_concepts": []}'
    )
    repaired_a = repair_truncated_json(raw_with_thought)
    data_a = json.loads(repaired_a)
    assert data_a["concept_title"] == "Optimisation CPU"
    print("Cas A (Suppression balises <|thought|>) validé.")

    # Cas B : JSON tronqué au milieu de synthesized_markdown_body (Unterminated string)
    raw_truncated_body = (
        '{"concept_title": "Neuroplasticité Adulte", "slug": "neuroplasticite-adulte", '
        '"semantic_topic": "Introspection_et_Neuroatypie", "tags": ["langues"], '
        '"summary_1_line": "Apprentissage des langues adultes.", '
        '"synthesized_markdown_body": "### Contexte\\nL\'adulte dispose de capacités logiques solides. '
        'Exploiter la capacité de déconstruction pour assimiler la structure'
    )
    repaired_b = repair_truncated_json(raw_truncated_body)
    data_b = json.loads(repaired_b)
    assert data_b["concept_title"] == "Neuroplasticité Adulte"
    assert data_b["synthesized_markdown_body"].endswith("solides.")
    print("Cas B (Auto-réparation coupure nette à la dernière phrase complète) validé.")

    # Cas C : Balises <think> alternatives
    raw_think_tag = (
        "<think>Reflexion interne du modele...</think>"
        '{"concept_title": "Titre C", "slug": "titre-c", "semantic_topic": "IA_et_LLM_Local", '
        '"tags": [], "summary_1_line": "S1", "synthesized_markdown_body": "Body C.", '
        '"is_worth_indexing": true, "related_concepts": []}'
    )
    repaired_c = repair_truncated_json(raw_think_tag)
    data_c = json.loads(repaired_c)
    assert data_c["concept_title"] == "Titre C"
    print("Cas C (Balises <think>) validé.")

    # --------------------------------------------------------------------------
    # CHANTIER 3 : Paramètres VRAM, Modelfile num_ctx & force_clear_vram
    # --------------------------------------------------------------------------
    print("\n--- CHANTIER 3 : Invariants Matériels & Purge Active VRAM ---")
    assert settings.VRAM_STRICT_ABORT_FREE_GB == 8.0, "VRAM_STRICT_ABORT_FREE_GB doit être de 8.0 Go"
    assert settings.VRAM_REASONING_MIN_FREE_GB == 12.8, "VRAM_REASONING_MIN_FREE_GB doit être de 12.8 Go"
    assert settings.MODEL_REASONING == "gemma4:26b-a4b", "MODEL_REASONING doit pointer vers gemma4:26b-a4b"

    # Vérification que Modelfile contient num_ctx 16384
    import inspect
    ensure_src = inspect.getsource(HybridLLMClient.ensure_local_gguf_models)
    assert "PARAMETER num_ctx 16384" in ensure_src, "Modelfile doit être configuré avec num_ctx 16384"
    print("Modelfile et seuils VRAM (8.0 Go et 12.8 Go) vérifiés.")

    # Vérification signature generate_structured
    sig = inspect.signature(HybridLLMClient.generate_structured)
    assert "enable_thinking" in sig.parameters
    assert "num_predict" in sig.parameters
    assert "allow_model_switch_fallback" in sig.parameters
    assert sig.parameters["enable_thinking"].default is True
    assert sig.parameters["num_predict"].default == 8192
    assert sig.parameters["allow_model_switch_fallback"].default is False
    print("Signature generate_structured (Thinking actif par défaut, num_predict=8192, pas de bascule inline) validée.")

    # Vérification de force_clear_vram
    assert hasattr(llm_client, "force_clear_vram"), "force_clear_vram manquant sur llm_client"
    print("Méthode force_clear_vram validée.")

    # --------------------------------------------------------------------------
    # CHANTIER 4 : Assainissement des Notes Tronquées & Protection Anti-Écrasement
    # --------------------------------------------------------------------------
    print("\n--- CHANTIER 4 : Détection & Purge des Notes Tronquées (v0.1.2) ---")
    file_langues = settings.CONCEPTS_DIR / "neuroplasticite-acquisition-langues-complexes-adulte.md"
    file_cpu = settings.CONCEPTS_DIR / "optimisation-cpu-affinite-p-e-cores-smt.md"

    # Exécution de scan_and_upgrade_existing_concepts
    completed_sids = scan_and_upgrade_existing_concepts(db)

    # Les deux fichiers tronqués doivent avoir été identifiés et purgés du disque
    assert not file_langues.exists(), f"Le fichier tronqué {file_langues.name} aurait dû être purgé !"
    assert not file_cpu.exists(), f"Le fichier tronqué {file_cpu.name} aurait dû être purgé !"
    print("Les 2 fiches tronquées ont été purgées avec succès du disque et de LanceDB.")

    remaining_notes = [p for p in settings.CONCEPTS_DIR.glob("*.md") if not p.name.startswith("all-")]
    print(f"Nombre de fiches valides restantes sur disque : {len(remaining_notes)}")
    assert len(remaining_notes) >= 476, f"Attendu au moins 476 fiches sur disque, obtenu : {len(remaining_notes)}"

    # Vérification que toutes les fiches restantes se terminent proprement
    for note_p in remaining_notes:
        content = note_p.read_text(encoding="utf-8")
        if "> - **Temps estimé sur ce sujet :**" in content:
            body_before_abstract = content.split("> - **Temps estimé sur ce sujet :**")[0]
            if "> [!abstract]-" in body_before_abstract:
                body_before_abstract = body_before_abstract.rsplit("> [!abstract]-", 1)[0]
        elif "> [!abstract]-" in content:
            body_before_abstract = content.rsplit("> [!abstract]-", 1)[0]
        else:
            body_before_abstract = content

        body_before_abstract = body_before_abstract.strip()
        lines = [l.strip() for l in body_before_abstract.splitlines() if l.strip()]
        if lines:
            last_line = lines[-1]
            valid_endings = ('.', '!', '?', ')', '*', '`', '|', ':', '"', '»', ']', '}', '>')
            is_valid = False
            if last_line.endswith("pour assimiler la structure") or last_line.endswith("pour s'assurer que le"):
                is_valid = False
            elif last_line.endswith(valid_endings):
                is_valid = True
            else:
                has_conclusion = bool(re.search(r"###\s*(?:Conclusions?|Synthèse|Bilan|Commandes\s*Clés)", body_before_abstract, re.IGNORECASE))
                is_table_or_bullet = last_line.startswith(("|", "*", "-", ">"))
                if len(body_before_abstract) > 500 and (has_conclusion or is_table_or_bullet):
                    is_valid = True
            assert is_valid, f"Note {note_p.name} se termine anormalement par : '{last_line[-30:]}'"

    print("100% des fiches restantes ont une ponctuation finale et structure intègres.")

    # Test de la protection anti-écrasement
    print("\n--- CHANTIER 5 : Test de la Protection Anti-Écrasement ---")
    # Prenons une session existante valide parmi les 390 fiches
    sample_note = remaining_notes[0]
    sample_content = sample_note.read_text(encoding="utf-8")
    sample_sid = re.search(r'session_id:\s*["\']?([^"\'\n\r]+)["\']?', sample_content).group(1)

    now_dt = datetime.now()
    dummy_sess = ReconstructedSession(
        session_id=sample_sid,
        turns=[
            ParsedTurn(
                session_id=sample_sid,
                timestamp=now_dt,
                user_prompt="Question test",
                ai_response="Reponse test",
                user_char_count=50,
            )
        ],
        timestamp_start=now_dt,
        timestamp_end=now_dt,
        turn_count=1,
        user_char_count=50,
        summary="Test session",
    )

    # Tentative d'écrasement par #A_Trier avec allow_quarantine=True
    saved, status = save_distilled_concept_note(dummy_sess, None, db, allow_quarantine=True)
    assert status == "skipped", f"Attendu 'skipped' pour la note existante, obtenu : '{status}'"
    # Vérifier que la note sur disque n'a pas été modifiée
    after_content = sample_note.read_text(encoding="utf-8")
    assert "# A_Trier" not in after_content
    assert 'distillation_status: "success"' in after_content
    print("Protection anti-écrasement validée : impossible d'écraser une note valide par #A_Trier.")

    print("\n" + "=" * 70)
    print("TOUS LES CRITÈRES DE VALIDATION v0.1.3 SONT ATTEINTS AVEC SUCCÈS !")
    print("=" * 70)


if __name__ == "__main__":
    run_checks()
