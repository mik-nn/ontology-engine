"""End-to-end tests for the ontology engine pipeline.

Each test exercises one or more pipeline stages against the real project
source tree. Tests run from the project root (enforced by conftest.py).
"""
import pytest
from pathlib import Path
from rdflib import Namespace, RDF

from storage.graph_store import GraphStore
from storage.id_manager import uri

OE  = Namespace("https://ontologist.ai/ns/oe/")
DB  = Namespace("https://ontologist.ai/ns/databook#")
CGA = Namespace("https://ontologist.ai/ns/cga/")


# ──────────────────────────────────────────────
# Stage 2 — Introspection
# ──────────────────────────────────────────────

class TestIntrospection:
    @pytest.fixture
    def introspected(self):
        from introspection.project_scanner import ProjectScanner
        from introspection.code_parser import CodeParser
        from introspection.doc_parser import DocParser

        store = GraphStore()
        ProjectScanner(store, project_root=".").scan()
        CodeParser(store, project_root=".").parse_all()
        DocParser(store, project_root=".").parse_all()
        return store

    def test_project_holon_created(self, introspected):
        results = list(introspected.query(
            "SELECT ?s WHERE { ?s a <https://ontologist.ai/ns/oe/ProjectHolon> }"
        ))
        assert len(results) >= 1

    def test_code_modules_detected(self, introspected):
        results = list(introspected.query(
            "SELECT ?s WHERE { ?s a <https://ontologist.ai/ns/oe/CodeModule> }"
        ))
        assert len(results) >= 10, f"Expected many CodeModules, got {len(results)}"

    def test_code_functions_parsed(self, introspected):
        results = list(introspected.query(
            "SELECT ?s WHERE { ?s a <https://ontologist.ai/ns/oe/CodeFunction> }"
        ))
        assert len(results) >= 5

    def test_data_modules_detected(self, introspected):
        results = list(introspected.query(
            "SELECT ?s WHERE { ?s a <https://ontologist.ai/ns/oe/DataModule> }"
        ))
        assert len(results) >= 1

    def test_depends_on_edges_exist(self, introspected):
        results = list(introspected.query(
            "SELECT ?s ?o WHERE { ?s <https://ontologist.ai/ns/oe/dependsOn> ?o }"
        ))
        assert len(results) >= 1

    def test_graph_store_module_present(self, introspected):
        """graph_store.py must be detected as a CodeModule."""
        results = list(introspected.query("""
            SELECT ?s WHERE {
                ?s a <https://ontologist.ai/ns/oe/CodeModule> .
                FILTER(CONTAINS(STR(?s), "graph-store"))
            }
        """))
        assert len(results) >= 1

    def test_save_and_reload(self, introspected, tmp_path):
        path = str(tmp_path / "introspection.trig")
        introspected.save(path)
        store2 = GraphStore()
        store2.load(path)
        assert len(store2) == len(introspected)


# ──────────────────────────────────────────────
# Stage 5 — Verification
# ──────────────────────────────────────────────

class TestVerification:
    @pytest.fixture
    def verified(self):
        from introspection.project_scanner import ProjectScanner
        from introspection.code_parser import CodeParser
        from verification.rule_engine import RuleEngine

        store = GraphStore()
        ProjectScanner(store, project_root=".").scan()
        CodeParser(store, project_root=".").parse_all()

        engine = RuleEngine(store, shapes_paths=[
            "core/shacl/databook_shapes.ttl",
            "core/shacl/dependencies_shapes.ttl",
        ])
        return engine.run(), store

    def test_verification_returns_rule_report(self, verified):
        from verification.rule_engine import RuleReport
        report, _ = verified
        assert isinstance(report, RuleReport)

    def test_no_p01_cycles_in_project(self, verified):
        """The real project must have no dependency cycles."""
        report, _ = verified
        cycles = [v for v in report.violations if v.rule_id == "P01"]
        assert cycles == [], f"Found cycles: {[v.message for v in cycles]}"

    def test_shacl_conforms_on_real_project(self, verified):
        """SHACL must not produce hard violations on the real project."""
        report, _ = verified
        shacl_violations = [v for v in report.violations if v.source == "shacl"]
        assert shacl_violations == [], (
            f"SHACL violations: {[v.message for v in shacl_violations]}"
        )


# ──────────────────────────────────────────────
# Stage 7 — Planning
# ──────────────────────────────────────────────

