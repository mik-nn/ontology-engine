"""ont — interactive REPL dialog mode.

Entry point when `ont` is called with no arguments.

Slash commands bypass LLM parsing entirely:
  /run <request>    /verify    /introspect    /status
  /explain <topic>  /init      /visualize     /tools
  /help             /quit

Free text is parsed by IntentParser (Anthropic tool use → Pydantic Intent)
and then dispatched deterministically.

Knowledge gate: before run/verify/introspect, the graph is checked for gaps.
If any are found the user is interviewed before the operation proceeds.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from interaction.intents import Intent

console = Console()

_SLASH_HELP = """\
[bold cyan]/run[/bold cyan] [dim]<request>[/dim]   execute pipeline
[bold cyan]/verify[/bold cyan]           validate graph via SHACL
[bold cyan]/introspect[/bold cyan]       rebuild introspection graph
[bold cyan]/status[/bold cyan]           show recent events
[bold cyan]/explain[/bold cyan] [dim]<topic>[/dim]  explain a concept or decision chain
[bold cyan]/init[/bold cyan]             initialise project
[bold cyan]/visualize[/bold cyan]        open graph viewer
[bold cyan]/tools[/bold cyan]            manage LLM adapters
[bold cyan]/help[/bold cyan]             show this message
[bold cyan]/quit[/bold cyan]             exit

