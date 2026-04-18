"""Stage 6 — Context Explainer.

Produces a structured explanation of why each entity was included or excluded
from a ContextPacket. Answers:
  - Why included: which rule / predicate path / depth brought it in
  - Why excluded: which pruning pass removed it and why
  - Which rules fired: depth limit, budget, dedup, metadata strip

Output: ContextExplanation dataclass with:
  - include_reasons: dict[uri → human-readable string]
  - exclude_reasons: dict[uri → human-readable string]
  - rule_log: ordered list of strings describing pruning decisions
  - summary: compact one-paragraph text
  - annotated_prompt: to_prompt_text() + appended explanation section
"""
from __future__ import annotations

from dataclasses import dataclass, field

from context.context_builder import ContextPacket


@dataclass
class ContextExplanation:
    packet_id: str
    include_reasons: dict[str, str]   = field(default_factory=dict)
    exclude_reasons: dict[str, str]   = field(default_factory=dict)
    rule_log: list[str]               = field(default_factory=list)
    summary: str                      = ""

    def print(self) -> None:
        print(f"=== Context Explanation [{self.packet_id}] ===")
        print(f"\nSummary: {self.summary}")
        print(f"\nIncluded ({len(self.include_reasons)}):")
        for uri, reason in list(self.include_reasons.items())[:15]:
            print(f"  ✓ {_local(uri)}: {reason}")
        print(f"\nExcluded ({len(self.exclude_reasons)}):")
        for uri, reason in list(self.exclude_reasons.items())[:10]:
            print(f"  ✗ {_local(uri)}: {reason}")
        if self.rule_log:
            print(f"\nRule log:")
            for entry in self.rule_log:
                print(f"  · {entry}")

    def as_prompt_section(self) -> str:
        lines = ["## Why This Context?", ""]
        lines.append(self.summary)
        lines.append("")
        lines.append("**Included:**")
        for uri, reason in list(self.include_reasons.items())[:8]:
            lines.append(f"- {_local(uri)}: {reason}")
        if self.exclude_reasons:
            lines.append("")
            lines.append("**Excluded:**")
            for uri, reason in list(self.exclude_reasons.items())[:5]:
                lines.append(f"- {_local(uri)}: {reason}")
        return "\n".join(lines)


class ContextExplainer:
    """Derives human-readable reasoning from a (raw, pruned) ContextPacket pair."""

    def explain(self, raw: ContextPacket, pruned: ContextPacket) -> ContextExplanation:
        expl = ContextExplanation(packet_id=pruned.packet_id)

        # Include reasons from BFS traversal
        for uri, reason in pruned.included.items():
            expl.include_reasons[uri] = self._humanise_include(uri, reason, pruned)

        # Exclude reasons from pruning passes
        for uri, reason in pruned.excluded.items():
            expl.exclude_reasons[uri] = self._humanise_exclude(reason)

        # Entities that were in raw but removed by pruner
        raw_uris  = {r.s for r in raw.records} | {r.o for r in raw.records
                     if r.o.startswith("http")}
        kept_uris = {r.s for r in pruned.records} | {r.o for r in pruned.records
                     if r.o.startswith("http")}
        implicit_removed = raw_uris - kept_uris - set(pruned.excluded)
        for uri in implicit_removed:
            expl.exclude_reasons[uri] = "removed during pruning (budget or dedup)"

        # Rule log
        expl.rule_log = self._build_rule_log(raw, pruned)  # type: ignore[arg-type]

        # Summary
        expl.summary = self._build_summary(raw, pruned, expl)

        return expl

    def _humanise_include(self, uri: str, reason: str, p: ContextPacket) -> str:
        if reason == "anchor":
            return f"anchor entity — this is the subject of the context request"
        if "BFS depth" in reason:
            depth = reason.split()[-1]
            # Find the predicate path that brought it in
            paths = [r.p.split("/")[-1].split("#")[-1]
                     for r in p.records if r.o == uri or r.s == uri]
            via = paths[0] if paths else "unknown predicate"
            return f"reached at depth {depth} via {via}"
        return reason

    def _humanise_exclude(self, reason: str) -> str:
        if "metadata predicate" in reason:
            return "structural/metadata triple — not semantically relevant to LLM"
        if "duplicate" in reason:
            return "duplicate (s, p) pair — shallower copy kept"
        if "depth" in reason and "budget" in reason:
            return "too far from anchor and exceeded token budget"
        if "truncated" in reason:
            return reason
        return reason

    def _build_rule_log(self, raw: ContextPacket,
                        pruned: ContextPacket) -> list[str]:
        log = []
        log.append(f"BFS completed: {raw.triple_count} triples at depth ≤ {raw.depth_used}")
        log.append(f"Token estimate before pruning: ~{raw.token_estimate}")

        removed_total = raw.triple_count - pruned.triple_count
        if removed_total:
            meta_count = sum(1 for r in raw.records if r.is_metadata)
            log.append(f"Pass 1 — metadata strip: up to {meta_count} metadata triples eligible")
            log.append(f"Total removed: {removed_total} triples")

        log.append(f"Token estimate after pruning: ~{pruned.token_estimate}")
        log.append(f"Databook fragments retained: {len(pruned.databook_fragments)}")
        return log

    def _build_summary(self, raw: ContextPacket, pruned: ContextPacket,
                       expl: ContextExplanation) -> str:
        anchor_local = _local(pruned.anchor_uri)
        n_inc = len(expl.include_reasons)
        n_exc = len(expl.exclude_reasons)
        budget_status = "within budget" if pruned.token_estimate <= 4000 else "over budget"

        return (
            f"Context built around '{anchor_local}' ({pruned.anchor_type}) at depth "
            f"{pruned.depth_used}. {n_inc} entities included, {n_exc} excluded. "
            f"~{pruned.token_estimate} tokens ({budget_status}). "
            f"{len(pruned.databook_fragments)} Databook fragment(s) attached."
        )


def _local(uri: str) -> str:
    return uri.split("/")[-1].split("#")[-1].replace("-", "_")
