"""Task router — maps (task_type, subtask_executor) → execution strategy.

The two axes of the routing decision:

  task_type     — the high-level intent classified by TaskClassifier
  node_executor — the subtask-level hint from the decomposition pattern
                  ("reasoning" | "llm" | "git_client")

Result is one of:
  "logical"    → LogicalExecutor  (SPARQL + owlrl + pyshacl, no LLM)
  "generative" → StructuredOutputExecutor (SHACL-shaped LLM output)
  "llm"        → LLMExecutor as-is (code writing, free-form text)
  "git"        → git_client path (unchanged)

Routing table rationale (Cagle):
  "Logical tasks are solved logically; generative tasks are solved
   generatively." The boundary is whether the answer can be derived
   deterministically from the graph state.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from planning.task_type_registry import get as get_task_cfg

ExecutionMode = Literal["logical", "structured", "llm", "git"]

# ─────────────────────────────────────────────────────────────────────────────
# Which subtask names use structured output (SHACL MadLibs) vs free-form LLM
# ─────────────────────────────────────────────────────────────────────────────
_STRUCTURED_SUBTASKS = frozenset({
    # DocumentTask
    "write-documentation", "write-docs",
    # AnalysisTask
    "produce-report",
    # ExplainTask
    "generate-explanation",
    # DesignTask
    "draft-structure",
    # ReviewTask / DebugTask
    "produce-review", "diagnose",
})

# Subtask names that stay as free-form LLM (code content, not structured data)
_FREEFORM_SUBTASKS = frozenset({
    "write-code", "apply-changes", "apply-migration",
    "apply-refactor", "apply-fix", "write-glue-code",
    "execute-solution", "draft-interface",
    "search-web", "synthesize-results",
})


class TaskRouter:
    """Decides which executor handles a given (task_type, subtask_node) pair."""

    def route(self, task_type: str, node_executor: str, subtask_name: str = "") -> ExecutionMode:
        """Return the ExecutionMode for this combination.

        Priority order:
          1. git_client nodes → always "git"
          2. reasoning nodes  → always "logical"
          3. llm nodes with structured subtask name → "structured"
          4. llm nodes with free-form subtask name  → "llm"
          5. task-level executor_mode from registry as tie-breaker
        """
        if node_executor == "git_client":
            return "git"

        if node_executor == "reasoning":
            return "logical"

        # node_executor == "llm" — decide structured vs free-form
        if subtask_name in _STRUCTURED_SUBTASKS:
            return "structured"

        if subtask_name in _FREEFORM_SUBTASKS:
            return "llm"

        # Fall back to task-type registry
        cfg = get_task_cfg(task_type)
        if cfg.executor_mode == "logical":
            return "logical"
        if cfg.executor_mode == "generative":
            # generative + llm node → structured if not explicitly free-form
            return "structured"

        # hybrid: default to structured for llm nodes not in free-form list
        return "structured"

    def use_structured_output(self, task_type: str, subtask_name: str) -> bool:
        """Convenience predicate: True when the llm subtask should use StructuredOutputExecutor."""
        return self.route(task_type, "llm", subtask_name) == "structured"


# Module-level singleton — import and use directly
router = TaskRouter()