Or type freely — natural language is parsed automatically."""


# ─────────────────────────────────────────────────────────
# Public entry point
# ─────────────────────────────────────────────────────────

def start(config_path: Optional[Path] = None) -> None:
    """Launch the REPL. Called from cli/main.py when ont runs with no args."""
    from cli.config import load_config, project_root

    cfg = load_config(config_path)
    root = project_root(cfg, config_path)
    sys.path.insert(0, str(root))

    repl = _Repl(cfg=cfg, root=root)
    repl.run()


# ─────────────────────────────────────────────────────────
# Internal REPL class
# ─────────────────────────────────────────────────────────

class _Repl:
    def __init__(self, cfg: dict, root: Path) -> None:
        self._cfg = cfg
        self._root = root
        self._parser = self._init_parser()

    # ── lifecycle ──────────────────────────────────────────

    def _init_parser(self):
        try:
            from interaction.intent_parser import IntentParser
            parser = IntentParser()
            console.print(f"[dim]LLM backend: {parser.backend_name}[/dim]")
            return parser
        except RuntimeError as exc:
            console.print(f"[yellow]⚠  {exc}[/yellow]")
            console.print("[dim]Free-text parsing disabled — use /commands.[/dim]")
            return None

    def run(self) -> None:
        console.print(Panel(
            _SLASH_HELP,
            title="[bold]ont — ontology engine[/bold]",
            subtitle=f"[dim]{self._root}[/dim]",
            border_style="cyan",
        ))

        while True:
            try:
                line = input("\n[ont]> ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[dim]Bye.[/dim]")
                break

            if not line:
                continue

            if line.lower() in ("quit", "exit", "q"):
                console.print("[dim]Bye.[/dim]")
                break

            if line.startswith("/"):
                self._dispatch_slash(line)
            else:
                self._dispatch_free(line)

    # ── routing ────────────────────────────────────────────

    def _dispatch_slash(self, line: str) -> None:
        parts = line[1:].split(None, 1)
        cmd = parts[0].lower()
        rest = parts[1].strip() if len(parts) > 1 else ""

        routes = {
            "run":        lambda: self._do_run(rest or None),
            "verify":     lambda: self._do_verify(None),
            "introspect": lambda: self._do_introspect(),
            "status":     lambda: self._do_status(),
            "explain":    lambda: self._do_explain(rest or None),
            "init":       lambda: self._do_init(),
            "visualize":  lambda: self._do_visualize(),
            "tools":      lambda: self._do_tools(),
            "help":       lambda: self._do_help(),
            "quit":       lambda: sys.exit(0),
        }
        handler = routes.get(cmd)
        if handler:
            handler()
        else:
            console.print(f"[red]Unknown command: /{cmd}[/red]  — type /help")

    def _dispatch_free(self, text: str) -> None:
        if not self._parser:
            console.print(
                "[yellow]Free-text parsing requires ANTHROPIC_API_KEY.[/yellow] "
                "Use /commands or export the key."
            )
            return

        console.print("[dim]parsing…[/dim]", end="\r")
        intent = self._parser.parse(text)

        # 1. Knowledge gap: LLM says it needs clarification
        if intent.needs_clarification:
            q = intent.clarification_question or "Could you be more specific?"
            console.print(f"[cyan]?[/cyan]  {q}")
            return

        # 2. Dangerous action: ask before proceeding
        if intent.is_dangerous:
            from interaction.confirmation import confirm
            if not confirm(intent.danger_description or "This action may be destructive."):
                return

        # 3. Knowledge gate: check graph for gaps before mutating operations
        if intent.type in ("run", "verify", "introspect"):
            self._knowledge_gate()

        # 4. Dispatch
        dispatch = {
            "run":        lambda: self._do_run(intent.request),
            "verify":     lambda: self._do_verify(intent.target),
            "introspect": lambda: self._do_introspect(),
            "status":     lambda: self._do_status(),
            "explain":    lambda: self._do_explain(intent.concept),
            "init":       lambda: self._do_init(),
            "visualize":  lambda: self._do_visualize(),
            "tools":      lambda: self._do_tools(),
            "help":       lambda: self._do_help(),
            "quit":       lambda: sys.exit(0),
            "unknown":    lambda: console.print(
                f"[yellow]I couldn't map that to a command.[/yellow] "
                f"Try rephrasing or use /help."
            ),
        }
        fn = dispatch.get(intent.type, dispatch["unknown"])
        fn()

    # ── knowledge gate ─────────────────────────────────────

    def _knowledge_gate(self) -> None:
        """Check for graph knowledge gaps and interview the user if any exist."""
        try:
            from storage.graph_store import GraphStore
            from interaction.interviewer import Interviewer

            store = GraphStore.load(self._root, self._cfg)
            interviewer = Interviewer(store)
            gaps = interviewer._detect_gaps()
            if not gaps:
                return
            console.print(
                f"\n[yellow]⚑  {len(gaps)} knowledge gap(s) detected.[/yellow] "
                "Answering them before proceeding…"
            )
            interviewer.run()
        except Exception:
            pass  # never block an operation because the gate itself failed

    # ── command handlers ───────────────────────────────────

    def _do_run(self, request: Optional[str]) -> None:
        if not request:
            try:
                request = input("  Request: ").strip()
            except (EOFError, KeyboardInterrupt):
                return
            if not request:
                return

        console.print(f"[bold cyan]Request:[/bold cyan] {request}\n")
        prev = os.getcwd()
        os.chdir(self._root)
        try:
            from pipeline.pipeline_orchestrator import PipelineOrchestrator
            result = PipelineOrchestrator(
                auto=False, commit=False, push=False, verbose=True
            ).run(request)
            if result.failed:
                console.print(
                    f"\n[bold red]FAILED[/bold red]: {'; '.join(result.errors)}"
                )
            else:
                console.print("\n[bold green]COMPLETED[/bold green]")
        except ImportError as exc:
            console.print(f"[red]Import error: {exc}[/red]")
        except SystemExit:
            pass
        finally:
            os.chdir(prev)

    def _do_verify(self, target: Optional[str]) -> None:
        graph_dir = self._root / self._cfg.get("project", {}).get("graph_dir", "logs/graphs")
        graph_file = Path(target) if target else graph_dir / "introspection.trig"

        if not graph_file.exists():
            console.print(
                f"[yellow]Graph not found: {graph_file}. Run /introspect first.[/yellow]"
            )
            return

        console.print(f"[bold cyan]Verifying:[/bold cyan] {graph_file}")
        prev = os.getcwd()
        os.chdir(self._root)
        try:
            from pipeline.verify import main as run_verify
            run_verify(interactive=True, graph_path=str(graph_file))
        except ImportError as exc:
            console.print(f"[red]Import error: {exc}[/red]")
        except SystemExit:
            pass
        finally:
            os.chdir(prev)

    def _do_introspect(self) -> None:
        prev = os.getcwd()
        os.chdir(self._root)
        try:
            from pipeline.introspect import main as run_introspect
            run_introspect()
        except ImportError as exc:
            console.print(f"[red]Import error: {exc}[/red]")
        except SystemExit:
            pass
        finally:
            os.chdir(prev)

    def _do_status(self) -> None:
        from rdflib import ConjunctiveGraph

        g = ConjunctiveGraph()
        events_dir = self._root / "logs" / "events"
        graph_dir = self._root / self._cfg.get("project", {}).get("graph_dir", "logs/graphs")

        sources = sorted(events_dir.glob("*.trig")) if events_dir.exists() else []
        for name in ("planned.trig", "verified.trig", "introspection.trig"):
            p = graph_dir / name
            if p.exists():
                sources.append(p)

        loaded = []
        for src in sources:
            g.parse(str(src), format="trig")
            loaded.append(src.name)

        if not loaded:
            console.print("[yellow]No graph files found. Run /introspect first.[/yellow]")
            return

        console.print(f"[dim]Sources: {', '.join(loaded)}[/dim]")

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
        results = list(g.query(_SPARQL))
        if not results:
            console.print("[yellow]No pipeline events found.[/yellow]")
            return

        table = Table(title="Pipeline Events")
        table.add_column("Type",      style="cyan")
        table.add_column("Agent",     style="white")
        table.add_column("Status",    style="green")
        table.add_column("State")
        table.add_column("Timestamp")
        for row in results:
            table.add_row(
                str(row.type).split("/")[-1],
                str(row.agent).split("/")[-1],
                str(row.status).split("/")[-1],
                str(row.state or ""),
                str(row.ts or ""),
            )
        console.print(table)

    def _do_explain(self, concept: Optional[str]) -> None:
        if not concept:
            try:
                concept = input("  Explain what? ").strip()
            except (EOFError, KeyboardInterrupt):
                return
            if not concept:
                return

        _explain(concept, self._root, self._cfg)

    def _do_init(self) -> None:
        prev = os.getcwd()
        os.chdir(self._root)
        try:
            from cli.commands.init import init as run_init
            import typer
            ctx = typer.Context(typer.main.get_command(typer.Typer()))
            run_init.__wrapped__(ctx) if hasattr(run_init, "__wrapped__") else None
        except Exception:
            # Fallback: invoke via typer app
            from cli.commands.init import app as init_app
            from typer.testing import CliRunner
            result = CliRunner(mix_stderr=False).invoke(init_app, [])
            if result.output:
                console.print(result.output)
        finally:
            os.chdir(prev)

    def _do_visualize(self) -> None:
        from cli.commands.visualize import app as viz_app
        from typer.testing import CliRunner
        result = CliRunner(mix_stderr=False).invoke(viz_app, [])
        if result.output:
            console.print(result.output)

    def _do_tools(self) -> None:
        from cli.commands.tools import app as tools_app
        from typer.testing import CliRunner
        result = CliRunner(mix_stderr=False).invoke(tools_app, ["--help"])
        if result.output:
            console.print(result.output)

    def _do_help(self) -> None:
        console.print(Panel(_SLASH_HELP, title="Commands", border_style="cyan"))


# ─────────────────────────────────────────────────────────
# /explain — SPARQL-backed decision chain explanation
# ─────────────────────────────────────────────────────────

_RULE_DOCS: dict[str, str] = {
    # Gap rules
    "G01": "Databook missing [bold]title[/bold] — required by db:title constraint.",
    "G02": "Databook missing [bold]transformer[/bold] — must be one of: human / llm / sparql / xslt.",
    "G03": "Databook missing [bold]version[/bold] — required for reproducibility.",
    "G04": "CodeModule missing [bold]description[/bold] — auto-resolved from docstring when possible.",
    "G05": "Plan missing [bold]planType[/bold] — must be one of: ExplainTask / AnalysisTask / DesignTask / ImplementTask / RefactorTask.",
    "G06": "Entity flagged [bold]'interview'[/bold] by VerifyCLI — requires human clarification.",
    # Verification rules
    "R01": "SHACL shape: [bold]db:TitleShape[/bold] — every Databook must have a non-empty title.",
    "R02": "SHACL shape: [bold]db:TransformerShape[/bold] — transformer value must be in the allowed set.",
    "R03": "SHACL shape: module path must be resolvable.",
    "R04": "SHACL shape: Plan must reference a valid oe:Agent.",
    "R05": "SHACL shape: Event must have prov:startedAtTime.",
    "R06": "SHACL shape: CodeModule filePath must exist on disk.",
    "R07": "SHACL shape: Databook version must follow semver pattern.",
    "R08": "SHACL shape: Plan planType must be in the allowed enum.",
}

_STAGE_DOCS: dict[str, str] = {
    "1": "Stage 1 — [bold]Introspection[/bold]: scan source code → build RDF introspection graph.",
    "2": "Stage 2 — [bold]Planning[/bold]: ontology + SHACL derive a Plan graph from the introspection graph.",
    "3": "Stage 3 — [bold]Verification[/bold]: run rule engine + SHACL shapes on the plan graph.",
    "4": "Stage 4 — [bold]Interview[/bold]: detect knowledge gaps via SPARQL, collect answers from the user.",
    "5": "Stage 5 — [bold]Enrichment[/bold]: apply user answers + inferred triples to the plan graph.",
    "6": "Stage 6 — [bold]Execution[/bold]: LLM executes each task node in topological order.",
    "7": "Stage 7 — [bold]Post-verification[/bold]: validate execution results against SHACL shapes.",
    "8": "Stage 8 — [bold]Commit[/bold]: write verified results to the graph store.",
    "9": "Stage 9 — [bold]Sync[/bold]: push events and graphs to remote storage.",
}


def _explain(concept: str, root: Path, cfg: dict) -> None:
    c = concept.strip()

    # Rule / gap IDs
    key = c.upper()
    if key in _RULE_DOCS:
        console.print(f"\n[bold cyan]{key}[/bold cyan]  {_RULE_DOCS[key]}")
        return

    # Stage numbers
    import re
    m = re.search(r"\b(\d)\b", c)
    if m and m.group(1) in _STAGE_DOCS:
        console.print(f"\n{_STAGE_DOCS[m.group(1)]}")
        return

    # SPARQL lookup — search graph for entities matching the concept
    try:
        from rdflib import ConjunctiveGraph

        g = ConjunctiveGraph()
        graph_dir = root / cfg.get("project", {}).get("graph_dir", "logs/graphs")
        for name in ("introspection.trig", "planned.trig", "verified.trig"):
            p = graph_dir / name
            if p.exists():
                g.parse(str(p), format="trig")

        # Try to find a subject whose URI contains the concept keyword
        sparql = f"""
            SELECT ?s ?p ?o WHERE {{
                ?s ?p ?o .
                FILTER(CONTAINS(LCASE(STR(?s)), LCASE("{c}")))
            }} LIMIT 20
        """
        rows = list(g.query(sparql))
        if rows:
            table = Table(title=f"Graph entries matching '{c}'")
            table.add_column("Subject",   style="cyan",  overflow="fold")
            table.add_column("Predicate", style="yellow", overflow="fold")
            table.add_column("Object",    style="white",  overflow="fold")
            for row in rows:
                table.add_row(
                    str(row.s).split("/")[-1],
                    str(row.p).split("/")[-1],
                    str(row.o)[:80],
                )
            console.print(table)
            return
    except Exception:
        pass

    console.print(
        f"[yellow]No documentation found for [bold]{c}[/bold].[/yellow]\n"
        "Try a rule ID (G01–G06, R01–R08), stage number (1–9), or an entity keyword."
    )
