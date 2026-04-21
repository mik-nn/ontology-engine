---
title: "Lions and Tigers and Bears, Oh My!"
source: "https://ontologist.substack.com/p/lions-and-tigers-and-bears-oh-my?utm_source=profile&utm_medium=reader2"
date: "Feb 26"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!TQGs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd517dc1-3d05-4960-a2b4-1f2d4cdcdbff_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!TQGs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd517dc1-3d05-4960-a2b4-1f2d4cdcdbff_2688x1536.jpeg)

This post is a catch-all of ideas I’ve been exploring as I spend more time examining the implications of SHACL and RDF-Star. Nothing profound, just some practical applications.

## Expressing Units

One of the more problematic issues of working with measures and values. There are several approaches you can take to do so. For instance, if you want to say that Jane Doe has a height of 158 cm (5’2” and change), there are a few different ways of expressing this.

Use nothing, and make sure all heights are stored as centimetres:

```
Person:JaneDoe a Class:Person ;
     Person:hasHeight "158"^^xsd:decimal ;
     .
```

While this is the simplest form, it makes a huge unstated assumption - everyone will know that this is in the unit of centimetres, which is far from guaranteed.

A second approach is to use a blank node:

```
Person:JaneDoe a Class:Person ;
     Person:hasHeight [
         height:hasValue "158"^^xsd:decimal ;
         height:hasUnits Unit:Centimetre ;
         ] ;
     .
```

This approach works, but it also means that you have to create a special property for height, another for length, another for temperature and so forth, and it adds a step in queries that you have to resolve. It can also be somewhat confusing, especially if you’re not used to dealing with blank nodes (which many people find uncomfortable).

The third approach is to use the datatype to express the units:

```
 Person:JaneDoe a Class:Person ;
     Person:hasHeight "158"^^Unit:Centimetre ;
     .
```

Then include the datatype “xd:decimal” in the definition of `Unit:Centimetre`.

I have advocated this form myself, but the problem with it is that you have to dereference the datatype to get the IRI for the type itself, and it makes determining the core datatype (here `xsd:decimal`) more complex. Additionally, many triple stores use atomic values to optimise storage, and by storing units in a database, you lose this optimisation. It’s also not a widely used convention.

As it turns out, however, with RDF-Star, you can also make use of a reification to store this information:

```
Person:JaneDoe Person:hasHeight "158^^xsd:decimal ~ {|
       measure:hasUnitType unit:Centimetres;
       |}
```

The ~ {| |} expression indicates a reification, without specifying a specific reification identifier. This is equivalent to:

```
Person:JaneDoe Person:hasHeight "158^^xsd:decimal .
<<Person:JaneDoe Person:hasHeight "158^^xsd:decimal>>
       measure:hasUnitType unit:Centimetres;
       .
```

The ~ {| |} does one other thing - it asserts the original statement, not just the reification, so you don’t have to include both. The < < > > creates a reified triple, meaning that it’s not specifically added to the triple store, but you often want to do both, as in the example above.

This can be interpreted as “Jane Doe, has a height of 158 units. These units of measure are in centimeters.”

How do we validate this using SHACL? This can be done with either SHACL 1.1 and dash: or with SHACL 1.2:

```
shape:Person_height a sh:PropertyShape ;
      sh:path Person:hasHeight ;
      sh:datatype xsd:decimal ;
      sh:reifierShape shape:Measure ;
     #dash:reifiedBy shape:Measure # (in SHACL 1.1 with dash:)
     .

shape:Measure a sh:NodeShape ;
    sh:targetClass class:Measure ;
    sh:property [
          a sh:PropertyShape; 
          sh:path measure:hasUnitType ;
          sh:class class:Unit ;
          sh:minCount 0;
          sh:maxCount 1;
          ].
```

This indicates that the Person shape has a property shape `shape:Person_height` that indicates the requirement that it has both a datatype of `xsd:decimal` and has `sh:reifierShape` of `shape:Measure` . The `class:Measure` class, in turn, has a property bound to `measure:hasUnitType` that is of class `class:Unit` . The specific unit may then contain additional information, labels, conversion factors and so forth, either home-grown or from a library such as QUTD.

