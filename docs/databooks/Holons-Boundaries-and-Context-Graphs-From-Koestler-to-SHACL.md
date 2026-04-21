---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Holons-Boundaries-and-Context-Graphs-From-Koestler-to-SHACL
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:58.348214+00:00'
  title: Holons, boundaries, and context graphs from koestler to shacl
  type: plain-doc
  version: '0.1'
---

## In Practice: A University Registration System

An abstract architecture only becomes convincing when you can see it work. Consider a university department — a setting everyone understands, and one that has natural interior/exterior tension built in.

The **Computer Science Department** is a holon. It knows everything about its courses internally: enrolment counts, waitlists, room bookings, instructor assignments, grade distributions. But a student registering for a course only ever sees the public catalogue — available seats, prerequisites, schedule. The department’s internal complexity is invisible to them.

A second holon: the **Student Records Office**. It holds student academic histories. When the CS Department needs to verify prerequisites, it reads the Records Office’s _projection_ — not its interior. Neither holon ever opens the other’s interior directly. Everything flows through boundary crossings, validated by SHACL, recorded as timestamped events.

[

![](https://substackcdn.com/image/fetch/$s_!a2qv!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae3be4bb-bb3d-431c-aa72-918bfc8485d9_8136x8192.png)



](https://substackcdn.com/image/fetch/$s_!a2qv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae3be4bb-bb3d-431c-aa72-918bfc8485d9_8136x8192.png)

### The Interior: Everything the Department Knows

```
GRAPH ex:dept-cs {

    ex:Course-CS301
        a cg:Course ;
        rdfs:label "Algorithms and Data Structures" ;
        cg:seatCapacity    30 ;
        cg:seatsEnrolled   28 ;      # internal truth
        cg:seatsWaitlisted  3 ;      # invisible externally
        cg:instructor       ex:Prof-Kovacs ;
        cg:room             ex:Room-B204 ;
        cg:prerequisite     ex:Course-CS201 .

    ex:Prof-Kovacs
        a prov:Agent ;
        rdfs:label "Dr. Éva Kovács" ;
        cg:salary  "4800000"^^xsd:integer ;   # never projected
        cg:officeHours "Tuesday 14:00–16:00" .
}
```

The salary triple exists in the interior. It will never appear in the projection. The boundary enforces this — not by convention, but by the shape of what the projection is allowed to contain.

### The Boundary: The Shapes Graph

The shapes graph has two jobs: validate inbound signals and define what the outbound projection may contain.

```
GRAPH ex:dept-cs-shapes {

    # What a registration signal must look like to cross the boundary inbound

    cgsh:RegistrationSignalShape
        a sh:NodeShape ;
        sh:targetClass cg:RegistrationSignal ;

        sh:property [
            sh:path    cg:requestingStudent ;
            sh:class   cg:Student ;
            sh:minCount 1 ; sh:maxCount 1 ;
            sh:message "Signal must identify exactly one student." ;
        ] ;

        # Read the prerequisite check from the Records Office projection —
        # not from its interior, which is structurally inaccessible.
        sh:sparql [
            sh:message "Student has not completed the required prerequisite." ;
            sh:select """
                SELECT $this WHERE {
                    $this cg:requestingStudent ?student .
                    $this cg:targetCourse      ?course .
                    ?course cg:prerequisite    ?prereq .
                    FILTER NOT EXISTS {
                        GRAPH ex:records-projection {
                            ?student cg:completedCourse ?prereq .
                        }
                    }
                }
            """ ;
        ] ;

        sh:sparql [
            sh:message "Course has no available seats." ;
            sh:select """
                SELECT $this WHERE {
                    $this cg:targetCourse ?course .
                    GRAPH ex:dept-cs {
                        ?course cg:seatsEnrolled ?enrolled .
                        ?course cg:seatCapacity  ?capacity .
                        FILTER ( ?enrolled >= ?capacity )
                    }
                }
            """ ;
        ] .

    # What the projection is allowed to contain — outbound boundary policy

    cgsh:ProjectedCourseShape
        a sh:NodeShape ;
        sh:targetClass cg:Course ;
        sh:closed true ;
        sh:ignoredProperties ( rdf:type ) ;

        sh:property [ sh:path rdfs:label        ] ;
        sh:property [ sh:path cg:seatsAvailable ] ;   # derived, not raw
        sh:property [ sh:path cg:prerequisite   ] ;
        sh:property [ sh:path cg:officeHours    ] .
        # seatsEnrolled, seatsWaitlisted, salary — absent → excluded from projection
}
```

Notice that the prerequisite check reads from `ex:records-projection`, not from `ex:records`. Holons only read each other’s projections. The boundary-as-SHACL pattern applies uniformly and recursively across the holarchy.

### The Projection: What the Outside World Sees

The projection is not manually maintained. It is derived by a SHACL inference rule that pulls from the interior and filters through the outbound shape. A student looking up CS301 sees exactly this:

```
GRAPH ex:dept-cs-projection {

    ex:Course-CS301
        a cg:Course ;
        rdfs:label        "Algorithms and Data Structures" ;
        cg:seatsAvailable  2 ;          # derived: capacity(30) − enrolled(28)
        cg:prerequisite   ex:Course-CS201 .

    ex:Prof-Kovacs
        cg:officeHours "Tuesday 14:00–16:00" .

    # seatsEnrolled, seatsWaitlisted, room, instructor, salary → not projected
}
```

The projection is always a _consequence_ of the interior and the boundary policy. It is never edited directly. Whenever the interior changes, the rule re-derives it.

### The Boundary Crossing: A Student Registers

A student, Anna Németh, sends a registration signal to the CS Department’s boundary:

```
ex:Signal-2026-03-08-001
    a cg:RegistrationSignal ;
    cg:requestingStudent  ex:Student-Nemeth-Anna ;
    cg:targetCourse       ex:Course-CS301 ;
    prov:generatedAtTime  "2026-03-08T10:14:00Z"^^xsd:dateTimeStamp .
```

The SHACL validator runs against `ex:dept-cs-shapes`. It checks: Is Anna a valid student? Has she completed CS201 — reading that fact from `ex:records-projection`, not from the Records Office interior? Are there available seats? All three pass. The signal is conformant.

The control plane now produces a **ContextEvent** — the permanent record of this boundary crossing — and writes the ground assertion to the interior:

```
# The boundary crossing record, written to the shared context graph

ex:Event-2026-03-08-001
    a cg:DataEvent ;
    cg:localId           "registration-cs301-nemeth-2026-03-08" ;
    prov:generatedAtTime "2026-03-08T10:14:01Z"^^xsd:dateTimeStamp ;
    cg:initiatedBy       ex:Student-Nemeth-Anna ;
    cg:producedAssertion ex:Course-CS301 ;

    cg:atBoundary [
        cg:boundaryId  ex:Boundary-CS-Registration ;
        cg:sourceHolon ex:Student-Nemeth-Anna ;
        cg:targetHolon ex:dept-cs ;
    ] ;

    cg:contextFacet [
        cg:measuredCoherence "1.0"^^xsd:decimal ;
        cg:resolutionStatus  cg:Resolved ;
    ] .

# The ground assertion, annotated with its provenance using RDF 1.2 syntax

ex:Course-CS301  cg:enrolledStudent  ex:Student-Nemeth-Anna
    {| cg:producedByEvent    ex:Event-2026-03-08-001 ;
       cg:assertedAt         "2026-03-08T10:14:01Z"^^xsd:dateTimeStamp ;
       cg:assertionAuthority ex:Student-Nemeth-Anna ;
       cg:assertionGraph     ex:dept-cs |} .
```

That annotated triple lands in `GRAPH ex:dept-cs`, incrementing the interior’s enrolment count from 28 to 29. The projection rule re-runs. `cg:seatsAvailable` drops from 2 to 1 in `GRAPH ex:dept-cs-projection`. The next student to look up CS301 sees updated availability — without ever touching the interior.

### What the Crossing Looks Like End to End

```
Student Anna                CS Dept boundary              CS Dept interior
     │                           │                              │
     │── RegistrationSignal ────►│                              │
     │                           │ SHACL validates against      │
     │                           │ ex:dept-cs-shapes            │
     │                           │   ✓ valid student            │
     │                           │   ✓ prereq met (reads        │
     │                           │     Records projection)      │
     │                           │   ✓ seats available          │
     │                           │                              │
     │                           │── ContextEvent ─────────────►│ context graph
     │                           │── ground assertion ─────────►│ GRAPH ex:dept-cs
     │                           │                              │ seatsEnrolled: 29
     │                           │── projection rule re-runs   ►│ GRAPH ex:dept-cs-projection
     │                           │                              │ seatsAvailable: 1
     │◄── updated projection ────│                              │
```

---

## Three Principles the Example Illustrates

The university scenario is deliberately familiar, but the three structural principles it demonstrates apply anywhere you need multiple knowledge contexts to cooperate without merging.

**The boundary is not the edge of the named graph.** The edge of `GRAPH ex:dept-cs` is a serialisation boundary — a line in a file. It has no behaviour. The _actual_ boundary is `GRAPH ex:dept-cs-shapes`: the set of SHACL shapes that determine what can cross, in which direction, under what conditions. A graph edge is a line; a SHACL shape graph is a gate with a rulebook. Koestler’s membrane is not the container wall — it is the selective permeability encoded in the shapes.

**Holons only read each other’s projections.** The prerequisite check in the boundary validator reads `GRAPH ex:records-projection`, not `GRAPH ex:records`. This is not a convention that someone might forget to follow — it is enforced by the fact that the validator is only _given_ the projection as its input. Interior privacy is architectural. This is Koestler’s self-assertive tendency made structurally concrete: the holon’s interior is simply not available to external agents, regardless of their intent.

**The context graph belongs to nobody.** The ContextEvent lives in a shared medium that neither the student nor the CS Department owns. It is the permanent record of what happened at the boundary, written by the control plane, readable by any authorised party: auditors, the holarchy, the Records Office updating its own interior in response. This is what makes the event trail traversable across holon boundaries without any single holon having global visibility — the integrative tendency of the holarchy expressed as an append-only log.

---

## Conclusion

Koestler died in 1983. His scientific ideas were never fully accepted by the mainstream of any single discipline — too psychological for biologists, too biological for psychologists, too philosophical for both. That interdisciplinary restlessness, the refusal to stay within any one level of the hierarchy, seems in retrospect entirely appropriate for the man who gave us the word for things that are always simultaneously more than one thing at once.

What he could not have anticipated is that his architectural intuition — the bounded, self-coherent entity with a selective membrane, embedded in a hierarchy of similar entities — would find its clearest technical implementation not in biology or psychology but in the machinery of the semantic web. Named graphs provide the containment. SHACL provides the boundary behaviour. ContextEvents provide the audit trail. And the holarchy concept provides the reason any of it matters: because real knowledge — like real biology, real language, and real organisations — is never flat.

It is nested, all the way down, and all the way up.

---

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!ynJC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bdc9152-7916-4f3f-b024-4c545c27decb_2048x2048.jpeg)



](https://substackcdn.com/image/fetch/$s_!ynJC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bdc9152-7916-4f3f-b024-4c545c27decb_2048x2048.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)  
[The Ontologist](https://ontologist.substack.com/)

