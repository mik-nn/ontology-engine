---
title: "Context Graphs and Event-Driven Architectures"
source: "https://ontologist.substack.com/p/context-graphs-and-event-driven-architectures?utm_source=profile&utm_medium=reader2"
date: "Mar 4"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!_bm0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdccf8290-bec7-49dc-bacd-87f2e0694de3_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!_bm0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdccf8290-bec7-49dc-bacd-87f2e0694de3_2688x1536.jpeg)

I’m now actively working on a book, _Context: The SHACL Revolution_, based in great part on what I’m writing in the Ontologist. Its focus is on most of what’s coming in RDF 1.2, but it’s also intended to provide a detailed guide about what can be done with the technology, not just how it works. My target date for completion is in April of this year, and you may note that, in many cases, I’ll be covering more basic topics on SHACL to fill some of the holes in the articles I’ve written to date, including this one.

## What is a Shape?

A shape is a way of describing a specific pattern in a graph. SHACL 1.1 defines two core kinds of shapes - a node shape and a property shape, while SHACL 1.2 defines a new shape called a class shape, which enhances the base node shape when it is used to clarify a particular class. There are other objects in shacl - rules, reification patterns and so forth, but in most cases these are used in a subordinate capacity to shapes themselves.

A **Node Shape** is the simplest shape. It defines a node. Well, duh. Perhaps it would be more helpful to clarify exactly what is meant by a node. A node in a graph is (usually) the subject of a triple. Most node shapes target particular nodes. In its simplest form, I can create a node shape that talks about one and only one node:

```
Shape:JaneDoeShape
    a sh:NodeShape ;
    sh:targetNode Person:JaneDoe ;
    . 
```

Now, by itself, this doesn’t really do much. It says that there is a node shape `Shape:JaneDoeShape`, and this shape “targets” (applies to) the node `Person:JaneDoe` .

