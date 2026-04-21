---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Transforming-RDF-by-Kurt-Cagle
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:49.658461+00:00'
  title: Transforming Rdf By Kurt Cagle
  type: plain-doc
  version: '0.1'
---

# Transforming Rdf By Kurt Cagle

[

![](https://substackcdn.com/image/fetch/$s_!XLI1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd639a7ec-c04b-4ffd-aeb4-97bf2e39b41e_1408x768.png)

](https://substackcdn.com/image/fetch/$s_!XLI1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd639a7ec-c04b-4ffd-aeb4-97bf2e39b41e_1408x768.png)

Copyright 2025 Kurt Cagle / The Ontologist

When people are working with RDF for the first time, it can seem overwhelming and, to be honest, rather useless, in part because they have come to RDF either from the SQL world or the JSON world, and there’s often little guidance about how to deal with the output. My goal with this column is to explore a few different ways that you can transform query output from RDF.

Before beginning, it’s worth understanding that RDF is NOT a specific format - rather, RDF is a way of expressing graphs abstractly that can be represented in many different formats (by my count, and this is probably low, there are something like 35 different RDF profiles currently in use), from JSON (many formats, most notably JSON-LD), XML, YAML, DDL (SQL) and CSV to HTML and Markdown to domain-specific languages such as Mermaid diagrams. This robustness is important because it means that you can encode, transmit and interpret RDF data to almost any database, input device, service or application out there.

This means that RDF can be transformed into almost any kind of output depending upon your requirements. The examples I give here use MarkLogic, but the same principles hold for most RDF store transformations.

## My NS Class

Over the years I’ve found that maintain the context of RDF - the namespaces and associated prefixes - can be a pain in the butt. As a consequence, I’ve found that it is often better to define the context separately (as a JSON map) then use a helper class that can work with different sets of contexts for different requirements. This not only makes it much easier to read and write TURTLE and SPARQL files, but it also allows for several handy additional functions (such as mapping from one set of prefixes to another).

For example, consider a Turtle RDF database that holds information on superheroes, such as the following record for Raven from DC’s Teen Titans series:

```
@prefix ex:   <http://example.org/> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix comics:   <https://theCagleReport.com/ns/>.
@prefix Character:   <https://theCagleReport.com/ns/Character#> .
@prefix CharacterType:   <https://theCagleReport.com/ns/CharacterType#>.
@prefix Universe:   <https://theCagleReport.com/ns/Universe#>.
@prefix Dimension:   <https://theCagleReport.com/ns/Dimension#>.
@prefix MyersBriggsType:   <https://theCagleReport.com/ns/MyersBriggsType#>.
@prefix DNDAlignment:   <https://theCagleReport.com/ns/DNDAlignment#>.
@prefix Org:   <https://theCagleReport.com/ns/Org#>.
@prefix OrgType:   <https://theCagleReport.com/ns/OrgType#>.
@prefix Gender:   <https://theCagleReport.com/ns/Gender#>.
@prefix Entity:   <https://theCagleReport.com/ns/Entity#>.
@prefix Concept:   <https://theCagleReport.com/ns/Concept#>.
@prefix SuperPowerType:   <https://theCagleReport.com/ns/SuperPowerType#>.
@prefix Weapon:   <https://theCagleReport.com/ns/Weapon#>.

Character:Raven
        rdf:type            Character: ;
        rdfs:label          "Raven"^^xsd:string;
        Character:alterEgo
                "Rachel Roth"^^xsd:string;
        Character:appearance
                "Long dark hair, pale skin, dark hooded cloak, red gem on forehead"^^xsd:string;
        Character:associatedWith
                Character:TeenTitans, Dimension:Azarath ;  # Added Azarath (her birthplace)
        rdfs:comment
                "A half-demon, half-human sorceress and member of the Teen Titans who uses her dark magic and telepathy to fight against her father Trigon and other cosmic threats."^^xsd:string;
        Character:dndAlignment
                DNDAlignment:True_Neutral ;
        Character:gender
                Gender:Female ;
        Character:lastUpdated
                "2024-01-15T09:45:22.00-05:00"^^xsd:dateTime ;  # Updated timestamp
        Character:memberOf
                Org:TeenTitans ;
        Character:myersBriggsType
                MyersBriggsType:INTP ;
        Character:superPowerType 
                SuperPowerType:Magic, 
                SuperPowerType:Telepathy, 
                SuperPowerType:Telekinesis, 
                SuperPowerType:DimensionalTravel,
                SuperPowerType:EmpathicManipulation ;  # Expanded powers
        Character:superPowersDescription
                "Dark magic, telepathy, telekinesis, dimensional travel, and empathic energy manipulation"^^xsd:string;
        Character:type
                CharacterType:Superhero, 
                CharacterType:HalfDemon ;  # Added hybrid lineage
        Character:universe 
                Universe:DCEU ;
        Character:romanticInterest 
                Character:BeastBoy ;
        Character:nemesis 
                Character:Trigon ;
        # New properties from Trigon's profile:
        Character:hasParent
                Character:Trigon ;  # Inverse of Trigon's "parentOf"
        Character:weakness
                "Emotional instability due to demonic heritage", 
                "Susceptibility to Trigon's corruption"^^xsd:string ;
        Character:allies
                Character:Starfire, Character:Cyborg, Character:Robin ;
.
```

We’ll make a key assumption here: every resource has an rdf:label - a label that provides a human-readable label for that resource. The other assumption is a bit of secret sauce.

I’ve attached a file to this article called ns.mjs which contains a number of useful class methods for managing the context of the graphs. The context is a dictionary of namespaces and their associated prefixes, and can simplify creating queries, among other things. For instance, if you want a dictionary of namespaces by prefix, you’d do the following in Javascript (note that this is the MarkLogic javascript, but it should be relatively easy to convert this to ecmascript:

```
'use strict';
declareUpdate();
const sem = require("/MarkLogic/semantics.xqy");
import { NS } from '/lib/ns.mjs';
let ns = new NS()
ns.map

>> Output
{
"ex": "http://example.org/", 
"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", 
"rdfs": "http://www.w3.org/2000/01/rdf-schema#", 
"owl": "http://www.w3.org/2002/07/owl#", 
"xsd": "http://www.w3.org/2001/XMLSchema#", 
"sh": "http://www.w3.org/ns/shacl#", 
"comics": "https://theCagleReport.com/ns/", 
"Character": "https://theCagleReport.com/ns/Character#", 
"CharacterType": "https://theCagleReport.com/ns/CharacterType#", 
"Graph": "https://theCagleReport.com/ns/CharacterGraph#",
"Universe": "https://theCagleReport.com/ns/Universe#", 
"Dimension": "https://theCagleReport.com/ns/Dimension#", 
"MyersBriggsType": "https://theCagleReport.com/ns/MyersBriggsType#", 
"DNDAlignment": "https://theCagleReport.com/ns/DNDAlignment#", 
"Org": "https://theCagleReport.com/ns/Org#", 
"OrgType": "https://theCagleReport.com/ns/OrgType#", 
"Gender": "https://theCagleReport.com/ns/Gender#", 
"Entity": "https://theCagleReport.com/ns/Entity#", 
"Concept": "https://theCagleReport.com/ns/Concept#", 
"SuperPowerType": "https://theCagleReport.com/ns/SuperPowerType#", 
"Weapon": "https://theCagleReport.com/ns/Weapon#"
}
```

Similarly, once you have the Namespace object ns, you can also retrieve the context for SPARQL queries:

```
ns.sparql()
>> Output
prefix ex: <http://example.org/> 
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
prefix owl: <http://www.w3.org/2002/07/owl#> 
prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
prefix sh: <http://www.w3.org/ns/shacl#> 
prefix comics: <http://theCagleReport.com/ns/> 
prefix Character: <http://theCagleReport.com/ns/Character#> 
prefix Graph: <http://theCagleReport.com/ns/Graph#> 
prefix CharacterType: <http://theCagleReport.com/ns/CharacterType#> 
prefix Universe: <http://theCagleReport.com/ns/Universe#> 
prefix Dimension: <http://theCagleReport.com/ns/Dimension#> 
prefix MyersBriggsType: <http://theCagleReport.com/ns/MyersBriggsType#> 
prefix DNDAlignment: <http://theCagleReport.com/ns/DNDAlignment#> 
prefix Org: <http://theCagleReport.com/ns/Org#> 
prefix OrgType: <http://theCagleReport.com/ns/OrgType#> 
prefix Gender: <http://theCagleReport.com/ns/Gender#> 
prefix Entity: <http://theCagleReport.com/ns/Entity#> 
prefix Concept: <http://theCagleReport.com/ns/Concept#> 
prefix SuperPowerType: <http://theCagleReport.com/ns/SuperPowerType#> 
prefix Weapon: <http://theCagleReport.com/ns/Weapon#> 
```

Note that there is very subtle difference between Turtle and Sparql contexts (the lack of the leading @ symbol and the terminating period), though more contemporary triple stores and libraries can use Sparql notation with Turtle. The library also has a ns.turtle() method that outputs the same context with the older `@.` syntax.

The NS class includes a couple of other functions - ns.curie(), which takes an IRI and matches it to the corresponding prefix + local name:

```
  ns.curie("http://theCagleReport.com/ns/Character#Raven")

// becomes

  "Character:Raven"
```

and ns.ciri() (curie to IRI) which performs the inverse operation. In MarkLogic, these are wrappers for **sem.curieShorten()** and **sem.curieExpand()**, but use the default ns.map rather than having to manually pass it in, as is the case with the latter two functions.

This library is available on my github site (NEED LINK).

## SPARQL Select and Transformations

The SPARQL select statement is the workhorse of SPARQL, and structurally it is similar to how a SQL query works in that it generates an array of rows, with each array holding the variable values of one graph traversal. The array, in turn, can be considered a record set.

For instance, consider a query that looks for all female superheroes (and or villains or anti-heroes) in the database:

```
// Javascript
'use strict';
declareUpdate();
const sem = require("/MarkLogic/semantics.xqy");
import { NS } from '/lib/ns.mjs';
let ns = new NS()
let query = `${ns.sparql}
select ?Name ?CharacterType ?Gender ?Publisher ?CharacterType ?DNDAlignment ?MyersBriggsType ?Appearance ?Comment where {
?s a Character: .
 ?s rdfs:label ?Name .
optional {
  ?s Character:type ?characterType.
  ?characterType rdfs:label ?CharacterType.
   }
optional {
  ?s Character:gender ?gender.
  ?gender rdfs:label ?Gender.
   }
optional {
  ?s Character:domain ?publisher.
  ?publisher rdfs:label ?Publisher.
   }
optional {
  ?s Character:dndAlignment ?dndAlignment.
  ?dndAlignment rdfs:label ?DNDAlignment.
   }
optional {
  ?s Character:myersBriggsType ?myersBriggsType.
  ?myersBriggsType rdfs:label ?MyersBriggsType.
   }
optional {
  ?s Character:appearance ?Appearance .
  }
optional {
  ?s rdfs:comment ?Comment .
  }
  
   
filter(STRSTARTS(?Gender,"Female"))
} order by ?Name
` // ends the SPARQL
let results = sem.sparql(query).toArray()
results // output results
```

This retrieves a JSON array of map objects, which can then be converted into an in-memory array of javascript objects:

```
 [
{
"Name": "Batgirl", 
"CharacterType": "Superhero", 
"Gender": "Female", 
"Publisher": "DC Extended Domain", 
"DNDAlignment": "Lawful Good", 
"MyersBriggsType": "INTJ", 
"Appearance": "Long red hair, bat-themed costume with purple and yellow color scheme, bat symbol on chest", 
"Comment": "The daughter of Gotham City Police Commissioner James Gordon, who becomes the crime-fighting heroine Batgirl, using her intellect, combat skills, and advanced technology to protect Gotham City."
}, 
{
"Name": "Batwoman", 
"CharacterType": "Superhero", 
"Gender": "Female", 
"Publisher": "DC Extended Domain", 
"DNDAlignment": "Lawful Good", 
"MyersBriggsType": "ISTJ", 
"Appearance": "Long red hair, bat-themed costume with red and black color scheme, bat symbol on chest", 
"Comment": "A wealthy heiress and cousin of Bruce Wayne who becomes the crime-fighting vigilante Batwoman, using her advanced combat skills and technology to protect Gotham City."
}, 
{
"Name": "Catwoman", 
"CharacterType": "Anti-hero", 
"Gender": "Female", 
"Publisher": "DC Extended Domain", 
"DNDAlignment": "True Neutral", 
"MyersBriggsType": "ISTP", 
"Appearance": "Short black hair, black catsuit with goggles, whip", 
"Comment": "A skilled thief and occasional ally of Batman, who uses her athletic abilities, martial arts skills, and cunning to navigate the criminal underworld of Gotham City."
}, 
{
"Name": "Harley Quinn", 
"CharacterType": "Anti-hero", 
"Gender": "Female", 
"Publisher": "DC Extended Domain", 
"DNDAlignment": "Chaotic Neutral", 
"MyersBriggsType": "ESFP", 
"Appearance": "Blonde hair with blue and pink highlights, red and black attire, wielding a baseball bat or mallet", 
"Comment": "A former psychiatrist at Arkham Asylum who falls in love with the Joker and becomes his accomplice, later branching out on her own as an antihero and member of the Suicide Squad."
}, 
{
"Name": "Poison Ivy", 
"CharacterType": "Supervillain", 
"Gender": "Female", 
"Publisher": "DC Extended Domain", 
"DNDAlignment": "Chaotic Neutral", 
"MyersBriggsType": "INFJ", 
"Appearance": "Long red hair, green attire with plant-like elements", 
"Comment": "A brilliant botanist who becomes the eco-terrorist Poison Ivy after a lab accident, using her control over plant life and her ability to secrete toxins to pursue her own agenda."
}, 
{
"Name": "Raven", 
"CharacterType": "Superhero", 
"Gender": "Female", 
"Publisher": "DC Extended Domain", 
"DNDAlignment": "True Neutral", 
"MyersBriggsType": "INTP", 
"Appearance": "Long dark hair, pale skin, dark hooded cloak, red gem on forehead", 
"Comment": "A half-demon, half-human sorceress and member of the Teen Titans who uses her dark magic and telepathy to fight against her father Trigon and other cosmic threats."
}, 
{
"Name": "Scarlet Witch", 
"CharacterType": "Superhero", 
"Gender": "Female", 
"Publisher": "Marvel Cinematic Domain", 
"DNDAlignment": "Chaotic Good", 
"MyersBriggsType": "INFJ", 
"Appearance": "Long brown hair, red attire, red magical energy surrounding hands", 
"Comment": "A former member of HYDRA who gains powerful abilities after being exposed to the Mind Stone, later joining the Avengers and using her reality-warping powers to protect Earth."
}, ... // More
]
```

Once in this format, transforming it is pretty straightforward. For instance, in Javascript you could output it as a series of records in HTML or MarkDown, using template literals. For instance:

```
let output = results.map((entry)=>`
<div class="${entry.CharacterType} Character"><h1>${entry.CharacterType}: ${entry.Name}</h1>
<ul>
<li><label>Character Type: </label>${entry.CharacterType}</li></label>
<li><label>Gender: </label>${entry.Gender}</li></label>
<li><label>Publisher: </label>${entry.Publisher}</li></label>
<li><label>Myers Briggs: </label>${entry.MyersBriggsType}</li></label>
<li><label>D&amp;D Alignment: </label>${entry.DNDAlignment}</li></label>
</ul>
<div class="Appearance">
<h2>Appearance</h2>
<p>${entry.Appearance}<p>
</div>
<div class="Comment">
<h2>Comment</h2>
<p>${entry.Comment}</p>
</div>
`).join('\n')
output += `<style>
h1 {font-size:14pt;padding:5pt;}
h2 {font-size:12pt}
.Superhero h1 {background-color:blue;color:white}
.LoveInterest h1  {background-color:red;color:white}
.Anti-hero h1 {background-color:purple;color:white}
.Supervillain h1 {background-color:black;color:white}
.Character {width:6in;font-family:Arial}
.Appearance {font-size:10pt;}
.Comment {font-size:10pt;}
label {font-weight:bold;}
</style>`
output // output stream passed as a response
```

This generates the following (with a few removed for redundancy):

## Superhero: Batgirl

-   **Character Type:** Superhero
    
-   **Gender:** Female
    
-   **Publisher:** DC Extended Universe
    
-   **Myers Briggs:** INTJ
    
-   **D&D Alignment:** Lawful Good
    

## Appearance

Long red hair, bat-themed costume with purple and yellow color scheme, bat symbol on chest

## Comment

The daughter of Gotham City Police Commissioner James Gordon, who becomes the crime-fighting heroine Batgirl, using her intellect, combat skills, and advanced technology to protect Gotham City.

## Superhero: Black Canary

-   **Character Type:** Superhero
    
-   **Gender:** Female
    
-   **Publisher:** DC Extended Universe
    
-   **Myers Briggs:** ESTP
    
-   **D&D Alignment:** Neutral Good
    

## Appearance

A blonde woman with wavy or straight hair, often wearing a black leather jacket, fishnet stockings, and a form-fitting bodysuit. She is known for her striking blue eyes and athletic physique. Her costume often includes gloves, boots, and a choker. In some versions, she also wears a domino mask. Her signature look exudes a mix of classic noir and modern street-fighter aesthetics.

## Comment

Black Canary is a skilled martial artist and street fighter, who possesses a powerful sonic scream known as the Canary Cry. She often fights alongside Green Arrow and is a member of the Justice League and the Birds of Prey.

## Anti-hero: Catwoman

-   **Character Type:** Anti-hero
    
-   **Gender:** Female
    
-   **Publisher:** DC Extended Universe
    
-   **Myers Briggs:** ISTP
    
-   **D&D Alignment:** True Neutral
    

## Appearance

Short black hair, black catsuit with goggles, whip

## Comment

A skilled thief and occasional ally of Batman, who uses her athletic abilities, martial arts skills, and cunning to navigate the criminal underworld of Gotham City.

## Anti-hero: Harley Quinn

-   **Character Type:** Anti-hero
    
-   **Gender:** Female
    
-   **Publisher:** DC Extended Universe
    
-   **Myers Briggs:** ESFP
    
-   **D&D Alignment:** Chaotic Neutral
    

## Appearance

Blonde hair with blue and pink highlights, red and black attire, wielding a baseball bat or mallet

## Comment

A former psychiatrist at Arkham Asylum who falls in love with the Joker and becomes his accomplice, later branching out on her own as an antihero and member of the Suicide Squad.

## LoveInterest: Lois Lane

-   **Character Type:** LoveInterest
    
-   **Gender:** Female
    
-   **Publisher:** DC Extended Universe
    
-   **Myers Briggs:** ENTP
    
-   **D&D Alignment:** Neutral Good
    

## Appearance

A stylish and confident woman with shoulder-length dark hair (often black or deep brown), sharp facial features, and expressive eyes. She is frequently shown wearing professional attire, such as blouses, blazers, and pencil skirts, reflecting her role as a top investigative journalist. Her look varies across adaptations, but she often exudes a classic, determined, and sophisticated presence.

## Comment

The girlfriend, and, in some versions, the wife of Superman. A reporter for The Daily Planet.

A few final things to note:

-   Generating tables can be done in a similar fashion - you can use the key names from the SPARQL query as the header columns and to interact across objects, or you can manually assign the keys in an array.
    

```
let item = results[0]
let keys = Object.keys(item)
let output = `<table><thead><tr>${keys.map(key=>`<th>${key}</th>`).join('')}</tr></thead><tbody>`
output += results.map((item)=>`<tr>{keys.map((key)=>`<td>${item[key]}</td>`).join('')}</tr>`).join('')
output += `</tbody></table>`
output // send to client
```

-   You can do something similar with Markdown (I’ll dig into this in a subsequent post).
    

This isn’t the only thing that you can do with SPARQL results. You can work with the graph as a graph using the CONSTRUCT statement. My next post will continue in this theme, as well as show you you can output content to deep XML structures.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!M8wl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde5991f2-2d1a-4b0a-b717-1daa8c79771f_1344x768.png)

](https://substackcdn.com/image/fetch/$s_!M8wl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde5991f2-2d1a-4b0a-b717-1daa8c79771f_1344x768.png)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.

