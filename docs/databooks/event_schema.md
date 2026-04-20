---
created: '2026-04-18'
id: event_schema
process:
  transformer: human
synced_at: '2026-04-20T12:43:44.631307+00:00'
title: Event Log Schema
type: reference
version: 1.1.0
---

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
oe:LLMAgent      a prov:Agent, prov:Soft
