"""Logical executor — handles reasoning subtasks without LLM.

Replaces the stub _exec_reasoning in PlanExecutor with real computation:
  - SHACL validation  (pyshacl)          → subtasks: validate-graph, verify-implementation
  - SPARQL queries    (rdflib)           → subtasks: introspect-scope, gather-context, …
  - owlrl reasoning   (owlrl)            → subtasks: gather-requirements, analyze-current

No LLM calls are made here.  All decisions are derived deterministically
from the graph state and the shapes in core/shacl/.

Cagle principle: "The holonic graph is the stable, low-bandwidth memory —
excellent at persistence, composability, and auditability."
"""
from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from rdflib import Graph, Namespace, URIRef

OE   = Namespace("https://ontologist.ai/ns/oe/")
DB   = Namespace("https://ontologist.ai/ns/databook#")
SH   = Namespace("http://www.w3.org/ns/shacl#")

# Subtask names that require SHACL validation
_SHACL_SUBTASKS = frozenset({
    "validate-graph", "verify-implementation", "validate-design",
    "run-validation", "check-shacl", "check-conformance",
})

# Subtask names that are answered by SPARQL alone
_SPARQL_SUBTASKS = frozenset({
    "introspect-scope", "gather-context", "gather-requirements",
    "analyze-current", "check-status",
})


@dataclass
class LogicalResult:
    """Structured result from a logical execution step."""
    subtask_name: str
    mode: str                          # "shacl" | "sparql" | "reasoning"
    conforms: Optional[bool] = None    # set for SHACL results
    violation_count: int = 0
    summary: str = ""
    details: list[str] = field(default_factory=list)


