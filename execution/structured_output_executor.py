"""Structured output executor — generative tasks via SHACL-shaped LLM output.

Implements the "SHACL as MadLibs" pattern from Kurt Cagle:
  1. Extract output schema from SHACL shapes (SPARQL over shapes graph)
  2. Embed JSON Schema in prompt as explicit output contract
  3. Call LLM — output must conform to the schema
  4. Parse JSON response
  5. Validate output against SHACL (for graph-typed outputs)
  6. Commit to graph or write to disk

Why this matters: the LLM fills in blanks defined by the ontology.
Invalid output is rejected before it touches the graph.

Cagle: "SHACL constraints as prior beliefs rather than rigid gates —
validation is not gatekeeping, it is the computation of prediction error."
"""
from __future__ import annotations

import json
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD

OE = Namespace("https://ontologist.ai/ns/oe/")
DB = Namespace("https://ontologist.ai/ns/databook#")
SH = Namespace("http://www.w3.org/ns/shacl#")

# ─────────────────────────────────────────────────────────────────────────────
# Built-in output schemas for task types without a dedicated SHACL shape
# These are JSON-Schema objects that define the tool call input.
# ─────────────────────────────────────────────────────────────────────────────

_BUILTIN_SCHEMAS: dict[str, dict] = {
    "AnalysisReport": {
        "type": "object",
        "description": "Structured analysis report derived from the graph.",
        "properties": {
            "summary":          {"type": "string", "description": "1–3 sentence overview."},
            "findings":         {"type": "array", "items": {"type": "string"},
                                 "description": "Specific observations, one per item."},
            "recommendations":  {"type": "array", "items": {"type": "string"},
                                 "description": "Actionable next steps."},
            "severity":         {"type": "string", "enum": ["info", "warning", "error"],
                                 "description": "Overall severity level."},
        },
        "required": ["summary", "findings", "severity"],
    },
    "Explanation": {
        "type": "object",
        "description": "Structured explanation of a concept or decision.",
        "properties": {
            "explanation":  {"type": "string", "description": "Full explanation text."},
            "key_concepts": {"type": "array", "items": {"type": "string"},
                             "description": "Key terms defined or referenced."},
            "examples":     {"type": "array", "items": {"type": "string"},
                             "description": "Concrete examples (optional)."},
        },
        "required": ["explanation"],
    },
    "DesignProposal": {
        "type": "object",
        "description": "Structured design or architectural proposal.",
        "properties": {
            "title":        {"type": "string"},
            "rationale":    {"type": "string", "description": "Why this design."},
            "components":   {"type": "array", "items": {"type": "string"},
                             "description": "Named components or modules."},
            "interfaces":   {"type": "array", "items": {"type": "string"},
                             "description": "Key interfaces or boundaries."},
            "trade_offs":   {"type": "array", "items": {"type": "string"}},
            "open_questions": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["title", "rationale", "components"],
    },
}

# Maps task_type → (schema_name, rdf_class_uri | None)
# rdf_class_uri is set when the output should be committed as RDF triples.
_TASK_SCHEMA_MAP: dict[str, tuple[str, Optional[str]]] = {
    "DocumentTask":  ("DatabookShape",   str(DB.Databook)),
    "AnalysisTask":  ("AnalysisReport",  None),
    "ExplainTask":   ("Explanation",     None),
    "DesignTask":    ("DesignProposal",  None),
    "ReviewTask":    ("AnalysisReport",  None),
    "DebugTask":     ("AnalysisReport",  None),
}


@dataclass
class StructuredResult:
    """Result from a structured-output LLM call."""
    subtask_name: str
    schema_used: str
    output_data: dict          # parsed JSON from LLM
    conforms: bool = True      # SHACL validation result (for graph outputs)
    violations: list[str] = field(default_factory=list)
    file_written: Optional[str] = None


class StructuredOutputExecutor:
    """Generative executor: SHACL shapes → JSON Schema → LLM → validate → commit."""

    def __init__(self, store, shapes_dir: Optional[Path] = None):
        self._store = store
        self._shapes_dir = shapes_dir or _find_shapes_dir()
        self._shapes_graph: Optional[Graph] = None

    # ─────────────────────────────────────────────────────────────────────────
    # Public entry point
    # ─────────────────────────────────────────────────────────────────────────

    def run(
        self,
        node,
        context,
        spec,
        llm_config: dict,
    ) -> StructuredResult:
        """Execute a generative subtask with structured LLM output.

        Steps:
          1. Resolve the output schema for this task type
          2. Build a prompt embedding the schema as the output contract
          3. Call the LLM; parse JSON response
          4. Validate against SHACL (if graph output)
          5. Write to disk / graph where applicable
          6. Return StructuredResult
        """
        schema_name, rdf_class = _TASK_SCHEMA_MAP.get(
            spec.original_type, ("AnalysisReport", None)
        )

        # Resolve JSON Schema: from SHACL graph or built-in
        if schema_name == "DatabookShape":
            json_schema = self._databook_schema_from_shacl()
        else:
            json_schema = _BUILTIN_SCHEMAS[schema_name]

        prompt = self._build_prompt(node, context, spec, json_schema)
        raw    = self._call_llm(prompt, json_schema, llm_config)
        data   = self._parse_json(raw)

        # SHACL validation for graph-typed outputs
        conforms, violations = True, []
        if rdf_class and data:
            conforms, violations = self._validate_against_shacl(
                data, rdf_class, schema_name
            )

        # Write file for documentation tasks
        file_written = None
        if spec.original_type == "DocumentTask" and data and conforms:
            file_written = self._write_databook(data, spec)

        return StructuredResult(
            subtask_name=node.name,
            schema_used=schema_name,
            output_data=data or {},
            conforms=conforms,
            violations=violations,
            file_written=file_written,
        )

    def format_output(self, result: StructuredResult) -> str:
        """Format StructuredResult as a string for PlanExecutor."""
        lines = [f"Structured output ({result.schema_used})"]
        if result.output_data.get("summary"):
            lines.append(f"  Summary: {result.output_data['summary'][:120]}")
        elif result.output_data.get("explanation"):
            lines.append(f"  {result.output_data['explanation'][:120]}")
        elif result.output_data.get("title"):
            lines.append(f"  Title: {result.output_data['title']}")
        if not result.conforms:
            lines.append(f"  ⚠  {len(result.violations)} SHACL violation(s):")
            lines.extend(f"    {v}" for v in result.violations[:3])
        if result.file_written:
            lines.append(f"  Written → {result.file_written}")
        return "\n".join(lines)

    # ─────────────────────────────────────────────────────────────────────────
    # Schema extraction
    # ─────────────────────────────────────────────────────────────────────────

    def _databook_schema_from_shacl(self) -> dict:
        """Build JSON Schema from db:DatabookShape via SPARQL over shapes graph."""
        g = self._get_shapes_graph()

        sparql = """
            PREFIX sh:  <http://www.w3.org/ns/shacl#>
            PREFIX db:  <https://ontologist.ai/ns/databook#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?path ?datatype ?minCount ?inList ?pattern WHERE {
                db:DatabookShape sh:property ?ps .
                ?ps sh:path ?path .
                OPTIONAL { ?ps sh:datatype  ?datatype  }
                OPTIONAL { ?ps sh:minCount  ?minCount  }
                OPTIONAL { ?ps sh:pattern   ?pattern   }
                OPTIONAL { ?ps sh:in        ?inList    }
            }
        """
        rows = list(g.query(sparql))

        properties: dict[str, Any] = {}
        required:   list[str]      = []

        for r in rows:
            prop_name = str(r.path).split("/")[-1].split("#")[-1]
            dtype     = str(r.datatype) if r.datatype else ""
            schema_type = _xsd_to_json_type(dtype)
            prop_entry: dict[str, Any] = {"type": schema_type}

            if r.pattern:
                prop_entry["pattern"] = str(r.pattern)

            # sh:in → enum
            if r.inList:
                enum_vals = _collect_rdf_list(g, URIRef(str(r.inList)))
                if enum_vals:
                    prop_entry["enum"] = enum_vals

            properties[prop_name] = prop_entry
            if r.minCount and int(str(r.minCount)) > 0:
                required.append(prop_name)

        if not properties:
            # Fall back to a minimal hard-coded schema
            return _BUILTIN_SCHEMAS.get("DatabookShape", {
                "type": "object",
                "properties": {
                    "id":          {"type": "string"},
                    "title":       {"type": "string"},
                    "version":     {"type": "string"},
                    "type":        {"type": "string"},
                    "created":     {"type": "string"},
                    "content":     {"type": "string"},
                    "transformer": {"type": "string",
                                    "enum": ["human", "llm", "sparql", "xslt"]},
                    "scope":       {"type": "string",
                                    "enum": ["permanent", "project", "task", "ephemeral"]},
                    "layer":       {"type": "string",
                                    "enum": ["architecture", "reference",
                                             "implementation", "meta", "spec"]},
                },
                "required": ["id", "title", "version", "type", "created", "content"],
            })

        return {"type": "object", "properties": properties, "required": required}

    # ─────────────────────────────────────────────────────────────────────────
    # Prompt construction
    # ─────────────────────────────────────────────────────────────────────────

    def _build_prompt(self, node, context, spec, json_schema: dict) -> str:
        schema_str = json.dumps(json_schema, indent=2)

        ctx_summary = _summarise_context(context)

        return textwrap.dedent(f"""
            Task: {spec.original_request}
            Subtask: {node.description}

            ## Project Context
            {ctx_summary}

            ## Output Contract
            You MUST respond with ONLY a valid JSON object that conforms to
            this schema — no markdown fences, no explanation, no extra keys:

            {schema_str}

            Respond now with the JSON object:
        """).strip()

    # ─────────────────────────────────────────────────────────────────────────
    # LLM call — adapter-agnostic, JSON-in-prompt strategy
    # ─────────────────────────────────────────────────────────────────────────

    def _call_llm(self, prompt: str, schema: dict, llm_config: dict) -> str:
        """Call LLM and return raw string response."""
        from execution.adapters.factory import create_for_role

        _SYSTEM = (
            "You are a structured data generator inside an ontology pipeline. "
            "You output ONLY valid JSON objects that match the schema given in the prompt. "
            "No prose, no markdown, no commentary — pure JSON."
        )

        try:
            from cli.config import find_config, load_config
            full_cfg = load_config(find_config())
        except Exception:
            full_cfg = {"llm": llm_config}

        adapter = create_for_role(full_cfg, llm_config.get("llm_role", "default"))
        result  = adapter.complete(
            system=_SYSTEM,
            user=prompt,
            max_tokens=llm_config.get("max_tokens", 4096),
        )
        return result.output

    # ─────────────────────────────────────────────────────────────────────────
    # JSON parsing — tolerates minor LLM formatting noise
    # ─────────────────────────────────────────────────────────────────────────

    def _parse_json(self, raw: str) -> Optional[dict]:
        """Extract JSON object from LLM response, stripping markdown fences."""
        text = re.sub(r"```(?:json)?\s*", "", raw).strip()
        text = re.sub(r"\s*```$", "", text).strip()
        # Find first {...} block
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    # ─────────────────────────────────────────────────────────────────────────
    # SHACL validation of LLM output
    # ─────────────────────────────────────────────────────────────────────────

    def _validate_against_shacl(
        self, data: dict, rdf_class_uri: str, schema_name: str
    ) -> tuple[bool, list[str]]:
        """Convert output dict → RDF graph, then validate with pyshacl."""
        try:
            import pyshacl
        except ImportError:
            return True, []   # can't validate, assume ok

        data_g   = self._dict_to_rdf(data, rdf_class_uri)
        shapes_g = self._get_shapes_graph()

        conforms, results_graph, _ = pyshacl.validate(
            data_g,
            shacl_graph=shapes_g,
            inference="none",
            abort_on_first=False,
        )

        violations: list[str] = []
        if not conforms:
            sparql = """
                PREFIX sh: <http://www.w3.org/ns/shacl#>
                SELECT ?msg WHERE {
                    ?r a sh:ValidationResult ;
                       sh:resultMessage ?msg .
                    FILTER(NOT EXISTS { ?r sh:resultSeverity sh:Warning })
                } LIMIT 10
            """
            violations = [str(row.msg) for row in results_graph.query(sparql)]

        return conforms, violations

    def _dict_to_rdf(self, data: dict, rdf_class_uri: str) -> Graph:
        """Serialize a flat dict to an RDF graph for SHACL validation."""
        g = Graph()
        subj = URIRef("urn:structured-output:result")
        cls  = URIRef(rdf_class_uri)
        ns   = Namespace(rdf_class_uri.rsplit("#", 1)[0].rsplit("/", 1)[0] + "/")

        g.add((subj, RDF.type, cls))

        for key, val in data.items():
            pred = ns[key]
            if isinstance(val, list):
                for item in val:
                    g.add((subj, pred, Literal(str(item))))
            elif isinstance(val, bool):
                g.add((subj, pred, Literal(val, datatype=XSD.boolean)))
            elif isinstance(val, int):
                g.add((subj, pred, Literal(val, datatype=XSD.integer)))
            elif val is not None:
                g.add((subj, pred, Literal(str(val))))

        return g

    # ─────────────────────────────────────────────────────────────────────────
    # Documentation writer
    # ─────────────────────────────────────────────────────────────────────────

    def _write_databook(self, data: dict, spec) -> Optional[str]:
        """Write a SHACL-validated Databook dict to a Markdown file."""
        import re as _re
        from datetime import date

        title   = data.get("title", "untitled")
        slug    = _re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        content = data.get("content", "")

        # Resolve output directory from spec or fall back to docs/databooks/
        out_dir = Path("docs/databooks")
        out_dir.mkdir(parents=True, exist_ok=True)

        fname = f"{slug}.md"
        fpath = out_dir / fname

        frontmatter = _build_frontmatter(data)
        fpath.write_text(f"{frontmatter}\n\n{content}\n", encoding="utf-8")
        return str(fpath)

    # ─────────────────────────────────────────────────────────────────────────
    # Shapes graph cache
    # ─────────────────────────────────────────────────────────────────────────

    def _get_shapes_graph(self) -> Graph:
        """Lazy-load and cache the merged shapes graph."""
        if self._shapes_graph is None:
            g = Graph()
            if self._shapes_dir and self._shapes_dir.exists():
                for ttl in sorted(self._shapes_dir.glob("*.ttl")):
                    g.parse(str(ttl), format="turtle")
            self._shapes_graph = g
        return self._shapes_graph


# ─────────────────────────────────────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────────────────────────────────────

def _xsd_to_json_type(xsd_uri: str) -> str:
    """Map XSD datatype URI → JSON Schema type string."""
    _MAP = {
        "integer": "integer", "int": "integer", "long": "integer",
        "boolean": "boolean",
        "decimal": "number", "float": "number", "double": "number",
    }
    local = xsd_uri.split("#")[-1].split("/")[-1].lower()
    return _MAP.get(local, "string")


def _collect_rdf_list(g: Graph, head: URIRef) -> list[str]:
    """Walk an rdf:first/rdf:rest list and return string values."""
    RDF_NS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    values = []
    node   = head
    seen   = set()
    while node and node != RDF_NS.nil and node not in seen:
        seen.add(node)
        first = g.value(node, RDF_NS.first)
        if first is not None:
            values.append(str(first))
        node = g.value(node, RDF_NS.rest)
    return values


def _summarise_context(context) -> str:
    """Extract a readable summary from a ContextPacket."""
    lines = []
    if hasattr(context, "task_request") and context.task_request:
        lines.append(f"Request: {context.task_request}")
    if hasattr(context, "entity_summaries"):
        summaries = context.entity_summaries or {}
        if isinstance(summaries, dict):
            items = list(summaries.items())[:5]
            for uri, desc in items:
                name = uri.split("/")[-1]
                lines.append(f"  Entity: {name} — {str(desc)[:80]}")
        else:
            for e in summaries[:5]:
                name = e.get("label") or e.get("uri", "?").split("/")[-1]
                desc = e.get("description", "")[:80]
                lines.append(f"  Entity: {name} — {desc}")
    if hasattr(context, "databook_fragments"):
        for d in (context.databook_fragments or [])[:3]:
            lines.append(f"  Databook: {d.get('title', '?')}")
    return "\n".join(lines) if lines else "(no context)"


def _build_frontmatter(data: dict) -> str:
    """Build YAML-like frontmatter from Databook dict."""
    from datetime import date
    lines = ["---"]
    for key in ("id", "title", "version", "type", "transformer",
                "scope", "layer", "created"):
        if key in data:
            lines.append(f"{key}: {data[key]}")
    if "created" not in data:
        lines.append(f"created: {date.today().isoformat()}")
    lines.append("---")
    return "\n".join(lines)


def _find_shapes_dir() -> Optional[Path]:
    """Walk up from execution/ to find core/shacl/."""
    here = Path(__file__).parent
    for candidate in [here.parent / "core" / "shacl",
                      Path("core/shacl")]:
        if candidate.exists():
            return candidate
    return None
