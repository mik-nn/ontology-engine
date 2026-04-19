from pathlib import Path
from typing import Optional

from rdflib import ConjunctiveGraph, Graph, Namespace, URIRef, Literal, RDF, OWL
from rdflib.term import Node
from pyshacl import validate

CGA  = Namespace("https://ontologist.ai/ns/cga/")
OE   = Namespace("https://ontologist.ai/ns/oe/")
BUILD = Namespace("https://ontologist.ai/ns/build#")
DB   = Namespace("https://ontologist.ai/ns/databook#")
PROV = Namespace("http://www.w3.org/ns/prov#")


class GraphStore:
    """ConjunctiveGraph wrapper that models the Holon four-graph architecture.

    Each holon IRI has four associated named graphs:
        <holon>/interior   — authoritative assertions
        <holon>/boundary   — SHACL shapes (loaded separately, not modified here)
        <holon>/projection — curated outward view
        <holon>/context    — provenance and structural membership
    """

    def __init__(self):
        self._g = ConjunctiveGraph()
        self._bind_namespaces()

    def _bind_namespaces(self):
        self._g.bind("cga",   CGA)
        self._g.bind("oe",    OE)
        self._g.bind("build", BUILD)
        self._g.bind("db",    DB)
        self._g.bind("prov",  PROV)

    # ──────────────────────────────────────────────
    # Write
    # ──────────────────────────────────────────────

    def add(self, s: Node, p: Node, o: Node, graph: Optional[URIRef] = None) -> None:
        ctx = self._g.get_context(graph) if graph else self._g
        ctx.add((s, p, o))

    def add_many(self, triples: list[tuple], graph: Optional[URIRef] = None) -> None:
        ctx = self._g.get_context(graph) if graph else self._g
        for triple in triples:
            ctx.add(triple)

    def declare_holon(self, holon_uri: URIRef, holon_type: URIRef) -> None:
        """Assert type + four-graph structure for a holon in its own context graph."""
        ctx_graph = URIRef(str(holon_uri) + "/context")
        interior  = URIRef(str(holon_uri) + "/interior")
        boundary  = URIRef(str(holon_uri) + "/boundary")
        projection = URIRef(str(holon_uri) + "/projection")

        self.add(holon_uri, RDF.type,              holon_type,      ctx_graph)
        self.add(holon_uri, CGA.hasInteriorGraph,  interior,        ctx_graph)
        self.add(holon_uri, CGA.hasBoundaryGraph,  boundary,        ctx_graph)
        self.add(holon_uri, CGA.hasProjectionGraph, projection,     ctx_graph)
        self.add(holon_uri, CGA.hasContextGraph,   ctx_graph,       ctx_graph)

    # ──────────────────────────────────────────────
    # Read
    # ──────────────────────────────────────────────

    def interior(self, holon_uri: URIRef) -> Graph:
        return self._g.get_context(URIRef(str(holon_uri) + "/interior"))

    def projection(self, holon_uri: URIRef) -> Graph:
        return self._g.get_context(URIRef(str(holon_uri) + "/projection"))

    def query(self, sparql: str):
        return self._g.query(sparql)

    def value(self, s: Node, p: Node, graph: Optional[URIRef] = None):
        ctx = self._g.get_context(graph) if graph else self._g
        return ctx.value(s, p)

    def subjects(self, predicate=None, obj=None, graph: Optional[URIRef] = None):
        ctx = self._g.get_context(graph) if graph else self._g
        return ctx.subjects(predicate, obj)

    # ──────────────────────────────────────────────
    # Persistence
    # ──────────────────────────────────────────────

    def save(self, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._g.serialize(path, format="trig")

    def load(self, path: str) -> None:
        self._g.parse(path, format="trig")

    def load_turtle(self, path: str, graph: Optional[URIRef] = None) -> None:
        g = Graph()
        g.parse(path, format="turtle")
        ctx = self._g.get_context(graph) if graph else self._g
        for triple in g:
            ctx.add(triple)

    # ──────────────────────────────────────────────
    # Validation
    # ──────────────────────────────────────────────

    def validate(self, shapes_paths: list[str]) -> tuple[bool, str]:
        """Run pyshacl. conforms=True when there are no sh:Violation results.
        sh:Warning and sh:Info results do not affect conforms (SHACL spec §3.4)."""
        from rdflib import SH
        shapes_graph = Graph()
        for p in shapes_paths:
            shapes_graph.parse(p, format="turtle")

        data_graph = Graph()
        for ctx in self._g.contexts():
            for triple in ctx:
                data_graph.add(triple)

        _, results_graph, report_text = validate(
            data_graph,
            shacl_graph=shapes_graph,
            inference="rdfs",
            abort_on_first=False,
        )

        # pyshacl returns conforms=False for sh:Warning too — we follow the spec:
        # only sh:Violation makes the graph non-conforming.
        violations = list(results_graph.subjects(SH.resultSeverity, SH.Violation))
        conforms = len(violations) == 0
        return conforms, report_text

    # ──────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────

    def __len__(self) -> int:
        return sum(1 for _ in self._g)

    def __repr__(self) -> str:
        return f"GraphStore({len(self)} triples, {len(list(self._g.contexts()))} graphs)"
