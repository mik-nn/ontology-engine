"""Stage 7 pipeline: classify → decompose → plan → execute → validate."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.graph_store import GraphStore
from planning.task_classifier import TaskClassifier
from planning.task_decomposer import TaskDecomposer
from planning.task_planner import TaskPlanner
from planning.plan_executor import PlanExecutor
from verification.rule_engine import RuleEngine

GRAPH_IN   = "logs/graphs/verified.trig"
GRAPH_OUT  = "logs/graphs/planned.trig"
SHAPES = [
    "core/shacl/databook_shapes.ttl",
    "core/shacl/dependencies_shapes.ttl",
    "core/shacl/planning_shapes.ttl",
]


def main(request: str, graph_path: str = GRAPH_IN) -> None:
    store = GraphStore()
    print(f"Loading graph from {graph_path}...")
    store.load(graph_path)
    print(f"  {store}")
    print(f"\nRequest: \"{request}\"\n")

    # ── Stage 7a: Classify ──────────────────────────────────
    print("=== Stage 7a: TaskClassifier ===")
    classifier = TaskClassifier(store, use_llm_fallback=False)
    result = classifier.classify(request)
    print(f"  task_type  : {result.task_type}")
    print(f"  confidence : {result.confidence:.2f}  (mode: {result.mode_used})")
    print(f"  scores     : {result.scores}")
    print(f"  entities   : {len(result.matched_entities)} matched")

    # ── Stage 7b: Decompose ─────────────────────────────────
    print("\n=== Stage 7b: TaskDecomposer ===")
    decomposer = TaskDecomposer(store)
    tree = decomposer.decompose(result)
    print(f"  plan_id    : {tree.plan_id}")
    print(f"  subtasks   : {len(tree.nodes)}")
    for n in tree.nodes:
        deps = [tree.nodes[d].name for d in n.depends_on] or ["—"]
        print(f"    {n.index}. {n.task_type:14} {n.name:25} deps={deps}")

    # ── Stage 7c: Plan ──────────────────────────────────────
    print("\n=== Stage 7c: TaskPlanner ===")
    planner = TaskPlanner(store, shapes=SHAPES)
    spec = planner.plan(tree)
    print(spec.summary())

    # ── Stage 7d: Execute ───────────────────────────────────
    print("\n=== Stage 7d: PlanExecutor ===")
    executor = PlanExecutor(store, verbose=True)
    report = executor.execute(spec)
    report.print()

    # ── Stage 7e: Rule Engine ───────────────────────────────
    print("\n=== Stage 7e: Post-execution Validation ===")
    engine = RuleEngine(store, shapes_paths=SHAPES)
    rule_report = engine.run()
    print(rule_report.summary())

    store.save(GRAPH_OUT)
    print(f"\nGraph saved → {GRAPH_OUT}")
    print(f"Store: {store}")

    if not report.success:
        print("\nExecution had failures — check report above.")
        sys.exit(1)

    print("\nStage 7 complete.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 pipeline/plan.py "<request>"')
        sys.exit(1)
    request_text = " ".join(sys.argv[1:])
    graph = "logs/graphs/verified.trig"
    main(request_text, graph_path=graph)
