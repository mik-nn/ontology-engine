"""Unit tests for storage/graph_store.py"""
import pytest
import tempfile
from pathlib import Path
from rdflib import URIRef, Literal, Namespace, RDF

from storage.graph_store import GraphStore
from storage.id_manager import uri, graph_uri

OE  = Namespace("https://ontologist.ai/ns/oe/")
CGA = Namespace("https://ontologist.ai/ns/cga/")


@pytest.fixture
def store():
    return GraphStore()


@pytest.fixture
def populated_store():
    s = GraphStore()
    mod = uri("module", "foo.py")
    g   = graph_uri(mod, "interior")
    s.add(mod, RDF.type, OE.CodeModule, g)
    s.add(mod, OE.functionName, Literal("foo"), g)
    return s, mod


class TestAdd:
    def test_add_triple_default_graph(self, store):
        s = URIRef("urn:s")
        p = URIRef("urn:p")
        o = Literal("hello")
        store.add(s, p, o)
        assert len(store) == 1

    def test_add_triple_named_graph(self, store):
        s = URIRef("urn:s")
        g = URIRef("urn:graph")
        store.add(s, RDF.type, OE.CodeModule, g)
        assert len(store) == 1

    def test_add_many(self, store):
        triples = [
            (URIRef("urn:a"), RDF.type, OE.CodeModule),
            (URIRef("urn:b"), RDF.type, OE.CodeFunction),
        ]
        store.add_many(triples)
        assert len(store) == 2


class TestDeclareHolon:
    def test_declares_four_graphs(self, store):
        holon = uri("module", "test.py")
        store.declare_holon(holon, OE.CodeModule)
        # The context graph should contain 5 triples (type + 4 graph links)
        ctx = graph_uri(holon, "context")
        ctx_g = store._g.get_context(ctx)
        assert len(ctx_g) == 5

    def test_holon_has_interior(self, store):
        holon = uri("module", "test.py")
        store.declare_holon(holon, OE.CodeModule)
        interior = graph_uri(holon, "interior")
        assert store._g.get_context(interior) is not None


class TestQuery:
    def test_sparql_select(self, populated_store):
        store, mod = populated_store
        results = list(store.query(
            "SELECT ?s WHERE { ?s a <https://ontologist.ai/ns/oe/CodeModule> }"
        ))
        assert len(results) == 1
        assert str(results[0][0]) == str(mod)


class TestValidate:
    def test_validate_returns_tuple(self, store):
        result = store.validate(["core/shacl/databook_shapes.ttl"])
        assert isinstance(result, tuple)
        assert len(result) == 2
        conforms, text = result
        assert isinstance(conforms, bool)
        assert isinstance(text, str)

    def test_empty_store_conforms(self, store):
        conforms, _ = store.validate(["core/shacl/databook_shapes.ttl"])
        assert conforms is True


class TestSaveLoad:
    def test_roundtrip(self, populated_store, tmp_path):
        store, mod = populated_store
        path = str(tmp_path / "test.trig")
        store.save(path)
        assert Path(path).exists()

        store2 = GraphStore()
        store2.load(path)
        assert len(store2) == len(store)

    def test_save_creates_parent_dirs(self, populated_store, tmp_path):
        store, _ = populated_store
        deep = str(tmp_path / "a" / "b" / "out.trig")
        store.save(deep)
        assert Path(deep).exists()


class TestLen:
    def test_empty_store_len_zero(self, store):
        assert len(store) == 0

    def test_len_after_add(self, store):
        store.add(URIRef("urn:s"), RDF.type, OE.CodeModule)
        assert len(store) == 1

    def test_repr(self, store):
        r = repr(store)
        assert "GraphStore" in r
