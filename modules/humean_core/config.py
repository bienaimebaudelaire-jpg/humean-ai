"""Configuration management for HUMEAN system."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class APIConfig(BaseModel):
    """Credentials and endpoints loaded from environment variables."""

    ollama: str | None = None
    gemini: str | None = None
    huggingface: str | None = None
    openai: str | None = None
    anthropic: str | None = None


class CognitiveEngineConfig(BaseModel):
    """Engine routing and context constraints."""

    primary: str = "gemini"
    fallbacks: list[str] = Field(default_factory=lambda: ["ollama", "huggingface"])
    energy_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    max_context_memories: int = Field(default=5, ge=0)


class ModulesConfig(BaseModel):
    """Declared status of HUMEAN modules."""

    gateway: str = "operational"
    memory: str = "operational"
    scheduler: str = "ready"
    ethics: str = "ready"
    monitoring: str = "operational"


class HumeanConfig(BaseModel):
    """Main HUMEAN configuration."""

    version: str = "1.0"
    name: str = "HUMEAN Cognitive System"
    mode: str = "development"
    auto_update: bool = True
    cognitive_engine: CognitiveEngineConfig = Field(default_factory=CognitiveEngineConfig)
    apis: APIConfig = Field(default_factory=APIConfig)
    modules: ModulesConfig = Field(default_factory=ModulesConfig)


def _normalise_config(data: dict[str, Any]) -> dict[str, Any]:
    """Accept both the legacy nested JSON shape and the typed model shape."""
    normalised = dict(data)
    system = normalised.pop("system", None)
    if isinstance(system, dict):
        for key in ("name", "mode", "auto_update"):
            if key not in normalised and key in system:
                normalised[key] = system[key]
    return normalised


def load_config(config_path: Path | None = None) -> HumeanConfig:
    """Load JSON configuration and apply environment-variable overrides."""
    path = config_path or Path(__file__).parent / "config" / "humean_config.json"
    config_data: dict[str, Any] = {}
    if path.exists():
        with path.open(encoding="utf-8-sig") as config_file:
            config_data = _normalise_config(json.load(config_file))

    apis = dict(config_data.get("apis", {}))
    env_api_mapping = {
        "GEMINI_API_KEY": "gemini",
        "OLLAMA_API_URL": "ollama",
        "HUGGINGFACE_API_KEY": "huggingface",
        "OPENAI_API_KEY": "openai",
        "ANTHROPIC_API_KEY": "anthropic",
    }
    for environment_name, api_name in env_api_mapping.items():
        if value := os.getenv(environment_name):
            apis[api_name] = value
    config_data["apis"] = apis

    if mode := os.getenv("HUMEAN_MODE"):
        config_data["mode"] = mode
    return HumeanConfig.model_validate(config_data)


_config: HumeanConfig | None = None


def get_config() -> HumeanConfig:
    """Return the cached application configuration."""
    global _config
    if _config is None:
        _config = load_config()
    return _config
