"""ont ai-todo — list all AI-Todos detected in the project graph."""
from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="List all stub/incomplete implementations detected by StubDetector.")
console = Console()

_SPARQL = """
PREFIX oe: <https://ontologist.ai/ns/oe/>
SELECT ?file ?line ?fn ?stubType ?desc ?priority ?status WHERE {
    GRAPH ?g {
        ?todo a oe:AITodo ;
              oe:filePath   ?file ;
              oe:lineNumber ?line ;
              oe:stubType   ?stubType ;
              oe:description ?desc ;
              oe:priority   ?priority ;
              oe:status     ?status .
        OPTIONAL { ?todo oe:functionName ?fn }
    }
} ORDER BY ?priority ?file ?line
"""

_PRIORITY_COLOR = {"high": "red", "medium": "yellow", "low": "dim"}


@app.callback(invoke_without_command=True)
def ai_todo(
    config: Path = typer.Option(None, "--config", "-c", help="Path to .ontology.toml"),
    graph: Path = typer.Option(None, "--graph", "-g", help="Graph file to query."),
    priority: str = typer.Option(None, "--priority", "-p", help="Filter: high|medium|low"),
    open_only: bool = typer.Option(True, "--open/--all", help="Show only open todos (default: open)."),
) -> None:
    from cli.config import load_config, project_root
    cfg = load_config(config)
    root = project_root(cfg, config)
    sys.path.insert(0, str(root))

    try:
        from rdflib import ConjunctiveGraph
    except ImportError:
        console.print("[red]rdflib not available.[/red]")
        raise typer.Exit(1)

    graph_dir = root / cfg.get("project", {}).get("graph_dir", "logs/graphs")
    graph_file = graph or graph_dir / "introspection.trig"

    if not graph_file.exists():
        console.print(f"[yellow]Graph not found: {graph_file}. Run `ont introspect` first.[/yellow]")
        raise typer.Exit(1)

    g = ConjunctiveGraph()
    g.parse(str(graph_file), format="trig")

    rows = list(g.query(_SPARQL))

    if not rows:
        console.print("[green]No AI-Todos found. All stubs are resolved![/green]")
        return

    # Filter
    if priority:
        rows = [r for r in rows if str(r.priority) == priority]
    if open_only:
        rows = [r for r in rows if str(r.status) == "open"]

    table = Table(
        title=f"AI-Todos — {len(rows)} found",
        show_lines=False,
    )
    table.add_column("P",       width=1,  no_wrap=True)
    table.add_column("File",    style="cyan", no_wrap=True)
    table.add_column("L",       width=5,  style="dim")
    table.add_column("Type",    width=14)
    table.add_column("Description")

    for row in rows:
        prio  = str(row.priority)
        color = _PRIORITY_COLOR.get(prio, "white")
        fn    = f" [{row.fn}]" if row.fn else ""
        table.add_row(
            f"[{color}]{prio[0].upper()}[/{color}]",
            str(row.file),
            str(row.line),
            str(row.stubType).replace("_", " "),
            str(row.desc)[:80] + fn,
        )

    console.print(table)
    console.print(
        f"\n[dim]Run `ont run \"implement <function>\"` to let the pipeline fix a specific stub.[/dim]"
    )
