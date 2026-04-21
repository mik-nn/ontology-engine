---
title: "Power Up Your SHACL Validation"
source: "https://ontologist.substack.com/p/power-up-your-shacl-validation?utm_source=profile&utm_medium=reader2"
date: "Mar 9"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!vLNA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4696e404-9b97-4c46-90e1-a3381b986299_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!vLNA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4696e404-9b97-4c46-90e1-a3381b986299_2688x1536.jpeg)

There has always been a fundamental problem with SPARQL: you need to understand the data model to use it. This can be a major limitation, especially when your data model consists of many OWL models constructed from different subordinate ontologies written by various standards bodies. I would also argue that because OWL is built on logical relationships, this process requires a deep understanding of the problem domain.

There are a few solutions to this - one is to provide a limited subset of queries that can be parameterised (as I’ve discussed in a recent paper). There are benefits to doing things this way, with the SPARQL being very general but constrained in such a way as to provide a certain degree of abstraction of the underlying graph. However, you still need to have someone write those queries.

A second alternative would be to use SHACL 1.2 node expressions, as discussed in my recent series on the capabilities of that language, but by itself, that specification is still in its infancy. There are some interesting design patterns and methodologies that can emerge from this approach, but this doesn’t necessarily resolve the natural language query aspect.

## Generating SHACL from Data

A final alternative would be to GENERATE SHACL 1.2 (or even just 1.1) from a known data graph from the source data via AI, modify it as appropriate, then use the SHACL to generate the SPARQL queries. I’ll discuss this approach in this post.

SHACL does not provide a logical inference schema (not directly, anyway); instead, it is primarily structural in nature and typically deals with lower-level classes, properties, and constraints. It is foundational, with OWL systems or others providing a higher-order reasoning capability, when utilized correctly. However, with the structural underpinnings in place, you have what’s needed to provide better queries.

Note as well that there is nothing keeping you from having both an OWL and a SHACL schema for a given dataset. This is fairly important, because it means that even if you do have an existing RDF database, a SHACL schema can be turned on or off without impacting the dataset. Finally, those SHACL graphs are likely to be very tiny compared to most data graphs. Tiny is good when dealing with AI because a SHACL schema can readily fit into an AI context whereas storing the entire database into the context will likely be unworkable.

_In the examples discussed here, I used Anthropic’s Claude Model Opus 4.5. As a caveat, this was not vibe computing. At every step you should review the artefacts produced, just as you should with any AI generated content._

## Building a Data Source

The first step involved data acquisition. You do not need the entire dataset that you’re working with, but you should obtain a sufficiently large sample to see patterns; as a rule of thumb, a spreadsheet is probably ideal for that. If you’re building a dataset from scratch, you can also generate such a dataset from a prompt. For instance,

```
create a dataset in Turtle showing fifteen DC superheroes (male and female) and supervillains (male and female) showing their gender, relative age, appearance, superpowers, where located, and their primary love interests, principle antagonists, and associated organizations. For gender, superpowers, locations love interests, antagonists and organisations, make each of these IRIs with corresponding entries rather than literals.
```

After thinking for a it, the AI generates a file (here with about 800 lines, a few of which are shown here):

