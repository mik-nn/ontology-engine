---
title: "The Holonic Graph: A New Architecture for Knowledge That Thinks"
source: "https://inferenceengineer.substack.com/p/the-holonic-graph-a-new-architecture?utm_source=profile&utm_medium=reader2"
date: "Apr 2"
tags: [article]
---

Copyright 2025 Kurt Cagle/The Cagle Report

[

![](https://substackcdn.com/image/fetch/$s_!nSud!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F151522bc-06aa-4658-959c-269791983d61_2048x1168.png)

](https://substackcdn.com/image/fetch/$s_!nSud!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F151522bc-06aa-4658-959c-269791983d61_2048x1168.png)

Building a knowledge graph can be a significant undertaking, and consequently, it is worth taking the time to figure out if you need to make that effort in establishing one. There are a few questions you can ask when assessing this effort.

-   **Information Sharing.** Are you likely to need to share information consistently with others, either within or outside your organisation? An ontology can be seen as a data contract, an agreement between partners about how you intend to communicate, and as such can reduce ambiguity and simplify data interchange, with knowledge graphs on each side of the equations.
    
-   **Artificial Intelligence.** Are you communicating with an LLM for specific information in a structured form? Most LLMs have consumed common standards, such as schema.org or BFO, and can, with a certain degree of caution, reference these standardized ontologies to generate content with these particular constraints. This is discussed more in this paper below.
    
-   **Integration.** A knowledge graph (and its associated ontology) can make it far easier to both standardize on terminology and provide consistent information for integration, both by establishing specific nomenclature for variables (really helpful with Excel documents), and by acting as a data hub for transformation purposes.
    
-   **Master Data Management.** One of the most powerful aspects of a knowledge graph is its ability to manage keys (indeed, a knowledge graph at its core is a key management system). It can also be used to mint keys and track them across multiple platforms.
    
-   **360 Systems.** Most 360 systems (such as a Customer 360 system) are basically very weak knowledge graphs - they show the interrelationships between customers and other resources, but they tend to be very limited when it comes to showing other types of resources. A knowledge graph is a true 360 system, letting you see the whole of a business or organization, not just one very narrow part.
    
-   **Networked Systems.** Do you have networks of things that are all interrelated in your organizations - people within sub-organizations working on projects for clients involving products or equipment in different places? Relational databases can work reasonably well for comparatively simple networks, but past a certain point, the complexities can overwhelm relational systems, where ontologies and knowledge graphs begin to shine.
    
-   **Publishing and Authoring.** The authoring landscape is changing - single large books are increasingly becoming collections of interrelated modular sections, characters (intellectual property) become intertwined in an array of media, and different authors provide their own spin or stories on established characters changing histories. Knowledge graphs are a good mechanism for managing this complexity and to help with the authoring process, especially as more and more organisations take on many of the characteristics of publishing as once physical production goes virtual.
    
-   **Healthcare / IoT / Supply Chains** While one part of healthcare IT is focused on patient records, another key part is resource management, especially IoT devices and inventory (supply chain) control. Both are good candidates for knowledge graphs, as such systems tend to be graph-like in the first place. Supply chains can also be modeled as knowledge graph systems, usually in conjunction with event routers indicating state changes.
    
-   **Tracking Provenance or Context.** Knowing that data changes may not be enough - knowing why data changes can often be far more informative, but this requires having data about data (metadata) that may itself be complex. This is an area where knowledge graphs excel.
    
-   **Annotations and Commentary.** In a similar vein, being able to comment upon events (or comment about a comment) is becoming an increasingly important component in information systems (social media can be viewed in this light), regardless of where the original material resides. Knowledge graphs are well suited to this type of freeform content.
    
-   **Narrative Structured Content.** In general, while knowledge graphs are good at creating relationships between concepts contained in narrative structures (documents), markup content in general is better stored in XML (or HTML), though it can be transformed to RDF quite readily for analysis. A combination of a semantic store and a content store is very powerful, allowing you to take advantage of both, and significantly with most formats you can also embed RDF within HTML or XML (or vice versa).
    

## When Are Other Systems Better?

On the other hand, there are times when other kinds of data systems are better, though even there, they can integrate with knowledge graphs in other capacities:

-   **High-speed Transactional Systems.** When the incoming data is relatively linear and flat, it is generally better to use more traditional RDBMs systems, but you can use knowledge graphs as a way to store and retrieve analytics that derive from these systems (as well as to deeper graph analytics that can’t be done easily in an RDBMS).
    
-   **When Inferencing Doesn't Matter.** JSON stores are generally schema-less, and may be a better solution when dealing with information with a known consistent external structure (perhaps from a data feed) that just needs to be captured for later harvesting. However, knowledge graphs, in general, are better for storing processed content, as this can hold richer metadata, and an ontology can be useful even when inferencing (beyond a very simple layer for administration purposes) is not a strict requirement.
    
-   **Similarity Analysis.** Knowledge graphs are perfect when dealing with faceted searches where you're looking to find experts with known qualifications (as one example). However, they are less ideal for doing similarity searches, where you're looking for resources that may have similar attributes, but these attributes aren't known a priori. In this case, you may be better off working with a vector store. However, many more recent knowledge graph stores are incorporating vector-store functionality, including those used for LLMs.
    

It's worth noting in many cases that knowledge graphs can also provide part of the functionality of a system, and increasingly data stores are becoming hybrid, with KGs working in conjunction with other technologies in the same platform, rather than independently as the sole data repository.

## Conclusion

Knowledge graphs should be considered an integral part of your organization’s data life cycle - to facilitate integration, establish consistent terminology, store complex data structures, improve search and transformation, and ground artificial intelligence systems. They should not be seen as just another database but as a data hub to connect various heterogeneous data systems and applications and, as such, to ultimately power the applications and data processes that run your organization.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!YmRn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4d90817-b892-4ed3-9d72-e3e9fe56981c_1024x1024.jpeg)

](https://substackcdn.com/image/fetch/$s_!YmRn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4d90817-b892-4ed3-9d72-e3e9fe56981c_1024x1024.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.

## Recent Articles

[

## Creating a Simple Knowledge Graph (and a Pizza) with AI

](https://ontologist.substack.com/p/creating-a-simple-knowledge-graph)

·

January 27, 2025

[![Creating a Simple Knowledge Graph (and a Pizza) with AI](https://substackcdn.com/image/fetch/$s_!JO0t!,w_1300,h_650,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe049dab0-4e7c-438c-b261-af29819cede4_1344x768.png)](https://ontologist.substack.com/p/creating-a-simple-knowledge-graph)

Building a knowledge graph from scratch can seem like a daunting proposition, but if done right, you can put a pretty decent working ontology together in under an hour with an AI. It should be refined and tested before you put it into implementation, of course, but a big part of building knowledge graphs really come down to doing some homework before y…

[

## Hypergraphs and RDF

](https://ontologist.substack.com/p/hypergraphs-and-rdf)

·

January 25, 2024

[![Hypergraphs and RDF](https://substackcdn.com/image/fetch/$s_!PJxU!,w_1300,h_650,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2f4f3f2-1c8d-4370-9ea2-66da3169d4a8_800x512)](https://ontologist.substack.com/p/hypergraphs-and-rdf)

The topic of hypergraphs has come up of late in a couple of different discussion groups, and it seems like a good opportunity to explore what they are, and how they fit (or don’t) in the broader RDF ecosystem.