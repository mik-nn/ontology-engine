---
title: "Lions and Tigers and Bears, Oh My!"
source: "https://ontologist.substack.com/p/lions-and-tigers-and-bears-oh-my?utm_source=profile&utm_medium=reader2"
date: "Feb 26"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!QWgx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba199bc8-d9cb-4cbf-ae05-04c95b2285fc_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!QWgx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba199bc8-d9cb-4cbf-ae05-04c95b2285fc_2688x1536.png)

When I was in college, I had an organic chemistry class as part of my physics major. I’d had several years of high school chemistry, including a full year of organic, so I thought that the college class would be a breeze. I was wrong.

Chemistry tends to be divided into inorganic chemistry and organic chemistry. Inorganic chemistry is mostly about states of matter. You have 112 known elements and an additional 6 that are postulated but have not been confirmed in the period table, and most of these have well-known states - various isotopes, densities, shell distributions, decay paths if radioactive, and so forth. Inorganic elements do form molecules, but they are usually reasonably well known and regular - various sorts of crystals, liquids, glasses and similar constructs - and they are comparatively simple.

Organic molecules, on the other hand, are made up for the most of perhaps 18 of those elements, with carbon, oxygen, hydrogen, nitrogen and sulfur predominating. What makes them so striking is that carbon has four free orbitals, making it the perfect backbone for long, complex chains, with variants of water (H2O) and ammonia (NH3) providing variety along these chains. Carbon can also form pentene and benzene rings, which, like other carbon-containing molecules, form complex structures.

We tend to think of these organic chemicals as being discrete units, with similar structures forming specific classes of organic compounds. For instance, there are twenty-two amino acids that make up proteins and five nucleic acids that together make up the complex chains of DNA and RNA, which in turn can contain billions upon billions of potential configurations. Yet at the same time, it’s worth noting that these molecules are essentially conceptual in nature - there are no clear boundary lines that demarcate when one molecule ends, and another begins, only bonds of various strengths. This is why inorganic and organic chemistry, while sharing the same building blocks, often differ dramatically in how we think about organising them.

SHACL is not just a different set of predicates from OWL, but also represents a conceptual shift in the way that you think about graphs. If OWL can be thought of as class-based thinking, then SHACL is conceptually closer to shape-based thinking.

**Shape-based thinking** is different from Class-based thinking. With **class thinking**, inheritance and inference play significant roles. You concentrate on each assertion independently, and you generally restrict classes based on the predicates being used. This can make OWL in particular difficult to follow, because inheritance can make relationships relatively obscure. There is also a constant tug of war in which you’re trying to balance the number of classes vs. the number of predicates.

With shapes, on the other hand, you can work with data at a more abstract level, effectively looking at the expectation of how properties are formed, to build out specific molecules of data, rather than just atoms (instances of classes).

This has several advantages:

-   You need fewer predicates (and arguably fewer classes), making your ontologies smaller and easier to navigate.
    
-   The same predicate can change its meaning depending on the context around it. This makes them more responsive to large systems.
    
-   You can use `sh:in property` to identify nodes belonging to a particular set. This can cut down on deeply nested taxonomies, in particular, by treating taxonomy constraints as structural definitions rather than class inheritance.
    
-   Shapes can be explicitly applied to nodes or node patterns without having to construct explicit classes.
    
-   Shapes are a more natural way of working with RDF Lists.
    
-   Shapes are designed to be self-documenting, not just in terms of providing descriptions, but also of giving messages when nodes fail validation, including severity.
    
-   Classes require inferencing - the use of rules to generate (construct) triples based upon specific logical formalisms, meaning that if the rules are not specified or available, class-based thinking fails. Shapes are rethinking how we define rules, seeing them as a natural artefact of validation.
    
