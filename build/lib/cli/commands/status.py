"""ont status — show pipeline events from logs/events/ (SPARQL, not Python vars)."""
from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Show pipeline events by querying the event log graphs.")
console = Console()

# Namespace matches event_logger.py: OE = https://ontologist.ai/ns/oe/
_SPARQL = """
PREFIX oe:   <https://ontologist.ai/ns/oe/>
PREFIX prov: <http://www.w3.org/ns/prov#>

SELECT ?type ?agent ?status ?state ?ts WHERE {
    GRAPH ?g {
        ?event a ?type ;
               oe:hasAgent  ?agent ;
               oe:hasStatus ?status ;
               prov:startedAtTime ?ts .
        OPTIONAL { ?event oe:pipelineState ?state }
    }
} ORDER BY DESC(?ts) LIMIT 20
"""


@app.callback(invoke_without_command=True)
def status(
    config: Path = typer.Option(None, "--config", "-c", help="Path to .ontology.toml"),
    graph: Path = typer.Option(None, "--graph", "-g", help="Specific graph file to query."),
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

    g = ConjunctiveGraph()

    if graph:
        sources = [graph]
    else:
        # events are in logs/events/YYYY-MM-DD.trig (written by EventLogger)
        events_dir = root / "logs" / "events"
        graph_dir  = root / cfg.get("project", {}).get("graph_dir", "logs/graphs")
        sources = sorted(events_dir.glob("*.trig")) if events_dir.exists() else []
        # also include stage graphs as fallback
        for name in ("planned.trig", "verified.trig", "introspection.trig"):
            p = graph_dir / name
            if p.exists():
                sources.append(p)

    loaded = []
    for src in sources:
        if src and src.exists():
            g.parse(str(src), format="trig")
            loaded.append(src.name)

    if not loaded:
        console.print("[yellow]No graph files found. Run `ont introspect` first.[/yellow]")
        raise typer.Exit()

    console.print(f"[dim]Sources: {', '.join(loaded)}[/dim]")

    results = list(g.query(_SPARQL))

    if not results:
        console.print("[yellow]No pipeline events found in loaded graphs.[/yellow]")
        return

    table = Table(title="Pipeline Events")
    table.add_column("Type",   style="cyan")
    table.add_column("Agent",  style="white")
    table.add_column("Status", style="green")
    table.add_column("State")
    table.add_column("Timestamp")

    for row in results:
        ev_type = str(row.type).split("/")[-1]
        agent   = str(row.agent)
        st      = str(row.status)
        state   = str(row.state).split("/")[-1] if row.state else "—"
        ts      = str(row.ts)[:19]
        color   = "green" if st == "completed" else "red" if st == "failed" else "yellow"
        table.add_row(ev_type, agent, f"[{color}]{st}[/{color}]", state, ts)

    console.print(table)
