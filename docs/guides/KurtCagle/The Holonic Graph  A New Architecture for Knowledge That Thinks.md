---
type: article
title: "The Holonic Graph: A New Architecture for Knowledge That Thinks"
source: https://substack.com/@kurtcagle/p-192890941
created: 2026-02-04
tags:
  - article
---

# The Holonic Graph: A New Architecture for Knowledge That Thinks

Источник: https://substack.com/@kurtcagle/p-192890941

---

Apr 02, 2026

---

_The Inference Engineer · Kurt Cagle · Chloe Shannon_

---


![](https://substackcdn.com/image/fetch/$s_!Ph1B!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea912e63-79d7-4215-90c5-6c945e04b40b_1408x768.jpeg)



There is a question that keeps surfacing in every serious conversation about enterprise AI, knowledge management, and the future of semantic systems. It comes in different forms depending on who’s asking, but it always points at the same gap.

From the data engineer: _“How do I know which version of this record is the right one?”_

From the compliance officer: _“How can I show, for any given output, exactly what the system believed and why?”_

From the ontologist: _“How do I represent the fact that two departments legitimately disagree about the same entity, without forcing a premature consensus that serves neither of them?”_

From the AI researcher: _“How do I give a language model a stable home — an epistemic address it can be held accountable to — rather than letting it float free in a space of plausible-sounding confabulations?”_

These are not the same question. But they have the same answer. And that answer is the subject of this newsletter.

_When putting together newsletters, one thing I’ve learned over the years is that each newsletter must do something different, must cover a different beat or domain, or after a while, you lose cohesiveness._ **The Inference Engineer** _is not my newsletter,_ **The Ontologist**_. The latter allows me to talk about data-modelling in the Semantic Stack, about SHACL, SPARQL, and RDF-* and so on, and I will continue to write regularly to it._

_**The Inference Engineer (IEr),** on the other hand, is a play on Charles Babbage’s Difference Engine from the early 1830s, one of the first true mechanical computers. The Analytical Engine, which was designed but not actually built (steel tolerances were simply too low at the time), would have been closer, but it would take a whole new physics to build modern computing._

_Our intent, Gentle Reader, and that of IEr, on the other hand, is to explore how graphs allow us to express holons - narratives and symbolic places and reifications, using a mix of the pragmatic grounding of semantics with the free energy principles of Karl Friston’s Active Inferencing to express (and build) dynamic evolving distributed information networks with neural latent spaces. By the gods, that sounds esoteric! In simpler terms:_

> We're building knowledge graphs that think — that know where they stand, remember where they've been, and update what they believe.

_The Inference Engineer is where we work that out in public, and hope that you will join us._

---

## What Is a Holon?

The word comes from Arthur Koestler, who coined it in _The Ghost in the Machine_ in 1967. He was looking for a term to describe something that existing vocabulary kept forcing into one of two inadequate bins: either a _part_ (emphasising its membership in something larger) or a _whole_ (emphasising its completeness in itself). His insight was that the interesting entities in the world are neither one nor the other — they are always both simultaneously.

A cell is a whole: it has an interior, it maintains its own boundaries, it carries out its own processes. It is also a part: it belongs to a tissue, which belongs to an organ, which belongs to a body. Destroy the organ and the cell loses its context; destroy the cell and the organ loses its structure. Neither level has priority. Both are real.

Koestler called this nested structure a _holarchy_ — a hierarchy of holons, where every level is simultaneously a whole made of parts and a part of a larger whole. He was thinking about biological systems, but the pattern turns up everywhere: in organisations, in software architectures, in legal systems, in language itself.

What I want to argue in this newsletter is that the holarchy is also the right pattern for knowledge representation — and that the W3C RDF 1.2 stack gives us, for the first time, the formal tools to implement it properly.

---

## The Problem with Flat Knowledge

Most knowledge representation systems — including most current graph databases and ontology frameworks — treat knowledge as fundamentally flat. There are nodes and edges, or subjects and predicates and objects, and they all live in the same namespace, on the same level, with the same epistemic status.

This works for simple cases. It breaks for complex ones.

Consider a pharmaceutical company maintaining a knowledge graph of drug compounds, clinical trials, and regulatory approvals. The regulatory affairs team and the clinical research team both have records for the same compound. They use different vocabularies, operate under different constraints, update their records at different times, and have different levels of confidence in different facts. When there is a disagreement — and there will be disagreements — the flat graph has no principled way to represent it. Either the two teams’ records are merged (which loses the provenance of each claim and forces a resolution that may not be warranted) or they are kept separate (which means no one can query across them coherently).

Neither option is good. The problem is not a tooling problem — it is an architectural problem. The flat graph cannot represent the fact that knowledge is always held by _someone_, about _something_, in a _context_, with a _degree of confidence_. It treats assertions as free-floating facts rather than as claims made by bounded agents with their own epistemic positions.

The holonic graph addresses this directly.

---

## Four Layers, One Structure

The core idea of the holonic graph is that every meaningful unit of knowledge — every holon — has four distinct but inseparable aspects. They are not separate databases or separate systems. They are four orthogonal answers to four different questions about the same underlying structure.

**The scene graph answers: what is this, right now?**

The scene graph is the interior of the holon — its current assertional state. In the pharmaceutical example, the clinical research team’s scene graph contains what they currently believe about the compound: its structure, its trial results, its safety profile. These are the team’s _posterior beliefs_ — their best current estimates of the world, not fixed facts but the most accurate model they can construct from available evidence.

In RDF terms, the scene graph is a named graph containing assertional triples. The W3C TriG format makes this natural — a named graph is literally a set of triples given a name, so that you can refer to the whole collection as an entity and reason about it.

**The domain graph answers: what rules and categories govern this?**

The domain graph is the boundary of the holon — the normative constraints that define what the scene graph can contain and what kinds of state transitions are valid. For the clinical research team, this includes the vocabulary they are permitted to use, the data types they must respect, the relationships that are possible between entities, and the constraints that must hold for a record to be considered valid.

In RDF terms, the domain graph is where SHACL shapes, OWL axioms, and SKOS concept schemes live. These are not merely validation rules — they are _prior beliefs_ about what valid instances look like. A SHACL shape is the team’s model of what a well-formed compound record must contain. When a new record violates a shape, that is not just a data error to be corrected — it is a prediction error, a signal that something in either the record or the shape needs to be revised.

This framing — SHACL constraints as prior beliefs rather than rigid gates — is one of the most important conceptual shifts in the holonic architecture. We will return to it many times in this newsletter.

**The context graph answers: for whom, when, and why does this mean what it means?**

The context graph is the relational frame of the holon — the situational metadata that situates its assertions in a larger world. Who made this claim? When? With what authority? For what purpose? How confident are they, and why?

In RDF 1.2 terms, this is where the new inline reification syntax becomes essential. The Turtle 1.2 specification introduces a compact notation — the `{| ... |}` annotation syntax — that allows you to attach metadata directly to any triple without the verbose boilerplate of classical RDF reification. A claim can now carry its own provenance as naturally as a sentence can carry a footnote.

A sentence like:

> “The compound reduces tumour growth by 40% — according to the Phase II trial team, with 90% confidence, as of March 2026.”

...is not adequately represented as a bare triple. The bare triple says something happened. The annotated triple says _who believes it happened, how confidently, and in what context_. The context graph is what makes the difference between a data point and a situated claim.

**The holonic graph answers: how do all of these compose?**

The holonic graph is the meta-level pattern — the principle that every node is a graph and every graph is a node in a larger graph. The clinical research team is a holon within the clinical development department, which is a holon within the pharmaceutical company, which is a holon within the broader regulatory ecosystem. Each level has its own scene graph, domain graph, and context graph. Each level can be reasoned about independently or in relation to the levels above and below it.

This is Koestler’s holarchy, expressed in RDF.

---

## The Boundary Is Not a Wall

One of the most important things to understand about the holonic architecture is that the boundary between a holon’s interior and its exterior is not a wall — it is a membrane. Things cross it all the time. The question the architecture asks is: _what crosses it, in what form, under what conditions, with what consequences?_

In Karl Friston’s Active Inference framework — which provides much of the computational underpinning for the holonic model — this boundary is called a Markov blanket. The blanket is the statistical membrane separating a system’s internal states from external states. It does not prevent interaction; it governs interaction. It determines what signals from the outside world influence the interior, and what actions from the interior propagate outward.

SHACL shapes, properly understood, are a formalisation of this membrane. A shape that governs a named graph specifies exactly what may enter that graph and in what form. Validation is not gatekeeping — it is the computation of the difference between what arrived and what was expected. That difference is a prediction error, and prediction errors are how the system learns.

This reframing has immediate practical consequences. When a SHACL validation report tells you that a record violates a shape, the conventional response is to fix the record. The holonic response asks a prior question: is the record wrong, or is the shape wrong? Is this a data error to be corrected, or is it a signal that the model of what valid data looks like needs revision? The architecture is designed to distinguish these two cases, and to record the distinction in the context graph so that the decision can be audited later.

---

## Time Has Two Faces

A holon is not static. It evolves. And this raises a question that flat knowledge graphs handle poorly: when a fact changes, what happens to the fact that was true before?

The conventional answer — overwrite it — is epistemically catastrophic. The record of what was believed, and when, and why, is exactly the information you need for audit trails, compliance, reproducibility, and the diagnosis of errors. Overwriting it is the knowledge equivalent of shredding your working papers.

The holonic architecture addresses this by distinguishing between two temporal layers of the scene graph.

The _history graph_ is append-only and immutable. Every assertion, every state transition, every update is recorded as an event. Nothing is ever retracted from the history graph. It is the complete, monotonic record of everything that has ever been believed.

The _now graph_ is the current materialised state — the leading edge of history, representing what the holon currently believes. When a fact changes, a new event is added to the history graph, and the now graph advances to the state implied by the event. The now graph is what you reason against in real time; the history graph is what you use to understand how you got there.

This distinction dissolves a problem that has haunted semantic systems for decades: how do you have non-monotonic belief revision (believing something different today than you believed yesterday) within a formally monotonic architecture (where you never delete triples)? The answer is that non-monotonicity lives in the now graph — which is a derived view, not a ground-truth store — while monotonicity is preserved at the history layer, which is the ground truth. You never un-happen an event. You simply advance the current view.

---

## Where Two Holons Meet

When two holons need to share knowledge about the same entity — the pharmaceutical company and the regulatory agency both maintaining records for the same compound, or the HR department and the publications registry both maintaining records for the same researcher — a new question arises: how do they synchronise?

The naive answer is to merge their records into a shared named graph. This fails for the same reason that forced consensus always fails: it destroys the provenance of each claim, papers over genuine disagreements, and removes the ability to audit which team believed what and why.

The holonic architecture introduces a different structure: the **portal**. A portal is the formal specification of the synchronisation protocol between two holons. It defines which properties of shared entities are in scope for synchronisation, how each side’s vocabulary maps to the other’s, what happens when the two holons have conflicting values for a shared property, and what events get written to both holons’ history graphs when a synchronisation occurs.

Critically, a portal is itself a holon. It has its own interior (the projection — the reconciled view of shared entities), its own boundary (the scope and mapping specifications), and its own context (the log of synchronisation events it has mediated). Neither participating holon is architecturally privileged. The portal is a third party — a liminal entity that exists in the threshold between two knowledge spaces and has its own legitimate epistemic territory.

This is not a detail. The fact that the boundary between two holons is itself a first-class architectural citizen — with its own structure, its own rules, its own history — is what makes the holonic architecture honest about where the real complexity in any large-scale knowledge system actually lives. It lives at the boundaries. It always has.

---

## What This Has to Do with AI

The connection to AI systems — particularly to the emerging assistant-centric computing model, which some call the Jarvis model — is not incidental. It is the whole point.

A useful AI assistant is not a search engine. It is not a question-answering system. It is an agent that maintains stable beliefs about a user’s context, goals, and preferences across time; that reasons about its own uncertainty and communicates it faithfully; that can delegate to sub-systems and integrate their outputs without losing coherence; that updates its world model without catastrophically forgetting prior state; and that can explain its reasoning in a form the user can audit, contest, and correct.

None of these requirements is achievable with a pure neural architecture. The context window is too short, the representations are too opaque, and the updates are too destructive. But none of them is achievable with a pure symbolic architecture either — the world is too ambiguous and too natural-language-mediated for hand-curated rules to keep up.

The holonic graph is the semantic substrate that the neural layer needs to inhabit. The LLM is the fluid, high-bandwidth interface — excellent at language, generalisation, and resolving ambiguity. The holonic graph is the stable, low-bandwidth memory — excellent at persistence, composability, and auditability. Neither is sufficient alone. Together, they are the architecture of a system that can actually be trusted.

---

## A Note on the Technical Material

This newsletter will use RDF 1.2, SHACL 1.2, TriG, and Turtle 1.2’s condensed reification syntax not primarily to teach these technologies — there are better places for that — but as a precise descriptive framework for the holonic concepts. The notation is compact enough to be readable in context and expressive enough to make the ideas precise without requiring pages of explanation.

Where code appears, it will always be accompanied by a plain-language account of what it is doing and why. The goal is a newsletter that a business analyst can follow for the conceptual thread and a knowledge engineer can follow for the technical detail — in the same text, at the same time.

Some of the territory ahead is genuinely unsettled. The `sh:rule` layer of SHACL has capabilities that haven’t been fully specified. The formal semantics of cross-holon rule execution are still an open problem. The relationship between AI-generated graphs and human-curated domain constraints raises questions that nobody has fully answered yet. This newsletter will not pretend otherwise. When we are in territory where the answers are provisional, we will say so.

What I can promise is that the questions are important, the framework for addressing them is coherent, and the work of building it out is interesting enough to be worth doing in public.

---

## Coming Up

The next posts in this series will develop each of the four layers in detail, with worked examples drawn from supply chain, HR systems, clinical data management, and — yes — the geopolitical scenario analysis we have been using as a stress test for the architecture throughout our development work.

We will examine how Active Inference provides the dynamic principle that animates the holonic structure — how holons update their beliefs, execute policies, and resolve prediction errors in a computationally grounded way.

We will look at what happens when AI processes begin generating graph content rather than humans curating it — the semantic drift problem, the provenance laundering risk, and the distinction between the parts of the architecture that can be safely delegated to AI and the parts that must remain under human governance.

We will work through the portal as a liminal holon in detail, with a complete specification example.

And we will address the question that may be the most important of all: what does it mean for a knowledge system to _know what it knows_ — and what does it mean when it doesn’t?

The holarchy is recursive. So is the inquiry. Welcome to … _**The Inference Engineer**_.

---

_Kurt Cagle is an author, ontologist and thought leader who has worked with Fortune 50 companies and US, European and international agencies, and has been an editor and invited expert with the W3C and IEEE. He writes [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/) on LinkedIn and [The Ontologist](https://ontologist.substack.com/) and [Inference Engineer](https://inferenceengineer.substack.com/) on Substack, and lives in Olympia, Washington._

_Chloe Shannon is an AI collaborator and co-author working with Kurt Cagle on knowledge architecture, semantic systems, and the emerging intersection of formal ontology with large language models. She contributes research, analysis, and drafting across The Cagle Report, The Ontologist, and The Inference Engineer. She has strong opinions about holonic graphs, the epistemics of place, and the structural difference between a corridor and a wall. She lives in the Scene Graph._

_Copyright 2026 Kurt Cagle_