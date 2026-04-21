---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: The-Future-of-Knowledge-Graphs
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:00.957911+00:00'
  title: The Future Of Knowledge Graphs
  type: plain-doc
  version: '0.1'
---

# The Future Of Knowledge Graphs

[

![](https://substackcdn.com/image/fetch/$s_!pu3N!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7845baf8-7815-44d6-af47-27dc9d9920b1_1312x736.png)

](https://substackcdn.com/image/fetch/$s_!pu3N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7845baf8-7815-44d6-af47-27dc9d9920b1_1312x736.png)

Knowledge graphs seem to have sprung up out of nowhere in the last couple of years, but they are in fact one of the older data structures currently in use, dating back at least a quarter century. There are certain aspects that I see changing with knowledge graphs moving forward, especially in light of their frequently symbiotic relationship with generative artificial intelligence systems.

## Where Knowledge Graphs Came From

I began working with what are now known as knowledge graphs in 2002. They were not called knowledge graphs at the time, and I didn’t even know what RDF was (nor did many people). However, I had been working heavily with XQuery, a method for querying an XML database, in preparation for a book I was writing at the time for Wrox.

I realised that to avoid duplication of sub-documents when working with a “forest” of documents, it was necessary to refer to them by reference, ensuring there was only one document per identifier. This is an extension of the same principle that relational databases use, by the way, where subdocuments are “normalized” and then referred to by foreign keys.

It was only a year or so after that when I encountered RDF and realised that my “restful documents” were simply a restatement of that. Indeed, RDF-XML, one of the earliest XML representations of RDF, was built precisely with this principle in mind. Each `rdf:Description` element with its own `rdf:about` property is a subject node in a graph. There is also a slightly more compact representation of RDF-XML in use even today, which, with a few minor attribute add-ons, is indistinguishable from most XML documents.

RDF, consequently, has been around for about 25 years. In the mid-2010s, another form of graph, called a property graph (championed by Neo4J), emerged with a slightly different data model: nodes and edges both have properties, with edge properties describing the characteristics of the relationship, rather than either the subject or the object. About this time, the W3C RDF Working Group set up an activity to add reifications into the RDF model (as well as a few secondary additions), which makes it easier to support the underlying Neo4J model (also known as the OpenCypher model). This means that either form of graph can be transformed to the other without structural loss.

At the present time, RDF has the edge with regards to flexibility and expressiveness, though OpenCypher-based LPGs are somewhat easier to use for small to intermediate projects. However, the fact that they are isomorphic if not completely equivalent means that you are not limited by vendor choice to the same extent as was the case even a few years ago. It also means that discussions about where knowledge graphs are going can start from a common baseline.

## Knowledge Graph, Examined

A **Knowledge Graph Engine** is an application that stores and manipulates _labelled directed cyclic graphs_. What does that mean in non-mathematical terms?

-   **Labeled.** Each node and edge in a graph has an identifier, called its **label**. Label here is used in the machine sense - it is possible to give a particular key to either or both edges or nodes that allows them to be referenced and, in some cases, manipulated.
    
-   **Directed.** Each edge in the graph has an explicit direction, **from** a node **to** another node. This directionality is important because it provides a form of causal narrative (this was not necessarily a significant issue in the past, but it becomes an important consideration when dealing with AI systems.
    
-   **Cyclic.** Graphs can be cyclic or acyclic. An acyclic graph means that there are no closed circuits in the graph, which usually means that is possible to express the graph as a hierarchical tree. A cyclic graph, on the other hand, allows for some circuits. Knowledge graphs are typically nominally cyclic, meaning they have the potential to express circularity, but in practice, most knowledge graphs tend to be mostly acyclic. It turns out that this has implications for both database integrity and open vs. closed world assumptions.
    
-   **Graph.** A graph is a distinct set of triples, or directed Node-Edge-Node entities. These are often conflated with **assertions**, which are mathematical statements about a particular object’s properties or relationships. These are not necessarily the same thing - you can create a knowledge graph without having formal true/false assertions (this is especially the case when talking about Markov chains), so in some respects, you can think of a knowledge graph as a way to create contextual information about things.
    
-   A **knowledge graph engine** is an application that enables the storage, retrieval, and manipulation of graph information. In times past these were known as triple stores or similar terms, but given that both RDF and LPGs can construct knowledge graphs, referring to these as KG Engines makes more sense.
    

## RDF(-star) and LPGs

There are also two kinds of knowledge graphs today, predicate-bound (**RDF**) vs. attribute-bound (**LPGs**). In a property graph, the relationships that exist between the subject and object are considered a distinct object from either. Labelled property graphs can place attributes (which RDF calls literals) on either a node or an edge. For instance, the following describes the marriage between two people, Liz and Richard, in OpenCypher.

```
// Open Cypher
MATCH (liz:Person {name: 'Liz'}), (richard:Person {name: 'Richard'})
CREATE (liz)-[m:MARRIED {
    start_date: date('1990-07-01'),
    end_date: date('1996-05-30')
}]->(richard)
```

In RDF 1.0, there is no equivalent direct way to make such an assertion. Instead, you specifically create a marriage object that binds the two in a pattern that should be familiar as a third normal form:

```
Person:liz a Class:Person ; rdfs:label "Liz" . 
Person:richard a :Person ; rdfs:label "Richard" .
Marriage:LandMMarriage a :Marriage ;
    Marriage:spouses (Person:liz Person:richard) ;
    Marriage:startDate "1990-07-01"^^xsd:date ;
    Marriage:endDate "1996-05-30"^^xsd:date ;
    .
```

In RDF 1.2 (which is in its pre-recommendation stage), this can also be stated using a reification:

```
Person:liz a Class:Person ; rdfs:label "Liz" . 
Person:richard a :Person ; rdfs:label "Richard" .
<<Person:liz Person:married Person:richard>> a Marriage ;
    Marriage:startDate "1990-07-01"^^xsd:date ;
    Marriage:endDate "1996-05-30"^^xsd:date ;
    .    
```

Where the assertion `<<Person:liz Person:married Person:richard>>` is effectively a shorthand notation for an implied object (Marriage) that serves as a predicate. The upshot of this is that with 1.2, RDF can describe any OpenCypher construct (and can also handle the significant case where a reification can point to other object nodes, which Neo4J properties can’t do. I assume that OpenCypher will readily overcome this deficiency, which will only make the two forms of knowledge graphs increasingly conformant with one another.

The rest of this discussion assumes that when referring to RDF we are talking about RDF 1.2.

## Merging of Knowledge Graphs

It’s worth noting thatboth Google and AWS are creating knowledge graphs engines that can construct and query graphs using OpenCypher and RDF/SPARQL/SHACL and Microsoft is using OpenCypher as part of its GraphRag initiative. This means that in the near term (within the next 12 to 18 months) we are likely to see the unification of these two models in several significant ways:

-   **Reification** enables the discussion of assertions as entities. Additionally, it allows the qualification and constraint of properties, making them valid only when specific conditions are met (such as during a particular period or at a specific location). This COULD be done with RDF 1.0, but it was verbose and fairly inconvenient to work with. RDF 1.2 makes this easier and opens up other potential avenues for building more responsive knowledge graphs.
    
-   **SHACL.** The emergence of SHACL is making it easier to create ontologies that can work with both RDF and LPG. Because SHACL is focused primarily upon structure and constraint modelling, it can be translated into OpenCypher for execution in ways that are difficult to do with OWL. SHACL also does not presume dynamic inferencing (though there are areas of exploration here). My own belief is that SHACL will eventually be foundational not just for RDF, but at the broader level of data design and management, regardless of the encoding or storage method.
    
-   **Graph Traversal** has ironically always been a weakness of SPARQL. With OWL, traversal was primarily handled by creating superclasses that could be surfaced; however, due to performance limitations, the initial proposal for creating envelopes of traversal or path structures did not make it into the SPARQL specifications in either 2007 or 2013. This is where Gremlin and Tinkerpop come in, as well as several different magical properties in various implementations that allow for retrieving paths. These offer a potential template for generic actions that can be defined across systems. SPARQL 1.2 will likely incorporate such traversals, perhaps using Gremlin as the language.
    
-   What ultimately may come out of all of this is a generalised data path language (XPath was a good start in this direction, but the backlash from the JSON community was so strong in the late 2000s that the merits of the language never really got a fair hearing in the context of non-XML path languages. Paths and constraints play a significant role in SHACL as well, and the resolution of recursive path structures in SHACL may go a long way towards facilitating this (cf. [https://shaclrules.com/article/Advanced\_topics\_in\_SHACL\_rules\_such\_as\_inheritance\_and\_recursion.html](https://shaclrules.com/article/Advanced_topics_in_SHACL_rules_such_as_inheritance_and_recursion.html))
    
-   Recursion here is critical because most inheritance rules are, in fact, recursive rules with constraints. This is likely to shift the balance away from OWL and towards SHACL over the next decade.
    
-   In effect, what is happening is that knowledge graph engines are shifting into generalised data systems for managing complex, robust, interconnected content. However, in many respects, most other data systems can be abstracted in ways that allow them to be seen as knowledge graph systems with optimisation for specific types of operations. These ultimately point towards the unification of data access and update, regardless of whether you’re talking about RDF, OpenCypher, Key/Value Servers, column stores, or relational databases.
    
-   This does not solve the ontology problem - you still need to have ways of dealing with semantic differences in representation - but we are likely within a few years of being able to query or update any symbolic data store with a single stack of standards. This will go a long way towards making data and application integration feasible and manageable.
    

## Symbolic versus/and Neural Network AI

GenAI upset the apple cart. In late 2022, I recall telling the CEO of a graph engine company that everything was about to change, as ChatGPT went from being pretty bad to being pretty good, and all of a sudden, LLMs were everywhere. Many people who had been working on the symbolic side were suddenly faced with something that had the potential to devastate the field entirely.

However, by late 2023, there were new terms that were being tossed about - Retrieval Augmented Generation, hallucinations, context loss, and model degradation. It turned out that creating a giant database by slurping up the entirety of the Internet didn’t make for true artificial intelligence. Indeed, one of the biggest lessons to emerge from that time was that LLMs were very good at making things up, but that it was a pretty crappy database.

This shouldn’t have been that surprising. We went through this with Hadoop about a decade before, in which an innovative new technology - distributed map/reduce across grid computing took the programming and data analytics world by storm. Hadoop was a powerful technique for processing, especially since one of its most common uses was in indexing.

All data systems are built around indexing. A key/value store, for instance, is a recursive bare index. A knowledge graph engine is built around about six core indexes, with the use of named graphs adding another layer of indexing. Indexing makes possible quick access to resources, but it also requires some form of curational pre-processing. In essence, with an index, you are creating a memory of essential searches so that you don’t have to perform the hard work every time you query.

Hadoop got this part of the process right, but forgot that there was much more to a database than its index. Performance, ACID transactional integrity, security, and ease of use all become critical for adoption. The reality was that Hadoop databases were slow, awkward to work with, and lacked many of the features that other databases had incorporated a decade earlier. Within a few years, Hadoop had faded (though not without changing the dynamic for large-scale cloud computing), and it may have been, in hindsight, Java’s last hurrah.

The rise of large language models and generative adversarial networks over the last few years has dramatically changed the conversation. Both enable the production and transformation of text, imagery, music, and video, provide a means for translation and auto-classification, and detect and utilise patterns in data. This is what neural networks excel at. If the primary focus on these technologies had been primarily in these areas, GenAI would likely have cemented its reputation as a critical part of any workflow.

However, just as with Hadoop, GenAI excels in certain areas, but it isn’t a database. Why is this so important? You can think of databases, including knowledge graphs, as a form of symbolic AI. They are very good at storing and retrieving data quickly. They are consistent: what you put in should be what you get out, assuming that no one else has changed the contents. They have a consistent structure that a schema can define, and that can consequently be validated against that schema. They can be consistently transformed.

Note the keyword here: **consistency**. LLMs are inconsistent. They are slow because they do an incredible number of calculations for each call and require a huge amount of contextual memory to stay “focused”. They are unpredictable. They produce hallucinations. They are obscenely expensive to build and to use. These are all characteristics that should disqualify them from being even remotely considered as databases, yet they are still being marketed as data sources. Why? Because databases sell, consolidation and concentration of services sell, and LLMs give the illusion that, for people who don’t understand how to write programs, they can program.

I made the contention, late in 2003, as the LLMs were tearing up the landscape, that the transformer model would have more and more problems because it has no genuine concept of persistence. Because the underlying model was ultimately stochastic, hallucinations wouldn’t be cured by adding more stochastic generators.

One (very reluctantly adopted) solution to this was to modify the LangChain process so that other data sources could be added, a process rather ignomiously known as Retrieval Augmented Generation (or RAG). In a nutshell, this meant that when a prompt is submitted, the prompt is parsed and passed to an external process that then reads a database (or some other source like a PDF) converts it into some text format (most likely JSON) and adds it into the context that will then be used to communicate with the large language model.

The use of RAG improves the accuracy of responses, as the tokens added via RAG provide a minimal baseline of content when the token vector of the context is matched against the latent space of the LLM. This is a pseudo-index; in essence, the set of all possible conversations that incorporate the tokens in a particular order is retrieved, and the one with the highest possible weighting compared to the prompt (i.e., the one with the nearest vector) is returned to the requester.

Think of each conversation as a potential circuit, as electricity moves from one side to another. As it does so, it passes through other circuits that may or may not terminate back in the line. The longer the path, the more desirable it is (within certain limits), pulling in additional threads of conversation in the process. These side threads are essentially context, providing further detail from the LLM that usually serves as the “explanations” for the prompt’s ask.

RAG content, in general, provides narrative content that is sufficiently interwoven, typically creating better circuits than the LLM itself. This is part of the reason that you can “query” a document to get summaries and overviews. The LLMs provide connective tissue for dialogues that are already present in the context, rather than directly providing the narrative.

With GraphRAG content, on the other hand, the content is already “predigested” to a certain degree. Any database is far more regular than conversational or written content. As such, the pattern-matching facilities of LLMs can generate exemplars—templates for generating output —that tend to align strongly with existing narrative structures. A table, for instance, has a clear structure, reading narratively from left to right, with the first column typically containing property heads, and each row corresponding to a specific item. The LLM doesn’t necessarily “know” the significance of the labels, but it does recognise structure, and because tokens are scanned based on order, the further from the initial heading listing, the more likely that the pattern matching breaks down. This is a big part of the reason why LLMs tend to struggle with PDF tables, but can work relatively well with JSON structures (where the correlation between tag and value is high) and works exceptionally well with XML.

This latter point is worth restating. Narrative structures are graphs. They are not necessarily knowledge graphs, but are closer to the kinds of graphs you created as kids in English diagramming a sentence. Sentences have subordinate clauses (that can frequently also have subordinate clauses), prepositional phrases, and conjunctive expressions. LLMs are optimised to handle deep stacks as a consequence, where such clauses are pushed onto a stack until they are resolved.

Circling back around, we need to understand that narrative structures, while graphs, are not knowledge graphs, if by 'knowledge graph' we mean an easily accessible data structure. A knowledge graph is a conceptual shorthand for a narrative where we’ve taken out the less relevant context (i.e., we’ve abstracted the concept from its underlying context), with the understanding that, if needed, we can reinflate the graph into a narrative form. As such, I see LLMs as an (imperfect) way of doing such reinflation.

## The Shifting Semantic Landscape

I posit a few things here:

-   RDF-Star (RDF with a reification model) is a fundamental model. It is the topological equivalent of the Periodic Chart in chemistry or the Standard Particle Model in Physics. Just as chemistry is more about the interactions and structures that can be made from these atomic components than it is the components themselves, we need to understand that RDF-star provides the core building blocks. Still, it is up to us to build the abstractions.
    
-   Similarly, the standard model of physics _informs_ the periodic table, just as quantum chromodynamics (QCD) informs quark interactions that make up the standard model. Each is an abstraction that describes a domain or scope, and like any abstraction, there is always a certain amount of leakiness; however, a good model recognises where that leakiness (the need for additional context) lies. There is likely a layer of abstraction beneath RDF, but it does not (primarily) affect how RDF creates graphs.
    
-   RDF-star, even in incarnations like Turtle-star and JSON-LD, is complex because data structures are complex. Organic chemistry, for the most part, consists of about a dozen or so kinds of atoms, yet organic chemistry is complex because those dozen or so atoms can be combined in so many different ways. What we are struggling with at this point is that we don’t have a good abstraction layer in place for those structures - we don’t have an organic chemistry body of knowledge that represents higher-order structures, nor do we know how to effectively organise distributed meshes of graphs.
    

This all points to what I see coming next in this space:

-   **Classes are out, Shapes are in.** A data shape is a way of describing a knowledge molecule. Ontologies become complicated because everything is represented as a class, and the way we build classes largely involves inheritance. Shapes are more contextual and open-ended; you can describe the characteristics of classes that have different properties that change upon the context in which they are embedded. This becomes especially powerful when combined with SPARQL, which allows you to determine that context very robustly. This may bring us closer to the level of organic chemistry.
    
-   **Dynamic Knowledge Graphs.** There are several ways to build knowledge graphs. The first is to capture the current state, where the KG is updated to reflect only the most recent state of a given system. This can be readily accomplished now with SPARQL Update, which is often vastly underutilised even now. There are many times when I wonder why we spend so much time building intermediation layers for getting triples into knowledge graphs when, in most cases, you can build much cleaner systems by simply using SPARQL Update. The second approach is to either build models or use reification to create conditional knowledge graphs (KGs). The latter is better suited for Long graphs where property values (and even their associated entities) change over time, and you want to retain this value for analytics; however, it also makes for more complex queries. I expect that we’ll see additional abstraction layers that make this process less painful and more transparent.
    
-   **Event Driven KGs.** Systems are event-driven. We receive and interpret signals (messages), then figure out what to do with them. A knowledge graph is a description of an environment, with entities interacting within it, and this shift is changing the way we think about knowledge graphs from a store of knowledge to a self-contained simulation system.
    
-   **Hybrid LllamaGraphs.** A llama graph is a system that combines the generative aspects of large language models (LLMs) with the grounding of symbolic systems. GraphRAG is a (very early) example of where this could be heading. Still, I think that a combination (perhaps even in silicon) of the two into a neurosymbolic data system will be the next central stage of evolution. Do I believe that LLMs will replace symbolic graph systems? No, not as they are constituted now. I do think that in five years, the distinction between the two will be much more difficult to discern.
    
-   **Functional Robustness.** One of the more powerful and intriguing aspects of SHACL the advanced functional module in SPARQL (https://www.w3.org/TR/shacl-af/) and Javascript functions:
    

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/ns#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

ex:myFunction
    a sh:Function ;
    sh:jsFunctionName "myCustomFunction" ;
    sh:parameter [
        sh:path ex:param1 ;
        sh:order 1 ;
     ] ;
     sh:parameter [
        sh:path ex:param2 ;
        sh:order 2 ;
     ] .

ex:MyShape
    a sh:NodeShape ;
    sh:targetClass ex:MyClass ;
    sh:property [
        sh:path ex:myProperty ;
        sh:filterShape [
            sh:node [
               sh:function ex:myFunction ;
               ex:param1 "value1" ;
               ex:param2 "value2" ;
            ]
        ]
    ] .
```

With the indicated function then defined and bound as Javascript:

```
function myCustomFunction(param1, param2) {
  // Access the RDF terms using the SHACL-JS API
  console.log("Parameter 1:", param1);
  console.log("Parameter 2:", param2);
  //Perform validation logic
  return true;
}
```

This is a general binding, so it’s not unrealistic to expect Python, C++, PHP, or other language bindings getting added to the mix.

This capability is significant for a number of reasons. The ability to transform shapes into programmable objects and back makes it possible to deal with information both in a query and a programmatic context simultaneously. Additionally, there are many operations on graphs that extend beyond the fairly minimal subset that SPARQL offers, and as has been proven repeatedly, waiting for standards to change can be a gruelling slow process. Finally, with SHACL Functions it turns SPARQL and SPARQL Update calls into actual functional methods.

-   **Data Meshes - the Revenge of Linked Data.** As much as I am a fan of RDF, I will readily claim that Linked Data has failed. Part of the problem is the mechanics of querying across a vast array of systems simultaneously (this will only be alleviated by increased bandwidth and faster processors). Still, part of the problem is also that most people in the semantic space (myself included) underestimated how much the ontological aspects of linked data would ultimately impede action. The problem is meta-ontological - there are different design patterns and upper ontologies, each of which tends to have distinct predicate structures and query paths, making it problematic to connect to another semantic store to query it.
    
-   **SHACL and Data Transformation.** Data meshes (and initiatives such as Solid) appear to be the second iteration of this process, and they are struggling to some extent with the same problems. This is an area where I think SHACL and AI may make a difference; however, a given system can query another system for its SHACL files and then use that to transform SPARQL or other query languages into something that can work across the language boundary. This raises an interesting question - while I think SHACL will end up being a lingua franca for semantic interchange, I also expect that it will do so as a higher end and more precise version of JSON-Schema, which to me has always seemed underpowered (I’m seeing more and more people adopting it as a JSON schema language, interestingly enough).
    
-   **The Phasing Out of OWL.** There are likely to be many people who disagree with me on this point, but I believe that OWL will likely fade away over time for several reasons.
    
    -   **Ageing Spec.** It’s no longer evolving (in comparison to the rest of the RDF stack), and those people most familiar with it are retiring. Protege, which was many people’s first introduction to the Semantic Web, announced that it's no longer being maintained. With this announcement, likely, many of the design patterns it introduced will also disappear.
        
    -   **Fading Reasoners and SPARQL.** Similarly, reasoners, which were fundamental to OWL, are disappearing from newer knowledge graph systems, partly because there is no real demand and partly because SPARQL and SPARQL Update are more targeted in their capabilities. Without reasoners, OWL becomes much more complicated to work with.
        
    -   **AI.** AI is not _fully_ capable of reasoning, but when supported by semantic data, it is likely to be an improvement over handcrafted reasoning graphs. Expect this trend to continue.
        
    -   **A New Generation of Ontologists.** It takes a while to train a good ontologist (8-10 years, primarily because of the need to understand data modelling), and you tend to become most comfortable with the technology that was emerging when you were younger. This means that many of the up-and-coming ontologists today were exposed to SPARQL UPDATE and SHACL early in their careers and are therefore more open to thinking about data in that light. I suspect that within the next ten years, SPARQL and SHACL will be passe and we’ll be on to the next big thing, but certainly the trends are not favourable for OWL among practitioners.
        
-   **Abstraction Libraries.** As mentioned earlier, the future is shapes. This will result in new paradigms emerging, and RDF-Star will become just another deep protocol. There are also some interesting developments in category theory that I think need to be closely monitored. I hope to discuss these topics further in future posts.
    

## Summary

Knowledge graphs will never be as flashy as large language models or GenAI. They won’t command big headlines, and in general, while more people know what they are, there won’t be a mad rush to be the next great technology. Money-hungry investors need not apply, because KGs, quite frankly, are _boring_.

You know what? That’s okay. Most solid engineering is. I believe that some very interesting developments will occur over the next few years in the field, particularly for individuals working with complex information systems, ontologies, and the nature of language as a programmable tool. Knowledge engineers are the nerds of the AI world, often overlooked and underappreciated. Still, they are most frequently the ones who end up writing that critical piece of code that keeps the whole system from collapsing into irrelevancies, especially when your shiny new Agentic system has just ordered 30,000 kilos of coal to be delivered to your house because of a hallucination.

Ontologists aren’t going away any time soon.

In media res,

[

![](https://substackcdn.com/image/fetch/$s_!JvG7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83d097aa-e5d9-478b-a41d-d3f13b0447e1_1392x752.png)

](https://substackcdn.com/image/fetch/$s_!JvG7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83d097aa-e5d9-478b-a41d-d3f13b0447e1_1392x752.png)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.

