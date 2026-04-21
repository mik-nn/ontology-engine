---
type: article
title: Без названия
source: https://substack.com/@kurtcagle/p-190256594
created: 2026-03-08
tags:
  - article
---

# A Library Task in SHACL

Источник: https://substack.com/@kurtcagle/p-190256594

---

Mar 08, 2026

---

[

![](https://substackcdn.com/image/fetch/$s_!8xuU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bc049d4-115e-4ae0-a972-8dea410ee188_2688x1536.jpeg)



](https://substackcdn.com/image/fetch/$s_!8xuU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bc049d4-115e-4ae0-a972-8dea410ee188_2688x1536.jpeg)

With apologies to both pTerry and Philip Pullman.

Imagine you’re running a library. Every book in the library _must_ have a title — you can’t catalogue something that has no name. But your library has inherited books from several different collections, and they don’t all use the same convention for recording titles. Some use a sticker on the spine labelled **“Title:”**, others use a card in the front pocket labelled **“Preferred Name:”**, and a few older volumes have a fancy illuminated plate with the title written in a special calligraphic script.

This SHACL piece does two jobs: it acts as both a **librarian inspector** and a **label printer**.

---

### The Inspector (the Constraint Component)

The inspector walks through every book and asks: _does this book have a title I can find, in any of the three conventions?_ If it finds none — no spine sticker, no pocket card, no illuminated plate — it raises a complaint: _“Book at shelf location X is missing any recognizable title.”_

What makes this reusable is that the inspector doesn’t hardwire which label conventions it checks. You hand it a slip of paper saying _“for this collection, the primary convention is the spine sticker, and the fallback is the pocket card.”_ A different collection could hand it different instructions, and the same inspector handles both. That’s what the `primaryLabelProp` and `secondaryLabelProp` parameters do — they’re the instructions you hand to the inspector.

The illuminated plate (SKOS-XL) is always checked as a last resort regardless, because it’s structurally more complex — the title isn’t written directly on the book but on a separate decorative page that the book points to. The inspector knows to follow that pointer.

### Building The Custom Constraint Component

A `sh:ConstraintComponent` needs: declared parameters, and a validator (SPARQL SELECT or ASK). The key subtlety is that any shape which uses a property matching a component’s `sh:parameter/sh:path` automatically invokes the component — that’s how SHACL components compose into shapes.

```
@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:     <http://example.org/> .

# ── Shared prefix declarations (reused by validators and rules) ──────────────

ex:CommonPrefixes a sh:PrefixDeclaration ;
    sh:declare
        [ sh:prefix "rdfs"   ; sh:namespace "http://www.w3.org/2000/01/rdf-schema#"^^xsd:anyURI ],
        [ sh:prefix "skos"   ; sh:namespace "http://www.w3.org/2004/02/skos/core#"^^xsd:anyURI ],
        [ sh:prefix "skosxl" ; sh:namespace "http://www.w3.org/2008/05/skos-xl#"^^xsd:anyURI ],
        [ sh:prefix "ex"     ; sh:namespace "http://example.org/"^^xsd:anyURI ] .


# ── Constraint Component ─────────────────────────────────────────────────────
#
#  Validates that a node carries at least one of two configurable label
#  properties (defaults: rdfs:label, skos:prefLabel).  SKOS-XL is also
#  checked unconditionally as a third fallback inside the validator.

ex:RequiresLabelComponent a sh:ConstraintComponent ;
    rdfs:label "Requires Label Component" ;
    rdfs:comment """Constraint that fires when a node has neither a primary
                    nor a secondary label property (nor a SKOS-XL literalForm).""" ;

    sh:parameter [
        sh:path        ex:primaryLabelProp ;
        sh:nodeKind    sh:IRI ;
        sh:optional    true ;
        sh:defaultValue rdfs:label ;
        sh:description "Primary label predicate to require (default: rdfs:label)" ;
    ] ;

    sh:parameter [
        sh:path        ex:secondaryLabelProp ;
        sh:nodeKind    sh:IRI ;
        sh:optional    true ;
        sh:defaultValue skos:prefLabel ;
        sh:description "Fallback label predicate to require (default: skos:prefLabel)" ;
    ] ;

    sh:validator ex:RequiresLabelSelectValidator .


ex:RequiresLabelSelectValidator a sh:SPARQLSelectValidator ;
    sh:message "Node <{$this}> must carry at least one of: {$primaryLabelProp}, \
                {$secondaryLabelProp}, or a skosxl:prefLabel/skosxl:literalForm." ;
    sh:prefixes ex:CommonPrefixes ;
    sh:select """
        SELECT $this ?path ?value
        WHERE {
            # Violation fires when ALL three paths are absent
            FILTER NOT EXISTS { $this $primaryLabelProp   ?v1 }
            FILTER NOT EXISTS { $this $secondaryLabelProp ?v2 }
            FILTER NOT EXISTS {
                $this skosxl:prefLabel ?xlNode .
                ?xlNode skosxl:literalForm ?v3 .
            }
            # Bind a representative path for the validation report
            BIND( $primaryLabelProp AS ?path )
        }
    """ .
```

---

### The Label Printer (the Rules)

Once we’re confident a book has _some_ kind of title, we want to stamp three standardized labels onto every book so that any downstream system — a card catalog, a website, a mobile app — can grab a label without knowing which original convention the title came from.

The label printer resolves the title once using a strict preference order (_spine sticker first, pocket card second, illuminated plate last_) and then stamps:

- `ex:label` — the title exactly as found, just re-stamped in a single known location
    
- `ex:lowerCaseLabel` — the title in all lowercase, useful for search and sorting
    
- `ex:upperCaseLabel` — the title in all caps, useful for display headings or signage
    

All three stamps happen independently and in parallel — none of them waits for another to finish, because they’re all drawing from the same original source rather than from each other’s output.

### The Node Shape: Wiring the Component and Attaching Rules

Shapes invoke the component simply by using its parameter predicates as properties:

```
ex:LabelledResourceShape a sh:NodeShape ;
    sh:targetClass ex:LabelledResource ;          # or sh:targetSubjectsOf, etc.

    # ── Invoke the constraint component ──
    ex:primaryLabelProp   rdfs:label ;
    ex:secondaryLabelProp skos:prefLabel ;

    # ── Attach the three inference rules ──
    sh:rule ex:CanonicalLabelRule,
            ex:LowerCaseLabelRule,
            ex:UpperCaseLabelRule .
```

### The Three SPARQL Rules

All three share the same priority-ordered COALESCE pattern for label resolution.

```
# ── Rule 1: ex:label  (canonical, priority-ordered echo) ────────────────────

ex:CanonicalLabelRule a sh:SPARQLRule ;
    rdfs:label "Canonical label rule" ;
    rdfs:comment """Derives ex:label preferring rdfs:label, then skos:prefLabel,
                    then skosxl:prefLabel/skosxl:literalForm.""" ;
    sh:prefixes ex:CommonPrefixes ;
    sh:construct """
        CONSTRUCT { $this ex:label ?canonLabel }
        WHERE {
            OPTIONAL { $this rdfs:label        ?rdfsLabel }
            OPTIONAL { $this skos:prefLabel    ?skosLabel }
            OPTIONAL {
                $this skosxl:prefLabel ?xlNode .
                ?xlNode skosxl:literalForm ?xlLabel .
            }
            BIND( COALESCE(?rdfsLabel, ?skosLabel, ?xlLabel) AS ?canonLabel )
            FILTER( BOUND(?canonLabel) )
        }
    """ .


# ── Rule 2: ex:lowerCaseLabel ────────────────────────────────────────────────

ex:LowerCaseLabelRule a sh:SPARQLRule ;
    rdfs:label "Lower-case label rule" ;
    rdfs:comment "Derives ex:lowerCaseLabel from the canonical label source." ;
    sh:prefixes ex:CommonPrefixes ;
    sh:construct """
        CONSTRUCT { $this ex:lowerCaseLabel ?lower }
        WHERE {
            OPTIONAL { $this rdfs:label        ?rdfsLabel }
            OPTIONAL { $this skos:prefLabel    ?skosLabel }
            OPTIONAL {
                $this skosxl:prefLabel ?xlNode .
                ?xlNode skosxl:literalForm ?xlLabel .
            }
            BIND( COALESCE(?rdfsLabel, ?skosLabel, ?xlLabel) AS ?base )
            FILTER( BOUND(?base) )
            BIND( LCASE(?base) AS ?lower )
        }
    """ .


# ── Rule 3: ex:upperCaseLabel ────────────────────────────────────────────────

ex:UpperCaseLabelRule a sh:SPARQLRule ;
    rdfs:label "Upper-case label rule" ;
    rdfs:comment "Derives ex:upperCaseLabel from the canonical label source." ;
    sh:prefixes ex:CommonPrefixes ;
    sh:construct """
        CONSTRUCT { $this ex:upperCaseLabel ?upper }
        WHERE {
            OPTIONAL { $this rdfs:label        ?rdfsLabel }
            OPTIONAL { $this skos:prefLabel    ?skosLabel }
            OPTIONAL {
                $this skosxl:prefLabel ?xlNode .
                ?xlNode skosxl:literalForm ?xlLabel .
            }
            BIND( COALESCE(?rdfsLabel, ?skosLabel, ?xlLabel) AS ?base )
            FILTER( BOUND(?base) )
            BIND( UCASE(?base) AS ?upper )
        }
    """ .
```

### A Few Design Notes Worth Flagging

**Language tag behaviour** — `LCASE()`/`UCASE()` in SPARQL 1.1 preserve the language tag on a plain literal, so `"Hello World"@en` becomes `"hello world"@en`. That’s usually what you want, but worth being explicit about in any documentation.

**Multiple labels** — if `rdfs:label` has several values (multiple languages, multiple plain strings), `COALESCE` picks whichever SPARQL returns first. If you need deterministic selection (e.g. prefer `@en`), add a `FILTER(LANG(?rdfsLabel) = "en")` block or use a `sh:SPARQLRule` `ORDER BY`/`LIMIT 1` sub-select pattern.

**Rule execution order** — SHACL 1.2 respects `sh:order` on rules. Since all three rules depend on the same source triple (not on each other’s output), they’re independent, and ordering doesn’t matter here. If you later derive `ex:lowerCaseLabel` _from_ `ex:label` rather than independently, add `sh:order 0` on the canonical rule and `sh:order 1` on the case rules.

`sh:defaultValue` **availability** — this is in the SHACL spec but not all engines implement it for component parameters; Jena/TopBraid do, some others don’t. A defensive fallback is to declare the default explicitly in the shape rather than relying on the component default.

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