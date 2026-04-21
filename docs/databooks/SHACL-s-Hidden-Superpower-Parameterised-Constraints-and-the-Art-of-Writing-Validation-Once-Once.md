---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: SHACL-s-Hidden-Superpower-Parameterised-Constraints-and-the-Art-of-Writing-Validation-Once-Once
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:05.429189+00:00'
  title: Shacl’s hidden superpower parameterised constraints and the art of writing
    validation once
  type: plain-doc
  version: '0.1'
---

## Building a Realistic Component Library

The address example is instructive precisely because international postal addresses don’t just vary in _which pattern is valid_ — they vary in _which fields must exist_, which are _forbidden_, and whether those fields are _required or optional_. That requires three separate components working in concert.

### The Required Property Component

```
ex:RequiredPropertyConstraint a sh:ConstraintComponent ;
  sh:parameter [
    sh:path     ex:requiredProperty ;
    sh:nodeKind sh:IRI ;
    sh:name     "requiredProperty" ;
  ] ;
  sh:parameter [
    sh:path     ex:missingPropertyMessage ;
    sh:datatype xsd:string ;
    sh:name     "missingPropertyMessage" ;
    sh:description """
      Optional message template. Use {property} as a placeholder
      for the property IRI. If omitted, a default message is generated.
    """ ;
    sh:optional true ;
  ] ;
  sh:validator ex:RequiredPropertySelectValidator .

ex:RequiredPropertySelectValidator a sh:SPARQLSelectValidator ;
  sh:select """
    SELECT $this ?value ?message WHERE {
      OPTIONAL { $this $requiredProperty ?value . }
      BIND(
        IF( !BOUND(?value) || STR(?value) = "",
          IF( BOUND($missingPropertyMessage),
            REPLACE( $missingPropertyMessage,
                     "\\{property\\}", STR($requiredProperty) ),
            CONCAT("Required field <", STR($requiredProperty),
                   "> is missing on <", STR($this), ">.")
          ),
          ""
        )
        AS ?message
      )
      FILTER( ?message != "" )
    }
  """ .
```

Note the `$missingPropertyMessage` parameter: the message template is itself a parameter, which means each shape can supply domain-appropriate wording — including in languages other than English — without touching the validator logic. This is the meta-move that turns a validation tool into a data quality communication layer.

### The Forbidden Property Component

```
ex:ForbiddenPropertyConstraint a sh:ConstraintComponent ;
  sh:parameter [
    sh:path     ex:forbiddenProperty ;
    sh:nodeKind sh:IRI ;
    sh:name     "forbiddenProperty" ;
  ] ;
  sh:parameter [
    sh:path     ex:addressTypeName ;
    sh:datatype xsd:string ;
    sh:name     "addressTypeName" ;
    sh:optional true ;
  ] ;
  sh:validator ex:ForbiddenPropertySelectValidator .

ex:ForbiddenPropertySelectValidator a sh:SPARQLSelectValidator ;
  sh:select """
    SELECT $this ?value ?message WHERE {
      OPTIONAL { $this $forbiddenProperty ?value . }
      BIND(
        IF( BOUND(?value),
          CONCAT(
            "Field <", STR($forbiddenProperty), ">",
            " is not permitted on a ",
            IF( BOUND($addressTypeName), $addressTypeName, "this" ),
            " address. Found value: '", STR(?value), "'.",
            " Node: <", STR($this), ">."
          ),
          ""
        )
        AS ?message
      )
      FILTER( ?message != "" )
    }
  """ .
```

### Three Shapes, Three Structures, Same Components

