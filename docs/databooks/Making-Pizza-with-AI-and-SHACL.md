---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Making-Pizza-with-AI-and-SHACL
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:47.249082+00:00'
  title: Making Pizza With Ai And Shacl
  type: plain-doc
  version: '0.1'
---

# Making Pizza With Ai And Shacl

[

![](https://substackcdn.com/image/fetch/$s_!0LRe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb71cfce-ad8e-4cda-a905-cc2c82628b23_1344x768.png)

](https://substackcdn.com/image/fetch/$s_!0LRe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb71cfce-ad8e-4cda-a905-cc2c82628b23_1344x768.png)

## My LLMs Are Not Databases Rant

For some time, I have made it a point to argue that AI (specifically LLMs) are not databases. Some of the reasons have to do with characteristics that LLMs lack that databases have:

-   **Atomicity**: All statements are made independent of other statements. LLMs are contextual, meaning that the previous statement (set of tokens) influences the current statement.
    
-   **Consistency.** Any operation will move the database from one consistent state to another. There is no consistency with an LLM, because the context changes from one prompt to the next.
    
-   **Isolation.** If multiple operations are performed in a query or update, these are treated as if each operation is distinct (and can consequently be rolled back). LLMs cannot be rolled back; the context in that regard is a crude hack.
    
-   **Durability.** If an update is made to a database, it will remain durable until a future update is made. LLM contexts can maintain very limited durability, but typically only by re-entering the changes made with every prompt.
    

These should be familiar to people who have worked with databases, as they form the foundation for ACID, something critical for most kinds of datastores. The fact that an LLM actually supports _none_ of these means that an LLM should never be used in situations where data integrity becomes critical.

I’ll be honest - I think one of the things that has so pissed me off about all of the Hype and Hopium about LLMs is that there has always been this implicit notion that, if you just give it enough time, the powers that be that control the Chat/Coding space will somehow make an LLM into a database that can run for 1/10,000th of the cost, 1/1,000th of the time, and has more than fifty years of development, exploration, and infrastructure about it - the relational database.

An LLM is not a database - it is a very, very expensive mechanism to do pattern matching and enable conversation, and with a great deal of work it can give a fairly weak semblance of reasoning, but only by having any number of OTHER LLMs racking up token costs acting to double check reasoning on ginormous server systems locked up in special water-cooled facilities with water blessed by the high priests of Hopium.

Have I made my point? Yeah, I’m pissed. I’m writing this particular piece because LLMs are actually pretty useful for doing certain kinds of ontology work, but that’s because the LLMs are being purposed primarily to provide pattern matching and formatting for the REAL data, which is actually contained in an ACID compliant knowledge graph systems[1](https://substack.com/@kurtcagle/p-189271561#footnote-1-172541092) along with relevant schema (here in SHACL).

In this particular piece, I’m going to be working with Anthropic’s Claude Opus 4.1, but these should work with DeepSeek, Google’s Gemini, and yes, (ick) Open AI 4o. The biggest issue that you may face is the need for a large enough context, as SHACL files, while quite condensed, can still make for large files.

## Modelling a Pizza

Pizzas make remarkably good sample pieces because they are just complex enough to not be trivial. Not surprisingly, there are a number of different ontologies for pizza creation. The following one was generated from a MermaidJS diagram.

[

![](https://substackcdn.com/image/fetch/$s_!Rnen!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2bc0b200-1fee-4a20-99bc-3b7a032b94fb_3657x3840.png)

](https://substackcdn.com/image/fetch/$s_!Rnen!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2bc0b200-1fee-4a20-99bc-3b7a032b94fb_3657x3840.png)

I start almost all of my SHACL development from MermaidJS graph (flowchart) files. The reason for this is simple - you can put together exemplars or use cases that allow you to test ideas without getting too deep into code too early. The source file for this is as follows:

```
%% Mermaid file for a sample pizza

flowchart LR
    classDef literal fill:#FFFFFC;
    classDef comment stroke:lightGray,fill:#FFFFE0,font-size:8pt,text-align:left;
    classDef blank fill:black,color:white;
    classDef abstract stroke-dasharray:2 1;
    classDef node stroke:black;
    classDef header font-size:14pt,font-weight:bold,stroke:none,fill:none;
    classDef pizza fill:maroon,color:white
    classDef pizzaSize fill:#FFE0B0
    classDef pizzaShape fill:#EAF4FF
    classDef pizzaStyle fill:#F4EAFF
    classDef pizzaDelivery fill:#EAFFF4
    classDef pizzaConfig fill:lightBlue
    classDef topping fill:orange
    classDef cheeseTopping fill:lightYellow
    classDef meatTopping fill:brown,color:white
    classDef vegetableTopping fill:green,color:white
    classDef sauce fill:red,color:white
    classDef crust fill:#FFF4EA

Pizza1["<b>Pizza</b><br>MyPie1"]:::pizza
PizzaDiv1[PizzaDiv]:::blank
Pizza1 -- has division -->PizzaDiv1
Pizza1 -- has pizza size -->Medium[<b>Pizza Size</b><br>Medium]:::pizzaSize
Pizza1 -- has pizza style -->ThinCrust[<b>Pizza Style</b><br>Thin Crust]:::pizzaStyle
Pizza1 -- has pizza shape -->Round[<b>Pizza Shape</b><br>Round]:::pizzaShape
Pizza1 -- has pizza delivery -->Delivered[<b>Pizza Delivery</b><br>Delivered]:::pizzaDelivery
PizzaDiv1 -- has configuration --> Sicilian[<b>Pizza Config</b><br>The Sicilian]:::pizzaConfig & Custom[<b>Pizza Config</b><br>Custom]:::pizzaConfig
Custom -- has cheese topping -->Parmesan[<b>Cheese Topping</b><br>Parmesan]:::cheeseTopping
Custom -- has meat topping -->Sausage[<b>Meat Topping</b><br>Sausage]:::meatTopping
Sicilian -- has label -->SicilianName[[<b>xsd:string</b><br>Sicilian]]:::literal
Sicilian -- has sauce -->Marinara[<b>Sauce Topping</b><br>Marinara]:::sauce
Sicilian -- has cheese topping -->Mozzarella[<b>Cheese Topping</b><br>Mozzarella]:::cheeseTopping
Sicilian -- has meat topping -->Pepperoni[<b>Meat Topping</b><br>Pepperoni]:::meatTopping
Sicilian -- has vegetable topping -->Mushrooms[<b>Vegetable Topping</b><br>Mushrooms]:::vegetableTopping
Sicilian -- has crust -->WheatCrust[<b>Crust</b><br>Wheat Crust]:::crust
```

I’ll let the model speak for itself, though there is a point to consider with this. I think that Protege is a pretty good tool for organizing an ontology is everything that you’re working with is a class, but _not everything is a hierarchy_.

In general, by starting with exemplars, which are in essence just use cases, you can create any number of different test examples that let you construct objects, then once you have been able to capture these, you can then use tools like LLMs, to help you build the structures that are likely to be most useful to your particular use case.

This may seem a little background for those who learned ontology development by working with Protege or other tools like it, but the reality is that what you are trying to do is just model things, and by starting with those things, you (or perhaps an LLM) can then help you find the underlying COMMON classes and properties.

This little advice came from more than three decades of data modelling, and years of being told that I had to start from a root class and build things out. This is a lot like trying to build a car by creating a generic chassis, generic wheels, generic engine and so forth, then building out all possible variations of these.

Yes you can do all of this, but it is often MUCH easier to start with a description of a few different kinds of cars (or pizzas), then finding points of commonality. You’ll eventually get to the same place, but usually with exemplars you’ll get there so much faster.

In this case, I started with an assumption about a Sicilian pizza (which is usually, though not always, sausage, mushrooms, pepperoni and occasionally black olives in a red sauce on a thin crust wheat pizza shell). I also made a simplifying assumption that a pizza might be broken up into divisions of equal-sized arcs, with one division representing a whole pizza, two divisions representing half pizzas and so forth.

Note here that I made some tentative steps on what I thought relevant classes might be (the items in bold at the top of each box). Some of this can be inferred, but the more that you can provide structure at this stage, the less you’ll have to rework down the road by a wide margin.

## Pizza, AI, Turtle, SHACL

Once you have worked out an exemplar, the next stage comes in translating it into RDF. This is where I save the mermaidJS file as pizza.mmd.txt, then go to my LLM in question. For testing purposes, you can use chat directly here to upload the pizza.mmd.txt file as an attachment with the following prompt:

```
> Given the attached file (pizza.mmd.txt) create a Turtle file, assuming the namespace pz = <https://example.com/ns/pizza#>.
```

After a few seconds, Claude comes back with:

```
# MyPizza1.ttl
@prefix pz: <https://example.com/ns/pizza#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# Pizza instance
pz:MyPie1 rdf:type pz:Pizza ;
    pz:hasDivision pz:PizzaDiv ;
    pz:hasPizzaSize pz:Medium ;
    pz:hasPizzaStyle pz:ThinCrust ;
    pz:hasPizzaShape pz:Round ;
    pz:hasPizzaDelivery pz:Delivered .

# Pizza division
pz:PizzaDiv rdf:type pz:PizzaDiv ;
    pz:hasConfiguration pz:TheSicilian ,
                        pz:Custom .

# Pizza configurations
pz:TheSicilian rdf:type pz:PizzaConfig ;
    pz:hasLabel "Sicilian"^^xsd:string ;
    pz:hasSauce pz:Marinara ;
    pz:hasCheeseTopping pz:Mozzarella ;
    pz:hasMeatTopping pz:Pepperoni ;
    pz:hasVegetableTopping pz:Mushrooms ;
    pz:hasCrust pz:WheatCrust .

pz:Custom rdf:type pz:PizzaConfig ;
    pz:hasCheeseTopping pz:Parmesan ;
    pz:hasMeatTopping pz:Sausage .

# Pizza properties
pz:Medium rdf:type pz:PizzaSize .
pz:ThinCrust rdf:type pz:PizzaStyle .
pz:Round rdf:type pz:PizzaShape .
pz:Delivered rdf:type pz:PizzaDelivery .

# Toppings
pz:Marinara rdf:type pz:SauceTopping .
pz:Mozzarella rdf:type pz:CheeseTopping .
pz:Parmesan rdf:type pz:CheeseTopping .
pz:Pepperoni rdf:type pz:MeatTopping .
pz:Sausage rdf:type pz:MeatTopping .
pz:Mushrooms rdf:type pz:VegetableTopping .

# Crust
pz:WheatCrust rdf:type pz:Crust .
```

With this as a start, issue a couple more prompts to clarify:

```
> Add in labels for each unresolved IRI, as well as explanations for what these are.
```

This generates the following Turtle along with some base analysis work (which I won’t reproduce here)

```
# MyPizza2.ttl
@prefix pz: <https://example.com/ns/pizza#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# Pizza instance
pz:MyPie1 rdf:type pz:Pizza ;
    rdfs:label "My Pie 1"@en ;
    rdfs:comment "A specific pizza instance with thin crust, medium size, and mixed toppings"@en ;
    pz:hasDivision pz:PizzaDiv ;
    pz:hasPizzaSize pz:Medium ;
    pz:hasPizzaStyle pz:ThinCrust ;
    pz:hasPizzaShape pz:Round ;
    pz:hasPizzaDelivery pz:Delivered .

# Pizza division
pz:PizzaDiv rdf:type pz:PizzaDiv ;
    rdfs:label "Pizza Division"@en ;
    rdfs:comment "A logical division of a pizza that can contain multiple configuration sections"@en ;
    pz:hasConfiguration pz:TheSicilian ,
                        pz:Custom .

# Pizza configurations
pz:TheSicilian rdf:type pz:PizzaConfig ;
    rdfs:label "The Sicilian"@en ;
    rdfs:comment "A traditional Sicilian-style pizza configuration with marinara sauce, mozzarella, pepperoni, mushrooms, and wheat crust"@en ;
    pz:hasLabel "Sicilian"^^xsd:string ;
    pz:hasSauce pz:Marinara ;
    pz:hasCheeseTopping pz:Mozzarella ;
    pz:hasMeatTopping pz:Pepperoni ;
    pz:hasVegetableTopping pz:Mushrooms ;
    pz:hasCrust pz:WheatCrust .

pz:Custom rdf:type pz:PizzaConfig ;
    rdfs:label "Custom Configuration"@en ;
    rdfs:comment "A custom pizza configuration with parmesan cheese and sausage toppings"@en ;
    pz:hasCheeseTopping pz:Parmesan ;
    pz:hasMeatTopping pz:Sausage .

# Pizza properties
pz:Medium rdf:type pz:PizzaSize ;
    rdfs:label "Medium"@en ;
    rdfs:comment "A medium-sized pizza, typically 12 inches in diameter"@en .

pz:ThinCrust rdf:type pz:PizzaStyle ;
    rdfs:label "Thin Crust"@en ;
    rdfs:comment "A pizza style characterized by a thin, crispy crust base"@en .

pz:Round rdf:type pz:PizzaShape ;
    rdfs:label "Round"@en ;
    rdfs:comment "Traditional circular pizza shape"@en .

pz:Delivered rdf:type pz:PizzaDelivery ;
    rdfs:label "Delivered"@en ;
    rdfs:comment "Pizza delivery method where the pizza is brought to the customer"@en .

# Toppings
pz:Marinara rdf:type pz:SauceTopping ;
    rdfs:label "Marinara"@en ;
    rdfs:comment "Classic Italian tomato-based pizza sauce with herbs and garlic"@en .

pz:Mozzarella rdf:type pz:CheeseTopping ;
    rdfs:label "Mozzarella"@en ;
    rdfs:comment "Traditional Italian cheese, commonly used on pizza, known for its mild flavor and excellent melting properties"@en .

pz:Parmesan rdf:type pz:CheeseTopping ;
    rdfs:label "Parmesan"@en ;
    rdfs:comment "Hard, aged Italian cheese with a sharp, nutty flavor, often grated over pizza"@en .

pz:Pepperoni rdf:type pz:MeatTopping ;
    rdfs:label "Pepperoni"@en ;
    rdfs:comment "Spicy American salami made from cured pork and beef, a popular pizza topping"@en .

pz:Sausage rdf:type pz:MeatTopping ;
    rdfs:label "Sausage"@en ;
    rdfs:comment "Seasoned ground meat (usually pork or beef) formed into small pieces for pizza topping"@en .

pz:Mushrooms rdf:type pz:VegetableTopping ;
    rdfs:label "Mushrooms"@en ;
    rdfs:comment "Sliced fungi, typically button or cremini mushrooms, used as a savory pizza topping"@en .

# Crust
pz:WheatCrust rdf:type pz:Crust ;
    rdfs:label "Wheat Crust"@en ;
    rdfs:comment "Pizza crust made from wheat flour, providing the base structure of the pizza"@en .
```

At this point it’s worth spending a couple of minutes reviewing the Turtle code to make sure you’re capturing what you’re expecting. One more prompt may be worth adding:

```
 > Extend this with subclass relationships indicating that all toppings are subclasses of the pz:Topping class.
```

This produces the final version:

```
# MyPizza3.ttl

@prefix pz: <https://example.com/ns/pizza#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# Pizza instance
pz:MyPie1 rdf:type pz:Pizza ;
    rdfs:label "My Pie 1"@en ;
    rdfs:comment "A specific pizza instance with thin crust, medium size, and mixed toppings"@en ;
    pz:hasDivision pz:PizzaDiv ;
    pz:hasPizzaSize pz:Medium ;
    pz:hasPizzaStyle pz:ThinCrust ;
    pz:hasPizzaShape pz:Round ;
    pz:hasPizzaDelivery pz:Delivered .

# Pizza division
pz:PizzaDiv rdf:type pz:PizzaDiv ;
    rdfs:label "Pizza Division"@en ;
    rdfs:comment "A logical division of a pizza that can contain multiple configuration sections"@en ;
    pz:hasConfiguration pz:TheSicilian ,
                        pz:Custom .

# Pizza configurations
pz:TheSicilian rdf:type pz:PizzaConfig ;
    rdfs:label "The Sicilian"@en ;
    rdfs:comment "A traditional Sicilian-style pizza configuration with marinara sauce, mozzarella, pepperoni, mushrooms, and wheat crust"@en ;
    pz:hasLabel "Sicilian"^^xsd:string ;
    pz:hasSauce pz:Marinara ;
    pz:hasCheeseTopping pz:Mozzarella ;
    pz:hasMeatTopping pz:Pepperoni ;
    pz:hasVegetableTopping pz:Mushrooms ;
    pz:hasCrust pz:WheatCrust .

pz:Custom rdf:type pz:PizzaConfig ;
    rdfs:label "Custom Configuration"@en ;
    rdfs:comment "A custom pizza configuration with parmesan cheese and sausage toppings"@en ;
    pz:hasCheeseTopping pz:Parmesan ;
    pz:hasMeatTopping pz:Sausage .

# Pizza properties
pz:Medium rdf:type pz:PizzaSize ;
    rdfs:label "Medium"@en ;
    rdfs:comment "A medium-sized pizza, typically 12 inches in diameter"@en .

pz:ThinCrust rdf:type pz:PizzaStyle ;
    rdfs:label "Thin Crust"@en ;
    rdfs:comment "A pizza style characterized by a thin, crispy crust base"@en .

pz:Round rdf:type pz:PizzaShape ;
    rdfs:label "Round"@en ;
    rdfs:comment "Traditional circular pizza shape"@en .

pz:Delivered rdf:type pz:PizzaDelivery ;
    rdfs:label "Delivered"@en ;
    rdfs:comment "Pizza delivery method where the pizza is brought to the customer"@en .

# Topping class hierarchy
pz:Topping rdfs:label "Topping"@en ;
    rdfs:comment "General class for all pizza toppings - ingredients added to the pizza base"@en .

pz:SauceTopping rdfs:subClassOf pz:Topping ;
    rdfs:label "Sauce Topping"@en ;
    rdfs:comment "Liquid or semi-liquid toppings that provide flavor and moisture to pizza"@en .

pz:CheeseTopping rdfs:subClassOf pz:Topping ;
    rdfs:label "Cheese Topping"@en ;
    rdfs:comment "Dairy-based toppings that provide richness and binding properties to pizza"@en .

pz:MeatTopping rdfs:subClassOf pz:Topping ;
    rdfs:label "Meat Topping"@en ;
    rdfs:comment "Protein-based toppings derived from animal sources"@en .

pz:VegetableTopping rdfs:subClassOf pz:Topping ;
    rdfs:label "Vegetable Topping"@en ;
    rdfs:comment "Plant-based toppings that add flavor, texture, and nutritional value"@en .

# Topping instances
pz:Marinara rdf:type pz:SauceTopping ;
    rdfs:label "Marinara"@en ;
    rdfs:comment "Classic Italian tomato-based pizza sauce with herbs and garlic"@en .

pz:Mozzarella rdf:type pz:CheeseTopping ;
    rdfs:label "Mozzarella"@en ;
    rdfs:comment "Traditional Italian cheese, commonly used on pizza, known for its mild flavor and excellent melting properties"@en .

pz:Parmesan rdf:type pz:CheeseTopping ;
    rdfs:label "Parmesan"@en ;
    rdfs:comment "Hard, aged Italian cheese with a sharp, nutty flavor, often grated over pizza"@en .

pz:Pepperoni rdf:type pz:MeatTopping ;
    rdfs:label "Pepperoni"@en ;
    rdfs:comment "Spicy American salami made from cured pork and beef, a popular pizza topping"@en .

pz:Sausage rdf:type pz:MeatTopping ;
    rdfs:label "Sausage"@en ;
    rdfs:comment "Seasoned ground meat (usually pork or beef) formed into small pieces for pizza topping"@en .

pz:Mushrooms rdf:type pz:VegetableTopping ;
    rdfs:label "Mushrooms"@en ;
    rdfs:comment "Sliced fungi, typically button or cremini mushrooms, used as a savory pizza topping"@en .

# Crust
pz:WheatCrust rdf:type pz:Crust ;
    rdfs:label "Wheat Crust"@en ;
    rdfs:comment "Pizza crust made from wheat flour, providing the base structure of the pizza"@en .
```

The next stage is something of a leap of faith, but from here we can generate the corresponding SHACL file:

```
Based on the latest Turtle pizza listing, create a documented SHACL file. 

Using the existing ingredients as a pattern, include other common meat, cheese, vegetable and sauce toppings as well as different types of crusts, sizes, delivery methods, and shapes. 

Create a programmatic sh:name triple for generating graphQL type variable names. 

Incorporate RDFS subClassOf and subPropertyOf relationships but not rdfs:range and rdfs:domain. 

Include cardinality relationships where they can be inferred.

Include sh:nodeKind relationships for each property shape.

Where appropriate, incorporate specific sh:message and sh:severity messages
```

This takes a little while to generate, but eventually you end up with the following SHACL file (saved as pizza.shacl.ttl.txt)

```
@prefix pz: <https://example.com/ns/pizza#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# =============================================================================
# SHACL SHAPES FOR PIZZA ONTOLOGY
# =============================================================================
# This SHACL file defines validation constraints for a pizza ordering system.
# It includes shapes for pizzas, toppings, configurations, and related entities.
# Each shape includes sh:name properties for GraphQL type generation, specific
# validation messages, and comprehensive node kind specifications.
# =============================================================================

# -----------------------------------------------------------------------------
# MAIN PIZZA SHAPE
# -----------------------------------------------------------------------------

pz:PizzaShape a sh:NodeShape ;
    sh:name "Pizza" ;
    sh:targetClass pz:Pizza ;
    rdfs:label "Pizza Shape"@en ;
    rdfs:comment "Validation shape for pizza instances, ensuring all required properties are present"@en ;
    sh:message "Pizza validation failed - check required properties"@en ;
    sh:severity sh:Violation ;
    sh:property [
        sh:path pz:hasPizzaSize ;
        sh:name "pizzaSize" ;
        sh:class pz:PizzaSize ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "Every pizza must have exactly one size specified"@en ;
        sh:severity sh:Violation ;
        sh:description "Every pizza must have exactly one size"@en ;
    ] ;
    sh:property [
        sh:path pz:hasPizzaStyle ;
        sh:name "pizzaStyle" ;
        sh:class pz:PizzaStyle ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "Every pizza must have exactly one style specified"@en ;
        sh:severity sh:Violation ;
        sh:description "Every pizza must have exactly one style"@en ;
    ] ;
    sh:property [
        sh:path pz:hasPizzaShape ;
        sh:name "pizzaShape" ;
        sh:class pz:PizzaShape ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "Every pizza must have exactly one shape specified"@en ;
        sh:severity sh:Violation ;
        sh:description "Every pizza must have exactly one shape"@en ;
    ] ;
    sh:property [
        sh:path pz:hasPizzaDelivery ;
        sh:name "deliveryMethod" ;
        sh:class pz:PizzaDelivery ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "Every pizza must have exactly one delivery method specified"@en ;
        sh:severity sh:Violation ;
        sh:description "Every pizza must have exactly one delivery method"@en ;
    ] ;
    sh:property [
        sh:path pz:hasDivision ;
        sh:name "divisions" ;
        sh:class pz:PizzaDiv ;
        sh:nodeKind sh:IRI ;
        sh:minCount 0 ;
        sh:message "Invalid pizza division reference"@en ;
        sh:severity sh:Warning ;
        sh:description "Pizza may have zero or more divisions"@en ;
    ] .

# -----------------------------------------------------------------------------
# PIZZA DIVISION SHAPE
# -----------------------------------------------------------------------------

pz:PizzaDivShape a sh:NodeShape ;
    sh:name "PizzaDivision" ;
    sh:targetClass pz:PizzaDiv ;
    rdfs:label "Pizza Division Shape"@en ;
    rdfs:comment "Validation shape for pizza divisions, which contain configurations"@en ;
    sh:message "Pizza division must have at least one configuration"@en ;
    sh:severity sh:Violation ;
    sh:property [
        sh:path pz:hasConfiguration ;
        sh:name "configurations" ;
        sh:class pz:PizzaConfig ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:message "Pizza division must contain at least one valid configuration"@en ;
        sh:severity sh:Violation ;
        sh:description "Pizza division must have at least one configuration"@en ;
    ] .

# -----------------------------------------------------------------------------
# PIZZA CONFIGURATION SHAPE
# -----------------------------------------------------------------------------

pz:PizzaConfigShape a sh:NodeShape ;
    sh:name "PizzaConfiguration" ;
    sh:targetClass pz:PizzaConfig ;
    rdfs:label "Pizza Configuration Shape"@en ;
    rdfs:comment "Validation shape for pizza configurations, defining topping and crust constraints"@en ;
    sh:message "Invalid pizza configuration - check toppings and crust"@en ;
    sh:severity sh:Warning ;
    sh:property [
        sh:path pz:hasLabel ;
        sh:name "configLabel" ;
        sh:datatype xsd:string ;
        sh:nodeKind sh:Literal ;
        sh:maxCount 1 ;
        sh:message "Configuration can have at most one label"@en ;
        sh:severity sh:Warning ;
        sh:description "Optional configuration label"@en ;
    ] ;
    sh:property [
        sh:path pz:hasCrust ;
        sh:name "crust" ;
        sh:class pz:Crust ;
        sh:nodeKind sh:IRI ;
        sh:minCount 0 ;
        sh:maxCount 1 ;
        sh:message "Configuration can have at most one crust type"@en ;
        sh:severity sh:Warning ;
        sh:description "Configuration may have at most one crust type"@en ;
    ] ;
    sh:property [
        sh:path pz:hasSauce ;
        sh:name "sauceToppings" ;
        sh:class pz:SauceTopping ;
        sh:nodeKind sh:IRI ;
        sh:minCount 0 ;
        sh:maxCount 2 ;
        sh:message "Too many sauces - maximum of 2 sauce toppings recommended"@en ;
        sh:severity sh:Warning ;
        sh:description "Configuration may have zero to two sauce toppings"@en ;
    ] ;
    sh:property [
        sh:path pz:hasCheeseTopping ;
        sh:name "cheeseToppings" ;
        sh:class pz:CheeseTopping ;
        sh:nodeKind sh:IRI ;
        sh:minCount 0 ;
        sh:message "Invalid cheese topping reference"@en ;
        sh:severity sh:Warning ;
        sh:description "Configuration may have zero or more cheese toppings"@en ;
    ] ;
    sh:property [
        sh:path pz:hasMeatTopping ;
        sh:name "meatToppings" ;
        sh:class pz:MeatTopping ;
        sh:nodeKind sh:IRI ;
        sh:minCount 0 ;
        sh:message "Invalid meat topping reference"@en ;
        sh:severity sh:Warning ;
        sh:description "Configuration may have zero or more meat toppings"@en ;
    ] ;
    sh:property [
        sh:path pz:hasVegetableTopping ;
        sh:name "vegetableToppings" ;
        sh:class pz:VegetableTopping ;
        sh:nodeKind sh:IRI ;
        sh:minCount 0 ;
        sh:message "Invalid vegetable topping reference"@en ;
        sh:severity sh:Warning ;
        sh:description "Configuration may have zero or more vegetable toppings"@en ;
    ] .

# -----------------------------------------------------------------------------
# TOPPING HIERARCHY SHAPES
# -----------------------------------------------------------------------------

pz:ToppingShape a sh:NodeShape ;
    sh:name "Topping" ;
    sh:targetClass pz:Topping ;
    rdfs:label "Base Topping Shape"@en ;
    rdfs:comment "Base validation shape for all pizza toppings"@en ;
    sh:message "Topping must have proper label and description"@en ;
    sh:severity sh:Violation ;
    sh:property [
        sh:path rdfs:label ;
        sh:name "label" ;
        sh:datatype rdf:langString ;
        sh:nodeKind sh:Literal ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "Every topping must have exactly one label"@en ;
        sh:severity sh:Violation ;
        sh:description "Every topping must have exactly one label"@en ;
    ] ;
    sh:property [
        sh:path rdfs:comment ;
        sh:name "description" ;
        sh:datatype rdf:langString ;
        sh:nodeKind sh:Literal ;
        sh:minCount 0 ;
        sh:maxCount 1 ;
        sh:message "Topping can have at most one description"@en ;
        sh:severity sh:Info ;
        sh:description "Optional description for the topping - at most one"@en ;
    ] .

# Sauce Topping Shape
pz:SauceToppingShape a sh:NodeShape ;
    sh:name "SauceTopping" ;
    sh:targetClass pz:SauceTopping ;
    rdfs:label "Sauce Topping Shape"@en ;
    rdfs:comment "Validation shape for sauce toppings"@en ;
    sh:message "Invalid sauce topping properties"@en ;
    sh:severity sh:Warning .

# Cheese Topping Shape
pz:CheeseToppingShape a sh:NodeShape ;
    sh:name "CheeseTopping" ;
    sh:targetClass pz:CheeseTopping ;
    rdfs:label "Cheese Topping Shape"@en ;
    rdfs:comment "Validation shape for cheese toppings"@en ;
    sh:message "Invalid cheese topping properties"@en ;
    sh:severity sh:Warning .

# Meat Topping Shape
pz:MeatToppingShape a sh:NodeShape ;
    sh:name "MeatTopping" ;
    sh:targetClass pz:MeatTopping ;
    rdfs:label "Meat Topping Shape"@en ;
    rdfs:comment "Validation shape for meat toppings"@en ;
    sh:message "Invalid meat topping properties"@en ;
    sh:severity sh:Warning .

# Vegetable Topping Shape
pz:VegetableToppingShape a sh:NodeShape ;
    sh:name "VegetableTopping" ;
    sh:targetClass pz:VegetableTopping ;
    rdfs:label "Vegetable Topping Shape"@en ;
    rdfs:comment "Validation shape for vegetable toppings"@en ;
    sh:message "Invalid vegetable topping properties"@en ;
    sh:severity sh:Warning .

# -----------------------------------------------------------------------------
# PIZZA ATTRIBUTE SHAPES
# -----------------------------------------------------------------------------

# Pizza Size Shape
pz:PizzaSizeShape a sh:NodeShape ;
    sh:name "PizzaSize" ;
    sh:targetClass pz:PizzaSize ;
    rdfs:label "Pizza Size Shape"@en ;
    rdfs:comment "Validation shape for pizza sizes"@en ;
    sh:message "Invalid pizza size - must be one of: Personal, Small, Medium, Large, Extra Large, Family"@en ;
    sh:severity sh:Violation ;
    sh:in ( pz:Personal pz:Small pz:Medium pz:Large pz:ExtraLarge pz:Family ) .

# Pizza Style Shape
pz:PizzaStyleShape a sh:NodeShape ;
    sh:name "PizzaStyle" ;
    sh:targetClass pz:PizzaStyle ;
    rdfs:label "Pizza Style Shape"@en ;
    rdfs:comment "Validation shape for pizza styles"@en ;
    sh:message "Invalid pizza style - must be one of: Thin Crust, Thick Crust, Stuffed Crust, Deep Dish, Flatbread, Neapolitan, Pan"@en ;
    sh:severity sh:Violation ;
    sh:in ( pz:ThinCrust pz:ThickCrust pz:StuffedCrust pz:DeepDish pz:Flatbread pz:Neapolitan pz:Pan ) .

# Pizza Physical Shape
pz:PizzaPhysicalShapeShape a sh:NodeShape ;
    sh:name "PizzaPhysicalShape" ;
    sh:targetClass pz:PizzaShape ;
    rdfs:label "Pizza Physical Shape Shape"@en ;
    rdfs:comment "Validation shape for pizza physical shapes"@en ;
    sh:message "Invalid pizza shape - must be one of: Round, Square, Rectangular"@en ;
    sh:severity sh:Violation ;
    sh:in ( pz:Round pz:Square pz:Rectangular ) .

# Pizza Delivery Shape
pz:PizzaDeliveryShape a sh:NodeShape ;
    sh:name "PizzaDelivery" ;
    sh:targetClass pz:PizzaDelivery ;
    rdfs:label "Pizza Delivery Shape"@en ;
    rdfs:comment "Validation shape for pizza delivery methods"@en ;
    sh:message "Invalid delivery method - must be one of: Delivered, Pickup, Dine In, Takeaway"@en ;
    sh:severity sh:Violation ;
    sh:in ( pz:Delivered pz:Pickup pz:DineIn pz:Takeaway ) .

# Crust Shape
pz:CrustShape a sh:NodeShape ;
    sh:name "Crust" ;
    sh:targetClass pz:Crust ;
    rdfs:label "Crust Shape"@en ;
    rdfs:comment "Validation shape for pizza crusts"@en ;
    sh:message "Invalid crust type - must be one of the approved crust varieties"@en ;
    sh:severity sh:Warning ;
    sh:in ( pz:WheatCrust pz:GlutenFreeCrust pz:CauliflowerCrust pz:SourdoughCrust pz:WholeWheatCrust ) .

# =============================================================================
# RDFS CLASS AND PROPERTY DEFINITIONS
# =============================================================================

# -----------------------------------------------------------------------------
# CLASS HIERARCHY WITH SUBCLASS RELATIONSHIPS
# -----------------------------------------------------------------------------

# Base classes
pz:Pizza rdf:type rdfs:Class ;
    rdfs:label "Pizza"@en ;
    rdfs:comment "A pizza - the main entity in our pizza ontology. Each pizza has exactly one size, style, shape, and delivery method, with zero or more divisions"@en .

pz:PizzaDiv rdf:type rdfs:Class ;
    rdfs:label "Pizza Division"@en ;
    rdfs:comment "A logical division of a pizza that can contain multiple configurations. Each division belongs to exactly one pizza and has one or more configurations"@en .

pz:PizzaConfig rdf:type rdfs:Class ;
    rdfs:label "Pizza Configuration"@en ;
    rdfs:comment "A specific configuration of toppings and crust for a pizza or pizza section. Each configuration belongs to exactly one division and may have various toppings and at most one crust"@en .

# Topping hierarchy with subclass relationships
pz:Topping rdf:type rdfs:Class ;
    rdfs:label "Topping"@en ;
    rdfs:comment "General class for all pizza toppings - ingredients added to the pizza base. Each topping instance has exactly one label and at most one description"@en .

pz:SauceTopping rdfs:subClassOf pz:Topping ;
    rdf:type rdfs:Class ;
    rdfs:label "Sauce Topping"@en ;
    rdfs:comment "Liquid or semi-liquid toppings that provide flavor and moisture to pizza. Typically 0-2 sauce toppings per configuration"@en .

pz:CheeseTopping rdfs:subClassOf pz:Topping ;
    rdf:type rdfs:Class ;
    rdfs:label "Cheese Topping"@en ;
    rdfs:comment "Dairy-based toppings that provide richness and binding properties to pizza. Multiple cheese toppings can be applied to one configuration"@en .

pz:MeatTopping rdfs:subClassOf pz:Topping ;
    rdf:type rdfs:Class ;
    rdfs:label "Meat Topping"@en ;
    rdfs:comment "Protein-based toppings derived from animal sources. Multiple meat toppings can be applied to one configuration"@en .

pz:VegetableTopping rdfs:subClassOf pz:Topping ;
    rdf:type rdfs:Class ;
    rdfs:label "Vegetable Topping"@en ;
    rdfs:comment "Plant-based toppings that add flavor, texture, and nutritional value. Multiple vegetable toppings can be applied to one configuration"@en .

# Specialized cheese subcategories
pz:SoftCheese rdfs:subClassOf pz:CheeseTopping ;
    rdf:type rdfs:Class ;
    rdfs:label "Soft Cheese"@en ;
    rdfs:comment "Soft, creamy cheeses that spread easily"@en .

pz:HardCheese rdfs:subClassOf pz:CheeseTopping ;
    rdf:type rdfs:Class ;
    rdfs:label "Hard Cheese"@en ;
    rdfs:comment "Aged, firm cheeses that are often grated or shaved"@en .

# Specialized meat subcategories  
pz:ProcessedMeat rdfs:subClassOf pz:MeatTopping ;
    rdf:type rdfs:Class ;
    rdfs:label "Processed Meat"@en ;
    rdfs:comment "Cured, smoked, or otherwise processed meat products"@en .

pz:FreshMeat rdfs:subClassOf pz:MeatTopping ;
    rdf:type rdfs:Class ;
    rdfs:label "Fresh Meat"@en ;
    rdfs:comment "Fresh, cooked meat that has not been cured or processed"@en .

# Pizza attribute classes with cardinality constraints
pz:PizzaSize rdf:type rdfs:Class ;
    rdfs:label "Pizza Size"@en ;
    rdfs:comment "The size category of a pizza - each pizza has exactly one size"@en .

pz:PizzaStyle rdf:type rdfs:Class ;
    rdfs:label "Pizza Style"@en ;
    rdfs:comment "The preparation style or crust type of a pizza - each pizza has exactly one style"@en .

pz:PizzaShape rdf:type rdfs:Class ;
    rdfs:label "Pizza Shape"@en ;
    rdfs:comment "The physical shape of a pizza - each pizza has exactly one shape"@en .

pz:PizzaDelivery rdf:type rdfs:Class ;
    rdfs:label "Pizza Delivery"@en ;
    rdfs:comment "The method by which a pizza is delivered to the customer - each pizza has exactly one delivery method"@en .

pz:Crust rdf:type rdfs:Class ;
    rdfs:label "Crust"@en ;
    rdfs:comment "The base layer of a pizza made from dough - each configuration has at most one crust type"@en .

# -----------------------------------------------------------------------------
# PROPERTY HIERARCHY WITH SUBPROPERTY RELATIONSHIPS
# -----------------------------------------------------------------------------

# Base property for all topping relationships
pz:hasTopping rdf:type rdf:Property ;
    rdfs:label "has topping"@en ;
    rdfs:comment "Base property for relating configurations to any type of topping"@en .

# Topping subproperties
pz:hasSauce rdfs:subPropertyOf pz:hasTopping ;
    rdf:type rdf:Property ;
    rdfs:label "has sauce"@en ;
    rdfs:comment "Relates a configuration to its sauce toppings - zero or more sauces per configuration (typically 0-2)"@en .

pz:hasCheeseTopping rdfs:subPropertyOf pz:hasTopping ;
    rdf:type rdf:Property ;
    rdfs:label "has cheese topping"@en ;
    rdfs:comment "Relates a configuration to its cheese toppings - zero or more cheeses per configuration"@en .

pz:hasMeatTopping rdfs:subPropertyOf pz:hasTopping ;
    rdf:type rdf:Property ;
    rdfs:label "has meat topping"@en ;
    rdfs:comment "Relates a configuration to its meat toppings - zero or more meats per configuration"@en .

pz:hasVegetableTopping rdfs:subPropertyOf pz:hasTopping ;
    rdf:type rdf:Property ;
    rdfs:label "has vegetable topping"@en ;
    rdfs:comment "Relates a configuration to its vegetable toppings - zero or more vegetables per configuration"@en .

# Pizza core properties
pz:hasPizzaSize rdf:type rdf:Property ;
    rdfs:label "has pizza size"@en ;
    rdfs:comment "Relates a pizza to its size - exactly one size per pizza"@en .

pz:hasPizzaStyle rdf:type rdf:Property ;
    rdfs:label "has pizza style"@en ;
    rdfs:comment "Relates a pizza to its preparation style - exactly one style per pizza"@en .

pz:hasPizzaShape rdf:type rdf:Property ;
    rdfs:label "has pizza shape"@en ;
    rdfs:comment "Relates a pizza to its physical shape - exactly one shape per pizza"@en .

pz:hasPizzaDelivery rdf:type rdf:Property ;
    rdfs:label "has pizza delivery"@en ;
    rdfs:comment "Relates a pizza to its delivery method - exactly one delivery method per pizza"@en .

pz:hasDivision rdf:type rdf:Property ;
    rdfs:label "has division"@en ;
    rdfs:comment "Relates a pizza to its logical divisions - zero or more divisions per pizza"@en .

pz:hasConfiguration rdf:type rdf:Property ;
    rdfs:label "has configuration"@en ;
    rdfs:comment "Relates a pizza division to its topping configurations - at least one configuration per division"@en .

# Configuration properties
pz:hasLabel rdf:type rdf:Property ;
    rdfs:label "has label"@en ;
    rdfs:comment "Assigns a textual label to a configuration - at most one label per configuration"@en .

pz:hasCrust rdf:type rdf:Property ;
    rdfs:label "has crust"@en ;
    rdfs:comment "Relates a configuration to its crust type - at most one crust per configuration"@en .

# =============================================================================
# INDIVIDUAL INSTANCES
# =============================================================================

# -----------------------------------------------------------------------------
# PIZZA SIZES
# -----------------------------------------------------------------------------

pz:Personal rdf:type pz:PizzaSize ;
    rdfs:label "Personal"@en ;
    rdfs:comment "Individual-sized pizza, typically 6-8 inches in diameter"@en .

pz:Small rdf:type pz:PizzaSize ;
    rdfs:label "Small"@en ;
    rdfs:comment "Small pizza, typically 10 inches in diameter"@en .

pz:Medium rdf:type pz:PizzaSize ;
    rdfs:label "Medium"@en ;
    rdfs:comment "Medium-sized pizza, typically 12 inches in diameter"@en .

pz:Large rdf:type pz:PizzaSize ;
    rdfs:label "Large"@en ;
    rdfs:comment "Large pizza, typically 14 inches in diameter"@en .

pz:ExtraLarge rdf:type pz:PizzaSize ;
    rdfs:label "Extra Large"@en ;
    rdfs:comment "Extra large pizza, typically 16-18 inches in diameter"@en .

pz:Family rdf:type pz:PizzaSize ;
    rdfs:label "Family"@en ;
    rdfs:comment "Family-sized pizza, typically 20+ inches in diameter"@en .

# -----------------------------------------------------------------------------
# PIZZA STYLES
# -----------------------------------------------------------------------------

pz:ThinCrust rdf:type pz:PizzaStyle ;
    rdfs:label "Thin Crust"@en ;
    rdfs:comment "Pizza style characterized by a thin, crispy crust base"@en .

pz:ThickCrust rdf:type pz:PizzaStyle ;
    rdfs:label "Thick Crust"@en ;
    rdfs:comment "Pizza style with a thick, chewy crust base"@en .

pz:StuffedCrust rdf:type pz:PizzaStyle ;
    rdfs:label "Stuffed Crust"@en ;
    rdfs:comment "Pizza style with cheese or other fillings baked into the crust edge"@en .

pz:DeepDish rdf:type pz:PizzaStyle ;
    rdfs:label "Deep Dish"@en ;
    rdfs:comment "Chicago-style pizza with a thick crust forming a deep pan"@en .

pz:Flatbread rdf:type pz:PizzaStyle ;
    rdfs:label "Flatbread"@en ;
    rdfs:comment "Very thin, flat crust style pizza"@en .

pz:Neapolitan rdf:type pz:PizzaStyle ;
    rdfs:label "Neapolitan"@en ;
    rdfs:comment "Traditional Italian thin-crust pizza style"@en .

pz:Pan rdf:type pz:PizzaStyle ;
    rdfs:label "Pan"@en ;
    rdfs:comment "Thick crust pizza baked in a deep pan with crispy bottom"@en .

# -----------------------------------------------------------------------------
# PIZZA SHAPES
# -----------------------------------------------------------------------------

pz:Round rdf:type pz:PizzaShape ;
    rdfs:label "Round"@en ;
    rdfs:comment "Traditional circular pizza shape"@en .

pz:Square rdf:type pz:PizzaShape ;
    rdfs:label "Square"@en ;
    rdfs:comment "Square-shaped pizza, often associated with Sicilian style"@en .

pz:Rectangular rdf:type pz:PizzaShape ;
    rdfs:label "Rectangular"@en ;
    rdfs:comment "Rectangular pizza shape, common for party-sized pizzas"@en .

# -----------------------------------------------------------------------------
# DELIVERY METHODS
# -----------------------------------------------------------------------------

pz:Delivered rdf:type pz:PizzaDelivery ;
    rdfs:label "Delivered"@en ;
    rdfs:comment "Pizza delivery method where the pizza is brought to the customer"@en .

pz:Pickup rdf:type pz:PizzaDelivery ;
    rdfs:label "Pickup"@en ;
    rdfs:comment "Customer collects the pizza from the restaurant"@en .

pz:DineIn rdf:type pz:PizzaDelivery ;
    rdfs:label "Dine In"@en ;
    rdfs:comment "Pizza is consumed at the restaurant"@en .

pz:Takeaway rdf:type pz:PizzaDelivery ;
    rdfs:label "Takeaway"@en ;
    rdfs:comment "Pizza is prepared for customer to take away"@en .

# -----------------------------------------------------------------------------
# CRUST TYPES
# -----------------------------------------------------------------------------

pz:WheatCrust rdf:type pz:Crust ;
    rdfs:label "Wheat Crust"@en ;
    rdfs:comment "Traditional pizza crust made from wheat flour"@en .

pz:GlutenFreeCrust rdf:type pz:Crust ;
    rdfs:label "Gluten Free Crust"@en ;
    rdfs:comment "Pizza crust made without gluten-containing ingredients"@en .

pz:CauliflowerCrust rdf:type pz:Crust ;
    rdfs:label "Cauliflower Crust"@en ;
    rdfs:comment "Low-carb pizza crust made primarily from cauliflower"@en .

pz:SourdoughCrust rdf:type pz:Crust ;
    rdfs:label "Sourdough Crust"@en ;
    rdfs:comment "Pizza crust made with sourdough starter for tangy flavor"@en .

pz:WholeWheatCrust rdf:type pz:Crust ;
    rdfs:label "Whole Wheat Crust"@en ;
    rdfs:comment "Healthier pizza crust made from whole wheat flour"@en .

# -----------------------------------------------------------------------------
# SAUCE TOPPINGS
# -----------------------------------------------------------------------------

pz:Marinara rdf:type pz:SauceTopping ;
    rdfs:label "Marinara"@en ;
    rdfs:comment "Classic Italian tomato-based pizza sauce with herbs and garlic"@en .

pz:Pesto rdf:type pz:SauceTopping ;
    rdfs:label "Pesto"@en ;
    rdfs:comment "Green sauce made from basil, garlic, pine nuts, and olive oil"@en .

pz:BBQSauce rdf:type pz:SauceTopping ;
    rdfs:label "BBQ Sauce"@en ;
    rdfs:comment "Tangy barbecue sauce, popular with meat toppings"@en .

pz:WhiteSauce rdf:type pz:SauceTopping ;
    rdfs:label "White Sauce"@en ;
    rdfs:comment "Creamy white sauce made from butter, garlic, and herbs"@en .

pz:BuffaloSauce rdf:type pz:SauceTopping ;
    rdfs:label "Buffalo Sauce"@en ;
    rdfs:comment "Spicy sauce typically used with chicken toppings"@en .

pz:AlfredoSauce rdf:type pz:SauceTopping ;
    rdfs:label "Alfredo Sauce"@en ;
    rdfs:comment "Rich cream-based sauce with parmesan and garlic"@en .

pz:RanchSauce rdf:type pz:SauceTopping ;
    rdfs:label "Ranch Sauce"@en ;
    rdfs:comment "Creamy herb-based sauce popular as pizza drizzle"@en .

# -----------------------------------------------------------------------------
# CHEESE TOPPINGS
# -----------------------------------------------------------------------------

# Soft cheeses
pz:Mozzarella rdf:type pz:SoftCheese ;
    rdfs:label "Mozzarella"@en ;
    rdfs:comment "Traditional Italian cheese, commonly used on pizza, known for its mild flavor and excellent melting properties"@en .

pz:Ricotta rdf:type pz:SoftCheese ;
    rdfs:label "Ricotta"@en ;
    rdfs:comment "Fresh, creamy Italian cheese often used in white pizzas"@en .

pz:Mascarpone rdf:type pz:SoftCheese ;
    rdfs:label "Mascarpone"@en ;
    rdfs:comment "Rich, creamy Italian cheese with buttery flavor"@en .

pz:BurrataTopping rdf:type pz:SoftCheese ;
    rdfs:label "Burrata"@en ;
    rdfs:comment "Fresh Italian cheese with creamy center, added after baking"@en .

# Hard cheeses
pz:Parmesan rdf:type pz:HardCheese ;
    rdfs:label "Parmesan"@en ;
    rdfs:comment "Hard, aged Italian cheese with a sharp, nutty flavor, often grated over pizza"@en .

pz:Cheddar rdf:type pz:HardCheese ;
    rdfs:label "Cheddar"@en ;
    rdfs:comment "Sharp, firm cheese that adds a distinctive tangy flavor"@en .

pz:Romano rdf:type pz:HardCheese ;
    rdfs:label "Romano"@en ;
    rdfs:comment "Sharp, salty Italian cheese similar to Parmesan"@en .

pz:Asiago rdf:type pz:HardCheese ;
    rdfs:label "Asiago"@en ;
    rdfs:comment "Italian cheese with nutty, slightly sweet flavor when aged"@en .

# Other cheese varieties
pz:Provolone rdf:type pz:CheeseTopping ;
    rdfs:label "Provolone"@en ;
    rdfs:comment "Semi-hard Italian cheese with a mild, slightly sweet flavor"@en .

pz:Feta rdf:type pz:CheeseTopping ;
    rdfs:label "Feta"@en ;
    rdfs:comment "Greek cheese with a tangy, salty flavor and crumbly texture"@en .

pz:Gouda rdf:type pz:CheeseTopping ;
    rdfs:label "Gouda"@en ;
    rdfs:comment "Dutch cheese with a sweet, nutty flavor that melts well"@en .

pz:BleuCheese rdf:type pz:CheeseTopping ;
    rdfs:label "Blue Cheese"@en ;
    rdfs:comment "Pungent cheese with blue-green veins, popular with buffalo chicken"@en .

pz:Fontina rdf:type pz:CheeseTopping ;
    rdfs:label "Fontina"@en ;
    rdfs:comment "Italian cheese with mild, nutty flavor and excellent melting properties"@en .

pz:GruyereCheese rdf:type pz:CheeseTopping ;
    rdfs:label "Gruyère"@en ;
    rdfs:comment "Swiss cheese with complex, nutty flavor and smooth melting"@en .

# -----------------------------------------------------------------------------
# MEAT TOPPINGS
# -----------------------------------------------------------------------------

# Processed meats
pz:Pepperoni rdf:type pz:ProcessedMeat ;
    rdfs:label "Pepperoni"@en ;
    rdfs:comment "Spicy American salami made from cured pork and beef, a popular pizza topping"@en .

pz:Salami rdf:type pz:ProcessedMeat ;
    rdfs:label "Salami"@en ;
    rdfs:comment "Cured sausage with a distinctive spicy flavor"@en .

pz:Ham rdf:type pz:ProcessedMeat ;
    rdfs:label "Ham"@en ;
    rdfs:comment "Cured pork that adds a salty, smoky flavor to pizza"@en .

pz:Bacon rdf:type pz:ProcessedMeat ;
    rdfs:label "Bacon"@en ;
    rdfs:comment "Crispy, fatty pork strips that add smoky flavor and texture"@en .

pz:Prosciutto rdf:type pz:ProcessedMeat ;
    rdfs:label "Prosciutto"@en ;
    rdfs:comment "Thinly sliced, dry-cured Italian ham with delicate flavor"@en .

pz:Pancetta rdf:type pz:ProcessedMeat ;
    rdfs:label "Pancetta"@en ;
    rdfs:comment "Italian cured pork belly, similar to bacon but not smoked"@en .

pz:Chorizo rdf:type pz:ProcessedMeat ;
    rdfs:label "Chorizo"@en ;
    rdfs:comment "Spicy Spanish or Mexican sausage with paprika and chili"@en .

pz:Anchovies rdf:type pz:ProcessedMeat ;
    rdfs:label "Anchovies"@en ;
    rdfs:comment "Small, salty fish that add an intense umami flavor"@en .

# Fresh meats
pz:Sausage rdf:type pz:FreshMeat ;
    rdfs:label "Sausage"@en ;
    rdfs:comment "Seasoned ground meat (usually pork or beef) formed into small pieces for pizza topping"@en .

pz:Chicken rdf:type pz:FreshMeat ;
    rdfs:label "Chicken"@en ;
    rdfs:comment "Cooked chicken breast or thigh meat, often grilled or roasted"@en .

pz:GroundBeef rdf:type pz:FreshMeat ;
    rdfs:label "Ground Beef"@en ;
    rdfs:comment "Seasoned ground beef, commonly used on meat lovers' pizzas"@en .

pz:Turkey rdf:type pz:FreshMeat ;
    rdfs:label "Turkey"@en ;
    rdfs:comment "Lean poultry meat that provides protein with less fat than pork"@en .

pz:Meatballs rdf:type pz:FreshMeat ;
    rdfs:label "Meatballs"@en ;
    rdfs:comment "Seasoned balls of ground meat, typically beef and pork mixture"@en .

pz:PhillySteak rdf:type pz:FreshMeat ;
    rdfs:label "Philly Steak"@en ;
    rdfs:comment "Thinly sliced steak, popular on Philly cheesesteak pizzas"@en .

# -----------------------------------------------------------------------------
# VEGETABLE TOPPINGS
# -----------------------------------------------------------------------------

pz:Mushrooms rdf:type pz:VegetableTopping ;
    rdfs:label "Mushrooms"@en ;
    rdfs:comment "Sliced fungi, typically button or cremini mushrooms, used as a savory pizza topping"@en .

pz:BellPeppers rdf:type pz:VegetableTopping ;
    rdfs:label "Bell Peppers"@en ;
    rdfs:comment "Sweet, colorful peppers that add crunch and mild flavor"@en .

pz:Onions rdf:type pz:VegetableTopping ;
    rdfs:label "Onions"@en ;
    rdfs:comment "Sliced onions that add sharp flavor and become sweet when cooked"@en .

pz:Tomatoes rdf:type pz:VegetableTopping ;
    rdfs:label "Tomatoes"@en ;
    rdfs:comment "Fresh tomato slices that add acidity and freshness"@en .

pz:Olives rdf:type pz:VegetableTopping ;
    rdfs:label "Olives"@en ;
    rdfs:comment "Brined olives (black or green) that add salty, rich flavor"@en .

pz:Spinach rdf:type pz:VegetableTopping ;
    rdfs:label "Spinach"@en ;
    rdfs:comment "Leafy greens that add nutritional value and mild flavor"@en .

pz:Artichokes rdf:type pz:VegetableTopping ;
    rdfs:label "Artichokes"@en ;
    rdfs:comment "Marinated artichoke hearts with a tangy, tender texture"@en .

pz:Jalapenos rdf:type pz:VegetableTopping ;
    rdfs:label "Jalapeños"@en ;
    rdfs:comment "Spicy peppers that add heat and flavor to pizza"@en .

pz:RedPeppers rdf:type pz:VegetableTopping ;
    rdfs:label "Red Peppers"@en ;
    rdfs:comment "Roasted red peppers that add sweet, smoky flavor"@en .

pz:Pineapple rdf:type pz:VegetableTopping ;
    rdfs:label "Pineapple"@en ;
    rdfs:comment "Sweet tropical fruit that adds tropical flavor (controversial on pizza)"@en .

pz:BlackOlives rdf:type pz:VegetableTopping ;
    rdfs:label "Black Olives"@en ;
    rdfs:comment "Mild, brined black olives that add subtle salty flavor"@en .

pz:KalamataOlives rdf:type pz:VegetableTopping ;
    rdfs:label "Kalamata Olives"@en ;
    rdfs:comment "Greek olives with rich, fruity flavor and meaty texture"@en .

pz:SunDriedTomatoes rdf:type pz:VegetableTopping ;
    rdfs:label "Sun-Dried Tomatoes"@en ;
    rdfs:comment "Concentrated tomato flavor with chewy texture"@en .

pz:Basil rdf:type pz:VegetableTopping ;
    rdfs:label "Fresh Basil"@en ;
    rdfs:comment "Aromatic herb that adds fresh, peppery flavor"@en .

pz:Arugula rdf:type pz:VegetableTopping ;
    rdfs:label "Arugula"@en ;
    rdfs:comment "Peppery leafy green, often added after baking"@en .

pz:Capers rdf:type pz:VegetableTopping ;
    rdfs:label "Capers"@en ;
    rdfs:comment "Small, brined flower buds that add tangy, salty bursts"@en .

pz:Eggplant rdf:type pz:VegetableTopping ;
    rdfs:label "Eggplant"@en ;
    rdfs:comment "Grilled or roasted eggplant with mild, smoky flavor"@en .

pz:Zucchini rdf:type pz:VegetableTopping ;
    rdfs:label "Zucchini"@en ;
    rdfs:comment "Mild squash that adds texture and subtle flavor"@en .

pz:Broccoli rdf:type pz:VegetableTopping ;
    rdfs:label "Broccoli"@en ;
    rdfs:comment "Green vegetable florets that add nutrition and mild flavor"@en .

pz:Corn rdf:type pz:VegetableTopping ;
    rdfs:label "Corn"@en ;
    rdfs:comment "Sweet corn kernels that add crunch and sweetness"@en .

pz:RedOnions rdf:type pz:VegetableTopping ;
    rdfs:label "Red Onions"@en ;
    rdfs:comment "Milder than white onions with purple color and sweet flavor"@en .
```

Several points of note.

-   The prompt above was the consolidation of several prompts to provide the most optimal outcome.
    
-   While rdfs:subClassOf and rdfs:subPropertyOf relationships were included, rdfs:domain and rdfs:range were not, both because they are somewhat redundant and to minimize space.
    
-   The sh:name property has become a defacto equivalent for both GraphQL names and simplifications for JSON-LD (as opposed to being just another synonym for rdfs:label), and is used as such here. Typically, this defaults to the local name for the property.
    
-   The sh:in property is used to identify enumerated classes such as the following:
    

```
# Pizza Physical Shape
pz:PizzaPhysicalShapeShape a sh:NodeShape ;
    sh:name "PizzaPhysicalShape" ;
    sh:targetClass pz:PizzaShape ;
    rdfs:label "Pizza Physical Shape Shape"@en ;
    rdfs:comment "Validation shape for pizza physical shapes"@en ;
    sh:in ( pz:Round pz:Square pz:Rectangular ) .
```

-   I also included sh:message and sh:severity triples that were customized for each property shape, to provide better documentation for validation than the default.
    
-   As always the case with transformers, spend time reviewing the output to make sure you don’t see any surprise gotchas.
    

## Using the Pizza SHACL

So, once you have the SHACL, what can you do with it?

One of the more powerful aspects of this is using it to interpret prompt requests. For instance, assuming you have attached the SHACL as a file, the following property:

```
Convert this into Turtle, using the attached pizza SHACL file:

I'd like a thick crust half and half pizza, with one half Sicilian, the other hawaiian, for delivery
```

returns the following:

```
@prefix pz: <https://example.com/ns/pizza#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# Half-and-Half Pizza: Sicilian and Hawaiian
pz:HalfAndHalfPizzaOrder001 rdf:type pz:Pizza ;
    rdfs:label "Half Sicilian Half Hawaiian Pizza"@en ;
    rdfs:comment "Thick crust pizza with one half Sicilian and one half Hawaiian for delivery"@en ;
    pz:hasPizzaSize pz:Large ;
    pz:hasPizzaStyle pz:ThickCrust ;
    pz:hasPizzaShape pz:Round ;
    pz:hasPizzaDelivery pz:Delivered ;
    pz:hasDivision pz:SicilianHalf001 ;
    pz:hasDivision pz:HawaiianHalf001 .

# First Division - Sicilian Half
pz:SicilianHalf001 rdf:type pz:PizzaDiv ;
    rdfs:label "Sicilian Half"@en ;
    rdfs:comment "One half of the pizza with Sicilian-style toppings"@en ;
    pz:hasConfiguration pz:SicilianConfig001 .

# Sicilian Configuration
pz:SicilianConfig001 rdf:type pz:PizzaConfig ;
    rdfs:label "Sicilian Configuration"@en ;
    rdfs:comment "Traditional Sicilian pizza with marinara, mozzarella, and classic toppings"@en ;
    pz:hasLabel "Sicilian Half"@en ;
    pz:hasCrust pz:WheatCrust ;
    # Sicilian typically uses marinara sauce
    pz:hasSauce pz:Marinara ;
    # Traditional Sicilian cheese blend
    pz:hasCheeseTopping pz:Mozzarella ;
    pz:hasCheeseTopping pz:Parmesan ;
    # Classic Sicilian meat toppings
    pz:hasMeatTopping pz:Pepperoni ;
    pz:hasMeatTopping pz:Sausage ;
    # Traditional Sicilian vegetable toppings
    pz:hasVegetableTopping pz:Mushrooms ;
    pz:hasVegetableTopping pz:BellPeppers ;
    pz:hasVegetableTopping pz:Onions ;
    pz:hasVegetableTopping pz:BlackOlives .

# Second Division - Hawaiian Half
pz:HawaiianHalf001 rdf:type pz:PizzaDiv ;
    rdfs:label "Hawaiian Half"@en ;
    rdfs:comment "One half of the pizza with Hawaiian-style toppings"@en ;
    pz:hasConfiguration pz:HawaiianConfig001 .

# Hawaiian Configuration
pz:HawaiianConfig001 rdf:type pz:PizzaConfig ;
    rdfs:label "Hawaiian Configuration"@en ;
    rdfs:comment "Traditional Hawaiian pizza with ham and pineapple"@en ;
    pz:hasLabel "Hawaiian Half"@en ;
    pz:hasCrust pz:WheatCrust ;
    # Hawaiian typically uses marinara or tomato sauce
    pz:hasSauce pz:Marinara ;
    # Traditional Hawaiian cheese
    pz:hasCheeseTopping pz:Mozzarella ;
    # Hawaiian meat topping
    pz:hasMeatTopping pz:Ham ;
    # Hawaiian vegetable topping
    pz:hasVegetableTopping pz:Pineapple .
```

This creates an RDF Turtle file showing two distinct halves - one Sicilian, the other Hawaiian, with the associated ingredients. You can also do the same with JSON-LD, with

```
Convert this into Compact JSON-LD, using the attached pizza SHACL file:

I'd like a thick crust half and half pizza, with one half Sicilian, the other Hawaiian, for delivery
```

```
{
  "@context": {
    "pz": "https://example.com/ns/pizza#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "@vocab": "https://example.com/ns/pizza#",
    
    "Pizza": "pz:Pizza",
    "PizzaDiv": "pz:PizzaDiv", 
    "PizzaConfig": "pz:PizzaConfig",
    "PizzaSize": "pz:PizzaSize",
    "PizzaStyle": "pz:PizzaStyle",
    "PizzaShape": "pz:PizzaShape",
    "PizzaDelivery": "pz:PizzaDelivery",
    "Crust": "pz:Crust",
    "SauceTopping": "pz:SauceTopping",
    "CheeseTopping": "pz:CheeseTopping",
    "MeatTopping": "pz:MeatTopping",
    "VegetableTopping": "pz:VegetableTopping",
    
    "pizzaSize": { "@id": "pz:hasPizzaSize", "@type": "@id" },
    "pizzaStyle": { "@id": "pz:hasPizzaStyle", "@type": "@id" },
    "pizzaShape": { "@id": "pz:hasPizzaShape", "@type": "@id" },
    "deliveryMethod": { "@id": "pz:hasPizzaDelivery", "@type": "@id" },
    "divisions": { "@id": "pz:hasDivision", "@type": "@id" },
    "configurations": { "@id": "pz:hasConfiguration", "@type": "@id" },
    "configLabel": { "@id": "pz:hasLabel", "@type": "xsd:string" },
    "crust": { "@id": "pz:hasCrust", "@type": "@id" },
    "sauceToppings": { "@id": "pz:hasSauce", "@type": "@id" },
    "cheeseToppings": { "@id": "pz:hasCheeseTopping", "@type": "@id" },
    "meatToppings": { "@id": "pz:hasMeatTopping", "@type": "@id" },
    "vegetableToppings": { "@id": "pz:hasVegetableTopping", "@type": "@id" },
    
    "label": { "@id": "rdfs:label", "@type": "rdf:langString" },
    "comment": { "@id": "rdfs:comment", "@type": "rdf:langString" }
  },
  
  "@graph": [
    {
      "@id": "pz:HalfAndHalfPizzaOrder001",
      "@type": "Pizza",
      "label": { "@value": "Half Sicilian Half Hawaiian Pizza", "@language": "en" },
      "comment": { "@value": "Thick crust pizza with one half Sicilian and one half Hawaiian for delivery", "@language": "en" },
      "pizzaSize": "pz:Large",
      "pizzaStyle": "pz:ThickCrust", 
      "pizzaShape": "pz:Round",
      "deliveryMethod": "pz:Delivered",
      "divisions": [
        "pz:SicilianHalf001",
        "pz:HawaiianHalf001"
      ]
    },
    
    {
      "@id": "pz:SicilianHalf001",
      "@type": "PizzaDiv",
      "label": { "@value": "Sicilian Half", "@language": "en" },
      "comment": { "@value": "One half of the pizza with Sicilian-style toppings", "@language": "en" },
      "configurations": "pz:SicilianConfig001"
    },
    
    {
      "@id": "pz:SicilianConfig001", 
      "@type": "PizzaConfig",
      "label": { "@value": "Sicilian Configuration", "@language": "en" },
      "comment": { "@value": "Traditional Sicilian pizza with marinara, mozzarella, and classic toppings", "@language": "en" },
      "configLabel": "Sicilian Half",
      "crust": "pz:WheatCrust",
      "sauceToppings": "pz:Marinara",
      "cheeseToppings": [
        "pz:Mozzarella",
        "pz:Parmesan"
      ],
      "meatToppings": [
        "pz:Pepperoni", 
        "pz:Sausage"
      ],
      "vegetableToppings": [
        "pz:Mushrooms",
        "pz:BellPeppers", 
        "pz:Onions",
        "pz:BlackOlives"
      ]
    },
    
    {
      "@id": "pz:HawaiianHalf001",
      "@type": "PizzaDiv", 
      "label": { "@value": "Hawaiian Half", "@language": "en" },
      "comment": { "@value": "One half of the pizza with Hawaiian-style toppings", "@language": "en" },
      "configurations": "pz:HawaiianConfig001"
    },
    
    {
      "@id": "pz:HawaiianConfig001",
      "@type": "PizzaConfig",
      "label": { "@value": "Hawaiian Configuration", "@language": "en" },
      "comment": { "@value": "Traditional Hawaiian pizza with ham and pineapple", "@language": "en" },
      "configLabel": "Hawaiian Half", 
      "crust": "pz:WheatCrust",
      "sauceToppings": "pz:Marinara",
      "cheeseToppings": "pz:Mozzarella",
      "meatToppings": "pz:Ham",
      "vegetableToppings": "pz:Pineapple"
    }
  ]
}
```

This is where the sh:name property comes in handy, as it is used to provide the labels for the various components of the pizza according to the established context file:

You can also use the SHACL to do informal validation:

```
> Given the shacl file, can I have a pizza with herrings on it?
```

The output is as follows:

_Looking at the SHACL file, I can see that herrings are not defined as one of the available toppings in the pizza ontology._

_The meat toppings defined in the ontology are:_

_**Processed Meats:**_

-   _Pepperoni, Salami, Ham, Bacon, Prosciutto, Pancetta, Chorizo, Anchovies_
    

_**Fresh Meats:**_

-   _Sausage, Chicken, Ground Beef, Turkey, Meatballs, Philly Steak_
    

_While **anchovies** are included (which are also small fish), **herrings** are not specifically defined in the ontology._

You can also get the formal messages back with the following prompt:

```
Given the shacl file, can I have a pizza with herrings on it? Show me the formal SHACL messages
```

Output:

```
# =============================================================================
# FORMAL SHACL VALIDATION REPORT
# =============================================================================

# Validation Result 1: Invalid meat topping reference
[] rdf:type sh:ValidationReport ;
    sh:conforms false ;
    sh:result [
        rdf:type sh:ValidationResult ;
        sh:resultSeverity sh:Warning ;
        sh:resultPath pz:hasMeatTopping ;
        sh:focusNode pz:HerringConfig001 ;
        sh:value pz:Herrings ;
        sh:sourceConstraintComponent sh:ClassConstraintComponent ;
        sh:sourceShape pz:PizzaConfigShape ;
        sh:resultMessage "Invalid meat topping reference"@en ;
        sh:detail "The value 'pz:Herrings' for property 'pz:hasMeatTopping' does not conform to the expected class 'pz:MeatTopping' with proper definition" ;
    ] .

# Validation Result 2: Undefined class instance  
[] rdf:type sh:ValidationReport ;
    sh:conforms false ;
    sh:result [
        rdf:type sh:ValidationResult ;
        sh:resultSeverity sh:Violation ;
        sh:resultPath rdf:type ;
        sh:focusNode pz:Herrings ;
        sh:value pz:MeatTopping ;
        sh:sourceConstraintComponent sh:NodeKindConstraintComponent ;
        sh:resultMessage "Topping must have proper label and description"@en ;
        sh:detail "The instance 'pz:Herrings' lacks required rdfs:label property as specified in pz:ToppingShape" ;
    ] .

# Validation Result 3: Missing required topping properties
[] rdf:type sh:ValidationReport ;
    sh:conforms false ;
    sh:result [
        rdf:type sh:ValidationResult ;
        sh:resultSeverity sh:Violation ;
        sh:resultPath rdfs:label ;
        sh:focusNode pz:Herrings ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:sourceShape pz:ToppingShape ;
        sh:resultMessage "Every topping must have exactly one label"@en ;
        sh:detail "Missing required rdfs:label for topping instance pz:Herrings" ;
    ] .
```

In this case, the SHACL messages inform the generated human readable responses.

Let’s take this full circle (a pizza pie, natch), and generate a mermaid file based upon the generated half and half pizza:

[

![](https://substackcdn.com/image/fetch/$s_!3Zpk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff7f6c8c2-ba12-4a81-a8b4-12523293f480_3840x2735.png)

](https://substackcdn.com/image/fetch/$s_!3Zpk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff7f6c8c2-ba12-4a81-a8b4-12523293f480_3840x2735.png)

Finally, you can use this to drive image generation:

```
> Make a good Google Nano Banana image generation prompt under 2500 (plain text)  for an appetizing pizza based upon the attached halfAndHalf.ttl file:
```

The output is:

```
Create a photorealistic image of a mouthwatering large round pizza with thick golden-brown crust, perfectly split down the middle into two distinct halves. The pizza sits on a rustic wooden board with warm overhead lighting casting appetizing shadows. LEFT SICILIAN HALF: Rich marinara sauce base with bubbling melted mozzarella and grated parmesan creating golden-brown spots. Loaded with crispy pepperoni slices with slightly curled edges, crumbled Italian sausage pieces, fresh sliced mushrooms, colorful red and yellow bell pepper strips, translucent caramelized onions, and glossy black olives scattered throughout. The toppings are abundant and layered, creating a hearty, robust appearance. RIGHT HAWAIIAN HALF: Bright marinara sauce base with perfectly melted mozzarella cheese. Features thick-cut ham slices with caramelized edges and bright yellow pineapple chunks that are slightly caramelized from the oven heat, showing some golden browning on the edges. The simpler topping arrangement creates visual contrast with the busy Sicilian side. The thick crust should be golden-brown with slight char spots, showing a pillowy texture with visible air bubbles. Steam rises gently from the hot pizza. The cheese is perfectly melted with some attractive browning and stretchy pulls visible. Professional food photography lighting emphasizes the textures - the glossy pepperoni oils, the vibrant vegetable colors, the golden cheese bubbling, and the rustic crust texture. Background shows a cozy pizzeria setting with soft focus. The overall image should make viewers immediately crave this delicious half-and-half pizza combination.
```

Passing this into Google’s Nano Banana, we get this mouth-watering treat:

[

![](https://substackcdn.com/image/fetch/$s_!Nuc2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ea45db7-3cb4-4d10-a519-5e4722cf1bf9_1344x768.png)

](https://substackcdn.com/image/fetch/$s_!Nuc2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ea45db7-3cb4-4d10-a519-5e4722cf1bf9_1344x768.png)

Bon Appetit!

[

![](https://substackcdn.com/image/fetch/$s_!XZQb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80757ac1-3eef-4c0c-9099-2867c323019f_1024x1024.jpeg)

](https://substackcdn.com/image/fetch/$s_!XZQb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80757ac1-3eef-4c0c-9099-2867c323019f_1024x1024.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.

[1](https://substack.com/@kurtcagle/p-189271561#footnote-anchor-1-172541092)

An RDF knowledge graph is mostly ACID compliant, but because you are dealing with open world assumption links that may or may not be within a given dataset, atomicity has a slightly different interpretation for such links (e.g., you don’t necessarily have referential integrity in a knowledge graph). This isn’t necessarily that major an issue, as RDF assumes that the entire world is a global data system, but it’s worth mentioning.

