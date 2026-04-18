"""Stage 9 pipeline: export graph → DOT + JSON → open viewer."""
import sys
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.graph_store import GraphStore
from visualization.graph_exporter import export_json, export_dot

GRAPH_IN   = "logs/graphs/executed.trig"
JSON_OUT   = "logs/graphs/graph.json"
DOT_OUT    = "logs/graphs/graph.dot"
VIEWER     = "visualization/graph_viewer/index.html"


def main(
    graph_path: str = GRAPH_IN,
    open_browser: bool = False,
    include_events: bool = False,
) -> None:
    store = GraphStore()
    print(f"Loading graph from {graph_path}...")
    store.load(graph_path)
    print(f"  {store}\n")

    print("=== Stage 9: GraphExporter ===")

    eg = export_json(store, JSON_OUT, include_events=include_events)
    print(f"  JSON → {JSON_OUT}  ({len(eg.nodes)} nodes, {len(eg.edges)} edges)")

    export_dot(store, DOT_OUT, include_events=include_events)
    print(f"  DOT  → {DOT_OUT}")

    # Group summary
    from collections import Counter
    groups = Counter(n.group for n in eg.nodes)
    for g, n in sorted(groups.items()):
        print(f"    {g:12} {n} nodes")

    print(f"\nViewer: {Path(VIEWER).resolve()}")
    if open_browser:
        webbrowser.open(str(Path(VIEWER).resolve().as_uri()))
        print("  Opened in browser.")
    else:
        print("  Run with --open to launch browser, or open the file directly.")

    print("\nStage 9 complete.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Stage 9 — Graph Visualization Export")
    parser.add_argument("--graph",   default=GRAPH_IN, help="Input .trig graph")
    parser.add_argument("--open",    action="store_true", help="Open viewer in browser")
    parser.add_argument("--events",  action="store_true", help="Include event nodes")
    args = parser.parse_args()
    main(graph_path=args.graph, open_browser=args.open, include_events=args.events)
