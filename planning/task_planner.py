"""Stage 7 — Task Planner (no LLM).

Takes a SubtaskTree and produces a validated, topologically sorted Plan:
  1. Topological sort using Kahn's algorithm on dependsOn edges
  2. Executor assignment per subtask type (from rules, not LLM)
  3. Cycle detection (raises PlanningError if cycle found)
  4. SHACL validation of the Plan node
  5. Writes PlanGenerated event

Returns a PlanSpec ready for PlanExecutor.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from rdflib import Namespace, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri as make_uri, graph_uri
from planning.task_decomposer import SubtaskTree, SubtaskNode

OE   = Namespace("https://ontologist.ai/ns/oe/")
PROV = Namespace("http://www.w3.org/ns/prov#")
XSD  = Namespace("http://www.w3.org/2001/XMLSchema#")

# Routing rules — map TaskType → executor (deterministic, no LLM)
_EXECUTOR_MAP: dict[str, str] = {
    "ExplainTask":  "llm",
    "DesignTask":   "llm",
    "ImplementTask": "llm",
    "RefactorTask": "llm",
    "AnalysisTask": "reasoning",
}

# Which task types require git_client as a post-step
_GIT_REQUIRED = {"ImplementTask", "RefactorTask"}


class PlanningError(Exception):
    pass


@dataclass
class PlanSpec:
    plan_id: str
    plan_uri: str
    original_type: str
    original_request: str
    matched_entities: list[str]
    ordered_subtasks: list[SubtaskNode] = field(default_factory=list)
    executor_map: dict[str, str]        = field(default_factory=dict)  # name → executor

    def summary(self) -> str:
        lines = [
            f"Plan: {self.plan_id}  ({self.original_type})",
            f"Request: {self.original_request[:80]}",
            f"Steps ({len(self.ordered_subtasks)}):",
        ]
        for i, node in enumerate(self.ordered_subtasks, 1):
            deps = ", ".join(self.ordered_subtasks[d].name
                             for d in node.depends_on) or "—"
            lines.append(f"  {i}. [{node.executor:12}] {node.name}  (deps: {deps})")
        return "\n".join(lines)


class TaskPlanner:
    """Produces a validated, topologically sorted PlanSpec from a SubtaskTree."""

    def __init__(self, store: GraphStore,
                 shapes: list[str] | None = None):
        self.store = store
        self.shapes = shapes or [
            "core/shacl/planning_shapes.ttl",
            "core/shacl/holon_shapes.ttl",
        ]

    def plan(self, tree: SubtaskTree) -> PlanSpec:
        ordered = self._topo_sort(tree.nodes)
        self._assign_executors(ordered, tree)

        plan_uri = make_uri("plan", tree.plan_id)
        spec = PlanSpec(
            plan_id=tree.plan_id,
            plan_uri=str(plan_uri),
            original_type=tree.original_type,
            original_request=tree.original_request,
            matched_entities=tree.matched_entities,
            ordered_subtasks=ordered,
            executor_map={n.name: n.executor for n in ordered},
        )

        self._update_graph_order(spec)
        self._validate(spec)
        self._emit_event(spec)
        return spec

    # ──────────────────────────────────────────────
    # Kahn's topological sort
    # ──────────────────────────────────────────────

    def _topo_sort(self, nodes: list[SubtaskNode]) -> list[SubtaskNode]:
        in_degree = {n.index: len(n.depends_on) for n in nodes}
        adjacency: dict[int, list[int]] = {n.index: [] for n in nodes}
        for n in nodes:
            for dep in n.depends_on:
                adjacency[dep].append(n.index)

        queue = [n for n in nodes if in_degree[n.index] == 0]
        result: list[SubtaskNode] = []

        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbour_idx in adjacency[node.index]:
                in_degree[neighbour_idx] -= 1
                if in_degree[neighbour_idx] == 0:
                    neighbour = next(n for n in nodes if n.index == neighbour_idx)
                    queue.append(neighbour)

        if len(result) != len(nodes):
            raise PlanningError(
                f"Cycle detected in subtask dependsOn graph — plan {nodes} is invalid."
            )
        return result

    # ──────────────────────────────────────────────
    # Executor assignment
    # ──────────────────────────────────────────────

    def _assign_executors(self, nodes: list[SubtaskNode],
                          tree: SubtaskTree) -> None:
        for node in nodes:
            # Decomposer already set executor — override only if needed by rules
            if node.name.endswith("commit-changes"):
                node.executor = "git_client"
            elif node.task_type in _EXECUTOR_MAP and node.executor not in ("git_client",):
                node.executor = _EXECUTOR_MAP[node.task_type]

    # ──────────────────────────────────────────────
    # Write execution order back to graph
    # ──────────────────────────────────────────────

    def _update_graph_order(self, spec: PlanSpec) -> None:
        plan_uri = URIRef(spec.plan_uri)
        interior = graph_uri(plan_uri, "interior")
        self.store.add(plan_uri, OE.hasStatus, Literal("ready"), interior)

        for step, node in enumerate(spec.ordered_subtasks, 1):
            sub_uri = URIRef(node.uri)
            sub_int = graph_uri(sub_uri, "interior")
            self.store.add(sub_uri, OE.executionOrder, Literal(step), sub_int)
            self.store.add(sub_uri, OE.hasExecutor,
                           Literal(node.executor), sub_int)

    # ──────────────────────────────────────────────
    # SHACL validation
    # ──────────────────────────────────────────────

    def _validate(self, spec: PlanSpec) -> None:
        try:
            conforms, report = self.store.validate(self.shapes)
        except FileNotFoundError:
            return  # shapes not yet created — skip during bootstrap
        if not conforms:
            raise PlanningError(f"Plan SHACL validation failed:\n{report}")

    # ──────────────────────────────────────────────
    # Event
    # ──────────────────────────────────────────────

    def _emit_event(self, spec: PlanSpec) -> None:
        from datetime import datetime, timezone
        from rdflib import RDF
        plan_uri = URIRef(spec.plan_uri)
        ev = make_uri("event", f"plan-generated-{spec.plan_id}")
        PIPE = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")

        self.store.add(ev, RDF.type,       OE.PlanGenerated,            PIPE)
        self.store.add(ev, OE.hasAgent,    Literal("PlanningAgent"),    PIPE)
        self.store.add(ev, OE.hasStatus,   Literal("success"),          PIPE)
        self.store.add(ev, OE.planUri,     plan_uri,                    PIPE)
        self.store.add(ev, OE.stepCount,   Literal(len(spec.ordered_subtasks)), PIPE)
        self.store.add(ev, PROV.startedAtTime,
                       Literal(datetime.now(timezone.utc).isoformat(),
                               datatype=XSD.dateTime),                  PIPE)
