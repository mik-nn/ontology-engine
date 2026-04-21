---
title: "What Does SHACL Do?"
source: "https://ontologist.substack.com/p/what-does-shacl-do?utm_source=profile&utm_medium=reader2"
date: "Mar 19"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!W3Mh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43bf3cee-a860-4da3-be85-25953be94de0_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!W3Mh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43bf3cee-a860-4da3-be85-25953be94de0_2688x1536.jpeg)

We’re beginning to see the effects of knowledge graphs and context graphs bringing significant improvements in the reliability of LLM responses (and a corresponding reduction in hallucinations), something I (and others) have been predicting for some time. In this post, I present my thoughts on _why_ this may be the case and explore how it could be implemented and what its limitations are.

## Definitions

I need to define several terms, each building on the previous one, for this to be clear.

-   **Constraint.** A specific limitation on how a given property is expressed - its cardinality (permissible number of items per property), data type, the patterns used by literals (text encoded string), upper and lower limits of data ranges and so forth. Constraints serve to box in permissible values in the data.
    
-   **Schema**. The aggregate of all of the constraints that the data follows. A schema can be thought of as a blueprint for how data is structured, known as its data model. UML is a form of schema, as is Data Definition Language (DDL used by SQL), Regular Expressions, the XML Schema Definition Language, and even MCP (which can be thought of as one way of limiting the possible parameters and return values of services). SHACL (the Shape Constraint Language) is, at its core, a schema.
    
-   **Taxonomy.** A system of classification. The Dewey Decimal System, Library of Congress (LoC) Classifications, the Linnaean Classification, and the Simple Knowledge Organisation System (SKOS) are all forms of taxonomy. This is typically used to impose _semantic_ constraints, ensuring that a particular property value is drawn from a set of well-defined enumerated values.
    
-   **Assertion.** An assertion is a statement that follows schematic constraints. It need not be true (most data systems assume truthiness without defining it), but it must be internally consistent with other assertions in a belief system.
    
-   **Belief System.** This, loosely, is a framework of assertions taken as internally consistent, and can be formulated as follows: if you believe in X and X implies Y, then you believe in Y.
    
-   **Graphs.** An assertion can usually be decomposed into a set of simpler assertions (think of sentence diagrams from grade school) that have a specific direction (typically moving from past to future). The set of decomposable assertions is connected into networks, also known as graphs. Graph theorists usually refer to these as labelled directed cyclic graphs (LDCGs). In the semantic sense, when we talk about graphs, we usually mean LDCGs, which are the most generalised form of graphs (all graphs can be represented as LDCGs).
    
-   **Nodes and Edges.** A node is a representation of a thing via a specific identifier. An edge is a connection between two nodes that specifies a relationship. In an LDCG, an assertion connects a node to another node via an edge in a certain direction, from the subject (the node that identifies a thing) to the object (the node that bears the relationship to the subject). The relationship itself is called a predicate. This is often abbreviated as SPO and can be considered the direction of the assertion.
    
-   **LDAGs**. A Labelled Directed Acyclic Graph is a graph in which no loops form (if you traverse the graph, you’ll never encounter a given node more than once). A hierarchy is a form of LDAG, as is a tree. LDAGs may be embedded within LDCGs, meaning that while all LDAGs are LDCGs, not all LDCGs are LDAGs. This gets into **topology**, which is the generalised study of data shapes.
    
-   **Data Shapes.** Most data fall into specific data structures. Linked lists, hierarchies, sequences, bags (also known as hash tables or dictionaries), and similar structures are all examples of data shapes. Data shapes are a natural consequence of schemas, and they are composable (you create more complex shapes from simpler ones). SHACL is the Shape Constraint Language, which indicates how shapes can both be validated and composed.
    
