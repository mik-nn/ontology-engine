---
title: "SHACL Taxonomy Revisited"
source: "https://ontologist.substack.com/p/shacl-taxonomy-revisited?utm_source=profile&utm_medium=reader2"
date: "Mar 8"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!ADPi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe53a0700-c122-445f-a959-7cffa7ec07af_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!ADPi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe53a0700-c122-445f-a959-7cffa7ec07af_2688x1536.jpeg)

As I was working on a recent SHACL/AI taxonomy post, one of the major problems I kept encountering was how to represent named entities. Named Entity Recognition (NER) has always been more an art than a science, in significant part because there is no algorithmic mechanism available that will allow you to differentiate a name of a company from a name of a person or thing definitively.

The idea of using public taxonomies for NER and classification has, of course, been around for several decades. Still, it hasn’t been widely adopted in large part because there hasn’t been sufficient use case to justify the maintenance headaches of such taxonomies. However, I think this is changing. As more and more organisations need to be able to specify the SAME things using the same identifiers, there is a growing awareness of (and investment in) public IRI knowledge bases.

Note, again, taxonomies by themselves are not necessarily ontologies: an ontology is generally an agreed-upon standard for the structure of data, something that’s very useful, of course, but something that doesn’t necessarily tell you anything about identity. A taxonomy (especially a public taxonomy), on the other hand, is all about identity - how do you provide a common _name_ for an entity that is nonetheless universal and easily referenceable.

What’s more, one of the areas where I think large LLMs are VERY useful is in the successful trawling of such public taxonomies that can, in turn, be referenced from within an LLM itself. For instance, using Claude, I can get a good sampling of IRIs for Barack Obama:

### 

General Knowledge Bases

-   **Wikidata**
    
    -   IRI: `http://www.wikidata.org/entity/Q76`
        
    -   The canonical linked data hub; links to most other identifiers
        
-   **DBpedia**
    
    -   IRI: `http://dbpedia.org/resource/Barack_Obama`
        
    -   Wikipedia-derived; English DBpedia
        
-   **YAGO**
    
    -   IRI: `http://yago-knowledge.org/resource/Barack_Obama`
        

### Library & Authority Control

-   **VIAF** (Virtual International Authority File)
    
    -   IRI: `http://viaf.org/viaf/52010985`
        
    -   Clusters 50+ national library records
        
-   **Library of Congress Name Authority**
    
    -   IRI: `http://id.loc.gov/authorities/names/n2008054754`
        
-   **GND** (German National Library)
    
    -   IRI: `https://d-nb.info/gnd/132522136`
        
-   **ISNI**
    
    -   IRI: `https://isni.org/isni/0000000138447099`
        
-   **BnF** (Bibliothèque nationale de France)
    
    -   IRI: `https://data.bnf.fr/ark:/12148/cb15505097z`
        
-   **SUDOC** (French academic libraries)
    
    -   IRI: `https://www.idref.fr/119585049`
        

### Academic & Research

-   **ORCID**
    
    -   Not applicable (ORCID is for researchers claiming their own works)
        
-   **Freebase** (archived, but still referenced)
    
    -   ID: `/m/02mjmr`
        
    -   Google Knowledge Graph derived from this
        

### Media & Entertainment

-   **IMDb**
    
    -   ID: `nm1682433`
        
    -   No official RDF; access via Wikidata property P345
        
-   **MusicBrainz**
    
    -   IRI: `https://musicbrainz.org/artist/85752a4a-c3d3-4c5c-9a5a-6a6c82d4b921`
        
    -   Listed as artist (Grammy-winning audiobook narrations)
        

### Geographic (birthplace reference)

-   **GeoNames** (Honolulu)
    
    -   IRI: `https://sws.geonames.org/5856195/`
        
    -   His birthplace; linked from Wikidata P19
        

### Social & Web

-   **Twitter/X**
    
    -   Username: `BarackObama`
        
    -   Wikidata property P2002
        
-   **Facebook**
    
    -   ID: `barackobama`
        
    -   Wikidata property P2013
        

Similarly, if I ask:

```
Give me a description in Turtle RDF, using the schema.org namespace, for the entity with IRI: http://www.wikidata.org/entity/Q76
```

I get the response:

