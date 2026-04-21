"""ont run — execute the full pipeline for a request."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Run the full pipeline for a natural-language request.")
console = Console()


@app.callback(invoke_without_command=True)
def run(
    request: str = typer.Argument(..., help="Natural-language change request."),
    config: Path = typer.Option(None, "--config", "-c", help="Path to .ontology.toml"),
    auto: bool = typer.Option(False, "--auto", "-a", help="Non-interactive mode."),
    commit: bool = typer.Option(False, "--commit", help="Commit results to git."),
    push: bool = typer.Option(False, "--push", help="Push after commit."),
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q"),
) -> None:
    from cli.config import load_config, project_root
    cfg = load_config(config)
    root = project_root(cfg, config)

    sys.path.insert(0, str(root))

    try:
        from pipeline.pipeline_orchestrator import PipelineOrchestrator
    except ImportError as exc:
        console.print(f"[red]Cannot import pipeline from {root}: {exc}[/red]")
        raise typer.Exit(1)

    console.print(f"[bold cyan]Project:[/bold cyan] {root}")
    console.print(f"[bold cyan]Request:[/bold cyan] {request}\n")

    pipeline_cfg = cfg.get("pipeline", {})
    effective_auto   = auto   or pipeline_cfg.get("auto",   False)
    effective_commit = commit or pipeline_cfg.get("commit", False)
    effective_push   = push   or pipeline_cfg.get("push",   False)

    prev = os.getcwd()
    os.chdir(root)
    try:
        orchestrator = PipelineOrchestrator(auto=effective_auto, commit=effective_commit, push=effective_push, verbose=verbose)
        result = orchestrator.run(request)
    except SystemExit as e:
        if e.code:
            raise typer.Exit(int(e.code))
    finally:
        os.chdir(prev)

    if result.failed:
        console.print(f"\n[bold red]FAILED[/bold red]: {'; '.join(result.errors)}")
        raise typer.Exit(1)

    console.print("\n[bold green]COMPLETED[/bold green]")
