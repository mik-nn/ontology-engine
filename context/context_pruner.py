"""Stage 6 — Context Pruner.

Enforces a token budget on a ContextPacket by removing records in priority order:
  1. Metadata predicates (oe:fileSizeBytes, oe:lineNumber, graph structure URIs)
  2. Deepest-depth records first (lowest semantic relevance)
  3. Truncation of db:content literals to shorter excerpts
  4. Removal of duplicate (s, p) pairs keeping shallower copy

Returns a new ContextPacket with updated excluded dict explaining each removal.
"""
from __future__ import annotations

from copy import deepcopy

from context.context_builder import ContextPacket, TripleRecord, _METADATA, _DATABOOK_PROPS
from rdflib import Namespace

DB = Namespace("https://ontologist.ai/ns/databook#")
OE = Namespace("https://ontologist.ai/ns/oe/")

_CONTENT_TRUNCATE_STEP = 300   # chars removed per truncation pass
_CONTENT_MIN_LEN       = 100   # never truncate below this


class ContextPruner:
    """Reduces a ContextPacket to fit within a token budget.

    Strategy (applied in order until budget is met):
      Pass 1 — remove pure-metadata triples
      Pass 2 — deduplicate (s, p) pairs — keep shallowest
      Pass 3 — remove records at max depth (least relevant)
      Pass 4 — truncate db:content literals progressively
      Pass 5 — remove records at max_depth-1, etc.
    """

    def __init__(self, max_tokens: int = 4000, content_max_chars: int = 600):
        self.max_tokens = max_tokens
        self.content_max_chars = content_max_chars

    def prune(self, packet: ContextPacket) -> ContextPacket:
        p = deepcopy(packet)

        if p.token_estimate <= self.max_tokens:
            return p  # already within budget

        p = self._pass_metadata(p)
        if p.token_estimate <= self.max_tokens:
            return self._finalize(p)

        p = self._pass_dedup(p)
        if p.token_estimate <= self.max_tokens:
            return self._finalize(p)

        p = self._pass_depth(p)
        if p.token_estimate <= self.max_tokens:
            return self._finalize(p)

        p = self._pass_truncate_content(p)
        if p.token_estimate > self.max_tokens:
            p = self._signal_decomposition(p)
        return self._finalize(p)

    # ──────────────────────────────────────────────
    # Pruning passes
    # ──────────────────────────────────────────────

    def _pass_metadata(self, p: ContextPacket) -> ContextPacket:
        kept, removed = [], []
        for r in p.records:
            if r.is_metadata:
                removed.append(r)
            else:
                kept.append(r)
        for r in removed:
            p.excluded[r.s] = p.excluded.get(r.s, "metadata predicate removed for budget")
        p.records = kept
        p.token_estimate = self._estimate(p)
        return p

    def _pass_dedup(self, p: ContextPacket) -> ContextPacket:
        seen: dict[tuple, int] = {}   # (s, p) → index of best (shallowest) record
        for i, r in enumerate(p.records):
            key = (r.s, r.p)
            if key not in seen or r.depth < p.records[seen[key]].depth:
                seen[key] = i
        keep_idxs = set(seen.values())
        kept, removed = [], []
        for i, r in enumerate(p.records):
            if i in keep_idxs:
                kept.append(r)
            else:
                removed.append(r)
        for r in removed:
            p.excluded[r.s] = p.excluded.get(r.s, "duplicate triple removed")
        p.records = kept
        p.token_estimate = self._estimate(p)
        return p

    def _pass_depth(self, p: ContextPacket) -> ContextPacket:
        if not p.records:
            return p
        max_d = max(r.depth for r in p.records)
        while max_d > 0 and p.token_estimate > self.max_tokens:
            kept, removed = [], []
            for r in p.records:
                if r.depth == max_d:
                    removed.append(r)
                else:
                    kept.append(r)
            for r in removed:
                p.excluded[r.s] = f"depth {r.depth} removed — over token budget"
            p.records = kept
            p.token_estimate = self._estimate(p)
            max_d -= 1
        return p

    def _pass_truncate_content(self, p: ContextPacket) -> ContextPacket:
        content_pred = str(DB.content)
        current_len = self.content_max_chars

        while p.token_estimate > self.max_tokens and current_len > _CONTENT_MIN_LEN:
            current_len = max(_CONTENT_MIN_LEN, current_len - _CONTENT_TRUNCATE_STEP)
            for r in p.records:
                if r.p == content_pred and len(r.o) > current_len:
                    r.o = r.o[:current_len] + "…"
                    p.excluded[r.s] = p.excluded.get(
                        r.s, f"db:content truncated to {current_len} chars")
            # Rebuild databook fragments with new truncation
            for frag in p.databook_fragments:
                if frag.get("content_excerpt") and len(frag["content_excerpt"]) > current_len:
                    frag["content_excerpt"] = frag["content_excerpt"][:current_len] + "…"
            p.token_estimate = self._estimate(p)

        return p

    def _signal_decomposition(self, p: ContextPacket) -> ContextPacket:
        """Mark the packet as needing task decomposition.

        Called when all pruning passes are exhausted and the token budget
        is still exceeded.  The hint describes *why* the context is too
        large so the planner can split the task appropriately.
        """
        p.needs_decomposition = True
        entity_count = len(p.included)
        db_count = len(p.databook_fragments)
        over_by = p.token_estimate - self.max_tokens
        existing_hint = p.decomposition_hint  # may already have chunking note

        hint_parts = [
            f"Context exceeds budget by ~{over_by} tokens "
            f"({p.token_estimate} > {self.max_tokens}).",
            f"Scope: {entity_count} entities, {db_count} databooks.",
            "Decomposition options:",
            "  • Narrow anchor — use a single function/class instead of a module.",
            "  • Split by layer — request architecture or implementation layer only.",
            "  • Break task — decompose into subtasks with separate context packets.",
        ]
        if existing_hint:
            hint_parts.append(existing_hint)

        p.decomposition_hint = " ".join(hint_parts)
        return p

    def _finalize(self, p: ContextPacket) -> ContextPacket:
        # Rebuild databook fragments from remaining records
        from_records = self._rebuild_fragments(p)
        if from_records:
            # Records-derived fragments take precedence (properly pruned)
            p.databook_fragments = from_records
        # else: keep whatever was injected externally (e.g. _collect_all_databooks)
        return p

    def _rebuild_fragments(self, p: ContextPacket) -> list[dict]:
        from rdflib import RDF
        db_uris: set[str] = set()
        for r in p.records:
            if r.p == str(RDF.type) and r.o.endswith("Databook"):
                db_uris.add(r.s)

        fragments = []
        for db_uri in db_uris:
            frag: dict = {"uri": db_uri}
            for r in p.records:
                if r.s != db_uri:
                    continue
                if r.p == str(DB.title):
                    frag["title"] = r.o
                elif r.p == str(DB.content):
                    frag["content_excerpt"] = r.o
                elif r.p == str(DB.type):
                    frag["type"] = r.o
                elif r.p == str(DB.scope):
                    frag["scope"] = r.o
                elif r.p == str(DB.layer):
                    frag["layer"] = r.o
                elif r.p == str(DB.hierarchy):
                    frag["hierarchy"] = r.o
            if frag.get("title") or frag.get("content_excerpt"):
                fragments.append(frag)
        return fragments

    @staticmethod
    def _estimate(p: ContextPacket) -> int:
        chars = sum(len(r.s) + len(r.p) + len(r.o) for r in p.records)
        chars += sum(len(str(v)) for f in p.databook_fragments for v in f.values())
        return int(chars / 4 * 1.2)
