"""Unit tests for needs_decomposition signal in ContextPruner and ContextBuilder."""
import pytest
from copy import deepcopy
from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri, graph_uri
from context.context_builder import ContextPacket, TripleRecord, ContextBuilder
from context.context_pruner import ContextPruner

DB = Namespace("https://ontologist.ai/ns/databook#")
OE = Namespace("https://ontologist.ai/ns/oe/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


def make_packet(token_estimate=100, triple_count=10,
                task_request=None, decomposition_hint="") -> ContextPacket:
    p = ContextPacket(
        packet_id="test-001",
        anchor_uri="https://ontologist.ai/ns/oe/module/test",
        anchor_type="CodeModule",
        task_request=task_request,
        decomposition_hint=decomposition_hint,
    )
    # Add synthetic records to reach the desired token estimate
    chars_needed = int(token_estimate * 4 / 1.2)
    filler = "x" * (chars_needed // triple_count)
    for i in range(triple_count):
        p.records.append(TripleRecord(
            s=f"https://example.com/s{i}",
            p="https://example.com/p",
            o=filler,
            depth=1,
            is_metadata=False,
            is_databook=False,
        ))
    p.token_estimate = token_estimate
    return p


class TestContextPacketDecompositionFields:
    def test_default_needs_decomposition_false(self):
        p = make_packet()
        assert p.needs_decomposition is False

    def test_default_decomposition_hint_empty(self):
        p = make_packet()
        assert p.decomposition_hint == ""

    def test_to_json_includes_decomposition_fields(self):
        p = make_packet()
        p.needs_decomposition = True
        p.decomposition_hint = "Too large"
        j = p.to_json()
        assert j["needs_decomposition"] is True
        assert j["decomposition_hint"] == "Too large"

    def test_to_json_false_when_not_set(self):
        p = make_packet()
        j = p.to_json()
        assert j["needs_decomposition"] is False


class TestContextPrunerDecomposition:
    def test_no_decomposition_when_within_budget(self):
        p = make_packet(token_estimate=500)
        pruner = ContextPruner(max_tokens=1000)
        result = pruner.prune(p)
        assert result.needs_decomposition is False

    def _over_budget_packet(self) -> ContextPacket:
        """Packet with many depth-0, non-metadata, non-content records.

        These survive metadata pruning, dedup, and depth pruning (max_d=0 stops
        the depth loop), and truncate_content has nothing to truncate (no
        db:content predicates).  So the packet remains over budget after all
        passes and _signal_decomposition must fire.
        """
        p = ContextPacket(
            packet_id="test-002",
            anchor_uri="https://ontologist.ai/ns/oe/module/test",
            anchor_type="CodeModule",
        )
        # 200 distinct (s,p) pairs at depth 0 — each 50 chars; total ~10k chars
        filler = "A" * 50
        for i in range(200):
            p.records.append(TripleRecord(
                s=f"https://example.com/entity{i}",
                p="https://example.com/name",   # NOT in _METADATA, NOT db:content
                o=filler,
                depth=0,
                is_metadata=False,
                is_databook=False,
            ))
        p.token_estimate = 10000  # deliberately high; pruner will recalculate
        return p

    def test_decomposition_signaled_when_over_budget(self):
        """When all pruning passes exhausted, needs_decomposition=True."""
        p = self._over_budget_packet()
        pruner = ContextPruner(max_tokens=10)   # tiny budget
        result = pruner.prune(p)
        assert result.needs_decomposition is True

    def test_decomposition_hint_contains_budget_info(self):
        p = self._over_budget_packet()
        pruner = ContextPruner(max_tokens=10)
        result = pruner.prune(p)
        assert result.needs_decomposition is True
        hint = result.decomposition_hint.lower()
        assert "budget" in hint or "token" in hint or "exceed" in hint

    def test_existing_hint_preserved_in_decomposition(self):
        """Chunking hint from ContextBuilder is appended to decomposition hint."""
        p = make_packet(token_estimate=5000)
        p.decomposition_hint = "Databook content was chunked"
        pruner = ContextPruner(max_tokens=50)
        result = pruner.prune(p)
        if result.needs_decomposition:
            assert "chunked" in result.decomposition_hint


class TestContextBuilderTaskContext:
    def test_task_request_stored_in_packet(self):
        store = GraphStore()
        # Add a minimal anchor
        mod_uri = uri("module", "test.py")
        g = graph_uri(mod_uri, "interior")
        store.add(mod_uri, RDF.type, OE.CodeModule, g)

        builder = ContextBuilder(store, max_depth=0, max_tokens=1000)
        packet = builder.build(str(mod_uri), task_request="add BFS traversal", task_type="implementation")
        assert packet.task_request == "add BFS traversal"
        assert packet.task_type == "implementation"

    def test_no_task_request_defaults_to_none(self):
        store = GraphStore()
        mod_uri = uri("module", "test2.py")
        g = graph_uri(mod_uri, "interior")
        store.add(mod_uri, RDF.type, OE.CodeModule, g)

        builder = ContextBuilder(store, max_depth=0, max_tokens=1000)
        packet = builder.build(str(mod_uri))
        assert packet.task_request is None
        assert packet.task_type is None
