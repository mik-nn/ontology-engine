"""Unit tests for verification/rule_engine.py"""
import pytest
from rdflib import Namespace, RDF, Literal, URIRef

from storage.graph_store import GraphStore
from storage.id_manager import uri, graph_uri
from verification.rule_engine import RuleEngine, RuleReport, RuleViolation

OE  = Namespace("https://ontologist.ai/ns/oe/")
CGA = Namespace("https://ontologist.ai/ns/cga/")

SHAPES = [
    "core/shacl/databook_shapes.ttl",
    "core/shacl/dependencies_shapes.ttl",
]


@pytest.fixture
def empty_store():
    return GraphStore()


@pytest.fixture
def store_with_module():
    s = GraphStore()
    mod = uri("module", "mymod.py")
    g = graph_uri(mod, "interior")
    s.add(mod, RDF.type, OE.CodeModule, g)
    fn = uri("task", "mymod-py-myfunc")
    s.add(fn, RDF.type, OE.CodeFunction, g)
    s.add(fn, OE.functionName, Literal("myfunc"), g)
    s.add(fn, OE.definedIn, mod, g)
    return s, mod


class TestRuleEngineRun:
    def test_returns_rule_report(self, empty_store):
        engine = RuleEngine(empty_store, shapes_paths=SHAPES)
        result = engine.run()
        assert isinstance(result, RuleReport)

    def test_empty_store_conforms(self, empty_store):
        engine = RuleEngine(empty_store, shapes_paths=SHAPES)
        report = engine.run()
        assert report.conforms is True
        assert report.violations == []

    def test_report_has_violations_list(self, empty_store):
        engine = RuleEngine(empty_store, shapes_paths=SHAPES)
        report = engine.run()
        assert isinstance(report.violations, list)
        assert isinstance(report.warnings, list)
        assert isinstance(report.infos, list)


class TestRuleReportSummary:
    def test_summary_contains_conforms(self):
        r = RuleReport(conforms=True)
        assert "YES" in r.summary()

    def test_summary_violation_count(self):
        v = RuleViolation("P01", "violation", "urn:x", "msg", "python")
        r = RuleReport(conforms=False, violations=[v])
        assert "1" in r.summary()

    def test_all_issues(self):
        v = RuleViolation("P01", "violation", "urn:x", "msg", "python")
        w = RuleViolation("P02", "warning",   "urn:y", "msg", "python")
        r = RuleReport(conforms=False, violations=[v], warnings=[w])
        assert len(r.all_issues) == 2


class TestCycleDetection:
    def test_no_cycle_no_violation(self, empty_store):
        a = uri("module", "a.py")
        b = uri("module", "b.py")
        g = graph_uri(a, "interior")
        empty_store.add(a, OE.dependsOn, b, g)

        engine = RuleEngine(empty_store, shapes_paths=SHAPES)
        report = engine.run()
        p01 = [v for v in report.violations if v.rule_id == "P01"]
        assert p01 == []

    def test_cycle_produces_violation(self, empty_store):
        a = uri("module", "a.py")
        b = uri("module", "b.py")
        ga = graph_uri(a, "interior")
        gb = graph_uri(b, "interior")
        empty_store.add(a, OE.dependsOn, b, ga)
        empty_store.add(b, OE.dependsOn, a, gb)

        engine = RuleEngine(empty_store, shapes_paths=SHAPES)
        report = engine.run()
        p01 = [v for v in report.violations if v.rule_id == "P01"]
        assert len(p01) >= 1
        assert "Cycle" in p01[0].message


class TestModuleFunctionWarning:
    def test_module_without_function_gets_warning(self, empty_store):
        mod = uri("module", "empty_mod.py")
        g = graph_uri(mod, "interior")
        empty_store.add(mod, RDF.type, OE.CodeModule, g)

        engine = RuleEngine(empty_store, shapes_paths=SHAPES)
        report = engine.run()
        p02 = [w for w in report.warnings if w.rule_id == "P02"]
        assert len(p02) == 1

    def test_module_with_function_no_warning(self, store_with_module):
        store, _ = store_with_module
        engine = RuleEngine(store, shapes_paths=SHAPES)
        report = engine.run()
        p02 = [w for w in report.warnings if w.rule_id == "P02"]
        assert p02 == []


class TestHolonInteriorEmpty:
    def test_empty_interior_produces_info(self, empty_store):
        mod = uri("module", "x.py")
        empty_store.declare_holon(mod, OE.CodeModule)
        # Interior is empty — should trigger P03

        engine = RuleEngine(empty_store, shapes_paths=SHAPES)
        report = engine.run()
        p03 = [i for i in report.infos if i.rule_id == "P03"]
        assert len(p03) >= 1
