"""Stage 7 — Task Decomposer (no LLM).

Decomposes a ClassificationResult into a SubtaskTree using ontology patterns.
Each task type has a canonical decomposition sequence.
Subtasks carry dependsOn edges forming a DAG, written to the graph store.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri as make_uri, graph_uri
from planning.task_classifier import ClassificationResult

OE   = Namespace("https://ontologist.ai/ns/oe/")
CGA  = Namespace("https://ontologist.ai/ns/cga/")
PROV = Namespace("http://www.w3.org/ns/prov#")
XSD  = Namespace("http://www.w3.org/2001/XMLSchema#")

# ──────────────────────────────────────────────────────────
# Decomposition patterns
# Each entry: (subtask_type, name, description, executor, depends_on_indices)
# ──────────────────────────────────────────────────────────
_PATTERNS: dict[str, list[tuple[str, str, str, str, list[int]]]] = {
    "ExplainTask": [
        ("AnalysisTask",  "gather-context",
         "Collect relevant facts, code, and Databook fragments via ContextBuilder.",
         "reasoning", []),
        ("ExplainTask",   "generate-explanation",
         "Use LLM to synthesize a human-readable explanation from the context packet.",
         "llm", [0]),
    ],
    "AnalysisTask": [
        ("AnalysisTask",  "introspect-scope",
         "Run ProjectScanner and CodeParser to establish the current state of the scope.",
         "reasoning", []),
        ("AnalysisTask",  "validate-graph",
         "Run SHACL + RuleEngine to detect any existing violations.",
         "reasoning", [0]),
        ("AnalysisTask",  "produce-report",
         "Use LLM to generate a structured analysis report from the context packet.",
         "llm", [0, 1]),
    ],
    "DesignTask": [
        ("AnalysisTask",  "gather-requirements",
         "Extract requirements from Databooks and user-provided context.",
         "reasoning", []),
        ("DesignTask",    "draft-structure",
         "Use LLM to propose module/class/interface structure aligned with the ontology.",
         "llm", [0]),
        ("AnalysisTask",  "validate-design",
         "Map the draft structure to ontology classes and run SHACL validation.",
         "reasoning", [1]),
    ],
    "ImplementTask": [
        ("AnalysisTask",  "understand-scope",
         "Build context packet for target module; identify dependsOn chain.",
         "reasoning", []),
        ("DesignTask",    "draft-interface",
         "Use LLM to propose class/function signatures and docstrings.",
         "llm", [0]),
        ("ImplementTask", "write-code",
         "Use LLM to generate implementation conforming to the drafted interface.",
         "llm", [1]),
        ("AnalysisTask",  "verify-implementation",
         "Run SHACL + RuleEngine on updated graph; check imports and structure.",
         "reasoning", [2]),
        ("ImplementTask", "commit-changes",
         "Stage and commit generated files via GitAgent.",
         "git_client", [3]),
    ],
    "RefactorTask": [
        ("AnalysisTask",  "analyze-current",
         "Build context packet; identify code smells and structural violations.",
         "reasoning", []),
        ("DesignTask",    "plan-refactor",
         "Use LLM to propose refactoring steps within the ontology model.",
         "llm", [0]),
        ("RefactorTask",  "apply-changes",
         "Use LLM to rewrite affected modules per the refactor plan.",
         "llm", [1]),
        ("AnalysisTask",  "verify-refactor",
         "Run cycle detection, SHACL, and diff review.",
         "reasoning", [2]),
        ("RefactorTask",  "commit-changes",
         "Commit refactored files via GitAgent.",
         "git_client", [3]),
    ],
}


@dataclass
class SubtaskNode:
    index: int
    task_type: str       # "AnalysisTask" | "ExplainTask" | ...
    name: str            # short slug
    description: str
    executor: str        # "llm" | "reasoning" | "git_client"
    depends_on: list[int]  # indices into sibling list
    uri: str             = ""
    status: str          = "pending"


@dataclass
class SubtaskTree:
    plan_id: str
    original_type: str
    original_request: str
    matched_entities: list[str]
    nodes: list[SubtaskNode] = field(default_factory=list)   # topological order


class TaskDecomposer:
    """Rule-based task decomposition — no LLM involvement."""

    def __init__(self, store: GraphStore):
        self.store = store

    def decompose(self, result: ClassificationResult) -> SubtaskTree:
        pattern = _PATTERNS.get(result.task_type, _PATTERNS["AnalysisTask"])
        plan_id = f"plan-{uuid.uuid4().hex[:8]}"

        tree = SubtaskTree(
            plan_id=plan_id,
            original_type=result.task_type,
            original_request=result.raw_request,
            matched_entities=result.matched_entities,
        )

        for i, (task_type, name, desc, executor, deps) in enumerate(pattern):
            node = SubtaskNode(
                index=i,
                task_type=task_type,
                name=name,
                description=desc,
                executor=executor,
                depends_on=deps,
            )
            tree.nodes.append(node)

        self._write_to_graph(tree)
        self._emit_event(tree)
        return tree

    def _write_to_graph(self, tree: SubtaskTree) -> None:
        plan_uri = make_uri("plan", tree.plan_id)
        self.store.declare_holon(plan_uri, OE.Plan)

        interior = graph_uri(plan_uri, "interior")
        self.store.add(plan_uri, OE.hasStatus,   Literal("pending"),         interior)
        self.store.add(plan_uri, OE.planRequest, Literal(tree.original_request), interior)
        self.store.add(plan_uri, OE.planType,    Literal(tree.original_type), interior)

        for node in tree.nodes:
            sub_uri = make_uri("subtask", f"{tree.plan_id}-{node.name}")
            node.uri = str(sub_uri)

            self.store.declare_holon(sub_uri, OE.Subtask)
            sub_int = graph_uri(sub_uri, "interior")
            sub_ctx = graph_uri(sub_uri, "context")

            task_class = getattr(OE, node.task_type, OE.TaskHolon)
            self.store.add(sub_uri, RDF.type,        task_class,               sub_int)
            self.store.add(sub_uri, OE.taskName,     Literal(node.name),       sub_int)
            self.store.add(sub_uri, OE.description,  Literal(node.description), sub_int)
            self.store.add(sub_uri, OE.hasExecutor,  Literal(node.executor),   sub_int)
            self.store.add(sub_uri, OE.hasStatus,    Literal("pending"),       sub_int)
            self.store.add(sub_uri, OE.subtaskIndex, Literal(node.index),      sub_int)
            self.store.add(sub_uri, CGA.partOf,      plan_uri,                 sub_ctx)

            # dependsOn edges by index → URI
            for dep_idx in node.depends_on:
                dep_name = tree.nodes[dep_idx].name
                dep_uri = make_uri("subtask", f"{tree.plan_id}-{dep_name}")
                self.store.add(sub_uri, OE.dependsOn, dep_uri, sub_int)

        # Write entity context for matched entities
        for ent_uri in tree.matched_entities:
            self.store.add(plan_uri, OE.concernsEntity,
                           URIRef(ent_uri), interior)

    def _emit_event(self, tree: SubtaskTree) -> None:
        from datetime import datetime, timezone
        plan_uri = make_uri("plan", tree.plan_id)
        ev = make_uri("event", f"task-decomposed-{tree.plan_id}")
        PIPE = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")

        self.store.add(ev, RDF.type,        OE.TaskDecomposed,          PIPE)
        self.store.add(ev, OE.hasAgent,     Literal("PlanningAgent"),   PIPE)
        self.store.add(ev, OE.hasStatus,    Literal("success"),         PIPE)
        self.store.add(ev, OE.planUri,      plan_uri,                   PIPE)
        self.store.add(ev, OE.subtaskCount, Literal(len(tree.nodes)),   PIPE)
        self.store.add(ev, PROV.startedAtTime,
                       Literal(datetime.now(timezone.utc).isoformat(),
                               datatype=XSD.dateTime),                  PIPE)