```
ex:USAddressShape a sh:NodeShape ;
  sh:targetClass ex:USAddress ;

  ex:requiredProperty        ex:streetLine1 ;
  ex:requiredProperty        ex:city ;
  ex:requiredProperty        ex:state ;
  ex:requiredProperty        ex:zipCode ;
  ex:missingPropertyMessage  "US addresses require a two-letter state code. \
                              Field {property} is missing." ;

  ex:constrainedProperty     ex:state ;
  ex:matchPattern            "^[A-Z]{2}$" ;

  ex:constrainedProperty     ex:zipCode ;
  ex:matchPattern            "^[0-9]{5}(-[0-9]{4})?$" ;

  ex:forbiddenProperty       ex:postcode ;
  ex:forbiddenProperty       ex:postalCode ;
  ex:addressTypeName         "US" ;

  sh:property [
    sh:path ex:countryCode ;
    sh:hasValue "US" ;
  ] .


ex:UKAddressShape a sh:NodeShape ;
  sh:targetClass ex:UKAddress ;

  ex:requiredProperty        ex:streetLine1 ;
  ex:requiredProperty        ex:city ;
  ex:requiredProperty        ex:postcode ;
  ex:missingPropertyMessage
    "UK addresses must include a valid Royal Mail postcode. \
     Field {property} is absent. Example: 'SW1A 2AA'." ;

  ex:constrainedProperty     ex:postcode ;
  ex:matchPattern            "^[A-Z]{1,2}[0-9][0-9A-Z]?\\s?[0-9][A-Z]{2}$" ;

  ex:forbiddenProperty       ex:state ;
  ex:forbiddenProperty       ex:zipCode ;
  ex:forbiddenProperty       ex:postalCode ;
  ex:addressTypeName         "UK" ;

  sh:property [
    sh:path ex:countryCode ;
    sh:hasValue "GB" ;
  ] .


ex:DEAddressShape a sh:NodeShape ;
  sh:targetClass ex:DEAddress ;

  ex:requiredProperty        ex:streetLine1 ;
  ex:requiredProperty        ex:postalCode ;
  ex:requiredProperty        ex:city ;
  ex:missingPropertyMessage
    "Deutsche Adressen erfordern eine fünfstellige Postleitzahl. \
     Feld {property} fehlt." ;

  ex:constrainedProperty     ex:postalCode ;
  ex:matchPattern            "^[0-9]{5}$" ;

  ex:constrainedProperty     ex:bundesland ;
  ex:matchPattern            "^.{3,50}$" ;
  ex:patternOptional         true ;

  ex:forbiddenProperty       ex:state ;
  ex:forbiddenProperty       ex:zipCode ;
  ex:forbiddenProperty       ex:postcode ;
  ex:addressTypeName         "DE" ;

  sh:property [
    sh:path ex:countryCode ;
    sh:hasValue "DE" ;
  ] .
```

The structural variation across the three shapes is substantial: US requires `ex:state` and forbids `ex:postcode`; UK requires `ex:postcode` and forbids `ex:state`; German requires `ex:postalCode` (a different property from both) with a different pattern, has an optional `ex:bundesland` with a minimum length, and forbids both of the others. Three entirely different structural profiles — and the whole apparatus runs on three components written once.

### Sample Data — Valid Instances

With the shapes declared, here is conformant data for each address type. Each instance satisfies every active constraint in its shape.

```
@prefix ex:   <https://example.org/ns/constraint#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

# ── US — valid ────────────────────────────────────────────────────

# Standard five-digit ZIP
ex:Address_US_001 a ex:USAddress ;
  ex:streetLine1 "742 Evergreen Terrace" ;
  ex:city        "Springfield" ;
  ex:state       "IL" ;
  ex:zipCode     "62701" ;
  ex:countryCode "US" .

# ZIP+4 extended format — also valid against the pattern
ex:Address_US_002 a ex:USAddress ;
  ex:streetLine1 "1600 Pennsylvania Avenue NW" ;
  ex:city        "Washington" ;
  ex:state       "DC" ;
  ex:zipCode     "20500-0003" ;
  ex:countryCode "US" .


# ── UK — valid ────────────────────────────────────────────────────

# Minimal required fields only
ex:Address_UK_001 a ex:UKAddress ;
  ex:streetLine1 "221B Baker Street" ;
  ex:city        "London" ;
  ex:postcode    "NW1 6XE" ;
  ex:countryCode "GB" .

# With optional county — field is permitted, no pattern constraint applies
ex:Address_UK_002 a ex:UKAddress ;
  ex:streetLine1 "4 Privet Drive" ;
  ex:city        "Little Whinging" ;
  ex:county      "Surrey" ;
  ex:postcode    "GU25 4PJ" ;
  ex:countryCode "GB" .


# ── German — valid ────────────────────────────────────────────────

# House number on the street line — correct German convention
ex:Address_DE_001 a ex:DEAddress ;
  ex:streetLine1 "Unter den Linden 77" ;
  ex:postalCode  "10117" ;
  ex:city        "Berlin" ;
  ex:countryCode "DE" .

# With optional Bundesland — value is 6 chars, satisfies ^.{3,50}$
ex:Address_DE_002 a ex:DEAddress ;
  ex:streetLine1 "Marienplatz 1" ;
  ex:postalCode  "80331" ;
  ex:city        "München" ;
  ex:bundesland  "Bayern" ;
  ex:countryCode "DE" .
```

