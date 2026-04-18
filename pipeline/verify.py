"""Stage 5 pipeline: load graph → rule engine → optional human verification."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.graph_store import GraphStore
from verification.rule_engine import RuleEngine
from verification.verify_cli import VerifyCLI

GRAPH_IN  = "logs/graphs/introspection.trig"
GRAPH_OUT = "logs/graphs/verified.trig"


def main(interactive: bool = True, graph_path: str = GRAPH_IN) -> RuleEngine:
    store = GraphStore()

    print(f"Loading graph from {graph_path}...")
    store.load(graph_path)
    print(f"  {store}")

    print("\n=== Stage 5: Rule Engine ===")
    engine = RuleEngine(store)
    report = engine.run()
    print()
    report.print_all()

    if interactive and report.all_issues:
        print("\n=== Stage 5: Human Verification ===")
        cli = VerifyCLI(store, report, auto_confirm_infos=True)
        cli.run()

    store.save(GRAPH_OUT)
    print(f"\nVerified graph saved → {GRAPH_OUT}")

    if not report.conforms:
        print("\nPipeline halted — unresolved violations remain.")
        sys.exit(1)

    print("\nStage 5 complete — graph is conformant.")
    return engine


if __name__ == "__main__":
    interactive = "--auto" not in sys.argv
    graph = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") \
            else GRAPH_IN
    main(interactive=interactive, graph_path=graph)
