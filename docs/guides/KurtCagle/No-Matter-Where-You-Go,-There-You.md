---
title: "Dungeons & Declarations: What a Five-Room Game Reveals About Holonic Graph Architecture"
source: "https://inferenceengineer.substack.com/p/dungeons-and-declarations-what-a?utm_source=profile&utm_medium=reader2"
date: "Apr 4"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!K_Vo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff295d7d6-4d9b-40c1-a1cc-eac74f882c29_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!K_Vo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff295d7d6-4d9b-40c1-a1cc-eac74f882c29_2688x1536.png)

After posting my last article, I had a question from one of my readers:

> What’s the difference between context and perspective?”

This takes me back to one of my all time favorite movies (besides The Princess Bride), Buckaroo Banzai, when the eponymous character was about to start a set with his band:

<iframe src="https://www.youtube-nocookie.com/embed/OxvnWPIpKtU?rel=0&amp;autoplay=0&amp;showinfo=0&amp;enablejsapi=0" frameborder="0" loading="lazy" gesture="media" allow="autoplay; fullscreen" allowautoplay="true" allowfullscreen="true" width="728" height="409"></iframe>

The quote itself was, not surprisingly, not from the movie, but was instead attributed to the apocryphal philosopher Kong Qiu, known better in the Western World as Confucius. It is also, for me, one of my touchstone sayings, because it describes the world of graphs perfectly.

We tend to see the world of graphs from “above”, usually using what I call the tinkertoy view of graphs where you have nodes as balls connected by edges (sticks or strings). This view can be useful for comprehension, but in reality, this viewpoint, unfiltered, can also prove somewhat problematical, both because there is usually far more irrelevant information than relevant and because certain properties (such as generalized types) can often have far too many nodes to comfortable fit in a single diagram (at least without a magnifying glass)

