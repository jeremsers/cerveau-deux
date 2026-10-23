"""
Module 2 : Démon de Télémétrie Cognitive Temps Réel (0-VRAM).
Surveille en tâche de fond l'activité du bureau Windows 11 sans keylogging,
filtre la confidentialité, calcule le Dwell Time et déclenche des captures d'écran différées
sauvegardées en .webp pour traitement nocturne. Empreinte VRAM = 0 Mo, charge CPU < 2 %.
"""

from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
import logging
import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from PIL import Image, ImageGrab
import psutil
import win32gui
import win32process

# Activation du DPI Awareness sous Windows 11 pour coordonnées d'écran exactes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

from src.config import settings
from src.database.db_manager import DBManager, RawActivityRecord

logger = logging.getLogger("Exocortex.TelemetryDaemon")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


# ==============================================================================
# STRUCTURES WIN32 BAS NIVEAU
# ==============================================================================

class LASTINPUTINFO(ctypes.Structure):
    """Structure Win32 pour GetLastInputInfo (mesure d'inactivité physique)."""
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("dwTime", wintypes.DWORD),
    ]


# ==============================================================================
# CALCUL PERCEPTUEL DHASH & MESURES D'INPUT SANS KEYLOGGING
# ==============================================================================

def compute_dhash_64(image: Image.Image, hash_size: int = 8) -> int:
    """
    Calcule le Difference Hash (dHash) 64-bit d'une image PIL.
    Redimensionne en (hash_size + 1, hash_size) en niveaux de gris et compare les pixels adjacents.
    """
    resized = image.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = list(resized.getdata())
    width = hash_size + 1
    difference = 0
    for row in range(hash_size):
        row_offset = row * width
        for col in range(hash_size):
            left_pixel = pixels[row_offset + col]
            right_pixel = pixels[row_offset + col + 1]
            if left_pixel > right_pixel:
                difference |= (1 << (row * hash_size + col))
    return difference


def hamming_distance(h1: int, h2: int) -> int:
    """Calcule la distance de Hamming (nombre de bits différents) entre deux dHash."""
    return bin(h1 ^ h2).count("1")


def get_user_idle_seconds() -> float:
    """
    Interroge l'API Win32 GetLastInputInfo pour connaître le temps écoulé depuis la dernière
    action physique (souris ou clavier). ZÉRO keylogging du contenu des frappes.
    """
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        current_tick = ctypes.windll.kernel32.GetTickCount()
        elapsed_ms = (current_tick - lii.dwTime) & 0xFFFFFFFF
        return elapsed_ms / 1000.0
    return 0.0


# ==============================================================================
# ÉTAT EN RAM D'UNE SESSION DE FENÊTRE
# ==============================================================================

class WindowSessionState:
    """Représente l'état accumulé en mémoire sur la fenêtre active en cours."""

    def __init__(self, executable: str, window_title: str, hwnd: int) -> None:
        self.executable = executable
        self.window_title = window_title
        self.hwnd = hwnd
        self.timestamp_start: datetime = datetime.now()
        self.timestamp_last_seen: datetime = self.timestamp_start
        self.active_input_ticks: int = 0
        self.total_ticks: int = 0
        self.screenshot_path: Optional[str] = None
        self.last_dhash: Optional[int] = None
        self.last_screenshot_ts: Optional[datetime] = None

    @property
    def duration_sec(self) -> int:
        return max(1, int((self.timestamp_last_seen - self.timestamp_start).total_seconds()))

    @property
    def is_active_input(self) -> bool:
        if self.total_ticks == 0:
            return True
        return (self.active_input_ticks / self.total_ticks) >= 0.25

    @property
    def input_intensity(self) -> float:
        if self.total_ticks == 0:
            return 0.0
        return round(min(1.0, self.active_input_ticks / max(1, self.total_ticks)), 2)

    def record_tick(self, is_active: bool) -> None:
        self.total_ticks += 1
        if is_active:
            self.active_input_ticks += 1
        self.timestamp_last_seen = datetime.now()


# ==============================================================================
# DÉMON PRINCIPAL DE TÉLÉMÉTRIE
# ==============================================================================

