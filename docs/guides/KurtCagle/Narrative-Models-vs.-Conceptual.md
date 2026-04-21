---
title: "Dungeons & Declarations: What a Five-Room Game Reveals About Holonic Graph Architecture"
source: "https://inferenceengineer.substack.com/p/dungeons-and-declarations-what-a?utm_source=profile&utm_medium=reader2"
date: "Apr 4"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!ubAQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80e97625-2616-4020-9228-9eded6d3318b_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!ubAQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80e97625-2616-4020-9228-9eded6d3318b_2688x1536.png)

Since the emergence of LLMs a couple of years ago, I’ve been trying to understand the difference between the inherent data information structures of a latent space as compared to that of a conceptual space (which I’ll refer to colloquially as a knowledge graph). I’ve been sensing for a while that the distinction between the two is important, and lately I think I’ve nailed down why they are both similar and fundamentally different.

## Understanding Symbolic Graphs

A knowledge graph, at its core, is known mathematically as a labeled directed cyclic graph (also known as an LDCG). What this means is that there is a graph (a connection of nodes and edges) where each edge has a distinct direction from one node to another, and where nodes can have one or more edges either in or out. Furthermore, each node and edge has an associated “label”, which more properly should be considered a unique identifier. Identifiers do not necessarily need to be globally unique, but they should be locally unique to the graph.

Cyclic graphs imply that there is the possibility of a circuit - if you follow a path of edges, you may find one path that, even with the directional nature of the graph will eventually return you back to an initial node, creating a loop. Cyclic graphs do not require the presence of a loop, only that loops are not precluded from forming. If loops are precluded, then what you have is a labeled directed acyclic graph or LDAG. All LDAGs are also LDCGs, but not all LDCGs are LDAGs. An LDAG is usually called either a sequence if there is no branching, or a tree if there is there is. Taxonomies are usually LDAGs.

For the sake of not having to parse acronyms, I’ll refer to cyclic graphs here to mean LDCGs, and acyclic graphs to mean LDAGs.

Most data representations are ultimately acyclic graphs. Relational databases are conventionally acyclic - while it is possible to create a circular reference in a relational database, most such databases will actively throw an error if one is detected, because a processor can easily end up in an infinite loop if it encounters one. Most object models are trees, with XML and JSON (and other similar formats such as YAML) being representations of such graphs in different notations. RDF is a cyclic graph that is usually acyclic, but it doesn’t have to be. This is important, because it implies that you can represent all acyclic graphs using RDF, but also most cyclic graphs if you’re creative about how you manage iteration.

Most programs are cyclic graphs, because they encompass both loops and conditions. A program is not a data structure - it exists at a different level of abstraction with the notion of instructions (imperative statements) rather than definitions (declarative statements), with a statement typically being the assignment of an expression to a named variable or the parametric invocation of a function with the consequent assignment. Conditions are tests - if a certain condition is satisfied, then one branch is executed. Otherwise, a different branch is executed. This is still a graph, but it is not necessarily a data graph, though at any given time, the application's state can be rendered as a data graph. What this means in practice is that if you have an application graph along with initial parameters, the application graph generates a set (or graph) of data graphs.

When people talk about data graphs, they are usually referring to knowledge graphs, which are a subset of labelled directed cyclic graphs, in which the edge identifies a relationship between nodes as concepts. Some graph languages (Neo4J in particular) assumes that there is a distinction between relationships and attributes - a relationship exists between two node resources, while attributes are named literal values. Other graph languages (mostly in the Resource Description Framework family) treat attributes and relationships both as edges, with the objects of such assertions either being literals (strings, numbers, dates, etc.), or resources with unique identifiers (International Resource Identifiers).

I’m not going to get into details about either representation, other than to say that each node is intended to act as an identifier of entities or concepts (real or, well … conceptual), with its “label” being at a minimum locally, and preferably globally, unique. That is to say, an LDCG is a description of an interconnected conceptual space, where each node is a symbol. This is why this is approach is often referred to as Symbolic AI. The resulting graph is known as a _knowledge graph_.

