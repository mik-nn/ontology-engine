"""Stage 4 — UserFeedback.

Maps a raw user answer string to one or more RDF triples and writes
them to the graph. Each answer is also recorded as a UserAnswerReceived
event with full PROV-O provenance.

The mapping is driven by the gap descriptor produced by Interviewer —
no LLM involvement, no guessing.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from rdflib import Namespace, RDF, Literal, URIRef, XSD as RDF_XSD

from storage.graph_store import GraphStore
from storage.id_manager import uri as make_uri, graph_uri

OE   = Namespace("https://ontologist.ai/ns/oe/")
DB   = Namespace("https://ontologist.ai/ns/databook#")
PROV = Namespace("http://www.w3.org/ns/prov#")
XSD  = Namespace("http://www.w3.org/2001/XMLSchema#")
PIPE = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")


@dataclass
class GapDescriptor:
    """Describes a single gap that needs a user answer."""
    rule_id: str
    subject_uri: str
    predicate_uri: str
    question: str
    datatype: Optional[str] = None      # xsd: type name, e.g. "string"
    allowed_values: Optional[list[str]] = None
    severity: str = "warning"           # "violation" | "warning"


@dataclass
class FeedbackResult:
    gap: GapDescriptor
    raw_answer: str
    accepted: bool
    triples_written: int = 0
    error: Optional[str] = None


class UserFeedback:
    """Applies a user's answer to a gap and writes it to the graph."""

    def __init__(self, store: GraphStore):
        self.store = store

    def apply(self, gap: GapDescriptor, raw_answer: str) -> FeedbackResult:
        """Validate answer, write triple(s), emit event."""
        answer = raw_answer.strip()

        if gap.allowed_values and answer not in gap.allowed_values:
            return FeedbackResult(
                gap=gap,
                raw_answer=raw_answer,
                accepted=False,
                error=(
                    f"'{answer}' is not one of: "
                    f"{', '.join(gap.allowed_values)}"
                ),
            )

        if not answer:
            return FeedbackResult(
                gap=gap,
                raw_answer=raw_answer,
                accepted=False,
                error="Empty answer — skipped.",
            )

        subject  = URIRef(gap.subject_uri)
        pred     = URIRef(gap.predicate_uri)
        target_g = graph_uri(subject, "interior")

        if gap.datatype == "string":
            obj = Literal(answer, datatype=XSD.string)
        elif gap.datatype == "integer":
            try:
                obj = Literal(int(answer), datatype=XSD.integer)
            except ValueError:
                return FeedbackResult(
                    gap=gap, raw_answer=raw_answer, accepted=False,
                    error=f"Expected integer, got: {answer}",
                )
        else:
            obj = Literal(answer)

        self.store.add(subject, pred, obj, target_g)
        self._emit_event(gap, answer)

        return FeedbackResult(
            gap=gap,
            raw_answer=raw_answer,
            accepted=True,
            triples_written=1,
        )

    def _emit_event(self, gap: GapDescriptor, answer: str) -> None:
        ev = make_uri("event", f"user-answer-{uuid.uuid4().hex[:8]}")
        now = datetime.now(timezone.utc).isoformat()

        self.store.add(ev, RDF.type,           OE.UserAnswerReceived, PIPE)
        self.store.add(ev, OE.hasAgent,        Literal("HumanAnalyst"), PIPE)
        self.store.add(ev, OE.hasStatus,       Literal("success"), PIPE)
        self.store.add(ev, OE.concernsRule,    Literal(gap.rule_id), PIPE)
        self.store.add(ev, OE.concernsSubject, URIRef(gap.subject_uri), PIPE)
        self.store.add(ev, OE.userAnswer,      Literal(answer), PIPE)
        self.store.add(ev, PROV.startedAtTime,
                       Literal(now, datatype=XSD.dateTime), PIPE)
