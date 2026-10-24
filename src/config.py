"""
Module de configuration centrale pour le système 'Exocortex & Télémétrie Cognitive'.
Définit les chemins d'accès, seuils matériels VRAM, paramètres d'inférence et listes noires.
"""

from __future__ import annotations

import os
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


# ==============================================================================
# TAXONOMIE FERMÉE DES 16 MACRO-CATÉGORIES OFFICIELLES (v0.1.2)
# ==============================================================================

AUTHORIZED_SEMANTIC_TOPICS: Dict[str, str] = {
    "IA_et_LLM_Local": "Architectures RAG, LLM locaux, GGUF, VRAM, agents IA, fine-tuning et prompt engineering",
    "Dev_et_Architecture_Tech": "Développement web (Astro, React, TS), backend, API, Python, bases de données, cloud et accessibilité",
    "HomeLab_et_Hardware": "Serveurs domestiques (Plex, Riven, Debrid, Docker), réseau/DNS, montage/dépannage PC, périphériques et consoles handheld",
    "Chefferie_Projet_et_Produit": "Gestion de projet digital, Product Ownership, cadrage MVP, UX/UI design, soutenances et méthodologie",
    "Marketing_et_Acquisition": "Google Ads, GA4, GTM, SEO/SEA, tunnels de vente, copywriting, Stripe/Make/Brevo et conversion (CRO)",
    "Freelance_et_Carriere": "Positionnement freelance, tarification, formations professionnelles (OpenClassrooms, France Travail) et carrière",
    "Admin_Finance_et_Droit": "Démarches MDPH/AAH/RSDAE, droit français/suisse, fiscalité, immobilier, gestion patrimoniale et litiges",
    "Introspection_et_Neuroatypie": "Fonctionnement HPI/TSA/TDAH/AuDHD, masking, monotropisme, bilans cliniques (ADOS-2, EMA, CRA) et métacognition",
    "Sante_et_Pharmacologie": "Suivi médical, dentaire, sommeil/apnée, pharmacologie, vaporisation, cannabinoïdes et réduction des risques",
    "Nutrition_et_Cuisine": "Volume eating, batch cooking, science culinaire, cuiseurs à riz, Ninja Creami, glycémie et équipements de cuisine",
    "Philo_et_Epistemologie": "Absurdisme (Camus), spinozisme, épistémologie, éthique, logique formelle, métaphysique et physique théorique",
    "Sociologie_et_Geopolitique": "Analyse systémique des sociétés, économie politique, géopolitique, mouvements sociaux, démographie et débats idéologiques",
    "Gaming_et_GameDesign": "Jeux solo, RPG, modding, émulation, analyse de game design, jeux incrémentaux et jeux de plateau/JDR",
    "MMORPG_et_Esport": "World of Warcraft (Mythic+, raid, guildes), Guild Wars 2, League of Legends, TFT, theorycrafting et scène esport",
    "Musique_MAO_et_Culture_Pop": "Production musicale (Maschine, Ableton, VST), Suno AI, K-Pop, rap, webtoons, mangas, animes, séries et culture web",
    "A_Trier": "Catégorie de quarantaine réservée aux échecs techniques de distillation en attente de retraitement",
}


# ==============================================================================
# VOCABULAIRES PARTAGÉS BACKEND ↔ INTERFACES (v0.5.4, B2/B5)
# ==============================================================================
# Source unique servie par l'API (/api/meta/vocabulary) : les interfaces ne codent plus
# leurs propres listes de modes ou de statuts.

COGNITIVE_MODES: Dict[str, Dict[str, str]] = {
    "production": {"label": "Production", "color": "#38bdf8"},
    "exploration": {"label": "Exploration", "color": "#f59e0b"},
    "chat_ia": {"label": "Chat IA", "color": "#8b5cf6"},
    "gaming": {"label": "Gaming", "color": "#f43f5e"},
    "media": {"label": "Média", "color": "#10b981"},
    "non_classe": {"label": "Non classé", "color": "#64748b"},
}
UNCLASSIFIED_MODE = "non_classe"

