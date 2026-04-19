"""Unit tests for storage/id_manager.py"""
import pytest
from rdflib import URIRef
from storage.id_manager import uri, graph_uri, _slug

BASE = "https://ontologist.ai/ns/oe/"


class TestSlug:
    def test_lowercase(self):
        assert _slug("MyModule") == "mymodule"

    def test_spaces_become_dashes(self):
        assert _slug("hello world") == "hello-world"

    def test_dots_become_dashes(self):
        assert _slug("code_parser.py") == "code-parser-py"

    def test_multiple_separators_collapse(self):
        assert _slug("a__b--c") == "a-b-c"

    def test_leading_trailing_stripped(self):
        assert _slug("  foo  ") == "foo"

    def test_path_separator(self):
        assert _slug("introspection/code_parser.py") == "introspection-code-parser-py"


class TestUri:
    def test_module_uri(self):
        result = uri("module", "storage/graph_store.py")
        assert isinstance(result, URIRef)
        assert str(result) == BASE + "module/storage-graph-store-py"

    def test_task_uri(self):
        result = uri("task", "my task")
        assert str(result) == BASE + "task/my-task"

    def test_unknown_type_uses_type_as_prefix(self):
        result = uri("custom", "foo")
        assert "custom/foo" in str(result)

    def test_returns_uriref(self):
        assert isinstance(uri("project", "ontology-engine"), URIRef)


class TestGraphUri:
    def test_interior(self):
        holon = URIRef(BASE + "module/foo")
        g = graph_uri(holon, "interior")
        assert str(g) == BASE + "module/foo/interior"

    def test_boundary(self):
        holon = URIRef(BASE + "module/bar")
        assert str(graph_uri(holon, "boundary")).endswith("/boundary")

    def test_all_layers(self):
        holon = URIRef(BASE + "module/x")
        for layer in ("interior", "boundary", "projection", "context"):
            assert graph_uri(holon, layer) == URIRef(str(holon) + f"/{layer}")
