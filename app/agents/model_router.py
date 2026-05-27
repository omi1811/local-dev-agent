import logging

import requests

from app.core.config import settings

logger = logging.getLogger(__name__)


class ModelRouter:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self.current_models = None

    def _call_ollama(self, model: str, prompt: str, temperature: float) -> str:
        """Send a request to Ollama and return the generated text."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
            "option": {"num_ctx": 4096},
        }
        try:
            logger.info("Calling Ollama API for model '%s' with prompt length %s", model, len(prompt))
            response = requests.post(url, json=payload, timeout=180)
            response.raise_for_status()
            return response.json()["response"].strip()
        except requests.RequestException as e:
            logger.error("Error calling Ollama API: %s", e)
            raise RuntimeError(f"Failed to call Ollama API: {e}")

    def run_maker(self, system_prompt: str, user_prompt: str) -> str:
        """Run the maker model to generate code."""
        full_prompt = f"{system_prompt}\nUSER REQUEST:\n{user_prompt}"
        return self._call_ollama(settings.CODER_MODEL, full_prompt, settings.TEMPERATURE_CODER)

    def run_planner(self, system_prompt: str, user_prompt: str) -> str:
        """Reviewer model: critiques code."""
        full_prompt = f"{system_prompt}\nCODE TO REVIEW:\n{user_prompt}"
        return self._call_ollama(settings.PLANNER_MODEL, full_prompt, settings.TEMPERATURE_PLANNER)
import logging

import requests

from app.core.config import settings

logger = logging.getLogger(__name__)


class ModelRouter:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self.current_models = None

    def _call_ollama(self, model: str, prompt: str, temperature: float) -> str:
        """Send a request to Ollama and return the generated text."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
            "option": {"num_ctx": 4096},
        }
        try:
            logger.info("Calling Ollama API for model '%s' with prompt length %s", model, len(prompt))
            response = requests.post(url, json=payload, timeout=180)
            response.raise_for_status()
            return response.json()["response"].strip()
        except requests.RequestException as e:
            logger.error("Error calling Ollama API: %s", e)
            raise RuntimeError(f"Failed to call Ollama API: {e}")

    def run_maker(self, system_prompt: str, user_prompt: str) -> str:
        """Run the maker model to generate code."""
        full_prompt = f"{system_prompt}\nUSER REQUEST:\n{user_prompt}"
        return self._call_ollama(settings.CODER_MODEL, full_prompt, settings.TEMPERATURE_CODER)

    def run_planner(self, system_prompt: str, user_prompt: str) -> str:
        """Reviewer model: critiques code."""
        full_prompt = f"{system_prompt}\nCODE TO REVIEW:\n{user_prompt}"
        return self._call_ollama(settings.PLANNER_MODEL, full_prompt, settings.TEMPERATURE_PLANNER)
import requests
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class ModelRouter:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self.current_models = None

    def _call_ollama(self, model: str, prompt: str, temperature: float) -> str:
        """Send a request to the Ollama to generate a response from the specified model, return text."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
            "option": {"num_ctx": 4096}
        }
        try:
            logger.info(f"Calling Ollama API for model '{model}' with prompt length {len(prompt)}")
            response = requests.post(url, json=payload, timeout=180)
            response.raise_for_status()
            return response.json()["response"].strip()
        except requests.RequestException as e:
            logger.error(f"Error calling Ollama API: {e}")
            raise RuntimeError(f"Failed to call Ollama API: {e}")
        
    def run_maker(self, system_prompt: str, user_prompt: str) -> str:
        """Run the maker model to generate code."""
        full_prompt = f"{system_prompt}\nUSER REQUEST:\n{user_prompt}"
        return self._call_ollama(settings.CODER_MODEL, full_prompt, settings.TEMPERATURE_CODER)
    
    def run_planner(self, system_prompt: str, user_prompt: str) -> str:
        """Reviewer model: critiques code"""
        full_prompt = f"{system_prompt}\nCODE TO REVIEW:\n{user_prompt}"
        return self._call_ollama(settings.PLANNER_MODEL, full_prompt, settings.TEMPERATURE_PLANNER)
