---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: The-Open-World-Closed-World-Conundrum
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:09.361857+00:00'
  title: The open world closed world conundrum
  type: plain-doc
  version: '0.1'
---

# The open world closed world conundrum

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


