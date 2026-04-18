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

    def parse_all(self) -> dict:
        counts = {"databooks": 0, "plain_docs": 0}
        for path in self.root.rglob("*"):
            if path.is_dir() or path.suffix.lower() not in _DOC_EXTS:
                continue
            if any(p in {".venv", "__pycache__"} for p in path.parts):
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
            # Minimal Databook from filename
            self.store.add(module_uri, DB.title,  Literal(path.stem),   interior)
            self.store.add(module_uri, DB.content, Literal(content[:500]), interior)
            return "plain"

    def _emit_databook(self, db_meta: dict, content: str,
                       module_uri: URIRef, interior: URIRef,
                       projection: URIRef) -> None:
        self.store.add(module_uri, RDF.type,    DB.Databook,                        projection)
        self.store.add(module_uri, DB.id,       Literal(str(db_meta.get("id", ""))), interior)
        self.store.add(module_uri, DB.title,    Literal(str(db_meta.get("title", ""))), interior)
        self.store.add(module_uri, DB.version,  Literal(str(db_meta.get("version", ""))), interior)
        self.store.add(module_uri, DB.type,     Literal(str(db_meta.get("type", ""))), interior)
        self.store.add(module_uri, DB.created,  Literal(str(db_meta.get("created", ""))), interior)
        self.store.add(module_uri, DB.content,  Literal(content.strip()[:2000]),    interior)

        if "license" in db_meta:
            self.store.add(module_uri, DB.license, Literal(str(db_meta["license"])), interior)

        process = db_meta.get("process", {})
        if isinstance(process, dict) and "transformer" in process:
            self.store.add(module_uri, DB.transformer,
                           Literal(str(process["transformer"])), interior)

        for a in _coerce_list(db_meta.get("author") or db_meta.get("authors", [])):
            if isinstance(a, dict):
                self.store.add(module_uri, DB.authorName, Literal(a.get("name", "")), interior)
                if "iri" in a:
                    self.store.add(module_uri, DB.authorIRI, URIRef(a["iri"]), interior)
            else:
                self.store.add(module_uri, DB.authorName, Literal(str(a)), interior)

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


def _extract_frontmatter(content: str) -> Optional[dict]:
    sep = content.find("\n---\n")
    if sep == -1:
        sep = content.find("\n---")
    if sep == -1:
        return None
    try:
        return yaml.safe_load(content[:sep])
    except yaml.YAMLError:
        return None


def _coerce_list(value) -> list:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]
