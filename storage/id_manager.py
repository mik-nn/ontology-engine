import re
from rdflib import URIRef

BASE = "https://ontologist.ai/ns/oe/"

_TYPE_PATHS = {
    "project":  "project/",
    "module":   "module/",
    "task":     "task/",
    "plan":     "plan/",
    "subtask":  "subtask/",
    "event":    "event/",
    "databook": "databook/",
    "agent":    "agent/",
    "pipeline": "pipeline/",
}

def _slug(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")

def uri(entity_type: str, name: str) -> URIRef:
    """Return a stable URI for a given type and name.

    >>> uri("module", "introspection/code_parser.py")
    rdflib.term.URIRef('https://ontologist.ai/ns/oe/module/introspection-code-parser-py')
    """
    prefix = _TYPE_PATHS.get(entity_type, f"{entity_type}/")
    return URIRef(BASE + prefix + _slug(name))

def graph_uri(holon_uri: URIRef, layer: str) -> URIRef:
    """Return the named graph URI for a holon layer.

    layer: 'interior' | 'boundary' | 'projection' | 'context'
    """
    return URIRef(str(holon_uri) + f"/{layer}")