Every one of these passes validation cleanly. The US addresses have correctly-cased two-letter state codes and numeric ZIP codes; neither carries `ex:postcode` or `ex:postalCode`. The UK addresses carry `ex:postcode` in Royal Mail format and no US or German fields. The German addresses carry `ex:postalCode` (a distinct property from `ex:zipCode`) with a five-digit value, and the second carries `ex:bundesland` with a value long enough to satisfy the minimum-length pattern.

### Sample Data — Invalid Instances and What the Validator Says

Now for the instructive part. One failure per shape, illustrating each of the three failure modes: pattern mismatch, required field missing, and forbidden field present.

```
# ── US failures ───────────────────────────────────────────────────

# Pattern failure: state is lowercase — violates ^[A-Z]{2}$
ex:Address_US_BAD_001 a ex:USAddress ;
  ex:streetLine1 "100 Main Street" ;
  ex:city        "Portland" ;
  ex:state       "or" ;           # should be "OR"
  ex:zipCode     "97201" ;
  ex:countryCode "US" .

# Pattern failure: ZIP contains a letter — violates ^[0-9]{5}(-[0-9]{4})?$
ex:Address_US_BAD_002 a ex:USAddress ;
  ex:streetLine1 "100 Main Street" ;
  ex:city        "Portland" ;
  ex:state       "OR" ;
  ex:zipCode     "9720X" ;        # not numeric
  ex:countryCode "US" .

# Forbidden field: carries ex:postcode — UK field, forbidden on USAddress
ex:Address_US_BAD_003 a ex:USAddress ;
  ex:streetLine1 "100 Main Street" ;
  ex:city        "Portland" ;
  ex:state       "OR" ;
  ex:zipCode     "97201" ;
  ex:postcode    "NW1 6XE" ;      # forbidden
  ex:countryCode "US" .


# ── UK failures ───────────────────────────────────────────────────

# Missing required field: no postcode at all
ex:Address_UK_BAD_001 a ex:UKAddress ;
  ex:streetLine1 "10 Downing Street" ;
  ex:city        "London" ;
  ex:countryCode "GB" .

# Pattern failure: postcode in lowercase without space
ex:Address_UK_BAD_002 a ex:UKAddress ;
  ex:streetLine1 "10 Downing Street" ;
  ex:city        "London" ;
  ex:postcode    "sw1a2aa" ;      # should be "SW1A 2AA"
  ex:countryCode "GB" .

# Forbidden field: carries ex:state — US field, forbidden on UKAddress
ex:Address_UK_BAD_003 a ex:UKAddress ;
  ex:streetLine1 "10 Downing Street" ;
  ex:city        "London" ;
  ex:postcode    "SW1A 2AA" ;
  ex:state       "LN" ;           # forbidden
  ex:countryCode "GB" .


# ── German failures ───────────────────────────────────────────────

# Pattern failure: postalCode is 4 digits — violates ^[0-9]{5}$
ex:Address_DE_BAD_001 a ex:DEAddress ;
  ex:streetLine1 "Kurfürstendamm 100" ;
  ex:postalCode  "1011" ;         # one digit short
  ex:city        "Berlin" ;
  ex:countryCode "DE" .

# Forbidden field: carries ex:zipCode — US property, forbidden on DEAddress
ex:Address_DE_BAD_002 a ex:DEAddress ;
  ex:streetLine1 "Kurfürstendamm 100" ;
  ex:postalCode  "10711" ;
  ex:zipCode     "10711" ;        # forbidden
  ex:city        "Berlin" ;
  ex:countryCode "DE" .

# Pattern failure on optional field: bundesland is 2 chars, below ^.{3,50}$ minimum
ex:Address_DE_BAD_003 a ex:DEAddress ;
  ex:streetLine1 "Kurfürstendamm 100" ;
  ex:postalCode  "10711" ;
  ex:city        "Berlin" ;
  ex:bundesland  "BE" ;           # 2 chars — violates minimum length
  ex:countryCode "DE" .
```

