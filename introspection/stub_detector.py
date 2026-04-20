"""Stage 2 — StubDetector.

Scans each Python file using AST to find incomplete implementations:
  - functions/methods whose body is a stub (pass, NotImplementedError, stub string)
  - # TODO / # FIXME / # AI-TODO inline comments
  - docstring-level "Stage N will ..." markers

Each finding is stored as oe:AITodo in the module's interior graph.
LLM executor reads these to prioritise what to implement next.
"""
from __future__ import annotations

import ast
import re
import tokenize
import io
from pathlib import Path

from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri as make_uri, graph_uri

OE = Namespace("https://ontologist.ai/ns/oe/")

_SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".mypy_cache", ".kilo", "build", "dist", ".eggs", ".github"}

# Patterns that mark a comment as an AI-Todo
_COMMENT_RE = re.compile(r"#\s*(TODO|FIXME|AI-TODO|HACK|STAGE\s+\d+:)[:\s]*(.*)", re.IGNORECASE)

# Markers in RETURN string values that mean the function IS a stub (not talks about stubs)
_STUB_RETURN_MARKERS = {
    "executor stub",
    "stage 8 wires",
    "stage 8 will",
    "not yet implemented",
    "wire real",
    "will replace",
    "wires gitag",
}


def _is_abstract(func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Return True if decorated with @abstractmethod or @property+@abstractmethod."""
    for dec in func_node.decorator_list:
        name = getattr(dec, "id", None) or getattr(dec, "attr", None) or ""
        if name == "abstractmethod":
            return True
    return False


def _is_stub_body(func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[bool, str]:
    """Return (is_stub, reason) for a function AST node."""
    if _is_abstract(func_node):
        return False, ""
    body = func_node.body
    # Strip leading docstring for body-length check
    effective_body = body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        effective_body = body[1:]

    # Empty after stripping docstring
    if not effective_body:
        return True, "empty body (pass/docstring only)"

    # Single effective statement
    if len(effective_body) == 1:
        stmt = effective_body[0]

        # pass or ...
        if isinstance(stmt, ast.Pass):
            return True, "empty body (pass)"
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
            val = str(stmt.value.value)
            if val == "...":
                return True, "empty body (...)"

        # raise NotImplementedError(...)
        if isinstance(stmt, ast.Raise):
            exc = stmt.exc
            if exc and isinstance(exc, ast.Call):
                if getattr(exc.func, "id", "") == "NotImplementedError":
                    return True, "raises NotImplementedError"

        # return "... executor stub ..." — only return-level strings count
        if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Constant):
            val = str(stmt.value.value).lower()
            if any(m in val for m in _STUB_RETURN_MARKERS):
                return True, f"stub return: {stmt.value.value[:80]}"

    # Multi-statement: check all return statements for stub markers
    for node in ast.walk(ast.Module(body=effective_body, type_ignores=[])):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
            val = str(node.value.value).lower()
            if any(m in val for m in _STUB_RETURN_MARKERS):
                return True, f"stub return: {node.value.value[:80]}"

        # f-string returns: look for JoinedStr with stub markers
        if isinstance(node, ast.Return) and isinstance(node.value, ast.JoinedStr):
            parts = []
            for v in node.value.values:
                if isinstance(v, ast.Constant):
                    parts.append(str(v.value).lower())
            joined = " ".join(parts)
            if any(m in joined for m in _STUB_RETURN_MARKERS):
                return True, f"stub f-string return: {joined[:80]}"

    return False, ""


def _extract_comments(source: str) -> list[tuple[int, str, str]]:
    """Return list of (line_no, tag, text) for TODO/FIXME/AI-TODO comments."""
    results = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for tok_type, tok_str, (srow, _), _, _ in tokens:
            if tok_type == tokenize.COMMENT:
                m = _COMMENT_RE.match(tok_str)
                if m:
                    results.append((srow, m.group(1).upper(), m.group(2).strip()))
    except tokenize.TokenError:
        pass
    return results


class StubDetector:
    """Detects stub/incomplete code and writes oe:AITodo nodes to the graph."""

    def __init__(self, store: GraphStore, project_root: str):
        self.store = store
        self.root = Path(project_root).resolve()

    def detect_all(self) -> dict:
        counts = {"stubs": 0, "todos": 0}
        for path in self.root.rglob("*.py"):
            if any(p in _SKIP_DIRS for p in path.parts):
                continue
            c = self._detect_file(path)
            counts["stubs"] += c["stubs"]
            counts["todos"] += c["todos"]
        return counts

    def _detect_file(self, path: Path) -> dict:
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except (SyntaxError, UnicodeDecodeError):
            return {"stubs": 0, "todos": 0}

        rel = path.relative_to(self.root)
        module_uri = make_uri("module", str(rel))
        interior = graph_uri(module_uri, "interior")

        counts = {"stubs": 0, "todos": 0}

        # --- Function/method stubs ---
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                is_stub, reason = _is_stub_body(node)
                if is_stub:
                    self._emit_aitodo(
                        module_uri=module_uri,
                        interior=interior,
                        rel_path=str(rel),
                        line=node.lineno,
                        stub_type="function_stub",
                        function_name=node.name,
                        description=f"{node.name}(): {reason}",
                        priority=self._priority(reason),
                    )
                    counts["stubs"] += 1

        # --- TODO/FIXME comments ---
        for line_no, tag, text in _extract_comments(source):
            self._emit_aitodo(
                module_uri=module_uri,
                interior=interior,
                rel_path=str(rel),
                line=line_no,
                stub_type="todo_comment",
                function_name=None,
                description=f"{tag}: {text}" if text else tag,
                priority="medium" if tag in ("TODO", "FIXME") else "high",
            )
            counts["todos"] += 1

        return counts

    def _priority(self, reason: str) -> str:
        if "stage 8" in reason.lower() or "wire real" in reason.lower():
            return "high"
        if "not implemented" in reason.lower():
            return "high"
        if "pass" in reason.lower():
            return "low"
        return "medium"

    def _emit_aitodo(
        self,
        module_uri: URIRef,
        interior: URIRef,
        rel_path: str,
        line: int,
        stub_type: str,
        function_name: str | None,
        description: str,
        priority: str,
    ) -> None:
        slug = f"{rel_path.replace('/', '-').replace('.', '-')}-{line}"
        todo_uri = make_uri("aitodo", slug)

        self.store.add(todo_uri, RDF.type,          OE.AITodo,             interior)
        self.store.add(todo_uri, OE.inModule,        module_uri,            interior)
        self.store.add(todo_uri, OE.filePath,        Literal(rel_path),     interior)
        self.store.add(todo_uri, OE.lineNumber,      Literal(line),         interior)
        self.store.add(todo_uri, OE.stubType,        Literal(stub_type),    interior)
        self.store.add(todo_uri, OE.description,     Literal(description),  interior)
        self.store.add(todo_uri, OE.priority,        Literal(priority),     interior)
        self.store.add(todo_uri, OE.status,          Literal("open"),       interior)

        if function_name:
            self.store.add(todo_uri, OE.functionName, Literal(function_name), interior)

        # back-link from module
        self.store.add(module_uri, OE.hasAITodo, todo_uri, interior)
