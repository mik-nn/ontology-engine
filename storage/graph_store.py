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

# Ontology files loaded into the reasoner base
_ONTOLOGY_FILES = [
    "core/ontology/core.ttl",
    "core/ontology/dependencies.ttl",
]


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
    # Reasoning
    # ──────────────────────────────────────────────

    def reason(self, regime: str = "RDFS") -> int:
        """Apply forward-chaining inference and materialise inferred triples.

        Regimes (owlrl):
          "RDFS"     — rdfs:subClassOf transitivity, rdfs:domain/range, rdfs:subPropertyOf
          "OWL_RL"   — RDFS + owl:inverseOf, owl:TransitiveProperty, property chains
          "RDFS_OWL" — full OWL-RL closure

        Returns the number of newly inferred triples added.

        Inferred triples land in a dedicated named graph
        <urn:oe:inferred> so they can be distinguished from asserted facts.
        """
        import owlrl

        # Flatten the ConjunctiveGraph into a single Graph for owlrl
        flat = Graph()
        for ctx in self._g.contexts():
            for triple in ctx:
                flat.add(triple)

        # Load ontology TBox so the reasoner knows the class/property hierarchy
        for path in _ONTOLOGY_FILES:
            p = Path(path)
            if p.exists():
                flat.parse(str(p), format="turtle")

        before = len(flat)

        closure_cls = {
            "RDFS":     owlrl.RDFSClosure.RDFS_Semantics,
            "OWL_RL":   owlrl.OWLRL_Semantics,
            "RDFS_OWL": owlrl.RDFS_OWLRL_Semantics,
        }.get(regime, owlrl.RDFSClosure.RDFS_Semantics)

        owlrl.DeductiveClosure(closure_cls).expand(flat)

        after = len(flat)
        new_triples = after - before

        # Write inferred triples into a dedicated named graph
        inferred_graph = URIRef("urn:oe:inferred")
        ctx = self._g.get_context(inferred_graph)
        existing = set(self._g)
        for triple in flat:
            if triple not in existing:
                ctx.add(triple)

        return new_triples

    def is_inferred(self, s: Node, p: Node, o: Node) -> bool:
        """Return True if this triple exists only in the inferred graph (not asserted)."""
        inferred_graph = URIRef("urn:oe:inferred")
        return (s, p, o) in self._g.get_context(inferred_graph)

    def module_for_file(self, abs_path: str) -> Optional[URIRef]:
        """Return the oe:CodeModule URI for an absolute file path, or None.

        Relies on oe:absolutePath written by CodeParser._parse_file().
        Enables bidirectional code ↔ holon mapping:
          code file → holon:  module_for_file(path)
          holon → code file:  store.value(module_uri, OE.absolutePath)
        """
        sparql = (
            "PREFIX oe: <https://ontologist.ai/ns/oe/>\n"
            "SELECT ?m WHERE {\n"
            f'  ?m oe:absolutePath "{abs_path}" .\n'
            "} LIMIT 1"
        )
        for row in self._g.query(sparql):
            return row.m
        return None

    def public_api(self, module_uri: URIRef) -> list[tuple[str, str]]:
        """Return [(name, type)] of public exports from the module's projection graph.

        type is either 'function' or 'class'.
        """
        proj = URIRef(str(module_uri) + "/projection")
        sparql = (
            "PREFIX oe: <https://ontologist.ai/ns/oe/>\n"
            "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
            f"SELECT ?name ?kind WHERE {{\n"
            f"  GRAPH <{proj}> {{\n"
            "    ?m oe:exports ?sym .\n"
            "    OPTIONAL { ?sym oe:functionName ?fname }\n"
            "    OPTIONAL { ?sym oe:className    ?cname }\n"
            "    BIND(COALESCE(?fname, ?cname) AS ?name)\n"
            "    ?sym rdf:type ?kind .\n"
            "  }\n"
            "}"
        )
        results = []
        for row in self._g.query(sparql):
            kind_local = str(row.kind).split("/")[-1].split("#")[-1]
            results.append((str(row.name), kind_local))
        return results

    def subclasses_of(self, class_uri: URIRef) -> list[URIRef]:
        """SPARQL query for all subclasses (direct + transitive via inferred graph).

        Requires reason() to have been called first for transitive closure.
        """
        sparql = f"""
            SELECT DISTINCT ?sub WHERE {{
                ?sub <{RDF.type}> <{OWL.Class}> .
                ?sub <{URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf')}> <{class_uri}> .
            }}
        """
        return [row.sub for row in self._g.query(sparql)]

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
