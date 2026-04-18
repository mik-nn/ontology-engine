"""Stage 4 pipeline: detect gaps → interview → enrich → validate → save."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.graph_store import GraphStore
from interaction.interviewer import Interviewer
from verification.rule_engine import RuleEngine

GRAPH_IN  = "logs/graphs/introspection.trig"
GRAPH_OUT = "logs/graphs/interviewed.trig"
SHAPES = [
    "core/shacl/databook_shapes.ttl",
    "core/shacl/dependencies_shapes.ttl",
    "core/shacl/planning_shapes.ttl",
]


def main(graph_path: str = GRAPH_IN) -> None:
    store = GraphStore()
    print(f"Loading graph from {graph_path}...")
    store.load(graph_path)
    print(f"  {store}\n")

    # ── Stage 4: Interview ──────────────────────────────────
    print("=== Stage 4: Interviewer ===")
    interviewer = Interviewer(store)
    session = interviewer.run()

    # ── Post-interview validation ───────────────────────────
    if session.gaps_closed > 0:
        print("=== Post-interview Validation ===")
        engine = RuleEngine(store, shapes_paths=SHAPES)
        report = engine.run()
        print(report.summary())

    store.save(GRAPH_OUT)
    print(f"\nGraph saved → {GRAPH_OUT}")
    print(f"Store: {store}")
    print("\nStage 4 complete.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Stage 4 — Interactive Interview"
    )
    parser.add_argument(
        "--graph",
        default=GRAPH_IN,
        help="Input .trig graph (default: logs/graphs/introspection.trig)",
    )
    args = parser.parse_args()
    main(graph_path=args.graph)
