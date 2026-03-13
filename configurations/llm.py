"""
Singleton configuration loader for LLM providers.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from dtos.configurations.llm import LLMConfigurationDTO


def _env_bool(name: str, default: Optional[bool] = None) -> Optional[bool]:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class LLMConfiguration:
    """
    Lazily loads LLM configuration from ``config/llm/config.json``, then
    applies environment variable overrides for secrets and toggles.
    """

    _instance: Optional["LLMConfiguration"] = None

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent.parent
        config_path = base_path / "config" / "llm" / "config.json"
        raw: dict = {}
        if config_path.exists():
            raw = json.loads(config_path.read_text())

        # Apply environment overrides (no secrets in JSON)
        # OpenAI
        openai_cfg = raw.setdefault("openai", {})
        if (v := os.getenv("OPENAI_API_KEY")) is not None:
            openai_cfg["api_key"] = v
        if (v := os.getenv("OPENAI_BASE_URL")) is not None:
            openai_cfg["base_url"] = v
        if (v := os.getenv("OPENAI_MODEL")) is not None:
            openai_cfg["model"] = v
        if (v := _env_bool("OPENAI_ENABLED")) is not None:
            openai_cfg["enabled"] = v

        # Anthropic
        anthropic_cfg = raw.setdefault("anthropic", {})
        if (v := os.getenv("ANTHROPIC_API_KEY")) is not None:
            anthropic_cfg["api_key"] = v
        if (v := os.getenv("ANTHROPIC_BASE_URL")) is not None:
            anthropic_cfg["base_url"] = v
        if (v := os.getenv("ANTHROPIC_MODEL")) is not None:
            anthropic_cfg["model"] = v
        if (v := _env_bool("ANTHROPIC_ENABLED")) is not None:
            anthropic_cfg["enabled"] = v

        # Ollama
        ollama_cfg = raw.setdefault("ollama", {})
        if (v := os.getenv("OLLAMA_BASE_URL")) is not None:
            ollama_cfg["base_url"] = v
        if (v := os.getenv("OLLAMA_MODEL")) is not None:
            ollama_cfg["model"] = v
        if (v := _env_bool("OLLAMA_ENABLED")) is not None:
            ollama_cfg["enabled"] = v

        # Gemini
        gemini_cfg = raw.setdefault("gemini", {})
        if (v := os.getenv("GEMINI_API_KEY")) is not None:
            gemini_cfg["api_key"] = v
        if (v := os.getenv("GEMINI_MODEL")) is not None:
            gemini_cfg["model"] = v
        if (v := _env_bool("GEMINI_ENABLED")) is not None:
            gemini_cfg["enabled"] = v

        self._config = LLMConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "LLMConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> LLMConfigurationDTO:
        return self._config


__all__ = [
    "LLMConfiguration",
]

