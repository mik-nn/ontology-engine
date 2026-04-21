---
title: "SHACL Taxonomy Revisited"
source: "https://ontologist.substack.com/p/shacl-taxonomy-revisited?utm_source=profile&utm_medium=reader2"
date: "Mar 8"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!hcgQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8e04411-88ee-44bc-bd05-20cd0d19f67f_1344x768.png)

](https://substackcdn.com/image/fetch/$s_!hcgQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8e04411-88ee-44bc-bd05-20cd0d19f67f_1344x768.png)

Copyright 2025 Kurt Cagle / The Ontologist

Ontologies come in various styles that reflect different intents, historical age, and structural organisation. Knowing the difference can help you decide what kind of ontology you need for your own particular organisation or application.

## Glossaries and Vocabularies

The simplest ontologies are typically **vocabularies** or **glossaries** - sets of terms that are listed, defined (described), and occasionally contain acronyms, synonyms, and related terms. They usually have a straightforward document-oriented structure and seldom are usually very shallow, perhaps with some keyword differentiation tied to a formal or informal taxonomy. Most content management systems are specialised glossaries.

A good example of a glossary knowledge graph is something like Wikipedia (or more technically, Wikidata), where the ontology is primarily focused on the structural content of the entries. This is also a case where the encoding of the schema is actually managed primarily as something like an XSD document, rather than RDF, per se, but there is a lot of overlap.

## Taxonomies

Taxonomies provide organisations of categories, which can be thought of as groups of related knowledge domains. Perhaps the most famous taxonomy is the Linnaeus taxonomy, first established in the 18th century as a way of organising different groups of animals and plants primarily based upon similarity, though such taxonomies go back millennia. Library catalogs such as the Dewey Decimal System or the Library of Congress system are another form of taxonomy.

[

![](https://substackcdn.com/image/fetch/$s_!wx7t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b87d4f8-5394-4a5d-b7e6-33ac492f6563_2415x3840.png)

](https://substackcdn.com/image/fetch/$s_!wx7t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b87d4f8-5394-4a5d-b7e6-33ac492f6563_2415x3840.png)

Dewey Decimal System with detail of one branch.

Typically, taxonomies or hierarchical and are organised along degrees of specificity. For instance, an organisation chart (org chart) for a company is a kind of taxonomy, with power roles devolving the further you are in the tree from the senior executive for the corporation.

This process of devolution usually follows a single property (such as skos:narrower) that identifies roles that have narrower scopes. Such taxonomies typically have relatively few predicates beyond these base ones, beyond a general "related" term, with the rest of the terms focusing on annotations (an item's nomenclature, textural definition, acronyms or abbreviations and so forth). Many business ontologies incorporate a taxonomic layer that not only identifies specialised categories but also may identify the categories of the elements described by these categories as data sets (e.g., Employees and Customers may both be considered categories in the taxonomic portion of a business ontology).

## Enterprise Knowledge Graphs

Enterprise ontologies are what most people think of when dealing with ontologies. These are typically also referred to as knowledge graphs. These usually describe the objects and relationships of the most important entities to an organization and tend to focus heavily on customers, employees, vendors, products, services, brands, and similar entities.

These graphs are highly connected and factor into production and media generation. Some are comparatively static, others are more temporarily-oriented, and frequently incorporate taxonomies as subgraphs within the overall graph.

[

![](https://substackcdn.com/image/fetch/$s_!BQGI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc3ab4307-4e91-49ae-9eb1-86229509d637_1701x3840.png)

](https://substackcdn.com/image/fetch/$s_!BQGI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc3ab4307-4e91-49ae-9eb1-86229509d637_1701x3840.png)

A simple knowledge graph

## Data and Service Catalogues

These systems provide a breakdown of data structures within databases, web service endpoint locations, parameters and output, and functional libraries. In effect, such catalogues offer input and output definitions for data generators and consumers and are increasingly used for AI Agentic Systems. These often also include Access Control Level data to indicate who has access to these systems.

## Master Data Management

One of the more complex problems in computing is master data management - being able to identify when two records represent the same object (or when two similar objects may not be the same thing). If you have two knowledge graphs (ontology + data) with data coming from different sources that have different identifiers, the knowledge graph by itself is not likely to be able to solve this by itself. However, a knowledge graph working in conjunction with a vector store that has just enough metadata to indicate similar pairs can often handle both sides of the equation - using the vector store for similarity analysis (identifying the likely matches) then using the knowledge graph for deep comparisons and retrieval provides a nice complementary set of capabilities that mirror KGs + LLMs (which are, after all, vector stores).

## Operational Ontologies

Some ontologies specifically focus on designing structures, identifying rules or enabling processes. This includes the RDF Schema ontology (RDFS), OWL (Web Ontology Language), SHACL (Shape Constraint Language, ODRL (Open Digital Rights Language), PROV-O  and many others. These ontologies are usually very specialised and are comparatively small but have an outsized influence in the ontology community. They also usually have minimal taxonomies but tend to utilise data structures more heavily than other systems.

## Upper-Level Ontologies (ULO)

There are frequently referred to as base, top or abstract ontologies or as ontological frameworks. An upper-level ontology (ULO) is a special kind of operational ontology which defines abstract classes that can be subclassed to provide a framework for interfaces. These are toolkits for building other ontologies, though most tend to target the enterprise knowledge graph audience. These include systems such as GIST, the Basic Formal Ontology (BFO), and generalised ontologies such as Schema.org. It is possible to use these out of the box, but in most cases, you will want to extend these ontologies for specific use cases.

## Local Ontologies

When you create a relational schema, a spreadsheet, a PDF file or similar documents that have an implicit schema, it is convenient to discuss these as if they were RDF documents with their schemas. Tools such as TARQL or R2RML can be used to extract triples from these documents, and especially with spreadsheets, these tools can use column names as predicates to generate RDF. These **local ontologies** usually have (at best) a very informal schema, but because that ordering is generally consistent, the resulting content can be mapped to more formal schemas.

The advantage of such an approach is that your integration can be seen as the attempt to map from one ontology to another, rather than as a bespoke, one-off operation. This makes architecture somewhat easier, as a processing pipeline can be abstracted as a series of ontological transformations.

## Canonical Ontologies

Your organisation has particular data modelling needs specific to its mission; consequently, you likely have a distinct language unique to that organisation. This language, or ontology, is often called a canonical ontology because it consistently unifies terminology within that organization. Canonical ontologies may be built on other ontologies but are also usually extended to handle specific needs. The key value of a canonical ontology is that it can act as a data interchange hub. Rather than trying to hold each potential pairing between disparate ontologies, it becomes a reference intermediary that other ontologies can be transformed into or out of.

[

![](https://substackcdn.com/image/fetch/$s_!D-T1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0a96a21-0917-4a6c-a3e0-6deaf345fbde_3840x2722.png)

](https://substackcdn.com/image/fetch/$s_!D-T1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0a96a21-0917-4a6c-a3e0-6deaf345fbde_3840x2722.png)

The principle advantage of creating a canonical ontology is that you replace a combinatorial number of transformations (one for each pair of ontologies that you're working with) with just two consistent transformations, one from the source ontology to the canonical ontology, the second from the canonical ontology to the target ontology. This can radically simplify the management of your ontological space, especially in those cases where each ontology represents a separate database, spreadsheet, document, activity stream or even simplified new graphs (see below).

## Interchange or Pidjin Ontologies

An interchange ontology is used to communicate between different systems. This differs from a canonical ontology in that it often has a more general, simplified architecture to get a reasonable amount of shared information across while not necessarily describing everything in the graph, and it differs from a local ontology by being a commonly agreed upon standard.

Schema.org is a good example of an interchange ontology. It is a broad ontology containing several classes with reasonably comprehensive properties. It may not necessarily reflect an organisation's internal canonical ontology. Still, because of its breadth, it will likely contain enough information that other organisations can understand the language involved and translate it into their internal canonical image. Most industry ontologies are interchange ontologies - good at getting essential information across even if they don't necessarily reflect the ontology of any organisation.

## Temporal vs. Now Ontologies

Time is … complicated. Information changes regularly; a canonical ontology should track these changes, typically via reifications. Such graphs tend to be complex to query (and, in many cases, querying these directly may cause security concerns). Such canonical graphs are also known as **temporal graphs** because they are sensitive to time and other constraints.

On the other hand, a **now** graph represents a certain snapshot in time in which the constraints are set to a particular set of conditions. These graphs are often considerably more straightforward, in part because there is no need to establish such constraints and in part because specific properties can be calculated in the now graph that may be inefficient to do so in the temporal graph, such as the average of time series data. Moreover, complex data structures can be collapsed in the **now** graph, making it easier to access the information.

[

![](https://substackcdn.com/image/fetch/$s_!JNFU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19920cce-4ffb-4cb8-9f80-4fa6ab4832db_781x403.png)

](https://substackcdn.com/image/fetch/$s_!JNFU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19920cce-4ffb-4cb8-9f80-4fa6ab4832db_781x403.png)

The ontology of a temporal graph will be different from the ontology of the now graph, though it will likely be similar. The **now** graph, being calculated will also be somewhat out of sync with the temporal graph. The advantage of having two such graphs is that the **now** graph can be made public for query. In contrast, the temporal graph is equivalent to a staging server containing ongoing information curators can maintain independently, including versioning information. In contrast, the **now** graph only displays the most recent version.

## Final Thoughts

This taxonomy is neither comprehensive nor exclusive, but it does provide a way to figure out the general structures of what you’re trying to do with an ontology. I hope to dig deeper into each of these, especially the Enterprise Knowledge Graph, as this is an area that most people are currently exploring.

I started The Ontologist late in 2023 with great intentions, but found that maintaining multiple newsletters and multiple life issues (thank the gods that 2024 is in the rearview mirror, even if 2025 looks disturbing). I’m working on my new book Context now, discussing ontologies, AI, and language in general, and will be posting excerpts from that book here on The Ontologist as I complete them, so expect more regular posts in the future. I also have more multimedia plans for The Cagle Report and The Ontologist, including eventually a course on my own particular RDF-based methodologies.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!pVwx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe303b5ae-6d59-4311-89e8-e0b117e09212_1024x1024.jpeg)

](https://substackcdn.com/image/fetch/$s_!pVwx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe303b5ae-6d59-4311-89e8-e0b117e09212_1024x1024.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.