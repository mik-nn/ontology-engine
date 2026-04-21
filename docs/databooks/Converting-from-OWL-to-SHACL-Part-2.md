---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Converting-from-OWL-to-SHACL-Part-2
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:57.214729+00:00'
  title: Converting from owl to shacl, part 2
  type: plain-doc
  version: '0.1'
---

# Converting from owl to shacl, part 2

[

![](https://substackcdn.com/image/fetch/$s_!h_i6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51ca79c2-f036-42ae-a490-0752fa464939_2688x1536.jpeg)



](https://substackcdn.com/image/fetch/$s_!h_i6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51ca79c2-f036-42ae-a490-0752fa464939_2688x1536.jpeg)

_Jessica Talisman has been publishing a superb series on the development of ontologies:_

[

![](https://substackcdn.com/image/fetch/$s_!6thL!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7ece832-4723-4e82-8898-e149a93fa09b_995x995.png)Intentional Arrangement

Ontology, Part III

The full NTWF ontology is available here on Substack for paying subscribers, and as a PDF, near the conclusion of this essay. I will be publishing the SPARQL testing environment once I have it up and running…

Read more

a month ago · 6 likes · 10 comments · Jessica Talisman

](https://jessicatalisman.substack.com/p/ontology-part-iii?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

_She recently reached out to me about writing an article on converting from OWL to SHACL. As I’ve been leading up to the issue, it seemed like a good opportunity to take up the challenge._

_This is the second in a series on converting OWL to SHACL, where I’ll actually delve into a working example, based upon Jessica’s OWL ontology, to develop a hybrid system that combines both SHACL and OWL._

## A Hybrid Ontology

In part I, I ended my post with the thought that one of the strongest design patterns when dealing with OWL to SHACL conversions is not to replace but to augment, providing both validation and open world dynamics in the same package. This is the approach I’m going to take here.

The NTWF ontology is a process flow ontology, built primarily around a Workflow:

```
#
----------------------------------------------------------------------
-------
# Class: ntwf:Workflow
# CQ: "What are all the steps in a workflow, and in what order?"
# Standards survey: prov:Plan (process semantics), schema:CreativeWork
# (document semantics)
# Gap: Neither standard represents a named organizational workflow
with
# administrative metadata and step structure as a first-class
entity.
#
----------------------------------------------------------------------
-------
ntwf:Workflow
a owl:Class ;
rdfs:subClassOf prov:Plan ;
rdfs:subClassOf schema:CreativeWork ;
rdfs:label "Workflow"@en ;
rdfs:comment
"A named, versioned organizational process at Special
Solutions, consisting of an ordered sequence of steps intended to
produce a defined outcome. Subclasses prov:Plan for process semantics
and schema:CreativeWork for document and discovery semantics.
Administrative metadata (title, description, created, modified,
identifier) is supplied entirely by Dublin Core terms — no custom
metadata properties are required. dct:modified is the property that
makes stale-workflow queries answerable."@en ;
rdfs:isDefinedBy <https://ontology.specialsolutions.example.com/
workflow> .
```

This is a core object in the ontology, in that everything else is built around it. Class definitions in OWL usually flow toward the consolidating objects (a bottom-up bias), so property declarations are usually “attached” through `rdfs:domain` or `owl:restriction` declarations. Because Workflow is a base class, the properties that it inherits are likely to be annotative, so, looking through the ontology we get the following:

```
ntwf:hasStep
    a owl:ObjectProperty ;
    rdfs:domain ntwf:Workflow ;
    rdfs:range ntwf:WorkflowStep ;
    rdfs:label "has step"@en ;
    rdfs:comment
        "Links a Workflow to one of the WorkflowStep individuals it
contains. Inverse of ntwf:isStepOf. Does not encode order — sequence
is expressed by ntwf:sequencePosition (integer) and ntwf:precedesStep
(transitive ordering relation)."@en ;
    owl:inverseOf ntwf:isStepOf ;
    rdfs:isDefinedBy <https://ontology.specialsolutions.example.com/
workflow> .

ntwf:workflowStatus
    a owl:ObjectProperty , owl:FunctionalProperty ;
    rdfs:domain ntwf:Workflow ;
    rdfs:range skos:Concept ;
    rdfs:label "workflow status"@en ;
    rdfs:comment
        "Links a Workflow to exactly one SKOS concept from
ntwf:WorkflowStatusScheme representing its current lifecycle status.
Declared owl:FunctionalProperty — a workflow has one current status.
Bridges the CBox vocabulary into the TBox without promoting status
concepts to OWL classes. The range is skos:Concept; values should be
drawn from ntwf:WorkflowStatusScheme."@en ;
rdfs:isDefinedBy <https://ontology.specialsolutions.example.com/
workflow> .
```

We can also flesh this out with the ntwf:workflowStep definition and properties:

```
ntwf:WorkflowStep
    a owl:Class ;
    rdfs:subClassOf prov:Activity ;
    rdfs:label "Workflow Step"@en ;
    rdfs:comment
        "An atomic, individually addressable unit of work within a
workflow. Subclasses prov:Activity, inheriting prov:startedAtTime,
prov:endedAtTime, prov:wasAssociatedWith, prov:used, and
prov:generated. Each step is assigned exactly one ntwf:Role via
ntwf:assignedRole (functional), has an integer sequence position via
ntwf:sequencePosition (functional), and carries a boolean
ntwf:requiresHumanApproval flag. Steps may produce or consume
ntwf:WorkflowArtifact individuals and dcat:Dataset individuals."@en ;
rdfs:isDefinedBy <https://ontology.specialsolutions.example.com/
workflow> . 

ntwf:isStepOf
    a owl:ObjectProperty ;
    rdfs:domain ntwf:WorkflowStep ;
    rdfs:range ntwf:Workflow ;
    rdfs:label "is step of"@en ;
    rdfs:comment
        "Inverse of ntwf:hasStep. Enables navigation from a step to
its containing workflow without traversing the full step list."@en ;
    owl:inverseOf ntwf:hasStep ;
    rdfs:isDefinedBy <https://ontology.specialsolutions.example.com/
workflow> .

ntwf:precedesStep
    a owl:ObjectProperty , owl:TransitiveProperty ;
    rdfs:domain ntwf:WorkflowStep ;
    rdfs:range ntwf:WorkflowStep ;
    rdfs:label "precedes step"@en ;
    rdfs:comment
       "Expresses the execution ordering relationship between
workflow steps. Declared owl:TransitiveProperty — a reasoner will
infer that if step A precedes step B and step B precedes step C, then
step A precedes step C. This inference is used to validate that the
ABox step chain is internally consistent before deployment.
Complements ntwf:sequencePosition: use the integer for positional
queries, use the transitive property for full ordering-chain
reasoning."@en ;
    rdfs:isDefinedBy <https://ontology.specialsolutions.example.com/
workflow> .

ntwf:stepDescription
    a owl:AnnotativeProperty , owl:TransitiveProperty ;
    rdfs:domain ntwf:WorkflowStep ;
    rdfs:range xsd:string ;
    rdfs:label "step description"@en ;
    rdfs:comment
       "Provides a description of the intent of the step."@en ;
    rdfs:isDefinedBy <https://ontology.specialsolutions.example.com/
workflow> .
```

A SHACL Node Shape is not a class, though it is is frequently used to build a class. I’m going to add three new namespaces here - sh: and ntwfsh: (which I’ll declare in a bit). The sh: namespace is the SHACL namespace and contains all of the terms in the SHACL ontology for constructing SHACL, while the shape: namespace is used to identify specific shapes that are specific to the ntwf: namespace (these become building blocks for ntwf:).

The workflow node shape can then be described as follows:

```
shape:Workflow a sh:NodeShape ;
      sh:targetClass ntfs:Workflow ;
      sh:property shape:Workflow_hasStep, shape:workflowStatus ;
.
```

What this essentially says is that the set of nodes to be worked on is the set of nodes of type `ntfs:Workflow`, and that there are two property validators (property shapes) that each node should be checked against.

As an aside, note that the SHACL model is the reverse of the RDFS/OWL model, with the node shape forward linking to the properties, rather than the inverse via the `rdfs:domain` property or the `owl:restriction` property. This can be seen in the following diagram:

[

![](https://substackcdn.com/image/fetch/$s_!C99r!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F057aa18d-7c4a-44a8-adbd-99680792eb30_3285x1835.png)



](https://substackcdn.com/image/fetch/$s_!C99r!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F057aa18d-7c4a-44a8-adbd-99680792eb30_3285x1835.png)

Regarding the second breakdown, the old:equivalentClass property should generally be used preferentially. What it says is that the Base Class should be treated as equivalent to the referred class, which is typically anonymous here, for purposes of adding a property. An example of this can be seen as follows:

```
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <https://example.org/ns#> .

ex:SeniorEngineer a owl:Class ;
    rdfs:label "Senior Engineer" ;
    owl:equivalentClass [
        a owl:Class ;
        owl:intersectionOf (
            ex:Engineer
            [ a owl:Restriction ;
              owl:onProperty ex:yearsExperience ;
              owl:minQualifiedCardinality "8"^^xsd:nonNegativeInteger ;
              owl:onDataRange xsd:integer ]
            [ a owl:Restriction ;
              owl:onProperty ex:hasSkill ;
              owl:someValuesFrom ex:LeadershipSkill ]
        )
    ] .
```

In this case, a senior engineer is equivalent to an engineer with 8 years of experience and leadership skills. This gets away from the forced hierarchy of r`dfs:subClassO`f, though personally the SHACL phrasing is more intuitive, and requires fewer hops in the graph.

A common naming pattern for property shapes is to give it as shape:class_property for the simplest constraints, then add additional underscored tags for any qualifiers. The `shape:Workflow_hasStep` property shape can then be defined as follows:

```
shape:Workflow_hasStep a sh:PropertyShape ;
     sh:name "workflow step" ;
     sh:path ntwf:WorkflowStep ;
     sh:nodeKind sh:IRI;
     sh:class ntwf:WorkflowStep ;
     sh:codeIdentifier "workflowStep" ;
.
```

In this case, the property shape identifies a path, which can be either a predicate (here `ntwf:WorkFlowStep`) or a compound path of some sort (which I’ll cover in a subsequent post).

> Significantly, this approach of wrapping the specific path implementation creates an abstraction layer that enables more complex operations, giving a much more expressive and nuanced interpretation of properties in SHACL.

The path should resolve to an IRI rather than a literal (`sh:nodeKind sh:iri`) and the node value should be a workflow step. Finally, the property shape is useful for storing additional metadata, such as a code identifier, which can be used by JSON-LD or similar formats to define hash names.

Notice that there is no cardinality information here. This is because there is an implicit assumption that sh:minCount is 0, and sh:maxCount is unbounded. If either of these are explicitly specified then these would need to be included in the property shape definition.

The second property illustrates binding to a SKOS concept:

```
shape:Workflow_WorkflowStatus
    a sh:PropertyShape ;
    sh:path ntwf:worflowStatus ;
    sh:class skos:Concept ;
    sh:nodeKind sh:IRI ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:node [
       sh:property [
          sh:path skos:inScheme ;
          sh:hasValue ntwf:WorkflowStatusScheme;
       ] ;
    ] 
.
```

This is a similar property shape, but with a twist: the sh:node attribute here provides a link to a node shape with an implicit property shape, indicating that the node value (the object or ?o in the ?s ?p ?o graph) is a closs with a `skos:inScheme` predicate, pointing to the `ntwf:WorkflowStatusScheme` . This retrieves one concept from the workflow status scheme.

The full listing for the two node shapes and their associated property shapes and taxonomies is shown as follows:

```
@prefix sh:      <http://www.w3.org/ns/shacl#> .
@prefix shape:   <http://example.org/shapes/ntwf/> .
@prefix ntwf:    <http://example.org/ontology/ntwf/> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:      <http://example.org/data/> .
@prefix dcterms: <http://purl.org/dc/terms/> .

# ── Shapes  ──────────────────────────────────────────────────────

shape:Workflow
    a sh:NodeShape ;
    sh:targetClass ntwf:Workflow ;
    sh:property shape:Workflow_hasStep, shape:Workflow_WorkflowStatus ;
.

shape:WorkflowStep
    a sh:NodeShape ;
    sh:targetClass ntwf:WorkflowStep ;
    sh:property shape:WorkflowStep_precedesStep, 
                shape:WorkflowStep_isStepOf, 
                shape:WorkflowStep_stepDescription ;
 .

shape:Workflow_hasStep
    a sh:PropertyShape ;
    sh:name "workflow step" ;
    sh:path ntwf:hasStep ;
    sh:nodeKind sh:IRI ;
    sh:class ntwf:WorkflowStep ;
    sh:minCount 1 ;
    sh:codeIdentifier "workflowStep" ;
    sh:node shape:WorkflowStep ;
.

shape:Workflow_WorkflowStatus
    a sh:PropertyShape ;
    sh:path ntwf:workflowStatus ;
    sh:class skos:Concept ;
    sh:nodeKind sh:IRI ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:node [
        sh:property [
            sh:path skos:inScheme ;
            sh:hasValue ntwf:WorkflowStatusScheme ;
        ] ;
    ] ;
.

shape:WorkflowStep_precedesStep
    a sh:PropertyShape ;
    sh:name "precedes step" ;
    sh:path ntwf:precedesStep ;
    sh:nodeKind sh:IRI ;
    sh:class ntwf:WorkflowStep ;
    sh:codeIdentifier "precedesStep" ;
    sh:node shape:WorkflowStep ;
.

shape:WorkflowStep_isStepOf
    a sh:PropertyShape ;
    sh:name "is step of" ;
    sh:path ntwf:isStepOf ;
    sh:nodeKind sh:IRI ;
    sh:class ntwf:Workflow ;
    sh:codeIdentifier "isStepOf" ;
    sh:node shape:Workflow ;
.

shape:WorkflowStep_stepDescription
    a sh:PropertyShape ;
    sh:name "step description" ;
    sh:path ntwf:stepDescription ;
    sh:nodeKind sh:Literal ;
    sh:datatype rdf:LangString ;
    sh:codeIdentifier "description" ;
.


# ── SKOS Vocabulary ─────────────────────────────────────────────────────────

ntwf:WorkflowStatusScheme
    a skos:ConceptScheme ;
    skos:prefLabel "Workflow Status Scheme"@en ;
    dcterms:description "Controlled vocabulary for workflow lifecycle states." ;
.

ntwf:StatusDraft
    a skos:Concept ;
    skos:prefLabel "Draft"@en ;
    skos:inScheme ntwf:WorkflowStatusScheme ;
    skos:notation "DRAFT" ;
.

ntwf:StatusActive
    a skos:Concept ;
    skos:prefLabel "Active"@en ;
    skos:inScheme ntwf:WorkflowStatusScheme ;
    skos:notation "ACTIVE" ;
.

ntwf:StatusComplete
    a skos:Concept ;
    skos:prefLabel "Complete"@en ;
    skos:inScheme ntwf:WorkflowStatusScheme ;
    skos:notation "COMPLETE" ;
.

ntwf:StatusSuspended
    a skos:Concept ;
    skos:prefLabel "Suspended"@en ;
    skos:inScheme ntwf:WorkflowStatusScheme ;
    skos:notation "SUSPENDED" ;
.
```

Once you have the SHACL defined, it becomes easier to test the SHACL against both valid and invalid data. The valid dataset is given below, and returns a conformant response message:

```
@prefix sh:      <http://www.w3.org/ns/shacl#> .
@prefix shape:   <http://example.org/shapes/ntwf/> .
@prefix ntwf:    <http://example.org/ontology/ntwf/> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix ex:      <http://example.org/data/> .
@prefix dcterms: <http://purl.org/dc/terms/> .


# ════════════════════════════════════════════════════════════════
#  VALID EXAMPLE
# ════════════════════════════════════════════════════════════════
#
# Workflow:
#   ✓ a ntwf:Workflow
#   ✓ ntwf:hasStep — ≥1 values, all sh:IRI, all a ntwf:WorkflowStep
#   ✓ ntwf:workflowStatus — exactly 1, sh:IRI, a skos:Concept,
#       skos:inScheme ntwf:WorkflowStatusScheme
#
# Each WorkflowStep:
#   ✓ ntwf:precedesStep — sh:IRI, a ntwf:WorkflowStep  (where present)
#   ✓ ntwf:isStepOf     — sh:IRI, a ntwf:Workflow
#   ✓ ntwf:stepDescription — rdf:LangString ("..."@lang)

ex:Workflow_Valid
    a ntwf:Workflow ;
    dcterms:title "Valid Document Review Workflow"@en ;
    ntwf:hasStep
        ex:Step_V_Intake,
        ex:Step_V_Review,
        ex:Step_V_Approve ;
    ntwf:workflowStatus ntwf:StatusActive ;
.

ex:Step_V_Intake
    a ntwf:WorkflowStep ;
    dcterms:title "Intake"@en ;
    ntwf:stepDescription "Receive and log the incoming request."@en ;
    ntwf:isStepOf ex:Workflow_Valid ;
    ntwf:precedesStep ex:Step_V_Review ;
.

ex:Step_V_Review
    a ntwf:WorkflowStep ;
    dcterms:title "Review"@en ;
    ntwf:stepDescription "Assess the request against acceptance criteria."@en ;
    ntwf:isStepOf ex:Workflow_Valid ;
    ntwf:precedesStep ex:Step_V_Approve ;
.

ex:Step_V_Approve
    a ntwf:WorkflowStep ;
    dcterms:title "Approve"@en ;
    ntwf:stepDescription "Issue final disposition."@en ;
    ntwf:isStepOf ex:Workflow_Valid ;
    # terminal step — no ntwf:precedesStep (sh:minCount absent → 0 is fine)
.

# Multiple language tags on stepDescription are all valid —
# each value is a distinct rdf:LangString literal.
ex:Step_V_MultiLang
    a ntwf:WorkflowStep ;
    ntwf:stepDescription "Translate documentation."@en ;
    ntwf:stepDescription "Übersetzen Sie die Dokumentation."@de ;
    ntwf:stepDescription "Traduire la documentation."@fr ;
    ntwf:isStepOf ex:Workflow_Valid ;
.
```

Several invalid examples are given below:

```


# ════════════════════════════════════════════════════════════════
#  SHARED RESOURCES FOR INVALID EXAMPLES
# ════════════════════════════════════════════════════════════════

ex:Step_Good                          # clean step for use as a reference IRI
    a ntwf:WorkflowStep ;
    ntwf:stepDescription "A well-formed step."@en ;
    ntwf:isStepOf ex:Workflow_Valid ;
.

ex:SomeDocument  a ex:Document .      # wrong class for sh:class ntwf:WorkflowStep
ex:SomeProject   a ex:Project .       # wrong class for sh:class ntwf:Workflow

ex:AnotherScheme a skos:ConceptScheme .

ex:StatusRogue
    a skos:Concept ;
    skos:prefLabel "Rogue"@en ;
    skos:inScheme ex:AnotherScheme ;  # NOT ntwf:WorkflowStatusScheme
.


# ════════════════════════════════════════════════════════════════
#  INVALID — WORKFLOW LEVEL
# ════════════════════════════════════════════════════════════════

# ── WF-1: no ntwf:hasStep ────────────────────────────────────────
# shape:Workflow_hasStep  sh:minCount 1  →  0 < 1

ex:Workflow_NoSteps
    a ntwf:Workflow ;
    dcterms:title "Workflow with no steps"@en ;
    ntwf:workflowStatus ntwf:StatusDraft ;
.


# ── WF-2: no ntwf:workflowStatus ─────────────────────────────────
# shape:Workflow_WorkflowStatus  sh:minCount 1  →  0 < 1

ex:Workflow_NoStatus
    a ntwf:Workflow ;
    dcterms:title "Workflow with no status"@en ;
    ntwf:hasStep ex:Step_Good ;
.


# ── WF-3: two ntwf:workflowStatus values ─────────────────────────
# shape:Workflow_WorkflowStatus  sh:maxCount 1  →  2 > 1

ex:Workflow_TwoStatuses
    a ntwf:Workflow ;
    dcterms:title "Workflow with duplicate status"@en ;
    ntwf:hasStep ex:Step_Good ;
    ntwf:workflowStatus ntwf:StatusActive ;
    ntwf:workflowStatus ntwf:StatusDraft ;
.


# ── WF-4: status concept in wrong scheme ─────────────────────────
# sh:node [ sh:property [ sh:path skos:inScheme ;
#                         sh:hasValue ntwf:WorkflowStatusScheme ] ]
# ex:StatusRogue is in ex:AnotherScheme, not ntwf:WorkflowStatusScheme

ex:Workflow_WrongScheme
    a ntwf:Workflow ;
    dcterms:title "Workflow with out-of-scheme status"@en ;
    ntwf:hasStep ex:Step_Good ;
    ntwf:workflowStatus ex:StatusRogue ;
.


# ── WF-5: workflowStatus is a blank node ─────────────────────────
# shape:Workflow_WorkflowStatus  sh:nodeKind sh:IRI
# Blank nodes are sh:BlankNode, not sh:IRI

ex:Workflow_BlankStatus
    a ntwf:Workflow ;
    dcterms:title "Workflow with inline blank-node status"@en ;
    ntwf:hasStep ex:Step_Good ;
    ntwf:workflowStatus [
        a skos:Concept ;
        skos:prefLabel "Inline"@en ;
        skos:inScheme ntwf:WorkflowStatusScheme ;
    ] ;
.


# ── WF-6: hasStep value is wrong rdf:type ────────────────────────
# shape:Workflow_hasStep  sh:class ntwf:WorkflowStep
# ex:SomeDocument is a named IRI (nodeKind passes) but
# is not typed as ntwf:WorkflowStep

ex:Workflow_WrongStepClass
    a ntwf:Workflow ;
    dcterms:title "Workflow whose step is a Document"@en ;
    ntwf:hasStep ex:SomeDocument ;
    ntwf:workflowStatus ntwf:StatusDraft ;
.


# ── WF-7: hasStep value is a literal ─────────────────────────────
# shape:Workflow_hasStep  sh:nodeKind sh:IRI
# Literals are never sh:IRI

ex:Workflow_LiteralStep
    a ntwf:Workflow ;
    dcterms:title "Workflow with literal step reference"@en ;
    ntwf:hasStep "step-one" ;
    ntwf:workflowStatus ntwf:StatusDraft ;
.


# ════════════════════════════════════════════════════════════════
#  INVALID — WORKFLOWSTEP LEVEL
# ════════════════════════════════════════════════════════════════

# ── WS-1: stepDescription is a plain xsd:string ──────────────────
# shape:WorkflowStep_stepDescription  sh:datatype rdf:LangString
# Plain literals ("..."^^xsd:string) are NOT rdf:LangString.
# This was VALID in the previous shape version; it is now a violation.

ex:Step_PlainString
    a ntwf:WorkflowStep ;
    ntwf:stepDescription "Triage the incoming request."^^xsd:string ; # ← violation
    ntwf:isStepOf ex:Workflow_Valid ;
.


# ── WS-2: stepDescription is an untyped bare literal ─────────────
# Turtle bare strings resolve to xsd:string in RDF 1.1,
# which is not rdf:LangString

ex:Step_BareLiteral
    a ntwf:WorkflowStep ;
    ntwf:stepDescription "No language tag here." ;                   # ← xsd:string → violation
    ntwf:isStepOf ex:Workflow_Valid ;
.


# ── WS-3: stepDescription is a numeric literal ───────────────────
# sh:nodeKind sh:Literal passes (integers are literals),
# but sh:datatype rdf:LangString fails (xsd:integer ≠ rdf:LangString)

ex:Step_IntegerDescription
    a ntwf:WorkflowStep ;
    ntwf:stepDescription 42 ;                                        # ← xsd:integer → violation
    ntwf:isStepOf ex:Workflow_Valid ;
.


# ── WS-4: stepDescription is an IRI ──────────────────────────────
# shape:WorkflowStep_stepDescription  sh:nodeKind sh:Literal
# IRIs are never sh:Literal (fails both nodeKind and datatype)

ex:Step_IriDescription
    a ntwf:WorkflowStep ;
    ntwf:stepDescription ex:SomeDocument ;                           # ← IRI → nodeKind violation
    ntwf:isStepOf ex:Workflow_Valid ;
.


# ── WS-5: precedesStep points to wrong class ─────────────────────
# shape:WorkflowStep_precedesStep  sh:class ntwf:WorkflowStep
# ex:SomeDocument is a named IRI (nodeKind passes) but wrong type

ex:Step_BadPrecedesClass
    a ntwf:WorkflowStep ;
    ntwf:stepDescription "Step that chains to a Document."@en ;
    ntwf:precedesStep ex:SomeDocument ;                              # ← not ntwf:WorkflowStep
    ntwf:isStepOf ex:Workflow_Valid ;
.


# ── WS-6: precedesStep is a blank node ───────────────────────────
# shape:WorkflowStep_precedesStep  sh:nodeKind sh:IRI

ex:Step_BlankPrecedes
    a ntwf:WorkflowStep ;
    ntwf:stepDescription "Step with inline successor."@en ;
    ntwf:precedesStep [                                              # ← blank node → nodeKind violation
        a ntwf:WorkflowStep ;
        ntwf:stepDescription "Inline next step."@en ;
    ] ;
    ntwf:isStepOf ex:Workflow_Valid ;
.


# ── WS-7: isStepOf points to wrong class ─────────────────────────
# shape:WorkflowStep_isStepOf  sh:class ntwf:Workflow
# ex:SomeProject is a named IRI but is not typed as ntwf:Workflow

ex:Step_BadIsStepOf
    a ntwf:WorkflowStep ;
    ntwf:stepDescription "Step that belongs to a Project."@en ;
    ntwf:isStepOf ex:SomeProject ;                                   # ← not ntwf:Workflow
.


# ── WS-8: isStepOf is a blank node ───────────────────────────────
# shape:WorkflowStep_isStepOf  sh:nodeKind sh:IRI

ex:Step_BlankIsStepOf
    a ntwf:WorkflowStep ;
    ntwf:stepDescription "Step whose parent workflow is inline."@en ;
    ntwf:isStepOf [                                                  # ← blank node → nodeKind violation
        a ntwf:Workflow ;
        ntwf:workflowStatus ntwf:StatusDraft ;
    ] ;
.
```

The invalid content, when run through a SHACL validator, returns the following Turtle response messages:

````
@prefix sh:      <http://www.w3.org/ns/shacl#> .
@prefix shape:   <http://example.org/shapes/ntwf/> .
@prefix ntwf:    <http://example.org/ontology/ntwf/> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix ex:      <http://example.org/data/> .
@prefix dcterms: <http://purl.org/dc/terms/> .

# ════════════════════════════════════════════════════════════════
#  SHACL VALIDATION REPORT
# ════════════════════════════════════════════════════════════════
# Notes on conventions used:
#   • sh:value is omitted for sh:MinCountConstraintComponent and
#     sh:MaxCountConstraintComponent — there is no single offending
#     value node; the violation is on the count itself.
#   • WF-4 (wrong scheme): the processor validates the value node
#     (ex:StatusRogue) against the anonymous sh:node shape. The
#     inner violation focus is ex:StatusRogue, not the workflow.
#     pySHACL and TopBraid both surface the inner result.
#   • Blank node sh:value entries use [] notation; processors
#     assign internal identifiers in practice.

[] a sh:ValidationReport ;
    sh:conforms false ;

    # ── WF-1 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Workflow_NoSteps ;
        sh:resultPath         ntwf:hasStep ;
        sh:sourceShape        shape:Workflow_hasStep ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Minimum count of 1 required for ntwf:hasStep; found 0."@en ;
    ] ;

    # ── WF-2 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Workflow_NoStatus ;
        sh:resultPath         ntwf:workflowStatus ;
        sh:sourceShape        shape:Workflow_WorkflowStatus ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Minimum count of 1 required for ntwf:workflowStatus; found 0."@en ;
    ] ;

    # ── WF-3 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Workflow_TwoStatuses ;
        sh:resultPath         ntwf:workflowStatus ;
        sh:sourceShape        shape:Workflow_WorkflowStatus ;
        sh:sourceConstraintComponent sh:MaxCountConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Maximum count of 1 exceeded for ntwf:workflowStatus; found 2."@en ;
    ] ;

    # ── WF-4 ─────────────────────────────────────────────────────
    # Outer: sh:NodeConstraintComponent on the workflow focus node
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Workflow_WrongScheme ;
        sh:resultPath         ntwf:workflowStatus ;
        sh:value              ex:StatusRogue ;
        sh:sourceShape        shape:Workflow_WorkflowStatus ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Value ex:StatusRogue does not conform to sh:node constraint on ntwf:workflowStatus."@en ;
    ] ;
    # Inner: sh:HasValueConstraintComponent on the value node itself
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:StatusRogue ;
        sh:resultPath         skos:inScheme ;
        sh:sourceConstraintComponent sh:HasValueConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Expected skos:inScheme value ntwf:WorkflowStatusScheme; not found on ex:StatusRogue."@en ;
    ] ;

    # ── WF-5 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Workflow_BlankStatus ;
        sh:resultPath         ntwf:workflowStatus ;
        sh:value              [] ;   # the offending blank node
        sh:sourceShape        shape:Workflow_WorkflowStatus ;
        sh:sourceConstraintComponent sh:NodeKindConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Expected sh:IRI for ntwf:workflowStatus; found blank node."@en ;
    ] ;

    # ── WF-6 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Workflow_WrongStepClass ;
        sh:resultPath         ntwf:hasStep ;
        sh:value              ex:SomeDocument ;
        sh:sourceShape        shape:Workflow_hasStep ;
        sh:sourceConstraintComponent sh:ClassConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Value ex:SomeDocument is not an instance of ntwf:WorkflowStep."@en ;
    ] ;

    # ── WF-7 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Workflow_LiteralStep ;
        sh:resultPath         ntwf:hasStep ;
        sh:value              "step-one" ;
        sh:sourceShape        shape:Workflow_hasStep ;
        sh:sourceConstraintComponent sh:NodeKindConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Expected sh:IRI for ntwf:hasStep; found literal \"step-one\"."@en ;
    ] ;

    # ── WS-1 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Step_PlainString ;
        sh:resultPath         ntwf:stepDescription ;
        sh:value              "Triage the incoming request."^^xsd:string ;
        sh:sourceShape        shape:WorkflowStep_stepDescription ;
        sh:sourceConstraintComponent sh:DatatypeConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Expected datatype rdf:LangString for ntwf:stepDescription; found xsd:string."@en ;
    ] ;

    # ── WS-2 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Step_BareLiteral ;
        sh:resultPath         ntwf:stepDescription ;
        sh:value              "No language tag here." ;   # bare = xsd:string in RDF 1.1
        sh:sourceShape        shape:WorkflowStep_stepDescription ;
        sh:sourceConstraintComponent sh:DatatypeConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Expected datatype rdf:LangString for ntwf:stepDescription; found xsd:string (bare literal)."@en ;
    ] ;

    # ── WS-3 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Step_IntegerDescription ;
        sh:resultPath         ntwf:stepDescription ;
        sh:value              42 ;
        sh:sourceShape        shape:WorkflowStep_stepDescription ;
        sh:sourceConstraintComponent sh:DatatypeConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Expected datatype rdf:LangString for ntwf:stepDescription; found xsd:integer."@en ;
    ] ;

    # ── WS-4 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Step_IriDescription ;
        sh:resultPath         ntwf:stepDescription ;
        sh:value              ex:SomeDocument ;
        sh:sourceShape        shape:WorkflowStep_stepDescription ;
        sh:sourceConstraintComponent sh:NodeKindConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Expected sh:Literal for ntwf:stepDescription; found IRI ex:SomeDocument."@en ;
    ] ;

    # ── WS-5 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Step_BadPrecedesClass ;
        sh:resultPath         ntwf:precedesStep ;
        sh:value              ex:SomeDocument ;
        sh:sourceShape        shape:WorkflowStep_precedesStep ;
        sh:sourceConstraintComponent sh:ClassConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Value ex:SomeDocument is not an instance of ntwf:WorkflowStep."@en ;
    ] ;

    # ── WS-6 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Step_BlankPrecedes ;
        sh:resultPath         ntwf:precedesStep ;
        sh:value              [] ;   # the offending blank node
        sh:sourceShape        shape:WorkflowStep_precedesStep ;
        sh:sourceConstraintComponent sh:NodeKindConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Expected sh:IRI for ntwf:precedesStep; found blank node."@en ;
    ] ;

    # ── WS-7 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Step_BadIsStepOf ;
        sh:resultPath         ntwf:isStepOf ;
        sh:value              ex:SomeProject ;
        sh:sourceShape        shape:WorkflowStep_isStepOf ;
        sh:sourceConstraintComponent sh:ClassConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Value ex:SomeProject is not an instance of ntwf:Workflow."@en ;
    ] ;

    # ── WS-8 ─────────────────────────────────────────────────────
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          ex:Step_BlankIsStepOf ;
        sh:resultPath         ntwf:isStepOf ;
        sh:value              [] ;   # the offending blank node
        sh:sourceShape        shape:WorkflowStep_isStepOf ;
        sh:sourceConstraintComponent sh:NodeKindConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Expected sh:IRI for ntwf:isStepOf; found blank node."@en ;
    ] ;
