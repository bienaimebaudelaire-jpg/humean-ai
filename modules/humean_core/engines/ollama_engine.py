"""Ollama local cognitive engine."""

import os
from typing import Any, Optional

import aiohttp

from modules.humean_core.engines.base import CognitiveEngine, EngineResponse


class OllamaEngine(CognitiveEngine):
    """Local Ollama engine (LLaMA, Mistral, Neural Chat, etc)."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: str = "llama2",
        config: Optional[dict[str, Any]] = None,
    ):
        """Initialize Ollama engine.

        Args:
            base_url: Ollama server URL (default: http://localhost:11434)
            model: Model to use (llama2, mistral, neural-chat, etc)
            config: Additional configuration
        """
        super().__init__(config=config)
        self.base_url = base_url or os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        self.model = model

    async def process(
        self,
        prompt: str,
        context: Optional[list[dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> EngineResponse:
        """Process prompt using local Ollama."""
        messages = []
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120),
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Ollama error: {response.status}")

                    data = await response.json()
                    return EngineResponse(
                        content=data["message"]["content"],
                        engine="ollama",
                        confidence=0.85,
                        metadata={
                            "model": self.model,
                            "eval_count": data.get("eval_count"),
                        },
                    )
        except Exception as e:
            raise RuntimeError(f"Ollama processing failed: {str(e)}")

    def health_check(self) -> bool:
        """Check if Ollama server is running."""
        import requests

        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False
