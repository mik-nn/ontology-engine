---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Understanding-Shapes-by-Kurt
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:11.274962+00:00'
  title: Understanding Shapes By Kurt
  type: plain-doc
  version: '0.1'
---

# Understanding Shapes By Kurt

[

![](https://substackcdn.com/image/fetch/$s_!Sz95!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12d5448b-ad2e-458f-9334-2085b0532e92_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!Sz95!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12d5448b-ad2e-458f-9334-2085b0532e92_2688x1536.png)

Bertrand Russell and Alfred North Whitehead, co-authors of the Principia Mathematica (1910)

\[Edited for Corrections\]

When I first encountered SHACL, about eight years ago now, I didn’t really see the value in it. It looked to me kind of like someone had taken the XML Schema Langauge and adapted it for use in RDF. There’s value in this, no doubt - part of the reason that RDF is so hard to understand is that, for the most part, there is a tacit assumption that you have to use OWL for modelling ontologies because, well, that’s all that there was, but the OWL model can be daunting for those who aren’t coming into it from a deep computer science or mathematics background. SHACL didn’t bridge that gap … it started from a very different set of base assumptions, ones that were more familiar to programmers.

What I didn’t realise until after I’d spent some time working with it was that SHACL also broke another core OWL assumption, one so embedded in OWL that you don’t even notice it. This assumption is the primacy of _classes_. In OWL, everything is a class. Most classes are subclasses of other classes. Properties are instances of classes. Instances are (arguably) singleton classes. OWL is set theory incarnate, and since so much of classical mathematical logic is predicated upon set theory, it’s not surprising that classes predominate, and you cannot talk about RDF without talking about classes.

Yet, while there are classes in SHACL, as well, they aren’t as dominant. Instead, SHACL concentrates on the concept of Shapes.

## Shapes Aren’t Classes

If OWL is all about set theory, SHACL is all about graph theory. A SHACL **shape** can be thought of as a description of how things are connected to one another, and it is intimately associated with the notion of paths. If you can describe the characteristics of how things connect via paths, then you have a mechanism for much better abstracting out patterns without any prejudgment about what those patterns mean. You can still reason on these shapes, but reasoning is only one use case for SHACL, and is really not even the primary one.

Let’s start at the beginning.

I used to have a Cat named Bright Eyes. She was a lovely, tiny Russian Blue, and held sway in an elegant way in our house for fifteen years before finally succumbing to cancer about a year ago. In SHACL, I could talk about her in the following terms:

```
shape:BrightEyesShape a sh:NodeShape ; 
    sh:targetNode ex:BrightEyes ;
    sh:property shape:BrightEyesShape_Name ,
                shape:BrightEyesShape_Species ,
                shape:BrightEyesShape_Breed ,
                shape:BrightEyesShape_Gender ,
                shape:BrightEyesShape_Size ,
                shape:BrightEyesShape_Age ,
                shape:BrightEyesShape_PetParent . 
```

The first line indicates that we are defining a shape about a particular node, with the second line indicating that this node is the instance node for Bright Eyes. Notice beyond the assertion that shape:BrightEyesShape is a sh:Node, there are no explicit references to classes anywhere here. Instead, what is being asserted is that a shape describing Bright Eyes has a species, a coat, a gender, a size, an age, and a pet parent as property shapes.By itself, this set of assertions tells you nothing about the RDF (yet). It’s just scaffolding.

We can then start to define the property shapes. First, for property species:

```
shape:BrightEyesShape_Species a sh:PropertyShape ;
    sh:path ex:hasSpecies ;
    sh:minCount 1;
    sh:maxCount 1;
    sh:nodeKind sh:IRI ;
    sh:hasValue ex:FelisDomesticus .
```

This provides metadata about the property associated with species. First, it gives the path (sh:path) that indicates how the property itself is defined. The path here is specified just as a single predicate (ex:hasSpecies), but it is possible to create more complex paths. It then specifies the cardinality (there is one and only one value that should be on the path). It indicates the kind of object for this path (a sh:IRI, meaning that the object is another object node rather than a literal) and finally, it specifies what this particular value is (ex:FelisDomesticus, or the common house cat).

This is a very roundabout way of describing a single relationship:

```
ex:BrightEyes ex:hasSpecies ex:FelisDomesticus .
```

Note again that there are no assumptions being made here about classes, only about nodes and predicate paths. You can similarly talk about literals, such as name:

```
shape:BrightEyesShape_Name a sh:PropertyShape ;
    sh:path ex:hasName ;
    sh:nodeKind sh:Literal ;
    sh:datatype xs:string ;
    sh:hasValue "Bright Eyes"^^xs:string .
```

In this case, there are no constraints on names (she had a few familiar names, and some cats may have no names whatsoever). This is a literal, and is designated as such, of type xs:string .

Most of the other properties look similar, and I won’t enumerate them here. What’s significant is that once you have this, you have a mechanism that connects nodes with structural metadata. For instance, I can determine the cardinality of the predicate sh:hasSpecies by doing a SPARQL query (assuming the SHACL is in the triple store graph):

```
SELECT ?predicate ?minOccurs ?maxOccurs WHERE {
    VALUES (?node ?predicate) {(ex:BrightEyes ex:hasSpecies)}
    ?shape sh:targetNode ?node .
    ?shape sh:property ?property .
    ?property sh:path ?predicate .
    optional {?property sh:minCount ?minOccurs }
    optional {?property sh:maxCount ?maxOccurs }
}
```

Note that this is consistent regardless of the underlying types of relationships, whereas OWL gets complicated in that it defines different kinds of relationships logically.

One other point that’s worth making here: the use of IRIs for shapes is primarily a pedantic convention. It can make code more readable. However, the above shape could just as readily be expressed via blank nodes:

```
[] a sh:NodeShape ; 
    sh:targetNode ex:BrightEyes ;
    sh:property [
         a sh:PropertyShape ;
         sh:path ex:hasName ;
         sh:nodeKind sh:Literal ;
         sh:datatype xs:string ;
         sh:hasValue “Bright Eyes”^^xs:string ;
   ],[
         a sh:PropertyShape ;
         sh:path ex:hasSpecies ;
         sh:minCount 1;
         sh:maxCount 1;
         sh:nodeKind sh:IRI ;
         sh:hasValue ex:FelisDomesticus .

  ],[...] .
```

Either form is correct; the question largely comes down to whether you will need to reference a node shape in the future.

## Shapes Can Build Classes, However

The difference between describing a single instance and describing a class is fairly minimal.

```
shape:CatShape a sh:NodeShape ; 
    sh:targetClass ex:Cat ; # targetClass used here
    sh:property shape:CatShape_Name ,
                shape:CatShape_Species ,
                shape:CatShape_Breed ,
                shape:CatShape_Gender ,
                shape:CatShape_Size ,
                shape:CatShape_Age ,
                shape:CatShape_PetParent .

shape:CatShape_Name a sh:PropertyShape ;
    sh:path ex:hasName ;
    sh:nodeKind sh:Literal ;
    sh:datatype xs:string ;
    # no sh:hasValue property
    .

shape:CatShape_Species a sh:PropertyShape ;
    sh:path ex:hasSpecies ;
    sh:minCount 1;
    sh:maxCount 1;
    sh:nodeKind sh:IRI ;
    sh:class ex:Species ; #sh:class used here
    # no sh:hasValue property
    .

...
```

In this particular case, the sh:targetNode property is replaced with a sh:targetClass property that points to the IRI designating the Cat class (ex:Cat). In the property shapes, the sh:hasValue property is removed, and for literals, the datatype is added if it’s not specified earlier (it can be retrieved in the instance data from the sh:hasValue, but doesn’t have to be).

However, it should be noted that you can also create shape nodes that don’t need to specifically target a class. For instance, you might have noted that ex:Cat and ex:FelisDomesticis are more than likely the same thing. As such, you could use the sh:targetSubjectsOf property of ex:Species, and the same property as a constraint definition:

```
shape:FelisDomesticisShape a sh:NodeShape ; 
    sh:targetSubjectsOf ex:FelisDomesticis ; # targetClass used here
    sh:property shape:FelisDomesticisShape_Name ,
                shape:FelisDomesticisShape_Species ,
                shape:FelisDomesticisShape_Breed ,
                shape:FelisDomesticisShape_Gender ,
                shape:FelisDomesticisShape_Size ,
                shape:FelisDomesticisShape_Age ,
                shape:FelisDomesticisShape_PetParent .

shape:FelisDomesticisShape_Species a sh:PropertyShape ;
    sh:path ex:hasSpecies ;
    sh:minCount 1;
    sh:maxCounts 1;
    sh:nodeKind sh:IRI ;
    sh:class ex:Species ; #sh:class used here
    sh:hasValue sh:hasValue ex:FelisDomesticis ;
    .
```

What this shape does is indicate that any node that has the statement

```
?node ex:hasSpecies ex:FelisDomesticis .
```

will have the specific properties defined. In effect, this creates a class without specifically declaring a class via rdf:type. This capability is enormously useful because it makes it possible to create ersatz classes and corresponding properties that are tailored for specific conditions.

For instance, you could create one set of shapes for cats (Felis Domesticus) and another for dogs (Canis lupus familiaris) that each tailor some property (or define properties) that are unique to each species. For instance, the property ex:hasBreed might vary depending upon whether you’re dealing with a cat or a dog:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix shape: <http://example.org/shapes/> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

shape:PetShape
    a sh:NodeShape ;
    sh:targetClass ex:Pet ;
    sh:property [
        sh:path ex:species ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ] ;
    # Rule for cats
    sh:rule [
        a sh:SPARQLRule ;
        sh:condition [
            sh:property [
                sh:path ex:species ;
                sh:hasValue ex:FelisDomesticus ;
            ] ;
        ] ;
        sh:deactivated false ;
        sh:node shape:CatPropertyShape ;
    ] ;
    # Rule for dogs
    sh:rule [
        a sh:SPARQLRule ;
        sh:condition [
            sh:property [
                sh:path ex:species ;
                sh:hasValue ex:CanisLupusFamiliaris ;
            ] ;
        ] ;
        sh:deactivated false ;
        sh:node shape:DogPropertyShape ;
    ] .

shape:CatPropertyShape
    a sh:NodeShape ;
    sh:property [
        sh:path ex:breed ;
        sh:datatype xs:string ;
        sh:minCount 1 ;
        sh:in ( “Persian” “Siamese” “Maine Coon”, "Russian Blue" ) ;
    ] ;
    sh:property [
        sh:path ex:feed ;
        sh:datatype xs:string ;
        sh:pattern “^(wet|dry) cat food$” ;
    ] .

shape:DogPropertyShape
    a sh:NodeShape ;
    sh:property [
        sh:path ex:breed ;
        sh:datatype xs:string ;
        sh:minCount 1 ;
        sh:in ( “Labrador” “German Shepherd” “Poodle” ) ;
    ] ;
    sh:property [
        sh:path ex:feed ;
        sh:datatype xs:string ;
        sh:pattern “^(wet|dry) dog food$” ;
    ] .
 
```

This makes use of the SHACL advanced features, which may or may not be supported in your SHACL validator, but this doesn’t necessarily matter if you are using SHACL for structural metadata.

For instance, in this particular case, the shape has two particular rules (vie the sh:rule property). The first checks for two conditions - whether the species is ex:FelisDomesticus or ex:CanusLupusFamiliaris. In the first case, the cat shape should be utilised, while the dog shape is used in the second case. The cat shape specifies cat breeds (path `ex:breed`) and looks for the pattern of wet or dry cat food (`ex:feed`), while the second specifies dog breeds and looks for the pattern of wet or dry dog food.

A few key points here: I’ve set the `sh:targetClass` as `ex:Pet`, though I could have just as readily used `sh:targetSubjectsOf` on `ex:hasSpecies`. Classes are useful for a formal ontology, but in general there’s a tradeoff between making a taxonomy sufficiently deep to be useful but not so deep as to be computationally difficult to management.

The latter form can prove very useful when any given taxonomy class has a large number of members or when you have properties that range across multiple classes. This also reduces the need to do deep (and expensive) inferencing, especially in examples such as transitive closure for something like rdfs:subClassOf, which can get deep.

## SHACL Rules

It’s worth taking a look at SHACL Rules in more detail. Consider the cat rule from the previous section:

```
    sh:rule [
        a sh:SPARQLRule ;
        sh:condition [
            sh:property [
                sh:path ex:species ;
                sh:hasValue ex:FelisDomesticus ;
            ] ;
        ] ;
        sh:deactivated false ;
        sh:node shape:CatPropertyShape ;
    ]
```

A role consists of a condition, an activation indicator, and node that holds the appropriate shape if the condition is met. Put another way, it’s a router to other shapes. From SPARQL, you can basically follow the SHACL pattern:

```
SELECT distinct ?subShape WHERE {
    VALUES ?this {ex:BrightEyes}
    ?this a ?class .
    ?this ?predicate ?value .
    ?shape sh:targetClass ?class .
    ?shape sh:rule ?rule .
    ?rule sh:deactivated false .
    ?rule sh:condition ?condition .
    ?condition sh:property ?property .
    ?property sh:path ?predicate .
    ?property sh:hasValue ?value .
    ?rule sh:node ?subShape .
    }
 
```

This will retrieve all shapes that are valid for the given node (indicated by `?this`), which in the case of Bright Eyes should just be the shape `shape:CatPropertyShape`. Walking through the query:

1.  For the test node (`ex:BrightEyes`, aka `?this`), retrieve its `?class`, along with all of its predicates and their object values.
    
2.  Determine the `?shape` associated with the `?class`.
    
3.  Once you get the `?shape`, retrieve all of the `rules` associated with that `?shape` (we’re ignoring the cardinality properties for now).
    
4.  Make sure that the `?rule` is active.
    
5.  For each active `?rule`, get the `?condition` associated with the rule.
    
6.  Retrieve the `?property` nodes associated with that `?condition`.
    
7.  For each `?property`, test that the property’s path corresponds to one of the defined `?predicates` for `?this`, and that it has the indicated value.
    
8.  If every `?property` satisfies this ?condition, then retrieve the relevant `?subShape`.
    

Once you have the relevant subShape, then you can mine that shape for metadata.

This naturally leads to a significant observation:

## SHACL Is More Than Validation

A lot of people who have worked heavily with OWL tend to poo-poo SHACL, saying that its only real use is validation. Certainly, validation is an important use case, in large part because it provides a first line of defence against incoming data to ensure that data corresponds to a valid structure.

This is accomplished via an external validator, one that applies presented nodes to a graph containing SHACL and returns a message indicating either that the SHACL is valid or that it fails validation in certain ways. Some validators read the SHACL and construct an internal model, while others generate a SPARQL file from that SHACL file and then apply each node in the target set to the SPARQL to determine the appropriate message.

However, one of the major benefits of working with SHACL is that you can also hang metadata on SHACL shapes, which is discouraged in OWL. As a simple example, I’ve often found that it is useful to know both the singular and plural form of a class. If I talk about the plural of “person” in English, it’s “people”, not (usually) “persons”. The property `sh:name` is often given over to the singular form of a given class or shape, but you can extend this with something like shx:pluralName (the shx: namespace indicates a local customisation).

```
shape:PersonShape a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:name "person"^^xs:string ;
    shx:pluralName "people"^^xs:string ;
    sh:property ...
```

This can help with tables and user interfaces in general, as you can get the relevant plural name for a column (and with rules you can even get subshape names in the same way).

Another example comes with type-aheads and suggestions. The sh:in property, for instance, can be used to retrieve the allowable set of items for a dropdown or checkbox list that’s relatively fixed. Again, showing the Cat shape with the property breed,

```
shape:CatShape
    a sh:NodeShape ;
    sh:targetClass ex:Cat ;
    sh:property [
        sh:path ex:breed ;
        sh:datatype xs:string ;
        sh:minCount 1 ;
        sh:in ( “Persian” “Siamese” “Maine Coon”, "Russian Blue" ) ;
    ] ;
    ...
.
```

You can write a simple SPARQL statement that will retrieve a list of values:

```
SELECT ?classPlural (GROUP_CONCAT(?breed,separator=";") as ?breeds)
WHERE {
    ?shape sh:targetClass ?class .
    ?shape shx:pluralForm ?classPlural.
    ?shape sh:property ?property .
    ?property sh:path ex:breed .
    sh:in rdf:rest*/rdf:first ?breed .
} GROUP BY ?property ORDER BY ?classPlural ?breed 
```

This will return a map of the form:

```
[{"classPlural": "Cats", "breeds": “Maine Coon;Persian;Russian Blue;Siamese”},
 {”classPlural”: “Dogs”, “breeds”: “German Shepherd;Labrador;Poodle”}]
 
```

You could also return the IRIs for each breed, if these are defined, but since these will likely reflect the `rdf:label` of each of these breeds, this adds just one additional direct lookup to retrieve the breed information.

This also points to the use of SHACL for storing user interface information, as well as documentation specific to the properties, classes, and shapes in question. Indeed, the ability to add annotations makes SHACL the _natural_ place to put documentation about the data model, particular combined with sh:order and sh:group properties and the sh:message properties for warnings, and from this to then generate comprehensive information about the ontology as a specification.

Rules also become important for classification purposes. You can create a rule, for instance, that will let you read both the species and the weight of a given pet, then use this (just as given above) to determine whether the size of the pet was considered small, medium, or large for that species from within a SPARQL query, with the ranges established as part of the breed itself. Do this in a SPARQL UPDATE query given the above, and you have the means to intelligently create or update a ranged enumeration property automatically.

## SHACL Is Not (Exclusively) Closed World

I keep hearing this: SHACL only works for closed models. That’s simply not true. There is a property `sh:closed` in the s`h:NodeShape` class that when set to true indicates that the properties contained within its `sh:property` set are considered to be comprehensive, but when set to false, this indicates that there may be other properties that are definable that are not contained in the given list. The default for `sh:closed` is `false`, meaning that the default model for SHACL is open.

What this means in principle is simple - if a property is found for a given node, it is considered to be an error in validation IF `sh:closed` is `true`, otherwise, no error is generated (though a warning might be). The `sh:closed` option is primarily used when your data comes from a database that is implicitly closed, where it can help prevent a process from adding properties to the data that didn’t come from the database itself.

It is up to you as an ontologist whether your model is open or closed. This can also be rephrased: _OWL has no way to model a closed-world assumption_. From a governance perspective, this might actually be a strong incentive _not_ to use OWL for your modelling language, especially if you’re dealing with data that needs to interact with relational databases.

## Logical vs. Structural Inferencing

This brings me back full circle. SHACL has a couple of properties that optimize for classes. Because a lot of data is organised around classes historical due to the evolution of ontology practice over time, the idea of creating a distinct sh:targetClass makes some sense. However, in practice, this is identical to:

```
shape:Foo sh:targetSubjectsOf rdf:type ;
    sh:property [ 
          sh:path rdf:type ;
          sh:hasValue ?class ;
          ] .
```

with a conditional rule giving the current value of the type. In other words, there is a structural definition in SHACL that is completely independent of the notion of classes.

Many of the problems that I’ve seen with OWL have come about because people used logical modelling badly. For instance, it’s common to model a hand as having four fingers and a thumb, with minOccurs/maxOccurs for fingers set to 4. In point of fact, a hand has ten digits (ordinarily), each of which is distinct - left thumb, left index finger, left middle finger, left ring finger, left pinky, right thumb, etc. People may have more than ten fingers due to genetic anomalies, or fewer than ten fingers due to accident or disease, but this is a case where the model resolves itself to a 0:1:many situation if it recognises the distinction between fingers as a separate property.

Much of the logic involving disjoint sets also falls into this definition, and has to do with the fact that our definitions of what we mean by ’ are frequently overloaded. Most often, this comes down to the fact that things with common properties may still be different types. For instance, in OWL, it’s easy to say that pets are the disjoint union of dogs and cats (a vast simplification). However, in the SHACL view of the world, this usually comes down to the fact that specific shapes have different rules depending on the information's context, and this, in turn, affects how properties are defined.

Inferencing also works heavily with the notion of transitive closure, such as rdfs:subClassOf, which relates to class entities in a mother-daughter relationship. SHACL has provisions for handling transitive closure via the sh:path function.

```
ex:DescendantShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:property [
        sh:path ( ex:hasChild “+” ) ;  # One or more child relationships
        sh:maxCount 100 ;  # Limit total descendants
        sh:message “Cannot have more than 100 descendants” ;
    ] .
```

or

```
ex:OrganizationHierarchyShape
    a sh:NodeShape ;
    sh:targetClass ex:Organization ;
    sh:property [
        sh:path [ sh:zeroOrMorePath ex:partOf ] ;
        sh:class ex:Organization ;
        sh:message “All parent organizations must be of type Organization” ;
    ] ;
    sh:property [
        sh:path [ sh:oneOrMorePath ex:partOf ] ;
        sh:nodeKind sh:IRI ;
        sh:message “All parent organizations must be IRIs” ;
    ] .
```

SHACL may not be as terse (though it is surprisingly terse) as OWL is, but that’s only because OWL hides a lot of complexity in named relationships, and because it relies upon reasoners over different rulesets in order to surface triples. Over time, I expect that SHACL will likely develop a logical inference layer independently (efforts are underway to do so), but I also expect that structural inferencing, where you identify shapes as structural patterns first and then can use that to _infer_ logical patterns, will likely come to predominate.

SHACL also has (through the DASH extension library) the `dash:reifiedBy` property (discussed in an earlier post) that points to a _shape_ (yup) that identifies the characteristics of any reification metadata. I see such relationships as fairly critical in the shift from static knowledge graphs to process graphs that enable conditional assertions and allow a graph to evolve over time without being destructive.

The problem I see with OWL is that it doesn’t support fuzzy logic and generally avoids reification whenever possible. This doesn’t mean it can’t (just as OWL was never really built for named graphs but can reluctantly work with them), only that by going with a more structural inferential pattern with a more modern view of the evolution of RDF, you’re moving into a mode that both human beings and machines (AIs) can work with because they are dealing with structural rather than formal logical relationships.

Is this a bad thing? Structural inferencing is more graph-oriented (and contextual), whereas logical inferential systems rely on humans recognising and properly modelling specific relationships and, as stated before, are built primarily on set theory, which assumes everything is a class of one form or another. Both are valid ways of thinking, of reasoning, but my suspicion is that AI likely works better with structural patterns.

We’ll see.

In media res,

[

![](https://substackcdn.com/image/fetch/$s_!GRVn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6d56a18-934c-4dab-af16-dbcae3b94481_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!GRVn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6d56a18-934c-4dab-af16-dbcae3b94481_2688x1536.png)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please contact me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please consider contributing something to support my work, allowing me to continue writing.

