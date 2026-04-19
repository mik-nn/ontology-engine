"""Stage 6 pipeline: load verified graph → build context → prune → explain → validate."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.graph_store import GraphStore
from context.context_builder import ContextBuilder
from context.context_pruner import ContextPruner
from context.context_explainer import ContextExplainer
from verification.rule_engine import RuleEngine

GRAPH_IN   = "logs/graphs/verified.trig"
CONTEXT_OUT = "logs/graphs/context.trig"
SHAPES = [
    "core/shacl/databook_shapes.ttl",
    "core/shacl/dependencies_shapes.ttl",
    "core/shacl/context_shapes.ttl",
]
MAX_TOKENS = 4000
MAX_DEPTH  = 3


def main(anchor_uri: str | None = None, graph_path: str = GRAPH_IN) -> dict:
    store = GraphStore()
    print(f"Loading graph from {graph_path}...")
    store.load(graph_path)
    print(f"  {store}")

    # Pick a default anchor: prefer graph_store or context_builder, else first CodeModule
    if not anchor_uri:
        from rdflib import Namespace, RDF
        OE = Namespace("https://ontologist.ai/ns/oe/")
        preferred = ("storage-graph-store-py", "context-context-builder-py",
                     "verification-rule-engine-py")
        candidates: list[str] = []
        for ctx in store._g.contexts():
            for s in ctx.subjects(RDF.type, OE.CodeModule):
                candidates.append(str(s))
        for pref in preferred:
            for c in candidates:
                if pref in c:
                    anchor_uri = c
                    break
            if anchor_uri:
                break
        if not anchor_uri and candidates:
            anchor_uri = candidates[0]

    if not anchor_uri:
        print("No anchor URI found — run Stage 2 first.")
        sys.exit(1)

    print(f"\n=== Stage 6: ContextBuilder (anchor={anchor_uri.split('/')[-1]}) ===")
    builder = ContextBuilder(store, max_depth=MAX_DEPTH, max_tokens=MAX_TOKENS)
    raw = builder.build(anchor_uri)
    print(f"  raw triples  : {raw.triple_count}")
    print(f"  token est.   : {raw.token_estimate}")
    print(f"  databooks    : {len(raw.databook_fragments)}")

    print("\n=== Stage 6: ContextPruner ===")
    pruner = ContextPruner(max_tokens=MAX_TOKENS)
    pruned = pruner.prune(raw)
    print(f"  after prune  : {pruned.triple_count} triples")
    print(f"  token est.   : {pruned.token_estimate}")
    print(f"  excluded     : {len(pruned.excluded)}")

    print("\n=== Stage 6: ContextExplainer ===")
    explainer = ContextExplainer()
    explanation = explainer.explain(raw, pruned)
    explanation.print()

    print("\n=== Stage 6: SHACL Validation (ContextPacket event) ===")
    conforms, report = store.validate(SHAPES)
    if conforms:
        print("  SHACL: PASS")
    else:
        print("  SHACL: FAIL")
        print(report)

    store.save(CONTEXT_OUT)
    print(f"\nGraph saved → {CONTEXT_OUT}")

    print("\n=== Prompt Text Preview (first 1200 chars) ===")
    prompt = pruned.to_prompt_text() + "\n\n" + explanation.as_prompt_section()
    print(prompt[:1200])
    print("…" if len(prompt) > 1200 else "")

    packet_json = pruned.to_json()
    json_path = "logs/graphs/context_packet.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(packet_json, f, indent=2, ensure_ascii=False)
    print(f"\nContext packet JSON → {json_path}")

    return packet_json


if __name__ == "__main__":
    anchor = sys.argv[1] if len(sys.argv) > 1 else None
    main(anchor_uri=anchor)