### Validation Report Output

The SELECT validators construct their messages from actual data values, so each violation is immediately actionable — the report tells you the node, the property, the offending value, and why it failed. This is what the validation engine returns:

[

![](https://substackcdn.com/image/fetch/$s_!REH7!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5de5d38a-f1fa-4499-9e48-0beede91b858_1541x997.png)



](https://substackcdn.com/image/fetch/$s_!REH7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5de5d38a-f1fa-4499-9e48-0beede91b858_1541x997.png)

Two things are worth noting in this table. First, `Address_UK_BAD_001`‘s message is in a completely different register from the others — it cites Royal Mail convention and offers an example value, because that message template was supplied directly in `ex:UKAddressShape`. The German shape supplies its missing-field message in German. The validator logic is identical for all three; the communication layer is different. This is the `$missingPropertyMessage` parameter doing its job.

Second, `Address_DE_BAD_003` demonstrates the optional field pattern working correctly. `ex:bundesland` is declared with `ex:patternOptional true` — its _absence_ does not trigger a violation. But its _presence_ with an invalid value does. The validator distinguishes between “field is absent and that’s fine” and “field is present and wrong”. Both cases are handled by a single `OPTIONAL { ... }` clause in the SELECT query.

---

## ASK vs SELECT Validators

The choice between `sh:SPARQLAskValidator` and `sh:SPARQLSelectValidator` follows a single principle: how much do you need to say about the failure?

`sh:SPARQLAskValidator` returns a boolean. It is appropriate when the violation type is self-explanatory and the static `sh:message` string (which supports `{$param}` interpolation) provides enough context. It is fast, readable, and easy to test.

```
ex:SimpleRangeValidator a sh:SPARQLAskValidator ;
  sh:message
    "Value of {$measuredProperty} must be between {$minValue} and {$maxValue}." ;
  sh:ask """
    ASK {
      $this $measuredProperty ?v .
      FILTER( ?v >= $minValue && ?v <= $maxValue )
    }
  """ .
```

`sh:SPARQLSelectValidator` returns rows — one per violation, each with `$this`, `?value`, and `?message`. It is appropriate when the message needs to be constructed from the actual data values, not just the parameters. The `BIND( ... AS ?message )` pattern with a `FILTER( ?message != "" )` is the standard idiom: compute a message string if a violation exists, return an empty string otherwise, and filter to rows where something went wrong.

```
ex:DetailedRangeValidator a sh:SPARQLSelectValidator ;
  sh:select """
    SELECT $this ?value ?message WHERE {
      $this $measuredProperty ?value .
      BIND(
        IF( ?value < $minValue,
          CONCAT("Value ", STR(?value), " is below minimum ",
                 STR($minValue), " for <", STR($this), ">"),
          IF( ?value > $maxValue,
            CONCAT("Value ", STR(?value), " exceeds maximum ",
                   STR($maxValue), " for <", STR($this), ">"),
            ""
          )
        )
        AS ?message
      )
      FILTER( ?message != "" )
    }
  """ .
```

The SELECT validator tells you the node, the actual offending value, and why it is wrong — not just that something is wrong. In a system where validation reports are surfaced to downstream consumers, a UI, or a regulatory audit, the difference matters.

---

## A Candidate Library

Across real-world domains, the same structural patterns recur. The following are strong candidates for parameterisation — families where the logic is identical across instances and only the values differ.

**Lexical pattern validation.** Postcodes, phone numbers, identifiers, currency codes, NPI numbers, ISBNs, IBANs, registration codes. Always the same structure: does the value of property X match regex Z? One component, supply property and pattern per shape.

**Numeric ranges with optional units.** Blood pressure, temperature, financial limits, dosage bounds, weight thresholds, engineering tolerances. Parameterise the measured property, min/max bounds, and optionally the expected unit IRI.

**Cardinality across property sets.** The native `sh:minCount`/`sh:maxCount` applies to a single property per `sh:property` block. Cross-property constraints — _“at least one of email, phone, or postal address must be present”_, _“exactly one of brandName or genericName”_ — are not natively expressible and are a natural component candidate.

**Temporal validity windows.** A resource is valid between two dates. Common in credentials, contracts, licences, pricing records, drug approvals. Parameterise the start-date property, the end-date property, and optionally a flag permitting open-ended validity.

**Referential integrity with typed targets.** Does a property value reference a node of the right type that satisfies a given shape? Parameterise the referencing property and the target shape IRI. Useful when the expected type of a referenced entity varies by context.

**Conditional presence.** _“If property A has value V, then property B is required.”_ This is `sh:if`/`sh:then` in SHACL 1.2, but as a parameterised component it becomes portable across any pair of properties in any shape. Employment status requiring salary range; diagnosis code requiring supporting documentation; payment method requiring account details.

**Mutual exclusivity.** Exactly one of a named set of properties may be present. Common in classification systems where multiple coding schemes exist but only one should be applied per record.

---

## Where Parameterisation Is Overkill

The case for parameterisation is not unlimited. There are clear patterns where the overhead is not warranted.

**When native SHACL handles it in under five lines.** `sh:minCount 1` on `foaf:name` is one line. Writing a `RequiredPropertyConstraint` to express the same thing adds thirty lines of infrastructure for zero gain. SHACL’s built-in constraint keywords — `sh:minCount`, `sh:maxCount`, `sh:datatype`, `sh:nodeKind`, `sh:class`, `sh:pattern` — are highly optimised and perfectly readable. The argument for a component only starts when native keywords cannot express the constraint or when the constraint recurs across many shapes.

**When the logic is genuinely unique.** Some constraints are specific to a single shape and will never recur. The internal structure of a SWIFT MT103 identifier field, or a regulatory-scheme-specific document reference format that exists in exactly one context, is not a parameterisation candidate. Write it inline. Wrapping unique logic in a component buys indirection with no reuse.

**When the SPARQL structure itself must vary, not just the values.** Parameterisation works when the same query shape runs with different bound variables. If the only way to reuse a validator would require changing the fundamental structure of the SPARQL query between uses — adding or removing joins, changing the aggregation strategy — you have identified two different logical families, not one. Write two components.

**When the schema is stable and closed-world.** A document type that has been standardised for decades with no structural variants is not a good parameterisation candidate. The payoff is handling variation; without variation, there is no payoff.

**In exploratory or prototype work.** If you are sketching a shape to answer a specific question about a specific dataset, the overhead of designing a correct, documented, tested constraint component is wasteful. Write the validator inline, get the answer, refactor later if the pattern recurs.

---

## The Decision Framework

Before writing any component, ask three questions in sequence:

**Does this constraint logic appear — or will it appear — across more than one shape?** If no, write it inline.

**Does it vary only in parameter values, or in query structure?** If the structure varies, you have two different families. Write two components.

**Is the domain stable enough that a reusable component won’t become a liability?** Rapid schema evolution can make components more expensive to maintain than inline validators, because a structural change to the component propagates everywhere it is used.

If all three answers are yes, parameterise. Otherwise, use the simplest tool that works.

A practical table:

[

![](https://substackcdn.com/image/fetch/$s_!5pir!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe40a08d9-0f06-4829-9aa0-4d7c17b35770_697x437.png)



](https://substackcdn.com/image/fetch/$s_!5pir!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe40a08d9-0f06-4829-9aa0-4d7c17b35770_697x437.png)

The four-parameter ceiling is a heuristic, not a rule, but it has intuitive backing: a component with five or six parameters typically indicates that it is doing two things, and the cure is decomposition rather than more parameters.

---

## The Meta- Level: Shapes as a Type System

When parameterised constraint components are used consistently across a domain, something shifts architecturally. The collection of components begins to look less like a validation library and more like a _schema language for the domain_ — a vocabulary of constraint families that can be composed into structural specifications.

The address example demonstrates this clearly. The three address shapes are not validation scripts. They are _type declarations_: a US address is a thing that has these required properties with these patterns, and must not have these other properties. The components are the grammar; the shapes are the sentences.

This reframing has a practical consequence: the shapes become the canonical answer to the question _“what does it mean for a US address to be valid?”_ They are readable by domain experts, auditable by compliance teams, and extensible by adding new shapes rather than modifying existing logic. Adding an Australian address type means writing one new shape that supplies parameters to existing components — no new validators, no new infrastructure.

There is a deeper connection here. In Active Inference terms — the framework that maps onto holonic knowledge representation — the domain graph layer is a Markov blanket: a normative boundary that separates what a thing is from what it is allowed to do and be. SHACL shapes are the formal expression of that boundary. Parameterised constraints make the boundary _compositional_ — you can build it from parts rather than declaring it monolithically for each type.

This is also where the limits of parameterisation become interesting. The dispatcher pattern — where a component’s parameter is itself a shape IRI, and the component validates that a referenced node conforms to the named shape — is the point at which SHACL starts to behave like a type system with runtime dispatch. The component declares a structural policy: _“this property’s value must conform to the shape appropriate for its type.”_ The shapes encode the type-specific structure. The SHACL engine is the type checker.

```
ex:SubSchemaConstraint a sh:ConstraintComponent ;
  sh:parameter [
    sh:path     ex:appliesShape ;
    sh:nodeKind sh:IRI ;
    sh:name     "appliesShape" ;
  ] ;
  sh:parameter [
    sh:path     ex:onProperty ;
    sh:nodeKind sh:IRI ;
    sh:name     "onProperty" ;
  ] ;
  sh:validator ex:SubSchemaValidator .

ex:SubSchemaValidator a sh:SPARQLAskValidator ;
  sh:ask """
    ASK {
      $this $onProperty ?nested .
      ?nested a ?type .
      ?appliesShape sh:targetClass ?type .
    }
  """ .
```

Whether this level of abstraction is appropriate depends entirely on whether the domain genuinely exhibits that kind of structural polymorphism. International postal addresses do. Medical device identifiers often do. A single-format internal identifier scheme does not.

---

## Implications for Best Practices

The following practices emerge from experience with parameterised constraint design at scale.

**Design components before shapes.** Before writing any Turtle, survey the constraints you need and ask which share a logical family. Components are harder to change after they are deployed — every shape that uses them is affected by a modification to the validator. Getting the component right before building twenty shapes on top of it is worth the design time.

**Write components with the rigour of library functions.** A parameterised component that has a subtle bug is more dangerous than an inline validator, because the bug is invisible and pervasive. Test every component against both known-valid and known-invalid data before deploying. Document each parameter’s semantics in `sh:description`. Make the `sh:labelTemplate` human-readable, so validation reports identify which component fired.

**Prefer SELECT validators for production systems.** ASK validators are faster to write and easier to read. SELECT validators produce validation reports that are actionable without additional context. For any system where validation output is consumed by downstream processes, a UI, or a compliance audit trail, the SELECT validator’s per-violation diagnostic messages are worth the extra lines.

**Use** `sh:optional true` **generously.** A component with an optional parameter that enables additional checks is more flexible than two separate components for the with-and-without cases. The `BOUND($param)` pattern in SPARQL handles optional parameters cleanly.

**Keep message templates in the shapes, not the components.** The component validator should generate a sensible default message when no template is supplied. But the message that domain experts, end users, or regulators actually see should live in the shape — which is where domain knowledge is declared. This is the `$missingPropertyMessage` pattern from the address example, and it is the right separation of concerns.

**Four parameters is a practical ceiling.** Beyond four, a component typically indicates that two different logical families have been conflated. Decompose before adding the fifth parameter.

**The library is infrastructure — treat it accordingly.** A constraint component library earns its place by being trustworthy and stable. Version it. Document it. Test it. A library of ten well-designed, thoroughly tested components is more valuable than a library of fifty hastily written ones.

---

## Conclusion

SHACL parameterised constraints are not a niche feature. They are the mechanism by which SHACL scales from a collection of per-type validation scripts into a composable, maintainable data quality infrastructure. The pattern is: identify the logical family, write the validator once, supply the varying values as parameters in each shape, and let the SHACL engine do the dispatch.

The address example — US, UK, and German addresses validated by the same three components with structurally different parameter sets — illustrates the payoff at small scale. At large scale, a domain with dozens of entity types and hundreds of constraints becomes significantly more tractable when the constraint logic is concentrated in a small, well-tested component library rather than distributed across hundreds of bespoke shapes.

The design discipline is real. Identifying the right families, keeping components focused, testing them thoroughly, and knowing when the pattern is overkill all require judgment that comes with practice. But the payoff — a constraint vocabulary that is readable, auditable, extensible, and maintainable — is exactly what data quality as an architectural concern looks like.

The key was always the logic. Whether you pick it up early depends on how many shapes you intend to write.

