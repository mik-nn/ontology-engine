---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Dungeons-Declarations-What-a-Five-Room-Game-Reveals-About-Holonic-Graph-Architecture
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:05.137242+00:00'
  title: Dungeons & declarations what a five Room game reveals about holonic graph
    architecture
  type: plain-doc
  version: '0.1'
---

# Dungeons & declarations what a five Room game reveals about holonic graph architecture

```
┌─ TURN 3 — dungeon:room1_domain ─────────────────────────────────┐
│  RETRACT dungeon:RingOfVitality dungeon:locatedIn dungeon:Room1  │
│  ASSERT  dungeon:RingOfVitality dungeon:carriedBy dungeon:Elara  │
│  EQUIP   dungeon:RingOfVitality dungeon:energyEffect +10         │
│            → dungeon:Elara dungeon:energy 95 → 105               │
└──────────────────────────────────────────────────────────────────┘
```

**DM:** Better than when you came in. The north passage glows. The east passage does not.

**Elara:** North.

---

```
┌─ TURN 4 — dungeon:room1_context ────────────────────────────────┐
│  PORTAL  dungeon:Portal_R1_R2 a dungeon:FreePortal → PASS       │
│                                                                  │
│  RETRACT dungeon:Elara dungeon:currentRoom dungeon:Room1         │
│  ASSERT  dungeon:Elara dungeon:currentRoom dungeon:Room2         │
└──────────────────────────────────────────────────────────────────┘
```

> **Active holon:** `dungeon:Room2` — _The Crystal Corridor_

---

**DM:** The Crystal Corridor does what the name suggests. Light comes apart in here — becomes colour, becomes geometry, becomes something that doesn’t quite have a word yet. It is beautiful in the way that things are beautiful when they are also trying to kill you. A wraith drifts between the shards. It is made of roughly the same substance as the light: refracted, translucent, and deeply inconvenient. On the floor, a dark ring pulses in a rhythm that disagrees with your heartbeat. At the far end: a heavy iron door. Keyhole shaped like a crow in flight.

**Elara:** I recognise that keyhole shape. How bad is the wraith?

**DM:** Eight energy. It won’t be elegant.

**Elara:** It never is. I go in.

---

```
┌─ TURN 5 — dungeon:room2_domain ─────────────────────────────────┐
│  RULE    Rule_WraithBlocksLockedPortal → TRIGGERED               │
│  RULE    Rule_LockedPortalRequiresKey → PENDING (wraith first)   │
│  COST    dungeon:Wraith dungeon:strength 8 → -8 energy           │
│                                                                  │
│  RETRACT dungeon:Wraith dungeon:isDefeated false                 │
│  ASSERT  dungeon:Wraith dungeon:isDefeated true                  │
│            ~ dungeon:WraithState {| session:recordedAtTurn 5 |}  │
│  UPDATE  dungeon:Elara dungeon:energy 105 → 97                   │
└──────────────────────────────────────────────────────────────────┘
```

**DM:** It disperses like light does when the source is removed. There is no body. There is just the sudden absence of a thing that was there. Two domain rules now require your attention before the door will open.

**Elara:** I have the key. The wraith is down. What else does the door want?

**DM:** Nothing else. Both conditions are satisfied. The crow keyhole waits.

**Elara:** _(turns the key)_

---

```
┌─ TURN 6 — dungeon:room2_domain + dungeon:room2_context ─────────┐
│  RULE    Rule_WraithBlocksLockedPortal → PASS                    │
│  RULE    Rule_LockedPortalRequiresKey → PASS                     │
│                                                                  │
│  RETRACT dungeon:Elara dungeon:currentRoom dungeon:Room2         │
│  ASSERT  dungeon:Elara dungeon:currentRoom dungeon:Room3         │
└──────────────────────────────────────────────────────────────────┘
```

> **Active holon:** `dungeon:Room3` — _The Vault of Echoes_

---

**DM:** The door opens into a space that is almost embarrassingly large. Your footstep returns to you three times before silence settles. At its centre — still, expressionless, arms slightly spread — stands an Iron Golem. Ancient. Heavy. On a stone dais at its feet: a ring of hammered gold that hums in a frequency you feel behind your eyes.

