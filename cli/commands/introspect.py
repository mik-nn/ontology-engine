"""ont introspect — scan project and build introspection graph."""
from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Scan the project and emit an introspection graph.")
console = Console()


@app.callback(invoke_without_command=True)
def introspect(
    config: Path = typer.Option(None, "--config", "-c", help="Path to .ontology.toml"),
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q"),
) -> None:
    from cli.config import load_config, project_root
    cfg = load_config(config)
    root = project_root(cfg, config)

    sys.path.insert(0, str(root))

    try:
        from pipeline.introspect import main as run_introspect
    except ImportError as exc:
        console.print(f"[red]Cannot import pipeline.introspect from {root}: {exc}[/red]")
        raise typer.Exit(1)

    console.print(f"[bold cyan]Introspecting:[/bold cyan] {root}")

    import os
    prev = os.getcwd()
    os.chdir(root)
    try:
        run_introspect(project_root=str(root))
    except SystemExit as e:
        if e.code:
            raise typer.Exit(int(e.code))
    finally:
        os.chdir(prev)

    console.print(f"[green]Done.[/green] Graph → {root}/logs/graphs/introspection.trig")