class TestPlanning:
    @pytest.fixture
    def plan_result(self):
        from planning.task_classifier import TaskClassifier
        from planning.task_decomposer import TaskDecomposer
        from planning.task_planner import TaskPlanner

        store = GraphStore()
        classifier = TaskClassifier(store)
        result = classifier.classify("implement a new enrichment module")

        decomposer = TaskDecomposer(store)
        tree = decomposer.decompose(result)

        planner = TaskPlanner(store, shapes=[
            "core/shacl/databook_shapes.ttl",
            "core/shacl/dependencies_shapes.ttl",
        ])
        spec = planner.plan(tree)
        return result, tree, spec, store

    def test_classifier_returns_implement(self, plan_result):
        result, _, _, _ = plan_result
        assert result.task_type == "ImplementTask"

    def test_tree_has_nodes(self, plan_result):
        _, tree, _, _ = plan_result
        assert len(tree.nodes) >= 1

    def test_plan_spec_has_id(self, plan_result):
        _, _, spec, _ = plan_result
        assert spec.plan_id

    def test_subtasks_written_to_graph(self, plan_result):
        _, _, spec, store = plan_result
        results = list(store.query(
            "SELECT ?s WHERE { ?s a <https://ontologist.ai/ns/oe/Subtask> }"
        ))
        assert len(results) >= 1


# ──────────────────────────────────────────────
# Stage 8+9 — DocSync + Visualization
# ──────────────────────────────────────────────

class TestDocSync:
    def test_sync_all_returns_list(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from rdflib import Literal
        from storage.id_manager import graph_uri
        from pipeline.event_logger import EventLogger
        from pipeline.doc_sync import DocSync

        store = GraphStore()
        logger = EventLogger(store)
        syncer = DocSync(store, logger)

        # Populate with a minimal databook
        db_uri = uri("databook", "e2e-test")
        g = graph_uri(db_uri, "interior")
        store.add(db_uri, RDF.type, DB.Databook, g)
        store.add(db_uri, DB.id, Literal("e2e_test"), g)
        store.add(db_uri, DB.title, Literal("E2E Test Book"), g)

        written = syncer.sync_all()
        assert isinstance(written, list)
        assert len(written) == 1

    def test_synced_file_valid_frontmatter(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from rdflib import Literal
        from storage.id_manager import graph_uri
        from pipeline.event_logger import EventLogger
        from pipeline.doc_sync import DocSync

        store = GraphStore()
        syncer = DocSync(store, EventLogger(store))

        db_uri = uri("databook", "fmtest")
        g = graph_uri(db_uri, "interior")
        store.add(db_uri, RDF.type, DB.Databook, g)
        store.add(db_uri, DB.id, Literal("fmtest"), g)
        store.add(db_uri, DB.title, Literal("FM Test"), g)

        syncer.sync_all()
        text = list((tmp_path / "docs" / "databooks").glob("*.md"))[0].read_text()
        assert text.startswith("---\n")


class TestVisualization:
    def test_export_json_produces_nodes_and_edges(self):
        from introspection.project_scanner import ProjectScanner
        from visualization.graph_exporter import export_json
        import tempfile, os

        store = GraphStore()
        ProjectScanner(store, project_root=".").scan()

        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "graph.json")
            result = export_json(store, out)
            assert len(result.nodes) >= 1
            assert Path(out).exists()

    def test_export_dot_produces_file(self):
        from introspection.project_scanner import ProjectScanner
        from visualization.graph_exporter import export_dot
        import tempfile, os

        store = GraphStore()
        ProjectScanner(store, project_root=".").scan()

        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "graph.dot")
            export_dot(store, out)
            assert Path(out).exists()
            content = Path(out).read_text()
            assert "digraph" in content


# ──────────────────────────────────────────────
# Full pipeline (--auto, no git/push)
# ──────────────────────────────────────────────

class TestFullPipeline:
    def test_pipeline_runs_without_exception(self, tmp_path, monkeypatch):
        """Full orchestrator run in --auto mode must not crash."""
        # Redirect log output to tmp_path to avoid polluting project logs
        monkeypatch.setenv("OE_LOGS_DIR", str(tmp_path / "logs"))

        from pipeline.pipeline_orchestrator import PipelineOrchestrator
        orchestrator = PipelineOrchestrator(auto=True, commit=False,
                                            push=False, verbose=False)
        run = orchestrator.run("analyze the ontology engine project")

        assert not run.failed, f"Pipeline failed: {run.errors}"

    def test_pipeline_produces_introspection_graph(self, tmp_path, monkeypatch):
        monkeypatch.setenv("OE_LOGS_DIR", str(tmp_path / "logs"))

        from pipeline.pipeline_orchestrator import PipelineOrchestrator, GRAPH_INTROSPECT
        orchestrator = PipelineOrchestrator(auto=True, commit=False,
                                            push=False, verbose=False)
        orchestrator.run("explain the graph store module")
        assert Path(GRAPH_INTROSPECT).exists()