This approach is powerful because it ensures that the annotations adhere to specific rules. It’s likely to be faster than a standard lookup because, upon ingestion, the Turtle 1.2 interpreter can optimise triple terms and their associated reifiers for fast recall, and is likely to be comparable or slightly faster than using a blank node for the same data.

Querying for both values and units is also straightforward with the new notation:

```
select ?person ?height ?unit where {
     ?person Person:hasHeight ?height.
     BIND( <<( ?person Person:hasHeight ?height )>> AS ?measure )
     optional {
        ?measure measure:hasUnitType ?unit.
         }
     }
```

The BIND statement here uses the «( )» notation to indicate a triple term reifier, and is functionally equivalent to the SPARQL TRIPLE(?s,?p,?o) function. In both cases, this returns _all_ reifiers for a given triple.

_Please note: the notation contained for reification herein is still unstable and may change._

## Expressing Subpopulations

I’ve discussed this scenario before, but often you want to qualify a particular statistic, such as a population, with an indication of WHAT and WHEN. Again, you can use reifiers and SHACL:

```
@prefix Country:     <http://example.org/country/> .
@prefix Demographic: <http://example.org/demographic/> .
@prefix gender:      <http://example.org/gender/> .
@prefix ageGroup:    <http://example.org/ageGroup/> .
@prefix xsd:         <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs:        <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf:         <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

# =============================================================================
# Reference Data - Gender
# =============================================================================
gender:Female   a rdfs:Class ; rdfs:label "Female" .
gender:Male     a rdfs:Class ; rdfs:label "Male" .
gender:Unspecified a rdfs:Class ; rdfs:label "Unspecified" .

# =============================================================================
# Reference Data - Age Groups
# =============================================================================
ageGroup:Age0-17        a rdfs:Class ; rdfs:label "Age 0-17" .
ageGroup:Age18-64       a rdfs:Class ; rdfs:label "Age 18-64" .
ageGroup:Age65AndOlder  a rdfs:Class ; rdfs:label "Age 65 and Older" .

# =============================================================================
# Scotland Entity
# =============================================================================
Country:Scotland a Country:Country ;
    rdfs:label "Scotland" .

# =============================================================================
# 2021 Census Data
# =============================================================================

# Total Population 2021
Country:Scotland Country:hasTotalPopulation 5788679 ~Country:Scotland-total-2021 .
Country:Scotland-total-2021 Demographic:hasYear "2021"^^xsd:gYear .

# Gender Breakdown 2021
Country:Scotland Country:hasPopulationByDemographic 2770823 ~Country:Scotland-female-2021 .
Country:Scotland-female-2021
    Demographic:hasYear "2021"^^xsd:gYear ;
    Demographic:hasGender gender:Female ;
    Demographic:hasPercentage 0.4786 .

Country:Scotland Country:hasPopulationByDemographic 2559764 ~Country:Scotland-male-2021 .
Country:Scotland-male-2021
    Demographic:hasYear "2021"^^xsd:gYear ;
    Demographic:hasGender gender:Male ;
    Demographic:hasPercentage 0.4422 .

Country:Scotland Country:hasPopulationByDemographic 458092 ~Country:Scotland-unspecified-2021 .
Country:Scotland-unspecified-2021
    Demographic:hasYear "2021"^^xsd:gYear ;
    Demographic:hasGender gender:Unspecified ;
    Demographic:hasPercentage 0.0791 .

# Age Group Breakdown 2021
Country:Scotland Country:hasPopulationByDemographic 259169 ~Country:Scotland-age0-17-2021 .
Country:Scotland-age0-17-2021
    Demographic:hasYear "2021"^^xsd:gYear ;
    Demographic:hasAgeGroup ageGroup:Age0-17 ;
    Demographic:hasPercentage 0.0448 .

Country:Scotland Country:hasPopulationByDemographic 5269182 ~Country:Scotland-age18-64-2021 .
Country:Scotland-age18-64-2021
    Demographic:hasYear "2021"^^xsd:gYear ;
    Demographic:hasAgeGroup ageGroup:Age18-64 ;
    Demographic:hasPercentage 0.9103 .

Country:Scotland Country:hasPopulationByDemographic 260328 ~Country:Scotland-age65plus-2021 .
Country:Scotland-age65plus-2021
    Demographic:hasYear "2021"^^xsd:gYear ;
    Demographic:hasAgeGroup ageGroup:Age65AndOlder ;
    Demographic:hasPercentage 0.0450 .

# =============================================================================
# 2011 Census Data
# =============================================================================

# Total Population 2011
Country:Scotland Country:hasTotalPopulation 5295403 ~Country:Scotland-total-2011 .
Country:Scotland-total-2011 Demographic:hasYear "2011"^^xsd:gYear .

# Gender Breakdown 2011
# Source: Scotland's Census 2011 - 2,728,000 women (51.5%), 2,567,400 men (48.5%)
Country:Scotland Country:hasPopulationByDemographic 2728000 ~Country:Scotland-female-2011 .
Country:Scotland-female-2011
    Demographic:hasYear "2011"^^xsd:gYear ;
    Demographic:hasGender gender:Female ;
    Demographic:hasPercentage 0.5150 .

Country:Scotland Country:hasPopulationByDemographic 2567400 ~Country:Scotland-male-2011 .
Country:Scotland-male-2011
    Demographic:hasYear "2011"^^xsd:gYear ;
    Demographic:hasGender gender:Male ;
    Demographic:hasPercentage 0.4850 .

# Note: 2011 census did not have "Unspecified" gender category
# Including a zero record for schema completeness
Country:Scotland Country:hasPopulationByDemographic 3 ~Country:Scotland-unspecified-2011 .
Country:Scotland-unspecified-2011
    Demographic:hasYear "2011"^^xsd:gYear ;
    Demographic:hasGender gender:Unspecified ;
    Demographic:hasPercentage 0.0000 .

# Age Group Breakdown 2011
# Derived from Scotland's Census 2011:
#   Under 15: 16.1% (~852,560), 65+: 16.8% (~889,628)
#   Estimated 15-17 as ~3.5% to derive 0-17 (~19.6%) and 18-64 (~63.6%)
#   Source: National Records of Scotland 2011 Census

Country:Scotland Country:hasPopulationByDemographic 1037899 ~Country:Scotland-age0-17-2011 .
Country:Scotland-age0-17-2011
    Demographic:hasYear "2011"^^xsd:gYear ;
    Demographic:hasAgeGroup ageGroup:Age0-17 ;
    Demographic:hasPercentage 0.1960 .

Country:Scotland Country:hasPopulationByDemographic 3367876 ~Country:Scotland-age18-64-2011 .
Country:Scotland-age18-64-2011
    Demographic:hasYear "2011"^^xsd:gYear ;
    Demographic:hasAgeGroup ageGroup:Age18-64 ;
    Demographic:hasPercentage 0.6360 .

Country:Scotland Country:hasPopulationByDemographic 889628 ~Country:Scotland-age65plus-2011 .
Country:Scotland-age65plus-2011
    Demographic:hasYear "2011"^^xsd:gYear ;
    Demographic:hasAgeGroup ageGroup:Age65AndOlder ;
    Demographic:hasPercentage 0.1680 .
```

