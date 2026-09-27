import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolated_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Isolate tests from local environment and .env files."""
    for key in list(os.environ):
        if key.startswith("RG_"):
            monkeypatch.delenv(key, raising=False)

    monkeypatch.chdir(tmp_path)
