"""ont visualize — export graph to standalone HTML viewer."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Export ontology graph to a standalone HTML viewer (no server needed).")
console = Console()


@app.callback(invoke_without_command=True)
def visualize(
    config: Path = typer.Option(None, "--config", "-c", help="Path to .ontology.toml"),
    graph: Path = typer.Option(None, "--graph", "-g", help="Graph file to visualise."),
    open_browser: bool = typer.Option(False, "--open", "-o", help="Open in browser after export."),
    events: bool = typer.Option(False, "--events", "-e", help="Include event nodes."),
) -> None:
    from cli.config import load_config, project_root
    cfg = load_config(config)
    root = project_root(cfg, config)
    sys.path.insert(0, str(root))

    try:
        from pipeline.visualize import main as run_visualize
    except ImportError as exc:
        console.print(f"[red]Cannot import pipeline.visualize from {root}: {exc}[/red]")
        raise typer.Exit(1)

    graph_dir = root / cfg.get("project", {}).get("graph_dir", "logs/graphs")
    graph_file = str(graph) if graph else str(graph_dir / "executed.trig")

    prev = os.getcwd()
    os.chdir(root)
    try:
        run_visualize(
            graph_path=graph_file,
            open_browser=open_browser,
            include_events=events,
        )
    except SystemExit as e:
        if e.code:
            raise typer.Exit(int(e.code))
    finally:
        os.chdir(prev)
