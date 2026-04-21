---
type: article
title: Converting from OWL to SHACL, Part I
source: https://substack.com/@kurtcagle/p-190513937
created: 2026-03-12
tags:
  - article
---

# Converting from OWL to SHACL, Part I

Источник: https://substack.com/@kurtcagle/p-190513937

---

Mar 12, 2026

[

![](https://substackcdn.com/image/fetch/$s_!ZwsS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6950ed48-7593-48b2-9530-5d56842f16d2_1344x768.jpeg)



](https://substackcdn.com/image/fetch/$s_!ZwsS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6950ed48-7593-48b2-9530-5d56842f16d2_1344x768.jpeg)

_Jessica Talisman has been publishing a superb series on the development of ontologies:_

[

![](https://substackcdn.com/image/fetch/$s_!6thL!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7ece832-4723-4e82-8898-e149a93fa09b_995x995.png)Intentional Arrangement

Ontology, Part III

The full NTWF ontology is available here on Substack for paying subscribers, and as a PDF, near the conclusion of this essay. I will be publishing the SPARQL testing environment once I have it up and running…

Read more

a month ago · 6 likes · 10 comments · Jessica Talisman

](https://jessicatalisman.substack.com/p/ontology-part-iii?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

_She recently reached out to me about writing an article on converting from OWL to SHACL. As I’ve been leading up to the issue, it seemed like a good opportunity to take up the challenge._

_I’m breaking this up into two articles, simply because it’s worth covering in depth some of the design implications of RDFS/OWL vs. SHACL first._

_I also want to thank Peter Rivett, who walked me through several subtle gotchas I originally got wrong on OWL._

## Reasons for Conversions

Before digging in too deeply into the nuts and bolts of doing a conversion, it’s worth taking the time to examine why you would want to convert from OWL to SHACL in the first place. There are several possible benefits to doing so:

- **More UML-Centric.** SHACL is a lower-level protocol that works better for describing information in a more traditional UML-centric approach than OWL does, in a manner similar to the XML Schema Definition Language (XSD), JSON-Schema, and SQL Data Description Language (DDL), as well as more readily aligning with tabular data sources such as CSV and Excel.
    
- **Validation.** SHACL is more oriented toward validation, especially for new content uploaded to a knowledge graph. OWL can be used for validation, but it’s not really designed for customisable validation, and the fact that most reasoner profiles provide very limited support for validation natively means that SHACL works better as part of a data pipeline.
    
- **No Reasoner.** Not all RDF engines have accessible support for reasoners, and even those that do don’t necessarily have support for all profiles of reasoners. With SHACL rules, you can make triple generation portable by bringing only enough of a model into a schema set to handle the specific use cases for that schema.
    
- **Closed, But With Open Optional.** OWL is built on the open world assumption. SHACL is closed-world, making it useful for dealing with data conversions from relational databases that need to have a close-world assumption.
    
- **When Classes Aren’t Available.** One surprisingly common use case is when incoming data lacks class bindings. SHACL can be configured to look specifically for certain constraint patterns without needing to know a priori which class a resource is used for. In effect, this turns SHACL into a first-pass classifier.
    
- **Reification Support.** OWL does not have native support for reification; SHACL does. If you are working with reified (annotational) content, converting OWL to SHACL, then adding support for reification via SHACL provides one way of making data based on OWL better designed for reification.
    

One additional approach that can give you the best of both worlds is to add SHACL to OWL. In this case, the OWL provides support for inferencing, while SHACL allows you to work with structural definitions, which are often more direct and easier to understand. This also lets you define both documentation and validation handlers more consistently.

## Conversion Design Considerations

OWL does not necessarily map directly to SHACL in all cases because their underlying design models differ. Knowing what these differences are can avert catastrophe.

## `rdfs:subClassOf` vs `sh:node` in a NodeShape

These operate in fundamentally different layers of the RDF stack — one is **ontological** (T-Box), the other is **validation** (S-Box). They can produce superficially similar effects but differ in nature, semantics, and practical consequences.

---

### `rdfs:subClassOf` — Ontological Inheritance

```
ex:Animal a owl:Class .
ex:Dog rdfs:subClassOf ex:Animal .
```

This is a **statement about the world** (or your model of it). It asserts a subsumption relationship between classes in the T-Box:

- Any instance of `ex:Dog` is _entailed_ to also be an instance of `ex:Animal`
    
- This entailment is _inferential_ — a reasoner must materialize it, or a SPARQL query must account for it via `rdfs:subClassOf*`
    
- It says nothing directly about what properties a node must have
    
- It has no validation semantics on its own
    

When combined with a NodeShape, it tells you _what kind of thing_ is being constrained:

```
ex:Dog rdfs:subClassOf ex:Animal ;

shape:DogShape a sh:NodeShape ;
    sh:targetClass ex:Dog ;
    sh:property [ sh:path ex:breed ] ;
.
```

But here the `rdfs:subClassOf` is a claim about the _shape resource_ in the ontology, not a SHACL mechanism — SHACL validators will **ignore it entirely** unless you explicitly wire it up.

---

### `sh:node` — Validation Delegation

```
shape:DogShape a sh:NodeShape ;
    sh:targetClass ex:Dog ;
    sh:node shape:AnimalShape ;
    sh:property [ sh:path ex:breed ] .
```

This is a **validation constraint** — it asserts that the focus node must _also pass validation_ against `shape:AnimalShape`. It is:

- Processed directly by any conformant SHACL validator with no inference required
    
- Purely about constraint satisfaction, not ontological membership
    
- Transitive only at validation time (not in the graph itself)
    
- Capable of producing its own validation results with `sh:sourceShape` pointing to the delegated shape
    

---

### Side-by-side comparison

[

![](https://substackcdn.com/image/fetch/$s_!A0iw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c6054ae-a227-48a6-8333-ad54d15efd71_738x430.png)



](https://substackcdn.com/image/fetch/$s_!A0iw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c6054ae-a227-48a6-8333-ad54d15efd71_738x430.png)

---

### The subtle interplay

Where they _interact_ is through `sh:targetClass` and RDFS entailment. Consider:

```
ex:Dog rdfs:subClassOf ex:Animal .

shape:AnimalShape a sh:NodeShape ;
    sh:targetClass ex:Animal ;
    sh:property [ sh:path ex:name ] .
```

If your SHACL engine is running in **RDFS entailment regime**, then instances of `ex:Dog` are entailed to be `ex:Animal`, and therefore fall within `shape:AnimalShape`‘s target — without any `sh:node` anywhere. But most production SHACL validators (including pySHACL in default mode) do **not** apply RDFS entailment unless explicitly configured, so this only works if those triples are already materialized.

`sh:node` by contrast requires **no entailment regime** — it works in plain SHACL regardless.

---

### Design guidance

Use `rdfs:subClassOf` when you’re making a **claim about your domain model** — what things _are_.

Use `sh:node` when you’re **composing validation constraints** — what things _must satisfy_.

In a well-architected ontology system (T-Box / A-Box / S-Box separation), these live in different graphs and serve different masters. Conflating them — e.g., assuming that `rdfs:subClassOf` alone will cause a SHACL validator to inherit constraints — is one of the more common sources of validation gaps in real-world deployments.

## Disjoint Classes: OWL vs SHACL 1.2

### OWL — Ontological Disjointness

OWL provides two mechanisms:

```
# Pairwise — explicit bilateral assertion
ex:Animal owl:disjointWith ex:Vehicle .

# N-ary — more compact for multiple classes
[ a owl:AllDisjointClasses ;
  owl:members ( ex:Animal ex:Vehicle ex:Location ) ] .
```

This is an open**-world T-Box assertion** — it states that no individual can simultaneously be a member of both classes. A reasoner will:

- Detect a contradiction if `ex:Fido a ex:Animal, ex:Vehicle`
    
- Infer `ex:Fido a owl:Nothing` (the empty class) in that case
    
- Flag this as an _inconsistency_ — the ontology itself becomes incoherent
    

The key point: **OWL disjointness is about logical consistency**, not data quality. It operates through entailment and requires a DL reasoner (HermiT, Pellet, ELK) to enforce. A plain SPARQL query or SHACL validator won’t see it.

---

### SHACL 1.2 — Constraint-Based Disjointness

SHACL has no native `sh:disjointWith` for classes. You model disjointness as a **validation constraint** using one of several patterns:

#### Pattern 1: `sh:not` + `sh:class` (SHACL 1.1, still primary)

```
shape:AnimalShape a sh:NodeShape ;
    sh:targetClass ex:Animal ;
    sh:not [
        sh:class ex:Vehicle
    ] .
```

This says: any node targeted as `ex:Animal` must **not** conform to `sh:class ex:Vehicle`. Symmetric disjointness requires two shapes:

```
shape:VehicleShape a sh:NodeShape ;
    sh:targetClass ex:Vehicle ;
    sh:not [ sh:class ex:Animal ] .
```

#### Pattern 2: `sh:xone` for mutual exclusion

```
shape:PhysicalEntityShape a sh:NodeShape ;
    sh:targetClass ex:PhysicalEntity ;
    sh:xone (
        [ sh:class ex:Animal ]
        [ sh:class ex:Vehicle ]
        [ sh:class ex:Location ]
    ) .
```

`sh:xone` (exactly one) enforces that the focus node satisfies **exactly one** of the listed class memberships — mutual exclusion across the whole set in a single shape. This is the closest structural analog to `owl:AllDisjointClasses`.

#### Pattern 3: SHACL 1.2 `sh:if`/`sh:then`/`sh:else`

SHACL 1.2 opens up conditional disjointness patterns:

```
shape:DisjointCheck a sh:NodeShape ;
    sh:targetClass ex:PhysicalEntity ;
    sh:if [ sh:class ex:Animal ] ;
    sh:then [
        sh:not [ sh:class ex:Vehicle ] ;
        sh:not [ sh:class ex:Location ]
    ] .
```

This is more expressive for asymmetric or conditional disjointness scenarios — e.g., “if something is classified as an Animal, it must not also be a Vehicle” — without requiring the symmetric mirror shape.

---

### Side-by-side comparison

[

![](https://substackcdn.com/image/fetch/$s_!dHbd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89a1e4a5-4dfd-4f8e-8240-62e733e899ae_744x458.png)



](https://substackcdn.com/image/fetch/$s_!dHbd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89a1e4a5-4dfd-4f8e-8240-62e733e899ae_744x458.png)

---

### The fundamental semantic gap

This is the crux of the difference:

- OWL disjointness says the **world cannot contain** an individual of both types — it’s a metaphysical claim. If your data violates it, the data (rather than the graph) is _broken_.
    
- SHACL disjointness says **this data instance fails a quality check** — it’s an engineering claim. If your data violates it, you get a report and move on.
    

OWL operates under the **Open World Assumption** — absence of a type assertion doesn’t mean the type is absent. SHACL operates under a **locally closed** assumption over its targets — what’s in the graph is what gets checked.

This means OWL disjointness can cascade into inferences, while SHACL disjointness simply flags the node and continues. For most production data validation scenarios — particularly when ingesting third-party data — the SHACL approach is more operationally tractable. OWL disjointness is more useful when you’re doing automated classification or building a canonical knowledge graph where consistency must be guaranteed.

## `owl:Restriction` and `sh:PropertyShape`

These two constructs are often conflated because they both constrain how properties are used on classes — but they operate in fundamentally different paradigms.

---

### `owl:Restriction` — Open-World Entailment

An `owl:Restriction` is a **logical axiom** in the OWL sense. It participates in the Open World Assumption and is used by a reasoner to _infer_ class membership or derive new facts.

```
ex:LabResult
  a owl:Class ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ex:hasValue ;
    owl:allValuesFrom xsd:decimal
  ] .
```

What this says logically: _if something is a_ `LabResult`_, then any value of_ `ex:hasValue` _must be an_ `xsd:decimal`. A reasoner can use this to **classify** an individual or detect an inconsistency — but under OWA it will not flag a _missing_ value as an error, and it will not tell you the graph is invalid. It tells you what _must be true in all possible worlds consistent with the ontology_.

Key OWL restriction types:

[

![](https://substackcdn.com/image/fetch/$s_!KyI9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0fae8cb2-21f5-4524-abc4-88e2c531c593_740x274.png)



](https://substackcdn.com/image/fetch/$s_!KyI9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0fae8cb2-21f5-4524-abc4-88e2c531c593_740x274.png)

Because OWL operates under OWA, a missing triple is simply _unknown_, not _invalid_.

---

### `sh:PropertyShape` — Closed-World Validation

A `sh:PropertyShape` is a **validation rule**. It operates under the Closed World Assumption — the graph you hand to the SHACL engine is treated as complete — and produces a `sh:ValidationReport` rather than inferred triples.

```
ex:LabResultShape
  a sh:NodeShape ;
  sh:targetClass ex:LabResult ;
  sh:property [
    a sh:PropertyShape ;
    sh:path ex:hasValue ;
    sh:datatype xsd:decimal ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:minInclusive 0.0 ;
  ] .
```

This says: _validate every instance of_ `ex:LabResult` _in this graph — it must have exactly one_ e`x:hasValue` _that is a non-negative decimal_. If the triple is absent or wrong, you get a `sh:Violation`. No inference, no entailment.

---

[

![](https://substackcdn.com/image/fetch/$s_!H5Oo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faac2507b-4bd8-4a92-a45c-05a859be7f18_740x492.png)



](https://substackcdn.com/image/fetch/$s_!H5Oo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faac2507b-4bd8-4a92-a45c-05a859be7f18_740x492.png)

[

![](https://substackcdn.com/image/fetch/$s_!_gSx!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4402a3ca-c10f-48fd-a8c4-ca247c0351a1_1440x1353.png)



](https://substackcdn.com/image/fetch/$s_!_gSx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4402a3ca-c10f-48fd-a8c4-ca247c0351a1_1440x1353.png)

---

### Why Both Matter — and Why They Don’t Overlap

The temptation is to think you can replace one with the other. You cannot, because they answer different questions:

- **OWL restriction**: “What is necessarily true about this class of thing across all possible models?” — classification, consistency checking, inference.
    
- **SHACL property shape**: “Does _this specific graph_, right now, conform to these data quality rules?” — validation, report generation, governance.
    

In a well-architected stack (your T-Box / S-Box framing), they are **complementary layers**: the OWL T-Box defines what entities _mean_, and SHACL shapes define what instance data _must look like_ to be considered valid for a given application context. The same property can carry an `owl:allValuesFrom` restriction in the ontology _and_ a tighter `sh:datatype` + `sh:minCount` constraint in a shape — because the ontology expresses logical necessity while the shape expresses operational fitness.

This is also why SHACL shapes can be **context-sensitive** in ways OWL restrictions cannot: you can have one shape for data ingestion, a stricter one for regulatory reporting, and a permissive one for a draft workflow — all validating the same underlying ontology class, none of them touching the T-Box.

---

## Entailments

One additional point - SHACL 1.2 rules do create _entailments_, just as OWL and RDFS rules in a reasoner do.

In logic, an entailment is a relationship between statements where one or more statements _necessarily make another statement true_ — not by assertion, but by the rules of inference built into the logical system. If A entails B, then in any world where A is true, B cannot be false.

The classic form: if you know “all ravens are black” and “this is a raven,” the statement “this is black” is _entailed_ — you didn’t assert it, but the logic forces it to be true.

---

### In RDF/OWL terms

The entailment machinery is defined by the _semantics_ of the vocabulary you’re using. RDF, RDFS, and OWL each define progressively richer entailment regimes.

**RDFS entailment** — if you assert:

turtle

```
ex:hasValue rdfs:range xsd:decimal .
ex:result1   ex:hasValue  "3.14"^^xsd:decimal .
```

A reasoner _entails_ `"3.14" a xsd:decimal` — even though you never wrote that triple. The range axiom forces it.

**OWL entailment** — if you assert:

turtle

```
ex:LabResult rdfs:subClassOf ex:Measurement .
ex:r1        a ex:LabResult .
```

A reasoner entails `ex:r1 a ex:Measurement` — class membership propagates up the hierarchy automatically.

The entailed triples are not stored in the explicit (original) graph; they exist in the _logical closure_ — the full set of facts that _must be true_ given your assertions and the entailment rules. **Note:** This is very much implementation-dependent; for what it’s worth, check with your vendor about the behaviour of their implementation.

---

### The key property: it’s truth-preserving and non-defeasible

Entailment isn’t probabilistic or heuristic. If the axioms are true and the inference rule is sound, the conclusion is guaranteed. This distinguishes it from:

- **Implication** in everyday language (”if it’s raining, probably the ground is wet”) — which can fail
    
- **SHACL validation** — which checks conformance but infers nothing
    
- **SPARQL CONSTRUCT** — which generates new triples but only by explicit query pattern, not by logical necessity. Note that this output is output to the calling process, it’s not actually stored in the graph.
    
- **SPARQL UPDATE INSERT** — which generates new triples in a manner similar to SPARQL CONSTRUCT, but _does_ reinsert the triples back into the graph.
    

---

### Why it matters for your architecture

The reason the OWL/SHACL distinction matters so much is precisely here: OWL axioms _participate in entailment_ while SHACL shapes do not (though SHACL rules do, which I hope to cover more in another article. A `sh:PropertyShape` saying `sh:minCount 1` does not entail that a value exists — it reports that one is missing. An `owl:someValuesFrom` restriction, under a closed-world reasoner, _does_ entail existence (or flags an inconsistency if it can’t be satisfied).

This is also why mixing OWL and SHACL carelessly causes confusion — people write SHACL shapes expecting them to constrain reasoning, or write OWL restrictions expecting them to validate data, and neither does what the other does.

---

## RDFS/OWL Entailment vs. SHACL Rule Generation

SHACL Rules are the precise point where SHACL crosses over from pure validation into entailment territory — and it’s one of the less-discussed parts of the spec.

---

### What SHACL Rules Are

Defined in the SHACL Advanced Features specification, `sh:Rule` allows a shape to _generate new triples_ when its conditions are met. The three rule types are:

`sh:TripleRule` — the most direct: if a node matches the shape, assert a new triple.

```
ex:LabResultShape
  a sh:NodeShape ;
  sh:targetClass ex:LabResult ;
  sh:rule [
    a sh:TripleRule ;
    sh:subject sh:this ;
    sh:predicate rdf:type ;
    sh:object ex:ValidatedMeasurement ;
  ] .
```

Every `ex:LabResult` in the graph gets `rdf:type ex:ValidatedMeasurement` added. That’s entailment — new facts derived from existing ones.

`sh:SPARQLRule` — uses a SPARQL CONSTRUCT body, giving you full graph pattern power:

```
ex:CycleShape
  a sh:NodeShape ;
  sh:targetClass ex:ProficiencyTestCycle ;
  sh:rule [
    a sh:SPARQLRule ;
    sh:construct """
      CONSTRUCT {
        $this ex:hasStatus ex:Closed .
      }
      WHERE {
        $this ex:closedDate ?d .
        FILTER ( ?d < NOW() )
      }
    """ ;
  ] .
```

`sh:ExpressionRule` — uses SHACL-SPARQL expressions rather than full CONSTRUCT queries; less commonly used in practice.

---

### How It Relates to Entailment

As mentioned before, SHACL Rules produce what the spec calls **inferred triples** — and this is genuine entailment in the logical sense, not just data transformation. Given the same graph and the same rules, the

same triples are always derived. It’s deterministic and truth-preserving within the closed world of the graph.

However, there are two important qualifications that distinguish it from OWL entailment:

**1. It’s CWA entailment, not OWA entailment.** SHACL Rules fire on the graph as it exists. OWL entailment reasons over all _possible_ models consistent with the axioms. A SHACL rule won’t infer that a value _must exist_ somewhere — it only acts on what’s actually present.

**2. Execution is procedural, not declarative-logical.** OWL reasoners compute a full deductive closure — they find everything that _must_ be true simultaneously. SHACL Rules execute iteratively, and the spec defines a specific iteration semantics: rules fire in `sh:order` sequence, and the output of one rule can be input to the next. This makes SHACL Rules closer to **Datalog** or **forward-chaining production rules** than to OWL’s model-theoretic semantics.

---

### The Iteration / Fixpoint Question

The spec says rules should be applied until a **fixpoint** is reached — no new triples are produced on another pass. This is exactly how Datalog works, and it gives SHACL Rules a well-defined termination condition _provided the rules are non-recursive in a way that would grow the graph unboundedly_. Circular rules that keep generating new nodes are the pathological case to avoid.

```
# Safe: converges after one pass
sh:rule [
  a sh:TripleRule ;
  sh:subject sh:this ;
  sh:predicate ex:isProcessed ;
  sh:object true ;
] .

# Dangerous: could generate infinite chain if not carefully bounded
sh:rule [
  a sh:SPARQLRule ;
  sh:construct """
    CONSTRUCT { ?next ex:precedes $this }
    WHERE { $this ex:precedes ?prev . BIND(IRI(CONCAT(STR($this),"_next")) AS ?next) }
  """ ;
] .
```

---

### Where This Sits in The Four-Box Model

This is actually the interesting architectural implication: SHACL Rules inhabit the **boundary between S-Box and A-Box**. The rule lives in the S-Box (it’s part of the shape graph), but its _output_ lands in the A-Box (new instance triples). This makes SHACL Rules a principled mechanism for:

- **Materialization** — pre-computing derived facts for query performance
    
- **Classification without OWL** — assigning rdf:type based on data conditions, without needing a full OWL reasoner
    
- **Cross-shape inference** — propagating status or flags across related entities
    

In the example context this is directly useful: you can write an `sh:SPARQLRule` that derives `ex:hasStatus ex:NonConformant` on a cycle when its results breach thresholds, without touching the T-Box ontology at all — keeping your inference logic in the constraint/rule layer where it can be versioned and swapped independently of the ontology.

---

## The Conundrum of `sh:closed`

In SHACL, there is a Node Shape property called `sh:closed` that can be set to true or false (the default). At the same time, I’ve made several references to the fact that SHACL is a closed world validator, so wouldn’t `sh:closed false` prove this wrong?

This is a question that catches a lot of people out, because the two concepts sound similar — both seem to be about “allowing things you haven’t explicitly specified” — but they operate at completely different levels.

---

### What `sh:closed false` Actually Does

`sh:closed` is a constraint on **property scope** — specifically, whether the shape will generate violations for properties on a focus node that aren’t mentioned in any of its `sh:property` declarations.

`sh:closed true` means: flag any property not explicitly listed in this shape (or in `sh:ignoredProperties`) as a violation. It’s a closed-envelope check.

`sh:closed false` (the default — you rarely need to write it explicitly) means: don’t generate violations for unlisted properties. The shape is silent about them. Whatever `sh:property` constraints you’ve specified are still fully enforced — you just don’t penalize extra properties.

```
ex:ResultShape
  a sh:NodeShape ;
  sh:targetClass ex:Result ;
  sh:closed false ;           # default — redundant but explicit
  sh:property [
    sh:path ex:hasValue ;
    sh:datatype xsd:decimal ;
    sh:minCount 1 ;
  ] .
 
```

This shape validates that every `ex:Result` has at least one decimal `ex:hasValue`. If a result node also carries `prov:wasAttributedTo` or `skos:note` or anything else — the shape doesn’t care. Those properties are outside its scope. But the `sh:minCount 1` on `ex:hasValue` is still enforced under full CWA: if the triple is absent, it’s a violation.

---

### Why This Is Not the Open World Assumption

The OWA is about what you conclude from _absence of information_. Under OWA, a missing triple is epistemically neutral — it means “unknown,” not “false.” A reasoner will not conclude that a value doesn’t exist just because it isn’t asserted.

SHACL always operates under CWA, regardless of `sh:closed`. The graph handed to the SHACL engine is treated as complete. Absence is absence.

The difference between `sh:closed true` and `sh:closed false` has nothing to do with this. Both operate under CWA. The distinction is purely:

- `sh:closed true`: the shape has an opinion about _all_ properties on the focus node — unlisted ones are violations.
    
- `sh:closed false`: the shape has an opinion only about the properties it explicitly mentions — it is agnostic about the rest.
    

“Agnostic about unlisted properties” is not the same as “unknown whether they exist.” The SHACL engine knows exactly what properties are in the graph. It just isn’t asked to evaluate them against this shape.

---

[

![](https://substackcdn.com/image/fetch/$s_!CK2r!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbeaf937f-5656-418b-8115-039de237ce9e_757x304.png)



](https://substackcdn.com/image/fetch/$s_!CK2r!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbeaf937f-5656-418b-8115-039de237ce9e_757x304.png)

A useful way to hold the distinction: OWA is about the _logical completeness of the world model_. `sh:closed false` is about the _coverage of a particular validation contract_. You can have a very tightly constrained shape with `sh:closed false` — it just doesn’t police what it wasn’t asked to police.

---

### Where This Matters Practically

The most common place this distinction becomes operationally significant is when you’re layering shapes. If you have a base shape for ex`:Result` and a more specific shape for `ex:CertifiedResult`, you typically want `sh:closed false` on the base shape so that the subclass shape’s additional properties don’t cause base-shape violations. The base shape enforces its contract; the subclass shape enforces its own additions. Neither shape needs to know about the other’s properties.

If you set `sh:closed true` on the base shape, you’d have to enumerate every property that any subclass shape might use in `sh:ignoredProperties` — which defeats the extensibility of the model and is exactly the kind of tight coupling that makes SQL schemas brittle.

---

## Understanding the Uses Cases for Closed vs. Open Reasoners

This distinction between Open World and Closed World dynamics highlights the primary differences between RDFS/OWL and SHACL, and why you might choose to convert from one to the other. Both are capable of reasoning, if by reasoning you mean “to use specific graph patterns to generate triples”, especially once SHACL Rules are taken into account.

There are a number of key use cases where one or the other approach works better:

### Open-World RDFS/OWL: Business Use Cases

- **Cross-organizational knowledge integration.** Data from partners, regulators, and external sources arrives with assumptions you don’t control. OWL’s tolerance for unknown facts means external triples that don’t fit your current schema are additional information, not errors — the model absorbs them without breaking.
    
- **Standards publishing and downstream specialization.** Vocabularies like SNOMED CT, FIBO, and GS1 are published as OWL ontologies so adopters can subclass and extend them without invalidating the upstream definitions. The parent ontology remains stable; specializations compose on top of it.
    
- **Research and hypothesis generation.** Pharmaceutical, genomic, and clinical data is inherently partial — a compound _may_ inhibit a target, a gene _may_ be implicated in a pathway. OWL’s existential and universal restrictions let reasoners classify and connect entities across incomplete datasets, surfacing relationships no explicit assertion made.
    
- **Federated enterprise knowledge graphs.** When HR, finance, and operations each own their data with independent update cadences, OWL’s class and property hierarchies provide a shared conceptual layer each domain populates independently — no schema migration required, no central bottleneck.
    
- **Product and content catalogues with evolving attributes.** E-commerce and media platforms add new product attributes continuously. An OWL-based catalogue accommodates new properties on any entity without requiring every existing record to be updated — unknown attributes on older records are simply absent, not invalid.
    

---

### Closed-World SHACL: Business Use Cases

- **API and ingestion contract enforcement.** When a vendor or system submits a payload, you need a binary conformance answer. SHACL validation reports are structured, actionable, and pipeline-ready — the CWA is appropriate because the submission is the complete record and missing fields are genuine errors.
    
- **Regulatory compliance documentation.** FDA, ISO, and financial reporting regimes require submitted data to be demonstrably complete at the moment of submission. SHACL shapes function as machine-executable, versionable compliance rules — `sh:minCount 1` on a required field is an auditable assertion that the field was checked, something OWL cannot provide.
    
- **Workflow state gating.** Records moving through lifecycle states — Draft, Active, Closed, Archived — have distinct data requirements at each transition. SHACL shapes scoped per state, checked at transition time, enforce completeness as a precondition rather than a post-hoc audit.
    
- **Multi-tenant data quality governance.** Different customers of a SaaS platform carry different data quality obligations. SHACL shape graphs are first-class RDF resources that can be versioned and assigned per tenant — one customer’s shape requiring a field another treats as optional — without touching the shared ontology.
    
- **ETL validation and load lineage.** Before loading transformed data into a warehouse or graph, SHACL validation generates a structured report that becomes part of the load record — documenting what was checked, what passed, and what was remediated. This creates auditable data lineage that neither SQL constraints nor OWL axioms produce.
    
- **Form and document completeness checking.** Insurance underwriting, loan origination, and clinical intake all require specific fields before a record can progress. SHACL shapes encode these requirements declaratively, separate from application logic, and generate human-readable violation messages that drive UI feedback or rejection notices.
    

---

**The governing principle:** use OWL where the domain is larger than your data and meaning must survive federation; use SHACL where the data is the complete record and operational correctness must be enforced and documented.

There is also another alternative - use both RDFS/OWL and SHACL together as part of the same ontology:

## Using RDFS/OWL and SHACL Together: A Layered Methodology

The two technologies address different questions and should be designed in that order: first establish what things _mean_, then specify what data about those things must _look like_ in a given operational context.

---

### Layer 1 — Build the Ontology (T-Box)

Define your classes, properties, and relationships in RDFS/OWL. This layer should be stable, domain-driven, and independent of any particular application or workflow. Key outputs:

- **Class hierarchy** — `rdfs:subClassOf` chains capturing domain taxonomy
    
- **Property definitions** — `owl:ObjectProperty`, `owl:DatatypeProperty`, domain/range declarations
    
- **Logical axioms** — `owl:equivalentClass`, `owl:disjointWith`, restriction axioms where inference is genuinely needed
    
- **Shared vocabulary** — alignment with external ontologies via `owl:sameAs`, `skos:exactMatch`, or `owl:equivalentClass`
    

The ontology answers: _what does this entity type mean, and how does it relate to other entity types?_ It should not encode operational rules, workflow states, or data quality requirements — those belong in SHACL.

---

### Layer 2 — Populate the Instance Graph (A-Box)

Assert instance data against the ontology vocabulary. In RDF 1.2 / RDF-Star, reification annotations attach provenance, timestamps, and confidence directly to triples at this layer — keeping the instance graph append-only and audit-ready without separate audit tables.

---

### Layer 3 — Define Validation Shapes (S-Box)

Write SHACL NodeShapes and PropertyShapes that target the classes defined in the ontology. Shapes should be:

- **Context-scoped** — a shape for ingestion may be permissive; a shape for regulatory submission may be strict. Same ontology class, different shapes for different operational moments.
    
- **Compositional** — use `sh:node` and `sh:and` to inherit from base shapes rather than duplicating constraints. The base shape enforces the minimum; specialized shapes layer additional requirements.
    
- **Decoupled from the T-Box** — shapes reference ontology classes and properties but do not redefine their meaning. Changing a shape does not alter the ontology, and vice versa.
    

---

### Layer 4 — Run Inference Before Validation (Where Applicable)

If your ontology uses reasoning-dependent constructs — `rdfs:subClassOf`, `owl:equivalentClass`, property chains — materialize the inferred triples before running SHACL validation. SHACL operates on the graph as-is; it does not invoke a reasoner. A common failure mode is writing a shape targeting `ex:LabResult` when instances are only typed as `ex:ChemicalLabResult` (a subclass) — without prior inference or an `rdfs:subClassOf` materialization step, those instances are invisible to the shape.

The pipeline therefore runs: **assert → reason → validate**, not **assert → validate**.

---

### Layer 5 — Use SHACL Rules for Lightweight Materialization

Where full OWL reasoning is too heavyweight or unavailable, `sh:SPARQLRule` can materialize derived facts — status flags, classification assignments, computed relationships — that SHACL validation then checks. This keeps inference logic in the shape graph rather than in application code, and makes it versionable alongside the shapes.

---

## Summary Pipeline

```
T-Box Ontology (OWL/RDFS)
        │
        ▼
A-Box Instance Data (RDF-Star, append-only)
        │
        ▼
Inference / Materialization (OWL reasoner or SHACL Rules)
        │
        ▼
SHACL Validation (context-scoped shapes)
        │
        ▼
Validation Report → pipeline gate / compliance record / UI feedback
```

---

## Caveats

**Reasoning scope must be explicit.** OWL has multiple sublanguages (OWL Lite, OWL DL, OWL Full) with different computational complexity profiles. OWL Full is undecidable. For most enterprise use cases OWL DL or OWL 2 RL — which has polynomial complexity and maps cleanly to rule-based materialization — is the appropriate choice. Specify which profile your ontology targets.

**SHACL does not validate entailed triples unless they are materialized.** This is the most common integration failure. If your validation depends on inferred class membership or inferred property values, those inferences must be written into the graph first. Document this dependency explicitly in your architecture.

**Shapes and ontologies version independently — govern that gap.** An ontology property can be deprecated while shapes still reference it, or a shape can impose constraints that contradict a later ontology revision. Treat the T-Box/S-Box interface as a versioned contract: when the ontology changes, audit all shapes that reference the changed terms.

`sh:closed true` **and open-world ontologies are in direct tension.** If you close a shape over a class that participates in an open-world ontology — one that external parties extend — you will generate violations for legitimate properties you simply haven’t enumerated. Use `sh:closed true` only on shapes whose property envelope you fully control.

**SHACL Rules introduce ordering dependencies.** If you use `sh:SPARQLRule` for materialisation, the rule execution order (`sh:order`) matters and must be documented. Undeclared dependencies between rules produce non-deterministic results across engines.

**Engine support for Advanced Features is uneven.** Core SHACL validation is widely supported. SHACL Rules, SHACL-SPARQL constraints, and SHACL 1.2 features like `sh:reifierShape` have varying support across pySHACL, TopBraid, GraphDB, Stardog and others. Validate the engine's capabilities against your feature requirements before committing to a design that depends on them.

---

In my next post, I will explore the process of conversion, using both manual and AI techniques, and will go into a little more depth on how SHACL can bind to RDFS/OWL to give you the best of both worlds.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!z8wo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9e22a8e-3987-4b51-8be6-af42f83d7b07_2048x2048.jpeg)



](https://substackcdn.com/image/fetch/$s_!z8wo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9e22a8e-3987-4b51-8be6-af42f83d7b07_2048x2048.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)