DISTILLATION_STATUSES: Dict[str, str] = {
    "success": "Distillée",
    "pending": "En attente",
    "misc_noise": "Bruit (triviale)",
    "failed_fallback": "Échec (quarantaine)",
}


def normalize_cognitive_mode(mode: Optional[str]) -> str:
    """Ramène un mode inconnu ou NULL à 'non_classe' (jamais à un mode arbitraire)."""
    return mode if mode in COGNITIVE_MODES else UNCLASSIFIED_MODE



# Règles ordonnées de normalisation (première catégorie gagnante). Un mot-clé correspond à un
# mot entier du tag ; une racine d'au moins 5 lettres correspond aussi en préfixe (« psycho » ->
# « psychotherapie ») ; un mot-clé à plusieurs mots est cherché comme expression.
_TOPIC_KEYWORD_RULES = [
    ("Musique_MAO_et_Culture_Pop", ["suno", "mao", "musique", "ableton", "kpop", "k pop", "anime", "manga", "webtoon", "popculture", "cinema", "serie", "culture"]),
    ("HomeLab_et_Hardware", ["homelab", "docker", "riven", "plex", "debrid", "hardware", "nas", "pc", "handheld", "console", "routeur", "dns"]),
    ("IA_et_LLM_Local", ["rag", "llm", "gguf", "vram", "ollama", "agent", "prompt", "fine tuning", "embedding", "gpt", "gemini", "claude"]),
    ("Dev_et_Architecture_Tech", ["astro", "react", "typescript", "python", "backend", "frontend", "api", "sqlite", "lancedb", "css", "tailwind", "devops", "git", "web", "cloud"]),
    ("Marketing_et_Acquisition", ["ads", "marketing", "ga4", "gtm", "seo", "sea", "copywriting", "cro", "stripe", "brevo", "make", "tunnel", "acquisition"]),
    ("Freelance_et_Carriere", ["freelance", "tarification", "client", "commercial", "carriere", "openclassrooms", "france travail", "emploi", "cv", "stage", "prospection"]),
    ("Admin_Finance_et_Droit", ["mdph", "aah", "rsdae", "droit", "juridique", "fiscal", "impot", "immobilier", "patrimoine", "finance", "litige", "suisse", "caf", "banque"]),
    ("Introspection_et_Neuroatypie", ["neuro", "hpi", "tsa", "tdah", "audhd", "autis", "masking", "monotropism", "ados", "cra", "psycho", "metacognit", "introspection", "atypie"]),
    ("Sante_et_Pharmacologie", ["sante", "medical", "dentaire", "sommeil", "apnee", "pharmaco", "vapo", "vaporis", "cannab", "weed", "cbd", "thc", "ordonnance", "therap"]),
    ("Nutrition_et_Cuisine", ["nutrition", "cuisine", "volume eating", "eating", "calorie", "repas", "cuiseur", "riz", "creami", "glycem", "recette", "aliment", "gastronomie"]),
    ("Philo_et_Epistemologie", ["philo", "spinoza", "camus", "absurd", "epistemol", "ethique", "logique", "metaphys", "physique", "morale"]),
    ("Sociologie_et_Geopolitique", ["sociol", "geopolit", "politique", "economie", "demograph", "ideolog", "societe", "histoire"]),
    ("MMORPG_et_Esport", ["mmorpg", "warcraft", "wow", "mythic", "raid", "guilde", "guild wars", "tft", "league of legends", "esport", "theorycraft"]),
    ("Gaming_et_GameDesign", ["gaming", "game", "modding", "emulat", "rpg", "jdr", "steam", "switch", "jeu", "jeux"]),
    ("Chefferie_Projet_et_Produit", ["projet", "produit", "product", "mvp", "ux", "ui", "soutenance", "agile", "scrum", "cadrage"]),
]
# Mots-clés de 5 lettres ou plus qui ne doivent PAS correspondre en préfixe (ambigus)
_EXACT_ONLY_KEYWORDS = {"switch"}


