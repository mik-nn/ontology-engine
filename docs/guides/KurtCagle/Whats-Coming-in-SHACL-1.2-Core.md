---
title: "What Does SHACL Do?"
source: "https://ontologist.substack.com/p/what-does-shacl-do?utm_source=profile&utm_medium=reader2"
date: "Mar 19"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!v4Dj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b6502db-f1b1-4234-86df-6cae08512428_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!v4Dj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b6502db-f1b1-4234-86df-6cae08512428_2688x1536.jpeg)

[In my first post in this series](https://ontologist.substack.com/p/whats-coming-in-shacl-12-core-part), I examined several new object classes in SHACL 1.2, including Shape classes, SHACL Lists, and Reification Shapes. The second post explores [node expressions and dynamic SHACL](https://ontologist.substack.com/p/whats-coming-in-shacl-12-core-part-870). This, the final post in the series, will examine custom functions, SHACL-SPARQL, Named Graphs, Compact SHACL, and other intriguing developments in the world of SHACL 1.2.

## Custom Named Parameter Functions

One of the more frustrating aspects of SPARQL is that there is no intrinsic way within the language itself to define functions. There is a _weak_ mechanism in the SPARQL specification for passing external functions in, though it is not consistently implemented, and in general, the assumption is that such functions need to be a part of the SPARQL engine, not the SPARQL language.

SHACL finally addresses this by providing a mechanism to define functions within the underlying SHACL model. One direct implication is that you can define libraries of functions that multiple systems can utilise, and consequently provide interfaces for implementing these functions across platforms. If nothing else, this is a huge step forward for RDF-based systems.

A function is defined with both parameters and a corresponding body. For instance, consider a function that calculates an average.

```
ex:AverageExpression
    a sh:NamedParameterExpressionFunction ;
    rdfs:label “Average expression”@en ;
    rdfs:comment “Computes the average of the nodes provided by ex:average.” ;
    rdfs:subClassOf sh:NamedParameterExpression ;
    sh:parameter ex:AverageExpression-average ;
    sh:bodyExpression [
        sparql:divide (
            [ shnex:sum [ shnex:arg ex:average ] ]
            [ shnex:count [ shnex:arg ex:average ] ]
        )
    ] ;
.
ex:AverageExpression-average
    a sh:Parameter ;
    sh:path ex:average ;
    sh:name “average” ;
    sh:description “The nodes of which the average shall be computed.” ;
    sh:keyParameter true ;
.
```

In this particular case, the function is a `sh:NamedParameterExpressionFunction` with one parameter, defined in `ex:AverageExpression-average`, which contains as an argument a sequence of nodes, identified by the path `ex:average`. In the body (the `sh:bodyExpression`) the calculations are then performed, first by performing a sum on the nodes, then dividing this by a count on the same nodes.

The parameter itself is defined here independently through the `ex:AverageExpression-average` `sh:Parameter`. It is a key parameter, which means that the `sh:path` of the parameter is used to identify the parameter within the body itself. For instance, a function can calculate the average income from salaries as follows:

```
ex:CompanyShape-averageIncome
    a sh:PropertyShape ;
    sh:path ex:averageIncome ;
    sh:datatype xsd:decimal ;
    sh:values [
        ex:average [
            shnex:pathValues ( ex:employee ex:income )
        ]
    ] .
```

This is a calculated property that would set the ex:averageIncome predicate in the output to the average with a corresponding skew value.

## List Parameter Expressions and `sh:arg`

This is just one form of a function, however. A simpler one can be seen with a function that takes two parameters and inserts a space between them:

```
ex:spacedConcat
    a sh:ListParameterExpressionFunction ;
    rdfs:label “Spaced concat expression”@en ;
    rdfs:subClassOf sh:ListParameterExpression ;
    sh:bodyExpression [
        sparql:concat (
            [ shnex:arg 0 ]
            “ “
            [ shnex:arg 1 ]
        )
    ] .
```

In this case, the parameters are referenced not by name but by position, as given by the `shnex:arg` predicate.

This would then be invoked as follows:

```
ex:Person-fullName
    a sh:PropertyShape ;
    sh:path ex:fullName ;
    sh:datatype xsd:string ;
    sh:values [
        ex:spacedConcat (
            [ shnex:pathValues ex:firstName ]
            [ shnex:pathValues ex:lastName ]
        )
    ] .
```

Here, the target node is an instance of type `ex:Person`, with two internal states `ex:firstName` and `ex:lastName`, which generates a sh:fullName property that concatenates the two as a string with a space between them. This approach is useful when you’re dealing with singleton values rather than sequences of nodes.

A similar approach can be used with the function current age, which takes a date-time as an argument and returns the period (in years) between that time and now, whatever that is at the moment:

```
ex:current-age
    a sh:ListParameterExpressionFunction ;
    rdfs:label “Current Age”@en ;
    rdfs:subClassOf sh:ListParameterExpression ;
    sh:bodyExpression [
        sparql:year ([
            sparql:minus (
                [ sparql:now () ]
                [ shnex:arg 0 ]
            )
       ])
    ] .
```

Thus, for ex:Person:

```
ex:Person as ex:ShapeClass ;
   ex:property ex:Person-birthDate, ex:Person-age ;
   .

ex:Person-birthDate
    a sh:PropertyShape ;
    sh:path ex:birthDate ;
    sh:datatype xs:gYear;
    .

ex:Person-age
    a sh:PropertyShape ;
    sh:path ex:age ;
    sh:datatype xs:gYearMonthDuration ;
    sh:values [
        ex:current-age (
            [ shnex:pathValues ex:birthDate ]
        )
    ] .
```

The data graph would look like the following:

```
# data graph
Person:JaneDoe a ex:Person ;
   ex:birthDate "2000-01-01"^^xs:date ;
   .
```

The output graph would look as follows:

```
# output graph
Person:JaneDoe a ex:Person ;
   ex:birthDate “2000-01-01”^^xs:date ;
   ex:current-age "25"^^xs:gYear . # added by the ex:current-year function.
   .
```

## SHACL-SPARQL Node Expressions

If your SHACL engine supports them, you can also use SPARQL queries as node expressions. For instance, rather than using SHACL functions, you can use SPARQL to generate the `ex:fullName` property, assuming that the `ex:Person` node shape defines `ex:firstName` and `ex:lastName` properties.

```
ex:Person-fullName
	a sh:PropertyShape ;
	sh:name "full name" ;
	sh:path ex:fullName ;
	sh:values [
		sh:prefixes <http://example.org/ns> ;
		sh:select """
			SELECT ?fullName
			WHERE {
				$this ex:firstName ?firstName .
				$this ex:lastName ?lastName .
				BIND (CONCAT(?firstName, " ", ?lastName) 
                                      AS ?fullName) .
			}
		"""
	] ;
	sh:datatype xsd:string .

<http://example.org/ns>
	a owl:Ontology ;
	sh:declare [
		sh:prefix "ex" ;
		sh:namespace “http://example.org/ns#”^^xsd:anyURI ;
	] .
```

In this case, the $this variable holds the IRI of the targetNode (here, an instance of person), and the first field in the SELECT statement represents the query result (if more than one item is returned, this returns an unordered list).

Within the `sh:values` source, you can see the property `sh:prefixes <http://example.org/ns>.` This contains a pointer to an ontology that includes namespace declarations, which are then passed to the SPARQL query. This is a handy feature because it lets you define all your namespaces in one place and retrieve them by reference, significantly reducing development effort and the risk of inconsistencies from manually entering them into SPARQL. Note also that this allows the system to retrieve all active namespace prefixes via SPARQL or SHACL, which is problematic with direct SPARQL calls.

This is also a good place to document WHAT each namespace is intended to represent. As someone who has spent days tracking down errant namespaces, I find additional documentation highly useful.

It is possible (though I can’t confirm this) that an SHACL-SPARQL expression can pass parameters into the bound SPARQL queries via the `sh:parameter` predicate, either in the property shape definition or as a value in the `sh:values` element. If that’s the case, then the local name of `sh:path` that property is used as the parameter (e.g., if the path is sh:firstName, then the SPARQL would set the value of the variable `?firstName` to the object node of the path). _I’ll update this section once I’ve verified it works._

## SPARQL Expressions

One other useful technique is to take advantage of the `sh:sparqlExpr` property. Used in `sh:values,` This property lets you evaluate a SPARQL expression as if it were part of a bind clause in SPARQL. For instance,

```
ex:Resource-uriLength
	a sh:PropertyShape ;
	sh:name "uri length" ;
	sh:path ex:uriLength ;
	sh:values [
		sh:sparqlExpr "STRLEN(STR($this))" ;
	          ] ;
	sh:datatype xsd:integer .
```

In this case, it takes the $this argument (bound to the focus node), converts it to a string from an IRI, then retrieves its length. This is functionally the same as:

```
ex:Resource-uriLength
	a sh:PropertyShape ;
	sh:name “uri length” ;
	sh:path ex:uriLength ;
	sh:values [
		sh:select """
			SELECT (STRLEN(STR($this)) AS ?result)
			WHERE {
			}
		""" ;
	] ;
	sh:datatype xsd:integer .
```

This can be used in conjunction with `sh:nodes` or `sh:pathValues` statements.

## SHACL and Named Graphs

Named graphs play an essential role in SHACL, separating model information from data. SHACL can be stored in the same graph as the data, but there are a few advantages to keeping it in a separate named graph:

-   A smaller named graph is more efficient for SHACL engines, resulting in better performance
    
-   A SHACL named graph can be cleared and loaded independently of the data set
    
-   Multiple SHACL named graphs can be configured to handle different operations (e.g., function libraries).
    

SHACL 1.2 adds a few capabilities to work more effectively with named graphs.

The `sh:shapesGraph` property identifies graphs in the graph space that should be used by a SHACL-aware engine:

```
<http://example.com/myDataGraph>
	sh:shapesGraph ex:graph-shapes1 ;
	sh:shapesGraph ex:graph-shapes2 .
```

This identifies all named graphs that should be treated as a union for SHACL operations. Exactly how this is utilised depends on the implementation, but it performs a role similar to `owl:imports`.

A parameter for the SHACL engine (`subClassOfInShapesGraph`) indicates whether `rdfs:subClassOf` statements should be stored in the data graph (the default) or the shape graph. This can be important if inferencing is enabled, as putting this information in the shape graph can make it more efficient to handle subclass relationships.

Similarly, the `sh:disabled` The flag in SHACL 1.2 can now take a node expression as its value, which is computed as a Boolean. It toggles specific node or property shapes under certain conditions (e.g., enabling or disabling message output for debugging, then disabling it for production systems).

## SHACL Compact Syntax

SHACL can seem daunting, especially when creating complex property shapes. One area of exploration for the working group has been to create a new compact syntax, one not based on Turtle, that can make it easier to write SHACL that can then be transformed into a full graph representation.

For instance, consider the following SHACL:

```
# Turtle SHACL
@base <http://example.com/ns> .
@prefix ex: <http://example.com/ns#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.com/ns>
	rdf:type owl:Ontology ;
	owl:imports <http://example.com/person-ontology> .

ex:PersonShape
	a sh:NodeShape ;
	sh:targetClass ex:Person ;
	sh:closed true ;
	sh:ignoredProperties ( rdf:type ) ;
	sh:property [
		sh:path ex:ssn ;
		sh:maxCount 1 ;
		sh:datatype xsd:string ;
		sh:pattern “^\\d{3}-\\d{2}-\\d{4}$” ;
	] ;
	sh:property [
		sh:path ex:worksFor ;
		sh:class ex:Company ;
		sh:nodeKind sh:IRI ;
	] ;
	sh:property [
		sh:path ex:address ;
		sh:maxCount 1 ;
		sh:nodeKind sh:BlankNode ;
		sh:node [
			sh:property [
				sh:path ex:city ;
				sh:datatype xsd:string ;
				sh:minCount 1 ;
				sh:maxCount 1 ;
			] ;
			sh:property [
				sh:path ex:postalCode ;
				sh:or ( [ sh:datatype xsd:integer ] [ sh:datatype xsd:string ] ) ;
				sh:minCount 1 ;
				sh:maxCount 1 ;
				sh:maxLength 5 ;
			] ;
		] ;
	] .
```

This creates a very simple person object, but it can still be daunting. The compact notation can look considerably cleaner and easier to understand:

```
# Compact SHACL
BASE <http://example.com/ns>

IMPORTS <http://example.com/person-ontology>

PREFIX ex: <http://example.com/ns#>

shape ex:PersonShape -> ex:Person {
	closed=true ignoredProperties=[rdf:type] . 

	ex:ssn       xsd:string [0..1] pattern=”^\\d{3}-\\d{2}-\\d{4}$” .
	ex:worksFor  IRI ex:Company [0..*] .
	ex:address   BlankNode [0..1] {
		ex:city xsd:string [1..1] .
		ex:postalCode xsd:integer|xsd:string [1..1] maxLength=5 .
	} .
}
```

Here, the core properties of most SHACL constructs (especially cardinality and similar constraints) are specified compactly, with each property constraint (such as pattern or max-length) then added as an attribute (very similar to XML, for what it’s worth). Blank node structures (such as arrays of addresses) are then identified by a BlankNode object, and indentation also looks a lot like YAML.

So far, relatively little of the more advanced SHACL 1.2 features have made their way into Compact SHACL, but they will, and they are handled via BNF production rules. This means that most BNF processors can readily parse them into a more tokenised form.

## Future SHACL

I have deliberately held off on writing about SHACL UI and SHACL Rules here, in part because they are relatively deep topics in their own right and in part because they are still very much works in progress. This series was also not an exhaustive look at SHACL 1.2, though I like to believe I’ve hit the high points.

SHACL takes a different approach to graphs than SPARQL. When you run a SPARQL query, each variable defines a value as part of a tuple. That tuple, in turn, is either used to generate a table or create another graph by filling in the specific values into a template of the tuple.

SHACL, on the other hand, is built mainly around iteration. In the validation case, this iteration returns reports; however, the process can also generate different types of output. Again, I think there is a very close correspondence between XSLT vs XQuery in the XML world and SPARQL vs SHACL in the RDF - both XSLT and SPARQL look at the structure as a graph focused on edges (the path as a series of joins) while the second looks at the same structure through the lens of iterations. Both are practical approaches that complement one another, as graphs are intrinsically multifaceted.

I hope you, gentle reader, have enjoyed this series, and I look forward to your feedback.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!a6tv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ac52d01-89e8-45f2-9e8b-d15dea736af9_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!a6tv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ac52d01-89e8-45f2-9e8b-d15dea736af9_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.