-   **Reifications and Hypergraphs.** A reification is an assertion not about a particular thing, but a particular relationship between two things. A hypergraph is a graph that allows for reifications. Both RDF 1.2 (an extension to RDF) and labelled property graphs (LPGs) allow for reifications, and consequently are hypergraphs. (**Note:** there is a mathematical definition of a hypergraph that is a little more expansive, but in terms of LDCGs, thinking of a hypergraph as being a graph that supports reification is usually a good compromise.
    
-   **Property Paths.** The sequence of labelled edges that connect two nodes in a graph. Property paths make shapes possible. XPath was an early property path language in XML. SPARQL and SHACL are both built on property paths.
    
-   **Validation.** A particular graph can be considered **shape valid** if it satisfies the constraints imposed upon it by its shapes. It is considered **semantically valid** if every assertion in a graph is either a fundamental axiom or can be composed from fundamental axioms - it is, in effect, “proved” logically.
    
-   **Rules.** A rule is a definition that defines how a predicate (a property, for all intents and purposes) is defined, given a particular data shape. Rules consistently generate new assertions from existing assertions. A rule usually consists of the structural validation of a given node, followed by the construction of one or more new assertions.
    
-   **Inferences and Contexts.** To infer something means that you can make a consistent assertion within the belief system (graph) by showing that there is one or more rules that can be articulated in that belief system that lead to the generation of that assertion. A **context** in that regard is the minimal subset (or subgraph) of assertions that satisfy those rules for a given assertion. The context, to quote columnist Paul Harvey, is _the rest of the story_.
    
-   **Narrative.** If you start on a particular node and follow the directed property path within an LDCG, the set of assertions follows a (usually hierarchical) network. If you serialise it based on the network's subtrees in encounter order, you obtain a narrative. This is true for any graph, whether it is an assertion graph used for knowledge graphs or the implicit latent space that enables large language models.
    
-   **Knowledge Graph.** A knowledge graph is an LDCG graph in which data is largely represented by conceptual topics and entities. It is used frequently for both master data management and encyclopedic coverage. You can think of a knowledge graph as a particular design pattern for RDF, but it’s not the only one, simply the one that most people are familiar with.
    
-   **Context Graph.** A context graph differs from a knowledge graph in that it primarily serves as a log of events and their surrounding context. This may contain relevant information, but it shifts the focus from curated content that is relatively easily searchable and highly integrated to viewing the world through the lens of events, which often can provide a more historical perspective of the evolution of entities. Note that knowledge graphs and context graphs are complementary: the context graph ingests information and serves as a system of record, while the knowledge graph synthesises this information and makes it more accessible. A good system likely employs both. Note that an enterprise context graph is still a context graph.
    
-   **Ontology.** An ontology is the combination of the schemas, taxonomy, and rules that collectively describe the behaviour of a graph. Some ontologies describe tools for creating other ontologies, whereas others are primarily organisational, historical, or topical.
    
-   **Symbolic AI.** The combination of schemas, taxonomies and rules collectively makes up what is often dubbed Symbolic AI. This works on the assumption that symbolic AI is discrete rather than continuous (fuzzy), though you can build fuzzy qualifiers into symbolic AI by treating assertions as qualified statements with one or more symbolic weights (likelihood, statistical priors, confidence of authorship, etc.).
    

## A Quick Guide to LLMs

Large Language Models first became widely used around 2018, as part of the evolution of natural language understanding systems. They are also definable by definitions:

-   **Corpus/Training Set.** Neural networks are trained by examining numerous data examples to identify patterns. This is known as the training set, and is usually labelled. It may consist of dozens to billions of documents.
    
-   **Neural Network.** A neural network typically involves a filter algorithm to identify patterns based on labelling data or tokenisation, and, from that, to apply a transformation to these elements. This transformation typically involves clusters of similar points, which can be used for classification, typically employing linear algebra in high-dimensional spaces to map those clusters.
    
-   **Tokenisation.** Tokenisation involves the breakdown of source documents into individual words, small groups of words, or patterns. These create very long arrays, each cell of which is associated with a specific token or pattern, indicating the relative frequency of these tokens compared to other tokens
    
-   **Encodings and Latent Spaces.** In neural net terms, this takes that array for each document and converts it into a vector of what’s called a Latent Space. The system records each token’s label and also indicates patterns in the preceding and following tokens. The latent space thus contains tokens (which approximate semantic concepts) and their proximity to other tokens in this high-dimensional space, based on similarity and velocity. The closer a token is to such points in latent space, the more likely it is to be involved in one or more narratives. Note that this latent space forms a fuzzy fractal network of overlapping narratives, which bears some resemblance to a graph. I refer to this as a **quasi-graph,** or **fuzzy graph**, and it is classified as an accretion fractal in chaos theory.
    
-   **Transformers.** A transformer works by making the documents as small as possible (usually only a few hundred tokens long, max) in order to determine similarity (using encoding algorithms such as TF-IDF or BM25) to create vectors to identify where in this latent space a particular narrative resides, then uses a similar conversion to take prompts and use them to find the closest relevant mappings. The upshot is that this, too, yields a directed graph. It’s not necessarily semantic - there’s no real curation involved beyond the selection of the initial corpus. In effect, the transformer identifies the space of narratives most closely related to the prompt, then walks the best-fit graph to deserialise the resulting graph into a particular narrative. This is how an LLM “talks” to a person in a linear stream.
    
-   **Weights.** Each document has a specific weight; some carry greater significance than others. These weights affect the surrounding space, altering the clustering and, consequently, the potential topology of the quasi-graph. Weights are typically encodings of tensors (think generalised matrices) that get multiplied against the initial latent space to determine which concepts are closer or farther away.
    
-   **Temperature.** Within a latent space, the concept of distance is important, but not necessarily intuitive, especially when dealing with high-dimensional content (most latent spaces are in the 10,000 to 25,000 dimension category, far higher than can be visualised by even the most genius human beings). Temperature in a large language model is a measure that is used to determine how far out in the latent space a given set of tokens can be in order to be detectable for selection. When the temperature is low, only the nearest tokens are selected, which often yields very sparse token responses; this can improve accuracy but also be much more stultifying. As the temperature increases, the search range expands, but the likelihood of narratives that are less relevant (or irrelevant) also rises. This can provide much more polished text, but lead to far more hallucinations. This is a fundamental limitation of the model, and it’s mathematical in nature.
    
-   **Context Window and LangChain.** The context window can be thought of as the working memory of an LLM. When a prompt is submitted, this is the buffer that holds the tokenised prompt. It also holds additional information - usually guardrails, but also the responses from previous prompts in order to create continuity in chats. The context window is managed by a process called a LangChain, which is still, in many respects, one of the most important parts of an LLM, primarily because of its role in RAG.
    
-   **RAG and GraphRAG.** Retrieval-Augmented Generation (RAG) was originally a hack (reluctantly implemented) in LangChain that enabled tokenisation of external content through a service architecture. GraphRAG was similar, in effect passing the serialisation of a graph as a data source. Both are useful because they add specific tokens into the context window that represent the serialisation of narratives, and because they are part of the prompt context, they have a higher priority of appearing in the resulting graph before serialisation. The challenge with GraphRAG is that it doesn’t necessarily constrain the rules of what the data structures look like, but only provides an ad hoc pattern that the LLM has to interpret through learning by example. Moreover, a knowledge graph is a very compact representation of information, meaning that some knowledge graphs can rival LLMs in terms of size and complexity.
    
-   **Agentic Services.** The implementation of agentic services ultimately comes back down to the development of a mix of RAG and LLM content, often using other LLMs to do validation and fact checking.
    

## SHACL as LLM MadLibs

The next piece of the puzzle is understanding that SHACL, SPARQL, and RAG all operate on similar principles.

One way of thinking about a latent space is to imagine that each token in the latent space is a magnet. The further away in that space two such tokens are placed, the less attraction they have to one another. Words that are similar to one another, such as king and prince, in general, the more they attract one another. Queen and princess, on the other hand, are similar in some respects but different than others, say they may be conceptually similar but in different directions.

Additionally, narrative structures tend to be more attractive. For instance, you can talk about both “Elizabeth Windsor, who was the Queen of England” and “Charles Windows, who is the King of England”. Elizabeth and Windsor have a fairly strong attraction, Elizabeth and Queen have a very high attraction, and Queen and England have a very high attraction, especially when joined by “of”. Note that ordering here is important - “Queen of England” occurs very frequently, but “England of Queen” almost never occurs, so there is a bias in the direction that is embedded within the latent space. (There’s a natural grammar that can be analysed and converted into a schematic ontology, but this is somewhat tangential here, though gist for another article in the near future.)

This level of attraction is important in understanding the mechanism for prompts. A prompt tokenises the text, but every token in the text has a 100% association with the next term in the prompt, because that next term has already been produced. This is why changing word order in a prompt can have an impact upon how a prompt is interpreted (and why entering prompts in reverse order can confuse an LLM).

Each token has a particular coordinate in latent space, and LangChain uses the LLM's temperature to determine not only what is closest but also what has the strongest associations. Tokens that are swept up then have an intrinsic bias based on the previously selected tokens, which, in turn, determine narrative order. Prompted tokens carry the greatest weight, and prompted alternatives always carry greater weight than anything in the latent space. Put another way, if the temperature is zero, you should get back the prompt you put in, as the serialisation of a graph. On the other hand, when the temperature is higher, the number of threshold narratives can get to be quite high, so you have to compare the best candidate narratives primarily based on how closely attracted the respective tokens in that graph are in that latent space.

You could embed a graph in the latent space, but this assumes the graph is static, which loses many of the benefits of graph-based information, and the overall weight of such a graph will still be lower than the token weights in the prompt. Graphs can grow large quickly; however, passing the graph in toto is usually not feasible.

However, consider this from an RDF-Star perspective.

```
ex:ElizabethWindsor ex:role ex:Queen ~ {| ex:of ex:England, ex:from "1956"; ex:to "2024" |} .
ex:Queen rdfs:subClassOf ex:Ruler .
```

This is a reification, because there are queens of many countries, but Elizabeth as queen is actually the assertion being qualified. It also closely matches the narrative structure as given above.

SPARQL solves this through decomposition:

```
SELECT $PERSON $ROLE $REGION WHERE {
    ?person ex:role ?role .
    ?person ex:label token($PERSON) .
    ?role ex:label $token(ROLE) .
    ?reifier rdf:reifies triple(?person, ex:role, ?role).
    ?reifier ex:of ?geoRegion .
    ?geoRegion ex:label token($REGION) .
    optional {
       ?reifier ex:from $FROM .
       filter($DATE >= $FROM)       
       }
    optional {
       ?reifier ex:to $TO.
       filter($DATE < $TO )       
       } 
    }
```

The $PERSON, $ROLE, $REGION, $FROM, and $TO variables are all labels, and are different from the camel case variables that are specifically IRIs. The token function is a hypothetical function that converts a work or phrase into a specific tokenised form.

If you ask a question of an RDF database, you must know its schema. You can sort of get around it if that schema follows certain conventions (use of `rdfs:label` or `rdf:type`, but all too often, constructing a query often involves digging into the data structure. This is one of the real benefits of an LLM - you can query it without knowing a schema, but it comes at the cost of not having a manageable structure.

Let’s build a set of SHACL 1.2 shapes for describing this structure:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

# ============================================================================
# SKOS Concept Shapes
# ============================================================================

# Base shape for all SKOS Concepts
ex:ConceptShape
    a sh:NodeShape ;
    sh:targetClass skos:Concept ;
    sh:property [
        sh:path skos:prefLabel ;
        sh:datatype rdf:langString ;
        sh:uniqueLang true ;
        sh:message "Each concept should have one preferred label per language" ;
    ] ;
    sh:property [
        sh:path skos:altLabel ;
        sh:datatype rdf:langString ;
        sh:message "Alternative labels must be language-tagged strings" ;
    ] ;
    sh:property [
        sh:path skos:definition ;
        sh:datatype rdf:langString ;
        sh:message "Definitions must be language-tagged strings" ;
    ] ;
    sh:property [
        sh:path skos:broader ;
        sh:class skos:Concept ;
        sh:message "Broader concepts must be SKOS concepts" ;
    ] ;
    sh:property [
        sh:path skos:narrower ;
        sh:class skos:Concept ;
        sh:message "Narrower concepts must be SKOS concepts" ;
    ] ;
    sh:property [
        sh:path skos:related ;
        sh:class skos:Concept ;
        sh:message "Related concepts must be SKOS concepts" ;
    ] ;
    sh:property [
        sh:path skos:inScheme ;
        sh:class skos:ConceptScheme ;
        sh:minCount 1 ;
        sh:message "Concept must belong to at least one concept scheme" ;
    ] .

# Shape for Concept Schemes
ex:ConceptSchemeShape
    a sh:NodeShape ;
    sh:targetClass skos:ConceptScheme ;
    sh:property [
        sh:path skos:prefLabel ;
        sh:datatype rdf:langString ;
        sh:uniqueLang true ;
        sh:minCount 1 ;
        sh:message "Concept scheme must have at least one preferred label" ;
    ] ;
    sh:property [
        sh:path skos:hasTopConcept ;
        sh:class skos:Concept ;
        sh:message "Top concepts must be SKOS concepts" ;
    ] .

# ============================================================================
# Domain-Specific Concept Shapes
# ============================================================================

# Shape for Role concepts (Queen, King, President, etc.)
ex:RoleConceptShape
    a sh:NodeShape ;
    sh:targetNode ex:Ruler, ex:Queen, ex:King, ex:President ;
    sh:property [
        sh:path rdf:type ;
        sh:hasValue skos:Concept ;
        sh:minCount 1 ;
        sh:message "Role must be typed as skos:Concept" ;
    ] ;
    sh:property [
        sh:path skos:inScheme ;
        sh:hasValue ex:RolesScheme ;
        sh:minCount 1 ;
        sh:message "Role concept must be in the Roles concept scheme" ;
    ] ;
    sh:property [
        sh:path skos:broader ;
        sh:class skos:Concept ;
        sh:message "Role must have broader role concept if hierarchical" ;
    ] .

# Shape for Geographic Region concepts
ex:GeoRegionConceptShape
    a sh:NodeShape ;
    sh:targetNode ex:GeoRegion, ex:Country, ex:England ;
    sh:property [
        sh:path rdf:type ;
        sh:hasValue skos:Concept ;
        sh:minCount 1 ;
        sh:message "Geographic entity must be typed as skos:Concept" ;
    ] ;
    sh:property [
        sh:path skos:inScheme ;
        sh:hasValue ex:GeographyScheme ;
        sh:minCount 1 ;
        sh:message "Geographic concept must be in the Geography concept scheme" ;
    ] ;
    sh:property [
        sh:path skos:broader ;
        sh:class skos:Concept ;
        sh:message "Geographic region should have broader geographic concept" ;
    ] .

# ============================================================================
# Person and Role Assertion Shapes
# ============================================================================

# Shape for Person with role assertions
ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:property ex:PersonShape-role .

ex:PersonShape-role
    a sh:PropertyShape ;
    sh:path ex:role ;
    sh:class ex:Role ;
    sh:minCount 1 ;
    sh:message "Person must have at least one role" ;
    # Validate the RDF-star annotations (reifier) on the role triple
    sh:reifierShape ex:RoleAnnotationShape .

# Shape for validating the reifier (RDF-star annotations)
ex:RoleAnnotationShape
    a sh:NodeShape ;
    sh:property [
        sh:path ex:of ;
        sh:class ex:Country ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "Role assertion must specify exactly one country" ;
    ] ;
    sh:property [
        sh:path ex:from ;
        sh:datatype xsd:gYear ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "Role assertion must have exactly one start year" ;
    ] ;
    sh:property [
        sh:path ex:to ;
        sh:datatype xsd:gYear ;
        sh:minCount 0 ;
        sh:maxCount 1 ;
        sh:message "Role assertion may have at most one end year" ;
    ] ;
    sh:property [
        sh:path ex:from ;
        sh:lessThan ex:to ;
        sh:message "Start year must be before end year" ;
    ] .

# ============================================================================
# Role and Geographic Entity Shapes
# ============================================================================

# Shape for Role (connects to SKOS concepts)
ex:RoleShape
    a sh:NodeShape ;
    sh:targetClass ex:Role ;
    sh:property [
        sh:path rdf:type ;
        sh:hasValue skos:Concept ;
        sh:minCount 1 ;
        sh:message "Role must also be typed as skos:Concept" ;
    ] ;
    sh:property [
        sh:path skos:broader ;
        sh:class skos:Concept ;
        sh:minCount 1 ;
        sh:message "Role must have a broader concept" ;
    ] ;
    sh:property [
        sh:path skos:prefLabel ;
        sh:datatype rdf:langString ;
        sh:minCount 1 ;
        sh:message "Role must have at least one preferred label" ;
    ] .

# Shape for Country
ex:CountryShape
    a sh:NodeShape ;
    sh:targetClass ex:Country ;
    sh:property [
        sh:path rdf:type ;
        sh:hasValue skos:Concept ;
        sh:minCount 1 ;
        sh:message "Country must also be typed as skos:Concept" ;
    ] ;
    sh:property [
        sh:path skos:broader ;
        sh:hasValue ex:GeoRegion ;
        sh:minCount 1 ;
        sh:message "Country must be broader than GeoRegion" ;
    ] ;
    sh:property [
        sh:path skos:prefLabel ;
        sh:datatype rdf:langString ;
        sh:minCount 1 ;
        sh:message "Country must have at least one preferred label" ;
    ] .

# ============================================================================
# Concept Schemes
# ============================================================================

ex:RolesScheme
    a skos:ConceptScheme ;
    skos:prefLabel "Roles and Positions Concept Scheme"@en ;
    skos:definition "A hierarchical scheme of roles and positions"@en ;
    skos:hasTopConcept ex:Ruler .

ex:GeographyScheme
    a skos:ConceptScheme ;
    skos:prefLabel "Geographic Regions Concept Scheme"@en ;
    skos:definition "A hierarchical scheme of geographic regions"@en ;
    skos:hasTopConcept ex:GeoRegion .
```

This also presumes the following SKOS concepts, as well as a restatement of the original reified statement:

```
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

# ============================================================================
# SKOS Concept Hierarchies
# ============================================================================

# Role hierarchy
ex:Ruler 
    a ex:Role, skos:Concept ;
    skos:prefLabel "Ruler"@en, "Souverain"@fr ;
    skos:definition "A person who exercises sovereign authority over a territory"@en ;
    skos:inScheme ex:RolesScheme ;
    skos:topConceptOf ex:RolesScheme .

ex:Queen 
    a ex:Role, skos:Concept ;
    skos:prefLabel "Queen"@en, "Reine"@fr ;
    skos:altLabel "Queen Regnant"@en ;
    skos:definition "A female monarch who rules in her own right"@en ;
    skos:broader ex:Ruler ;
    skos:inScheme ex:RolesScheme .

ex:King 
    a ex:Role, skos:Concept ;
    skos:prefLabel "King"@en, "Roi"@fr ;
    skos:definition "A male monarch who rules in his own right"@en ;
    skos:broader ex:Ruler ;
    skos:related ex:Queen ;
    skos:inScheme ex:RolesScheme .

# Geographic hierarchy
ex:GeoRegion 
    a skos:Concept ;
    skos:prefLabel "Geographic Region"@en, "Région Géographique"@fr ;
    skos:definition "A defined area of the Earth's surface"@en ;
    skos:inScheme ex:GeographyScheme ;
    skos:topConceptOf ex:GeographyScheme .

ex:Country 
    a ex:Country, skos:Concept ;
    skos:prefLabel "Country"@en, "Pays"@fr ;
    skos:definition "A political entity with defined borders"@en ;
    skos:broader ex:GeoRegion ;
    skos:inScheme ex:GeographyScheme .

ex:England 
    a ex:Country, skos:Concept ;
    skos:prefLabel "England"@en, "Angleterre"@fr ;
    skos:altLabel "Angleland"@en ;
    skos:definition "A country that is part of the United Kingdom"@en ;
    skos:broader ex:Country ;
    skos:inScheme ex:GeographyScheme .

# ============================================================================
# Person with RDF-star Role Assertion
# ============================================================================

ex:ElizabethWindsor 
    ex:role ex:Queen ~ {| 
        ex:of ex:England; 
        ex:from "1952"^^xsd:gYear; 
        ex:to "2022"^^xsd:gYear 
    |} ;
    a ex:Person .
```

Once you have this information, you can use the pattern matching inherent in the SHACL graph to construct the relevant SPARQL query:

```
#Prompt

Using the defined SHACL, write a SPARQL-Star query to answer the question: Who was the ruler of England in 1982?
```

[

![](https://substackcdn.com/image/fetch/$s_!HRzM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4044c38-ba30-45b0-9e6a-32d7f7bfd72f_2048x2048.jpeg)

](https://substackcdn.com/image/fetch/$s_!HRzM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4044c38-ba30-45b0-9e6a-32d7f7bfd72f_2048x2048.jpeg)

This uses Claude with the above SHACL definition, and generates the following SPARQL-Star:

````
PREFIX ex: <http://example.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?person ?roleName ?from ?to
WHERE {
    # Match the triple term with annotations
    <<?person ex:role ?role>> ex:of ex:England ;
                              ex:from ?from ;
                              ex:to ?to .
    
    # Ensure the role is a type of Ruler
    ?role skos:broader* ex:Ruler .
    
    # Get the role's preferred label
    OPTIONAL { ?role skos:prefLabel ?roleName . FILTER(lang(?roleName) = "en") }
    
    # Filter for 1982
    FILTER(?from <= "1982"^^xsd:gYear && ?to >= "1982"^^xsd:gYear)
}
```
````

This generates the following results when queried against a supporting triple store:

```
?person                 ?roleName    ?from   ?to
ex:ElizabethWindsor    "Queen"@en   1952    2022
```

A similar query can return a graph. The SPARQL-Star:

```
PREFIX ex: <http://example.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

CONSTRUCT {
    <<?person ex:role ?role>> ex:of ex:England ;
                              ex:from ?from ;
                              ex:to ?to .
}
WHERE {
    <<?person ex:role ?role>> ex:of ex:England ;
                              ex:from ?from ;
                              ex:to ?to .
    
    FILTER(?from <= "1982"^^xsd:gYear && ?to >= "1982"^^xsd:gYear)
    
    ?role skos:broader+ ex:Ruler .
}
```

This creates the following Turtle output:

```
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:ElizabethWindsor ex:role ex:Queen ~ {| 
    ex:of ex:England ;
    ex:from "1952"^^xsd:gYear ;
    ex:to "2022"^^xsd:gYear 
|} .
```

Which is where we started.

Once you have this, you can then pass the generated output to an LLM for post-processing:

```
# Prompt
Working with the derived Turtle (reprinted here, create a human language representation.

@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:ElizabethWindsor ex:role ex:Queen ~ {| 
    ex:of ex:England ;
    ex:from "1952"^^xsd:gYear ;
    ex:to "2022"^^xsd:gYear 
|} .
```

This in turn generates within the LLM the following output:

_Here are several human language representations of varying detail:_

## _Concise Version_

_**Elizabeth Windsor was Queen of England from 1952 to 2022.**_

## _Structured Versions_

### _Narrative Form_

_Elizabeth Windsor held the role of Queen. This role was specifically of England, beginning in 1952 and ending in 2022._

### _Formal Description_

_**Subject:** Elizabeth Windsor

**Role:** Queen

**Jurisdiction:** England

**Period:** 1952–2022

**Duration:** 70 years_

### _Detailed Explanation_

_This statement describes Elizabeth Windsor’s role as Queen. The core assertion is that Elizabeth Windsor had the role of Queen. Additionally, this role relationship carries contextual information: it was a role specifically over England, it began in the year 1952, and it concluded in the year 2022._

## _Technical Explanation_

### _RDF-star Structure Explained_

_The triple has two parts:_

_**Base Triple:**_

-   _Elizabeth Windsor (subject) → had the role of (predicate) → Queen (object)_
    

_**Annotations on the Triple:** The relationship itself has three properties:_

-   _**Location:** England (where this role applied)_
    
-   _**Start Date:** 1952 (when the role began)_
    
-   _**End Date:** 2022 (when the role ended)_
    

### _Timeline Representation_

```
Elizabeth Windsor as Queen of England
|
1952 ========================== 2022
     [70-year reign]
```

## _Question-Answer Format_

_**Q: Who was Elizabeth Windsor?**

A: Someone who held the role of Queen._

_**Q: Queen of where?**

A: England._

_**Q: When did she serve as Queen?**

A: From 1952 to 2022._

_**Q: How long was her reign?**

A: 70 years._

## _Natural Language Variations_

-   _Elizabeth Windsor reigned as Queen of England for 70 years, from 1952 until 2022._
    
-   _The Queen of England from 1952 to 2022 was Elizabeth Windsor._
    
-   _Elizabeth Windsor’s tenure as Queen of England spanned from 1952 to 2022._
    
-   _Between 1952 and 2022, Elizabeth Windsor served as Queen of England._
    

## _Key Semantic Points_

_The RDF-star notation_ `~ {| ... |}` _captures **metadata about the relationship itself**, not just about the entities. This allows us to say:_

-   _✅ The role relationship is temporally bounded_
    
-   _✅ The role relationship has geographic scope_
    
-   _✅ These properties belong to the relationship, not to Elizabeth Windsor or Queen as standalone entities_
    

_This is more precise than saying “Elizabeth Windsor was born in 1952” or “Queens rule for 70 years” - it specifically describes **this particular role relationship**._

The key point is that you can use SHACL to generate SPARQL for a given query against an external knowledge graph, which in turn yields the requested results as a table, JSON, graph, or similar structure. This can then be passed back to the LLM to ensure that the prompt contains sufficient relevant information (and is limited to that information) to be consistent with the knowledge graph, a process I call _grounding_.

You can additionally ask the LLM to generate additional content that does not come from the grounding, and to indicate it in the output:

```
# Prompt
Repeat, but add additional information that may be relevant, indicating in the output what content may be less reliable because it comes from unsourced content.
```

This generates the following:

_Here are enriched human language representations with reliability indicators:_

## _Concise Version_

_**Elizabeth Windsor was Queen of England from 1952 to 2022.**_

_Note: She is commonly known as Queen Elizabeth II and also reigned over other Commonwealth realms beyond England.\[^uncertain\]_

## _Structured Narrative_

### _Core Facts (from data)_

_Elizabeth Windsor held the role of Queen of England from 1952 to 2022, a reign of 70 years._

### _Contextual Information (inferred/general knowledge)_

_Elizabeth Windsor is more commonly known by her regnal name, **Queen Elizabeth II**.\[^uncertain\] She became Queen following the death of her father, King George VI, on February 6, 1952.\[^uncertain\] Her coronation ceremony took place on June 2, 1953.\[^uncertain\]_

_While the data specifies “England,” she was actually the monarch of the **United Kingdom** (which includes England, Scotland, Wales, and Northern Ireland) and served as head of state for numerous Commonwealth realms including Canada, Australia, and New Zealand.\[^uncertain\]_

_She died on September 8, 2022, at Balmoral Castle in Scotland,\[^uncertain\] making her the longest-reigning British monarch in history.\[^uncertain\] She was succeeded by her son, who became King Charles III.\[^uncertain\]_

## _Detailed Explanation with Reliability Markers_

### _What We Know For Certain (from the RDF data):_

-   _**Subject:** Elizabeth Windsor_
    
-   _**Role:** Queen_
    
-   _**Geographic Scope:** England_
    
-   _**Start Year:** 1952_
    
-   _**End Year:** 2022_
    
-   _**Duration:** 70 years (calculated)_
    

### _What We Can Reasonably Infer:_

-   _The role ended due to her death (end dates for monarchies typically indicate death unless abdication)\[^uncertain\]_
    
-   _She was likely born before 1952, probably in the 1920s (to be an adult monarch)\[^uncertain\]_
    

### _Additional Context (unsourced):_

-   _**Full Title:** Her Majesty Queen Elizabeth II\[^uncertain\]_
    
-   _**Birth:** April 21, 1926, in London\[^uncertain\]_
    
-   _**Accession:** February 6, 1952 (though coronation was June 2, 1953)\[^uncertain\]_
    
-   _**Full Territorial Scope:** United Kingdom and Commonwealth realms, not just England\[^uncertain\]_
    
-   _**Family:** Daughter of King George VI and Queen Elizabeth; mother of King Charles III\[^uncertain\]_
    
-   _**Significant Events:** Ruled through major historical periods including decolonization, the Cold War, and Brexit\[^uncertain\]_
    
-   _**Death:** September 8, 2022, age 96\[^uncertain\]_
    
-   _**Legacy:** Longest-reigning British monarch, longest-serving female head of state in history\[^uncertain\]_
    

## _Timeline with Reliability Indicators_

### _Verified from Data:_

```
1952 ================================ 2022
     Elizabeth Windsor as Queen
```

### _Enriched Timeline (unverified):_

```
1926[?]          1952                                    2022[?]
  |               |                                        |
 Born[?]      Became Queen                              Died[?]
           (Feb 6, actual)[?]                    (Sept 8, specific)[?]
           (Jun 2, coronation)[?]
```

## _Question-Answer Format with Sources_

_**Q: Who was Elizabeth Windsor?**

A: ✓ Someone who held the role of Queen.

A: \[^uncertain\] More commonly known as Queen Elizabeth II; born 1926._

_**Q: Queen of where?**

A: ✓ England (as stated in the data).

A: \[^uncertain\] More accurately, the United Kingdom and Commonwealth realms._

_**Q: When did she serve as Queen?**

A: ✓ From 1952 to 2022 (confirmed in data).

A: \[^uncertain\] Specifically from February 6, 1952, to September 8, 2022._

_**Q: How long was her reign?**

A: ✓ 70 years (calculated from dates).

A: \[^uncertain\] 70 years and 214 days, making her the longest-reigning British monarch._

_**Q: What happened in 1952 and 2022?**

A: ✓ These mark the beginning and end of her reign.

A: \[^uncertain\] 1952: Her father King George VI died. 2022: She died at age 96._

## _Reliability Legend_

_Symbol Meaning ✓ **Verified** - directly stated in the RDF data (calculated) **Derived** - logically computed from verified data \[^uncertain\] **Unsourced** - from general knowledge, not verified by the provided data \[?\] **Speculative** - reasonable inference but uncertain_

## _Semantic Precision Notes_

### _What the Data Actually Says:_

_The RDF triple makes a very specific claim: there is a relationship between “Elizabeth Windsor” and “Queen” via the property “role,” and this relationship has three annotations:_

-   _Geographic scope: England_
    
-   _Temporal start: 1952_
    
-   _Temporal end: 2022_
    

### _What the Data Does NOT Claim:_

-   _✗ That “Elizabeth Windsor” is the same person as “Queen Elizabeth II”\[^uncertain\]_
    
-   _✗ The specific dates within those years\[^uncertain\]_
    
-   _✗ Why the role ended (death vs. abdication)\[^uncertain\]_
    
-   _✗ That she ruled over territories beyond England\[^uncertain\]_
    
-   _✗ Any biographical details (birth, family, etc.)\[^uncertain\]_
    

### _Data Quality Considerations:_

_**Potential Issues:**_

-   _The scope “England” may be imprecise; the UK would be more accurate\[^uncertain\]_
    
-   _Year-level precision (xsd:gYear) loses the specific dates\[^uncertain\]_
    
-   _The identifier “Elizabeth Windsor” is her family name, not her regnal name\[^uncertain\]_
    

_**Why This Matters:** In a knowledge graph context, linking this data to other authoritative sources (Wikidata, DBpedia, etc.) would allow verification and enrichment of these uncertain claims while maintaining provenance._

_\[^uncertain\]: This information is not present in the provided RDF data and comes from general knowledge or inference. It should be verified against authoritative sources before use in critical applications._

This raises an important point. The knowledge graph lists Elizabeth Winsor as the queen of England, but her remit was actually that of the United Kingdom as well as serving as symbolic head of a number of other countries. A knowledge graph may have erroneous, incomplete, or poorly curated data; what a knowledge graph does do is provide a consistent data modelled in a consistent way.

An example of this (not explored here) is that you may have a knowledge graph that describes the people, products, places, properties, etc., for your organisation, something that won’t likely be in a large-scale LLM. This information is much more likely to be up-to-date and reflective of the state of the organisation, and may even provide a temporal or event-driven approach to that data (in other words, be a context graph).

## SHACL as a Contract

I’ve laid these out both to ensure we are all on the same page and to substantiate a point. I have defined terminology and, more specifically, advanced terminology based on simpler terms. I have established an agreement between me, as the writer, and you, as the reader, regarding the language we use to communicate. I have done so by defining more complex **rules** constructed from similar assertions, by providing **constraints** governing how the terms and relationships interact, and by identifying the principal classes of entities and common concepts under consideration through classification.

SHACL is the shape constraint language. It is a **contract** I make as the designer of a graph, ensuring that the rules and constraints are followed. By using the graph, you are implicitly agreeing to this language … whether _you_ are a human being or an LLM. An ontology comprises _**rules**_, _**constraints**_, and _**taxonomy**_. At its core, it is as defined by SHACL.

There are many ontologies. Some of them are very useful. Some of them are a waste of space and time. Many were developed by practitioners addressing a particular use case and attempting to extend it, only to discover that problem domains differ across organisations. All too often, people choose ontologies because others use them, or it was the first one that they encountered on Google when they searched, or because it’s what they remember when they did a semantics proof of concept problem twenty years ago. They want to do as little actual design work as possible, in part because many business leaders view design work as a waste of time rather than an integral part of innovation.

Here’s the reality. The moment that you decide to borrow an ontology, you will come across use cases that you don’t understand or that don’t seem applicable to your domain, and you will fork that ontology. Over time, as your enterprise data requirements evolve, the data will increasingly deviate from the source ontology, a phenomenon known as ontological drift. I believe that extant ontologies should be seen as templates, points of departure, but if you’re going to do work in the semantic space, your ontology will be unique to your specific organisational scope. This is fine; there is absolutely nothing that says that you can’t use a starter kit, but be aware that going in, this is what is going to happen.

Here’s where you can get value out of that ontology, and ultimately, it has to do with LLMs … and SHACL (and by extension SPARQL). SHACL defines the structure, indicates where classes are used for classification (taxonomy) and can evaluate rules (which you can think of as computed assertions or statements, like a person who was born in 1960 being 66 years old in 2026. It can do so recursively, compose complex, context-sensitive data structures, and work with hypergraphs (which I believe reification enables). You can build other ontologies from SHACL, including the Ur-languages of OWL, RDF-Schema, SKOS, and so forth. It’s the assembly language of semantics.

An LLM does not need to load the entirety of your knowledge graph OR context graph into its context window. It’s a waste of time and money, is not really what LLMs are good at, and destroys one of the big advantages that knowledge graphs have: KGs can evolve in real time, LLMs cannot.

Instead, you load the SHACL and sufficient of the taxonomy to provide relevant classifications (ironically, preferred labels, alternative labels, and descriptions). Use Turtle - every LLM since Gato (the earliest version of ChatGPT) knows how to work with Turtle, and it is a very terse representation that’s ideal for use with graphs. Add it to your skills.md or operating code, and perhaps integrate it into the data evaluation layer code, so that you can load _only the SHACL you need_.

Similarly, you can load the SHACL and other forms of data (including LLM sourced content) in order to cause the data in question to adhere to the structure and taxonomy of the relevant ontology, as well as to compute relevant information based upon clearly articulated rules. This becomes absolutely essential when dealing with text (especially meeting and interaction transcripts), imagery, and video, but it can also facilitate transformations between data types. Moreover, if a source and target shacl are provided, a transformer can generate a mapping function so that the source can be mapped to the target as closely as possible without having to regenerate this transformation repeatedly.

## Benefits and Drawbacks of SHACL with LLMs

There are many good reasons as to why you would do this:

-   If you have the SHACL and a services-enabled knowledge graph, have the LLM read the SHACL, then use this as a basis for generating a SPARQL query against the knowledge graph that uses that SHACL. You’ve given the LLM instructions about what the data shape looks like, and once you have that, writing queries becomes straightforward, especially for an LLM.
    
-   If there is no answer, you can indicate that the question is not meaningful or that the information is unknown, rather than having the LLM return a fabricated response. This can help to segregate known information from generated but potentially inaccurate information.
    
-   You end up needing far fewer tokens once you move past the SHACL declaration. This can significantly reduce token costs, particularly for complex answers.
    
-   You can introduce computed nodes into the dataset using SHACL without introducing black-box calculations. This makes SHACL-based LLM systems more accurate and resilient.
    
-   The resulting dataset from those queries can be converted into any format required for tokenisation. What you are tokenising at that point is usually abbreviated forms of IRIs and related literals (again, Turtle is great for this). LLMs like Turtle make not just terms but narrative patterns trivial to create as graphs, which the LLM already works with. This essentially short-circuits the need to do extensive queries against the LLM because you’ve already had the system build the graphs in the first place.
    
-   Do you understand the Turtle? Does it really matter if you don’t? The output of the resulting Turtle will be used by the LLM to generate a more comprehensive Markdown output. Let the LLM do what it’s good at - transforming - while letting the knowledge graph do what it’s best at - maintaining encyclopedic content as a system of record or providing a log of processes (including business processes) that persist beyond one session.
    
-   Additionally, if your SHACL ontology is online, you can have your LLM establish a context that points to this ontology so that other systems can also read that particular ontology and use it to help communicate what you intended to do. This is pretty critical, actually. One of the major problems the Semantic Web has long faced is that ontology identifiers have not always resolved to a definition file or stream. If, when making a service invocation, you can say: go to GitHub and use this starting SHACL file and anything it connects to, then you don’t have to actually waste tokens trying to set up definitions; your downstream user can even cache frequently used specifications as a temporary master file. You have, in essence, created a contract based upon your definition that they can work with automatically.
    
-   SHACL is remarkably self-documenting: pass a SHACL to an LLM and instruct it to create documentation, and it will produce a high-quality (and typically very accurate) Markdown document, including Mermaid diagrams to illustrate classes and relationships.
    
-   Load a SHACL into an LLM, then point it to a website, image or PDF, and the LLM will generate from that file something that will fit very closely to the offered RDF schema, because it has both structural knowledge about the ontology and semantic knowledge that can be inferred from labels and other annotative metadata, something that can then be dropped into your knowledge graph with little to know friction. Moreover, because SHACL has rules, one of the more onerous parts of that process - connecting a new item to a graph at various connection points- can be performed automatically upon ingestion, and can be validated to either ensure that it conforms to the specification or reported on to indicate the potential problems that the object has.
    
-   You can also use LLMs to help you design your SHACL initially, either from an industry-established specification or based on your particular needs and requirements as a bespoke ontology. This was a months-long effort not that many years ago; you can do it today over the course of a week, with most of that time spent building consensus that the model being developed is adequate.
    
-   SHACL is conditional. One particular use case involved making a description optional for most clients, but for a few specific clients, making this description required was paramount. This is difficult to model in languages such as OWL; it’s trivial to model in SHACL.
    
-   I frequently have the LLM emulate a SHACL 1.2 validation processor and rules engine. This would ordinarily be problematic because the specification is still evolving, although most of the core is stable. By using the SHACL specification, however, it performs advanced operations remarkably well. It’s not a replacement for binary code, but from a design or conversion standpoint, it’s still more advanced than most of what’s currently out there.
    
-   Another useful technique is to pass in the SHACLs for two different ontologies, then have the LLM generate a transformation (in Python, JavaScript, SPARQL Update, or a host of other languages) that applies this based on the broadest possible interpretations of each specification. It’s much easier to build such transformations once, then cross-reference them based upon source and target data types, than it is to write transformations every time you need to pull information from one system to another. This is a huge benefit for data integration efforts.
    
-   Again, the best approach when working with agentic systems is not to have the LLM become the validation layer (not yet, anyway). Instead, when dealing with many use cases in which validation is important, have the LLM write an application based on shapes. This way, you incur the processing costs only once, rather than once per instance.
    

Are there drawbacks? A few.

-   The SHACL layer will be domain-specific; therefore, you will likely need to select which shapes to load, given the problems at hand. It’s not a universal ground.
    
-   You have to develop the SHACL. Fortunately, you can frequently provide a good foundation for that SHACL by evaluating existing sample content with an LLM. You still need to test and validate the schema, but this can be accomplished within a much shorter timeframe (days rather than months).
    
-   Because of limitations in the context window architecture, you can load only so much into that window before you run the risk of cognitive decay. SHACL files themselves are fairly small, but poorly designed taxonomies can get quite large, and at some point, you need to make decisions about how much of those taxonomies should stay native to the knowledge graph (taxonomy design is a topic in its own right).
    
-   The SHACL standard predates the LLM architecture (SHACL - 2017; Transformers - 2018), but because it was outside the mainstream, fewer people are proficient in its use. SHACL has consequently gained a reputation as less mature, which is not warranted (even SHACL 1.2, in development, is largely a formalisation of components that had been developed in related standards).
    
-   You have to think more about architecture and design. I’m not sure this is a drawback. Vibe coding is failing after less than two years because projects were underspecified and because LLMs without constraints tend to veer off into hallucinations. SHACL provides consistency, validation, a blueprint for generation, and self-documentation. It is a specification _of_ your architecture. You spend more time in the design phase but far less time on coding, testing, and maintenance, where most technical debt typically resides.
    

## Conclusion

The examples provided here are meant to suggest a few ways that LLMs and SHACL (structure + taxonomy + rules) can be (and should be) used together, but also to emphasise that you can design systems that combine structural and semantic rigour via shapes with the flexibility and expressiveness of transformers. SHACL tells a knowledge graph how to be queried and what to generate, transformers enhance and present that content.

I’ve touched only peripherally on context graphs here (which are essentially semantic organisational or system logs or traces) but the kind of architecture discussed here figures heavily in using such logs to create dynamic digital twins of these systems, and from there to build testable simulations of those systems given specific input criteria. These will be explored more in a subsequent post.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!zZBj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F399f130b-6e59-4aa9-a140-699451ba9d9a_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!zZBj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F399f130b-6e59-4aa9-a140-699451ba9d9a_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.