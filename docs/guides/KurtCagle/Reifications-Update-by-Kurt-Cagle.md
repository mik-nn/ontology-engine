---
title: "Kurt Cagle"
source: "https://substackcdn.com/image/fetch/$s_!uFS1!,w_1200,h_400,c_pad,f_auto,q_auto:best,fl_progressive:steep,b_auto:border,b_rgb:FFFFFF/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60c6d44f-8b5b-406a-8818-94d79cd28fc2_1024x1024.png"
date: ""
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!JktM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc10c6c72-a84c-491e-8948-78d1e71e8e22_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!JktM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc10c6c72-a84c-491e-8948-78d1e71e8e22_2688x1536.jpeg)

I am rather notorious for getting involved with working and standards groups, becoming heavily focused on certain approaches, then getting sidetracked to other endeavours. I think it’s an artefact both of trying to keep up-to-date on a lot of different tech and also just my own natural ADHD tendencies kicking (oooh, shiny!), coupled with the fact that I’m not independently wealthy, so everything has to be done around trying to just find work to keep a roof over my head while I do so.

One thing I’ve been watching for a while now is the debate in the RDF-Star working group about how to represent reifications. I’ve had my own proposals, and there have been many others over the last few years, but it appears to me that an emerging consensus is now forming, one that I suspect will be where reifications are headed in the future.

RDF has had reifications from the beginning. The original RDF specification discusses reifications, defining a reification as a means of describing triples. However, the mechanism for doing so at the time was both cumbersome to work with in RDF (requiring three additional triples for each assertion) and programmatically inefficient. It’s been my contention for a while that part of this is that there is a distinction between RDF and Turtle here, and that when you get right down to it, the Turtle notation for RDF is the real culprit.

That’s not completely the case, mind you - you also need a way to encode reifications within knowledge graph engines efficiently, and a lot of the reason that vendors didn’t LIKE reifications was because it required a core change to how THEY had implemented RDF in the first place. However, this argument has largely been resolved in a wider variety of systems, as processor speeds and memory availability have both improved dramatically since the early 2000s.

## Expressing RDF Reifications

There are currently two different ways of expressing RDF reifications, one fairly stable, another more recent (and in many respects more flexible). The first one is the use of the double angle bracket format << and >> , which encompasses a triple:

```
<< :liz :married :richard >> :accordingTo :bob .
```

The double angle notation is a way of saying “this expression is a reified triple". What does this mean exactly? A reified triple can be thought of as a triple that is being discussed but not necessarily asserted to be true. Put another way, it isn’t asserted as a triple in the active graph. It would be like saying:

```
<< :theMoon :isMadeOf :greenCheese >> :accordingTo :mike .
```

There is no explicit statement in the graph that says that the Moon is made of green cheese, only Mike’s contention that this COULD be an assertion. This is equivalent to the more cumbersome set of statements:

```
_:b1 rdf:subject :theMoon ;
     rdf:predicate :isMadeOf ;
     rdf:object :greenCheese ;
     .
```

I made the distinction at one point in the RDF-star working group that you could say this assertion hasn’t been indexed directly; if you go looking for it in the graph, it’s not there, not directly. This has been a point of contention about reification for some time now.

On the other hand, you can assert this statement directly, then create a reification of the statement:

```
:theMoon :isMadeOf :greenCheese . 
     # Asserts that the moon is made of green cheese
<< :theMoon :isMadeOf :greenCheese >> :accordingTo :mike .
     # Asserts that the statement just made was made by :mike .
```

In this case, the original assertion IS in the graph, where the reification then provides commentary (an annotation) about that assertion. You can break this down even further:

```
:theMoon :isMadeOf :greenCheese . 
_:b1 rdf:subject :theMoon ;
     rdf:predicate :isMadeOf ;
     rdf:object :greenCheese ;
     .
_:b1 :accordingTo :mike .
I 
```

This first statement is the assertion being made in the graph. The second group of assertions identifies a blank node \_:b1 that can identify the components of this assertion, while the final statement indicates that the blank node (a reifier) of the original statement was made according to :mike .