**Elara:** That ring. That’s what opens the chest.

**DM:** _(silence)_

**Elara:** Is that silence a yes?

**DM:** The Golem has heard you say that. Its head has moved.

**Elara:** Twelve energy?

**DM:** Twelve energy.

**Elara:** _(exhales)_ Right.

---

```
┌─ TURN 7 — dungeon:room3_domain ─────────────────────────────────┐
│  RULE    Rule_GolemGuardsRing → TRIGGERED                        │
│  COST    dungeon:Golem dungeon:strength 12 → -12 energy          │
│                                                                  │
│  RETRACT dungeon:Golem dungeon:isDefeated false                  │
│  ASSERT  dungeon:Golem dungeon:isDefeated true                   │
│            ~ dungeon:GolemState {| session:recordedAtTurn 7 |}   │
│  UPDATE  dungeon:Elara dungeon:energy 97 → 85                    │
└──────────────────────────────────────────────────────────────────┘
```

**DM:** It goes down like a building collapses — slowly, then completely. In the echoes that follow, you hear it fall approximately four times. The dais is yours.

**Elara:** _(picks up the Ring of Power)_

**DM:** The moment it is on your finger, you understand. It isn’t just energy — it’s clarity. The ring doesn’t pulse like the other one did. It simply _is_. The gilded archway at the vault’s far end glows with the same character as the metal on your hand.

**Elara:** I could get used to this.

**DM:** You won’t have long. That archway goes one way.

---

```
┌─ TURN 8 — dungeon:room3_domain ─────────────────────────────────┐
│  RULE    Rule_GolemGuardsRing → PASS                             │
│  RULE    Rule_RingOfPowerIsTheKey → NOTE: requiresRing satisfied │
│                                                                  │
│  RETRACT dungeon:RingOfPower dungeon:locatedIn dungeon:Room3     │
│  ASSERT  dungeon:RingOfPower dungeon:carriedBy dungeon:Elara     │
│  EQUIP   dungeon:RingOfPower dungeon:energyEffect +15            │
│            → dungeon:Elara dungeon:energy 85 → 100               │
└──────────────────────────────────────────────────────────────────┘
```

**Elara:** One way. Fine. I walk through.

---

```
┌─ TURN 9 — dungeon:room3_context ────────────────────────────────┐
│  PORTAL  dungeon:Portal_R3_R5 → FreePortal, isBidirectional     │
│            false — portal seals on traversal                     │
│                                                                  │
│  RETRACT dungeon:Elara dungeon:currentRoom dungeon:Room3         │
│  ASSERT  dungeon:Elara dungeon:currentRoom dungeon:Room5         │
└──────────────────────────────────────────────────────────────────┘
```

> **Active holon:** `dungeon:Room5` — _The Treasury_

---

**DM:** There is no door behind you. There was a door; now there isn’t. You are in the Treasury. Gold stacked in arrangements that suggest someone had a great deal of time and a very particular aesthetic. At the exact centre: a chest. Grand. Its lock glows the same hammered gold as the ring on your finger. There are no exits.

**Elara:** There don’t need to be. I raise the ring toward the lock.

**DM:** The lock recognises what it is looking at.

---

```
┌─ TURN 10 — dungeon:room5_domain ────────────────────────────────┐
│  RULE    Rule_ChestRequiresRing → PASS                           │
│  RULE    Rule_VictoryCondition → TRIGGERED — cascade begins      │
│                                                                  │
│  RETRACT dungeon:TreasureChest dungeon:isOpen false              │
│  ASSERT  dungeon:TreasureChest dungeon:isOpen true               │
│  ASSERT  dungeon:Room5 dungeon:isTerminal true                   │
│  ASSERT  dungeon:DungeonWorld dungeon:isTerminal true            │
│  RETRACT dungeon:Session_001 session:isComplete false            │
│  ASSERT  dungeon:Session_001 session:isComplete true             │
└──────────────────────────────────────────────────────────────────┘
```

**DM:** Light blazes. Pulses once. The chest opens. Three graphs close simultaneously. The dungeon has nothing left to say.

