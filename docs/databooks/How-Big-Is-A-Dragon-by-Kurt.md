---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: How-Big-Is-A-Dragon-by-Kurt
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:07.961312+00:00'
  title: How Big Is A Dragon By Kurt
  type: plain-doc
  version: '0.1'
---

# How Big Is A Dragon By Kurt

[

![](https://substackcdn.com/image/fetch/$s_!nexi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1db3604a-29b1-4a53-8d48-3258122d73c6_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!nexi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1db3604a-29b1-4a53-8d48-3258122d73c6_2688x1536.jpeg)

Smaug Alert

There are a number of different kinds of dragons, so the answer to this can vary pretty dramatically.

-   An Adult Welsh Great Dragon (_Draconis Cymris Maximus_) has been reputed to be up to 23 meters in length, with a total mass of 1800 kg, and a wingspan of 18 meters.
    
-   The North American Firebird (_Draconis Quetzulcoatlis_) is smaller, at 16 to 17 meters, and a mass of only about 1300 kg.
    
-   The Chinese Water Dragon (_Asiatidraco sinensis_) , which has minimal wings for its body size, is the longest - at 28 meters, but it’s total mass is considerably lower at 1600 kg.
    
-   The Berkian Night Fury (_Noctodracus Berkilandus_) , found primarily in Nordic regions, is a relatively compact eight meters with a mass of approximately 500 kg, though it’s lightning-like discharge and stealth coloration make it one of the more feared.
    
-   Finally, the Pernian Fire-Lizard, (_Ouroborus cataphractus flammarum_) is seldom more than 1 meter in length and 15 kg, making it the smallest known draconic species.
    

This is not an article about dragons. It is an article about facts.

None of the above is arguably incorrect. People, especially those in English-speaking cultures, recognise Welsh dragons, most notably Smaug from The Lord of the Rings, with the dragons of Westeros (a fictionalised medieval Britannia) being another example. Chinese dragons feature regularly in Asian New Year's parades, and are used as one of the most recognisable symbols of China. Cave paintings and stone carvings of the Firebird and its Aztec relative, Quetzalcoatl, feature prominently in Mesoamerican culture, and so forth. One could argue that the pterodactyl fits the definition of a winged dragon and lived for far longer than humans (from the early Jurassic to the end of the Cretaceous, more than 150 million years).

As an ontologist, I can create a knowledge graph of dragons, and it will likely be extensive, given their pervasive presence in global human culture. This points to one of the most important aspects of a knowledge graph:

> A knowledge graph is not a collection of facts. Rather, it is a collection of assertions. These are not the same thing.

An assertion is a statement of belief. I believe that an adult Welsh Dragon can grow to as large as 23 meters in length, which can be stated in Turtle (1.2) as:

```
Dragon:Welsh a Class:Dragon ;
    Animal:hasMaxLength 23 ~ _:defineUnits {| a Class:Measure; Measure:hasUnits:Meters |} ;
    .
```

That assertion is valid in that it conforms to a schema. I can even support this statement semantically with evidence:

```
Dragon:Welsh a Class:Dragon ;
    Animal:hasMaxLength 23 
         ~ _:defineUnits {| a Class:Measure; Measure:hasUnits Units:Meters |},
         ~ _:theHobbit {| a Class:Annotation; Annotation:by Person:JRRTolkien ; 
              Annotation:source BookSeries:LordOfTheRings; 
              Event:date "1941"^^xsd:date |},
         ~ _:theMabinogion {| a Class:Annotation; Annotation:source BookSeries:Mabinogion; 
              Event:date "1430"^^xsd:date |} ;
    .
```

All of these are valid statements. In case this syntax is unfamiliar, it is equivalent to:

```
# Base triple
Dragon:Welsh Animal:hasMaxLength 23 .

# Three distinct reifications
_:defineUnits rdf:reifies << Dragon:Welsh Animal:hasMaxLength 23 >> ;
    a Class:Measure ;
    Measure:hasUnits Units:Meters .

_:theHobbit rdf:reifies << Dragon:Welsh Animal:hasMaxLength 23 >> ;
    a Class:Annotation ;
    Annotation:by Person:JRRTolkien ;
    Annotation:source BookSeries:LordOfTheRings ;
    Event:date "1941"^^xsd:date .

_:theMabinogion rdf:reifies << Dragon:Welsh Animal:hasMaxLength 23 >> ;
    a Class:Annotation ;
    Annotation:source BookSeries:Mabinogion ;
    Event:date "1430"^^xsd:date .
```

_Valid is not the same as real._

There is no evidence that a Welsh Dragon, or any dragon for that matter, ever existed. There are no preserved dragon skins or skeletons that were contemporary to the stories in which they were depicted. There are media depictions galore - drawings and paintings and photographs and videos - that show “real” dragons, but these are all creations, either through special effects or digital productions.

Dragons are _epistemological_ creatures.

This is a big word, which can be defined as an entity represented through some form of media (a message, from the Greek epistle), but which may or may not exist in reality. Ordinarily, this means that you are getting assertions about the reality of certain statements based upon the authority of others (through a medium that they provide) rather than getting these assertions from your own senses.

However, it can also be argued that even your senses constitute a medium: when you perceive something, your senses provide you with sight, sound, smell, tactile sensation, and so forth, each of which provides evidence that what you perceive exists outside your brain.

Most of what you know is epistemological. I have never met Barack Obama, but I’ve seen videos of him, heard him speak, and read accounts about him by others. I have relied on others' perceptions, as relayed through the media, to build a consistent picture of his existence, despite having no direct confirmation that he does in fact exist.

This is true of every single piece of data that you will encounter. When you work with a dataset, you are dealing with an observation that has been encoded in a medium and thus made epistemological. This was what Marshall McLuhan was talking about in the 1960s when he said, “The medium is the message.”

When I say the maximum size of a Welsh dragon is 23 meters, this is a message, an assertion. The question of the historian or analyst should be, “Is this message trustworthy?” or, put another way, “Do I trust the bearer of this message that this statement reflects reality?”

This is called _**prove**nance_. It _proves_ the reality of the assertion. It is not a region in France (that’s Provence)!

In an epistemological universe, provenance is a vehicle for acquiring trust. More to the point, provenance can be thought of as the mechanism that anchors statements within a graph to a particular frame of reference, rather than just to reality per se. This is a very subtle but important distinction. If my frame of reference (my context) is “The Real World”, then such assertions are nonsensical, unless these are treated as fictional entities. However, in a “World Where Dragons Are Real”, these assertions may very well be a reflection of that reality. Similarly, there will be situations in which something is applicable at certain times but not at others.

These are a form of constraints. In effect, reification determines the conditions under which a statement is considered valid or invalid. This is another form of context and can be a powerful tool, expecially when pulled into an ontological framework.

## The Annotation Context Ontology

Several years ago, I collaborated with Rick Jellife to promote Schematron, which was intended to provide a more robust reporting layer for the newly published XML Schema Definition Language (XSD). Schematron was based on a similar annotation framework and was intended to provide a secondary semantic layer to the structural layer of XSD. In many respects, SHACL can be seen as drawing on Schematron as one of its inspirations.

Schematron reflected two distinct modes of thinking about contextual annotations. The first was to indicate a node that should be valid but isn’t for a specific reason, at which point an error message is reported. The second is more subtle - an assertion that is likely invalid in most circumstances, but is valid in specific exceptions.

In RDF, the default assumption has always been that an assertion is valid. RDF-Star makes this more complex because the assertion may be invalid but still hold true in specific circumstances. This means that you need a more specific framework to handle both cases, often referred to as positive versus negative assertions.

I’ve been working on a framework to make this possible, which I’m calling the Annotation Context Ontology (ACO). This provides a Context class with a number of distinct properties, rendered as SHACL, that can be used to indicate when a particular assertion is defined conditionally.

A first draft of the ACO is available at [https://github.com/kurtcagle/annotation-context-ontology/](https://github.com/kurtcagle/annotation-context-ontology/) . Please note that this is _not_ a standard, and is provided for edification purposes only.

## Using the ACO

For instance, consider the dragon length example given earlier. The following shows how it could be annotated to consider two specific cases - if dragon is an adolescent, versus if it’s an adult:

```
@prefix ctx: <http://ontologist.substack.com/ns/context#> .
@prefix dragon: <http://example.org/dragons/> .
@prefix animal: <http://example.org/animal/> .

# Define contexts
ctx:JuvenileStage a ctx:TemporalContext ;
    rdfs:label "Juvenile Stage" ;
    ctx:requires [ animal:ageInYears [ sh:maxExclusive 100 ] ] .

ctx:AdultStage a ctx:TemporalContext ;
    rdfs:label "Adult Stage" ;
    ctx:requires [ animal:ageInYears [ sh:minInclusive 100 ] ] .

# Instance declaration

dragon:Smaug a animal:Dragon ;
     animal:ageInYears 99 .

# Contextual statement
dragon:Smaug animal:hasLength 8 
    ~ _:juvenileAssertion {| 
        ctx:holdsIn ctx:JuvenileStage ;
        ctx:failsIn ctx:AdultStage ;
        ctx:confidence 0.95
    |} .

dragon:Smaug animal:hasLength 23 
    ~ _:adultAssertion {| 
        ctx:holdsIn ctx:AdultStage ;
        ctx:failsIn ctx:JuvenileStage ;
        ctx:confidence 0.98
    |} .

```

This is an example of using a _Temporal Context_. Here two temporal contexts are defined, one which covers the regime when a dragon is a juvenile (< 100 years old), vs when it is an adult ( 100 years or older). The `ctx:requires` predicate contains the relevant preconditions that the dragon (the instance) must have in order to satisfy that condition.

There are two specific assertions that are then given - one indicating the length of the dragon if it’s a juvenile, the second the length if it’s an adult. In the ctx:juvenileAssertion, the assertion is considered true (`ctx:holds`) if the dragon has the `_:JuvenileStage` context, but is considered false (`ctx:fails`) if the dragon has an `_:AdultStage` context.

So why put two assertions giving different lengths for the dragon? Something is either true or it’s not, right? In this particular case, yes - the length will be 8 because the dragon is a juvenile (he’s 99)

However, if the statement:

```
dragon:Smaug animal:ageInYears 99 .
```

is _generated_, then at some point, the dragon will turn 100, and be considered an adult. When that happens, the max length for that dragon expands to 23 meters.

In other words, a **state change** has occurred, and that changes the regime under which the dragon’s length is determined.

This example may seem a little arbitrary, but think about the question of who you voted for in the last election. If you are 17, you cannot vote yet; it is a legal constraint, but at 18 you can (in the United States, at least).

This approach turns the graph into a **state machine**. You go from saying “this is the way things are to” to “when the graph is in this state, then these are the conditions that apply”. This is important because, in a state machine, you typically have a few dynamic variables (time being a major one), and their evolution over time causes the graph to move through various states.

## Contexts

ACO provides four specialised context types:

**Temporal Context**

For time-based scoping:

```
ctx:ChildhoodStage a ctx:TemporalContext ;
    rdfs:label “Childhood” ;
    ctx:requires [ 
        :age [ sh:maxExclusive 13 ] 
    ] .
```

The temporal context, as indicated above, facilitates evolution in time.

#### **Spatial Context**

For location-based scoping:

```
ctx:IndoorEnvironment a ctx:SpatialContext ;
    rdfs:label “Indoor” ;
    ctx:requires [ 
        geo:within :BuildingBoundary 
    ] .
```

The spatial context facilitates evolution in space, thereby influencing outcomes when a given entity is in a room, city, country or similar place.

#### **Epistemic Context**

For knowledge source scoping:

```
ctx:ScientificConsensus a ctx:EpistemicContext ;
    rdfs:label “Scientific Consensus” ;
    rdfs:comment “Peer-reviewed published findings” .
```

This context occurs when dealing with information from a particular source, publisher or publication regime.

#### **Modal Context**

For possible worlds:

```
ctx:AlternateHistory a ctx:ModalContext ;
    rdfs:label “Alternate History” ;
    rdfs:comment “Hypothetical scenario where event X didn’t occur” .
```

This context is useful for describing alternative worlds or scenarios. For instance, you could have `ctx:RealWorld` and `ctx:WorldWhereDragonsExist` as different contexts, allowing you to effectively posit regimes.

It should be noted that all of these are subclasses of `ctx:Context` , and you can extend this to handle other types of context as appropriate.

## Determining Strength of Provenance

Epistemic context is somewhat simpler, in that it can determine various regimes of data while offering a measure of confidence in that data:

```
@prefix dragon: <http://example.org/dragons/> .
@prefix book: <http://example.org/book/> .
@prefix ctx: <http://ontologist.substack.com/ns/context#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

# Define epistemic contexts (sources)
ctx:TolkienCanon a ctx:EpistemicContext ;
    rdfs:label "Tolkien Canon" ;
    rdfs:comment "Information from J.R.R. Tolkien's works" .

ctx:WelshMythology a ctx:EpistemicContext ;
    rdfs:label "Welsh Mythology" ;
    rdfs:comment "Traditional Welsh mythological accounts" .

ctx:ModernAnalysis a ctx:EpistemicContext ;
    rdfs:label "Modern Analysis" ;
    rdfs:comment "Contemporary scholarly synthesis" .

# Tolkien's claim
dragon:Welsh animal:hasMaxLength 23 
    ~ _:tolkienClaim {| 
        ctx:holdsIn ctx:TolkienCanon ;
        ctx:confidence 0.9 ;
        prov:wasAttributedTo :JRRTolkien ;
        prov:generatedAtTime "1954"^^xsd:gYear ;
        rdfs:comment "From The Hobbit descriptions"
    |} .

# Welsh mythology claim
dragon:Welsh animal:hasMaxLength 21 
    ~ _:welshClaim {| 
        ctx:holdsIn ctx:WelshMythology ;
        ctx:confidence 0.6 ;
        prov:wasAttributedTo :MabinogionScribe ;
        prov:generatedAtTime "1430"^^xsd:gYear ;
        rdfs:comment "From Mabinogion manuscript"
    |} .

# Modern scholarly estimate
dragon:Welsh animal:hasMaxLength 19 
    ~ _:modernClaim {| 
        ctx:holdsIn ctx:ModernAnalysis ;
        ctx:confidence 0.85 ;
        prov:wasAttributedTo :DrJaneSmith ;
        prov:generatedAtTime "2020"^^xsd:gYear ;
        rdfs:comment "Statistical analysis of all sources suggests 19m average"
    |} .
```

Here, three contexts are defined: Tolkien’s work, the Mabinogion (a famous 14th-century collection of Welsh tales and mythology), and a modern analysis. Each provides a different estimate of Smaug's length, based on different criteria and interpretations, and each interpretation, in turn, includes a confidence percentage indicating the likelihood that the number is accurate.

You can then query against this dataset to retrieve the most likely source of analysis to be accurate:

```
PREFIX dragon: <http://example.org/dragons/>
PREFIX animal: <http://example.org/animal/>
PREFIX ctx: <http://ontologist.substack.com/ns/context#>
PREFIX prov: <http://www.w3.org/ns/prov#>

SELECT ?length ?context ?confidence ?author ?date
WHERE {
    dragon:Welsh animal:hasMaxLength ?length .
    ?stmt rdf:reifies << dragon:Welsh animal:hasMaxLength ?length >> ;
          ctx:holdsIn ?context ;
          ctx:confidence ?confidence ;
          prov:wasAttributedTo ?author ;
          prov:generatedAtTime ?date .
}
ORDER BY DESC(?date)
```

This in turn generates the following output:

[

![](https://substackcdn.com/image/fetch/$s_!K1hT!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa5aafcf-4bcb-4a86-98bb-4ba4b34d0b5f_1400x400.jpeg)

](https://substackcdn.com/image/fetch/$s_!K1hT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa5aafcf-4bcb-4a86-98bb-4ba4b34d0b5f_1400x400.jpeg)

## Use Cases and Examples

The Annotation Context Ontology (ACO) facilitates the management of information that varies with context—e.g., who said it, when, where, or under what conditions. It preserves multiple valid perspectives on the same facts rather than forcing a single “truth.”

### 1\. Historical Records: Conflicting Accounts from Different Sources

**The Challenge:** Historical events often have contradictory accounts from different observers, each valid within its own perspective.

**Example:** The height of Napoleon Bonaparte is recorded differently across sources: French military records claim 5’7”, British propaganda portrayed him as 5’2”, and modern historians estimate 5’6”. ACO preserves all three claims with their sources (French Imperial Army, British cartoonists, 20th century scholarship) and confidence levels, allowing researchers to understand both the facts and the political narratives.

### 2\. Scientific Data: Measurements under Varying Conditions

**The Challenge:** Scientific measurements produce different results based on experimental conditions, equipment precision, and methodological approaches.

**Example:** The speed of light was measured as 299,796 km/s by Michelson in 1926, 299,792.5 km/s by Essen in 1950, and 299,792.458 km/s (current standard) by laser interferometry in 1983. ACO tracks each measurement with its experimental context (equipment used, measurement method, atmospheric conditions, margin of error), showing the progression of scientific precision over time while maintaining the validity of each measurement within its experimental framework.

### 3\. Multi-Agent Systems: Different Perspectives and Beliefs

**The Challenge:** In systems with multiple autonomous agents (robots, AI assistants, or distributed sensors), each agent may have partial or conflicting information about the same situation.

**Example:** Three warehouse robots tracking inventory might report different quantities for the same item: Robot A (camera-based) counts 47 boxes, Robot B (RFID scanner) detects 45 tagged items, and Robot C (weight sensor) calculates 46 units based on total weight. ACO captures each robot’s perspective with its sensing modality, last update time, and confidence score, allowing the system to reconcile differences or flag discrepancies for human review.

### 4\. Temporal Data: Properties that Change Over Time

**The Challenge:** Many properties aren’t static but change over time—population, prices, ownership, political boundaries—yet we need to query historical states accurately.

**Example:** The price of Bitcoin varies constantly. ACO can represent: $30,000 on January 1, 2024 (source: Coinbase, recorded at 9:00 AM EST), $45,000 on March 15, 2024 (source: Binance, recorded at 2:30 PM EST), and $28,000 on May 20, 2024 (source: Kraken, recorded at 11:15 AM EST). This allows financial analysts to query “What was Bitcoin’s price on March 1st according to Coinbase?” or “Show me price trends across all exchanges during Q1 2024.”

### 5\. Provenance: Tracking Source and Reliability of Information

**The Challenge:** Understanding the provenance of information and its reliability is critical for decision-making, especially when combining data from multiple sources with varying reliability.

**Example:** A medical diagnosis system might receive: patient symptoms (directly reported, high reliability but subjective), lab results (hospital equipment, very high reliability, calibrated daily), family history (patient recall, medium reliability, may be incomplete), and WebMD search results (patient research, low reliability, may be misinterpreted). ACO tracks each information source, when it was obtained, who provided it, and quality metrics, helping doctors weigh evidence appropriately.

### 6\. Modal Reasoning: Possible, Necessary, and Counterfactual Statements

**The Challenge:** Some statements aren’t about what is true, but what could be true, must be true, or would have been true under different circumstances.

**Example:** Urban planning scenario analysis: “The new highway will reduce commute times by 15 minutes” (predicted/possible), “Traffic must increase if population grows 20%” (necessary consequence), and “If we had built the subway extension in 2010, downtown congestion would be 30% lower today” (counterfactual). ACO distinguishes between actual observations, predictions, logical necessities, and alternative scenarios, each with different epistemic status and confidence levels.

### 7\. Knowledge Graphs: Integrating Data from Multiple Sources

**The Challenge:** Enterprise knowledge graphs combine data from dozens of sources—databases, APIs, documents, spreadsheets—each with different update frequencies, reliability levels, and coverage. Conflicts are inevitable.

**Example:** A company’s customer database might show: CRM system says customer relocated to Austin (updated yesterday, high confidence), LinkedIn profile shows Seattle location (updated 3 months ago, user-provided), shipping records show recent deliveries to Portland (last week, factual), and email signature lists a Denver office (current email, may be headquarters not residence). Rather than forcing one answer, ACO preserves all location claims with their source systems, timestamps, and confidence scores, allowing queries like “What’s the customer’s most recent verified address?” or “Show all known locations for this customer with source attribution.”

## Why This Matters

Traditional databases force us to pick one version of the truth and discard the rest. ACO recognises that context matters—the “right” answer often depends on who’s asking, when they’re asking, and what they need it for. By preserving contextual information alongside facts, ACO enables more nuanced analysis, better decision-making, and a richer understanding of complex information landscapes.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!A6Fl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff8726d9-1bb7-440a-a2b0-387b730ad9b5_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!A6Fl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff8726d9-1bb7-440a-a2b0-387b730ad9b5_2688x1536.jpeg)

They are always so cute when they’re young.

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.