class LogicalExecutor:
    """Executes reasoning subtasks via SPARQL + owlrl + pyshacl."""

    def __init__(self, store, shapes_dir: Optional[Path] = None):
        self._store = store
        self._shapes_dir = shapes_dir or _find_shapes_dir()

    # ─────────────────────────────────────────────────────────────
    # Public entry point
    # ─────────────────────────────────────────────────────────────

    def run(self, node) -> LogicalResult:
        """Dispatch by subtask name → correct logical mode."""
        name = node.name.lower()

        if name in _SHACL_SUBTASKS or "shacl" in name or "validat" in name:
            return self._run_shacl(node)

        if name in _SPARQL_SUBTASKS or "scope" in name or "context" in name:
            return self._run_sparql(node)

        return self._run_reasoning(node)

    # ─────────────────────────────────────────────────────────────
    # Mode 1: SHACL validation
    # ─────────────────────────────────────────────────────────────

    def _run_shacl(self, node) -> LogicalResult:
        """Run pyshacl over the full store against all shapes files."""
        try:
            import pyshacl
        except ImportError:
            return LogicalResult(
                subtask_name=node.name, mode="shacl",
                summary="pyshacl not installed — skipped.",
            )

        shapes_graph = self._load_shapes()
        data_graph   = self._store._g

        conforms, results_graph, _ = pyshacl.validate(
            data_graph,
            shacl_graph=shapes_graph,
            inference="rdfs",
            abort_on_first=False,
        )

        violations = self._parse_violations(results_graph)
        summary = (
            "Graph conforms to all shapes." if conforms
            else f"{len(violations)} violation(s) found."
        )

        return LogicalResult(
            subtask_name=node.name,
            mode="shacl",
            conforms=conforms,
            violation_count=len(violations),
            summary=summary,
            details=violations[:10],   # cap detail list
        )

    def _load_shapes(self) -> Graph:
        """Merge all .ttl files from the shapes directory into one graph."""
        g = Graph()
        if self._shapes_dir and self._shapes_dir.exists():
            for ttl in sorted(self._shapes_dir.glob("*.ttl")):
                g.parse(str(ttl), format="turtle")
        return g

    def _parse_violations(self, results_graph: Graph) -> list[str]:
        """Extract sh:resultMessage from SHACL results graph."""
        sparql = """
            PREFIX sh: <http://www.w3.org/ns/shacl#>
            SELECT ?focus ?path ?msg WHERE {
                ?result a sh:ValidationResult ;
                        sh:focusNode ?focus ;
                        sh:resultMessage ?msg .
                OPTIONAL { ?result sh:resultPath ?path }
                FILTER(
                    NOT EXISTS { ?result sh:resultSeverity sh:Warning }
                )
            } LIMIT 50
        """
        rows = list(results_graph.query(sparql))
        lines = []
        for r in rows:
            focus = str(r.focus).split("/")[-1]
            path  = str(r.path).split("/")[-1].split("#")[-1] if r.path else "?"
            msg   = str(r.msg)
            lines.append(f"  {focus} [{path}]: {msg}")
        return lines

    # ─────────────────────────────────────────────────────────────
    # Mode 2: SPARQL analysis
    # ─────────────────────────────────────────────────────────────

    def _run_sparql(self, node) -> LogicalResult:
        """Run task-specific SPARQL against the graph store."""
        name = node.name.lower()

        if "introspect" in name or "scope" in name:
            return self._sparql_project_scope(node)
        if "context" in name or "gather" in name:
            return self._sparql_gather_context(node)
        if "requirement" in name:
            return self._sparql_requirements(node)
        if "analyze" in name or "current" in name:
            return self._sparql_code_metrics(node)

        return self._sparql_project_scope(node)

    def _sparql_project_scope(self, node) -> LogicalResult:
        """Count modules, functions, databooks, and existing violations."""
        q = """
            PREFIX oe:  <https://ontologist.ai/ns/oe/>
            PREFIX db:  <https://ontologist.ai/ns/databook#>
            PREFIX sh:  <http://www.w3.org/ns/shacl#>
            SELECT
                (COUNT(DISTINCT ?cm)  AS ?code_modules)
                (COUNT(DISTINCT ?dm)  AS ?data_modules)
                (COUNT(DISTINCT ?db)  AS ?databooks)
                (COUNT(DISTINCT ?fn)  AS ?functions)
            WHERE {
                OPTIONAL { ?cm a oe:CodeModule }
                OPTIONAL { ?dm a oe:DataModule }
                OPTIONAL { ?db a db:Databook }
                OPTIONAL { ?fn a oe:CodeFunction }
            }
        """
        rows = list(self._store.query(q))
        if rows:
            r = rows[0]
            summary = (
                f"Scope: {r.code_modules} CodeModules, "
                f"{r.data_modules} DataModules, "
                f"{r.databooks} Databooks, "
                f"{r.functions} functions."
            )
        else:
            summary = "Scope query returned no results."

        return LogicalResult(
            subtask_name=node.name, mode="sparql", summary=summary,
        )

    def _sparql_gather_context(self, node) -> LogicalResult:
        """Pull entity descriptions, databooks, and module summaries."""
        q = """
            PREFIX oe:  <https://ontologist.ai/ns/oe/>
            PREFIX db:  <https://ontologist.ai/ns/databook#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT DISTINCT ?entity ?desc WHERE {
                { ?entity a oe:CodeModule ; oe:description ?desc }
                UNION
                { ?entity a db:Databook ; db:title ?desc }
            } LIMIT 20
        """
        rows = list(self._store.query(q))
        details = [f"  {str(r.entity).split('/')[-1]}: {str(r.desc)[:80]}"
                   for r in rows]
        summary = f"Context gathered: {len(rows)} entities."
        return LogicalResult(
            subtask_name=node.name, mode="sparql",
            summary=summary, details=details,
        )

    def _sparql_requirements(self, node) -> LogicalResult:
        """Extract requirements from Databooks."""
        q = """
            PREFIX db: <https://ontologist.ai/ns/databook#>
            SELECT ?title ?content WHERE {
                ?db a db:Databook ;
                    db:title ?title ;
                    db:content ?content .
                FILTER(CONTAINS(LCASE(str(?title)), "requirement")
                    || CONTAINS(LCASE(str(?title)), "spec")
                    || CONTAINS(LCASE(str(?title)), "architecture"))
            } LIMIT 10
        """
        rows = list(self._store.query(q))
        details = [f"  [{str(r.title)}]: {str(r.content)[:120]}" for r in rows]
        summary = f"Requirements extracted: {len(rows)} relevant Databooks."
        return LogicalResult(
            subtask_name=node.name, mode="sparql",
            summary=summary, details=details,
        )

    def _sparql_code_metrics(self, node) -> LogicalResult:
        """Check code quality indicators: missing descriptions, large files."""
        q_missing = """
            PREFIX oe: <https://ontologist.ai/ns/oe/>
            SELECT (COUNT(DISTINCT ?m) AS ?missing) WHERE {
                ?m a oe:CodeModule .
                FILTER NOT EXISTS { ?m oe:description ?d }
            }
        """
        q_large = """
            PREFIX oe: <https://ontologist.ai/ns/oe/>
            SELECT ?m ?size WHERE {
                ?m a oe:CodeModule ; oe:fileSizeBytes ?size .
                FILTER(xsd:integer(?size) > 10000)
            } ORDER BY DESC(?size) LIMIT 5
        """
        missing = list(self._store.query(q_missing))
        large   = list(self._store.query(q_large))

        missing_count = int(missing[0].missing) if missing else 0
        large_names   = [str(r.m).split("/")[-1] for r in large]

        details = []
        if missing_count:
            details.append(f"  {missing_count} CodeModule(s) missing description (G04).")
        if large_names:
            details.append(f"  Large files (>10KB): {', '.join(large_names)}")

        summary = (
            f"Code metrics: {missing_count} missing descriptions"
            + (f", {len(large_names)} large files." if large_names else ".")
        )
        return LogicalResult(
            subtask_name=node.name, mode="sparql",
            summary=summary, details=details,
        )

    # ─────────────────────────────────────────────────────────────
    # Mode 3: owlrl reasoning + summary
    # ─────────────────────────────────────────────────────────────

    def _run_reasoning(self, node) -> LogicalResult:
        """Materialize owlrl inferences, then return a summary of new triples."""
        try:
            import owlrl
        except ImportError:
            return LogicalResult(
                subtask_name=node.name, mode="reasoning",
                summary="owlrl not installed — reasoning skipped.",
            )

        g = self._store._g
        before = len(g)
        owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)
        after  = len(g)
        new    = after - before

        summary = (
            f"Reasoning complete: {new} new triple(s) inferred "
            f"(graph: {before} → {after})."
        )
        return LogicalResult(
            subtask_name=node.name, mode="reasoning", summary=summary,
        )

    # ─────────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────────

    def format_output(self, result: LogicalResult) -> str:
        """Format LogicalResult as a human-readable string for PlanExecutor."""
        lines = [result.summary]
        lines.extend(result.details)
        return "\n".join(lines)


def _find_shapes_dir() -> Optional[Path]:
    """Walk up from execution/ to find core/shacl/."""
    here = Path(__file__).parent
    for candidate in [here.parent / "core" / "shacl",
                      Path("core/shacl")]:
        if candidate.exists():
            return candidate
    return None