.
```

---

### Plain text equivalents
```
WF-1  ex:Workflow_NoSteps
      MinCountConstraintComponent on ntwf:hasStep
      Minimum count of 1 required for ntwf:hasStep; found 0.

WF-2  ex:Workflow_NoStatus
      MinCountConstraintComponent on ntwf:workflowStatus
      Minimum count of 1 required for ntwf:workflowStatus; found 0.

WF-3  ex:Workflow_TwoStatuses
      MaxCountConstraintComponent on ntwf:workflowStatus
      Maximum count of 1 exceeded for ntwf:workflowStatus; found 2.

WF-4  ex:Workflow_WrongScheme  [outer]
      NodeConstraintComponent on ntwf:workflowStatus, value ex:StatusRogue
      Value ex:StatusRogue does not conform to sh:node constraint on ntwf:workflowStatus.

      ex:StatusRogue  [inner — value node validated against anonymous shape]
      HasValueConstraintComponent on skos:inScheme
      Expected skos:inScheme value ntwf:WorkflowStatusScheme; not found on ex:StatusRogue.

WF-5  ex:Workflow_BlankStatus
      NodeKindConstraintComponent on ntwf:workflowStatus
      Expected sh:IRI for ntwf:workflowStatus; found blank node.

WF-6  ex:Workflow_WrongStepClass
      ClassConstraintComponent on ntwf:hasStep, value ex:SomeDocument
      Value ex:SomeDocument is not an instance of ntwf:WorkflowStep.

