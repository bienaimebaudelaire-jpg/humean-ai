"""Configuration management for HUMEAN system."""

import json
import os
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load .env file
load_dotenv()


class APIConfig(BaseModel):
    """API Configuration."""

    ollama: Optional[str] = Field(default=None, description="Ollama API URL")
    gemini: Optional[str] = Field(default=None, description="Gemini API key")
    huggingface: Optional[str] = Field(default=None, description="HuggingFace API key")


class CognitiveEngineConfig(BaseModel):
    """Cognitive Engine Configuration."""

    primary: str = Field(default="gemini", description="Primary cognitive engine")
    fallbacks: list[str] = Field(default=["ollama", "huggingface"], description="Fallback engines")
    energy_threshold: float = Field(default=0.5, description="Energy threshold")
    max_context_memories: int = Field(default=5, description="Max context memories")


class ModulesConfig(BaseModel):
    """Modules status configuration."""

    gateway: str = Field(default="operational")
    memory: str = Field(default="operational")
    scheduler: str = Field(default="ready")
    ethics: str = Field(default="ready")
    monitoring: str = Field(default="operational")


class HumeanConfig(BaseModel):
    """Main HUMEAN configuration."""

    version: str = Field(default="1.0")
    name: str = Field(default="HUMEAN Cognitive System")
    mode: str = Field(default="development")
    auto_update: bool = Field(default=True)
    cognitive_engine: CognitiveEngineConfig = Field(default_factory=CognitiveEngineConfig)
    apis: APIConfig = Field(default_factory=APIConfig)
    modules: ModulesConfig = Field(default_factory=ModulesConfig)


def load_config(config_path: Optional[Path] = None) -> HumeanConfig:
    """Load configuration from JSON file with environment variable overrides.

    Args:
        config_path: Path to config file. Defaults to humean_config.json in current dir.

    Returns:
        HumeanConfig instance with environment variables applied.
    """
    if config_path is None:
        config_path = Path(__file__).parent / "config" / "humean_config.json"

    # Load from JSON
    config_data = {}
    if config_path.exists():
        with open(config_path) as f:
            config_data = json.load(f)

    # Override with environment variables
    if gemini_key := os.getenv("GEMINI_API_KEY"):
        if "apis" not in config_data:
            config_data["apis"] = {}
        config_data["apis"]["gemini"] = gemini_key

    if ollama_url := os.getenv("OLLAMA_API_URL"):
        if "apis" not in config_data:
            config_data["apis"] = {}
        config_data["apis"]["ollama"] = ollama_url

    if hf_key := os.getenv("HUGGINGFACE_API_KEY"):
        if "apis" not in config_data:
            config_data["apis"] = {}
        config_data["apis"]["huggingface"] = hf_key

    if mode := os.getenv("HUMEAN_MODE"):
        config_data["mode"] = mode

    return HumeanConfig(**config_data)


# Global config instance
_config: Optional[HumeanConfig] = None


def get_config() -> HumeanConfig:
    """Get or initialize the global config instance."""
    global _config
    if _config is None:
        _config = load_config()
    return _config
