"""
Client d'inférence hybride (Ollama Local + Cloud SOTA) avec sonde matérielle VRAM (RTX 4070 Ti Super),
exclusion mutuelle stricte en VRAM (keep_alive=0) et support de sorties structurées Pydantic v2.
"""

from __future__ import annotations

import json
import logging
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import requests
from pydantic import BaseModel, ValidationError

from src.config import settings

logger = logging.getLogger("Exocortex.LLM")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

T = TypeVar("T", bound=BaseModel)


class VRAMInsufficientError(RuntimeError):
    """Levée lorsque la VRAM libre est inférieure au seuil critique (< 8.0 Go)."""
    pass


class HardwareProbe:
    """Sonde matérielle temps réel pour GPU NVIDIA via pynvml avec repli subprocess nvidia-smi."""

    @staticmethod
    def get_vram_info() -> Tuple[float, float]:
        """
        Retourne (vram_libre_gb, vram_totale_gb).
        Tente d'abord pynvml / nvidia-ml-py, puis bascule sur nvidia-smi en cas d'absence.
        """
        # 1. Tentative via pynvml
        try:
            import pynvml
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            if device_count > 0:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                free_gb = round(mem_info.free / (1024 ** 3), 2)
                total_gb = round(mem_info.total / (1024 ** 3), 2)
                pynvml.nvmlShutdown()
                return free_gb, total_gb
        except Exception as exc:
            logger.debug("Sonde pynvml non disponible ou échec (%s), repli sur nvidia-smi...", exc)

        # 2. Repli via nvidia-smi
        try:
            cmd = ["nvidia-smi", "--query-gpu=memory.free,memory.total", "--format=csv,noheader,nounits"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=5)
            lines = res.stdout.strip().splitlines()
            if lines:
                parts = lines[0].split(",")
                free_mb = float(parts[0].strip())
                total_mb = float(parts[1].strip())
                return round(free_mb / 1024.0, 2), round(total_mb / 1024.0, 2)
        except Exception as exc:
            logger.warning("Échec de la commande nvidia-smi : %s", exc)

        # 3. Repli par défaut si aucun outil GPU n'est accessible
        logger.warning("Impossible de sonder le GPU. Hypothèse conservatrice : 16 Go libres.")
        return 16.0, 16.0