```
# DC Superhero Turtle

@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dc: <http://example.org/dc-universe/> .
@prefix dcc: <http://example.org/dc-universe/character/> .
@prefix dcp: <http://example.org/dc-universe/power/> .
@prefix dcl: <http://example.org/dc-universe/location/> .
@prefix dcg: <http://example.org/dc-universe/gender/> .
@prefix dco: <http://example.org/dc-universe/organization/> .

# =============================================================================
# ONTOLOGY CLASSES
# =============================================================================

dc:Character a rdfs:Class ;
    rdfs:label “Character” ;
    rdfs:comment “A character in the DC Universe” .

dc:Hero a rdfs:Class ;
    rdfs:subClassOf dc:Character ;
    rdfs:label “Hero” ;
    rdfs:comment “A superhero character” .

dc:Villain a rdfs:Class ;
    rdfs:subClassOf dc:Character ;
    rdfs:label “Villain” ;
    rdfs:comment “A supervillain character” .

dc:AntiHero a rdfs:Class ;
    rdfs:subClassOf dc:Character ;
    rdfs:label “Anti-Hero” ;
    rdfs:comment “A morally ambiguous character” .

dc:Gender a rdfs:Class ;
    rdfs:label “Gender” ;
    rdfs:comment “Gender classification” .

dc:Superpower a rdfs:Class ;
    rdfs:label “Superpower” ;
    rdfs:comment “A superhuman ability or power” .

dc:Location a rdfs:Class ;
    rdfs:label “Location” ;
    rdfs:comment “A place in the DC Universe” .

dc:Organization a rdfs:Class ;
    rdfs:label “Organization” ;
    rdfs:comment “A group or organization in the DC Universe” .

# =============================================================================
# PROPERTIES
# =============================================================================

dc:hasGender a rdf:Property ;
    rdfs:label “has gender” ;
    rdfs:domain dc:Character ;
    rdfs:range dc:Gender .

dc:hasAge a rdf:Property ;
    rdfs:label “has age” ;
    rdfs:domain dc:Character ;
    rdfs:range xsd:string ;
    rdfs:comment “Relative age category of the character” .

dc:hasAppearance a rdf:Property ;
    rdfs:label “has appearance” ;
    rdfs:domain dc:Character ;
    rdfs:range xsd:string ;
    rdfs:comment “Physical description of the character” .

dc:hasPower a rdf:Property ;
    rdfs:label “has power” ;
    rdfs:domain dc:Character ;
    rdfs:range dc:Superpower .

dc:locatedIn a rdf:Property ;
    rdfs:label “located in” ;
    rdfs:domain dc:Character ;
    rdfs:range dc:Location .

dc:hasLoveInterest a rdf:Property ;
    rdfs:label “has love interest” ;
    rdfs:domain dc:Character ;
    rdfs:range dc:Character .

dc:hasAntagonist a rdf:Property ;
    rdfs:label “has antagonist” ;
    rdfs:domain dc:Character ;
    rdfs:range dc:Character .

dc:memberOf a rdf:Property ;
    rdfs:label “member of” ;
    rdfs:domain dc:Character ;
    rdfs:range dc:Organization .

dc:realName a rdf:Property ;
    rdfs:label “real name” ;
    rdfs:domain dc:Character ;
    rdfs:range xsd:string .

dc:alias a rdf:Property ;
    rdfs:label “alias” ;
    rdfs:domain dc:Character ;
    rdfs:range xsd:string .

# =============================================================================
# GENDER INSTANCES
# =============================================================================

dcg:Male a dc:Gender ;
    rdfs:label “Male” .

dcg:Female a dc:Gender ;
    rdfs:label “Female” .

# =============================================================================
# SUPERPOWER INSTANCES
# =============================================================================

dcp:SuperStrength a dc:Superpower ;
    rdfs:label “Super Strength” ;
    rdfs:comment “Extraordinary physical strength beyond human limits” .

dcp:Flight a dc:Superpower ;
    rdfs:label “Flight” ;
    rdfs:comment “Ability to fly through the air” .

dcp:HeatVision a dc:Superpower ;
    rdfs:label “Heat Vision” ;
    rdfs:comment “Ability to emit intense heat beams from eyes” .

dcp:XRayVision a dc:Superpower ;
    rdfs:label “X-Ray Vision” ;
    rdfs:comment “Ability to see through solid objects” .

# =============================================================================
# LOCATION INSTANCES
# =============================================================================

dcl:Metropolis a dc:Location ;
    rdfs:label “Metropolis” ;
    rdfs:comment “The City of Tomorrow, home to Superman” .

dcl:Gotham a dc:Location ;
    rdfs:label “Gotham City” ;
    rdfs:comment “Dark and crime-ridden city, home to Batman” .


# =============================================================================
# ORGANIZATION INSTANCES
# =============================================================================

dco:JusticeLeague a dc:Organization ;
    rdfs:label “Justice League” ;
    rdfs:comment “Premier superhero team of the DC Universe” .

dco:BatFamily a dc:Organization ;
    rdfs:label “Bat Family” ;
    rdfs:comment “Batman’s network of allies and proteges” .


# =============================================================================
# CHARACTER INSTANCES - HEROES
# =============================================================================

# --- SUPERMAN ---
dcc:Superman a dc:Hero ;
    rdfs:label “Superman” ;
    dc:realName “Clark Kent” ;
    dc:alias “Kal-El” , “The Man of Steel” , “The Last Son of Krypton” ;
    dc:hasGender dcg:Male ;
    dc:hasAge “Adult (appears early 30s, actual age much older due to Kryptonian physiology)” ;
    dc:hasAppearance “Tall, muscular build with black hair and blue eyes. Wears iconic blue suit with red cape, red boots, and ‘S’ shield emblem on chest.” ;
    dc:hasPower dcp:SuperStrength , dcp:Flight , dcp:HeatVision , dcp:XRayVision , 
               dcp:Invulnerability , dcp:SuperSpeed , dcp:FreezeBreath , dcp:EnhancedSenses ;
    dc:locatedIn dcl:Metropolis ;
    dc:hasLoveInterest dcc:LoisLane , dcc:WonderWoman ;
    dc:hasAntagonist dcc:LexLuthor , dcc:Darkseid ;
    dc:memberOf dco:JusticeLeague .

# --- WONDER WOMAN ---
dcc:WonderWoman a dc:Hero ;
    rdfs:label “Wonder Woman” ;
    dc:realName “Diana Prince” ;
    dc:alias “Princess Diana of Themyscira” , “Amazon Princess” ;
    dc:hasGender dcg:Female ;
    dc:hasAge “Adult (immortal, thousands of years old but appears early 30s)” ;
    dc:hasAppearance “Tall, athletic Amazon warrior with long black hair and blue eyes. Wears red and gold armor with tiara, silver bracelets, and carries golden lasso.” ;
    dc:hasPower dcp:SuperStrength , dcp:Flight , dcp:AmazonianTraining , dcp:LassoOfTruth ,
               dcp:Bracelets , dcp:DivineBlessing , dcp:Immortality , dcp:MartialArts ;
    dc:locatedIn dcl:Themyscira , dcl:Metropolis ;
    dc:hasLoveInterest dcc:SteveT , dcc:Superman , dcc:Batman ;
    dc:hasAntagonist dcc:Cheetah , dcc:Darkseid ;
    dc:memberOf dco:JusticeLeague , dco:Amazons .

# --- BATMAN ---
dcc:Batman a dc:Hero ;
    rdfs:label “Batman” ;
    dc:realName “Bruce Wayne” ;
    dc:alias “The Dark Knight” , “The Caped Crusader” , “World’s Greatest Detective” ;
    dc:hasGender dcg:Male ;
    dc:hasAge “Adult (mid-40s)” ;
    dc:hasAppearance “Tall, extremely muscular with black hair and blue eyes. Wears dark gray and black armored suit with cape, cowl with pointed ears, and bat emblem on chest.” ;
    dc:hasPower dcp:MartialArts , dcp:DetectiveSkills , dcp:Stealth , dcp:Gadgetry ,
               dcp:GeniusIntellect , dcp:Acrobatics ;
    dc:locatedIn dcl:Gotham ;
    dc:hasLoveInterest dcc:Catwoman , dcc:TaliaAlGhul , dcc:WonderWoman ;
    dc:hasAntagonist dcc:Joker , dcc:LexLuthor ;
    dc:memberOf dco:JusticeLeague , dco:BatFamily .
```

