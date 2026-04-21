"""Stage 8 — DocSync.

Reads entity state from the graph and regenerates Markdown Databook files.
Only syncs entities whose graph state has changed since last sync.
LLM does not write files — this module is the only file writer.
"""
from __future__ import annotations

import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from rdflib import Namespace, URIRef

from storage.graph_store import GraphStore
from pipeline.event_logger import EventLogger

OE   = Namespace("https://ontologist.ai/ns/oe/")
DB   = Namespace("https://ontologist.ai/ns/databook#")
PROV = Namespace("http://www.w3.org/ns/prov#")

DOCS_DIR = Path("docs/databooks")


class DocSync:
    """Syncs graph entity state back to Markdown Databook files."""

    def __init__(self, store: GraphStore, logger: EventLogger):
        self.store = store
        self.logger = logger
        DOCS_DIR.mkdir(parents=True, exist_ok=True)

    def sync_all(self) -> list[str]:
        """Sync all Databook entities in graph → Markdown. Returns list of written paths."""
        written = []
        for databook_uri in self._find_databooks():
            path = self._sync_databook(databook_uri)
            if path:
                written.append(path)
        return written

    def sync_entity(self, entity_uri: str) -> Optional[str]:
        """Sync one entity by URI. Returns path written or None."""
        uri = URIRef(entity_uri)
        return self._sync_databook(uri)

    # Paths that are read-only source material — never sync these back to docs/databooks/
    _SOURCE_PATH_SEGMENTS = ("docs-guides-", "docs/guides/")

    def _find_databooks(self) -> list[URIRef]:
        from rdflib import RDF
        uris = []
        for s in self.store._g.subjects(RDF.type, DB.Databook):
            uri_str = str(s)
            if any(seg in uri_str for seg in self._SOURCE_PATH_SEGMENTS):
                continue   # skip source-material nodes; they must not overwrite databooks
            uris.append(s)
        return uris

    def _sync_databook(self, uri: URIRef) -> Optional[str]:
        g = self.store._g

        def val(pred):
            v = g.value(uri, pred)
            return str(v) if v else None

        db_id    = val(DB.id)
        title    = val(DB.title)
        version  = val(DB.version)
        db_type  = val(DB.type)
        created  = val(DB.created)
        content  = val(DB.content)
        transformer = val(DB.transformer)
        scope    = val(DB.scope)
        layer    = val(DB.layer)
        hierarchy_v = g.value(uri, DB.hierarchy)
        task_type = val(DB.taskType)
        depends_on = [str(o) for o in g.objects(uri, DB.dependsOn)]

        if not (db_id and title):
            return None

        slug = _make_slug(db_id)
        out_path = DOCS_DIR / f"{slug}.md"

        db_meta: dict = {"id": db_id, "title": title}
        if version:
            db_meta["version"] = version
        if db_type:
            db_meta["type"] = db_type
        if scope:
            db_meta["scope"] = scope
        if layer:
            db_meta["layer"] = layer
        if hierarchy_v is not None:
            db_meta["hierarchy"] = int(hierarchy_v)
        if task_type:
            db_meta["task_types"] = [t.strip() for t in task_type.split(",") if t.strip()]
        if depends_on:
            db_meta["depends_on"] = sorted(depends_on)
        if created:
            db_meta["created"] = created
        if transformer:
            db_meta["process"] = {"transformer": transformer}
        db_meta["synced_at"] = datetime.now(timezone.utc).isoformat()

        frontmatter = yaml.dump(
            {"databook": db_meta}, allow_unicode=True, default_flow_style=False
        ).strip()

        # Body resolution: always prefer the longer version (disk > graph).
        # This preserves human edits and restored guide content over the
        # graph's potentially-stale snapshot.
        graph_body = _strip_frontmatter(content) if content else ""
        if out_path.exists():
            existing = out_path.read_text(encoding="utf-8")
            disk_body = _strip_frontmatter(existing)
            body = disk_body if len(disk_body) >= len(graph_body) else graph_body
        else:
            body = graph_body

        if not body.strip():
            body = f"# {title}\n\n*Synced from ontology graph.*\n"
        elif not body.lstrip().startswith('#'):
            body = f"# {title}\n\n{body}"

        text = f"---\n{frontmatter}\n---\n\n{body}\n"
        out_path.write_text(text, encoding="utf-8")

        self.logger.log(
            "DocumentationSynced",
            agent="DocSync",
            status="synced",
            databookUri=uri,
            outputPath=str(out_path),
        )

        return str(out_path)


def _make_slug(db_id: str) -> str:
    """Convert a Databook id to a safe filesystem slug."""
    import re
    s = db_id.strip()
    s = re.sub(r"[^\w\s.\-]", "-", s)   # replace all non-slug chars with hyphens
    s = re.sub(r"\s+", "-", s)           # spaces → hyphens
    s = re.sub(r"-{2,}", "-", s)         # collapse multiple hyphens
    s = s.strip("-")
    return s[:100]


def _strip_frontmatter(content: str) -> str:
    """Return markdown body with all leading YAML frontmatter blocks removed."""
    lines = content.split('\n')
    last_sep = -1
    for i, line in enumerate(lines[:150]):
        if line.strip() == '---':
            last_sep = i
    if last_sep >= 0:
        body = '\n'.join(lines[last_sep + 1:])
        return body.lstrip('\n')
    return content
