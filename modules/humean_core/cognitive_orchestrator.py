"""Cognitive orchestrator for managing multiple engines with fallbacks."""

import asyncio
import logging
from typing import Any, Optional

from modules.humean_core.engines.base import CognitiveEngine, EngineResponse
from modules.humean_core.engines.factory import EngineFactory

logger = logging.getLogger(__name__)


class CognitiveOrchestrator:
    """Orchestrates multiple cognitive engines with intelligent fallback."""

    def __init__(self, engines_config: list[dict[str, Any]]):
        """Initialize orchestrator with engine configurations.

        Args:
            engines_config: List of engine configs with 'type', 'api_key', 'model', etc
        """
        self.engines: list[CognitiveEngine] = []
        self.engine_names: list[str] = []

        for config in engines_config:
            engine_type = config.pop("type")
            api_key = config.pop("api_key", None)
            model = config.pop("model", None)

            try:
                engine = EngineFactory.create(
                    engine_type=engine_type,
                    api_key=api_key,
                    model=model,
                    config=config,
                )
                self.engines.append(engine)
                self.engine_names.append(engine_type)
                logger.info(f"Initialized {engine_type} engine")
            except Exception as e:
                logger.warning(f"Failed to initialize {engine_type}: {e}")

    async def process(
        self,
        prompt: str,
        context: Optional[list[dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> EngineResponse:
        """Process prompt through engines with fallback.

        Args:
            prompt: Input prompt
            context: Conversation context
            temperature: Sampling temperature
            max_tokens: Max tokens in response

        Returns:
            EngineResponse from first successful engine

        Raises:
            RuntimeError: If all engines fail
        """
        errors = []

        for engine, engine_name in zip(self.engines, self.engine_names):
            try:
                logger.debug(f"Trying {engine_name} engine")
                if not engine.health_check():
                    logger.warning(f"{engine_name} health check failed")
                    continue

                response = await engine.process(
                    prompt=prompt,
                    context=context,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                logger.info(f"Successfully processed with {engine_name}")
                return response

            except Exception as e:
                error_msg = f"{engine_name}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"Engine {engine_name} failed: {e}")
                continue

        error_summary = "; ".join(errors)
        raise RuntimeError(
            f"All cognitive engines failed: {error_summary}"
        )
