---
type: article
title: "HOLONS: A New Hope"
source: https://substack.com/@kurtcagle/p-191726100
created: 2026-03-25
tags:
  - article
---

# HOLONS: A New Hope

Источник: https://substack.com/@kurtcagle/p-191726100

---

Mar 25, 2026

---


![](https://substackcdn.com/image/fetch/$s_!cGzP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9298598d-f774-4b33-ae85-33d8406187df_2688x1536.jpeg)


In my last post on context graphs, I went fairly in-depth into theory, especially about holons and the four graph model. I’m going to switch gear and walk through some examples that I think might make a little clearer how one can design with a context graph in mind.

_**TL/DR Warning:** This is long, even by my standards. It’s probably worth getting a cup of coffee while reading it, or, if you have too much on your plate, running it through an LLM for a better breakdown. Moreover, I am not proposing a formal terminology here for class or property names, though there is at least a skeletal foundation for it. My hope is that it will kick-start discussions and prompt people to consider the potential and pitfalls of this architectural approach._

## The Power of Scenes

A transcript or log is a foundational document for context graphs. Transcripts are usually time-oriented, record conversations and who said them, and frequently carry a lot of implied semantics. They also occur within a holonic context: movie and television scripts, for instance, break down naturally into natural movie, act, and scene boundaries that have significance in defining or bounding the scope of interaction, and support the idea of parallelism - where different interactions may be happening in different areas simultaneously.

In a movie, there is a distinction between a camera cut and a scene; the camera records what is happening within the scene from a certain point of view- first-person POV, closeups, long shots, etc., but the scene itself is intended to provide a narrative - you very seldom deviate from that narrative mid-scene. The first scene in Star Wars IV, A New Hope, (past the long narrative scroll) has a large, formidable Imperial Cruiser overtaking a smaller courier ship, which immediately cuts to a corridor where Princess Leia gives R2D2 the plans to the Death Star, moments before Darth Vader and the Imperial Stormtroopers enter, and she’s been taken captive.

The scene here has established a place within the narrative, and while the camera moves about, the story flow remains continuous. This is the distinction between scene (narrative flow), place (the physical boundaries), and viewpoint (observational point of view). Characters may enter or exit this scene, but there’s an implicit boundary that they cross that takes them into or out of the scene. This is the _holon boundary,_ and it defines the edges of the scene. Such entrances and exits are especially significant for several reasons:

- A character enters a scene for a reason; they have intent - if they weren’t important, they would not be entering. They typically are there to increase the tension in a scene.
    
- A character exits a scene for a reason; they have either resolved their intent or have been stymied.
    
- If they have done neither, then the character is simply part of the background, or their significance has not yet been revealed. Crossing the boundary in either direction triggers an event.
    
- Time and space are always relative within such a scene; the timing of events (utterances and actions) within the scene in a transcript are usually relevant only to the viewer (how much time has passed relative to when the viewer started watching the scene). All that is known in Star Wars was that this whole story was told in a galaxy far, far away.
    
- A scene ends when the PoV character exits through a portal into a different scene. A portal could be a door, a tunnel, a teleport beam, or the PoV character’s death or loss of consciousness; the key is that it represents a transition, and that transition is controllable (this falls into the definition of a liminal space) . A transition is the crossing of a holonic boundary.
    
- Note that the next scene does not have to feature the character crossing out immediately and crossing back in, but in both writing and visual media, this tends to be the case. In Star Wars, for instance, the PoV character is neither Darth Vader nor Leia Organa, but RD2D, and the scene ends when officers on the Imperial Cruiser detect an errant pod release (which shows no life forms, but contains the trashcan-shaped droid and his gold metallic companion). The next scene is on Tatooine, showing the two droids walking the sand dunes away from the escape pod.
    
- Star Wars, as a whole, can be argued to be the story as told by R2D2, since that character is in nearly every scene. This can be seen in the narrative graph for R2D2:
    

[

![](https://substackcdn.com/image/fetch/$s_!oYH0!,w_5760,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fece6d786-4c3d-4647-9b29-601648989f27_6885x8191.png)



](https://substackcdn.com/image/fetch/$s_!oYH0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fece6d786-4c3d-4647-9b29-601648989f27_6885x8191.png)

Not all holon are like this, though most have the same narrative closure conventions:

- Ground the holon in a place and time.
    
- Designate (or reference) the primary characters, and record their events:
    
    - (Are they already there?
        
    - Do they enter the holon?
        
    - Have they been established (declared)?
        
    - How do they interact with other characters?
        
    - What portals are available to transfer to another holon, and what are the preconditions or constraints of transit?
        
    - Can characters transfer things from one holon to another, and so forth?
        
- Are there scene trajectories? This is important. In a movie (static medium), the portal that triggers a transition to a different holon is one-to-one with the movie's trajectory. In a game, there may be several potential portals; they form a graph with multiple final holons (in this case, endings).
    
- How are holon portals represented? When Hans, Luke, Obi-Wan and the droids are forced by the stormtroopers on Tatooine to escape aboard the Millennium Falcon, the portal was the loading ramp to the ship; the next scene was aboard the Falcon. The portal (indeed any holon) representation is called its projection - how the ship appears from the outside in its dock, as one example. Projections are important because they are calculated from the holon's internal state, which is usually not directly observable. The portal projection may include an icon that serves as a portal trigger.
    
- The boundary itself can be seen as rules, constraints, and permissions. It normally doesn’t have a physical representation (that’s the projection), but it does contain the logic for transition.
    
- Note that while holons may represent sequential scenes, they can also represent successive layers of depth - world, country, city, neighbourhood, for instance.
    
- Holons may also be vehicles, with the view out of the windows being a projection of the space around them. Such projections are not necessarily accessible through the portal (the portal, in this case, is locked), but the projection of that portal as the viewscreen, window, or map in the interior holon can provide such visualisations. For instance, when the Falcon hesitantly enters hyperspace, the viewport is a portal, with the projection appearing on the screen.
    

## Producing the Graph Transcript

I work a lot with transcripts and, as such, have been developing a SHACL constraint schema. This is one of the areas where I think LLMs do remarkably well - take a movie transcript such as the following:

```
The 20th Century Fox and Lucasfilm Ltd. logos play, with the Fox fanfare over both logos. After it ends, the text "A long time ago in a galaxy far, far away..." fades in and out. Then we get an extreme close-up of "STAR WARS," outlined in yellow, zooming out on a space background. The title crawl scrolls up underneath.

Episode IV
A NEW HOPE

It is a period of civil war. Rebel
spaceships, striking from a
hidden base, have won their
first victory against the evil
GALACTIC EMPIRE.

During the battle, Rebel spies
have managed to steal secret
plans to the Empire’s ultimate
weapon, the DEATH STAR, an
armoured space station with
enough power to destroy an
entire planet.

Pursued by the Empire's sinister
agents, Princess Leia races home
aboard her starship, custodian of
the stolen plans that can save her
people and restore freedom to the
galaxy....

The Secret Plans
After the crawl ends, we pan down on two planets. Lasers flash across the screen, and a Rebel spaceship, the Tantive IV, flies into view, being pursued by the Empire's Star Destroyer. The conflict goes on until one of the Star Destroyer's bolts causes an explosion on the Tantive IV. Inside the ship are two robots, C-3PO (Anthony Daniels) and R2-D2 (Kenny Baker). The former is a Protocol droid, tall and golden, while the latter is a shorter, blue-and-white Astromech droid. Rebel soldiers run across the halls of the ship.

C-3PO: Did you hear that? (R2-D2 beeps.) They shut down the main reactor. We'll be destroyed for sure.
More Rebel soldiers get into formation.

C-3PO: This is madness.
Just then, a door falls down, and out comes the Empire's soldiers, known as Stormtroopers, clad in white armor with distinct black markings. The Rebel soldiers and Stormtroopers fight by way of blaster bolts.

C-3PO: We're doomed. [R2-D2 beeps] There'll be no escape for the princess this time.

[Just then, they hear a clanking noise.]

C-3PO: What's that?

[Beep Blip Beep]

C-3PO: R2-D2, where are you?

[Beep Blip Blip]

C-3PO: At last! Where have you been? They're heading in this direction. What are we going to do? We'll be sent to the spice mines of Kessel, smashed into who knows what!

Wait a minute. Where are you going?

Stormtrooper: The Death Star plans are not in the main computer.

Darth Vader: Where are those transmissions you intercepted? What have you done with those plans?

We intercepted no transmissions. This is a consular ship. We're on a diplomatic mission.

Darth Vader: If this is a consular ship, where is the ambassador?

Darth Vader: Commander, tear this ship apart until you've found those plans, and bring me the passengers! I want them alive!

Stormtrooper: There's one. Set for stun.

Stormtrooper: She'll be all right. Inform Lord Vader we have a prisoner.

C-3PO: Hey! You're not permitted in there. It's restricted. You'll be deactivated for sure.

[Beep Blip]

Don't you call me a mindless philosopher, you overweight glob of grease! Now come out before somebody sees you.

[Whistle Blip Blip]

Secret mission? What plans? What are you talking about? I'm not getting in there.

C-3PO: I'm going to regret this.

There goes another one.

Hold your fire. There's no life-forms. It must have short-circuited.

C-3PO: That's funny. The damage doesn't look as bad from out here. Are you sure this thing is safe? [R2-D2 beeps] Oh.

Leia: Darth Vader. Only you could be so bold. The Imperial Senate will not sit still for this. When they hear you've attacked a diplomatic-

Darth Vader: Don't act so surprised, Your Highness. You weren't on any mercy mission this time. Several transmissions were beamed to this ship by rebel spies. I want to know what happened to the plans they sent you.

Leia: I don't know what you're talking about. I'm a member of the Imperial Senate on a diplomatic mission to Alderaan.

Darth Vader: You are part of the Rebel Alliance and a traitor. Take her away!

Holding her is dangerous. If word of this gets out, it could generate sympathy for the rebellion in the senate.

Darth Vader: I've traced the rebel spies to her. Now she is my only link to finding their secret base.

She'll die before she'll tell you anything.

Darth Vader: Leave that to me. Send a distress signal, and then inform the senate that all aboard were killed.

Praji: Lord Vader, the battle station plans are not aboard this ship, and no transmissions were made. An escape pod was jettisoned during the fighting, but no life-forms were aboard.

Darth Vader: She must have hidden the plans in the escape pod. Send a detachment down to retrieve them- See to it personally, Commander. There'll be no one to stop us this time.

Praji: Yes, sir.

C-3PO: How did we get into this mess? I really don't know how. We seem to be made to suffer. It's our lot in life. [R2-D2 beeps] I've got to rest before I fall apart. My joints are almost frozen. What a desolate place this is!

[Bleep Blip]

Where do you think you're going?

Well, I'm not going that way. It's much too rocky. This way is much easier.

What makes you think there are settlements over there?

...
```

and pass in both the SHACL representation of the target schema along with the following prompt:

> ```
> Given the attached SHACL, create a context graph of this section of the movie, with each holon generally indicating a scene change, and with the movie itself being a holon. 
> 
> At each point when a character, place, change of scene, concept or so forth is introduced (moves into the boundary of the holon event) create a declaration for that entity. 
> 
> A scene is defined as the bounded immediate system in which the characters or other entities (such as space ships) interact, with breaks from one holon to the next creating new holons that reference the previous holon if significant factors (typically place) remains the same, and with references to previous holon events . Holons should incorporate context graphs (the description of where things are for the movie or scene in terms of entities), interior graphs for entities that need them, boundary graphs describing SHACL constraints and shapes on the boundary interface, and projection graphs that describe the generated appearance of entities based either as static constructs, or as generated triples. These should use SHACL 1.2 as defined at https://www.w3.org/TR/2026/WD-shacl12-core-20260319/, and should use ~ {| |} reification notation as part of the TURTLE 1.2 specification. 
> 
> Log all events in which entities enter or leave the holon boundaries. Utterances and actions similarly are events that can refer to previous utterances or events indicating inResposeTo or influenceBy, with these utilising named reifications. Motivation, changes of movement, emotional states, topical themes, etc., can be added as annotations, with degrees of confidence and indications of who or what made these evaluations, using Wikidata as reference term ontologies. If timestamps are provided in the transcript, incorporate them as metadata, otherwise estimate them based upon the length of utterances. 
> 
> The desired end product should be a Turtle/Trig document indicating named graph holons in the four holon model.
> ```

What gets generated here is a set of context graphs as a TRIG file, aka Turtle with named graphs. A full breakdown is revealing here:

**Scale:** 52KB, 1,366 lines. Serialised as plain Turtle (the shapes graph is self-contained; no TriG wrapper needed since there’s only one graph of shapes).

**31 named** `sh:NodeShape` **IRIs** across nine sections:

The **structural shapes** (§2–§3) cover `MovieHolonShape`, `SceneHolonShape`, a SPARQL-based `UniqueSequenceShape` to catch duplicate sequence numbers within a movie, and `ProjectionContentShape` / `ContextProvenanceShape` for the projection and context layer requirements. The `SceneHolonShape` mandates all four layer graph IRIs, a single `cga:partOf`, and a positive-integer `sequenceNumber`.

The **entity hierarchy** (§4) defines a base `EntityShape` and six subtype shapes — Character, Place, Vehicle, Organization, PhysicalObject, ConceptEntity — each using `sh:node swsh:EntityShape` to inherit the base label requirement. The `ConceptEntityShape` includes a `sh:Trace` message encouraging Wikidata alignment via `owl:sameAs`.

The **event shapes** (§5) define a base `EventShape` (mandatory `cga:content`, timestamp regex, optional motivations and emotional states) with four subtypes. `UtteranceShape` is the most constrained: it mandates exactly one `cga:speaker`, recommends an addressee, and uses `sh:reifierShape swsh:ResponseAnnotationShape` on both `cga:inResponseTo` and `cga:influencedBy` — This is the SHACL 1.2 mechanism that validates the `~ swevt:rid {| cga:confidence ... |}` annotations from the TriG document. `DecisionShape` requires at least one `cga:hasMotivation` at Warning severity.

The **boundary event shapes** (§6) add an `EntryEntityConsistencyShape` as a SPARQL constraint that verifies every `cga:entity` reference resolves to a declared `cga:Entity` subclass.

The **annotation shapes** (§7) include `ResponseAnnotationShape` (validates reifier nodes: decimal confidence in [0,1], `prov:Agent` assessedBy, optional rationale), `ConfidenceCoverageShape` (any reifier naming `assessedBy` must also carry `cga:confidence`), plus taxonomy shapes for `cga:Motivation` and `cga:EmotionalState`.

The **inter-holon consistency shapes** (§8) are all SPARQL-based:

- `HolonChainSymmetryShape` — checks `followingHolon`/`precedingHoln` are mutual
    
- `ContainmentSymmetryShape` — checks `partOf`/`containsHolon` are mutual
    
- `ExitPrecededByEntryShape` — every EntityExit should have a matching EntityEntry
    
- `MacGuffinTrackingShape` — specifically checks R2 exists without `carriedObject: DeathStarPlans`
    
- `SequenceContinuityShape` — no gaps greater than 1 in sequenceNumber
    

**11 SHACL Rules (§9)** using `sh:SPARQLRule` (plus one `sh:TripleRule` for the `partOf` inverse sketch):

## Understanding the Context Graph

The first part of the context graph is a standard knowledge graph that declares namespaces:

```
prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:    <http://www.w3.org/2002/07/owl#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix schema: <https://schema.org/> .
@prefix wd:     <https://www.wikidata.org/entity/> .

@prefix cga:    <https://ontologist.ai/ns/cga/> .
@prefix sw:     <https://ontologist.ai/ex/sw/anh/> .
@prefix swc:    <https://ontologist.ai/ex/sw/char/> .
@prefix swp:    <https://ontologist.ai/ex/sw/place/> .
@prefix swv:    <https://ontologist.ai/ex/sw/vehicle/> .
@prefix swo:    <https://ontologist.ai/ex/sw/org/> .
@prefix swx:    <https://ontologist.ai/ex/sw/concept/> .
@prefix swobj:  <https://ontologist.ai/ex/sw/object/> .
@prefix swevt:  <https://ontologist.ai/ex/sw/event/> .
@prefix swann:  <https://ontologist.ai/ex/sw/ann/> .
@prefix swsh:   <https://ontologist.ai/ex/sw/shapes/> .
```

or readers less familiar with RDF vocabulary conventions, the following summarises the load-bearing `cga:` properties used throughout:

- `cga:MovieHolon`**,** `cga:SceneHolon` — Top-level containers; a movie contains scene holons
    
- `cga:hasInteriorGraph` — Points to the named graph holding events and utterances within the holon
    
- `cga:hasBoundaryGraph` — Points to the named graph holding SHACL shapes and entry/exit events
    
- `cga:hasProjectionGraph` — Points to the named graph holding the outward-facing summary of the holon
    
- `cga:hasContextGraph` — Points to the named graph holding provenance and metadata about the holon itself
    
- `cga:EntityEntry` **/** `cga:EntityExit` — Events recording when an entity crosses a holon boundary
    
- `cga:Utterance` **/** `cga:Action` **/** `cga:Decision` — Typed events within the interior graph
    
- `cga:inResponseTo` **/** `cga:influencedBy` — Causal links between events; annotated with confidence via RDF 1.2 reification
    
- `cga:hasMotivation` **/** `cga:hasEmotionalState` — Analyst annotations on intent and affect
    

These properties are defined in the `cga:` ontology at `https://ontologist.ai/ns/cga/`, which is a work in progress under the W3C Context Graph Community Group.

With these declared, the code assigns classes as well as enumerative states:

```
# ── Motivations ───────────────────────────────────────────────────────────────
swann:Mot_Survival    a cga:Motivation ; rdfs:label "Survival"@en .
swann:Mot_Duty        a cga:Motivation ; rdfs:label "Duty / Mission"@en .
swann:Mot_Profit      a cga:Motivation ; rdfs:label "Self-interest / Profit"@en .
swann:Mot_Friendship  a cga:Motivation ; rdfs:label "Loyalty / Friendship"@en .
swann:Mot_Vengeance   a cga:Motivation ; rdfs:label "Justice / Vengeance"@en .
swann:Mot_Power       a cga:Motivation ; rdfs:label "Power and Control"@en .
swann:Mot_Protection  a cga:Motivation ; rdfs:label "Protecting Others"@en .
swann:Mot_Intel       a cga:Motivation ; rdfs:label "Intelligence Extraction"@en .
swann:Mot_Duty        a cga:Motivation ; rdfs:label "Duty / Mission"@en .
swann:Mot_Adventure   a cga:Motivation ; rdfs:label "Adventure / Freedom"@en .
swann:Mot_Fear        a cga:Motivation ; rdfs:label "Fear-driven action"@en .

# ── Emotional States ──────────────────────────────────────────────────────────
swann:Emo_Fear          a cga:EmotionalState ; rdfs:label "Fear"@en .
swann:Emo_Anxiety       a cga:EmotionalState ; rdfs:label "Anxiety"@en .
swann:Emo_Despair       a cga:EmotionalState ; rdfs:label "Despair"@en .
swann:Emo_Determination a cga:EmotionalState ; rdfs:label "Determination"@en .
swann:Emo_Grief         a cga:EmotionalState ; rdfs:label "Grief"@en .
swann:Emo_Wonder        a cga:EmotionalState ; rdfs:label "Wonder / Awe"@en .
swann:Emo_Suspicion     a cga:EmotionalState ; rdfs:label "Suspicion"@en .
swann:Emo_Exasperation  a cga:EmotionalState ; rdfs:label "Exasperation"@en .
swann:Emo_Hope          a cga:EmotionalState ; rdfs:label "Hope"@en .
swann:Emo_Resignation   a cga:EmotionalState ; rdfs:label "Resignation"@en .
swann:Emo_Arrogance     a cga:EmotionalState ; rdfs:label "Arrogance"@en .
swann:Emo_Curiosity     a cga:EmotionalState ; rdfs:label "Curiosity"@en .
swann:Emo_Excitement    a cga:EmotionalState ; rdfs:label "Excitement"@en .
swann:Emo_Sorrow        a cga:EmotionalState ; rdfs:label "Sorrow"@en .
swann:Emo_Relief        a cga:EmotionalState ; rdfs:label "Relief"@en .
swann:Emo_Anger         a cga:EmotionalState ; rdfs:label "Anger"@en .
swann:Emo_Indignation   a cga:EmotionalState ; rdfs:label "Moral Indignation"@en .
swann:Emo_Longing       a cga:EmotionalState ; rdfs:label "Longing / Yearning"@en .
swann:Emo_Trust         a cga:EmotionalState ; rdfs:label "Trust / Faith"@en .
swann:Emo_Cynicism      a cga:EmotionalState ; rdfs:label "Cynicism"@en .
swann:Emo_Elation       a cga:EmotionalState ; rdfs:label "Elation"@en .
swann:Emo_Acceptance    a cga:EmotionalState ; rdfs:label "Acceptance / Peace"@en .
swann:Emo_Regret        a cga:EmotionalState ; rdfs:label "Regret"@en .
swann:Emo_Defiance      a cga:EmotionalState ; rdfs:label "Defiance"@en .
swann:Emo_Confusion     a cga:EmotionalState ; rdfs:label "Confusion"@en .

sw:HumanAnalyst a prov:Agent ;
    rdfs:label "Kurt Cagle (human analyst)"@en .

sw:LLMAgent a prov:Agent ;
    rdfs:label "Claude Sonnet 4.6 (LLM inference pass)"@en ;
    prov:actedOnBehalfOf sw:HumanAnalyst .

sw:Analyst a prov:Agent ;
    rdfs:label "Holonic Analyst — composite agent"@en ;
    prov:wasAssociatedWith sw:HumanAnalyst, sw:LLMAgent .
```

and not coincidentally declaring the analyst who identified confidence levels. Note that provenance in a decision-support context is not merely cosmetic. A confidence score of `0.98` means something different depending on whether it originated from human domain expertise reviewing the transcript or from an LLM inference pass over it. PROV-O already provides the vocabulary to make this distinction cleanly — `prov:actedOnBehalfOf` lets you express that the LLM was operating under human direction, while keeping the two sources separable for downstream consumers who need to weight them differently. In production contexts, high-stakes decisions recorded in the graph should carry provenance that a compliance auditor could interrogate.

This is followed by entity declarations, including characters, vehicles, organisations, places, concepts, and things:

```
# ═══════════════════════════════════════════════════════════════════════════════
# ENTITY DECLARATIONS
# ═══════════════════════════════════════════════════════════════════════════════

swc:C3PO a cga:Character ; rdfs:label "C-3PO"@en ; skos:altLabel "See-Threepio"@en ;
    cga:portrayedBy "Anthony Daniels" ;
    schema:description "Protocol droid; human-cyborg relations; fluent 6M+ languages"@en ;
    cga:allegiance swo:RebelAlliance ; cga:species "Protocol Droid" ; owl:sameAs wd:Q159776 .

swc:R2D2 a cga:Character ; rdfs:label "R2-D2"@en ; skos:altLabel "Artoo"@en ;
    cga:portrayedBy "Kenny Baker" ;
    schema:description "Astromech droid; carrier of Death Star plans and Leia's message"@en ;
    cga:allegiance swo:RebelAlliance ; cga:species "Astromech Droid" ; owl:sameAs wd:Q154941 .

swc:DarthVader a cga:Character ; rdfs:label "Darth Vader"@en ; skos:altLabel "Anakin Skywalker"@en ;
    cga:portrayedBy "David Prowse" ;
    schema:description "Dark Lord of the Sith; fallen Jedi; Empire's enforcer"@en ;
    cga:allegiance swo:GalacticEmpire ; cga:forceAlignment swx:DarkSide ; owl:sameAs wd:Q170505 .

swc:PrincessLeia a cga:Character ; rdfs:label "Princess Leia Organa"@en ;
    cga:portrayedBy "Carrie Fisher" ;
    schema:description "Princess of Alderaan; Senator; Rebel leader; custodian of Death Star plans"@en ;
    cga:allegiance swo:RebelAlliance ; owl:sameAs wd:Q170489 .

swc:LukeSkywalker a cga:Character ; rdfs:label "Luke Skywalker"@en ;
    cga:portrayedBy "Mark Hamill" ;
    schema:description "Moisture farm boy on Tatooine; Force-sensitive; son of Anakin"@en ;
    cga:allegiance swo:RebelAlliance ; cga:forceAlignment swx:LightSide ; owl:sameAs wd:Q51810 .

swc:ObiWanKenobi a cga:Character ; rdfs:label "Obi-Wan Kenobi"@en ; skos:altLabel "Ben Kenobi"@en ;
    cga:portrayedBy "Alec Guinness" ;
    schema:description "Jedi Master; Luke's mentor; hermit in Jundland Wastes"@en ;
    cga:forceAlignment swx:LightSide ; owl:sameAs wd:Q217032 .

swc:HanSolo a cga:Character ; rdfs:label "Han Solo"@en ;
    cga:portrayedBy "Harrison Ford" ;
    schema:description "Smuggler; captain of Millennium Falcon; reluctant hero"@en ;
    cga:occupation "Smuggler, freighter captain" ; owl:sameAs wd:Q154904 .

swc:Chewbacca a cga:Character ; rdfs:label "Chewbacca"@en ; skos:altLabel "Chewie"@en ;
    schema:description "Wookiee first mate of Millennium Falcon"@en ;
    cga:species "Wookiee" ; owl:sameAs wd:Q161171 .

swc:OwenLars a cga:Character ; rdfs:label "Owen Lars"@en ; skos:altLabel "Uncle Owen"@en ;
    schema:description "Moisture farmer; Luke's guardian uncle"@en ; cga:occupation "Moisture farmer" .

swc:BeruLars a cga:Character ; rdfs:label "Beru Lars"@en ; skos:altLabel "Aunt Beru"@en ;
    schema:description "Luke's aunt; sympathetic to Luke's ambitions"@en .

swc:GrandMoffTarkin a cga:Character ; rdfs:label "Grand Moff Tarkin"@en ;
    cga:portrayedBy "Peter Cushing" ;
    schema:description "Governor; commander of the Death Star"@en ;
    cga:allegiance swo:GalacticEmpire ; cga:militaryRank "Grand Moff" .

swc:Greedo a cga:Character ; rdfs:label "Greedo"@en ; cga:species "Rodian" ;
    schema:description "Rodian bounty hunter; works for Jabba the Hutt"@en .

swc:JabbaTheHutt a cga:Character ; rdfs:label "Jabba the Hutt"@en ; cga:species "Hutt" ;
    schema:description "Hutt crime lord; Han Solo's creditor"@en .

swc:Biggs a cga:Character ; rdfs:label "Biggs Darklighter"@en ;
    schema:description "Luke's childhood friend; Rebel X-Wing pilot Red Three"@en ;
    cga:allegiance swo:RebelAlliance .

swc:Wedge a cga:Character ; rdfs:label "Wedge Antilles"@en ;
    schema:description "Rebel X-Wing pilot Red Two"@en ; cga:allegiance swo:RebelAlliance .

swc:Tagge a cga:Character ; rdfs:label "General Tagge"@en ;
    cga:allegiance swo:GalacticEmpire ; cga:militaryRank "General" .

swc:Motti a cga:Character ; rdfs:label "Admiral Motti"@en ;
    cga:allegiance swo:GalacticEmpire ; cga:militaryRank "Admiral" .

swc:Praji a cga:Character ; rdfs:label "Commander Praji"@en ;
    cga:allegiance swo:GalacticEmpire ; cga:militaryRank "Commander" .

swc:RedLeader   a cga:Character ; rdfs:label "Red Leader"@en ; cga:allegiance swo:RebelAlliance .
swc:GoldLeader  a cga:Character ; rdfs:label "Gold Leader"@en ; cga:allegiance swo:RebelAlliance .
swc:Porkins     a cga:Character ; rdfs:label "Jek Porkins (Red Six)"@en ; cga:allegiance swo:RebelAlliance .
swc:Stormtroopers a cga:Character ; rdfs:label "Imperial Stormtroopers"@en ; cga:allegiance swo:GalacticEmpire .

swc:Jawas a cga:Character ; rdfs:label "Jawas"@en ; cga:species "Jawa" ;
    schema:description "Small Tatooine desert scavengers; trade in droids"@en .

swc:RebelSoldiers a cga:Character ; rdfs:label "Rebel Soldiers"@en ; cga:allegiance swo:RebelAlliance .
swc:Sandpeople a cga:Character ; rdfs:label "Tusken Raiders"@en ; cga:species "Tusken Raider" .
swc:MosEisleyPatrons a cga:Character ; rdfs:label "Mos Eisley Cantina Patrons"@en .
swc:RebelPilots a cga:Character ; rdfs:label "Rebel Pilots (collective)"@en ; cga:allegiance swo:RebelAlliance .
swc:RebelYavinCommand a cga:Character ; rdfs:label "Yavin Rebel Command"@en ; cga:allegiance swo:RebelAlliance .
swc:Dianoga a cga:Character ; rdfs:label "Dianoga"@en ; cga:species "Dianoga" .

# ── Places ────────────────────────────────────────────────────────────────────
swp:TantiveIV           a cga:Place ; rdfs:label "Tantive IV interior"@en .
swp:Space               a cga:Place ; rdfs:label "Open Space"@en .
swp:Tatooine            a cga:Place ; rdfs:label "Tatooine"@en ; owl:sameAs wd:Q174162 .
swp:TatooineDesert      a cga:Place ; rdfs:label "Tatooine desert surface"@en ; schema:containedInPlace swp:Tatooine .
swp:JundlandWastes      a cga:Place ; rdfs:label "Jundland Wastes"@en ; schema:containedInPlace swp:Tatooine .
swp:MosEisley           a cga:Place ; rdfs:label "Mos Eisley"@en ; schema:containedInPlace swp:Tatooine .
swp:MosEisleyCantina    a cga:Place ; rdfs:label "Mos Eisley Cantina"@en ; schema:containedInPlace swp:MosEisley .
swp:DockingBay94        a cga:Place ; rdfs:label "Docking Bay 94"@en ; schema:containedInPlace swp:MosEisley .
swp:MosEisleyStreet     a cga:Place ; rdfs:label "Mos Eisley streets"@en ; schema:containedInPlace swp:MosEisley .
swp:LarsHomestead       a cga:Place ; rdfs:label "Lars Homestead"@en ; schema:containedInPlace swp:Tatooine .
swp:LarsGarage          a cga:Place ; rdfs:label "Lars Homestead Garage"@en ; schema:containedInPlace swp:LarsHomestead .
swp:BensHut             a cga:Place ; rdfs:label "Obi-Wan's Hut"@en ; schema:containedInPlace swp:Tatooine .
swp:DeathStar           a cga:Place ; rdfs:label "Death Star"@en .
swp:DSConferenceRoom    a cga:Place ; rdfs:label "Death Star Conference Room"@en ; schema:containedInPlace swp:DeathStar .
swp:DSDetentionBlock    a cga:Place ; rdfs:label "Detention Block AA-23"@en ; schema:containedInPlace swp:DeathStar .
swp:DSMainHangar        a cga:Place ; rdfs:label "Death Star Hangar Bay 327"@en ; schema:containedInPlace swp:DeathStar .
swp:DSGarbageMasher     a cga:Place ; rdfs:label "Garbage Masher 3263827"@en ; schema:containedInPlace swp:DeathStar .
swp:DSTrench            a cga:Place ; rdfs:label "Death Star Exhaust Trench"@en ; schema:containedInPlace swp:DeathStar .
swp:DSComputerRoom      a cga:Place ; rdfs:label "Death Star Computer Alcove"@en ; schema:containedInPlace swp:DeathStar .
swp:DSHangarDeck        a cga:Place ; rdfs:label "Death Star corridors and hangar approach"@en ; schema:containedInPlace swp:DeathStar .
swp:Alderaan            a cga:Place ; rdfs:label "Alderaan"@en .
swp:AlderaanSystem      a cga:Place ; rdfs:label "Alderaan System (debris field)"@en .
swp:MillenniumFalconInterior a cga:Place ; rdfs:label "Millennium Falcon interior"@en .
swp:YavinBase           a cga:Place ; rdfs:label "Yavin 4 — Rebel Base"@en .
swp:YavinOrbit          a cga:Place ; rdfs:label "Yavin orbit / battlespace"@en .

# ── Vehicles ──────────────────────────────────────────────────────────────────
swv:TantiveIV        a cga:Vehicle ; rdfs:label "Tantive IV"@en ; cga:operator swc:PrincessLeia .
swv:StarDestroyer    a cga:Vehicle ; rdfs:label "Star Destroyer (Devastator)"@en ; cga:allegiance swo:GalacticEmpire .
swv:MillenniumFalcon a cga:Vehicle ; rdfs:label "Millennium Falcon"@en ; cga:captain swc:HanSolo .
swv:EscapePod        a cga:Vehicle ; rdfs:label "Escape Pod"@en .
swv:JawaSandcrawler  a cga:Vehicle ; rdfs:label "Jawa Sandcrawler"@en ; cga:operator swc:Jawas .
swv:LandSpeeder      a cga:Vehicle ; rdfs:label "Luke's Landspeeder"@en ; cga:operator swc:LukeSkywalker .
swv:TIEFighter       a cga:Vehicle ; rdfs:label "TIE Fighter"@en ; cga:allegiance swo:GalacticEmpire .
swv:XWing            a cga:Vehicle ; rdfs:label "X-Wing Starfighter"@en ; cga:allegiance swo:RebelAlliance .
swv:YWing            a cga:Vehicle ; rdfs:label "Y-Wing Starfighter"@en ; cga:allegiance swo:RebelAlliance .
swv:VadersTIE        a cga:Vehicle ; rdfs:label "Darth Vader's TIE Advanced"@en ; cga:operator swc:DarthVader .

# ── Organisations ─────────────────────────────────────────────────────────────
swo:GalacticEmpire  a cga:Organization ; rdfs:label "Galactic Empire"@en .
swo:RebelAlliance   a cga:Organization ; rdfs:label "Rebel Alliance"@en .
swo:ImperialSenate  a cga:Organization ; rdfs:label "Imperial Senate"@en ; cga:status "Dissolved" .
swo:HuttOrg         a cga:Organization ; rdfs:label "Jabba's Organization"@en .
swo:JediOrder       a cga:Organization ; rdfs:label "Jedi Order"@en ; cga:status "Nearly extinct" .

# ── Concepts ──────────────────────────────────────────────────────────────────
swx:TheForce    a cga:ConceptEntity ; rdfs:label "The Force"@en ; owl:sameAs wd:Q131566 .
swx:DarkSide    a cga:ConceptEntity ; rdfs:label "Dark Side"@en ; skos:broader swx:TheForce .
swx:LightSide   a cga:ConceptEntity ; rdfs:label "Light Side"@en ; skos:broader swx:TheForce .
swx:CloneWars   a cga:ConceptEntity ; rdfs:label "Clone Wars"@en .
swx:OldRepublic a cga:ConceptEntity ; rdfs:label "The Old Republic"@en .

# ── Physical Objects ──────────────────────────────────────────────────────────
swobj:DeathStarPlans a cga:PhysicalObject ;
    rdfs:label "Death Star Technical Readouts"@en ;
    schema:description "Plans containing 2m exhaust port weakness"@en ;
    cga:storedIn swc:R2D2 .

swobj:LeiaHologram a cga:PhysicalObject ;
    rdfs:label "Leia's holographic message to Obi-Wan"@en ; cga:storedIn swc:R2D2 .

swobj:AnakinLightsaber a cga:PhysicalObject ;
    rdfs:label "Anakin Skywalker's lightsaber (blue)"@en .

swobj:RestrainingBolt a cga:PhysicalObject ;
    rdfs:label "R2-D2's restraining bolt"@en .

swobj:ProtonTorpedoes a cga:PhysicalObject ;
    rdfs:label "Proton Torpedoes"@en .

swobj:ExhaustPort a cga:PhysicalObject ;
    rdfs:label "Thermal Exhaust Port"@en ;
    schema:description "2-metre target; Death Star's critical weakness"@en .

swobj:HomingBeacon a cga:PhysicalObject ;
    rdfs:label "Imperial homing beacon"@en .
```

What’s significant here is that even before you have the context graph, you have a very serviceable knowledge graph. The knowledge declares what it is, while the context graph indicates how it evolves.

[

![](https://substackcdn.com/image/fetch/$s_!-T65!,w_5760,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87dab8d6-adc3-4870-9459-b0959a72dfed_4976x8192.png)



](https://substackcdn.com/image/fetch/$s_!-T65!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87dab8d6-adc3-4870-9459-b0959a72dfed_4976x8192.png)

The movie holon holds the whole thing together:

```
# ═══════════════════════════════════════════════════════════════════════════════
# MOVIE HOLON SPINE
# ═══════════════════════════════════════════════════════════════════════════════

sw:movie-anh a cga:MovieHolon ;
    rdfs:label "Star Wars Episode IV: A New Hope"@en ;
    schema:dateCreated "1977-05-25"^^xsd:date ; schema:director "George Lucas" ;
    cga:hasInteriorGraph   sw:movie-int ;
    cga:hasBoundaryGraph   sw:shacl-shapes ;
    cga:hasProjectionGraph sw:movie-prj ;
    cga:hasContextGraph    sw:movie-ctx ;
    cga:containsHolon
        sw:s001, sw:s002, sw:s003, sw:s004, sw:s005, sw:s006, sw:s007,
        sw:s008, sw:s009, sw:s010, sw:s011, sw:s012, sw:s013, sw:s014,
        sw:s015, sw:s016, sw:s017, sw:s018, sw:s019, sw:s020, sw:s021,
        sw:s022, sw:s023, sw:s024, sw:s025, sw:s026, sw:s027 .

GRAPH sw:movie-int {
    swo:GalacticEmpire schema:adversary swo:RebelAlliance .
    swobj:DeathStarPlans cga:targettedBy swo:GalacticEmpire ; cga:soughtBy swo:RebelAlliance .
    swx:TheForce schema:description "An energy field created by all living things; surrounds and binds the galaxy"@en .
}
GRAPH sw:movie-prj {
    sw:movie-anh
        cga:narrativeFunction "Hero's journey: farm boy becomes saviour; mentor sacrifice; Force awakening"@en ;
        cga:thematicContent "Hope vs tyranny; destiny; found family; power of belief"@en .
}
GRAPH sw:movie-ctx {
    sw:movie-anh prov:wasAttributedTo sw:Analyst ;
        cga:dataSource "Star Wars Episode IV: A New Hope — full transcript"^^xsd:string .
}
```

Note that the context named graph (sw:movie-ctx) references the movie holon (sw:movie-anh) - this is what is contained within the context graph. This in turn identifies the interior graph, boundary graph, projection graph and an indirection back to the context graph, before listing the scene holons for scenes 1 to 27.

A typical scene graph (here for scene #2) follows a similar structure, with the spine of the scenes going through the holons, not the graphs.

```
# ═══════════════════════════════════════════════════════════════════════════════
# S002 — TANTIVE IV CORRIDOR BATTLE
# ═══════════════════════════════════════════════════════════════════════════════
sw:s002 a cga:SceneHolon ; rdfs:label "S002 — Tantive IV Corridor Battle"@en ;
    cga:sequenceNumber 2 ; cga:primaryLocation swp:TantiveIV ;
    cga:partOf sw:movie-anh ;
    cga:precedingHolon sw:s001 ; cga:followingHolon sw:s003 ;
    cga:hasInteriorGraph sw:s002-int ; cga:hasBoundaryGraph sw:s002-bnd ;
    cga:hasProjectionGraph sw:s002-prj ; cga:hasContextGraph sw:s002-ctx .

GRAPH sw:s002-int {
    swevt:s02a a cga:StateChange ;
        cga:content "Star Destroyer overtakes Tantive IV; reactor hit; main systems failing"@en ;
        cga:actor swv:StarDestroyer ; cga:patient swv:TantiveIV ;
        cga:estimatedTimestamp "00:02:00" .

    swevt:s02u01 a cga:Utterance ;
        cga:speaker swc:C3PO ; cga:addressee swc:R2D2 ;
        cga:content "They shut down the main reactor. We'll be destroyed for sure. This is madness. We're doomed. There'll be no escape for the princess this time."@en ;
        cga:hasEmotionalState swann:Emo_Fear, swann:Emo_Despair ;
        cga:estimatedTimestamp "00:02:15" ;
        cga:inResponseTo swevt:s02a ~ swevt:r02u01 {|
            cga:confidence "0.98"^^xsd:decimal ;
            cga:assessedBy sw:Analyst ;
            cga:rationale "C-3PO directly responds to reactor shutdown announcement"@en
        |} .

    swevt:s02b a cga:Action ;
        cga:actor swc:Stormtroopers ;
        cga:content "Stormtroopers breach airlock; corridor firefight with Rebel soldiers begins"@en ;
        cga:influencedBy swevt:s02a ~ swevt:r02b {|
            cga:confidence "1.0"^^xsd:decimal ; cga:assessedBy sw:Analyst
        |} .

    swevt:s02c a cga:Action ;
        cga:actor swc:PrincessLeia ;
        cga:content "Leia records holographic plea to Obi-Wan Kenobi; loads Death Star plans into R2-D2"@en ;
        cga:consequences swobj:LeiaHologram ;
        cga:hasMotivation swann:Mot_Duty ; cga:hasEmotionalState swann:Emo_Determination ;
        cga:estimatedTimestamp "00:03:10" .

    swevt:s02d a cga:Action ;
        cga:actor swc:DarthVader ;
        cga:content "Vader enters Tantive IV over bodies of Rebel soldiers; demands Death Star plans"@en ;
        cga:estimatedTimestamp "00:04:00" .

    swevt:s02u02 a cga:Utterance ;
        cga:speaker swc:DarthVader ; cga:addressee swc:RebelSoldiers ;
        cga:content "Where are those transmissions you intercepted? What have you done with those plans?"@en ;
        cga:hasMotivation swann:Mot_Intel ; cga:hasEmotionalState swann:Emo_Anger ;
        cga:inResponseTo swevt:s02d ~ swevt:r02u02 {|
            cga:confidence "1.0"^^xsd:decimal ; cga:assessedBy sw:Analyst
        |} .

    swevt:s02e a cga:PhysicalAction ;
        cga:actor swc:Stormtroopers ; cga:patient swc:PrincessLeia ;
        cga:content "Stormtroopers stun and capture Princess Leia"@en ;
        cga:influencedBy swevt:s02u02 ~ swevt:r02e {|
            cga:confidence "1.0"^^xsd:decimal ; cga:assessedBy sw:Analyst
        |} ;
        cga:estimatedTimestamp "00:05:00" .

    swevt:s02u03 a cga:Utterance ;
        cga:speaker swc:PrincessLeia ; cga:addressee swc:DarthVader ;
        cga:content "Darth Vader. Only you could be so bold. The Imperial Senate will not sit still for this."@en ;
        cga:hasEmotionalState swann:Emo_Indignation, swann:Emo_Defiance ;
        cga:estimatedTimestamp "00:05:30" .

    swevt:s02u04 a cga:Utterance ;
        cga:speaker swc:DarthVader ; cga:addressee swc:PrincessLeia ;
        cga:content "You weren't on any mercy mission. You are part of the Rebel Alliance and a traitor. Take her away!"@en ;
        cga:hasMotivation swann:Mot_Intel ;
        cga:inResponseTo swevt:s02u03 ~ swevt:r02u04 {|
            cga:confidence "1.0"^^xsd:decimal ; cga:assessedBy sw:Analyst
        |} .

    swevt:s02u05 a cga:Utterance ;
        cga:speaker swc:Praji ; cga:addressee swc:DarthVader ;
        cga:content "The battle station plans are not aboard this ship; no transmissions were made. An escape pod was jettisoned — no life-forms aboard."@en ;
        cga:estimatedTimestamp "00:07:00" .

    swevt:s02u06 a cga:Utterance ;
        cga:speaker swc:DarthVader ;
        cga:content "She must have hidden the plans in the escape pod. Send a detachment down to retrieve them. There'll be no one to stop us this time."@en ;
        cga:hasMotivation swann:Mot_Intel ;
        cga:inResponseTo swevt:s02u05 ~ swevt:r02u06 {|
            cga:confidence "1.0"^^xsd:decimal ; cga:assessedBy sw:Analyst
        |} .

    swevt:s02f a cga:Action ;
        cga:actor swc:R2D2, swc:C3PO ;
        cga:content "Droids escape in escape pod; jettisoned to Tatooine; no life-form reading prevents interception"@en ;
        cga:influencedBy swevt:s02c ~ swevt:r02f {|
            cga:confidence "0.97"^^xsd:decimal ;
            cga:assessedBy sw:Analyst ;
            cga:rationale "Droids escape pod launch directly follows Leia loading plans into R2"@en
        |} ;
        cga:estimatedTimestamp "00:06:30" .
}
GRAPH sw:s002-bnd {
    swevt:e002a a cga:EntityEntry ; cga:entity swc:C3PO ; cga:isFirstAppearance true ; cga:entryMode "scene-open" .
    swevt:e002b a cga:EntityEntry ; cga:entity swc:R2D2 ; cga:isFirstAppearance true ;
        cga:entryMode "scene-open" ; cga:carriedObject swobj:DeathStarPlans, swobj:LeiaHologram .
    swevt:e002c a cga:EntityEntry ; cga:entity swc:DarthVader ; cga:isFirstAppearance true ; cga:entryMode "dramatic-entrance" .
    swevt:e002d a cga:EntityEntry ; cga:entity swc:PrincessLeia ; cga:isFirstAppearance true .
    swevt:e002e a cga:EntityEntry ; cga:entity swc:Stormtroopers ; cga:isFirstAppearance true ; cga:entryMode "breach" .
    swevt:e002f a cga:EntityEntry ; cga:entity swc:RebelSoldiers ; cga:isFirstAppearance true .
    swevt:e002g a cga:EntityEntry ; cga:entity swc:Praji ; cga:isFirstAppearance true .
    swevt:e002h a cga:EntityEntry ; cga:entity swv:TantiveIV ; cga:isFirstAppearance true .
    swevt:e002i a cga:EntityEntry ; cga:entity swv:StarDestroyer ; cga:isFirstAppearance true .
    swevt:x002a a cga:EntityExit ; cga:entity swc:C3PO ; cga:destinationHolon sw:s003 ; cga:entryMode "escape-pod" .
    swevt:x002b a cga:EntityExit ; cga:entity swc:R2D2 ; cga:destinationHolon sw:s003 ;
        cga:entryMode "escape-pod" ; cga:carriedObject swobj:DeathStarPlans, swobj:LeiaHologram .
    swevt:x002c a cga:EntityExit ; cga:entity swc:PrincessLeia ; cga:entryMode "prisoner — detained aboard Devastator" .
}
GRAPH sw:s002-prj {
    sw:s002 cga:narrativeFunction "Introduces droids, Vader, Leia; MacGuffin transferred to R2; Empire establishes menace"@en ;
        cga:thematicContent "Imperial power; hope through unlikely vessels"@en ;
        cga:establishes swc:C3PO, swc:R2D2, swc:DarthVader, swc:PrincessLeia ;
        cga:prerequisiteFor sw:s003 .
}
GRAPH sw:s002-ctx {
    sw:s002 prov:wasAttributedTo sw:Analyst ;
        rdfs:comment "All causal reifications annotated inline. Context graph carries scene provenance only."@en .
}
```

The internal graph for the scene contains the dialogue and actions for that scene, and, for each utterance and action, also indicates what they were in response to. Each also provides an indication of the speaker's emotional state and motivation based on the utterance text. You can unwind any given conversation by following the `cga:inResponseTo` thread in reverse order. This can often be more useful than just following timestamps, particularly since there are four distinct conversations here that overlap.

The boundary graph indicates when characters cross the boundaries into and out of the holon. This is important for a few reasons - characters always have significance in a scene: by tracing when they enter or leave that scene, you can frequently ascertain the significance of the scene itself. This information is in fact used for determining the projection graph - from the perspective of the movie, this is the abstract and representation of the scene as an entity within the broader context of the movie itself.

Additionally, the context graph in this scene just says that annotations are stored inline to the utterances, rather than being decomposed into the context graph. Both work and are valid.

The linear spine used here — `cga:precedingHolon` / `cga:followingHolon` — reflects Star Wars’ sequential narrative structure. This works cleanly for stories and logs where there is a single thread of primary concern. For domains where holons run in parallel — simultaneous scenes, concurrent supply chain processes, multi-team organizational decisions — the linear chain is insufficient.

The natural extension is to treat the `cga:containsHolon` relationship on the parent holon as a partial order rather than a sequence: scene holons at the same `cga:sequenceNumber` are understood as concurrent rather than sequential. A `cga:synchronisesAt` property can then express the points where parallel holons rejoin — the equivalent of a cinematic crosscut resolving to a shared scene. This is left as an open design point in the current model, but worth anticipating if you are considering applying this architecture to anything more parallelized than a linear narrative.

Moreover, timestamps in this graph come in two varieties, and it’s important to distinguish them. Where a source document provides a timestamp directly, `cga:timestamp` carries that value. Where a timestamp has been estimated — by an LLM or human analyst working from utterance length, scene pacing, or contextual inference — `cga:estimatedTimestamp` is used instead, and ideally carries a reified confidence annotation:

turtle

```
swevt:s02u01 cga:estimatedTimestamp "00:02:15"
    ~ swevt:r02u01-ts {|
        cga:confidence "0.7"^^xsd:decimal ;
        cga:assessedBy sw:Analyst ;
        cga:rationale "Estimated from approximate utterance length and scene pacing"@en
    |} .
```

The confidence here is intentionally lower than the causal attributions — the estimation method is genuinely less reliable than direct textual evidence of causation.

## Querying the Graph

There are pros and cons to the holonic approach. On the plus side, this approach creates a very useful separation of concerns; there is a very natural encapsulation with context graphs that can work well in capturing data and keeping it in discrete, manageable, traceable, functional subgraphs. It also handles datalog capture especially well.

On the minus side, this approach adds some complexity to the model, especially since dealing with graph handles often means that you lose a certain amount of easy transitive closure. This isn’t necessarily that major a hardship: the script to retrieve every utterance that Leia makes throughout the movie is not especially onerous:

```
PREFIX cga:   <https://ontologist.ai/ns/cga/>
PREFIX swc:   <https://ontologist.ai/ex/sw/char/>
PREFIX swevt: <https://ontologist.ai/ex/sw/event/>
PREFIX sw:    <https://ontologist.ai/ex/sw/anh/>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT
    ?scene
    ?sceneLabel
    ?timestamp
    ?addresseeLabel
    (GROUP_CONCAT(DISTINCT ?emoSafe ; separator=" · ") AS ?emotions)
    ?content
WHERE {
    GRAPH ?intGraph {
        ?utterance  a              cga:Utterance ;
                    cga:speaker    swc:PrincessLeia ;
                    cga:content    ?content .
        OPTIONAL { ?utterance cga:estimatedTimestamp ?timestamp . }
        OPTIONAL { ?utterance cga:addressee          ?addr . }
        OPTIONAL {
            ?utterance cga:hasEmotionalState ?emo .
            ?emo  a cga:EmotionalState ;
                  rdfs:label ?emoLabel .
        }
        BIND(COALESCE(?emoLabel, "") AS ?emoSafe)
    }
    ?scene cga:hasInteriorGraph ?intGraph ;
           rdfs:label ?sceneLabel .
    OPTIONAL { ?addr a cga:Character ; rdfs:label ?addresseeLabel . }
}
GROUP BY ?scene ?sceneLabel ?timestamp ?addresseeLabel ?content
ORDER BY ?scene ?timestamp ?utterance
```

In this case, you iterate through each of the interior graphs by limiting the query to just those graphs, then, once you have the scene established. This also combines all emotional markers into a single field.

Note: `?scene` is included in `GROUP BY` to ensure correct aggregation across multiple interior graphs that may share scene labels; it appears in the SELECT for completeness even if downstream display suppresses the raw IRI.

For the above example, the output then looks like the following:

[

![](https://substackcdn.com/image/fetch/$s_!7nmW!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda5e5513-a638-446f-8023-53f447c7e414_1972x1454.png)



](https://substackcdn.com/image/fetch/$s_!7nmW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda5e5513-a638-446f-8023-53f447c7e414_1972x1454.png)

The above query worked, but the initial run highlighted the fact that we were estimating the time stamps rather than drawing from the source (which lacked them), while the addressee required some additional analysis to infer the likely addressee, since it was not obvious even with a first pass analyis. Since Leia tended to make snarky comments that were not clearly directed toward any one character, this fell into a gray zone that the LLM needed additional clarity to answer fully.

---

Before moving on, it’s worth being precise about what these two query modes actually are, because they serve different purposes and should not be conflated.

The SPARQL query above requires a SPARQL-capable runtime — a triple store, an in-memory quad store like Apache Jena, or a SPARQL-over-file tool like SPARQL Anything. It is deterministic, formally correct, and reproducible. If the graph is valid, the query returns exactly the right rows every time.

What follows is something different: using the TriG document itself, unparsed, as a direct input to an LLM prompt. This works because the normalised, self-describing structure of RDF makes the document largely legible to a language model without the need for a query engine to intermediate. The tradeoff is that you trade formal precision for inferential flexibility — the LLM can answer questions that would require complex multi-hop SPARQL to express, but the answers carry statistical rather than logical certainty.

Neither mode replaces the other. The claim that “not once did I put content into a triple store” applies to the _LLM query path_ — and that is still a meaningful observation, because a large and growing category of useful questions can now be answered against a serialised knowledge graph without a data infrastructure dependency. The SPARQL path remains essential when you need exact, auditable, reproducible answers.

> **Two Query Modes, Two Guarantees**
> 
> _SPARQL over a triple store:_ deterministic, auditable, requires infrastructure.
> 
> _LLM over a TriG document:_ inferential, flexible, requires only a file and a model.
> 
> Both appear in this article. They are complementary, not interchangeable.

This has actually been one of the big gating factors toward using a straight knowledge graph approach - you either needed to query the KG to get tabular content (which loses connections) or you needed to do complex queries to isolate content within the triple store itself. In the context graph case above, however, you have a self-contained knowledge graph that can still be validated (perhaps in an offline process) then cached or persisted for retrieval, without necessarily putting it into a triple store. You still might want to do that for analytics purposes, mind you, but that becomes a separate problem from using this data with an LLM.

This also helps to resolve another problem. Context graphs are essentially append-only logs. Logs inevitably fill up, and consequently older data needs to be either dropped or archived. If you were to take a metadata snapshot of a contained context graph and persist that with a URL link to the resource in question, then retrieving a specific log file becomes trivial.

This approach works cleanly at the scale of a single media property or a bounded project context, where the total TriG document fits comfortably within an LLM’s context window — currently in the range of 100K to 200K tokens for frontier models, which accommodates roughly 500–800KB of dense RDF. Beyond that threshold, you need a retrieval layer.

The natural retrieval unit is the holon itself. Because each scene holon is a self-contained named graph cluster with a known IRI and a projection graph summarizing its narrative function, you can build a lightweight metadata index — essentially a SKOS-style summary graph containing only the projection graphs and entity boundary events from each holon — that fits in context and serves as a routing document. An agentic service can query that index to identify which holon files are relevant, then load only those. This is a form of RDF-native RAG (Retrieval-Augmented Generation), and the holonic structure makes it considerably cleaner than chunking prose: your retrieval boundaries are semantically meaningful rather than arbitrary.

For very large deployments — supply chain event logs, continuous organizational decision records — you will almost certainly need a triple store for analytics alongside the document-as-blob approach for LLM consumption. These are not competing architectures; they serve different query patterns.

For instance, you can create separate context logs for each media project in the Star Wars universe and have an agentic service load the relevant files at query time.

The principal downside to this approach is that you become more dependent upon the LLM “filling in the blanks” and potentially hallucinating the data. One way to mitigate this is to take advantage of the context annotations to indicate what is “known” data coming from a curated source, with anything that doesn’t have a clear provenance trail being indicated in the output as such, as is the case from above where we’re already asking the LLM to fill in the blanks in the generation of the content from the transcript in the first place (there are no timestamps in the source, for instance, so these have to be estimated).

The other advantage of using the context graph is a contained source is that you can make queries as prompts in the LLM that would be difficult or impossible to do with SPARQL. For instance,

```
Given the attached context graph, identify the decisions made by Darth Vader, 
Obi-Wan Kenobi and Luke Skywalker, and their consequences on the direction of the movie, 
as a table
```

After a bit of spinning, this generates the following:

[

![](https://substackcdn.com/image/fetch/$s_!pAqb!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a8acea2-4909-437e-82d7-727939c933c3_1844x1630.png)



](https://substackcdn.com/image/fetch/$s_!pAqb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a8acea2-4909-437e-82d7-727939c933c3_1844x1630.png)

This is at the heart of a decision support system - examining the logs to find when decisions were made, what the motivating factors were in making those decisions, and the consequences of those decisions. The data to do this was inherent within the context graph, but the query to write it in SPARQL would have beyond most people, and moreover would probably only be useful once. This is an area where LLMs do well.

Another unexpected consequence of this: retrospective patching. The LLM (Claude here) identified several points where additional content could have been inferred from the original generation but wasn’t; it was only obvious upon retrospection that these needed to have been in there (the same could be said for timestamp estimates and addressee fields). This is a key aspect of learning - looking back at your mistakes and adjusting what' is known as a consequence.

This information could be encoded as triples. I specifically asked Claude to surface just these new triples (which it did) then to apply it as a post-facto patch, below:

```
# ###############################################################################
# ANH HOLONIC CONTEXT GRAPH - DECISION PATCH
#
# Adds to the v2 graph:
#   (A) Additional  a cga:Decision  type on existing Action/StateChange events
#       whose actors are Vader, Obi-Wan, or Luke and that function as pivotal
#       choices in the narrative.
#   (B) Three new cga:Decision events whose corresponding choice was previously
#       expressed only through an Utterance or had no IRI at all.
#   (C) cga:consequences triples on the four existing Luke cga:Decision events
#       that were missing them.
#
# Each assertion in interior graphs carries an inline reifier annotation
# (confidence + rationale) per the Turtle 1.2 / RDF 1.2 pattern in v2.
#
# MERGE STRATEGY: Load this file into the same dataset as v2; graphs are
# additive - no existing triple is modified or retracted.
#
# Authors : Kurt Cagle / Claude Sonnet 4.6 - The Ontologist Newsletter
# Date    : 2026-03-23
# ###############################################################################

@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:    <http://www.w3.org/2002/07/owl#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix prov:   <http://www.w3.org/ns/prov#> .

@prefix cga:    <https://ontologist.ai/ns/cga/> .
@prefix sw:     <https://ontologist.ai/ex/sw/anh/> .
@prefix swc:    <https://ontologist.ai/ex/sw/char/> .
@prefix swp:    <https://ontologist.ai/ex/sw/place/> .
@prefix swv:    <https://ontologist.ai/ex/sw/vehicle/> .
@prefix swobj:  <https://ontologist.ai/ex/sw/object/> .
@prefix swevt:  <https://ontologist.ai/ex/sw/event/> .
@prefix swann:  <https://ontologist.ai/ex/sw/ann/> .

sw:Analyst a prov:Agent ;
    rdfs:label "Holonic Analyst (Cagle/Claude Sonnet 4.6) — decision patch"@en .

# ###############################################################################
# (A) TYPE ELEVATION  - existing IRIs; only new triples added
# ###############################################################################

# ## A1. S002 # Vader boards Tantive IV and demands plans (swevt:s02d) #########
GRAPH sw:s002-int {
    swevt:s02d a cga:Decision ;
        cga:consequences swv:EscapePod ~ swevt:r02d-conseq-a {|
            cga:confidence  "0.99"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Vader's seizure of the ship directly forces the droid escape-pod launch"@en
        |} ;
        cga:consequences swobj:DeathStarPlans ~ swevt:r02d-conseq-b {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Plans remain with R2 because Vader fails to retrieve them before pod launches"@en
        |} .
}
GRAPH sw:s002-ctx {
    sw:s002 rdfs:comment
        "Decision patch: swevt:s02d elevated to cga:Decision; two consequences asserted."@en .
}

# ## A2. S010 # Vader Force-chokes Motti (swevt:s10a) #########################
GRAPH sw:s010-int {
    swevt:s10a a cga:Decision ;
        cga:consequences swx:TheForce ~ swevt:r10a-conseq {|
            cga:confidence  "0.95"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Demonstration cements Force as a real power within the Imperial command structure"@en
        |} .
}
GRAPH sw:s010-ctx {
    sw:s010 rdfs:comment
        "Decision patch: swevt:s10a elevated to cga:Decision; The Force noted as consequence."@en .
}

# ## A3. S009 # Obi-Wan presents Anakin's lightsaber (swevt:s09a) #############
#   Note: cga:consequences swobj:AnakinLightsaber already asserted in v2.
#   We add the withholding-of-truth as a second consequence.
GRAPH sw:s009-int {
    swevt:s09a a cga:Decision ;
        cga:consequences swc:LukeSkywalker ~ swevt:r09a-conseq {|
            cga:confidence  "0.98"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Presenting the lightsaber and framing Vader as betrayer seeds Luke's Jedi destiny; deliberate omission of Vader's true identity shapes Luke's motivation throughout the trilogy"@en
        |} .
}
GRAPH sw:s009-ctx {
    sw:s009 rdfs:comment
        "Decision patch: swevt:s09a elevated to cga:Decision; Luke's seeded destiny noted as consequence."@en .
}

# ## A4. S016 # Obi-Wan trains Luke with blast shield down (swevt:s16b) ########
GRAPH sw:s016-int {
    swevt:s16b a cga:Decision ;
        cga:consequences swevt:s27d ~ swevt:r16b-conseq {|
            cga:confidence  "0.92"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "The blast-shield training establishes Luke's trust in the Force without visual input, directly enabling the targeting-computer switch-off at Yavin"@en
        |} .
}
GRAPH sw:s016-ctx {
    sw:s016 rdfs:comment
        "Decision patch: swevt:s16b elevated to cga:Decision; causal link to s27d noted."@en .
}

# ## A5. S023 # Obi-Wan allows himself to be struck down (swevt:s23c) ##########
GRAPH sw:s023-int {
    swevt:s23c a cga:Decision ;
        cga:consequences swevt:s27d ~ swevt:r23c-conseq-a {|
            cga:confidence  "0.97"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Obi-Wan's transcendence enables his disembodied voice to guide Luke at Yavin; sacrifice is instrumentally necessary for the Force-guided torpedo shot"@en
        |} ;
        cga:consequences swevt:s27g ~ swevt:r23c-conseq-b {|
            cga:confidence  "0.95"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Without Obi-Wan's post-death guidance the Death Star is not destroyed in this engagement"@en
        |} .
}
GRAPH sw:s023-ctx {
    sw:s023 rdfs:comment
        "Decision patch: swevt:s23c elevated to cga:Decision; consequences link to s27d and s27g."@en .
}

# ## A6. S005 # Luke removes R2-D2's restraining bolt (swevt:s05b) #############
GRAPH sw:s005-int {
    swevt:s05b a cga:Decision ;
        cga:consequences swobj:LeiaHologram ~ swevt:r05b-conseq-a {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Removing the bolt enables the full hologram to play; partial hologram in restrained state only hinted at Obi-Wan's name"@en
        |} ;
        cga:consequences swevt:s05u05 ~ swevt:r05b-conseq-b {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Full message triggers Luke's 'old Ben Kenobi' recognition — the call to adventure made explicit"@en
        |} .
}
GRAPH sw:s005-ctx {
    sw:s005 rdfs:comment
        "Decision patch: swevt:s05b elevated to cga:Decision; hologram and Luke's recognition as consequences."@en .
}

# ###############################################################################
# (B) NEW DECISION EVENTS - choices previously expressed only as utterances
#     or with no IRI at all
# ###############################################################################

# ## B1. S021 # Vader's decision to confront Obi-Wan alone ####################
#   The choice is surfaced through utterance swevt:s21u03 but was not typed
#   as a cga:Decision. New IRI: swevt:s21dec
GRAPH sw:s021-int {
    swevt:s21dec a cga:Decision ;
        cga:actor             swc:DarthVader ;
        cga:content           "Vader resolves to confront Obi-Wan personally and alone, breaking from the command briefing"@en ;
        cga:estimatedTimestamp "01:18:30" ;
        cga:hasMotivation     swann:Mot_Vengeance ;
        cga:hasEmotionalState swann:Emo_Determination ;
        cga:inResponseTo      swevt:s21u01 ~ swevt:r21dec-trigger {|
            cga:confidence  "0.97"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Vader's Force tremor perception (s21u01) directly motivates the decision to break and act"@en
        |} ;
        cga:consequences      swevt:s23b ~ swevt:r21dec-conseq-a {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Vader going unescorted to the hangar is the direct precondition of the duel"@en
        |} ;
        cga:consequences      swevt:s23c ~ swevt:r21dec-conseq-b {|
            cga:confidence  "0.97"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Vader's personal presence in the hangar, not delegated to stormtroopers, creates the conditions for Obi-Wan's chosen sacrifice"@en
        |} .
}
GRAPH sw:s021-ctx {
    sw:s021 prov:wasAttributedTo sw:Analyst ;
        rdfs:comment "Decision patch: new swevt:s21dec captures Vader's choice to face Obi-Wan alone."@en .
}

# ## B2. S018 # Obi-Wan departs alone to disable the tractor beam #############
#   The choice was expressed in utterance swevt:s18u03 but the departure
#   action itself had no Decision-typed IRI.
GRAPH sw:s018-int {
    swevt:s18dec a cga:Decision ;
        cga:actor             swc:ObiWanKenobi ;
        cga:content           "Obi-Wan resolves to disable the tractor beam alone, explicitly separating his path from Luke's"@en ;
        cga:estimatedTimestamp "01:10:30" ;
        cga:hasMotivation     swann:Mot_Duty ;
        cga:hasEmotionalState swann:Emo_Acceptance ;
        cga:inResponseTo      swevt:s18b ~ swevt:r18dec-trigger {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "R2's discovery of the tractor-beam control locations (s18b) is the immediate prompt for Obi-Wan's decision"@en
        |} ;
        cga:consequences      swevt:s23c ~ swevt:r18dec-conseq-a {|
            cga:confidence  "0.96"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Obi-Wan's solitary mission path leads him to the hangar corridor where Vader is waiting; the sacrifice is a foreseeable consequence of choosing to go alone"@en
        |} ;
        cga:consequences      swevt:s14d ~ swevt:r18dec-conseq-b {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Tractor beam disabled → Falcon can depart — proximate consequence of the mission succeeding"@en
        |} .
}
GRAPH sw:s018-ctx {
    sw:s018 prov:wasAttributedTo sw:Analyst ;
        rdfs:comment "Decision patch: new swevt:s18dec captures Obi-Wan's choice to go alone."@en .
}

# ## B3. S027 # Vader enters the trench personally in his TIE Advanced #########
#   No Action IRI existed for this choice in the v2 graph.
GRAPH sw:s027-int {
    swevt:s27vdec a cga:Decision ;
        cga:actor             swc:DarthVader ;
        cga:content           "Vader personally joins the trench battle in his TIE Advanced rather than directing from the Death Star command deck"@en ;
        cga:estimatedTimestamp "01:50:00" ;
        cga:hasMotivation     swann:Mot_Power ;
        cga:hasEmotionalState swann:Emo_Arrogance, swann:Emo_Determination ;
        cga:consequences      swevt:s27e ~ swevt:r27vdec-conseq {|
            cga:confidence  "0.98"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Vader in the trench is the direct target of Han Solo's return attack; had Vader remained on the Death Star, Han's intervention would not have cleared Luke's run"@en
        |} .
}
GRAPH sw:s027-ctx {
    sw:s027 prov:wasAttributedTo sw:Analyst ;
        rdfs:comment "Decision patch: new swevt:s27vdec captures Vader's choice to enter the trench personally."@en .
}

# ###############################################################################
# (C) CONSEQUENCES ON EXISTING LUKE DECISIONS - all four were missing this
# ###############################################################################

# ## C1. S009 # swevt:s09c # Luke refuses the call ############################
GRAPH sw:s009-int {
    swevt:s09c
        cga:consequences swevt:s11c ~ swevt:r09c-conseq {|
            cga:confidence  "0.99"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "The refusal leaves Luke at the homestead; the destruction of the homestead (s011) is what converts the refusal into the acceptance — s09c is the necessary precondition of s11c"@en
        |} .
}

# ## C2. S011 # swevt:s11c # Luke accepts the call ############################
GRAPH sw:s011-int {
    swevt:s11c
        cga:consequences sw:s012 ~ swevt:r11c-conseq-a {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Acceptance drives immediate departure toward Mos Eisley; all subsequent Death Star scenes depend on this threshold crossing"@en
        |} ;
        cga:consequences swevt:s14d ~ swevt:r11c-conseq-b {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Departure from Tatooine aboard the Falcon is the direct downstream event"@en
        |} .
}

# ## C3. S019 # swevt:s19a # Luke devises the disguise plan ###################
GRAPH sw:s019-int {
    swevt:s19a
        cga:consequences swevt:s20a ~ swevt:r19a-conseq-a {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "The disguise plan is directly executed as the detention block infiltration"@en
        |} ;
        cga:consequences swc:PrincessLeia ~ swevt:r19a-conseq-b {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Leia's rescue is the stated goal and outcome of the plan"@en
        |} ;
        cga:consequences swobj:DeathStarPlans ~ swevt:r19a-conseq-c {|
            cga:confidence  "0.95"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Leia's rescue reunites the plans-custodian with R2; both reach Yavin, enabling the briefing and battle"@en
        |} .
}

# ## C4. S027 # swevt:s27d # Luke switches off targeting computer #############
GRAPH sw:s027-int {
    swevt:s27d
        cga:consequences swevt:s27f ~ swevt:r27d-conseq-a {|
            cga:confidence  "1.0"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "Switching off the computer is the immediate precondition for the Force-guided torpedo shot (s27f); without it Luke would have fired on targeting data alone and missed"@en
        |} ;
        cga:consequences swevt:s27g ~ swevt:r27d-conseq-b {|
            cga:confidence  "0.99"^^xsd:decimal ;
            cga:assessedBy  sw:Analyst ;
            cga:rationale   "The chain reaction destruction of the Death Star is the terminal consequence of this single decision"@en
        |} .
}
```

This is where RDF shines as a data format - patching does not involve rewriting the existing context graph, but simply appending the patch to the document. This retrospective approach also works well with the context graph as a document approach: you can clearly trace change provenance, and the graph becomes more self-aware over time, so you can log not only new changes to the base but also more nuanced interpretations that only become clear as the graph grows and becomes richer.

## Applications and Takeaways

As my regular readers may have noted, I tend to write in order to better understand, not just for my audience. There were some surprising consequences to this approach, significant ones for how we address knowledge graphs and context graphs within the province of LLMs.

- _Not once in this whole process did I put content into a triple store._ Let that one sink in for a bit. I did semantic manipulation for a fairly complex graph without ever needing to parse it, index it, or otherwise deal with a data container more complex than a TRIG-formatted text file. Indeed, in most cases in the last few months, I’ve had to create an LLM-based emulator of a SHACL 1.2 validator or similar tool _because the technology to do it in a triple store had not yet caught up with the spec_. Will bespoke executable code be faster? Absolutely, but the very fact that we can create such a pre-emulator in the first case should tell you where we’re going. The triple store will give you efficiency and performance, but it is no longer a prerequisite for working with semantics. I think this is a huge shift.
    
- _The holonic approach works._ There is more overhead, but by separating scene graphs holonically, you enforce the concept of holonic boundaries and projections - you see only what you need to see, transit across boundaries creates traces that can be logged and interpreted, and you can cleanly append content without having to go through complex ingest issues. Holons create graphs of graphs and are a critical step in constructing hypergraphs.
    
- _Packaging Holons._ The process of going from a transcript to a context graph holon creates a natural data package that effectively contains not only the holons but also any additional relevant declarations (such as taxonomic metadata or entity declarations/definitions). These can be persisted as text blobs rather than indexed, because such are a natural substrate for LLMs to work with as a queryable serialised document, and the normalised nature of RDF means that an append-only architecture can prove especially effective, especially in conjunction with a context “deprecated” flag for indicating when specific assertions are no longer in force.  
    The normalised nature of RDF means that an append-only architecture can prove especially effective. This also means that provenance distinctions — between source-provided data, analyst-inferred data, and LLM-estimated data — should be maintained consistently throughout the model, not just for causal attributions but for all asserted values, including timestamps.
    
- _Serialisation as Holons._ Any event tracking function, from the flow of text in a book to music and media to supply chain movements to organisational dynamics and decision making to production systems, legal code making, and financial reporting, all of these can be expressed in a holonic manner. I suspect that PROV-O, with its emphasis on process, could be recast in holonic terms almost trivially.
    
- _Context Graphs are built on Knowledge Graphs_, as the Entity Flow Knowledge Graph illustrates. Such knowledge graphs can be thought of as the initial state (or initial conditions) of the context graph, with each holon, in turn, being an interactive evolution of a particular scene graph that leaves its imprint at the boundaries of the holon in question.
    
- **A note on LLM-emulated validation.** Throughout this process, SHACL 1.2 validation was performed by an LLM emulator rather than a conformant validator, because tooling for SHACL 1.2 Working Draft features — particularly `sh:reifierShape` and the new reification syntax — has not yet fully caught up with the specification. This is worth naming honestly.  
      
    SHACL validation is formally precise and closed-world: a conformant validator produces a deterministic result. An LLM emulator is statistically approximate and open-world. The confidence annotations in the reifications could be systematically wrong in ways that are invisible in the output, and there is currently no easy way to verify them without running a conformant engine.  
    
    This is not a reason to avoid the approach — it’s a reason to treat LLM-emulated validation as a development-time approximation rather than a production guarantee. As conformant SHACL 1.2 tooling matures, the emulated validation step should be replaced with or augmented by a proper validator. The architecture anticipates this: the boundary graph and its shapes are already isolated in their own named graph, making it straightforward to drop in a real validator once the tooling is ready.
    

There are a few caveats worth bringing up, however:

- Holonic Concept Graphs depend on three critical technologies: reification, named graphs, and validation/rule systems. These are beginning to emerge in existing tool systems, but the specifications are still evolving (named graphs have not yet been more than obliquely touched in RDF 1.2, as one example, though it is possible that it may end up becoming an extension standard to SHACL 1.2). This means that while you can build context graphs as outlined here now, it’s likely going to be across LLM emulators for some time. I hope to help facilitate the changes necessary to make these things first within the RDF community, and hopefully in a way that can be expressed within LPGs such as Neo4J and GQL as well.
    
- _Note: I have dissociated myself from the W3C Context Graph Community Group, as I believe that it is being set up by its chair under false pretences to solve a problem that has nothing to do with context graphs, or even graph technology in general._
    
- I see context graphs as being a major substrate for grounding large language models, a stance I’m seeing more and more reflected in the machine learning community as well. It won’t “fix” the problems inherent with LLMs - the malleability and uncertainty are the price you pay for the inherent confabulatory nature of LLMs, but it will significantly mitigate effects when you need to ensure an accurate world model.
    
- I have not touched on Active Inference in depth, though the architecture here is graph-centric for building an ActInf system. I expect that as we begin to build out something like the holon model, active inference, and the minimisation of surprise as a means of achieving the evolution of a system, these will factor more and more heavily.
    
- Finally, I don’t want to get bogged down in OWL inferencing vs. SHACL arguments; you need both. SHACL can tell you about the graph as is, and can even manage a projection graph layer, but OWL is a semantic layer used heavily by business, legal, educational, medical and scientific domains, and the rules of semantic generalisation hold as much today as they did a decade ago.
    

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!dzjw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f2c1ff0-19e5-4e2e-8534-1edff781eb6f_2048x2048.png)



](https://substackcdn.com/image/fetch/$s_!dzjw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f2c1ff0-19e5-4e2e-8534-1edff781eb6f_2048x2048.png)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)  
[The Ontologist](https://ontologist.substack.com/)

If you like these articles, please consider becoming a paid subscriber. It helps me support my work so I can continue writing code, in-depth analyses, educational pieces, and more.

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly. If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.

_© 2026 Kurt Cagle and Claude Sonnet 4.6 for The Ontologist Newsletter. This article reflects the state of both ecosystems as of early 2026. Specification and tooling status evolve rapidly; readers should verify the current implementation support for specific features before making an architectural commitment._

_Kurt Cagle is a consulting ontologist and the publisher of The Ontologist and The Cagle Report newsletters._