This makes use of two distinct properties - `Country:hasTotalPopulation` and `Country:hasPopulationByDemographic` . The Demographic class contains various categorisations, including `Demographic:hasGender` and `Demographic:hasAgeGroup`, as well as specifying the year of the survey and the percentage calculation for each subpopulation, which for a given demographic, should total 100% (give or take a bit in rounding errors from the source).

Note, as is typically the case, it is possible to model Demographic so that it is a stand-alone class, but in this case, the organisation as an annotation makes it clearer about what is going on.

The SHACL that validates this shape is given as follows:

```
@prefix sh:         <http://www.w3.org/ns/shacl#> .
@prefix xsd:        <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:       <http://www.w3.org/2000/01/rdf-schema#> .
@prefix Country:    <http://example.org/country/> .
@prefix Demographic: <http://example.org/demographic/> .
@prefix gender:     <http://example.org/gender/> .
@prefix ageGroup:   <http://example.org/ageGroup/> .

# =============================================================================
# SHACL 1.2 Schema for Population Demographics with RDF-star Annotations
# =============================================================================

# -----------------------------------------------------------------------------
# Shape for Country entities
# -----------------------------------------------------------------------------
Country:CountryShape
    a sh:NodeShape ;
    sh:targetSubjectsOf Country:hasPopulationByDemographic, Country:hasTotalPopulation ;
    rdfs:label "Country Shape" ;
    rdfs:comment "Validates country entities with population demographic data." ;
    sh:property Country:CountryShape-hasPopulationByDemographic ;
    sh:property Country:CountryShape-hasTotalPopulation ;
.

# -----------------------------------------------------------------------------
# Property shape for hasPopulationByDemographic with reifier validation
# -----------------------------------------------------------------------------
Country:CountryShape-hasPopulationByDemographic
    a sh:PropertyShape ;
    sh:path Country:hasPopulationByDemographic ;
    sh:name "population by demographic" ;
    sh:description "Population count for a specific demographic group." ;
    sh:datatype xsd:integer ;
    sh:minInclusive 0 ;
    # Validate the RDF-star annotation (reifier) on each triple
    sh:reifierShape Demographic:DemographicAnnotationShape ;
.

# -----------------------------------------------------------------------------
# Property shape for hasTotalPopulation with reifier validation  
# -----------------------------------------------------------------------------
Country:CountryShape-hasTotalPopulation
    a sh:PropertyShape ;
    sh:path Country:hasTotalPopulation ;
    sh:name "total population" ;
    sh:description "Total population count for a given year." ;
    sh:datatype xsd:integer ;
    sh:minInclusive 0 ;
    # Validate the RDF-star annotation (reifier) on each triple
    sh:reifierShape Demographic:TotalPopulationAnnotationShape ;
.

# -----------------------------------------------------------------------------
# Node shape for demographic annotations (reifiers)
# Enforces that only ONE classification type can be present at a time
# -----------------------------------------------------------------------------
Demographic:DemographicAnnotationShape
    a sh:NodeShape ;
    rdfs:label "Demographic Annotation Shape" ;
    rdfs:comment "Validates demographic annotations on population triples. Ensures only one classification type (gender OR age group) is present." ;
    
    # Required: must have a year
    sh:property Demographic:DemographicAnnotationShape-hasYear ;
    
    # Required: must have a percentage
    sh:property Demographic:DemographicAnnotationShape-hasPercentage ;
    
    # CRITICAL: Exactly one classification type constraint
    # Uses sh:xone to ensure mutual exclusivity - either gender OR age group, not both
    sh:xone (
        Demographic:HasGenderOnlyShape
        Demographic:HasAgeGroupOnlyShape
    ) ;
.

# -----------------------------------------------------------------------------
# Shape requiring ONLY gender classification (no age group)
# -----------------------------------------------------------------------------
Demographic:HasGenderOnlyShape
    a sh:NodeShape ;
    rdfs:label "Gender Classification Only" ;
    rdfs:comment "Shape for demographic entries classified by gender only." ;
    sh:property [
        sh:path Demographic:hasGender ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( gender:Female gender:Male gender:Unspecified ) ;
        sh:name "gender" ;
        sh:description "Gender classification for the demographic group." ;
    ] ;
    sh:property [
        sh:path Demographic:hasAgeGroup ;
        sh:maxCount 0 ;  # Explicitly forbid age group when gender is present
    ] ;
.

# -----------------------------------------------------------------------------
# Shape requiring ONLY age group classification (no gender)
# -----------------------------------------------------------------------------
Demographic:HasAgeGroupOnlyShape
    a sh:NodeShape ;
    rdfs:label "Age Group Classification Only" ;
    rdfs:comment "Shape for demographic entries classified by age group only." ;
    sh:property [
        sh:path Demographic:hasAgeGroup ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( ageGroup:Age0-17 ageGroup:Age18-64 ageGroup:Age65AndOlder ) ;
        sh:name "age group" ;
        sh:description "Age group classification for the demographic group." ;
    ] ;
    sh:property [
        sh:path Demographic:hasGender ;
        sh:maxCount 0 ;  # Explicitly forbid gender when age group is present
    ] ;
.

# -----------------------------------------------------------------------------
# Property shape for hasYear
# -----------------------------------------------------------------------------
Demographic:DemographicAnnotationShape-hasYear
    a sh:PropertyShape ;
    sh:path Demographic:hasYear ;
    sh:name "year" ;
    sh:description "The census year for this demographic data point." ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:gYear ;
.

# -----------------------------------------------------------------------------
# Property shape for hasPercentage
# -----------------------------------------------------------------------------
Demographic:DemographicAnnotationShape-hasPercentage
    a sh:PropertyShape ;
    sh:path Demographic:hasPercentage ;
    sh:name "percentage" ;
    sh:description "Percentage of total population for this demographic group in the given year." ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:decimal ;
    sh:minInclusive "0.0"^^xsd:decimal ;
    sh:maxInclusive "1.0"^^xsd:decimal ;
.

# -----------------------------------------------------------------------------
# Node shape for total population annotations (simpler - year only, optional gender)
# -----------------------------------------------------------------------------
Demographic:TotalPopulationAnnotationShape
    a sh:NodeShape ;
    rdfs:label "Total Population Annotation Shape" ;
    rdfs:comment "Validates annotations on total population triples." ;
    sh:property [
        sh:path Demographic:hasYear ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:gYear ;
        sh:name "year" ;
    ] ;
    # Gender is optional on total population (typically Unspecified or omitted)
    sh:property [
        sh:path Demographic:hasGender ;
        sh:maxCount 1 ;
        sh:in ( gender:Female gender:Male gender:Unspecified ) ;
        sh:name "gender" ;
    ] ;
.

# =============================================================================
# SKOS-style vocabulary definitions for Gender and AgeGroup
# =============================================================================

gender:Female
    rdfs:label "Female" ;
    rdfs:comment "Female gender classification." ;
.

gender:Male
    rdfs:label "Male" ;
    rdfs:comment "Male gender classification." ;
.

gender:Unspecified
    rdfs:label "Unspecified" ;
    rdfs:comment "Unspecified or other gender classification." ;
.

ageGroup:Age0-17
    rdfs:label "Age 0-17" ;
    rdfs:comment "Minor age group (children and adolescents)." ;
.

ageGroup:Age18-64
    rdfs:label "Age 18-64" ;
    rdfs:comment "Working age adult group." ;
.

ageGroup:Age65AndOlder
    rdfs:label "Age 65 and Older" ;
    rdfs:comment "Senior age group." ;
.
```