WF-7  ex:Workflow_LiteralStep
      NodeKindConstraintComponent on ntwf:hasStep, value "step-one"
      Expected sh:IRI for ntwf:hasStep; found literal "step-one".

WS-1  ex:Step_PlainString
      DatatypeConstraintComponent on ntwf:stepDescription
      Expected datatype rdf:LangString for ntwf:stepDescription; found xsd:string.

WS-2  ex:Step_BareLiteral
      DatatypeConstraintComponent on ntwf:stepDescription
      Expected datatype rdf:LangString for ntwf:stepDescription; found xsd:string (bare literal).

WS-3  ex:Step_IntegerDescription
      DatatypeConstraintComponent on ntwf:stepDescription
      Expected datatype rdf:LangString for ntwf:stepDescription; found xsd:integer.

WS-4  ex:Step_IriDescription
      NodeKindConstraintComponent on ntwf:stepDescription, value ex:SomeDocument
      Expected sh:Literal for ntwf:stepDescription; found IRI ex:SomeDocument.

WS-5  ex:Step_BadPrecedesClass
      ClassConstraintComponent on ntwf:precedesStep, value ex:SomeDocument
      Value ex:SomeDocument is not an instance of ntwf:WorkflowStep.

WS-6  ex:Step_BlankPrecedes
      NodeKindConstraintComponent on ntwf:precedesStep
      Expected sh:IRI for ntwf:precedesStep; found blank node.

