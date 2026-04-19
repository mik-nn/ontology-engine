"""Tool registry — ordered list of deterministic tools checked before planning."""
from __future__ import annotations

from typing import Any

from execution.tools.base import Tool, ToolResult


class ToolRegistry:
    """Holds all registered tools. dispatch() picks the first confident match."""

    def __init__(self) -> None:
        self._tools: list[Tool] = []

    def register(self, tool: Tool) -> "ToolRegistry":
        """Register a tool. Returns self for chaining."""
        self._tools.append(tool)
        return self

    def dispatch(self, request: str, **ctx: Any) -> ToolResult | None:
        """Find the best-matching tool and run it. Returns None if no match."""
        best_tool: Tool | None = None
        best_score = 0.0
        for tool in self._tools:
            score = tool.matches(request)
            if score > best_score:
                best_score = score
                best_tool = tool
        if best_tool and best_score > 0:
            return best_tool.run(request, **ctx)
        return None

    def list_tools(self) -> list[Tool]:
        """Return all registered tools."""
        return list(self._tools)


# ── Default registry — import and extend from anywhere ────────────────────────

_registry = ToolRegistry()


def get_registry() -> ToolRegistry:
    """Return the process-level default registry."""
    return _registry


def register(tool: Tool) -> None:
    """Register a tool in the default registry."""
    _registry.register(tool)