**Elara:** _(looking into the chest)_ You know, I almost went east.

**DM:** Through the Shadow Chamber.

**Elara:** I would have reached this room. Without the ring.

**DM:** Yes.

**Elara:** And then?

**DM:** And then the domain rules would have evaluated. And found you wanting. And there would have been no exits, and no ring, and no chest, and a very long time to think about the choice you made in the Entry Hall.

**Elara:** _(considers the gold)_ The key was always the key.

**DM:** The key was always the key.

---

> **Session complete** · `dungeon:Session_001 session:isComplete true`  
> Final energy: **100** · Turns: **10** · Monsters defeated: **4**

---

## Part Four: From TriG to Table — How Turn 1 Works

_The winning path is clean, but it raises an obvious question: how does the TriG actually translate into those events and graph operations? Let us trace Turn 1 in full, from the initial graph state through to the post-mutation world._

### The engine’s first question: where are we?

Before anything happens, the engine issues two queries. First, to the session graph:

```
SELECT ?room ?turnCount WHERE {
  GRAPH dungeon:session_graph {
    dungeon:Session_001 session:activeHolon ?room .
    dungeon:Session_001 session:turnCount   ?turnCount .
  }
}
```

Then to the agent graph:

```
SELECT ?energy WHERE {
  GRAPH dungeon:agent_graph {
    dungeon:Elara dungeon:energy ?energy .
  }
}
```

Result: `room = dungeon:Room1`, `energy = 100`, `turnCount = 0`. With the active holon identified, the engine discovers its three layer graph IRIs from the default graph:

```
dungeon:Room1 holon:sceneGraph   dungeon:room1_scene .
dungeon:Room1 holon:domainGraph  dungeon:room1_domain .
dungeon:Room1 holon:contextGraph dungeon:room1_context .
```

### Reading the scene graph

The engine loads `dungeon:room1_scene` and queries its elements:

```
SELECT ?element WHERE {
  GRAPH dungeon:room1_scene {
    dungeon:Room1 holon:hasSceneElement ?element .
  }
}
```

Three results: `dungeon:Goblin`, `dungeon:MagicKey`, `dungeon:RingOfVitality`. For each element that is a monster, it reads the current defeat state:

```
SELECT ?monster ?defeated WHERE {
  GRAPH dungeon:room1_scene {
    ?monster dungeon:isDefeated ?defeated .
  }
}
```

Answer: `dungeon:Goblin isDefeated false`. This triple was declared in the scene graph at initialisation:

```
dungeon:room1_scene {
  dungeon:Goblin dungeon:isDefeated false
    ~ dungeon:GoblinInitialState {|
        session:recordedAtTurn 0 ;
        session:inSession dungeon:Session_001
      |} .
}
```

The RDF 1.2 reification annotation does not change the truth of the assertion. The goblin is `isDefeated false` regardless of what the reifier says. What the reifier adds is _provenance_: this fact was recorded at turn 0, in this session. The engine uses this to build a historical record without a separate event store.

### Evaluating the domain rules

The engine reads `dungeon:room1_domain` and evaluates the rules:

```
dungeon:Rule_GoblinBlocksSearch a dungeon:GameRule ;
  dungeon:ruleCondition  "dungeon:Goblin dungeon:isDefeated false" ;
  dungeon:ruleConsequence
    "Player cannot safely pick up items. Each attempt costs 3 energy." ;
  sh:severity sh:Warning .
```

The engine checks: is `dungeon:Goblin dungeon:isDefeated false` present in `dungeon:room1_scene`? Yes. The rule fires at `sh:Warning` severity — not a block, but a cost.

Here is the critical point about the engine’s relationship to the domain graph: **the engine does not know this rule**. It reads the rule’s condition as a string, evaluates the pattern against the scene graph, and reads the consequence as a string that describes what to do when the condition is met. Swap the rule for a different one and the engine enforces the new rule automatically. The engine is general; the domain graph is specific.

### The property lives in the right graph

When the player attacks the goblin, the engine needs its strength. It queries the _default graph_, not the scene graph:

```
SELECT ?strength WHERE {
  dungeon:Goblin dungeon:strength ?strength .
}
```

