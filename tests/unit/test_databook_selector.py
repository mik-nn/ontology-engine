"""Unit tests for context/databook_selector.py"""
import pytest
from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri, graph_uri
from context.databook_selector import DatabookSelector

DB = Namespace("https://ontologist.ai/ns/databook#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


def add_databook(store, db_id, title, scope, layer, hierarchy=1,
                 task_types=None, content="", depends_on=None):
    db_uri = uri("module", f"docs/databooks/{db_id}.md")
    g = graph_uri(db_uri, "interior")
    proj = graph_uri(db_uri, "projection")
    store.add(db_uri, RDF.type,    DB.Databook,          proj)
    store.add(db_uri, DB.id,       Literal(db_id),       g)
    store.add(db_uri, DB.title,    Literal(title),       g)
    store.add(db_uri, DB.scope,    Literal(scope),       g)
    store.add(db_uri, DB.layer,    Literal(layer),       g)
    store.add(db_uri, DB.hierarchy, Literal(hierarchy, datatype=XSD.integer), g)
    if content:
        store.add(db_uri, DB.content, Literal(content),  g)
    if task_types:
        store.add(db_uri, DB.taskType, Literal(",".join(task_types)), g)
    if depends_on:
        for dep_id in depends_on:
            dep_uri = uri("module", f"docs/databooks/{dep_id}.md")
            store.add(db_uri, DB.dependsOn, dep_uri, g)
    return db_uri


@pytest.fixture
def store_with_databooks():
    store = GraphStore()
    add_databook(store, "ARCH",    "Architecture", "permanent", "architecture", 0)
    add_databook(store, "CONV",    "Conventions",  "permanent", "architecture", 1, depends_on=["ARCH"])
    add_databook(store, "STACK",   "Stack",        "project",   "implementation", 1, depends_on=["ARCH"])
    add_databook(store, "TESTING", "Testing",      "task",      "spec", 1,
                 task_types=["testing"], depends_on=["CONV"])
    add_databook(store, "PLANNING","Planning",     "task",      "implementation", 1,
                 task_types=["planning"])
    add_databook(store, "TODO",    "Todo",         "ephemeral", "implementation", 3)
    return store


class TestSelect:
    def test_permanent_always_included(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        frags = sel.select()
        titles = {f["title"] for f in frags}
        assert "Architecture" in titles
        assert "Conventions" in titles

    def test_project_always_included(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        frags = sel.select()
        titles = {f["title"] for f in frags}
        assert "Stack" in titles

    def test_ephemeral_excluded_by_default(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        frags = sel.select()
        titles = {f["title"] for f in frags}
        assert "Todo" not in titles

    def test_ephemeral_included_when_requested(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        frags = sel.select(include_ephemeral=True)
        titles = {f["title"] for f in frags}
        assert "Todo" in titles

    def test_task_excluded_without_matching_type(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        frags = sel.select(task_type=None)
        titles = {f["title"] for f in frags}
        assert "Testing" not in titles
        assert "Planning" not in titles

    def test_task_included_with_matching_type(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        frags = sel.select(task_type="testing")
        titles = {f["title"] for f in frags}
        assert "Testing" in titles
        assert "Planning" not in titles

    def test_layer_filter(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        frags = sel.select(layer_filter="architecture")
        assert all(f.get("layer") == "architecture" for f in frags)

    def test_hierarchy_filter(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        frags = sel.select(max_hierarchy=0)
        assert all(f.get("hierarchy", 0) <= 0 for f in frags)

    def test_sorted_by_hierarchy_then_scope(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        frags = sel.select()
        # h=0 items come before h=1 items
        h_vals = [f.get("hierarchy", 3) for f in frags]
        assert h_vals == sorted(h_vals)

    def test_depends_on_dependency_pulled_in(self, store_with_databooks):
        """If a selected databook depends on another, dependency is included."""
        sel = DatabookSelector(store_with_databooks)
        # TESTING depends on CONV which depends on ARCH — both already permanent
        frags = sel.select(task_type="testing")
        titles = {f["title"] for f in frags}
        assert "Architecture" in titles
        assert "Conventions" in titles


class TestSelectRelevant:
    def test_returns_frags_and_was_chunked_flag(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        frags, was_chunked = sel.select_relevant(token_budget=100000)
        assert isinstance(frags, list)
        assert isinstance(was_chunked, bool)

    def test_large_budget_not_chunked(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        _, was_chunked = sel.select_relevant(token_budget=100000)
        assert was_chunked is False

    def test_tiny_budget_triggers_chunking(self, store_with_databooks):
        store = GraphStore()
        long_content = "word " * 500  # ~2500 chars
        add_databook(store, "BIG", "Big Doc", "permanent", "architecture", 0,
                     content=long_content)
        add_databook(store, "BIG2", "Big Doc 2", "permanent", "reference", 1,
                     content=long_content)
        sel = DatabookSelector(store)
        _, was_chunked = sel.select_relevant(token_budget=100)
        assert was_chunked is True

    def test_result_within_budget(self, store_with_databooks):
        store = GraphStore()
        content = "section word " * 200
        add_databook(store, "DOC1", "Doc One", "permanent", "architecture", 0, content=content)
        add_databook(store, "DOC2", "Doc Two", "project",   "implementation", 1, content=content)
        sel = DatabookSelector(store)
        frags, _ = sel.select_relevant(token_budget=200)
        total_tokens = sum(
            int(len(f.get("content_excerpt", "")) / 4 * 1.2)
            for f in frags
        )
        assert total_tokens <= 220  # slight slack


class TestSelectChain:
    def test_chain_follows_depends_on(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        testing_uri = str(uri("module", "docs/databooks/TESTING.md"))
        chain = sel.select_chain([testing_uri])
        titles = [f["title"] for f in chain]
        # TESTING depends on CONV, CONV depends on ARCH → chain: ARCH, CONV, TESTING
        assert titles.index("Architecture") < titles.index("Conventions")
        assert titles.index("Conventions") < titles.index("Testing")

    def test_chain_no_cycles(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        arch_uri = str(uri("module", "docs/databooks/ARCH.md"))
        chain = sel.select_chain([arch_uri])
        uris = [f["uri"] for f in chain]
        assert len(uris) == len(set(uris))  # no duplicates

    def test_chain_unknown_uri_ignored(self, store_with_databooks):
        sel = DatabookSelector(store_with_databooks)
        chain = sel.select_chain(["https://example.com/nonexistent"])
        assert chain == []
