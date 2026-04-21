---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Down-the-RDFS-Rabbit-Hole-by-Kurt
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:00.700161+00:00'
  title: Down The Rdfs Rabbit Hole By Kurt
  type: plain-doc
  version: '0.1'
---

# Down The Rdfs Rabbit Hole By Kurt

[

![](https://substackcdn.com/image/fetch/$s_!DGny!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F355bb577-8631-489c-a9f2-95c33851fc28_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!DGny!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F355bb577-8631-489c-a9f2-95c33851fc28_2688x1536.jpeg)

I’ve been exploring the implications of three distinct aspects of RDF 1.2 - reification, SHACL, and the core RDFS properties of `rdfs:subClassOf` and `rdfs:subPropertyOf`, and have found that the notion of subclassing properties leads down a very interesting rabbit hole. How these tie in is a richer question than the `rdfs:subClassOf` case because properties have additional dimensions — domain, range, cardinality, and path behaviour — that interact with both SHACL shapes and RDF-Star annotations in distinct ways.

The Core Problem With `rdfs:subPropertyOf` is that `rdfs:subPropertyOf` under RDFS entailment means that if

then every `ex:hasFather` triple entails a corresponding `ex:hasParent` triple. This is a **triple-generating inference** (Edit: as does rdfs:subClassOf, something I mistated earlier). The implications for SHACL are significant because SHACL operates on the asserted graph, not the inferred graph, unless inference is explicitly enabled.

_Note: The following gets a bit hairy code-wise, and goes into more depth than I normally do, but the implications are important, because sub-property inheritance actually lies at the heart of how the semantic web works, especially with RDF 1.2. This article should be seen as a continuation of my previous article_

[

## Lions and Tigers and Bears, Oh My!

](https://ontologist.substack.com/p/lions-and-tigers-and-bears-oh-my)

·

Feb 26

[![Lions and Tigers and Bears, Oh My!](https://substackcdn.com/image/fetch/$s_!9iji!,w_1300,h_650,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd44dbbe0-e215-47b1-90a0-776d896c758c_2688x1536.jpeg)](https://ontologist.substack.com/p/lions-and-tigers-and-bears-oh-my)

The Shape Constraint Language (SHACL) represents a significant shift in how graphs are specified and modelled. It makes a few very big, fundamental assumptions, not least that classes are no longer primary objects. This can be a real challenge if your first exposure to ontologies came from the use of classes in Protege. This is not to say that you can’t…

## What SHACL 1.2 Adds for Property Inheritance

**Property shape inheritance through sh:and** works the same way as for node shapes, but the target is now a property shape rather than a node shape:

```
# Abstract — base property constraint bundle
ex:hasParentConstraints a sh:PropertyShape ;
    sh:path ex:hasParent ;
    sh:nodeKind sh:IRI ;
    sh:minCount 1 ;
    sh:maxCount 2 ;
    sh:message "hasParent must reference 1-2 IRI nodes." .

# Specialised — narrows the base constraint
ex:hasFatherConstraints a sh:PropertyShape ;
    sh:and ( ex:hasParentConstraints ) ;
    sh:path ex:hasFather ;
    sh:qualifiedValueShape ex:MalePersonShape ;
    sh:qualifiedMinCount 1 ;
    sh:message "hasFather object must conform to MalePersonShape." .
```

The `sh:and` composition here carries the cardinality and nodeKind constraints from the parent property shape down to the child. Crucially, this is **constraint inheritance only** — it does not generate `ex:hasParent` triples from `ex:hasFather` assertions, which is what RDFS would do. Whether that gap matters depends on whether your pipeline needs the entailed triples or just the validation behaviour.

`sh:path` **expression specialisation** is where SHACL 1.2 node expressions become genuinely powerful for property hierarchies. You can express that a specialised property must satisfy the same constraints as its parent by reference to a path expression target:

```
ex:ParentPropertyShape a sh:NodeShape ;
    sh:target [
        a sh:SPARQLTarget ;
        sh:select """
            SELECT ?this WHERE {
                ?this ex:hasFather|ex:hasMother ?parent .
            }
        """
    ] ;
    sh:property [
        sh:path ex:hasFather|ex:hasMother ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1
    ] .
```

The `|` alternative path acts as a union across the property hierarchy without needing RDFS to materialise `ex:hasParent` triples. This is the SHACL-native substitute for subproperty entailment in validation contexts.

**Inverse and path-based subproperty expression** is new territory in SHACL 1.2. The path expression algebra now supports enough operators that you can express complex property hierarchy relationships directly:

```
# A node shape validating that anything reachable via hasFather
# or hasMother satisfies the same constraints as hasParent
ex:ParentReachabilityShape a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:property [
        sh:path [ sh:alternativePath ( ex:hasFather ex:hasMother ) ] ;
        sh:node ex:PersonShape ;
        sh:nodeKind sh:IRI
    ] .
```

## RDF-Star Annotations on rdfs:subPropertyOf

This is where the design space opens up significantly. Just as with `rdfs:subClassOf`, you can now annotate the subproperty assertion itself:

```
ex:hasFather rdfs:subPropertyOf ex:hasParent
    {| ex:constrainedBy ex:hasFatherConstraints ;
       ex:inverseConstrainedBy ex:hasFatherInverseConstraints ;
       sh:severity sh:Warning ;
       ex:entailmentRequired true ;
       dcterms:description "hasFather specialises hasParent; 
                             entailment must be materialised 
                             before SHACL validation." ;
       prov:wasAttributedTo ex:KurtCagle ;
       dcterms:modified "2026-01-15"^^xsd:date |} .
```

Several annotation predicates are specifically meaningful for property hierarchies that weren’t relevant for class hierarchies:

`ex:entailmentRequired` flags that a SPARQL CONSTRUCT or inference step must be run before validation — because SHACL won’t generate the `ex:hasParent` triples from `ex:hasFather` assertions automatically. This is metadata your pipeline can query to decide whether to run a pre-validation materialisation step.

`ex:inverseConstrainedBy` captures constraints on the inverse direction — particularly useful for symmetric or functional properties where the subproperty relationship has constraint implications in both directions.

`sh:severity` on the annotation expresses that violations of the constraint attached to this subproperty step should carry a specific severity, which your shape generator can propagate into the emitted `sh:PropertyShape`.

## The Entailment Gap Problem

The most important implication — and the most underappreciated — is that SHACL’s closed-world validation and RDFS subproperty entailment pull in opposite directions. Consider:

```
# Data
ex:alice ex:hasFather ex:bob .

# Ontology
ex:hasFather rdfs:subPropertyOf ex:hasParent .

# Shape
ex:PersonShape a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:property [
        sh:path ex:hasParent ;
        sh:minCount 1 ;
        sh:message "Every person must have a hasParent assertion."
    ] .
```

Under RDFS inference, `ex:alice ex:hasParent ex:bob` is entailed and the shape passes. Without inference — which is the default in `pyshacl` with `inference="none"` — the shape fails because the `ex:hasParent` triple is not asserted. This is the entailment gap, and it’s a structural tension that RDF-Star annotations can help manage but cannot eliminate.

The annotation-driven approach allows you to encode which properties require materialisation explicitly:

```
# Pre-validation materialisation query — generated from annotations
CONSTRUCT {
    ?s ex:hasParent ?o .
}
WHERE {
    << ex:hasFather rdfs:subPropertyOf ex:hasParent >>
        ex:entailmentRequired true .
    ?s ex:hasFather ?o .
}
```

Your pipeline queries the ontology for all `rdfs:subPropertyOf` triples annotated with `ex:entailmentRequired true`, generates the corresponding CONSTRUCT queries, materialises the entailed triples into the data graph, and then runs SHACL validation. The annotation makes the pipeline’s pre-processing requirements self-describing.

## Property Chain Axioms (owl:propertyChainAxiom)

`rdfs:subPropertyOf` in OWL also supports property chain axioms — `ex:hasGrandfather owl:propertyChainAxiom (ex:hasFather ex:hasFather)` — which have no direct equivalent in SHACL. With RDF-Star you can annotate these too:

```
ex:hasGrandfather rdfs:subPropertyOf ex:hasAncestor
    {| ex:chainAxiom ( ex:hasFather ex:hasFather ) ;
       ex:constrainedBy ex:hasGrandfatherConstraints ;
       ex:entailmentRequired true ;
       ex:materialiseWith ex:GrandfatherChainQuery |} .
```

The `ex:materialiseWith` annotation references a named SPARQL CONSTRUCT query stored elsewhere in the graph, which your pipeline retrieves and executes before validation. The annotation on the subproperty triple becomes a complete operational specification of what the pipeline needs to do to close the entailment gap before handing off to SHACL.

## Symmetric and Functional Properties

These interact with SHACL 1.2 path expressions in ways worth calling out explicitly. For a symmetric property:

```
ex:isMarriedTo rdfs:subPropertyOf ex:isRelatedTo
    {| ex:symmetric true ;
       ex:constrainedBy ex:isMarriedToConstraints |} .
```

The annotation `ex:symmetric true` can drive generation of a bidirectional SPARQL target in the shapes graph:

```
ex:isMarriedToShape a sh:NodeShape ;
    sh:target [
        a sh:SPARQLTarget ;
        sh:select """
            SELECT ?this WHERE {
                { ?this ex:isMarriedTo ?x }
                UNION
                { ?x ex:isMarriedTo ?this }
            }
        """
    ] ;
    sh:node ex:isMarriedToConstraints .
```

For a functional property — where `sh:maxCount 1` is the constraint — the annotation can flag that the constraint should be applied in both directions if the property is also inverse functional:

```
ex:hasBiologicalMother rdfs:subPropertyOf ex:hasMother
    {| ex:functional true ;
       ex:inverseFunctional true ;
       ex:constrainedBy ex:hasBiologicalMotherConstraints |} .
```

## The Resulting Architecture

The full picture for property hierarchy management in a SHACL 1.2 / RDF-Star pipeline looks like this:

```
rdfs:subPropertyOf triple
    ↓ annotated with
RDF-Star annotation block
    {| ex:constrainedBy       → constraint shape IRI
       ex:entailmentRequired  → boolean flag
       ex:materialiseWith     → CONSTRUCT query reference
       ex:symmetric           → boolean
       ex:functional          → boolean
       sh:severity            → severity IRI |}
    ↓ drives
Pipeline pre-processing
    → materialise entailed triples via CONSTRUCT
    → generate targeted property shapes from annotations
    ↓ feeds
SHACL validator
    → closed-world validation on materialised + asserted graph
    → property shape inheritance via sh:and chains
    → alternative path expressions substituting for subproperty union
```

The key architectural conclusion is that `rdfs:subPropertyOf` sits at the intersection of two fundamentally different semantic regimes — open-world RDFS entailment and closed-world SHACL validation — and RDF-Star annotations are the mechanism that makes the boundary between those regimes explicit, queryable, and operationally manageable without collapsing either regime into the other.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!vmRZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6815dc1-707d-4c4d-9b4d-da39bb92725d_2048x2048.jpeg)

](https://substackcdn.com/image/fetch/$s_!vmRZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6815dc1-707d-4c4d-9b4d-da39bb92725d_2048x2048.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

If you like these articles, please consider becoming a paid subscriber. It helps support me so that I can continue writing code, in-depth analyses, educational pieces, and more.

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.

