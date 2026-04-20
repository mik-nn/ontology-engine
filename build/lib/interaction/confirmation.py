"""Dangerous-action confirmation guard.

Usage:
    from interaction.confirmation import confirm

    if not confirm("Push 3 commits to origin/main"):
        return
"""
from __future__ import annotations

from rich.console import Console
from rich.prompt import Confirm

_console = Console()


def confirm(description: str, default: bool = False) -> bool:
    """Print a danger banner and prompt y/N. Returns True if the user confirms."""
    _console.print()
    _console.print("[bold red]⚠  DANGEROUS ACTION[/bold red]")
    _console.print(f"  {description}")
    return Confirm.ask("  Proceed?", default=default)
