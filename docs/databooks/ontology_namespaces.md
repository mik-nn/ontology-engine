---
created: '2026-04-18'
id: ontology_namespaces
process:
  transformer: human
synced_at: '2026-04-20T12:50:29.232885+00:00'
title: Ontology Namespace Reference
type: reference
version: 1.1.0
---

databook:
  id: ontology_namespaces
  title: "Ontology Namespace Reference"
  version: 1.1.0
  type: reference
  domain: ontology-engine
  status: active
  created: 2026-04-18
  updated: 2026-04-18
  author:
    - name: Michael
      iri: https://ontologist.ai/agents/michael
  process:
    transformer: human
    inputs: []
  license: CC-BY-4.0
  tags:
    - ontology
    - namespaces
    - rdf
---
# Ontology Namespace Reference

Ground truth: https://ontologist.ai/ns/ (The Ontologist — see archive)

## Active Namespaces

| Prefix | URI | Source | Description |
|---|---|---|---|
| `cga:` | `https://ontologist.ai/ns/cga/` | ground truth | Contextual Graph Architecture — Holon four-graph model |
| `build:` | `https://ontologist.ai/ns/build#` | ground truth | Build pipeline vocabulary — Stage, Target, Source, PythonPackage |
| `db:` | `https://ontologist.ai/ns/databook#` | ground truth | Databook nodes — canonical semantic document format |
| `oe:` | `https://ontologist.ai/ns/oe/` | project | Ontology Engine — project-specific classes and properties |
| `prov:` | `http://www.w3.org/ns/prov#` | W3C | PROV-O — provenance vocabulary |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | W3C | SKOS — concept schemes and taxonomies |
| `sh:` | `http://www.w3.org/ns/shacl#` | W3C | SHACL — constraint language |
| `owl:` | `http://www.w3.org/2002/07/owl#` | W3C | OWL 2 — ontology language |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | W3C | XSD datatypes |

## Core Classes (current)

### Holon Architecture (`cga:`)
- `cga:Holon` — base class; four graphs: interior, boundary, projection, context
- `cga:hasInteriorGraph`, `cga:hasBoundaryGraph`, `cga:hasProjectionGraph`, `cga:hasContextGraph`
- `cga:partOf`, `cga:memberOf`, `cga:holonDepth`

### Ontology Engine (`oe:`)
| Class | Stage | Description |
|---|---|---|
| `oe:ProjectHolon` | 1 | Top-level project container |
| `oe:ModuleHolon`, `oe:CodeModule`, `oe:DataModule`, `oe:ServiceModule`, `oe:ConfigModule` | 2 | Code struc