A few quick notes - the namespaces largely align with classes, which works very well with a structural approach to schemas. Almost all connections that describe relationships are to IRIs rather than strings. The more that you can do this, the richer your dataset will be. Most of the relational code is in RDFS, which provides domain and range information but little else. There’s also very little in the way of an upper ontology, because that requires inferencing along subdomains. If you have these, you can likely obtain richer, more conditional SHACL, but the above is a reasonable bare minimum.

Once you have this sample (as a turtle file or similar resource), then you can generate the SHACL via an AI with the following prompt:

```
# Claude Prompt

For this dataset, construct  a SHACL schema. All node and property shapes should have understandable IRIs and be given by reference.
```

The output of this property is a SHACL 1.1 schema (change to SHACL 1.2 in the prompt to get a more refined version of same).

```
#DC SHACL Shapes for DC Universe Characters Ontology

@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix dc: <http://example.org/dc-universe/> .
@prefix dcc: <http://example.org/dc-universe/character/> .
@prefix dcp: <http://example.org/dc-universe/power/> .
@prefix dcl: <http://example.org/dc-universe/location/> .
@prefix dcg: <http://example.org/dc-universe/gender/> .
@prefix dco: <http://example.org/dc-universe/organization/> .
@prefix dcsh: <http://example.org/dc-universe/shapes/> .

# =============================================================================
# SHACL SHAPES FOR DC UNIVERSE ONTOLOGY
# =============================================================================

# =============================================================================
# NODE SHAPES - Core Classes
# =============================================================================

# -----------------------------------------------------------------------------
# Character Shape (Base shape for all characters)
# -----------------------------------------------------------------------------
dcsh:CharacterShape a sh:NodeShape ;
    sh:targetClass dc:Character ;
    rdfs:label “Character Shape” ;
    rdfs:comment “Validates instances of dc:Character” ;
    sh:property dcsh:CharacterShape-label ;
    sh:property dcsh:CharacterShape-hasGender ;
    sh:property dcsh:CharacterShape-hasAge ;
    sh:property dcsh:CharacterShape-hasAppearance ;
    sh:property dcsh:CharacterShape-locatedIn ;
    sh:property dcsh:CharacterShape-hasLoveInterest ;
    sh:property dcsh:CharacterShape-hasAntagonist ;
    sh:property dcsh:CharacterShape-memberOf ;
    sh:property dcsh:CharacterShape-realName ;
    sh:property dcsh:CharacterShape-alias .

# -----------------------------------------------------------------------------
# Hero Shape
# -----------------------------------------------------------------------------
dcsh:HeroShape a sh:NodeShape ;
    sh:targetClass dc:Hero ;
    rdfs:label “Hero Shape” ;
    rdfs:comment “Validates instances of dc:Hero” ;
    sh:property dcsh:CharacterShape-label ;
    sh:property dcsh:CharacterShape-hasGender ;
    sh:property dcsh:CharacterShape-hasAge ;
    sh:property dcsh:CharacterShape-hasAppearance ;
    sh:property dcsh:HeroShape-hasPower ;
    sh:property dcsh:CharacterShape-locatedIn ;
    sh:property dcsh:CharacterShape-hasLoveInterest ;
    sh:property dcsh:CharacterShape-hasAntagonist ;
    sh:property dcsh:HeroShape-memberOf ;
    sh:property dcsh:CharacterShape-realName ;
    sh:property dcsh:CharacterShape-alias .

# -----------------------------------------------------------------------------
# Villain Shape
# -----------------------------------------------------------------------------
dcsh:VillainShape a sh:NodeShape ;
    sh:targetClass dc:Villain ;
    rdfs:label “Villain Shape” ;
    rdfs:comment “Validates instances of dc:Villain” ;
    sh:property dcsh:CharacterShape-label ;
    sh:property dcsh:CharacterShape-hasGender ;
    sh:property dcsh:CharacterShape-hasAge ;
    sh:property dcsh:CharacterShape-hasAppearance ;
    sh:property dcsh:VillainShape-hasPower ;
    sh:property dcsh:CharacterShape-locatedIn ;
    sh:property dcsh:CharacterShape-hasLoveInterest ;
    sh:property dcsh:VillainShape-hasAntagonist ;
    sh:property dcsh:VillainShape-memberOf ;
    sh:property dcsh:CharacterShape-realName ;
    sh:property dcsh:CharacterShape-alias .

# -----------------------------------------------------------------------------
# Anti-Hero Shape
# -----------------------------------------------------------------------------
dcsh:AntiHeroShape a sh:NodeShape ;
    sh:targetClass dc:AntiHero ;
    rdfs:label “Anti-Hero Shape” ;
    rdfs:comment “Validates instances of dc:AntiHero” ;
    sh:property dcsh:CharacterShape-label ;
    sh:property dcsh:CharacterShape-hasGender ;
    sh:property dcsh:CharacterShape-hasAge ;
    sh:property dcsh:CharacterShape-hasAppearance ;
    sh:property dcsh:AntiHeroShape-hasPower ;
    sh:property dcsh:CharacterShape-locatedIn ;
    sh:property dcsh:CharacterShape-hasLoveInterest ;
    sh:property dcsh:CharacterShape-hasAntagonist ;
    sh:property dcsh:CharacterShape-memberOf ;
    sh:property dcsh:CharacterShape-realName ;
    sh:property dcsh:CharacterShape-alias .

# -----------------------------------------------------------------------------
# Gender Shape
# -----------------------------------------------------------------------------
dcsh:GenderShape a sh:NodeShape ;
    sh:targetClass dc:Gender ;
    rdfs:label “Gender Shape” ;
    rdfs:comment “Validates instances of dc:Gender” ;
    sh:property dcsh:GenderShape-label ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type rdfs:label ) .

# -----------------------------------------------------------------------------
# Superpower Shape
# -----------------------------------------------------------------------------
dcsh:SuperpowerShape a sh:NodeShape ;
    sh:targetClass dc:Superpower ;
    rdfs:label “Superpower Shape” ;
    rdfs:comment “Validates instances of dc:Superpower” ;
    sh:property dcsh:SuperpowerShape-label ;
    sh:property dcsh:SuperpowerShape-comment .

# -----------------------------------------------------------------------------
# Location Shape
# -----------------------------------------------------------------------------
dcsh:LocationShape a sh:NodeShape ;
    sh:targetClass dc:Location ;
    rdfs:label “Location Shape” ;
    rdfs:comment “Validates instances of dc:Location” ;
    sh:property dcsh:LocationShape-label ;
    sh:property dcsh:LocationShape-comment .

# -----------------------------------------------------------------------------
# Organization Shape
# -----------------------------------------------------------------------------
dcsh:OrganizationShape a sh:NodeShape ;
    sh:targetClass dc:Organization ;
    rdfs:label “Organization Shape” ;
    rdfs:comment “Validates instances of dc:Organization” ;
    sh:property dcsh:OrganizationShape-label ;
    sh:property dcsh:OrganizationShape-comment .

# =============================================================================
# PROPERTY SHAPES - Character Properties
# =============================================================================

# -----------------------------------------------------------------------------
# Label Property Shape (reusable)
# -----------------------------------------------------------------------------
dcsh:CharacterShape-label a sh:PropertyShape ;
    rdfs:label “Character Label Property Shape” ;
    rdfs:comment “Every character must have exactly one rdfs:label” ;
    sh:path rdfs:label ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:minLength 1 ;
    sh:message “Character must have exactly one non-empty label” .

# -----------------------------------------------------------------------------
# Gender Property Shape
# -----------------------------------------------------------------------------
dcsh:CharacterShape-hasGender a sh:PropertyShape ;
    rdfs:label “Character Gender Property Shape” ;
    rdfs:comment “Character gender must reference a valid dc:Gender instance” ;
    sh:path dc:hasGender ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:node dcsh:GenderValueShape ;
    sh:message “Character must have exactly one gender from the defined gender values” .

dcsh:GenderValueShape a sh:NodeShape ;
    rdfs:label “Gender Value Shape” ;
    rdfs:comment “Validates that gender values are from the allowed set” ;
    sh:in ( dcg:Male dcg:Female ) ;
    sh:message “Gender must be either dcg:Male or dcg:Female” .

# -----------------------------------------------------------------------------
# Age Property Shape
# -----------------------------------------------------------------------------
dcsh:CharacterShape-hasAge a sh:PropertyShape ;
    rdfs:label “Character Age Property Shape” ;
    rdfs:comment “Character age is a string describing relative age” ;
    sh:path dc:hasAge ;
    sh:datatype xsd:string ;
    sh:minCount 0 ;
    sh:maxCount 1 ;
    sh:minLength 5 ;
    sh:message “Age must be a descriptive string of at least 5 characters” .

# -----------------------------------------------------------------------------
# Appearance Property Shape
# -----------------------------------------------------------------------------
dcsh:CharacterShape-hasAppearance a sh:PropertyShape ;
    rdfs:label “Character Appearance Property Shape” ;
    rdfs:comment “Character appearance is a descriptive string” ;
    sh:path dc:hasAppearance ;
    sh:datatype xsd:string ;
    sh:minCount 0 ;
    sh:maxCount 1 ;
    sh:minLength 20 ;
    sh:message “Appearance must be a descriptive string of at least 20 characters” .

# -----------------------------------------------------------------------------
# Real Name Property Shape
# -----------------------------------------------------------------------------
dcsh:CharacterShape-realName a sh:PropertyShape ;
    rdfs:label “Character Real Name Property Shape” ;
    rdfs:comment “Character’s real/civilian name” ;
    sh:path dc:realName ;
    sh:datatype xsd:string ;
    sh:minCount 0 ;
    sh:maxCount 1 ;
    sh:minLength 1 ;
    sh:message “Real name must be a non-empty string” .

# -----------------------------------------------------------------------------
# Alias Property Shape
# -----------------------------------------------------------------------------
dcsh:CharacterShape-alias a sh:PropertyShape ;
    rdfs:label “Character Alias Property Shape” ;
    rdfs:comment “Character may have multiple aliases or nicknames” ;
    sh:path dc:alias ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
    sh:message “Each alias must be a non-empty string” .

# -----------------------------------------------------------------------------
# Located In Property Shape
# -----------------------------------------------------------------------------
dcsh:CharacterShape-locatedIn a sh:PropertyShape ;
    rdfs:label “Character Location Property Shape” ;
    rdfs:comment “Character location must reference valid dc:Location instances” ;
    sh:path dc:locatedIn ;
    sh:node dcsh:LocationReferenceShape ;
    sh:message “Location must be a valid dc:Location instance” .

dcsh:LocationReferenceShape a sh:NodeShape ;
    rdfs:label “Location Reference Shape” ;
    rdfs:comment “Validates references to Location instances” ;
    sh:class dc:Location ;
    sh:message “Referenced location must be an instance of dc:Location” .

# -----------------------------------------------------------------------------
# Love Interest Property Shape
# -----------------------------------------------------------------------------
dcsh:CharacterShape-hasLoveInterest a sh:PropertyShape ;
    rdfs:label “Character Love Interest Property Shape” ;
    rdfs:comment “Love interest must reference valid dc:Character instances” ;
    sh:path dc:hasLoveInterest ;
    sh:node dcsh:CharacterReferenceShape ;
    sh:message “Love interest must be a valid dc:Character instance” .

dcsh:CharacterReferenceShape a sh:NodeShape ;
    rdfs:label “Character Reference Shape” ;
    rdfs:comment “Validates references to Character instances” ;
    sh:or (
        [ sh:class dc:Character ]
        [ sh:class dc:Hero ]
        [ sh:class dc:Villain ]
        [ sh:class dc:AntiHero ]
    ) ;
    sh:message “Referenced character must be an instance of dc:Character or its subclasses” .

# -----------------------------------------------------------------------------
# Antagonist Property Shape
# -----------------------------------------------------------------------------
dcsh:CharacterShape-hasAntagonist a sh:PropertyShape ;
    rdfs:label “Character Antagonist Property Shape” ;
    rdfs:comment “Antagonist must reference valid dc:Character instances” ;
    sh:path dc:hasAntagonist ;
    sh:node dcsh:CharacterReferenceShape ;
    sh:message “Antagonist must be a valid dc:Character instance” .

# -----------------------------------------------------------------------------
# Member Of Property Shape
# -----------------------------------------------------------------------------
dcsh:CharacterShape-memberOf a sh:PropertyShape ;
    rdfs:label “Character Organization Membership Property Shape” ;
    rdfs:comment “Organization membership must reference valid dc:Organization instances” ;
    sh:path dc:memberOf ;
    sh:node dcsh:OrganizationReferenceShape ;
    sh:message “Organization must be a valid dc:Organization instance” .

dcsh:OrganizationReferenceShape a sh:NodeShape ;
    rdfs:label “Organization Reference Shape” ;
    rdfs:comment “Validates references to Organization instances” ;
    sh:class dc:Organization ;
    sh:message “Referenced organization must be an instance of dc:Organization” .

# =============================================================================
# PROPERTY SHAPES - Hero-Specific
# =============================================================================

dcsh:HeroShape-hasPower a sh:PropertyShape ;
    rdfs:label “Hero Superpower Property Shape” ;
    rdfs:comment “Heroes must have at least one superpower” ;
    sh:path dc:hasPower ;
    sh:minCount 1 ;
    sh:node dcsh:SuperpowerReferenceShape ;
    sh:message “Hero must have at least one valid superpower” .

dcsh:HeroShape-memberOf a sh:PropertyShape ;
    rdfs:label “Hero Organization Membership Property Shape” ;
    rdfs:comment “Heroes should belong to at least one organization” ;
    sh:path dc:memberOf ;
    sh:minCount 1 ;
    sh:node dcsh:OrganizationReferenceShape ;
    sh:severity sh:Warning ;
    sh:message “Hero should belong to at least one organization” .

dcsh:SuperpowerReferenceShape a sh:NodeShape ;
    rdfs:label “Superpower Reference Shape” ;
    rdfs:comment “Validates references to Superpower instances” ;
    sh:class dc:Superpower ;
    sh:message “Referenced superpower must be an instance of dc:Superpower” .

# =============================================================================
# PROPERTY SHAPES - Villain-Specific
# =============================================================================

dcsh:VillainShape-hasPower a sh:PropertyShape ;
    rdfs:label “Villain Superpower Property Shape” ;
    rdfs:comment “Villains typically have at least one superpower or ability” ;
    sh:path dc:hasPower ;
    sh:minCount 1 ;
    sh:node dcsh:SuperpowerReferenceShape ;
    sh:message “Villain must have at least one valid superpower or ability” .

dcsh:VillainShape-hasAntagonist a sh:PropertyShape ;
    rdfs:label “Villain Antagonist Property Shape” ;
    rdfs:comment “Villains should have at least one hero antagonist” ;
    sh:path dc:hasAntagonist ;
    sh:minCount 1 ;
    sh:node dcsh:CharacterReferenceShape ;
    sh:severity sh:Warning ;
    sh:message “Villain should have at least one antagonist (hero they oppose)” .

dcsh:VillainShape-memberOf a sh:PropertyShape ;
    rdfs:label “Villain Organization Membership Property Shape” ;
    rdfs:comment “Villain organization memberships” ;
    sh:path dc:memberOf ;
    sh:node dcsh:OrganizationReferenceShape ;
    sh:message “Organization must be a valid dc:Organization instance” .

# =============================================================================
# PROPERTY SHAPES - Anti-Hero-Specific
# =============================================================================

dcsh:AntiHeroShape-hasPower a sh:PropertyShape ;
    rdfs:label “Anti-Hero Superpower Property Shape” ;
    rdfs:comment “Anti-Heroes may have superpowers” ;
    sh:path dc:hasPower ;
    sh:node dcsh:SuperpowerReferenceShape ;
    sh:message “If present, superpower must be a valid dc:Superpower instance” .

# =============================================================================
# PROPERTY SHAPES - Gender Class
# =============================================================================

dcsh:GenderShape-label a sh:PropertyShape ;
    rdfs:label “Gender Label Property Shape” ;
    rdfs:comment “Gender must have exactly one label” ;
    sh:path rdfs:label ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message “Gender must have exactly one label” .

# =============================================================================
# PROPERTY SHAPES - Superpower Class
# =============================================================================

dcsh:SuperpowerShape-label a sh:PropertyShape ;
    rdfs:label “Superpower Label Property Shape” ;
    rdfs:comment “Superpower must have exactly one label” ;
    sh:path rdfs:label ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message “Superpower must have exactly one label” .

dcsh:SuperpowerShape-comment a sh:PropertyShape ;
    rdfs:label “Superpower Comment Property Shape” ;
    rdfs:comment “Superpower should have a description” ;
    sh:path rdfs:comment ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:minLength 10 ;
    sh:severity sh:Warning ;
    sh:message “Superpower should have a descriptive comment of at least 10 characters” .

# =============================================================================
# PROPERTY SHAPES - Location Class
# =============================================================================

dcsh:LocationShape-label a sh:PropertyShape ;
    rdfs:label “Location Label Property Shape” ;
    rdfs:comment “Location must have exactly one label” ;
    sh:path rdfs:label ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message “Location must have exactly one label” .

dcsh:LocationShape-comment a sh:PropertyShape ;
    rdfs:label “Location Comment Property Shape” ;
    rdfs:comment “Location should have a description” ;
    sh:path rdfs:comment ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:minLength 10 ;
    sh:severity sh:Warning ;
    sh:message “Location should have a descriptive comment of at least 10 characters” .

# =============================================================================
# PROPERTY SHAPES - Organization Class
# =============================================================================

dcsh:OrganizationShape-label a sh:PropertyShape ;
    rdfs:label “Organization Label Property Shape” ;
    rdfs:comment “Organization must have exactly one label” ;
    sh:path rdfs:label ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message “Organization must have exactly one label” .

dcsh:OrganizationShape-comment a sh:PropertyShape ;
    rdfs:label “Organization Comment Property Shape” ;
    rdfs:comment “Organization should have a description” ;
    sh:path rdfs:comment ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:minLength 10 ;
    sh:severity sh:Warning ;
    sh:message “Organization should have a descriptive comment of at least 10 characters” .

# =============================================================================
# SPARQL-BASED CONSTRAINTS
# =============================================================================

# -----------------------------------------------------------------------------
# Antagonist Reciprocity Check (Warning)
# -----------------------------------------------------------------------------
dcsh:AntagonistReciprocityShape a sh:NodeShape ;
    sh:targetSubjectsOf dc:hasAntagonist ;
    rdfs:label “Antagonist Reciprocity Shape” ;
    rdfs:comment “Checks if antagonist relationships are reciprocal” ;
    sh:severity sh:Info ;
    sh:sparql dcsh:AntagonistReciprocityConstraint .

dcsh:AntagonistReciprocityConstraint a sh:SPARQLConstraint ;
    rdfs:label “Antagonist Reciprocity Constraint” ;
    sh:message “Character {$this} has antagonist {?antagonist} but the relationship is not reciprocal” ;
    sh:severity sh:Info ;
    sh:prefixes [
        sh:declare [ sh:prefix “dc” ; sh:namespace “http://example.org/dc-universe/”^^xsd:anyURI ]
    ] ;
    sh:select “”“
        SELECT $this ?antagonist
        WHERE {
            $this dc:hasAntagonist ?antagonist .
            FILTER NOT EXISTS { ?antagonist dc:hasAntagonist $this }
        }
    “”“ .


# =============================================================================
# ENUMERATION CONSTRAINTS
# =============================================================================

# -----------------------------------------------------------------------------
# Valid Powers Enumeration Shape
# -----------------------------------------------------------------------------
dcsh:ValidPowersShape a sh:NodeShape ;
    sh:targetObjectsOf dc:hasPower ;
    rdfs:label “Valid Powers Enumeration Shape” ;
    rdfs:comment “Ensures hasPower only references defined superpowers” ;
    sh:in (
        dcp:SuperStrength dcp:Flight dcp:HeatVision dcp:XRayVision
        dcp:Invulnerability dcp:SuperSpeed dcp:FreezeBreath dcp:MartialArts
        dcp:DetectiveSkills dcp:Stealth dcp:Gadgetry dcp:Telepathy
        dcp:AquaticAbilities dcp:MarineTelepathy dcp:SpeedForceConnection
        dcp:TimeTravel dcp:Phasing dcp:PowerRing dcp:HardLightConstructs
        dcp:Acrobatics dcp:EideticMemory dcp:Hacking dcp:GeniusIntellect
        dcp:PoweredArmor dcp:Immortality dcp:OmegaBeams dcp:OmegaEffect
        dcp:CheetahSpeed dcp:Claws dcp:EnhancedSenses dcp:UnderwaterCombat
        dcp:AdvancedTechnology dcp:Whip dcp:Thievery dcp:Psychology
        dcp:ChaosManipulation dcp:AmazonianTraining dcp:LassoOfTruth
        dcp:Bracelets dcp:DivineBlessing
        dcp:Cybernetics dcp:TechnologicalInterface dcp:SonicScream
        dcp:Magic dcp:Sorcery dcp:BackwardsSpeech dcp:EnhancedReflexes
        dcp:RegenerativeHealing dcp:TacticalGenius dcp:WeaponsMaster
        dcp:Shapeshifting dcp:MindControl dcp:EnergyProjection
    ) ;
    sh:message “Power must be one of the defined dc:Superpower instances” .

# -----------------------------------------------------------------------------
# Valid Locations Enumeration Shape
# -----------------------------------------------------------------------------
dcsh:ValidLocationsShape a sh:NodeShape ;
    sh:targetObjectsOf dc:locatedIn ;
    rdfs:label “Valid Locations Enumeration Shape” ;
    rdfs:comment “Ensures locatedIn only references defined locations” ;
    sh:in (
        dcl:Metropolis dcl:Gotham dcl:Themyscira dcl:Atlantis
        dcl:CentralCity dcl:CoastCity dcl:Oa dcl:Apokolips
        dcl:NationalCity dcl:ArkhamAsylum dcl:LexCorpTower dcl:BelleReve
        dcl:Detroit dcl:Shadowcrest dcl:StarCity dcl:Aeaea
    ) ;
    sh:message “Location must be one of the defined dc:Location instances” .

# -----------------------------------------------------------------------------
# Valid Organizations Enumeration Shape
# -----------------------------------------------------------------------------
dcsh:ValidOrganizationsShape a sh:NodeShape ;
    sh:targetObjectsOf dc:memberOf ;
    rdfs:label “Valid Organizations Enumeration Shape” ;
    rdfs:comment “Ensures memberOf only references defined organizations” ;
    sh:in (
        dco:JusticeLeague dco:BatFamily dco:Amazons dco:GreenLanternCorps
        dco:LegionOfDoom dco:SuicideSquad dco:LexCorp dco:SecretSociety
        dco:DarksidesElite dco:BirdsOfPrey dco:BlackMantaMilitia dco:GothamCitySirens
        dco:TeenTitans dco:JusticeSociety dco:ShadowpactAllies dco:HiveOrganization
    ) ;
    sh:message “Organization must be one of the defined dc:Organization instances” .
```

