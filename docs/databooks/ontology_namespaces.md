---
databook:
  created: '2026-04-18'
  hierarchy: 0
  id: ontology_namespaces
  layer: reference
  process:
    transformer: human
  scope: permanent
  synced_at: '2026-04-21T14:10:41.547808+00:00'
  title: Ontology Namespace Reference
  type: reference
  version: 1.1.0
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
| `oe:ModuleHolon`, `oe:CodeModule`, `oe:DataModule`, `oe:ServiceModule`, `oe:ConfigModule` | 2 | Code structure |
| `oe:TaskHolon`, `oe:AnalysisTask`, `oe:DesignTask`, `oe:ExplainTask`, `oe:ImplementTask`, `oe:RefactorTask` | 7 | Task types |
| `oe:Plan`, `oe:Subtask` | 7 | Planning |
| `oe:Event` + 12 subclasses | 8 | Pipeline events (event-first model) |

### Build (`build:`)
- `build:PythonPackage`, `build:Stage`, `build:Target`, `build:Source`
- `build:name`, `build:version`, `build:requiredBy`, `build:dependsOn`

### Databook (`db:`)
- `db:Databook` (subClassOf `prov:Entity`)
- Required properties: `id`, `title`, `version`, `type`, `created`, `content`
- Optional: `transformer` (one of: `human`, `llm`, `sparql`, `xslt`), `license`, `authorName`, `authorIRI`, `processInput`

## Canonical DataBook Frontmatter

```yaml
databook:
  id: <string>
  title: <string>
  version: <semver>
  type: <string>
  created: <YYYY-MM-DD>
  author:
    - name: <string>
      iri: <URI>
  process:
    transformer: human | llm | sparql | xslt
    inputs: [<URI>, ...]
  license: <SPDX-identifier>
  tags: [<string>, ...]
```

## Event-First Modeling Rule

Before adding a predicate to the ontology, apply the four-question test (from ground truth):

1. Does the relation carry **provenance** (who asserted it)?
2. Does it carry **temporality** (valid from/until)?
3. Does it carry **conditionality** (contextual constraints)?
4. Does it carry **agency** (something happened to create it)?

If any answer is yes → model an `oe:Event` node, not a bare predicate. The predicate becomes a materialised view derived from the event.











