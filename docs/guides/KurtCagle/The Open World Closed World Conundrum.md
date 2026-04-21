---
type: article
title: The Open World/Closed World Conundrum
source: https://substack.com/@kurtcagle/p-190818401
created: 2026-04-10
tags:
  - article
---

# The Open World/Closed World Conundrum

Источник: https://substack.com/@kurtcagle/p-190818401

---

Mar 14, 2026

---

[

![](https://substackcdn.com/image/fetch/$s_!_qSH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffbdee95-356a-4d55-b3e0-d86fbb454158_2688x1536.jpeg)



](https://substackcdn.com/image/fetch/$s_!_qSH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffbdee95-356a-4d55-b3e0-d86fbb454158_2688x1536.jpeg)

My most recent series about converting from OWL to SHACL has had a lot of feedback and no small amount of pushback - not so much about the feasibility of doing so but rather whether one can or should mix models from what has become one of the defining characteristics of the semantic web: the open world vs. closed world assumption (OWA vs CWA).

It’s worth taking a deeper dive into what exactly the distinction is between the two, in part because I’m coming to believe that this duality masks a considerably more complex problem with model representations in general.

Some definitions:

### The Closed World Assumption

The closed world assumption (CWA) holds that the knowledge base is complete: if a statement cannot be proven true from the available information, then it is false. Absence of evidence is evidence of absence. This is the assumption that underlies virtually every relational database ever built. If you query a PostgreSQL table for employees with the title “VP of Engineering” and the query returns no rows, the system treats that as a definitive answer — the person doesn’t hold that title, full stop. The database is assumed to contain everything relevant to the question; gaps in the data are gaps in reality, not gaps in knowledge.

This assumption makes databases tractable for operational use. Constraints can be enforced without qualification. A NOT NULL constraint means the column must have a value, not that the value might exist somewhere outside the database’s current view. A UNIQUE constraint means no two rows share a value in this table, period. The system doesn’t hedge. It doesn’t say “no duplicate values are recorded here, but duplicates might exist in some as-yet-unintegrated dataset.” The world described by the database is taken to be the whole world relevant to the query.

Most practical software systems implicitly adopt the CWA whether they acknowledge it or not. When an e-commerce platform determines that a product is out of stock because inventory_count = 0, it is not entertaining the philosophical possibility that stock might exist somewhere unrecorded. When a hospital information system returns no allergy records for a patient, clinicians cannot safely treat that as “allergies unknown” — the system’s CWA design requires that the absence means no allergies on record, with all the care protocols that implies.

### The Open World Assumption

The open world assumption (OWA) holds that the knowledge base is explicitly incomplete: if a statement cannot be proven true, the correct conclusion is not that it is false, but that its truth value is unknown. Absence of evidence is merely the absence of evidence. The world extends beyond what has been captured, and any given knowledge base represents a partial, provisional view of a larger reality.

This is the foundational assumption of OWL and the wider Description Logic tradition from which it descends. An OWL ontology describing the class `Person` with a property `hasBirthplace` does not conclude that a particular person has no birthplace simply because none is asserted. The reasoner infers that the birthplace is unknown, not absent. This makes OWL reasoners correct in a particular philosophical sense — they will not draw conclusions that outrun their evidence — but it makes them frustrating for engineers who want to enforce constraints.

The OWA was deliberately chosen for the Semantic Web. Tim Berners-Lee’s original vision was a web of interlinked data contributed by many independent parties, where no single source could ever claim to be complete. A knowledge graph about scientific publications shouldn’t conclude that a researcher has no co-authors just because the current dataset lacks co-authorship triples — those facts might exist in a dozen other datasets that haven’t been integrated yet. The OWA is the epistemically honest stance for a distributed, federated knowledge environment where completeness is structurally impossible.

### Why the Distinction Matters for Graph-Based Systems

The tension between these assumptions is a source of significant confusion and engineering friction in semantic technology stacks, because the dominant tooling combines both — often without clearly declaring which assumption governs each operation.

RDF and OWL operate under the OWA. SPARQL, when used for data retrieval against a known dataset, is typically operated by users under implicit CWA expectations — if the query returns nothing, practitioners treat it as “not in the graph,” not as “unknown.” SHACL introduces explicit constraint enforcement that presupposes closure over the graph being validated — a `sh:minCount 1` constraint fails when no values are present, which is a CWA judgment. It does not produce a third result, meaning “values might exist but are unrecorded.” The moment SHACL rules begin generating new triples that feed back into subsequent validation, the question of which assumption governs the combined system becomes genuinely difficult to answer, because the graph is no longer a fixed object being inspected but a changing surface being written to by the same machinery that is meant to validate it.

A workable heuristic for practitioners is this: use the OWA when modelling the _domain_ — what kinds of things exist, how they relate, what properties they may have — because the domain genuinely extends beyond any given dataset. Use the CWA when modelling _operations_ — what the pipeline requires, what constraints must hold for a record to be processed, what constitutes a valid fact for publication — because operational correctness demands closure. The problem is that OWL was designed for the former and is routinely pressed into service for the latter, while SHACL was designed to enforce the latter but operates on graphs whose primary semantics remain governed by the former. The seam between them is where indeterminacy lives, and it is where most non-trivial semantic modelling problems eventually surface.

## Fundamental Dissonances

Note that this is NOT an RDF problem; it is a knowledge representation problem with implications in a number of areas. As the RDF 1.2 stack becomes more heavily baked, the implications of this particular problem are beginning to percolate up from the depths in a number of key areas:

### The Move Towards Closed Models

The generation of triples in order to “make good” on logical assertions from rule-based systems raises the question of what exactly is a graph, when that graph is dynamic. OWL generates an internal entailment graph that is queryable, but raises the question about whether the union of the source graph + entailment graph (each of which is a de facto named graph) is really the same thing as the pre-entailment source graph. OWA says yes, CWA says no.

This gets back to a dissonance in the nature of graphs themselves. Named graphs were not part of the original concept for the Semantic Web, but began to be utilised by the publication of SPARQL 1.0 in 2007 (and were discussed earlier). As originally envisioned, the semantic web was seen as a single vast graph, which was part of how the Open World Assumption first came to be. The idea of global identifiers arose from this notion, though even here, there were signs of things to come with blank nodes, which were effectively local identifiers that existed primarily to handle certain common use cases, most immediately being linked lists.

Since then, there has been a slow but inexorable move toward closed world systems in RDF. SPARQL did not assume a reasoner in the mix - it worked on the graph as presented, and it had the tools to handle problematic constructs such as transitive closures, utilising property paths. Named graphs constrained data sets, making it easier to partition them, and SPARQL and SPARQL UPDATE support in version 1.1 added named graph support, and moreover, reducing the dependency upon materialised triples. SHACL was a closed-world schematic language that built on SPARQL, with SHACL 1.2 only strengthening this.

Finally, Generative AI solutions are moving toward graphs (and subordinate representations) that presume closed-world assumptions - Agentic AI architectures talk to programmatic endpoints rather than exposing SPARQL capabilities directly, in part in response to security concerns, in part due to limited familiarity of SPARQL to the typical programmer (especially when dealing with unknown schematic and taxonomic elements), and in part because generating SPARQL from SHACL is best done within a secured pipeline.

### **Hypergraph Structures and Reifications**

When you annotate an assertion (reify it), you are, in essence, establishing a context for the validity of that assertion that is no longer truly binary. If an annotation is contextual, then should the base assertion be considered true, false, or “it depends”? If an assertion is made only through reification - I create a contention (a reification statement) but do not specifically introduce this contention into the graph (don’t make it explicitly indexable), then does it participate in the logic of the graph?

_This is an issue that has actually consumed several years’ worth of discussion within the RDF-Star working group, due to the fundamental dissonance between open and closed models._

I’m convinced that reification is the future of RDF, but OWL predates any significant reification layer by a couple of decades, while the closed-world SHACL (1.2) has built-in support for reification. While this becomes a tooling issue to a certain extent, any classical OWL representation will end up losing a lot of the expressiveness of RDF-Star capabilities and notation. So, even though reification is somewhat orthogonal to the open-world/closed-world argument, the reality is that OWL will need to be revised significantly to provide that support (notationally, if nothing else), which gives SHACL (and implicitly the CWA) the edge in adoption.

### **Indeterminacy and Trivalent Logic.**

SQL has a fairly primitive trivalent logical system: it recognises TRUE, FALSE, and NULL, where NULL can be taken as a proxy for _Indeterminate_ (this echoes the previous point, of course). SPARQL has a form of trivalent logic in that you can use the BOUND() function with a variable that has the value `false` if the variable is undefined (though this requires an OPTIONAL keyword:

```
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <https://example.org/ns#> .
@prefix sh:   <http://www.w3.org/ns/shacl#> .
```

---

#### Part 1 — The Data Graph

Three engineers with different states of the `ex:yearsExperience` property: one known, one explicitly null-signalled via a sentinel, one simply absent.

```
ex:alice a ex:Engineer ;
    rdfs:label "Alice" ;
    ex:yearsExperience 10 .          # known — 10 years

ex:bob a ex:Engineer ;
    rdfs:label "Bob" ;
    ex:yearsExperience 0 .           # ambiguous: genuinely 0, or "not recorded"?
                                     # the graph cannot distinguish these

ex:carol a ex:Engineer ;
    rdfs:label "Carol" .             # absent entirely — no yearsExperience triple
                                     # under OWA this is indeterminate, not false
```

---

#### Part 2 — SPARQL: trivalence emerges at FILTER

SPARQL’s `FILTER` evaluates to **true**, **false**, or **error**.  
The spec (§17.2) mandates that `error` is treated identically to `false` at the row-elimination boundary — silently dropping the row rather than surfacing indeterminacy.

```
PREFIX ex:  <https://example.org/ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?engineer ?label ?years ?verdict
WHERE {
    ?engineer a ex:Engineer .
    OPTIONAL { ?engineer rdfs:label      ?label }
    OPTIONAL { ?engineer ex:yearsExperience ?years }

    # FILTER operates in three-valued Kleene logic internally:
    #   ?years >= 8   → true  (alice: included)
    #   ?years >= 8   → false (bob:   excluded, 0 < 8)
    #   ?years >= 8   → error (carol: ?years unbound → numeric comparison
    #                          evaluates to error → treated as false → row dropped)
    #
    # Carol disappears silently.  The query cannot distinguish
    # "carol has < 8 years" from "carol's experience is unknown."

    BIND(
        IF( !BOUND(?years),          "indeterminate",
        IF( ?years >= 8,             "senior",
                                     "junior" ))
    AS ?verdict )

    # Restore Carol by moving the filter into the BIND, not into FILTER.
    # Without the BIND trick, FILTER NOT EXISTS is the only other escape hatch:
    #   ... FILTER( BOUND(?years) && ?years >= 8 )
    # — but that still silently excludes unbound rows rather than flagging them.
}
ORDER BY ?engineer
```

[

![](https://substackcdn.com/image/fetch/$s_!loxk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd09c6353-a79a-4374-b825-977cdb76ed83_739x217.png)



](https://substackcdn.com/image/fetch/$s_!loxk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd09c6353-a79a-4374-b825-977cdb76ed83_739x217.png)

The `BIND/IF/BOUND` Pattern is the standard SPARQL workaround for surfacing the third value, but it requires deliberate authoring. A plain `FILTER(?years >= 8)` would return only Alice, with Carol’s indeterminate state entirely invisible to the query consumer.

---

#### Part 3 — SHACL 1.2 Node Shape with `sh:sparql`

SHACL’s own binary result model (`sh:conforms true/false`) cannot natively represent indeterminacy. The shape below uses `sh:sparql` with a `SELECT` that explicitly projects a `?logicState` column carrying the three-valued result, then uses `sh:message` templating to surface it in the validation report — making the indeterminate case visible rather than collapsing it to a violation or a pass.

```
ex:EngineerSeniorityShape
    a sh:NodeShape ;
    sh:targetClass ex:Engineer ;
    rdfs:label "Engineer Seniority — Trivalent Assessment"@en ;
    rdfs:comment """
        Demonstrates trivalent logic within a SHACL 1.2 sh:sparql constraint.
        Outcome for each focus node:
          TRUE          — yearsExperience is bound and >= 8   → no violation raised
          FALSE         — yearsExperience is bound and < 8    → sh:Violation
          INDETERMINATE — yearsExperience is absent entirely  → sh:Warning
        The third state is made explicit rather than silently collapsing to FALSE.
    """@en ;

    sh:sparql [
        a sh:SPARQLConstraint ;
        rdfs:label "Trivalent seniority check"@en ;

        sh:message """Seniority logic state for {?label}: {?logicState}. \
Value: {?years}. \
INDETERMINATE means yearsExperience is absent — cannot determine seniority \
under OWA; assert the property or close the world explicitly."""@en ;

        sh:severity sh:Warning ;       # shapes engine sees all non-TRUE rows;
                                       # severity is overridden per-row in message
                                       # (SHACL 1.2 does not support per-row
                                       #  severity from SELECT — use message text)

        sh:select """
            PREFIX ex:   <https://example.org/ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

            SELECT $this ?label ?years ?logicState
            WHERE {
                $this a ex:Engineer .
                OPTIONAL { $this rdfs:label          ?label }
                OPTIONAL { $this ex:yearsExperience  ?years }

                # Three-valued evaluation via BIND/IF/BOUND.
                # FILTER(?years >= 8) would silently drop the unbound row;
                # instead we project the logic state and let the shapes engine
                # decide what to surface.
                BIND(
                    IF( !BOUND(?years),
                        "INDETERMINATE"^^xsd:string ,
                    IF( ?years >= 8 ,
                        "TRUE"^^xsd:string ,
                        "FALSE"^^xsd:string ))
                AS ?logicState )

                # Return only the non-TRUE rows so SHACL treats them as violations/warnings.
                # TRUE rows produce no binding here → no constraint result → implicit pass.
                FILTER( ?logicState != "TRUE"^^xsd:string )
            }
        """
    ] .
```

---

#### Part 4 — What the Validation Report Looks Like

For the three-node graph above, the shapes engine produces:

```
ex:bob   → logicState=FALSE         → sh:Warning  (severity inherited from shape)
ex:carol → logicState=INDETERMINATE → sh:Warning
ex:alice → (no result row)          → implicit pass
```

`ex:bob` and `ex:carol` both surface, but with semantically distinct messages. Without the `BOUND` guard, `ex:carol` would produce no result row at all — passing silently — because an unbound `?years` in a numeric `FILTER` evaluates to `error`, which SPARQL downcasts to `false`, which causes the row to be dropped before the shapes engine ever sees it.

---

[

![](https://substackcdn.com/image/fetch/$s_!sJ4M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd724287-62d3-49e1-831c-4d97349e437c_720x365.png)



](https://substackcdn.com/image/fetch/$s_!sJ4M!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd724287-62d3-49e1-831c-4d97349e437c_720x365.png)

The practical implication is that both SPARQL and SHACL require deliberate, non-default authoring to avoid silently collapsing `INDETERMINATE` into `FALSE` — which is exactly the closed-world assumption re-entering through the implementation back-door, even when the data model is formally open-world.

On the other hand - and I believe this is significant - short of completely re-engineering SHACL to handle trivalence, this is probably the best path forward to being able to handle indeterminancy. In many respects, SHACL has tended to take a more pragmatic approach to modelling than OWL has, so that, even though it is a CWA solution, it can, at a minimum, handle the core requirement of validation, even in the presence of indeterminacy.

## Entailment vs. SHACL Rules and SPARQL Update

SPARQL changed the entailment debate with the introduction of property paths, which reduced (though didn’t fully eliminate) the requirement that you needed to create entailment triples in order to perform reasoning. You could compute transitive closures with a couple of lines of SPARQL, rather than fully materialising all possible entailed triples.

Similarly, symmetric relationships such as `owl:sameAs` could be readily encompassed with a simple query:

```
CONSTRUCT {
    ?s ?p ?o .
    ?t ?p ?o .
}
WHERE {
    # Transitive + symmetric closure via property path
    ?s (owl:sameAs | ^owl:sameAs)+ ?t .

    # Guard: no self-loops, no blank nodes
    FILTER(?s != ?t)
    FILTER(isIRI(?s) && isIRI(?t))

    # Collect triples from either node
    { ?s ?p ?o }
    UNION
    { ?t ?p ?o }
}
```

This involves a certain number of trade-offs; for a small number of owl:sameAs relationships, materialised triples are probably faster, but because owl:sameAs materialisation grows as O(n²) (I believe), the overall memory overhead makes SPARQL much more efficient for large n. As master-data-management (MDM) is fairly critically dependent upon such owl:sameAs operations, this has shifted utilisation away from materialisation and towards property paths, which arguably favour CWA dynamics.

This carries over to SHACL, which can be thought of as the compartmentalisation of SPARQL. SHACL works using a combination of three factors: a node shape that identifies the focus nodes under consideration, constraint shapes (including property shapes) that establish how aspects of the graph related to each focus node are shaped, and one or more rules that indicate what triples are added to a named graph when a particular focus node is selected. All three use SPARQL in the background.

This triple dependency on SPARQL creates an interesting situation, precisely because SPARQL operates on the graph, that is, on one or more specific named graphs. This could be a data graph. It could be some external graph. It could even work upon the same graph that houses the SHACL itself, meaning that a query could use the state of its own shapes as part of the query … _or could mutate that SHACL when invoked in a subsequent iteration_. I will get into self-modifying code in a future post, but there is nothing in SHACL that restricts that use case.

**Note:** Most conformant engines (TopBraid, jena-shacl, pySHACL) _do_ restrict it in practice by freezing the shapes graph before validation, which is reasonable - changing the rules mid-validation defeats the whole purpose of validation.

A SHACL Rule, especially, becomes simply a producer of triples into a named graph. It is, in effect, a modified form of SPARQL UPDATE insert. While there may be implementation-specific limitations, as currently proposed, when a focus node is selected and has a rule, that rule in effect locks down the graph as is, queries the graph to get a feature set (analogous to WHERE in SPARQL), then uses that feature set to generate new triples (analogous to CONSTRUCT or INSERT). This happens only once because it uses the existing selected focus nodes, not newly created ones. _There are no entailment triples, and consequently, this is a closed-world assumption environment._

This does not stop an external process from invoking a new selection of nodes and running the rules on those nodes. Indeed, if you treat the graph as a state machine, this is exactly what happens - each rule invocation changes the state of the graph, which becomes the ground state for any subsequent rule set. If nothing is selected (no shapes are found in the requested configuration), then the state machine stops until a new mutation event occurs.

There’s an important side effect to this. In a SHACL environment, you simply do not need to generate as many triples, which translates into smaller indexes and more efficient processes. In some cases, you can generate those (for instance, if you have a rule that generates `rdfs:subClassOf` relationships, the overhead of those triples is comparatively small (a few hundred triples) compared to the performance benefits involved in having these relationships in the index vs. computing them with a double pass loop in SPARQL. However, in other cases (such as owl:sameAs), the inherent cost of keeping all of those subordinate identities in memory makes using SPARQL paths far more performant.

## Conclusion

I want to be clear: I'm not arguing that Closed World is better than Open World, or the reverse. My point is simpler — that the direction of travel is toward closed-world systems, and that this is being driven from multiple directions at once. Performance pressures, query complexity, and data security concerns are all pushing that way. So are the demands of hypergraph architectures, and the growing need to connect formal graph-based systems with AI and machine learning. Whether or not this shift is philosophically desirable, it appears to be happening regardless.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!LJcW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcfa07df-b395-45a3-9faa-7cd50ea35558_2048x2048.jpeg)



](https://substackcdn.com/image/fetch/$s_!LJcW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcfa07df-b395-45a3-9faa-7cd50ea35558_2048x2048.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)  
[The Ontologist](https://ontologist.substack.com/)
