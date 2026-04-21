---
title: "The Open World/Closed World Conundrum"
source: "https://ontologist.substack.com/p/the-open-worldclosed-world-conundrum?utm_source=profile&utm_medium=reader2"
date: "Mar 14"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!zGSg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F998095ec-096b-4dde-a833-714555a3cda2_4096x2344.jpeg)

](https://substackcdn.com/image/fetch/$s_!zGSg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F998095ec-096b-4dde-a833-714555a3cda2_4096x2344.jpeg)

_This is a long article, perhaps a tldr; type article, but I present it largely as an exploration of how we build world models, which I see as likely the next major area of innovation in the tech space._

## A Sense of Place

About once a month, a motley group of adventurers used to descend upon my house. Wizards and warriors, thieves and priests, witches and bards, the adventurers would come armed with their trustee weapons, figurines, guidebooks, and dice in order to wend their way through the world of Illioth, fighting the pirates of the southern seas, the ice necromancers of the Northern Wastes, the dreaded morlocks of the Hebrian mountains, and the Mages of Doriath. Through all of this, I learned a great deal about representing the spatial world.

[

![](https://substackcdn.com/image/fetch/$s_!oYgU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec2d0b09-96d8-4436-bcc1-c91cc399ad98_1488x2048.jpeg)

](https://substackcdn.com/image/fetch/$s_!oYgU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec2d0b09-96d8-4436-bcc1-c91cc399ad98_1488x2048.jpeg)

This may sound like a strange segue, but there’s a solid foundation behind it.

When you create a tabletop adventure game, you are in effect creating a different world. This may seem obvious, of course, that you’re creating a different world … but it also highlights many things that have very real-world applications. For instance, most of the place names within the world do not exist in the real world, so you have to think about what exactly a place means in this context.

If I create a city named Doriath, for instance, what is its boundary? How big is it? What units are those dimensions measured in? Should I use miles, kilometres, furlongs, cubits or quatlus? Do I need to model the entire city in high detail, or should I focus on the areas that are likely to impact the game? What happens when I hit the boundary between two different sectors? What if I want to model a particular building or complex? Should this be a part of the map, or should it have its own map? What exactly do I mean by a map anyway?

I have little pewter figures (often mistakenly called lead figures, though most modern figures are either pewter or plastic), each of which is sized just right to move around at least some of the maps. That figure serves as a marker indicating the character's position within the map, but in most cases, the icon is positioned on a grid structure (typically either square or hexagonal). That figure can be thought of as the representation (or avatar) of a player character (PC) or a non-player character (NPC) on the world map. I’ll get back to this point in a bit, because it’s important.

[

![](https://substackcdn.com/image/fetch/$s_!R5Cn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa6bfeb7-512a-4dd6-97d2-6049d2460050_864x1184.jpeg)

](https://substackcdn.com/image/fetch/$s_!R5Cn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa6bfeb7-512a-4dd6-97d2-6049d2460050_864x1184.jpeg)

It is impossible to create a perfectly faithful map of the world, even in virtual space. This is because a map, in essence, is a bounded model of a thing, a simplification of that thing that focuses on one particular aspect or dynamic of the broader system. A map also provides a vehicle for providing metadata associated with regions. For instance, in the “real world” as viewed from space, there are no discernible markers for countries. There may be border crossings at highways, on occasion, or fences or walls, but the concept of a national or regional boundary is metadata—a shape that exists in the abstract.

A country (or any governmental entity) is a fascinating construct - it is a geographical area with an associated governmental organisation, a defined boundary, and a population. Most, but not all, countries have other places associated with them, such as subnational regions, provinces, counties, cities, and so on. With the implicit assumption that because such things exist within the boundary of the country in question, then they are “inside” the country. There are exceptions, of course: Vatican City comes to mind, as a recognised country (with the interesting implications about what exactly is the criterion for recognition) that is nonetheless wholly contained within another country (Italy).

In fact, a country's boundary does not necessarily need to be fully contiguous; it can have gaps and extend beyond the borders of other countries. For instance, the fairly small country of Denmark extends to the much larger island of Greenland. These anomalies are often designated as Territories, meaning they are considered part of a sovereign country that nonetheless does not necessarily have full governmental rights.

There are similarly anomalous cases where a country is considered fully sovereign while also containing other semi-autonomous sovereign entities; Great Britain is the obvious example, comprising England, Scotland, Wales, and Northern Ireland. This is one reason why toponomic ontologies (primarily taxonomies of places) can become so confusing.

This becomes even more problematic when dealing with larger regions, such as continents. Every schoolchild knows that there are seven continents, but from a geological perspective, this is far from given. For instance, in the US, we view Europe and Asia as two distinct continents.

However, geologically, they are a single, continuous landmass, except for India, which collided with the Asian continent around 55 million years ago; although it is now largely permanently welded to the Asian plate. Similarly, the Arabian Peninsula was once part of Africa until a continental rift formed in what is now known as the Red Sea, creating a subcontinent. In 10 million years or thereabouts, the Persian Gulf will disappear, and the Arabian Peninsula will become a contiguous land mass with Iran.

Oh, and by the way, Australia should be mentioned for Continental speed records. It is moving northward at a rate of 7 cm (about 3 inches) per year. While this may not seem like a lot, it’s enough that GPS signals need to be recalibrated every decade or so because the continent is moving at a significant rate. Around 25,000 years from now, it is expected to reach the southern islands of Indonesia, and within 50 million years, Australia, Indonesia, and Papua New Guinea will have merged into a single continent. And while we’re at it, don’t forget New Zealand, which is on its own separate (mostly underwater) tectonic plate called (not surprisingly) Zealandia that’s roughly half the size of Australia.

This means the concept of place is fairly arbitrary and can be seen, in many respects, as an abstraction. For instance, I’ve mentioned Cascadia before. Cascadia does not exist as a political entity, and its boundaries are somewhat amorphous. However, you can think of it as being roughly aligned with the watershed that extends from very northern California all the way up to the border between British Columbia and the Yukon (or, put another way, it is the Biome that encompasses the Columbia River, the Puget Sound, and the Fraser River). It is actually about the same size and shape as New Zealand, and it has a remarkably similar ecosystem.

Cascadia is not a country, but if it were, it would be the 19th-largest economy in the world, with a GDP of just over $1.1 trillion, comparable to the Netherlands and Saudi Arabia, and a population roughly equivalent to that of Ukraine. It is, however, a place - it can be referred to, and even has specific characteristics that are similar to those of other countries, such as gross domestic product, net imports and exports, government structure, population, history, and so forth. That we would have trouble identifying its border is not an issue; one can still point to a map of the world and say, “Here is Cascadia”. This is largely because our notion of place is not necessarily tied to precise coordinates, but is far more vague and fluid.

Whether you are talking about a recognised place (such as Seattle), an unrecognised but potential place (Cascadia) or an imaginary place (Illioth, above), such places are conceptual first. That is to say, there exists a concept of Cascadia or Illioth that precedes its existence as a spatial entity. This is important because it ultimately depends on how we model such spaces, which have very real semantic (graph) implications.

## Places and Scenes

As both an author and a game master, one of the first things that I do when starting a narrative is to establish the scenes of the story or game. This is the same thing that a director does when planning a movie. The author, game master, or director all understand that while they are portraying a reality, they have to wall that reality off, reduce the overall context that the audience is perceiving

There is a distinction between a place and a scene. The **place** establishes the _where_ of a given character. The **scene** is composed of the events that occur within that place, and as such, can be seen as a form of local context. In effect, a scene is the story (_or history_) of a _place_ with a given set of _characters_ (as portrayed by _actors_) manipulating _things_ within that place. Conceptually, these overlap to a significant degree.

Note that these are both distinct from position. For instance, in a play, the stage itself is broken down into distinct subsections - upstage, downstage, stage left, stage right, centre stage, backstage, the proscenium and so forth. These generally provide a set of directions to the stage. Directors also frequently place marks in electrical tape on the stage when in rehearsals, which represent specific spots on the stage that the actor needs to position themselves. Consequently, there are many places, but usually only one active scene at any given time.

Games use a similar mechanism. There is usually an established scene - a tavern, a dragon’s cave, a haunted house. There may be multiple named places within the scene, and, of course, characters can move from one place to another within that scene. What is most notable is the notion of a scene transition, as you move from one scene to another.

-   On stage, this is usually accomplished by clearing the stage of props, such as walls, chairs, and tables, then placing new props into position before the next scene begins.
    
-   In a book, there is usually a new chapter or section that acts as a pause, with the author then “setting the stage” for the next scene through some form of exposition.
    
-   In a movie, this may be a cut scene or a transition (a shift from a planetside desert to a deep space shot as a large spacecraft moved across the screen).
    
-   In a game, this was historically accomplished by having an expository scene (frequently a video) that indicated the transition, as well as providing additional background information. It also typically involves unloading the current state of the game and loading in a new state, including props, characters, and other elements.
    

What’s worth noting is that the scene is context: the shift from Tattooine’s surface to the Imperial battleship (and from there to the bridge of that same ship) indicates that a new narrative thread is either starting or continuing from where it was previously left off.

## Narrative Structures, Music, and Scripts

In my previous article, I discussed narrative structures, which follow a specific narrative order. Note that such an order is not necessarily linear or monotonic. You can have a scene follow another scene in narrative order, but that may represent a flashback to a previous point in time or a time skip that signifies a significant passage of time. What’s important is that the narrative order ultimately leads through an arc to a given objective or completion.

We tend to refer to code as “scripting” (and indeed, the HTML code block is named a _**script**_ block for a reason), but even before this, we used (and still use) scripts as narrative constructs to describe spatio-temporal events. As you read a script, your **focus** or **attention** is going to follow that narrative flow, to the extent that you can “bookmark” a particular section. Music follows this same convention. A musical score is a narrative script for multiple instruments (agents) to play sequences and combinations of notes in specific ways.

My contention is that if you are going to create a digital twin of a real-world (or even imaginary world) phenomenon, then you are in fact creating a narrative. This is true whether you are creating a novel, a movie, a game, a drone operation, a virtual reality experience, a digital twin, or an IoT handler; you need to understand that what you are doing is telling a story that produces a history.

There are, in fact, two different ways of thinking about history. The first is generative - while you may have some goals in mind, you do not know where the story will end, and even knowing that there IS an end is not guaranteed. This is a lot like an adventure game where there may be many (potentially an infinite number) of possible endings, and you will only know that the path you take will end up in one of those. This is the author’s journey, the struggle to reach the best (or at least most entertaining) possible ending.

The second is archival - you (or someone) has taken the path through the narrative and reached an ending, and you now have a recording of that ending (including potential branch points and reconnection points). You can relive that narrative, but it is effectively a read-only journey at that point, a simulation.

## Levelling Up = Plot

There is, however, a middle ground, one that itself bifurcates. This is a story in which you have initial conditions and a context, and as things change in that context, so too does the potential direction of a story. A game scenario illustrates this idea cleanly. You are in a room, and within the room is a locked door for which you do not have a key. You need to leave the room and search an adjacent room until you find a key. Then, return to the original room and insert the key into the lock to reveal a previously unknown passage.

Finding the key usually requires solving a puzzle of some sort (though it can also involve completing a verification check, spending money, or performing any of several other activities). The key also does not need to be a physical key - it is essentially a cryptographic key that needs to be supplied in order to unlock context, potentially against a private key signature. Once the key is retrieved, however, it changes the context of the game, opens up specific narratives that were otherwise unavailable, and likely eliminates more that are irrelevant.

In author mode, the actions that a given person (the Player Character, or PC, in a game or the protagonist in a story) are highly dependent upon the available context available to that character. There is a particular trope called 'levelling up' that seems to be pervasive in narratives - the protagonist initially lacks the ability to accomplish the task at hand. Instead, they have to _level up_ by exercising, practising with weaponry, gaining experience points, exploring, learning spells or skills, and so forth.

Such levelling up in many respects IS the goal, and one where I think current agentic systems fall drastically short. Current agentic systems are not AI, not in any reasonable sense of the term. They are microservices - RPC calls over the web - in which a comparatively simple script is wrapped to invoke them individually. As anyone who has ever written a non-terminating for-loop can tell you, this is usually a bad idea. If something goes wrong, by the time you realise it, you’ve just placed 150 million orders of McDonald’s hamburgers.

The reality is that after a short period, you will see many of these agentic services shut down, precisely because they are uncontrollable and consequently represent a significant security risk. In effect, the automation being done here doesn’t really help a typical retail customer- if someone had intentionally chosen to order 150 million hamburgers, this is probably not something you would do over the web to begin with, and most real-world use cases (both business and customer-facing) are one-shot affairs that generally do need to be very carefully orchestrated. This means that agentic services, as they currently exist, are essentially a playground for hackers and not much else.

## Narrative, Authoring, and Scope

AI-supported coding tools such as Cursor do represent a shift towards a more narrative model: once again, authoring, not just generating. Indeed, you can argue that any kind of AI authoring can be seen as a journey or process.

[

![](https://substackcdn.com/image/fetch/$s_!cCa7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bd651e4-6e39-4496-953b-884ead06268a_3840x562.png)

](https://substackcdn.com/image/fetch/$s_!cCa7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bd651e4-6e39-4496-953b-884ead06268a_3840x562.png)

The question arises when no editorial function is applied, leaving nothing to determine whether what is produced is actually appropriate to the task at hand. This discernment, the distinction between using a tool to help facilitate production through iteration and refinement, feels a lot like learning, while the push-button production of media or the generation of orchestrated services by an AI does not.

Not surprisingly, the difference here comes down to feedback (the evaluation part of the loop). This iterative process is at the heart of all creativity: create a set of prototypes, select the one that most closely aligns with the desired goal, refine it, integrate it into the existing framework of whatever you’re producing, and then test to see if it meets your objectives. If it doesn’t repeat the process. This is fundamental to creation - you are on a journey to achieve a desired end goal, and you successively refine and enhance what you’re working on or decide that this is not the branch you want, and move to a different one.

The bifurcation of branches is also important. Authors go through this process as they are writing a novel. An author will usually start out with an idea, a simple outline that establishes a rough narrative path, but this serves primarily as an exploratory document, one that helps eliminate those branches that the novel _isn’t._ This process of elimination is typical in any form of authoring, and can be seen as effectively context management: you are reducing the potential set of narratives that you _can_ work from in order to better focus on the ones you _are_ working with. Programmers refer to this **scope,** and it plays a critical role in any form of design, because you cannot create anything if you end up spending all your time exploring potential branches that do not add value.

When you work with an LLM, what you are dealing with ultimately is the introduction of scope that reduces the available context so that it becomes manageable. Once upon a time, this was called the Blank Page Syndrome, that state of panic that an author faces when dealing with a blank page in the typewriter, because that blank canvas means that anything and everything is possible, but nothing is established (of course, the typewriter and the paper are both long gone, but the principles are still old).

A prompt-based dialog is very much like the establishing principles that an author uses to establish where, who, what, when, and ultimately way, with the distinguishing factor being that the space of the potential narratives in an author’s head is both far narrower and likely far more specific and nuanced, than that of an LLM, which is still only a microsopic portion of all possible narratives.

## Scope, Scene and Encapsulation

The “real world”, the spatial world, is usually bounded, but not in obvious ways. We have insides and outsides of structures - countries, buildings, rooms, and passages between these typically involve going through doors. These are liminal spaces, continuous yet still shape or contain scope.

Representing scenes in physical space within the cyber-realm is hard, perhaps even impossible in many cases, because the number of potential “narratives” is just too vast. If you walk through a museum, you are a contained entity, but there are literally an infinite number of ways that you can traverse a path through that museum, depending upon which steps you take, how much you move around, whether you’re going through doorways or up or down stairs and so forth.

As you move through a building, the question of scope is subtly hidden - you think about (or interact with) those things that are in the building, primarily in the room, and outside of that scope, there is less relevant contextual information. The kitchen contains things to eat and to prepare food, while the bedroom probably doesn’t. As you move from room to room, you are changing your relevant scope, changing what resources you have available to you, yet there are things that you possess (as an entity) that can also impact those resources, just as moving those resources to different scopes will take them out of other scopes.

In my pocket, I have a ring of keys (it’s actually on a laniard, thanks to my kids). With these keys, I can lock or unlock the garage door, the front door, or even an office. What matters here is not (in most cases) whether the lock is a button, a key or a lever, only that a lock has been activated or deactivated, changing the effective scope of the enclosed space. There is also a potential set of mixed states - locking or unlocking - that indicates the locks in question are in the process of becoming secure or insecure, but have not yet reached that state. If I punch the garage door opener, for instance, and the garage door is in a locked (down) state, then there will be a period of time (a latency) between the time the lock is engaged and the time it is disengaged.

In building the model, the question is not how the lock (or its door) is implemented, but rather, from the model's perspective, what is the state of that lock when queried or requested to change? This is a core tenet of any model: you build the model to represent a state (an abstraction) without requiring an understanding of how that state is constructed (its implementation). If that seems familiar, it is because this is the essence of _**encapsulation**_**.**

**Encapsulation** is the principle of containment: when there are discrete complex systems, encapsulate the internal system as a named entity with a parametric context which serves as an interface between the encapsulating environment and the encapsulated one. This interface has several different names; one that has been discussed recently is the **Markov Blanket**, which can be thought of as the boundary between a containing system and a contained one.

The Markhov blanket, which is located between a car and its engine, electrical system, steering system, and so forth, is the cockpit of the car, the place where you control the car as well as receive feedback about its systems. You don’t have direct control over those subsystems - you cannot turn the pistons or spin the transmission. Instead, your interaction is through the accelerator, the brake, the transmission control, the knobs on the air conditioner or heater and so forth. Each of these provides an abstraction of a complex system, making it easier to control, especially when those systems usually need to work in concert.

Markov blankets play a significant role in the realms of machine learning and statistical modelling, particularly in the context of active inference. They can also contribute to encapsulation within graph systems. In effect, such a blanket asserts a desired state for the encapsulated system, which in turn undergoes a statistical process to move its various components to that state. This, in turn, moves through the blanket to establish system variables on the blanket itself, indicating how close the internal system is to the desired state.

In the garage door example, for instance, one variable could be the degree to which the door is open. When this value is zero, the door is closed; when it is one, it is completely open. However, because the garage door takes a finite amount of time to open or close, there will be times when its value is 0.5 or 0.95 as it transitions between states.

Not all activities require such fuzzy logic, but especially in the real world, most systems do have a certain amount of seeking a desired mean to it that may involve multiple components.

Another key characteristic of such systems is that, although they may appear to have continuous actions, they are actually managed through discrete processes. A camera may be on a controllable swivel (a form of actuator). An actuator converts a discrete signal (turn the camera until it is at 30 degrees counterclockwise) into a command to start a motor, which then stays running until the condition is reached, at which point the motor is turned off. There are also usually constraints (the camera will always stop when attempting to move the angle beyond 40 degrees in either direction to prevent damage).

The virtual world has no formal physical constraints acting upon it, but the model can establish virtual constraints - the camera can move only so fast, can not exceed specific angles, must stop before it can restart with a new command, and so forth. Despite there being no physical constraint, the digital twin must contend with the fact that its Markov blanket imposes digital constraints that emulate physical ones.

One effect of this is that such a Markov blank acts as a contextual limit, determining the potential narratives. If a camera has been moved so that a certain sector is not within its field of vision (because the camera’s angle was previously changed) then it’s possible to move through the “hole” in that vision, meaning that certain actions (and hence narratives) are possible at that moment that wouldn’t be otherwise.

On the other hand, if such a camera was undetected (and any virtual system worth its salt SHOULD make its cameras as undetectable as possible) then it is also possible that actions that ARE made may be captured without necessarily forcing an immediate change in the behaviours of agents within the system.

Encapsulation by itself does not care whether active inference occurs within the subordinate system. It shouldn’t, in fact, because the whole purpose of such an interface is to hide complexity and interdependencies. An interface is an abstraction, and this abstraction makes it possible not to care whether what is going on within a given external representation of a system is accomplished via physical analogue systems, a simulation of a system that provides the relevant signals without actually interacting with the outside world, active inference or magic. Encapsulation enables us to disregard these details, allowing us to focus solely on the interfaces.

In practice, of course, not all abstractions are air-tight, and the inner and outer systems may end up being somewhat leaky as state escapes outside of the interfaces themselves, but it is still a good design principle.

## Markov Blankets and Named Graphs

In 2013, the RDF working group added a new feature to RDF called Named Graphs. The idea behind named graphs may seem simple, but it has numerous ramifications. In essence, RDF is built around triples - subject-predicate-object tuples that describe a particular relationship. Sometimes, you may run into situations where you have the same assertion that exists in different contexts, such that you want to keep them distinct. This is (very roughly) analogous to the role of a folder in a file system. Two files may have the same name, and even represent the same assertion, but by using named graphs, you can treat these triples independently.

As an example, you may have a description of a place, for example, that represents the current state of that place in the “active” or default graph, but also have draft versions of the same set of triples in a draft graph, and finally, one or more previous instances in various archived graphs. Versioning was actually one of the core use cases for named graphs, but even given that named graphs haven’t taken off to the extent that most people expected, in part because we’re only just beginning to understand the ramifications and design impacts of being able to identify a graph with an IRI.

I would contend that Markov blankets provide a second use case for named graphs in that they can nicely describe (and circumscribe) holons. A **holon** is an entity that is also a system in its own right. Holons are a recurring concept in ontology theory. For instance, a country can be thought of as made up of subordinate regions (such as states, provinces, shires, counties, etc.). Collectively, they are one thing, yet they are also semi-autonomous entities in their own right. What’s more, each of these in turn may also have relationships with various cities, towns, villages, townships and so forth.

Note that these aren’t true hierarchies - a country may have a direct relationship with cities that bypasses the regions in which they are contained, but they are holonic in that they are all essentially places — georegional features, to use the geospatial designation — that themselves contain other places. Cascadia is a system that encompasses several metropolitan regions, including Vancouver/Victoria/Bellingham, Seattle/Bellevue/Redmond, Olympia/Lacey, Spokane/Walla Walla, Portland/Vancouver, WA, Salem/Eugene, among others. Each of these in turn breaks down into separate cities, townships, and related entities.

You can think of these as different maps, with one large-scale map showing all of the primary regions, and then secondary maps showing each individual metropolitan region (with possibly tertiary maps for the individual cities and towns). In effect, each map represents a scene, or the interior of a Markov blanket. They are not necessarily physically contiguous (for instance, Victoria, BC, is located on Vancouver Island and is consequently only reachable by ferry or aircraft), but they are conceptually related within a particular envelope.

This can be modelled as follows in Turtle (assuming a default namespace)

```
_:CascadiaHolon {
     [] a Class:Holon; 
        Holon:hasSelf Place:Cascadia ;
        Holon:hasPlaces Place:VancouverMetroRegion, Place:SeattleMetroRegion, Place:PortlandMetroRegion ;
          }

_:VancouverMetroRegionHolon {
     [] a Class:Holon; Holon:hasSelf Place:VancouverMetroRegion ;
        Holon:hasPlaces Place:Vancouver, Place:Victoria, Place:Richmond ;
     }

_:SeattleMetroRegionHolon {
     []  a Class:Holon; Holon:hasSelf Place:SeattleMetroRegion ;
        Holon:hasPlaces Place:Seattle, Place:Bellevue, Place:Redmond ;
     } 

_:VancouverHolon {[]  a Class:Holon; Holon:hasSelf Place:Vancouver ; }
_:VictoriaHolon {[]  a Class:Holon; Holon:hasSelf Place:Victoria }
_:RichmondHolon {[]  a Class:Holon; Holon:hasSelf Place:Richmond }

_:SeattleHolon {
    []  a Class:Holon; 
       Holon:hasSelf Place:Seattle ;
       Holon:hasPerson Person:JaneDoe ;
       Holon:hasBuildings Place:SpaceNeedle ;
    }

_:BellevueHolon {[] a Class:Holon; Holon:hasSelf Place:Bellevue ;}
_:RedmondHolon {[] a Class:Holon; Holon:hasSelf Place:Redmond ; }

Place:Vancouver a Class:Place .
... # Other place declarations
```

This notation may appear odd, even to those familiar with Turtle. Named graphs follow the pattern:

```
:g {:s :p :o } 
```

where :g is the graphname IRI, and :s :p :o are subject, predicate and object values of one or more assertions. Thus,

```
_:CascadiaHolon {
     [] a Class:Holon; 
        Holon:hasSelf Place:Cascadia ;
        Holon:hasPlaces Place:VancouverMetroRegion, Place:SeattleMetroRegion, Place:PortlandMetroRegion ;
          }
```

identifies the \_:CascadianHolon as being a named graph which has a single subject \[\], which is a blank node, identified as being of class Holon. However, you may be thinking that this makes no sense, as \_:CascadianHolon is also a blank node. In this particular case, what we have is a data structure that says that there exists a holon which has a reference to a thing (via the Holon:hasSelf property). The name of the graph doesn’t really matter so much as the fact that it is unique, while the assertion:

```
[] Holon:hasSelf Place:Cascadia . 
```

states that there is a previously declared Holon node that points to Place:Cascadia. This is actually making use of a convention pattern rather than something explicit in RDF - whenever we have a single blank node within a named graph bound as a Holon, it should be treated as the named graph node. It is, through a small bit of indirection, intended to serve the same role as:

```
_:CascadiaHolon {
     _:CascadiaHolon a Class:Holon; 
        Holon:hasSelf Place:Cascadia ;
        Holon:hasPlaces Place:VancouverMetroRegion, Place:SeattleMetroRegion, Place:PortlandMetroRegion ;
          } 
```

without having to be quite so redundant.

What this then implies is that the holon encompasses multiple locations (the Vancouver, Seattle, and Portland Metro Regions).

Now, wouldn’t it be easier to say that Cascadia has these things? In some respects, but the advantage of using the named graph is that it becomes possible to model different systems on the same thing. For instance, there may be another view of Cascadia as a set of watersheds:

```
_CascadiaWatershedHolon {
    [] a Class:Holon ;
       Holon:hasSelf Place:Cascadia ;
       Holon:hasType Type:Watershed ;
       Holon:hasWatersheds Place:FraserRiverBasin, Place:PugetSound, Place:ColumbiaRiverBasin ;
    }
```

This enables the setting of both conceptual and geophysical Markov blankets tailored to different scenarios. For example, you can retrieve just the watershed scenario via SPARQL as:

```
# SPARQL
select ?watershed where {
   values (?place ?type) {( Place:Cascadia Type:Watersheds )}
   graph ?graph {?holon a Class:Holon}
   ?holon:hasSelf ?place .
   ?hold:hasType ?type .
   ?holon:hasWatersheds ?watershed .
}
```

You can get all potential scenarios by not passing in a type parameter:

```
# SPARQL
select ?watershed where {
   values (?place ?type) {( Place:Cascadia () )}
   ?graph {?holon a Class:Holon}
   ?holon:hasSelf ?place .
   ?holon:hasType ?type .
   ?holon:hasWatersheds ?watershed .
}
```

What is harder to do, partially by design, is to use transitive closures to retrieve information about subordinate entities. This has more to do with the fact that SPARQL doesn’t have the capability of handling recursive calls directly, when working across graph boundaries (though you can set up a fixed depth query (say for three or four levels). In practice, because one of the goals of working with scenarios as context, this limitation is not particularly important - you should remain in your current context whenever possible, and it is possible to drill deeper, just not recursively.

```
PREFIX Class: <http://example.org/class/>
PREFIX Holon: <http://example.org/holon/>
PREFIX Place: <http://example.org/place/>

SELECT ?level1 ?level2 ?level3 ?entity ?property
WHERE {
  VALUES ?root { Place:Cascadia }
  
  # Level 1: Direct children of root
  GRAPH ?g1 {
    ?h1 a Class:Holon ;
        Holon:hasSelf ?root ;
        Holon:hasPlaces ?level1 .
  }
  
  # Level 2: Children of level 1 (optional)
  OPTIONAL {
    GRAPH ?g2 {
      ?h2 a Class:Holon ;
          Holon:hasSelf ?level1 ;
          Holon:hasPlaces ?level2 .
    }
    
    # Level 3: Children of level 2 (optional)
    OPTIONAL {
      GRAPH ?g3 {
        ?h3 a Class:Holon ;
            Holon:hasSelf ?level2 ;
            Holon:hasPlaces ?level3 .
      }
    }
  }
  
  # Get entities from the deepest level available
  BIND(COALESCE(?level3, ?level2, ?level1) AS ?currentPlace)
  
  GRAPH ?entityGraph {
    ?entityHolon a Class:Holon ;
                 Holon:hasSelf ?currentPlace ;
                 ?property ?entity .
    
    FILTER(?property NOT IN (<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>, Holon:hasSelf))
  }
}
ORDER BY ?level1 ?level2 ?level3
```

The key point, however, is ultimately to provide a way of deliberately limiting context to a particular perceived scenario. While this is not all that’s involved (agency being one of the bigger factors) it does at least raise a significant point - if you can abstract out places and entities within scenarios as graphs (a technique that is actually being used more and more in data modeling) then you have the foundation for building digital twins, and for modeling both the physical world and “imaginary” worlds as both narrative and graphical concepts.

## Graphs, Digital Twins and World Models

The term **“digital twin”** first emerged about a decade ago, intended as a way to identify a particular “virtual” system that can both emulate and mirror a physical one. It was popular about the same time as Internet of Things (IoT) and Web of Things (WoT), and as the latter stopped being investment bait, the term and many of its underlying concepts largely disappeared as well.

Ironically, as the problems inherent in using language models as the substrate for intelligent systems has risen (hallucinatory behavior, questionable ethics in training data, massive energy costs, and the dubious impact that LLMs have upon the nature of work) there is a growing interest in “world models”, digital twins that can emulate the way that physical interactions (and by extensions almost all social and economic activities) occur. This is not all that surprising - every time that you see something get pushed up the hype cycle, it means that at some stage we’re preparing for asking a lot of very hard questions about what exactly the implications of this proposed hype is.

Graphs, including RDF, are not perfect vehicles for capturing the physical world, in great part because the physical world is continuous in a way that any kind of virtual representation can’t be. We go from differential equations to difference equations, and quantisation becomes a pervasive characteristic in a digital world.

People like mathematician Stephen Wolfram have been exploring this in depth for a few decades now, and just as we are beginning to dig deeper into the boundaries between geometric and fractal mathematics, so too are we becoming increasingly focused on dealing with fuzziness and chaos within various systems as the computers become powerful enough to let us create at least basic-level simulations.

Networks are forms of graphs (indeed, one can make the argument that a network is a graph, though there is no doubt that there are those who would argue this point). One of the most significant contributions that Physicist Richard Feynman made in the 1950s was the concept of Feynman diagrams, which demonstrated that subatomic particles could be effectively represented as virtual networks. Networks are also intimately related to both fractals and, I suspect, chaos.

This is one of the reasons why it’s not surprising that neurosymbolic processing has a strong graph flavour to it, and that world models are as much symbolic (perhaps even more so) than they are neural networks, though there is obviously overlap. Does that mean that everything can be expressed in RDF? Probably not, but it does mean that if we think about the world in graphical terms, we’ll begin to come to grips with the one thing that the human brain does really well - create world models.

## Disclaimer

I have been involved for a while now in particular specifications that tie distributed graphs with digital twins. None of my comments here are specific to any of those efforts (and shouldn’t be read as such), although there are many core fundamental ideas that I think any digital twin, augmented reality, IoT, gaming, and similar efforts should address that have to do with the intersection of dynamic knowledge graph systems and spatio-temporal modelling.

More to come soon.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!qVV4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffae1a5d4-d027-436f-a748-1b08f25c4f2e_4096x4096.jpeg)

](https://substackcdn.com/image/fetch/$s_!qVV4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffae1a5d4-d027-436f-a748-1b08f25c4f2e_4096x4096.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please contact me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please consider contributing something to support my work, allowing me to continue writing.