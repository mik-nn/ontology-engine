---
title: "Coming soon"
source: "https://theinferenceengineer.substack.com/p/coming-soon?utm_source=profile&utm_medium=reader2"
date: "Mar 9"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!4VdO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F564ec432-d791-4662-9266-862255c9c261_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!4VdO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F564ec432-d791-4662-9266-862255c9c261_2688x1536.jpeg)

I’ve had a few conversations recently with people interested in becoming an ontologist (wow! finally, after too many decades!), in part because people are beginning to realise the value of knowledge graphs, but in part because, like many other fields in the past, ontology work is seen as being a ticket to big money. It’s probably worth dispelling the latter as a mythat the outset - it can pay reasonably well, but it is like any type of design work: you generally need a fairly high degree of expertise for a relatively short amount of time, and as such should be considered part of a particular skillset (especially information or data architecture) but not necessarily something that will keep you fully employed unless you work as a consultant.

An ontologist's position, at its core, is that of a data modeller. What this means in practice is that most of the job that you do is designing data models, and in that regard, it’s not all that different from any other architect position. Your goal, at the end of the day, is to identify the types or kinds of things that are important in a particular organisation (which usually tends to be fairly consistent for most things but can be widely divergent for others), then identify how they relate to one another. This model, in turn, can be used by developers to store and update information or to search datasets.

This can be broken down into the following tasks:

-   Working with business and technical stakeholders to determine which things are relevant to them as part of the organisation. This also involves ferreting out those objects which act as connective glue (contracts, products, things that tend to aggregate other things into more complex structures)
    
-   Establishing the relationships that exist between entities in an organisation. Sometimes these are obvious (Person:hasAddress, for instance), in other cases, the relationships are considerably more nuanced.
    
-   Expressing this information in a formal modelling language such as RDF. This can be done through modelling languages such as OWL or (more contemporarily) SHACL Shapes.
    
-   Building example content as test suites, as well as validating this content (this is especially the case with SHACL, which is designed for such validation).
    
-   Communicating the structures so created (think of SHACL, especially as a contract language between you, the stakeholders, and the development team).
    
-   Write SPARQL queries to perform generalised queries against datasets either for business logic or to handle common tasks (get all items of a given class or shape, ordered by some key). Such queries can actually end up making up a significant portion of an ontologist’s time.
    
-   Create documentation and visualisation of the associated ontologies
    

## Ontologist vs. Taxonomist

An ontologist frequently also does work that overlaps with that of a taxonomist, though the two have different roles:

-   The ontologist usually defines the language that the taxonomist uses to classify items within subject matter fields.
    
-   The taxonomist typically concentrates on the meaning and interpretation (i.e., the semantics) of specific classifications, while the ontologist focuses primarily on structural definitions that use these classifications.
    
-   The ontologist defines the properties, relationships and constraints that are used to categorise a given thing in a particular bucket, while the taxonomist usually uses these defined relationships to determine which particular bucket (class or shape) is used.
    
-   The ontologist may define a core (also called upper) taxonomy that is used to create the relevant scaffolding; taxonomists usually concentrate on subordinate classifications (subclassing).
    
-   The toolsets are usually different. Taxonomists typically work with a taxonomy management system that facilitates the definition and annotation of terms in a structured manner. An ontologist will often use more code-based tools that focus on building explicit data structures, which are often not as well-suited for taxonomy management.
    
-   A taxonomist will typically maintain a specific set of taxonomies, whereas ontologists will typically work on a project-by-project basis.
    

## Training to Become an Ontologist

There are several things that someone interested in working as an ontologist should focus on:

-   Become fluent with graph-based modelling languages, including RDF and LPGs (Neo4J in particular). On the RDF stack side, become familiar with Turtle, TRIG, JSON-LD, and RDF-XML.
    
-   Learn SHACL, RDFS and OWL. These are the languages that underlie almost the entire RDF stack, as far as modelling, validation, and increasingly documentation go. Know what the latter terms mean.
    
-   Learn SPARQL. SHACL can be thought of as a dedicated wrapper around SPARQL queries and filters.
    
