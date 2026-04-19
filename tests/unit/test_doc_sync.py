"""Unit tests for pipeline/doc_sync.py

Bug under test:
  Generated Markdown lacks the opening --- delimiter for YAML frontmatter.
"""
import pytest
from pathlib import Path
from rdflib import Namespace, RDF, Literal

from storage.graph_store import GraphStore
from storage.id_manager import uri, graph_uri
from pipeline.event_logger import EventLogger
from pipeline.doc_sync import DocSync

DB = Namespace("https://ontologist.ai/ns/databook#")
OE = Namespace("https://ontologist.ai/ns/oe/")


def make_databook(store, db_id="test_book", title="Test Book",
                  version="1.0.0", db_type="reference",
                  created="2026-04-18", content="# Hello\n"):
    db_uri = uri("databook", db_id)
    g = graph_uri(db_uri, "interior")
    store.add(db_uri, RDF.type, DB.Databook, g)
    store.add(db_uri, DB.id,      Literal(db_id),   g)
    store.add(db_uri, DB.title,   Literal(title),    g)
    store.add(db_uri, DB.version, Literal(version),  g)
    store.add(db_uri, DB.type,    Literal(db_type),  g)
    store.add(db_uri, DB.created, Literal(created),  g)
    store.add(db_uri, DB.content, Literal(content),  g)
    return db_uri


@pytest.fixture
def syncer(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    store = GraphStore()
    logger = EventLogger(store)
    return DocSync(store, logger), store


class TestFindDatabooks:
    def test_finds_databook_uri(self, syncer):
        ds, store = syncer
        make_databook(store)
        written = ds.sync_all()
        assert len(written) == 1

    def test_no_databooks_returns_empty(self, syncer):
        ds, store = syncer
        written = ds.sync_all()
        assert written == []


class TestFrontmatterFormat:
    def test_file_starts_with_dashes(self, syncer, tmp_path):
        """Regression: frontmatter must open with ---"""
        ds, store = syncer
        make_databook(store)
        ds.sync_all()
        files = list((tmp_path / "docs" / "databooks").glob("*.md"))
        assert len(files) == 1
        text = files[0].read_text()
        assert text.startswith("---\n"), (
            f"Frontmatter does not start with '---\\n'. Got:\n{text[:100]}"
        )

    def test_file_has_closing_dashes(self, syncer, tmp_path):
        ds, store = syncer
        make_databook(store)
        ds.sync_all()
        text = list((tmp_path / "docs" / "databooks").glob("*.md"))[0].read_text()
        lines = text.splitlines()
        # The second --- must appear somewhere after line 1
        assert "---" in lines[1:], "No closing --- found in frontmatter"

    def test_frontmatter_contains_title(self, syncer, tmp_path):
        ds, store = syncer
        make_databook(store, title="My Databook")
        ds.sync_all()
        text = list((tmp_path / "docs" / "databooks").glob("*.md"))[0].read_text()
        assert "My Databook" in text

    def test_body_after_frontmatter(self, syncer, tmp_path):
        ds, store = syncer
        make_databook(store, content="# Real body\n\nSome content.")
        ds.sync_all()
        text = list((tmp_path / "docs" / "databooks").glob("*.md"))[0].read_text()
        assert "# Real body" in text

    def test_synced_at_in_frontmatter(self, syncer, tmp_path):
        ds, store = syncer
        make_databook(store)
        ds.sync_all()
        text = list((tmp_path / "docs" / "databooks").glob("*.md"))[0].read_text()
        assert "synced_at" in text


class TestSyncEntity:
    def test_sync_entity_by_uri(self, syncer, tmp_path):
        ds, store = syncer
        db_uri = make_databook(store, db_id="single")
        path = ds.sync_entity(str(db_uri))
        assert path is not None
        assert Path(path).exists()

    def test_missing_id_returns_none(self, syncer):
        ds, store = syncer
        from rdflib import URIRef
        path = ds.sync_entity("https://ontologist.ai/ns/oe/databook/nonexistent")
        assert path is None


class TestDocSyncEvent:
    def test_event_logged_on_sync(self, syncer, tmp_path):
        ds, store = syncer
        make_databook(store)
        ds.sync_all()
        results = list(store.query(
            "SELECT ?s WHERE { ?s a <https://ontologist.ai/ns/oe/DocumentationSynced> }"
        ))
        assert len(results) >= 1