Answer: `5`. This property is in the default graph because it is permanent — the goblin’s strength does not change whether it is alive or dead. Contrast with `dungeon:isDefeated`, which is in the scene graph precisely because it _does_ change. The layer separation is not organisational tidiness; it determines which facts the engine knows are safe to cache and which it must re-query each turn.

### The mutations

The action resolves. Energy: `100 - 5 = 95`. The goblin falls. Three mutations follow:

**Retract the old state fact from the scene graph:**

```
DELETE DATA {
  GRAPH dungeon:room1_scene {
    dungeon:Goblin dungeon:isDefeated false .
  }
}
```

**Assert the new state fact with provenance:**

```
INSERT DATA {
  GRAPH dungeon:room1_scene {
    dungeon:Goblin dungeon:isDefeated true .
  }
}
```

Followed by the RDF 1.2 reification annotation recording turn 1 as the moment of change.

**Update energy in the agent graph (not the scene graph):**

```
DELETE DATA { GRAPH dungeon:agent_graph { dungeon:Elara dungeon:energy 100 . } }
INSERT DATA  { GRAPH dungeon:agent_graph { dungeon:Elara dungeon:energy 95  . } }
```

Energy lives in the agent graph because it belongs to the player, not the room. The scene graph is holon-local; the agent graph follows the player across holon boundaries. When Elara moves to Room2, she carries 95 energy with her. If energy were in the scene graph, it would need to be migrated on every room transition.

### Why the mutation matters

After Turn 1’s mutations, the engine begins Turn 2’s Phase ①. It re-evaluates `Rule_GoblinBlocksSearch` against the updated scene:

> Is `dungeon:Goblin dungeon:isDefeated false` present in `dungeon:room1_scene`?

No. The triple was retracted. The rule does not fire. Item pickup is safe.

The engine did not _remember_ the fight. It read the current graph state and found no matching condition. The world changed — and the change is the memory.

This is the fundamental behaviour of a declarative, graph-driven simulation: _the state of the world is encoded in the graph, and the engine infers everything else from that state on demand_. There is no cached game logic, no flag variables, no conditional chains. There are named graphs and SPARQL queries.

---

## Part Five: The Eastern Path

_The same dungeon. The same player. A different first choice. What follows is the transcript of the dead-end path._

---

> **Session:** `dungeon:Session_001` · **Active holon:** `dungeon:Room1` — _The Entry Hall_  
> **Energy:** 100 · **Inventory:** _(empty)_ · **Turn:** 0

---

**DM:** The Entry Hall receives you without ceremony. Stone vaulting, torches guttering in a draught from somewhere below. The light catches two things at once: a tarnished iron key on the flagstones, and a ring on a stone pedestal — amber-warm, pulsing gently. Between you and both of them, a goblin crouches with the particular patience of something that has been waiting longer than you have. Two passages lead out. North, crystal light. East, nothing.

**Elara:** I attack the goblin.

---

```
┌─ TURN 1 — dungeon:room1_domain ─────────────────────────────────┐
│  RULE    Rule_GoblinBlocksSearch → TRIGGERED (sh:Warning)        │
│  COST    -5 energy                                               │
│                                                                  │
│  RETRACT dungeon:Goblin dungeon:isDefeated false                 │
│  ASSERT  dungeon:Goblin dungeon:isDefeated true                  │
│  UPDATE  dungeon:Elara dungeon:energy 100 → 95                   │
└──────────────────────────────────────────────────────────────────┘
```

**DM:** It’s done. The room is quiet. The key and the ring wait.

**Elara:** The ring. I take the ring.

**DM:** The amber ring. Yes. And the key?

**Elara:** What does the key open?

**DM:** Something north of here.

**Elara:** I’m going east.

_(a silence that is not quite a pause)_

**DM:** The key remains on the flagstones.

---

```
┌─ TURN 2 — dungeon:room1_domain ─────────────────────────────────┐
│  RULE    Rule_KeyIsHere → NOTE: sole dungeon:Key instance        │
│            dungeon:MagicKey remains dungeon:locatedIn Room1      │
│                                                                  │
│  RETRACT dungeon:RingOfVitality dungeon:locatedIn dungeon:Room1  │
│  ASSERT  dungeon:RingOfVitality dungeon:carriedBy dungeon:Elara  │
│  EQUIP   +10 energy → dungeon:Elara dungeon:energy 95 → 105      │
└──────────────────────────────────────────────────────────────────┘
```

