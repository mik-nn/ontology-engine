---
type: article
title: "The Audit Procedure for Your Data: Business Constraints, XBRL and SHACL 1.2"
source: https://substack.com/@kurtcagle/p-193285689
created: 2026-05-04
tags:
  - article
---

# The Audit Procedure for Your Data: Business Constraints, XBRL and SHACL 1.2

Источник: https://substack.com/@kurtcagle/p-193285689

---
Apr 05, 2026

---

_The Ontologist | Kurt Cagle_


![](https://substackcdn.com/image/fetch/$s_!Vbix!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76abcf43-6167-4888-add2-6b51211d47ee_2688x1536.jpeg)

---

There is a habit of mind that afflicts almost everyone who encounters semantic web technology for the first time. Confronted with RDF, OWL, and the machinery of knowledge graphs, they immediately ask: _how do I model my domain?_ What are the classes? What are the properties? What is the taxonomy?

It’s a reasonable instinct. Modelling is how we make sense of complex domains. But it’s also, for a surprisingly large class of real business problems, the wrong place to start — and starting there leads to systems that are intellectually satisfying and practically inert.

This article is about a different starting point: constraints. Specifically, about how to use SHACL 1.2 — the W3C’s Shapes Constraint Language — to encode the rules that your data must satisfy, independently of whether you’ve built a complete ontological model of your domain. If you have a CPA’s intuition about financial reporting, you already understand the core idea. The rest is translation.

---

## Two Ways of Thinking About a Balance Sheet

Consider a balance sheet. A financial modeller approaching a balance sheet will want to define its structure: what line items exist, how they relate to each other, what the hierarchy of accounts looks like. They’ll build a chart of accounts — a careful taxonomy of every financial concept the organization tracks. This is legitimate, necessary work.

But an auditor approaching the same balance sheet thinks differently. They’re not primarily asking _what is here_. They’re asking _what must be true_. Assets must equal liabilities plus equity. Cash cannot be negative. Certain disclosures are mandatory if certain conditions hold. Related-party transactions must be identified. These rules don’t describe the balance sheet — they constrain it. They specify the conditions under which the data can be trusted.

The distinction is between a **chart of accounts** and an **audit procedure**. One is ontological — a map of the domain. The other is normative — a set of conditions the data must satisfy to be considered valid, complete, and reliable.

OWL is the chart of accounts. SHACL is the audit procedure.

Both are useful. But for many business problems — compliance, data governance, reporting validation, workflow integrity — the audit procedure is what you actually need, and you can write it without first completing the chart of accounts.

---

## What XBRL Already Knows

If you’ve worked with financial reporting standards, you’ve already encountered a constraint language — you just may not have thought of it that way.

XBRL (eXtensible Business Reporting Language) is, at its core, a system for encoding financial data in a structured, machine-readable form governed by taxonomies that specify what elements exist, what relationships hold between them, and what validation rules apply. The US GAAP taxonomy, for example, encodes not just the structure of financial statements but the rules that make them valid: which elements are required, what their allowable data types are, what mathematical relationships must hold between line items.

When a filing fails XBRL validation, it’s not because the data doesn’t match a model. It’s because the data violates a constraint. The validator doesn’t care about your ontology — it cares about whether your numbers are the right type, the right sign, the right relationship to each other.

SHACL generalizes this instinct. Where XBRL encodes financial reporting constraints for a specific, standardized domain, SHACL lets you encode the same class of constraint — type checking, cardinality, value ranges, structural relationships, conditional requirements — against any RDF graph, in any domain, on your own terms.

Think of SHACL as what XBRL would look like if it had been designed as a general-purpose constraint language rather than a financial reporting standard. The intellectual move is the same. The scope is much wider.

---

## Shapes, Not Classes

The fundamental unit of SHACL is the **shape**. A shape is a named set of constraints that a node in your graph must satisfy. It is not a class definition — it does not say what a thing _is_. It says what conditions must hold for a thing to be considered valid in a given context.

This distinction matters more than it first appears. A class definition is permanent and taxonomic — it places a thing in a hierarchy of kinds. A shape is contextual and operational — it specifies what must be true about a thing for a particular purpose, in a particular workflow, at a particular point in a process.

The same data node can satisfy multiple shapes, or fail one shape while satisfying another. An invoice might satisfy the shape for _syntactically valid invoice_ while failing the shape for _approved for payment_ — not because it’s the wrong kind of thing, but because it doesn’t yet meet the conditions required for a specific business action.

Let’s make this concrete. Here’s a minimal SHACL shape for a financial line item — the kind of constraint an auditor would recognize immediately:

```
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix fin:  <http://example.org/finance#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

fin:LineItemShape
    a sh:NodeShape ;
    sh:targetClass fin:LineItem ;
    sh:property [
        sh:path    fin:amount ;
        sh:datatype xsd:decimal ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:name    "amount" ;
        sh:message "Every line item must have exactly one decimal amount." ;
    ] ;
    sh:property [
        sh:path    fin:accountCode ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:name    "accountCode" ;
        sh:message "Every line item must reference an account code." ;
    ] .
```

Read this the way you’d read an audit checklist: _every line item must have exactly one amount, and that amount must be a decimal number. Every line item must have an account code._ No amount, wrong type, or missing account code — the shape reports a violation.

The business rule came first. The SHACL encoding followed it directly.

### Valid and Invalid: Line Items

Here’s what conforming and non-conforming data look like against this shape. RDF 1.2 introduces **triple annotations** using the `{| |}` syntax, which let you attach metadata — provenance, review status, entry timestamps — directly to individual triples without disrupting the graph structure. Think of annotations as the auditor’s margin notes: they travel with the fact they describe.

**Valid instance (Turtle with RDF 1.2 annotations):**

```
@prefix fin:  <http://example.org/finance#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

fin:lineItem001
    a fin:LineItem ;
    rdfs:label "Office Supplies Q1" ;
    fin:amount    "1250.00"^^xsd:decimal
        {| rdfs:label            "amount" ;
           prov:generatedAtTime  "2026-01-15"^^xsd:dateTime ;
           fin:enteredBy         fin:user_jsmith |} ;
    fin:accountCode "6100"^^xsd:string
        {| rdfs:label    "accountCode" ;
           fin:verifiedBy fin:auditor_acox ;
           fin:verifiedAt "2026-01-16"^^xsd:dateTime |} .
```

The annotations on `fin:amount` and `fin:accountCode` record _who_ entered the values and _when_ — provenance data that XBRL carries in context elements but that RDF 1.2 can attach directly to the triple. The shape validator sees only the unadorned triples; the annotations travel alongside as auditable metadata without interfering with constraint evaluation.

**Invalid instance — missing amount:**

```
fin:lineItem002
    a fin:LineItem ;
    rdfs:label    "Travel Expense March" ;
    fin:accountCode "6200"^^xsd:string
        {| rdfs:label   "accountCode" ;
           fin:enteredBy fin:user_bwong |} .
    # fin:amount is absent — violates sh:minCount 1
```

**Invalid instance — wrong datatype:**

```
fin:lineItem003
    a fin:LineItem ;
    rdfs:label    "Consulting Fees Q1" ;
    fin:amount    "four thousand dollars" ;  # xsd:string, not xsd:decimal — violation
    fin:accountCode "6300"^^xsd:string .
```

**Equivalent XBRL context and fact:**

In XBRL, the line item’s identity and provenance are carried in a `<context>` element; the fact itself is a typed element referencing that context. The constraint that the value must be numeric and present is enforced by the taxonomy’s element declaration, not expressed inline.

```
<?xml version="1.0" encoding="UTF-8"?>
<xbrl xmlns="http://www.xbrl.org/2003/instance"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
      xmlns:fin="http://example.org/finance/xbrl#">

  <!-- Context: the "who and when" that SHACL carries in triple annotations -->
  <context id="Q1_2026_jsmith">
    <entity>
      <identifier scheme="http://example.org/entities">ACME-CORP</identifier>
    </entity>
    <period>
      <startDate>2026-01-01</startDate>
      <endDate>2026-03-31</endDate>
    </period>
  </context>

  <unit id="USD"><measure>iso4217:USD</measure></unit>

  <!-- Valid fact: amount present, typed as decimal by taxonomy -->
  <fin:OfficeSuppliesExpense contextRef="Q1_2026_jsmith"
      decimals="2" unitRef="USD">1250.00</fin:OfficeSuppliesExpense>

  <!-- Invalid in XBRL: a string value where the taxonomy demands a numeric
       type is rejected at schema validation, before a processor sees it -->
  <!-- <fin:ConsultingFeesExpense contextRef="Q1_2026_jsmith"
       decimals="2" unitRef="USD">four thousand dollars</fin:ConsultingFeesExpense> -->

</xbrl>
```

The comparison is instructive. XBRL enforces the type constraint through the taxonomy schema — you can’t represent the wrong datatype in a valid XBRL instance. SHACL enforces it as a named rule against a graph that makes no such structural demand. The constraint is the same; the architecture differs. SHACL is the more flexible instrument precisely because the data layer and the constraint layer are fully separated.

---

## Materiality: Value Range Constraints

An auditor doesn’t just check that numbers exist — they check that numbers make sense. Revenue figures shouldn’t be negative. Certain ratios shouldn’t fall outside expected ranges. Expense amounts above a threshold require additional documentation.

SHACL handles this through value constraint components. Let’s extend our income statement example:

```
fin:RevenueShape
    a sh:NodeShape ;
    sh:targetClass fin:RevenueItem ;
    sh:property [
        sh:path         fin:amount ;
        sh:datatype     xsd:decimal ;
        sh:minInclusive "0"^^xsd:decimal ;
        sh:minCount     1 ;
        sh:maxCount     1 ;
        sh:name         "amount" ;
        sh:message      "Revenue amounts must be non-negative." ;
    ] .

fin:ExpenseShape
    a sh:NodeShape ;
    sh:targetClass fin:ExpenseItem ;
    sh:property [
        sh:path         fin:amount ;
        sh:datatype     xsd:decimal ;
        sh:minInclusive "0"^^xsd:decimal ;
        sh:minCount     1 ;
        sh:maxCount     1 ;
        sh:name         "amount" ;
        sh:message      "Expense amounts must be non-negative." ;
    ] .
```

`sh:minInclusive 0` is the SHACL expression of a rule every accountant knows: you don’t record negative revenue or negative expenses — you record contra-accounts. The constraint doesn’t model _why_ that’s true. It simply enforces that it is.

### Valid and Invalid: Value Ranges

**Valid instances:**

```
@prefix fin:  <http://example.org/finance#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

fin:revenue001
    a fin:RevenueItem ;
    rdfs:label "Product Sales Q1" ;
    fin:amount "485000.00"^^xsd:decimal
        {| rdfs:label            "amount" ;
           prov:generatedAtTime  "2026-03-31"^^xsd:dateTime ;
           fin:approvedBy        fin:mgr_dleon ;
           fin:source            fin:erp_system |} .

fin:expense001
    a fin:ExpenseItem ;
    rdfs:label "Payroll March" ;
    fin:amount "210000.00"^^xsd:decimal
        {| rdfs:label           "amount" ;
           prov:generatedAtTime "2026-03-31"^^xsd:dateTime ;
           fin:approvedBy       fin:mgr_dleon |} .
```

**Invalid instance — negative revenue:**

```
fin:revenue002
    a fin:RevenueItem ;
    rdfs:label "Returns Adjustment" ;
    fin:amount "-12000.00"^^xsd:decimal
        {| rdfs:label   "amount" ;
           fin:enteredBy fin:user_tpark |} .
    # Violates sh:minInclusive 0 — returns should be a contra-revenue account,
    # not a negative revenue entry.
```

**Equivalent XBRL:**

XBRL handles sign convention through taxonomy element definitions and calculation linkbases, which specify that certain elements must sum to others. A negative revenue figure typically fails a calculation consistency check rather than a simple type constraint.

```
  <context id="FY2026_Q1">
    <entity>
      <identifier scheme="http://example.org/entities">ACME-CORP</identifier>
    </entity>
    <period>
      <startDate>2026-01-01</startDate>
      <endDate>2026-03-31</endDate>
    </period>
  </context>

  <unit id="USD"><measure>iso4217:USD</measure></unit>

  <!-- Valid: positive revenue -->
  <fin:ProductSalesRevenue contextRef="FY2026_Q1"
      decimals="2" unitRef="USD">485000.00</fin:ProductSalesRevenue>

  <!-- Valid: positive expense -->
  <fin:PayrollExpense contextRef="FY2026_Q1"
      decimals="2" unitRef="USD">210000.00</fin:PayrollExpense>

  <!-- Invalid: negative revenue — XBRL calculation linkbase flags this
       as a consistency violation in a signed calculation check, but only
       if the calculation linkbase is present and the processor enforces it.
       SHACL enforces it unconditionally as a named constraint. -->
  <!-- <fin:ProductSalesRevenue contextRef="FY2026_Q1"
       decimals="2" unitRef="USD">-12000.00</fin:ProductSalesRevenue> -->
```

Note the architectural difference: XBRL’s sign constraints live in the calculation linkbase — a separate document expressing mathematical relationships between elements. SHACL collapses that into the same shape that expresses every other constraint on the data node.

---

## Structural Integrity: Node and Property Relationships

Financial statements have structural rules that go beyond individual line items. An income statement must reference a reporting period. A reporting period must have both a start date and an end date.

These are relational constraints — rules about how nodes in the graph connect to each other. SHACL handles them through `sh:node` (constraining the shape of a linked node) and property path constraints.

```
fin:ReportingPeriodShape
    a sh:NodeShape ;
    sh:targetClass fin:ReportingPeriod ;
    sh:property [
        sh:path     fin:startDate ;
        sh:datatype xsd:date ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:name     "startDate" ;
        sh:message  "A reporting period must have exactly one start date." ;
    ] ;
    sh:property [
        sh:path     fin:endDate ;
        sh:datatype xsd:date ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:name     "endDate" ;
        sh:message  "A reporting period must have exactly one end date." ;
    ] .

fin:IncomeStatementShape
    a sh:NodeShape ;
    sh:targetClass fin:IncomeStatement ;
    sh:property [
        sh:path    fin:reportingPeriod ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:node    fin:ReportingPeriodShape ;
        sh:name    "reportingPeriod" ;
        sh:message "An income statement must reference a valid reporting period." ;
    ] .
```

The `sh:node` constraint on `fin:reportingPeriod` says: not only must this property exist, but the node it points to must itself satisfy `fin:ReportingPeriodShape`. Structural validity cascades. An income statement is only valid if its reporting period is valid — which is exactly how an auditor would think about it.

### Valid and Invalid: Structural Relationships

**Valid instance — income statement with complete reporting period:**

```
@prefix fin:  <http://example.org/finance#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

fin:period_Q1_2026
    a fin:ReportingPeriod ;
    rdfs:label "Q1 2026" ;
    fin:startDate "2026-01-01"^^xsd:date
        {| rdfs:label       "startDate" ;
           fin:confirmedBy  fin:auditor_acox |} ;
    fin:endDate   "2026-03-31"^^xsd:date
        {| rdfs:label       "endDate" ;
           fin:confirmedBy  fin:auditor_acox |} .

fin:incomeStatement_Q1_2026
    a fin:IncomeStatement ;
    rdfs:label "ACME Corp Income Statement Q1 2026" ;
    fin:reportingPeriod fin:period_Q1_2026
        {| rdfs:label            "reportingPeriod" ;
           prov:generatedAtTime  "2026-04-01"^^xsd:dateTime ;
           fin:preparedBy        fin:user_jsmith |} ;
    fin:totalRevenue  "485000.00"^^xsd:decimal
        {| rdfs:label "totalRevenue" ; fin:approvedBy fin:mgr_dleon |} ;
    fin:totalExpenses "310000.00"^^xsd:decimal
        {| rdfs:label "totalExpenses" ; fin:approvedBy fin:mgr_dleon |} .
```

The annotations here serve as the electronic equivalent of sign-off initials on a printed financial statement — each material triple carries a record of who asserted it and when. This is metadata that traditionally lives in a separate audit workpaper; RDF 1.2 annotations allow it to travel with the triple.

**Invalid instance — broken period (missing end date):**

```
fin:period_broken
    a fin:ReportingPeriod ;
    rdfs:label "Incomplete Period" ;
    fin:startDate "2026-01-01"^^xsd:date
        {| rdfs:label "startDate" ; fin:enteredBy fin:user_tpark |} .
    # fin:endDate absent — fin:ReportingPeriodShape violation.
    # This cascades: any fin:IncomeStatement referencing this period
    # will also fail via its sh:node constraint.

fin:incomeStatement_broken
    a fin:IncomeStatement ;
    rdfs:label "Statement with broken period reference" ;
    fin:reportingPeriod fin:period_broken
        {| rdfs:label "reportingPeriod" ; fin:enteredBy fin:user_tpark |} .
```

**Invalid instance — no period reference at all:**

```
fin:incomeStatement_orphan
    a fin:IncomeStatement ;
    rdfs:label "Orphaned Income Statement" ;
    fin:totalRevenue "200000.00"^^xsd:decimal .
    # fin:reportingPeriod absent entirely — sh:minCount 1 violation.
```

**Equivalent XBRL:**

In XBRL, the reporting period is not a data node — it is a `<context>` element, structurally required by the instance document format. A fact with no context reference is a malformed document, caught by schema validation before a business rules processor ever sees it.

```
  <!-- Valid: complete context with start and end dates (duration period) -->
  <context id="FY2026_Q1_complete">
    <entity>
      <identifier scheme="http://example.org/entities">ACME-CORP</identifier>
    </entity>
    <period>
      <startDate>2026-01-01</startDate>
      <endDate>2026-03-31</endDate>
    </period>
  </context>

  <fin:TotalRevenues contextRef="FY2026_Q1_complete"
      decimals="2" unitRef="USD">485000.00</fin:TotalRevenues>

  <!-- Invalid in XBRL: a duration context with no endDate is schema-invalid.
       SHACL expresses the same rule as an explicit, named, reportable constraint;
       XBRL expresses it as a document structure violation caught by XML Schema.
       Both enforce the rule; only SHACL produces a named, human-readable
       violation report attributing the failure to a specific constraint. -->
```

This contrast is worth pausing on. XBRL achieves structural integrity through document architecture — the format itself makes certain violations impossible to represent. SHACL achieves it through explicit, named, auditable constraints that can be selectively enforced, versioned, and reported against. Neither is strictly superior; they reflect different design philosophies about where to locate the rules.

---

## Conditional Requirements: The Disclosure Trigger

One of the most powerful — and most underused — features of SHACL core is `sh:or`, `sh:and`, and `sh:not`, which allow you to express conditional business rules. In financial reporting, many requirements are triggered conditionally: _if_ a related-party transaction exists, _then_ a disclosure is required.

```
fin:RelatedPartyTransactionShape
    a sh:NodeShape ;
    sh:targetClass fin:Transaction ;
    sh:property [
        sh:path     fin:isRelatedParty ;
        sh:datatype xsd:boolean ;
        sh:maxCount 1 ;
        sh:name     "isRelatedParty" ;
    ] ;
    sh:or (
        [
            sh:property [
                sh:path     fin:isRelatedParty ;
                sh:hasValue false ;
            ]
        ]
        [
            sh:property [
                sh:path     fin:relatedPartyDisclosure ;
                sh:minCount 1 ;
                sh:name     "relatedPartyDisclosure" ;
                sh:message  "Related-party transactions require a disclosure reference." ;
            ]
        ]
    ) .
```

Read this as: _a transaction is valid if either it is not a related-party transaction, or it has a disclosure reference._ If it’s flagged as related-party with no disclosure, validation fails.

### Valid and Invalid: Conditional Disclosure

**Valid — arm’s-length transaction, no disclosure required:**

```
@prefix fin:  <http://example.org/finance#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

fin:txn_vendor_001
    a fin:Transaction ;
    rdfs:label "Vendor Payment — Office Depot" ;
    fin:amount "4200.00"^^xsd:decimal
        {| rdfs:label            "amount" ;
           prov:generatedAtTime  "2026-02-14"^^xsd:dateTime |} ;
    fin:isRelatedParty false
        {| rdfs:label    "isRelatedParty" ;
           fin:assertedBy fin:user_jsmith ;
           fin:assertedAt "2026-02-14"^^xsd:dateTime |} .
```

**Valid — related-party transaction WITH disclosure:**

```
fin:txn_related_001
    a fin:Transaction ;
    rdfs:label "Consulting Services — CEO Family Trust" ;
    fin:amount "75000.00"^^xsd:decimal
        {| rdfs:label            "amount" ;
           prov:generatedAtTime  "2026-03-01"^^xsd:dateTime |} ;
    fin:isRelatedParty true
        {| rdfs:label    "isRelatedParty" ;
           fin:assertedBy fin:auditor_acox ;
           fin:reviewedAt "2026-03-15"^^xsd:dateTime |} ;
    fin:relatedPartyDisclosure fin:disclosure_RPT_2026_001
        {| rdfs:label   "relatedPartyDisclosure" ;
           fin:filedBy   fin:counsel_mjones ;
           fin:filedAt   "2026-03-16"^^xsd:dateTime |} .
```

Note what the annotations accomplish here: the `fin:isRelatedParty` triple carries a `fin:reviewedAt` timestamp showing it was reviewed by the auditor _after_ the transaction was entered. The `fin:relatedPartyDisclosure` triple carries a `fin:filedAt` timestamp. The temporal relationship between those two annotations is auditable evidence of process compliance — something that would otherwise live in a separate workpaper.

**Invalid — related-party transaction WITHOUT disclosure:**

```
fin:txn_related_002
    a fin:Transaction ;
    rdfs:label "IT Services — Board Member LLC" ;
    fin:amount "38500.00"^^xsd:decimal
        {| rdfs:label            "amount" ;
           prov:generatedAtTime  "2026-03-20"^^xsd:dateTime |} ;
    fin:isRelatedParty true
        {| rdfs:label   "isRelatedParty" ;
           fin:enteredBy fin:user_bwong |} .
    # fin:relatedPartyDisclosure is absent.
    # sh:or fails: isRelatedParty is not false, AND no disclosure exists.
    # Violation: "Related-party transactions require a disclosure reference."
```

**Equivalent XBRL:**

XBRL handles related-party disclosures through taxonomy elements and filing structure. The conditional relationship — _if_ related party, _then_ disclosure required — is not directly expressible as a machine-executable rule in XBRL. It lives in the reviewer’s checklist or a custom validation layer built on top of the XBRL processor.

```
  <!-- Valid: arm's-length transaction -->
  <fin:VendorPayment contextRef="FY2026_Q1_complete"
      decimals="2" unitRef="USD">4200.00</fin:VendorPayment>
  <fin:IsRelatedPartyTransaction contextRef="FY2026_Q1_complete"
      >false</fin:IsRelatedPartyTransaction>

  <!-- Valid: related-party with disclosure reference -->
  <fin:ConsultingServicesExpense contextRef="FY2026_Q1_complete"
      decimals="2" unitRef="USD">75000.00</fin:ConsultingServicesExpense>
  <fin:IsRelatedPartyTransaction contextRef="FY2026_Q1_complete"
      >true</fin:IsRelatedPartyTransaction>
  <fin:RelatedPartyDisclosureRef contextRef="FY2026_Q1_complete"
      >RPT-2026-001</fin:RelatedPartyDisclosureRef>

  <!-- Invalid in the SHACL sense: related-party with no disclosure.
       XBRL has no native mechanism to catch this conditionally.
       A standard XBRL validator will not report a violation here. -->
  <fin:BoardMemberServicesExpense contextRef="FY2026_Q1_complete"
      decimals="2" unitRef="USD">38500.00</fin:BoardMemberServicesExpense>
  <fin:IsRelatedPartyTransaction contextRef="FY2026_Q1_complete"
      >true</fin:IsRelatedPartyTransaction>
  <!-- RelatedPartyDisclosureRef absent: no XBRL validator catches this. -->
```

This is where SHACL meaningfully extends what XBRL can express. The conditional disclosure rule has real regulatory weight — in XBRL, it lives in human procedure. In SHACL, it lives in the data layer, is machine-executable, and produces a named, reportable violation with a clear message.

---

## Severity: Not All Violations Are Equal

An auditor distinguishes between a material misstatement and an immaterial one. SHACL 1.2 preserves this distinction through `sh:severity`. Three levels are defined: `sh:Violation` (the default — the data fails the constraint), `sh:Warning` (the data is suspect but not definitively invalid), and `sh:Info` (informational — worth noting but not a failure).

```
fin:ThresholdWarningShape
    a sh:NodeShape ;
    sh:targetClass fin:ExpenseItem ;
    sh:property [
        sh:path         fin:amount ;
        sh:maxInclusive "10000"^^xsd:decimal ;
        sh:severity     sh:Warning ;
        sh:name         "amount" ;
        sh:message      "Expense items over $10,000 should be reviewed for documentation." ;
    ] .
```

### Valid, Warning, and Violation: Severity in Practice

**Passes cleanly — amount below threshold:**

```
@prefix fin:  <http://example.org/finance#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

fin:expense_under
    a fin:ExpenseItem ;
    rdfs:label "Courier Services March" ;
    fin:amount "340.00"^^xsd:decimal
        {| rdfs:label   "amount" ;
           fin:enteredBy fin:user_jsmith |} ;
    fin:accountCode "6400"^^xsd:string
        {| rdfs:label "accountCode" |} .
    # No violation, no warning. Passes fin:ThresholdWarningShape cleanly.
```

**Triggers warning — amount over threshold, data technically valid:**

```
fin:expense_over
    a fin:ExpenseItem ;
    rdfs:label "Legal Retainer Q1" ;
    fin:amount "45000.00"^^xsd:decimal
        {| rdfs:label            "amount" ;
           fin:enteredBy         fin:user_bwong ;
           fin:reviewRequired    true
               {| fin:reason "threshold exceeded" |} |} ;
    fin:accountCode "6500"^^xsd:string
        {| rdfs:label "accountCode" |} .
    # SHACL reports sh:Warning:
    # "Expense items over $10,000 should be reviewed for documentation."
    # Data is not invalid; a human review workflow is triggered.
```

Note the nested annotation: `fin:reviewRequired true` is itself annotated with `fin:reason "threshold exceeded"` — RDF 1.2 allows annotations on annotations, providing a full audit chain without leaving the triple layer.

**XBRL equivalent — materiality thresholds:**

XBRL has no native severity model. A value either satisfies the schema type and calculation constraints or it doesn’t. Materiality thresholds and review triggers are entirely external to the format — they live in audit procedures and engagement letters. SHACL encodes them in the data layer alongside structural constraints, meaning a single validation pass produces a unified report covering hard violations, soft warnings, and informational flags.

```
  <!-- Below threshold: no flag in either XBRL or SHACL -->
  <fin:CourierExpense contextRef="FY2026_Q1_complete"
      decimals="2" unitRef="USD">340.00</fin:CourierExpense>

  <!-- Over threshold: XBRL has no mechanism to generate a warning here.
       An external audit tool must compare this value against a policy rule
       defined entirely outside the XBRL instance and taxonomy.
       SHACL generates a named sh:Warning in the same validation report
       that catches type errors, cardinality failures, and missing disclosures. -->
  <fin:LegalRetainerExpense contextRef="FY2026_Q1_complete"
      decimals="2" unitRef="USD">45000.00</fin:LegalRetainerExpense>
```

The severity model gives SHACL a vocabulary that pure schema languages lack: the difference between _wrong_, _suspicious_, and _worth noting_ is meaningful in business contexts, and SHACL lets you encode all three in the same constraint document, evaluated in a single pass.

---

## Reading the Report: What a SHACL Validator Actually Returns

All of the constraint definitions above are worth nothing unless a validator runs them against real data and produces something actionable. SHACL 1.2 specifies a standard validation report format — itself expressed as RDF — that captures every violation, warning, and informational result from a validation run. Understanding what that report contains, and how to read it, closes the loop between writing shapes and using them in practice.

### The Tabular View

When a business analyst or auditor asks “what’s wrong with this data?”, the most useful first answer is a flat summary table. Here is the consolidated report from running all of the shapes defined in this article against the invalid instances introduced in each section:

# Focus Node Shape Property Severity Message 1 `fin:lineItem002` `fin:LineItemShape` `fin:amount` Violation Every line item must have exactly one decimal amount. 2 `fin:lineItem003` `fin:LineItemShape` `fin:amount` Violation Every line item must have exactly one decimal amount. 3 `fin:revenue002` `fin:RevenueShape` `fin:amount` Violation Revenue amounts must be non-negative. 4 `fin:period_broken` `fin:ReportingPeriodShape` `fin:endDate` Violation A reporting period must have exactly one end date. 5 `fin:incomeStatement_broken` `fin:IncomeStatementShape` `fin:reportingPeriod` Violation An income statement must reference a valid reporting period. 6 `fin:incomeStatement_orphan` `fin:IncomeStatementShape` `fin:reportingPeriod` Violation An income statement must reference a valid reporting period. 7 `fin:txn_related_002` `fin:RelatedPartyTransactionShape` `fin:relatedPartyDisclosure` Violation Related-party transactions require a disclosure reference. 8 `fin:expense_over` `fin:ThresholdWarningShape` `fin:amount` **Warning** Expense items over $10,000 should be reviewed for documentation.

Rows 1–7 are hard violations — data that fails a constraint and must be corrected before the dataset can be considered valid. Row 8 is a warning — data that is structurally sound but triggers a review workflow. An auditor reading this table knows immediately: seven items require remediation, one requires a documented review. The table is machine-generated from the same shapes that encode the business rules. There is no separate report template to maintain.

Note row 5: `fin:incomeStatement_broken` fails not because it is itself malformed, but because the period it references (`fin:period_broken`) is missing an end date. This is the cascade effect of `sh:node` — the structural integrity constraint propagates up from the referenced node to the referencing one. The report surfaces both failures, giving the data owner a complete picture of what needs to be fixed and in what order (fix the period first; the income statement violation will clear automatically on re-validation).

### The Formal SHACL Report

Behind that table is a structured RDF document. Every SHACL validator produces a `sh:ValidationReport` instance — a machine-readable record of the full validation run that can itself be stored, queried, compared across periods, and used as input to downstream workflows. Here is the report corresponding to the table above, in Turtle:

```
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix fin:  <http://example.org/finance#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

fin:ValidationReport_2026_Q1
    a sh:ValidationReport ;
    sh:conforms false ;
    prov:generatedAtTime "2026-04-05T09:00:00"^^xsd:dateTime ;
    rdfs:label "Q1 2026 Financial Data Validation — Full Run" ;

    ## Result 1: lineItem002 — missing amount
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          fin:lineItem002 ;
        sh:resultPath         fin:amount ;
        sh:sourceShape        fin:LineItemShape ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Every line item must have exactly one decimal amount." ;
    ] ;

    ## Result 2: lineItem003 — wrong datatype on amount
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          fin:lineItem003 ;
        sh:resultPath         fin:amount ;
        sh:value              "four thousand dollars" ;
        sh:sourceShape        fin:LineItemShape ;
        sh:sourceConstraintComponent sh:DatatypeConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Every line item must have exactly one decimal amount." ;
    ] ;

    ## Result 3: revenue002 — negative revenue
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          fin:revenue002 ;
        sh:resultPath         fin:amount ;
        sh:value              "-12000.00"^^xsd:decimal ;
        sh:sourceShape        fin:RevenueShape ;
        sh:sourceConstraintComponent sh:MinInclusiveConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Revenue amounts must be non-negative." ;
    ] ;

    ## Result 4: period_broken — missing endDate
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          fin:period_broken ;
        sh:resultPath         fin:endDate ;
        sh:sourceShape        fin:ReportingPeriodShape ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "A reporting period must have exactly one end date." ;
    ] ;

    ## Result 5: incomeStatement_broken — period fails sh:node cascade
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          fin:incomeStatement_broken ;
        sh:resultPath         fin:reportingPeriod ;
        sh:value              fin:period_broken ;
        sh:sourceShape        fin:IncomeStatementShape ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "An income statement must reference a valid reporting period." ;
    ] ;

    ## Result 6: incomeStatement_orphan — no period reference at all
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          fin:incomeStatement_orphan ;
        sh:resultPath         fin:reportingPeriod ;
        sh:sourceShape        fin:IncomeStatementShape ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "An income statement must reference a valid reporting period." ;
    ] ;

    ## Result 7: txn_related_002 — related-party with no disclosure
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          fin:txn_related_002 ;
        sh:resultPath         fin:relatedPartyDisclosure ;
        sh:sourceShape        fin:RelatedPartyTransactionShape ;
        sh:sourceConstraintComponent sh:OrConstraintComponent ;
        sh:resultSeverity     sh:Violation ;
        sh:resultMessage      "Related-party transactions require a disclosure reference." ;
    ] ;

    ## Result 8: expense_over — over threshold (Warning, not Violation)
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode          fin:expense_over ;
        sh:resultPath         fin:amount ;
        sh:value              "45000.00"^^xsd:decimal ;
        sh:sourceShape        fin:ThresholdWarningShape ;
        sh:sourceConstraintComponent sh:MaxInclusiveConstraintComponent ;
        sh:resultSeverity     sh:Warning ;
        sh:resultMessage      "Expense items over $10,000 should be reviewed for documentation." ;
    ] .
```

Several structural features of this report are worth noting.

`sh:conforms false` is the top-level verdict. A report where every result is a `sh:Warning` or `sh:Info` — and no `sh:Violation` exists — would still set `sh:conforms true`, because warnings do not constitute failure. This maps directly onto audit practice: a dataset with review flags is not an invalid dataset; it’s a dataset requiring follow-up. A dataset with violations is. The distinction is machine-readable and unambiguous.

`sh:sourceConstraintComponent` identifies _which constraint type_ triggered each result — `sh:MinCountConstraintComponent`, `sh:DatatypeConstraintComponent`, `sh:MinInclusiveConstraintComponent`, and so on. This allows downstream tooling to categorize violations by type, prioritize remediation queues, or route results to different review workflows. Type errors go to data entry. Cardinality violations go to completeness review. Conditional failures go to compliance.

`sh:value` appears only when there is an _actual value_ to report — the wrong datatype string in result 2, the negative decimal in result 3, the offending period node in result 5, the over-threshold amount in result 8. Where the violation is a missing value (results 1, 4, 6) there is nothing to report in `sh:value`, because the problem is absence rather than incorrectness.

The report is itself an RDF graph. It can be stored in the same triplestore as the data it validates. It can be annotated with remediation notes using the same RDF 1.2 `{| |}` syntax applied to the data throughout this article. It can be queried with SPARQL — “show me all Violations in the Q1 report that have not yet been remediated” is a straightforward query against a report graph augmented with a `fin:remediatedAt` annotation. The audit trail and the validation system use the same substrate.

---

## What This Unlocks

The OWL-first approach to knowledge modelling produces rich, expressive class hierarchies that answer the question: _what kinds of things exist in this domain, and how do they relate?_ That’s valuable work. But it tends to produce systems that are hard to validate, hard to explain to non-technical stakeholders, and hard to connect to operational business processes.

SHACL-first thinking — approaching a domain through its constraints rather than its taxonomy — produces something different: a set of explicit, executable, human-readable business rules that can be applied to data at any point in a workflow. The rules can be reviewed by a business analyst without reading a line of RDF. They can be explained to an auditor. They can be version-controlled, compared across reporting periods, and used to generate meaningful validation reports rather than opaque schema errors.

RDF 1.2 annotations add a further dimension: the data that satisfies (or violates) those constraints can carry its own provenance inline — who asserted it, when, under what authority — without requiring a separate metadata store or a parallel audit trail. The annotated triple _is_ the audited fact.

More practically: you don’t need to finish the ontology before you can validate the data. The shapes can be written incrementally, against whatever graph structure you already have, targeting the rules that matter most for your immediate business need. This is the constraint-first mindset — and for the class of problems that business analysts actually face, it’s often the faster, more tractable, and more maintainable approach.

---

## A Note on Scope: SHACL 1.2 Core vs. What Comes Next

Everything in this article uses SHACL 1.2 core — property constraints, node constraints, cardinality, value ranges, logical operators, and severity. This is the layer that maps cleanly onto business rules a CPA or business analyst would recognize.

SHACL also has a more powerful layer: SHACL-AF (Advanced Features) introduces rules, functions, and SPARQL-based constraints that let you express derived values, cross-graph inferences, and complex validation logic. That territory is worth a dedicated article, but it’s a different cognitive register — closer to a rules engine than an audit checklist. The boundary matters, and we’ll explore it separately.

Similarly, the relationship between SHACL 1.2 and XBRL goes deeper than this article has space to develop. There is a reasonable argument that XBRL taxonomies could be expressed as SHACL shape libraries, making financial reporting constraints reusable against any RDF-structured financial data rather than requiring XBRL-specific tooling. That too is a conversation for another piece.

For now: if you can write it as a business rule in plain English, you can probably encode it in SHACL 1.2 core. Start there. The chart of accounts can wait.
