"""Stage 7 — Plan Executor.

Iterates a PlanSpec in topological order. For each subtask:
  1. Build context packet (ContextBuilder + ContextPruner)
  2. Dispatch to executor stub (Stage 8 will replace stubs with real LLM/git calls)
  3. Write ExecutionResult to graph
  4. Validate with RuleEngine
  5. Update subtask status and emit event

Executor stubs:
  - llm       → logs context + placeholder result
  - reasoning → runs SPARQL/RuleEngine queries, no LLM
  - git_client → stubs a commit (Stage 8 wires the real GitAgent)
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri as make_uri, graph_uri
from context.context_builder import ContextBuilder
from context.context_pruner import ContextPruner
from planning.task_planner import PlanSpec
from planning.task_decomposer import SubtaskNode

OE   = Namespace("https://ontologist.ai/ns/oe/")
PROV = Namespace("http://www.w3.org/ns/prov#")
XSD  = Namespace("http://www.w3.org/2001/XMLSchema#")
PIPE = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")

MAX_TOKENS = 4000
MAX_DEPTH  = 3


@dataclass
class ExecutionResult:
    subtask_name: str
    executor: str
    status: str              # "completed" | "failed" | "skipped"
    output_summary: str
    context_token_estimate: int = 0
    error: Optional[str]        = None


@dataclass
class ExecutionReport:
    plan_id: str
    results: list[ExecutionResult] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return all(r.status == "completed" for r in self.results)

    def print(self) -> None:
        print(f"\nExecution Report — plan {self.plan_id}")
        for r in self.results:
            icon = "✓" if r.status == "completed" else "✗"
            print(f"  {icon} [{r.executor:12}] {r.subtask_name}: {r.output_summary[:60]}")
            if r.error:
                print(f"      ERROR: {r.error}")


class PlanExecutor:
    """Runs each subtask in topological order."""

    def __init__(self, store: GraphStore, verbose: bool = True):
        self.store = store
        self.verbose = verbose
        self._builder = ContextBuilder(store, max_depth=MAX_DEPTH, max_tokens=MAX_TOKENS)
        self._pruner  = ContextPruner(max_tokens=MAX_TOKENS)

    def execute(self, spec: PlanSpec) -> ExecutionReport:
        report = ExecutionReport(plan_id=spec.plan_id)
        plan_uri = URIRef(spec.plan_uri)
        interior = graph_uri(plan_uri, "interior")
        self.store.add(plan_uri, OE.hasStatus, Literal("active"), interior)

        for node in spec.ordered_subtasks:
            if self.verbose:
                print(f"  → [{node.executor:12}] {node.name}")

            result = self._execute_subtask(node, spec)
            report.results.append(result)
            self._update_subtask(node, result)

            if result.status == "failed":
                self.store.add(plan_uri, OE.hasStatus,
                               Literal("failed"), interior)
                break

        if report.success:
            self.store.add(plan_uri, OE.hasStatus,
                           Literal("completed"), interior)

        self._emit_plan_event(spec, report)
        return report

    # ──────────────────────────────────────────────
    # Subtask dispatch
    # ──────────────────────────────────────────────

    def _execute_subtask(self, node: SubtaskNode,
                         spec: PlanSpec) -> ExecutionResult:
        # Pick anchor: first matched entity, or plan URI itself
        anchor = (spec.matched_entities[0] if spec.matched_entities
                  else spec.plan_uri)

        # Build context
        raw    = self._builder.build(anchor)
        pruned = self._pruner.prune(raw)

        try:
            if node.executor == "reasoning":
                output = self._exec_reasoning(node, pruned)
            elif node.executor == "llm":
                output = self._exec_llm(node, pruned, spec)
            elif node.executor == "git_client":
                output = self._exec_git(node, pruned)
            else:
                output = f"Unknown executor '{node.executor}' — skipped."

            return ExecutionResult(
                subtask_name=node.name,
                executor=node.executor,
                status="completed",
                output_summary=output,
                context_token_estimate=pruned.token_estimate,
            )
        except Exception as exc:
            return ExecutionResult(
                subtask_name=node.name,
                executor=node.executor,
                status="failed",
                output_summary="",
                error=str(exc),
            )

    # ──────────────────────────────────────────────
    # Executors
    # ──────────────────────────────────────────────

    def _exec_reasoning(self, node: SubtaskNode, ctx) -> str:
        triples = ctx.triple_count
        entities = len(ctx.entity_summaries)
        return (f"Reasoning completed: {triples} triples analysed, "
                f"{entities} entities in scope.")

    # Write-subtask names that should produce file content and write it to disk
    _WRITE_SUBTASKS = {"write-code", "apply-changes", "generate-explanation"}

    def _exec_llm(self, node: SubtaskNode, ctx, spec: "PlanSpec") -> str:
        from execution.llm_executor import LLMExecutor
        from cli.config import find_config, load_config
        cfg_path = find_config()
        llm_cfg = load_config(cfg_path).get("llm", {"provider": "claude-code"})

        ai_todos = self._collect_ai_todos(ctx.anchor_uri)
        executor = LLMExecutor.from_config(llm_cfg)

        # For write subtasks: resolve target file and feed current content to LLM
        target_file: str | None = None
        target_content: str | None = None
        if node.name in self._WRITE_SUBTASKS:
            target_file = self._resolve_target_file(spec)
            if target_file:
                try:
                    from pathlib import Path
                    target_content = Path(target_file).read_text(encoding="utf-8")
                except OSError:
                    target_content = ""

        # Enrich the task description with original user request
        task_desc = node.description
        if spec.original_request and node.name in self._WRITE_SUBTASKS:
            task_desc = f"Original request: {spec.original_request}\n\n{task_desc}"

        result = executor.run(
            task_description=task_desc,
            context=ctx,
            ai_todos=ai_todos,
            target_file=target_file,
            target_file_content=target_content,
        )
        self._store_llm_output(node, result.output)

        # Write code to disk for write-subtasks
        written = ""
        if node.name in self._WRITE_SUBTASKS and target_file and result.output.strip():
            written = self._write_file(target_file, result.output)
            self._mark_todos_resolved(target_file)

        summary = f"LLM completed ({result.summary})."
        if written:
            summary += f" {written}"
        else:
            summary += f" Output: {result.output[:80].strip()}"
        return summary

    def _exec_git(self, node: SubtaskNode, ctx) -> str:
        from pipeline.git_client import GitClient, GitCommitResult, GitPushResult
        git = GitClient()
        name = node.name

        if name == "check-status":
            status = git.status()
            return f"git status:\n{status}" if status else "Working tree clean."

        if name == "stage-changes":
            changed = git.changed_files()
            if not changed:
                return "Nothing to stage — working tree clean."
            git.stage(changed)
            return f"Staged {len(changed)} file(s): {', '.join(changed[:5])}"

        if name in ("commit-changes", "commit-all"):
            changed = git.changed_files()
            if not changed:
                return "Nothing to commit — working tree clean."
            git.stage(changed)
            msg = f"ont: {node.description[:72]}"
            result: GitCommitResult = git.commit(msg)
            if result.success:
                return f"Committed {len(changed)} file(s): {result.commit_hash} on {result.branch}"
            return f"Commit failed: {result.error}"

        if name == "push-to-remote":
            result: GitPushResult = git.push()
            if result.success:
                return f"Pushed branch '{result.branch}' to {result.remote}."
            return f"Push failed: {result.error}"

        # Fallback for custom git subtask names: stage + commit
        changed = git.changed_files()
        if not changed:
            return "No changed files."
        git.stage(changed)
        msg = f"ont: {node.description[:72]}"
        r: GitCommitResult = git.commit(msg)
        if r.success:
            return f"Committed {len(changed)} file(s): {r.commit_hash}"
        return f"Commit failed: {r.error}"

    # ──────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────

    def _collect_ai_todos(self, anchor_uri: str) -> list[dict]:
        """Return AI-Todos linked to the anchor module (or all if none linked)."""
        results = list(self.store._g.query(f"""
            PREFIX oe: <https://ontologist.ai/ns/oe/>
            SELECT ?file ?fn ?desc ?priority WHERE {{
                ?todo a oe:AITodo ;
                      oe:filePath ?file ;
                      oe:description ?desc ;
                      oe:priority ?priority .
                OPTIONAL {{ ?todo oe:functionName ?fn }}
                OPTIONAL {{
                    ?mod oe:hasAITodo ?todo .
                    FILTER(?mod = <{anchor_uri}>)
                }}
            }} ORDER BY ?priority LIMIT 10
        """))
        return [
            {
                "file": str(r.file),
                "function": str(r.fn) if r.fn else None,
                "reason": str(r.desc),
                "priority": str(r.priority),
            }
            for r in results
        ]

    def _resolve_target_file(self, spec: "PlanSpec") -> str | None:
        """Return a file path from matched entities or by parsing the original request."""
        import re
        # 1. matched entity → oe:filePath in graph
        for uri in spec.matched_entities:
            from rdflib import URIRef
            fp = self.store._g.value(URIRef(uri), OE.filePath)
            if fp:
                return str(fp)
        # 2. extract *.py path from the request text
        m = re.search(r'[\w./\\-]+\.py\b', spec.original_request)
        if m:
            return m.group(0)
        return None

    def _write_file(self, path: str, content: str) -> str:
        """Write LLM output to a file. Strips accidental markdown fences."""
        import re as _re
        from pathlib import Path
        # Strip outermost ```python / ``` fences if the model added them
        cleaned = _re.sub(r'^```[a-z]*\n?', '', content.strip())
        cleaned = _re.sub(r'\n?```$', '', cleaned)
        Path(path).write_text(cleaned, encoding="utf-8")
        return f"Written → {path} ({len(cleaned)} chars)"

    def _mark_todos_resolved(self, file_path: str) -> None:
        """Mark all oe:AITodo nodes for a file as resolved in the graph."""
        results = list(self.store._g.query(f"""
            PREFIX oe: <https://ontologist.ai/ns/oe/>
            SELECT ?todo ?g WHERE {{
                GRAPH ?g {{ ?todo a oe:AITodo ; oe:filePath ?fp .
                           FILTER(str(?fp) = "{file_path}") }}
            }}
        """))
        for row in results:
            todo_uri = row.todo
            g_uri = row.g
            self.store.add(todo_uri, OE.hasStatus, Literal("resolved"), g_uri)

    def _store_llm_output(self, node: SubtaskNode, output: str) -> None:
        sub_uri = URIRef(node.uri)
        interior = graph_uri(sub_uri, "interior")
        self.store.add(sub_uri, OE.llmOutput, Literal(output), interior)

    # ──────────────────────────────────────────────
    # Graph updates
    # ──────────────────────────────────────────────

    def _update_subtask(self, node: SubtaskNode,
                        result: ExecutionResult) -> None:
        sub_uri = URIRef(node.uri)
        sub_int = graph_uri(sub_uri, "interior")
        now = datetime.now(timezone.utc).isoformat()

        self.store.add(sub_uri, OE.hasStatus,
                       Literal(result.status), sub_int)
        self.store.add(sub_uri, OE.outputSummary,
                       Literal(result.output_summary), sub_int)
        self.store.add(sub_uri, PROV.endedAtTime,
                       Literal(now, datatype=XSD.dateTime), sub_int)

        node.status = result.status
        self._emit_subtask_event(node, result)

    def _emit_subtask_event(self, node: SubtaskNode,
                            result: ExecutionResult) -> None:
        ev = make_uri("event", f"subtask-executed-{uuid.uuid4().hex[:6]}")
        now = datetime.now(timezone.utc).isoformat()

        self.store.add(ev, RDF.type,          OE.PlanExecuted,            PIPE)
        self.store.add(ev, OE.hasAgent,       Literal("PlanningAgent"),   PIPE)
        self.store.add(ev, OE.hasStatus,      Literal(result.status),     PIPE)
        self.store.add(ev, OE.subtaskUri,     URIRef(node.uri),           PIPE)
        self.store.add(ev, OE.executorUsed,   Literal(result.executor),   PIPE)
        self.store.add(ev, PROV.startedAtTime,
                       Literal(now, datatype=XSD.dateTime),               PIPE)

    def _emit_plan_event(self, spec: PlanSpec,
                         report: ExecutionReport) -> None:
        ev = make_uri("event", f"plan-executed-{spec.plan_id}")
        now = datetime.now(timezone.utc).isoformat()
        status = "success" if report.success else "failure"

        self.store.add(ev, RDF.type,       OE.PlanExecuted,               PIPE)
        self.store.add(ev, OE.hasAgent,    Literal("PlanningAgent"),      PIPE)
        self.store.add(ev, OE.hasStatus,   Literal(status),               PIPE)
        self.store.add(ev, OE.planUri,     URIRef(spec.plan_uri),         PIPE)
        self.store.add(ev, OE.stepCount,   Literal(len(report.results)),  PIPE)
        self.store.add(ev, PROV.startedAtTime,
                       Literal(now, datatype=XSD.dateTime),               PIPE)
