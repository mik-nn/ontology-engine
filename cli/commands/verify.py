"""ont verify — run rule engine + optional SHACL on the introspection graph."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Validate the introspection graph via rule engine and SHACL.")
console = Console()


@app.callback(invoke_without_command=True)
def verify(
    config: Path = typer.Option(None, "--config", "-c", help="Path to .ontology.toml"),
    graph: Path = typer.Option(None, "--graph", "-g", help="Graph file to validate (default: logs/graphs/introspection.trig)"),
    auto: bool = typer.Option(False, "--auto", "-a", help="Non-interactive — skip human verification prompts."),
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q"),
) -> None:
    from cli.config import load_config, project_root
    cfg = load_config(config)
    root = project_root(cfg, config)

    sys.path.insert(0, str(root))

    graph_dir = root / cfg.get("project", {}).get("graph_dir", "logs/graphs")
    graph_file = graph or graph_dir / "introspection.trig"

    if not graph_file.exists():
        console.print(f"[yellow]Graph not found: {graph_file}. Run `ont introspect` first.[/yellow]")
        raise typer.Exit(1)

    try:
        from pipeline.verify import main as run_verify
    except ImportError as exc:
        console.print(f"[red]Cannot import pipeline.verify from {root}: {exc}[/red]")
        raise typer.Exit(1)

    console.print(f"[bold cyan]Verifying:[/bold cyan] {graph_file}")

    prev = os.getcwd()
    os.chdir(root)
    try:
        run_verify(interactive=not auto, graph_path=str(graph_file))
    except SystemExit as e:
        if e.code:
            raise typer.Exit(int(e.code))
    finally:
        os.chdir(prev)
