---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: A-Library-Task-in-SHACL
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:03.336738+00:00'
  title: A library task in shacl
  type: plain-doc
  version: '0.1'
---

## Why Bundle These Two Things Together?

The inspector and the printer solve opposite problems that arise from the same root cause: _heterogeneous data_.

When data comes from many sources with different labelling habits, you have two obligations. First, _catch the gaps_ — find things that slipped through with no label at all. Second, _normalise the survivors_ — take everything that does have a label and bring it into a consistent form so the rest of your system doesn’t have to care about history.

The constraint component handles the first obligation. The rules handle the second. Putting them in the same shape means they travel together — you deploy one thing and get both behaviours. The shape is the policy; the component and the rules are how the policy is enforced.

## SHACL Label Constraint & Rules — Worked Example

### The Dataset (`data.ttl`)

```
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:     <http://example.org/> .

# ── Node 1: rdfs:label only ────────────────────────────────────────────────
# The simple, canonical case. Should pass and derive all three labels from rdfs:label.

ex:AncientRome a ex:LabelledResource ;
    rdfs:label "Ancient Rome"@en ;
    rdfs:comment "The civilization centred on the city of Rome." .

# ── Node 2: skos:prefLabel only ───────────────────────────────────────────
# Common in thesauri and controlled vocabularies. Should pass; derivations fall
# through to the skos:prefLabel value.

ex:NeuralNetwork a ex:LabelledResource ;
    skos:prefLabel "Neural Network"@en ;
    skos:definition "A computing system loosely modelled on the animal brain." .

# ── Node 3: skosxl:prefLabel via literalForm ──────────────────────────────
# The reified SKOS-XL pattern. The title is on a separate blank node.
# Should pass; the validator follows the pointer.

ex:QuantumEntanglement a ex:LabelledResource ;
    skosxl:prefLabel [
        a skosxl:Label ;
        skosxl:literalForm "Quantum Entanglement"@en ;
        ex:script "Latin" ;
    ] ;
    rdfs:comment "A physical phenomenon with no classical analogue." .

# ── Node 4: Both rdfs:label AND skos:prefLabel ────────────────────────────
# rdfs:label should win the COALESCE race for all three derived predicates.

ex:BlackHole a ex:LabelledResource ;
    rdfs:label    "Black Hole"@en ;
    skos:prefLabel "black hole"@en ;
    rdfs:comment  "A region of spacetime where gravity is so strong that nothing can escape." .

# ── Node 5: rdfs:label in multiple languages ─────────────────────────────
# COALESCE picks whichever SPARQL returns first (engine-dependent order).
# Illustrates the "non-deterministic multi-language" caveat.

ex:Democracy a ex:LabelledResource ;
    rdfs:label "Democracy"@en ;
    rdfs:label "Démocratie"@fr ;
    rdfs:label "Demokratie"@de ;
    rdfs:comment "A system of government by the whole population." .

# ── Node 6: NO label of any kind ─────────────────────────────────────────
# Should FAIL validation. No derived triples should be produced.

ex:Unlabelled a ex:LabelledResource ;
    rdfs:comment "This resource has a comment but no label whatsoever." .
```

Six nodes covering every label scenario:

[

![](https://substackcdn.com/image/fetch/$s_!_hfk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc52089db-8eda-4832-b341-d34619deb8b1_725x424.png)



](https://substackcdn.com/image/fetch/$s_!_hfk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc52089db-8eda-4832-b341-d34619deb8b1_725x424.png)

---

### Step 1 — Validation Report

```
Validation Report
Conforms: False
Results (1):

Constraint Violation in SPARQLConstraintComponent:
    Severity:     sh:Violation
    Source Shape: ex:LabelledResourceShape
    Focus Node:   ex:Unlabelled
    Value Node:   ex:Unlabelled
    Message:      Node <http://example.org/Unlabelled> has no rdfs:label,
                  skos:prefLabel, or skosxl:prefLabel/literalForm.
```

Exactly one violation — only `ex:Unlabelled` fires. All five labelled nodes pass silently.

---

### Step 2 — Inferred Triples (grouped by subject)

#### ex:AncientRome

Source: `rdfs:label "Ancient Rome"@en`

```
ex:AncientRome
    ex:label          "Ancient Rome"@en ;
    ex:lowerCaseLabel "ancient rome"@en ;
    ex:upperCaseLabel "ANCIENT ROME"@en .
```

---

#### ex:NeuralNetwork

Source: `skos:prefLabel "Neural Network"@en` (no rdfs:label — falls through to second slot)

```
ex:NeuralNetwork
    ex:label          "Neural Network"@en ;
    ex:lowerCaseLabel "neural network"@en ;
    ex:upperCaseLabel "NEURAL NETWORK"@en .
```

---

#### ex:QuantumEntanglement

#### Source: `skosxl:prefLabel [ skosxl:literalForm "Quantum Entanglement"@en ]` (validator follows the blank-node pointer; no rdfs:label or skos:prefLabel present)

```
ex:QuantumEntanglement
    ex:label          "Quantum Entanglement"@en ;
    ex:lowerCaseLabel "quantum entanglement"@en ;
    ex:upperCaseLabel "QUANTUM ENTANGLEMENT"@en .
```

---

#### ex:BlackHole

Source: has **both** `rdfs:label "Black Hole"@en` and `skos:prefLabel "black hole"@en`. `rdfs:label` wins the `COALESCE` race.

```
ex:BlackHole
    ex:label          "Black Hole"@en ;    # ← rdfs:label wins
    ex:lowerCaseLabel "black hole"@en ;
    ex:upperCaseLabel "BLACK HOLE"@en .
```

---

#### ex:Democracy

Source: `rdfs:label` in three languages — `@en`, `@fr`, `@de`. Because there is no `FILTER(LANG(...) = "en")` guard, COALESCE promotes **all three** values and three triples are produced per derived predicate. Language tags are preserved by `LCASE()`/`UCASE()` as per SPARQL 1.1.

```
ex:Democracy
    ex:label          "Democracy"@en, "Démocratie"@fr, "Demokratie"@de ;
    ex:lowerCaseLabel "democracy"@en, "démocratie"@fr, "demokratie"@de ;
    ex:upperCaseLabel "DEMOCRACY"@en, "DÉMOCRATIE"@fr, "DEMOKRATIE"@de .
```

_Note:_ `UCASE("Démocratie"@fr)` _→_ `"DÉMOCRATIE"@fr` _— Unicode case-folding handled correctly by the SPARQL engine._

---

#### ex:Unlabelled

No labels of any kind. **Validation fails. No derived triples produced.**

---

### Step 3 — Full Inferred Graph (Turtle, additions only)

```
@prefix ex: <http://example.org/> .

ex:AncientRome
    ex:label          "Ancient Rome"@en ;
    ex:lowerCaseLabel "ancient rome"@en ;
    ex:upperCaseLabel "ANCIENT ROME"@en .

ex:BlackHole
    ex:label          "Black Hole"@en ;
    ex:lowerCaseLabel "black hole"@en ;
    ex:upperCaseLabel "BLACK HOLE"@en .

ex:Democracy
    ex:label          "Democracy"@en, "Démocratie"@fr, "Demokratie"@de ;
    ex:lowerCaseLabel "democracy"@en, "démocratie"@fr, "demokratie"@de ;
    ex:upperCaseLabel "DEMOCRACY"@en, "DÉMOCRATIE"@fr, "DEMOKRATIE"@de .

ex:NeuralNetwork
    ex:label          "Neural Network"@en ;
    ex:lowerCaseLabel "neural network"@en ;
    ex:upperCaseLabel "NEURAL NETWORK"@en .

ex:QuantumEntanglement
    ex:label          "Quantum Entanglement"@en ;
    ex:lowerCaseLabel "quantum entanglement"@en ;
    ex:upperCaseLabel "QUANTUM ENTANGLEMENT"@en .
```

---

The Flowchart for this is as follows:

[

![](https://substackcdn.com/image/fetch/$s_!qa1s!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb0c0fbe-4e82-4990-857e-c863ed1ea7d6_4466x8192.png)



](https://substackcdn.com/image/fetch/$s_!qa1s!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb0c0fbe-4e82-4990-857e-c863ed1ea7d6_4466x8192.png)

### Engine Note: pyshacl vs TopBraid / Jena

The original design used `ex:RequiresLabelComponent` (a `sh:ConstraintComponent`) with a `sh:SPARQLAskValidator` whose body used `$primaryLabelProp` and `$secondaryLabelProp` parameter substitution. This works correctly on **TopBraid Composer** and **Apache Jena/SHACL** where the spec-compliant parameter substitution mechanism is implemented.

**pyshacl** (≤ 0.26.x) does not substitute component parameter URIs into ASK/SELECT validator bodies, causing every node to be flagged regardless of whether it has a label. The workaround used here is:

- Keep the `ex:RequiresLabelComponent` declaration with its parameters as _metadata only_ (no `sh:validator` on the component).
    
- Add a concrete `sh:sparql` / `sh:SPARQLConstraint` directly on the shape with the predicates hardcoded. This is the active enforcer in pyshacl.
    
- On a full SHACL 1.2 engine, the component validator takes over and the hardcoded `sh:sparql` block can be removed, making the shape fully generic.
    

## Summary

This is the heart of a transformation:

- first, **identify** those nodes that satisfy a given pattern or shape (here, a node that has some kind of title), which is handled by the constraint part of the shape.
    
- Once you have these nodes, **determine** the labels by looking at a cascading selection of possibilities - rdfs:label, skos:prefLabel, skosxl:prefLabel/skosxl:literalForm
    
- Finally, use these to **construct** three distinct label fields, a direct transcription, then a matching upper and lower case conversion.
    

This is a fairly simple one-pass transformation. I’ll be covering more complex scenarios (where the first pass generated content that may then be used to feed additional transformations) in a subsequent post.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!kZQT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc16e34c7-c81c-4fb5-bbf0-587752bbdde3_2048x2048.jpeg)



](https://substackcdn.com/image/fetch/$s_!kZQT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc16e34c7-c81c-4fb5-bbf0-587752bbdde3_2048x2048.jpeg)

You have to watch out for the books around here. They like to take flight.

[Kurt Cagle](https://linkedin.com/in/kurtcagle)  
[The Ontologist](https://ontologist.substack.com/)