def _fold(text: str) -> str:
    norm = unicodedata.normalize("NFKD", text)
    return "".join(c for c in norm if not unicodedata.combining(c)).lower()


def _topic_tokens(tag: str) -> List[str]:
    """Mots d'un tag : découpage sur _ - . / espaces et sur les frontières CamelCase."""
    camel_split = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", tag)
    words = [w for w in re.split(r"[_\-\s/.,]+", _fold(tag)) if w]
    camel_words = [w for w in re.split(r"[_\-\s/.,]+", _fold(camel_split)) if w]
    # Mots du tag puis sous-mots CamelCase (« HomeLab » donne « homelab », « home » et « lab »)
    return words + [w for w in camel_words if w not in words]


def _keyword_matches(keyword: str, tokens: List[str]) -> bool:
    parts = _fold(keyword).split()
    if len(parts) > 1:
        return f" {' '.join(parts)} " in f" {' '.join(tokens)} "
    kw = parts[0]
    if len(kw) >= 5 and kw not in _EXACT_ONLY_KEYWORDS:
        return any(t == kw or t.startswith(kw) for t in tokens)
    return kw in tokens

def normalize_to_macro_topic(raw_topic: str) -> str:
    """
    Normalise de façon déterministe n'importe quel tag hérité ou émergent
    vers l'une des 16 macro-catégories fermées de l'Exocortex.
    """
    if not raw_topic:
        return "A_Trier"

    clean = raw_topic.strip().strip("'\"`")
    if clean in AUTHORIZED_SEMANTIC_TOPICS:
        return clean

    # Mappages directs pour tags v0.1.1 et historiques
    EXACT_MAPPINGS = {
        # IA & LLM
        "LLM_Local_et_Hardware": "IA_et_LLM_Local",
        "IA_Agentique_et_RAG": "IA_et_LLM_Local",
        "Prompt_Engineering": "IA_et_LLM_Local",
        "Fine_Tuning_LLM": "IA_et_LLM_Local",
        "Architecture_RAG": "IA_et_LLM_Local",
        "Inference_VRAM": "IA_et_LLM_Local",
        # Dev & Tech
        "Dev_Web_et_Stack_Astro": "Dev_et_Architecture_Tech",
        "Data_Engineering": "Dev_et_Architecture_Tech",
        "Systeme_Win32": "Dev_et_Architecture_Tech",
        "Obsidian_Exocortex": "Dev_et_Architecture_Tech",
        # HomeLab & Hardware
        "HomeLab_MediaServer": "HomeLab_et_Hardware",
        "HomeLab_Docker": "HomeLab_et_Hardware",
        # Chefferie de projet & UX
        "Chefferie_Projet_et_UX": "Chefferie_Projet_et_Produit",
        # Freelance & Carrière
        "Freelance_et_Acquisition": "Freelance_et_Carriere",
        # Santé & Pharmacologie
        "Sante_et_Admin_Perso": "Sante_et_Pharmacologie",
        # Nutrition & Cuisine
        "Nutrition_Volume_Eating": "Nutrition_et_Cuisine",
        # Philo & Épistémologie
        "Philo_Droit_et_Morale": "Philo_et_Epistemologie",
        "Metaphysique_et_Physique": "Philo_et_Epistemologie",
        # Sociologie & Géopolitique
        "Sociologie_et_Politique": "Sociologie_et_Geopolitique",
        # Gaming & GameDesign
        "Gaming_Solo_et_Modding": "Gaming_et_GameDesign",
        # MMORPG & Esport
        "MMORPG_Theorycraft": "MMORPG_et_Esport",
        # Musique, MAO & Pop Culture
        "Analyse_Musicale_et_MAO": "Musique_MAO_et_Culture_Pop",
        "Prompt_Engineering_et_Suno": "Musique_MAO_et_Culture_Pop",
        "Webtoons_Manga_et_Anime": "Musique_MAO_et_Culture_Pop",
        "Linguistique_et_Culture_Web": "Musique_MAO_et_Culture_Pop",
        "Quantified_Self": "Introspection_et_Neuroatypie",
        "General": "A_Trier",
        "Non_Classe": "A_Trier",
    }

    if clean in EXACT_MAPPINGS:
        return EXACT_MAPPINGS[clean]

    # Analyse par MOTS ENTIERS (v0.5.5, B17) : « Psychotherapie » ne tombe plus dans Dev à cause
    # de « api », ni « Enjeux_Climatiques » dans Gaming à cause de « jeu ».
    tokens = _topic_tokens(clean)
    for topic, keywords in _TOPIC_KEYWORD_RULES:
        if any(_keyword_matches(kw, tokens) for kw in keywords):
            return topic

    return "A_Trier"


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


