"""Stage 4 — Interviewer.

Detects gaps in the graph by querying for missing required properties,
then runs a structured CLI interview to collect answers and close those gaps.

Gap detection is driven by SPARQL + rule IDs — not LLM heuristics.
Each answer is applied via UserFeedback, which writes triples + events.

Gap sources:
  G01  Databook missing title          (mirrors R01)
  G02  Databook missing transformer    (mirrors R02)
  G03  Databook missing version
  G04  Module with no description
  G05  Plan with no planType
  G06  Entities flagged 'interview' by VerifyCLI
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from interaction.user_feedback import UserFeedback, GapDescriptor, FeedbackResult

OE  = Namespace("https://ontologist.ai/ns/oe/")
DB  = Namespace("https://ontologist.ai/ns/databook#")
CGA = Namespace("https://ontologist.ai/ns/cga/")

_RESET  = "\033[0m"
_YELLOW = "\033[93m"
_CYAN   = "\033[96m"
_RED    = "\033[91m"
_GREEN  = "\033[92m"
_BOLD   = "\033[1m"


@dataclass
class InterviewSession:
    gaps_found: int = 0
    gaps_closed: int = 0
    gaps_skipped: int = 0
    results: list[FeedbackResult] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"Interview complete — "
            f"{self.gaps_found} gaps found, "
            f"{self.gaps_closed} closed, "
            f"{self.gaps_skipped} skipped."
        )


class Interviewer:
    """Detects graph gaps and collects user answers via structured CLI."""

    def __init__(self, store: GraphStore):
        self.store = store
        self._feedback = UserFeedback(store)

    def run(self) -> InterviewSession:
        session = InterviewSession()
        gaps = self._detect_gaps()

        # Auto-resolve G04 gaps from file content before asking the user
        gaps, auto_closed = self._auto_resolve_g04(gaps)
        session.gaps_found = len(gaps) + auto_closed
        session.gaps_closed += auto_closed

        if not gaps:
            if auto_closed:
                print(f"\n{_GREEN}All gaps auto-resolved from source ({auto_closed} module(s)).{_RESET}")
            else:
                print(f"\n{_GREEN}No gaps found — graph is complete.{_RESET}")
            return session

        print(f"\n{_BOLD}{'─'*60}{_RESET}")
        print(f"  {_BOLD}Stage 4 — Interview{_RESET}  "
              f"({len(gaps)} gap(s) detected)")
        print(f"{_BOLD}{'─'*60}{_RESET}")
        print(f"  {_YELLOW}[s]{_RESET} skip   "
              f"  {_GREEN}[answer]{_RESET} type value and press Enter\n")

        for idx, gap in enumerate(gaps, 1):
            result = self._ask(idx, len(gaps), gap)
            session.results.append(result)
            if result.accepted:
                session.gaps_closed += 1
                print(f"  {_GREEN}✓ Saved.{_RESET}\n")
            else:
                session.gaps_skipped += 1
                if result.error and "skipped" not in result.error.lower():
                    print(f"  {_RED}✗ {result.error}{_RESET}\n")
                else:
                    print(f"  Skipped.\n")

        print(f"{_BOLD}{'─'*60}{_RESET}")
        print(f"  {session.summary()}")
        print(f"{_BOLD}{'─'*60}{_RESET}\n")
        return session

    # ──────────────────────────────────────────────
    # Gap detection (SPARQL-driven)
    # ──────────────────────────────────────────────

    def _detect_gaps(self) -> list[GapDescriptor]:
        gaps: list[GapDescriptor] = []
        gaps.extend(self._gap_g01_databook_title())
        gaps.extend(self._gap_g02_databook_transformer())
        gaps.extend(self._gap_g03_databook_version())
        gaps.extend(self._gap_g04_module_no_description())
        gaps.extend(self._gap_g05_plan_no_type())
        return gaps

    def _gap_g01_databook_title(self) -> list[GapDescriptor]:
        results = self.store._g.query("""
            PREFIX db:  <https://ontologist.ai/ns/databook#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?s WHERE {
                ?s rdf:type db:Databook .
                FILTER NOT EXISTS { ?s db:title ?t . FILTER(STRLEN(STR(?t)) > 0) }
            }
        """)
        return [
            GapDescriptor(
                rule_id="G01",
                subject_uri=str(row.s),
                predicate_uri=str(DB.title),
                question=f"Databook {_short(str(row.s))} has no title. Enter a title:",
                datatype="string",
                severity="violation",
            )
            for row in results
        ]

    def _gap_g02_databook_transformer(self) -> list[GapDescriptor]:
        results = self.store._g.query("""
            PREFIX db:  <https://ontologist.ai/ns/databook#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?s WHERE {
                ?s rdf:type db:Databook .
                FILTER NOT EXISTS { ?s db:transformer ?t }
            }
        """)
        return [
            GapDescriptor(
                rule_id="G02",
                subject_uri=str(row.s),
                predicate_uri=str(DB.transformer),
                question=(
                    f"Databook {_short(str(row.s))} has no transformer. "
                    f"Enter one of [human / llm / sparql / xslt]:"
                ),
                datatype="string",
                allowed_values=["human", "llm", "sparql", "xslt"],
                severity="warning",
            )
            for row in results
        ]

    def _gap_g03_databook_version(self) -> list[GapDescriptor]:
        results = self.store._g.query("""
            PREFIX db:  <https://ontologist.ai/ns/databook#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?s ?title WHERE {
                ?s rdf:type db:Databook .
                OPTIONAL { ?s db:title ?title }
                FILTER NOT EXISTS { ?s db:version ?v }
            }
        """)
        return [
            GapDescriptor(
                rule_id="G03",
                subject_uri=str(row.s),
                predicate_uri=str(DB.version),
                question=(
                    f"Databook '{row.title or _short(str(row.s))}' "
                    f"has no version. Enter version (e.g. 1.0.0):"
                ),
                datatype="string",
                severity="warning",
            )
            for row in results
        ]

    def _gap_g04_module_no_description(self) -> list[GapDescriptor]:
        results = self.store._g.query("""
            PREFIX oe:  <https://ontologist.ai/ns/oe/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?s WHERE {
                ?s rdf:type oe:CodeModule .
                FILTER NOT EXISTS { ?s oe:description ?d }
            }
            LIMIT 5
        """)
        return [
            GapDescriptor(
                rule_id="G04",
                subject_uri=str(row.s),
                predicate_uri=str(OE.description),
                question=f"Module {_short(str(row.s))} has no description. Describe it (or s to skip):",
                datatype="string",
                severity="warning",
            )
            for row in results
        ]

    def _auto_resolve_g04(
        self, gaps: list[GapDescriptor]
    ) -> tuple[list[GapDescriptor], int]:
        """Try to fill G04 gaps from file docstrings or path heuristics.

        Returns (remaining_gaps, auto_closed_count).
        """
        import ast as _ast
        from pathlib import Path

        remaining: list[GapDescriptor] = []
        closed = 0

        for gap in gaps:
            if gap.rule_id != "G04":
                remaining.append(gap)
                continue

            desc = self._infer_description(gap.subject_uri)
            if desc:
                result = self._feedback.apply(gap, desc)
                if result.accepted:
                    closed += 1
                    continue
            remaining.append(gap)

        return remaining, closed

    def _infer_description(self, module_uri: str) -> str | None:
        """Extract description from source file docstring or infer from module path."""
        import ast as _ast
        from pathlib import Path
        from rdflib import URIRef

        uri_ref = URIRef(module_uri)
        fp_lit = self.store._g.value(uri_ref, OE.filePath)
        if fp_lit is None:
            return None

        # filePath is relative to project root (cwd)
        file_path = Path(str(fp_lit))
        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path
        if not file_path.exists():
            return None

        try:
            source = file_path.read_text(encoding="utf-8")
            tree = _ast.parse(source, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError, OSError):
            return None

        # 1. Use existing module docstring
        docstring = _ast.get_docstring(tree)
        if docstring:
            return docstring.strip()[:500]

        # 2. Infer from functions/classes defined in the file
        names = [
            node.name
            for node in _ast.walk(tree)
            if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef))
            and not node.name.startswith("_")
        ]
        if names:
            parts = str(file_path).replace("\\", "/").split("/")
            pkg = parts[-2] if len(parts) >= 2 else ""
            symbols = ", ".join(names[:5])
            return f"Package initializer for {pkg} — exports: {symbols}."

        # 3. Fallback: derive from package path
        parts = str(file_path).replace("\\", "/").split("/")
        pkg = parts[-2] if len(parts) >= 2 else str(file_path.stem)
        return f"Package namespace init for {pkg}."

    def _gap_g05_plan_no_type(self) -> list[GapDescriptor]:
        results = self.store._g.query("""
            PREFIX oe:  <https://ontologist.ai/ns/oe/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?s WHERE {
                ?s rdf:type oe:Plan .
                FILTER NOT EXISTS { ?s oe:planType ?t }
            }
        """)
        allowed = ["ExplainTask", "AnalysisTask", "DesignTask",
                   "ImplementTask", "RefactorTask"]
        return [
            GapDescriptor(
                rule_id="G05",
                subject_uri=str(row.s),
                predicate_uri=str(OE.planType),
                question=(
                    f"Plan {_short(str(row.s))} has no type. "
                    f"Enter one of {allowed}:"
                ),
                datatype="string",
                allowed_values=allowed,
                severity="warning",
            )
            for row in results
        ]

    # ──────────────────────────────────────────────
    # CLI prompt
    # ──────────────────────────────────────────────

    def _ask(self, idx: int, total: int, gap: GapDescriptor) -> FeedbackResult:
        severity_color = _RED if gap.severity == "violation" else _YELLOW
        tag = gap.severity.upper()

        print(f"[{idx}/{total}] {severity_color}[{tag}]{_RESET} "
              f"{_CYAN}{gap.rule_id}{_RESET}")
        print(f"  {gap.question}")

        if gap.allowed_values:
            print(f"  Allowed: {', '.join(gap.allowed_values)}")

        while True:
            try:
                raw = input("  → ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nAborted.")
                return FeedbackResult(
                    gap=gap, raw_answer="", accepted=False,
                    error="Aborted by user.",
                )

            if raw.lower() in ("s", "skip", ""):
                return FeedbackResult(
                    gap=gap, raw_answer=raw, accepted=False,
                    error="skipped",
                )

            result = self._feedback.apply(gap, raw)
            if not result.accepted:
                print(f"  {_RED}✗ {result.error}{_RESET}")
                print("  Try again, or type 's' to skip.")
                continue

            return result


def _short(uri: str, n: int = 50) -> str:
    return uri if len(uri) <= n else "…" + uri[-n:]
