---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: SHACL-Taxonomy-Revisited
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:47.741758+00:00'
  title: Shacl taxonomy revisited
  type: plain-doc
  version: '0.1'
---

# Shacl taxonomy revisited

[

![](https://substackcdn.com/image/fetch/$s_!LrmO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb09f6eb0-1205-4731-8e24-451e4162870e_2688x1536.jpeg)



](https://substackcdn.com/image/fetch/$s_!LrmO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb09f6eb0-1205-4731-8e24-451e4162870e_2688x1536.jpeg)

There was a recent addition to the SHACL 1.2 Core Specification that I think may have a fairly major impact on how we think about taxonomies ... and inheritance. At the same time, a handy little SHACL block may also simplify working with taxonomies.

When people hear the word "ontologies," they tend to think first of the most prevalent use case: organising concepts. Indeed, while OWL tends to get most of the airplay when it comes to ontologies, most of what we call ontologies are, technically speaking, taxonomies built around SKOS.

SKOS - the Simple Knowledge Organisation System, has been around for about twenty-five years now. It was designed primarily to mirror hierarchical taxonomies that involve narrower specificity in some dimension. It’s always had a rather uncomfortable relationship with OWL and RDFS, in that the former tends to focus on conceptual categories, while the latter is usually more oriented towards class inheritance.

What’s the distinction between the two? In theory, one (SKOS) tends to be more semantically oriented, more related to meaning. In practice, I have seen organisations use both interchangeably, or even mix terms so they have both together, typically with the RDFS side having something like e`x:Concept` as a class that can be inherited as an abstraction layer.

## Transitive Closure Hierarchies and Polyhierarchies

I throw the term transitive closure around a lot when discussing taxonomies, but for the most part, the concept is pretty simple. In RDF terms, you often see transitive closures of the form:

```
ex:CatusDomesticis rdfs:subClassOf ex:Felis .
ex:Felis rdfs:subClassOf ex:Felinidae .
ex:Felinidae rdfs:subClassOf ex:Carnivore .
ex:Carnivore rdfs:subClassOf ex:Mammal .
ex:Mammal rdfs:subClassOf ex:Chordate .
ex:Chordate rdfs:subClassOf ex:Animal .
```

In more abstract terms, a transitive relationship looks like:

```
:a1 :p :a2 .
:a2 :p :a3 .
...
a:N-1 :p :aN
```

where each term has the same :p relationship. While there are exceptions (most notably linked lists), transitive relationships usually form lists in one direction (rootward), and trees in the other direction (leafward), and either the instance class or some superclass of the instance class can be found in each of the resources in the closure.

A **closure,** by the way, is the set of some or all nodes that participate in the same chained hierarchy.

When each child (leafward node) has only one parent, the transitive closure is usually known as a **hierarchy**, while if a child can have more than one parent, this becomes known as a **polyhierarchy**. Polyhierarchies can split and rejoin, but they can’t, in general, link back on themselves; that is to say, they are directionally acyclic. A good example of a polyhierarchy is git commit graph, and you can make the argument that a **context graph** or history graph is also polyhierarchical in nature.

In RDFS, the `rdfs:subClassOf` relationship is (almost always) hierarchical in nature- as you move toward the root, the classes become more generalised, until eventually you hit the root, which becomes the top of the (inverted) tree. In most such hierarchies, the root node will be maximally generalised, such as `owl:Thing` or `rdfs:Resource` - it has a minimal set of properties (mostly annotational properties that all subclasses have, such as `rdfs:label.` or `rdf:type.`

## Is owl:Thing a class or an instance?

This is a question that is often asked, and represents one of the more complex fundamental challenges of OWL. The answer is yes, it’s both, and the answer illuminates something fundamental about how OWL handles the metalevel.

**Formally,** `owl:Thing` **is a class.** It is the universal class — the class of which every individual is a member. Every instance of every class is also an instance of `owl:Thing`. It’s the top of the A-Box/T-Box instance hierarchy, the OWL equivalent of `rdfs:Resource` at the RDFS level.

**But it is also an individual** — specifically, it is an instance of `owl:Class`. In OWL’s own type system, `owl:Thing` has the triple `owl:Thing rdf:type owl:Class`. So it is simultaneously a class (something things can be typed as) and an individual (something that is typed as `owl:Class`).

This is not a contradiction — it’s a consequence of OWL operating across multiple metalevels simultaneously. The RDF data model has no inherent restriction on a node being both subject and object of `rdf:type` triples pointing in different directions and at different levels.

**The precise layering:**

```
owl:Class       ← metaclass (instances of this are classes)
    ↑ rdf:type
owl:Thing       ← universal class (instances of this are individuals)
    ↑ rdf:type
ex:Cat          ← domain class
    ↑ rdf:type
ex:Mittens      ← individual
```

Every node in that chain is an _instance_ of the thing above it, and every node except `ex:Mittens` is a _class_ relative to the things below it. `owl:Thing` is a class from below and an instance from above.

**Where it gets vertiginous:** `owl:Class` is itself an instance of `owl:Class`. And `owl:Thing` is a subclass of itself via `rdfs:subClassOf` reflexivity. OWL formally acknowledges these as intended features, not paradoxes, because it operates under the _standard interpretation_ which stratifies the levels carefully enough to avoid genuine contradiction — but only by stipulation, not by any inherent structural barrier in RDF.

**The lay audience version:**

`owl:Thing` is the concept of _thinghood itself_ — the most abstract class imaginable, so abstract that it contains literally everything. But the moment you ask “what kind of thing is `owl:Thing`?”, the answer is “it’s a class” — which means it’s a member of the class of all classes. So it is simultaneously a container and a contained thing, depending on which direction you’re looking from.

It’s the ontological equivalent of the category of all categories — which is itself a category.

**Bringing it back to the SKOS/OWL/SHACL thread:** this is exactly why the box boundaries are design commitments rather than hard structural barriers. The RDF data model doesn’t prevent you from collapsing the levels. OWL’s semantics impose discipline through the interpretation rules, SKOS imposes discipline by convention, and SHACL imposes discipline by explicit constraint — but none of them can fully prevent someone from writing triples that blur the boundaries. The boxes are intellectual commitments enforced by tooling, not physical walls.

## The new `sh:rootClass` in SHACL 1.2

Recently, a new property `sh:rootClass`, was added to SHACL as a constraint. It solves an interesting problem. Let’s say you have a classification taxonomy that looks like the following:

```
ex:Role rdfs:subClassOf ex:Concept .
ex:Manager rdfs:subClassOf ex:Role .
ex:SalesManager rdfs:subClassOf ex:Manager .
ex:TechnicalManager rdfs:subClassOf ex:Manager .
ex:RegionalManager rdfs:subClassOf ex:SalesManager .
ex:AccountManager rdfs:subClassOf ex:SalesManager .
ex:ProgramManager rdfs:subClassOf ex:TechnicalManager .
ex:ProjectManager rdfs:subClassOf ex:TechnicalManager .
ex:Engineer rdfs:subClassOf ex:Role .
ex:Architect rdfs:subClassOf ex:Engineer .
ex:InformationArchitect rdfs:subClassOf ex:Architect .
ex:SystemsArchitect rdfs:subClassOf ex:Architect .
ex:Programmer rdfs:subClassOf ex:Engineer .
ex:Tester rdfs:subClassOf ex:Programmer .
ex:UIUXDeveloper rdfs:subClassOf ex:Programmer .
```

This can be visualised as follows:

[

![](https://substackcdn.com/image/fetch/$s_!nkMt!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc95b26d3-3b31-47c8-bbec-65419c80f533_5802x3280.png)



](https://substackcdn.com/image/fetch/$s_!nkMt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc95b26d3-3b31-47c8-bbec-65419c80f533_5802x3280.png)

This is a typical taxonomy: it’s hierarchical, with each subclass representing a high degree of specificity in job functionality, and, typically, cross-domain items at the same level have roughly the same level of specificity.

Would it be better rendered as SKOS? It doesn’t really matter: SKOS works upon the principle that `skos:broader` indicates a broader scope without necessarily indicating the implementation of that scope, while `rdfs:subClassOf` makes at least the implicit promise that there is an implementation of that scope, but structurally, I could replace `rdfs:subClassOf` with `skos:broader` and get functionally the same chart:

[

![](https://substackcdn.com/image/fetch/$s_!P1cA!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff81e413a-5c93-44d4-84c3-f964b248a708_5320x3280.png)



](https://substackcdn.com/image/fetch/$s_!P1cA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff81e413a-5c93-44d4-84c3-f964b248a708_5320x3280.png)

Put another way - the use of subClassOf (an RDF relationship) vs. `skos:broader` (a SKOS relationship) is largely an idiosyncratic accident of history rather than a functional distinction.

Given the above taxonomy, to specify a property (call it `Shape:Person_engineeringRole`) indicating that the property value should be limited just to Engineer or its descendants, you’d use the following SHACL property shape:

```

ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:property ex:Person_hasEngineeringRole .

ex:Person_hasEngineeringRole
    a sh:PropertyShape ;
    sh:path ex:hasEngineeringRole ;
    sh:rootClass ex:Engineer ;
    sh:message "Value must be ex:Engineer or a subclass thereof." ;
    sh:name "has engineering role" ;
    sh:description "Constrains engineering role assignments to the Engineer subtree." .  

# Valid - ex:SystemsArchitect is a subclass of ex:Engineer
ex:JaneDoe
    a ex:Person ;
    ex:hasEngineeringRole ex:SystemsArchitect .

# Invalid - ex:ProjectManager is a subclass of ex:TechnicalManager,
# not of ex:Engineer
ex:JohnSmith
    a ex:Person ;
    ex:hasEngineeringRole ex:ProjectManager .
```

The engineering roles that are valid according to this are shown in red.

[

![](https://substackcdn.com/image/fetch/$s_!XO-N!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff41c140a-74e9-4fd7-8078-fa688678d9a5_5320x3280.png)



](https://substackcdn.com/image/fetch/$s_!XO-N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff41c140a-74e9-4fd7-8078-fa688678d9a5_5320x3280.png)

Admittedly, this is not a well-designed taxonomy; it is used primarily to illustrate how you can use `sh:rootClass` as a way to easily partition a hierarchy and select from a given node or its descendants. It can also be expressed as a SPARQL constraint:

```
ex:Person_hasEngineeringRole
    a sh:PropertyShape ;
    sh:path ex:hasEngineeringRole ;
    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:message "Value must be ex:Engineer or a subclass thereof." ;
        sh:prefixes ex: ;
        sh:select """
            SELECT $this ?value
            WHERE {
                $this ex:hasEngineeringRole ?value .
                FILTER NOT EXISTS {
                    ?value rdfs:subClassOf* ex:Engineer .
                }
            }
        """ ;
    ] .
```

In this case, the $this parameter indicates the active matching node (here Jane Doe or John Smith) while the value parameter indicates that if the `ex:hasEngineeringRole` property value is not in the transitive closure of `ex:Engineer`, then an error report is fired.

This can be a little confusing if you’re not used to how the sh:sparql constrain works. SHACL’s `sh:select` validator reports **violations** — rows returned by the SELECT are things that _failed_, not things that passed.

So the logic is inverted relative to what you might first reach for. You want to flag values that are _not_ in the engineering subtree, which means you SELECT for the cases where the membership check fails. `FILTER NOT EXISTS` is how you express “there is no evidence that this value belongs” — if the subclass path cannot be walked to `ex:Engineer`, the filter passes and the row is returned, which SHACL interprets as a violation.

## SKOS and SHACL

In recent years, there’s been a move by taxonomists away from building deep hierarchies in SKOS and instead using ConceptSchemes with multiple connected concepts, using the skos:inScheme property. For instance, the above list of roles could be refactored as:

```
ex:RegionManager skos:inScheme ex:ManagerRole, ex:SalesRole .
ex:AccountManager skos:inScheme ex:ManagerRole, ex:SalesRole .
ex:ProgramManager skos:inScheme ex:ManagerRole,ex:TechnicalRole, ex:SalesRole .
ex:ProjectManager skos:inScheme ex:ManagerRole, ex:TechnicalRole .

ex:InformationArchitect skos:inScheme ex:TechnicalRole, ex:ArchitectRole .
ex:SystemsArchitect skos:inScheme ex:TechnicalRole, ex:ArchitectRole .
ex:SolutionsArchitect skos:inScheme ex:TechnicalRole, ex:ArchitectRole .

ex:Programmer skos:inScheme ex:TechnicalRole .
ex:Tester skos:inScheme ex:TechnicalRole .
ex:UIUXDeveloper skos:inScheme ex:TechnicalRole .
```

There are a number of advantages to this approach. First, it allows a way to partition roles into a Venn diagram -

[

![](https://substackcdn.com/image/fetch/$s_!SJBE!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48d23163-2460-4027-a171-e3a1d46545b9_2008x1308.png)



](https://substackcdn.com/image/fetch/$s_!SJBE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48d23163-2460-4027-a171-e3a1d46545b9_2008x1308.png)

You can also create a mapping between the concept schemes and the roles:

[

![](https://substackcdn.com/image/fetch/$s_!rGj6!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3085f50-d0c7-4e0a-abb7-23ec9f65c08f_5773x3955.png)



](https://substackcdn.com/image/fetch/$s_!rGj6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3085f50-d0c7-4e0a-abb7-23ec9f65c08f_5773x3955.png)

This is, in fact, a form of faceting, where the concept schemes are the facets and the concepts are the facet values.

If you are using this form of faceting, then limiting roles to a single particular facet (such as Technical Role, same as Engineering Role above), then the SHACL becomes only a bit more complex:

```
ex:Person_hasTechnicalRole a sh:PropertyShape ;
   sh:path ex:hasTechnicalRole ;
  # all values are Concept from a "Technical Role" scheme
  sh:class skos:Concept ;
  sh:node [
    sh:property [
      sh:path skos:inScheme ;
      sh:hasValue ex:TechnicalRole;
    ] ;
  ] .
```

There are several benefits to this approach:

- Concepts can be in multiple concept schemes simultaneously. This decomposition is closer to how LLMs are trained, and it makes classification easier.
    
- It’s generally faster as you are replacing a costly tree traversal with a linear lookup.
    
- It better fits in with a compositional style of modelling - there’s a clear association between a particular scheme and the property involved.
    
- This creates a clear differentiation between classes and concepts - classes provide inheritance, concepts identify state.
    

There are also a couple of drawbacks, especially if you are used to working with inheritance.

- This replaces a single tree having child nodes with lists of concept schemes and single flat lists. If you prefer a more drill-down oriented approach concept schemes probably aren’t the way you want to go.
    
- This approach doesn’t work as well when your taxonomy also drives your inheritance structure. The `skos:broader` property denotes semantic generalisation without necessarily specifying what such generalisation means, while `rdfs:subClassOf` indicates that the subclassing class inherits the properties of the superclass (and its ancestors).
    

Thus, the decision about whether to use class inheritance or concept inheritance can both drive how you design your SHACL.

## Siting Your Taxonomy

This question drives a key decision in your design: does taxonomic data belong in your schema graph or your data graph? I’ve not made a lot of distinction in my writings about these as distinct graphs, in part because the location of which graph this context is in is largely immaterial to both SHACL and reification from a modelling perspective, though it looms larger at the application level.

If your taxonomy is contained within your class architecture (i.e., RDFS/OWL), then the taxonomy will intrinsically be defined within the SHACL, likely explicitly subclassing some `ex:Concept` class. This can create a larger SHACL set, though in most cases the inheritance structures here are still relatively shallow.

If your taxonomy is primarily located in SKOS (especially if built around concept schemes rather than broader/narrower divisions) then it may be worth putting information into the schema named graph anyway because this will still be smaller than the data graph (and hence faster to process). There’s nothing stopping you from putting the taxonomy into the data graph, but if you’re doing a lot of validation work, it’s probably better situated into the schema graph.

My recommendation: use SKOS and skos:inScheme to create facets, and the above design pattern, which can be made parametric with a property validator:

In SHACL 1.2, you’d do this via a `sh:ConstraintComponent` — parameterizing the scheme IRI, while leaving `sh:path` as the natural variation point at each `sh:PropertyShape` instantiation:

```
# ── Reusable Component Definition ──────────────────────────────────────────

ex:ConceptInSchemeComponent a sh:ConstraintComponent ;
    sh:parameter [
        sh:path ex:scheme ;
        sh:class skos:ConceptScheme ;
        sh:description "The SKOS ConceptScheme the value must belong to." ;
    ] ;
    sh:propertyValidator [
        a sh:SPARQLValidator ;
        sh:message "Value {$value} is not a skos:Concept in scheme {$scheme}" ;
        sh:prefixes [
            sh:declare [ sh:prefix "skos" ;
                sh:namespace "http://www.w3.org/2004/02/skos/core#"^^xsd:anyURI ] ;
        ] ;
        sh:select """
            SELECT $this ?value
            WHERE {
                FILTER NOT EXISTS {
                    ?value  a              skos:Concept ;
                            skos:inScheme  $scheme .
                }
            }
        """ ;
    ] .


# ── SHACL Instantiations (path is the only thing that varies) ────────────────────

ex:Person_hasTechnicalRole a sh:PropertyShape ;
    sh:path   ex:hasTechnicalRole ;
    ex:scheme ex:TechnicalRole .

ex:Person_hasJobFunction a sh:PropertyShape ;
    sh:path   ex:hasJobFunction ;
    ex:scheme ex:JobFunction . 

# ── SKOS Taxonomy ────────────────────────────────────────────────────────────

ex:TechnicalRole a skos:ConceptScheme ;
    skos:prefLabel "Technical Role"@en ;
    skos:definition "Roles requiring specialist technical skills."@en .

ex:Programmer a skos:Concept ;
    skos:prefLabel "Programmer"@en ;
    skos:inScheme ex:TechnicalRole ;
    skos:topConceptOf ex:TechnicalRole .

ex:DataEngineer a skos:Concept ;
    skos:prefLabel "Data Engineer"@en ;
    skos:inScheme ex:TechnicalRole ;
    skos:topConceptOf ex:TechnicalRole .

ex:SystemsArchitect a skos:Concept ;
    skos:prefLabel "Systems Architect"@en ;
    skos:inScheme ex:TechnicalRole ;
    skos:topConceptOf ex:TechnicalRole .


ex:JobFunction a skos:ConceptScheme ;
    skos:prefLabel "Job Function"@en ;
    skos:definition "Broad organisational functions a person may belong to."@en .

ex:SalesManager a skos:Concept ;
    skos:prefLabel "Sales Manager"@en ;
    skos:inScheme ex:JobFunction ;
    skos:topConceptOf ex:JobFunction .

ex:ProductManagement a skos:Concept ;
    skos:prefLabel "Product Management"@en ;
    skos:inScheme ex:JobFunction ;
    skos:topConceptOf ex:JobFunction .

ex:HumanResources a skos:Concept ;
    skos:prefLabel "Human Resources"@en ;
    skos:inScheme ex:JobFunction ;
    skos:topConceptOf ex:JobFunction .


# ── Data ─────────────────────────────────────────────────────────────────────

# Valid — Programmer is a concept in ex:TechnicalRole
ex:JaneDoe a ex:Person ;
    ex:hasTechnicalRole ex:Programmer ;
    ex:hasJobFunction   ex:ProductManagement .

# Invalid — SalesManager is in ex:JobFunction, not ex:TechnicalRole
ex:JohnSmith a ex:Person ;
    ex:hasTechnicalRole ex:SalesManager .

# Valid — DataEngineer is a concept in ex:TechnicalRole
ex:AkiraNakamura a ex:Person ;
    ex:hasTechnicalRole ex:DataEngineer ;
    ex:hasJobFunction   ex:HumanResources .
```

_I haven’t talked a lot about parametric constraint components, but they can turbocharge what you can do with SHACL, because they extend SHACL itself. Expect a more detailed article soon about them._

A few design notes:

- `sh:propertyValidator` is the right hook here rather than `sh:nodeValidator`, because `$value` is already bound by the property shape machinery — no need to traverse `$PATH` manually.
    
- The original `sh:class skos:Concept` check is folded into the SPARQL `WHERE` clause alongside `skos:inScheme`, keeping the constraint atomic.
    
- `ex:scheme` becomes a first-class predicate on any PropertyShape, making the component self-documenting and queryable via SPARQL across your graph.
    
- If you want a pure node-expression approach instead of SPARQL (closer to the original `sh:node` nesting), SHACL 1.2 node expressions can do it, but the component pattern is more idiomatic for reuse at scale.
    

Another advantage of keeping the SKOS within the shapes graph is that your taxonomy would then become part of your documentation, which can provide significant benefits to LLM interpretation when performing natural language processing.

## Summary

Taxonomies play an oversized role in any ontology: for the most part, they do a lot of the heavy lifting when it comes to semantics. When designing your ontologies, if you have deep structural inheritance of interfaces, then using `rdfs:subClassOf` type organisational systems will likely be necessary, but sometimes (most of the time) you just need to create clusters, or concept schemes, of related concepts, without having to get into the details about which specific properties differentiate such schemas. This faceted approach (using SKOS with `skos:inScheme`) is usually much more flexible, and, for working with SHACL, in particular, it also integrates better with LLMs (anything that reduces the number of hops in a graph is generally better than creating deep trees).

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!XB-D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a4727b7-7774-4b4a-a2b7-123b26b47b09_2048x2048.jpeg)



](https://substackcdn.com/image/fetch/$s_!XB-D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a4727b7-7774-4b4a-a2b7-123b26b47b09_2048x2048.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)  
[The Ontologist](https://ontologist.substack.com/))


