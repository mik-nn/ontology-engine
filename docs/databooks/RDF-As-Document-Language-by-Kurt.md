---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: RDF-As-Document-Language-by-Kurt
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:51.997172+00:00'
  title: Rdf As Document Language By Kurt
  type: plain-doc
  version: '0.1'
---

# Rdf As Document Language By Kurt

[

![](https://substackcdn.com/image/fetch/$s_!bDfb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9abcd685-af61-4627-9ba9-905069f29ae8_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!bDfb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9abcd685-af61-4627-9ba9-905069f29ae8_2688x1536.jpeg)

_This started out as an article on RDF as assembly language, but as I wrote it, I realized that there was another question that needed to be answered first - how to you describe narrative documents semantically. It’s perhaps overlong - I had a number of code samples that I felt were relevant, but mostly it comes down to thinking about … well, stories._

## Narratives as Temporal Structures

When you think about it, reading is really weird, especially reading fiction. As you progress through a novel, a bare page gives way to a scene that becomes more vivid over time, with characters that talk and interact with one another creating an evolving tapestry that can be more vivid than real life. What is so odd about narratives is that at any given point in a book you are moving through time via a series of events, each of which provides more contextual information while at the same time keeping you focused on the “now”.

This process is facilitated by the notion of traversal. Typically a book is deconstructed into chapters, which are then deconstructed into scenes, and from there into paragraphs and dialog. XML serializes structures via containment, retaining order at any given level as nodes are encountered and going deeper into the the tree of a document before moving laterally from sibling to sibling. JSON uses a similar convention, encoding information serially via arrays in a specific order and recursively going deeper until leaf items in that array are reached (there are no attached arrays).

By following this “down then right” traversal method in hierarchies (especially when those hierarchies are events), you are in effect creating a serialisation of that hierarchy as a narrative. This is really what most “documents” are built around - the notion of sequential serialization of increasingly detailed information derived from walking a hierarchical outline in temporal order.

Put another way, most documents can be written as outlines of some sort, with each subsection providing increasingly detailed information. In practice, you can think of PowerPoint presentations as being “drill-down” oriented semi-serialisations of documents into some kind of talk.

This notion of temporal serialization is important, because it is also (not surprisingly) what happens with LLM transformers generate successive contextual layers with attention. This is not by itself in the model. Rather, it’s in the (full) prompt. The ordering of the prompt (passed prompt + RAG + guardrails) has a significant impact upon the narrative structures, in essence, building specific ordered output that reflects prompt narrative. This is why using RAG on PDF documents works as well as it does - the RAG is reflecting this implicit ordering bias, with gathered context providing deeper and deeper “dives” into the information space.

RDF is capable of representing such narrative outlines, but it requires using the abstraction that Turtle utilizes, specifically the collection ( ) operators. To understand how this works (and why it is actually fairly fundamental to all representions of RDF, not just Turtle), it’s worth getting a better understanding of how denormalization works. This in turn means going beyond RDF at its simplest form and seeing it as a language for expressing complex data structures.

## Why Developers Don’t Like RDF

After nearly 25 years, you’d think that RDF would be far more prevalent than it is. After all, it was contemporary with XML, and preceded JSON by nearly a decade. Yet it has struggled to make its way into enterprise-level systems for a wide number of reasons:

-   It looks very verbose (lot’s of repetition of namespaces in particular).
    
-   It doesn’t feat neatly into the dictionary/array mindset that most programmers are familiar with
    
-   Namespaces are confusing.
    
-   Graphs? We don’t need no stinkin’ graphs!
    
-   You needed a PhD in logical systems just to make it useful
    
-   It was slow.
    
-   You couldn’t use dot notation with it (convert it into Javascript or Python objects)
    
-   It’s not SQL
    
-   RDF isn’t powerful enough
    
-   There are easier ways of doing things
    

Some of these were true even ten years ago, some of these are still true but aren’t necessarily relevant, and some were never true. That doesn’t always seem to matter with technology - once a given tech has been perceived as not meeting the immediate needs of developers RIGHT NOW, it usually ends up in the equivalent of the cheap bins at Target.

However, like much of what came from the very fertile brain of Tim Berners-Lee, RDF has had a curious staying power, although it took the advent of GenAI for it to finally really hit its stride. Part of the reason it has taken so long is that most people coming to RDF have seen it in earlier incarnations, such as RDF-XML:

```
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
         xmlns:pz="https://example.com/ns/pizza#">

  <!-- Pizza instance -->
  <pz:Pizza rdf:about="https://example.com/ns/pizza#MyPie1">
    <rdfs:label xml:lang="en">My Pie 1</rdfs:label>
    <rdfs:comment xml:lang="en">A specific pizza instance with thin crust, medium size, and mixed toppings</rdfs:comment>
    <pz:hasDivision rdf:resource="https://example.com/ns/pizza#PizzaDiv"/>
    <pz:hasPizzaSize rdf:resource="https://example.com/ns/pizza#Medium"/>
    <pz:hasPizzaStyle rdf:resource="https://example.com/ns/pizza#ThinCrust"/>
    <pz:hasPizzaShape rdf:resource="https://example.com/ns/pizza#Round"/>
    <pz:hasPizzaDelivery rdf:resource="https://example.com/ns/pizza#Delivered"/>
  </pz:Pizza>

  <!-- Pizza division -->
  <pz:PizzaDiv rdf:about="https://example.com/ns/pizza#PizzaDiv">
    <rdfs:label xml:lang="en">Pizza Division</rdfs:label>
    <rdfs:comment xml:lang="en">A logical division of a pizza that can contain multiple configuration sections</rdfs:comment>
    <pz:hasConfiguration rdf:resource="https://example.com/ns/pizza#TheSicilian"/>
    <pz:hasConfiguration rdf:resource="https://example.com/ns/pizza#Custom"/>
  </pz:PizzaDiv>

  <!-- Pizza configurations -->
  <pz:PizzaConfig rdf:about="https://example.com/ns/pizza#TheSicilian">
    <rdfs:label xml:lang="en">The Sicilian</rdfs:label>
    <rdfs:comment xml:lang="en">A traditional Sicilian-style pizza configuration with marinara sauce, mozzarella, pepperoni, mushrooms, and wheat crust</rdfs:comment>
    <pz:hasLabel rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Sicilian</pz:hasLabel>
    <pz:hasSauce rdf:resource="https://example.com/ns/pizza#Marinara"/>
    <pz:hasCheeseTopping rdf:resource="https://example.com/ns/pizza#Mozzarella"/>
    <pz:hasMeatTopping rdf:resource="https://example.com/ns/pizza#Pepperoni"/>
    <pz:hasVegetableTopping rdf:resource="https://example.com/ns/pizza#Mushrooms"/>
    <pz:hasCrust rdf:resource="https://example.com/ns/pizza#WheatCrust"/>
  </pz:PizzaConfig>

  <pz:PizzaConfig rdf:about="https://example.com/ns/pizza#Custom">
    <rdfs:label xml:lang="en">Custom Configuration</rdfs:label>
    <rdfs:comment xml:lang="en">A custom pizza configuration with parmesan cheese and sausage toppings</rdfs:comment>
    <pz:hasCheeseTopping rdf:resource="https://example.com/ns/pizza#Parmesan"/>
    <pz:hasMeatTopping rdf:resource="https://example.com/ns/pizza#Sausage"/>
  </pz:PizzaConfig>

  <!-- Pizza properties -->
  <pz:PizzaSize rdf:about="https://example.com/ns/pizza#Medium">
    <rdfs:label xml:lang="en">Medium</rdfs:label>
    <rdfs:comment xml:lang="en">A medium-sized pizza, typically 12 inches in diameter</rdfs:comment>
  </pz:PizzaSize>

  <pz:PizzaStyle rdf:about="https://example.com/ns/pizza#ThinCrust">
    <rdfs:label xml:lang="en">Thin Crust</rdfs:label>
    <rdfs:comment xml:lang="en">A pizza style characterized by a thin, crispy crust base</rdfs:comment>
  </pz:PizzaStyle>

  <pz:PizzaShape rdf:about="https://example.com/ns/pizza#Round">
    <rdfs:label xml:lang="en">Round</rdfs:label>
    <rdfs:comment xml:lang="en">Traditional circular pizza shape</rdfs:comment>
  </pz:PizzaShape>

  <pz:PizzaDelivery rdf:about="https://example.com/ns/pizza#Delivered">
    <rdfs:label xml:lang="en">Delivered</rdfs:label>
    <rdfs:comment xml:lang="en">Pizza delivery method where the pizza is brought to the customer</rdfs:comment>
  </pz:PizzaDelivery>

  <!-- Toppings -->
  <pz:SauceTopping rdf:about="https://example.com/ns/pizza#Marinara">
    <rdfs:label xml:lang="en">Marinara</rdfs:label>
    <rdfs:comment xml:lang="en">Classic Italian tomato-based pizza sauce with herbs and garlic</rdfs:comment>
  </pz:SauceTopping>

  <pz:CheeseTopping rdf:about="https://example.com/ns/pizza#Mozzarella">
    <rdfs:label xml:lang="en">Mozzarella</rdfs:label>
    <rdfs:comment xml:lang="en">Traditional Italian cheese, commonly used on pizza, known for its mild flavor and excellent melting properties</rdfs:comment>
  </pz:CheeseTopping>

  <pz:CheeseTopping rdf:about="https://example.com/ns/pizza#Parmesan">
    <rdfs:label xml:lang="en">Parmesan</rdfs:label>
    <rdfs:comment xml:lang="en">Hard, aged Italian cheese with a sharp, nutty flavor, often grated over pizza</rdfs:comment>
  </pz:CheeseTopping>

  <pz:MeatTopping rdf:about="https://example.com/ns/pizza#Pepperoni">
    <rdfs:label xml:lang="en">Pepperoni</rdfs:label>
    <rdfs:comment xml:lang="en">Spicy American salami made from cured pork and beef, a popular pizza topping</rdfs:comment>
  </pz:MeatTopping>

  <pz:MeatTopping rdf:about="https://example.com/ns/pizza#Sausage">
    <rdfs:label xml:lang="en">Sausage</rdfs:label>
    <rdfs:comment xml:lang="en">Seasoned ground meat (usually pork or beef) formed into small pieces for pizza topping</rdfs:comment>
  </pz:MeatTopping>

  <pz:VegetableTopping rdf:about="https://example.com/ns/pizza#Mushrooms">
    <rdfs:label xml:lang="en">Mushrooms</rdfs:label>
    <rdfs:comment xml:lang="en">Sliced fungi, typically button or cremini mushrooms, used as a savory pizza topping</rdfs:comment>
  </pz:VegetableTopping>

  <!-- Crust -->
  <pz:Crust rdf:about="https://example.com/ns/pizza#WheatCrust">
    <rdfs:label xml:lang="en">Wheat Crust</rdfs:label>
    <rdfs:comment xml:lang="en">Pizza crust made from wheat flour, providing the base structure of the pizza</rdfs:comment>
  </pz:Crust>

</rdf:RDF>
```

For your average developer, they take one look at this and say “Nope, I don’t have an XML toolchain, not important for me.”

Similarly, others will look at NT notation (also RDF):

```
# Pizza instance
<https://example.com/ns/pizza#MyPie1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#Pizza> .
<https://example.com/ns/pizza#MyPie1> <http://www.w3.org/2000/01/rdf-schema#label> "My Pie 1"@en .
<https://example.com/ns/pizza#MyPie1> <http://www.w3.org/2000/01/rdf-schema#comment> "A specific pizza instance with thin crust, medium size, and mixed toppings"@en .
<https://example.com/ns/pizza#MyPie1> <https://example.com/ns/pizza#hasDivision> <https://example.com/ns/pizza#PizzaDiv> .
<https://example.com/ns/pizza#MyPie1> <https://example.com/ns/pizza#hasPizzaSize> <https://example.com/ns/pizza#Medium> .
<https://example.com/ns/pizza#MyPie1> <https://example.com/ns/pizza#hasPizzaStyle> <https://example.com/ns/pizza#ThinCrust> .
<https://example.com/ns/pizza#MyPie1> <https://example.com/ns/pizza#hasPizzaShape> <https://example.com/ns/pizza#Round> .
<https://example.com/ns/pizza#MyPie1> <https://example.com/ns/pizza#hasPizzaDelivery> <https://example.com/ns/pizza#Delivered> .

# Pizza division
<https://example.com/ns/pizza#PizzaDiv> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#PizzaDiv> .
<https://example.com/ns/pizza#PizzaDiv> <http://www.w3.org/2000/01/rdf-schema#label> "Pizza Division"@en .
<https://example.com/ns/pizza#PizzaDiv> <http://www.w3.org/2000/01/rdf-schema#comment> "A logical division of a pizza that can contain multiple configuration sections"@en .
<https://example.com/ns/pizza#PizzaDiv> <https://example.com/ns/pizza#hasConfiguration> <https://example.com/ns/pizza#TheSicilian> .
<https://example.com/ns/pizza#PizzaDiv> <https://example.com/ns/pizza#hasConfiguration> <https://example.com/ns/pizza#Custom> .

# Pizza configurations
<https://example.com/ns/pizza#TheSicilian> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#PizzaConfig> .
<https://example.com/ns/pizza#TheSicilian> <http://www.w3.org/2000/01/rdf-schema#label> "The Sicilian"@en .
<https://example.com/ns/pizza#TheSicilian> <http://www.w3.org/2000/01/rdf-schema#comment> "A traditional Sicilian-style pizza configuration with marinara sauce, mozzarella, pepperoni, mushrooms, and wheat crust"@en .
<https://example.com/ns/pizza#TheSicilian> <https://example.com/ns/pizza#hasLabel> "Sicilian"^^<http://www.w3.org/2001/XMLSchema#string> .
<https://example.com/ns/pizza#TheSicilian> <https://example.com/ns/pizza#hasSauce> <https://example.com/ns/pizza#Marinara> .
<https://example.com/ns/pizza#TheSicilian> <https://example.com/ns/pizza#hasCheeseTopping> <https://example.com/ns/pizza#Mozzarella> .
<https://example.com/ns/pizza#TheSicilian> <https://example.com/ns/pizza#hasMeatTopping> <https://example.com/ns/pizza#Pepperoni> .
<https://example.com/ns/pizza#TheSicilian> <https://example.com/ns/pizza#hasVegetableTopping> <https://example.com/ns/pizza#Mushrooms> .
<https://example.com/ns/pizza#TheSicilian> <https://example.com/ns/pizza#hasCrust> <https://example.com/ns/pizza#WheatCrust> .

<https://example.com/ns/pizza#Custom> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#PizzaConfig> .
<https://example.com/ns/pizza#Custom> <http://www.w3.org/2000/01/rdf-schema#label> "Custom Configuration"@en .
<https://example.com/ns/pizza#Custom> <http://www.w3.org/2000/01/rdf-schema#comment> "A custom pizza configuration with parmesan cheese and sausage toppings"@en .
<https://example.com/ns/pizza#Custom> <https://example.com/ns/pizza#hasCheeseTopping> <https://example.com/ns/pizza#Parmesan> .
<https://example.com/ns/pizza#Custom> <https://example.com/ns/pizza#hasMeatTopping> <https://example.com/ns/pizza#Sausage> .

# Pizza properties
<https://example.com/ns/pizza#Medium> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#PizzaSize> .
<https://example.com/ns/pizza#Medium> <http://www.w3.org/2000/01/rdf-schema#label> "Medium"@en .
<https://example.com/ns/pizza#Medium> <http://www.w3.org/2000/01/rdf-schema#comment> "A medium-sized pizza, typically 12 inches in diameter"@en .

<https://example.com/ns/pizza#ThinCrust> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#PizzaStyle> .
<https://example.com/ns/pizza#ThinCrust> <http://www.w3.org/2000/01/rdf-schema#label> "Thin Crust"@en .
<https://example.com/ns/pizza#ThinCrust> <http://www.w3.org/2000/01/rdf-schema#comment> "A pizza style characterized by a thin, crispy crust base"@en .

<https://example.com/ns/pizza#Round> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#PizzaShape> .
<https://example.com/ns/pizza#Round> <http://www.w3.org/2000/01/rdf-schema#label> "Round"@en .
<https://example.com/ns/pizza#Round> <http://www.w3.org/2000/01/rdf-schema#comment> "Traditional circular pizza shape"@en .

<https://example.com/ns/pizza#Delivered> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#PizzaDelivery> .
<https://example.com/ns/pizza#Delivered> <http://www.w3.org/2000/01/rdf-schema#label> "Delivered"@en .
<https://example.com/ns/pizza#Delivered> <http://www.w3.org/2000/01/rdf-schema#comment> "Pizza delivery method where the pizza is brought to the customer"@en .

# Toppings
<https://example.com/ns/pizza#Marinara> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#SauceTopping> .
<https://example.com/ns/pizza#Marinara> <http://www.w3.org/2000/01/rdf-schema#label> "Marinara"@en .
<https://example.com/ns/pizza#Marinara> <http://www.w3.org/2000/01/rdf-schema#comment> "Classic Italian tomato-based pizza sauce with herbs and garlic"@en .

<https://example.com/ns/pizza#Mozzarella> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#CheeseTopping> .
<https://example.com/ns/pizza#Mozzarella> <http://www.w3.org/2000/01/rdf-schema#label> "Mozzarella"@en .
<https://example.com/ns/pizza#Mozzarella> <http://www.w3.org/2000/01/rdf-schema#comment> "Traditional Italian cheese, commonly used on pizza, known for its mild flavor and excellent melting properties"@en .

<https://example.com/ns/pizza#Parmesan> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#CheeseTopping> .
<https://example.com/ns/pizza#Parmesan> <http://www.w3.org/2000/01/rdf-schema#label> "Parmesan"@en .
<https://example.com/ns/pizza#Parmesan> <http://www.w3.org/2000/01/rdf-schema#comment> "Hard, aged Italian cheese with a sharp, nutty flavor, often grated over pizza"@en .

<https://example.com/ns/pizza#Pepperoni> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#MeatTopping> .
<https://example.com/ns/pizza#Pepperoni> <http://www.w3.org/2000/01/rdf-schema#label> "Pepperoni"@en .
<https://example.com/ns/pizza#Pepperoni> <http://www.w3.org/2000/01/rdf-schema#comment> "Spicy American salami made from cured pork and beef, a popular pizza topping"@en .

<https://example.com/ns/pizza#Sausage> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#MeatTopping> .
<https://example.com/ns/pizza#Sausage> <http://www.w3.org/2000/01/rdf-schema#label> "Sausage"@en .
<https://example.com/ns/pizza#Sausage> <http://www.w3.org/2000/01/rdf-schema#comment> "Seasoned ground meat (usually pork or beef) formed into small pieces for pizza topping"@en .

<https://example.com/ns/pizza#Mushrooms> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#VegetableTopping> .
<https://example.com/ns/pizza#Mushrooms> <http://www.w3.org/2000/01/rdf-schema#label> "Mushrooms"@en .
<https://example.com/ns/pizza#Mushrooms> <http://www.w3.org/2000/01/rdf-schema#comment> "Sliced fungi, typically button or cremini mushrooms, used as a savory pizza topping"@en .

# Crust
<https://example.com/ns/pizza#WheatCrust> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://example.com/ns/pizza#Crust> .
<https://example.com/ns/pizza#WheatCrust> <http://www.w3.org/2000/01/rdf-schema#label> "Wheat Crust"@en .
<https://example.com/ns/pizza#WheatCrust> <http://www.w3.org/2000/01/rdf-schema#comment> "Pizza crust made from wheat flour, providing the base structure of the pizza"@en .
```

By now, programmers are starting to twitch, because this is not simple to work with and way too verbose. Turtle may be a bit better:

```
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

but it still is in a format that most programmers don’t know how to parse and don’t know what to do with even if it is parsed. Finally, after several years had passed, a JSON version arrived (JSON-LD):

```
{
  "@context": {
    "@vocab": "https://example.com/ns/pizza#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "label": "rdfs:label",
    "comment": "rdfs:comment",
    "hasDivision": {"@type": "@id"},
    "hasPizzaSize": {"@type": "@id"},
    "hasPizzaStyle": {"@type": "@id"},
    "hasPizzaShape": {"@type": "@id"},
    "hasPizzaDelivery": {"@type": "@id"},
    "hasConfiguration": {"@type": "@id"},
    "hasSauce": {"@type": "@id"},
    "hasCheeseTopping": {"@type": "@id"},
    "hasMeatTopping": {"@type": "@id"},
    "hasVegetableTopping": {"@type": "@id"},
    "hasCrust": {"@type": "@id"},
    "hasLabel": {"@type": "xsd:string"}
  },
  "@graph": [
    {
      "@id": "MyPie1",
      "@type": "Pizza",
      "label": {
        "@value": "My Pie 1",
        "@language": "en"
      },
      "comment": {
        "@value": "A specific pizza instance with thin crust, medium size, and mixed toppings",
        "@language": "en"
      },
      "hasDivision": "PizzaDiv",
      "hasPizzaSize": "Medium",
      "hasPizzaStyle": "ThinCrust",
      "hasPizzaShape": "Round",
      "hasPizzaDelivery": "Delivered"
    },
    {
      "@id": "PizzaDiv",
      "@type": "PizzaDiv",
      "label": {
        "@value": "Pizza Division",
        "@language": "en"
      },
      "comment": {
        "@value": "A logical division of a pizza that can contain multiple configuration sections",
        "@language": "en"
      },
      "hasConfiguration": ["TheSicilian", "Custom"]
    },
    {
      "@id": "TheSicilian",
      "@type": "PizzaConfig",
      "label": {
        "@value": "The Sicilian",
        "@language": "en"
      },
      "comment": {
        "@value": "A traditional Sicilian-style pizza configuration with marinara sauce, mozzarella, pepperoni, mushrooms, and wheat crust",
        "@language": "en"
      },
      "hasLabel": "Sicilian",
      "hasSauce": "Marinara",
      "hasCheeseTopping": "Mozzarella",
      "hasMeatTopping": "Pepperoni",
      "hasVegetableTopping": "Mushrooms",
      "hasCrust": "WheatCrust"
    },
    {
      "@id": "Custom",
      "@type": "PizzaConfig",
      "label": {
        "@value": "Custom Configuration",
        "@language": "en"
      },
      "comment": {
        "@value": "A custom pizza configuration with parmesan cheese and sausage toppings",
        "@language": "en"
      },
      "hasCheeseTopping": "Parmesan",
      "hasMeatTopping": "Sausage"
    },
    {
      "@id": "Medium",
      "@type": "PizzaSize",
      "label": {
        "@value": "Medium",
        "@language": "en"
      },
      "comment": {
        "@value": "A medium-sized pizza, typically 12 inches in diameter",
        "@language": "en"
      }
    },
    {
      "@id": "ThinCrust",
      "@type": "PizzaStyle",
      "label": {
        "@value": "Thin Crust",
        "@language": "en"
      },
      "comment": {
        "@value": "A pizza style characterized by a thin, crispy crust base",
        "@language": "en"
      }
    },
    {
      "@id": "Round",
      "@type": "PizzaShape",
      "label": {
        "@value": "Round",
        "@language": "en"
      },
      "comment": {
        "@value": "Traditional circular pizza shape",
        "@language": "en"
      }
    },
    {
      "@id": "Delivered",
      "@type": "PizzaDelivery",
      "label": {
        "@value": "Delivered",
        "@language": "en"
      },
      "comment": {
        "@value": "Pizza delivery method where the pizza is brought to the customer",
        "@language": "en"
      }
    },
    {
      "@id": "Marinara",
      "@type": "SauceTopping",
      "label": {
        "@value": "Marinara",
        "@language": "en"
      },
      "comment": {
        "@value": "Classic Italian tomato-based pizza sauce with herbs and garlic",
        "@language": "en"
      }
    },
    {
      "@id": "Mozzarella",
      "@type": "CheeseTopping",
      "label": {
        "@value": "Mozzarella",
        "@language": "en"
      },
      "comment": {
        "@value": "Traditional Italian cheese, commonly used on pizza, known for its mild flavor and excellent melting properties",
        "@language": "en"
      }
    },
    {
      "@id": "Parmesan",
      "@type": "CheeseTopping",
      "label": {
        "@value": "Parmesan",
        "@language": "en"
      },
      "comment": {
        "@value": "Hard, aged Italian cheese with a sharp, nutty flavor, often grated over pizza",
        "@language": "en"
      }
    },
    {
      "@id": "Pepperoni",
      "@type": "MeatTopping",
      "label": {
        "@value": "Pepperoni",
        "@language": "en"
      },
      "comment": {
        "@value": "Spicy American salami made from cured pork and beef, a popular pizza topping",
        "@language": "en"
      }
    },
    {
      "@id": "Sausage",
      "@type": "MeatTopping",
      "label": {
        "@value": "Sausage",
        "@language": "en"
      },
      "comment": {
        "@value": "Seasoned ground meat (usually pork or beef) formed into small pieces for pizza topping",
        "@language": "en"
      }
    },
    {
      "@id": "Mushrooms",
      "@type": "VegetableTopping",
      "label": {
        "@value": "Mushrooms",
        "@language": "en"
      },
      "comment": {
        "@value": "Sliced fungi, typically button or cremini mushrooms, used as a savory pizza topping",
        "@language": "en"
      }
    },
    {
      "@id": "WheatCrust",
      "@type": "Crust",
      "label": {
        "@value": "Wheat Crust",
        "@language": "en"
      },
      "comment": {
        "@value": "Pizza crust made from wheat flour, providing the base structure of the pizza",
        "@language": "en"
      }
    }
  ]
}
```

At this point, many programmers' eyes light up, because they’re not using RDF but are instead using JSON, which they now know how to work with. Although it is still a little verbose, the code can be parsed cleanly in JavaScript or Python.

They can also opt for GraphQL, which enables the use of JSON and allows them to write information to a graph via a GraphiQL interface. They don’t care about the fact that it is a graph, only that it fits their particular tool chain.

Indeed, you can even encode the same RDF as a diagram, which is just one more representation:

[

![](https://substackcdn.com/image/fetch/$s_!ANBl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc30e7c3-3989-4b2f-94fc-ac59c4490e5f_3840x2735.png)

](https://substackcdn.com/image/fetch/$s_!ANBl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc30e7c3-3989-4b2f-94fc-ac59c4490e5f_3840x2735.png)

And for those who are YAML proponents, there’s even the Manchester notation:

```
Prefix: pz: <https://example.com/ns/pizza#>
Prefix: xsd: <http://www.w3.org/2001/XMLSchema#>
Prefix: rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
Prefix: rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# Pizza Classes
Class: pz:Pizza
Class: pz:PizzaDiv
Class: pz:PizzaConfig
Class: pz:PizzaSize
Class: pz:PizzaStyle
Class: pz:PizzaShape
Class: pz:PizzaDelivery
Class: pz:SauceTopping
Class: pz:CheeseTopping
Class: pz:MeatTopping
Class: pz:VegetableTopping
Class: pz:Crust

# Object Properties
ObjectProperty: pz:hasDivision
ObjectProperty: pz:hasPizzaSize
ObjectProperty: pz:hasPizzaStyle
ObjectProperty: pz:hasPizzaShape
ObjectProperty: pz:hasPizzaDelivery
ObjectProperty: pz:hasConfiguration
ObjectProperty: pz:hasSauce
ObjectProperty: pz:hasCheeseTopping
ObjectProperty: pz:hasMeatTopping
ObjectProperty: pz:hasVegetableTopping
ObjectProperty: pz:hasCrust

# Data Properties
DataProperty: pz:hasLabel

# Individuals

Individual: pz:MyPie1
    Types: pz:Pizza
    Annotations: rdfs:label "My Pie 1"@en,
                rdfs:comment "A specific pizza instance with thin crust, medium size, and mixed toppings"@en
    Facts: pz:hasDivision pz:PizzaDiv,
           pz:hasPizzaSize pz:Medium,
           pz:hasPizzaStyle pz:ThinCrust,
           pz:hasPizzaShape pz:Round,
           pz:hasPizzaDelivery pz:Delivered

Individual: pz:PizzaDiv
    Types: pz:PizzaDiv
    Annotations: rdfs:label "Pizza Division"@en,
                rdfs:comment "A logical division of a pizza that can contain multiple configuration sections"@en
    Facts: pz:hasConfiguration pz:TheSicilian,
           pz:hasConfiguration pz:Custom

Individual: pz:TheSicilian
    Types: pz:PizzaConfig
    Annotations: rdfs:label "The Sicilian"@en,
                rdfs:comment "A traditional Sicilian-style pizza configuration with marinara sauce, mozzarella, pepperoni, mushrooms, and wheat crust"@en
    Facts: pz:hasLabel "Sicilian"^^xsd:string,
           pz:hasSauce pz:Marinara,
           pz:hasCheeseTopping pz:Mozzarella,
           pz:hasMeatTopping pz:Pepperoni,
           pz:hasVegetableTopping pz:Mushrooms,
           pz:hasCrust pz:WheatCrust

Individual: pz:Custom
    Types: pz:PizzaConfig
    Annotations: rdfs:label "Custom Configuration"@en,
                rdfs:comment "A custom pizza configuration with parmesan cheese and sausage toppings"@en
    Facts: pz:hasCheeseTopping pz:Parmesan,
           pz:hasMeatTopping pz:Sausage

Individual: pz:Medium
    Types: pz:PizzaSize
    Annotations: rdfs:label "Medium"@en,
                rdfs:comment "A medium-sized pizza, typically 12 inches in diameter"@en

Individual: pz:ThinCrust
    Types: pz:PizzaStyle
    Annotations: rdfs:label "Thin Crust"@en,
                rdfs:comment "A pizza style characterized by a thin, crispy crust base"@en

Individual: pz:Round
    Types: pz:PizzaShape
    Annotations: rdfs:label "Round"@en,
                rdfs:comment "Traditional circular pizza shape"@en

Individual: pz:Delivered
    Types: pz:PizzaDelivery
    Annotations: rdfs:label "Delivered"@en,
                rdfs:comment "Pizza delivery method where the pizza is brought to the customer"@en

Individual: pz:Marinara
    Types: pz:SauceTopping
    Annotations: rdfs:label "Marinara"@en,
                rdfs:comment "Classic Italian tomato-based pizza sauce with herbs and garlic"@en

Individual: pz:Mozzarella
    Types: pz:CheeseTopping
    Annotations: rdfs:label "Mozzarella"@en,
                rdfs:comment "Traditional Italian cheese, commonly used on pizza, known for its mild flavor and excellent melting properties"@en

Individual: pz:Parmesan
    Types: pz:CheeseTopping
    Annotations: rdfs:label "Parmesan"@en,
                rdfs:comment "Hard, aged Italian cheese with a sharp, nutty flavor, often grated over pizza"@en

Individual: pz:Pepperoni
    Types: pz:MeatTopping
    Annotations: rdfs:label "Pepperoni"@en,
                rdfs:comment "Spicy American salami made from cured pork and beef, a popular pizza topping"@en

Individual: pz:Sausage
    Types: pz:MeatTopping
    Annotations: rdfs:label "Sausage"@en,
                rdfs:comment "Seasoned ground meat (usually pork or beef) formed into small pieces for pizza topping"@en

Individual: pz:Mushrooms
    Types: pz:VegetableTopping
    Annotations: rdfs:label "Mushrooms"@en,
                rdfs:comment "Sliced fungi, typically button or cremini mushrooms, used as a savory pizza topping"@en

Individual: pz:WheatCrust
    Types: pz:Crust
    Annotations: rdfs:label "Wheat Crust"@en,
                rdfs:comment "Pizza crust made from wheat flour, providing the base structure of the pizza"@en
```

However, in all cases, these are _different equivalent representations of the exact same thing_. RDF is simply an abstraction, a way of articulating graphs. It still uses namespaces, because namespaces are ways of organizing related information into a single package, just as libraries are used in more tr,aditional programming environments, but for the most part if you have any representation of RDF, then you have every representation of RDF.

## RDF Documents

Part of what makes RDF so incomprehensible is the fact that when people encounter it in the world, the RDF in most representations is normalised. In relational database terms, this means that everything has been broken down into distinct tables, with primary keys providing identifiers to a given row in any table representing an entity, and foreign keys then being the link to the primary key of a different row in a different (usually) table.

Documents, on the other hand, are typically normalized, acting as containers. For instance, the same pizza structure as given above, previously proken into classes, can also be normalized to an implicit structure (here in Turtle):

```
@prefix pz: <https://example.com/ns/pizza#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# Pizza instance with embedded division and configurations
pz:MyPie1 rdf:type pz:Pizza ;
    rdfs:label "My Pie 1"@en ;
    rdfs:comment "A specific pizza instance with thin crust, medium size, and mixed toppings"@en ;
    pz:hasDivision [
        rdf:type pz:PizzaDiv ;
        rdfs:label "Pizza Division"@en ;
        rdfs:comment "A logical division of a pizza that can contain multiple configuration sections"@en ;
        pz:hasConfiguration [
            rdf:type pz:PizzaConfig ;
            rdfs:label "The Sicilian"@en ;
            rdfs:comment "A traditional Sicilian-style pizza configuration with marinara sauce, mozzarella, pepperoni, mushrooms, and wheat crust"@en ;
            pz:hasLabel "Sicilian"^^xsd:string ;
            pz:hasSauce [
                rdf:type pz:SauceTopping ;
                rdfs:label "Marinara"@en ;
                rdfs:comment "Classic Italian tomato-based pizza sauce with herbs and garlic"@en
            ] ;
            pz:hasCheeseTopping [
                rdf:type pz:CheeseTopping ;
                rdfs:label "Mozzarella"@en ;
                rdfs:comment "Traditional Italian cheese, commonly used on pizza, known for its mild flavor and excellent melting properties"@en
            ] ;
            pz:hasMeatTopping [
                rdf:type pz:MeatTopping ;
                rdfs:label "Pepperoni"@en ;
                rdfs:comment "Spicy American salami made from cured pork and beef, a popular pizza topping"@en
            ] ;
            pz:hasVegetableTopping [
                rdf:type pz:VegetableTopping ;
                rdfs:label "Mushrooms"@en ;
                rdfs:comment "Sliced fungi, typically button or cremini mushrooms, used as a savory pizza topping"@en
            ] ;
            pz:hasCrust [
                rdf:type pz:Crust ;
                rdfs:label "Wheat Crust"@en ;
                rdfs:comment "Pizza crust made from wheat flour, providing the base structure of the pizza"@en
            ]
        ] ,
        [
            rdf:type pz:PizzaConfig ;
            rdfs:label "Custom Configuration"@en ;
            rdfs:comment "A custom pizza configuration with parmesan cheese and sausage toppings"@en ;
            pz:hasCheeseTopping [
                rdf:type pz:CheeseTopping ;
                rdfs:label "Parmesan"@en ;
                rdfs:comment "Hard, aged Italian cheese with a sharp, nutty flavor, often grated over pizza"@en
            ] ;
            pz:hasMeatTopping [
                rdf:type pz:MeatTopping ;
                rdfs:label "Sausage"@en ;
                rdfs:comment "Seasoned ground meat (usually pork or beef) formed into small pieces for pizza topping"@en
            ]
        ]
    ] ;
    pz:hasPizzaSize [
        rdf:type pz:PizzaSize ;
        rdfs:label "Medium"@en ;
        rdfs:comment "A medium-sized pizza, typically 12 inches in diameter"@en
    ] ;
    pz:hasPizzaStyle [
        rdf:type pz:PizzaStyle ;
        rdfs:label "Thin Crust"@en ;
        rdfs:comment "A pizza style characterized by a thin, crispy crust base"@en
    ] ;
    pz:hasPizzaShape [
        rdf:type pz:PizzaShape ;
        rdfs:label "Round"@en ;
        rdfs:comment "Traditional circular pizza shape"@en
    ] ;
    pz:hasPizzaDelivery [
        rdf:type pz:PizzaDelivery ;
        rdfs:label "Delivered"@en ;
        rdfs:comment "Pizza delivery method where the pizza is brought to the customer"@en
    ] .
```

The use of blank node notation here is not that dissimilar to the use of dictionaries as a grouping mechanism, with each blank node in turn having a local IRI that is implicitly defined by the graph itself. This is essentially equivalent to the JSON-LD compact denormalized form:

```
{
  "@context": {
    "@vocab": "https://example.com/ns/pizza#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "label": "rdfs:label",
    "comment": "rdfs:comment"
  },
  "@id": "MyPie1",
  "@type": "Pizza",
  "label": "My Pie 1",
  "@language": "en",
  "comment": "A specific pizza instance with thin crust, medium size, and mixed toppings",
  "hasDivision": {
    "@type": "PizzaDiv",
    "label": "Pizza Division",
    "comment": "A logical division of a pizza that can contain multiple configuration sections",
    "hasConfiguration": [
      {
        "@type": "PizzaConfig",
        "label": "The Sicilian",
        "comment": "A traditional Sicilian-style pizza configuration with marinara sauce, mozzarella, pepperoni, mushrooms, and wheat crust",
        "hasSauce": {
          "@type": "SauceTopping",
          "label": "Marinara",
          "comment": "Classic Italian tomato-based pizza sauce with herbs and garlic"
        },
        "hasCheeseTopping": {
          "@type": "CheeseTopping",
          "label": "Mozzarella",
          "comment": "Traditional Italian cheese, commonly used on pizza, known for its mild flavor and excellent melting properties"
        },
        "hasMeatTopping": {
          "@type": "MeatTopping",
          "label": "Pepperoni",
          "comment": "Spicy American salami made from cured pork and beef, a popular pizza topping"
        },
        "hasVegetableTopping": {
          "@type": "VegetableTopping",
          "label": "Mushrooms",
          "comment": "Sliced fungi, typically button or cremini mushrooms, used as a savory pizza topping"
        },
        "hasCrust": {
          "@type": "Crust",
          "label": "Wheat Crust",
          "comment": "Pizza crust made from wheat flour, providing the base structure of the pizza"
        }
      },
      {
        "@type": "PizzaConfig",
        "label": "Custom Configuration",
        "comment": "A custom pizza configuration with parmesan cheese and sausage toppings",
        "hasCheeseTopping": {
          "@type": "CheeseTopping",
          "label": "Parmesan",
          "comment": "Hard, aged Italian cheese with a sharp, nutty flavor, often grated over pizza"
        },
        "hasMeatTopping": {
          "@type": "MeatTopping",
          "label": "Sausage",
          "comment": "Seasoned ground meat (usually pork or beef) formed into small pieces for pizza topping"
        }
      }
    ]
  },
  "hasPizzaSize": {
    "@type": "PizzaSize",
    "label": "Medium",
    "comment": "A medium-sized pizza, typically 12 inches in diameter"
  },
  "hasPizzaStyle": {
    "@type": "PizzaStyle",
    "label": "Thin Crust",
    "comment": "A pizza style characterized by a thin, crispy crust base"
  },
  "hasPizzaShape": {
    "@type": "PizzaShape",
    "label": "Round",
    "comment": "Traditional circular pizza shape"
  },
  "hasPizzaDelivery": {
    "@type": "PizzaDelivery",
    "label": "Delivered",
    "comment": "Pizza delivery method where the pizza is brought to the customer"
  }
}
```

The denormalized form is significant in both cases because it replaces global named identifiers (IRIs) with local blank node identifiers. In effect, this means that the only thing that has a referenceable identifier is the document root <`https://example.com/ns/pizza#myPie1>.` The _**shape**_ or underlying structure, remains the same (a SPARQL query, for instance, will work regardess of whether IRIs or blank nodes are used), it’s just that the specific identifiers for components are no longer directly referenceable - they can only be referenced by providing a property path.

Direction matters when determining properties; in a document-centric denormalized view, for instance, you generally want your properties to go from a single concept root (such as `pz:MyPie1`) out along the properties to new objects until you eventually reach the end of property paths. There are exceptions - it is possible in a graph to create a loop, for instance - but in practice it’s rare for that to happen; the overwhelming number of cases will create trees, even if a given node is shared between two or more objects. For instance, in the above denormalized case, I can do a path query that will retrieve all of the meat toppings on a pizza by using a property path that looks like:

```
{root}/pz:hasDivision/pz:hasConfiguration/pz:hasMeatTopping
```

This would retrieve a set of meat toppings (here in JSON):

```
[{
    "@id":"_:MeatTopping_Pepperoni",
    "@type": "MeatTopping",
    "label": "Pepperoni",
    "comment": "Spicy American salami made from cured pork and beef, a popular pizza topping"
},{
    "@id":"_:MeatTopping_Sausage",
    "@type": "MeatTopping",
    "label": "Sausage",
    "comment": "Seasoned ground meat (usually pork or beef) formed into small pieces for pizza topping"
  }
]
```

where the @id here is a local identifier that will likely be generated from the data store, but that is given the blank node identifier of something like

```
  _:MeatTopping_Pepperoni
```

to indicate that the exact identifier is locally defined. In other words, this value might more likely like something like:

```
https://example.com/genid/a5e4c112319a33186cedefa
```

These special purpose identifiers are known as Skolem IRIs and are usually system specific; a parser will treat them as blank nodes.

Those of you familiar with XML may recognize some similarity between RDF property nodes and XPath, the language for using document property paths to retrieve sets of nodes. Indeed, though there currently isn’t such a specification (property paths are being considered as part of of SPARQL 1.2), you could specify a turtle property path using blank node expressions to retrieve only those meats that are available on the Sicilian half (division) of the pizza.

```
{root}/pz:hasDivision/pz:hasConfiguration[pz:label "Sicilian"]/pz:hasMeatTopping
```

This congruency between graphs and documents is important, but it also challenges some long-held notions in modelling, one of the biggest of which being that it doesn’t really matter which direction a link (or predicate is set). If you work on the assumption that a top-down approach with a document-centric model is important, then this needs to be maintained consistently within the model.

In essence, you want predicates defined in such a way that they naturally create documents, and the boundaries (leaves) of that document are the point at which there are no more outgoing connections for any given node within that tree. A simple example of this is where you have a book that has a color cover, and a taxonomy that identifies the potential colors:

[

![](https://substackcdn.com/image/fetch/$s_!XJeE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42c4e52b-4edf-49fd-8bbd-447bcb290ab8_3840x2923.png)

](https://substackcdn.com/image/fetch/$s_!XJeE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42c4e52b-4edf-49fd-8bbd-447bcb290ab8_3840x2923.png)

There are in effect two “documents” here, the first consisting of an entity (book) that incorporates a cover color, the second the taxonomy of color terms for that book cover. They overlap in part on the facets themselves, but its worth noting that while the Green facet is part of the book “tree”, the Red facet is not. If, from a given object node, you followed all outbound predicates, you will get a distinct tree for that object even if assets are shared. Thus model direction matters significantly.

## RDF DOMs and SHACL Shapes

This notion of RDF documents is important, because it runs somewhat counter to the perception of RDF as simply a set of assertions. In essence, once you start thinking structurally about documents as data shapes, it becomes easier to be able to visualize content - and to determine the boundaries of that content.

A data document is an example of a **Document Object Model** (or DOM). HTML is one of the earliest examples of a document object model, though it can be argued that SGML (the Structured Generalised Markup Language), which preceded it, was a tool for creating DOMs. A **DOM Document** is an instance (or example) of a DOM that follows a set of specific rules, usually known as a schema.

A DOM Document has a number of characteristics.

-   **Hierarchical.** A DOM Document is typically a tree, meaning that there is some form of root node that identifies the character of that tree.
    
-   **Heterogenous.** The nodes of a DOM Document have a variety of types, depending on the functions required. For instance, in HTML, you have a Head and Body object, each of which holds different kinds of elements.
    
-   The **Element name** (specifically, it’s qualified name) is the equivalent of a predicate in RDF. This may seem a little counterintuitive, and has more to do with the fact that HTML was the first significant DOM language and predated XML by nearly a decade.
    
-   **Narrative ordering.** HTML carried with it an implicit ordering because of its origins as a markup language, and this carried through into the general principle of DOMs. What this means is that the order of nodes within a DOM do matter. RDF by itself has a couple of mechanisms to facilitate this, but they necessitate working either with linked lists or numbered rdf nodes, neither of which are ideal.
    
-   **Text Nodes.** A text node is a container for text, and (more or less) corresponds to a literal.
    
-   **Attributes.** An HTML or XML attribute is placed on an element and effectively describes some characteristic of that element that is specific to the combination of subject, element property and value. In RDF terms, an attribute is a pure blank node with literal properties.
    

### Narrative Ordering

There’s a lot to parse and unpack here. The first point that really needs to be explained is _narrative ordering_. In theory, most data properties do not have an explicit order. In practice, however, a data structure can be thought of as a very terse story - you tend to put the declarations and definitions at the beginning, focus on the big “story” associated with a particular thing, then put less important information farther down.

As important, most data structures can be thought of as processing stacks - you process higher order structures first, then do a deep dive (pushing the state onto the stack) until you can complete it, at which point, you pop the resulting structure off the stack and go to a higher level of abstraction. Such stack processing may, in fact, be a key to cognitive computing and is just as relevant with knowledge graph structures as it is with LLMs.

RDF has two ways of creating ordering. The first is to use rdf:N entries, where N is a number:

```
ex:Items rdf:1 ex:Item1; rdf:2 ex:Item2 ; rdf:3 ex:Item3 .
```

This works when the number of items is small, but it requires some specialized handling when numbers get beyond ten or so and requires a certain level of inheritance to be present.

The other form is to use _**linked lists**_. A linked list is more or less the equivalent of an array in a programming language. It is a structure rather than a property, and it has always been an uncomfortable fit within OWL, though it actually works rather nicely with SHACL. This may actually be due to the fact that as RDF has moved increasingly towards SPARQL/Turtle, the notation for specific structures in Turtle has also become more abstract.

A sequence using a linked list is depicted in Turtle as an expression of space separated items within a set of parentheses:

```
ex:Items ex:hasList (ex:Item1 ex:Item2 ex:Item3) .
```

This may seem like a trivial change, but it can be interpreted as ex:Items has an ordered list with itsems, ex:Item1, ex:Item2, and ex:Item3 respectively. An HTML document can be rendered using this capability, along with blank nodes:

```
# Turtle
@prefix h: <http://www.w3.org/1999/xhtml> .
@prefix ex: <http://example.com/> .

ex:MyWebPage a h:Html;
    h:contains (
        [a h:Head;
         h:contains (
             [a h:Link; h:href "myExternalFile.css"; h:rel "stylesheet"]
             [a h:Title; h:textContent "My Web Page"]
             )]
        [a h:Body;
         h:contains (
             [a h:Article;
              h:contains (
                 [a h:H1; h:textContent "This is My Web Page"]
                 [a h:Para; h:contains (
                      [a h:Text; h:textContent "This is a "]
                      [a h:Emphasis; h:textContent "test"]
                      [a h:Text; h:textContent ". This is only a "]
                      [a h:Emphasis; h:textContent "test"]
                 )]
                 [a h:Ul;
                  h:contains (
                      [a h:Li; h:textContent "Item 1"]
                      [a h:Li; h:textContent "Item 2"]
                      [a h:Li; h:textContent "Item 3"]
                     )] 
              )]
         )]
    ) .
```

Now, this probably does not look like RDF (or Turtle) at first glance, but it is in fact syntactically correct. If you normalise it by introducing named blank nodes, incorporating the Turtle () notation, and add in type declarations, this is equivalent to:

```
# NORMALIZED RDF STRUCTURE WITH COLLECTIONS IN TURTLE
# This demonstrates proper normalization with:
# - Named blank nodes (no anonymous [] nodes)
# - Explicit collection syntax using ()
# - Clear hierarchical containment relationships
# - Consistent property usage

@prefix h: <http://www.w3.org/1999/xhtml> .
@prefix ex: <http://example.com/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

# NORMALIZED STRUCTURE: Main webpage resource with explicit type and collection
ex:MyWebPage 
    rdf:type h:Html ;
    h:contains ( _:head _:body ) .

# NORMALIZED HEAD SECTION: Named blank node with collection of children
_:head 
    rdf:type h:Head ;
    h:contains ( _:link _:title ) .

# NORMALIZED HEAD CHILDREN: Explicitly named elements with properties
_:link 
    rdf:type h:Link ;
    h:href "myExternalFile.css" ;
    h:rel "stylesheet" .

_:title 
    rdf:type h:Title ;
    h:textContent "My Web Page" .

# NORMALIZED BODY SECTION: Named blank node with collection 
_:body 
    rdf:type h:Body ;
    h:contains ( _:article ) .

# NORMALIZED ARTICLE SECTION: Named blank node with collection of children
_:article 
    rdf:type h:Article ;
    h:contains ( _:h1 _:ul ) .

# NORMALIZED ARTICLE CHILDREN: Explicitly named elements
_:h1 
    rdf:type h:H1 ;
    h:textContent "This is My Web Page" .

# NORMALIZED LIST SECTION: Named blank node with collection of list items
_:ul 
    rdf:type h:Ul ;
    h:contains ( _:li1 _:li2 _:li3 ) .

# NORMALIZED LIST ITEMS: Each item explicitly named and typed
_:li1 
    rdf:type h:Li ;
    h:textContent "Item 1" .

_:li2 
    rdf:type h:Li ;
    h:textContent "Item 2" .

_:li3 
    rdf:type h:Li ;
    h:textContent "Item 3" .

# NORMALIZATION VERIFICATION:
# ✓ All blank nodes have explicit names (_:head, _:body, etc.)
# ✓ All types are explicitly declared with rdf:type (can be replaced with 'a')
# ✓ Collections use proper Turtle () syntax
# ✓ No anonymous [] blank nodes remain
# ✓ Hierarchical structure is preserved and clear
# ✓ All properties are consistently named and typed
```

Most of the logic here is handled via two explicit properties - h:contains and h:textContent. The h:contains property indicates that the object (either a single node or a linked list of nodes) is contained within the element in question. The important thing here is that the h:contains property can assume a linked list structure. This can be seen in a SHACL declaration for the property:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix h: <http://www.w3.org/1999/xhtml> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

_:containsPropertyShape a sh:PropertyShape ;
    sh:path h:contains ;
    sh:or (
        [ 
            # Singleton: single HTML element
            sh:class h:Element 
            sh:minOccurs 1;
            sh:maxOccurs 1 ;
        ]
        [ 
            # Linked list: RDF list containing HTML elements
            sh:class rdf:List ;
            sh:property [
                sh:path rdf:rest*/rdf:first ;
                sh:class h:Element
            ] ;
        ]
    ) .
```

This also assumes that all of html classes are subclasses of h:Element. Note the path for rdf:List - `rdf:rest*/rdf:first`. The `sh:or` expression serves to indicate that the value (the object) will either be an item of class Element (or some subclass) or the secondary path will be a linked list as indicated by the rdf:rest/rdf:first structure.

The text content, in turn, indicated by `h:textContent` will typically be a literal value. If there is no inline content (such as a bold or italic indicator) then text content will be just the literal value, otherwise, the h:Text element will be used to hold content around the entity and the markup element will be part of a sequence. For instance:

```
... [a h:Para; h:contains (
       [a h:Text; h:textContent "This is a "]
       [a h:Emphasis; h:textContent "test"]
       [a h:Text; h:textContent ". This is only a "]
       [a h:Emphasis; h:textContent "test"]
    )]
...
```

The total RDF can be readily converted to HTML, in this case by following transitive closure on `h:contains`.

```
<!DOCTYPE html>
<html>
<head>
    <link href="myExternalFile.css" rel="stylesheet">
    <title>My Web Page</title>
</head>
<body>
    <article>
        <h1>This is My Web Page</h1>
        <p>This is a <b>Test</b>. This is only a <b>Test</b>.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
            <li>Item 3</li>
        </ul>
    </article>
</body>
</html>
```

So how does this conversion occur? That is a discussion for the next post.

### OntoHTML and More

**One final note:** Flores Bakker, who works as an ontologist for the Dutch government, has worked extensively developing [RDF as documents (https://github.com/floresbakker/](https://github.com/floresbakker/)). His approach is a bit different (he uses rdf:NNN type notation for ordering), but he has built detailed RDF document versions for HTML, SVG, JavaScript, Archimate and other common document and language standards (far beyond what I’ve covered here) and should definitely be explored in depth by anyone interested in this topic.

## Summary

Overall, documents can be readily decomposed into outlines at various levels that effectively create a narrative flow. This provides a powerful layer for modeling - in essence, rather than trying to use a “traditional” ontological breakdown, you can decompose information in such a way that it tells a story, one that works both for attempting to get detailed information from a knowledge graph but also one that establishes a powerful paradigm for graph embeddings within large language models. It has the added benefit of keeping context close, and consequently reducing the space that attention seeking mechanisms need to span to get relevant content.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!0RPf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ac5ba56-95e5-4624-b4cc-bb6bdd39d2be_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!0RPf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ac5ba56-95e5-4624-b4cc-bb6bdd39d2be_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

Also, I am currently looking for new projects or work. If anyone is looking for a CTO or Director level AI/Ontologist, please contact me through my calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.

