"""Stage 2 pipeline: project introspection → graph store → SHACL validation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.graph_store import GraphStore
from introspection.project_scanner import ProjectScanner
from introspection.code_parser import CodeParser
from introspection.doc_parser import DocParser

GRAPH_OUT = "logs/graphs/introspection.trig"
SHAPES = [
    "core/shacl/databook_shapes.ttl",
    "core/shacl/dependencies_shapes.ttl",
]


def main(project_root: str = ".") -> GraphStore:
    store = GraphStore()

    print("=== Stage 2: ProjectScanner ===")
    result = ProjectScanner(store, project_root).scan()
    print(f"  project : {result['project_uri']}")
    print(f"  files   : {sum(result['file_counts'].values())} "
          f"({result['file_counts']})")

    print("\n=== Stage 2: CodeParser ===")
    code = CodeParser(store, project_root).parse_all()
    print(f"  classes : {code['classes']}")
    print(f"  functions: {code['functions']}")
    print(f"  imports : {code['imports']}")

    print("\n=== Stage 2: DocParser ===")
    docs = DocParser(store, project_root).parse_all()
    print(f"  databooks : {docs['databooks']}")
    print(f"  plain docs: {docs['plain_docs']}")

    print(f"\n=== Graph store: {store} ===")

    print("\n=== SHACL Validation ===")
    conforms, report = store.validate(SHAPES)
    if conforms:
        print("  SHACL: PASS")
    else:
        print("  SHACL: FAIL")
        print(report)
        sys.exit(1)

    store.save(GRAPH_OUT)
    print(f"\nGraph saved → {GRAPH_OUT}")
    return store


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    main(root)