[

![](https://substackcdn.com/image/fetch/$s_!wHsD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ade61e2-25bb-46e5-9fe5-f788829a0519_1911x410.png)

](https://substackcdn.com/image/fetch/$s_!wHsD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ade61e2-25bb-46e5-9fe5-f788829a0519_1911x410.png)

Where things become a little more interesting is when you reference a property shape for that node:

```
Shape:JaneDoeShape
    a sh:NodeShape ;
    sh:targetNode Person:JaneDoe ;
    sh:property Shape:FulllName_PropertyShape ;
    .

Shape:FulllName_PropertyShape a sh:PropertyShape ;
    .
```

This is a fully functional, albeit _very boring_ SHACL ontology, as it only talks about one node and one property, but it’s useful nonetheless to understand the structure. In this case, the node shape has a property called `Shape:FullName_PropertyShape`. It should be noted that this is an abstraction: without knowing the internal contents of this particular property shape, you can only say that such a property exists; as it stands here, there is no implementation of that relationship.

The simplest implementation involves adding a path:

```
Shape:JaneDoeShape
    a sh:NodeShape ;
    sh:targetNode Person:JaneDoe ;
    sh:property Shape:FulllName_PropertyShape ;
    .

Shape:FulllName_PropertyShape a sh:PropertyShape ;
   sh:path Person:hasFullName ; # added path to the property shape.
    .

# Data:
Person:JaneDoe Person:hasFullName "Jane Doe"^^xsd:string .
```

What this does is create an association between the property shape and the predicate path that describes this relationship.

[

![](https://substackcdn.com/image/fetch/$s_!bCEC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F624176cb-5335-422c-81ed-0544b96fb8ae_4861x777.png)

](https://substackcdn.com/image/fetch/$s_!bCEC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F624176cb-5335-422c-81ed-0544b96fb8ae_4861x777.png)

In simple terms, the node shape identifies the target node or nodes and has one or more properties. The property shape associates each property with a path (typically, but not always, a predicate).

Having identified how the property relates to the node, you can also add additional metadata that generally describes the object of that relationship. For instance, you can say several things about the full name property:

-   Jane Doe has one and only full name (that’s probably not always true, but for now, it’s a good approximation).
    
-   The full name is a literal (what’s called its nodekind.
    
-   The full name has an `xsd:string` datatype
    

This can be expressed with additional SHACL attributes:

```
Shape:JaneDoeShape
    a sh:NodeShape ;
    sh:targetNode Person:JaneDoe ;
    sh:property Shape:FulllName_PropertyShape ;
    .

Shape:FulllName_PropertyShape a sh:PropertyShape ;
   sh:path Person:hasFullName ; # added path to the property shape.
   sh:nodeKind sh:Literal ;
   sh:datatype xsd:string ;
   sh:minCount 1 ;
   sh:maxCount 1 ;
   .
```

If no s`h:minCount` is given, SHACL assumes that you can have zero full names (or whatever the property is in question). If no `sh:maxCount` is given, then SHACL assumes that there is no limit on the number of full names that can be provided.

Suppose that Jane has a cat named Felicia (Latin for _Female Cat_). We can define another property shape called `Shape:HasCatPropertyShape` and add it to the list of the node shape:

```
Shape:JaneDoeShape
    a sh:NodeShape ;
    sh:targetNode Person:JaneDoe ;
    sh:property Shape:FulllName_PropertyShape, Shape:HasCat_PropertyShape ;
    .

Shape:FulllName_PropertyShape a sh:PropertyShape ;
   sh:path Person:hasFullName ; # added path to the property shape.
   sh:nodeKind sh:Literal ;
   sh:datatype xsd:string ;
   sh:minCount 1 ;
   sh:maxCount 1 ;
   .

Shape:HasCat_PropertyShape a sh:PropertyShape ;
   sh:path Person:hasCat ; # added path to the property shape.
   sh:nodeKind sh:IRI ;
   .

# Data:
Person:JaneDoe Person:hasFullName "Jane Doe"^^xsd:string ;
        Person:hasCat Cat:Felicia .
```

In this case, we’ve identified that Jane Doe may have a HasCat property, bound to the Person:hasCat path. It is an IRI (meaning that there is a subject somewhere in the graph that defines the object of this assertion (e.g., `Cat:Felicia`). There’s also no limit on how many objects this property has: it could be 30, in which case Jane Doe is definitely a crazy cat lady. It could also be zero (and hence not in the graph).

[

![](https://substackcdn.com/image/fetch/$s_!9rGt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff21ac1fd-a15e-44d8-81e4-6153adf62bab_4961x1270.png)

](https://substackcdn.com/image/fetch/$s_!9rGt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff21ac1fd-a15e-44d8-81e4-6153adf62bab_4961x1270.png)

There is a subtle but important thing to note here. First, beyond identifying shapes (`[] a sh:NodeShape`, `[] a sh:PropertyShape`), there are NO mentions of classes. SHACL has tools for managing classes, but you can, in fact, use SHACL without knowing anything _about_ classes.

This is significant because SHACL is a structural language, rather than a class-based (or inferential) one. There are ways to perform inference (logic) within SHACL, notably SHACL Rules, but at its core, SHACL simply defines patterns. This conceptual simplicity means that SHACL can be thought of as a semantic machine language, operating beneath inference-based systems.

## Node Shapes, Classes and Shape Classes

That said, selecting individual nodes within a graph can become unwieldy very quickly. You likely don’t want to write separate SHACL node constraints for every instance individually; you are much more likely to want to talk about the behaviour of a set of instances, otherwise known as a class.

We can extend our graph to cover more people (and more cats), in this case by specifying a `sh:targetClass` in the nodeshape:

```
Shape:PersonShape
    a sh:NodeShape ;
    sh:targetClass Class:Person ;
    sh:property Shape:Person_FulllName_PropertyShape, Shape:Person_HasCat_PropertyShape ;
    .

Shape:Person_FullName_PropertyShape a sh:PropertyShape ;
   sh:path Person:hasFullName ; # added path to the property shape.
   sh:nodeKind sh:Literal ;
   sh:datatype xsd:string ;
   sh:minCount 1 ;
   sh:maxCount 1 ;
   .

Shape:Person_HasCat_PropertyShape a sh:PropertyShape ;
   sh:path Person:hasCat ; # added path to the property shape.
   sh:nodeKind sh:IRI ;
   sh:class Class:Cat ;
   .

Shape:CatShape
    a sh:NodeShape ;
    sh:targetClass Class:Cat ;
    sh:property Shape:Cat_FullName_PropertyShape ;
    .

Shape:Cat_FullName_PropertyShape a sh:PropertyShape ;
   sh:path Cat:hasFullName ; # added path to the property shape.
   sh:nodeKind sh:Literal ;
   sh:datatype xsd:string ;
   sh:minCount 1 ;
   sh:maxCount 1 ;
   .

# Data:
Person:JaneDoe a Class:Person ;
    Person:hasFullName "Jane Doe"^^xsd:string ;
    Person:hasCat Cat:Felicia, Cat:Dinah ;
    .

Person:MichaelJones a Classs:Person ;
    Person:hasFullName "Michael Jones"^^xsd:string ;
    Person:hasCat Cat:Thomas ;
    .

Cat:Felicia a Class:Cat ;
   Cat:hasFullName "Felicia"^^xsd:string ;
   .
Cat:Dinah a Class:Cat ;
  Cat:hasFullName "Dinah"^^xsd:string ;
  .
Cat:Thomas a Class:Cat ;
  Cat:hasFullName "Thomas"^^xsd:string ;
  .
```

This graph is bigger, but not conceptually that different visually:

[

![](https://substackcdn.com/image/fetch/$s_!cjkS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd96c5ca-81f3-481b-bef2-7ad9c4292fc0_6750x8040.png)

](https://substackcdn.com/image/fetch/$s_!cjkS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd96c5ca-81f3-481b-bef2-7ad9c4292fc0_6750x8040.png)

In the new Person Shape, there’s a new assertion using the `sh:targetClass` property:

```
Shape:PersonShape
    a sh:NodeShape ;
    sh:targetClass Class:Person ;
    sh:property Shape:Person_FullName_PropertyShape, Shape:Person_HasCat_PropertyShape ;
    .
```

The `sh:targetClass` identified all of the nodes that are identified as being instances (have an `rdf:type` relationship with the relevant target, here `Person:JaneDoe` and `Person:MichaelJones`. Note that, unlike before, you do have to make sure that you identify the class of each instance in the model in order for sh:targetClass to work.

```
Person:JaneDoe a Class:Person . # where "a" is a shorthand for rdf:type in Turtle.
```

## Property Shapes and Blank Nodes

Property shapes can be named, as is illustrated above, but you can also create an inline property node by using blank node bracket notation. For instance, the above could be rewritten as:

```
Shape:PersonShape
    a sh:NodeShape ;
    sh:targetClass Class:Person ;
    sh:property [
         a sh:PropertyShape ;
         sh:path Person:hasFullName ; # added path to the property shape.
         sh:nodeKind sh:Literal ;
         sh:datatype xsd:string ;
         sh:minCount 1 ;
         sh:maxCount 1 ;
        ],[
        a sh:PropertyShape ;
        sh:path Person:hasCat ; # added path to the property shape.
        sh:nodeKind sh:IRI ;
        sh:class Class:Cat ;
        ]
  .

Shape:CatShape
    a sh:NodeShape ;
    sh:targetClass Class:Cat ;
    sh:property [
        a sh:PropertyShape ;
        sh:path Cat:hasFullName ; # added path to the property shape.
        sh:nodeKind sh:Literal ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        ]
   .
```

The use of blank nodes can make for easier-to-understand shapes, but at the cost of being unable to refer to those shapes outside of the scope of the particular calling class.

There’s an example here that can better illustrate this point. Note that both people and cats have `hasFullName` properties, but one is in the `person:` namespace while the other is in the `cat:` namespace. Since they essentially describe the same properties, it may make more sense to consolidate these into a single property shape that can be invoked from multiple other node shapes:

```
Shape:PersonShape
    a sh:NodeShape ;
    sh:targetClass Class:Person ;
    sh:property Shape:Thing_hasFullName ;
    sh:property [
        a sh:PropertyShape ;
        sh:path Person:hasCat ; # added path to the property shape.
        sh:nodeKind sh:IRI ;
        sh:class Class:Cat ;
        ]
  .

Shape:CatShape
    a sh:NodeShape ;
    sh:targetClass Class:Cat ;
    sh:property Shape:Thing_hasFullNamePropertyShape ;
    .

Shape:ThingShape ;
    a sh:NodeShape ;
    sh:targetClass Class:Thing ;
    sh:property Shape:Thing_hasFullNamePropertyShape ;
    .

Shape:Thing_hasFullNamePropertyShape
         a sh:PropertyShape ;
         sh:path Thing:hasFullName ; # added path to the property shape.
         sh:nodeKind sh:Literal ;
         sh:datatype xsd:string ;
         sh:minCount 1 ;
         sh:maxCount 1 ;
        .

# Data

Person:JaneDoe a Class:Person ;
      Thing:hasFullName "Jane Doe"^^xsd:string ;
      Person:hasCat Cat:Felicia ;
      .

Cat:Felicia a Class:Cat ;
      Thing:hasFullName "Felicia"^^xsd:string ;
      .
```

In this case, those properties that are specific to the class, such as `Person:hasCat,` are defined inline, but those properties that are common to multiple classes are passed by reference.

## Understanding Target Nodes

The use of target nodes needs to be explained in more depth. The role of a node shape, when you get right to it, is to identify within the graph the subjects (node list) that will be examined for validation. For instance, if you have a class called `Class:Person` , then the above SHACL node shape (with `sh:targetClass Class:Person`) will look for all subjects (instances) that have a predicate of `rdf:type` and an object of `Class:Person` and will then validate whether each subject passes that validation (i.e., has the correct patterns specified by the properties).

Put more simply: _shape nodes gather, property nodes validate._

Note that the gathering part is similar to how a SPARQL query works:

```
select $this WHERE {
    $this rdf:type Class:Person .
}
```

(and in fact this is how you use SPARQL for validation within SHACL). It retrieves a list of subjects, which is then passed to the property node validators or rules. You can also use SHACL-SPARQL to express this relationship, which will be discussed in greater detail later.

However, this also points to a different processing model for SHACL than it does for SPARQL.

**SPARQL** operates on RDF graphs (typically indexed for performance), with the WHERE clause performing pattern matching to create **variable bindings** for all variables in the graph patterns. The SELECT statement then projects these bindings (with potential transformations via expressions) to produce the specified result columns.

**SHACL**, in contrast, operates on a node-centric model: target declarations produce a set of focus nodes, and the processor iterates over each node to evaluate constraints independently. This often makes more sense in programmatic workflows, as it is often easier to iterate over a list from a processing standpoint than to use pattern matching, especially when dealing with RDF stored in files rather than in indexed databases.

[

![](https://substackcdn.com/image/fetch/$s_!kDjT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab5744b6-2740-40e2-b377-43f31e3bd470_5652x3025.png)

](https://substackcdn.com/image/fetch/$s_!kDjT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab5744b6-2740-40e2-b377-43f31e3bd470_5652x3025.png)

The SHACL validator in effect iterates over the targeted nodes (collected in whatever manner) and for each node, iterates over the properties to determine which properties are invalidated.

The flow diagram for this process can be seen here:

[

![](https://substackcdn.com/image/fetch/$s_!-V8I!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4011a128-367a-42fe-ac26-50d7186e6e66_8192x4788.png)

](https://substackcdn.com/image/fetch/$s_!-V8I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4011a128-367a-42fe-ac26-50d7186e6e66_8192x4788.png)

It is worth noting that those subjects that are selected are validated; if they validate, they receive a report indicating that they are valid, otherwise they receive a report that they are invalid, with the associated error messages, with each report being in Turtle (Reports will be covered in the next chapter).

## Other Targeting Strategies

Frequently, you may find that you want to target relationships that are not strictly speaking class relationships. For instance, if you have a taxonomy based upon SKOS, then you may frequently want to check for nodes that are children of a broader taxonomy, you could use the `sh:targetSubjectsOf` property as your target node selector. This will return the subjects for all triples that have the skos:broader property. An example shows how this might work for

```
# Node shape definition
ex:NarrowerConceptShape
    a sh:NodeShape ;
    sh:targetSubjectsOf skos:broader ;
    sh:property Shape:Broader_PropertyShape, Shape:HasFurColor_PropertyShape ;
    .
# Property shape definitions (separate statements)
Shape:Broader_PropertyShape 
    a sh:PropertyShape ;
    sh:path skos:broader ;
    sh:class skos:Concept ;
    sh:hasValue ex:Mammal ;
    .
Shape:HasFurColor_PropertyShape 
    a sh:PropertyShape ;
    sh:path Mammal:hasFurColor ;
    sh:class Class:FurColor ;
    sh:minCount 1;
    .

# Data that would validate successfully:
ex:Dog 
    a skos:Concept ;
    skos:broader ex:Mammal ;
    Mammal:hasFurColor Color:Brown .

Color:Brown a Class:FurColor .
ex:Mammal a skos:Concept .

# Would produce: sh:conforms true

ex:Parrot 
    a skos:Concept ;
    skos:broader ex:Bird ;
    Bird:hasFurColor Color:Blue ;
    Bird:isPushingUpTheDaisies true ;
    .

Color:Brown a Class:FurColor .
Color:Blue a Class:FeatherColor .
ex:Bird a skos:Concept .

# Would produce: sh:conforms false
```

Significantly, this provides a way of iterating over subjects that aren’t necessarily instances of classes (such as all immediate narrower terms of mammals, as illustrated here).

Again, note the distinction here between SPARQL and SHACL. In SPARQL, you are, in essence, doing a Venn diagram to find all possible solutions that satisfy the WHERE constraints. In SHACL, in the above example, you are specifying all taxonomy children, then testing them to make sure that they are children of (subjects of) `ex:Mammal`. The parrot is not an `ex:Mammal`; it is an `ex:Bird`. It will still be tested for validity.

The `sh:targetObjectsOf` property works in a similar manner, but the targets in this case will be objects rather than subjects from the triples, based upon the predicate. This will typically be used with things like RDF sets, which have the `rdf:member` property, with the set then having a list of members as objects:

```
# SHACL
ex:CommitteeMemberShape
    sh:targetObjectsOf rdf:member ;
    sh:property [
        sh:path rdfs:label
    ].

# Data
# Validates all objects of rdf:member triples#
ex:SafetyCommittee
    a rdf:Bag ;
    rdf:member ex:Person1 ;  # ← Person1 is TARGETED
    rdf:member ex:Person2 ;  # ← Person2 is TARGETED
    rdf:member ex:Person3 ;  # ← Person3 is TARGETED
.
```

This will validate all members of the `ex:SafetyCommittee` if they have `rdfs:label` properties, and will give `sh:conform false` otherwise.

## The sh:targetWhere property

In SHACL 1.2, another targeting property was added because sh:targetSubjectsOf and sh:targetObjectsOf could be inefficient when the dataset was large. The sh:targetWhere property lets you create multiple conditions that all must be set for a given item to be selected into the node list. For example, consider Benefit Eligible Employees. The shape for such employees might look like the following:

```
ex:BenefitEligibleEmployeeShape
    a sh:NodeShape ;
    
    # WHO: Full-time employees with 90+ days
    sh:targetWhere [
        sh:class ex:Employee ;
        sh:property [
            sh:path ex:employmentStatus ;
            sh:hasValue "full-time" ;
        ] ;
        sh:property [
            sh:path ex:daysEmployed ;
            sh:minInclusive 90 ;
        ] ;
    ] ;
    
    # WHAT: Must have benefit enrollment
    sh:property [
        sh:path ex:healthBenefitPlan ;
        sh:minCount 1 ;
    ] ;
    .

# Data

ex:Alice
    a ex:Employee ;
    ex:employmentStatus "full-time" ;
    ex:daysEmployed 120 ;
    ex:healthBenefitPlan "Gold" ;  # ✓ Has benefits
    .

ex:Bob
    a ex:Employee ;
    ex:employmentStatus "full-time" ;
    ex:daysEmployed 150 ;
    # ✗ Missing benefits - VIOLATION!
    .

ex:Charlie
    a ex:Employee ;
    ex:employmentStatus "part-time" ;  # ← NOT full-time
    ex:daysEmployed 200 ;
    # Not targeted - no validation
    .

ex:Diana
    a ex:Employee ;
    ex:employmentStatus "full-time" ;
    ex:daysEmployed 45 ;  # ← Less than 90 days
    # Not targeted - no validation
    .
```

Here, the node list is defined as the intersection of two properties: employment status (must be full-time) and number of days employed (at least 90 days). They must also be employees. This cuts down the list to those who are eligible.

The SHACL then validates this set to determine whether it has a health benefit plan. If they do, they pass validation. If they don’t, this will return a report indicating that they don’t have a plan yet and will consequently need to choose one.

Notice in the data that Alice meets the criteria and has a plan in place. Bob meets the criteria but doesn’t have a plan, while neither Charlie nor Diana meet the requirements. The node list will only include Alice and Bob as a consequence, with Alice validating and Bob failing validation.

The `sh:targetWhere` Property will likely become a fairly essential part of SHACL, because it performs much the same function as SPARQL in that it uses matches against complex triples in context in order to reduce the overall number of target nodes that need to be processed. At the same time, it still works best for indexed triple stores (in essence, it IS constructing a SPARQL query so you don’t have to). Simple class matching is still preferable in that regard for basic use cases, but `sh:targetWhere` can be much more powerful when you need complex overlapping queries.

## Summary

The ability to target nodes is fundamental to SHACL and is the primary role of the SHACL node shape. It also happens to be a good way to design shaped or structural schemas. SHACL differs from SPARQL in that the former is primarily list-oriented: it determines what should be processed, then either validates each item in the list against the property shapes or constructs new triples using SHACL rules. This can be extended to other operations as well.

In my next post, I plan to dive deeper into property shapes and begin exploring the world of reporting.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!xFEb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08cd5023-6f2f-403f-96bc-34a09b24d64c_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!xFEb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08cd5023-6f2f-403f-96bc-34a09b24d64c_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.