class HybridLLMClient:
    """
    Client orchestrateur respectant le budget VRAM de la RTX 4070 Ti Super (16 Go).
    Gère l'exclusion mutuelle des modèles, la bascule 12B/26B et les sorties Pydantic v2.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = 180.0,
    ) -> None:
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.currently_loaded_model: Optional[str] = None
        self._session = requests.Session()

    # ==========================================================================
    # SONDE ET SÉLECTION DU MODÈLE SELON LA VRAM
    # ==========================================================================

    def check_and_select_model(self, requested_model: str) -> str:
        """
        Vérifie la VRAM libre réelle et applique la politique stricte :
        - VRAM < 8 Go : Session Gaming/3D active -> Lève VRAMInsufficientError.
        - 8 Go <= VRAM < 14.5 Go : Forcer le modèle rapide (gemma4:12b).
        - VRAM >= 14.5 Go : Autoriser le modèle demandé (gemma4:26b-a4b).
        """
        free_gb, total_gb = HardwareProbe.get_vram_info()
        logger.info("VRAM GPU : %.2f Go libres / %.2f Go totales", free_gb, total_gb)

        if free_gb < settings.MIN_FREE_VRAM_GB:
            msg = (
                f"VRAM insuffisante ({free_gb:.2f} Go < {settings.MIN_FREE_VRAM_GB} Go). "
                "Une session 3D/Gaming ou un autre processus sature le GPU. Report de l'inférence."
            )
            logger.error(msg)
            raise VRAMInsufficientError(msg)

        if free_gb < settings.FULL_DUAL_MODEL_VRAM_GB:
            if requested_model == settings.MODEL_HEAVY_SYNTHESIS:
                logger.warning(
                    "VRAM intermédiaire (%.2f Go < %.2f Go). Déclassement de '%s' vers le modèle rapide '%s'.",
                    free_gb,
                    settings.FULL_DUAL_MODEL_VRAM_GB,
                    requested_model,
                    settings.MODEL_FAST_VISION,
                )
                return settings.MODEL_FAST_VISION

        return requested_model

    def is_alive(self, timeout: float = 0.5) -> bool:
        """Vérifie rapidement si le backend LLM (Ollama ou llama_server) est démarré et joignable."""
        if settings.LLM_BACKEND == "llama_server":
            try:
                resp = self._session.get(f"{settings.LLAMA_SERVER_BASE_URL}/models", timeout=timeout)
                return resp.status_code == 200
            except Exception:
                return False
        try:
            resp = self._session.get(f"{self.base_url}/api/tags", timeout=timeout)
            return resp.status_code == 200
        except Exception:
            return False

    def ensure_local_gguf_models(self) -> Dict[str, bool]:
        """
        Vérifie et provisionne automatiquement les modèles GGUF locaux dans Ollama.
        Si gemma4:12b ou gemma4:26b-a4b sont absents d'Ollama mais que les fichiers .gguf
        sont présents dans settings.MODELS_DIR, génère le Modelfile et crée le modèle.
        """
        status: Dict[str, bool] = {
            settings.MODEL_FAST_VISION: False,
            settings.MODEL_HEAVY_SYNTHESIS: False,
        }
        if settings.LLM_BACKEND == "llama_server":
            logger.info("Backend llama_server configuré, les modèles GGUF sont gérés par le serveur dédié.")
            return status

        if not self.is_alive(timeout=1.0):
            logger.warning("Serveur Ollama non joignable à %s, provisioning ignoré.", self.base_url)
            return status

        # Récupération des modèles déjà enregistrés dans Ollama
        existing_models = set()
        try:
            resp = self._session.get(f"{self.base_url}/api/tags", timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                for m in data.get("models", []):
                    name = m.get("name", "")
                    existing_models.add(name)
                    if ":" in name:
                        existing_models.add(name.split(":")[0])
        except Exception as exc:
            logger.warning("Impossible de lister les modèles Ollama : %s", exc)

        models_to_check = [
            (settings.MODEL_FAST_VISION, settings.GGUF_FAST_PATH),
            (settings.MODEL_HEAVY_SYNTHESIS, settings.GGUF_HEAVY_PATH),
        ]

        for model_name, gguf_path in models_to_check:
            if any(model_name in em or em.startswith(model_name) for em in existing_models):
                logger.info("Modèle Ollama '%s' déjà disponible.", model_name)
                status[model_name] = True
                continue

            if not gguf_path.exists():
                logger.warning("Binaire GGUF introuvable pour '%s' à l'emplacement : %s", model_name, gguf_path)
                continue

            logger.info("Modèle '%s' absent d'Ollama. Création automatique depuis %s...", model_name, gguf_path.name)
            modelfile_content = (
                f"FROM \"{gguf_path.resolve().as_posix()}\"\n"
                'TEMPLATE """{{ if .System }}<start_of_turn>system\n'
                '{{ .System }}<end_of_turn>\n'
                '{{ end }}{{ if .Prompt }}<start_of_turn>user\n'
                '{{ .Prompt }}<end_of_turn>\n'
                '{{ end }}<start_of_turn>model\n'
                '{{ .Response }}<end_of_turn>\n'
                '"""\n'
                'PARAMETER stop "<start_of_turn>"\n'
                'PARAMETER stop "<end_of_turn>"\n'
            )

            modelfile_path = settings.MODELS_DIR / f"Modelfile.{model_name.replace(':', '_')}"
            try:
                modelfile_path.write_text(modelfile_content, encoding="utf-8")
                # 1. Tentative via l'API REST Ollama /api/create
                create_url = f"{self.base_url}/api/create"
                create_payload = {
                    "name": model_name,
                    "modelfile": modelfile_content,
                    "stream": False,
                }
                c_resp = self._session.post(create_url, json=create_payload, timeout=600.0)
                if c_resp.status_code == 200:
                    logger.info("Modèle Ollama '%s' créé avec succès via API REST !", model_name)
                    status[model_name] = True
                    continue
            except Exception as exc:
                logger.debug("Tentative API REST pour créer '%s' : %s", model_name, exc)

            # 2. Repli via CLI subprocess ollama create
            try:
                cmd = ["ollama", "create", model_name, "-f", str(modelfile_path.resolve())]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=600.0)
                if res.returncode == 0:
                    logger.info("Modèle Ollama '%s' créé avec succès via CLI !", model_name)
                    status[model_name] = True
                else:
                    logger.warning("Échec de 'ollama create' pour '%s' : %s", model_name, res.stderr)
            except Exception as exc:
                logger.error("Erreur d'exécution de 'ollama create' pour '%s' : %s", model_name, exc)

        return status

    # ==========================================================================
    # EXCLUSION MUTUELLE ET PURGE MÉMOIRE (KEEP_ALIVE=0)
    # ==========================================================================

    def unload_model(self, model_name: str) -> bool:
        """Décharge immédiatement un modèle de la VRAM en envoyant keep_alive=0 à Ollama."""
        if not self.is_alive():
            self.currently_loaded_model = None
            return False
        try:
            url = f"{self.base_url}/api/generate"
            payload = {"model": model_name, "keep_alive": 0}
            resp = self._session.post(url, json=payload, timeout=5)
            if resp.status_code == 200:
                logger.info("Modèle '%s' déchargé avec succès de la VRAM (keep_alive=0).", model_name)
                if self.currently_loaded_model == model_name:
                    self.currently_loaded_model = None
                return True
        except Exception as exc:
            logger.warning("Échec du déchargement du modèle '%s' : %s", model_name, exc)
        return False

    def unload_all_models(self) -> None:
        """Purger l'intégralité des modèles connus pour garantir 0 Mo alloué."""
        models_to_purge = [
            settings.MODEL_FAST_VISION,
            settings.MODEL_HEAVY_SYNTHESIS,
            settings.MODEL_EMBEDDING,
        ]
        if self.currently_loaded_model and self.currently_loaded_model not in models_to_purge:
            models_to_purge.append(self.currently_loaded_model)

        for model in models_to_purge:
            self.unload_model(model)
        self.currently_loaded_model = None
        time.sleep(0.5)  # Pause brève pour libération pilote NVIDIA

    # ==========================================================================
    # GÉNÉRATION TEXTUELLE LOCALE
    # ==========================================================================

    def generate_text(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        keep_alive: int = 0,
        temperature: float = 0.2,
    ) -> str:
        """
        Exécute une génération textuelle simple sur Ollama avec contrôle de VRAM.
        keep_alive=0 par défaut pour purger la mémoire après le traitement.
        """
        if not self.is_alive():
            raise ConnectionError(f"Le serveur Ollama à {self.base_url} est inaccessible.")

        target_model = model or settings.MODEL_FAST_VISION
        effective_model = self.check_and_select_model(target_model)

        # Si un autre modèle était en mémoire, le purger
        if self.currently_loaded_model and self.currently_loaded_model != effective_model:
            self.unload_model(self.currently_loaded_model)

        if settings.LLM_BACKEND == "llama_server":
            url = f"{settings.LLAMA_SERVER_BASE_URL}/chat/completions"
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            payload = {
                "model": effective_model,
                "messages": messages,
                "temperature": temperature,
                "stream": False,
            }
            try:
                resp = self._session.post(url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            except requests.RequestException as exc:
                logger.error("Erreur requête HTTP llama_server (%s) : %s", url, exc)
                raise

        url = f"{self.base_url}/api/chat"
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": effective_model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
            "keep_alive": keep_alive,
        }

        try:
            resp = self._session.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            self.currently_loaded_model = effective_model if keep_alive != 0 else None
            return data.get("message", {}).get("content", "").strip()
        except requests.RequestException as exc:
            logger.error("Erreur de requête HTTP vers Ollama (%s) : %s", url, exc)
            raise

    def generate_vision(
        self,
        prompt: str,
        image_path: Path,
        system: str = "",
        model: Optional[str] = None,
        keep_alive: int = 0,
    ) -> str:
        """
        Analyse multimodale d'une capture d'écran (.webp) via gemma4:12b sur Ollama.
        L'image est encodée en base64 selon le contrat standard Ollama /api/chat.
        """
        if not image_path.exists():
            return ""

        if not self.is_alive():
            logger.warning("Ollama hors ligne pour l'analyse vision de '%s'.", image_path.name)
            return f"[Capture {image_path.name}]"

        import base64
        with open(image_path, "rb") as img_f:
            b64_image = base64.b64encode(img_f.read()).decode("utf-8")

        target_model = model or settings.MODEL_FAST_VISION
        effective_model = self.check_and_select_model(target_model)

        if self.currently_loaded_model and self.currently_loaded_model != effective_model:
            self.unload_model(self.currently_loaded_model)

        url = f"{self.base_url}/api/chat"
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt, "images": [b64_image]})

        payload = {
            "model": effective_model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.1},
            "keep_alive": keep_alive,
        }

        try:
            resp = self._session.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            self.currently_loaded_model = effective_model if keep_alive != 0 else None
            return data.get("message", {}).get("content", "").strip()
        except Exception as exc:
            logger.warning("Échec de l'analyse visuelle de '%s' : %s", image_path.name, exc)
            return f"[Capture {image_path.name}]"

    # ==========================================================================
    # GÉNÉRATION STRUCTURÉE PYDANTIC V2
    # ==========================================================================

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system: str = "",
        model: Optional[str] = None,
        keep_alive: int = 0,
    ) -> T:
        """
        Génère une réponse garantie conforme au schéma Pydantic v2 en mode format='json'.
        Effectue une tentative de réparation si le premier parse JSON échoue.
        """
        target_model = model or settings.MODEL_FAST_VISION
        effective_model = self.check_and_select_model(target_model)

        if not self.is_alive():
            raise ConnectionError(f"Le serveur Ollama à {self.base_url} est inaccessible.")

        if self.currently_loaded_model and self.currently_loaded_model != effective_model:
            self.unload_model(self.currently_loaded_model)

        json_schema = json.dumps(response_model.model_json_schema(), ensure_ascii=False)
        strict_system = (
            (system + "\n\n" if system else "")
            + f"Tu dois impérativement répondre UNIQUEMENT avec un objet JSON valide conforme à ce schéma JSON :\n{json_schema}"
        )

        messages = [
            {"role": "system", "content": strict_system},
            {"role": "user", "content": prompt},
        ]

        if settings.LLM_BACKEND == "llama_server":
            url = f"{settings.LLAMA_SERVER_BASE_URL}/chat/completions"
            payload = {
                "model": effective_model,
                "messages": messages,
                "response_format": {"type": "json_object"},
                "temperature": 0.1,
                "stream": False,
            }
            try:
                resp = self._session.post(url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                raw_text = resp.json()["choices"][0]["message"]["content"].strip()
                parsed_dict = json.loads(raw_text)
                return response_model.model_validate(parsed_dict)
            except Exception as exc:
                logger.error("Erreur parsing structuré llama_server : %s", exc)
                raise

        url = f"{self.base_url}/api/chat"
        payload = {
            "model": effective_model,
            "messages": messages,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.1},
            "keep_alive": keep_alive,
        }

        try:
            resp = self._session.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            raw_text = resp.json().get("message", {}).get("content", "").strip()
            self.currently_loaded_model = effective_model if keep_alive != 0 else None

            # Parsing JSON et validation Pydantic
            parsed_dict = json.loads(raw_text)
            return response_model.model_validate(parsed_dict)
        except (ValidationError, json.JSONDecodeError) as err:
            logger.warning("Échec du parsing initial JSON (%s). Tentative d'extraction manuelle...", err)
            # Tentative d'extraction de bloc {...}
            import re
            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                try:
                    fixed_dict = json.loads(match.group(0))
                    return response_model.model_validate(fixed_dict)
                except Exception:
                    pass
            raise

    # ==========================================================================
    # EMBEDDINGS VECTORIELS (BGE-M3)
    # ==========================================================================

    def generate_embeddings(
        self,
        text: str,
        model: Optional[str] = None,
        keep_alive: int = 0,
    ) -> List[float]:
        """Génère un vecteur d'embedding via bge-m3 sur Ollama."""
        target_model = model or settings.MODEL_EMBEDDING

        if not self.is_alive():
            raise ConnectionError(f"Le serveur Ollama à {self.base_url} est inaccessible.")

        if self.currently_loaded_model and self.currently_loaded_model != target_model:
            self.unload_model(self.currently_loaded_model)

        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": target_model,
            "prompt": text,
            "keep_alive": keep_alive,
        }
        try:
            resp = self._session.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            self.currently_loaded_model = target_model if keep_alive != 0 else None
            return data.get("embedding", [])
        except requests.RequestException as exc:
            logger.error("Erreur lors de la génération d'embeddings avec '%s' : %s", target_model, exc)
            raise

    # ==========================================================================
    # INTÉGRATION CLOUD SOTA (GOOGLE-GENAI SDK)
    # ==========================================================================

    def generate_cloud_sota(
        self,
        prompt: str,
        system: str = "",
        response_model: Optional[Type[T]] = None,
        model: Optional[str] = None,
    ) -> Union[str, T]:
        """
        Appel optionnel vers un modèle Cloud SOTA (ex: gemini-2.5-flash / gemini-2.5-pro)
        via le SDK officiel google-genai pour traiter des contextes massifs (Passe 2).
        """
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError(
                "Clé d'API GEMINI_API_KEY absente. "
                "Pour utiliser le mode Cloud SOTA, renseignez GEMINI_API_KEY dans votre fichier .env."
            )

        try:
            from google import genai
            from google.genai import types
        except ImportError:
            raise ImportError(
                "Le SDK 'google-genai' n'est pas installé. "
                "Veuillez l'installer via : pip install google-genai"
            )

        target_model = model or settings.GEMINI_MODEL
        client = genai.Client(api_key=api_key)

        config_kwargs: Dict[str, Any] = {}
        if system:
            config_kwargs["system_instruction"] = system

        if response_model:
            config_kwargs["response_mime_type"] = "application/json"
            config_kwargs["response_schema"] = response_model

        config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

        logger.info("Envoi de la requête Cloud SOTA au modèle '%s'...", target_model)
        resp = client.models.generate_content(
            model=target_model,
            contents=prompt,
            config=config,
        )

        output_text = resp.text or ""
        if response_model:
            parsed = json.loads(output_text)
            return response_model.model_validate(parsed)
        return output_text


# Instance par défaut prête à l'emploi
llm_client = HybridLLMClient()