The problem with this is that you can create multiple reifiers for the same subject, predicate, and object. Put another way, different people may have different annotations that they want to make about the same triple. This is illustrated as follows:

```
:theMoon :isMadeOf :greenCheese . 
     # Asserts that the moon is made of green cheese
<< :theMoon :isMadeOf :greenCheese >> :accordingTo :mike .
     # Asserts that the statement just made was made by :mike .
<< :theMoon :isMadeOf :greenCheese >> :refutedBy :jane .
     # Asserts that the statement just made was refuted by :jane .
```

This decomposes as:

```
:theMoon :isMadeOf :greenCheese . 
_:b1 rdf:subject :theMoon ;
     rdf:predicate :isMadeOf ;
     rdf:object :greenCheese ;
     .
_:b2 rdf:subject :theMoon ;
     rdf:predicate :isMadeOf ;
     rdf:object :greenCheese ;
     .
_:b1 :accordingTo :mike .
_:b2 :refutedBy :jane .
I 
```

Each of the angle-bracketed reifications has the same subject, predicate and object. However, the annotations were made by different people at different times (and more importantly, were added independently of one another), so there are, in fact, two reifications of the same statement. This is also fairly cumbersome.

## Introducing Named Anonymous Nodes

The crux of the problem lies in the fact that the double angle brackets, by themselves, involve _**anonymous nodes[1](https://substack.com/@kurtcagle/p-189271561#footnote-1-175325025)**_. An **anonymous node** is a node created by the system that is inaccessible to subsequent assertions. The use of bracket notation also suffers from this - when you use a bracket to indicate a blank node, then there is no way that you can refer to that bracket directly by name, even locally. For instance:

```
:recording :hasInterval 
      [ a :Interval ;
        :start "03:01:25"^^xsd:time; 
        :end "03:12:17"^^xsd:time;
      ],[
        a :Interval ;
        :start “05:23:14”^^xsd:time; 
        :end “06:01:19”^^xsd:time;
      ].
```

There is no way that you can explicitly reference either of these two intervals in Turtle (you can in SPARQL, of course, but only indirectly).

With RDF 1.2, a new operator, the naming operator, was introduced, with the syntax `~ :name` . For instance,

```
:theMoon :isMadeOf :greenCheese . #1
<< :theMoon :isMadeOf :greenCheese ~ _:b1>> :accordingTo :mike . #2
<< :theMoon :isMadeOf :greenCheese ~ _:b2>> :refutedBy :jane . #3
_:b1 :madeOn "2025-07-05"^^xsd:date . #4
_:b2 :madeOn "2025-09-3"^^xsd:date . #5
```

In this case, I’ve made an assertion (#1) that the moon is made of green cheese. In #2, a reification of the statement was made by Mike (referenced as the \_:mikeNode blank node), and in #3, another reification was made, indicating the statement was refuted by Jane. In #4 and #5, additional information is added about the first and second reifications, respectively.

I would argue that the ~ operator is actually assigning a formal name to an anonymous blank node. At the moment, this is used only for reifications (which produce such anonymous blank nodes), but it could (and IMHO should) be extended to bracket blank nodes as well.

There is another form of this notation which combines both the assertion and the reification, and this uses the {| |} operator. The simpler form of this notation looks something like the following:

```
:theMoon :isMadeOf :greenCheese {|:accordingTo :mike |} .
```

This notation let’s you assert that the moon is made of green cheese, but also indicates that there is an implicit reification of that statement with everything in the {| |} brackets being annotations on that reification - in effect, the triple has an implicit blank node reifier, and the curly brace identifiers act like square bracket blank nodes, with the reifier then being the subject for each statement.

However, as with the angle braces, you can also create a named identifier for the anonymous node. This can be seen in the following example:

```
:theMoon :isMadeOf :greenCheese ~ _:b1 {| :accordingTo :mike |} .
_:b1 :madeOn “2025-07-05”^^xsd:date
     
```

In this case, the triple is asserted, and then the named operator indicates that the reification of the statement (as a blank node) has the formal name \_:b1. Anything within the brackets is then an assertion on \_:b1. This allows for both assertion and reification without the bracket notation.

This can be extended by adding another naming operator:

```
:theMoon :isMadeOf :greenCheese 
    ~ _:b1 {| :accordingTo :mike |}
    ~ _:b2 {| :refutedBy :jane |}.

_:b1 :madeOn “2025-07-05”^^xsd:date .
_:b2 :madeOn “2025-09-3”^^xsd:date .
```

This can also be written as

```
:theMoon :isMadeOf :greenCheese 
    ~ _:b1 {| :accordingTo :mike ; :madeOn “2025-07-05”^^xsd:date ; |}
    ~ _:b2 {| :refutedBy :jane ; :madeOn “2025-09-3”^^xsd:date |}.
```

This notation packs a lot of information in a very compact form. This can be fully decomposed as:

```
:theMoon :isMadeOf :greenCheese .
_:b1 rdf:subject :theMoon ;
     rdf:predicate :isMadeOf ;
     rdf:object :greenCheese ;
     .
_:b2 rdf:subject :theMoon ;
     rdf:predicate :isMadeOf ;
     rdf:object :greenCheese ;
     .
_:b1 :accordingTo :mike ;
     :madeOn  “2025-07-05”^^xsd:date ;
     .
_:b2 :refutedBy :jane ;
     :madeOn “2025-09-3”^^xsd:date ;
     .
```

Now, because what you’re doing here is naming a previously anonymous node, this COULD also be extended to blank nodes with the same notation:

```
# Turtle Non-standard!
:recording :hasInterval 
       ~ :i3 [a :Interval ;
        :start “03:01:25”^^xsd:time; 
        :end “03:12:17”^^xsd:time; 
      ] ,  ~ :i4 [
        a :Interval ;
        :start “05:23:14”^^xsd:time; 
        :end “06:01:19”^^xsd:time;
      ].

:i3 :accordingTo :jane .
:i4 :accordingTo :mike .
```

In this case, it simply adds the later assertions to the blank node entities:

```
# Turtle Non-standard!
:recording :hasInterval 
       ~ :i3 [a :Interval ;
        :start “03:01:25”^^xsd:time; 
        :end “03:12:17”^^xsd:time; 
        :accordingTo :jane ;
      ] ,  ~ :i4 [
        a :Interval ;
        :start “05:23:14”^^xsd:time; 
        :end “06:01:19”^^xsd:time;
        :accordingTo :mike ;
      ].
```

This is not in the current specification, though it probably should be, as it’s the same operation (naming an otherwise anonymous blank node) in both cases. This also makes it structurally closer to JSON:

```
// JSON
"recording":{"hasInterval":[ 
       {"i3": { "a": ":Interval" ,
         "start": “03:01:25”^^xsd:time, 
         "end": “03:12:17”^^xsd:time, 
         "accordingTo": ":jane" ;
         }},  
       {"i4": { "a": ":Interval"
        "start": “05:23:14”^^xsd:time; 
        "end": “06:01:19”^^xsd:time;
        "accordingTo": ":mike" ;
      }}
   ]}
```

## Implications of Reification Notation

While it is sometimes derided as syntactical sugar, the use of the naming notation and condensed reification forms can simplify the writing of Turtle, especially with regard to reifications.

For instance, consider a store that is open certain days, but those days change over specific intervals. This is one of those cases where you could model it a number of different ways, but a reifier could help dramatically. Start with a basic assertion:

```
VERSION     “1.2”
PREFIX :    <http://www.example.org/>

:myStore :isOpen true ~ _:summer {|
      a :DaysList ;
      :storeDays ("monday" "tuesday" "wednesday" "thursday" "saturday");
      :from "2025-06-01"^^xsd:date ;
      :to "2025-08-31"^^xsd:date ; |} 
    ~ _:fall {|
      a :DaysList ;
      :storeDays ("monday" "tuesday" "wednesday" "thursday" "friday" "saturday" "sunday") ;
      :from “2025-09-01”^^xsd:date ;
      :to “2025-11-30”^^xsd:date ; |} 
    ~ _:winter {|
      a :DaysList ;
      :storeDays ( "tuesday" "wednesday" "thursday" "friday") ;
      :from “2025-12-01”^^xsd:date ;
      :to “2026-02-28”^^xsd:date ; |} 
      .
```

First, note that the use of the VERSION “1.2” prolog statement. This tells the turtle parser to use RDF 1.2 parsing rules.

Each of the reifications covers a different interface, summer 2025, fall 2025, winter 2025-26, and specifies which days the store is open.

Before getting into querying, there’s a question here about whether this is the best data model. _Every reification can be modelled without reification._ In this particular case, you could invert the store entry around DaysList as follows:

```
[] a :DaysList ;
     :hasStore :myStore ;
     :storeDays (”monday” “tuesday” “wednesday” “thursday” “saturday”);
     :from “2025-06-01”^^xsd:date ;
     :to “2025-08-31”^^xsd:date ;
     . 

[] a :DaysList ;
     :hasStore :myStore ;
     :storeDays (”monday” “tuesday” “wednesday” “thursday” “friday” “saturday” “sunday”) ;
     :from “2025-09-01”^^xsd:date ;
     :to “2025-11-30”^^xsd:date ;
     . 
[] a DaysList ;
     :hasStore :myStore ;
     :storeDays (“tuesday” “wednesday” “thursday” “friday”) ;
     :from “2025-12-01”^^xsd:date ;
     :to “2026-02-281”^^xsd:date ;
     .
```

However, what this does is decouple the obvious relationship between a given store (you may have multiple stores) and the days the store is open. If the data is entered all at once, then this might be worth decoupling, but if stores are entered as distinct entities (which is more likely to be the case), then going the reification route might very well be worth it, as you can group your data into clear records. In those cases where you have a number of potential states (not just open and closed, which can be represented as a binary), the organisational benefits of reification become even more obvious.

Querying the data shows how reification works in SPARQL (this is SPARQL 1.2, so it probably hasn’t made its way into engines yet, though the TRIPLE() function may have):

```
VERSION “1.2”
PREFIX : <http://example/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fn: <http://www.w3.org/2005/xpath-functions#>

SELECT ?store ?day ?isOpenThisDay {
    values (?store ?date) {( :myStore "2025-07-03"^^xsd:date)}
    ?store :isOpen true .
    BIND( <<(  ?store :isOpen true)>> AS ?tt )
    ?tt :from ?from .
    ?tt :to ?to .
    filter(?date >= ?from && ?date <= ?to)
    ?tt :storeDays :?list .
    ?list rdf:rest*/rdf:first ?day.
    bind(fn:format-date(xs:date(?date),”[F]”) = ?day as ?isOpenThisDay)
    filter(?isOpenThisDay)
    }
```

This will retrieve the days of the week that the store is open on for that particular date (here: `”monday” “tuesday” “wednesday” “thursday” “saturday”).`

The statement

```
<<(  ?store :isOpen true)>>
```

extracts the reification(s) for that particular triple and assigns each to ?tt . This, in turn, becomes the blank node for the particular instance of the daysList.

The final bind statement uses the format-date function from XQuery (which is usually supported by SPARQL implementations) by passing a “picture” string that configures a formatted output string. In this case, it uses the dayOfWeek \[F\] picture string to retrieve the day of the week for the given date, which can then be compared with the list of open days to indicate whether the store is open that day, and is stored in the `?isOpenThisDay` variable. It is a fairly simple exercise to extend this to specific hours for each day, and to exempt certain holidays, one I leave to the reader.

A key benefit of the {| |} notation is that you can use it without having to break the subject context, which is more difficult when working with the «» notation. For instance, the above declaration can be extended as follows:

```
VERSION     “1.2”
PREFIX :    <http://www.example.org/>

:myStore
   a :Store ;
   :location "123 Sesame St., NY, NY, 00123" ; 
   :isOpen true ~ _:summer {|
       a :DaysList ;
       :storeDays (”monday” “tuesday” “wednesday” “thursday” “saturday”);
       :from “2025-06-01”^^xsd:date ;
       :to “2025-08-31”^^xsd:date ; |} #... more reifications
       ;
   # ... more properties
   .
```

As a general rule of thumb, include a class declaration (such as `_:summer a :DaysList;` here) to indicate the class being represented by the reification.

## Routes and Inverting Graphs

There are several benefits to doing this. For instance, consider an airline route map expressed in this way:

```
airport:SEA a :Airport ;
    airport:routesTo airport:SFO ~ route:SEASFO {|
        a :Route ;
        route:carrier carrier:BigSkyAirlines ;
        route:number "18259"^^xsd:integer ;
        route:duration "P02:21"^^xsd:dayTimeDuration;
        route:contraRoute route:SFOSEA ;
        |},
    airport:LAX ~ route:SEALAX {|
       a :Route ;
        route:carrier carrier:BigSkyAirlines ;
        route:number “7253”^^xsd:integer ;
        route:duration “P03:55”^^xsd:dayTimeDuration;
        route:contraRoute route:LAXSEA ;
        |},
    airport:DEN ~ route:SEADEN {|
       a :Route ;
        route:carrier carrier:ColumbinaAirlines ;
        route:number “118”^^xsd:integer ;
        route:duration “P03:17”^^xsd:dayTimeDuration;
        route:contraRoute route:DENSEA ;
        |};
   .

airport:SFO a :Airport ;
    :routesTo airport:SEA ~ route:SFOSEA {|
        a :Route ;
        route:carrier carrier:BigSkyAirlines ;
        route:number “18260”^^xsd:integer ;
        route:duration “P02:21”^^xsd:dayTimeDuration;
        route:contraRoute route:SEASFO ;
        |},
     # ...
     .
```

The named reifier syntax essentially allows you to create subordinate structures that nonetheless have identifiers. In the above example, for instance, the reifiers create _routes_ with referenceable names. Since each route is reified relative to a specific starting airport, this means that you can independently define the routes. In the above example, for instance, this can be rewritten as:

```
airport:SEA a :Airport ;
    airport:routesTo airport:SFO ~ route:SEASFO ,
        airport:LAX ~ route:SEALAX ,
        airport:DEN ~ route:SEADEN ;
    .

route:SEASFO
        a :Route ;
        route:carrier carrier:BigSkyAirlines ;
        route:number “18259”^^xsd:integer ;
        route:duration “P02:21”^^xsd:dayTimeDuration;
        route:contraRoute route:SFOSEA ;
        .
route:SEALAX
        a :Route ;
        route:carrier carrier:BigSkyAirlines ;
        route:number “7253”^^xsd:integer ;
        route:duration “P03:55”^^xsd:dayTimeDuration;
        route:contraRoute route:LAXSEA ;
       .

route:SEADEN
       a :Route ;
       route:carrier carrier:ColumbinaAirlines ;
       route:number “118”^^xsd:integer ;
       route:duration “P03:17”^^xsd:dayTimeDuration;
       route:contraRoute route:DENSEA ;
       .
# ... same for other airports.
```

A query that asked for all routes as instances of :Route would return route objects independent of the airports. On the other hand, you can retrieve both the starting and ending airport by using the subject() and object() function on the reifier:

```
# SPARQL 1.2
select ?routeNumber ?start ?end where {
    ?route a :Route .
    bind(subject(?route) as ?start)
    bind(object(?route) as ?end)
    ?route route:number ?routeNumber . 
}
```

Put another way, such reification patterns are often highly efficient when you have graph networks that alternate between the same node types and property types. You can, in effect, invert the graphs so that the nodes and edges swap places (routes are connected by airports, rather than airports being connected by routes). These kinds of patterns occur all the time - family trees (people and marriages), highway maps (roads and municipalities), chemical pathways (molecules and reactions), organisational charts (people and reporting structures), and so many more.

This is likely to be one of several patterns that reification opens up. These structures were possible before, but because, in many cases, they are effectively echoes of third or fourth normal form structures, they were not always cleanly implemented in data models.

## Movie Chains and Versioning

Another pattern that you see frequently is the movie chain issue. For instance, in the Harry Potter movie series, you have characters such as Dumbledore, played by several different actors, who may appear in overlapping movies. This can be modelled in RDF, but it often tends to get complicated. However, with reification, you can make statements such as:

```
movie:HP1 movie:hasCharacter character:Dumbledore ~ movieCharacter:HP1-Dumbledore {| a :MovieCharacter ; movieCharacter:playedBy actor:RichardHarris |} 

movie:HP2 movie:hasCharacter character:Dumbledore ~ movieCharacter:HP2-Dumbledore {| a :MovieCharacter ; movieCharacter:playedBy actor:RichardHarris |} 

movie:HP3 movie:hasCharacter character:Dumbledore ~ movieCharacter:HP3-Dumbledore {| a :MovieCharacter ; movieCharacter:playedBy actor:MichaelGambon |}
```

In this particular case, all three movies feature the same book character, but because Harris died before the third movie started filming, the directors changed the actor for the third film to Michael Gambon.

Additionally, there is a distinction between a book character and a movie character, along with different annotations that may be added for each particular portrayal. The named reifier effectively provides an efficient mechanism for creating different versions, adding specific metadata as it becomes known, something that is far more typical when dealing with document-like data.

Versioning is a critical part of any data model, but it is often not well addressed, except in the simplest cases. This is typically indicative of object-focused rather than subject-focused reifications. A movie-character “table”, for example, is a way of expressing specific “versions” of characters that are tied to a particular film or similar medium, even when that character spans multiple different films. Again, this is an example of a pattern that can be modelled without reification, but becomes easier to work with if you do use it.

This is also a pattern that labelled property graphs do particularly well (they actually assume an anonymous reifier in their data model, even though this may not have been intentional). With RDF-Star and named reifiers, this becomes much easier to incorporate into the RDF stack as well.

## Is Reification Bad RDF Design?

I’ve received a couple of comments recently from other ontologists who question whether reification is a good design choice for RDF. I’ve been thinking about this a lot recently.

I think if you arbitrarily put properties into a reification graph, then what you’re going to get out of it is a hole in your design where there are effectively no constraints. This is not exclusive to reification, by the way. Any time that you allow for open-ended properties without some degree of discipline, you’re going to eventually end up with something unmanageable.

This is part of the reason why I think it’s important that whenever you create a reification graph, that graph should incorporate some kind of signal indicating the interface that the graph should use. For instance, in the airport model, the first statement that is contained in the reifications is the one declaring that the reification should be treated as a route. This means that if you have a constraint language applied to the reification, such as SHACL, then there exist shapes for a Route class and associated properties that can be applied to a reifier.

Put another way, a reifier is simply a node that by itself has no semantics beyond the associations to an assertion’s subject, predicate and object. It is the designer of the ontology who can determine what constitutes a valid assignment for that node.

In [https://www.datashapes.org/reification.html](https://www.datashapes.org/reification.html) (part of the datashape, or dash: documentation), there is a proposal for handling reifications, using the `dash:reifiableBy` property. For instance, in the Airport SHACL, you may have a property shape as follows:

```
ex:AirportShape-routesTo
    a sh:PropertyShape ;
    sh:path airport:routesTo ;
    sh:nodeKind sh:IRI ;
    sh:class :Airport ;
    dash:reifiableBy :RouteShape .  
```

The airport:routesTo predicate binds to a class, but the dash:refiableBy predicate indicates what the reifier’s shape is. This can, in turn, be defined as follows:

```
# Turtle SHACL
:RouteShape a sh:NodeShape ;
     sh:targetClass :Route ;
     sh:excludeProperties 
     sh:property [
          a sh:PropertyShape ;
          sh:path route:carrier ;
          sh:nodeKind sh:IRI ;
          sh:minOccurs 1;
          sh:maxOccurs 1;
          sh:class :Carrier ;      
      ],[
          a sh:PropertyShape ;
          sh:path route:number ;
          sh:nodeKind sh:Literal ;
          sh:minOccurs 1;
          sh:maxOccurs 1;
          sh:datatype xsd:integer ;      
      ],[
          a sh:PropertyShape ;
          sh:path route:duration ;
          sh:nodeKind sh:Literal ;
          sh:minOccurs 1;
          sh:maxOccurs 1;
          sh:datatype xsd:dayTimeDuration ;      
      ],[
          a sh:PropertyShape ;
          sh:path route:contraRoute ;
          sh:nodeKind sh:IRI ;
          sh:minOccurs 0;
          sh:class :Route ;      
      ] .
```

What this means is that the reifier must conform to :RouteShape in order to be considered valid (and by extension, must have the four predicates route:carrier, route:number, route:duration, and route:contraRoute). Note that this only applies the triples that have airports as subject and object and a predicate of airport:routesTo. Any other kinds of triples would have different reifiers.

Note also that if inheritance is involved, and all classes evolve from a class such as rdfs:Class and all predicates from rdf:Property then you could make a general reification for annotations, meaning that every reification inherits from the :Annotation class. The upshot of this is that if annotation includes the properties annot:label, annot:description, annot:starts, annot:ends, and annot:reportedBy, then your reification graph might look something like:

```
airport:SEA a :Airport ;
    airport:routesTo airport:SFO ~ route:SEASFO {|
        a :Route ;
        route:carrier carrier:BigSkyAirlines ;
        route:number “18259”^^xsd:integer ;
        route:duration “P02:21”^^xsd:dayTimeDuration;
        route:contraRoute route:SFOSEA ;
        annot:label "Seatle to San Francisco Route" ;
        annot:description "This is the flight from Seattle to San Francisco" ;
        annot:starts "2021-03-02"^^xsd:date ;
        annot:reportedBy person:JaneDoe ;
        |}, ...
```

One way of looking at it is that with dash:reifiableBy, it becomes possible to make reifications an important (and testable) part of the model, rather than simply a potential hodgepodge of properties with no consistent rhyme or reason in their use.

Will this style result in poor design? I think it will lead to a different way of thinking about design, one that is more document-centric than the current best practices would recognise, but not necessarily any worse than what exists now.

## Conclusion

The rdf-star spec (and the corresponding Turtle, SPARQL, and SHACL specs) are all moving into their final end-game configuration. I personally would have chosen a different symbol than the tilda (~) (I like the “->” symbol myself) but overall, I think that the use of an anonymous node identifier for reification is fundamentally sound. That SPARQL and SHACL both have considerations for the use of such reification is encouraging as well; it means that reification can become a key part RDF data model within the next year or so (platforms such as Jena are already incorporating these changes now).

I’m looking forward to seeing what will emerge from all of this.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!hmVg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee305764-ba77-46fb-9ea3-4d5281d7761d_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!hmVg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee305764-ba77-46fb-9ea3-4d5281d7761d_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please contact me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please consider contributing something to support my work, allowing me to continue writing.

[1](https://substack.com/@kurtcagle/p-189271561#footnote-anchor-1-175325025)

I should clarify that the term **anonymous node** is mine, not the working group’s. An anonymous node is one that arises in Turtle when you use any kind of blank node operator (such as bracketed expressions or, in this case, reification) that introduces a node that can’t be referenced even locally as a blank node. This means that you have to either create an explicit reference to the node that terminates the structure and then define that node elsewhere (losing the benefit of being able to create more document-like structures) or you simply use bracket notation and lose the benefit of referencing it outside of the scope of the block. This is a Turtle problem, not an RDF problem.