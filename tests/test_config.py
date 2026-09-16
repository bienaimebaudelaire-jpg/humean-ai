"""Tests for configuration module."""

import os
import tempfile
from pathlib import Path

import pytest

from modules.humean_core.config import HumeanConfig, load_config


def test_load_default_config():
    """Test loading default configuration."""
    config = load_config()

    assert config.version == "1.0"
    assert config.name == "HUMEAN Cognitive System"
    assert config.mode == "development"
    assert config.cognitive_engine.primary == "gemini"


def test_config_with_custom_json():
    """Test loading configuration from custom JSON file."""
    config_data = {
        "version": "1.0",
        "name": "Test System",
        "mode": "test",
        "cognitive_engine": {
            "primary": "ollama",
            "fallbacks": ["gemini"],
        },
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        import json

        json.dump(config_data, f)
        temp_path = f.name

    try:
        config = load_config(Path(temp_path))
        assert config.name == "Test System"
        assert config.mode == "test"
        assert config.cognitive_engine.primary == "ollama"
    finally:
        os.unlink(temp_path)


def test_config_environment_override():
    """Test environment variable overrides."""
    os.environ["GEMINI_API_KEY"] = "test-gemini-key"
    os.environ["HUMEAN_MODE"] = "production"

    try:
        config = load_config()
        assert config.apis.gemini == "test-gemini-key"
        assert config.mode == "production"
    finally:
        os.environ.pop("GEMINI_API_KEY", None)
        os.environ.pop("HUMEAN_MODE", None)


def test_humean_config_validation():
    """Test that HumeanConfig validates properly."""
    config = HumeanConfig(
        version="1.0",
        name="Test",
        mode="test",
        cognitive_engine={"primary": "gemini"},
    )

    assert config.version == "1.0"
    assert config.cognitive_engine.primary == "gemini"