This is a sound skeletal schema. It infers cardinality relationships, establishes constraints about what is allowed vs non-allowed enumerations, incorporates appropriate metadata, including error messages, and uses SHACL-SPARQL constructs that can in turn be used to inform SPARQL queries down the road.

It is worth taking the time to check these validations. This provides a considerably richer schema and can also be used to validate the broader dataset.

If you have a SHACL 1.2 validator, it may be worth generating SHACL 1.2. A sample of this can be seen as follows (for a node expression):

```
dcsh:HeroHasVillainAntagonistExpression a sh:NodeExpression ;
    rdfs:label “Hero Has Villain Antagonist Expression” ;
    rdfs:comment “SHACL 1.2 node expression: checks that heroes have at least one villain antagonist” ;
    sh:message “Hero should have at least one villain as antagonist” ;
    sh:severity sh:Info ;
    # sh:exists returns true if the nested expression yields at least one node
    sh:exists [
        a sh:NodeExpression ;
        # sh:nodes navigates from focus node along a path
        sh:nodes [ sh:path dc:hasAntagonist ] ;
        # sh:filterShape filters to only nodes matching the shape
        sh:filterShape [ sh:class dc:Villain ]
    ] .
```

If you have the information in files or a triple store that supports validation, you should test it against your dataset to determine whether any violations occur. Note that the goal here is not to test the dataset itself, but rather to calibrate the schema so that it validates properly.

