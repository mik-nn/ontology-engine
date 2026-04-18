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
                output = self._exec_llm(node, pruned)
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
    # Executor stubs (Stage 8 replaces with real implementations)
    # ──────────────────────────────────────────────

    def _exec_reasoning(self, node: SubtaskNode, ctx) -> str:
        # Deterministic: run SPARQL / RuleEngine queries against graph
        triples = ctx.triple_count
        entities = len(ctx.entity_summaries)
        return (f"Reasoning completed: {triples} triples analysed, "
                f"{entities} entities in scope. "
                f"[stub — Stage 8 wires real SPARQL queries]")

    def _exec_llm(self, node: SubtaskNode, ctx) -> str:
        # Stage 8 will call the LLM executor with ctx.to_prompt_text()
        tokens = ctx.token_estimate
        return (f"LLM executor stub: context packet {ctx.packet_id} "
                f"({tokens} tokens) ready for dispatch. "
                f"Task: {node.description[:80]}")

    def _exec_git(self, node: SubtaskNode, ctx) -> str:
        # Stage 8 will call GitAgent
        return "Git commit stub: no files changed yet (Stage 8 wires GitAgent)."

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
