---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Converting-from-OWL-to-SHACL-Part-I
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:56.052753+00:00'
  title: Converting from owl to shacl, part i
  type: plain-doc
  version: '0.1'
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