Symbolic systems are important because they describe a condensed version of information reduced to a minimal subset of terms and relationships. It borrows heavily upon computer data representations - lists, tables, hashes, trees, and queues - because these provide a way to describe relationships abstractly in a (mostly) non-narrative manner. However, it is worth noting that traversing such graphs does “tell” a story - at this time, at this place, this event happened, with this result (as one example) - albeit in a very condensed format. A graph traversal path, then, corresponds to one story, one narrative, within a vast array of narratives.

## Language as Narrative Model

Humans, like all animals (and arguably some plants), communicate both with one another and with other sentient beings. They do so by exchanging signals. Consider, for instance, your typical songbird. That songbird has a repertoire of signals that it uses - trills, tweets, clicks, and so forth, often repeated - to send out messages to other songbirds. They evolved this language because songbirds are small and the world is large and dense, and sound travels farther than sight does in such environments. The songs may translate (roughly) into simple messages - “I am here!”, “There are berries here!”, “A predator approaches!”, “This is my territory, stay away!”, ”I want to mate!”, “Help me!”, “Where are you?”, and so forth.

These signals, by and large, have standardized to the point where they are now instinctive, though regional variations may emerge due to isolation from other populations. Two different species of songbirds may very well evolve different signals that represent the same thing, and as such, may no longer understand one another.

Language, consequently, tends to follow the same dynamics as population drift - as two populations encounter one another, they have trouble communicating. Over time, however, they develop a _pidgin,_ which consists of reasonably common concepts that the two groups both understand and consequently standardize on. Pidgins are simplified language - they are not as nuanced and expressive as established languages, but they provide a mechanism for communication on the important stuff - trade, sex, protection, and so forth.

The key point here is that language does not track concepts - it tracks and interrogates intent and action: “I’m going to the store,” “Do you want to come with?” “I went to the store yesterday to buy some food.” There are concepts here, of course, but unlike with a typical declarative knowledge graph, the focus tends to be on the assertions and queries of imperative actions.

What this produces is not a graph but rather a quasi-graph. The closest analogy I can come up with is imagining cobwebs mixed with dust bunnies but in many more dimensions. The filaments of the cobwebs are the threads of conversation or narratives. The dust bunnies are clusters of congestion, where linguistic structure represents conceptual similarity. The tf-idf encoding algorithm, which generates these mappings, tends to filter out grammatically common structures - they are there, but the tf-idf algorithm works primarily by finding those terms or phrases that are relatively uncommon compared to the grammatical connections and putting more weight on those.

## Indexed vs. Narrative

In declarative models, a node representing an entity has both properties (characteristics that **define** that entity) and inbound context **references**, that talk _about_ the entity in some way. For instance, in a database, the row identifier in a given table - its **primary key** , typically holds information that give table characteristics for that row (it’s properties), while a **foreign key** is a reference to that primary key. An **attribute** is a value for a given property that contains a literal value - a string, a number, a date, etc.

When a person makes a query on a relational database by passing a key, the database usually doesn’t search through all the rows in a table to find that key. Instead, most databases rely upon an **index**, in which, for a given primary key, a list of all the rows in various tables that reference that key are stored.

This means that when you do a **join** in SQL, only those rows for a given table that have that particular identifier as a foreign key are given, and these in turn are can be used to pass properties of the referenced row so that they can be added to a tuple, or a vector of properties. This way, for instance, if you have a million rows in your database, only a few hundred or a few dozen get passed to the database server because they are indexed. This is why databases can be very fast - they are looking up far fewer items than they would be by iterating and comparing through all possible values.

