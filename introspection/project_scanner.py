from pathlib import Path
from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri, graph_uri

OE    = Namespace("https://ontologist.ai/ns/oe/")
CGA   = Namespace("https://ontologist.ai/ns/cga/")
BUILD = Namespace("https://ontologist.ai/ns/build#")
PROV  = Namespace("http://www.w3.org/ns/prov#")
XSD   = Namespace("http://www.w3.org/2001/XMLSchema#")

_SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".mypy_cache"}

_EXT_TO_CLASS = {
    ".py":    OE.CodeModule,
    ".ttl":   OE.DataModule,
    ".trig":  OE.DataModule,
    ".n3":    OE.DataModule,
    ".jsonld":OE.DataModule,
    ".md":    OE.DataModule,   # DataModules that are docs — doc_parser classifies further
    ".rst":   OE.DataModule,
    ".yaml":  OE.ConfigModule,
    ".yml":   OE.ConfigModule,
    ".toml":  OE.ConfigModule,
    ".json":  OE.ConfigModule,
    ".env":   OE.ConfigModule,
}


class ProjectScanner:
    """Stage 2 — scans the project directory and writes Module holons to the graph store.

    Each discovered file becomes an oe:ModuleHolon subtype with:
        - interior graph: file metadata (path, size, extension)
        - context graph:  cga:partOf → project holon + ModuleDetected event
    """

    def __init__(self, store: GraphStore, project_root: str):
        self.store = store
        self.root = Path(project_root).resolve()

    def scan(self) -> dict:
        project_uri = uri("project", self.root.name)
        self.store.declare_holon(project_uri, OE.ProjectHolon)
        self.store.add(project_uri, OE.rootPath, Literal(str(self.root)),
                       graph_uri(project_uri, "interior"))

        counts: dict[str, int] = {}
        for path in self._walk():
            module_uri = self._emit_module(path, project_uri)
            ext = path.suffix.lower()
            counts[ext] = counts.get(ext, 0) + 1

        self._emit_scan_event(project_uri, sum(counts.values()))
        return {"project_uri": str(project_uri), "file_counts": counts}

    def _walk(self):
        for path in sorted(self.root.rglob("*")):
            if path.is_dir():
                continue
            if any(part in _SKIP_DIRS for part in path.parts):
                continue
            yield path

    def _emit_module(self, path: Path, project_uri: URIRef) -> URIRef:
        rel = path.relative_to(self.root)
        module_uri  = uri("module", str(rel))
        module_type = _EXT_TO_CLASS.get(path.suffix.lower(), OE.DataModule)

        self.store.declare_holon(module_uri, module_type)

        interior = graph_uri(module_uri, "interior")
        self.store.add(module_uri, OE.filePath,    Literal(str(rel)),        interior)
        self.store.add(module_uri, OE.fileName,    Literal(path.name),       interior)
        self.store.add(module_uri, OE.fileExt,     Literal(path.suffix),     interior)
        self.store.add(module_uri, OE.fileSizeBytes, Literal(path.stat().st_size), interior)

        ctx = graph_uri(module_uri, "context")
        self.store.add(module_uri, CGA.partOf, project_uri, ctx)

        self._emit_module_event(module_uri, module_type)
        return module_uri

    def _emit_module_event(self, module_uri: URIRef, module_type: URIRef) -> None:
        import uuid
        from datetime import datetime, timezone

        event_uri = uri("event", f"module-detected-{uuid.uuid4().hex[:8]}")
        pipeline_interior = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")

        self.store.add(event_uri, RDF.type,        OE.ModuleDetected,              pipeline_interior)
        self.store.add(event_uri, OE.hasAgent,     Literal("IntrospectionAgent"),  pipeline_interior)
        self.store.add(event_uri, OE.hasStatus,    Literal("success"),             pipeline_interior)
        self.store.add(event_uri, OE.moduleUri,    module_uri,                     pipeline_interior)
        self.store.add(event_uri, OE.moduleType,   module_type,                    pipeline_interior)
        self.store.add(event_uri, PROV.startedAtTime,
                       Literal(datetime.now(timezone.utc).isoformat(), datatype=XSD.dateTime),
                       pipeline_interior)

    def _emit_scan_event(self, project_uri: URIRef, total: int) -> None:
        import uuid
        from datetime import datetime, timezone

        event_uri = uri("event", f"project-scanned-{uuid.uuid4().hex[:8]}")
        pipeline_interior = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")

        self.store.add(event_uri, RDF.type,        OE.ProjectScanned,              pipeline_interior)
        self.store.add(event_uri, OE.hasAgent,     Literal("IntrospectionAgent"),  pipeline_interior)
        self.store.add(event_uri, OE.hasStatus,    Literal("success"),             pipeline_interior)
        self.store.add(event_uri, OE.projectUri,   project_uri,                    pipeline_interior)
        self.store.add(event_uri, OE.moduleCount,  Literal(total),                 pipeline_interior)
        self.store.add(event_uri, PROV.startedAtTime,
                       Literal(datetime.now(timezone.utc).isoformat(), datatype=XSD.dateTime),
                       pipeline_interior)
