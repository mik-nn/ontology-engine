---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: What-Does-SHACL-Do
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:03.948857+00:00'
  title: What does shacl do
  type: plain-doc
  version: '0.1'
---

# What does shacl do

[

![](https://substackcdn.com/image/fetch/$s_!duF1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe76ad1dd-bffc-42f8-811c-c463cf036b56_2048x1168.jpeg)



](https://substackcdn.com/image/fetch/$s_!duF1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe76ad1dd-bffc-42f8-811c-c463cf036b56_2048x1168.jpeg)

I started writing about SHACL several months ago, but both my understanding has increased, and several significant changes to the specification have also occurred. Consequently, I felt it might be worth revisiting exactly how SHACL works (with an emphasis on SHACL 1.2).

## A SHACL Pipeline

SHACL has a very definite workflow from a pipeline standpoint:

- **Select** the focus nodes that will be used by the SHACL process. This is managed by a **Node Shape**.
    
- **Validate** each focus node by comparing it to a set of constraint shapes, and for each constraint that it fails to match, generate a report. If the node fits the shape, it is considered valid. This mostly covers Property Shapes, but it can also cover **SPARQL Constraints**. Constraint nodes only check validity, but do not add nodes to the graph.
    
- **Generate** triples as output if one or more rules are in place for each focus node that validates.
    

That’s it. If there are no validation constraints, all focus nodes will be passed to the rules to generate output. If there are constraints but no rules, then reports will be generated for each focus node that fails validation. If there are multiple rules, the graph is locked for that SHACL process until the whole process completes.

For each stage in the pipeline, the SHACL typically will perform a SPARQL query on the graph relative to each focus node. In many respects, you can think of SHACL as the next stage of evolution for SPARQL, making it possible to utilise it for processing pipelines. You could use a combination of SPARQL query and SPARQL update functions to do the same thing, but the SHACL approach allows you to combine three different functions into a single (often much better performing) call.

## Exploring This Pattern From Use Cases

It’s always useful to see real world (more or less) use cases to illustrate how a given technology works. In this case, consider the following:

### Use Case: Evaluating an Exam

> All of the students in Mrs. Cunningham’s Sophomore English Class take a midterm test on Shakespeare’s plays. Those students who receive an A on the test get a good citation on their record and are validated. Those who received a B on the test are validated but don’t get the citation. Those students who received a C or D on their tests are validated with a warning, while those who receive an F are invalidated with a report indicating they need remediation.

This covers all bases: all students who get everything but an F pass the exam, students who get an A get a gold star, students with a C or D are flagged as potential watch cases, and those with an F need special attention (they failed validation).

The dataset is fairly simple:

```
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh:    <http://www.w3.org/ns/shacl#>
PREFIX shnex: <http://www.w3.org/ns/shacl-node-expr#>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>
PREFIX ex:    <http://example.com/school#>

# ─────────────────────────────────────────────────
# ONTOLOGY
# ─────────────────────────────────────────────────

ex:Student          a rdfs:Class .
ex:Teacher          a rdfs:Class .
ex:EnglishClass     a rdfs:Class .
ex:Citation         a rdfs:Class .
ex:RemediationFlag  a rdfs:Class .

ex:enrolledIn       a rdf:Property .   # Student → EnglishClass
ex:taughtBy         a rdf:Property .   # EnglishClass → Teacher
ex:classYear        a rdf:Property .   # EnglishClass → xsd:string
ex:subject          a rdf:Property .   # EnglishClass → xsd:string
ex:shakespeareGrade a rdf:Property .   # Student → xsd:string ("A"–"F")
ex:goodCitation     a rdf:Property .   # Student → Citation (rule-generated)
ex:needsRemediation a rdf:Property .   # Student → RemediationFlag (rule-generated)

# ─────────────────────────────────────────────────
# CLASS INSTANCE — THE TARGET CLASS
# ─────────────────────────────────────────────────

ex:CunninghamSophomoreEnglish
    a ex:EnglishClass ;
    ex:taughtBy   ex:MrsCunningham ;
    ex:classYear  "Sophomore" ;
    ex:subject    "English" ;
    ex:className  "Sophomore English — Mrs. Cunningham" .

ex:MrsCunningham
    a ex:Teacher ;
    ex:name "Cunningham" .

# Citation and remediation resources
ex:ShakespeareMidtermCitation
    a ex:Citation ;
    ex:description "Outstanding performance on Shakespeare Midterm" .

ex:ShakespeareMidtermRemediation
    a ex:RemediationFlag ;
    ex:description "Remediation required: Shakespeare Midterm" ;
    ex:course      ex:CunninghamSophomoreEnglish .


# ─────────────────────────────────────────────────
# DATA GRAPH — STUDENTS AND GRADES
# ─────────────────────────────────────────────────

# A grade — conforms + citation rule fires
ex:AliceKowalski
    a ex:Student ;
    ex:name             "Alice Kowalski" ;
    ex:enrolledIn       ex:CunninghamSophomoreEnglish ;
    ex:shakespeareGrade "A" .

# B grade — conforms, no citation, no warning
ex:BenTremblay
    a ex:Student ;
    ex:name             "Ben Tremblay" ;
    ex:enrolledIn       ex:CunninghamSophomoreEnglish ;
    ex:shakespeareGrade "B" .

# C grade — conforms with Warning
ex:CarlaFontaine
    a ex:Student ;
    ex:name             "Carla Fontaine" ;
    ex:enrolledIn       ex:CunninghamSophomoreEnglish ;
    ex:shakespeareGrade "C" .

# D grade — conforms with Warning
ex:DavidOsei
    a ex:Student ;
    ex:name             "David Osei" ;
    ex:enrolledIn       ex:CunninghamSophomoreEnglish ;
    ex:shakespeareGrade "D" .

# F grade — Violation + remediation rule fires
ex:EvaLindqvist
    a ex:Student ;
    ex:name             "Evan Lindqvist" ;
    ex:enrolledIn       ex:CunninghamSophomoreEnglish ;
    ex:shakespeareGrade "F" .

# Not in this class — not targeted, not validated at all
ex:FrankMueller
    a ex:Student ;
    ex:name             "Frank Mueller" ;
    ex:enrolledIn       ex:OtherClass ;
    ex:shakespeareGrade "B" . 
```

Notice that there are several distinct scenarios here: Frank Mueller is not in Mrs. Cunningham’s class, for instance (there may be multiple sophomore English classes taking the same test, for instance). Additionally, there’s a simple taxonomy indicating either citation (commendation) or remediation.

While there may be potentially many shapes here, let’s concentrate on the one involving this particular test:

```
# ─────────────────────────────────────────────────
# SHAPES GRAPH
# ─────────────────────────────────────────────────

ex:ShakespeareMidtermShape
    a sh:NodeShape ;

    # TARGET: all students enrolled in Mrs. Cunningham's class
    # Uses inverse path to walk from the class back to enrolled students
    sh:targetNode [
        shnex:pathValues [ sh:inversePath ex:enrolledIn ] ;
        shnex:focusNode ex:CunninghamSophomoreEnglish ;
    ] ;


    # ── Structural prerequisite ───────────────────
    # Every targeted student must have exactly one grade recorded
    sh:property [
        sh:path     ex:shakespeareGrade ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:in       ( "A" "B" "C" "D" "F" ) ;
        sh:message  "Student must have exactly one valid Shakespeare midterm grade." ;
    ] ;

    # ── F grade: Violation ────────────────────────
    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:severity sh:Violation ;
        sh:message  "Grade F — student requires remediation in Shakespeare." ;
        sh:prefixes ex: ;
        sh:select   """
            PREFIX ex: <http://example.com/school#>
            SELECT $this ?value
            WHERE {
                $this ex:shakespeareGrade ?value .
                FILTER(?value = "F")
            }
        """ ;
    ] ;

    # ── C or D: Warning ───────────────────────────
    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:severity sh:Warning ;
        sh:message  "Grade C or D — student performance below expectations on Shakespeare midterm." ;
        sh:prefixes ex: ;
        sh:select   """
            PREFIX ex: <http://example.com/school#>
            SELECT $this ?value
            WHERE {
                $this ex:shakespeareGrade ?value .
                FILTER(?value IN ("C", "D"))
            }
        """ ;
    ] ;

    # ── A grade: Info (citation was awarded by rule) ──
    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:severity sh:Info ;
        sh:message  "Grade A — good citation awarded." ;
        sh:prefixes ex: ;
        sh:select   """
            PREFIX ex: <http://example.com/school#>
            SELECT $this ?value
            WHERE {
                $this ex:shakespeareGrade ?value .
                FILTER(?value = "A")
            }
        """ ;
    ] .
```

The `ex:ShakespeareMidtermShape` node shape identifies the focus nodes to be used. Note here that this shape does not look specifically for a "student class” via `sh:targetClass`, because this would include all students who took the test, not just those in Mrs Cunningham’s class. Instead, it looks specifically for those students that are enrolled in this teacher’s class:

```
sh:targetNode [
        shnex:pathValues [ sh:inversePath ex:enrolledIn ] ;
        shnex:focusNode ex:CunninghamSophomoreEnglish ;
    ] ;
```

The inversePath may be a little confusing. The focus node in this case is the class session designator `ex:CunninghamSophomoreEnglish` , which is an object for each student, but is a subject for the targetNode. The above translates to SPARQL as:

```
SELECT $this WHERE {
    ex:CunninghamSophomoreEnglish ^ex:enrolledIn $this .
}
```

which is the inverse of:

```
SELECT $this WHERE {
    $this ex:CunninghamSophomoreEnglish .
}
```

This is why you’ll frequently see sh:inversePath with `sh:targetNode` and similar directives.

This retrieves a set of target nodes (student records) that can then be validated to determine whether they satisfy certain conditions.

The first constraint is a property shape that determines structural compliance for the grade itself:

```
# ── Structural prerequisite ───────────────────
    # Every targeted student must have exactly one grade recorded
    sh:property [
        sh:path     ex:shakespeareGrade ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:in       ( "A" "B" "C" "D" "F" ) ;
        sh:severity sh:Violation ;
        sh:message  "Student must have exactly one valid Shakespeare midterm grade." ;
    ] ;
```

A property shape is a constraint on the value of a specific property (as specified by its path). In this case, the student will have _one and only one_ grade for this particular test, as represented by the latters “A” through “F”, not including “E”. If the value for this field is “E”, this is a validation failure. If there is no grade given, this is a validation failure. If the value is a number, this is a validation failure. The `sh:message` provides an indication that the overall property failed due to the overall combination of these factors, but the SHACL engine may also provide additional information specific to one particular constraint” (the value is not in the list provided, for instance).

The next constraint on the focus node is the condition that the grade is an “F”, meaning that student failed the test (a validation error). Note that this isn’t a structural constraint but rather a business constraint requiring remediation. This is handled with a SPARQL constraint:

```
# ── F grade: Violation ────────────────────────
    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:severity sh:Violation ;
        sh:message  "Grade F — student requires remediation in Shakespeare." ;
        sh:prefixes ex: ;
        sh:select   """
            PREFIX ex: <http://example.com/school#>
            SELECT $this ?value
            WHERE {
                $this ex:shakespeareGrade ?value .
                FILTER(?value = "F")
            }
        """ ;
    ] ;
```

In this case, the focus node (represented by $this) performs a query that checks the grade (assigned to ?value) and if that value is “F” then the overall constraint _fails_. This can trip up people unfamiliar with SHACL: constraints look for specific conditions that indicate failure, not success. The sh:severity also informs the validator that it should treat this as a violation (the highest order of severity). This will generate a report in either text or as RDF (depending upon the settings of the pipeline), with the report looking something like:

```
 [ a sh:ValidationReport ;
  sh:conforms false ;       # false because EvaLindqvist has a Violation

  # Alice — sh:Info (citation noted)
  sh:result [
      a sh:ValidationResult ;
      sh:focusNode ex:AliceKowalski ;
      sh:resultSeverity sh:Info ;
      sh:resultMessage "Grade A — good citation awarded." ;
      sh:value "A" ;
  ] ;

  # Carla — sh:Warning
  sh:result [
      a sh:ValidationResult ;
      sh:focusNode ex:CarlaFontaine ;
      sh:resultSeverity sh:Warning ;
      sh:resultMessage "Grade C or D — student performance below expectations on Shakespeare midterm." ;
      sh:value "C" ;
  ] ;

  # David — sh:Warning
  sh:result [
      a sh:ValidationResult ;
      sh:focusNode ex:DavidOsei ;
      sh:resultSeverity sh:Warning ;
      sh:resultMessage "Grade C or D — student performance below expectations on Shakespeare midterm." ;
      sh:value "D" ;
  ] ;

  # Evan — sh:Violation
  sh:result [
      a sh:ValidationResult ;
      sh:focusNode ex:EvaLindqvist ;
      sh:resultSeverity sh:Violation ;
      sh:resultMessage "Grade F — student requires remediation in Shakespeare." ;
      sh:value "F" ;
  ] ;
] .
```

Note a couple things here: first, the validation indicates that conformance is false, but only because there was a violation (for Evan at the bottom). Had Evan received a “D” and no one else received an “F” then the report would have conformed to validation.For instance, Carla and David (with grades of “C” and “D” respectively had warnings but not violations because of the severity setting:

```
 # ── C or D: Warning ───────────────────────────
    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:severity sh:Warning ;
        sh:message  "Grade C or D — student performance below expectations on Shakespeare midterm." ;
        sh:prefixes ex: ;
        sh:select   """
            PREFIX ex: <http://example.com/school#>
            SELECT $this ?value
            WHERE {
                $this ex:shakespeareGrade ?value .
                FILTER(?value IN ("C", "D"))
            }
        """ ;
    ] ;
```

Finally, you can create situations where a constraint is intended to ascertain a positive outcome, such as a student receiving an “A”.

```
# ── A grade: Info (citation was awarded by rule) ──
    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:severity sh:Info ;
        sh:message  “Grade A — good citation awarded.” ;
        sh:prefixes ex: ;
        sh:select   “”“
            PREFIX ex: <http://example.com/school#>
            SELECT $this ?value
            WHERE {
                $this ex:shakespeareGrade ?value .
                FILTER(?value = “A”)
            }
        “”“ ;
    ] .
```

The important takeaway here is that the reports indicate remarkable conditions. For instance, Ben Trimbley doesn’t show up at all in the report because there is no specific SHACL constraint that covers the “B” grade contingency - this is the expected grade.

## Rules as Generators

The rules section can be facilitated in one of two ways - either through a separate non-Turtle format called Shacl Rule Language (SRL) or via SHACL statements in Turtle that do much the same thing. SRL is basically the same as SPARQL, but with a RULE command rather than a CONSTRUCT command.

This can be seen in the separate SRL Rules discussed above:

```
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex:   <http://example.com/school#>

# Rule 1: Award good citation to A students
# Fires only if citation not already present (idempotent)

RULE { ?student ex:goodCitation ex:ShakespeareMidtermCitation }
WHERE {
    ?student rdf:type ex:Student .
    ?student ex:enrolledIn ex:CunninghamSophomoreEnglish .
    ?student ex:shakespeareGrade "A" .
    NOT { ?student ex:goodCitation ex:ShakespeareMidtermCitation }
}

# Rule 2: Flag F students for remediation

RULE { ?student ex:needsRemediation ex:ShakespeareMidtermRemediation }
WHERE {
    ?student rdf:type ex:Student .
    ?student ex:enrolledIn ex:CunninghamSophomoreEnglish .
    ?student ex:shakespeareGrade "F" .
    NOT { ?student ex:needsRemediation ex:ShakespeareMidtermRemediation }
}
```

Rule 1 handles the case where the student received an A on the mid-term. Note that it only fires when the citation has not already been added into the graph. Similarly Rule 2 handles the case where the student received an F on the mid-term.

By the way, this can be combined with annotations (reification:)

```
RULE {
    ?student ex:goodCitation ex:ShakespeareMidtermCitation
        ~ ?citationEvent {|
            a        ex:CitationEvent ;
            ex:when  ?time ;
        |}
}
WHERE {
    ?student rdf:type ex:Student .
    ?student ex:enrolledIn ex:CunninghamSophomoreEnglish .
    ?student ex:shakespeareGrade "A" .

    NOT { ?student ex:goodCitation ex:ShakespeareMidtermCitation }

    BIND( NOW() AS ?time )
    BIND( IRI(CONCAT(
              STR(ex:ShakespeareMidtermCitation),
              'Event',
              '-',
              STRUUID()
          )) AS ?citationEvent )
}

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex:  <http://example.com/school#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

RULE {
    ?student ex:needsRemediation ex:ShakespeareMidtermRemediation
        ~ ?remediationEvent {|
            a        ex:RemediationEvent ;
            ex:when  ?time ;
        |}
}
WHERE {
    ?student rdf:type ex:Student .
    ?student ex:enrolledIn ex:CunninghamSophomoreEnglish .
    ?student ex:shakespeareGrade "F" .

    NOT { ?student ex:needsRemediation ex:ShakespeareMidtermRemediation }

    BIND( NOW() AS ?time )
    BIND( IRI(CONCAT(
              STR(ex:ShakespeareMidtermRemediation),
              'Event',
              '-',
              STRUUID()
          )) AS ?remediationEvent )
}
```

When the rules are run, the state of the graph is evaluated:

[

![](https://substackcdn.com/image/fetch/$s_!nfnm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F705cf004-37b0-431c-ab7e-ed0ed326907b_723x666.png)



](https://substackcdn.com/image/fetch/$s_!nfnm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F705cf004-37b0-431c-ab7e-ed0ed326907b_723x666.png)

and the new inferences are made:

```
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex:   <http://example.com/school#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

# ─────────────────────────────────────────────────────────────────────────────
# Rule 1 output — AliceKowalski receives her citation.
#
# The asserted triple:
#   ex:AliceKowalski ex:goodCitation ex:ShakespeareMidtermCitation
#
# The reifier ex:ShakespeareMidtermCitation-<uuid> annotates that triple
# with provenance: the class of event and the timestamp of rule execution.
# ─────────────────────────────────────────────────────────────────────────────

ex:AliceKowalski ex:goodCitation ex:ShakespeareMidtermCitation
    ~ ex:ShakespeareMidtermCitationEvent-a3f7c82d-1b4e-4f9a-8c2d-6e5f0a1b3c7d {|
        a        ex:CitationEvent ;
        ex:when  "2026-03-16T09:00:00Z"^^xsd:dateTime ;
    |} .

# ─────────────────────────────────────────────────────────────────────────────
# Rule 2 output — EvaLindqvist is flagged for remediation.
#
# The asserted triple:
#   ex:EvaLindqvist ex:needsRemediation ex:ShakespeareMidtermRemediation
#
# The reifier annotates it with the event class and execution timestamp.
# ─────────────────────────────────────────────────────────────────────────────

ex:EvaLindqvist ex:needsRemediation ex:ShakespeareMidtermRemediation
    ~ ex:ShakespeareMidtermRemediationEvent-d9e2f15b-7a3c-4b8e-9f1d-2c4a6b8d0e3f {|
        a        ex:RemediationEvent ;
        ex:when  "2026-03-16T09:00:00Z"^^xsd:dateTime ;
    |} .
```

By the way, a similar event indicating the termination of the remediation event can be added (Evan took a retest a week later) through rules in a similar manner, giving this:

```
ex:EvaLindqvist ex:receivedRemediation ex:ShakespeareMidtermRemediation
    ~ ex:ShakespeareMidtermRemediationTerminationEvent-7a3c15b-d9e2f-4b8e-0e3f-2c4a6b8d9f1d {|
        a        ex:RemediationTerminationEvent ;
        ex:when  “2026-03-21T09:00:00Z”^^xsd:dateTime ;
        event:oldGrade "F" ;
        event:newGrade "C" ;
        event:terminates ex:ShakespeareMidtermRemediationEvent-d9e2f15b-7a3c-4b8e-9f1d-2c4a6b8d0e3f; 
    |} .
```

This doesn’t change the “F” in the graph - that event still happened, but it does indicate that Evan was able to retake the test to get a “C”, and it is this value that ends up determining his total grade for the class.

### The Missing Link

Note something that may not be obvious - SHACL rules do not currently work with the focus nodes of a node shape. This is perhaps not that surprising - the SHACL rules spec is considerably less developed than the SHACL validation specification. However, it is nonetheless a curious omission, given the utility of iterative shape generators.

The following is speculation on my part on how the use of focus nodes could be integrated into the SRL notation and the shrl: namespace, representing the human authorable and machine specific version of the specification. It is NOT canonical, and is only an exercise in what SHAPES might look like with iterated focus nodes:

The rules engine needs a way to say “for each node that shape `S` targets, bind it to variable `?x`.” This is currently only expressible by duplicating the targeting logic as triple patterns in the rule body — brittle, redundant with the shape definition, and invisible to any change in the shape’s targeting.

Three integration points need to be defined: abstract syntax, grammar, and evaluation semantics.

---

### Abstract Syntax Addition

The spec would need a new rule body element type alongside `triple pattern`, `condition expression`, `negation element`, and `assignment`:

```
focus node element
:   A focus node element is a rule body element that binds a variable
    to the focus node set of a named sh:NodeShape evaluated against
    the current evaluation graph.
    Focus node elements appear in the body of a rule.
    A focus node element consists of:
      - a shape IRI (an IRI identifying a sh:NodeShape in the shapes graph)
      - a variable (the binding variable for each focus node)
```

The rule body element definition would be extended:

```
rule body element
:   A rule body element is any element that can appear in a rule body:
    a triple pattern,
    a condition expression,
    a negation element,
    an assignment,
    an aggregation element,
    or a focus node element.      ← NEW
```

---

### Grammar Addition

The cleanest syntax reuses the `FOCUS` keyword, which is not currently reserved. Two forms are useful — a simple binding and an inline shape reference:

```
[17]  BodyNotTriples  ::=  Filter | Negation | Assignment | FocusNodes

[NEW] FocusNodes      ::=  FocusNodesBound | FocusNodesInline

# Form A: named shape — bind focus nodes of a known shape IRI
[NEW] FocusNodesBound ::=  'FOCUS' Var 'IN' iri

# Form B: inline shape — define targeting criteria inline
[NEW] FocusNodesInline ::=  'FOCUS' Var 'MATCHING' TriplesTemplateBlock
```

**Form A** — named shape reference:

sparql

```
RULE { ?student ex:needsRemediation ex:Remediation }
WHERE {
    FOCUS ?student IN ex:CunninghamStudentShape
    ?student ex:shakespeareGrade "F" .
    NOT { ?student ex:needsRemediation ex:Remediation }
}
```

This binds `?student` to each node in the focus node set of `ex:CunninghamStudentShape` as evaluated against the current evaluation graph.

**Form B** — inline targeting:

sparql

````
RULE { ?student ex:needsRemediation ex:Remediation }
WHERE {
    FOCUS ?student MATCHING {
        sh:targetClass ex:Student ;
        sh:property [ sh:path ex:enrolledIn ; sh:hasValue ex:CunninghamSophomoreEnglish ]
    }
    ?student ex:shakespeareGrade "F" .
}
```

Form B is more expressive but introduces a SHACL mini-language inside a rule body, which has implementation complexity implications. Form A is the safer starting point for the FPWD.

---

## 3. Well-formedness Conditions

Two additions to the existing well-formedness rules:
```
- The variable of a focus node element at position i of a rule body
  must not occur in any triple pattern at position j where j < i.
  (i.e. it is introduced by the focus node element, not pre-bound.)

- The shape IRI of a focus node element must identify a well-formed
  sh:NodeShape in the shapes graph. It is an error if the IRI
  resolves to no shape or to a non-NodeShape resource.
```

The second condition requires the rules engine to have access to a shapes graph — which leads directly to the next point.

---

## 4. Evaluation Algorithm Changes

The current algorithm signature:
```
Inputs:  data graph G (base graph), rule set RS
Output:  inferred graph GI
```

Must become:
```
Inputs:  data graph G (base graph), rule set RS, shapes graph SG
Output:  inferred graph GI
```

The shapes graph `SG` is read-only during rule evaluation — rules cannot modify it, and inferred triples are never written to it.

The rule body evaluation pseudocode gains a new branch:
```
# Evaluate rule body (extended)

for each rule element rElt in B:

    if rElt is a triple pattern TP:
        # ... existing logic unchanged ...

    if rElt is a condition expression F:
        # ... existing logic unchanged ...

    if rElt is an assignment(V, expr):
        # ... existing logic unchanged ...

    if rElt is a focus node element(V, shapeIRI):    ← NEW
        SEQ1 = {}
        # Evaluate sh:targetClass, sh:targetNode, sh:targetSubjectsOf,
        # sh:targetObjectsOf, sh:target (node expressions) against GI
        # using the shapes graph SG to resolve shapeIRI
        let FN = evalFocusNodes(shapeIRI, GI, SG)
        for each focusNode f in FN:
            let μ_f = { V → f }          # single-variable solution
            for each μ in SEQ:
                if compatible(μ_f, μ):
                    add merge(μ_f, μ) to SEQ1
        SEQ = SEQ1
```

Where `evalFocusNodes(shapeIRI, G, SG)` is defined as:
```
evalFocusNodes(shapeIRI, G, SG):
    let shape = lookup(shapeIRI, SG)
    let FN = {}

    for each sh:targetClass C of shape:
        FN ∪= { n | (n, rdf:type, C) ∈ G }
        FN ∪= { n | ∃ C' : (C', rdfs:subClassOf*, C) ∧ (n, rdf:type, C') ∈ G }

    for each sh:targetNode N of shape:
        if N is an IRI or literal: FN ∪= { N }
        if N is a node expression:  FN ∪= evalNodeExpr(N, G)   # SHACL 1.2 Node Expr

    for each sh:targetSubjectsOf P of shape:
        FN ∪= { n | ∃ o : (n, P, o) ∈ G }

    for each sh:targetObjectsOf P of shape:
        FN ∪= { n | ∃ s : (s, P, n) ∈ G }

    for each sh:target T of shape:
        FN ∪= evalSPARQLTarget(T, G)

    return FN
```

This is exactly the SHACL Core focus node algorithm — no new semantics, just invoked from the rules evaluation layer.

---

## 5. Stratification Impact

Focus node elements have a dependency relationship that the stratification algorithm must account for. A rule containing `FOCUS ?x IN ex:MyShape` depends on the focus node set of `ex:MyShape`, which in turn depends on any rules that produce triples consumed by `ex:MyShape`'s targeting mechanism.

The stratification layer of a rule containing a focus node element must be:
```
max(
    layer of all other rule body elements,
    layer of all rules whose heads could add or remove nodes from
    the focus node set of the referenced shape
)
````

In practice this means: if a rule `R1` fires `FOCUS ?x IN ex:MyShape`, and another rule `R2` produces `rdf:type` triples for the class targeted by `ex:MyShape`, then `R1` must be in a higher or equal stratum to `R2`. This ensures `R1` sees the complete focus node set including `R2`‘s contributions.

---

### Interaction with Node Expressions

Since SHACL 1.2 Node Expressions (`shnex:instancesOf`, `shnex:filterShape` etc.) are valid values of `sh:targetNode`, a `FOCUS` element automatically gains the ability to target dynamically computed node sets — including filtered sets, intersections, and SPARQL-computed targets — without any additional grammar. The expressiveness of the Node Expressions spec is inherited for free.

sparql

````
# ex:EstonianCompanyShape uses shnex:instancesOf + shnex:filterShape
# (from our earlier example). The FOCUS element below targets the
# same dynamically computed set without repeating the filter logic.

RULE { ?company ex:vatStatus ex:EURegistered }
WHERE {
    FOCUS ?company IN ex:EstonianCompanyShape
    NOT { ?company ex:vatStatus ex:EURegistered }
}
```

---

## 7. Negation Interaction

The negation element `NOT { }` can apply to a focus node element directly, giving "nodes NOT in the focus set of shape S":
```
[19]  Negation  ::=  'NOT' '{' BodyBasic '}'
                   | 'NOT' FocusNodes         ← extension
````

sparql

```
RULE { ?x ex:uncategorised true }
WHERE {
    ?x rdf:type ex:Company .
    NOT FOCUS ?x IN ex:CategorisedCompanyShape
}
```

---

### Complete Example Against the Cunningham Scenario

With the extension, the two school rules simplify to:

sparql

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex:  <http://example.com/school#>

# ex:CunninghamStudentShape is already declared as:
#   sh:targetClass ex:Student ;
#   sh:property [ sh:path ex:enrolledIn ;
#                 sh:hasValue ex:CunninghamSophomoreEnglish ]
# The rule body does not repeat this — it delegates to the shape.

RULE {
    ?student ex:goodCitation ex:ShakespeareMidtermCitation
        ~ ?citationEvent {|
            a ex:CitationEvent ; ex:when ?time ;
        |}
}
WHERE {
    FOCUS ?student IN ex:CunninghamStudentShape
    ?student ex:shakespeareGrade "A" .
    NOT { ?student ex:goodCitation ex:ShakespeareMidtermCitation }
    BIND(NOW() AS ?time)
    BIND(IRI(CONCAT(STR(ex:ShakespeareMidtermCitation),'-',STRUUID())) AS ?citationEvent)
}

RULE {
    ?student ex:needsRemediation ex:ShakespeareMidtermRemediation
        ~ ?remediationEvent {|
            a ex:RemediationEvent ; ex:when ?time ;
        |}
}
WHERE {
    FOCUS ?student IN ex:CunninghamStudentShape
    ?student ex:shakespeareGrade "F" .
    NOT { ?student ex:needsRemediation ex:ShakespeareMidtermRemediation }
    BIND(NOW() AS ?time)
    BIND(IRI(CONCAT(STR(ex:ShakespeareMidtermRemediation),'-',STRUUID())) AS ?remediationEvent)
}
```

The enrollment constraint is expressed once in the shape and referenced twice in the rules. If the class or enrollment predicate changes, only the shape needs updating.

---

## Summary of Changes to the Spec

[

![](https://substackcdn.com/image/fetch/$s_!5ZZC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbb40c08-b8e6-452a-b982-9a53ebc9f5b0_763x449.png)



](https://substackcdn.com/image/fetch/$s_!5ZZC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbb40c08-b8e6-452a-b982-9a53ebc9f5b0_763x449.png)

---

## New Vocabulary Additions to `shrl:`

Three new terms are needed in the `shrl:` namespace:

turtle

````
PREFIX shrl: <http://www.w3.org/ns/shacl-rules#>
PREFIX sh:   <http://www.w3.org/ns/shacl#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>

# ── shrl:FocusNodeElement ────────────────────────────────────────────────────
# The class of focus node body elements.
# A blank node of this type in shrl:body binds a variable to the
# focus node set of a named or inline shape.

shrl:FocusNodeElement
    a owl:Class ;
    rdfs:label "Focus Node Element" ;
    rdfs:comment """A rule body element that binds a variable to the focus
                    node set of a sh:NodeShape evaluated against the
                    evaluation graph.""" ;
    rdfs:subClassOf shrl:RuleBodyElement .

# ── shrl:focusShape ──────────────────────────────────────────────────────────
# The KEY PARAMETER of a FocusNodeElement.
# Value is either:
#   • an IRI identifying a named sh:NodeShape in the shapes graph, or
#   • a blank node carrying sh:targetClass / sh:targetNode etc.
#     (inline shape definition — equivalent to SRL Form B)

shrl:focusShape
    a owl:ObjectProperty ;
    rdfs:label "focus shape" ;
    rdfs:comment """The sh:NodeShape whose focus node set is computed.
                    This is the key parameter of shrl:FocusNodeElement.""" ;
    rdfs:domain shrl:FocusNodeElement ;
    rdfs:range  sh:NodeShape .

# ── shrl:focusVar ────────────────────────────────────────────────────────────
# The variable that receives each focus node as a binding.
# Value must be a shrl:var blank node (consistent with existing
# shrl:subject / shrl:object variable pattern).

shrl:focusVar
    a owl:ObjectProperty ;
    rdfs:label "focus variable" ;
    rdfs:comment """The variable bound to each node in the focus node set.""" ;
    rdfs:domain shrl:FocusNodeElement .
```

---

## Pattern: Named Shape Reference

The SRL form:
```
FOCUS ?student IN ex:CunninghamStudentShape
````

Becomes in `shrl:`

````
[
    a shrl:FocusNodeElement ;
    shrl:focusShape ex:CunninghamStudentShape ;
    shrl:focusVar   [ shrl:var "student" ]
]
```

---

## Pattern: Inline Shape Definition

The SRL Form B:
```
FOCUS ?student MATCHING {
    sh:targetClass ex:Student ;
    sh:property [ sh:path ex:enrolledIn ;
                  sh:hasValue ex:CunninghamSophomoreEnglish ]
}
````

Becomes:

turtle

````
[
    a shrl:FocusNodeElement ;
    shrl:focusShape [
        sh:targetClass ex:Student ;
        sh:property [
            sh:path     ex:enrolledIn ;
            sh:hasValue ex:CunninghamSophomoreEnglish ;
        ]
    ] ;
    shrl:focusVar [ shrl:var "student" ]
]
```

The value of `shrl:focusShape` is a blank node that carries standard SHACL targeting vocabulary. No new predicates are needed for the inline form — the existing `sh:targetClass`, `sh:property`, `sh:targetNode` etc. are used directly.

---

## Pattern: Negated Focus

The SRL extension:
```
NOT FOCUS ?x IN ex:CategorisedCompanyShape
````

Extends the existing `shrl:not` pattern. Currently `shrl:not` wraps a list of triple patterns. With the extension it also accepts a `shrl:FocusNodeElement`:

```
[
    shrl:not [
        a shrl:FocusNodeElement ;
        shrl:focusShape ex:CategorisedCompanyShape ;
        shrl:focusVar   [ shrl:var "x" ]
    ]
]
```

---

## Complete Example: Cunningham Rules in Full `shrl:` Syntax

```
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sh:    <http://www.w3.org/ns/shacl#>
PREFIX shrl:  <http://www.w3.org/ns/shacl-rules#>
PREFIX sparql: <http://www.w3.org/ns/sparql#>
PREFIX ex:    <http://example.com/school#>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

# ─────────────────────────────────────────────────────────────────────────────
# Shape definition (in the shapes graph)
# The rules reference this by IRI — it does not need to be repeated.
# ─────────────────────────────────────────────────────────────────────────────

ex:CunninghamStudentShape
    a sh:NodeShape ;
    sh:targetClass ex:Student ;
    sh:property [
        sh:path     ex:enrolledIn ;
        sh:hasValue ex:CunninghamSophomoreEnglish ;
    ] .

# ─────────────────────────────────────────────────────────────────────────────
# Rule Set
# ─────────────────────────────────────────────────────────────────────────────

ex:CunninghamRuleSet
    a shrl:RuleSet ;
    shrl:ruleSet (

        # ── Rule 1: Good citation for A grade ────────────────────────────────

        [
            a shrl:Rule ;

            shrl:head (
                # ?student ex:goodCitation ex:ShakespeareMidtermCitation
                #     ~ ?citationEvent {| a ex:CitationEvent ; ex:when ?time |}
                [
                    shrl:subject   [ shrl:var "student" ] ;
                    shrl:predicate ex:goodCitation ;
                    shrl:object    ex:ShakespeareMidtermCitation ;
                    shrl:reifier   [ shrl:var "citationEvent" ] ;
                    shrl:annotation (
                        [ shrl:predicate rdf:type ;    shrl:object ex:CitationEvent ]
                        [ shrl:predicate ex:when ;     shrl:object [ shrl:var "time" ] ]
                    )
                ]
            ) ;

            shrl:body (

                # FOCUS ?student IN ex:CunninghamStudentShape
                [
                    a shrl:FocusNodeElement ;
                    shrl:focusShape ex:CunninghamStudentShape ;
                    shrl:focusVar   [ shrl:var "student" ]
                ]

                # ?student ex:shakespeareGrade "A"
                [
                    shrl:subject   [ shrl:var "student" ] ;
                    shrl:predicate ex:shakespeareGrade ;
                    shrl:object    "A"
                ]

                # NOT { ?student ex:goodCitation ex:ShakespeareMidtermCitation }
                [
                    shrl:not (
                        [
                            shrl:subject   [ shrl:var "student" ] ;
                            shrl:predicate ex:goodCitation ;
                            shrl:object    ex:ShakespeareMidtermCitation
                        ]
                    )
                ]

                # BIND(NOW() AS ?time)
                [
                    shrl:assign [ shrl:var "time" ] ;
                    shrl:expr   [ sparql:now () ]
                ]

                # BIND(IRI(CONCAT(STR(ex:ShakespeareMidtermCitation),'-',STRUUID())) AS ?citationEvent)
                [
                    shrl:assign [ shrl:var "citationEvent" ] ;
                    shrl:expr   [
                        sparql:iri (
                            [
                                sparql:concat (
                                    [ sparql:str ( ex:ShakespeareMidtermCitation ) ]
                                    "-"
                                    [ sparql:struuid () ]
                                )
                            ]
                        )
                    ]
                ]
            ) ;
        ]

        # ── Rule 2: Remediation flag for F grade ─────────────────────────────

        [
            a shrl:Rule ;

            shrl:head (
                [
                    shrl:subject   [ shrl:var "student" ] ;
                    shrl:predicate ex:needsRemediation ;
                    shrl:object    ex:ShakespeareMidtermRemediation ;
                    shrl:reifier   [ shrl:var "remediationEvent" ] ;
                    shrl:annotation (
                        [ shrl:predicate rdf:type ;  shrl:object ex:RemediationEvent ]
                        [ shrl:predicate ex:when ;   shrl:object [ shrl:var "time" ] ]
                    )
                ]
            ) ;

            shrl:body (

                # FOCUS ?student IN ex:CunninghamStudentShape
                [
                    a shrl:FocusNodeElement ;
                    shrl:focusShape ex:CunninghamStudentShape ;
                    shrl:focusVar   [ shrl:var "student" ]
                ]

                # ?student ex:shakespeareGrade "F"
                [
                    shrl:subject   [ shrl:var "student" ] ;
                    shrl:predicate ex:shakespeareGrade ;
                    shrl:object    "F"
                ]

                # NOT { ?student ex:needsRemediation ex:ShakespeareMidtermRemediation }
                [
                    shrl:not (
                        [
                            shrl:subject   [ shrl:var "student" ] ;
                            shrl:predicate ex:needsRemediation ;
                            shrl:object    ex:ShakespeareMidtermRemediation
                        ]
                    )
                ]

                # BIND(NOW() AS ?time)
                [
                    shrl:assign [ shrl:var "time" ] ;
                    shrl:expr   [ sparql:now () ]
                ]

                # BIND(IRI(CONCAT(...)) AS ?remediationEvent)
                [
                    shrl:assign [ shrl:var "remediationEvent" ] ;
                    shrl:expr   [
                        sparql:iri (
                            [
                                sparql:concat (
                                    [ sparql:str ( ex:ShakespeareMidtermRemediation ) ]
                                    "-"
                                    [ sparql:struuid () ]
                                )
                            ]
                        )
                    ]
                ]
            ) ;
        ]

    ) .
```

---

## Two Points on the Reification Head Serialisation

The `shrl:` vocabulary as currently specified has no terms for `shrl:reifier` or `shrl:annotation` — those constructs exist in SRL via the grammar productions `Reifier` [27] and `AnnotationBlock` [61] but have no defined RDF syntax equivalent yet. The spec notes this gap implicitly when it says the RDF syntax mapping is incomplete. The two terms above are the natural extension:

turtle

```
shrl:reifier
    a owl:ObjectProperty ;
    rdfs:comment """The reifier variable or IRI for a triple template
                    in a rule head. Corresponds to the ~ VarOrReifierId
                    grammar production.""" .

shrl:annotation
    a owl:ObjectProperty ;
    rdfs:comment """An RDF list of subject-less predicate/object pairs
                    forming the {| |} annotation block on a head triple
                    template.""" .
```

These follow directly from the existing `shrl:subject` / `shrl:predicate` / `shrl:object` pattern — annotation entries are the same structure minus the subject, since the subject is the reifier node itself.

---

## Structural Comparison

[

![](https://substackcdn.com/image/fetch/$s_!579i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F955c9f85-d930-4baa-bc1e-afc098ac3f27_751x424.png)



](https://substackcdn.com/image/fetch/$s_!579i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F955c9f85-d930-4baa-bc1e-afc098ac3f27_751x424.png)

The `shrl:` serialisation is significantly more verbose than SRL for the same semantics — which is expected, since it is the machine-readable form intended for tooling rather than human authoring. The SRL text file is the authoring surface; the `shrl:` Turtle is what processors consume after parsing.

## Conclusion

There are several key takeaways here.

- **Node shapes** (including reification shapes) serve to identify the set of focus nodes to be acted upon by validation, and potentially by rules.
    
- **Constraint shapes**, including both property shapes and SPARQL shapes, constrain node shapes in certain ways, and in the case of property shapes, determine behaviour based upon paths.
    
- **Node Expressions** make it possible to compute values that are not explicitly stated for purposes of comparison (I didn’t cover these in detail here, but will do so soon). These are roughly equivalent to the SPARQL bind expression
    
- **SHACL rules**, at least in theory, perform reasoning on specific datasets (including the enumerated focus nodes). In point of fact, we’re not quite there yet, and it can be argued that SHACL rules are fired whenever a containing node shape is processed. I expect this will become clarified over the next year, because with it, SHACL effectively creates the equivalent of a reasoner.
    
- **State Machines.** SHACL enables a state machine on a graph. I’ll be exploring this contention in much more detail in a subsequent post, but I think it’s one of the more exciting developments in the RDF world.
    

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!TGHy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23b39742-411c-4a26-9583-dd203787981c_2048x2048.jpeg)



](https://substackcdn.com/image/fetch/$s_!TGHy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23b39742-411c-4a26-9583-dd203787981c_2048x2048.jpeg)

I had a reader tell me that they dubbed my eponymous character Professor Shacl, the Ontologist. Perhaps …

[Kurt Cagle](https://linkedin.com/in/kurtcagle)  
[The Ontologist](https://ontologist.substack.com/)


