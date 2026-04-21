---
title: "The Holonic Graph: A New Architecture for Knowledge That Thinks"
source: "https://inferenceengineer.substack.com/p/the-holonic-graph-a-new-architecture?utm_source=profile&utm_medium=reader2"
date: "Apr 2"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!ReWS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa31b8e8-243d-424a-91b9-c34d52a3ef06_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!ReWS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa31b8e8-243d-424a-91b9-c34d52a3ef06_2688x1536.jpeg)

The term knowledge graph is a relatively recent invention, as far as I can tell, appearing in regular usage only about a decade ago. Graphs themselves date back centuries, with much of the foundations of graph theory tracing to Leonhard Euler in the 18th century, but the use of labelled directed cyclic graphs (LDCGs) for data storage can be traced to work in the 1980s and 90s.

The recent focus on using knowledge graphs as a way of grounding large language models (LLMs) is very recent (2022-23), and to a certain extent, is still unexplored territory. This is why I believe it’s essential to recognise that not all knowledge graphs are created equal, and that how we build a knowledge graph from the outset can significantly affect how it is used.

Knowledge graphs (KGs) come in several different flavours:

-   Taxonomies
    
-   Facet-Based KGs
    
-   Associated KGs
    
-   Annotational KGs
    
-   Reified KGs
    
-   Holonic KGs and Hypergraphs
    
-   Computable KGs
    
-   Hybrid AI KGs
    

This list is far from comprehensive, and many knowledge graphs exhibit aspects of all of these.

## Taxonomies and Data Dictionaries

This remains one of the largest applications of knowledge graphs. Most organisations maintain taxonomies of relevant terms, often referred to as data dictionaries or vocabularies, which are generally organised into categories and sub-categories. These are lists of items, with sufficient metadata to provide primary labels, descriptions, synonyms, and publication information. These are usually arranged hierarchically, from general to specific, and typically include relatively few predicates beyond those necessary to maintain the hierarchy.

Taxonomy-based KGs are typically used for human purposes rather than to drive automation processes, and usually have a hierarchical class structure with leaf-node instances. For instance, a retail company may maintain a taxonomy of products by product type (shoes, shirts, pants, etc.), with each type further broken down into brands and, from there, into individual products. The distinction between category and thing is often unclear.

Such taxonomies may drive “drill-down” type user interfaces, but can be brittle and arbitrary. They have more structure than a simple linear list of classes, but not a lot more; however, they are easier to conceptualise. In my experience, they often inform an ontologist about existing priorities within an organisation, but they don’t contain much detail about the relationships between such classes.

## Faceted Knowledge Graphs

In a gem, a facet is one particular face of the geometry of the polished crystal. In an ontology, a facet is typically a property that can take on a (reasonably small) set of values. Rather than saying that an adult woman’s violet long-sleeved blouse is a subclass of long-sleeved blouses is a subclass of blouses, it is a subclass of clothing tops, etc., the blouse in question is faceted along different categories:

-   an item of clothing (category)
    
-   worn as a top (figure location)
    
-   worn as a loose blouse (garment style)
    
-   worn by women (gender)
    
-   with long sleeves (sleeve length)
    
-   of colour violet (garment colour)
    
-   worn by adults (age group).
    

In this case, the “class” involved is made up of aggregated properties, each of which in turn has a value from an enumerated list (e.g., colour could be {violet, aqua, tan, grey, etc.}). Facets have a significant advantage over hierarchies: they can be used to compose classes while retaining some inheritance through constraints. For instance, the colour(s) of a given garment may be selected from a long list of colours, but each product line ultimately includes only a subset of those colours.

Faceting reduces the number of classes dramatically. It allows you to view the instance data in several ways (by colour, by gender, by garment style, by age group, etc.) and to create subsets defined by intersections of these facets (e.g., all garments with long sleeves and violet colour).

Facets can be likened to radical groups in chemistry, such as hydrogen or hydroxyl, in that many different entities may connect (point to) a facet. Still, facets usually don’t have many outbound links. Put another way, even rdf:type, one of the most central properties in RDF, is simply a way of describing the dominant facet of an entity.

## Associated Knowledge Graphs

Faceted knowledge graphs are a subset of associated knowledge graphs. In general, association graphs relate entities based on containment or ownership. For instance, a contract may create connections between two or more parties; classes have associated students and teachers; authors have associated books (and vice versa); and so forth.

