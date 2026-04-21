---
title: "SHACL Taxonomy Revisited"
source: "https://ontologist.substack.com/p/shacl-taxonomy-revisited?utm_source=profile&utm_medium=reader2"
date: "Mar 8"
tags: [article]
---

I’ve talked a lot about knowledge graphs, and ontologies in particular, in this column, but I haven’t spent as much time talking about taxonomies. However, understanding the distinction (and especially how these play into SHACL) can make it far easier to design effective knowledge graphs.

When working with knowledge graphs, it’s easy to get overwhelmed by the complexity. However, at a core level, a knowledge graph can be broken down into a few key (albeit somewhat overlapping) sections:

-   The **ontology** (the underlying structure, which you can think of as the _**shape**_ of the knowledge graph).
    
-   The **taxonomy** (the classifications used to _**organise**_ information into different conceptual knowledge systems).
    
-   The **instance data** consists of models of individual _**items**_ that use both the ontology to shape and the taxonomy to classify different facets of those items.
    
-   **Annotations** (often described via reifications) that indicate the _**events**_ that the properties of an object participate in or that provide an external description or comments about the items.
    

-   **Operational content** can be thought of as both configuration code and the set of queries that are used to access the knowledge graph. This also includes external ontologies such as OWL or SHACL.
    

What is most noteworthy here is that there is a distinction between the top three, and how they are handled, and even defined, varies significantly from one another.

Taxonomies can, at their core, be considered lists of concepts or categories, whereas instance data are lists of things. This is a subtle but important distinction, and one that is not always easy to tell apart. This gets down to some basic grammar, specifically the use of nouns and adjectives. A noun is typically a thing or some assemblage of things (such as a person, a government, a place, a book). What’s most notable about things is that they are generally unique.

An adjective, on the other hand, is qualitative or descriptive, providing characterisations about nouns that help to differentiate one particular set of items from others. We talk about tall people, green books, and fast cars. Each of these terms (_tall_, _green_, _fast_) in terms is a state that a given property (or facet) can take, here _height, colour, speed_. The noun in this case is a set of individuals, while each facet determines a particular characteristic or classification of that individual in some way.

Such facets and their corresponding concepts make up the bulk of taxonomies. In OWL, these are referred to as individuals, with the set of related individuals called an enumeration. in SKOS, each group or set is known as a concept scheme with each individual value known as a concept. In XSD, these same concepts are called enumeration values, with the sets of related enumerations called an enumeration type. In data modeling, the variable (such as color) is often referred to as a facet, while the specific instance of that value (such as green) is referred to as the facet value.

