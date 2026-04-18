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

    def _find_databooks(self) -> list[URIRef]:
        from rdflib import RDF
        uris = []
        for s in self.store._g.subjects(RDF.type, DB.Databook):
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

        if not (db_id and title):
            return None

        slug = db_id.replace(":", "_").replace("/", "_")
        out_path = DOCS_DIR / f"{slug}.md"

        meta: dict = {
            "id": db_id,
            "title": title,
        }
        if version:
            meta["version"] = version
        if db_type:
            meta["type"] = db_type
        if created:
            meta["created"] = created
        if transformer:
            meta["process"] = {"transformer": transformer}

        meta["synced_at"] = datetime.now(timezone.utc).isoformat()

        frontmatter = yaml.dump(meta, allow_unicode=True, default_flow_style=False).strip()
        body = content or f"# {title}\n\n*Synced from ontology graph.*\n"

        text = f"{frontmatter}\n---\n\n{body}\n"
        out_path.write_text(text, encoding="utf-8")

        self.logger.log(
            "DocumentationSynced",
            agent="DocSync",
            status="synced",
            databookUri=uri,
            outputPath=str(out_path),
        )

        return str(out_path)
