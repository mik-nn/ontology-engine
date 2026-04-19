"""Stage 9 pipeline: export graph → DOT + JSON → open viewer."""
import sys
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.graph_store import GraphStore
from visualization.graph_exporter import export_json, export_dot

GRAPH_IN        = "logs/graphs/executed.trig"
GRAPH_FALLBACK  = "logs/graphs/introspection.trig"
JSON_OUT        = "logs/graphs/graph.json"
DOT_OUT         = "logs/graphs/graph.dot"
VIEWER_TEMPLATE = "visualization/graph_viewer/index.html"
VIEWER_OUT      = "logs/graphs/viewer.html"


def _embed_into_html(graph_data: dict, template: str, out: str) -> None:
    """Inject graph JSON into viewer HTML — works with file:// (no CORS)."""
    import json
    html = Path(template).read_text(encoding="utf-8")
    inline = json.dumps(graph_data, ensure_ascii=False)
    html = html.replace(
        "const GRAPH_EMBEDDED = null; /* __GRAPH_DATA__ */",
        f"const GRAPH_EMBEDDED = {inline};",
    )
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(html, encoding="utf-8")


def main(
    graph_path: str = GRAPH_IN,
    open_browser: bool = False,
    include_events: bool = False,
) -> None:
    # Fallback to introspection graph if executed graph doesn't exist yet
    if not Path(graph_path).exists() and graph_path == GRAPH_IN:
        graph_path = GRAPH_FALLBACK

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
    import json
    groups = Counter(n.group for n in eg.nodes)
    for g, n in sorted(groups.items()):
        print(f"    {g:12} {n} nodes")

    # Generate standalone HTML with embedded data (works with file://)
    with open(JSON_OUT, encoding="utf-8") as f:
        graph_data = json.load(f)
    _embed_into_html(graph_data, VIEWER_TEMPLATE, VIEWER_OUT)
    print(f"\nStandalone viewer → {Path(VIEWER_OUT).resolve()}")

    if open_browser:
        webbrowser.open(str(Path(VIEWER_OUT).resolve().as_uri()))
        print("  Opened in browser.")
    else:
        print("  Open in browser: file://" + str(Path(VIEWER_OUT).resolve()))

    print("\nStage 9 complete.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Stage 9 — Graph Visualization Export")
    parser.add_argument("--graph",   default=GRAPH_IN, help="Input .trig graph")
    parser.add_argument("--open",    action="store_true", help="Open viewer in browser")
    parser.add_argument("--events",  action="store_true", help="Include event nodes")
    args = parser.parse_args()
    main(graph_path=args.graph, open_browser=args.open, include_events=args.events)
