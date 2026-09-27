import typer

from research_global_health.config import get_settings
from research_global_health.logging_setup import setup_logging

app = typer.Typer()


@app.command()
def version() -> None:
    """Show the application version."""
    typer.echo("research-global-health 0.1.0")


@app.command("check-config")
def check_config() -> None:
    """Validate and show the application configuration."""
    settings = get_settings()
    setup_logging(settings.log_level)

    typer.echo(f"data_dir: {settings.data_dir}")
    typer.echo(f"log_level: {settings.log_level}")
    typer.echo(f"request_timeout: {settings.request_timeout}")
    typer.echo(f"max_concurrency: {settings.max_concurrency}")
    typer.echo(f"github_token_set: {settings.github_token is not None}")