def _env_list(name: str, default: str) -> List[str]:
    """Lit une variable d'environnement sous forme de liste séparée par des virgules."""
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


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

    # --- Contraintes Matérielles VRAM (RTX 4070 Ti Super 16 Go sous Windows 11) ---
    MIN_FREE_VRAM_GB: float = Field(
        default_factory=lambda: float(os.getenv("MIN_FREE_VRAM_GB", "8.0"))
    )
    FULL_DUAL_MODEL_VRAM_GB: float = Field(
        default_factory=lambda: float(os.getenv("FULL_DUAL_MODEL_VRAM_GB", "12.8"))
    )
    VRAM_STRICT_ABORT_FREE_GB: float = Field(
        default_factory=lambda: float(os.getenv("VRAM_STRICT_ABORT_FREE_GB", "8.0"))
    )
    VRAM_REASONING_MIN_FREE_GB: float = Field(
        default_factory=lambda: float(os.getenv("VRAM_REASONING_MIN_FREE_GB", "12.8"))
    )
    TAKEOUT_MAX_DISTILL_SESSIONS: int = Field(
        default_factory=lambda: int(os.getenv("TAKEOUT_MAX_DISTILL_SESSIONS", "0"))  # 0 = Toutes les sessions qualifiées
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
        default_factory=lambda: int(os.getenv("INACTIVITY_SESSION_THRESHOLD_MIN", "45"))
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
    BROWSER_RECEIVER_HOST: str = Field(
        default_factory=lambda: os.getenv("BROWSER_RECEIVER_HOST", "127.0.0.1")
    )
    BROWSER_RECEIVER_PORT: int = Field(
        default_factory=lambda: int(os.getenv("BROWSER_RECEIVER_PORT", "8502"))
    )
    WEB_GUI_HOST: str = Field(
        default_factory=lambda: os.getenv("WEB_GUI_HOST", "127.0.0.1")
    )
    WEB_GUI_PORT: int = Field(
        default_factory=lambda: int(os.getenv("WEB_GUI_PORT", "8500"))
    )
    # Origines autorisées en CORS sur l'API 8500 (dev front local uniquement, v0.5.2 D1).
    # L'interface web servie par FastAPI est same-origin et n'en a pas besoin.
    WEB_GUI_CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: _env_list(
            "WEB_GUI_CORS_ORIGINS",
            "http://localhost:4321,http://127.0.0.1:4321,http://localhost:5173,http://127.0.0.1:5173",
        )
    )
    # Noms d'hôte acceptés (en-tête Host) : bloque le DNS rebinding vers 8500.
    WEB_GUI_ALLOWED_HOSTS: List[str] = Field(
        default_factory=lambda: _env_list("WEB_GUI_ALLOWED_HOSTS", "127.0.0.1,localhost")
    )
    BROWSER_RECEIVER_MAX_BODY_BYTES: int = Field(
        default_factory=lambda: int(os.getenv("BROWSER_RECEIVER_MAX_BODY_BYTES", str(512 * 1024)))
    )

    # --- Compilation Google Drive : catégories jamais exportées (v0.5.2, D6) ---
    DRIVE_EXCLUDED_TOPICS: List[str] = Field(
        default_factory=lambda: _env_list(
            "DRIVE_EXCLUDED_TOPICS",
            "Sante_et_Pharmacologie,Introspection_et_Neuroatypie,Admin_Finance_et_Droit",
        )
    )

    # --- Détection Anti-Dérive / Rabbit Hole (v0.3.0 - Module 8) ---
    DRIFT_MAX_SWITCHES_30MIN: int = Field(
        default_factory=lambda: int(os.getenv("DRIFT_MAX_SWITCHES_30MIN", "25"))
    )
    DRIFT_MAX_PASSIVE_MIN: int = Field(
        default_factory=lambda: int(os.getenv("DRIFT_MAX_PASSIVE_MIN", "90"))
    )

    # --- Listes Noires de Confidentialité (v0.5.2, D7) ---
    # Termes recherchés en MOTS ENTIERS (insensible à la casse et aux accents) dans les titres de
    # fenêtres, d'onglets et les tours de chat : navigation privée, gestionnaires de mots de passe,
    # établissements bancaires et administrations. Les termes génériques ("login", "connexion",
    # "bank", "password") ne sont plus utilisés : ils écartaient des fenêtres techniques légitimes.
    # Extensible par TITLE_BLACKLIST_EXTRA (liste séparée par des virgules).
    TITLE_BLACKLIST: List[str] = Field(
        default_factory=lambda: [
            # Navigation privée
            "inprivate", "navigation privée", "private browsing", "incognito", "fenêtre privée",
            # Gestionnaires de mots de passe
            "bitwarden", "1password", "keepass", "keepassxc", "lastpass", "dashlane", "proton pass",
            # Banques, paiement et administrations
            "boursorama", "boursobank", "crédit agricole", "credit agricole", "bnp paribas",
            "société générale", "societe generale", "la banque postale", "caisse d'épargne",
            "caisse d'epargne", "banque populaire", "crédit mutuel", "credit mutuel", "lcl",
            "hello bank", "fortuneo", "monabanq", "revolut", "qonto", "paypal", "impots.gouv.fr",
        ] + _env_list("TITLE_BLACKLIST_EXTRA", "")
    )
    # Domaines dont toute URL est exclue (correspondance sur le nom d'hôte et ses sous-domaines).
    SENSITIVE_DOMAINS: List[str] = Field(
        default_factory=lambda: [
            "boursorama.com", "boursobank.com", "credit-agricole.fr", "ca-paris.fr", "bnpparibas.net",
            "mabanque.bnpparibas", "societegenerale.fr", "labanquepostale.fr", "caisse-epargne.fr",
            "banquepopulaire.fr", "creditmutuel.fr", "cic.fr", "lcl.fr", "hellobank.fr", "fortuneo.fr",
            "monabanq.com", "revolut.com", "n26.com", "qonto.com", "paypal.com", "impots.gouv.fr",
            "ameli.fr", "caf.fr", "franceconnect.gouv.fr", "bitwarden.com", "1password.com",
            "lastpass.com", "dashlane.com", "accounts.google.com", "login.microsoftonline.com",
            "login.live.com",
        ] + _env_list("SENSITIVE_DOMAINS_EXTRA", "")
    )
    EXE_BLACKLIST: List[str] = Field(
        default_factory=lambda: [
            "keepass.exe",
            "keepassxc.exe",
            "1password.exe",
            "bitwarden.exe",
            "dashlane.exe",
            "credentialuihost.exe",
            "authhost.exe",
        ]
    )
    BROWSER_EXECUTABLES: List[str] = Field(
        default_factory=lambda: ["chrome", "msedge", "brave", "firefox", "opera", "vivaldi"]
    )

    PROLONGED_SESSION_THRESHOLD_SEC: int = Field(
        default_factory=lambda: int(os.getenv("PROLONGED_SESSION_THRESHOLD_SEC", "180"))
    )
    # Inactivité au-delà de laquelle la fenêtre en cours est close (v0.5.5, A5) : le temps sans
    # saisie n'est plus compté comme de l'activité. Seuil plus long pour les fenêtres média
    # (lecture vidéo sans souris ni clavier).
    IDLE_SPLIT_THRESHOLD_SEC: int = Field(
        default_factory=lambda: int(os.getenv("IDLE_SPLIT_THRESHOLD_SEC", "300"))
    )
    IDLE_SPLIT_MEDIA_THRESHOLD_SEC: int = Field(
        default_factory=lambda: int(os.getenv("IDLE_SPLIT_MEDIA_THRESHOLD_SEC", "3600"))
    )

    # Fuseau des horodatages stockés (v0.5.5, A12) : toutes les dates en base sont en heure
    # locale naïve, comme celles du démon ; les exports Takeout en UTC sont convertis.
    LOCAL_TIMEZONE: str = Field(
        default_factory=lambda: os.getenv("LOCAL_TIMEZONE", "Europe/Paris")
    )

    # --- Kanban : dépôts autorisés pour le context-pack (v0.5.1, D3) ---
    # Liste de racines séparées par ';'. Vide = tout dépôt Git local est accepté.
    KANBAN_ALLOWED_REPO_ROOTS: List[Path] = Field(
        default_factory=lambda: [
            Path(p.strip()).resolve()
            for p in os.getenv("KANBAN_ALLOWED_REPO_ROOTS", "").split(";")
            if p.strip()
        ]
    )

    # --- Captures d'écran : purge des orphelins du staging (v0.5.1, A4) ---
    SCREEN_ORPHAN_MAX_AGE_HOURS: int = Field(
        default_factory=lambda: int(os.getenv("SCREEN_ORPHAN_MAX_AGE_HOURS", "24"))
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
    def MISC_ARCHIVE_PATH(self) -> Path:
        return self.META_DIR / "00_MISC_ET_BRUIT_ARCHIVE.md"

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
    def KANBAN_SPECS_DIR(self) -> Path:
        return self.VAULT_ROOT / "03_Kanban_Specs"

    @property
    def AGENT_QUEUE_PATH(self) -> Path:
        return self.KANBAN_SPECS_DIR / "AGENT_QUEUE.md"

    @property
    def BOOTLOADER_PATH(self) -> Path:
        return self.META_DIR / "00_BOOTLOADER_DEMAIN.md"

    @property
    def DRIFT_STATE_PATH(self) -> Path:
        return self.SYSTEM_BUFFER_DIR / "drift_state.json"

    @property
    def VOICE_INBOX_DIR(self) -> Path:
        return self.SYSTEM_BUFFER_DIR / "voice_inbox"

    @property
    def VOICE_PROCESSED_DIR(self) -> Path:
        return self.VOICE_INBOX_DIR / "processed"

    @property
    def CONCEPTS_ARCHIVE_MERGED_DIR(self) -> Path:
        return self.CONCEPTS_DIR / "_Archive_Merged"

    @property
    def CONCEPTS_QUARANTINE_DIR(self) -> Path:
        """Fiches retirées par le Vault Doctor (déplacées, jamais supprimées)."""
        return self.CONCEPTS_DIR / "_Quarantine"

    @property
    def MODEL_REASONING(self) -> str:
        """Alias pour MODEL_HEAVY_SYNTHESIS (gemma4:26b-a4b)."""
        return self.MODEL_HEAVY_SYNTHESIS

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
            self.KANBAN_SPECS_DIR,
            self.VOICE_INBOX_DIR,
            self.VOICE_PROCESSED_DIR,
            self.CONCEPTS_ARCHIVE_MERGED_DIR,
            self.CONCEPTS_QUARANTINE_DIR,
            self.TAKEOUT_DIR,
            self.MODELS_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Instance globale de configuration prête à l'emploi
settings = Settings()