Typically, an associated knowledge graph is structurally similar to a relational data model, in which you have complex composed objects that connect to other complex composed objects, as well as to faceted terms. 1-to-many or 0-to-many relationships predominate (most facets are 1-to-1). Moreover, associated knowledge graphs tend to be much more temporally oriented, as associations begin and end over time.

The transition from faceted to associated knowledge graphs can be pretty subtle. A list of states or provinces, for instance, can be seen as a facet. Still, addresses are associated structures, and a political knowledge graph may decompose states as complex structures in their own right.

## Annotational Knowledge Graphs

Annotational knowledge graphs typically involve commentary about (typically document) entities, in which opinions, comments, imagery, and similar content refer to that entity (possibly a reference to a document as a URL). Annotational systems originally evolved out of standards such as Dublin Core, though this was expanded as the Web Annotation Standard on one hand and Schema.org on the other hand. Annotational metadata is frequently critical for maintaining data provenance and assisting with data governance.

What’s critical with annotational KGs is that they are typically referential in nature, not the definition of an entity, but a description about the entity. This is external information about a resource as perceived outside of that resource itself - what people think about that resource, and it represents a layer of abstraction that is a precursor to reification.

## Reified Knowledge Graphs

Within the RDF specification in 2003, there was a section devoted to reifications, which are essentially statements about statements, which was a way to associate an identifier with a triple (subject/predicate/object). At the time, there were comparatively few reified knowledge graphs, both because reifications could be modelled using intermediate objects in OWL and because most triple stores could not afford the performance overhead of maintaining reified statements.

By the late 2010s, the need to address individual statements was becoming more pressing. One reason for this was the emergence of labelled property graphs (LPGs), which were built on a model where an assertion could have additional literal values on the property relationship (this was especially true of Neo4J). This gave rise to the effort to create a consistent extension of RDF, called RDF-Star, that could provide a better foundation for reification. This effort is ongoing; the RDF-Star standard is likely to be formally ratified as a W3C Recommendation sometime in mid to late 2026, and most commercial and open-source databases already provide some support for the proposed standard.

One key aspect introduced by RDF-Star is that reification can determine whether a particular statement is conditionally valid. For instance, a store can be identified as open. Still, reification indicates that this statement may be false in certain contexts (e.g., a store may be open only for specific hours on a given day). This also opens the possibility that a statement can be conditionally true in a Bayesian sense (i.e., as a probability under a prior).

Similarly, reifications make it easier notationally to discuss invertible graphs, in which edges between nodes of a given type (such as routes between two airports) can be converted into nodes with inverted edges (e.g., route nodes connected by two airport edges). This makes specific graph analytics considerably simpler to perform.

Reified graphs are relatively new; consequently, several best practices are likely to emerge over the next few years.

## Holonic Graphs and Hypergraphs

A long-standing problem with RDF has been how to express holons effectively. A **holon** is an entity that is also itself a system. An organisation, for instance, is a holon: it can be treated as a thing in specific contexts, but it also has an internal structure that makes up that thing.

Holons are essential at an architectural level for describing digital twins and spatial systems. Various groups are proposing several standards to establish best practices for representing such holons, most of which are based on named graphs. Named graphs have been around since 2013, but their adoption rate has been relatively low (in part because we haven’t had a solid use case for them until comparatively recently). I expect that holonic standards will likely be “on deck” sometime between now and 2027.

Hypergraphs have also been discussed in technical circles for the last several years. Technically speaking, RDF could be treated as a hypergraph (meaning that nodes, edges, and reifications could all have one or more edges). Still, in practice, hypergraphs are likely to emerge only with SHACL 1.2. Most RDF-Star-based hypergraphs are currently in their earliest stages, and I’m unaware of any production-level versions of holonic graphs.

I see holonic graphs, in particular, as essential for digital twin and spatial web development.

## Computable Knowledge Graphs

For the last twenty-five years, the primary mechanism for interacting with a knowledge graph has been SPARQL, a language intended to “query” a graph and return either a graph or a table derived from it. SPARQL 1.1, published in 2013, introduced a mechanism for adapting SPARQL so that the graph output of a query could be used to update the graph. In theory, this is a powerful tool. In practice, it’s almost too powerful, in that, with access to SPARQL Update (SU), you also have total control over the graph, whether you should have or not. Consequently, SU is deployed only rarely in most enterprises due to security concerns.