-   When combined with SHACL [rules](https://w3c.github.io/data-shapes/shacl12-rules/) and [node expressions](https://w3c.github.io/data-shapes/shacl12-node-expr/) (part of SHACL 1.2), SHACL shapes become generative. That is to say, shape properties can be created that are computed based on context rather than asserted. This reduces the need for complex SPARQL queries dramatically, as you can ask for a “view” of a particular node that will use SHACL to determine what goes into that view. SHACL may use SPARQL to calculate part of that view, of course, but this approach is both more restful and safer in general.
    

## Molecular Shapes

So what does this have to do with data modelling? Simply put, you can think of traditional OWL-based inferential modelling as the equivalent of inorganic chemistry, where the class view predominates. It is a language of logical formalisms, of inheritance from more generalised patterns, of the notion that everything within the graph is accurate, and of the idea that new knowledge is essentially surfaced by following logical assertions.

A shape-based language, such as SHACL, is not class-based but rather structure-based, and typically treats properties not as single edges but as more complex structures in their own right.

For instance, consider the following: how do you model populations of a country when it consists of multiple sub-populations, in this case, populations of various tribes in England in the early Medieval Period:

[

![](https://substackcdn.com/image/fetch/$s_!42Vc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde8011a6-7be8-4659-a652-003000f4455a_2347x3104.png)

](https://substackcdn.com/image/fetch/$s_!42Vc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde8011a6-7be8-4659-a652-003000f4455a_2347x3104.png)

Several things of note here:

-   The blue box represents an entity here - the thing being modelled.
    
-   The black boxes represent blank nodes in RDF, but can be thought of as equivalent to an array of maps of anonymous objects in JSON.
    
-   The green boxes represent categories, which in this case are used to differentiate an object based upon some classification scheme.
    
-   The light red boxes represent period properties, covering the period from 600 AD (the approximate end of the Roman occupation) to 1065 AD (just before the Norman invasion). Note that both Country and Population have periods.
    
-   The yellow boxes are literals - generally numeric values, dates or strings.
    
-   Each population has an identical structure, including a population type (the population of a specific tribe), the count of that population, and a percentage of that count relative to the total. Note that this also includes a “Total” population type, with a percentage of 100% and a count of 1,000,000 people (an estimate on the high end of the average number of people in Britain during this period).
    

This example illustrates a core idea in shapes: the same property may have different “meanings” depending on additional contextual information. Here, in particular, there is a distinction between a partial population and a total population, even though there is one property (has population) for describing both. This implies that there are two distinct population shapes, even though they appear identical in definition. The SHACL for the country shape makes this explicit:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

# Node Shape for Country
ex:CountryShape
    a sh:NodeShape ;
    sh:targetClass ex:Country ;
    sh:property ex:CountryShape-totalPopulation ;
    sh:property ex:CountryShape-partialPopulation ;
    sh:property ex:CountryShape-period ;
    sh:closed false .
```

This identifies three properties - total population, partial population, and period. What’s very important to note here is that total population and partial population are not themselves predicates in the graph. Instead, they are properties of the shape. In effect, you are abstracting out a relationship that moves beyond what’s in the graph itself, which is one of the compelling aspects of shapes.

The total population property shape, in turn, can be stated as follows:

```
ex:CountryShape-totalPopulation
    a sh:PropertyShape ;
    sh:path ex:hasPopulation ;
    sh:name “total population” ;
    sh:description “The total population of the country with temporal extent” ;
    sh:class ex:Population ;
    sh:nodeKind sh:BlankNodeOrIRI ;
    sh:node ex:TotalPopulationShape ;
    sh:minCount 1 ;
    sh:maxCount 1 .
```

This uses the path `ex:hasPopulation` , which points to an entity of type `ex:Population`, that may be either an IRI or a blank node, and that is defined by the `ex:TotalPopulationShape`. It is also a required property (minCount 1, maxCount 1).

The total population shape, in turn, is defined as follows:

```
ex:TotalPopulationShape
    a sh:NodeShape ;
    sh:targetClass ex:Population ;
    sh:property [
        sh:path ex:hasPopulationType ;
        sh:class ex:PopulationType ;
        sh:nodeKind sh:IRI ;
        sh:hasValue ex:Total ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path ex:hasPopulationPercentage ;
        sh:datatype xsd:integer ;
        sh:nodeKind sh:Literal ;
        sh:minInclusive 100 ;
        sh:maxInclusive 100 ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path ex:hasPopulationCount ;
        sh:datatype xsd:integer ;
        sh:nodeKind sh:Literal ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ]  ;
    sh:property [
        sh:path ex:hasPeriod ;
        sh:class ex:Period ;
        sh:nodeKind sh:BlankNodeOrIRI ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:node ex:PeriodShape ;
    ] .
```

The total population shape identifies the total population, meaning the population count of all of the aggregate partial populations, and this consequently means that the percentage must be 100% and the population type (determined by the `ex:populationType` path) must be `ex:Total`.

Similarly, the partial population shape indicates the population of a tribe or group within this total population:

```
ex:PartialPopulationShape
    a sh:NodeShape ;
    sh:targetClass ex:Population ;
    sh:property [
        sh:path ex:hasPopulationType ;
        sh:class ex:PopulationType ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path ex:hasPopulationPercentage ;
        sh:datatype xsd:integer ;
        sh:nodeKind sh:Literal ;
        sh:minInclusive 0 ;
        sh:maxInclusive 99 ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path ex:hasPopulationCount ;
        sh:datatype xsd:integer ;
        sh:nodeKind sh:Literal ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ]  ;

    sh:property [
        sh:path ex:hasPeriod ;
        sh:class ex:Period ;
        sh:nodeKind sh:BlankNodeOrIRI ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:node ex:PeriodShape ;
    ] .
```

Here, the population type is constrained to an item from the list of various sub-populations (which doesn’t include `ex:Total)`, and the percentage is between 0% and 99%. Again, same predicates (`ex:hasPopulationType`, etc.) but with different interpretations.

Finally, the period shape indicates the period during which this information is valid.

```
ex:PeriodShape a sh:NodeShape ;
    sh:targetClass ex:Period ;
    sh:property ex:PeriodShape_from, ex:PeriodShape_to ;
    sh:closed false ;
    .

ex:PeriodShape_from a sh:PropertyShape;
    sh:path ex:from ;
    sh:datatype xs:date ;
    sh:nodeKind sh:Literal ;
    sh:minOccurs 1 ;
    sh:maxOccurs 1 ;
    .

ex:PeriodShape_to a sh:PropertyShape;
    sh:path ex:to ;
    sh:datatype xs:date ;
    sh:nodeKind sh:Literal ;
    sh:minOccurs 1 ;
    sh:maxOccurs 1 ;
    .
```

In the above example, all populations share the same range, so treating that range as a distinct object makes sense.

The inline use of `sh:property` (i.e., the use of blank nodes rather than named shapes) works best when you have properties that are strictly bound to the parent class. Since both Country and Population make use of Period, when a node match is made, the `sh:node` value there indicates which node shape to use rather than telling the shape validator to find the shape associated with the path. In some cases, this may be redundant, but in others, it can provide context, just as the total population and partial population shapes use the same path but have different property nodes.

## Specifying Inclusion and Ordering

It is likely that in a knowledge base, you have different (though potentially overlapping) sub-population groups or language groups within a country. You can use RDFS in conjunction with SHACL to be able to specify a particular subset of population types. For instance, for Britain and Scotland, you may have the following defined as part of your SHACL:

```
# Define country subclasses
ex:England a ex:Country, ex:BritishCountry .
ex:Scotland ex:Country, ex:ScottishCountry .

# Target by subclass
ex:BritishCountryShape
    a sh:NodeShape ;
    sh:targetClass ex:BritishCountry ;
    sh:property [
        sh:path ex:hasPopulation ;
        sh:node ex:BritishPopulationShape ;
    ] .

ex:BritishPopulationShape
    a sh:NodeShape ;
    sh:property [
        sh:path ex:hasPopulationType ;
        sh:in (ex:Romans ex:Saxons ex:Angles ex:Welsh ex:Danes ex:Normans) ;
    ] .

# Target by subclass
ex:ScotlandCountryShape
    a sh:NodeShape ;
    sh:targetClass ex:ScotlandCountry ;
    sh:property [
        sh:path ex:hasPopulation ;
        sh:node ex:ScottishPopulationShape ;
    ] .

ex:ScottishPopulationShape
    a sh:NodeShape ;
    sh:property [
        sh:path ex:hasPopulationType ;
        sh:in ( ex:Picts ex:Danes ex:Welsh ex:Caledonians ) ;
    ] .
```

Note again that we have defined both specific shapes for each region, with the notion that each country has two classes that define it (the general country class and a specific regional class). There is also a node shape for each country and a property shape on the `ex:hasPopulationType` path.

Note that `ex:Saxons`, `ex:Angles`, `ex:Danes, ex:Picts`, etc., are each of class `ex:PopulationType` , which is a class containing all possible population subgroups for all countries in the graph. This is actually a preferable design: each class has the maximum number of instances, with the shapes then handling different partitions of that instance space.

There is some overlap (there were Danes in Scotland during the Medieval period), and, from an ethnographic standpoint, one question that may be asked is: “For a given country, provide a list of the available sub-populations?” In this case, you can query directly in the SHACL model:

```
prefix sh: <http://www.w3.org/ns/shacl#>
prefix ex: <http://example.org/>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT distinct ?country (group_concat(?population;separator=', ') as ?populations) 
WHERE {
    # Country is an instance of a country class.
    ?country a ?countryClass .

    # The class is a target class of a country shape
    ?countryShape sh:targetClass ?countryClass .

    # The country shape has one or or properties. Iterate on those.
    ?countryShape sh:property ?propertyShape .

    # for each property shape, see if it is bound to ex:hasPopulation 
    ?propertyShape sh:path ex:hasPopulation

    # if it does, then retrieve the sh:node property to determine
    # the definition 
    ?propertyShape sh:node ?populationNodeShape .

    # if the population node shape's path is bound to ex:hasPopulationType
    ?populationNodeShape sh:path ex:hasPopulationType .

    # then look in the sh:in property to get the population list

    ?populationNodeShape sh:in ?populationList

    # iterate over the list to retrieve the population
    ?populationList rdf:rest*/rdf:first ?population
    }
group by ?country order by ?country
```

This will retrieve the following table

```
|     country |                           population                          |
|-------------|---------------------------------------------------------------|
| ex:Britain  |ex:Romans, ex:Saxons, ex:Angles, ex:Welsh, ex:Danes, ex:Normans|
| ex:Scotland |ex:Picts, ex:Danes, ex:Welsh, ex:Caledonians                   |
```

There are a few things of note here. This could have been done with SKOS or `owl:NamedInstance` terms, but the advantage here is that ordering is preserved. OWL is not particularly focused on ordering, but it often turns out that ordering is an implicit property that matters, such as the order of when tribes first appeared in a particular country. This can be easily superceded, but by capturing enumerations (enumerated items in a list) in this way, you have the advantage of having a natural implicit order.

What’s more, this resolves one of the thornier problems of using an explicit index in a list of concepts or categories - the same property may be in two different sequences in different ways. By taking advantage of a linked list as a way of getting enumerations, the ordering will change based on what’s in the SHACL property shape.

## Validation … and Beyond!

I’ve been showing several examples of SHACL that use it to inform the data model rather than to validate data nodes. Part of the reason for this has to do with the fact that validation, while important, isn’t really that important - it is helpful to determine whether incoming datasets should be added into the graph and can be beneficial for categorisation. Still, neither of these activities really affects queries or logical updates much.

Part of the reason for this is that validation and query are nearly opposite events. Most SPARQL queries perform joins on triples to create what’s called an n-tuple, or a linear vector where each variable represents one slot in the n-tuple. A SELECT statement indicates which particular variable values are displayed for a given configuration that matches the n-tuple output, as well as performing some additional set operations on this set of tuples for concatenation, counts, sums and similar analytics.

A SPARQL query effectively searches the database index for assertions (triples). If a requested triple in SPARQL is not found, then that candidate n-tuple is eliminated as viable and dropped from the n-tuple set.

Validation, on the other hand, tests nodes against a SHACL file (graph) and only produces output (a report) if the nodes being tested do not satisfy the conditions of the node or property shape. Put another way, in validation, you assert that something is true; if the assertion fails, you generate an error message (a report); otherwise, you create a pass message (one with zero error responses). This is roughly the opposite of how SPARQL works, though it mirrors other data standards such as XML Schema vs. XSLT.

> The point of this is that it is worth thinking about SHACL as a description of a data model, not just as a tool for validation, something that lives within the RDF graph, rather than something distinct.

There are several advantages to this approach.

-   You can use most of the core SHACL model in SPARQL without running the validator, as in the example in the previous section.
    
-   You can generate SHACL-based objects in JavaScript or Python. This is an approach pioneered by TopQuadrant, and will be explored in more depth in a subsequent post.
    
-   Several libraries exist for converting SHACL graphs into GraphQL queryable and mutable interfaces, and vice versa.
    
-   You can use SHACL to generate rich interfaces in HTML or Markdown via SELECT statements that generate maps for tables, CONSTRUCT statements that create JSON-LD, or RDF-XML passed to XSLT.
    
-   You can generate pre-emptive SHACL from datasets. This is actually one of the more powerful capabilities that an LLM can provide, as quite frequently ad-hoc datasets (CSVs, Excel documents, unstructured JSON, etc.) have implicit structures but often lack explicit ones. I use this approach with Claude all the time when developing an initial model; it still requires some editorial curation afterwards, but this can dramatically reduce the time to model.
    
-   You can also pass a SHACL file in Turtle to an LLM along with a general dataset, and have the LLM use the SHACL to convert and format the dataset to use that particular schema (or use the LLM to create mock data records that correspond to the LLM for testing purposes).
    
-   SHACL can be used in conjunction with Mermaid.js and other graphing languages to build data model diagrams, graphs, and flowcharts. I frequently model a particular shape in Mermaid, then use it to generate SHACL; similarly, the SHACL can be used in conjunction with its associated RDF datasets for various visualisations (typically via an LLM such as Claude or Deepseek).
    
-   Finally, SHACL is an effective way to specify all kinds of domain-specific languages (DSLs). This will also be part of an upcoming post.
    

It is likely that as the SHACL language matures, there will be more areas where SHACL will be utilised, mainly as you can express SHACL as JSON-LD quite readily.

Shape-based thinking, centred on querying and manipulating molecules of data that represent different interpretations of how data is assembled, will shift how ontologies are built (and how data is modelled in general). I don’t necessarily see this as an either/or about whether OWL or SHACL is superior — they both have their uses - but I see SHACL at this point evolving in such a way that it will largely subsume and replace most of the logical formalisms of OWL, while retaining a more structured focus (especially with the work being down with inferencing in the upcoming SHACL 1.2).

In Medieval Res,

[

![](https://substackcdn.com/image/fetch/$s_!GKpq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5308ad33-e613-49c5-9efd-35b9c140871b_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!GKpq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5308ad33-e613-49c5-9efd-35b9c140871b_2688x1536.png)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please contact me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please consider contributing to support my work and allow me to continue writing.