-   Learn XSD. Yes, it’s XML, but a significant part of the RDF modelling language is heavily influenced by XSD, especially SHACL.
    
-   Learn JSON-LD, especially context files. It is likely that you will need to transition from Turtle to JSON-LD, then to XML-RPC (and increasingly to Manchester notation, which is built around YAML).
    
-   Spend time with Neo4J as well. It is possible to create an ontology (albeit not as easily) with Neo4J, and the app is widely used. Learn the distinction between the models - RDF can be used to build models that are conformant Neo4J (which has somehow become the poster-child for Labelled Property Graphs), but it means that you have to think about RDF reification in certain ways (fodder for my next post, in fact).
    
-   A background as a programmer building data structures can definitely help, especially when dealing with data interchange and data engineering. Ontologists often have to spend some time doing data conversions (especially from Excel and CSV).
    
-   Some experience as a business analyst, librarian, or taxonomist is also recommended, but not necessarily required.
    
-   Some knowledge of formal logical systems, especially predicate analysis and graph theory, is useful but again not required. Many ontologists do come from this background, and frequently have deep insights into the structural modelling and inferential logic in particular.
    
-   Knowledge engineering (that is to say, building ingestion pipelines and transformations) can also be a good stepping stone into semantics - a lot of knowledge engineers gain a basic grounding in RDF as one target for data systems flows.
    
-   Linguistics (especially computational linguistics) is a valuable asset, not only because there is significant overlap in working with structural graphs, but also because fluency in multiple languages can be beneficial when working on multilingual knowledge graphs.
    
-   I’ve also found that fluency with JavaScript, Python, or Java can help considerably, especially when dealing with ontologies outside the context of the database.
    
-   Finally, I believe that having a solid understanding of how LLMs and RAGs operate is becoming increasingly important in the field, as this often serves as a point of intersection between symbolic and neural network-based AIs.
    

Most training for ontology occurs at the Master's level, with institutions such as Oxford University, the University of Buffalo (NY), the University of Washington, Stanford University, the Massachusetts Institute of Technology, Rensselaer Polytechnic, and Edinburgh University offering courses in Computational Ontology. Many of these delve into specific areas, including biomedical ontologies, but they also provide a general foundation in semantic theory. Additionally, I strongly recommend The Semantic Web for the Working Ontologist by Dean Allemang and James Hendler, as well as Learning SPARQL by Bob DuCharme (all of whom I’ve known and, in some cases, worked with and consider mentors).

_I will get off my butt and get my own SHACL ontology book out soon. Watch this space!_

Note that I don’t think you need to have a Master’s Degree to become an ontologist. If you don’t want to install a triple store engine. Most LLMs (I especially like Anthropic’s Claude for this) can emulate a triple store fairly well. I’ll go into more detail about this in an upcoming post and show how you can use it to gain some proficiency with SPARQL and SHACL, both without needing to set up a heavy environment.

## Conclusion

Remember that an ontologist is a form of data architect, meaning that they shape how we represent information within an organisation. Conceptually, this is an odd role - up until comparatively recently, the notion that it was even necessary to do that would have been questioned, but the reality is that as organisations have become larger, more diffuse, and more data-oriented, the need to identify not only what is important to an organisation but also how it was shaped is becoming more and more pressing, and this is really what an ontologist does.

My gut feeling, after some forty years of watching how businesses evolve over time, is that some of the ontologist role is transient; it is, in fact, not hard to build standards today with LLM tools, and one of my principle arguments is that a key role for an ontology, especially with something like SHACL or OWL, is to serve as a contract that exists either between people within an organization or between two or more distinct organisations concerning the language for communication. This implies that a more subtle role for the ontologist is acting in the capacity of a lawyer or legislator concerning the language that binds people together, not so much creating that language, but ensuring that the language created is, in fact, desirable for all parties.

Something to think about, I suppose.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!CaAU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7b5dda1-d236-4631-b879-30a8851428f8_2048x2048.jpeg)

](https://substackcdn.com/image/fetch/$s_!CaAU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7b5dda1-d236-4631-b879-30a8851428f8_2048x2048.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please contact me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please consider contributing something to support my work, allowing me to continue writing.