```
@prefix schema: <http://schema.org/> .
@prefix wd: <http://www.wikidata.org/entity/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

wd:Q76 a schema:Person ;
    schema:name "Barack Obama"@en ;
    schema:givenName "Barack" ;
    schema:familyName "Obama" ;
    schema:additionalName "Barack Hussein Obama II" ;
    schema:description "44th President of the United States (2009–2017)"@en ;
    schema:birthDate "1961-08-04"^^xsd:date ;
    schema:birthPlace wd:Q18094 ;  # Honolulu
    schema:gender schema:Male ;
    schema:nationality wd:Q30 ;  # United States
    schema:spouse wd:Q13133 ;  # Michelle Obama
    schema:children wd:Q15070044 , wd:Q15070048 ;  # Malia, Sasha
    schema:alumniOf wd:Q49088 ,   # Columbia University
                    wd:Q13371 ;   # Harvard Law School
    schema:hasOccupation [
        a schema:Occupation ;
        schema:name "politician"
    ] , [
        a schema:Occupation ;
        schema:name "lawyer"
    ] , [
        a schema:Occupation ;
        schema:name "author"
    ] ;
    schema:jobTitle "44th President of the United States" ;
    schema:worksFor wd:Q35535 ;  # United Nations (post-presidency affiliations)
    schema:memberOf wd:Q29552 ;  # Democratic Party
    schema:award wd:Q37922 ,     # Nobel Peace Prize
                 wd:Q41254 ;     # Grammy Award
    schema:sameAs <http://viaf.org/viaf/52010985> ,
                  <http://dbpedia.org/resource/Barack_Obama> ,
                  <http://id.loc.gov/authorities/names/n2008054754> ,
                  <https://d-nb.info/gnd/132522136> ,
                  <https://isni.org/isni/0000000138447099> ;
    schema:image <https://commons.wikimedia.org/wiki/Special:FilePath/President_Barack_Obama.jpg> ;
    schema:url <https://barackobama.com/> .

# Birthplace expansion
wd:Q18094 a schema:Place ;
    schema:name "Honolulu"@en ;
    schema:containedInPlace wd:Q782 .  # Hawaii

# Spouse expansion  
wd:Q13133 a schema:Person ;
    schema:name "Michelle Obama"@en .

# Educational institutions
wd:Q49088 a schema:CollegeOrUniversity ;
    schema:name "Columbia University"@en .

wd:Q13371 a schema:CollegeOrUniversity ;
    schema:name "Harvard Law School"@en .

# Political party
wd:Q29552 a schema:Organization ;
    schema:name "Democratic Party"@en .

# Awards
wd:Q37922 a schema:Thing ;
    schema:name "Nobel Peace Prize"@en .

wd:Q41254 a schema:Thing ;
    schema:name "Grammy Award"@en . 
```

