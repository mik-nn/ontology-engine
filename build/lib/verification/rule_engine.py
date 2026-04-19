"""Rule Engine — Stage 5.

Two complementary rule layers:
  1. SHACL rules  — declarative, loaded from core/rules/rules.ttl,
                    evaluated via pyshacl against the graph store.
  2. Python rules — structural checks that SPARQL cannot express cleanly
                    (cycle detection, size thresholds, cross-graph checks).

Both layers return a unified RuleReport.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from rdflib import Graph, Namespace, URIRef
from pyshacl import validate as shacl_validate

from storage.graph_store import GraphStore

OE   = Namespace("https://ontologist.ai/ns/oe/")
CGA  = Namespace("https://ontologist.ai/ns/cga/")
BUILD = Namespace("https://ontologist.ai/ns/build#")
PROV = Namespace("http://www.w3.org/ns/prov#")

DEFAULT_RULES_PATH = "core/rules/rules.ttl"
DEFAULT_SHAPES = [
    "core/shacl/databook_shapes.ttl",
    "core/shacl/dependencies_shapes.ttl",
    "core/shacl/holon_shapes.ttl",
]


@dataclass
class RuleViolation:
    rule_id: str
    severity: str          # "violation" | "warning" | "info"
    subject: str           # URI string
    message: str
    source: str            # "shacl" | "python"


@dataclass
class RuleReport:
    conforms: bool
    violations: list[RuleViolation] = field(default_factory=list)
    warnings: list[RuleViolation]   = field(default_factory=list)
    infos: list[RuleViolation]      = field(default_factory=list)

    @property
    def all_issues(self) -> list[RuleViolation]:
        return self.violations + self.warnings + self.infos

    def summary(self) -> str:
        lines = [
            f"conforms : {'YES' if self.conforms else 'NO'}",
            f"violations: {len(self.violations)}",
            f"warnings  : {len(self.warnings)}",
            f"infos     : {len(self.infos)}",
        ]
        return "\n".join(lines)

    def print_all(self) -> None:
        print(self.summary())
        for v in self.all_issues:
            tag = {"violation": "[VIOLATION]", "warning": "[WARNING]",
                   "info": "[INFO]"}.get(v.severity, "[?]")
            print(f"  {tag} [{v.source}] {v.rule_id}")
            print(f"         subject: {v.subject}")
            print(f"         message: {v.message}")


class RuleEngine:
    """Evaluates both SHACL and Python rules against a GraphStore."""

    def __init__(self, store: GraphStore,
                 shapes_paths: Optional[list[str]] = None,
                 rules_path: str = DEFAULT_RULES_PATH):
        self.store = store
        self.shapes_paths = shapes_paths or DEFAULT_SHAPES
        self.rules_path = rules_path

    def run(self) -> RuleReport:
        report = RuleReport(conforms=True)

        self._run_shacl(report)
        self._run_python_rules(report)

        report.conforms = len(report.violations) == 0
        return report

    # ──────────────────────────────────────────────
    # SHACL layer
    # ──────────────────────────────────────────────

    def _run_shacl(self, report: RuleReport) -> None:
        shapes_graph = Graph()
        for p in self.shapes_paths:
            shapes_graph.parse(p, format="turtle")
        # Also load the declarative rules file
        try:
            shapes_graph.parse(self.rules_path, format="turtle")
        except FileNotFoundError:
            pass

        data_graph = self._flatten()

        conforms, results_graph, results_text = shacl_validate(
            data_graph,
            shacl_graph=shapes_graph,
            inference="rdfs",
            abort_on_first=False,
        )

        for violation in _parse_shacl_results(results_graph):
            if violation.severity == "violation":
                report.violations.append(violation)
            elif violation.severity == "warning":
                report.warnings.append(violation)
            else:
                report.infos.append(violation)

    def _flatten(self) -> Graph:
        """Merge all named graphs into a single Graph for SHACL evaluation."""
        g = Graph()
        for ctx in self.store._g.contexts():
            for triple in ctx:
                g.add(triple)
        return g

    # ──────────────────────────────────────────────
    # Python rules
    # ──────────────────────────────────────────────

    def _run_python_rules(self, report: RuleReport) -> None:
        self._rule_no_dependency_cycles(report)
        self._rule_code_modules_have_functions(report)
        self._rule_holon_interior_not_empty(report)

    def _rule_no_dependency_cycles(self, report: RuleReport) -> None:
        """P01: Detect cycles in oe:dependsOn edges (DFS)."""
        # Build adjacency from all contexts
        adj: dict[str, set[str]] = {}
        for ctx in self.store._g.contexts():
            for s, p, o in ctx:
                if str(p) == str(OE.dependsOn):
                    adj.setdefault(str(s), set()).add(str(o))

        visited: set[str] = set()
        stack: set[str] = set()
        cycles: list[list[str]] = []

        def dfs(node: str, path: list[str]) -> None:
            if node in stack:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:])
                return
            if node in visited:
                return
            visited.add(node)
            stack.add(node)
            for neighbour in adj.get(node, []):
                dfs(neighbour, path + [neighbour])
            stack.discard(node)

        for node in list(adj):
            dfs(node, [node])

        for cycle in cycles:
            short = " → ".join(_short(n) for n in cycle[:4])
            report.violations.append(RuleViolation(
                rule_id="P01",
                severity="violation",
                subject=cycle[0],
                message=f"Cycle detected in oe:dependsOn: {short} → ...",
                source="python",
            ))

    def _rule_code_modules_have_functions(self, report: RuleReport) -> None:
        """P02: CodeModule should expose at least one CodeFunction — skip __init__ stubs."""
        from rdflib import RDF
        for ctx in self.store._g.contexts():
            for module_uri in ctx.subjects(RDF.type, OE.CodeModule):
                local = str(module_uri).split("/")[-1]
                # __init__.py and similar stubs are legitimately empty
                if local in ("__init__-py", "init-py") or local.endswith("-init-py"):
                    continue
                has_fn = False
                for other_ctx in self.store._g.contexts():
                    if any(True for _ in other_ctx.triples((None, OE.definedIn, module_uri))):
                        has_fn = True
                        break
                if not has_fn:
                    report.warnings.append(RuleViolation(
                        rule_id="P02",
                        severity="warning",
                        subject=str(module_uri),
                        message="CodeModule declares no functions (may be a stub — add content or suppress).",
                        source="python",
                    ))

    def _rule_holon_interior_not_empty(self, report: RuleReport) -> None:
        """P03: Every declared interior graph should have at least one triple."""
        for ctx in self.store._g.contexts():
            for holon_uri, _, interior_uri in ctx.triples((None, CGA.hasInteriorGraph, None)):
                interior_ctx = self.store._g.get_context(interior_uri)
                if len(interior_ctx) == 0:
                    report.infos.append(RuleViolation(
                        rule_id="P03",
                        severity="info",
                        subject=str(holon_uri),
                        message="Holon interior graph is empty — no assertions written yet.",
                        source="python",
                    ))


# ──────────────────────────────────────────────────────────
# SHACL results parser
# ──────────────────────────────────────────────────────────

SH = Namespace("http://www.w3.org/ns/shacl#")

def _parse_shacl_results(results_graph: Graph) -> list[RuleViolation]:
    violations = []
    for result in results_graph.subjects(SH.resultSeverity, None):
        severity_uri = str(results_graph.value(result, SH.resultSeverity) or "")
        severity = "violation" if "Violation" in severity_uri else \
                   "warning"   if "Warning"   in severity_uri else "info"

        focus = str(results_graph.value(result, SH.focusNode) or "")
        msg   = str(results_graph.value(result, SH.resultMessage) or "")
        src   = str(results_graph.value(result, SH.sourceShape) or "")

        rule_id = _short(src) if src else "SHACL"

        violations.append(RuleViolation(
            rule_id=rule_id,
            severity=severity,
            subject=focus,
            message=msg,
            source="shacl",
        ))
    return violations


def _short(uri: str) -> str:
    """Abbreviate a URI to its local name."""
    return re.split(r"[/#]", uri)[-1] or uri
