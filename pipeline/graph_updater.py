"""Stage 8 — GraphUpdater.

Applies executor results to the graph, validates with SHACL,
and emits update events.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from rdflib import Namespace, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import graph_uri
from pipeline.event_logger import EventLogger

OE   = Namespace("https://ontologist.ai/ns/oe/")
PROV = Namespace("http://www.w3.org/ns/prov#")
XSD  = Namespace("http://www.w3.org/2001/XMLSchema#")


@dataclass
class ApplyResult:
    subtask_uri: str
    success: bool
    violations: list[str]
    error: Optional[str] = None


class GraphUpdater:
    """Applies executor output to the graph and validates the result."""

    def __init__(
        self,
        store: GraphStore,
        logger: EventLogger,
        shapes_paths: list[str],
    ):
        self.store = store
        self.logger = logger
        self.shapes_paths = shapes_paths

    def apply_result(
        self,
        subtask_uri: str,
        status: str,
        output_summary: str,
        executor: str,
        extra_triples: Optional[list[tuple]] = None,
    ) -> ApplyResult:
        """Write subtask outcome to graph, validate, return ApplyResult."""
        sub_uri = URIRef(subtask_uri)
        sub_int = graph_uri(sub_uri, "interior")
        now = datetime.now(timezone.utc).isoformat()

        self.store.add(sub_uri, OE.hasStatus,
                       Literal(status), sub_int)
        self.store.add(sub_uri, OE.outputSummary,
                       Literal(output_summary), sub_int)
        self.store.add(sub_uri, OE.executorUsed,
                       Literal(executor), sub_int)
        self.store.add(sub_uri, PROV.endedAtTime,
                       Literal(now, datatype=XSD.dateTime), sub_int)

        if extra_triples:
            for s, p, o in extra_triples:
                self.store.add(s, p, o, sub_int)

        violations = self._validate(subtask_uri)
        success = status == "completed" and not violations

        self.logger.log(
            "PlanExecuted",
            agent="GraphUpdater",
            status="updated" if success else "violation",
            subtaskUri=sub_uri,
            executorUsed=executor,
        )

        return ApplyResult(
            subtask_uri=subtask_uri,
            success=success,
            violations=violations,
        )

    def _validate(self, subtask_uri: str) -> list[str]:
        try:
            report = self.store.validate(self.shapes_paths)
            return [str(v.message) for v in report.violations
                    if subtask_uri in str(getattr(v, "focus_node", ""))]
        except Exception as exc:
            return [f"Validation error: {exc}"]
