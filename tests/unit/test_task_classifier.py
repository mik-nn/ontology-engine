"""Unit tests for planning/task_classifier.py"""
import pytest
from storage.graph_store import GraphStore
from planning.task_classifier import TaskClassifier, ClassificationResult

TASK_TYPES = {"ExplainTask", "ImplementTask", "RefactorTask", "AnalysisTask", "DesignTask"}


@pytest.fixture
def classifier():
    return TaskClassifier(GraphStore())


class TestClassificationResult:
    def test_result_has_expected_fields(self, classifier):
        result = classifier.classify("explain how this works")
        assert isinstance(result, ClassificationResult)
        assert result.task_type in TASK_TYPES
        assert 0.0 <= result.confidence <= 1.0
        assert isinstance(result.matched_entities, list)
        assert isinstance(result.scores, dict)

    def test_scores_cover_all_types(self, classifier):
        result = classifier.classify("build something")
        assert set(result.scores.keys()) == TASK_TYPES


class TestKeywordClassification:
    @pytest.mark.parametrize("text,expected", [
        ("explain how the graph store works", "ExplainTask"),
        ("describe the pipeline stages",      "ExplainTask"),
        ("implement a new enrichment module", "ImplementTask"),
        ("create a Tavily client",            "ImplementTask"),
        ("refactor the rule engine",          "RefactorTask"),
        ("optimize the context builder",      "RefactorTask"),
        ("analyze the dependency graph",      "AnalysisTask"),
        ("review the SHACL violations",       "AnalysisTask"),
        ("design a new ontology schema",      "DesignTask"),
        ("architect the enrichment layer",    "DesignTask"),
    ])
    def test_classification(self, classifier, text, expected):
        result = classifier.classify(text)
        assert result.task_type == expected, (
            f"Expected {expected}, got {result.task_type} "
            f"(scores={result.scores})"
        )

    def test_mode_is_keyword(self, classifier):
        result = classifier.classify("implement a feature")
        assert result.mode_used == "keyword"

    def test_raw_request_stored(self, classifier):
        req = "refactor the event logger"
        result = classifier.classify(req)
        assert result.raw_request == req

    def test_confidence_above_threshold_for_clear_request(self, classifier):
        result = classifier.classify("implement a brand new authentication module")
        assert result.confidence > 0.45


class TestEntityMatching:
    def test_no_entities_on_empty_store(self, classifier):
        result = classifier.classify("explain graph_store")
        assert result.matched_entities == []

    def test_entity_matched_from_store(self):
        from rdflib import Namespace, RDF
        from storage.id_manager import uri, graph_uri

        OE = Namespace("https://ontologist.ai/ns/oe/")
        store = GraphStore()
        mod = uri("module", "graph_store.py")
        g = graph_uri(mod, "interior")
        store.add(mod, RDF.type, OE.CodeModule, g)

        # Classifier must be created AFTER populating the store
        # so _build_module_index() picks up the new module.
        clf = TaskClassifier(store)
        # _match_entities checks: slug (dashes→underscores) or local_name (dashes→spaces)
        # local "graph-store-py" → space form "graph store py"
        result = clf.classify("explain graph store py module")
        assert str(mod) in result.matched_entities
