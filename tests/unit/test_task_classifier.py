"""Unit tests for planning/task_classifier.py

TaskClassifier has three modes:
  mode 0 (sparql+verb): entity-type reasoning from graph + verb detection via _VERB_TASK
  mode 1 (keyword):     pattern scoring via _RULES — used when mode 0 returns None
  mode 2 (micro_model): TF-IDF + LogisticRegression — used when both above are weak

When the store is empty, mode 0 fires verb_only (confidence 0.55) if the request
contains a verb matched by _VERB_TASK, otherwise returns None and mode 1 (keyword)
takes over.
"""
import pytest
from storage.graph_store import GraphStore
from planning.task_classifier import TaskClassifier, ClassificationResult
from planning.task_type_registry import ALL_TYPES

ALL_TASK_TYPES = set(ALL_TYPES)


@pytest.fixture
def clf():
    return TaskClassifier(GraphStore())


# ── Result structure ───────────────────────────────────────────────────────

class TestClassificationResult:
    def test_returns_classification_result(self, clf):
        result = clf.classify("explain how this works")
        assert isinstance(result, ClassificationResult)

    def test_task_type_is_known(self, clf):
        result = clf.classify("implement a new module")
        assert result.task_type in ALL_TASK_TYPES

    def test_confidence_in_range(self, clf):
        result = clf.classify("refactor the pipeline")
        assert 0.0 <= result.confidence <= 1.0

    def test_scores_cover_all_14_types(self, clf):
        result = clf.classify("build something")
        assert set(result.scores.keys()) == ALL_TASK_TYPES

    def test_raw_request_stored(self, clf):
        req = "refactor the event logger"
        result = clf.classify(req)
        assert result.raw_request == req

    def test_matched_entities_is_list(self, clf):
        result = clf.classify("explain graph_store")
        assert isinstance(result.matched_entities, list)

    def test_mode_used_is_string(self, clf):
        result = clf.classify("implement a feature")
        assert isinstance(result.mode_used, str)
        assert result.mode_used != ""


# ── Task type classification ───────────────────────────────────────────────
#
# These cases use inputs that produce a deterministic winner.
# Mode is noted for documentation but not asserted — only the task type matters.

class TestClassification:
    @pytest.mark.parametrize("text,expected", [
        # ExplainTask — "explain" matches _VERB_TASK → verb_only
        ("explain how the graph store works",       "ExplainTask"),
        ("describe the pipeline stages",             "ExplainTask"),
        # ImplementTask — "implement"/"create" match _VERB_TASK → verb_only
        ("implement a new enrichment module",        "ImplementTask"),
        ("create a new Tavily client",               "ImplementTask"),
        # RefactorTask — "refactor"/"optimize" match _VERB_TASK → verb_only
        ("refactor the rule engine",                 "RefactorTask"),
        ("optimize the context builder",             "RefactorTask"),
        # AnalysisTask — "analyze" matches _VERB_TASK → verb_only
        ("analyze the dependency graph",             "AnalysisTask"),
        ("investigate the missing entities",         "AnalysisTask"),
        # DesignTask — "design"/"architect" match _VERB_TASK → verb_only
        ("design a new ontology schema",             "DesignTask"),
        ("architect the enrichment layer",           "DesignTask"),
        # ReviewTask — "review" + "code" matches _RULES → keyword
        ("review the SHACL violations",              "ReviewTask"),
        ("review this pull request for issues",      "ReviewTask"),
        # GitTask — "commit" without "git" matches _RULES → keyword
        ("commit all changed files",                 "GitTask"),
        ("push to github",                           "GitTask"),
        # ValidateTask — "run tests" doesn't match _VERB_TASK → keyword
        ("run the full test suite",                  "ValidateTask"),
        ("check SHACL conformance",                  "ValidateTask"),
        # DebugTask — "debug" matches _VERB_TASK → verb_only
        ("debug why the pipeline fails",             "DebugTask"),
        ("trace the root cause of the error",        "DebugTask"),
        # SearchTask — "search" matches _VERB_TASK → verb_only
        ("search for the rdflib docs",               "SearchTask"),
        ("look up the ollama REST API",              "SearchTask"),
        # DocumentTask — "write documentation" matches _VERB_TASK → verb_only
        ("write documentation for the context builder", "DocumentTask"),
        ("update readme with new CLI commands",          "DocumentTask"),
        # MigrateTask — "migrate" stem doesn't match _VERB_TASK boundary → keyword
        ("migrate from ConjunctiveGraph to Dataset", "MigrateTask"),
        ("upgrade the anthropic SDK to latest",      "MigrateTask"),
        # IntegrateTask — "integrate" stem doesn't match _VERB_TASK → keyword
        ("integrate the ollama adapter with the factory", "IntegrateTask"),
        ("integrate the metrics module into the pipeline", "IntegrateTask"),
        # ComplexTask — "end-to-end" matches _RULES → keyword
        ("end-to-end implementation of the full pipeline", "ComplexTask"),
        ("comprehensive redesign of the context strategy", "ComplexTask"),
    ])
    def test_classifies_correctly(self, clf, text, expected):
        result = clf.classify(text)
        assert result.task_type == expected, (
            f"Expected {expected}, got {result.task_type} "
            f"(mode={result.mode_used}, scores={result.scores})"
        )


