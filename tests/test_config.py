from pathlib import Path

import pytest
from pydantic import ValidationError

from research_global_health.config import Settings, get_settings


def test_settings_defaults() -> None:
    """Settings should have the expected default values."""
    settings = get_settings()

    assert settings.github_token is None
    assert settings.data_dir == Path("data")
    assert settings.log_level == "INFO"
    assert settings.request_timeout == 30.0
    assert settings.max_concurrency == 8


def test_settings_read_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings should read values from environment variables."""
    monkeypatch.setenv("RG_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("RG_MAX_CONCURRENCY", "16")

    settings = Settings()

    assert settings.log_level == "DEBUG"
    assert settings.max_concurrency == 16


def test_rejects_invalid_concurrency(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings should reject non-positive concurrency."""
    monkeypatch.setenv("RG_MAX_CONCURRENCY", "0")

    with pytest.raises(ValidationError):
        Settings()
