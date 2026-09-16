"""OpenAI GPT cognitive engine."""

import os
from typing import Any, Optional

import aiohttp

from modules.humean_core.engines.base import CognitiveEngine, EngineResponse


class OpenAIEngine(CognitiveEngine):
    """OpenAI GPT-4, GPT-4o cognitive engine."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
        config: Optional[dict[str, Any]] = None,
    ):
        """Initialize OpenAI engine.

        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4o, gpt-4-turbo, gpt-4)
            config: Additional configuration
        """
        super().__init__(api_key or os.getenv("OPENAI_API_KEY"), config)
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"

    async def process(
        self,
        prompt: str,
        context: Optional[list[dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> EngineResponse:
        """Process prompt using OpenAI API."""
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        messages = []
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": self.config.get("top_p", 1.0),
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
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
                        raise Exception(f"OpenAI API error: {error_data}")

                    data = await response.json()
                    return EngineResponse(
                        content=data["choices"][0]["message"]["content"],
                        engine="openai",
                        confidence=0.95,
                        tokens_used={
                            "prompt": data.get("usage", {}).get("prompt_tokens", 0),
                            "completion": data.get("usage", {}).get("completion_tokens", 0),
                        },
                        metadata={
                            "model": self.model,
                            "finish_reason": data["choices"][0].get("finish_reason"),
                        },
                    )
        except Exception as e:
            raise RuntimeError(f"OpenAI processing failed: {str(e)}")

    def health_check(self) -> bool:
        """Check if OpenAI API is accessible."""
        return bool(self.api_key)
