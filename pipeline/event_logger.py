"""Stage 8 — EventLogger.

Writes pipeline events to:
  1. The main GraphStore (PIPE interior graph)
  2. Daily log files at logs/events/YYYY-MM-DD.trig
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from rdflib import Namespace, RDF, Literal, URIRef, ConjunctiveGraph

from storage.graph_store import GraphStore
from storage.id_manager import uri as make_uri

OE   = Namespace("https://ontologist.ai/ns/oe/")
PROV = Namespace("http://www.w3.org/ns/prov#")
XSD  = Namespace("http://www.w3.org/2001/XMLSchema#")
PIPE = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")

EVENTS_DIR = Path("logs/events")


class EventLogger:
    """Records pipeline events to GraphStore and daily TriG log files."""

    def __init__(self, store: GraphStore):
        self.store = store
        EVENTS_DIR.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        event_type: str,
        agent: str,
        status: str,
        **extra_props,
    ) -> URIRef:
        """Write one pipeline event. Returns the event URI."""
        slug = f"{event_type.lower()}-{uuid.uuid4().hex[:6]}"
        ev = make_uri("event", slug)
        now = datetime.now(timezone.utc).isoformat()

        event_class = getattr(OE, event_type, OE.Event)

        self.store.add(ev, RDF.type,          event_class,                PIPE)
        self.store.add(ev, OE.hasAgent,       Literal(agent),             PIPE)
        self.store.add(ev, OE.hasStatus,      Literal(status),            PIPE)
        self.store.add(ev, PROV.startedAtTime,
                       Literal(now, datatype=XSD.dateTime),               PIPE)

        for prop_name, value in extra_props.items():
            prop = getattr(OE, prop_name, None) or URIRef(str(OE) + prop_name)
            if isinstance(value, URIRef):
                self.store.add(ev, prop, value, PIPE)
            else:
                self.store.add(ev, prop, Literal(str(value)), PIPE)

        self._append_to_daily_log(ev, event_class, agent, status, now, extra_props)
        return ev

    def _append_to_daily_log(
        self,
        ev: URIRef,
        event_class: URIRef,
        agent: str,
        status: str,
        now: str,
        extra_props: dict,
    ) -> None:
        date_str = now[:10]
        log_path = EVENTS_DIR / f"{date_str}.trig"

        g = ConjunctiveGraph()
        if log_path.exists():
            g.parse(str(log_path), format="trig")

        named = g.get_context(PIPE)
        named.add((ev, RDF.type, event_class))
        named.add((ev, OE.hasAgent, Literal(agent)))
        named.add((ev, OE.hasStatus, Literal(status)))
        named.add((ev, PROV.startedAtTime,
                   Literal(now, datatype=XSD.dateTime)))

        for prop_name, value in extra_props.items():
            prop = getattr(OE, prop_name, None) or URIRef(str(OE) + prop_name)
            if isinstance(value, URIRef):
                named.add((ev, prop, value))
            else:
                named.add((ev, prop, Literal(str(value))))

        g.serialize(destination=str(log_path), format="trig")
