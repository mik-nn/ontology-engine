from pathlib import Path
from typing import Optional

import yaml
from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri, graph_uri

OE  = Namespace("https://ontologist.ai/ns/oe/")
CGA = Namespace("https://ontologist.ai/ns/cga/")
DB  = Namespace("https://ontologist.ai/ns/databook#")
PROV = Namespace("http://www.w3.org/ns/prov#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

_DOC_EXTS = {".md", ".rst", ".txt"}


class DocParser:
    """Stage 2 — parses documentation files into db:Databook nodes.

    For each doc file in the project:
        - if it has YAML frontmatter with a 'databook' key → full Databook
        - otherwise → lightweight Databook with title inferred from filename

    Writes to the module's interior graph and the pipeline's interior graph (events).
    Classifies the DataModule holon as db:Databook in projection graph.
    """

    def __init__(self, store: GraphStore, project_root: str):
        self.store = store
        self.root = Path(project_root).resolve()

    # Directories treated as read-only source material — parsed for content
    # but never registered as managed db:Databook nodes in the graph.
    _SOURCE_DIRS = {"docs/guides", "docs/sources"}

    def parse_all(self) -> dict:
        counts = {"databooks": 0, "plain_docs": 0, "sources": 0}
        _SKIP_DIRS = {".venv", "__pycache__", ".git", ".kilo",
                      "node_modules", "dist", ".eggs", "ontology_engine.egg-info"}
        for path in self.root.rglob("*"):

            if path.is_dir() or path.suffix.lower() not in _DOC_EXTS:
                continue
            if any(p in _SKIP_DIRS for p in path.parts):
                continue
            try:
                rel = path.relative_to(self.root)
            except ValueError:
                continue
            # Skip guide/source directories — they are read-only reference material
            rel_str = rel.as_posix()
            if any(rel_str.startswith(src + "/") for src in self._SOURCE_DIRS):
                counts["sources"] += 1
                continue
            result = self._parse_file(path)
            if result == "databook":
                counts["databooks"] += 1
            else:
                counts["plain_docs"] += 1
        return counts

    def parse_file(self, path: str) -> str:
        return self._parse_file(Path(path).resolve())

    def _parse_file(self, path: Path) -> str:
        rel = path.relative_to(self.root)
        module_uri = uri("module", str(rel))
        interior   = graph_uri(module_uri, "interior")
        projection = graph_uri(module_uri, "projection")

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return "skip"

        meta = _extract_frontmatter(content)

        if meta and "databook" in meta:
            db_meta = meta["databook"]
            self._emit_databook(db_meta, content, module_uri, interior, projection)
            self._emit_databook_event(module_uri, db_meta.get("id", str(rel)))
            return "databook"
        else:
            # Minimal Databook from filename — registered so ContextBuilder and DocSync can find it
            title = _infer_title(path)
            self.store.add(module_uri, RDF.type,   OE.Databook,             projection)
            self.store.add(module_uri, RDF.type,   DB.Databook,             projection)
            self.store.add(module_uri, DB.id,      Literal(_slugify_id(path.stem)), interior)
            self.store.add(module_uri, DB.version, Literal("0.1"),          interior)
            self.store.add(module_uri, DB.type,    Literal("plain-doc"),    interior)
            self.store.add(module_uri, DB.created, Literal(_file_date(path)), interior)
            self.store.add(module_uri, DB.title,   Literal(title),          interior)
            self.store.add(module_uri, DB.content, Literal(_strip_frontmatter(content)), interior)
            # Auto-assign classification defaults for undeclared docs
            self.store.add(module_uri, DB.scope,       Literal("project"),  interior)
            self.store.add(module_uri, DB.layer,       Literal("meta"),     interior)
            self.store.add(module_uri, DB.hierarchy,
                           Literal(3, datatype=XSD.integer),                interior)
            self.store.add(module_uri, DB.transformer, Literal("human"),    interior)
            return "plain"

    def _emit_databook(self, db_meta: dict, content: str,
                       module_uri: URIRef, interior: URIRef,
                       projection: URIRef) -> None:
        self.store.add(module_uri, RDF.type,    OE.Databook,                        projection)
        self.store.add(module_uri, RDF.type,    DB.Databook,                        projection)
        self.store.add(module_uri, DB.id,       Literal(_slugify_id(str(db_meta.get("id", "")))), interior)
        self.store.add(module_uri, DB.title,    Literal(str(db_meta.get("title", ""))), interior)
        self.store.add(module_uri, DB.version,  Literal(str(db_meta.get("version", ""))), interior)
        self.store.add(module_uri, DB.type,     Literal(str(db_meta.get("type", ""))), interior)
        self.store.add(module_uri, DB.created,  Literal(str(db_meta.get("created", ""))), interior)
        body = _strip_frontmatter(content)
        self.store.add(module_uri, DB.content,  Literal(body),                      interior)

        if "license" in db_meta:
            self.store.add(module_uri, DB.license, Literal(str(db_meta["license"])), interior)

        process = db_meta.get("process", {})
        transformer = process.get("transformer") if isinstance(process, dict) else None
        if not transformer:
            # Infer from scope: permanent/project → human; task → llm; ephemeral → sparql
            scope_val = db_meta.get("scope", "project")
            transformer = {"task": "llm", "ephemeral": "sparql"}.get(scope_val, "human")
        self.store.add(module_uri, DB.transformer, Literal(transformer), interior)

        for a in _coerce_list(db_meta.get("author") or db_meta.get("authors", [])):
            if isinstance(a, dict):
                self.store.add(module_uri, DB.authorName, Literal(a.get("name", "")), interior)
                if "iri" in a:
                    self.store.add(module_uri, DB.authorIRI, URIRef(a["iri"]), interior)
            else:
                self.store.add(module_uri, DB.authorName, Literal(str(a)), interior)

        # ── Classification fields (scope / layer / hierarchy / task routing) ──
        scope = db_meta.get("scope")
        if scope:
            self.store.add(module_uri, DB.scope, Literal(str(scope)), interior)

        layer = db_meta.get("layer")
        if layer:
            self.store.add(module_uri, DB.layer, Literal(str(layer)), interior)

        hierarchy = db_meta.get("hierarchy")
        if hierarchy is not None:
            self.store.add(module_uri, DB.hierarchy,
                           Literal(int(hierarchy), datatype=XSD.integer), interior)

        task_types = _coerce_list(db_meta.get("task_types") or [])
        if task_types:
            joined = ",".join(str(t) for t in task_types)
            self.store.add(module_uri, DB.taskType, Literal(joined), interior)

        # depends_on: accepts either a full module URI or a bare sibling ID
        for dep_id in _coerce_list(db_meta.get("depends_on") or []):
            if str(dep_id).startswith("http"):
                dep_uri = URIRef(dep_id)
            else:
                dep_uri = uri("module", f"docs/databooks/{dep_id}.md")
            self.store.add(module_uri, DB.dependsOn, dep_uri, interior)

    def _emit_databook_event(self, module_uri: URIRef, doc_id: str) -> None:
        import uuid
        from datetime import datetime, timezone

        event_uri = uri("event", f"databook-updated-{uuid.uuid4().hex[:8]}")
        pipeline_interior = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")

        self.store.add(event_uri, RDF.type,        OE.DatabookUpdated,             pipeline_interior)
        self.store.add(event_uri, OE.hasAgent,     Literal("IntrospectionAgent"),  pipeline_interior)
        self.store.add(event_uri, OE.hasStatus,    Literal("success"),             pipeline_interior)
        self.store.add(event_uri, OE.databookUri,  module_uri,                     pipeline_interior)
        self.store.add(event_uri, PROV.startedAtTime,
                       Literal(datetime.now(timezone.utc).isoformat(), datatype=XSD.dateTime),
                       pipeline_interior)


def _slugify_id(raw: str) -> str:
    """Normalize a Databook id to a safe slug (no spaces, commas, or special chars)."""
    import re
    s = raw.strip()
    s = re.sub(r"[^\w\s.\-]", "-", s)   # replace all non-slug chars with hyphens
    s = re.sub(r"\s+", "-", s)           # spaces → hyphens
    s = re.sub(r"-{2,}", "-", s)         # collapse multiple hyphens
    s = s.strip("-")
    return s[:100]


def _infer_title(path: Path) -> str:
    """Human-readable title from file stem (kebab/snake → Title Case words)."""
    import re
    stem = path.stem
    words = re.split(r"[-_]", stem)
    return " ".join(w.capitalize() for w in words if w)


def _file_date(path: Path) -> str:
    """ISO date string from file mtime, or today as fallback."""
    from datetime import date
    try:
        return date.fromtimestamp(path.stat().st_mtime).isoformat()
    except OSError:
        return date.today().isoformat()


def _extract_frontmatter(content: str) -> Optional[dict]:
    """Merge all ---/--- segments near file start — handles accumulated corrupted blocks."""
    import re
    segments = re.split(r'(?m)^---$', content)
    merged: dict = {}
    for seg in segments:  # scan all segments until markdown content
        seg_stripped = seg.strip()
        if not seg_stripped:
            continue
        if seg_stripped.lstrip().startswith('#'):  # reached Markdown content
            break
        try:
            parsed = yaml.safe_load(seg_stripped)
            if isinstance(parsed, dict) and parsed:
                merged.update(parsed)
        except yaml.YAMLError:
            pass
    return merged if merged else None


def _strip_frontmatter(content: str) -> str:
    """Return markdown body with all leading YAML frontmatter blocks removed."""
    lines = content.split('\n')
    last_sep = -1
    for i, line in enumerate(lines[:150]):  # only scan first 150 lines
        if line.strip() == '---':
            last_sep = i
    if last_sep >= 0:
        body = '\n'.join(lines[last_sep + 1:])
        return body.lstrip('\n')
    return content


def _coerce_list(value) -> list:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]
