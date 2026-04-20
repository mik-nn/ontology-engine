"""Stage 6 — Context Builder.

Performs BFS from an anchor URI across all named graphs in the store.
Returns a ContextPacket with triples, Databook fragments, entity summaries,
and include/exclude provenance — ready for pruning and LLM delivery.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

from rdflib import Namespace, URIRef, Literal, RDF
from rdflib.term import Node

from storage.graph_store import GraphStore
from storage.id_manager import uri as make_uri

OE    = Namespace("https://ontologist.ai/ns/oe/")
CGA   = Namespace("https://ontologist.ai/ns/cga/")
BUILD = Namespace("https://ontologist.ai/ns/build#")
DB    = Namespace("https://ontologist.ai/ns/databook#")
PROV  = Namespace("http://www.w3.org/ns/prov#")

# Asymmetric traversal to prevent hub fan-out (project node connects everything).
# Outgoing: follow structural edges away from the anchor.
_TRAVERSAL_OUT = {
    str(OE.dependsOn),
    str(OE.definedIn),
    str(CGA.partOf),      # module → project (structural context)
    str(BUILD.dependsOn),
}
# Incoming: pull in entities that reference the anchor — functions, tasks.
# cga:partOf intentionally excluded here: pulling siblings via project is noise.
_TRAVERSAL_IN = {
    str(OE.definedIn),    # functions/classes → anchor module
    str(OE.hasTask),
    str(BUILD.requiredBy),
}

# Keep for annotation in to_prompt_text
_HIGH_PRIORITY = _TRAVERSAL_OUT | _TRAVERSAL_IN

# Predicates that are metadata noise — collected but pruned first if over budget
_METADATA = {
    str(OE.fileSizeBytes), str(OE.fileExt), str(OE.fileName), str(OE.filePath),
    str(OE.lineNumber),
    str(CGA.hasInteriorGraph), str(CGA.hasBoundaryGraph),
    str(CGA.hasProjectionGraph), str(CGA.hasContextGraph),
    str(OE.holonDepth),
}

# Predicates that bring in Databook content
_DATABOOK_PROPS = {str(DB.title), str(DB.content), str(DB.version),
                   str(DB.type), str(DB.created), str(DB.transformer)}


@dataclass
class TripleRecord:
    s: str
    p: str
    o: str
    depth: int
    is_metadata: bool
    is_databook: bool


_CODE_PREDICATES = {
    str(OE.functionName), str(OE.className), str(OE.definedIn), str(OE.absolutePath),
    str(OE.description), str(OE.exports), str(OE.dependsOn), str(BUILD.dependsOn),
    str(BUILD.requiredBy), str(CGA.partOf), str(OE.lineNumber),
}

_ONTOLOGY_PREDICATES = {
    "http://www.w3.org/2000/01/rdf-schema#subClassOf",
    "http://www.w3.org/2000/01/rdf-schema#label",
    "http://www.w3.org/2000/01/rdf-schema#comment",
    "http://www.w3.org/2002/07/owl#equivalentClass",
}

_PLAN_PREDICATES = {
    str(OE.hasExecutor), str(OE.executionOrder), str(OE.hasStatus),
    str(OE.taskName), str(OE.subtaskIndex), str(OE.planRequest),
    str(OE.planType), str(OE.stepDesc),
}


@dataclass
class ContextPacket:
    packet_id: str
    anchor_uri: str
    anchor_type: str
    records: list[TripleRecord]          = field(default_factory=list)
    databook_fragments: list[dict]       = field(default_factory=list)
    entity_summaries: dict[str, str]     = field(default_factory=dict)
    token_estimate: int                  = 0
    depth_used: int                      = 0
    included: dict[str, str]            = field(default_factory=dict)
    excluded: dict[str, str]            = field(default_factory=dict)
    # Task context — populated by pipeline before LLM dispatch
    task_request: Optional[str]          = None
    task_type: Optional[str]             = None
    plan_steps: list[dict]               = field(default_factory=list)

    @property
    def semantic_records(self) -> list[TripleRecord]:
        return [r for r in self.records if not r.is_metadata]

    @property
    def triple_count(self) -> int:
        return len(self.records)

    def to_json(self) -> dict:
        return {
            "packet_id":          self.packet_id,
            "anchor_uri":         self.anchor_uri,
            "anchor_type":        self.anchor_type,
            "depth_used":         self.depth_used,
            "token_estimate":     self.token_estimate,
            "triple_count":       self.triple_count,
            "databook_fragments": self.databook_fragments,
            "entity_summaries":   self.entity_summaries,
            "triples":            [{"s": r.s, "p": r.p, "o": r.o, "depth": r.depth}
                                   for r in self.semantic_records],
            "included":           self.included,
            "excluded":           self.excluded,
            "task_request":       self.task_request,
            "task_type":          self.task_type,
            "plan_steps":         self.plan_steps,
        }

    def to_prompt_text(self) -> str:
        """4-section structured prompt: project_facts / domain_knowledge / task_spec / agent_instructions."""
        anchor_name = self.anchor_uri.split("/")[-1].replace("-", "_")
        header = (
            f"# Context packet  [{self.anchor_type}: {anchor_name}]\n"
            f"_anchor: {self.anchor_uri} | depth: {self.depth_used} | "
            f"triples: {self.triple_count} | tokens≈{self.token_estimate}_"
        )
        sections = [header]

        # ── 1. project_facts ──────────────────────────────────────────
        pf = self._section_project_facts()
        if pf:
            sections.append("## project_facts\n" + pf)

        # ── 2. domain_knowledge ───────────────────────────────────────
        dk = self._section_domain_knowledge()
        if dk:
            sections.append("## domain_knowledge\n" + dk)

        # ── 3. task_spec ──────────────────────────────────────────────
        ts = self._section_task_spec()
        if ts:
            sections.append("## task_spec\n" + ts)

        # ── 4. agent_instructions ─────────────────────────────────────
        ai = self._section_agent_instructions()
        if ai:
            sections.append("## agent_instructions\n" + ai)

        return "\n\n".join(sections)

    # ── Section renderers ─────────────────────────────────────────────

    def _section_project_facts(self) -> str:
        lines = []

        # Entity summaries (types + names)
        if self.entity_summaries:
            lines.append("### entities")
            for ent_uri, summary in list(self.entity_summaries.items())[:30]:
                local = ent_uri.split("/")[-1].replace("-", "_")
                lines.append(f"  {local}: {summary}")

        # Code dependencies
        dep_preds = {str(OE.dependsOn), str(BUILD.requiredBy), str(BUILD.dependsOn)}
        deps = [r for r in self.semantic_records if r.p in dep_preds]
        if deps:
            lines.append("### dependencies")
            for r in deps:
                s = r.s.split("/")[-1].replace("-", "_")
                o = r.o.split("/")[-1].replace("-", "_")
                p = r.p.split("#")[-1].split("/")[-1]
                lines.append(f"  {s} →[{p}]→ {o}")

        # Public API (exports)
        exports = [r for r in self.semantic_records if r.p == str(OE.exports)]
        if exports:
            lines.append("### public_api")
            for r in exports[:30]:
                sym = r.o.split("/")[-1].replace("-", "_")
                lines.append(f"  {sym}")

        # Other code facts (functions, classes, descriptions)
        code_shown = dep_preds | {str(OE.exports)}
        code_facts = [
            r for r in self.semantic_records
            if r.p in _CODE_PREDICATES and r.p not in code_shown
            and r.p not in _DATABOOK_PROPS and r.p != str(RDF.type)
        ]
        if code_facts:
            lines.append("### code_facts")
            for r in code_facts[:40]:
                s = r.s.split("/")[-1].replace("-", "_")
                p = r.p.split("#")[-1].split("/")[-1]
                o = r.o.split("/")[-1] if r.o.startswith("http") else r.o[:120]
                lines.append(f"  {s} · {p} · {o}")

        return "\n".join(lines)

    def _section_domain_knowledge(self) -> str:
        lines = []

        # Databook fragments (design decisions, ADRs)
        if self.databook_fragments:
            lines.append("### databooks")
            for frag in self.databook_fragments:
                lines.append(f"#### {frag.get('title', '(untitled)')}")
                if frag.get("content_excerpt"):
                    lines.append(frag["content_excerpt"])

        # Ontology class hierarchy
        hier = [r for r in self.semantic_records if r.p in _ONTOLOGY_PREDICATES]
        if hier:
            lines.append("### class_hierarchy")
            for r in hier[:20]:
                s = r.s.split("/")[-1].split("#")[-1]
                p = r.p.split("#")[-1].split("/")[-1]
                o = r.o.split("/")[-1].split("#")[-1]
                lines.append(f"  {s} {p} {o}")

        # rdf:type declarations (what things ARE in the ontology)
        type_facts = [r for r in self.semantic_records if r.p == str(RDF.type)
                      and ("ontologist.ai" in r.o or "w3.org" in r.o)]
        if type_facts:
            lines.append("### ontology_types")
            for r in type_facts[:20]:
                s = r.s.split("/")[-1].replace("-", "_")
                o = r.o.split("/")[-1].split("#")[-1]
                lines.append(f"  {s} rdf:type {o}")

        return "\n".join(lines)

    def _section_task_spec(self) -> str:
        lines = []
        if self.task_type:
            lines.append(f"task_type: {self.task_type}")
        if self.task_request:
            lines.append(f"request: {self.task_request}")
        if self.entity_summaries:
            lines.append("matched_entities:")
            anchor = self.anchor_uri
            lines.append(f"  anchor: {anchor.split('/')[-1]} ({self.anchor_type})")
            for uri_str, summary in list(self.entity_summaries.items())[:10]:
                if uri_str != anchor:
                    lines.append(f"  - {uri_str.split('/')[-1]}: {summary}")
        # Context provenance
        included_count = len(self.included)
        excluded_count = len(self.excluded)
        lines.append(f"context_scope: {included_count} entities included, {excluded_count} excluded")
        return "\n".join(lines)

    def _section_agent_instructions(self) -> str:
        lines = []
        if self.plan_steps:
            lines.append("execution_plan:")
            for step in self.plan_steps:
                order = step.get("order", "?")
                name  = step.get("name", "?")
                exec_ = step.get("executor", "?")
                desc  = step.get("description", "")
                lines.append(f"  step {order}: [{exec_}] {name}")
                if desc:
                    lines.append(f"    → {desc}")
        else:
            # Derive from graph records when no explicit plan passed
            exec_facts = [r for r in self.semantic_records if r.p in _PLAN_PREDICATES]
            if exec_facts:
                lines.append("plan_facts:")
                for r in exec_facts[:20]:
                    s = r.s.split("/")[-1].replace("-", "_")
                    p = r.p.split("/")[-1].split("#")[-1]
                    o = r.o if not r.o.startswith("http") else r.o.split("/")[-1]
                    lines.append(f"  {s} · {p} · {o}")
        lines.append("constraints:")
        lines.append("  - All code changes must be written to files before calling git_client")
        lines.append("  - SHACL validation must pass before commit")
        lines.append("  - LLM must not orchestrate — it only executes atomic steps")
        return "\n".join(lines)


class ContextBuilder:
    """BFS subgraph extraction anchored on a given URI.

    max_depth  — BFS hops from anchor (default 3)
    max_tokens — soft token budget; ContextPruner enforces it after build
    """

    def __init__(self, store: GraphStore, max_depth: int = 3,
                 max_tokens: int = 4000):
        self.store = store
        self.max_depth = max_depth
        self.max_tokens = max_tokens

    def build(self, anchor_uri: str) -> ContextPacket:
        anchor = URIRef(anchor_uri)
        anchor_type = self._type_label(anchor)

        packet = ContextPacket(
            packet_id=f"ctx-{uuid.uuid4().hex[:8]}",
            anchor_uri=anchor_uri,
            anchor_type=anchor_type,
        )

        visited: dict[str, int] = {anchor_uri: 0}   # uri → depth
        queue: list[tuple[URIRef, int]] = [(anchor, 0)]

        while queue:
            node, depth = queue.pop(0)
            if depth > self.max_depth:
                continue

            for ctx in self.store._g.contexts():
                # Outgoing
                for s, p, o in ctx.triples((node, None, None)):
                    self._add_triple(packet, s, p, o, depth)
                    # Expand outgoing neighbors via outgoing traversal set
                    p_str = str(p)
                    if (isinstance(o, URIRef) and str(o) not in visited
                            and p_str in _TRAVERSAL_OUT):
                        next_depth = depth + 1
                        if next_depth <= self.max_depth:
                            visited[str(o)] = next_depth
                            queue.append((o, next_depth))

                # Incoming — record all, expand only via incoming traversal set
                for s, p, o in ctx.triples((None, None, node)):
                    self._add_triple(packet, s, p, o, depth)
                    p_str = str(p)
                    if (isinstance(s, URIRef) and str(s) not in visited
                            and p_str in _TRAVERSAL_IN):
                        next_depth = depth + 1
                        if next_depth <= self.max_depth:
                            visited[str(s)] = next_depth
                            queue.append((s, next_depth))

        # Record included entities
        for ent_uri, d in visited.items():
            reason = "anchor" if d == 0 else f"BFS depth {d}"
            packet.included[ent_uri] = reason

        packet.depth_used = self.max_depth
        self._collect_databook_fragments(packet)
        self._build_summaries(packet)
        packet.token_estimate = self._estimate_tokens(packet)

        self._emit_event(packet)
        return packet

    def _add_triple(self, packet: ContextPacket,
                    s: Node, p: Node, o: Node, depth: int) -> None:
        p_str = str(p)
        o_str = str(o) if isinstance(o, URIRef) else str(o)
        packet.records.append(TripleRecord(
            s=str(s), p=p_str, o=o_str,
            depth=depth,
            is_metadata=p_str in _METADATA,
            is_databook=p_str in _DATABOOK_PROPS,
        ))

    def _type_label(self, uri: URIRef) -> str:
        for ctx in self.store._g.contexts():
            t = ctx.value(uri, RDF.type)
            if t:
                return str(t).split("/")[-1].split("#")[-1]
        return "Entity"

    def _collect_databook_fragments(self, packet: ContextPacket) -> None:
        seen: set[str] = set()
        for r in packet.records:
            if r.p == str(RDF.type) and r.o.endswith("Databook"):
                db_uri = r.s
                if db_uri in seen:
                    continue
                seen.add(db_uri)
                frag: dict = {"uri": db_uri}
                for rec in packet.records:
                    if rec.s != db_uri:
                        continue
                    if rec.p == str(DB.title):
                        frag["title"] = rec.o
                    elif rec.p == str(DB.content):
                        frag["content_excerpt"] = rec.o[:600] + ("…" if len(rec.o) > 600 else "")
                    elif rec.p == str(DB.type):
                        frag["type"] = rec.o
                if frag.get("title") or frag.get("content_excerpt"):
                    packet.databook_fragments.append(frag)

    def _build_summaries(self, packet: ContextPacket) -> None:
        types: dict[str, str] = {}
        names: dict[str, str] = {}
        for r in packet.records:
            if r.p == str(RDF.type):
                types[r.s] = r.o.split("/")[-1].split("#")[-1]
            for name_pred in (str(OE.functionName), str(OE.className),
                              str(OE.fileName), str(DB.title)):
                if r.p == name_pred:
                    names[r.s] = r.o

        for ent_uri in set(types) | set(names):
            t = types.get(ent_uri, "Entity")
            n = names.get(ent_uri, ent_uri.split("/")[-1])
            packet.entity_summaries[ent_uri] = f"{t}: {n}"

    def _estimate_tokens(self, packet: ContextPacket) -> int:
        chars = sum(len(r.s) + len(r.p) + len(r.o) for r in packet.records)
        chars += sum(len(str(v)) for f in packet.databook_fragments
                     for v in f.values())
        return int(chars / 4 * 1.2)

    def _emit_event(self, packet: ContextPacket) -> None:
        from datetime import datetime, timezone
        from rdflib import Literal as Lit
        PIPELINE_INTERIOR = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")
        XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

        ev = make_uri("event", f"context-built-{packet.packet_id}")
        self.store.add(ev, RDF.type,          OE.ContextBuilt,           PIPELINE_INTERIOR)
        self.store.add(ev, OE.hasAgent,        Lit("ContextAgent"),       PIPELINE_INTERIOR)
        self.store.add(ev, OE.hasStatus,       Lit("success"),            PIPELINE_INTERIOR)
        self.store.add(ev, OE.anchorUri,       URIRef(packet.anchor_uri), PIPELINE_INTERIOR)
        self.store.add(ev, OE.tokenEstimate,   Lit(packet.token_estimate), PIPELINE_INTERIOR)
        self.store.add(ev, OE.tripleCount,     Lit(packet.triple_count),  PIPELINE_INTERIOR)
        self.store.add(ev, OE.depthUsed,       Lit(packet.depth_used),    PIPELINE_INTERIOR)
        self.store.add(ev, PROV.startedAtTime,
                       Lit(datetime.now(timezone.utc).isoformat(),
                           datatype=XSD.dateTime),                        PIPELINE_INTERIOR)
