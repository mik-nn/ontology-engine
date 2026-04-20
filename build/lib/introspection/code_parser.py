import ast
from pathlib import Path

from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri, graph_uri

OE   = Namespace("https://ontologist.ai/ns/oe/")
CGA  = Namespace("https://ontologist.ai/ns/cga/")
PROV = Namespace("http://www.w3.org/ns/prov#")
XSD  = Namespace("http://www.w3.org/2001/XMLSchema#")


class CodeParser:
    """Stage 2 — AST analysis of Python files.

    For each .py file already registered as an oe:CodeModule in the store:
        - extracts class names → oe:AnalysisTask (design-time fact)
        - extracts function names → oe:Task nodes with oe:definedIn
        - extracts import names → oe:dependsOn edges between modules

    Writes to the module's interior graph.
    """

    def __init__(self, store: GraphStore, project_root: str):
        self.store = store
        self.root = Path(project_root).resolve()

    def parse_all(self) -> dict:
        counts = {"functions": 0, "classes": 0, "imports": 0}
        for path in self.root.rglob("*.py"):
            if any(p in {".venv", "__pycache__", ".kilo", ".git", "build", "dist", ".eggs"} for p in path.parts):
                continue
            c = self._parse_file(path)
            for k in counts:
                counts[k] += c.get(k, 0)
        return counts

    def parse_file(self, path: str) -> dict:
        return self._parse_file(Path(path).resolve())

    def _parse_file(self, path: Path) -> dict:
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except (SyntaxError, UnicodeDecodeError):
            return {}

        rel        = path.relative_to(self.root)
        module_uri = uri("module", str(rel))
        interior   = graph_uri(module_uri, "interior")
        projection = graph_uri(module_uri, "projection")
        mod_ctx    = graph_uri(module_uri, "context")

        counts = {"functions": 0, "classes": 0, "imports": 0}

        # ── Reverse mapping: absolute path → module URI (queryable via SPARQL)
        self.store.add(module_uri, OE.absolutePath,
                       Literal(str(path)), interior)

        # ── Module docstring → description
        docstring = ast.get_docstring(tree)
        if docstring:
            self.store.add(module_uri, OE.description,
                           Literal(docstring.strip()[:500]), interior)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                self._emit_function(node, module_uri, interior, projection)
                counts["functions"] += 1

            elif isinstance(node, ast.ClassDef):
                self._emit_class(node, module_uri, interior, projection)
                counts["classes"] += 1

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self._emit_import(alias.name, module_uri, interior)
                    counts["imports"] += 1

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self._emit_import(node.module, module_uri, interior)
                    counts["imports"] += 1

        return counts

    def _emit_function(self, node: ast.FunctionDef, module_uri: URIRef,
                       interior: URIRef, projection: URIRef) -> None:
        fn_uri = uri("task", f"{module_uri}-{node.name}")
        self.store.add(fn_uri, RDF.type,         OE.CodeFunction,      interior)
        self.store.add(fn_uri, OE.functionName,  Literal(node.name),   interior)
        self.store.add(fn_uri, OE.definedIn,     module_uri,           interior)
        self.store.add(fn_uri, OE.lineNumber,    Literal(node.lineno), interior)
        # Holon membership: function belongs to its module holon
        self.store.add(fn_uri, CGA.partOf,       module_uri,           interior)

        # Public API → projection graph (non-private, non-dunder)
        if not node.name.startswith("_"):
            self.store.add(module_uri, OE.exports,      fn_uri,               projection)
            self.store.add(fn_uri,     RDF.type,         OE.CodeFunction,      projection)
            self.store.add(fn_uri,     OE.functionName,  Literal(node.name),   projection)

    def _emit_class(self, node: ast.ClassDef, module_uri: URIRef,
                    interior: URIRef, projection: URIRef) -> None:
        cls_uri = uri("module", f"{module_uri}/{node.name}")
        self.store.add(cls_uri, RDF.type,       OE.CodeClass,         interior)
        self.store.add(cls_uri, OE.className,   Literal(node.name),   interior)
        self.store.add(cls_uri, OE.definedIn,   module_uri,           interior)
        self.store.add(cls_uri, OE.lineNumber,  Literal(node.lineno), interior)
        # Holon membership
        self.store.add(cls_uri, CGA.partOf,     module_uri,           interior)

        # Public classes → projection graph
        if not node.name.startswith("_"):
            self.store.add(module_uri, OE.exports,   cls_uri,              projection)
            self.store.add(cls_uri,    OE.className, Literal(node.name),   projection)

    def _emit_import(self, module_name: str, from_uri: URIRef,
                     interior: URIRef) -> None:
        if module_name.startswith((".", "storage", "introspection", "enrichment",
                                   "interaction", "verification", "context",
                                   "planning", "pipeline", "api", "visualization")):
            dep_uri = uri("module", module_name.replace(".", "/"))
        else:
            dep_uri = URIRef(f"https://ontologist.ai/ns/build#{module_name.split('.')[0]}")

        self.store.add(from_uri, OE.dependsOn, dep_uri, interior)