[

![](https://substackcdn.com/image/fetch/$s_!eXv0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ac8fc7c-6f87-42fa-82f5-eff73e2a73a5_3349x3840.png)

](https://substackcdn.com/image/fetch/$s_!eXv0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ac8fc7c-6f87-42fa-82f5-eff73e2a73a5_3349x3840.png)

Here, #T2R1 is short-hand for the identifier key in Table 2, Row 1.

Every database out there, except for the very simplest, is built with indexes. Most of the time, unless you are the one building the database, you’re probably not aware of those indexes because they are part of the query language. Some languages, such as SPARQL and GQL, use a composite key made up of three (or in the case of RDF, four) index keys (and consequently have multiple indexes).

Search engines (and consequently transformers, which are built on search engine architecture), do not use keys in the normal sense. Instead, they use tf/idf or bm25 encoding to create vectors from documents or fragments of documents, with those vectors in turn being defined by narrative sequences that are matched against specific tokens in an ordered vocabulary of tokens.

[

![](https://substackcdn.com/image/fetch/$s_!vcXy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84f0d576-ef4d-4759-a25a-b05d9b00383c_2392x3840.png)

](https://substackcdn.com/image/fetch/$s_!vcXy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84f0d576-ef4d-4759-a25a-b05d9b00383c_2392x3840.png)

Within the latent space, what gets produced is a series of intersecting sequences of expressions (tokens) that form different paths. If you start on a certain word, you can effectively construct several potential conversations. While any one item can lead to a large number of potential constructs (such as “far”, which references back to itself. (far far, far far far, and so forth), when you specify multiple terms, you are much more likely to identify a much smaller number of valid paths that form complete sentences, paragraphs, and more. For instance, specifying “once” and “princess” as tokens gives you only one path (not counting the looping for), in bold:

[

![](https://substackcdn.com/image/fetch/$s_!TR0i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0618c5e1-03f6-435e-9a5c-c523451cb6cd_2392x3840.png)

](https://substackcdn.com/image/fetch/$s_!TR0i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0618c5e1-03f6-435e-9a5c-c523451cb6cd_2392x3840.png)

With a sufficiently large sample, each word tends to develop a cluster around it, with some words, like articles(“a”,”the”,”an”, etc.) or “named” occurring so often that they can be seen primarily as being structural, but others, such as “princess” or “galaxy” appearing less often but with more prominence.

What happens with an LLM then is that the prompt uses the encoding vectors that have the largest number of matches in the lexicon to identify the largest number of relevant tokens in the dataset, then looks for the most comprehensive pathways (narratives) that match the tokens in the prompt. This is also why zero shot queries tend to usually retrieve garbage - the smaller and less specific the prompt, the less likely that you’ll find enough tokens to establish a valid narrative pathway, meaning that the output will tend to “hallucinate” among several potential narratives.

For instance, let’s say that you passed the three tokens “once”, “galaxy” and “leia” in your prompt. You’ll notice that while the bold sequence indicates what you’d expect, there are in fact three potential paths that those three tokens are all a part of:

```
once upon a time, in a galaxy far away, lived a beautiful princess named leia.
once upon a time, in a galaxy far away, lived a handsome prince named leia.
once upon a time, in a galaxy far away, lived a hideous ogre named leia.
```

_Note that all three of these are possible, though only one is valid - the other two are hallucinations._

Notice that when you have multiple paths, you also get a certain degree of constraint. Suppose that in the training dataset, there was some indication that leia was female, and that princesses are also (usually) female. This creates a new set of paths in blue (I removed the first part of the graph):

[

![](https://substackcdn.com/image/fetch/$s_!49yJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42f6bd94-ddb4-4c87-96bd-743dbcd8fd1a_3840x3449.png)

](https://substackcdn.com/image/fetch/$s_!49yJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42f6bd94-ddb4-4c87-96bd-743dbcd8fd1a_3840x3449.png)

This would be translated (with some very minor tweaking) as:

```
there lived a beautiful princess named Leia, of female gender
```

The blue path creates an implicit constraint - only one of the named entities is labeled “Leia”, and only the princess path also has the association with “female”. Note also that there is a second path that could be followed:

```
there lived a beautiful princess, of female gender.
```

Note that in this case, while both are correct, if you assume that the most fit construct will generally be the longest (and consequently containing the most information), the first response is likely superior.

## Resolving the Models

Semantic models such as RDF place the relationship (the predicate) between the object and the subject (such as “has gender”. However, this is mainly a historical convention rather than any explicit mathematical requirement, largely because such expressions somewhat mirror subject verb object relationships. However, in the vast number of cases, the determining factor for the relationship can be thought of as the following:

```
The predicate is given as the "type" of the subject composited with the "type" of the object: Leia (a named character) NamedCharacterHasGender female (a gender), with "Has" simply reinforcing the direction of the relationship.
```

This can be seen visually as follows:

[

![](https://substackcdn.com/image/fetch/$s_!v5re!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f5e0a24-2a72-4d08-94cf-49905d6df26c_3840x3498.png)

](https://substackcdn.com/image/fetch/$s_!v5re!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f5e0a24-2a72-4d08-94cf-49905d6df26c_3840x3498.png)

In other words, the predicate will, in general, be a reflection of the subject type, object type, and datatype (such as years). This means that (for many narratives) it should be possible to derive the relationship directly from the assertion, if that information is available within the graph.

The proximity measure, in general, of a latent space, identifies tokens that have a certain degree of similarity to one another, meaning that they usually occur in similar narrative sequences to mean roughly the same thing or that occur in general proximity in narrative sequences.. For instance, “female”, “woman”, “girl”, “queen”, etc., tend to be found together sufficiently often that their latent distances are comparatively small, but “female” and “asteroid” or “kumquat” are likely to have much larger latent distances.

That’s not to say that some terms may not have immediately obvious proximities, but nonetheless may surface, such as “female” and “bicycle”. Why? Because “female bikes” are a type of bicycle, usually lacking a strut (or having an angled strut) between the handlebar column and the seat, in theory, because men’s typically larger mass require more support on the bike itself.

Does this mean that Latent spaces are graphs? In the sense that they are narrative structures that can be encoded as a sequence of nodes, yes. In the sense that they are a full-blown knowledge graph, arguably no. However, one primary reason that they aren’t has to do with the fact that a knowledge graph is reliant upon having keys to perform retrieval of associated substructures.

[

![](https://substackcdn.com/image/fetch/$s_!4VX5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05d4a94d-e2bc-4216-94a6-106472c96b73_3840x3206.png)

](https://substackcdn.com/image/fetch/$s_!4VX5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05d4a94d-e2bc-4216-94a6-106472c96b73_3840x3206.png)

The identifiers here are given in the form `Type:LocalName`, but this is just for pedagological purposes. If you have specific identifiers that you want to associate with one (or more) terms, then by embedding the URIs for those resources (especially class, taxonomy or predicate terms) into your training data as a narrative structure, it becomes possible to create associations that can then be used in conjunction with a knowledge graph in a triple store or similar deterministic system. Moreover, by associating class type identifiers, you can correlate this information to determine the nature of the relationship between two entities.

Additionally, it should be possible to encode structural information (such as SHACL, XML Schema, JSON-Schema or similar component descriptions) that can then associate namespaces with commonly used prefixes.

Why do this? Most LLMs are already pretrained to work with SHACL in one form or another. This in turn means that the same kind of constraint logic that identified that if a named character in the above example is a princess, they are also female. The narrative structure in this case reinforces constraint matching, and SHACL can be applied either at the class, the property or the individual instance level. Similarly, RDF Schema (RDFS) can help with inheritance of abstract interfaces, giving much more sophisticated control over the reasoning capability of the model.

It should also be pointed out that the latent space is not, in and of itself, an ontology, but rather represents the potential union of many, many different ontologies. By identifying namespaces then providing identifiers in that namespace (or that conform to that namespace through something like SHACL which provides the ability to define context namespaces, this will cause a given model to coalesce around the namespaces in question, with information that is close to stick to a structure with terms (tokens) that are closest in meaning to that indicated by the ontology itself.

This is still subject to training data, mind you. If you’ve defined a protein taxonomy and you’ve trained your model on financial data, the likelihood that anything meaningful will coalesce around the schema is small. You CAN have multiple ontologies resident if you do have the training data, so long as you maintain distinct namespaces for each partition of the latent space.

So how do you encode this data? That’s a discussion for a subsequent article. In general terms, think about narrative structures (and doing your homework to ensure that you have a good idea about the underlying desired ontologies, about associating type associations and resource URIs with relevant token terms, and in general taking advantage of annotational metadata to better help “tell a story” with your knowledge graph that becomes meaningful to the LLM.

In media res,

[

![](https://substackcdn.com/image/fetch/$s_!_As3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3120125e-2976-4de4-be00-d06557c39bea_1344x768.png)

](https://substackcdn.com/image/fetch/$s_!_As3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3120125e-2976-4de4-be00-d06557c39bea_1344x768.png)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.