[

![](https://substackcdn.com/image/fetch/$s_!xehZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbabbe78c-a419-4782-9ca4-53ce818479c9_1494x2078.png)

](https://substackcdn.com/image/fetch/$s_!xehZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbabbe78c-a419-4782-9ca4-53ce818479c9_1494x2078.png)

This diversity of terms derives from the fact that different domains of interest have typically had to describe the same fundamental concept (a finite and relatively small set of related classes) in different ways.

What makes this complicated is that RDFS treats everything as classes, but in many respects this tends to overload what should be two (or even three) different kinds of relationships as a single `rdf:type`. Indeed, if you assume that a facet “group” is itself a conceptual facet, (in effect, what happens with `skos:concept`), then you eliminate the need to create an “overseer” class and can just use the facets as the cornerstone for a taxonomy.

## Creating a SHACL Taxonomy Term Shape

Shapes are more generalised than classes, allowing for some interesting applications when finding a good balance for modelling various concepts within taxonomies.

SKOS, or the Simple Knowledge Ontology System, is a taxonomy system that was first formalised in 2003, shortly after RDF became a standard. It has a number of features that make it suitable for the kind of taxonomies discussed above, but it is also a fixed standard that could use additional enhancements. To illustrate alternatives that nonetheless share many of the same characteristics, I’ll create a new namespace called tax: that illustrates a generalised structure for a taxonomy language. The following is a sample showing a simple colour taxonomy.

```
# Define the Comprehensive Color Taxonomy
color:ColorTaxonomy
    a tax:Taxonomy ;
    tax:identifier "COMPREHENSIVE_COLOR_SYSTEM" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Comprehensive Color Classification System"@en ;
    tax:alternativeLabel "Advanced Color Taxonomy"@en, "Système de Classification Chromatique"@fr, "Sistema de Clasificación de Colores"@es, "Umfassendes Farbklassifikationssystem"@de ;
    tax:acronym "CCCS" ;
    tax:description "Complete hierarchical organization of colors including primary, secondary, tertiary, neutral, warm, cool, and specialized color categories with international naming conventions"@en ;
    tax:version "2.0" .

# Level 0 - Major Color Categories
color:PRIMARY_COLORS
    a tax:Node ;
    tax:identifier "PRIMARY_COLORS" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Primary Colors"@en ;
    tax:alternativeLabel "Base Colors"@en, "Fundamental Colors"@en, "Couleurs Primaires"@fr, "Colores Primarios"@es, "Grundfarben"@de, "Colori Primari"@it, "Cores Primárias"@pt ;
    tax:synonym "Elementary Colors"@en, "Pure Colors"@en, "Couleurs Pures"@fr ;
    tax:acronym "PC" ;
    tax:antonym color:NEUTRAL_COLORS ;
    tax:description "Base colors that cannot be created by mixing other colors in traditional color theory"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:level 0 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

# Level 1 - Secondary Colors
color:GREEN
    a tax:Node ;
    tax:identifier "GREEN" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Green"@en ;
    tax:alternativeLabel "Vert"@fr, "Verde"@es, "Grün"@de, "Verde"@it, "Verde"@pt ;
    tax:synonym "Jade"@en, "Emerald Green"@en, "Vert Émeraude"@fr, "Verde Esmeralda"@es ;
    tax:antonym color:RED ;
    tax:description "Secondary color created by mixing blue and yellow, symbol of nature and growth"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:SECONDARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

# Level 2 - Shades of Color
color:EMERALD
    a tax:Node ;
    tax:identifier "EMERALD" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Emerald"@en ;
    tax:alternativeLabel "Emerald Green"@en, "Jewel Green"@en, "Vert Émeraude"@fr, "Verde Esmeralda"@es, "Smaragdgrün"@de, "Verde Smeraldo"@it ;
    tax:synonym "Brilliant Green"@en, "Gem Green"@en, "Vert Brillant"@fr ;
    tax:description "Vivid green with blue undertones, precious and luxurious"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:GREEN ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .
```

A more robust example of the taxonomy can be seen below :[1](https://substack.com/@kurtcagle/p-189271561#footnote-1-173117561)

This particular taxonomy can be illustrated via a mermaid diagram:

[

![](https://substackcdn.com/image/fetch/$s_!2lEi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbeb2f3c8-1934-4c3a-96c3-77328700b80a_3209x3840.png)

](https://substackcdn.com/image/fetch/$s_!2lEi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbeb2f3c8-1934-4c3a-96c3-77328700b80a_3209x3840.png)

Each entry has roughly the same properties, which are in many cases analogous to SKOS properties. For instance, the color “Emerald Green” can be rendered as follows:

```
color:EMERALD
    a tax:Node ;
    tax:identifier "EMERALD" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Emerald"@en ;
    tax:alternativeLabel "Emerald Green"@en, "Jewel Green"@en, "Vert Émeraude"@fr, "Verde Esmeralda"@es, "Smaragdgrün"@de, "Verde Smeraldo"@it ;
    tax:synonym "Brilliant Green"@en, "Gem Green"@en, "Vert Brillant"@fr ;
    tax:description "Vivid green with blue undertones, precious and luxurious"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:GREEN ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .
```

There are a few properties that are distinct from SKOS however:

-   **tax:level**. This indicates the distance of the given node from its root concept ( indicated by `tax:belongsToTaxonomy`). This makes it possible to determine the level of specificity of the taxonomy, rather than attempting to compute this on the fly (for instance, tax:level 0 would be Secondary Colours, tax:level 1 would be Green, and tax:level 2 would be Emerald Green).
    
-   **tax:status.** This is used to indicate whether the node in question is active or deprecated.
    
-   **tax:sortOrder.** This is used both to indicate a fixed ordering of child nodes for a given parent node, as well as a way to create an associated weight for a term (the sortOrder / the total number of siblings for that parent).
    
-   **tax:antonym.** This, in general, indicates an opposition to the term in question. For instance, the opposite of red will typically be its complementary colour, green. Note that with respect to colours, this is subject to a certain degree of interpretation.
    
-   **tax:defaultLanguage.** This is typically used to indicate the language used for interfaces if not otherwise specified.
    

The sort order and taxonomy levels provide a way to provide distance and weighting within the taxonomy, which makes them especially useful for mapping to neural network features. For instance, there are four shades of green from emerald green (with a sort order of 1) to olive green (with a sort order of 4). This means that you can create a “green feature” for forest green (3) with a weight of 0.75 (3/4).

Suppose you had the above taxonomy for cars (the Car shape) and wanted to create a specific constraint that the car had an exterior colour from a level two colour, such as emerald green. Such a usage might be part of a car declaration, such as:

```
car:Vehicle2024_001
    a car:Vehicle ;
    car:vin "1HGBH41JXMN109186" ;
    car:make "Honda" ;
    car:model "Civic" ;
    car:year 2024 ;
    car:hasExteriorColor color:EMERALD . #Here's the exterior color
```

The specific definition for the property shape car:hasExteriorColor would then look like the following (with the added constraint that it must be from one of four primary colour blocks of red, blue, green or grey):

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix car: <http://example.org/automotive#> .
@prefix tax: <http://example.org/taxonomy#> .
@prefix color: <http://example.org/color#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dash: <http://datashapes.org/dash#> .

# Car Shape with Exterior Color Property
:CarShape
    a sh:NodeShape ;
    sh:targetClass car:Vehicle ;
    sh:name "carShape" ;
    sh:label "Automotive Vehicle Validation Shape" ;
    sh:description "Validates properties of automotive vehicles including color specifications" ;
    
    sh:property [
        sh:name "exteriorColor" ;
        sh:label "Exterior Color Property" ;
        sh:description "Validates that exterior color references a specific level 2 color from the color taxonomy" ;
        sh:path car:hasExteriorColor ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:class tax:Node ;
        sh:message "Exterior color must reference exactly one level 2 color node from the color taxonomy" ;
        
        # Constraint to ensure it's a level 2 color
        sh:sparql [
            sh:name "exteriorColorLevelConstraint" ;
            sh:label "Exterior Color Level Constraint" ;
            sh:description "Ensures exterior color is a level 2 color from the active color taxonomy" ;
            sh:message "Exterior color must be a level 2 color (specific shade) from the color taxonomy" ;
            sh:select """
                SELECT $this WHERE {
                    $this car:hasExteriorColor ?color .
                    FILTER NOT EXISTS {
                        ?color tax:level 2 ;
                               tax:status "ACTIVE" ;
                               tax:belongsToTaxonomy color:ColorTaxonomy .
                    }
                }
            """
        ] ;
        
        # Additional constraint to ensure color is from approved categories
        sh:sparql [
            sh:name "exteriorColorCategoryConstraint" ;
            sh:label "Exterior Color Category Constraint" ;
            sh:description "Ensures exterior color belongs to an approved parent color category" ;
            sh:message "Exterior color must belong to Red, Blue, Green, or Gray color families" ;
            sh:select """
                SELECT $this WHERE {
                    $this car:hasExteriorColor ?color .
                    ?color tax:level 2 ;
                           tax:parentNode ?parentColor .
                    FILTER NOT EXISTS {
                        ?parentColor tax:identifier ?parentId .
                        FILTER(?parentId IN ("RED", "BLUE", "GREEN", "GRAY"))
                    }
                }
            """
        ]
    ] ;
```

The property first identifies that the property will be of type `tax:Node` , which doesn’t necessarily tell you a lot, but does indicate that the property should be a taxonomy node. This is actually pretty useful, because it segregates your knowledge graph into either entities (such as cars) or taxonomy terms (colours).

The second part of the `Car:hasExteriorColor` Property, however, provides a more nuanced definition by establishing two distinct constraints, which are specified as SPARQL constraints. The first constraint identifies that the colour must be from the set of _shades_ (aka level two colours), while the second limits those to shades within the RED, BLUE, GREEN or GRAY level 1 colours (in other words, no orange or purple cars here).

Significantly, each of these provides secondary messages that can be used both for validation and for documentation (as these messages essentially correspond to MUST, SHOULD, or CAN have clauses within a requirements document. Put another way:

> You can think of a SHACL graph as being the encoding of a requirements specification document.

One additional consequence of this structure is that taxonomies themselves can be seen not as one giant hierarchy, but rather a collection of independent collections of concepts, such as roles (various job titles), types (engine type, for instance), geofeatures (rivers, countries, cities, continents, etc.), genera (cats, dogs, gerbils) and similar breakdowns. Such taxonomy terms may have additional properties - units provide a good example of this - but the core terms remain the same.

The full taxonomy schema is quite extensive, but it should be noted that it is also mostly straightforward. For instance, the property shape for the path `tax:synonym` provides a fair amount of metadata for that particular predicate, metadata that often tends to get lost in OWL models:

```
    sh:property [
        sh:name "synonyms" ;
        dash:label "Synonyms Property" ;
        sh:description "Validates synonymous terms that have equivalent meaning to the primary label" ;
        sh:path tax:synonym ;
        sh:nodeKind sh:Literal ;
        sh:datatype rdf:langString ;
        sh:maxLength 100 ;
        sh:message "Synonyms are terms with equivalent meaning with language tags (max 100 characters each)" ;
        dash:analog skos:altLabel
    ] ;
```

The `dash:label` and `sh:description` properties obviously provide a way of identifying the properties (`dash:label` will likely become s`h:label` at some point, as the semantics for `sh:name` seem increasingly to use it as a variable or programmatic name. Additionally, synonyms are restricted to being of a certain length, which may be a constraint requirement for their inclusion in relational database fields.

The `dash:analog` property is worth especially noting here. An **analog** property is a property in a different namespace that serves a similar function to the indicated property, albeit not necessarily in an identical manner. The `tax:synonym` properties and the `skos:altLabel` properties, for instance, both obviously serve similar purposes in their respective ontologies, even if the way that they do it may vary somewhat. Analogs are useful primarily in intelligent systems where there is a clear transformation from one ontological property in one system to the analog in another. This can make for far more targeted mappings.

## Summary

This document is not a formal proposal for a taxonomy system; instead, it illustrates how to define taxonomy systems that integrate well with SHACL. Taxonomies play a very important role in knowledge graphs - they help to qualify (and to some extent quantify) the properties of entities, and as such can be seen as intermediate objects. All concepts are tax:Node terms in this particular view, making it easier to write queries for searching the taxonomy space. It should be noted that taxonomies are not SHACL, but they weave through SHACL definitions, providing context, flavour, and classification to your data.

In Media Res,

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please contact me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please consider contributing something to support my work, allowing me to continue writing.

[1](https://substack.com/@kurtcagle/p-189271561#footnote-anchor-1-173117561)

A more extensive colors taxonomy:

```
@prefix tax: <http://example.org/taxonomy#> .
@prefix color: <http://example.org/color#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

# Define the Comprehensive Color Taxonomy
color:ColorTaxonomy
    a tax:Taxonomy ;
    tax:identifier "COMPREHENSIVE_COLOR_SYSTEM" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Comprehensive Color Classification System"@en ;
    tax:alternativeLabel "Advanced Color Taxonomy"@en, "Système de Classification Chromatique"@fr, "Sistema de Clasificación de Colores"@es, "Umfassendes Farbklassifikationssystem"@de ;
    tax:acronym "CCCS" ;
    tax:description "Complete hierarchical organization of colors including primary, secondary, tertiary, neutral, warm, cool, and specialized color categories with international naming conventions"@en ;
    tax:version "2.0" .

# Level 0 - Major Color Categories
color:PRIMARY_COLORS
    a tax:Node ;
    tax:identifier "PRIMARY_COLORS" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Primary Colors"@en ;
    tax:alternativeLabel "Base Colors"@en, "Fundamental Colors"@en, "Couleurs Primaires"@fr, "Colores Primarios"@es, "Grundfarben"@de, "Colori Primari"@it, "Cores Primárias"@pt ;
    tax:synonym "Elementary Colors"@en, "Pure Colors"@en, "Couleurs Pures"@fr ;
    tax:acronym "PC" ;
    tax:antonym color:NEUTRAL_COLORS ;
    tax:description "Base colors that cannot be created by mixing other colors in traditional color theory"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:level 0 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

color:SECONDARY_COLORS
    a tax:Node ;
    tax:identifier "SECONDARY_COLORS" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Secondary Colors"@en ;
    tax:alternativeLabel "Mixed Colors"@en, "Derived Colors"@en, "Couleurs Secondaires"@fr, "Colores Secundarios"@es, "Sekundärfarben"@de, "Colori Secondari"@it, "Cores Secundárias"@pt ;
    tax:synonym "Composite Colors"@en, "Binary Colors"@en, "Couleurs Composées"@fr ;
    tax:acronym "SC" ;
    tax:description "Colors created by mixing two primary colors in equal proportions"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:level 0 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 2 .

color:TERTIARY_COLORS
    a tax:Node ;
    tax:identifier "TERTIARY_COLORS" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Tertiary Colors"@en ;
    tax:alternativeLabel "Intermediate Colors"@en, "Complex Colors"@en, "Couleurs Tertiaires"@fr, "Colores Terciarios"@es, "Tertiärfarben"@de, "Colori Terziari"@it, "Cores Terciárias"@pt ;
    tax:synonym "Six-Color Mixes"@en, "Couleurs Intermédiaires"@fr ;
    tax:acronym "TC" ;
    tax:description "Colors created by mixing a primary and an adjacent secondary color"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:level 0 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 3 .

color:WARM_COLORS
    a tax:Node ;
    tax:identifier "WARM_COLORS" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Warm Colors"@en ;
    tax:alternativeLabel "Hot Colors"@en, "Fire Colors"@en, "Couleurs Chaudes"@fr, "Colores Cálidos"@es, "Warme Farben"@de, "Colori Caldi"@it, "Cores Quentes"@pt ;
    tax:synonym "Advancing Colors"@en, "Stimulating Colors"@en, "Couleurs Stimulantes"@fr ;
    tax:acronym "WC" ;
    tax:antonym color:COOL_COLORS ;
    tax:description "Colors that evoke warmth, energy, and passion, typically containing red, orange, or yellow"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:level 0 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 4 .

color:COOL_COLORS
    a tax:Node ;
    tax:identifier "COOL_COLORS" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Cool Colors"@en ;
    tax:alternativeLabel "Cold Colors"@en, "Ice Colors"@en, "Couleurs Froides"@fr, "Colores Fríos"@es, "Kalte Farben"@de, "Colori Freddi"@it, "Cores Frias"@pt ;
    tax:synonym "Receding Colors"@en, "Calming Colors"@en, "Couleurs Apaisantes"@fr ;
    tax:acronym "CC" ;
    tax:antonym color:WARM_COLORS ;
    tax:description "Colors that evoke coolness, tranquility, and distance, typically containing blue, green, or purple"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:level 0 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 5 .

color:NEUTRAL_COLORS
    a tax:Node ;
    tax:identifier "NEUTRAL_COLORS" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Neutral Colors"@en ;
    tax:alternativeLabel "Achromatic Colors"@en, "Grayscale Colors"@en, "Couleurs Neutres"@fr, "Colores Neutros"@es, "Neutrale Farben"@de, "Colori Neutri"@it, "Cores Neutras"@pt ;
    tax:synonym "Monochrome Colors"@en, "Non-Colors"@en, "Earth Tones"@en, "Couleurs Achromatiques"@fr ;
    tax:acronym "NC" ;
    tax:antonym color:PRIMARY_COLORS ;
    tax:description "Achromatic colors and muted earth tones that lack pure chromatic content"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:level 0 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 6 .

# Level 1 - Primary Colors
color:RED
    a tax:Node ;
    tax:identifier "RED" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Red"@en ;
    tax:alternativeLabel "Rouge"@fr, "Rojo"@es, "Rot"@de, "Rosso"@it, "Vermelho"@pt ;
    tax:synonym "Crimson Red"@en, "Ruby"@en, "Rouge Rubis"@fr, "Rojo Rubí"@es ;
    tax:antonym color:GREEN ;
    tax:description "Primary color with wavelength approximately 700nm, symbol of passion and energy"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:PRIMARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

color:BLUE
    a tax:Node ;
    tax:identifier "BLUE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Blue"@en ;
    tax:alternativeLabel "Bleu"@fr, "Azul"@es, "Blau"@de, "Blu"@it, "Azul"@pt ;
    tax:synonym "Azure"@en, "Cerulean"@en, "Azur"@fr, "Celeste"@es ;
    tax:antonym color:ORANGE ;
    tax:description "Primary color with wavelength approximately 470nm, symbol of tranquility and depth"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:PRIMARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 2 .

color:YELLOW
    a tax:Node ;
    tax:identifier "YELLOW" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Yellow"@en ;
    tax:alternativeLabel "Jaune"@fr, "Amarillo"@es, "Gelb"@de, "Giallo"@it, "Amarelo"@pt ;
    tax:synonym "Golden"@en, "Amber"@en, "Doré"@fr, "Dorado"@es ;
    tax:antonym color:PURPLE ;
    tax:description "Primary color with wavelength approximately 580nm, symbol of joy and enlightenment"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:PRIMARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 3 .

# Level 1 - Secondary Colors
color:GREEN
    a tax:Node ;
    tax:identifier "GREEN" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Green"@en ;
    tax:alternativeLabel "Vert"@fr, "Verde"@es, "Grün"@de, "Verde"@it, "Verde"@pt ;
    tax:synonym "Jade"@en, "Emerald Green"@en, "Vert Émeraude"@fr, "Verde Esmeralda"@es ;
    tax:antonym color:RED ;
    tax:description "Secondary color created by mixing blue and yellow, symbol of nature and growth"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:SECONDARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

color:ORANGE
    a tax:Node ;
    tax:identifier "ORANGE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Orange"@en ;
    tax:alternativeLabel "Orange"@fr, "Naranja"@es, "Orange"@de, "Arancione"@it, "Laranja"@pt ;
    tax:synonym "Tangerine"@en, "Amber Orange"@en, "Pumpkin"@en, "Mandarine"@fr ;
    tax:antonym color:BLUE ;
    tax:description "Secondary color created by mixing red and yellow, symbol of enthusiasm and creativity"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:SECONDARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 2 .

color:PURPLE
    a tax:Node ;
    tax:identifier "PURPLE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Purple"@en ;
    tax:alternativeLabel "Violet"@en, "Lavender"@en, "Violet"@fr, "Púrpura"@es, "Lila"@de, "Viola"@it, "Roxo"@pt ;
    tax:synonym "Plum"@en, "Magenta"@en, "Prune"@fr, "Ciruela"@es ;
    tax:antonym color:YELLOW ;
    tax:description "Secondary color created by mixing red and blue, symbol of royalty and mystery"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:SECONDARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 3 .

# Level 1 - Tertiary Colors
color:RED_ORANGE
    a tax:Node ;
    tax:identifier "RED_ORANGE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Red-Orange"@en ;
    tax:alternativeLabel "Vermillion"@en, "Rouge-Orange"@fr, "Rojo-Naranja"@es, "Rot-Orange"@de, "Rosso-Arancione"@it ;
    tax:synonym "Scarlet"@en, "Flame"@en, "Vermillon"@fr ;
    tax:description "Tertiary color combining the passion of red with the energy of orange"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:TERTIARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

color:YELLOW_ORANGE
    a tax:Node ;
    tax:identifier "YELLOW_ORANGE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Yellow-Orange"@en ;
    tax:alternativeLabel "Amber"@en, "Jaune-Orange"@fr, "Amarillo-Naranja"@es, "Gelb-Orange"@de, "Giallo-Arancione"@it ;
    tax:synonym "Marigold"@en, "Honey"@en, "Miel"@fr ;
    tax:description "Tertiary color combining the brightness of yellow with the warmth of orange"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:TERTIARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 2 .

color:YELLOW_GREEN
    a tax:Node ;
    tax:identifier "YELLOW_GREEN" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Yellow-Green"@en ;
    tax:alternativeLabel "Chartreuse"@en, "Lime"@en, "Jaune-Vert"@fr, "Amarillo-Verde"@es, "Gelb-Grün"@de, "Giallo-Verde"@it ;
    tax:synonym "Spring Green"@en, "Citrus"@en, "Vert Printemps"@fr ;
    tax:description "Tertiary color combining the vibrancy of yellow with the freshness of green"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:TERTIARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 3 .

color:BLUE_GREEN
    a tax:Node ;
    tax:identifier "BLUE_GREEN" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Blue-Green"@en ;
    tax:alternativeLabel "Teal"@en, "Turquoise"@en, "Bleu-Vert"@fr, "Azul-Verde"@es, "Blau-Grün"@de, "Blu-Verde"@it ;
    tax:synonym "Aqua"@en, "Cyan"@en, "Turquoise"@fr ;
    tax:description "Tertiary color combining the depth of blue with the vitality of green"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:TERTIARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 4 .

color:BLUE_PURPLE
    a tax:Node ;
    tax:identifier "BLUE_PURPLE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Blue-Purple"@en ;
    tax:alternativeLabel "Indigo"@en, "Periwinkle"@en, "Bleu-Violet"@fr, "Azul-Púrpura"@es, "Blau-Lila"@de, "Blu-Viola"@it ;
    tax:synonym "Royal Blue"@en, "Sapphire"@en, "Indigo"@fr ;
    tax:description "Tertiary color combining the tranquility of blue with the mystery of purple"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:TERTIARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 5 .

color:RED_PURPLE
    a tax:Node ;
    tax:identifier "RED_PURPLE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Red-Purple"@en ;
    tax:alternativeLabel "Magenta"@en, "Fuchsia"@en, "Rouge-Violet"@fr, "Rojo-Púrpura"@es, "Rot-Lila"@de, "Rosso-Viola"@it ;
    tax:synonym "Hot Pink"@en, "Cerise"@en, "Fuchsia"@fr ;
    tax:description "Tertiary color combining the passion of red with the elegance of purple"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:TERTIARY_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 6 .

# Level 1 - Neutral Colors
color:BLACK
    a tax:Node ;
    tax:identifier "BLACK" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Black"@en ;
    tax:alternativeLabel "Noir"@fr, "Negro"@es, "Schwarz"@de, "Nero"@it, "Preto"@pt ;
    tax:synonym "Ebony"@en, "Jet Black"@en, "Onyx"@en, "Ébène"@fr ;
    tax:antonym color:WHITE ;
    tax:description "Achromatic color representing absence of light, symbol of elegance and formality"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:NEUTRAL_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

color:WHITE
    a tax:Node ;
    tax:identifier "WHITE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "White"@en ;
    tax:alternativeLabel "Blanc"@fr, "Blanco"@es, "Weiß"@de, "Bianco"@it, "Branco"@pt ;
    tax:synonym "Snow White"@en, "Pearl"@en, "Ivory"@en, "Blanc Neige"@fr ;
    tax:antonym color:BLACK ;
    tax:description "Achromatic color representing presence of all visible light, symbol of purity and simplicity"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:NEUTRAL_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 2 .

color:GRAY
    a tax:Node ;
    tax:identifier "GRAY" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Gray"@en ;
    tax:alternativeLabel "Grey"@en, "Gris"@fr, "Gris"@es, "Grau"@de, "Grigio"@it, "Cinza"@pt ;
    tax:synonym "Silver"@en, "Ash"@en, "Charcoal"@en, "Argent"@fr ;
    tax:description "Achromatic color between black and white, symbol of neutrality and sophistication"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:NEUTRAL_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 3 .

color:BROWN
    a tax:Node ;
    tax:identifier "BROWN" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Brown"@en ;
    tax:alternativeLabel "Brun"@fr, "Marrón"@es, "Braun"@de, "Marrone"@it, "Marrom"@pt ;
    tax:synonym "Chocolate"@en, "Coffee"@en, "Tan"@en, "Chocolat"@fr ;
    tax:description "Dark orange color, symbol of earthiness and reliability"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:NEUTRAL_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 4 .

color:BEIGE
    a tax:Node ;
    tax:identifier "BEIGE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it", "pt" ;
    tax:label "Beige"@en ;
    tax:alternativeLabel "Beige"@fr, "Beige"@es, "Beige"@de, "Beige"@it, "Bege"@pt ;
    tax:synonym "Cream"@en, "Sand"@en, "Ecru"@en, "Crème"@fr ;
    tax:description "Light grayish-yellow color, symbol of warmth and comfort"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:NEUTRAL_COLORS ;
    tax:level 1 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 5 .

# Level 2 - Specific Red Variations
color:CRIMSON
    a tax:Node ;
    tax:identifier "CRIMSON" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Crimson"@en ;
    tax:alternativeLabel "Deep Red"@en, "Blood Red"@en, "Cramoisi"@fr, "Carmesí"@es, "Karmesin"@de, "Cremisi"@it ;
    tax:synonym "Burgundy Red"@en, "Wine Red"@en, "Bordeaux"@fr ;
    tax:description "Deep, rich red with slight blue undertones, traditionally associated with nobility"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:RED ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

color:SCARLET
    a tax:Node ;
    tax:identifier "SCARLET" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Scarlet"@en ;
    tax:alternativeLabel "Bright Red"@en, "Fire Red"@en, "Écarlate"@fr, "Escarlata"@es, "Scharlach"@de, "Scarlatto"@it ;
    tax:synonym "Cardinal Red"@en, "Flame Red"@en, "Rouge Cardinal"@fr ;
    tax:description "Bright red with orange undertones, vivid and attention-grabbing"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:RED ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 2 .

color:MAROON
    a tax:Node ;
    tax:identifier "MAROON" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Maroon"@en ;
    tax:alternativeLabel "Dark Red"@en, "Oxblood"@en, "Marron"@fr, "Granate"@es, "Kastanienbraun"@de, "Marrone"@it ;
    tax:synonym "Chestnut"@en, "Mahogany Red"@en, "Châtaigne"@fr ;
    tax:description "Dark brownish-red color, sophisticated and muted"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:RED ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 3 .

color:ROSE
    a tax:Node ;
    tax:identifier "ROSE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Rose"@en ;
    tax:alternativeLabel "Pink"@en, "Blush"@en, "Rose"@fr, "Rosa"@es, "Rosa"@de, "Rosa"@it ;
    tax:synonym "Baby Pink"@en, "Dusty Rose"@en, "Rose Poudré"@fr ;
    tax:description "Light red color with white undertones, gentle and romantic"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:RED ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 4 .

# Level 2 - Specific Blue Variations
color:NAVY
    a tax:Node ;
    tax:identifier "NAVY" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Navy"@en ;
    tax:alternativeLabel "Navy Blue"@en, "Dark Blue"@en, "Bleu Marine"@fr, "Azul Marino"@es, "Marineblau"@de, "Blu Navy"@it ;
    tax:synonym "Midnight Blue"@en, "Deep Blue"@en, "Bleu Nuit"@fr ;
    tax:description "Very dark blue, professional and authoritative"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:BLUE ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

color:SKY_BLUE
    a tax:Node ;
    tax:identifier "SKY_BLUE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Sky Blue"@en ;
    tax:alternativeLabel "Light Blue"@en, "Powder Blue"@en, "Bleu Ciel"@fr, "Azul Cielo"@es, "Himmelblau"@de, "Azzurro Cielo"@it ;
    tax:synonym "Baby Blue"@en, "Celeste"@en, "Bleu Bébé"@fr ;
    tax:description "Light blue reminiscent of clear daytime sky, peaceful and airy"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:BLUE ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 2 .

color:ROYAL_BLUE
    a tax:Node ;
    tax:identifier "ROYAL_BLUE" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Royal Blue"@en ;
    tax:alternativeLabel "Imperial Blue"@en, "Brilliant Blue"@en, "Bleu Royal"@fr, "Azul Real"@es, "Königsblau"@de, "Blu Reale"@it ;
    tax:synonym "Cobalt Blue"@en, "Electric Blue"@en, "Bleu Cobalt"@fr ;
    tax:description "Vivid, deep blue with slight purple undertones, regal and distinguished"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:BLUE ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 3 .

# Level 2 - Specific Green Variations
color:EMERALD
    a tax:Node ;
    tax:identifier "EMERALD" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Emerald"@en ;
    tax:alternativeLabel "Emerald Green"@en, "Jewel Green"@en, "Vert Émeraude"@fr, "Verde Esmeralda"@es, "Smaragdgrün"@de, "Verde Smeraldo"@it ;
    tax:synonym "Brilliant Green"@en, "Gem Green"@en, "Vert Brillant"@fr ;
    tax:description "Vivid green with blue undertones, precious and luxurious"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:GREEN ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

color:FOREST_GREEN
    a tax:Node ;
    tax:identifier "FOREST_GREEN" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Forest Green"@en ;
    tax:alternativeLabel "Dark Green"@en, "Hunter Green"@en, "Vert Forêt"@fr, "Verde Bosque"@es, "Waldgrün"@de, "Verde Foresta"@it ;
    tax:synonym "Pine Green"@en, "Evergreen"@en, "Vert Sapin"@fr ;
    tax:description "Dark green reminiscent of dense forests, natural and grounding"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:GREEN ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 2 .

color:LIME_GREEN
    a tax:Node ;
    tax:identifier "LIME_GREEN" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Lime Green"@en ;
    tax:alternativeLabel "Bright Green"@en, "Electric Green"@en, "Vert Lime"@fr, "Verde Lima"@es, "Limettengrün"@de, "Verde Lime"@it ;
    tax:synonym "Neon Green"@en, "Acid Green"@en, "Vert Néon"@fr ;
    tax:description "Bright yellow-green color, energetic and modern"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:GREEN ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 3 .

color:OLIVE_GREEN
    a tax:Node ;
    tax:identifier "OLIVE_GREEN" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Olive Green"@en ;
    tax:alternativeLabel "Olive"@en, "Khaki Green"@en, "Vert Olive"@fr, "Verde Oliva"@es, "Olivgrün"@de, "Verde Oliva"@it ;
    tax:synonym "Military Green"@en, "Sage Green"@en, "Vert Sauge"@fr ;
    tax:description "Muted green with brown undertones, earthy and sophisticated"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:GREEN ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 4 .

# Level 2 - Specific Gray Variations
color:CHARCOAL
    a tax:Node ;
    tax:identifier "CHARCOAL" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Charcoal"@en ;
    tax:alternativeLabel "Dark Gray"@en, "Anthracite"@en, "Charbon"@fr, "Carbón"@es, "Anthrazit"@de, "Antracite"@it ;
    tax:synonym "Graphite"@en, "Slate"@en, "Ardoise"@fr ;
    tax:description "Very dark gray with slight blue undertones, sophisticated and modern"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:GRAY ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 1 .

color:SILVER
    a tax:Node ;
    tax:identifier "SILVER" ;
    tax:defaultLanguage "en" ;
    tax:supportedLanguages "en", "fr", "es", "de", "it" ;
    tax:label "Silver"@en ;
    tax:alternativeLabel "Light Gray"@en, "Metallic Gray"@en, "Argent"@fr, "Plata"@es, "Silber"@de, "Argento"@it ;
    tax:synonym "Platinum"@en, "Steel Gray"@en, "Gris Acier"@fr ;
    tax:description "Light gray with metallic qualities, elegant and refined"@en ;
    tax:belongsToTaxonomy color:ColorTaxonomy ;
    tax:parentNode color:GRAY ;
    tax:level 2 ;
    tax:status "ACTIVE" ;
    tax:sortOrder 2 .

# Establish all bidirectional antonym relationships
color:PRIMARY_COLORS tax:antonym color:NEUTRAL_COLORS .
color:NEUTRAL_COLORS tax:antonym color:PRIMARY_COLORS .
color:WARM_COLORS tax:antonym color:COOL_COLORS .
color:COOL_COLORS tax:antonym color:WARM_COLORS .
color:RED tax:antonym color:GREEN .
color:GREEN tax:antonym color:RED .
color:BLUE tax:antonym color:ORANGE .
color:ORANGE tax:antonym color:BLUE .
color:YELLOW tax:antonym color:PURPLE .
color:PURPLE tax:antonym color:YELLOW .
color:BLACK tax:antonym color:WHITE .
color:WHITE tax:antonym color:BLACK .

# Establish parent-child relationships
color:PRIMARY_COLORS tax:childNodes color:RED, color:BLUE, color:YELLOW .
color:SECONDARY_COLORS tax:childNodes color:GREEN, color:ORANGE, color:PURPLE .
color:TERTIARY_COLORS tax:childNodes color:RED_ORANGE, color:YELLOW_ORANGE, color:YELLOW_GREEN, color:BLUE_GREEN, color:BLUE_PURPLE, color:RED_PURPLE .
color:NEUTRAL_COLORS tax:childNodes color:BLACK, color:WHITE, color:GRAY, color:BROWN, color:BEIGE .
color:RED tax:childNodes color:CRIMSON, color:SCARLET, color:MAROON, color:ROSE .
color:BLUE tax:childNodes color:NAVY, color:SKY_BLUE, color:ROYAL_BLUE .
color:GREEN tax:childNodes color:EMERALD, color:FOREST_GREEN, color:LIME_GREEN, color:OLIVE_GREEN .
color:GRAY tax:childNodes color:CHARCOAL, color:SILVER .
```