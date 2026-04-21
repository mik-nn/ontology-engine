"""Task type registry — single source of truth for task routing.

Each TaskTypeConfig declares HOW a task type should be executed:
  - llm_role:       which [llm.<role>] adapter to use (→ .ontology.toml)
  - thinking:       enable extended thinking for this class of problem
  - search_before:  run WebSearch enrichment before LLM call
  - interview_gaps: SHACL gap codes to surface in the interview stage
  - executor_mode:  "logical" | "generative" | "hybrid"
      logical    — pure SPARQL + owlrl + pyshacl, no LLM (ValidateTask, GitTask)
      generative — LLM with SHACL-shaped structured output (DocumentTask, ImplementTask…)
      hybrid     — reasoning subtasks → LogicalExecutor;
                   llm subtasks → StructuredOutputExecutor (AnalysisTask, DesignTask)

The registry drives four pipeline decisions without LLM involvement:
  1. Model selection  — PlanExecutor reads llm_role → factory.create_for_role()
  2. Thinking toggle  — PlanExecutor passes thinking=True to LLMExecutor
  3. Executor mode    — TaskRouter reads executor_mode → routes to correct executor
  4. Pre-execution enrichment (future) — search_before triggers web tools

Adding a new task type here automatically propagates to the entire pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TaskTypeConfig:
    llm_role: str               # key in [llm.<role>] toml section
    thinking: bool              # enable extended thinking for this type
    search_before: bool         # trigger web-search enrichment pre-LLM
    interview_gaps: tuple       # SHACL gap codes to check before execution
    executor_mode: str = "generative"  # "logical" | "generative" | "hybrid"
    description: str = ""       # human-readable purpose


# ──────────────────────────────────────────────────────────────────────────────
# Registry — 14 task types
# Model routing: llm_role maps to [llm.write], [llm.reasoning], [llm.complex],
# or falls back to [llm] default when the role section is absent/commented out.
# ──────────────────────────────────────────────────────────────────────────────
REGISTRY: dict[str, TaskTypeConfig] = {

    # ── Existing types ────────────────────────────────────────────────────────

    "ImplementTask": TaskTypeConfig(
        llm_role="write",
        thinking=False,
        search_before=False,
        interview_gaps=("G04",),
        executor_mode="generative",
        description="Create or extend code: modules, classes, functions, adapters.",
    ),
    "ExplainTask": TaskTypeConfig(
        llm_role="default",
        thinking=False,
        search_before=False,
        interview_gaps=("G04",),
        executor_mode="generative",
        description="Answer questions, summarise, clarify how something works.",
    ),
    "RefactorTask": TaskTypeConfig(
        llm_role="write",
        thinking=False,
        search_before=False,
        interview_gaps=("G04",),
        executor_mode="generative",
        description="Restructure existing code without changing external behaviour.",
    ),
    "AnalysisTask": TaskTypeConfig(
        llm_role="reasoning",
        thinking=False,
        search_before=False,
        interview_gaps=(),
        executor_mode="hybrid",
        description="Investigate, audit, scan, or report on project state.",
    ),
    "DesignTask": TaskTypeConfig(
        llm_role="reasoning",
        thinking=True,
        search_before=False,
        interview_gaps=(),
        executor_mode="hybrid",
        description="Architect, model, or plan structure — blueprint before code.",
    ),
    "GitTask": TaskTypeConfig(
        llm_role="default",
        thinking=False,
        search_before=False,
        interview_gaps=(),
        executor_mode="logical",
        description="Git operations: commit, push, stage, sync.",
    ),

    # ── New types ─────────────────────────────────────────────────────────────

    "DebugTask": TaskTypeConfig(
        llm_role="reasoning",
        thinking=True,
        search_before=False,
        interview_gaps=(),
        executor_mode="hybrid",
        description="Diagnose failures, trace errors, find root cause.",
    ),
    "SearchTask": TaskTypeConfig(
        llm_role="default",
        thinking=False,
        search_before=True,
        interview_gaps=("G06",),
        executor_mode="generative",
        description="Look up external documentation, APIs, or specs.",
    ),
    "DocumentTask": TaskTypeConfig(
        llm_role="write",
        thinking=False,
        search_before=False,
        interview_gaps=("G01", "G02", "G03"),
        executor_mode="generative",
        description="Write or update documentation, READMEs, databooks.",
    ),
    "ValidateTask": TaskTypeConfig(
        llm_role="reasoning",
        thinking=False,
        search_before=False,
        interview_gaps=(),
        executor_mode="logical",
        description="Run tests, SHACL validation, lint, or type checking.",
    ),
    "MigrateTask": TaskTypeConfig(
        llm_role="write",
        thinking=True,
        search_before=True,
        interview_gaps=("G06",),
        executor_mode="generative",
        description="Upgrade APIs, schemas, or libraries to a new version.",
    ),
    "ReviewTask": TaskTypeConfig(
        llm_role="reasoning",
        thinking=False,
        search_before=False,
        interview_gaps=(),
        executor_mode="hybrid",
        description="Code review, quality assessment, security audit.",
    ),
    "IntegrateTask": TaskTypeConfig(
        llm_role="write",
        thinking=False,
        search_before=True,
        interview_gaps=("G06",),
        executor_mode="generative",
        description="Connect two systems/modules — adapters, bridges, wiring.",
    ),
    "ComplexTask": TaskTypeConfig(
        llm_role="complex",
        thinking=True,
        search_before=True,
        interview_gaps=(),
        executor_mode="generative",
        description="High-uncertainty multi-step problems requiring deep reasoning.",
    ),
}

_DEFAULT = TaskTypeConfig(
    llm_role="default",
    thinking=False,
    search_before=False,
    interview_gaps=(),
    description="Unknown task type — use default model.",
)

ALL_TYPES: frozenset[str] = frozenset(REGISTRY)


def get(task_type: str) -> TaskTypeConfig:
    """Return config for task_type, falling back to _DEFAULT if unknown."""
    return REGISTRY.get(task_type, _DEFAULT)
