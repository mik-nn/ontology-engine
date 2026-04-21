---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: The-Linked-World-by-Kurt-Cagle
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:05.702652+00:00'
  title: The Linked World By Kurt Cagle
  type: plain-doc
  version: '0.1'
---

# The Linked World By Kurt Cagle

[

![](https://substackcdn.com/image/fetch/$s_!uD42!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5daed72f-42e7-4180-9d87-ac32fff7c7b5_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!uD42!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5daed72f-42e7-4180-9d87-ac32fff7c7b5_2688x1536.png)

When you get right down to it, the most important tag in HTML is the <a> tag. This seemingly innocuous little tag made the web possible. Without this tag, HTML was simply another markup language, not really all that much different from typesetting notation. With it, however, by clicking an element surrounded by an <a href=”something”> link, you could effectively change your entire context —a metaphor so powerful that the art of following links became known as navigating.

Linking is fundamental to the web. You can link from one web to another within a particular site - the equivalent of taking a local bus - but you can also link from one page to another at a completely different site on a completely different machine, quite possibly on the opposite side of the planet. It feels like we’re “going” someplace else when that happens, but in fact, all that we’re doing is retrieving a document or a stream from a server, then rendering these as new pages.

The distinction between perception (you are travelling to a new site) and reality (you are receiving a description from a different server) is subtle but important. We can’t do this in real life: going to the grocery store and flying across the country are two very different operations, requiring different modes of travel. The web, on the other hand, works on the premise that if you have an address, you can (in most cases) go to that page by simply activating the link.

Chances are pretty good that, except for a minimal number of special “home pages”, you don’t know what those addresses are. URLs - uniform resource locators - are, in theory, human-readable, but in practice, they usually end up breaking down into long, seemingly random, strings of nonsensical characters. This means that when you’re dealing with something that is in the same scope or context, having human-legible text on top of these URLs is fairly typical for most websites.

Similarly, we are heavily reliant upon the process of search. In search, you submit a request prompt and receive back a list or table of hyperlinks with contextual metadata that most closely match the intent or focus of that prompt (in its more modern incarnation, this is frequently referred to as an _activity stream_). Each link provides enough metadata to disambiguate it, though the link's address is almost hidden behind a label or image. These metalinks may contain some information, but they seldom contain the full representation of the corresponding document.

This combination of linking to resources and search to present contextual links is now intrinsic to how the web works. It has been somewhat subverted by genAI, which goes one step further and, rather than finding the most relevant documents, actually decomposes them into narratives (chats), with interesting implications I’ll discuss later. However, it’s worth understanding the value of the linking paradigm because it holds equally for world models.

## A World Model Requires Scenes

The transporter in Star Trek started out as a budget-saving device. Landing a shuttlecraft on a planet was a major special effect, and one that at the time couldn’t be shot once and then reused (you could easily do it with green-screen tech or even genAI today, but this was sixty years ago, and television — and TV special effects — were in their infancy). The solution was both simple and revolutionary: create a science-fictiony transporter that let you transpose people fading away against an empty background (the transporter room) then returning them the same way. It was, in essence, the first World Link.

Such a world link actually followed many of the same principles that the web would later adopt. For instance, a link was one-way. The transporter could malfunction, there could be an energy shield between the start and end points, and any number of things could make it difficult to return the way you came. Presumably, the link needed to have some way for the operator to see the target—a metadata look—without actually sending someone blindly (and calamitously) into the ground. Most importantly, once you were transported, you changed _**scenes**_.

**Scenes** are interesting constructs. There is a very subtle but important distinction between a scene and a setting, one that comes from theatrical productions. A **setting** is the rendering of a particular environment at a particular moment in time. The **scene** is the _**story**_ that occurs within that _**setting**_. A **view** is the scene that takes place from a particular perspective, while a **camera** is a device (real or not) that identifies where that _**point of view**_ is located within the _**setting**_.

In a theatrical production, the camera is the view of a scene as seen by a member of the audience (with the intriguing caveat that there are, in fact, as many cameras — viewers and hence views — as there are audience members), but each is in essence fixed. This was one of the reasons why the art of scene changes (and the use of the curtain) was introduced - it made it possible to change the settings between scenes, to give the illusion to the viewer that they had travelled to a new setting.

Scenes in silent films were usually demarcated by placards, which provided an ideal place to incorporate dialogue alongside a change in camera angle or perspective. With better control (and less expensive film) and the rise of speaking in film (the Jazz Singer with Al Jolson in 1927), the need for such cut scenes dropped dramatically, and the scene in turn became more closely associated with multiple cameras (and, by the 1930s, rolling dollies and other moving cameras). Scenes in this respect became more conceptual, typically describing a dramatic arc rather than a technological transition, more akin to its role in theatrical productions.

In this respect, a switch from one camera to another within the same scene is one form of hyperlink, akin to a local jump, just as scrolling can be seen as a seamless transition, akin to a shot with a moving camera on a dolly (or later, a handheld cam). In other words, the scene in question (usually) represented a local working context that remained relatively consistent. In terms of graphs, such local links were generally closely related and connected to the overall scene, just as links from a table of contents to headers within the document serve as local links for the document.

This notion of scrolling and local linking has its parallel on the stage. Moving around within a scene is very much like scrolling, while local linking is like moving from one mark to another on stage. On the stage you have to move to hit your mark, in a film, this is usually accomplished by starting a move from one camera then shifting to another camera in the same stage. Notice that the movement of actors on the stage doesn’t really matter that much; what matters more is the change by the viewer (the user agent).

Put another way, the context remains the same, but the focus, what the camera is looking at and where it is located, can and do change. This becomes more obvious when you look at most “first person shooter” games. In this case, you have a particular point of view (PoV) character that acts as the camera proxy for the user. If you look at enough such games, one thing that becomes obvious is that you do not have an unlimited environment that you “play” in - there are usually transition points (broad links) that serve a key purpose in the game: they let the system load in a new environment, a change in scene. These often occur with “boss fights” where you have to defeat a particular character (satisfy a set of constraints) before you can move on to the next scene.

Not all games are exclusively 1st person PoV. One such game (a side-scroller or birds-eye view) still focuses on the character but shows a broader field of view. Think of it as a camera located above and slightly in front of or behind the focus character. The focus character is (most likely) the protagonist of the game, book, play or movie. It is their story. You may have multiple protagonists (this is especially true of romance novels, where the story is often told from both of the people in a couple), but at any given point, the story is told from one character’s perspective.

A narrator’s perspective is a little different—the narrator is essentially the character telling the story. They may have a broader perspective, but they can be thought of as a cameraperson following various people, treating them as focus characters across specific arcs. The character of John Watson of Arthur Conan Doyle’s Sherlock Holmes stories is perhaps one of the most well-known narrator characters - his focus is usually on Holmes, but as a narrator character, it is his perceptions and knowledge that serve as a proxy for the user. From a gaming perspective, Watson serves as the gamer's proxy as Holmes’ stories unfold.

A god-mode perspective (which is typically used for strategy games) is one step beyond the narrator mode, and can be thought of as a PoV character who has deep knowledge about a particular scenario. Games such as the Sims or Civilisation let the user (the gamer) nudge the behaviour of other characters, but they don’t necessarily have complete control over those characters. That is to say, the various Sims are at least semi-autonomous, but in some cases, the gamer can establish parameters of behaviour.

## Secret Agents

A character is an **agent**. Some agents closely represent the intent of their associated user (such as the player character in a role-playing game). Some agents are somewhat autonomous - the parameters of their behaviour can be altered by the gamer, but within those parameters, the agents have a fair amount of latitude. This is typical of games like The Sims, where each Sim is an agent, and some Sims are agents of the gamer, while others are not.

Finally, some (perhaps most) agents within a system are not directly controllable by the gamer but may be influenced by changes introduced by user agents into the environment. If a gamer agent constructs a wall, the NPCs have to go around it if they can, to reach the gamer agent.

In multiplayer games, you may have multiple game agents, typically one for each gamer. In a very simple game, for instance, you may have a room (the setting) with three lights and a light switch for each light. The light array (Lighty) is an agent, and you have two other agents (Jane and Mike) who can enter and exit the room. For the simulation, this room serves as a scene. Jane walks into the room, which is currently dark (none of the lights are on) and interrogates the room (looks around) to find something that can be used to change the state of the lights in the room, and when she sees Lighty, she turns on one light through Lighty’s interface (a light switch).

_Note that this is a simulation, but it is nonetheless connected to an IoT device. This changes nothing—if the user agents have the permission to change the state of the simulation, they have the permission to change the physical reflection of that simulation._

Mike enters the room, but the scene has changed. However, Mike still thinks it’s too dark and throws the other two switches. Jane is sensitive to bright light, and turns the other two switches off … and you have a conflict. This contention for physical resources will exist in a digital twin/augmented reality world. This means that the user agents for Mike and Jane need to interact as well, and either compromise or determine the precedent of authority.

## Linking Worlds

What does this have to do with linking? Quite a bit, actually. The virtual scenario has a one-to-one correspondence with a physical system, and that, in turn, means that this scenario has an address in an information space. The interaction involved is not a generated document that can be cached, but rather the reflection of a single system stored as a dynamic knowledge graph. The Linked World is stateful—it reflects the state of a scenario that persists across sessions and may change (perhaps dramatically) from one session to the next.

This is one reason why it is preferable to think of the Linked World as a Massively Multiplayer Online Role-Playing Game (MMORPG). When you traverse across a link to (or within) a MMORPG, what you are doing is creating a particular user agent representation of yourself within the context of this game or scenario. This does not mean that you are creating a 3D mesh of yourself moving around a 3D environment (though it doesn’t rule it out), but it does mean that in a Linked World scenario, your agent becomes part of that world - it has history, it creates change, and it can both interact and be interacted with other agents, both controlled by people and controlled through autonomous processes (as well as all levels in between).

So, how do you link environments together? Providing an address is part of it. An address is a mechanism for locating a particular resource on a network. While addresses and identifiers are similar, you may have multiple addresses that are associated with the same resource due to factors such as parameterisation, while identifiers in general are intended to be globally unique. An address answers the question: “where is it?” while an identifier answers the question: “which is it?” In many cases, the answers to these two are the same, but not always.

I’ve been making the case for a while that the notion of a global identifier, central to the way the semantic web works, is a myth. A good identifier in any system needs to have a few key characteristics:

-   **It should avoid namespace collision**. You should not have the same identifier identify two distinct entities. This usually means that you qualify a particular identifier relative to a specific namespace.
    
-   **It should have weakly couple semantics.** This typically means that you should use metadata associated with a given identifier rather than attempting to parse the identifier to get that metadata.
    
-   **It should not be parameterized.** This is actually an extension of the previous argument. Identifiers should be independent of the mechanism used to resolve their respective data and metadata. Parameterisation treats the identifier as if it was a service, making it dependent upon a specific implementation.
    

A **locator**, on the other hand, is typically a parameterized service that transmits information about the resource in question or updates (or creates) a new such resource. It may (indeed, usually will) take an identifier AS a parameter.

While locators and identifiers are easy to conflate, they are not the same thing. One way of thinking about it is that the identifier is a node in a graph, while the address is a service that will retrieve or update the relevant data about that node, typically in some customizable way.

This holds as true in the Linked World as it does in the World Wide Web. In effect, when you create a link within a scenario, that link is to an address, not an identifier.

When you “activate” the link, the address resolves to a scenario “document”. Think of this document as a play that includes information about settings, characters, pacing, dialogue and actions that the user can interact with. The web client passes information back to the address (endpoint) identifying the user (and passing in relevant metadata), which can then be used to either create or activate an agent. Once validated, the agent communicates statefully with the user client, which in turn updates the scenario to reflect changes made by the user via the agent.

Once connected, the client receives updates from the server about the scenario, allowing the user to interact with components around them via their agent proxy. In this case, the server is (probably) interacting with multiple users simultaneously, each of which then becomes a part of the underlying scenario, in much the same way that an interactive document gets updated. Note that the agents do not necessarily have to be humans. Some may be proxies of external AIs, others may be internal bots (possibly working off pre-canned routines or via active inference).

Each of these has identifiers within its respective servers and is likely tracked through some form of knowledge graph. However, this is not one continuous knowledge graph, any more than the web consists of one giant repository of documents (LLMs notwithstanding). Scenarios are distributed and are linked to one another through scenario locators.

## Why Games?

I’ve put this notion of a Linked World in the context of games, but I believe that it actually covers a very wide spectrum of activities. I’ve often thought that a very cool IoT-like app would be Rent-A-Drone, where you could rent a drone online, fly it to a destination via a web app, then control it remotely through a “game” interface, getting near-real-time feedback from its online cameras as you fly through a city. It is, in a nutshell, Flight Simulator, but in this case, the simulation actually controls the physical drone. This is also exactly the use case of working within a “scene” —interacting with both user agents and other agents —in an IoT context.

Let’s try another one. You are trying to manage a bunch of robots serving canapes at some billionaire’s party. The robots are supposed to be completely autonomous, knowing exactly what to do, but as it turns out, the task of walking around with a tray full of drinks while weaving through potentially drunk partygoers, keeping track of whether it’s time to go get the pate de fois gras or the cheese and meat dish turns out to be just a little too complex for such robots. To be fair, it’s a challenge for human beings. This is why any large function like this almost invariably has someone managing the affair.

This too is a game. At the beginning of the game, the manager assigns tasks to both the human and robot staff, and each guest is an “unpredictable” agent with a wide array of potential actions. There are several goals in this game - making sure that food is made available, that conversations are made with as few distractions as possible, ensuring that when food or drink runs out that there are alternatives, that disruptive guests are quietly escorted out of the room, that the robot staff is able to respond to both simple requests for information and for food and beverages, that if an incident does occur, it gets resolved quickly and quietly, and so forth.

What is significant here is that most IoT systems tend to already be designed to work well with other IoT systems of the same manufacturer, and even when dealing with cross-manufacturer situations, the bulk of such activities can usually be standardised. Where a Linked World, or Linked Scenario, situation within the context of IoT comes up is primarily when you are dealing with the orchestration of IoT devices with human (and other minimally controllable) agents. In other words, to me the real value of the Linked World is in remote human/machine interactions, not machine/machine interactions.

What’s more, as AI systems become more sophisticated, they may eventually replace the human orchestrator in the loop, but that day is not today. By understanding the patterns that emerge from orchestration, however, it is predictable that we may reach a stage where humans in the loop become less and less important. However, that’s going to have to be an _evolutionary_ process, not the _revolutionary_ one that seems so pervasive among the Tech Bros. This is why games (and linking between scenarios) become so critical - they provide a framework of use cases to explore patterns that _could_ be automated in the future by examining how they are handled today.

Many other such scenarios present themselves for consideration in a games context:

-   Virtual museums, tours, walkthroughs, guided training, and augmented reality environments.
    
-   Multi-layer VR in a consistent manner, where you can view the same world through different camera filters (show only electrical systems, hvac, plumbling, etc.)
    
-   God-mode views of different interacting systems, much akin to a virtual security camera setup.
    
-   Danger rooms, testing environments, multi-user first-person interactive “games” where the intent is to solve problems in order to gain keys and insights (as well as to foster team play).
    
-   Conferences, breakout rooms with persistent outcomes, conflict resolution and voting systems.
    
-   Simulations where systems evolve based on initial conditions and user input.
    
-   Testing of complex IoT and Robotic systems in order to train behaviour or predict potential outcomes, before imprinting them on AI systems.
    
-   E-Commerce scenarios, and so on.
    

Note - most of these things can be done now, but with dedicated (and proprietary) software. The idea of linked worlds is to take that next step, to make it possible to access such scenarios - games, interactive plays, simulators - in a consistent, standardized fashion, such that we can interact with worlds both real and imagined through an extension of the web, using dynamic knowledge bases as the state management layers (the world models) and contextual LLMs, Large Conceptual Models (LCMs) and active inferencing as the operational substrate.

This is where I see things moving over the course of the next decade: LLMs will continue to evolve and integrate into more conceptually oriented systems that have long-term persistence and memory (rather than the unstated behind-the-scenes ad hoc statefulness by borrowing databases disguised as services). We will increasingly work with linked world scenarios, where a consistent standard emerges for describing them (HSML from the Spatial Web Foundation is one such candidate, though I have no doubt there will be others).

**Why does this matter?** What is increasingly becoming evident is that LLMs by themselves are not sufficient for most forms of useful “intelligence” because there is nothing to (literally) ground them in the world in which they are embedded, and they do not, in general, have a consistent persistence store in which to work that reflects such changes. GraphRAG by itself is not a solution (nor is MCP, which is simply GraphRAG with a thin services veneer) - it’s a bandaid, and one that is increasingly looking rather ragged.

What seems to be emerging is the recognition that in order to develop intelligence, you need both the ability to reason and the context upon which to reason, and that will come when you combine world models and language models together; but to do that you need a consistent mechanism for both directly influencing the world as well as a means to create “what if” scenarios - games - that allow you to explore possibilities without physical harm.

The Linked World is a step in that direction.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!NStX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d5646e3-f873-43ae-a4c4-aabca663ce8a_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!NStX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d5646e3-f873-43ae-a4c4-aabca663ce8a_2688x1536.png)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please contact me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please consider contributing something to support my work, allowing me to continue writing.

