"""Stage 5 — Human Verification CLI.

Shows each SHACL/rule violation to the user and collects one of:
  [c] confirm   — accept as known exception, write to graph
  [i] interview — flag for Stage 4 interview (placeholder until Stage 4 is built)
  [s] skip      — note but take no action this run

All decisions are written as oe:UserAnswerReceived events to the pipeline interior graph.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri
from verification.rule_engine import RuleReport, RuleViolation

OE   = Namespace("https://ontologist.ai/ns/oe/")
PROV = Namespace("http://www.w3.org/ns/prov#")
XSD  = Namespace("http://www.w3.org/2001/XMLSchema#")

PIPELINE_INTERIOR = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")

_SEVERITY_COLORS = {
    "violation": "\033[91m",  # red
    "warning":   "\033[93m",  # yellow
    "info":      "\033[94m",  # blue
}
_RESET = "\033[0m"


class VerifyCLI:
    """Interactive terminal session for human verification of rule violations."""

    def __init__(self, store: GraphStore, report: RuleReport,
                 auto_confirm_infos: bool = True):
        self.store = store
        self.report = report
        self.auto_confirm_infos = auto_confirm_infos
        self._decisions: dict[str, str] = {}  # violation_id → decision

    def run(self) -> dict[str, str]:
        """Present each issue to the user. Returns decisions map."""
        issues = self.report.all_issues

        if not issues:
            print("No violations or warnings — graph is fully conformant.")
            return {}

        print(f"\n{'─'*60}")
        print(f"  Human Verification — {len(issues)} issue(s) to review")
        print(f"{'─'*60}")
        print("  [c] confirm (accept as known exception)")
        print("  [i] interview (flag for Stage 4 Q&A)")
        print("  [s] skip (no action this run)")
        print(f"{'─'*60}\n")

        for idx, issue in enumerate(issues, 1):
            decision = self._present_issue(idx, len(issues), issue)
            self._decisions[f"{issue.rule_id}::{issue.subject}"] = decision
            self._write_event(issue, decision)

        self._print_summary()
        return self._decisions

    def _present_issue(self, idx: int, total: int,
                       issue: RuleViolation) -> str:
        color = _SEVERITY_COLORS.get(issue.severity, "")
        tag = issue.severity.upper()

        if self.auto_confirm_infos and issue.severity == "info":
            print(f"[{idx}/{total}] {color}[{tag}]{_RESET} {issue.rule_id} — auto-confirmed")
            return "confirm"

        print(f"\n[{idx}/{total}] {color}[{tag}]{_RESET} {issue.rule_id}  ({issue.source})")
        print(f"  subject : {_shorten(issue.subject)}")
        print(f"  message : {issue.message}")

        while True:
            try:
                raw = input("  → [c]onfirm / [i]nterview / [s]kip : ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nAborted — remaining issues skipped.")
                return "skip"

            if raw in ("c", "confirm"):
                return "confirm"
            if raw in ("i", "interview"):
                return "interview"
            if raw in ("s", "skip", ""):
                return "skip"
            print("  Please enter c, i, or s.")

    def _write_event(self, issue: RuleViolation, decision: str) -> None:
        """Write a UserAnswerReceived event for each human decision."""
        event_uri = uri("event", f"user-answer-{uuid.uuid4().hex[:8]}")
        now = datetime.now(timezone.utc).isoformat()

        self.store.add(event_uri, RDF.type,
                       OE.UserAnswerReceived,       PIPELINE_INTERIOR)
        self.store.add(event_uri, OE.hasAgent,
                       Literal("HumanAnalyst"),     PIPELINE_INTERIOR)
        self.store.add(event_uri, OE.hasStatus,
                       Literal("success"),          PIPELINE_INTERIOR)
        self.store.add(event_uri, OE.concernsRule,
                       Literal(issue.rule_id),      PIPELINE_INTERIOR)
        self.store.add(event_uri, OE.concernsSubject,
                       URIRef(issue.subject) if issue.subject.startswith("http")
                       else Literal(issue.subject), PIPELINE_INTERIOR)
        self.store.add(event_uri, OE.userDecision,
                       Literal(decision),           PIPELINE_INTERIOR)
        self.store.add(event_uri, PROV.startedAtTime,
                       Literal(now, datatype=XSD.dateTime), PIPELINE_INTERIOR)

        if decision == "confirm":
            # Write a confirmed exception triple into the default graph
            self.store.add(event_uri, OE.isConfirmedException,
                           Literal(True),           PIPELINE_INTERIOR)

    def _print_summary(self) -> None:
        counts = {"confirm": 0, "interview": 0, "skip": 0}
        for d in self._decisions.values():
            counts[d] = counts.get(d, 0) + 1
        print(f"\n{'─'*60}")
        print(f"  Verification complete")
        print(f"  confirmed : {counts['confirm']}")
        print(f"  flagged   : {counts['interview']}  (queued for Stage 4 interview)")
        print(f"  skipped   : {counts['skip']}")
        print(f"{'─'*60}\n")


def _shorten(uri_str: str, max_len: int = 80) -> str:
    if len(uri_str) <= max_len:
        return uri_str
    return "..." + uri_str[-(max_len - 3):]
