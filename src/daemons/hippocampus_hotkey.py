"""
Module 5 : Injecteur Pré-Prompt Hippocampe Local (Pont A - Alt + Espace).
Démon ultra-léger (0 Mo VRAM, 0% CPU au repos) écoutant le raccourci global Alt+Espace :
1. Capture le texte saisi dans l'invite de commande ou la zone active (Ctrl+A -> Ctrl+C).
2. Interroge vector_store.py (k-NN top_k=5) via LanceDB et décharge immédiatement bge-m3.
3. Récupère la télémétrie SQLite cumulée sur les semantic_topics identifiés.
4. Concatène le prompt utilisateur et le bloc structuré <contexte_hippocampe_local>.
5. Réinjecte le tout via Ctrl+V et notifie l'utilisateur via signal sonore discret.
"""

from __future__ import annotations

import argparse
import ctypes
import logging
import os
import re
import sys
import time
import winsound
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import pyperclip
from pynput import keyboard

from src.config import settings
from src.database.db_manager import DBManager
from src.database.vector_store import vector_store
from src.llm.ollama_client import llm_client

logger = logging.getLogger("Exocortex.HippocampusHotkey")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

# Constantes Win32 Virtual Keys
VK_CONTROL = 0x11
VK_MENU = 0x12       # ALT
VK_A = 0x41
VK_C = 0x43
VK_V = 0x56
KEYEVENTF_KEYUP = 0x0002

user32 = ctypes.windll.user32


def win32_key_down(vk: int) -> None:
    """Simule l'enfoncement d'une touche bas niveau."""
    user32.keybd_event(vk, 0, 0, 0)


def win32_key_up(vk: int) -> None:
    """Simule le relâchement d'une touche bas niveau."""
    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)


def simulate_select_and_copy() -> str:
    """
    Sécurise le relâchement de la touche Alt, puis simule Ctrl+A puis Ctrl+C
    pour capturer le prompt en cours de frappe dans la zone active.
    """
    # 1. Relâchement forcé de la touche Alt
    win32_key_up(VK_MENU)
    time.sleep(0.04)

    # 2. Ctrl + A (Sélectionner tout)
    win32_key_down(VK_CONTROL)
    win32_key_down(VK_A)
    time.sleep(0.02)
    win32_key_up(VK_A)
    win32_key_up(VK_CONTROL)
    time.sleep(0.04)

    # 3. Ctrl + C (Copier)
    win32_key_down(VK_CONTROL)
    win32_key_down(VK_C)
    time.sleep(0.02)
    win32_key_up(VK_C)
    win32_key_up(VK_CONTROL)
    time.sleep(0.05)

    try:
        captured = pyperclip.paste()
        return captured.strip() if captured else ""
    except Exception as exc:
        logger.error("Erreur lors de la lecture du presse-papier : %s", exc)
        return ""


def simulate_paste_payload(payload: str) -> None:
    """Place le payload enrichi dans le presse-papier et simule Ctrl+V."""
    try:
        pyperclip.copy(payload)
        time.sleep(0.04)

        # Ctrl + V (Coller)
        win32_key_down(VK_CONTROL)
        win32_key_down(VK_V)
        time.sleep(0.02)
        win32_key_up(VK_V)
        win32_key_up(VK_CONTROL)
    except Exception as exc:
        logger.error("Erreur lors de l'injection du presse-papier : %s", exc)


def clean_markdown_excerpt(content: str, max_chars: int = 700) -> str:
    """
    Supprime le frontmatter YAML et les blocs callouts bruités
    pour n'extraire que l'essence intellectuelle de la note.
    """
    # Retrait frontmatter YAML
    cleaned = re.sub(r"^---[\s\S]*?---\s*", "", content).strip()
    # Retrait des callouts Obsidian dépliables pour ne pas dupliquer la télémétrie
    cleaned = re.sub(r"> \[!abstract\]-[\s\S]*?(?=\n\n|\Z)", "", cleaned).strip()

    if len(cleaned) > max_chars:
        # Tronquage propre au dernier saut de ligne ou phrase
        truncated = cleaned[:max_chars]
        last_break = max(truncated.rfind("\n"), truncated.rfind(". "))
        if last_break > 300:
            truncated = truncated[:last_break]
        return truncated + "\n[...]"
    return cleaned