Note here that I’m using the LLM for two things - resolving publicly addressable IRIs (here, Barack Obama’s Wikidata IRI `http://www.wikidata.org/entity/Q76),` then converting the result of this into a known ontology (schema.org). Note that this doesn’t guarantee consistency - you may get different data (and the possibility of hallucinations) - but it is far superior to what has gone before.

There’s a key point from the Claude conversation that I also want to pass on:

> This uses Wikidata IRIs as the subject and for related entities, but expresses the relationships using schema.org vocabulary. The `schema:sameAs` property links out to the equivalent IRIs in other authority systems, enabling traversal across the linked data web.

In other words, here _is_ an example in which one IRI can traverse similar entities across different knowledge bases, which was the fundamental premise of Linked Data in the first place.

Note that this approach can be broken down as follows: identify one or more reference standards you want to use to retrieve relevant information (e.g., the Wikidata identifier for President Barack Obama), and determine whether that entity is defined in that system. If this entity cannot be resolved, return something like the following so that you have a clear indication that an item doesn’t exist in that schema along with potential resolvers:

```

[] rdfs:label “Barack Biden” ; 
   ex:resolvable false ; 
   schema:iri <http://dbpedia.org/> ;
   # IRIs for Barack Obama and Joe Biden .
   schema:alternativeIRI <http://dbpedia.org/entity/Q76>, 
                      <http://www.wikidata.org/entity/Q6279> ;
   .
```

Note that this approach won’t necessarily work well for private taxonomies such as a company’s stores, employees, or parts lists, and there is no guarantee that very recent entries will be in these systems. However, if the choice is between standing up a knowledge graph to hold common reference data vs. using a publicly derived, already incorporated taxonomy from an LLM (say for place names, which benefit immensely from this technique), use the LLM.

Also note, that this moves well beyond people. Consider Benzyl Propionate, a chemical additive. It has identifiers in several systems (per prompt “Provide the properties for Benzyl Propionate as Turtle” as per Claude Opus 4.5):

```
@prefix schema: <http://schema.org/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix cheminf: <http://semanticscience.org/resource/> .
@prefix pubchem: <http://rdf.ncbi.nlm.nih.gov/pubchem/compound/> .
@prefix chebi: <http://purl.obolibrary.org/obo/CHEBI_> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

pubchem:CID31219 a schema:MolecularEntity , obo:CHEBI_23367 ;
    rdfs:label "Benzyl propionate"@en ;
    skos:prefLabel "Benzyl propionate"@en ;
    skos:altLabel "Benzyl propanoate"@en ,
                  "Phenylmethyl propanoate"@en ,
                  "Propanoic acid, phenylmethyl ester"@en ,
                  "Propionic acid benzyl ester"@en ;
    schema:description "A carboxylic ester used as a flavoring agent with a sweet, fruity odor"@en ;
    
    # Chemical identifiers
    schema:identifier [
        a schema:PropertyValue ;
        schema:propertyID "CAS" ;
        schema:value "122-63-4"
    ] ;
    cheminf:CHEMINF_000399 "122-63-4" ;  # CAS Registry Number
    
    # Structural properties
    schema:molecularFormula "C10H12O2" ;
    cheminf:CHEMINF_000334 "C10H12O2" ;  # Molecular Formula
    
    schema:molecularWeight "164.20"^^xsd:decimal ;
    cheminf:CHEMINF_000338 "164.201"^^xsd:decimal ;  # Molecular Weight
    
    schema:monoisotopicMolecularWeight "164.083729624"^^xsd:decimal ;
    
    # InChI and InChIKey
    schema:inChI "InChI=1S/C10H12O2/c1-2-10(11)12-8-9-6-4-3-5-7-9/h3-7H,2,8H2,1H3" ;
    schema:inChIKey "VHOMAPWVLKRQAZ-UHFFFAOYSA-N" ;
    
    # SMILES representations
    cheminf:CHEMINF_000018 "CCC(=O)OCc1ccccc1" ;  # Canonical SMILES
    cheminf:CHEMINF_000379 "CCC(=O)OCC1=CC=CC=C1" ;  # Isomeric SMILES
    
    # Physical properties
    schema:meltingPoint [
        a schema:PropertyValue ;
        schema:value "-30"^^xsd:decimal ;
        schema:unitCode "CEL"
    ] ;
    schema:boilingPoint [
        a schema:PropertyValue ;
        schema:value "222"^^xsd:decimal ;
        schema:unitCode "CEL"
    ] ;
    cheminf:CHEMINF_000454 "1.028"^^xsd:decimal ;  # Density (g/cm³)
    
    # Solubility
    schema:solubility "Soluble in alcohol and most fixed oils; slightly soluble in propylene glycol; insoluble in water and glycerin"@en ;
    
    # Classification
    obo:IAO_0000115 "A carboxylic ester that is the propanoate ester of benzyl alcohol"@en ;  # textual definition
    rdfs:subClassOf obo:CHEBI_33308 ;  # carboxylic ester
    obo:RO_0000087 obo:CHEBI_48318 ;  # has role: flavouring agent
    
    # Functional use
    schema:category "Flavoring agent"@en , "Fragrance ingredient"@en ;
    
    # Organoleptic properties
    schema:additionalProperty [
        a schema:PropertyValue ;
        schema:propertyID "odor" ;
        schema:value "Sweet, fruity, floral"
    ] , [
        a schema:PropertyValue ;
        schema:propertyID "taste" ;
        schema:value "Fruity, sweet, green, powdery with ripe berry nuance (at 15 ppm)"
    ] ;
    
    # Safety classification
    schema:additionalProperty [
        a schema:PropertyValue ;
        schema:propertyID "GHS_classification" ;
        schema:value "Not classified as hazardous"
    ] ;
    
    # Regulatory status
    schema:additionalProperty [
        a schema:PropertyValue ;
        schema:propertyID "FEMA_GRAS" ;
        schema:value "2150"
    ] , [
        a schema:PropertyValue ;
        schema:propertyID "FDA_status" ;
        schema:value "Generally Recognized as Safe (GRAS)"
    ] ;
    
    # Linked identifiers (sameAs)
    owl:sameAs chebi:41492 ,
               <http://www.chemspider.com/Chemical-Structure.28960.html> ,
               <http://www.wikidata.org/entity/Q27251695> ;
    
    # Provenance
    schema:isPartOf <http://rdf.ncbi.nlm.nih.gov/pubchem/> ;
    rdfs:seeAlso <https://pubchem.ncbi.nlm.nih.gov/compound/31219> ,
                 <https://www.chemspider.com/Chemical-Structure.28960.html> .

# Related substance: Benzyl alcohol (precursor)
<http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID244> a schema:MolecularEntity ;
    rdfs:label "Benzyl alcohol"@en ;
    schema:molecularFormula "C7H8O" .

# Related substance: Propionic acid (precursor)
<http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID1032> a schema:MolecularEntity ;
    rdfs:label "Propionic acid"@en ;
    schema:molecularFormula "C3H6O2" .

# Synthesis relationship
pubchem:CID31219 schema:isBasedOn <http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID244> ,
                                  <http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID1032> .
```

Note that this goes the other way as well. For instance, if you have content that you frequently utilize (such as states in the US or provinces in Canada), you can retrieve not only the data but also relevant public IRIs via a single LLM query that can in turn be stored in your knowledge graph.

The query:

```
Using the Geonames taxonomy, generate a Turtle RDF showing the 50 states of the United States, including relevant IRIs.
```

The output:

```
# Turtle RDF showing (some of) the 50 states of the USA.
@prefix gn: <http://www.geonames.org/ontology#> .
@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix wd: <http://www.wikidata.org/entity/> .

# United States of America (parent country)
<https://sws.geonames.org/6252001/> a gn:Feature ; # Geonames link
    rdfs:label "United States"@en ;
    gn:name "United States" ;
    gn:featureClass gn:A ;
    gn:featureCode gn:A.PCLI ;
    gn:countryCode "US" ;
    owl:sameAs wd:Q30 . # Wikidata link. 

# ============================================================================
# The 50 States of the United States
# GeoNames Feature Code: A.ADM1 (first-order administrative division)
# ============================================================================

# Alabama
<https://sws.geonames.org/4829764/> a gn:Feature ; # Geonames link
    rdfs:label "Alabama"@en ;
    gn:name "Alabama" ;
    gn:alternateName "AL" ;
    gn:featureClass gn:A ;
    gn:featureCode gn:A.ADM1 ;
    gn:countryCode "US" ;
    gn:adminCode1 "AL" ;
    gn:parentCountry <https://sws.geonames.org/6252001/> ;
    geo:lat "32.75041"^^xsd:decimal ;
    geo:long "-86.75026"^^xsd:decimal ;
    owl:sameAs wd:Q173 . # Wikidata link. 

# Alaska
<https://sws.geonames.org/5879092/> a gn:Feature ; # Geonames link
    rdfs:label "Alaska"@en ;
    gn:name "Alaska" ;
    gn:alternateName "AK" ;
    gn:featureClass gn:A ;
    gn:featureCode gn:A.ADM1 ;
    gn:countryCode "US" ;
    gn:adminCode1 "AK" ;
    gn:parentCountry <https://sws.geonames.org/6252001/> ;
    geo:lat "64.00028"^^xsd:decimal ;
    geo:long "-150.00028"^^xsd:decimal ;
    owl:sameAs wd:Q797 . # Wikidata link.
 
```

The output can be readily reconfigured for canonical internal ontologies, but the idea of storing IRIs as references in knowledge graphs to known public entities has significant merit.

Here’s a basic guide (as per Claude Opus 4.5) for standard taxonomies that I keep handy.

### General-Purpose Knowledge Bases

-   **Wikidata**
    
    -   Base IRI: `http://www.wikidata.org/entity/`
        
    -   Most comprehensive coverage; Q-identifiers; SPARQL endpoint; excellent for LLMs due to multilingual labels and descriptions
        
-   **DBpedia**
    
    -   Base IRI: `http://dbpedia.org/resource/`
        
    -   Wikipedia-derived; stable URIs; multiple language chapters
        
-   **YAGO**
    
    -   Base IRI: `http://yago-knowledge.org/resource/`
        
    -   Wikipedia + WordNet derived; strong typing
        

### People

-   **VIAF** (Virtual International Authority File)
    
    -   Base IRI: `http://viaf.org/viaf/`
        
    -   Coverage: Authors, historical figures; clusters national authority files
        
-   **ISNI** (International Standard Name Identifier)
    
    -   Base IRI: `https://isni.org/isni/`
        
    -   Coverage: Creators and contributors broadly
        
-   **ORCID**
    
    -   Base IRI: `https://orcid.org/`
        
-   -   Coverage: Living researchers and academics
        
-   **LC Name Authority** (Library of Congress)
    
    -   Base IRI: `http://id.loc.gov/authorities/names/`
        
    -   Coverage: Comprehensive; US bias but international coverage
        
-   **GND** (German National Library)
    
    -   Base IRI: `https://d-nb.info/gnd/`
        
    -   Coverage: Strong European coverage
        
-   **Wikidata**
    
    -   Base IRI: `http://www.wikidata.org/entity/`
        
    -   Coverage: Contemporary, historical, and fictional persons via `P31 = Q5` or subclasses
        

For **fictional people**, Wikidata is the most systematic source (`P31 = Q95074`), with good coverage of literary, film, and game characters.

### Places

-   **GeoNames**
    
    -   Base IRI: `https://sws.geonames.org/`
        
-   -   ~12M features; CC-BY license; stable numeric IDs
        
-   **Getty TGN** (Thesaurus of Geographic Names)
    
    -   Base IRI: `http://vocab.getty.edu/tgn/`
        
    -   Historical and current places; art-world focus
        
-   **Wikidata**
    
    -   Base IRI: `http://www.wikidata.org/entity/`
        
    -   Linked to GeoNames, TGN, ISO codes
        
-   **ISO 3166** (via Library of Congress)
    
    -   Base IRI: `http://id.loc.gov/vocabulary/countries/`
        
    -   Countries and subdivisions
        
-   **LinkedGeoData**
    
    -   Base IRI: `http://linkedgeodata.org/triplify/`
        
    -   OpenStreetMap as RDF
        

For **fictional places**, Wikidata provides the most systematic coverage with appropriate typing.

### Organizations

-   **LEI** (Legal Entity Identifier via GLEIF)
    
    -   Base IRI: `https://rdf.gleif.org/L1/`
        
    -   Legal entities in finance; ISO 17442 standard
        
-   **ROR** (Research Organization Registry)
    
    -   Base IRI: https://ror.org/
        
-   -   Research organizations; ~100K entities
        
-   **Wikidata**
    
    -   Base IRI: `http://www.wikidata.org/entity/`
        
    -   Broad organizational coverage
        
-   **ISNI**
    
    -   Base IRI: `https://isni.org/isni/`
        
    -   Also covers organizations, not just individuals
        
-   **Grid.ac**
    
    -   Base IRI: `https://www.grid.ac/institutes/`
        
    -   Research institutions (now feeding into ROR)
        

### Books and Media Works

-   **Open Library**
    
    -   Base IRI: `https://openlibrary.org/works/`
        
    -   Books; linked to ISBN
        
-   **OCLC/WorldCat**
    
    -   Base IRI: `http://www.worldcat.org/oclc/`
        
    -   Library holdings worldwide
        
-   **Wikidata**
    
    -   Base IRI: `http://www.wikidata.org/entity/`
        
    -   Works and editions with VIAF/ISBN links
        
-   **MusicBrainz**
    
    -   Base IRI: `https://musicbrainz.org/`
        
-   -   Music works, recordings, artists
        
-   **EIDR** (Entertainment Identifier Registry)
    
    -   Base IRI: `https://ui.eidr.org/view/content?id=`
        
    -   Entertainment works; ISO standard
        
-   **IMDB**
    
    -   No open IRIs; use Wikidata with property `P345` for cross-reference
        

### Chemicals, Elements, Substances

-   **PubChem**
    
    -   Base IRI: `http://rdf.ncbi.nlm.nih.gov/pubchem/compound/`
        
    -   ~100M compounds; RDF available
        
-   **ChEBI** (Chemical Entities of Biological Interest)
    
    -   Base IRI: `http://purl.obolibrary.org/obo/CHEBI_`
        
    -   Biological interest chemicals; OBO ontology
        
-   **ChEMBL**
    
    -   Base IRI: `https://www.ebi.ac.uk/chembl/compound_report_card/`
        
    -   Bioactive molecules
        
-   **Wikidata**
    
    -   Base IRI: `http://www.wikidata.org/entity/`
        
    -   Elements and compounds with InChI, CAS links
        
-   **IUPAC Gold Book**
    
    -   Base IRI: `https://goldbook.iupac.org/terms/view/`
        
    -   Chemical terminology definitions
        

For **elements**, the periodic table is well-covered in Wikidata with links to PubChem and ChEBI.

### Biology: Animals and Plants

-   **NCBI Taxonomy**
    
    -   Base IRI: `http://purl.obolibrary.org/obo/NCBITaxon_`
        
    -   Comprehensive; OBO format
        
-   **GBIF** (Global Biodiversity Information Facility)
    
    -   Base IRI: `https://www.gbif.org/species/`
        
    -   Global biodiversity; occurrence data
        
-   **ITIS** (Integrated Taxonomic Information System)
    
    -   Base IRI: `https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=`
        
    -   North American focus
        
-   **UniProt Taxonomy**
    
    -   Base IRI: `https://purl.uniprot.org/taxonomy/`
        
    -   Aligned with NCBI
        
-   **EOL** (Encyclopedia of Life)
    
    -   Base IRI: `https://eol.org/pages/`
        
    -   General species information
        
-   **IPNI** (International Plant Names Index)
    
    -   Base IRI: `https://www.ipni.org/n/`
        
    -   Plant nomenclature
        
-   **WFO** (World Flora Online)
    
    -   Base IRI: `http://www.worldfloraonline.org/taxon/wfo-`
        
    -   Authoritative plant taxonomy
        
-   **POWO** (Plants of the World Online)
    
    -   Base IRI: `https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:`
        
    -   Kew Gardens reference
        

### Legal Terminology

-   **EuroVoc**
    
    -   Base IRI: http://eurovoc.europa.eu/
        
-   -   EU multilingual thesaurus
        
-   **FIBO** (Financial Industry Business Ontology)
    
    -   Base IRI: `https://spec.edmcouncil.org/fibo/ontology/`
        
    -   Financial and legal ontology
        
-   **LC Subject Headings**
    
    -   Base IRI: `http://id.loc.gov/authorities/subjects/`
        
    -   Includes legal topics
        
-   **Akoma Ntoso**
    
    -   Base IRI: `http://docs.oasis-open.org/legaldocml/ns/akn/3.0/`
        
    -   Legal document markup standard
        
-   **Wikidata**
    
    -   Use property `P31 = Q7748` for legal concepts
        

### Physical Constants and Units

-   **QUDT** (Quantities, Units, Dimensions, Types)
    
    -   Units: `http://qudt.org/vocab/unit/`
        
    -   Constants: `http://qudt.org/vocab/constant/`
        
    -   Excellent RDF coverage
        
-   **OM** (Ontology of Units of Measure)
    
    -   Base IRI: `http://www.ontology-of-units-of-measure.org/resource/om-2/`
        
    -   Alternative units ontology
        
-   **CODATA**
    
    -   Available via Wikidata properties; linked from QUDT
        
-   **UCUM** (Unified Code for Units of Measure)
    
    -   Base IRI: http://unitsofmeasure.org/
        
    
    -   Healthcare and scientific focus
        

### Mathematical Concepts

-   **Wikidata**
    
    -   Base IRI: `http://www.wikidata.org/entity/`
        
    -   Theorems, algorithms, mathematicians
        
-   **DBpedia**
    
    -   Base IRI: `http://dbpedia.org/resource/`
        
    -   Good coverage of named theorems
        
-   **OEIS** (Online Encyclopedia of Integer Sequences)
    
    -   Base IRI: https://oeis.org/
        
-   -   Integer sequences with identifiers
        
-   **nLab**
    
    -   Base IRI: `https://ncatlab.org/nlab/show/`
        
    -   Category theory focus
        
-   **MathWorld**
    
    -   No stable IRIs; reference only
        

### Historical Events

-   **Wikidata**
    
    -   Base IRI: `http://www.wikidata.org/entity/`
        
    -   Best coverage; use `P31 = Q1190554` (occurrence)
        
-   **DBpedia**
    
    -   Base IRI: `http://dbpedia.org/resource/`
        
    -   Events, battles, treaties
        
-   **PeriodO**
    
    -   Base IRI: `http://n2t.net/ark:/99152/`
        
    -   Historical periods and cultural eras
        
-   **Getty AAT** (Art & Architecture Thesaurus)
    
    -   Base IRI: `http://vocab.getty.edu/aat/`
        
    -   Cultural/art events and concepts
        
-   **CIDOC-CRM**
    
    -   Base IRI: `http://www.cidoc-crm.org/cidoc-crm/`
        
    -   Event modeling ontology for cultural heritage
        

### Additional Taxonomic Categories

-   **Occupations** — ESCO
    
    -   Base IRI: `http://data.europa.eu/esco/occupation/`
        
-   **Diseases** — SNOMED CT
    
    -   Base IRI: `http://purl.bioontology.org/ontology/SNOMEDCT/`
        
-   **Drugs** — DrugBank
    
    -   Base IRI: `http://wifo5-03.informatik.uni-mannheim.de/drugbank/resource/drugs/`
        
-   **Foods** — FoodOn
    
    -   Base IRI: `http://purl.obolibrary.org/obo/FOODON_`
        
-   **Languages** — Glottolog
    
    -   Base IRI: `https://glottolog.org/resource/languoid/id/`
        
-   **Currencies** — ISO 4217 via Wikidata
    
    -   Base IRI: `http://www.wikidata.org/entity/`
        
-   **Art/Cultural Objects** — Getty AAT
    
    -   Base IRI: `http://vocab.getty.edu/aat/`
        
-   **Gene Ontology** — GO
    
    -   Base IRI: `http://purl.obolibrary.org/obo/GO_`
        
-   **Anatomy** — Uberon
    
    -   Base IRI: `http://purl.obolibrary.org/obo/UBERON_`
        

### Practical Notes for LLM Integration

**Best overall sources for LLM grounding:**

1.  **Wikidata** — broadest coverage, multilingual labels/descriptions, active SPARQL endpoint, consistent Q-identifier pattern
    
2.  **Library of Congress** — authoritative for names, subjects, languages; stable `id.loc.gov` URIs
    
3.  **OBO Foundry ontologies** — biological/chemical domains; consistent `purl.obolibrary.org` pattern
    
4.  **QUDT** — physical sciences; well-documented
    

**Key considerations:**

-   Prefer sources with `rdfs:label` and `rdfs:comment` or `skos:definition` — essential for LLM context
    
-   Wikidata’s `schema:description` property is particularly useful for disambiguation
    
-   Many OBO ontologies include `obo:IAO_0000115` (textual definition) which works well for prompts
    
-   For reconciliation, OpenRefine reconciliation endpoints exist for Wikidata, VIAF, GeoNames, and others
    

## Summary

As an ontologist, taxonomist, or information architect, keep an eye out for such public repositories. Whenever you are ingesting data into your knowledge graph, part of your ingestion pipeline should include querying against an LLM to determine whether the concept that you are putting into the knowledge graph doesn’t already have one or more public IRIs. If it does, add them in (`schema:isBasedOn` or `owl:sameAs` are both useful here). Such IRIs work exceptionally well when integrating public taxonomies via LLMs and can significantly reduce the complexity of master data management, especially for frequently referenced concepts.

Also, if publicly available industry taxonomies exist, LLMs are a good place to query about them. No one can be a subject-matter expert in everything. Moreover, even when there isn’t a comprehensive taxonomy (e.g., Health Insurance is a mess), such a search can identify potential areas for curation to help create or enrich taxonomies that expose public IRIs.

_**Disclosure:** portions of this article were prepared with Claude Opus 4.5._

In media res,

[

![](https://substackcdn.com/image/fetch/$s_!1P2y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3171eee2-8d8f-46a1-b661-53a6b17cff2a_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!1P2y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3171eee2-8d8f-46a1-b661-53a6b17cff2a_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.