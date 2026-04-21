"""Unit tests for new DocParser fields: scope, layer, hierarchy, taskType, dependsOn, transformer."""
import textwrap
import pytest
from pathlib import Path
from rdflib import Namespace, RDF

from storage.graph_store import GraphStore
from introspection.doc_parser import DocParser

DB  = Namespace("https://ontologist.ai/ns/databook#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


@pytest.fixture
def parser(tmp_path):
    store = GraphStore()
    p = DocParser(store, str(tmp_path))
    return p, store, tmp_path


def write_doc(tmp_path, filename, content):
    f = tmp_path / filename
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")
    return f


def get_val(store, subj_uri, pred):
    from rdflib import URIRef
    v = store._g.value(URIRef(subj_uri), pred)
    return str(v) if v is not None else None


def get_subjects(store):
    """Return all db:Databook URIs."""
    return [str(s) for s in store._g.subjects(RDF.type, DB.Databook)]


# ── Frontmatter parsing ────────────────────────────────────────────────────

FULL_FM = textwrap.dedent("""\
    ---
    databook:
      id: test-arch
      title: Test Architecture
      version: "1.0"
      type: plain-doc
      created: "2026-04-01"
      scope: permanent
      layer: architecture
      hierarchy: 0
      task_types:
        - planning
        - implementation
      depends_on:
        - CONVENTIONS
    ---

    # Test Architecture

    Content here.
""")


class TestFrontmatterFields:
    def test_scope_parsed(self, parser):
        p, store, tmp = parser
        f = write_doc(tmp, "arch.md", FULL_FM)
        p.parse_file(str(f))
        uris = get_subjects(store)
        assert uris
        assert get_val(store, uris[0], DB.scope) == "permanent"

    def test_layer_parsed(self, parser):
        p, store, tmp = parser
        f = write_doc(tmp, "arch.md", FULL_FM)
        p.parse_file(str(f))
        uris = get_subjects(store)
        assert get_val(store, uris[0], DB.layer) == "architecture"

    def test_hierarchy_parsed_as_integer(self, parser):
        p, store, tmp = parser
        f = write_doc(tmp, "arch.md", FULL_FM)
        p.parse_file(str(f))
        uris = get_subjects(store)
        val = store._g.value(
            next(store._g.subjects(RDF.type, DB.Databook)), DB.hierarchy
        )
        assert val is not None
        assert int(val) == 0

    def test_task_types_stored_as_comma_string(self, parser):
        p, store, tmp = parser
        f = write_doc(tmp, "arch.md", FULL_FM)
        p.parse_file(str(f))
        uris = get_subjects(store)
        tt = get_val(store, uris[0], DB.taskType)
        assert tt is not None
        assert "planning" in tt
        assert "implementation" in tt

    def test_depends_on_stored_as_uri(self, parser):
        p, store, tmp = parser
        f = write_doc(tmp, "arch.md", FULL_FM)
        p.parse_file(str(f))
        from rdflib import URIRef
        db_uri = next(store._g.subjects(RDF.type, DB.Databook))
        deps = list(store._g.objects(db_uri, DB.dependsOn))
        assert len(deps) == 1
        assert isinstance(deps[0], URIRef)
        assert "conventions" in str(deps[0]).lower()

    def test_transformer_inferred_from_scope_permanent(self, parser):
        """permanent scope without explicit transformer → human."""
        p, store, tmp = parser
        content = textwrap.dedent("""\
            ---
            databook:
              id: no-transformer
              title: No Transformer
              version: "1.0"
              type: plain-doc
              created: "2026-04-01"
              scope: permanent
              layer: architecture
              hierarchy: 1
            ---
            # No Transformer
        """)
        f = write_doc(tmp, "no_transformer.md", content)
        p.parse_file(str(f))
        uris = get_subjects(store)
        assert get_val(store, uris[0], DB.transformer) == "human"

    def test_transformer_inferred_from_scope_task(self, parser):
        """task scope without explicit transformer → llm."""
        p, store, tmp = parser
        content = textwrap.dedent("""\
            ---
            databook:
              id: task-doc
              title: Task Doc
              version: "1.0"
              type: plain-doc
              created: "2026-04-01"
              scope: task
              layer: spec
              hierarchy: 1
              task_types: [testing]
            ---
            # Task Doc
        """)
        f = write_doc(tmp, "task_doc.md", content)
        p.parse_file(str(f))
        uris = get_subjects(store)
        assert get_val(store, uris[0], DB.transformer) == "llm"

    def test_transformer_inferred_from_scope_ephemeral(self, parser):
        """ephemeral scope without explicit transformer → sparql."""
        p, store, tmp = parser
        content = textwrap.dedent("""\
            ---
            databook:
              id: todo-doc
              title: Todo
              version: "1.0"
              type: plain-doc
              created: "2026-04-01"
              scope: ephemeral
              layer: implementation
              hierarchy: 3
            ---
            # Todo
        """)
        f = write_doc(tmp, "todo.md", content)
        p.parse_file(str(f))
        uris = get_subjects(store)
        assert get_val(store, uris[0], DB.transformer) == "sparql"

    def test_explicit_transformer_not_overridden(self, parser):
        """Explicit transformer in frontmatter is preserved."""
        p, store, tmp = parser
        content = textwrap.dedent("""\
            ---
            databook:
              id: explicit-xslt
              title: XSLT Doc
              version: "1.0"
              type: plain-doc
              created: "2026-04-01"
              scope: permanent
              layer: reference
              hierarchy: 1
              process:
                transformer: xslt
            ---
            # XSLT Doc
        """)
        f = write_doc(tmp, "xslt_doc.md", content)
        p.parse_file(str(f))
        uris = get_subjects(store)
        assert get_val(store, uris[0], DB.transformer) == "xslt"


# ── Plain-doc (no frontmatter) defaults ───────────────────────────────────

class TestPlainDocDefaults:
    def test_plain_doc_gets_scope_project(self, parser):
        p, store, tmp = parser
        f = write_doc(tmp, "plain.md", "# Plain\n\nNo frontmatter here.")
        p.parse_file(str(f))
        uris = get_subjects(store)
        assert get_val(store, uris[0], DB.scope) == "project"

    def test_plain_doc_gets_layer_meta(self, parser):
        p, store, tmp = parser
        f = write_doc(tmp, "plain.md", "# Plain\n\nNo frontmatter.")
        p.parse_file(str(f))
        uris = get_subjects(store)
        assert get_val(store, uris[0], DB.layer) == "meta"

    def test_plain_doc_gets_hierarchy_3(self, parser):
        p, store, tmp = parser
        f = write_doc(tmp, "plain.md", "# Plain\n\nNo frontmatter.")
        p.parse_file(str(f))
        uris = get_subjects(store)
        val = store._g.value(
            next(store._g.subjects(RDF.type, DB.Databook)), DB.hierarchy
        )
        assert int(val) == 3

    def test_plain_doc_gets_transformer_human(self, parser):
        p, store, tmp = parser
        f = write_doc(tmp, "plain.md", "# Plain\n\nNo frontmatter.")
        p.parse_file(str(f))
        uris = get_subjects(store)
        assert get_val(store, uris[0], DB.transformer) == "human"

    def test_txt_file_gets_defaults(self, parser):
        p, store, tmp = parser
        f = write_doc(tmp, "requirements.txt", "rdflib>=6.0\npyshacl>=0.20")
        p.parse_file(str(f))
        uris = get_subjects(store)
        assert uris
        assert get_val(store, uris[0], DB.scope) == "project"
