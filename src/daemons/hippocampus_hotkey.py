"""
Module 5 : Injecteur Pré-Prompt Hippocampe Local (Pont A).
Démon ultra-léger (0 Mo VRAM, 0% CPU au repos) écoutant le raccourci global HIPPOCAMPUS_HOTKEY
(Ctrl+Alt+Espace par défaut depuis v0.5.6 ; Alt+Espace entrait en conflit avec le menu système) :
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
import threading
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
from src.database.graph_rag import HybridGraphRAG
from src.database.vector_store import vector_store
from src.llm.ollama_client import VRAMBusyError, llm_client
from src.utils.lifecycle import clear_stop_flag, stop_requested

logger = logging.getLogger("Exocortex.HippocampusHotkey")

# Attente maximale du GPU pour une injection interactive (v0.5.7, C8)
INTERACTIVE_VRAM_TIMEOUT_SEC = 3.0
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


_last_previous_clipboard: str = ""


def simulate_select_and_copy() -> str:
    """
    Sécurise le relâchement de la touche Alt, sauvegarde le presse-papier initial,
    place une sentinelle vide, simule Ctrl+A puis Ctrl+C, et attend via polling (jusqu'à 350 ms).
    Si aucun texte n'est capturé, restaure le presse-papier initial et annule.
    """
    global _last_previous_clipboard
    try:
        previous_clipboard = pyperclip.paste()
    except Exception:
        previous_clipboard = ""
    _last_previous_clipboard = previous_clipboard

    try:
        pyperclip.copy("")
    except Exception:
        pass

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

    # 4. Polling rapide (max 350 ms par pas de 15 ms)
    captured = ""
    start_time = time.time()
    while (time.time() - start_time) < 0.350:
        time.sleep(0.015)
        try:
            val = pyperclip.paste()
            if val:
                captured = val.strip()
                break
        except Exception:
            pass

    if not captured:
        # Échec de capture : restauration du presse-papier initial
        if previous_clipboard:
            try:
                pyperclip.copy(previous_clipboard)
            except Exception:
                pass
        return ""

    return captured


def simulate_paste_payload(payload: str, restore_clipboard: Optional[str] = None) -> None:
    """Place le payload enrichi dans le presse-papier, simule Ctrl+V et restaure l'ancien presse-papier."""
    global _last_previous_clipboard
    try:
        pyperclip.copy(payload)
        time.sleep(0.04)

        # Ctrl + V (Coller)
        win32_key_down(VK_CONTROL)
        win32_key_down(VK_V)
        time.sleep(0.02)
        win32_key_up(VK_V)
        win32_key_up(VK_CONTROL)

        # Délai pour laisser l'application cible consommer le Ctrl+V avant de restaurer
        time.sleep(0.120)

        clip_to_restore = restore_clipboard if restore_clipboard is not None else _last_previous_clipboard
        if clip_to_restore:
            pyperclip.copy(clip_to_restore)
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

    def __init__(
        self,
        db_manager: Optional[DBManager] = None,
        graph_rag: Optional[HybridGraphRAG] = None,
    ) -> None:
        self.db = db_manager or DBManager()
        self.graph_rag = graph_rag or HybridGraphRAG(db_manager=self.db)
        # Verrou non bloquant : une seule injection à la fois, sans jamais attendre dans le hook
        self._busy = threading.Lock()

    @property
    def is_processing(self) -> bool:
        return self._busy.locked()

    def build_enriched_payload(self, user_prompt: str, top_k: int = 5) -> str:
        """
        Construit le payload hybride : Prompt utilisateur + bloc <contexte_hippocampe_local>
        enrichi par GraphRAG (Hop 0 k-NN + Hop 1 Wikilinks de graphe).
        """
        if not user_prompt or len(user_prompt.strip()) < 3:
            return user_prompt

        logger.info("Requête Hippocampe sur : '%s...'", user_prompt[:60].replace("\n", " "))

        # 1. Recherche hybride GraphRAG (Hop 0 Vectoriel + Hop 1 Wikilinks)
        rag_result = self.graph_rag.search_hybrid(user_prompt, top_k=top_k, neighbor_k=3)
        primary_nodes = rag_result.get("primary_nodes", [])
        linked_neighbors = rag_result.get("linked_neighbors", [])

        if not primary_nodes and not linked_neighbors:
            logger.info("Aucune note conceptuelle trouvée pour cette requête.")
            return user_prompt

        # 2. Identification des topics uniques et interrogation SQLite
        found_topics: Set[str] = set()
        for r in (primary_nodes + linked_neighbors):
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

        # 3. Formatage des extraits de notes primaires (Hop 0)
        formatted_notes: List[str] = []
        seen_notes: Set[str] = set()
        note_idx = 1
        for r in primary_nodes:
            title = r.get("title") or r.get("slug") or f"Note_{note_idx}"
            slug = r.get("slug") or title
            if slug in seen_notes:
                continue
            seen_notes.add(slug)

            topic = r.get("semantic_topic") or "Non_Classe"
            sim_pct = r.get("similarity_pct", 50)
            raw_content = r.get("excerpt", "")
            excerpt = clean_markdown_excerpt(raw_content)

            note_block = (
                f"#### [{note_idx}] [[{title}]] (Topic: #{topic} | Match: ~{sim_pct}%)\n"
                f"{excerpt}"
            )
            formatted_notes.append(note_block)
            note_idx += 1
            if len(formatted_notes) >= 5:
                break

        # 4. Formatage des voisins liés par wikilinks (Hop 1)
        formatted_neighbors: List[str] = []
        for nb in linked_neighbors:
            nb_title = nb.get("title") or nb.get("slug")
            nb_topic = nb.get("semantic_topic") or "General"
            nb_excerpt = clean_markdown_excerpt(nb.get("excerpt", ""))
            formatted_neighbors.append(
                f"- **[[{nb_title}]]** (Topic: #{nb_topic}) : {nb_excerpt[:200]}"
            )

        # 5. Assemblage du bloc XML / Markdown
        telemetry_block = "\n".join(telemetry_summaries) if telemetry_summaries else "- Aucune télémétrie spécifique enregistrée."
        notes_block = "\n\n---\n\n".join(formatted_notes) if formatted_notes else "- Aucun extrait direct."

        graph_section = ""
        if formatted_neighbors:
            graph_section = f"\n\n### Connexions de Graphe (1-Hop Wikilinks) :\n" + "\n".join(formatted_neighbors)

        enriched_context = (
            f"\n\n<contexte_hippocampe_local>\n"
            f"> [!abstract]- Télémétrie & Mémoire Long-Terme Exocortex\n"
            f"> **Topics Détectés :** {', '.join([f'#{t}' for t in topics_list]) if topics_list else '#Général'}\n"
            f">\n"
            f"> **Historique & Investissement Temporel :**\n"
            f"{telemetry_block}\n\n"
            f"### Extraits Conceptuels Locaux Pertinents (k-NN LanceDB) :\n"
            f"{notes_block}"
            f"{graph_section}\n"
            f"</contexte_hippocampe_local>"
        )

        final_payload = user_prompt + enriched_context
        return final_payload

    def on_hotkey_triggered(self) -> Optional[threading.Thread]:
        """
        Callback du raccourci global (v0.5.6, E2). Il s'exécute sur le thread du hook clavier
        bas niveau de Windows : un hook trop lent est retiré silencieusement par le système
        (LowLevelHooksTimeout). Le callback ne fait donc que déléguer le travail (copie, GraphRAG,
        embedding, collage) à un thread dédié, et rend la main immédiatement.
        """
        if not self._busy.acquire(blocking=False):
            logger.info("Requête précédente en cours, activation ignorée.")
            return None
        worker = threading.Thread(target=self._process_hotkey, name="Hippocampus-Inject", daemon=True)
        worker.start()
        return worker

    def _process_hotkey(self) -> None:
        """Copie, enrichissement et réinjection, hors du thread du hook clavier."""
        try:
            logger.info("=== Raccourci %s détecté ===", settings.HIPPOCAMPUS_HOTKEY)
            prompt = simulate_select_and_copy()

            if not prompt or len(prompt) < 3:
                logger.warning("Texte capturé vide ou trop court (%d car.), annulation.", len(prompt))
                winsound.MessageBeep(winsound.MB_ICONHAND)
                return

            try:
                # Le GPU peut être tenu par la consolidation nocturne : attente bornée (C8)
                with llm_client.vram_session(timeout=INTERACTIVE_VRAM_TIMEOUT_SEC):
                    enriched_payload = self.build_enriched_payload(prompt, top_k=5)
            except VRAMBusyError as exc:
                logger.warning("Injection annulée : %s", exc)
                winsound.MessageBeep(winsound.MB_ICONHAND)
                return

            if enriched_payload != prompt:
                simulate_paste_payload(enriched_payload)
                logger.info("Injection réussie du contexte local dans la zone active !")
                # Bip sonore discret de confirmation
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            else:
                logger.info("Aucun enrichissement appliqué.")
                winsound.MessageBeep(winsound.MB_OK)

        except Exception as exc:
            logger.error("Erreur critique lors de l'injection Hippocampe : %s", exc, exc_info=True)
            winsound.MessageBeep(winsound.MB_ICONHAND)
        finally:
            self._busy.release()

    def run_daemon(self) -> None:
        """Démarre le listener d'écoute globale en arrière-plan."""
        # Raccourci configurable (E1) : Alt+Espace ouvre le menu système de la fenêtre sous
        # Windows et est souvent capté par PowerToys Run ; défaut Ctrl+Alt+Espace.
        hotkey_str = settings.HIPPOCAMPUS_HOTKEY
        logger.info("Démarrage de l'injecteur Hippocampe (écoute globale %s)...", hotkey_str)
        logger.info("Empreinte VRAM : 0 Mo | CPU au repos : 0 %%")

        clear_stop_flag()
        with keyboard.GlobalHotKeys({hotkey_str: self.on_hotkey_triggered}) as h:
            try:
                # Attente active légère pour réagir au signal d'arrêt propre (E4)
                while h.is_alive() and not stop_requested():
                    h.join(timeout=1.0)
            except KeyboardInterrupt:
                pass
            finally:
                h.stop()
                logger.info("Arrêt gracieux de l'injecteur Hippocampe.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Injecteur Pré-Prompt Hippocampe Local (raccourci HIPPOCAMPUS_HOTKEY)")
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
