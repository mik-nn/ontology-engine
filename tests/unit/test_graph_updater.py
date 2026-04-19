"""Unit tests for pipeline/graph_updater.py

Bug under test:
  _validate() calls store.validate() which returns tuple[bool, str],
  then tries to access .violations on the tuple → AttributeError.
"""
import pytest
from rdflib import Namespace, RDF, Literal

from storage.graph_store import GraphStore
from storage.id_manager import uri, graph_uri
from pipeline.event_logger import EventLogger
from pipeline.graph_updater import GraphUpdater, ApplyResult

OE = Namespace("https://ontologist.ai/ns/oe/")

SHAPES = [
    "core/shacl/databook_shapes.ttl",
    "core/shacl/dependencies_shapes.ttl",
]


@pytest.fixture
def store_with_subtask():
    store = GraphStore()
    sub = uri("subtask", "test-subtask-1")
    g = graph_uri(sub, "interior")
    store.add(sub, RDF.type, OE.Subtask, g)
    return store, sub


@pytest.fixture
def updater(store_with_subtask):
    # project_cwd (autouse) already set cwd = project root; shapes resolve correctly
    store, sub = store_with_subtask
    logger = EventLogger(store)
    return GraphUpdater(store, logger, SHAPES), store, sub


class TestApplyResult:
    def test_returns_apply_result(self, updater):
        gu, store, sub = updater
        result = gu.apply_result(
            subtask_uri=str(sub),
            status="completed",
            output_summary="All good",
            executor="test",
        )
        assert isinstance(result, ApplyResult)

    def test_successful_apply(self, updater):
        gu, store, sub = updater
        result = gu.apply_result(
            subtask_uri=str(sub),
            status="completed",
            output_summary="Done",
            executor="test",
        )
        assert result.success is True
        assert result.violations == []

    def test_failed_status_not_success(self, updater):
        gu, store, sub = updater
        result = gu.apply_result(
            subtask_uri=str(sub),
            status="failed",
            output_summary="Error occurred",
            executor="test",
        )
        assert result.success is False

    def test_status_written_to_graph(self, updater):
        gu, store, sub = updater
        gu.apply_result(
            subtask_uri=str(sub),
            status="completed",
            output_summary="summary",
            executor="rule",
        )
        val = store._g.value(sub, OE.hasStatus)
        assert str(val) == "completed"

    def test_output_summary_written(self, updater):
        gu, store, sub = updater
        gu.apply_result(
            subtask_uri=str(sub),
            status="completed",
            output_summary="my summary",
            executor="rule",
        )
        val = store._g.value(sub, OE.outputSummary)
        assert str(val) == "my summary"

    def test_extra_triples_written(self, updater):
        gu, store, sub = updater
        extra = [(sub, OE.customProp, Literal("custom_val"))]
        gu.apply_result(
            subtask_uri=str(sub),
            status="completed",
            output_summary="ok",
            executor="rule",
            extra_triples=extra,
        )
        val = store._g.value(sub, OE.customProp)
        assert str(val) == "custom_val"

    def test_validate_does_not_raise_attribute_error(self, updater):
        """Regression: _validate() must not raise AttributeError: 'tuple' has no .violations"""
        gu, store, sub = updater
        # This call triggers _validate() internally — must not raise
        try:
            result = gu.apply_result(
                subtask_uri=str(sub),
                status="completed",
                output_summary="ok",
                executor="rule",
            )
        except AttributeError as e:
            pytest.fail(f"_validate() raised AttributeError: {e}")
        assert isinstance(result.violations, list)