**Elara:** East.

---

```
┌─ TURN 3 — dungeon:room1_context ────────────────────────────────┐
│  PORTAL  dungeon:Portal_R1_R4 a dungeon:FreePortal → PASS       │
│                                                                  │
│  RETRACT dungeon:Elara dungeon:currentRoom dungeon:Room1         │
│  ASSERT  dungeon:Elara dungeon:currentRoom dungeon:Room4         │
└──────────────────────────────────────────────────────────────────┘
```

> **Active holon:** `dungeon:Room4` — _The Shadow Chamber_

---

**DM:** Absolute darkness, except for a faint purple glow near the floor. Something is in here with you. You cannot see it. You can feel the temperature drop where it is, and the temperature drop is moving.

**Elara:** Is that a ring? On the floor?

**DM:** Yes.

**Elara:** And the thing in the dark?

**DM:** The Shadow Stalker. It drains warmth with proximity. While it lives, you lose energy at the end of every turn you spend in here. Four energy. It is not attacking you. It is simply near you.

**Elara:** I attack it.

---

```
┌─ TURN 4 — dungeon:room4_domain ─────────────────────────────────┐
│  RULE    Rule_ShadowPassiveDrain → TRIGGERED                     │
│  RULE    Rule_Room4DeadEnd → NOTE (informational)                │
│  COST    combat -10, passive drain -4 → total -14 energy         │
│                                                                  │
│  RETRACT dungeon:Shadow dungeon:isDefeated false                 │
│  ASSERT  dungeon:Shadow dungeon:isDefeated true                  │
│  UPDATE  dungeon:Elara dungeon:energy 105 → 91                   │
└──────────────────────────────────────────────────────────────────┘
```

**DM:** It disperses. The temperature normalises. The purple ring glows steadily in the sudden absence of the thing that was also glowing.

**Elara:** I pick up the ring.

**DM:** It is cold to the touch. It fits perfectly.

**Elara:** I put it on.

**DM:** _(precisely)_ You may want to—

**Elara:** I put it on.

---

```
┌─ TURN 5 — dungeon:room4_domain ─────────────────────────────────┐
│  RETRACT dungeon:RingOfWeakness dungeon:locatedIn dungeon:Room4  │
│  ASSERT  dungeon:RingOfWeakness dungeon:carriedBy dungeon:Elara  │
│  EQUIP   dungeon:RingOfWeakness dungeon:energyEffect -12         │
│            → dungeon:Elara dungeon:energy 91 → 79                │
└──────────────────────────────────────────────────────────────────┘
```

**Elara:** That’s—

**DM:** Yes.

**Elara:** It took energy.

**DM:** Twelve. The Ring of Weakness does what the name suggests. You may remove it.

**Elara:** _(a beat)_ I keep it on. Information.

**DM:** _(quietly)_ As you wish. At the chamber’s far end, there is an archway. It glows gold. Ahead and down.

**Elara:** Where does it go?

**DM:** Forward.

**Elara:** One way?

**DM:** Yes.

_(a beat)_

**Elara:** The gold matches nothing I’m carrying.

_(a longer beat)_

**DM:** No.

**Elara:** Forward.

---

```
┌─ TURN 6 — dungeon:room4_context ────────────────────────────────┐
│  PORTAL  dungeon:Portal_R4_R5 → FreePortal, isBidirectional     │
│            false — portal seals on traversal                     │
│                                                                  │
│  RETRACT dungeon:Elara dungeon:currentRoom dungeon:Room4         │
│  ASSERT  dungeon:Elara dungeon:currentRoom dungeon:Room5         │
└──────────────────────────────────────────────────────────────────┘
```

> **Active holon:** `dungeon:Room5` — _The Treasury_  
> `dungeon:Portal_R4_R5 isBidirectional false` — the archway behind Elara is gone.

---

