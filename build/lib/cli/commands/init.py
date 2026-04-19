"""ont init — initialise a new project with .ontology.toml."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Prompt

app = typer.Typer(help="Initialise a project directory for the ontology engine.")
console = Console()

_TEMPLATE = """\
[project]
name = "{name}"
graph_dir = "logs/graphs"
shacl_shapes = [
    "core/shacl/databook_shapes.ttl",
    "core/shacl/dependencies_shapes.ttl",
    "core/shacl/planning_shapes.ttl",
]

[pipeline]
auto   = false
commit = false
push   = false

[llm]
provider = "claude-code"
model    = "claude-sonnet-4-6"
# provider = "ollama"
# model    = "llama3.2"
# base_url = "http://localhost:11434"
"""

_GITIGNORE_ENTRIES = ["logs/", ".ontology.toml.local"]


@app.callback(invoke_without_command=True)
def init(
    path: Path = typer.Argument(Path("."), help="Project directory (default: current)."),
    name: str = typer.Option(None, "--name", "-n", help="Project name (default: directory name)."),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing .ontology.toml."),
) -> None:
    target = path.resolve()
    config_file = target / ".ontology.toml"

    if config_file.exists() and not force:
        console.print(f"[yellow].ontology.toml already exists in {target}. Use --force to overwrite.[/yellow]")
        raise typer.Exit()

    project_name = name or (Prompt.ask("Project name", default=target.name))

    config_file.write_text(_TEMPLATE.format(name=project_name))
    console.print(f"[green]Created:[/green] {config_file}")

    # suggest log dirs
    for d in ["logs/graphs", "core/shacl"]:
        (target / d).mkdir(parents=True, exist_ok=True)
    console.print(f"[green]Created:[/green] logs/graphs/, core/shacl/")

    # append to .gitignore if present
    gitignore = target / ".gitignore"
    if gitignore.exists():
        existing = gitignore.read_text()
        additions = [e for e in _GITIGNORE_ENTRIES if e not in existing]
        if additions:
            with gitignore.open("a") as f:
                f.write("\n# ontology-engine\n")
                f.write("\n".join(additions) + "\n")
            console.print(f"[dim]Updated .gitignore[/dim]")

    console.print(f"\n[bold]Next:[/bold] cd {target} && ont run \"your request\"")
