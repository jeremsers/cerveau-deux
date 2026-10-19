"""
Module de configuration centrale pour le système 'Exocortex & Télémétrie Cognitive'.
Définit les chemins d'accès, seuils matériels VRAM, paramètres d'inférence et listes noires.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field


def _load_env_file(dotenv_path: Path) -> None:
    """Charge manuellement les variables d'environnement depuis un fichier .env si non déjà définies."""
    if not dotenv_path.exists():
        return
    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key and key not in os.environ:
                    os.environ[key] = val
    except Exception as exc:
        print(f"[Avertissement] Impossible de charger le fichier .env : {exc}")


# Chargement du fichier .env à la racine du projet
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
_load_env_file(_ENV_FILE)


class Settings(BaseModel):
    """Configuration globale du système Exocortex avec validation Pydantic v2."""

    # --- Chemins Principaux ---
    VAULT_ROOT: Path = Field(
        default_factory=lambda: Path(os.getenv("VAULT_ROOT", "./Vault_Data")).resolve()
    )
    TAKEOUT_DIR: Path = Field(
        default_factory=lambda: Path(os.getenv("TAKEOUT_DIR", "./takeout_raw")).resolve()
    )

    # --- Modèles d'Inférence LLM Locale (Ollama / Llama-server) ---
    MODELS_DIR: Path = Field(
        default_factory=lambda: Path(os.getenv("MODELS_DIR", "./models")).resolve()
    )
    LLM_BACKEND: str = Field(
        default_factory=lambda: os.getenv("LLM_BACKEND", "ollama").lower()  # "ollama" ou "llama_server"
    )
    GGUF_FAST_FILENAME: str = Field(
        default_factory=lambda: os.getenv("GGUF_FAST_FILENAME", "gemma-4-12b-it-Q4_K_M.gguf")
    )
    GGUF_HEAVY_FILENAME: str = Field(
        default_factory=lambda: os.getenv("GGUF_HEAVY_FILENAME", "gemma-4-26b-a4b-it-UD-IQ4_NL.gguf")
    )
    OLLAMA_BASE_URL: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    )
    LLAMA_SERVER_BASE_URL: str = Field(
        default_factory=lambda: os.getenv("LLAMA_SERVER_BASE_URL", "http://localhost:8080/v1").rstrip("/")
    )
    MODEL_FAST_VISION: str = Field(
        default_factory=lambda: os.getenv("MODEL_FAST_VISION", "gemma4:12b")
    )
    MODEL_HEAVY_SYNTHESIS: str = Field(
        default_factory=lambda: os.getenv("MODEL_HEAVY_SYNTHESIS", "gemma4:26b-a4b")
    )
    MODEL_EMBEDDING: str = Field(
        default_factory=lambda: os.getenv("MODEL_EMBEDDING", "bge-m3")
    )

    # --- Contraintes Matérielles VRAM (RTX 4070 Ti Super 16 Go) ---
    MIN_FREE_VRAM_GB: float = Field(
        default_factory=lambda: float(os.getenv("MIN_FREE_VRAM_GB", "8.0"))
    )
    FULL_DUAL_MODEL_VRAM_GB: float = Field(
        default_factory=lambda: float(os.getenv("FULL_DUAL_MODEL_VRAM_GB", "14.5"))
    )

    # --- Mode Cloud SOTA (Optionnel) ---
    TAKEOUT_MODE: str = Field(
        default_factory=lambda: os.getenv("TAKEOUT_MODE", "web_manual").lower()
    )
    GEMINI_API_KEY: Optional[str] = Field(
        default_factory=lambda: os.getenv("GEMINI_API_KEY", "").strip() or None
    )
    GEMINI_MODEL: str = Field(
        default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    )

    # --- Paramètres de Sessionisation & Filtrage Bruit (Module 1) ---
    INACTIVITY_SESSION_THRESHOLD_MIN: int = Field(
        default_factory=lambda: int(os.getenv("INACTIVITY_SESSION_THRESHOLD_MIN", "120"))
    )
    MIN_TURNS_THRESHOLD: int = Field(
        default_factory=lambda: int(os.getenv("MIN_TURNS_THRESHOLD", "3"))
    )
    MIN_USER_CHARS_THRESHOLD: int = Field(
        default_factory=lambda: int(os.getenv("MIN_USER_CHARS_THRESHOLD", "250"))
    )

    # --- Paramètres Corrélation Multi-Takeout (Google Search & YouTube) ---
    SEARCH_BURST_WINDOW_MIN: int = Field(
        default_factory=lambda: int(os.getenv("SEARCH_BURST_WINDOW_MIN", "45"))
    )
    SEARCH_BURST_MIN_EVENTS: int = Field(
        default_factory=lambda: int(os.getenv("SEARCH_BURST_MIN_EVENTS", "5"))
    )
    TEMPORAL_JOIN_BEFORE_MIN: int = Field(
        default_factory=lambda: int(os.getenv("TEMPORAL_JOIN_BEFORE_MIN", "60"))
    )
    TEMPORAL_JOIN_AFTER_MIN: int = Field(
        default_factory=lambda: int(os.getenv("TEMPORAL_JOIN_AFTER_MIN", "30"))
    )

    # --- Démon de Télémétrie Temps Réel Win32 (Module 2) ---
    POLLING_INTERVAL_SEC: float = Field(
        default_factory=lambda: float(os.getenv("POLLING_INTERVAL_SEC", "2.0"))
    )
    DWELL_TIME_THRESHOLD_SEC: int = Field(
        default_factory=lambda: int(os.getenv("DWELL_TIME_THRESHOLD_SEC", "20"))
    )
    DHASH_MAX_HAMMING_DISTANCE: int = Field(
        default_factory=lambda: int(os.getenv("DHASH_MAX_HAMMING_DISTANCE", "5"))
    )

    # --- Listes Noires de Confidentialité (Win32 Daemon) ---
    TITLE_BLACKLIST: List[str] = Field(
        default_factory=lambda: [
            "bitwarden",
            "1password",
            "keepass",
            "inprivate",
            "navigation privée",
            "private browsing",
            "incognito",
            "banque",
            "bank",
            "paypal",
            "impots.gouv.fr",
            "credit-agricole",
            "bourso",
            "bnp paribas",
            "societe generale",
            "login",
            "connexion",
            "authenticator",
            "mot de passe",
            "password",
            "master password",
            "credentials",
        ]
    )
    EXE_BLACKLIST: List[str] = Field(
        default_factory=lambda: [
            "keepass.exe",
            "1password.exe",
            "bitwarden.exe",
            "credentialuihost.exe",
            "authhost.exe",
        ]
    )

    PROLONGED_SESSION_THRESHOLD_SEC: int = Field(
        default_factory=lambda: int(os.getenv("PROLONGED_SESSION_THRESHOLD_SEC", "180"))
    )

    # --- Propriétés Calculées d'Arborescence Vault ---
    @property
    def META_DIR(self) -> Path:
        return self.VAULT_ROOT / "00_Meta"

    @property
    def PROFIL_COGNITIF_PATH(self) -> Path:
        return self.META_DIR / "Profil_Cognitif.md"

    @property
    def TAXONOMIE_TAGS_PATH(self) -> Path:
        return self.META_DIR / "Taxonomie_Tags.md"

    @property
    def EPISODIC_DIR(self) -> Path:
        return self.VAULT_ROOT / "01_Episodique"

    @property
    def CONCEPTS_DIR(self) -> Path:
        return self.VAULT_ROOT / "02_Concepts"

    @property
    def SYSTEM_BUFFER_DIR(self) -> Path:
        return self.VAULT_ROOT / "_System_Buffer"

    @property
    def SCREEN_STAGING_DIR(self) -> Path:
        return self.SYSTEM_BUFFER_DIR / "screen_staging"

    @property
    def TAKEOUT_STAGING_DIR(self) -> Path:
        return self.SYSTEM_BUFFER_DIR / "takeout_staging"

    @property
    def DB_PATH(self) -> Path:
        return self.SYSTEM_BUFFER_DIR / "telemetry.db"

    @property
    def SQLITE_DB_PATH(self) -> Path:
        return self.DB_PATH

    @property
    def LANCEDB_DIR(self) -> Path:
        return self.SYSTEM_BUFFER_DIR / "lancedb_store"

    @property
    def GOOGLE_DRIVE_SYNC_DIR(self) -> Path:
        return self.VAULT_ROOT / "Google_Drive_Sync"

    @property
    def GGUF_FAST_PATH(self) -> Path:
        """Chemin vers le binaire GGUF 12B (tolérance casse)."""
        p = self.MODELS_DIR / self.GGUF_FAST_FILENAME
        if not p.exists() and self.MODELS_DIR.exists():
            for c in self.MODELS_DIR.glob("*.gguf"):
                if c.name.lower() == self.GGUF_FAST_FILENAME.lower():
                    return c
        return p

    @property
    def GGUF_HEAVY_PATH(self) -> Path:
        """Chemin vers le binaire GGUF 26B (tolérance casse)."""
        p = self.MODELS_DIR / self.GGUF_HEAVY_FILENAME
        if not p.exists() and self.MODELS_DIR.exists():
            for c in self.MODELS_DIR.glob("*.gguf"):
                if c.name.lower() == self.GGUF_HEAVY_FILENAME.lower():
                    return c
        return p

    def ensure_directories(self) -> None:
        """Crée l'intégralité des répertoires requis pour Vault_Data et ses sous-dossiers techniques."""
        directories = [
            self.VAULT_ROOT,
            self.META_DIR,
            self.EPISODIC_DIR,
            self.CONCEPTS_DIR,
            self.SYSTEM_BUFFER_DIR,
            self.SCREEN_STAGING_DIR,
            self.TAKEOUT_STAGING_DIR,
            self.LANCEDB_DIR,
            self.GOOGLE_DRIVE_SYNC_DIR,
            self.TAKEOUT_DIR,
            self.MODELS_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Instance globale de configuration prête à l'emploi
settings = Settings()

