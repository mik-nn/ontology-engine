databook:
  id: event_schema
  title: "Event Log Schema"
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
    - events
    - logging
    - rdf
    - prov-o
    - event-first
---
# Event Log Schema

Aligned with ground truth: event-first ontology + RDF 1.2 reification + PROV-O.
See: https://ontologist.substack.com/p/when-predicates-lie-shacl-reification

## Design Principle: Event-First

Pipeline actions are **first-class events**, not bare predicates. A predicate like `oe:hasExecuted` is a materialised view — the event node is the authoritative record.

Four-question test before adding a predicate:
- Provenance? Temporality? Conditionality? Agency? → If yes to any → model as `oe:Event`.

## Namespaces

```turtle
@prefix oe:   <https://ontologist.ai/ns/oe/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
```

## Base Event Pattern (RDF 1.2 with reification)

```turtle
# Event node (interior graph of the PipelineHolon)
GRAPH <urn:oe:pipeline:interior> {
    :event_<uuid> a oe:PlanExecuted ;
        oe:hasAgent   "PlanningAgent" ;
        oe:hasTask    :task_<uri> ;
        oe:hasStatus  "success" ;
        prov:startedAtTime "2026-04-18T12:00:00Z"^^xsd:dateTime ;
        prov:endedAtTime   "2026-04-18T12:00:05Z"^^xsd:dateTime ;
        prov:wasAssociatedWith :agent_PlanningAgent .

    # RDF 1.2 annotation — confidence on the result link
    :event_<uuid> oe:hasResult :result_<uri>
        ~ :ann_<uuid> {|
            oe:confidence "0.97"^^xsd:decimal ;
            prov:wasAttributedTo :agent_PlanningAgent
        |} .
}
```

## PROV-O Agent Types

```turtle
oe:HumanAgent    a prov:Agent, prov:Person .
oe:SystemAgent   a prov:Agent, prov:SoftwareAgent .
oe:LLMAgent      a prov:Agent, prov:SoftwareAgent .
```

Agents are declared in `core/ontology/core.ttl` and referenced via `prov:wasAssociatedWith`.

## Event Types

| Type | Emitted By | Key Properties |
|---|---|---|
| `oe:ProjectScanned` | IntrospectionAgent | `oe:rootPath`, `oe:moduleCount` |
| `oe:ModuleDetected` | IntrospectionAgent | `oe:moduleUri`, `oe:moduleType` |
| `oe:ExternalKnowledgeAdded` | EnrichmentAgent | `oe:sourceUrl`, `oe:entityCount` |
| `oe:UserAnswerReceived` | InterviewAgent | `oe:question`, `oe:entityCreated` |
| `oe:OntologyValidated` | ValidationAgent | `oe:shapesUsed`, `oe:violationCount` |
| `oe:ContextBuilt` | ContextAgent | `oe:taskUri`, `oe:tripleCount`, `oe:tokenEstimate` |
| `oe:TaskDecomposed` | PlanningAgent | `oe:taskUri`, `oe:subtaskCount` |
| `oe:PlanGenerated` | PlanningAgent | `oe:planUri`, `oe:stepCount` |
| `oe:PlanExecuted` | PlanningAgent | `oe:planUri`, `oe:duration` |
| `oe:GitCommitPushed` | GitAgent | `oe:commitHash`, `oe:filesChanged` |
| `oe:DocumentationSynced` | DocSyncAgent | `oe:databookUri`, `oe:path` |
| `oe:DatabookUpdated` | DocSyncAgent / IntrospectionAgent | `oe:databookUri`, `oe:version` |

## Log File Convention

All events are written to the **interior graph** of the active `oe:PipelineHolon`.
Serialised daily to `logs/events/YYYY-MM-DD.trig` (TriG format, named graphs).

| Path | Content |
|---|---|
| `logs/events/YYYY-MM-DD.trig` | Daily event log — TriG with named graphs |
| `logs/runs/<run-id>.json` | Pipeline run summary (JSON) |
| `logs/audit/<run-id>-shacl.txt` | SHACL validation report |
| `logs/graphs/<run-id>.dot` | Graphviz DOT export |
| `logs/graphs/<run-id>.json` | JSON for web viewer |

## SHACL Validation of Events

Events are validated by `oe:EventShape` in `core/shacl/holon_shapes.ttl` immediately after logging.
`oe:hasAgent` and `oe:hasStatus` are required; a missing status blocks the pipeline.
