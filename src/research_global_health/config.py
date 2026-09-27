from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    github_token: str | None = None
    data_dir: Path = Path("data")
    log_level: str = "INFO"
    request_timeout: float = Field(default=30.0, gt=0)
    max_concurrency: int = Field(default=8, ge=1)

    model_config = SettingsConfigDict(
        env_prefix="RG_",
        env_file=".env",
        env_file_encoding="utf-8",
    )


def get_settings() -> Settings:
    """Return application settings."""
    return Settings()
