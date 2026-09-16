"""Anthropic Claude cognitive engine."""

import os
from typing import Any, Optional

import aiohttp

from modules.humean_core.engines.base import CognitiveEngine, EngineResponse


class AnthropicEngine(CognitiveEngine):
    """Anthropic Claude cognitive engine (Claude 3+)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-opus-20240229",
        config: Optional[dict[str, Any]] = None,
    ):
        """Initialize Anthropic engine.

        Args:
            api_key: Anthropic API key
            model: Model to use (claude-3-opus, claude-3-sonnet, claude-3-haiku)
            config: Additional configuration
        """
        super().__init__(api_key or os.getenv("ANTHROPIC_API_KEY"), config)
        self.model = model
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.api_version = "2024-06-01"

    async def process(
        self,
        prompt: str,
        context: Optional[list[dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> EngineResponse:
        """Process prompt using Anthropic API."""
        if not self.api_key:
            raise ValueError("Anthropic API key not configured")

        messages = []
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "max_tokens": max_tokens or 4096,
            "messages": messages,
            "temperature": temperature,
        }

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.api_version,
            "content-type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    if response.status != 200:
                        error_data = await response.json()
                        raise Exception(f"Anthropic API error: {error_data}")

                    data = await response.json()
                    return EngineResponse(
                        content=data["content"][0]["text"],
                        engine="anthropic",
                        confidence=0.95,
                        tokens_used={
                            "input": data.get("usage", {}).get("input_tokens", 0),
                            "output": data.get("usage", {}).get("output_tokens", 0),
                        },
                        metadata={
                            "model": self.model,
                            "stop_reason": data.get("stop_reason"),
                        },
                    )
        except Exception as e:
            raise RuntimeError(f"Anthropic processing failed: {str(e)}")

    def health_check(self) -> bool:
        """Check if Anthropic API is accessible."""
        return bool(self.api_key)