## Creating SPARQL from SHACL and Claude

Once you are comfortable with the SHACL, you use it with Claude to generate a SPARQL statement from a prompt:

```
Based solely on the Dc characters SHACL, create a SPARQL query that will answer the question: “Which character has the greatest number of connections, either as a love interest, a foe, or a member of the same organizations as the character?”
```

This generates the following SPARQL file:

```
# =============================================================================
# SPARQL Query: Character with Greatest Number of Connections
# Derived from: dc-characters-shacl.ttl
# =============================================================================
#
# Property paths derived from SHACL PropertyShapes:
#   - dcsh:CharacterShape-hasLoveInterest → dc:hasLoveInterest → dc:Character
#   - dcsh:CharacterShape-hasAntagonist   → dc:hasAntagonist   → dc:Character
#   - dcsh:CharacterShape-memberOf        → dc:memberOf        → dc:Organization
#
# Connections are counted as:
#   1. Love interests (bidirectional - either direction counts)
#   2. Foes/antagonists (bidirectional - either direction counts)
#   3. Co-members of shared organizations (other characters in same org)
#
# Each unique connected character is counted once per relationship type.
# =============================================================================

PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc:   <http://example.org/dc-universe/>
PREFIX dcc:  <http://example.org/dc-universe/character/>
PREFIX dco:  <http://example.org/dc-universe/organization/>

SELECT ?character ?characterName 
       ?loveInterestCount 
       ?foeCount 
       ?orgMemberCount 
       (?loveInterestCount + ?foeCount + ?orgMemberCount AS ?totalConnections)
WHERE {
    # Get all characters with labels
    ?character rdfs:label ?characterName .
    
    # Ensure it’s a character (has gender per dcsh:CharacterShape-hasGender)
    ?character dc:hasGender ?gender .
    
    # -------------------------------------------------------------------------
    # Subquery 1: Count Love Interest connections (bidirectional)
    # From dcsh:CharacterShape-hasLoveInterest
    # -------------------------------------------------------------------------
    {
        SELECT ?character (COUNT(DISTINCT ?loveConnection) AS ?loveInterestCount)
        WHERE {
            ?character dc:hasGender ?g .
            OPTIONAL {
                {
                    # Character has someone as love interest
                    ?character dc:hasLoveInterest ?loveConnection .
                }
                UNION
                {
                    # Someone has character as love interest
                    ?loveConnection dc:hasLoveInterest ?character .
                }
            }
        }
        GROUP BY ?character
    }
    
    # -------------------------------------------------------------------------
    # Subquery 2: Count Foe/Antagonist connections (bidirectional)
    # From dcsh:CharacterShape-hasAntagonist
    # -------------------------------------------------------------------------
    {
        SELECT ?character (COUNT(DISTINCT ?foeConnection) AS ?foeCount)
        WHERE {
            ?character dc:hasGender ?g .
            OPTIONAL {
                {
                    # Character has someone as antagonist
                    ?character dc:hasAntagonist ?foeConnection .
                }
                UNION
                {
                    # Someone has character as antagonist
                    ?foeConnection dc:hasAntagonist ?character .
                }
            }
        }
        GROUP BY ?character
    }
    
    # -------------------------------------------------------------------------
    # Subquery 3: Count co-members in shared organizations
    # From dcsh:CharacterShape-memberOf
    # -------------------------------------------------------------------------
    {
        SELECT ?character (COUNT(DISTINCT ?orgMember) AS ?orgMemberCount)
        WHERE {
            ?character dc:hasGender ?g .
            OPTIONAL {
                ?character dc:memberOf ?organization .
                ?orgMember dc:memberOf ?organization .
                FILTER(?orgMember != ?character)
            }
        }
        GROUP BY ?character
    }
}
ORDER BY DESC(?totalConnections) ?characterName
LIMIT 20
```

