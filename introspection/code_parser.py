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
            if any(p in {".venv", "__pycache__"} for p in path.parts):
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

        rel = path.relative_to(self.root)
        module_uri = uri("module", str(rel))
        interior   = graph_uri(module_uri, "interior")

        counts = {"functions": 0, "classes": 0, "imports": 0}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                self._emit_function(node, module_uri, interior)
                counts["functions"] += 1

            elif isinstance(node, ast.ClassDef):
                self._emit_class(node, module_uri, interior)
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
                       interior: URIRef) -> None:
        # oe:CodeFunction — structural fact, NOT a pipeline TaskHolon
        fn_uri = uri("task", f"{module_uri}-{node.name}")
        self.store.add(fn_uri, RDF.type,         OE.CodeFunction,      interior)
        self.store.add(fn_uri, OE.functionName,  Literal(node.name),   interior)
        self.store.add(fn_uri, OE.definedIn,     module_uri,           interior)
        self.store.add(fn_uri, OE.lineNumber,    Literal(node.lineno), interior)

    def _emit_class(self, node: ast.ClassDef, module_uri: URIRef,
                    interior: URIRef) -> None:
        # oe:CodeClass — structural fact, NOT a Holon
        cls_uri = uri("module", f"{module_uri}/{node.name}")
        self.store.add(cls_uri, RDF.type,       OE.CodeClass,         interior)
        self.store.add(cls_uri, OE.className,   Literal(node.name),   interior)
        self.store.add(cls_uri, OE.definedIn,   module_uri,           interior)
        self.store.add(cls_uri, OE.lineNumber,  Literal(node.lineno), interior)

    def _emit_import(self, module_name: str, from_uri: URIRef,
                     interior: URIRef) -> None:
        # External packages use build: namespace; local modules use oe:module/
        if module_name.startswith((".", "storage", "introspection", "enrichment",
                                   "interaction", "verification", "context",
                                   "planning", "pipeline", "api", "visualization")):
            dep_uri = uri("module", module_name.replace(".", "/"))
        else:
            dep_uri = URIRef(f"https://ontologist.ai/ns/build#{module_name.split('.')[0]}")

        self.store.add(from_uri, OE.dependsOn, dep_uri, interior)
