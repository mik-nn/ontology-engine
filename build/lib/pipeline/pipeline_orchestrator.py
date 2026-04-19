"""Stage 8 — PipelineOrchestrator.

Central state machine that drives the full pipeline:
  IDLE → INTROSPECTING → VERIFYING → PLANNING → EXECUTING → SYNCING → COMPLETED | FAILED

The ontology is the single source of truth. The orchestrator reads pipeline
state from the graph via SPARQL, not from Python variables.

LLM is an atomic executor only — it never orchestrates, logs, or pushes git.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.graph_store import GraphStore
from pipeline.event_logger import EventLogger
from pipeline.git_client import GitClient
from pipeline.doc_sync import DocSync


SHAPES = [
    "core/shacl/databook_shapes.ttl",
    "core/shacl/dependencies_shapes.ttl",
    "core/shacl/planning_shapes.ttl",
]

GRAPH_INTROSPECT = "logs/graphs/introspection.trig"
GRAPH_VERIFIED   = "logs/graphs/verified.trig"
GRAPH_PLANNED    = "logs/graphs/planned.trig"
GRAPH_EXECUTED   = "logs/graphs/executed.trig"


class PipelineState(Enum):
    IDLE          = "idle"
    INTROSPECTING = "introspecting"
    INTERVIEWING  = "interviewing"
    VERIFYING     = "verifying"
    PLANNING      = "planning"
    EXECUTING     = "executing"
    SYNCING       = "syncing"
    VISUALIZING   = "visualizing"
    COMPLETED     = "completed"
    FAILED        = "failed"


@dataclass
class PipelineRun:
    request: str
    state: PipelineState = PipelineState.IDLE
    errors: list[str] = field(default_factory=list)
    graph_path: Optional[str] = None

    @property
    def failed(self) -> bool:
        return self.state == PipelineState.FAILED

    def fail(self, reason: str) -> None:
        self.errors.append(reason)
        self.state = PipelineState.FAILED


class PipelineOrchestrator:
    """Drives the full pipeline from request to committed output.

    Each transition reads pipeline state from the graph, executes the
    corresponding stage, and writes results back as RDF events.
    """

    def __init__(
        self,
        auto: bool = False,
        commit: bool = False,
        push: bool = False,
        verbose: bool = True,
    ):
        self.auto = auto
        self.commit = commit
        self.push = push
        self.verbose = verbose

        self.store = GraphStore()
        self.logger = EventLogger(self.store)
        self.git = GitClient()

    def run(self, request: str, graph_path: Optional[str] = None) -> PipelineRun:
        run = PipelineRun(request=request, graph_path=graph_path)

        # ── Tool fast-path: deterministic tools skip the full pipeline ─────────
        tool_result = self._try_tool(run)
        if tool_result is not None:
            return run
        # ── Full pipeline ──────────────────────────────────────────────────────

        transitions = [
            (PipelineState.INTROSPECTING, self._stage_introspect),
            (PipelineState.INTERVIEWING,  self._stage_interview),
            (PipelineState.VERIFYING,     self._stage_verify),
            (PipelineState.PLANNING,      self._stage_plan),
            (PipelineState.EXECUTING,     self._stage_execute),
            (PipelineState.SYNCING,       self._stage_sync),
            (PipelineState.VISUALIZING,   self._stage_visualize),
        ]

        for state, handler in transitions:
            run.state = state
            self._print(f"\n{'='*50}")
            self._print(f"State: {state.value.upper()}")
            self._print(f"{'='*50}")

            try:
                handler(run)
            except Exception as exc:
                run.fail(f"{state.value}: {exc}")
                self.logger.log(
                    "PipelineHolon",
                    agent="PipelineOrchestrator",
                    status="failed",
                    pipelineState=state.value,
                    errorMessage=str(exc),
                )
                break

            if run.failed:
                break

        if not run.failed:
            run.state = PipelineState.COMPLETED
            self.logger.log(
                "PipelineHolon",
                agent="PipelineOrchestrator",
                status="completed",
            )
            self._print("\nPipeline completed successfully.")
        else:
            self._print(f"\nPipeline FAILED: {run.errors[-1]}")

        return run

    # ──────────────────────────────────────────────
    # Tool fast-path
    # ──────────────────────────────────────────────

    def _try_tool(self, run: PipelineRun):
        """Check the tool registry before running the full pipeline.

        Returns the ToolResult if a tool handled the request, else None.
        """
        import execution.tools.git_tools  # ensure tools are registered  # noqa: F401
        from execution.tools.registry import get_registry
        registry = get_registry()
        result = registry.dispatch(run.request, git=self.git, store=self.store)
        if result is None:
            return None

        self._print(f"\n{'='*50}")
        self._print(f"Tool: {result.tool_name}")
        self._print(f"{'='*50}")
        result.print()

        if result.success:
            run.state = PipelineState.COMPLETED
            self.logger.log(
                "ToolExecuted",
                agent="ToolRegistry",
                status="completed",
                toolName=result.tool_name,
                output=result.output[:200],
            )
            self._print("\nCompleted via tool (no pipeline needed).")
        else:
            run.fail(f"Tool {result.tool_name} failed: {result.error}")
            self.logger.log(
                "ToolExecuted",
                agent="ToolRegistry",
                status="failed",
                toolName=result.tool_name,
                errorMessage=result.error or "",
            )
        return result

    # ──────────────────────────────────────────────
    # Stage handlers
    # ──────────────────────────────────────────────

    def _stage_introspect(self, run: PipelineRun) -> None:
        from introspection.project_scanner import ProjectScanner
        from introspection.code_parser import CodeParser
        from introspection.doc_parser import DocParser

        scanner = ProjectScanner(self.store, project_root=".")
        scanner.scan()
        self._print(f"  Scanned: {self.store}")

        CodeParser(self.store, project_root=".").parse_all()
        DocParser(self.store, project_root=".").parse_all()

        conforms, shacl_text = self.store.validate(SHAPES)
        if not conforms:
            self._print(f"  [SHACL] {shacl_text[:200]}")

        self.store.save(GRAPH_INTROSPECT)
        run.graph_path = GRAPH_INTROSPECT
        self._print(f"  Saved → {GRAPH_INTROSPECT}")

        self.logger.log(
            "ProjectScanned",
            agent="PipelineOrchestrator",
            status="completed",
            outputPath=GRAPH_INTROSPECT,
        )

    def _stage_interview(self, run: PipelineRun) -> None:
        from interaction.interviewer import Interviewer

        if run.graph_path:
            self.store.load(run.graph_path)

        if self.auto:
            self._print("  --auto: skipping interview.")
            return

        interviewer = Interviewer(self.store)
        session = interviewer.run()
        self._print(f"  {session.summary()}")

        if session.gaps_closed > 0:
            self.store.save(GRAPH_INTROSPECT)
            run.graph_path = GRAPH_INTROSPECT
            self._print(f"  Updated → {GRAPH_INTROSPECT}")

        self.logger.log(
            "UserAnswerReceived",
            agent="PipelineOrchestrator",
            status="completed",
            gapsClosed=str(session.gaps_closed),
        )

    def _stage_verify(self, run: PipelineRun) -> None:
        from verification.rule_engine import RuleEngine
        from verification.verify_cli import VerifyCLI

        if run.graph_path:
            self.store.load(run.graph_path)

        engine = RuleEngine(
            self.store,
            shapes_paths=SHAPES + ["core/rules/rules.ttl"],
        )
        rule_report = engine.run()
        self._print(rule_report.summary())

        if rule_report.violations and not self.auto:
            cli = VerifyCLI(self.store, rule_report)
            cli.run()

        self.store.save(GRAPH_VERIFIED)
        run.graph_path = GRAPH_VERIFIED
        self._print(f"  Saved → {GRAPH_VERIFIED}")

        self.logger.log(
            "OntologyValidated",
            agent="PipelineOrchestrator",
            status="completed",
            violationCount=str(len(rule_report.violations)),
        )

    def _stage_plan(self, run: PipelineRun) -> None:
        from planning.task_classifier import TaskClassifier
        from planning.task_decomposer import TaskDecomposer
        from planning.task_planner import TaskPlanner

        if run.graph_path:
            self.store.load(run.graph_path)

        classifier = TaskClassifier(self.store)
        result = classifier.classify(run.request)
        self._print(f"  task_type={result.task_type}  confidence={result.confidence:.2f}")

        decomposer = TaskDecomposer(self.store)
        tree = decomposer.decompose(result)
        self._print(f"  subtasks={len(tree.nodes)}")

        planner = TaskPlanner(self.store, shapes=SHAPES)
        self._spec = planner.plan(tree)
        self._print(self._spec.summary())

        self.store.save(GRAPH_PLANNED)
        run.graph_path = GRAPH_PLANNED
        self._print(f"  Saved → {GRAPH_PLANNED}")

        self.logger.log(
            "PlanGenerated",
            agent="PipelineOrchestrator",
            status="completed",
            planId=self._spec.plan_id,
        )

    def _stage_execute(self, run: PipelineRun) -> None:
        from planning.plan_executor import PlanExecutor
        from verification.rule_engine import RuleEngine

        executor = PlanExecutor(self.store, verbose=self.verbose)

        exec_report = executor.execute(self._spec)
        exec_report.print()

        engine = RuleEngine(self.store, shapes_paths=SHAPES)
        rule_report = engine.run()
        self._print(rule_report.summary())

        self.store.save(GRAPH_EXECUTED)
        run.graph_path = GRAPH_EXECUTED
        self._print(f"  Saved → {GRAPH_EXECUTED}")

        if not exec_report.success:
            run.fail("Execution had failures — check report above.")

    def _stage_sync(self, run: PipelineRun) -> None:
        syncer = DocSync(self.store, self.logger)
        written = syncer.sync_all()
        self._print(f"  Synced {len(written)} databooks.")

        if self.commit and written:
            result = self.git.stage(written)
            if result:
                commit_result = self.git.commit(
                    f"chore: ontology pipeline sync — {run.request[:60]}"
                )
                if commit_result.success:
                    self._print(f"  Committed {commit_result.commit_hash} on {commit_result.branch}")
                    self.logger.log(
                        "GitCommitPushed",
                        agent="PipelineOrchestrator",
                        status="committed",
                        commitHash=commit_result.commit_hash or "",
                        branch=commit_result.branch or "",
                    )
                    if self.push:
                        push_result = self.git.push()
                        if push_result.success:
                            self._print(f"  Pushed to {push_result.remote}/{push_result.branch}")
                        else:
                            self._print(f"  Push failed: {push_result.error}")
                else:
                    self._print(f"  Commit failed: {commit_result.error}")

    # ──────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────

    def _stage_visualize(self, run: PipelineRun) -> None:
        from visualization.graph_exporter import export_json, export_dot

        eg = export_json(self.store, "logs/graphs/graph.json")
        export_dot(self.store, "logs/graphs/graph.dot")
        self._print(f"  Exported {len(eg.nodes)} nodes, {len(eg.edges)} edges")
        self._print("  Viewer → visualization/graph_viewer/index.html")

        self.logger.log(
            "DocumentationSynced",
            agent="PipelineOrchestrator",
            status="visualized",
            nodeCount=str(len(eg.nodes)),
            edgeCount=str(len(eg.edges)),
        )

    def _print(self, msg: str) -> None:
        if self.verbose:
            print(msg)


# ──────────────────────────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Ontology Engine Pipeline Orchestrator")
    parser.add_argument("request",         help="Natural language request to execute")
    parser.add_argument("--graph",         default=None, help="Start from existing .trig graph")
    parser.add_argument("--auto",          action="store_true", help="Skip interactive verify prompts")
    parser.add_argument("--commit",        action="store_true", help="Git commit synced files")
    parser.add_argument("--push",          action="store_true", help="Git push after commit (requires --commit)")
    parser.add_argument("--quiet",         action="store_true", help="Suppress verbose output")
    args = parser.parse_args()

    orchestrator = PipelineOrchestrator(
        auto=args.auto,
        commit=args.commit,
        push=args.push,
        verbose=not args.quiet,
    )
    run = orchestrator.run(args.request, graph_path=args.graph)
    sys.exit(0 if not run.failed else 1)


if __name__ == "__main__":
    main()
