"""Stage 9 — GraphExporter.

Exports the RDF graph to two read-only formats:
  - DOT  (Graphviz)
  - JSON (nodes + edges for web viewer)

Entity types are colour-coded. Only meaningful semantic edges are
exported — raw SHACL / provenance triples are excluded.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from rdflib import Namespace, URIRef, Literal

from storage.graph_store import GraphStore

OE    = Namespace("https://ontologist.ai/ns/oe/")
CGA   = Namespace("https://ontologist.ai/ns/cga/")
BUILD = Namespace("https://ontologist.ai/ns/build#")
DB    = Namespace("https://ontologist.ai/ns/databook#")
PROV  = Namespace("http://www.w3.org/ns/prov#")
RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

# ── Node types → display config ──────────────────────────────
_TYPE_CONFIG: dict[str, dict] = {
    "CodeModule":      {"color": "#4e9af1", "shape": "box",     "group": "module"},
    "DataModule":      {"color": "#7ec8e3", "shape": "box",     "group": "module"},
    "ConfigModule":    {"color": "#a8d8ea", "shape": "box",     "group": "module"},
    "ServiceModule":   {"color": "#6cb4ee", "shape": "box",     "group": "module"},
    "CodeFunction":    {"color": "#b8d4f8", "shape": "ellipse", "group": "code"},
    "CodeClass":       {"color": "#c8ddf8", "shape": "ellipse", "group": "code"},
    "Plan":            {"color": "#f4a261", "shape": "diamond", "group": "planning"},
    "Subtask":         {"color": "#f9c784", "shape": "diamond", "group": "planning"},
    "Databook":        {"color": "#2a9d8f", "shape": "database","group": "data"},
    "ProjectHolon":    {"color": "#e76f51", "shape": "star",    "group": "project"},
    "PythonPackage":   {"color": "#8ecae6", "shape": "box",     "group": "deps"},
    "Event":           {"color": "#ccc",    "shape": "dot",     "group": "events"},
}

# Fallback for unknown types
_DEFAULT_CONFIG = {"color": "#d0d0d0", "shape": "dot", "group": "other"}

# ── Edge predicates to export ────────────────────────────────
_EDGE_PREDICATES: dict[str, str] = {
    str(OE.dependsOn):          "dependsOn",
    str(OE.definedIn):          "definedIn",
    str(CGA.partOf):            "partOf",
    str(CGA.memberOf):          "memberOf",
    str(BUILD.dependsOn):       "dependsOn",
    str(BUILD.requiredBy):      "requiredBy",
    str(OE.hasTask):            "hasTask",
    str(OE.hasResult):          "hasResult",
    str(OE.concernsEntity):     "concerns",
    str(PROV.wasGeneratedBy):   "generatedBy",
}

# ── Event subclasses that ARE shown (others filtered out) ───
_SHOWN_EVENT_TYPES = {
    "ProjectScanned", "PlanGenerated", "PlanExecuted",
    "OntologyValidated", "ContextBuilt", "DocumentationSynced",
    "GitCommitPushed", "DatabookUpdated",
}


@dataclass
class ExportNode:
    id: str
    label: str
    type_name: str
    color: str
    shape: str
    group: str
    title: str = ""           # tooltip


@dataclass
class ExportEdge:
    source: str
    target: str
    label: str


@dataclass
class ExportGraph:
    nodes: list[ExportNode] = field(default_factory=list)
    edges: list[ExportEdge] = field(default_factory=list)

    def to_json(self) -> dict:
        return {
            "nodes": [
                {
                    "id":    n.id,
                    "label": n.label,
                    "type":  n.type_name,
                    "color": n.color,
                    "shape": n.shape,
                    "group": n.group,
                    "title": n.title,
                }
                for n in self.nodes
            ],
            "edges": [
                {"from": e.source, "to": e.target, "label": e.label}
                for e in self.edges
            ],
            "groups": sorted({n.group for n in self.nodes}),
        }

    def to_dot(self) -> str:
        lines = ["digraph OntologyEngine {",
                 '  graph [rankdir=LR fontname="Helvetica" bgcolor="#1e1e1e"];',
                 '  node  [fontname="Helvetica" fontsize=10 style=filled fontcolor=white];',
                 '  edge  [fontname="Helvetica" fontsize=9 color="#888888"];',
                 ""]
        for n in self.nodes:
            esc = n.label.replace('"', '\\"')
            lines.append(
                f'  "{n.id}" [label="{esc}" fillcolor="{n.color}" '
                f'shape={n.shape}];'
            )
        lines.append("")
        for e in self.edges:
            lines.append(
                f'  "{e.source}" -> "{e.target}" [label="{e.label}"];'
            )
        lines.append("}")
        return "\n".join(lines)


class GraphExporter:
    """Converts a GraphStore snapshot to DOT and JSON export formats."""

    def __init__(self, store: GraphStore, include_events: bool = False):
        self.store = store
        self.include_events = include_events
        self._g = store._g

    def export(self) -> ExportGraph:
        eg = ExportGraph()
        node_ids: set[str] = set()

        # ── Collect typed nodes ──────────────────────────────
        for s, _, o in self._g.triples((None, RDF_TYPE, None)):
            if not isinstance(s, URIRef):
                continue
            type_name = _local(str(o))
            cfg = _TYPE_CONFIG.get(type_name)

            # Filter events unless explicitly requested
            if cfg is None:
                # Check if it's an event subclass we want to show
                if not self.include_events:
                    continue
                if type_name not in _SHOWN_EVENT_TYPES:
                    continue
                cfg = _TYPE_CONFIG.get("Event", _DEFAULT_CONFIG)

            uid = str(s)
            if uid in node_ids:
                continue
            node_ids.add(uid)

            label = self._label(s, type_name)
            tooltip = self._tooltip(s, type_name)

            eg.nodes.append(ExportNode(
                id=uid,
                label=label,
                type_name=type_name,
                color=cfg["color"],
                shape=cfg["shape"],
                group=cfg["group"],
                title=tooltip,
            ))

        # ── Collect edges ────────────────────────────────────
        for pred_uri, pred_label in _EDGE_PREDICATES.items():
            pred = URIRef(pred_uri)
            for s, _, o in self._g.triples((None, pred, None)):
                if not isinstance(s, URIRef) or not isinstance(o, URIRef):
                    continue
                if str(s) in node_ids and str(o) in node_ids:
                    eg.edges.append(ExportEdge(
                        source=str(s),
                        target=str(o),
                        label=pred_label,
                    ))

        return eg

    # ──────────────────────────────────────────────
    # Label / tooltip helpers
    # ──────────────────────────────────────────────

    def _label(self, uri: URIRef, type_name: str) -> str:
        # Try known display properties first
        for prop in (OE.taskName, OE.functionName, OE.className,
                     DB.title, BUILD.name):
            v = self._g.value(uri, prop)
            if v:
                return str(v)[:40]
        # Fall back to URI local name
        return _local(str(uri))[:40]

    def _tooltip(self, uri: URIRef, type_name: str) -> str:
        parts = [f"<b>{type_name}</b>", str(uri)]
        for prop, label in [
            (OE.hasStatus,    "status"),
            (OE.description,  "desc"),
            (DB.version,      "version"),
            (OE.hasExecutor,  "executor"),
        ]:
            v = self._g.value(uri, prop)
            if v:
                parts.append(f"{label}: {str(v)[:60]}")
        return "<br>".join(parts)


# ──────────────────────────────────────────────────────────
# Convenience save functions
# ──────────────────────────────────────────────────────────

def export_json(store: GraphStore, out_path: str,
                include_events: bool = False) -> ExportGraph:
    eg = GraphExporter(store, include_events=include_events).export()
    Path(out_path).write_text(
        json.dumps(eg.to_json(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return eg


def export_dot(store: GraphStore, out_path: str,
               include_events: bool = False) -> ExportGraph:
    eg = GraphExporter(store, include_events=include_events).export()
    Path(out_path).write_text(eg.to_dot(), encoding="utf-8")
    return eg


def _local(uri: str) -> str:
    """Extract local name from URI."""
    for sep in ("#", "/"):
        if sep in uri:
            return uri.rsplit(sep, 1)[-1]
    return uri