This query can then be applied directly to the triplestore or to a file. For the sample dataset, this might produce a result like the following:

[

![](https://substackcdn.com/image/fetch/$s_!5_Xm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9675500-e01d-40fc-8990-910635721120_750x336.png)

](https://substackcdn.com/image/fetch/$s_!5_Xm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9675500-e01d-40fc-8990-910635721120_750x336.png)

## Summary

There are several points worth noting.

-   You develop the SHACL schema once (though you may augment it), in effect by training it with the raw data coming from the data set.
    
-   You create a SPARQL query with the SHACL once for every AI prompt. In this case, the SHACL tells the LLM the structure of the knowledge graph, and can use that information to then create a prompt that matches the output.
    
-   The SPARQL can then be applied procedurally to the broader graph, bypassing the AI.
    
-   At no time is the knowledge graph itself loaded into the AI context via LangChain; only the query results are. This keeps the active context small and manageable, and significantly reduces the overhead for RAG.
    
-   Once you have the SHACL, the source data can be anything - a table, a PDF file, an LLM, an image, etc., because you can use the SHACL to create an intermediate RDF turtle file that acts as your triple store source.
    
-   Note that if you have an existing SHACL file that you want to map to, this can go a long way toward building a general queryable system: the data file can be converted into RDF using SHACL and uploaded to an existing triple store. The SHACL can be used to generate a relevant query across the entire data store to identify additional connections.
    
-   Because you’re not actually querying the LLM for data, the token cost is pretty minimal - a one-time cost for the schema, a cost for translating non-RDF data into turtle using that schema (if necessary), and a one-time cost per query (part of which may be recouped if you can parameterise that query).
    
-   Finally, if the output of this is a data graph or table, there is no need to transform the production through the LLM; what is returned is a high-accuracy data structure. Certainly, you can apply post-transformers (such as JSON filters, XSLT converters, or, of course, LLMs) to the resulting data, but this is likely to yield data with very good fidelity compared to an LLM, with a predictable structure and a mechanism for structural validation.
    

In media res,

[

![](https://substackcdn.com/image/fetch/$s_!6je6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e0b3562-5616-4609-a78e-c599a5f2d577_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!6je6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e0b3562-5616-4609-a78e-c599a5f2d577_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.