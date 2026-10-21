"""
Client d'inférence hybride (Ollama Local + Cloud SOTA) avec sonde matérielle VRAM (RTX 4070 Ti Super),
exclusion mutuelle stricte en VRAM (keep_alive=0) et support de sorties structurées Pydantic v2.
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Type, TypeVar, Union

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import requests
from pydantic import BaseModel, ValidationError

from src.config import settings

logger = logging.getLogger("Exocortex.LLM")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

T = TypeVar("T", bound=BaseModel)


def repair_truncated_json(raw_text: str) -> str:
    """
    Répare un JSON tronqué (ex: num_predict épuisé) ou pollué par des balises de réflexion.
    - Supprime tout bloc de pensée interne (<|thought|> ou <think>).
    - Extrait le JSON à partir du premier '{'.
    - Si une chaîne est restée non fermée dans synthesized_markdown_body, coupe proprement
      à la dernière fin de phrase valide et referme l'objet JSON avec related_concepts: [].
    """
    if not raw_text:
        return "{}"

    # 1. Suppression des balises de réflexion (Thinking mode)
    cleaned = re.sub(r"<\|thought\|>.*?<\|/thought\|>", "", raw_text, flags=re.DOTALL)
    cleaned = re.sub(r"<think>.*?</think>", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"^.*?<\|/thought\|>", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"^.*?</think>", "", cleaned, flags=re.DOTALL)

    # 2. Extraction à partir du premier '{'
    start_brace = cleaned.find("{")
    if start_brace == -1:
        return cleaned.strip()

    candidate = cleaned[start_brace:].strip()

    # Si déjà valide, retour immédiat
    try:
        json.loads(candidate)
        return candidate
    except Exception:
        pass

    # 3. Réparation si synthesized_markdown_body est tronqué
    body_key = '"synthesized_markdown_body"'
    if body_key in candidate:
        key_pos = candidate.find(body_key)
        val_quote_start = candidate.find('"', key_pos + len(body_key) + 1)
        if val_quote_start != -1:
            best_cut = -1
            for end_char in [".", "!", "?", "\n"]:
                pos = candidate.rfind(end_char)
                if pos > val_quote_start and pos > best_cut:
                    best_cut = pos

            if best_cut > val_quote_start:
                cut_text = candidate[:best_cut + 1].rstrip()
                while cut_text.endswith("\\"):
                    cut_text = cut_text[:-1]

                repaired = cut_text + '", "related_concepts": []}'
                try:
                    json.loads(repaired)
                    return repaired
                except Exception:
                    pass

    # 4. Tentative générique de fermeture des guillemets et accolades manquants
    for suffix in ['"}', '"]}', '", "related_concepts": []}', '}']:
        try:
            cand = candidate.rstrip()
            while cand.endswith("\\"):
                cand = cand[:-1]
            test_rep = cand + suffix
            json.loads(test_rep)
            return test_rep
        except Exception:
            continue

    return candidate


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

    def is_model_loaded_in_ollama(self, model_name: str) -> bool:
        """Vérifie via l'API /api/ps d'Ollama si le modèle est déjà chargé en VRAM."""
        if self.currently_loaded_model == model_name:
            return True
        if settings.LLM_BACKEND == "llama_server":
            return True
        try:
            resp = self._session.get(f"{self.base_url}/api/ps", timeout=1.0)
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                for m in models:
                    loaded_name = m.get("name", "")
                    if model_name in loaded_name or loaded_name.startswith(model_name):
                        self.currently_loaded_model = model_name
                        return True
        except Exception:
            pass
        return False

    def check_and_select_model(self, requested_model: str) -> str:
        """
        Vérifie la VRAM libre réelle en tenant compte du modèle déjà chargé par l'Exocortex :
        - Si requested_model est DÉJÀ chargé en VRAM : l'autoriser immédiatement sans bloquer.
        - Si un AUTRE modèle Exocortex est chargé : le décharger d'abord pour mesurer la vraie VRAM libre.
        - Si VRAM < 8 Go ou (modèle 26B et VRAM < 12.8 Go) : purge active préalable via force_clear_vram().
        - Si après purge VRAM < 8 Go : Session Gaming/3D active -> Lève VRAMInsufficientError.
        - 8 Go <= VRAM < 12.8 Go : Déclassement vers le modèle rapide (gemma4:12b).
        - VRAM >= 12.8 Go : Autoriser le modèle demandé (gemma4:26b-a4b).
        """
        # 1. Si le modèle demandé est déjà résident en VRAM, la mémoire qu'il occupe est légitime !
        if self.is_model_loaded_in_ollama(requested_model):
            return requested_model

        # 2. Si un autre modèle Exocortex occupe la VRAM, on le décharge avant de mesurer la VRAM libre
        if self.currently_loaded_model and self.currently_loaded_model != requested_model:
            self.unload_model(self.currently_loaded_model)

        free_gb, total_gb = HardwareProbe.get_vram_info()

        # 3. Purge préventive active via /api/ps si mémoire basse (élimine les modèles fantômes)
        min_strict = getattr(settings, "VRAM_STRICT_ABORT_FREE_GB", settings.MIN_FREE_VRAM_GB)
        min_reasoning = getattr(settings, "VRAM_REASONING_MIN_FREE_GB", settings.FULL_DUAL_MODEL_VRAM_GB)
        is_heavy = requested_model in (settings.MODEL_HEAVY_SYNTHESIS, getattr(settings, "MODEL_REASONING", None))

        if free_gb < min_strict or (is_heavy and free_gb < min_reasoning):
            logger.info("VRAM disponible (%.2f Go) en dessous du seuil requis. Purge préventive active (force_clear_vram)...", free_gb)
            free_gb = self.force_clear_vram()

        logger.info("VRAM GPU : %.2f Go libres / %.2f Go totales", free_gb, total_gb)

        if free_gb < min_strict:
            msg = (
                f"VRAM insuffisante ({free_gb:.2f} Go < {min_strict} Go). "
                "Une session 3D/Gaming ou un autre processus externe sature le GPU. Report de l'inférence."
            )
            logger.error(msg)
            raise VRAMInsufficientError(msg)

        if free_gb < min_reasoning:
            if is_heavy:
                logger.warning(
                    "VRAM intermédiaire (%.2f Go < %.2f Go). Déclassement de '%s' vers le modèle rapide '%s'.",
                    free_gb,
                    min_reasoning,
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

    def is_cloud_available(self) -> bool:
        """Vérifie si une clé API Gemini Cloud SOTA est configurée."""
        return bool(settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY.strip()) > 5)

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
                "PARAMETER num_ctx 16384\n"
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

    def force_clear_vram(self) -> float:
        """
        Interroge /api/ps d'Ollama et décharge immédiatement tous les modèles résidents en VRAM
        (purge active des modèles fantômes d'anciens runs ou de crashs).
        Retourne la quantité de VRAM libre en Go après déchargement.
        """
        loaded_models: Set[str] = set()
        if self.is_alive():
            try:
                resp = self._session.get(f"{self.base_url}/api/ps", timeout=5.0)
                if resp.status_code == 200:
                    for m in resp.json().get("models", []):
                        name = m.get("name") or m.get("model")
                        if name:
                            loaded_models.add(name)
            except Exception as exc:
                logger.debug("Impossible d'interroger /api/ps lors du force_clear_vram : %s", exc)

        # Ajouter tous les modèles connus du système
        known_models = [
            settings.MODEL_HEAVY_SYNTHESIS,
            settings.MODEL_FAST_VISION,
            settings.MODEL_EMBEDDING,
        ]
        if hasattr(settings, "MODEL_REASONING") and settings.MODEL_REASONING:
            known_models.append(settings.MODEL_REASONING)
        for km in known_models:
            loaded_models.add(km)

        if self.currently_loaded_model:
            loaded_models.add(self.currently_loaded_model)

        for model_name in loaded_models:
            try:
                self.unload_model(model_name)
            except Exception as exc:
                logger.debug("Échec déchargement modèle '%s' : %s", model_name, exc)

        self.currently_loaded_model = None
        time.sleep(1.0)
        free_gb, _ = HardwareProbe.get_vram_info()
        logger.info("VRAM GPU après purge active (force_clear_vram) : %.2f Go libres", free_gb)
        return free_gb

    # ==========================================================================
    # GÉNÉRATION TEXTUELLE LOCALE
    # ==========================================================================

    def generate_text(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        keep_alive: Union[int, str] = 0,
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
            self.currently_loaded_model = effective_model if (keep_alive != 0 and keep_alive != "0") else None
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
        keep_alive: Union[int, str] = 0,
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
            self.currently_loaded_model = effective_model if (keep_alive != 0 and keep_alive != "0") else None
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
        keep_alive: Union[int, str] = 0,
        enable_thinking: bool = True,
        num_predict: int = 8192,
        allow_model_switch_fallback: bool = False,
    ) -> T:
        """
        Génère une réponse garantie conforme au schéma Pydantic v2 en mode format='json'.
        Supporte le mode thinking (enable_thinking=True, num_predict=8192) et la réparation automatique JSON.
        Si allow_model_switch_fallback=False, aucun changement de modèle ni retry inline n'est effectué
        (délégué aux vagues séquentielles d'orchestration pour éviter le ping-pong VRAM).
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
                "max_tokens": num_predict,
            }
            try:
                resp = self._session.post(url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                raw_text = resp.json()["choices"][0]["message"]["content"].strip()
                repaired_text = repair_truncated_json(raw_text)
                parsed_dict = json.loads(repaired_text)
                return response_model.model_validate(parsed_dict)
            except Exception as exc:
                logger.error("Erreur parsing structuré llama_server : %s", exc)
                raise

        url = f"{self.base_url}/api/chat"
        schema_dict = response_model.model_json_schema()

        def _execute_ollama_call(
            target_m: str,
            target_prompt: str,
            temp: float,
            pred: int,
            thinking: bool,
        ) -> T:
            call_system = strict_system
            if not thinking:
                call_system = (
                    call_system
                    + "\n\nIMPORTANT: Réponds directement et immédiatement en JSON sans phase de réflexion préliminaire."
                )

            msgs = [
                {"role": "system", "content": call_system},
                {"role": "user", "content": target_prompt},
            ]
            options = {
                "temperature": temp,
                "num_ctx": 16384,
                "num_predict": pred,
            }
            payload = {
                "model": target_m,
                "messages": msgs,
                "stream": False,
                "format": schema_dict,
                "options": options,
                "keep_alive": keep_alive,
            }
            if not thinking:
                payload["think"] = False

            resp = self._session.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            raw_text = resp.json().get("message", {}).get("content", "").strip()
            self.currently_loaded_model = target_m if (keep_alive != 0 and keep_alive != "0") else None

            # Parsing JSON et validation Pydantic avec auto-réparation
            repaired_text = repair_truncated_json(raw_text)
            try:
                parsed_dict = json.loads(repaired_text)
                return response_model.model_validate(parsed_dict)
            except (ValidationError, json.JSONDecodeError) as err:
                match = re.search(r"\{.*\}", repaired_text, re.DOTALL)
                if match:
                    fixed_dict = json.loads(match.group(0))
                    return response_model.model_validate(fixed_dict)
                raise err

        # Essai 1 : Appel standard sur le modèle cible
        try:
            return _execute_ollama_call(
                effective_model,
                prompt,
                temp=0.1,
                pred=num_predict,
                thinking=enable_thinking,
            )
        except Exception as exc1:
            if not allow_model_switch_fallback:
                logger.warning(
                    "Échec génération structurée sur '%s' (%s) [allow_model_switch_fallback=False]. Propagation de l'erreur.",
                    effective_model,
                    exc1,
                )
                raise

            logger.warning(
                "Échec Essai 1 génération structurée sur '%s' (%s). Déclenchement Essai 2 avec prompt tronqué (6000 chars)...",
                effective_model,
                exc1,
            )

        # Essai 2 (Fallback legacy uniquement) : Prompt tronqué à 6000 caractères max + pause de 1.5s
        time.sleep(1.5)
        truncated_prompt = prompt[:6000] if len(prompt) > 6000 else prompt
        try:
            return _execute_ollama_call(
                effective_model,
                truncated_prompt,
                temp=0.2,
                pred=4096,
                thinking=False,
            )
        except Exception as exc2:
            logger.warning(
                "Échec Essai 2 génération structurée sur '%s' (%s). Déclenchement Essai 3 de secours sur '%s'...",
                effective_model,
                exc2,
                settings.MODEL_FAST_VISION,
            )

        # Essai 3 (Fallback legacy uniquement) : Repli sur le modèle rapide (12b) avec déchargement VRAM préalable
        if self.currently_loaded_model:
            self.unload_model(self.currently_loaded_model)
        fallback_model = settings.MODEL_FAST_VISION
        return _execute_ollama_call(
            fallback_model,
            truncated_prompt,
            temp=0.2,
            pred=4096,
            thinking=False,
        )

    # ==========================================================================
    # EMBEDDINGS VECTORIELS (BGE-M3)
    # ==========================================================================

    def generate_embeddings(
        self,
        text: str,
        model: Optional[str] = None,
        keep_alive: Union[int, str] = 0,
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
            self.currently_loaded_model = target_model if (keep_alive != 0 and keep_alive != "0") else None
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
