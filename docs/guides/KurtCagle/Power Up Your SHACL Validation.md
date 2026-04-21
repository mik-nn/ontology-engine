---
type: article
title: Без названия
source: https://substack.com/@kurtcagle/p-190400612
created: 2026-03-09
tags:
  - article
---

# Power Up Your SHACL Validation]
## Using SHACL 1.2 New Features To Make Validation Far More Useful

Источник: https://substack.com/@kurtcagle/p-190400612

---

Mar 09, 2026

---

[

![](https://substackcdn.com/image/fetch/$s_!FBEA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20a98943-e3d9-4d4f-82a3-79349b38e54f_5376x3072.jpeg)



](https://substackcdn.com/image/fetch/$s_!FBEA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20a98943-e3d9-4d4f-82a3-79349b38e54f_5376x3072.jpeg)

SHACL is a validation language. When a validation succeeds, there’s no real metadata that needs to be passed - the node in question meets all existing criteria. When it fails, you want the results to be as informative as possible, because in general, the value of validation is figuring out why something went wrong.

SHACL 1.2 expands upon these options, making it possible to customise message output and add additional metadata to the report message in Turtle, making the content actionable.

## Validation Tools

There are several tools for performing SHACL Validation - among them, Python pySHACL, Jena’s SHACL CLI, and Top Quadrant’s shaclvalidate tool. It’s worth noting that there’s a meaningful distinction between the **Jena** `shacl` **CLI** and the **TopQuadrant** `shaclvalidate` tool (which is Jena-based but a separate distribution). Here’s the breakdown:

---

### pySHACL

#### CLI — `-f` flag

The `-f` / `--format` flag controls output format and accepts `human`, `table`, `turtle`, `xml`, `json-ld`, `nt`, or `n3`. The default is `human`.

```
# Turtle report to stdout
pyshacl -s shapes.ttl -f turtle data.ttl

# Turtle report written to file
pyshacl -s shapes.ttl -f turtle -o report.ttl data.ttl

# With advanced features enabled (needed for sh:resultAnnotation etc.)
pyshacl -s shapes.ttl -a -f turtle -o report.ttl data.ttl
```

Exit codes are meaningful for pipeline use: `0` = conformant, `1` = non-conformant, `2` = RuntimeError, `3` = feature not implemented.

### Python API — `serialize_report_graph`

When calling `pyshacl.validate()` directly, pass `serialize_report_graph="ttl"` to get the report graph back as a serialised Turtle string rather than an rdflib Graph object.

```
from pyshacl import validate

conforms, report_graph, report_text = validate(
    data_graph,
    shacl_graph=shapes_graph,
    data_graph_format="turtle",
    shacl_graph_format="turtle",
    advanced=True,          # required for sh:resultAnnotation
    inference="rdfs",
    serialize_report_graph="ttl",
)

# report_graph is now a Turtle string, not an rdflib.Graph
print(report_graph)
```

Without `serialize_report_graph`, `report_graph` is an `rdflib.Graph` you can serialise yourself:

```
conforms, report_graph, report_text = validate(
    data_graph,
    shacl_graph=shapes_graph,
    advanced=True,
)
# Serialise manually — gives you full control over prefixes etc.
turtle_out = report_graph.serialize(format="turtle")
```

---

### Jena `shacl` CLI

Jena’s `shacl` command takes a sub-command argument; the validate sub-command writes out results in text (`t`), compact (`c`), or RDF (`r`) formats, with multiple formats possible as a comma-separated list, and `all` outputting all three.

```
# RDF output (Turtle by default for Jena's RDF writer)
shacl validate --shapes shapes.ttl --data data.ttl --output r

# All three formats at once
shacl validate --shapes shapes.ttl --data data.ttl --output t,r

# Shapes and data can be the same file
shacl validate --data combined.ttl --output r
```

The `r` format produces the `sh:ValidationReport` as RDF — Jena will serialise it as Turtle. If you need a specific serialisation, pipe through `riot`:

```
shacl validate --shapes shapes.ttl --data data.ttl --output r \
  | riot --syntax=turtle --output=turtle -
```

---

### TopQuadrant `shaclvalidate` (separate distribution)

The TopQuadrant CLI tool (`shaclvalidate.sh` / `shaclvalidate.bat`) takes `-datafile` and `-shapesfile` parameters and always outputs in Turtle — it only accepts Turtle input and produces Turtle output, with no format flag.

```
shaclvalidate.sh -datafile data.ttl -shapesfile shapes.ttl > report.ttl
```

This is the more constrained of the two Jena-family tools but also the simplest to pipe into downstream processing.

---

### For PySHACL

One thing worth flagging with pySHACL: `advanced=True` (or `-a` on the CLI) is **required** for `sh:resultAnnotation` to be processed — without it, the annotations are silently ignored. The flag also enables `sh:SPARQLConstraint` evaluation, `sh:if`/`sh:then`/`sh:else`, and node expressions, so it’s effectively mandatory for anything beyond SHACL Core.

For a pipeline that passes the Turtle report to a downstream consumer, the cleanest pattern is:

```
pyshacl -s shapes.ttl -a -f turtle -o /tmp/report.ttl data.ttl
echo "Exit: $?"   # 0=conformant, 1=violations present
```

That gives you a machine-readable report that carries all `sh:resultAnnotation` triples, parseable by any RDF stack.

---

## The Reporting Stack in SHACL 1.2

A `sh:ValidationResult` carries these core properties out of the box:

[

![](https://substackcdn.com/image/fetch/$s_!rM6V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e265960-a42e-419a-9c8b-8d976d59887b_766x443.png)



](https://substackcdn.com/image/fetch/$s_!rM6V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e265960-a42e-419a-9c8b-8d976d59887b_766x443.png)

Property Description `sh:focusNode` The node that failed `sh:resultPath` The property path that failed `sh:value` The offending value `sh:sourceShape` The shape that triggered it `sh:sourceConstraintComponent` e.g. `sh:MinCountConstraintComponent` `sh:resultSeverity` `sh:Violation`, `sh:Warning`, `sh:Info` `sh:message` Human-readable text

The way to push _additional_ metadata into a result is `sh:resultAnnotation`, a SHACL 1.2 / Advanced Features mechanism.

---

## 1. Basic Severity and Custom Messages

```
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix ex:   <http://example.org/ns#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;

    sh:property [
        sh:path ex:email ;
        sh:minCount 1 ;
        sh:severity sh:Violation ;
        sh:message "A Person must have at least one email address."@en ;
        sh:message "Une Personne doit avoir au moins une adresse e-mail."@fr ;
    ] ;

    sh:property [
        sh:path ex:birthDate ;
        sh:datatype xsd:date ;
        sh:severity sh:Warning ;
        sh:message "For {$this}, birthDate should be xsd:date; value {$value} has wrong datatype."@en ;
    ] .
```

> `sh:message` supports `{$value}`, `{$path}`, and `{$this}` substitution tokens — these are resolved at validation time.

For instance, if you had the following Turtle:

```
ex:JaneDoe a ex:Person ;
     ex:birthDate 1996 ; #Birthdate is an integer.
     . 
```

The resulting error messages would look as follows:

```
@prefix sh:    <http://www.w3.org/ns/shacl#> .
@prefix ex:    <http://example.org/ns#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

[] a sh:ValidationReport ;
    sh:conforms false ;

    sh:result [
        a sh:ValidationResult ;
        sh:resultSeverity        sh:Violation ;
        sh:focusNode             ex:JaneDoe ;
        sh:resultPath            ex:email ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:sourceShape [
            sh:path     ex:email ;
            sh:minCount 1 ;
        ] ;
        sh:resultMessage "A Person must have at least one email address."@en ;
        sh:resultMessage "Une Personne doit avoir au moins une adresse e-mail."@fr ;
    ] ;

    sh:result [
        a sh:ValidationResult ;
        sh:resultSeverity        sh:Warning ;
        sh:focusNode             ex:JaneDoe ;
        sh:resultPath            ex:birthDate ;
        sh:value                 1996 ;   # bare integer = xsd:integer
        sh:sourceConstraintComponent sh:DatatypeConstraintComponent ;
        sh:sourceShape [
            sh:path     ex:birthDate ;
            sh:datatype xsd:date ;
        ] ;
        sh:resultMessage "For <http://example.org/ns#JaneDoe>, birthDate should be xsd:date; value 1996 has wrong datatype."@en ;
    ] .
```

The first message result indicates that Jane Doe doesn’t have an email as part of her message. This is a sh:Violation, as indicated by the sh:severity attribute.

The second message result is a warning, and indicates that the datatype for the ex:birthDate is not an xs:date value. It could be a string or a number, the latter of which is shown. This still may be processable (which is why it’s treated as a warning and not a violation) but it’s at least been reported.

The result message here uses both {$this} and {$value} to pass more precise information to the message text, in this case indicating the reference node (ex:JaneDoe) and the value (1996).

## Customising Severity

Yes — the three built-in severities form a suggested hierarchy, not a closed enumeration. The SHACL spec defines `sh:severity` as an open IRI-valued property.

The spec defines `sh:resultSeverity` with a range of `sh:Severity`, and the three built-in individuals (`sh:Violation`, `sh:Warning`, `sh:Info`) are instances of that class. But nothing prevents you from minting your own:

```
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix ex:   <http://example.org/ns#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

# Declare custom severity individuals
ex:Critical  a sh:Severity ;
    sh:message "Critical: immediate remediation required." .

ex:Blocker   a sh:Severity ;
    sh:message "Blocker: pipeline cannot proceed." .

ex:Advisory  a sh:Severity .

ex:ProductShape
    a sh:NodeShape ;
    sh:targetClass ex:Product ;

    sh:property [
        sh:path ex:regulatoryId ;
        sh:minCount 1 ;
        sh:severity ex:Critical ;
        sh:message "Products entering regulated markets MUST have a regulatory ID."@en ;
    ] ;

    sh:property [
        sh:path ex:description ;
        sh:minCount 1 ;
        sh:severity ex:Advisory ;
        sh:message "A description is strongly recommended for catalogue quality."@en ;
    ] .
```

The resulting report carries your IRI verbatim:

```
sh:result [
    a sh:ValidationResult ;
    sh:resultSeverity        ex:Critical ;
    sh:focusNode             ex:product99 ;
    sh:resultPath            ex:regulatoryId ;
    sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
    sh:resultMessage "Products entering regulated markets MUST have a regulatory ID."@en ;
] .
```

---

### The Conformance Question

This is the important practical caveat: **validators only understand** `sh:Violation` **when determining** `sh:conforms`. The spec says:

> A graph is conformant if and only if the validation report contains no results with `sh:resultSeverity sh:Violation`.

`sh:Warning` and `sh:Info` don’t affect `sh:conforms` either in strict spec terms — that’s a validator option, not a spec requirement. Custom severities are in the same boat: they pass straight through to the report, but the validator won’t know how to treat `ex:Critical` as worse than `sh:Violation`.

### Practical mitigation

If you want severity ordering to drive pipeline decisions, query the report yourself:

```
PREFIX sh:  <http://www.w3.org/ns/shacl#>
PREFIX ex:  <http://example.org/ns#>

SELECT ?node ?path ?message ?severity
WHERE {
    ?report a sh:ValidationReport ;
            sh:result ?result .
    ?result sh:focusNode  ?node ;
            sh:resultPath ?path ;
            sh:resultSeverity ?severity .
    OPTIONAL { ?result sh:resultMessage ?message }
}
ORDER BY (
    IF(?severity = ex:Critical,  1,
    IF(?severity = sh:Violation, 2,
    IF(?severity = ex:Blocker,   3,
    IF(?severity = sh:Warning,   4,
    IF(?severity = ex:Advisory,  5,
    IF(?severity = sh:Info,      6, 7)))))) )
```

Or model the ordering explicitly in your shapes graph using OWL or SKOS:

```
ex:SeverityScheme a skos:ConceptScheme ;
    skos:hasTopConcept ex:Critical .

ex:Critical  a sh:Severity, skos:Concept ;
    skos:broader sh:Violation ;
    ex:severityRank 1 .

ex:Blocker   a sh:Severity, skos:Concept ;
    skos:broader sh:Violation ;
    ex:severityRank 2 .

sh:Violation  a sh:Severity, skos:Concept ;
    ex:severityRank 3 .

sh:Warning    a sh:Severity, skos:Concept ;
    skos:narrower ex:Advisory ;
    ex:severityRank 4 .

ex:Advisory  a sh:Severity, skos:Concept ;
    ex:severityRank 5 .

sh:Info       a sh:Severity, skos:Concept ;
    ex:severityRank 6 .
```

That lets your report-processing layer do a simple `ex:severityRank` lookup rather than hardcoding IRI comparisons.

Each tool handles this slightly differently:

---

[

![](https://substackcdn.com/image/fetch/$s_!m2WD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F305c6092-3f06-445b-a4b8-561a76ac7244_740x318.png)



](https://substackcdn.com/image/fetch/$s_!m2WD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F305c6092-3f06-445b-a4b8-561a76ac7244_740x318.png)

The consistent story across all three: custom severities are faithfully recorded in the report but don’t change validator exit codes or `sh:conforms`. Your downstream pipeline code owns the interpretation.

---

> Custom severities are a clean way to align SHACL reporting with enterprise change-management vocabulary (e.g. `itil:P1`, `ex:DataQualityWarning`, `ex:AuditFlag`) without any loss of interoperability with the standard validators.

---

## 2. `sh:resultAnnotation` — Attaching Custom Metadata

`sh:ResultAnnotation` lets you bind arbitrary properties onto the `sh:ValidationResult` node. There are two flavours:

- `sh:annotationValue` — a fixed RDF term
    
- `sh:annotationVarName` — a SPARQL variable name (only meaningful inside `sh:SPARQLConstraint`)
    

```
@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix ex:     <http://example.org/ns#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .

ex:ProductShape
    a sh:NodeShape ;
    sh:targetClass ex:Product ;

    sh:property [
        sh:path ex:price ;
        sh:minInclusive 0.0 ;
        sh:datatype xsd:decimal ;
        sh:severity sh:Violation ;
        sh:message "Price must be a non-negative decimal."@en ;

        # Fixed annotations — stamped on every result from this constraint
        sh:resultAnnotation [
            sh:annotationProperty ex:errorCode ;
            sh:annotationValue ex:ERR_PRICE_NEGATIVE ;
        ] ;
        sh:resultAnnotation [
            sh:annotationProperty dcterms:source ;
            sh:annotationValue <https://example.org/rules/pricing-policy-v2> ;
        ] ;
        sh:resultAnnotation [
            sh:annotationProperty ex:remediation ;
            sh:annotationValue "Set ex:price to a value >= 0.0"^^xsd:string ;
        ] ;
    ] .
```

The resulting `sh:ValidationResult` node will carry:

```
[] a sh:ValidationResult ;
    sh:focusNode ex:product42 ;
    sh:resultPath ex:price ;
    sh:value "-5.00"^^xsd:decimal ;
    sh:resultSeverity sh:Violation ;
    sh:message "Price must be a non-negative decimal." ;
    ex:errorCode ex:ERR_PRICE_NEGATIVE ;
    dcterms:source <https://example.org/rules/pricing-policy-v2> ;
    ex:remediation "Set ex:price to a value >= 0.0" .
 
```

This is an important capability to note: As with `sh:resultSeverity`, you can add specific error codes, annotate with specific indications tying validation errors to policy violations in your organisation, or add specific help information to help mitigation and remediation of the data (and more). This could also be a place to add in post-processing pipeline hooks that can be handled by external processes downstream.

### Passing More Comples Structures

One more point - you can also pass blank-node constructions here rather than just single IRIs or messages:

Good edge case to document. The `sh:annotationValue` property accepts any RDF term, including a blank node — but there’s a subtlety worth knowing upfront.

### The Subtlety

In standard Turtle, blank nodes in shapes are _structural_ — each `[]` creates a fresh blank node at parse time, shared across the graph. When used as `sh:annotationValue`, that same blank node gets stamped onto **every** result the constraint fires. That’s fine if the blank node is purely descriptive (a structured metadata record that’s the same for all failures), but it means all results share the **same** blank node identity — not copies of it.

---

### Example — Structured Remediation Record

```
@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix ex:     <http://example.org/ns#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

ex:InvoiceShape
    a sh:NodeShape ;
    sh:targetClass ex:Invoice ;

    sh:property [
        sh:path ex:totalAmount ;
        sh:minInclusive "0.00"^^xsd:decimal ;
        sh:datatype xsd:decimal ;
        sh:severity sh:Violation ;
        sh:message "Invoice total must be a non-negative decimal."@en ;

        sh:resultAnnotation [
            sh:annotationProperty ex:remediation ;
            sh:annotationValue [
                a ex:RemediationRecord ;
                ex:action      "Correct ex:totalAmount to a non-negative xsd:decimal value." ;
                ex:assignedTo  ex:DataStewardTeam ;
                ex:priority    ex:High ;
                ex:ruleRef     <https://example.org/rules/finance/INV-001> ;
                dcterms:created "2026-01-15"^^xsd:date ;
            ] ;
        ] ;
    ] .
```

The resulting `sh:ValidationResult` node looks like:

```
[] a sh:ValidationResult ;
    sh:resultSeverity   sh:Violation ;
    sh:focusNode        ex:invoice_42 ;
    sh:resultPath       ex:totalAmount ;
    sh:value            "-150.00"^^xsd:decimal ;
    sh:resultMessage    "Invoice total must be a non-negative decimal."@en ;
    ex:remediation [
        a ex:RemediationRecord ;
        ex:action     "Correct ex:totalAmount to a non-negative xsd:decimal value." ;
        ex:assignedTo ex:DataStewardTeam ;
        ex:priority   ex:High ;
        ex:ruleRef    <https://example.org/rules/finance/INV-001> ;
        dcterms:created "2026-01-15"^^xsd:date ;
    ] .
```

---

### The Shared Identity Problem in Practice

If five invoices fail this constraint, all five `sh:ValidationResult` nodes will point to the **same** blank node via `ex:remediation`. That’s fine for read-only metadata like a remediation template, but breaks down if you later want to annotate individual results differently (e.g. tracking per-result resolution status).

The clean fix when you need per-result blank node instances is to drop to `sh:SPARQLConstraint` with `sh:annotationVarName`, constructing the blank node equivalent via a SPARQL `BIND`:

```
ex:InvoiceShape
    a sh:NodeShape ;
    sh:targetClass ex:Invoice ;

    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:severity sh:Violation ;
        sh:message "Invoice total must be a non-negative decimal."@en ;

        sh:resultAnnotation [
            sh:annotationProperty ex:remediationAction ;
            sh:annotationVarName  "action" ;
        ] ;
        sh:resultAnnotation [
            sh:annotationProperty ex:assignedTo ;
            sh:annotationVarName  "assignee" ;
        ] ;

        sh:select """
            PREFIX ex:  <http://example.org/ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT $this ?action ?assignee
            WHERE {
                $this ex:totalAmount ?amt .
                FILTER (!datatype(?amt) = xsd:decimal || ?amt < 0)
                BIND("Correct ex:totalAmount to a non-negative xsd:decimal value." AS ?action)
                BIND(ex:DataStewardTeam AS ?assignee)
            }
        """ ;
    ] .
```

Here each result gets its own bindings — they happen to be the same values in this example, but you could vary them per focus node (e.g. routing to different `?assignee` based on `ex:department`).

> The blank-node-as-`sh:annotationValue` pattern is best suited to **static structured metadata** — rule provenance records, remediation templates, documentation bundles — where identity sharing across results is harmless or even desirable. The moment you need the annotation to vary per focus node, reach for `sh:SPARQLConstraint` with `sh:annotationVarName` instead.

## 3. SPARQL Constraints with Dynamic Annotations

The above example also shows where `sh:annotationVarName` becomes powerful — you can bind _data from the graph_ into the result:

```
ex:EmployeeShape
    a sh:NodeShape ;
    sh:targetClass ex:Employee ;

    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:severity sh:Violation ;
        sh:message "Employee {$this} is assigned to department {$deptLabel} but that department is inactive."@en ;

        sh:resultAnnotation [
            sh:annotationProperty ex:affectedDepartment ;
            sh:annotationVarName "dept" ;        # binds ?dept from SELECT
        ] ;
        sh:resultAnnotation [
            sh:annotationProperty ex:departmentLabel ;
            sh:annotationVarName "deptLabel" ;   # binds ?deptLabel from SELECT
        ] ;
        sh:resultAnnotation [
            sh:annotationProperty ex:ruleId ;
            sh:annotationValue ex:RULE_INACTIVE_DEPT ;
        ] ;

        sh:select """
            PREFIX ex: <http://example.org/ns#>
            SELECT $this ?dept ?deptLabel
            WHERE {
                $this ex:department ?dept .
                ?dept ex:status ex:Inactive .
                OPTIONAL { ?dept ex:label ?deptLabel }
            }
        """ ;
    ] .
```

The `?dept` and `?deptLabel` bindings from the SELECT are threaded directly into the result node. This shows a valid and invalid example and the accompanying message results in Turtle

### Sample Data

#### Valid — conformant employee

```
@prefix ex:  <http://example.org/ns#> .

ex:dept_engineering
    a ex:Department ;
    ex:status ex:Active ;
    ex:label "Engineering" .

ex:AliceSmith
    a ex:Employee ;
    ex:name "Alice Smith" ;
    ex:department ex:dept_engineering .
```

`ex:dept_engineering` has `ex:status ex:Active`, so the SPARQL SELECT returns no rows for `ex:AliceSmith` — no violation fires.

---

#### Invalid — two employees, two failure modes

```
@prefix ex:  <http://example.org/ns#> .

# Department with a label
ex:dept_legacy
    a ex:Department ;
    ex:status ex:Inactive ;
    ex:label "Legacy Systems" .

# Department without a label — exercises the OPTIONAL branch
ex:dept_dissolved
    a ex:Department ;
    ex:status ex:Inactive .

ex:BobJones
    a ex:Employee ;
    ex:name "Bob Jones" ;
    ex:department ex:dept_legacy .

ex:CarolWu
    a ex:Employee ;
    ex:name "Carol Wu" ;
    ex:department ex:dept_dissolved .
```

---

### Resulting `sh:ValidationReport` in Turtle

```
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix ex:  <http://example.org/ns#> .

[] a sh:ValidationReport ;
    sh:conforms false ;

    # --- Bob Jones: dept_legacy is inactive, label present ---
    sh:result [
        a sh:ValidationResult ;
        sh:resultSeverity            sh:Violation ;
        sh:focusNode                 ex:BobJones ;
        sh:sourceConstraintComponent sh:SPARQLConstraintComponent ;
        sh:sourceShape               ex:EmployeeShape ;

        # {$this} and {$deptLabel} interpolated into sh:resultMessage
        sh:resultMessage
            "Employee <http://example.org/ns#BobJones> is assigned to department Legacy Systems but that department is inactive."@en ;

        # sh:annotationVarName "dept" → bound to ?dept from SELECT
        ex:affectedDepartment  ex:dept_legacy ;

        # sh:annotationVarName "deptLabel" → bound to ?deptLabel from SELECT
        ex:departmentLabel     "Legacy Systems" ;

        # sh:annotationValue — fixed IRI, same on every result
        ex:ruleId              ex:RULE_INACTIVE_DEPT ;
    ] ;

    # --- Carol Wu: dept_dissolved is inactive, NO label (OPTIONAL unbound) ---
    sh:result [
        a sh:ValidationResult ;
        sh:resultSeverity            sh:Violation ;
        sh:focusNode                 ex:CarolWu ;
        sh:sourceConstraintComponent sh:SPARQLConstraintComponent ;
        sh:sourceShape               ex:EmployeeShape ;

        # {$deptLabel} is unbound — pySHACL leaves the token unreplaced
        sh:resultMessage
            "Employee <http://example.org/ns#CarolWu> is assigned to department {$deptLabel} but that department is inactive."@en ;

        ex:affectedDepartment  ex:dept_dissolved ;

        # ex:departmentLabel is absent — unbound OPTIONAL produces no triple
        # ex:ruleId still fires because it uses sh:annotationValue, not sh:annotationVarName
        ex:ruleId              ex:RULE_INACTIVE_DEPT ;
    ] .
```

---

### Points Worth Noting

`{$this}` **expansion** renders as the full angle-bracket IRI in pySHACL (`<http://example.org/ns#BobJones>`), not the prefixed form. If you want a clean label in the message, bind a `?name` variable in the SELECT and use `{$name}` instead.

**Unbound OPTIONAL and** `sh:annotationVarName` behave differently from each other when the variable is `NULL`:

- The message template token `{$deptLabel}` is **left unreplaced** — the literal string `{$deptLabel}` appears in the output. This is a strong argument for always providing a fallback in the SELECT:
    

```
BIND(COALESCE(?deptLabel, "(unlabelled)") AS ?deptLabel)
```

- The annotation triple `ex:departmentLabel` is simply **omitted** — no triple is emitted if the variable is unbound. This is actually clean behaviour for the report consumer; an absent property is unambiguous, whereas a placeholder string in a message is not.
    

`sh:annotationValue` **vs** `sh:annotationVarName` — the `ex:ruleId` annotation appears on _both_ results identically because it uses the fixed-value form. It’s immune to the OPTIONAL problem, which is why rule catalogue references, doc links, and error codes are better modelled with `sh:annotationValue` and per-focus-node data is better modelled with `sh:annotationVarName`.

`sh:sourceShape` points to `ex:EmployeeShape` here (the named shape) rather than the anonymous blank node of the constraint, because the SPARQLConstraint is embedded directly in a named shape. This makes the report more navigable than the blank-node case.

---

## 4. Conditional Reporting with `sh:if` / `sh:then` / `sh:else`

SHACL 1.2’s conditional shapes let you vary the severity and message based on context:

```
ex:ContractShape
    a sh:NodeShape ;
    sh:targetClass ex:Contract ;

    sh:property [
        sh:path ex:expiryDate ;
        sh:if [
            # Condition: contract is of type HighValue
            sh:property [
                sh:path ex:contractTier ;
                sh:hasValue ex:HighValue ; # This could also be sh:in with multiple values
             ]
        ] ;
        sh:then [
            sh:minCount 1 ;
            sh:severity sh:Violation ;
            sh:message "High-value contracts MUST have an expiry date."@en ;
            sh:resultAnnotation [
                sh:annotationProperty ex:escalateTo ;
                sh:annotationValue ex:LegalTeam ;
            ] ;
        ] ;
        sh:else [
            sh:minCount 0 ;
            sh:severity sh:Info ;
            sh:message "Standard contracts should consider setting an expiry date."@en ;
        ] ;
    ] .
```

The new if/then/else construct is actually one of my favourite features of SHACL 1.2 messaging. One client had a particularly thorny problem - for most of their corporate users, if a description wasn’t included (or was blank), this had no real impact, but for other users, the description had to be there. This could have been resolved with two distinct shapes, but with sh:if/sh:then/sh:else it becomes possible to just simply change the severity from sh:Warning to sh:Violation. Warnings are considered compliant and pass validation, violations are not compliant and fail validation.

---

## 5. Nested Detail with `sh:detail`

For complex shapes-within-shapes, `sh:ValidationResult` can embed child results using `sh:detail`:

```
ex:AddressShape
    a sh:NodeShape ;
    sh:property [
        sh:path ex:postalCode ;
        sh:pattern "^[0-9]{5}$" ;
        sh:message "Postal code must be 5 digits."@en ;
        sh:resultAnnotation [
            sh:annotationProperty ex:field ;
            sh:annotationValue "postalCode" ;
        ] ;
    ] .

ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:property [
        sh:path ex:address ;
        sh:node ex:AddressShape ;
        sh:severity sh:Violation ;
        sh:message "Person has invalid address structure."@en ;
        # Child violations from AddressShape appear under sh:detail
    ] .
```

The outer result will have `sh:detail` pointing to the inner `sh:ValidationResult` from `ex:AddressShape` . The usage can be seen here:

### Sample Data

#### Valid — conformant person

```
@prefix ex: <http://example.org/ns#> .

ex:addr_valid
    a ex:Address ;
    ex:postalCode "97401" .

ex:JohnDoe
    a ex:Person ;
    ex:name    "John Doe" ;
    ex:address ex:addr_valid .
```

`"97401"` matches `^[0-9]{5}$` — no violations fire.

---

#### Invalid — three distinct failure modes

```
@prefix ex: <http://example.org/ns#> .

# Postal code contains letters
ex:addr_letters
    a ex:Address ;
    ex:postalCode "ABC12" .

# Postal code is only 4 digits — too short
ex:addr_short
    a ex:Address ;
    ex:postalCode "1234" .

# No postal code at all — pattern constraint doesn't fire,
# but a downstream minCount would; left here to show
# sh:detail is absent when the inner shape has nothing to report
# (only the outer sh:node fires if the node itself is absent/malformed)
ex:addr_empty
    a ex:Address .

ex:JaneDoe
    a ex:Person ;
    ex:name    "Jane Doe" ;
    ex:address ex:addr_letters .

ex:BobSmith
    a ex:Person ;
    ex:name    "Bob Smith" ;
    ex:address ex:addr_short .

ex:CarolWu
    a ex:Person ;
    ex:name    "Carol Wu" ;
    ex:address ex:addr_empty .
```

---

### Resulting `sh:ValidationReport` in Turtle

```
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix ex:  <http://example.org/ns#> .

[] a sh:ValidationReport ;
    sh:conforms false ;

    # ── Jane Doe ── postal code has letters ─────────────────────────────────

    sh:result [
        a sh:ValidationResult ;
        sh:resultSeverity            sh:Violation ;
        sh:focusNode                 ex:JaneDoe ;
        sh:resultPath                ex:address ;
        sh:value                     ex:addr_letters ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:sourceShape               ex:PersonShape ;
        sh:resultMessage             "Person has invalid address structure."@en ;

        # Inner violation from ex:AddressShape surfaced here
        sh:detail [
            a sh:ValidationResult ;
            sh:resultSeverity            sh:Violation ;
            sh:focusNode                 ex:addr_letters ;
            sh:resultPath                ex:postalCode ;
            sh:value                     "ABC12" ;
            sh:sourceConstraintComponent sh:PatternConstraintComponent ;
            sh:sourceShape               ex:AddressShape ;
            sh:resultMessage             "Postal code must be 5 digits."@en ;

            # sh:resultAnnotation from the inner property shape
            ex:field "postalCode" ;
        ] ;
    ] ;

    # ── Bob Smith ── postal code too short ───────────────────────────────────

    sh:result [
        a sh:ValidationResult ;
        sh:resultSeverity            sh:Violation ;
        sh:focusNode                 ex:BobSmith ;
        sh:resultPath                ex:address ;
        sh:value                     ex:addr_short ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:sourceShape               ex:PersonShape ;
        sh:resultMessage             "Person has invalid address structure."@en ;

        sh:detail [
            a sh:ValidationResult ;
            sh:resultSeverity            sh:Violation ;
            sh:focusNode                 ex:addr_short ;
            sh:resultPath                ex:postalCode ;
            sh:value                     "1234" ;
            sh:sourceConstraintComponent sh:PatternConstraintComponent ;
            sh:sourceShape               ex:AddressShape ;
            sh:resultMessage             "Postal code must be 5 digits."@en ;

            ex:field "postalCode" ;
        ] ;
    ] ;

    # ── Carol Wu ── address node has no postal code ──────────────────────────
    # sh:pattern only fires when a value is present — no ex:postalCode triple
    # means the pattern constraint never executes (sh:minCount is not set).
    # ex:addr_empty conforms to ex:AddressShape as written, so sh:node
    # does NOT fire, and Carol Wu produces no result at all.
    .
```

---

**Carol Wu produces no violation** — this catches many people out. `sh:pattern` (like `sh:datatype`, `sh:minInclusive`, etc.) is a _value constraint_: it evaluates against values that exist. With no `ex:postalCode` triple present and no `sh:minCount 1` on the property shape, `ex:AddressShape` reports conformant, `sh:node` doesn’t fire, and the outer `ex:PersonShape` result is absent too. If a missing postal code should be an error, you need to add `sh:minCount 1` to the inner property shape.

`sh:detail` **depth mirrors nesting depth.** If `ex:AddressShape` itself used `sh:node` to delegate to a further shape, you’d get `sh:detail` inside `sh:detail`. Validators preserve the full tree.

`sh:value` **on the outer result** is `ex:addr_letters` / `ex:addr_short` — the address _node_ that failed, not the postal code string. The postal code string appears as `sh:value` on the inner `sh:detail` result. This layering is what makes `sh:detail` useful for pinpointing exactly which sub-constraint failed when navigating the report programmatically.

**The** `ex:field` **annotation only appears on the inner result.** The `sh:resultAnnotation` is on the `ex:AddressShape` property shape, so it attaches to the `sh:PatternConstraintComponent` result, not the outer `sh:NodeConstraintComponent` result. If you need the field name available at the outer level too, you’d need a separate `sh:resultAnnotation` on the `sh:node` property shape in `ex:PersonShape`.

**SPARQL query to flatten the nested report** for display:

```
PREFIX sh:  <http://www.w3.org/ns/shacl#>
PREFIX ex:  <http://example.org/ns#>

SELECT ?person ?addressNode ?postalCode ?message ?field
WHERE {
    ?report a sh:ValidationReport ;
            sh:result ?outerResult .
    ?outerResult
        sh:focusNode  ?person ;
        sh:resultPath ex:address ;
        sh:value      ?addressNode ;
        sh:detail     ?innerResult .
    ?innerResult
        sh:resultPath ex:postalCode ;
        sh:resultMessage ?message .
    OPTIONAL { ?innerResult sh:value  ?postalCode }
    OPTIONAL { ?innerResult ex:field  ?field }
}
```

which results in the following output:

[

![](https://substackcdn.com/image/fetch/$s_!_IpT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85427b4a-913e-4e91-b409-7ea9b08cee21_776x274.png)



](https://substackcdn.com/image/fetch/$s_!_IpT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85427b4a-913e-4e91-b409-7ea9b08cee21_776x274.png)

  

---

## Key Takeaways

- `sh:resultAnnotation` on property shapes applies to **every result** that constraint fires — use `sh:annotationValue` for catalogue-style metadata (error codes, rule IDs, doc links, remediation hints, responsible team).
    
- `sh:annotationVarName` is exclusively meaningful inside `sh:SPARQLConstraint` — it binds SPARQL output variables. Outside SPARQL it has no effect.
    
- Severity cascades: the _most severe_ result from nested shapes (`sh:node`, `sh:property` with `sh:node`) determines what gets surfaced in summary reporting, but all `sh:detail` children are preserved.
    

The generation of messaging moves well beyond just passing a single static text message with SHACL 1.2, and the implications for data pipelines should be clear:

- The things that fail to validate often point to problems upstream in your signal acquisition process that can be caught and corrected early, rather than at the stage where bad data is affecting your production capabilities.
    
- This can also surface error messages that inform UI/UX design - setting warning styles in HTML, for instance, or adding remediation messages as popups to help your users adjust their input.
    
- The ability to assign custom severities, process codes and other error codes make it possible to handle things like error message routing downstream (sending an error email to a system admin, for instance).
    
- Finally, such messages can also be stored in a graph as first-class citizens and audited or used for analytics, just as would be the case for the inbound data itself.
    

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!Pj9F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43ca06fe-83d1-48ac-bed5-ad85e20358f1_4096x4096.jpeg)



](https://substackcdn.com/image/fetch/$s_!Pj9F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43ca06fe-83d1-48ac-bed5-ad85e20358f1_4096x4096.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)  
[The Ontologist](https://ontologist.substack.com/)