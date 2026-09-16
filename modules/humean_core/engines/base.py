"""Base classes for cognitive engines."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class EngineResponse:
    """Response from cognitive engine."""

    content: str
    engine: str
    confidence: float
    tokens_used: Optional[dict[str, int]] = None
    reasoning: Optional[str] = None
    metadata: dict[str, Any] | None = None


class CognitiveEngine(ABC):
    """Base class for cognitive engines."""

    def __init__(self, api_key: Optional[str] = None, config: Optional[dict[str, Any]] = None):
        """Initialize cognitive engine.

        Args:
            api_key: API key for the engine
            config: Engine-specific configuration
        """
        self.api_key = api_key
        self.config = config or {}

    @abstractmethod
    async def process(
        self,
        prompt: str,
        context: Optional[list[dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> EngineResponse:
        """Process a prompt through the cognitive engine.

        Args:
            prompt: The input prompt
            context: Previous conversation context
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response

        Returns:
            EngineResponse with model output
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if engine is operational."""
        pass
