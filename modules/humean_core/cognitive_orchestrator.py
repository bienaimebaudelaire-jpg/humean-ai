"""Cognitive orchestrator for managing multiple engines with fallbacks."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from modules.humean_core.engines.base import CognitiveEngine, EngineResponse
from modules.humean_core.engines.factory import EngineFactory

logger = logging.getLogger(__name__)


class CognitiveOrchestrator:
    """Try configured engines in order without mutating caller configuration."""

    def __init__(self, engines_config: list[dict[str, Any]], request_timeout: float = 120.0):
        self.engines: list[CognitiveEngine] = []
        self.engine_names: list[str] = []
        self.request_timeout = request_timeout

        for original_config in engines_config:
            config = dict(original_config)
            engine_type = config.pop("type", None)
            if not engine_type:
                logger.warning("Skipping engine configuration without a type")
                continue
            api_key = config.pop("api_key", None)
            model = config.pop("model", None)
            try:
                engine = EngineFactory.create(engine_type, api_key, model, config)
                self.engines.append(engine)
                self.engine_names.append(engine_type)
                logger.info("Initialized %s engine", engine_type)
            except (TypeError, ValueError) as error:
                logger.warning("Failed to initialize %s: %s", engine_type, error)

    async def process(
        self,
        prompt: str,
        context: list[dict[str, str]] | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> EngineResponse:
        """Process a prompt with timeout-protected sequential fallback."""
        errors: list[str] = []
        for engine, engine_name in zip(self.engines, self.engine_names):
            try:
                if not engine.health_check():
                    errors.append(f"{engine_name}: health check failed")
                    continue
                response = await asyncio.wait_for(
                    engine.process(prompt, context, temperature, max_tokens),
                    timeout=self.request_timeout,
                )
                logger.info("Successfully processed with %s", engine_name)
                return response
            except Exception as error:  # one provider must not stop fallback
                errors.append(f"{engine_name}: {error}")
                logger.warning("Engine %s failed: %s", engine_name, error)

        raise RuntimeError(f"All cognitive engines failed: {'; '.join(errors)}")