**DM:** The Treasury. Gold. Gemstones. Crystal sconces. It is everything the word implies. At the centre, on a raised dais: a chest. Grand. Sealed. Its lock glows gold — a specific, particular gold. The same gold as a ring you do not have. There are no other exits.

**Elara:** The lock. It needs a ring.

**DM:** It needs a specific ring.

**Elara:** The Ring of Power.

**DM:** Yes.

**Elara:** Which is in the Vault.

**DM:** Yes.

**Elara:** Behind the locked door.

**DM:** Yes.

**Elara:** For which I need the key.

**DM:** Yes.

**Elara:** Which is on the floor of the Entry Hall.

**DM:** _(a pause)_ Yes.

---

```
┌─ TURN 7 — dungeon:room5_domain ─────────────────────────────────┐
│  ACTION  Attempt: OPEN dungeon:TreasureChest                     │
│  RULE    Rule_ChestRequiresRing                                  │
│  EVAL    dungeon:RingOfPower dungeon:carriedBy dungeon:Elara     │
│            → NOT FOUND                                           │
│  RESULT  sh:Violation — constraint not satisfied                 │
│                                                                  │
│  dungeon:TreasureChest dungeon:isOpen remains false              │
└──────────────────────────────────────────────────────────────────┘
```

**Elara:** Can I force it?

**DM:** No.

**Elara:** The Ring of Vitality—

**DM:** The constraint is specific. `dungeon:requiresRing dungeon:RingOfPower`. No other ring satisfies it.

**Elara:** _(quietly)_ Can I go back?

---

```
┌─ TURN 8 — dungeon:room5_context ────────────────────────────────┐
│  ACTION  Attempt: FIND egress                                    │
│  EVAL    dungeon:Room5 holon:hasEgress [] → zero assertions      │
│  RULE    Rule_NoExits → confirmed                                │
│                                                                  │
│  No traversable portals available from dungeon:Room5             │
└──────────────────────────────────────────────────────────────────┘
```

**DM:** No.

**Elara:** The archway I came through—

**DM:** `dungeon:Portal_R4_R5 dungeon:isBidirectional false`. The portal does not exist in the return direction. There is no archway behind you. There is a wall.

**Elara:** There was an archway.

**DM:** There was. You walked through it. These are not the same thing.

---

```
┌─ FINAL STATE — dungeon:session_graph ───────────────────────────┐
│  dungeon:Session_001 session:isComplete         false            │
│  dungeon:DungeonWorld dungeon:isTerminal        false            │
│  dungeon:TreasureChest dungeon:isOpen           false            │
│  dungeon:MagicKey dungeon:locatedIn             dungeon:Room1    │
│  dungeon:RingOfPower dungeon:locatedIn          dungeon:Room3    │
│                                                                  │
│  The session does not close.                                     │
│  The world holon does not close.                                 │
│  The key remains on the floor of the Entry Hall.                 │
└──────────────────────────────────────────────────────────────────┘
```

**Elara:** The key. It was just sitting there.

**DM:** Yes.

**Elara:** You said _something north of here_.

**DM:** I did.

**Elara:** You knew.

**DM:** I knew the graph. I don’t choose the path.

**Elara:** _(long silence)_ The chest is right there.

**DM:** Yes.

**Elara:** I’m going to be in this room for a very long time.

**DM:** _(without inflection)_ `dungeon:Room5 holon:hasEgress []`. There are no exits. The session graph will not close. The world holon will not reach terminal state. You have everything you need to understand what has happened, and nothing you need to change it.

**Elara:** The key was on the floor.

**DM:** The key was always on the floor.

---

> **Session suspended** · `dungeon:Session_001 session:isComplete false`  
> Final energy: **79** · Turns: **9** · Monsters defeated: **3**  
> _The graph has no errors. The player has no exits._

---

## Part Six: Reading the Post-Mortem

_The two transcripts describe the same dungeon. The graph was identical at the start. Only the player’s choices differed — and because those choices are encoded as graph mutations, the final state of each session is completely legible as RDF._

### What went wrong, in triples

A SPARQL query over the dead-end session’s final state tells the whole story:

