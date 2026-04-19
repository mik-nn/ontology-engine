"""Unit tests for pipeline/event_logger.py"""
import pytest
from pathlib import Path
from rdflib import Namespace, RDF

from storage.graph_store import GraphStore
from pipeline.event_logger import EventLogger, PIPE

OE = Namespace("https://ontologist.ai/ns/oe/")


@pytest.fixture
def logger(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    store = GraphStore()
    return EventLogger(store), store


class TestLog:
    def test_returns_uri(self, logger):
        ev_logger, _ = logger
        ev = ev_logger.log("ProjectScanned", agent="TestAgent", status="completed")
        assert str(ev).startswith("https://ontologist.ai/ns/oe/event/")

    def test_event_written_to_store(self, logger):
        ev_logger, store = logger
        ev = ev_logger.log("ProjectScanned", agent="TestAgent", status="completed")
        results = list(store.query(
            f"SELECT ?s WHERE {{ GRAPH <{PIPE}> {{ ?s a <{OE.ProjectScanned}> }} }}"
        ))
        assert len(results) == 1
        assert str(results[0][0]) == str(ev)

    def test_agent_stored(self, logger):
        ev_logger, store = logger
        ev = ev_logger.log("PlanGenerated", agent="PipelineOrchestrator", status="ok")
        results = list(store.query(
            f'SELECT ?a WHERE {{ GRAPH <{PIPE}> {{ <{ev}> <{OE.hasAgent}> ?a }} }}'
        ))
        assert str(results[0][0]) == "PipelineOrchestrator"

    def test_extra_props_stored(self, logger):
        ev_logger, store = logger
        ev = ev_logger.log("OntologyValidated", agent="A", status="ok",
                           violationCount="3")
        results = list(store.query(
            f'SELECT ?v WHERE {{ GRAPH <{PIPE}> {{ <{ev}> <{OE.violationCount}> ?v }} }}'
        ))
        assert str(results[0][0]) == "3"

    def test_daily_log_file_created(self, logger, tmp_path):
        ev_logger, _ = logger
        ev_logger.log("ProjectScanned", agent="A", status="ok")
        log_files = list((tmp_path / "logs" / "events").glob("*.trig"))
        assert len(log_files) == 1

    def test_multiple_events_same_file(self, logger, tmp_path):
        ev_logger, _ = logger
        ev_logger.log("ProjectScanned", agent="A", status="ok")
        ev_logger.log("PlanGenerated", agent="B", status="ok")
        log_files = list((tmp_path / "logs" / "events").glob("*.trig"))
        assert len(log_files) == 1