# ── Mode detection ─────────────────────────────────────────────────────────

class TestModeDetection:
    def test_verb_only_mode_when_verb_matches_verb_task(self, clf):
        # "explain" matches _VERB_TASK pattern exactly → mode0 fires verb_only
        result = clf.classify("explain how the graph store works")
        assert result.mode_used == "verb_only"

    def test_keyword_mode_when_verb_doesnt_match_verb_task(self, clf):
        # "commit" without "git" doesn't match _VERB_TASK → mode0 returns None → mode1
        result = clf.classify("commit all changed files")
        assert result.mode_used == "keyword"

    def test_keyword_mode_for_migrate(self, clf):
        # "migrate" stem is "migrat" which doesn't match \b(migrat)\b in _VERB_TASK
        result = clf.classify("migrate from ConjunctiveGraph to Dataset")
        assert result.mode_used == "keyword"

    def test_keyword_mode_for_integrate(self, clf):
        result = clf.classify("integrate the ollama adapter")
        assert result.mode_used == "keyword"

    def test_confidence_above_threshold_for_clear_verb(self, clf):
        # A clear verb match should produce confidence >= threshold (0.45)
        result = clf.classify("implement a brand new authentication module")
        assert result.confidence >= 0.45

    def test_confidence_above_threshold_for_clear_keyword(self, clf):
        result = clf.classify("commit and push all staged files to github")
        assert result.confidence >= 0.45


# ── Entity matching ────────────────────────────────────────────────────────

class TestEntityMatching:
    def test_no_entities_on_empty_store(self, clf):
        result = clf.classify("explain graph_store")
        assert result.matched_entities == []

    def test_entity_matched_from_store(self):
        from rdflib import Namespace, RDF
        from storage.id_manager import uri, graph_uri

        OE = Namespace("https://ontologist.ai/ns/oe/")
        store = GraphStore()
        mod = uri("module", "graph_store.py")
        g = graph_uri(mod, "interior")
        store.add(mod, RDF.type, OE.CodeModule, g)

        clf = TaskClassifier(store)
        # local slug: "graph-store-py" → space form "graph store py"
        result = clf.classify("explain graph store py module")
        assert str(mod) in result.matched_entities

    def test_entity_match_boosts_confidence(self):
        from rdflib import Namespace, RDF
        from storage.id_manager import uri, graph_uri

        OE = Namespace("https://ontologist.ai/ns/oe/")
        store = GraphStore()
        mod = uri("module", "context_builder.py")
        g = graph_uri(mod, "interior")
        store.add(mod, RDF.type, OE.CodeModule, g)

        clf_with_entity = TaskClassifier(store)
        clf_empty = TaskClassifier(GraphStore())

        r_entity = clf_with_entity.classify("refactor context builder py")
        r_empty  = clf_empty.classify("refactor context builder py")
        # Entity match gives sparql+verb mode → higher or equal confidence
        assert r_entity.confidence >= r_empty.confidence


# ── RDF event emission ─────────────────────────────────────────────────────

class TestEventEmission:
    def test_event_written_to_graph(self, clf):
        clf.classify("implement a new feature")
        results = list(clf.store.query(
            "SELECT ?s WHERE { ?s a <https://ontologist.ai/ns/oe/TaskClassified> }"
        ))
        assert len(results) >= 1

    def test_event_contains_task_type(self, clf):
        clf.classify("explain the pipeline")
        results = list(clf.store.query(
            "SELECT ?t WHERE { ?s a <https://ontologist.ai/ns/oe/TaskClassified> ;"
            "                    <https://ontologist.ai/ns/oe/taskType> ?t }"
        ))
        assert any(str(r.t) == "ExplainTask" for r in results)

    def test_multiple_classifications_emit_multiple_events(self, clf):
        clf.classify("explain the pipeline")
        clf.classify("implement a new module")
        results = list(clf.store.query(
            "SELECT ?s WHERE { ?s a <https://ontologist.ai/ns/oe/TaskClassified> }"
        ))
        assert len(results) >= 2
