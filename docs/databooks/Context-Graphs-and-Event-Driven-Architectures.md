---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Context-Graphs-and-Event-Driven-Architectures
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:58.070186+00:00'
  title: Context graphs and event Driven architectures
  type: plain-doc
  version: '0.1'
---

# Context graphs and event Driven architectures

[

![](https://substackcdn.com/image/fetch/$s_!9iYH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98e89632-b9c2-4c95-a039-09b5b189ee5d_2688x1536.jpeg)



](https://substackcdn.com/image/fetch/$s_!9iYH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98e89632-b9c2-4c95-a039-09b5b189ee5d_2688x1536.jpeg)

A context graph, as I’ve discussed previously, is in effect a graph-oriented log of events. Sometimes those events are major (a change in corporate strategy), but most are tied to a particular process. This suggests that thinking about the utility of context graphs will most likely reflect an asynchronous event-driven environment over a graph (not all that dissimilar to the way an HTML or XML DOM works with its event architecture) rather than an imperative services architecture. When an event occurs, it creates an append-only response through an event handler (a rule) that may be directed to one or more (named) graphs as part of a processing pipeline.

The generated content makes extensive use of reification. The primary graph contains durable facts - those things that are being asserted as true. The reifications, on the other hand, qualify these assertions - when was this assertion made, who made it, under what context, during which session, in response to what event. The reifications themselves are generally named rather than anonymous because they can be referred to in later events.

For instance, consider Alice, who’s a banking customer who can perform a number of different actions (which in turn initiate events), including authentication, checking a balance, depositing money, or requesting a loan. This can be shown in the following diagram:

[

![](https://substackcdn.com/image/fetch/$s_!c8cx!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82be870c-d378-41f7-b43f-d17cc901f5a3_7227x5505.png)



](https://substackcdn.com/image/fetch/$s_!c8cx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82be870c-d378-41f7-b43f-d17cc901f5a3_7227x5505.png)

The data for this is given in the Turtle 1.2 file below

```
VERSION 1.2 # Needed for newer RDF processors
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix bank:  <https://example.bank/ontology#> .
@prefix ctx:   <https://example.bank/context#> .
@prefix ev:    <https://example.bank/event#> .
@prefix cust:  <https://example.bank/customer/> .
@prefix acct:  <https://example.bank/account/> .
@prefix sess:  <https://example.bank/session/> .
@prefix loan:  <https://example.bank/loan/> .
@prefix pay:   <https://example.bank/payment/> .

# -------------------------------------------------------
# Customer & Account Resources
# -------------------------------------------------------

cust:alice a bank:Customer ;
    bank:customerId   "C-00441"^^xsd:string ;
    bank:fullName     "Alice Marchetti" ;
    bank:riskTier     bank:StandardRisk .

acct:alice-checking a bank:CheckingAccount ;
    bank:accountHolder  cust:alice ;
    bank:accountNumber  "****7823" ;
    bank:currency       "USD" .

# -------------------------------------------------------
# Session Context  (groups the events into a single visit)
# -------------------------------------------------------

sess:S-20260303-C00441 a bank:BankingSession ;
    bank:customer   cust:alice ;
    bank:channel    bank:MobileApp ;
    bank:startTime  "2026-03-03T09:00:00Z"^^xsd:dateTime ;
    bank:ipAddress  "203.0.113.47" .

# The context graph node references all events
# produced during the session — the programmatic
# handle for the entire interaction envelope.

ctx:CG-S-20260303-C00441 a ctx:ContextGraph ;
    ctx:session  sess:S-20260303-C00441 ;
    ctx:subject  cust:alice ;
    ctx:events   ev:auth-001 ,
                 ev:balance-001 ,
                 ev:payment-001 ,
                 ev:loan-req-001 .

# -------------------------------------------------------
# EVENT 1 — Authentication
# The base triple asserts the relationship.
# The reifier ev:auth-001 carries the event envelope.
# -------------------------------------------------------

cust:alice bank:authenticatedWith bank:CoreSystem
    ~ ev:auth-001
    {| bank:session    sess:S-20260303-C00441 ;
       bank:timestamp  "2026-03-03T09:00:05Z"^^xsd:dateTime ;
       bank:authMethod bank:BiometricMFA ;
       bank:outcome    bank:Success ;
       bank:eventType  bank:AuthenticationEvent |} .

# -------------------------------------------------------
# EVENT 2 — Balance Enquiry
# The balance itself lives on the account resource;
# the *act of querying* it is what gets reified.
# -------------------------------------------------------

cust:alice bank:queriedBalance acct:alice-checking
    ~ ev:balance-001
    {| bank:session         sess:S-20260303-C00441 ;
       bank:timestamp       "2026-03-03T09:01:22Z"^^xsd:dateTime ;
       bank:balanceReturned "4823.57"^^xsd:decimal ;
       bank:currency        "USD" ;
       bank:eventType       bank:BalanceEnquiryEvent |} .

# -------------------------------------------------------
# EVENT 3 — Bill Payment
# The payment resource carries the durable record;
# the reifier annotates the intent + outcome.
# -------------------------------------------------------

pay:PAY-2026-0042 a bank:BillPayment ;
    bank:payee         "Pacific Gas & Electric" ;
    bank:referenceCode "PGE-INV-2026-03" ;
    bank:amount        "142.00"^^xsd:decimal ;
    bank:currency      "USD" .

cust:alice bank:initiatedPayment pay:PAY-2026-0042
    ~ ev:payment-001
    {| bank:session      sess:S-20260303-C00441 ;
       bank:timestamp    "2026-03-03T09:03:10Z"^^xsd:dateTime ;
       bank:fromAccount  acct:alice-checking ;
       bank:status       bank:Completed ;
       bank:authCode     "AUT-88123" ;
       bank:eventType    bank:BillPaymentEvent |} .

# -------------------------------------------------------
# EVENT 4 — Loan Request
# The application resource is the durable artefact;
# the reifier captures the submission event metadata.
# -------------------------------------------------------

loan:APP-2026-0881 a bank:LoanApplication ;
    bank:applicant      cust:alice ;
    bank:loanType       bank:PersonalLoan ;
    bank:requestedAmount "25000.00"^^xsd:decimal ;
    bank:currency        "USD" ;
    bank:termMonths      "60"^^xsd:integer .

cust:alice bank:submittedLoanApplication loan:APP-2026-0881
    ~ ev:loan-req-001
    {| bank:session      sess:S-20260303-C00441 ;
       bank:timestamp    "2026-03-03T09:06:45Z"^^xsd:dateTime ;
       bank:reviewedBy   bank:AutoUnderwritingEngine ;
       bank:status       bank:UnderReview ;
       bank:eventType    bank:LoanApplicationEvent |} .
```

---

### Design rationales

**Base triple vs. reifier separation.** The base triple states the _durable fact_ — Alice is a customer, the payment happened, the loan exists. The reifier carries the _ephemeral event envelope_: when, how, with what outcome. That maps cleanly onto an API where `POST /payments` creates the base resource, and the event log is a side-effect.

**The session as context graph.** `sess:S-20260303-C00441` is the temporal container; `ctx:CG-S-20260303-C00441` is the graph-level handle that groups `ev:*` reifiers. In a programmatic API, you’d retrieve the context graph to replay or audit the full session without needing to scan all triples for a customer.

**Named reifiers over anonymous** `{| |}` — because each event needs to be independently addressable. Anonymous annotation would work for provenance-only metadata (source, confidence) where you never need to JOIN on the annotation node. For API events, you always need that handle.

`bank:eventType` **as the API operation discriminator.** Rather than using `rdf:type` on the reifier directly, keeping `bank:eventType` as an annotation property means a SPARQL query can filter by event type without needing to pattern-match against the reifier class hierarchy — cleaner for the programmatic layer.

Once this is stored, you can retrieve a listing of events, their associated timestamp and their current status, as follows:

**SPARQL retrieval pattern**

```
PREFIX bank: <https://example.bank/ontology#>
PREFIX cust: <https://example.bank/customer/>
PREFIX sess: <https://example.bank/session/>

SELECT ?event ?type ?timestamp ?status WHERE {
    ?s rdf:reifies <<( cust:alice ?p ?o )>> .
    ?s bank:session     sess:S-20260303-C00441 ;
       bank:eventType   ?type ;
       bank:timestamp   ?timestamp .
    OPTIONAL { ?s bank:status ?status }
    BIND(?s AS ?event)
}
ORDER BY ?timestamp
```

This gives you the full event timeline for the session — the natural backing query for a `GET /sessions/{id}/events` endpoint.

## Creating Banking Shapes

The following Turtle identifies the SHACL Shapes and rules for the banking scenario. Apologies for the length, but this should provide some indication not only of the structures of the entities and events but also of the rules that enable new property generation.

```
# =============================================================================
# bank-context-graph-shapes.ttl
# SHACL 1.2 Shape Graph — Banking Context Graph / Event Reification
#
# Covers: Customer, CheckingAccount, BankingSession, ContextGraph,
#         BillPayment, LoanApplication, and per-event reifier shapes
#         for Authentication, Balance Enquiry, Bill Payment, Loan Application.
#
# SHACL 1.2 features used:
#   sh:reifierShape      — validates annotation nodes on RDF-Star reified triples
#   sh:SPARQLRule        — derives inferred triples from event patterns
#   sh:node              — single-shape inheritance for reifier base shape
#   sh:prefixes          — shared prefix declarations for SPARQL rules
# =============================================================================

@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:       <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:        <http://www.w3.org/2002/07/owl#> .
@prefix xsd:        <http://www.w3.org/2001/XMLSchema#> .
@prefix sh:         <http://www.w3.org/ns/shacl#> .
@prefix bank:       <https://example.bank/ontology#> .
@prefix ctx:        <https://example.bank/context#> .
@prefix bank-shape: <https://example.bank/shape#> .

# =============================================================================
# SHARED PREFIX DECLARATIONS
# Referenced by sh:prefixes in all SPARQL rules
# =============================================================================

bank-shape:PrefixDeclarations
    a owl:Ontology ;
    rdfs:label "Bank Shape Graph Prefix Declarations" ;
    sh:declare
        [ sh:prefix "rdf"  ; sh:namespace "http://www.w3.org/1999/02/22-rdf-syntax-ns#"^^xsd:anyURI ] ,
        [ sh:prefix "xsd"  ; sh:namespace "http://www.w3.org/2001/XMLSchema#"^^xsd:anyURI ] ,
        [ sh:prefix "bank" ; sh:namespace "https://example.bank/ontology#"^^xsd:anyURI ] ,
        [ sh:prefix "ctx"  ; sh:namespace "https://example.bank/context#"^^xsd:anyURI ] .


# =============================================================================
# BASE REIFIER SHAPE
# Abstract shape inherited by all per-event reifier shapes via sh:node.
# Validates the annotation envelope common to every event type:
#   bank:session, bank:timestamp, bank:eventType
# =============================================================================

bank-shape:BaseEventReifierShape
    a sh:NodeShape ;
    rdfs:label "Base Event Reifier Shape" ;
    sh:message "All event reifiers must carry exactly one bank:session, bank:timestamp, and bank:eventType." ;

    sh:property bank-shape:ReifierSessionProperty ;
    sh:property bank-shape:ReifierTimestampProperty ;
    sh:property bank-shape:ReifierEventTypeProperty .

bank-shape:ReifierSessionProperty
    a sh:PropertyShape ;
    rdfs:label "Reifier Session Reference" ;
    sh:path bank:session ;
    sh:class bank:BankingSession ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "Every event reifier must reference exactly one bank:BankingSession via bank:session." .

bank-shape:ReifierTimestampProperty
    a sh:PropertyShape ;
    rdfs:label "Reifier Event Timestamp" ;
    sh:path bank:timestamp ;
    sh:datatype xsd:dateTime ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "Every event reifier must carry exactly one xsd:dateTime via bank:timestamp." .

bank-shape:ReifierEventTypeProperty
    a sh:PropertyShape ;
    rdfs:label "Reifier Event Type" ;
    sh:path bank:eventType ;
    sh:nodeKind sh:IRI ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "Every event reifier must carry exactly one IRI via bank:eventType." .


# =============================================================================
# REIFIER SHAPE: Authentication Event
# Validates the reifier node on triples matching:
#   ?customer bank:authenticatedWith ?system
# =============================================================================

bank-shape:AuthEventReifierShape
    a sh:NodeShape ;
    rdfs:label "Authentication Event Reifier Shape" ;
    sh:message "Authentication event reifiers must satisfy the base event envelope and carry authMethod and outcome." ;

    # Inherit base envelope constraints
    sh:node bank-shape:BaseEventReifierShape ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Authentication Method" ;
        sh:path bank:authMethod ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( bank:BiometricMFA bank:PasswordMFA bank:TokenMFA bank:PIN ) ;
        sh:message "bank:authMethod must be one of bank:BiometricMFA, bank:PasswordMFA, bank:TokenMFA, or bank:PIN."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Authentication Outcome" ;
        sh:path bank:outcome ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( bank:Success bank:Failure bank:Locked ) ;
        sh:message "bank:outcome must be bank:Success, bank:Failure, or bank:Locked."
    ] ;

    # Event type pin: reifier must carry exactly bank:AuthenticationEvent
    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Event Type Pin (Authentication)" ;
        sh:path bank:eventType ;
        sh:hasValue bank:AuthenticationEvent ;
        sh:message "bank:eventType on an authentication reifier must be bank:AuthenticationEvent."
    ] .


# =============================================================================
# REIFIER SHAPE: Balance Enquiry Event
# Validates the reifier node on triples matching:
#   ?customer bank:queriedBalance ?account
# =============================================================================

bank-shape:BalanceEnquiryReifierShape
    a sh:NodeShape ;
    rdfs:label "Balance Enquiry Reifier Shape" ;
    sh:message "Balance enquiry reifiers must satisfy the base event envelope and carry balanceReturned and currency." ;

    sh:node bank-shape:BaseEventReifierShape ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Balance Returned" ;
        sh:path bank:balanceReturned ;
        sh:datatype xsd:decimal ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "bank:balanceReturned must be exactly one xsd:decimal value."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Balance Currency" ;
        sh:path bank:currency ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:pattern "^[A-Z]{3}$" ;
        sh:message "bank:currency must be an ISO 4217 three-letter currency code."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Event Type Pin (Balance Enquiry)" ;
        sh:path bank:eventType ;
        sh:hasValue bank:BalanceEnquiryEvent ;
        sh:message "bank:eventType on a balance enquiry reifier must be bank:BalanceEnquiryEvent."
    ] .


# =============================================================================
# REIFIER SHAPE: Bill Payment Event
# Validates the reifier node on triples matching:
#   ?customer bank:initiatedPayment ?payment
# =============================================================================

bank-shape:BillPaymentReifierShape
    a sh:NodeShape ;
    rdfs:label "Bill Payment Reifier Shape" ;
    sh:message "Bill payment reifiers must satisfy the base event envelope and carry fromAccount, status, and authCode." ;

    sh:node bank-shape:BaseEventReifierShape ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Payment Source Account" ;
        sh:path bank:fromAccount ;
        sh:class bank:CheckingAccount ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "bank:fromAccount must reference exactly one bank:CheckingAccount."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Payment Status" ;
        sh:path bank:status ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( bank:Completed bank:Pending bank:Failed bank:Reversed ) ;
        sh:message "bank:status must be bank:Completed, bank:Pending, bank:Failed, or bank:Reversed."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Payment Authorisation Code" ;
        sh:path bank:authCode ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:pattern "^AUT-[0-9]{5}$" ;
        sh:message "bank:authCode must match pattern AUT-NNNNN."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Event Type Pin (Bill Payment)" ;
        sh:path bank:eventType ;
        sh:hasValue bank:BillPaymentEvent ;
        sh:message "bank:eventType on a bill payment reifier must be bank:BillPaymentEvent."
    ] .


# =============================================================================
# REIFIER SHAPE: Loan Application Event
# Validates the reifier node on triples matching:
#   ?customer bank:submittedLoanApplication ?application
# =============================================================================

bank-shape:LoanApplicationReifierShape
    a sh:NodeShape ;
    rdfs:label "Loan Application Reifier Shape" ;
    sh:message "Loan application reifiers must satisfy the base event envelope and carry reviewedBy and status." ;

    sh:node bank-shape:BaseEventReifierShape ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Reviewing Agent" ;
        sh:path bank:reviewedBy ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "bank:reviewedBy must reference exactly one IRI (underwriting agent or automated system)."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Application Status" ;
        sh:path bank:status ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( bank:UnderReview bank:Approved bank:Rejected bank:Withdrawn ) ;
        sh:message "bank:status must be bank:UnderReview, bank:Approved, bank:Rejected, or bank:Withdrawn."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Event Type Pin (Loan Application)" ;
        sh:path bank:eventType ;
        sh:hasValue bank:LoanApplicationEvent ;
        sh:message "bank:eventType on a loan application reifier must be bank:LoanApplicationEvent."
    ] .


# =============================================================================
# NODE SHAPE: Customer
# =============================================================================

bank-shape:CustomerShape
    a sh:NodeShape ;
    sh:targetClass bank:Customer ;
    rdfs:label "Customer Shape" ;
    sh:message "A bank:Customer must carry a valid customerId, fullName, and riskTier." ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Customer ID" ;
        sh:path bank:customerId ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:pattern "^C-[0-9]{5}$" ;
        sh:message "bank:customerId must be exactly one xsd:string matching pattern C-NNNNN."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Customer Full Name" ;
        sh:path bank:fullName ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minLength 2 ;
        sh:message "bank:fullName must be exactly one non-empty string of at least 2 characters."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Customer Risk Tier" ;
        sh:path bank:riskTier ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( bank:StandardRisk bank:ElevatedRisk bank:HighRisk ) ;
        sh:message "bank:riskTier must be one of bank:StandardRisk, bank:ElevatedRisk, or bank:HighRisk."
    ] ;

    # ----------------------------------------------------------------
    # Event-carrying property shapes — each links to its reifier shape
    # via sh:reifierShape (SHACL 1.2)
    # ----------------------------------------------------------------

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Authentication Event Link" ;
        sh:path bank:authenticatedWith ;
        sh:nodeKind sh:IRI ;
        sh:minCount 0 ;
        sh:reifierShape bank-shape:AuthEventReifierShape ;
        sh:message "bank:authenticatedWith triples must have reifiers conforming to AuthEventReifierShape."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Balance Enquiry Event Link" ;
        sh:path bank:queriedBalance ;
        sh:class bank:CheckingAccount ;
        sh:minCount 0 ;
        sh:reifierShape bank-shape:BalanceEnquiryReifierShape ;
        sh:message "bank:queriedBalance triples must have reifiers conforming to BalanceEnquiryReifierShape."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Bill Payment Event Link" ;
        sh:path bank:initiatedPayment ;
        sh:class bank:BillPayment ;
        sh:minCount 0 ;
        sh:reifierShape bank-shape:BillPaymentReifierShape ;
        sh:message "bank:initiatedPayment triples must have reifiers conforming to BillPaymentReifierShape."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Loan Application Event Link" ;
        sh:path bank:submittedLoanApplication ;
        sh:class bank:LoanApplication ;
        sh:minCount 0 ;
        sh:reifierShape bank-shape:LoanApplicationReifierShape ;
        sh:message "bank:submittedLoanApplication triples must have reifiers conforming to LoanApplicationReifierShape."
    ] .


# =============================================================================
# NODE SHAPE: CheckingAccount
# =============================================================================

bank-shape:CheckingAccountShape
    a sh:NodeShape ;
    sh:targetClass bank:CheckingAccount ;
    rdfs:label "Checking Account Shape" ;
    sh:message "A bank:CheckingAccount must carry accountHolder, masked accountNumber, and currency." ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Account Holder" ;
        sh:path bank:accountHolder ;
        sh:class bank:Customer ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "bank:accountHolder must reference exactly one bank:Customer."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Masked Account Number" ;
        sh:path bank:accountNumber ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:pattern "^\\*{4}[0-9]{4}$" ;
        sh:message "bank:accountNumber must be a masked number in the format ****NNNN."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Account Currency" ;
        sh:path bank:currency ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:pattern "^[A-Z]{3}$" ;
        sh:message "bank:currency must be an ISO 4217 three-letter code."
    ] .


# =============================================================================
# NODE SHAPE: BankingSession
# =============================================================================

bank-shape:BankingSessionShape
    a sh:NodeShape ;
    sh:targetClass bank:BankingSession ;
    rdfs:label "Banking Session Shape" ;
    sh:message "A bank:BankingSession must carry customer, channel, and startTime." ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Session Customer" ;
        sh:path bank:customer ;
        sh:class bank:Customer ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "bank:customer must reference exactly one bank:Customer."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Session Channel" ;
        sh:path bank:channel ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( bank:MobileApp bank:WebPortal bank:BranchTerminal bank:ATM bank:PhoneIVR ) ;
        sh:message "bank:channel must be one of the approved banking channel values."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Session Start Time" ;
        sh:path bank:startTime ;
        sh:datatype xsd:dateTime ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "bank:startTime must be exactly one xsd:dateTime."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Session IP Address" ;
        sh:path bank:ipAddress ;
        sh:datatype xsd:string ;
        sh:maxCount 1 ;
        sh:pattern "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$" ;
        sh:message "bank:ipAddress, when present, must be a valid IPv4 address."
    ] ;

    # ----------------------------------------------------------------
    # Rule 1 — Derive bank:isAuthenticated true when a successful
    #           authentication event exists in the session.
    # ----------------------------------------------------------------
    sh:rule [
        a sh:SPARQLRule ;
        rdfs:label "Derive Session Authenticated Status" ;
        sh:message "A session containing a successful authentication event is marked bank:isAuthenticated true." ;
        sh:prefixes bank-shape:PrefixDeclarations ;
        sh:construct """
            CONSTRUCT {
                $this bank:isAuthenticated true .
            }
            WHERE {
                $this a bank:BankingSession .
                ?reifier rdf:reifies <<( ?customer bank:authenticatedWith ?system )>> ;
                         bank:session $this ;
                         bank:outcome bank:Success .
            }
        """
    ] ;

    # ----------------------------------------------------------------
    # Rule 2 — Flag sessions containing a failed authentication
    #           event as bank:AuthFailureSession.
    # ----------------------------------------------------------------
    sh:rule [
        a sh:SPARQLRule ;
        rdfs:label "Flag Session With Failed Authentication" ;
        sh:message "Sessions containing a failed authentication event are typed as bank:AuthFailureSession." ;
        sh:prefixes bank-shape:PrefixDeclarations ;
        sh:construct """
            CONSTRUCT {
                $this a bank:AuthFailureSession .
            }
            WHERE {
                $this a bank:BankingSession .
                ?reifier rdf:reifies <<( ?customer bank:authenticatedWith ?system )>> ;
                         bank:session $this ;
                         bank:outcome bank:Failure .
            }
        """
    ] ;

    # ----------------------------------------------------------------
    # Rule 3 — Flag sessions that carry operational events
    #           (payment or loan) without a prior successful auth.
    #           Indicates replay attack or session hijack candidate.
    # ----------------------------------------------------------------
    sh:rule [
        a sh:SPARQLRule ;
        rdfs:label "Flag Unauthenticated Operational Activity" ;
        sh:message "A session with payment or loan events but no successful authentication is typed as bank:SuspiciousSession." ;
        sh:prefixes bank-shape:PrefixDeclarations ;
        sh:construct """
            CONSTRUCT {
                $this a bank:SuspiciousSession .
            }
            WHERE {
                $this a bank:BankingSession .
                ?opReifier rdf:reifies <<( ?customer ?opPredicate ?opObject )>> ;
                           bank:session $this ;
                           bank:eventType ?evType .
                FILTER (?evType IN (bank:BillPaymentEvent, bank:LoanApplicationEvent))
                FILTER NOT EXISTS {
                    ?authReifier rdf:reifies <<( ?customer bank:authenticatedWith ?system )>> ;
                                 bank:session $this ;
                                 bank:outcome bank:Success .
                }
            }
        """
    ] .


# =============================================================================
# NODE SHAPE: ContextGraph
# =============================================================================

bank-shape:ContextGraphShape
    a sh:NodeShape ;
    sh:targetClass ctx:ContextGraph ;
    rdfs:label "Context Graph Shape" ;
    sh:message "A ctx:ContextGraph must reference a session, a subject customer, and at least one event reifier." ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Context Graph Session" ;
        sh:path ctx:session ;
        sh:class bank:BankingSession ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "ctx:session must reference exactly one bank:BankingSession."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Context Graph Subject" ;
        sh:path ctx:subject ;
        sh:class bank:Customer ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "ctx:subject must reference exactly one bank:Customer."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Context Graph Events" ;
        sh:path ctx:events ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:message "ctx:events must list at least one event reifier IRI."
    ] ;

    # ----------------------------------------------------------------
    # Rule 4 — Derive ctx:eventCount as the cardinality of ctx:events.
    # ----------------------------------------------------------------
    sh:rule [
        a sh:SPARQLRule ;
        rdfs:label "Derive Context Graph Event Count" ;
        sh:message "Derives ctx:eventCount as the count of events listed in ctx:events." ;
        sh:prefixes bank-shape:PrefixDeclarations ;
        sh:construct """
            CONSTRUCT {
                $this ctx:eventCount ?count .
            }
            WHERE {
                {
                    SELECT $this (COUNT(?event) AS ?count) WHERE {
                        $this ctx:events ?event .
                    }
                    GROUP BY $this
                }
            }
        """
    ] ;

    # ----------------------------------------------------------------
    # Rule 5 — Derive ctx:containsHighRiskEvent true when the session
    #           includes a loan application requiring enhanced review.
    # ----------------------------------------------------------------
    sh:rule [
        a sh:SPARQLRule ;
        rdfs:label "Derive Context Graph High Risk Event Flag" ;
        sh:message "A context graph is flagged ctx:containsHighRiskEvent true when a member event links to a loan application requiring enhanced review." ;
        sh:prefixes bank-shape:PrefixDeclarations ;
        sh:construct """
            CONSTRUCT {
                $this ctx:containsHighRiskEvent true .
            }
            WHERE {
                $this ctx:events ?reifier .
                ?reifier rdf:reifies <<( ?customer bank:submittedLoanApplication ?app )>> .
                ?app bank:requiresEnhancedReview true .
            }
        """
    ] .


# =============================================================================
# NODE SHAPE: BillPayment
# =============================================================================

bank-shape:BillPaymentShape
    a sh:NodeShape ;
    sh:targetClass bank:BillPayment ;
    rdfs:label "Bill Payment Shape" ;
    sh:message "A bank:BillPayment must carry payee, referenceCode, amount, and currency." ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Payee Name" ;
        sh:path bank:payee ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minLength 1 ;
        sh:message "bank:payee must be exactly one non-empty string."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Payment Reference Code" ;
        sh:path bank:referenceCode ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "bank:referenceCode must be exactly one non-empty string."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Payment Amount" ;
        sh:path bank:amount ;
        sh:datatype xsd:decimal ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minExclusive 0 ;
        sh:message "bank:amount must be exactly one positive xsd:decimal."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Payment Currency" ;
        sh:path bank:currency ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:pattern "^[A-Z]{3}$" ;
        sh:message "bank:currency must be an ISO 4217 three-letter code."
    ] .


# =============================================================================
# NODE SHAPE: LoanApplication
# =============================================================================

bank-shape:LoanApplicationShape
    a sh:NodeShape ;
    sh:targetClass bank:LoanApplication ;
    rdfs:label "Loan Application Shape" ;
    sh:message "A bank:LoanApplication must carry applicant, loanType, requestedAmount, currency, and termMonths." ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Loan Applicant" ;
        sh:path bank:applicant ;
        sh:class bank:Customer ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "bank:applicant must reference exactly one bank:Customer."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Loan Type" ;
        sh:path bank:loanType ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( bank:PersonalLoan bank:MortgageLoan bank:AutoLoan bank:BusinessLoan ) ;
        sh:message "bank:loanType must be one of bank:PersonalLoan, bank:MortgageLoan, bank:AutoLoan, or bank:BusinessLoan."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Requested Loan Amount" ;
        sh:path bank:requestedAmount ;
        sh:datatype xsd:decimal ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minExclusive 0 ;
        sh:message "bank:requestedAmount must be exactly one positive xsd:decimal."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Loan Currency" ;
        sh:path bank:currency ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:pattern "^[A-Z]{3}$" ;
        sh:message "bank:currency must be an ISO 4217 three-letter code."
    ] ;

    sh:property [
        a sh:PropertyShape ;
        rdfs:label "Loan Term in Months" ;
        sh:path bank:termMonths ;
        sh:datatype xsd:integer ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minInclusive 6 ;
        sh:maxInclusive 360 ;
        sh:message "bank:termMonths must be an integer between 6 and 360 inclusive."
    ] ;

    # ----------------------------------------------------------------
    # Rule 6 — Derive bank:requiresEnhancedReview true when
    #           requestedAmount > 50000 and the applicant is
    #           bank:StandardRisk.  Triggers Rule 5 on ContextGraph.
    # ----------------------------------------------------------------
    sh:rule [
        a sh:SPARQLRule ;
        rdfs:label "Flag High-Value Loan from Standard Risk Customer" ;
        sh:message "Loan applications over 50000 from a bank:StandardRisk customer are flagged bank:requiresEnhancedReview true." ;
        sh:prefixes bank-shape:PrefixDeclarations ;
        sh:construct """
            CONSTRUCT {
                $this bank:requiresEnhancedReview true .
            }
            WHERE {
                $this a bank:LoanApplication ;
                      bank:applicant ?customer ;
                      bank:requestedAmount ?amount .
                ?customer bank:riskTier bank:StandardRisk .
                FILTER (?amount > 50000)
            }
        """
    ] ;

    # ----------------------------------------------------------------
    # Rule 7 — Derive bank:requiresEnhancedReview true for any
    #           loan from an ElevatedRisk or HighRisk customer,
    #           regardless of amount.
    # ----------------------------------------------------------------
    sh:rule [
        a sh:SPARQLRule ;
        rdfs:label "Flag Any Loan from Elevated or High Risk Customer" ;
        sh:message "Any loan application from a bank:ElevatedRisk or bank:HighRisk customer is flagged bank:requiresEnhancedReview true." ;
        sh:prefixes bank-shape:PrefixDeclarations ;
        sh:construct """
            CONSTRUCT {
                $this bank:requiresEnhancedReview true .
            }
            WHERE {
                $this a bank:LoanApplication ;
                      bank:applicant ?customer .
                ?customer bank:riskTier ?tier .
                FILTER (?tier IN (bank:ElevatedRisk, bank:HighRisk))
            }
        """
    ] .

# =============================================================================
# End of bank-context-graph-shapes.ttl
# =============================================================================
```

## Summary

This illustrates the notion of **event traces**: when an event occurs, the system creates a description of that event, with durable facts providing the foundation, while the reifications establish additional contextual metadata about the event that inform it.

Note that this view of context graphs differs from traditional knowledge graphs, but it is also a more generalised form of what’s often discussed as decision support context graphs. This view is more audit-oriented; it will tell you which actions precipitated the events and their provenance. However, in both cases, you’re typically talking about decisions being made (if a loan was approved, who made the decision to approve it, why, and what the approval history is for that process).

The other thing to note here is that this context graph is much closer to an application than to simply an encyclopedic store of facts. It is also an append-only architecture: you are adding new content to the context graph non-destructively, rather than changing the state of properties. This aligns with many other architectural approaches.

I’ll be exploring this theme in more depth in upcoming posts.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!6te-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddac7c96-f8a6-437b-b7c9-51ec6a18acd9_2048x2048.jpeg)



](https://substackcdn.com/image/fetch/$s_!6te-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddac7c96-f8a6-437b-b7c9-51ec6a18acd9_2048x2048.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)  
[The Ontologist](https://ontologist.substack.com/)

