"""Tests for HUMEAN engine orchestration."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest

from modules.humean_core.config import HumeanConfig, load_config
from modules.humean_core.cognitive_orchestrator import CognitiveOrchestrator
from modules.humean_core.engines.base import CognitiveEngine, EngineResponse
from modules.humean_core.engines.factory import EngineFactory


class DummyEngine(CognitiveEngine):
    """Minimal engine for tests."""

    def __init__(self, *, response: str = "ok", fail: bool = False):
        self.response = response
        self.fail = fail

    async def process(self, prompt, context=None, temperature=0.7, max_tokens=None):
        if self.fail:
            raise RuntimeError("dummy failure")
        return EngineResponse(content=self.response, engine="dummy", confidence=0.9)

    def health_check(self):
        return not self.fail


def test_load_legacy_config_compatibility():
    """Legacy JSON structure should still load correctly."""
    legacy_payload = {
        "version": "1.0",
        "system": {
            "name": "Legacy System",
            "mode": "test",
            "auto_update": False,
        },
        "cognitive_engine": {
            "primary": "ollama",
            "fallbacks": ["gemini"],
            "energy_threshold": 0.8,
            "max_context_memories": 7,
        },
    }

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(legacy_payload, handle)
        temp_path = Path(handle.name)

    try:
        config = load_config(temp_path)
        assert config.name == "Legacy System"
        assert config.mode == "test"
        assert config.auto_update is False
        assert config.cognitive_engine.primary == "ollama"
        assert config.cognitive_engine.energy_threshold == 0.8
    finally:
        os.unlink(temp_path)


def test_environment_variables_override_config():
    """Environment variables should override JSON values when set."""
    os.environ["OPENAI_API_KEY"] = "openai-test-key"
    os.environ["HUMEAN_MODE"] = "production"

    try:
        config = load_config()
        assert config.apis.openai == "openai-test-key"
        assert config.mode == "production"
    finally:
        os.environ.pop("OPENAI_API_KEY", None)
        os.environ.pop("HUMEAN_MODE", None)


def test_humean_config_validates_thresholds():
    """Energy threshold must remain between 0 and 1."""
    with pytest.raises(ValueError):
        HumeanConfig(cognitive_engine={"primary": "gemini", "energy_threshold": 2.0})


def test_factory_registers_custom_engine():
    """Custom engines should be accepted via the factory."""
    EngineFactory.register("dummy", DummyEngine)
    engine = EngineFactory.create("dummy")
    assert isinstance(engine, DummyEngine)


@pytest.mark.asyncio
async def test_orchestrator_falls_back_when_primary_fails():
    """The orchestrator should keep trying providers after a failure."""
    class WorkingEngine(DummyEngine):
        def __init__(self):
            super().__init__(response="fallback works")

    EngineFactory.register("dummy-success", WorkingEngine)
    EngineFactory.register("dummy-fail", lambda: DummyEngine(fail=True))

    orchestrator = CognitiveOrchestrator(
        [
            {"type": "dummy-fail"},
            {"type": "dummy-success"},
        ],
        request_timeout=2.0,
    )

    response = await orchestrator.process("hello")
    assert response.content == "fallback works"


@pytest.mark.asyncio
async def test_orchestrator_raises_when_all_engines_fail():
    """The orchestrator should surface a clear error if all engines fail."""
    EngineFactory.register("dummy-always-fail", lambda: DummyEngine(fail=True))
    orchestrator = CognitiveOrchestrator(
        [
            {"type": "dummy-always-fail"},
            {"type": "dummy-always-fail"},
        ],
        request_timeout=2.0,
    )

    with pytest.raises(RuntimeError, match="All cognitive engines failed"):
        await orchestrator.process("hello")
