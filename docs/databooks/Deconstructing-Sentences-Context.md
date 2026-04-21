---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Deconstructing-Sentences-Context
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:48.143544+00:00'
  title: Deconstructing Sentences Context
  type: plain-doc
  version: '0.1'
---

# Deconstructing Sentences Context

[

![](https://substackcdn.com/image/fetch/$s_!wNfS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F552cb26a-56ca-4936-9e7c-3cce63482e47_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!wNfS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F552cb26a-56ca-4936-9e7c-3cce63482e47_2688x1536.jpeg)

Meet Jane Doe, Female Entrepreneur

Looking back, my first real encounters with graphs I remember date back to English class in junior high school. The teacher worked with us for about a week on documenting sentences. Most of the kids thought it was really pointless, but it stuck with me for some reason, and gave me my first inkling that language and graphs were intimately related.

Consider the following sentence:

```
Jane Doe, a person, worked as an accountant for BigCo, a company that manufactured widgets (part of their product line) from 2012 to 2021. 
```

The graph for this is directed, starting with an implicit root node (Sentence):

[

![](https://substackcdn.com/image/fetch/$s_!XegV!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34d38c28-a8b4-4618-8f18-3dd72262603e_6156x1580.png)

](https://substackcdn.com/image/fetch/$s_!XegV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34d38c28-a8b4-4618-8f18-3dd72262603e_6156x1580.png)

This, by the way, is exactly how an LLM sees a sentence. It is not, however, how you would encode this information in a knowledge graph. The normal approach to encapsulating this in RDF looks something like this:

```
ex:JaneDoe a ex:Person ;
     ex:WorkedAs ex:Accountant ;
     ex:WorkedFor ex:BigCo ;
     ex:from "2012 ;
     ex:top "2021" .
ex:BigCo a ex:Company ;
     ex:manufactured ex:Widget;
     ex:hasProductLine ex:BigCoProductLine .
ex:Widget a ex:Product ;
     ex:partOf ex:BigCoProductLine .
```

Put another way, most semantic modelling takes a class/property/instance approach. This requires identifying both classes and properties in advance, and it is far from intuitive, especially when you add inheritance (and other forms of inference) into the mix.

Ironically, while this captures a lot of information, in some respects it loses information as well that’s more subtle. Some of this is basic modelling that doesn’t become obvious until you have more of the story:

```
Jane Doe, a person, worked as an accountant for BigCo, a company that manufactured widgets (part of their product line) from 2012 to 2021. After that, in 2021, she became a senior accountant at BigCo until 2023, when Jane went on to work for SmallCo, a startup, as their CFO. SmallCo produced Whizbangs, which were similar to Widgets, but more advanced. 
```

This can be represented (almost verbatim) as reified Turtle:

```
PREFIX ex:   <http://example.org/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

ex:JaneDoe  a ex:Person  ; rdfs:label "Jane Doe" .
ex:BigCo    a ex:Company .
ex:SmallCo  a ex:Startup .
ex:Widget   a ex:Product .
ex:Whizbang a ex:Product .

ex:JaneDoe ex:workedFor ex:BigCo
    {| ex:role "Accountant"        ; ex:start "2012"^^xsd:gYear ; ex:end "2021"^^xsd:gYear |} ,
    {| ex:role "Senior Accountant" ; ex:start "2021"^^xsd:gYear ; ex:end "2023"^^xsd:gYear |} ;
    ex:workedFor ex:SmallCo
    {| ex:role "CFO" ; ex:start "2023"^^xsd:gYear |} .

ex:BigCo   ex:produces ex:Widget   {| ex:inProductLine true |} .
ex:SmallCo ex:produces ex:Whizbang .

ex:Whizbang ex:similarTo ex:Widget {| ex:moreAdvanced true |} .
```

In essence, there are now three distinct properties of Jane Doe working for someone: two for BigCo and one for SmallCo (a startup). This is shown in the following diagram:

[

![](https://substackcdn.com/image/fetch/$s_!KhrU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe4551b2-044c-4127-8663-0bf2fbd18dfd_4258x5300.png)

](https://substackcdn.com/image/fetch/$s_!KhrU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe4551b2-044c-4127-8663-0bf2fbd18dfd_4258x5300.png)

Another way to think about this is that RDF-Star reifiers create connections between triples, rather than just between nodes. The blue items represent the declared nodes. The labeled edges also contain connections that represent the triple as a subject, not just the predicate itself.

One of the big differences to note here is that the annotation itself likely has a distinct class, depending on the triple. For instance, in the relationship

```
?person ex:workedFor ?company
```

the expectation is that the annotation (or reification) class will be something like `ex:Employment`.

What do I mean by _reification class_? When you create an assertion, the predicate of that assertion (such as `ex:workedFor`) implies that there exists an object that can describe that relationship in depth. The class of that object is the **reification class**. For instance, ex:workedFor implies an employment or job class (let’s choose the former as it is more closely associated with long-term work). The reification can then be rewritten as:

In this case, ex:Employment can be seen as the reification class, with the additional properties being the properties defined by that class.

> _All reifications have a reification class._

This is true of any kind of blank node structure, by the way - the attributes of a data structures can collectively be identified as a class. For reifications, that class is usually the noun variant of the predication relationships (ex:workedFor → ex:Employment).

Note that the same subject and object classes may have multiple reification classes dependent upon the predicate. For instance,

has the same subject and object classes (`ex:Person` and `ex:Compan`y respectively) but the predicate creates a different type of reification class.

Significantly, the reifier class here is also a subclass of event. This creates another lemma:

> Most reifier classes will be some form of an event, typically describing an activity.

This isn’t always true (especially when subject and object are of the same class) but any time you have an indication of a process (worked at, founded) there’s usually going to be an event involved as the reifier class.

SHACL 1.2 can make such reifier classes explicit, through reifier shapes:

In this case, the `sh:reifierShape` property identifies a node shape that, in turn, defines what a founding event should look like.

Again, getting back to the sentence graphing, the above modelled Turtle translates direction into a natural language description:

> Jane Doe founded NewCo in 2022, receiving 1,000,000 initial shares.

This can be viewed graphically as follows:

[

![](https://substackcdn.com/image/fetch/$s_!UOsa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2df1ca90-4f8b-4c89-9ec4-32f86cdb468b_4279x1255.png)

](https://substackcdn.com/image/fetch/$s_!UOsa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2df1ca90-4f8b-4c89-9ec4-32f86cdb468b_4279x1255.png)

The whole Turtle content can then be stated as:

By the way, this can also be represented in a similar “near verbatim” style as Open Cypher:

```
// Create Person nodes
CREATE (janeDoe:Person {
  uri: 'http://example.org/JaneDoe',
  label: 'Jane Doe'
})

// Create Company nodes
CREATE (bigCo:Company {
  uri: 'http://example.org/BigCo'
})

CREATE (smallCo:Startup {
  uri: 'http://example.org/SmallCo'
})

CREATE (newCo:Startup {
  uri: 'http://example.org/NewCo'
})

// Create Product nodes
CREATE (widget:Product {
  uri: 'http://example.org/Widget'
})

CREATE (whizbang:Product {
  uri: 'http://example.org/Whizbang'
})

// Employment relationships (with reified properties)
CREATE (janeDoe)-[:WORKED_FOR {
  type: 'Employment',
  role: 'Accountant',
  start: 2012,
  end: 2021
}]->(bigCo)

CREATE (janeDoe)-[:WORKED_FOR {
  type: 'Employment',
  role: 'Senior Accountant',
  start: 2021,
  end: 2023
}]->(bigCo)

CREATE (janeDoe)-[:WORKED_FOR {
  type: 'Employment',
  role: 'CFO',
  start: 2023,
  end: 2025
}]->(smallCo)

// Founding relationship (with reified properties)
CREATE (janeDoe)-[:FOUNDED {
  type: 'FoundingEvent',
  start: 2026,
  initialShares: 1000000
}]->(newCo)

// Production relationships
CREATE (bigCo)-[:PRODUCES {
  inProductLine: true
}]->(widget)

CREATE (smallCo)-[:PRODUCES]->(whizbang)

// Product comparison relationship
CREATE (whizbang)-[:SIMILAR_TO {
  moreAdvanced: true
}]->(widget) 
```

The similarity here between the two should be obvious; if your are modeling with reifications, the mapping between Turtle 1.2 and Open Cypher becomes considerably cleaner than if you are using the older OWL modelling approach.

Finally, the reified forms can make for cleaner JSON-LD as well:

Here the “@annotation” directive provides the reification content.

## Conclusion

There are several takeaways here:

-   Reifications can make the translation from natural language expressions into Turtle 1.2 (and vice versa) much more natural, as well as making for more compact code.
    
-   The use of reifications also makes going between Turtle and Open Cypher (Neo4J’s LPG language much easier, as does translation to and from JSON-LD and YAML-LD.
    
-   Reifications have annotation classes, frequently based upon activity or process. That is to say, when you create a reifier, you aren’t just creating random properties - there’s usually something being described.
    
-   Context graphs and knowledge graphs frequently overlap - there’s usually no magical divide that separates one from the other, but as a general rule, the more that you build on events as the foundation of things (and hence need to annotate activity) the more context-graph-like your hypergraph becomes.
    

Once you see narrative as a series of consecutive events, and see reification as a mechanism to qualify subordinate clauses in narrative structures, modelling tends to become more natural, and more closely aligned with how we build world models.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!Yju-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F274586b6-0358-4a70-b2e3-f04b3f9b37ef_2048x2048.jpeg)

](https://substackcdn.com/image/fetch/$s_!Yju-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F274586b6-0358-4a70-b2e3-f04b3f9b37ef_2048x2048.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

If you like these articles, please consider becoming a paid subscriber. It helps support me so that I can continue writing code, in-depth analyses, educational pieces, and more.

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.