class TelemetryDaemon:
    """
    Démon de surveillance bas niveau Win32.
    Exécuté en tâche de fond avec une consommation nulle de VRAM.
    """

    def __init__(self, db_manager: Optional[DBManager] = None) -> None:
        self.db = db_manager or DBManager()
        settings.ensure_directories()
        self.current_state: Optional[WindowSessionState] = None
        self.context_switches_count: int = 0
        self.running: bool = False
        self._setup_signals()

    def _setup_signals(self) -> None:
        """Enregistre les gestionnaires d'arrêt gracieux SIGINT / SIGTERM."""
        signal.signal(signal.SIGINT, self._handle_exit)
        signal.signal(signal.SIGTERM, self._handle_exit)

    def _handle_exit(self, signum: int, frame: Any) -> None:
        """Arrêt gracieux : sauvegarde de la session en cours avant de quitter."""
        logger.info("Signal d'interruption reçu (%s). Sauvegarde de la session active...", signum)
        self.running = False
        self.flush_current_window()
        logger.info("Démon arrêté proprement.")
        sys.exit(0)

    def is_blacklisted(self, executable: str, window_title: str) -> bool:
        """Vérifie si la fenêtre courante contient un titre ou un exécutable interdit (mots de passe, banques)."""
        exe_lower = executable.lower()
        if any(b_exe.lower() in exe_lower for b_exe in settings.EXE_BLACKLIST):
            return True

        title_lower = window_title.lower()
        if any(b_title.lower() in title_lower for b_title in settings.TITLE_BLACKLIST):
            return True

        return False

    def get_foreground_window_info(self) -> Tuple[int, str, str]:
        """
        Récupère de manière sécurisée le handle, le nom de l'exécutable et le titre
        de la fenêtre actuellement au premier plan sous Windows 11.
        """
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return 0, "Idle", ""

            title = win32gui.GetWindowText(hwnd).strip()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            executable = "unknown"
            if pid > 0 and psutil.pid_exists(pid):
                try:
                    proc = psutil.Process(pid)
                    executable = proc.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            return hwnd, executable, title
        except Exception as exc:
            logger.debug("Erreur récupération fenêtre active : %s", exc)
            return 0, "unknown", ""

    def capture_window_webp(self, hwnd: int) -> Optional[Path]:
        """
        Capture uniquement le rectangle de la fenêtre active et compresse en .webp (qualité 75).
        Sauvegarde dans _System_Buffer/screen_staging/.
        """
        try:
            rect = win32gui.GetWindowRect(hwnd)
            left, top, right, bottom = rect
            width = right - left
            height = bottom - top

            if width < 100 or height < 100:
                return None

            # Capture via mss en priorité, avec fallback sur Pillow ImageGrab
            img: Optional[Image.Image] = None
            try:
                import mss
                with mss.mss() as sct:
                    monitor = {"left": left, "top": top, "width": width, "height": height}
                    sct_img = sct.grab(monitor)
                    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            except Exception as mss_exc:
                logger.debug("Échec capture mss, fallback ImageGrab : %s", mss_exc)
                img = ImageGrab.grab(bbox=(left, top, right, bottom), all_screens=True)

            if not img:
                return None

            # Calcul du dHash pour éviter les doublons perceptuels
            dhash = compute_dhash_64(img)
            if self.current_state and self.current_state.last_dhash is not None:
                dist = hamming_distance(dhash, self.current_state.last_dhash)
                if dist <= settings.DHASH_MAX_HAMMING_DISTANCE:
                    logger.debug("Capture identique (distance Hamming = %d <= %d). Ignorée.", dist, settings.DHASH_MAX_HAMMING_DISTANCE)
                    return None

            # Sauvegarde en .webp
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screen_{timestamp_str}.webp"
            save_path = settings.SCREEN_STAGING_DIR / filename
            img.save(save_path, "WEBP", quality=75)

            if self.current_state:
                self.current_state.last_dhash = dhash
                self.current_state.screenshot_path = str(save_path.resolve())
                self.current_state.last_screenshot_ts = datetime.now()

            logger.info("Capture visuelle différée enregistrée : %s (%dx%d)", filename, width, height)
            return save_path
        except Exception as exc:
            logger.warning("Échec de la capture d'écran pour hwnd=%s : %s", hwnd, exc)
            return None

    def flush_current_window(self) -> None:
        """Enregistre la fenêtre en mémoire dans SQLite si le Dwell Time (>= 20s) est respecté."""
        if not self.current_state:
            return

        state = self.current_state
        self.current_state = None

        duration = state.duration_sec
        # Filtre de Dwell Time : ignorer si durée < 20 secondes (bruit de zapping)
        if duration < settings.DWELL_TIME_THRESHOLD_SEC:
            self.context_switches_count += 1
            logger.debug(
                "Fenêtre quittée en %d s (< %d s). Considérée comme zapping.",
                duration,
                settings.DWELL_TIME_THRESHOLD_SEC,
            )
            return

        # Construction de l'enregistrement SQLite
        record = RawActivityRecord(
            timestamp_start=state.timestamp_start,
            timestamp_end=state.timestamp_last_seen,
            duration_sec=duration,
            executable=state.executable,
            window_title=state.window_title,
            ocr_snippet=None,
            screenshot_path=state.screenshot_path,
            active_input=state.is_active_input,
            input_intensity=state.input_intensity,
            semantic_topic=None,
            cognitive_mode=None,
            processed=False,
        )
        self.db.insert_raw_activities_batch([record])
        logger.info(
            "Activité enregistrée : [%s] '%s' (%d s, input_intensity=%.2f, capture=%s)",
            state.executable,
            state.window_title[:40],
            duration,
            state.input_intensity,
            bool(state.screenshot_path),
        )

    def step(self) -> None:
        """Exécute un cycle de surveillance élémentaire (polling 2s)."""
        hwnd, executable, title = self.get_foreground_window_info()

        # Filtrage de confidentialité
        if self.is_blacklisted(executable, title):
            logger.debug("Fenêtre blacklistée détectée : [%s] '%s'. Cycle ignoré.", executable, title)
            if self.current_state:
                self.flush_current_window()
            return

        # Mesure d'activité physique (souris/clavier) sans keylogging
        idle_seconds = get_user_idle_seconds()
        is_physically_active = (idle_seconds < 10.0)

        # Vérification si la fenêtre active a changé
        window_key_changed = (
            self.current_state is None
            or self.current_state.executable != executable
            or self.current_state.window_title != title
        )

        if window_key_changed:
            # Clôture de la fenêtre précédente
            if self.current_state is not None:
                self.flush_current_window()
            # Initialisation de la nouvelle fenêtre
            self.current_state = WindowSessionState(executable, title, hwnd)

        # Mise à jour de l'état courant
        if self.current_state:
            self.current_state.record_tick(is_physically_active)

            # Déclenchement de la capture visuelle différée si session prolongée (>= 180s)
            duration = self.current_state.duration_sec
            if duration >= settings.PROLONGED_SESSION_THRESHOLD_SEC:
                should_capture = (
                    self.current_state.screenshot_path is None
                    or (
                        self.current_state.last_screenshot_ts
                        and (datetime.now() - self.current_state.last_screenshot_ts).total_seconds() >= 180
                    )
                )
                if should_capture and hwnd > 0:
                    self.capture_window_webp(hwnd)

    def run_loop(self, max_cycles: Optional[int] = None, interval_sec: Optional[float] = None) -> None:
        """Boucle de polling principale du démon."""
        polling_interval = interval_sec or settings.POLLING_INTERVAL_SEC
        self.running = True
        logger.info("=== DÉMON DE TÉLÉMÉTRIE DÉMARRÉ (0 VRAM, polling=%.1f s) ===", polling_interval)

        cycles = 0
        try:
            while self.running:
                self.step()
                cycles += 1
                if max_cycles and cycles >= max_cycles:
                    break
                time.sleep(polling_interval)
        except KeyboardInterrupt:
            self._handle_exit(signal.SIGINT, None)
        finally:
            self.flush_current_window()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exocortex Real-Time Telemetry Daemon")
    parser.add_argument("--cycles", type=int, default=None, help="Nombre de cycles à exécuter avant arrêt (pour tests).")
    parser.add_argument("--interval", type=float, default=2.0, help="Intervalle de polling en secondes (défaut: 2.0).")
    args = parser.parse_args()

    daemon = TelemetryDaemon()
    daemon.run_loop(max_cycles=args.cycles, interval_sec=args.interval)