[

![](https://substackcdn.com/image/fetch/$s_!b2P7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70e5cfbe-c2c8-4357-a434-e1029da85991_3249x3840.png)

](https://substackcdn.com/image/fetch/$s_!b2P7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70e5cfbe-c2c8-4357-a434-e1029da85991_3249x3840.png)

Realistically, however, what you are usually looking for with a graph is a shape representation of a resource or object.

For instance, consider this “basic” resume:

[

![](https://substackcdn.com/image/fetch/$s_!RPWu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffeec672-341b-437a-b631-4dd84f59bc41_3808x3840.png)

](https://substackcdn.com/image/fetch/$s_!RPWu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffeec672-341b-437a-b631-4dd84f59bc41_3808x3840.png)

Notationally, this is a graph, but it is a graph in which a lot of the semantics are implied by presentation. Here, Jane Doe has had two jobs - as Vice President then President of the company BigCo. This presentation makes use of several conventions:

[

![](https://substackcdn.com/image/fetch/$s_!5X_q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1605c4f-f544-4b78-a9fe-8c457fdc80f3_3840x2104.png)

](https://substackcdn.com/image/fetch/$s_!5X_q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1605c4f-f544-4b78-a9fe-8c457fdc80f3_3840x2104.png)

The item at the left plays the role of a _context object_ - it establishes a frame of reference around which everything else is built. In the above case, the context object is the person Jane Doe.

In this notation, I’ve pulled out the identifier as a separate entry (in teal, above). The identifier is a URI or similar form of GUID that identifies the resource in question. Unless it’s directly pertinent, the graph assumes that such an identifier has been declared already and is an implementation detail, so will usually be omitted. Thus, the single node primary data for the person Jane Doe would be represented in Turtle RDF as:

```
@prefix Person: <http://www.example.com/Person#> .
@prefix Class: <http://www.example.com/Class#> .
# Additional standard RDF declarations

Person:JaneDoe a Class:Person ;
    rdfs:label "Jane Doe" ;
    rdfs:comment "Here's the record about Jane Doe."^^xsd:string ;
.
```

The literal properties are properties such as strings or dates. In the example of Jane has the nickname of “Janey” (and in this example is assumed to static).

The oddment in the above graph is the object property (the dashed oblong). This is a property on an object, but it is also a thing. That thing is called a reification, and it basically describes specific instances of the thing represented by the property.

To continue with the example, the two employment objects can be represented as follows in RDF:

```
Person:JaneDoe a Class:Person ;
     Person:employedBy Company:BigCo;
.

# Reification 1
<<Person:JaneDoe Person:employedBy Company:BigCo>>
     a Class:Employment ;
     Employee:hasRole Role:VicePresident ;
     Employee:from "2017-03-01"^^xsd:date ;
     Employee:to "2021-05-02"^^xsd:date ;
     .

# Reification 2
<<Person:JaneDoe Person:employedBy Company:BigCo>>
     a Class:Employment ;
     Employee:hasRole Role:President ;
     Employee:from "2021-05-03"^^xsd:date ;
     .
```

Each reification has a distinct (blank node) identifier. For instance, reification 1 might have an identifier of `_:employment1`, reification 2 would be `_:employment2`, and so forth. Reification notation is defined in rdf-star, a W3C proposal that should be ratified later this year. Note that here, because the reifier is distinct (and not coincidentally, unique) even though the reified triple is the same, the reifier node is not.

This, by the way, is exactly the model employed by Neo4J. A property in Neo4J is in fact a reifier on the assertion of a relationship between two nodes. To put that into more understandable English, it’s worth showcasing the openCypher relationships:

```
/ Create nodes for JaneDoe and BigCo
CREATE (janeDoe:Person {uri: 'http://example.com/Person#JaneDoe'})
CREATE (bigCo:Company {uri: 'http://example.com/Company#BigCo'})

// Create the employment relationship between JaneDoe and BigCo
CREATE (janeDoe)-[:employedBy]->(bigCo)

// Create the first reification (Employment 1)
CREATE (employment1:Employment {
    uri: 'http://example.com/Employment#1',
    hasRole: 'http://example.com/Role#VicePresident',
    from: date('2017-03-01'),
    to: date('2021-05-02')
})
CREATE (janeDoe)-[:hasEmployment]->(employment1)
CREATE (employment1)-[:employedBy]->(bigCo)

// Create the second reification (Employment 2)
CREATE (employment2:Employment {
    uri: 'http://example.com/Employment#2',
    hasRole: 'http://example.com/Role#President',
    from: date('2021-05-03')
})
CREATE (janeDoe)-[:hasEmployment]->(employment2)
CREATE (employment2)-[:employedBy]->(bigCo)
```

The underlying models create an emplicit relationship `[:hasEmployment]` that binds the two reifiers to the overall assertion, and it should be noted that in general the distinction between a property and an object is a lot more fluid than you might expect.

In SPARQL the use of the « » operator become more obvious. Assuming the above namespaces, you can get information about the reified objects as follows:

```
#Sparql
select ?person ?role ?from ?to where {
values ?person {Person:JaneDoe}
bind(triple(?person,Person:employedBy,?company) as ?employment)
?employment Employment:hasRole ?role.
?employment Employment:from ?from.
optional {
         Employment:to ?to
    }
} order by ?from
```

This creates a table as follows:

[

![](https://substackcdn.com/image/fetch/$s_!yTcf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c4142f0-e40f-4f8c-bdd4-6b454abbd87e_1240x414.png)

](https://substackcdn.com/image/fetch/$s_!yTcf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c4142f0-e40f-4f8c-bdd4-6b454abbd87e_1240x414.png)

With respect to the sparql, the function

```
bind(triple(?person,Person:employedBy,?company) as ?employment)
```

will retrieve from the RDF all assertion reifiers that satisfy the three properties. There may of course be zero, one, or many such reifiers. It’s also worth noting that such reifiers are always blank nodes - they cannot be directly referenced via URIs, though they can be worked with in SPARQL. This actually turns out to have significant consequences, not least of which being that such reifications can only be retrieved indirectly - you always need a known context object’s URI to retrieve it’s reifications.

## Perspective and the Validity of State

I’ve talked in previous articles about state, but it’s worth reiterating here. There are two different interpretations of a graph, and they have very definite implications. In the first interpretation, every single assertion within the graph is true. When people first construct knowledge graphs, they often assume this interpretation by default - after all, why would you put information that wasn’t true into a knowledge graph?

The answer, surprisingly enough, is because a knowledge graph is not necessarily a traditional database. It can be used as such of course, in which case you probably do want to make sure every assertion is valid, but knowledge graphs are much more interesting if you assume that assertions are true if unqualified, but are true or false (or possibly some intermediate state) if .

For example, in the above example, let’s say that in the above example, Lizie was a Director of Engineering at a company called TechCo from 2013 to 2017. The statement that she was at TechCo at some point is true, but the statement that she was at TechCo in 2019 is likely false. In other words, external context dictates that the person held a particular job at a certain time, but did not hold it at other times.

Space and time are usually important contextual information, but they are not the only kinds of information. Authority, topicality, publishing status (draft, published, etc.), commentary, routing and so on all determine whether or not an assertion is valid. More specifically, they serve to limit or constrain validity of a given assertion, and a great deal of metadata can build up over time over any assertion.

The other critical aspect of such metadata is that it can overlap. For instance, there is nothing that specifically says in the model that Jane Doe could not in fact have been simultaneously doing both the President and Vice President job at BigCo, at least until she could hand off the VP responsibilities. This is a scenario that occurs all the time. The real world tends to be very messy, in this regard.

Indeed, once you start into a model where you have the ability to qualify the validity of statements, you enter a realm in which a lot of fundamental notions of modelling break down. For instance, consider cardinality, which is a concept that emerged from SQL relational modeling. How do you model the constraint that you can only be married to one person at any given time, but you may have multiple marriages (even to the same person)? This can’t easily be broken down into a minOccurs/maxOccurs ruleset, because clearly, you can have multiple marriages, just so long as temporal constraints are satisfied (or you are a citizen of a country where monogamy is not a legal requirement).

For instance, consider the following:

```
Person:John Person:married Person:Jane .
Person:John Person:married Person:Wendy .

<< Person:John Person:married Person:Jane >>
   a Class:Marriage ;
   Marriage:startYear 1995 ;
   Marriage:endYear 2005 ;
   .

<< Person:John Person:married Person:Wendy >>
   a Class:Marriage ;
   Marriage:startYear 2004 ;
   Marriage:endYear 2009 ;
   .
```

How can you tell at any given time if a given spouse is practicing bigamy? The solution is pretty simple in SPARQL, even with reifications:

```
select ?spouse1 ?spouse2 ?overlapStartYear ?overlapEndYear where {
     values ?person {Person:John}
     bind(triple(?person, Person:married, ?spouse1) as ?marriage1)
     bind(triple(?person, Person:married, ?spouse2) as ?marriage2)
     filter(!sameTerm(?spouse1,?spouse2))
     ?marriage1 Marriage:startYear ?m1StartYear.
     ?marriage1 Marriage:endYear ?m1EndYear.
     ?marriage2 Marriage:startYear ?m2StartYear.
     ?marriage2 Marriage:endYear ?m2EndYear.
     BIND(IF(?m1StartYear < ?m2EndYear && ?m2StartYear < ?m1EndYear, 
        MAX(?m1StartYear, ?m2StartYear), 
           NULL) AS ?overlapStartYear)

     BIND(IF(?m1StartYear < ?m2EndYear && ?m2StartYear < ?m1EndYear, 
        MIN(?m1EndYear, ?m2EndYear), 
           NULL) AS ?overlapEndYear)
     }
```

This logic can be applied to any person as a SHACL validation:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix Person: <http://example.org/Person/> .
@prefix Marriage: <http://example.org/Marriage/> .
@prefix Class: <http://example.org/Class/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

Class:Person
    a sh:NodeShape ;
    sh:targetClass Class:Person ;
    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:severity sh:Violation ;
        sh:message "Person {?personName} has overlapping marriages: {?marriage1Label} and {?marriage2Label}." ;
        sh:prefixes <http://example.org/> ;
        sh:select """
            SELECT $this 
                  (<< $this Person:married ?spouse1 >> AS ?marriage1)
                  (<< $this Person:married ?spouse2 >> AS ?marriage2)
                  (CONCAT(STR(?spouse1), " (", STR(?start1), "-", IF(BOUND(?end1), STR(?end1), "present"), ")") AS ?marriage1Label)
                  (CONCAT(STR(?spouse2), " (", STR(?start2), "-", IF(BOUND(?end2), STR(?end2), "present"), ")") AS ?marriage2Label)
                  (COALESCE(?personName, STR($this)) AS ?personName)
            WHERE {
                # Get person's name (if exists) for error message
                OPTIONAL { $this foaf:name ?personName }  # Assuming foaf:name exists

                # Get distinct marriage pairs
                $this Person:married ?spouse1, ?spouse2 .
                FILTER (?spouse1 != ?spouse2 || 
                       (<< $this Person:married ?spouse1 >> != << $this Person:married ?spouse2 >>))

                # Get marriage details (using RDF-star)
                << $this Person:married ?spouse1 >> a Class:Marriage ;
                    Marriage:startYear ?start1 .
                OPTIONAL { << $this Person:married ?spouse1 >> Marriage:endYear ?end1 } .
                
                << $this Person:married ?spouse2 >> a Class:Marriage ;
                    Marriage:startYear ?start2 .
                OPTIONAL { << $this Person:married ?spouse2 >> Marriage:endYear ?end2 } .

                # Check for temporal overlap (handling open-ended marriages)
                FILTER (
                    # Case 1: Both marriages have end dates
                    ((BOUND(?end1) && BOUND(?end2) && ?start1 < ?end2 && ?start2 < ?end1) ||
                    # Case 2: Marriage1 is open-ended
                    (!BOUND(?end1) && ?start2 < ?start1) ||
                    # Case 3: Marriage2 is open-ended
                    (!BOUND(?end2) && ?start1 < ?start2)
                )
            }
            GROUP BY $this ?marriage1 ?marriage2 ?start1 ?end1 ?start2 ?end2 ?spouse1 ?spouse2
            """ ;
    ] .
```

This showcases a number of different potential scenarios - marriages that overlap, marriages within marriages, non-coincident marriages, and so forth.

## Final Thoughts

Realistically, overlapping marriages are probably not all that common an occurrence. However, this points to a broader issue. Events do overlap in reality all the time. If you’re a consultant, for instance, the reality is that at any given time, you will almost certainly have multiple clients at various stages of completion, from just getting underway to actively engaged to maintenance-stage. This is one of the key reasons why consultants’ CVs seem to be so contradictory: overlaps are pretty much a given. This can be usually be resolved if you look at a consultant’s schedule from the standpoint of billing hours, but a CV very seldom gets that granular.

This is an important point to remember when dealing with the creation of models. Any model is a tradeoff between ease of use and granularity, not only in space but also in time. Both add complexity, but with the benefit of greater fidelity in understanding.

Additionally, it’s worth remembering that no model is perfect. There is always information you do not have, context that costs time, energy, and money to resolve, and in most cases, such models are also discrete rather than continuous. Even neural net models are, for the most part, linear equations. Reality, on the other hand, is not. Graphs are useful devices (and get at the core of topology, which is no small thing), but graphs are still discretised views of reality.

Nonetheless, graphs ARE useful devices, because they make it possible to help you model at least some approximation of context. For the ontologist, this is always a useful thing.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!Dqyr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8df238c3-93ca-4304-a744-88c8298b1f4c_2048x2048.png)

](https://substackcdn.com/image/fetch/$s_!Dqyr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8df238c3-93ca-4304-a744-88c8298b1f4c_2048x2048.png)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.