"""Factory for creating cognitive engines."""

from typing import Any, Optional

from modules.humean_core.engines.anthropic_engine import AnthropicEngine
from modules.humean_core.engines.base import CognitiveEngine
from modules.humean_core.engines.ollama_engine import OllamaEngine
from modules.humean_core.engines.openai_engine import OpenAIEngine


class EngineFactory:
    """Factory for creating cognitive engines."""

    _engines = {
        "openai": OpenAIEngine,
        "gpt-4": OpenAIEngine,
        "gpt-4o": OpenAIEngine,
        "anthropic": AnthropicEngine,
        "claude": AnthropicEngine,
        "ollama": OllamaEngine,
        "llama": OllamaEngine,
    }

    @classmethod
    def create(
        cls,
        engine_type: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        config: Optional[dict[str, Any]] = None,
    ) -> CognitiveEngine:
        """Create a cognitive engine instance.

        Args:
            engine_type: Type of engine (openai, anthropic, ollama, etc)
            api_key: API key for the engine
            model: Model name to use
            config: Engine-specific configuration

        Returns:
            CognitiveEngine instance

        Raises:
            ValueError: If engine type is not supported
        """
        engine_type = engine_type.lower().strip()
        if engine_type not in cls._engines:
            raise ValueError(
                f"Unsupported engine type: {engine_type}. "
                f"Supported: {', '.join(cls._engines.keys())}"
            )

        engine_class = cls._engines[engine_type]

        if engine_type == "ollama" or engine_type == "llama":
            return engine_class(base_url=api_key, model=model or "llama2", config=config)
        else:
            return engine_class(api_key=api_key, model=model, config=config)

    @classmethod
    def register(cls, engine_type: str, engine_class: type[CognitiveEngine]) -> None:
        """Register a new engine type.

        Args:
            engine_type: Name of the engine type
            engine_class: Engine class (must inherit from CognitiveEngine)
        """
        if not issubclass(engine_class, CognitiveEngine):
            raise ValueError("Engine class must inherit from CognitiveEngine")
        cls._engines[engine_type.lower()] = engine_class