class HippocampusInjector:
    """Gestionnaire de l'injection sémantique et télémétrique de l'exocortex."""

    def __init__(self, db_manager: Optional[DBManager] = None) -> None:
        self.db = db_manager or DBManager()
        self.is_processing = False

    def build_enriched_payload(self, user_prompt: str, top_k: int = 5) -> str:
        """
        Construit le payload hybride : Prompt utilisateur + bloc <contexte_hippocampe_local>.
        """
        if not user_prompt or len(user_prompt.strip()) < 3:
            return user_prompt

        logger.info("Requête Hippocampe sur : '%s...'", user_prompt[:60].replace("\n", " "))

        # 1. Recherche vectorielle LanceDB k-NN
        vector_results = vector_store.search(user_prompt, top_k=top_k)

        if not vector_results:
            logger.info("Aucune note conceptuelle trouvée dans LanceDB pour cette requête.")
            return user_prompt

        # 2. Identification des topics uniques et interrogation SQLite
        found_topics: Set[str] = set()
        for r in vector_results:
            topic = r.get("semantic_topic")
            if topic and topic.strip() and topic != "Non_Classe":
                found_topics.add(topic.strip())

        topics_list = sorted(list(found_topics))
        telemetry_summaries: List[str] = []

        for topic in topics_list:
            stats = self.db.get_topic_telemetry_stats(topic)
            tot_h = stats.get("total_os_hours", 0.0)
            sessions_count = stats.get("chat_sessions_count", 0)
            fp_count = stats.get("footprints_count", 0)
            last_act = stats.get("last_active", "Inconnue")
            top_app = stats.get("dominant_app", "N/A")

            summary_item = (
                f"- **#{topic}** : {tot_h}h OS ({top_app}) | "
                f"{sessions_count} sessions Gemini | {fp_count} recherches/vidéos | Dernier focus : {last_act}"
            )
            telemetry_summaries.append(summary_item)

        # 3. Formatage des extraits de notes (déduplication par slug/titre)
        formatted_notes: List[str] = []
        seen_notes: Set[str] = set()
        note_idx = 1
        for r in vector_results:
            title = r.get("title") or r.get("slug") or f"Note_{note_idx}"
            slug = r.get("slug") or title
            if slug in seen_notes:
                continue
            seen_notes.add(slug)

            topic = r.get("semantic_topic") or "Non_Classe"
            dist = r.get("score", 1.0)
            # Distance cosinus approximée en score de proximité
            similarity_pct = max(0, min(100, int((1.0 - (dist / 2.0)) * 100))) if dist <= 2.0 else 50
            raw_content = r.get("content", "")
            excerpt = clean_markdown_excerpt(raw_content)

            note_block = (
                f"#### [{note_idx}] [[{title}]] (Topic: #{topic} | Match: ~{similarity_pct}%)\n"
                f"{excerpt}"
            )
            formatted_notes.append(note_block)
            note_idx += 1
            if len(formatted_notes) >= 5:
                break

        # 4. Assemblage du bloc XML / Markdown
        telemetry_block = "\n".join(telemetry_summaries) if telemetry_summaries else "- Aucune télémétrie spécifique enregistrée."
        notes_block = "\n\n---\n\n".join(formatted_notes)

        enriched_context = (
            f"\n\n<contexte_hippocampe_local>\n"
            f"> [!abstract]- Télémétrie & Mémoire Long-Terme Exocortex\n"
            f"> **Topics Détectés :** {', '.join([f'#{t}' for t in topics_list]) if topics_list else '#Général'}\n"
            f">\n"
            f"> **Historique & Investissement Temporel :**\n"
            f"{telemetry_block}\n\n"
            f"### Extraits Conceptuels Locaux Pertinents (k-NN LanceDB) :\n"
            f"{notes_block}\n"
            f"</contexte_hippocampe_local>"
        )

        final_payload = user_prompt + enriched_context
        return final_payload

    def on_hotkey_triggered(self) -> None:
        """Point d'entrée lors de la frappe du raccourci global Alt+Espace."""
        if self.is_processing:
            logger.info("Requête précédente en cours, activation ignorée.")
            return

        self.is_processing = True
        try:
            logger.info("=== Raccourci Alt+Espace détecté ===")
            prompt = simulate_select_and_copy()

            if not prompt or len(prompt) < 3:
                logger.warning("Texte capturé vide ou trop court (%d car.), annulation.", len(prompt))
                winsound.MessageBeep(winsound.MB_ICONHAND)
                return

            enriched_payload = self.build_enriched_payload(prompt, top_k=5)

            if enriched_payload != prompt:
                simulate_paste_payload(enriched_payload)
                logger.info("Injection réussie du contexte local dans la zone active !")
                # Bip sonore discret de confirmation
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            else:
                logger.info("Aucun enrichissement appliqué.")
                winsound.MessageBeep(winsound.MB_OK)

        except Exception as exc:
            logger.error("Erreur critique lors de l'injection Alt+Espace : %s", exc, exc_info=True)
            winsound.MessageBeep(winsound.MB_ICONHAND)
        finally:
            self.is_processing = False

    def run_daemon(self) -> None:
        """Démarre le listener d'écoute globale en arrière-plan."""
        logger.info("Démarrage de l'injecteur Hippocampe (Écoute globale Alt+Espace)...")
        logger.info("Empreinte VRAM : 0 Mo | CPU au repos : 0 %%")

        hotkey_str = "<alt>+<space>"
        with keyboard.GlobalHotKeys({hotkey_str: self.on_hotkey_triggered}) as h:
            try:
                h.join()
            except KeyboardInterrupt:
                logger.info("Arrêt gracieux de l'injecteur Hippocampe.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Injecteur Pré-Prompt Hippocampe Local (Alt+Espace)")
    parser.add_argument(
        "--test",
        type=str,
        default=None,
        help="Teste l'injection en mode headless sur une chaîne sans déclenchement physique du clavier."
    )
    args = parser.parse_args()

    injector = HippocampusInjector()

    if args.test:
        print(f"\n[TEST MODE] Requête : '{args.test}'")
        result = injector.build_enriched_payload(args.test, top_k=5)
        print("\n--- RÉSULTAT DU PAYLOAD ENRICHI ---")
        print(result)
        print("--- FIN DU PAYLOAD ---\n")
    else:
        injector.run_daemon()