WS-7  ex:Step_BadIsStepOf
      ClassConstraintComponent on ntwf:isStepOf, value ex:SomeProject
      Value ex:SomeProject is not an instance of ntwf:Workflow.

WS-8  ex:Step_BlankIsStepOf
      NodeKindConstraintComponent on ntwf:isStepOf
      Expected sh:IRI for ntwf:isStepOf; found blank node.
````

## Summary

This is, of course, not the entire OWL or SHACL schema. In general, if you have an existing OWL or RDFS ontology, a useful first step is to use an LLM to convert and generate the corresponding SHACL, and then go in by hand and manually clean up the exceptions. I’ll be covering this in my next post.

If you are designing an ontology from scratch, you may want to go the opposite route and develop the SHACL schema first as a foundation, especially if you’re working with an ontology where validation matters before inferencing. You can then define OWL relationships to complement the SHACL (or just go with SHACL rules, noting the distinctions between open and closed world assumption modelsdels).

This does raise a critical question: can you have both OWA and CWA active in the same model? The discussion about this gets into some fundamental isses about the nature of the closed/open world assumption duality, something that I’ll defer to a future post.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!DF3h!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe661b6e-311f-40a1-9f8f-969497f050da_2048x2048.jpeg)



](https://substackcdn.com/image/fetch/$s_!DF3h!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe661b6e-311f-40a1-9f8f-969497f050da_2048x2048.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)  
[The Ontologist](https://ontologist.substack.com/)

