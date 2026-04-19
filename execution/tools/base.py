"""Base classes for deterministic pipeline tools."""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:
    """Result of a direct tool invocation."""
    tool_name: str
    success: bool
    output: str
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def print(self) -> None:
        icon = "✓" if self.success else "✗"
        print(f"  {icon} [{self.tool_name}] {self.output}")
        if self.error:
            print(f"      ERROR: {self.error}")


class Tool(ABC):
    """A named, self-describing deterministic executor."""

    # Subclasses set these at class level
    name: str = ""
    description: str = ""
    patterns: list[str] = []      # regex patterns checked against the request

    def matches(self, request: str) -> float:
        """Return confidence 0.0–1.0. Default: 1.0 if any pattern matches."""
        text = request.lower()
        for p in self.patterns:
            if re.search(p, text, re.IGNORECASE):
                return 1.0
        return 0.0

    @abstractmethod
    def run(self, request: str, **ctx: Any) -> ToolResult: ...