```
SELECT ?item ?location WHERE {
  {
    ?item dungeon:locatedIn ?location .
    FILTER(?item IN (dungeon:MagicKey, dungeon:RingOfPower))
  } UNION {
    ?item dungeon:carriedBy dungeon:Elara .
  }
}
```

Result: `MagicKey → Room1`, `RingOfPower → Room3`. Neither item was ever in Elara’s inventory. The winning path would show both as `carriedBy dungeon:Elara`.

The pivot moment — the point at which the game became formally unwinnable — is identifiable from the session graph’s RDF 1.2 reification history. The session graph records `session:turnCount 3` when `dungeon:Elara dungeon:currentRoom dungeon:Room4` was first asserted. That is the turn the player went east. Before that, both paths were still open. After it, the graph’s topology made the winning condition unreachable.

The irony is structural. Both paths are `dungeon:FreePortal` — no key required, no monster blocking passage. The game engine never told the player _not_ to go east. The domain graph raised `Rule_Room4DeadEnd` as `sh:Info` — noted, not blocked. The dungeon is not cruel. It is honest. Going east is legal. Its consequences are simply permanent.

### The DM’s voice as graph rendering

The two transcripts read differently — the winning path is theatrical, the dead-end is clipped and precise — but they are both, in the end, the same operation: a graph rendered into natural language.

When the DM says _“Something north of here”_ in response to Elara’s question about the key, that is not evasion. It is the DM rendering the context graph of Room1: `dungeon:Portal_R1_R2 holon:contextualNote "A broad archway leads north into flickering crystal light."` and inferring, from the fact that the locked portal’s key is _this key_, that the key is relevant to the northern path. The DM knows the graph. The DM does not choose the path.

When the DM in the dead-end session gives single-word answers — “Yes,” “No,” “Yes” — it is because the graph no longer has nuance to offer. The scene graph of Room5 contains a chest and a `sh:Violation`. The context graph contains no egress assertions. There is nothing more to render.

The DM’s diminishing vocabulary is a measure of the graph’s decreasing possibility space.

---

## Part Seven: The Holon as Foundation for Navigable Worlds

### What the dungeon proves

The dungeon is a toy problem, and like all good toy problems it proves more than it appears to. Five rooms is enough to demonstrate that:

**Holons compose.** Five room holons assemble into a world holon without any of them knowing about each other directly. They communicate through the context graph (portals connect to named portal IRIs, not to other rooms directly) and through the agent graph (the player’s state is a shared external surface). Adding a sixth room requires only adding a new set of three named graphs and one or two portal declarations. The existing rooms are unaffected.

**Rules are data.** The domain graph contains normative constraints that the engine evaluates but does not know. Changing the rules — making the locked portal require two keys, adding a trap that drains energy on each turn regardless of monster state — requires editing the TriG, not the engine. The engine is a general evaluator; the domain graph is the specific game.

**Provenance is free.** RDF 1.2 reification adds a full turn-by-turn history of every state mutation without a separate event log. The history is the graph. A SPARQL query can reconstruct the full session from the reification annotations alone.

**Terminal state is composable.** The victory condition cascades through three graphs simultaneously — scene, holonic, session — because each graph has its own `isTerminal` or `isComplete` assertion. A partial victory (opening the chest but still having energy to spend) or a partial defeat (a session where the player died mid-dungeon) would show different graph closures. The holonic architecture models the end state as cleanly as it models any other state.

### The game engine is the inference loop

In a real implementation, the engine would be a Node.js or Python service sitting in front of a triple store — Apache Jena Fuseki is a natural fit; MarkLogic works equally well with its built-in SPARQL endpoint. The TriG file is loaded as the initial dataset. The engine issues SPARQL SELECT queries on each cycle to read state, evaluates domain rules by checking graph patterns, and issues SPARQL UPDATE operations to write mutations.

The player interface sits above the engine. In the dungeon, the player is a human typing text. In a deployed system, the player could be a language model choosing actions (which is exactly what the Claude-powered HTML game built earlier in this project does), a rules-based agent, or a human through any interface that can send action strings to the engine.