Most of this should be familiar based on a previous SHACL 1.2 article, but there is one point I wanted to focus on:

```
Demographic:DemographicAnnotationShape
    a sh:NodeShape ;
    rdfs:label "Demographic Annotation Shape" ;
    rdfs:comment "Validates demographic annotations on population triples. Ensures only one classification type (gender OR age group) is present." ;
    
    # Required: must have a year
    sh:property Demographic:DemographicAnnotationShape-hasYear ;
    
    # Required: must have a percentage
    sh:property Demographic:DemographicAnnotationShape-hasPercentage ;
    
    # CRITICAL: Exactly one classification type constraint
    # Uses sh:xone to ensure mutual exclusivity - either gender OR age group, not both
    sh:xone (
        Demographic:HasGenderOnlyShape
        Demographic:HasAgeGroupOnlyShape
    ) ;
.
```

Here, exclusivity is managed by sh:xone, which selects one of the demographic shapes from the group (this is roughly equivalent to a disjoint class in OWL). It should be noted that this approach allows you to determine mixed subpopulations. For example, if you want to know the number of women in the 18-64 category, you’d simply multiply the percentages from each demographic together (47.86% \* 91.03% = 43.57%) for the given year.

This can also use the schema to determine this value directly in SPARQL using the reification:

```
PREFIX Country:     <http://example.org/country/>
PREFIX Demographic: <http://example.org/demographic/>
PREFIX gender:      <http://example.org/gender/>
PREFIX ageGroup:    <http://example.org/ageGroup/>
PREFIX xsd:         <http://www.w3.org/2001/XMLSchema#>

SELECT ?country ?year 
       ?genderLabel ?genderPop ?genderPercent
       ?ageGroupLabel ?ageGroupPop ?ageGroupPercent
       ?totalPop
       (xsd:integer(?genderPop * ?ageGroupPop / ?totalPop) AS ?estimatedIntersection)
WHERE {
    # =================================================================
    # INPUT PARAMETERS - Multiple combinations supported
    # =================================================================
    VALUES (?yearParam ?genderParam ?ageGroupParam) {
        ("2021" "Female" "Age 18-64")
        ("2021" "Male"   "Age 18-64")
        ("2011" "Female" "Age 18-64")
    }
    
    # =================================================================
    # Mapping tables
    # =================================================================
    BIND(STRDT(?yearParam, xsd:gYear) AS ?year)
    
    VALUES (?genderLabel ?genderIRI) {
        ("Female"      gender:Female)
        ("Male"        gender:Male)
        ("Unspecified" gender:Unspecified)
    }
    FILTER(?genderLabel = ?genderParam)
    
    VALUES (?ageGroupLabel ?ageGroupIRI) {
        ("Age 0-17"         ageGroup:Age0-17)
        ("Age 18-64"        ageGroup:Age18-64)
        ("Age 65 and Older" ageGroup:Age65AndOlder)
    }
    FILTER(?ageGroupLabel = ?ageGroupParam)
    
    # =================================================================
    # Query patterns
    # =================================================================
    << ?country Country:hasTotalPopulation ?totalPop ~ ?totalReifier >> .
    ?totalReifier Demographic:hasYear ?year .
    
    << ?country Country:hasPopulationByDemographic ?genderPop ~ ?genderReifier >> .
    ?genderReifier Demographic:hasYear ?year ;
                   Demographic:hasGender ?genderIRI ;
                   Demographic:hasPercentage ?genderPercent .
    
    << ?country Country:hasPopulationByDemographic ?ageGroupPop ~ ?ageGroupReifier >> .
    ?ageGroupReifier Demographic:hasYear ?year ;
                     Demographic:hasAgeGroup ?ageGroupIRI ;
                     Demographic:hasPercentage ?ageGroupPercent .
}
ORDER BY ?year ?genderLabel ?ageGroupLabel
```

With output as follows:

[

![](https://substackcdn.com/image/fetch/$s_!EywE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97b4a3e5-64b4-4051-93ee-1826beaef2c3_1100x478.png)

](https://substackcdn.com/image/fetch/$s_!EywE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97b4a3e5-64b4-4051-93ee-1826beaef2c3_1100x478.png)

_Note: these are generated figures, not based on actual historical data._

## Next Steps: From SHACL to JSON-LD and Javascript Objects

I’ve been focusing primarily on internal Turtle representations of datasets using SHACL, but one of the more promising applications of SHACL is in the generation of dynamic objects. For instance, one could use a SHACL schema to generate a set of JavaScript classes that can be used in conjunction with JSON-LD to support both “detached” and “live” data applications.

I’ll be exploring this concept in depth in an upcoming post.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!59ih!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc360b5d9-e0d3-4654-8eae-599c437d725b_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!59ih!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc360b5d9-e0d3-4654-8eae-599c437d725b_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.