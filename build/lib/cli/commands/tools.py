"""ont tools — list all registered deterministic tools."""
from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="List deterministic tools available for direct execution.")
console = Console()


@app.callback(invoke_without_command=True)
def tools() -> None:
    """Show all registered tools that bypass the full pipeline."""
    import execution.tools.git_tools  # noqa: F401 — registers git tools
    from execution.tools.registry import get_registry

    registry = get_registry()
    tool_list = registry.list_tools()

    table = Table(title=f"Registered Tools — {len(tool_list)} found")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Description")
    table.add_column("Patterns", style="dim")

    for tool in tool_list:
        patterns = " | ".join(tool.patterns[:3])
        if len(tool.patterns) > 3:
            patterns += f" (+{len(tool.patterns) - 3} more)"
        table.add_row(tool.name, tool.description, patterns)

    console.print(table)
    console.print(
        "\n[dim]Add tools in [bold]execution/tools/[/bold] and call "
        "[bold]register(MyTool())[/bold] — they're picked up automatically.[/dim]"
    )
