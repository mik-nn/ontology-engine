---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Are-We-Thinking-About-Ontologies
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:10.578717+00:00'
  title: Are We Thinking About Ontologies
  type: plain-doc
  version: '0.1'
---

# Are We Thinking About Ontologies

[

![](https://substackcdn.com/image/fetch/$s_!CQmK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb620655d-d5b7-4dce-9f56-931740607630_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!CQmK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb620655d-d5b7-4dce-9f56-931740607630_2688x1536.jpeg)

_This has been on my mind for a while now, the idea that one of the big things holding RDF back is the notion of global identifiers. RDF has been associated with the concept of URIs (eventually IRIs) almost from its inception, but there have been some fundamental issues when dealing with narrative structures (and especially conversation) that have me questioning whether this is, in fact, too stringent a requirement. This is what I want to cover here, and I think it has significant implications. This was originally a LinkedIn post (so some of you who read my regular posts on LinkedIn might have seen it), but there is new content as well._

I’ve been thinking about conversations recently. Consider, for instance, the following snippet of conversation that may be heard at a cocktail party (or whatever the modern equivalent is):

> “I heard that Jane Doe has managed to get approval on her bill by enough other sponsors, and it should be out of committee and onto the floor by next week.”
> 
> “Wait, who’s Jane Doe?”
> 
> “She’s the Congresswoman from Massachusetts. You know, she’s on the Ways and Means committee. She’s the ranking member there.”
> 
> “Oh, yeah.”
> 
> “Anyway, the bill is supposed to …”

There’s a lot of information here, but significantly, it’s also difficult to look at it and say “Oh, I can just turn this into triples”. This is difficult first because it doesn’t necessarily fit into how an ontologist might structure this as data, but more to the point, there is no “formal” ontology for this to be mapped to.

Instead, there are a lot of concepts that MAY (or may not) have some IRI somewhere that effectively defines the concept in terms of other IRIs, and there’s a vague, amorphous cloud of things that we call language, which are highly contextual. If the people speaking are political junkies in the US Federal capital (or interact with those who do things there) then this conversation makes perfect sense. If, on the other hand, the people involved were Germans, chances are this conversation would be seen primarily as jibberish except for a small handful of Germans who closely follow American politics.

Put another way, there is an implicit but mostly unstated conceptual ontology that a specific group of people use, but without the implicit knowledge of the context of that ontology, most others have to determine things largely by inference. There are a few key ways in which this process happens:

-   **Deferred Classification (Late Binding).**
    
-   **Concensual Agreement and Ontological Scoping**
    
-   **Taxonomy Management and MDM**
    
-   **Contextual Definitions.**
    
-   **Self-Learning Symbolic AI**
    

## Deferred Classification

In the above example, there is a reference to a bill. Now, a bill can be many things: a proposed piece of legislation, a statement of charges in a transaction, a legislative act (see Bill of Attainder, which has some fascinating current implications), a listing of items in a shipment (a Bill of Lading), or the horny beak of a bird. It can also be a person’s name (short for William). All of these, of course, hold true for English; other languages may have similar terms.

In the conversation, we may be familiar with a term in one context, but not in another. If you’re familiar with the bill that you pay for electricity or what is presented at a restaurant, but not familiar with US politics, then the meaning can only be inferred by a definition that you make up from the local conversational context. It’s possible that you have a dictionary somewhere that will allow you to disambiguate the term, but you’re not going to whip out that dictionary in the middle of a conversation while simultaneously trying to hold a drink in a stemmed glass and a plastic plate with hors d’oeuvres on it.

Instead, you internally remember the word (stick a pin in it) and build up definitions by context. A **bill**, based upon the snippet of conversation that follows, is something that requires sponsorship from within a committee that can then be “sent to the floor”. The bill in question was submitted by Jane Doe, a Congresswoman from Massachusetts on the Ways and Means Committee and its ranking member. A floor in this case may possibly be the full assembly of congressional representatives, and presumably, they will perform some action (vote on the Bill) when the Bill is presented next week.

Some of this may be immediately relevant to the bill's definition (it requires submission by a Congressional representative), and some may not (the Congresswoman in this case is from Massachusetts, which is (likely) a state in the United States).

Note that nowhere have we made a formal IRI for a particular bill (there’s a vague notion of _this_ bill, but that’s about it) and the concept of the class **Bill** is tenuous at best. It consists of a set of property relationships that are not well specified. What likely does not exist is a deep ancestral tree of properties that make up subclass relationships, at least not yet.

## Consensual Agreement and Scope

As our questor moves around the cocktail party, he or she may learn more and start comparing notes across different instances of a bill. For instance, they may hear from someone else that a particular vote on the bill failed, and that it was sent back to the committee, while another vote on a different bill passed, sending it to the Senate for consideration.

As more information is gathered, the definition tightens through consensus, with spurious and erroneous properties removed and other relevant properties added to better constrain it. In essence, the class is defined in terms of other classes (usually through a combination of inheritance and composition). The larger the number of people using that particular class, the more likely it is that a working ontological definition for that class will be established, clarifying whether a given document is or is not a bill from a process standpoint.

The Consensual Agreement stage is important because it reduces ambiguity, though a certain degree of ambiguity is usually present in any classification (this is why most taxonomies tend to have an “Other” bucket, even though it is considered bad form to do so). In effect, the scope of the definition is primarily determined by the organisation of those who use the term. For instance, in a contract, critical terms are defined for the parties who agree to the terms of the document. In this regard, a contract can be seen as a scoped ontology - a way of determining what is meant by terms that embody specific concepts so that both (or all) parties have minimal ambiguity about what the contract is about.

We use standards when we wish to achieve a broad consensus on how specific concepts within the mandate of that standard are defined. A standard in this regard is a contract to use a common ontology (especially class and relationship information).

Note that this can also be turned on its head. If a particular organisation adopts a given ontology, this means that instances that are defined _in that ontology_ are classified in certain ways (they satisfy a taxonomy of classes). Another organisation with a different ontology _**will**_ classify the same things (instances) in different ways, because their classification criteria - the ontological schemas and corresponding taxonomies - are different. This does not mean that one ontology is correct and the other is wrong; it only means that two different organisations have different models for describing their operational realities.

The implication of this is profound - if two organisations cannot agree on the definitions of what makes up a class (the class properties) then global IRIs are only meaningful when you have full consensus from all parties about which ontology is in force. Put another way, there are no global IRIs, only varying degrees of _scoped locality._ What is generally uniform is not the IRIs of resources (these should be considered local to whatever the naming authority is that mints those IRIs) but IRIs of the schematic elements - the classification taxonomy and structural definitions for those classes.

## Master Data Management and Local IRIs

This means that most relevant identifiers are likely not specific IRIs, but rather contextual shapes of properties that together determine a specific scope. For instance, let’s say that you have two companies that each issue a badge with an associated badge number (an identifier) to a person when they come in board. For purposes of discussion, let’s assume that both companies have badge that happen to be five digit numbers. A given person, Jack, has worked for both A-Co and B-Co, and has badge numbers “12345” and “67890” for the companies A and B, respectively, while Jill, who works for B-Co, also happens to have the ID number “12345”.

In the simplest case, the badge ID is insufficient to disambiguate Jack from Jill - given the identifier “12345” both people will show up. Instead, you also have to specify for the “local” identifier the authority or issuer of the ID in question, which can be described in Turtle as:

```
# Turtle

PREFIX Class <http://example.com/ns/Class#>
PREFIX Employee <http://example.com/ns/Employee#>
PREFIX Identifier <http://example.com/ns/Identifier#>

[] a Class:Employee ;
    Employee:hasIdentifier [
        Identifier:hasValue "12345"^^xsd:string ;
        Identifier:hasAuthority Company:A-Co;
    Employee:hasName "Jack Sprat" .

[] a Class:Employee ;
    Employee:hasIdentifier [
        Identifier:hasValue “67890”^^xsd:string ;
        Identifier:hasAuthority Company:B-Co;
    Employee:hasName “Jack Sprat” .


[] a Class:Employee ;
    Employee:hasIdentifier [
        Identifier:hasValue “12345”^^xsd:string ;
        Identifier:hasAuthority Company:B-Co;
    Employee:hasName “Jill Lean” .
```

What is significant here is that each of these employee instances lacks a global identifier and instead uses a blank node. This means that there is an IRI within the data system that holds these values, but it’s not used to identify the individual globally (the latter can be done from the context block that holds both the badge identifier value and its issuing authority), which can be accomplished via SPARQL:

```
select ?employeeName ?badgeNum ?authority where {
     values (?badgeNum ?authority) {("12345"^^xsd:string Company:B-Co)}
     ?employee a Class:Employee .
     ?employee Employee:hasIdentifier ?identifier.
     ?identifier Identifier:value ?badgeNum .
     ?identifier Identifier:authority ?authority .
     ?employee Exmployee:hasName ?employeeName .
     }

--->
employeeName   badgeNum   authority
"Jill Lean"    "12345"    Company:B-Co
```

So, why do we not have global identifiers? Partially because it is possible (indeed probable) that there may be multiple systems (graphs) to which the same data has been uploaded without knowledge of the other system’s IRIs. This holds especially true when dealing with federated queries across multiple systems (and when aggregating data across systems). That is to say, the storage IRI in any given system is irrelevant (save that it needs to be unique WITHIN that system), but the local badge identifier + authority DOES need to be unique.

In effect, a qualified identifier is an identifier with sufficient context to fully disambiguate it. Yes, you could associate a unique IRI with that employee, but outside of those databases that you control, you don’t necessarily know whether others will choose to use your IRIs.

This is the thing about blank nodes: they are IRIs generated when a resource is parsed (e.g., from a Turtle file) and are specific only to the parsing system. When it is reserialized, the output is converted back into a blank node where the relationships of the blank nodes are still maintained, but the specific IRI of that node has changed.

This then brings up an interesting point. A Turtle document is a graph that is scoped to the document itself. When the Turtle document is parsed into internal triples within the database or in-memory, or serialised from triples, the specific IRIs of all the blank nodes will be converted to/from their corresponding database representation. This means that such blank nodes, even when they are named (such as \_:JillLean) are effectively local to the graph itself in its current form. The relationships and data structures are still maintained, but the IRIs are scoped.

The key takeaway here is that we should stop looking at IRIs as global resource identifiers. They are more structural in scope, intended primarily to hold together shapes of information rather than being simply keys in their own right, with secondary identifiers and richer context providing a better mechanism for finding resources.

## Taxonomy Mappings and Classification

An ontology typically consists of four major parts - a taxonomy that identifies the scale of classification, a schema that identifies the relationships between classes (and similar shapes), instances that satisfy a given classification scheme, and metadata (often on reifications) that serves to provide textual context to those instances.

What is often no appreciated about ingestion and creation of content from external data sources is that creating the relationships between entities (the schematic elements) is typically a fairly straitforward process - it’s model building, but it usually is model building with a goal towards having a local working ontology first. There are a number of different standard (or upper-level) ontologies out there: GIST, BFO (Basic Formal Ontology), Schema.org, and so foth, as well as industry standard ontologies for almost all areas.

What is often harder to find are good taxonomies that describe the different states a particular class can be in. In OWL, these are frequently called Named Instances, in XSD they are Enumerations, in general modelling they are frequently referred to as Controlled Vocabularies. They are frequently very industry, enterprise, or domain specific, and as such are usually not “contained” within these standard ontologies.

One problem that I think occurs when talking about knowledge engineering is that it tends to be oriented around pipeline transformations outside of the context of the existing database. We use TARQL or similar tools to generate Turtle, then we ingest the Turtle directly, but this also requires that we as ontologists KNOW the target ontology. This requirement, though great from the standpoint of keeping ontologists employed, is suboptimal when dealing with creating data flows within organisations.

This is part of why I see ingestion as being a two stage process. The first stage gets information from an exogenous ontology that will likely be suboptimal from the standpoint of storage and retrieval but that doesn’t make as big a demand upon the engineer knowing the remit of the entire knowledge graph, while the second stage is done contextually, allowing for synonym, stemmed, and tokenized matching that are contained within the taxonomy itself. This second transformation stage is much more readily accomplished using a Sparql Update script upon an intermediate graph stored in a named graph.

This two stage process becomes especially important because it is _rare_ that we have, going in, the data to do full-scale classification from raw sources. This is a reflection of the original conversation - we have to determine context from narrative, which often tends to be chary about how much will be provided at any given point in that narrative - which usually means that ingestion is not a single action but a continuous state of being for a knowledge graph that forms connections as new information is provided.

Indeed, this is one of the things that differentates an LLM from a knowledge graph. An LLM is graph-like (I find thinking about it as an overlapping graph of narratives provides a good example) but it is also fixed. You do not update an LLM, you rebuild it from scratch for every revision. A knowledge graph, on the other hand, should be seen as a dynamic system that queries its known states and based upon this refines its knowledge periodically as new data enters the system. Sometimes this process is straightforward - the addition of facts into the system, but sometimes it is also inferrential (surfacing new facts that are in fact the distillation of known but not necessarily conveniently connected information).

## Self-Learning in a Symbolic AI Context

This points to another facet of knowledge graph fact creation: it is in fact a background process that occurs through the application of rules that _may themselves be inferred and derived_. I think this was in fact one of the intentions of OWL originally, but one that was ultimately defeated because we didn’t have either the tools or the hardware in place to make it happen. This meant that you effectively had to know the facts that you were attempting to derive, and the creation of these rules tended to be very much a bottleneck, especially as most of what was produced was spurious - it surfaced information that likely was either obvious or irrelevant, even if true.

SHACL is, in many respects a significant step forward, because it provides information about structure without necessitating the need for inferencing. This decoupling may seem odd; for a while, even I made the observation that if you have SHACL you still need an inferencing layer, but I’m increasingly coming away thinking that perhaps you don’t.

If you have a way of specifying shapes, you have the vehicle to determine what _may be_ interesting rules. A graph can be thought of as a sparse matrix, where certain relationships between entities can be derived simply by comparing class rows and columns, but this something of a brute force method where a lot of potential combinations of subject class and object class are nonsensical.

However, a SHACL property shape is essentially a way of saying that there is a particular _path_ along the graph that determines a property - the property wraps the path, not vice versa. This is an intriguing notion, first because it moves the discussion past the single predicate stage (which is fairly limited), because it makes it easier to codify inferencing based upon something computational (a specific path pattern) rather than advisory (a transitive property), and because such patterns are composable. In other words, with shapes, it makes it easier to surface (and explore) much more complex paths, and from them, to generate more germane predicates that can encapsulate and name these composed patterns.

By simplifying the schema language, this can be used to by a system to identify metapatterns. Put another way, it should be fully possible to derive OWL from SHACL, but more, it also makes it much easier for such a system to generate (i.e., surface) potentially useful propety patterns dynamically, at which point the role of the ontologist shifts from being the designer of the patterns to being the one who prunes what are seen as irrelevant or counterproductive patterns (anti-patterns).

This gets at the heart of learning: the process of generalization. LLMs CAN generalize to a limited extent, but they are subjects to the limitations of linear context - they don’t “remember” such generalizations beyond a single session. SHACL-based knowledge graphs on the other hand can extend both their pattern matching and transformation not just of their data but also their schemas, in effect learning new patterns that they can both retain and build upon. I think we’re just scratching the surface here of what’s possible, and it’s a topic I hope to explore in much greater depth in the near future.

## Contextual Programming

One final point that’s worth examining here. A knowledge graph is a database, but its also more. It is a way of representing state within a system in ways that most databases really aren’t suited for. Relational databases usually keep a distinct boundary between data and schema. but in general knowledge graph schemas are directly accessible via a query or update, which means that they have a degree of self-introspection that SQL generally doesn’t have.

More to the point, this schema can be updated dynamically. As the knowledge graph learns more, it can adapt its own schema dynamically to reflect this learning. That schema is conceptual - declarative systems such as knowledge graphs can identify new properties contextually.

We don’t do a lot of this today, in part because knowledge graphs don’t have the “mystical” narrative capabilities that LLMs do — mystical in the sense that an LLM creates the illusion of narrative primarily by traversing patterns of existing narrative in ways that, while marginally explainable, seem to operate in ways that are difficult to predict. A symbolic knowledge graph will never do that, if only because we can see and understand the traversal of concepts in a knowledge graph. Yet at the same time, a knowledge graph is far more suited to be able to create dynamic digital twins and world models, precisely because it is consistent, FAIR, containable, and explainable.

I think the next stage of real programming is going to be contextual programming based upon symbolic AI systems. Patterns are seen as constraints upon named shapes of varying degrees of complexity, and once you have consistent patterns, you have programmability and computability. This is only peripherally procedural and linear, because I don’t think that we have yet fully reached the stage where SPARQL and SHACL are fully integrated, but it’s where we’re going.

SHACL allows you to identify shapes, which is a critical part of any rules engine. If I have the ability to say - for a given node, determine whether this node has this shape, then I have a mechanism for determining which rules need to be applied, and from that for determining how nodes are then transformed when those rules are applied.

There’s still a missing piece out there, a piece that says that when I have a graph how does that graph get transformed to other representations. There is no XSLT or XQuery for graph _**yet**_, nothing that can transform a subgraph into a Markdown narrative, so we have to go outside of the scope of the knowledge graph engine to apply that. That will come — you’re beginning to see shades of this in SHACL functions and UI considerations — but I think that for now LLMs have stalled much of the development on that front precisely because symbolic AI is not sexy, even when it does work.

One thing I will say. I’ve learned not to bet against Tim Berners-Lee. He has, directly and indirectly, come up with technologies that buck the prevailing trend, that seem overly complex and definitely different from the one that most programmers think about the world, yet his track record for coming up with technologies with staying power is unparalleled. My suspicion is that in fifteen years time, GenAI systems will look a lot more symbolic than they do today, and at their core will be something that Tim invented or helped to midwife.

## Conclusion

The world is a messy place, and we learn about the world not by creating a comprehensive model then trying to fit facts to it, but by encountering facts over time and trying to build a world view around those facts. A knowledge graph is a world view - a way of representing systems of related things in a way that can evolve over time. We’ve stumbled across pieces about how that may be achieved — I think that blank nodes, with their ability to represent structure WITHOUT requiring global keys, is a pretty amazing innovation, but it is also something that runs counter to what programmers tell us is the way that the world should work.

As we enter into the third phase of the semantic web, we’re coming to a disturbing conclusion. Ontologies can be (and perhaps even must be) evolving systems, and that means that we need to be careful about what we deem as absolute. We’re beginning to work with shapes as metapatterns, defining not just the characteristics of predicates but the characteristics of complex, multiply-constrained properties.

Perhaps these are beyond what human brains are capable of articulating - we are three dimensional thinkers, and graphs very quickly exceed such thinking, but if we have the tools whereby we can in fact define composable, queryable shapes that can then themselves be used to create more complex systems, we’re at a point where we’re talking about semantics in the same light as organic chemisty. That is to see, organic chemistry is powerful not because of the number of elements (most of organic chemistry can be specified by about a dozen elements), but powerful and rich due to the permutations of those elements.

So, my apologies here for getting in deep, but as we look towards the future beyond GenAI, I cannot help but thinking that the core will look a lot more like symbolic systems with just enough GenAI around the edges to capture and manipulate those symbolic patterns.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!z2r4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a335133-e4a3-47ee-b499-1a147c406e0b_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!z2r4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a335133-e4a3-47ee-b499-1a147c406e0b_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please contact me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please consider contributing something to support my work, allowing me to continue writing.

