"""ont — ontology-engine CLI entry point."""
from __future__ import annotations

import typer
from rich.console import Console

from cli.commands import run, verify, introspect, status, init, ai_todo, visualize

app = typer.Typer(
    name="ont",
    help="Ontology-driven pipeline engine. SHACL validates, ontology orchestrates, LLM executes.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)
console = Console()

app.add_typer(run.app,        name="run")
app.add_typer(verify.app,     name="verify")
app.add_typer(introspect.app, name="introspect")
app.add_typer(status.app,     name="status")
app.add_typer(init.app,       name="init")
app.add_typer(ai_todo.app,    name="ai-todo")
app.add_typer(visualize.app,  name="visualize")


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit.", is_eager=True),
) -> None:
    if version:
        from importlib.metadata import version as pkg_version
        try:
            v = pkg_version("ontology-engine")
        except Exception:
            v = "dev"
        console.print(f"ont [bold]{v}[/bold]")
        raise typer.Exit()


if __name__ == "__main__":
    app()
