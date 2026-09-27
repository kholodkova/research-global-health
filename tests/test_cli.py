from typer.testing import CliRunner

from research_global_health.cli import app

runner = CliRunner()


def test_version_command() -> None:
    """Version command should display the application version."""
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "research-global-health 0.1.0" in result.stdout


def test_check_config_does_not_expose_token() -> None:
    """Check-config should not expose the GitHub token."""
    secret_token = "super-secret-token"

    result = runner.invoke(
        app,
        ["check-config"],
        env={"RG_GITHUB_TOKEN": secret_token},
    )

    assert result.exit_code == 0
    assert "github_token_set: True" in result.stdout
    assert secret_token not in result.stdout