There are features of SHACL 1.2 that I think will change that, specifically node expressions. A node expression is a computed graph, meaning that the output of a node expression is a graph that does not actually exist within the knowledge graph itself. In SPARQL terms, it’s a CONSTRUCT expression; however, unlike CONSTRUCT, the output is determined by a shape (which can be thought of as being analogous to a VIEW). This means that if you have a way of specifying which SHAPE you are interested in, you also have a means of specifying which virtual graph you want to retrieve (_or you want to write to_).

The DESCRIBE statement in SPARQL should, in theory, be one of the most powerful aspects of the language, but in practice, it’s very underpowered. Suppose that instead you had a way to say “DESCRIBE this node using this SHAPE”. One shape may give you the ability to get a summary graph of the node, another may give you a deep structure of the same node, and the third may give you a representation that displays any dependent nodes as a summary list (think of RSS or Atom feeds).

With SPARQL, you have to create a complex query to achieve this, which is useful in perhaps 5% of cases but overkill for 95%. In SHACL, the SHAPE determines what is returned, and that shape can be controlled via ACLs.

Note that this is roughly what GraphQL does, but GraphQL is still too powerful (there are no limitations on what is returned) and imposes significant overhead. With SHACL node expressions, on the other hand, you have a good intermediate solution - something which generates a view of the data that is useful to a data consumer while still being protected via ACLs, and that also ensures that critical information within the graph that should nonetheless NOT be exposed to the public isn’t. This is a core requirement for almost any sector - medical, financial, legal, marketing data, etc., and turns a knowledge graph into a true knowledge base.

This is a relatively new technology, still in development, and while there are a few proprietary systems that do the same thing, none of them are built on the SHACL open standard foundation to date. I think that will change, and this will become an area of intense interest in the 2026-2030 timeframe.

I don’t see SPARQL going away, mind you. Instead, I see SPARQL becoming subsumed as an optional part of a SHACL 1.2 framework, something that can be used to write specialised rules that can’t readily be declared in any other way. However, because SPARQL is not a graph but rather a query language, it imposes significant limitations on what can be done with it.

## Hybrid AI Knowledge Graphs

This isn’t specifically an RDF knowledge graph per se, but rather an indication of where I see knowledge graphs going in the age of AI. Currently, most generative AI systems suffer from the same fundamental problems: they hallucinate. Graph RAG, in which the langchain of an LLM pulls in information from a symbolic KG, is a hack; the context of such a system is linear, and this means that a lot of the rich context that a knowledge graph has typically ends up getting flattened and serialized, often consuming so much of that context that meaningful LLM graphs don’t have any space to operate.

The next five years will see significant advances in how we design transformation systems; the current approach will likely prove to be a dead end, but this does not mean that we won’t find an architecture that gives us the best of both worlds. I suspect that it will not centre on the LLM's latent space. Still, in a re-engineering of the context as an in-memory graph in its own right, there are some very intriguing developments there on a number of fronts. However, most of these are still essentially frontier models.

Regardless, I still see a SHACL-based system as part of such a process, as SHACL provides a mechanism (especially as node expressions mature) to shape the output of LLMs and to support graph input for those same systems. This is a topic for a future post.

## Non-RDF Graph Systems

I should also address non-RDF-based systems. I do not expect graph systems such as Neo4J, TigerGraph, Cosmo, or other proprietary systems to go away, nor do I think they cannot be used for knowledge graphs, provided they have a mechanism to handle schema dynamics. There are also several newer systems (many of which I hope to review eventually) that may well mark a significant turning point in graph technology.

A primary reason I believe the W3C graph standards are essential is that they are open and not directly vendor-controlled. The W3C has a remarkable track record in that regard; it is not necessarily highly innovative, but if you look at what has survived over the years, it usually bears the W3C imprimatur. I attribute this to the fact that it is effectively a peer-reviewed standards design that incorporates input from several different perspectives.

I’m also increasingly of the opinion that SHACL will be the face of knowledge graph computing moving forward, because it IS both open and structurally oriented. The architecture for SHACL isn’t particularly new; it combines much of the work originating in XSD with a dynamic, rules-based model. If you accept that a shape is essentially a view, SHACL-based systems are pretty typical for symbolic type applications.

The future, of course, is not written in stone. Other standards may emerge; however, once a standard is established, it tends to have remarkable staying power. However, for now, SHACL and the W3C semantic stack will likely remain a major thread in working with knowledge graphs.

In media res,

[

![](https://substackcdn.com/image/fetch/$s_!YRtK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07173d1c-e65c-4e88-a1c1-efa1e2a646c3_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!YRtK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07173d1c-e65c-4e88-a1c1-efa1e2a646c3_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please consider contributing to support my work and allow me to continue writing.