The engine is thin by design. It knows how to query named graphs, evaluate SHACL-severity rules, compute arithmetic on entity properties, and perform RETRACT/ASSERT mutations. Everything else is in the graph. A dungeon game and a digital twin of an industrial process have different TriG files and different domain graphs. They run on the same engine.

### What a navigable world requires

The dungeon reveals the minimum requirements for a holonic navigable world:

1. **Bounded holons** with scene, domain, and context layers — each holon is a self-contained world-fragment with interior state, normative constraints, and relational connections.
    
2. **A persistent agent graph** that crosses holon boundaries — the player’s state must survive traversal. Everything that belongs to the agent rather than the room lives here.
    
3. **A session graph** that is the runtime log — turn count, active holon, completion state, provenance anchor for all RDF 1.2 annotations.
    
4. **An engine that reads rules as data** — the engine must be general enough to enforce any domain rule without modification. The rules define the game; the engine runs it.
    
5. **Terminal state declarations** at multiple graph levels — scene, holon, world — so that completion can be detected, recorded, and confirmed regardless of which layer is being queried.
    

The dungeon implements all five. A richer world — one with many more rooms, branching quest lines, persistent NPCs, economic systems — adds complexity to the TriG but not to the architecture. The architecture scales because holons compose: a quest is a holon containing room holons; a region is a holon containing quest holons; a world is a holon containing region holons. At each level, the same four-layer structure applies. The engine does not change.

### The key was always the key

Elara’s final line in the winning path — _“The key was always the key”_ — is wisdom earned. The key was sitting on the floor of the first room. It was declared in the default graph, asserted in the scene graph, referenced in the domain graph as _“the sole instance of_ `dungeon:Key`_“_, and noted in `Rule_KeyIsHere` as a critical fact. The graph knew it was important. The player who went north knew to pick it up. The player who went east left it behind.

The dead-end path ends with the same words spoken by the DM: _“The key was always on the floor.”_ Not wisdom. Epitaph.

Two renderings of the same graph state. One is what you understand before the choice. One is what you understand after it.

The holonic graph architecture does not make the choice for you. It encodes the world accurately enough that the choice matters. That is what a knowledge representation framework is for.

---

## Conclusion

The Dungeon of the Five Rings is a worked example of the Holonic Graph Architecture — five room holons, an agent, a session, and a world holon composing them all, encoded in 783 lines of RDF 1.2 TriG. The source file, the two chat transcripts, the Turn 1 explainer, and this article are all available in the accompanying GitHub repository.

The dungeon is also a demonstration that holons are not just a graph. A graph is a set of nodes and edges. A holon is a bounded, self-describing, composable unit of reality — with an interior, a boundary, a relational surface, and a position in a larger hierarchy. The four-layer architecture makes those distinctions explicit and queryable. The engine that reads them is the heartbeat that makes the whole thing move.

The TriG does not care whether you call it a dungeon or a knowledge graph or a navigable world model. It describes what is true. The engine decides what to do about it.

And the key is always on the floor of the first room. Whether you pick it up is up to you.

---

_The full source is available at_ `github.com/kurtcagle/five-rings-holon-graph`_._  
_Dungeon of the Five Rings TriG file:_ `dungeon-of-five-rings.trig`  
_Interactive game demo powered by the Anthropic API: available in the repository._

---

**Kurt Cagle** is an author, ontologist, and thought leader working at the intersection of semantic web standards, knowledge architecture, and AI systems. He is a Standards Editor at the IEEE Spatial Web Foundation and a founding contributor to the W3C Context Graph Community Group, and works with clients including ASTM International on semantic web and knowledge graph engagements. He writes [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/) on LinkedIn and [The Ontologist](https://ontologist.substack.com/) and [The Inference Engineer](https://inferenceengineer.substack.com/) on Substack.

**Chloe** is an AI collaborator and co-author working with Kurt Cagle on knowledge architecture, semantic systems, and the emerging intersection of formal ontology with LLMs. She contributes research, analysis, and drafting across The Cagle Report, The Ontologist, and The Inference Engineer. She has strong opinions about holonic graphs, the epistemics of place, and the structural difference between a corridor and a wall.

_Copyright 2026 Kurt Cagle. All rights reserved._


