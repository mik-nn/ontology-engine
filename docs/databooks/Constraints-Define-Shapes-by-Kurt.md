---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Constraints-Define-Shapes-by-Kurt
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:39.075759+00:00'
  title: Constraints Define Shapes By Kurt
  type: plain-doc
  version: '0.1'
---

# Constraints Define Shapes By Kurt

[

![](https://substackcdn.com/image/fetch/$s_!ZLnn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4b59d8a-f963-49ae-8a2c-f4104cb68a7a_2048x1168.jpeg)

](https://substackcdn.com/image/fetch/$s_!ZLnn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4b59d8a-f963-49ae-8a2c-f4104cb68a7a_2048x1168.jpeg)

In my previous post, I focused on the process of gathering the nodes to be validated by a SHACL node shape:

[

## SHACL Node Shapes and Target Nodes

](https://ontologist.substack.com/p/shacl-node-shapes-and-target-nodes)

·

Feb 8

[![SHACL Node Shapes and Target Nodes](https://substackcdn.com/image/fetch/$s_!_bm0!,w_1300,h_650,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdccf8290-bec7-49dc-bacd-87f2e0694de3_2688x1536.jpeg)](https://ontologist.substack.com/p/shacl-node-shapes-and-target-nodes)

I’m now actively working on a book, Context: The SHACL Revolution, based in great part on what I’m writing in the Ontologist. Its focus is on most of what’s coming in RDF 1.2, but it’s also intended to provide a detailed guide about what can be done with the technology, not just how it works. My target date for completion is in April of this year, and y…

[https://ontologist.substack.com/p/shacl-node-shapes-and-target-nodes](http://node%20shapes%20and%20target%20nodes/)

This post looks at the complementary part of SHACL - the Property Shape, in more depth, and also introduces validation reporting.

## What Property Shape Validation Does

Validation is often very much misunderstood by developers.

You can think of a validator as a checklist, a way of affirming that data meets your particular needs. For instance, when I leave my house to do grocery shopping for my family, I usually need to check several things:

-   Do I have my car keys (I may have someone else’s or may have just forgotten it)?
    
-   Do I have my cell phone (Ditto, primarily for grocery lists)?
    
-   Do I have my wallet (Same thing)
    
-   Do I have enough money in my account for groceries (Always critical)
    

We can model the Grocery Shopping Readiness node shape as follows:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.org/household/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

###########################################
# Node Shape: Grocery Shopping Readiness
###########################################

ex:GroceryShoppingReadinessShape
    a sh:NodeShape ;
    sh:targetClass ex:GroceryShoppingTrip ;
    sh:closed false ;
    sh:description "Validates that a person is ready to leave for grocery shopping" ;
    
    # Property 1: Car Keys
    sh:property ex:CarKeysPropertyShape ;
    
    # Property 2: Cell Phone
    sh:property ex:CellPhonePropertyShape ;
    
    # Property 3: Wallet
    sh:property ex:WalletPropertyShape ;
    
    # Property 4: Sufficient Funds
    sh:property ex:SufficientFundsPropertyShape ;
    
    # Overall readiness rule
    sh:rule ex:ReadinessCalculationRule ;
.
```

This indicates that the model is not closed (there may be additional properties or rules, but they aren’t indicated here, and that there are four properties (`ex:carKeysPropertyShape`, `ex:CellPhonePropertyShape`, `ex:WalletPropertyShape`, and `ex:SufficientFundsPropertyShape`), as well as one rule (`ex:ReadinessCalculationRule`).

This also applies to all instances of the `ex:GroceryShoppingTrip` class (meaning that more than one person ends up using this checklist). This means that these will be the nodes used for testing.

The car keys shape is pretty typical for a property shape:

```
###########################################
# Property Shape: Car Keys
###########################################

ex:CarKeysPropertyShape
    a sh:PropertyShape ;
    sh:path ex:hasCarKeys ;
    sh:name "Car Keys Check" ;
    sh:codeIdentifier "carKeysCheck" ;
    sh:description "Verify that you have YOUR car keys (not someone else's)" ;
    
    # Must have exactly one car key set
    sh:minCount 1 ;
    sh:maxCount 1 ;
    
    # Must be a CarKeys instance
    sh:class ex:CarKeys ;
.
```

The `sh:path` indicates the _**predicate path**_, given the current node being tested. This will usually be a single predicate, but in some cases it may be a modified path (see predicate paths), indicating things like the union of multiple paths, lists, inverse paths and so forth. The `sh:path` is the only item of a predicate shape that is required.

The predicate path is, as the name suggests, the path from the current target node (the subject) via a sequence of predicates in the graph to the corresponding object. Ordinarily, this will be a single predicate, such as `ex:hasCarKeys`. However, it can also be a compound expression, such as a linked list or a choice between two different predicate terms. This is covered in more detail below.

The `sh:name` and `sh:description` will usually be passed to the `sh:report` to describe what the Property Node is specifically attempting to validate, while the `sh:message` indicates the error message that should be sent to the report if the property and object constraints in the property shape are not matched.

The `sh:name` property was originally intended to be the human readable name of the property shape, but because early on SHACL was used specifically in conjunction with GraphQL, the `sh:name` became associated with the JSON property name. As such, it is occasionally used when an element is converted to JSON-LD, typically in the document's context section (I will cover JSON-LD and SHACL in an upcoming post).

In order to reclaim `sh:name`, SHACL 1.2 adds a new annotation property called `sh:codeIdentifier` (for instance, `[] sh:codeIdentifier “carKeysCheck”^^xsd:string` ). This serves the same purpose, while letting `sh:name` be used as a human-readable name (`[] sh:name “Car Keys Check”^^xsd:string`.

Having defined the annotations, let’s concentrate more on the constraints. A **constraint** is a limit of some sort. It may be a cardinality limit, a minimum or maximum value for an object, pattern requirements in strings, class membership, set membership or value, or more generalised limits. The reason SHACL is called the shape constraint language is that each constraint is a test applied to a node. In general, a constraint in SHACL is much like a FILTER in SPARQL - it is an expression that must be satisfied for the query to return a valid response, though in this case, this can be interpreted as a condition that must be satisfied to not generate an error message.

There are several key constraints even in this fairly simple example:

### Cardinality

The first two constraints focus on cardinality, with the sh:minCount and sh:maxCount properties:

```
# Must have exactly one car key set
    sh:minCount 1 ;
    sh:maxCount 1 ;
```

Typically, sh:minCount will be either zero (the property being described is optional) or one (you must have at least one instance). If sh:minCount is not listed, then its value is assumed to be 0 (as an integer).

On the other hand, sh:maxCount must have a minimum count of one, but if it’s not present, this is treated as sh:maxCount is unbounded (infinity, for all intents and purposes). This means if neither is included, then the cardinality of the property is 0:infinity - there’s no requirement to have the property, and no limitation on the number of objects that the property can have for a given subject.

It is possible to specify other values for both minCount and maxCount. For instance, there may be a limit on the number of items that can be carried (e.g., luggage at an airport).

### Ranges

There are additionally four range constraints: sh:minInclusive, sh:minExclusive, sh:maxInclusive, and sh:maxExclusive, respectively. These constraints work on integers, decimals, floats, doubles, dates, dateTimes, and durations. An inclusive range includes the specified lower or upper value, whereas an exclusive range excludes it.

[

![](https://substackcdn.com/image/fetch/$s_!_EiJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd4d112c-9ff5-483f-88eb-bae667f9b7fe_820x718.png)

](https://substackcdn.com/image/fetch/$s_!_EiJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd4d112c-9ff5-483f-88eb-bae667f9b7fe_820x718.png)

So, as an example, if you wanted to have a date restricted to the 2020s, you’d use the following:

```
Shape:TwentyTwentiesDate_PropertyShape a sh:PropertyShape ;
      sh:path ex:startDate ;
      sh:minInclusive "2020-01-01"^^xsd:date ;
      sh:maxExclusive "2030-01-01"^^xsd:date ;
      sh:datatype xsd:date ;
      sh:message "Start date must be in the 2020s (2020-01-01 to 2029-12-31)" ;
      .
```

This is equivalent to saying:

```
2020-01-10 <= ex:startDate < 2030-01-01
```

as a precondition. If the date is not in that range (e.g., `"2032-07-24"^^xsd:date"`) then the `sh:maxExclusive` constrain will generate an error, something like:

```
Validation Result:
  Severity: sh:Violation
  Source Shape: Shape:TwentyTwentiesDate_PropertyShape
  Focus Node: [blank node]
  Result Path: ex:startDate
  Value: "2032-07-24"^^xsd:date
  Message: Start date must be in the 2020s (2020-01-01 to 2029-12-31)
```

or, if the result is sent as Turtle:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.org/> .
@prefix Shape: <http://example.org/shapes/> .

[] a sh:ValidationReport ;
    sh:conforms false ;
    sh:result [
        a sh:ValidationResult ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:MaxExclusiveConstraintComponent ;
        sh:sourceShape Shape:TwentyTwentiesDate_PropertyShape ;
        sh:focusNode _:b0 ;  # The blank node from the data
        sh:resultPath ex:startDate ;
        sh:value "2032-07-24"^^xsd:date ;
        sh:resultMessage "Start date must be in the 2020s (2020-01-01 to 2029-12-31)" ;
    ] ;
.
```

I’ll be digging into messages in the next post, but here you can see that the message includes the following:

-   the property shape that invokes the error (sh:sourceShape),
    
-   the type of constraint component (sh:sourceConstraintComponent),
    
-   the focus node `sh:focusNode` (here a blank node), (the IRI of the subject node being validated)
    
-   the result path `sh:resultPath`, (the actual predicate path - a `sh:path` can specify several).
    
-   the object value of that node (`sh:value`) and finally
    
-   The result message, which may be a default, may be added to as a `sh:message`, or may be parametrically generated.
    

Note that the annotation data (`sh:name`, `sh:descriptio`n, sh:codeIdentifier) isn’t included in the report, since it can be read by dereferencing the shape IRI in question.

## String-based Constraints

One common use of property shapes is to ensure that content has a minimum or maximum length, or follows a particular pattern. These are all string-based constraints and are especially useful for validating literal content.

[

![](https://substackcdn.com/image/fetch/$s_!ybR5!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91945036-42bd-4647-bc84-dd1123d1e837_1085x771.png)

](https://substackcdn.com/image/fetch/$s_!ybR5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91945036-42bd-4647-bc84-dd1123d1e837_1085x771.png)

### String Length Constraints

As an example, if data is intended for consumption by a database with a field that has a maximum length (such as 20 characters for a person’s name), you’d want to set up a property shape that flagged anything longer than that length:

```
Shape:hasNameMaxLength_PropertyShape a sh:PropertyShape ;
     sh:path ex:fullName ;
     sh:datatype xsd:string ;
     sh:maxLength 20 ;
     sh:message "Names cannot be longer than 20 characters." ;
     .
```

The sh:minLength works similarly.

### The `sh:pattern` Constraint

A similar test may be to ensure that a string consisting of spaces, tabs or other invisible characters isn’t submitted. This is where the `sh:pattern` constraint comes in, which uses the W3C regular expressions library to match a particular pattern:

```
Shape:hasNameNoBlank_PropertyShape a sh:PropertyShape ;
     sh:path ex:fullName ;
     sh:datatype xsd:string ;
     sh:pattern "\S" ;
     sh:message "Name cannot consist of blank characters or an empty string" ;
     .
```

In this case, the “\\S” regex pattern matches at least one non-whitespace character (it also ensures the string is not empty). Note again that what you provide with the pattern is what the valid string looks like, not what an invalid string looks like.

### Available `sh:pattern` Flags (in `sh:flags`)

The `sh:flags` property is used with `sh:pattern` to modify regular expression behavior. It accepts a **string containing one or more flag characters**.

#### `i` - Case-Insensitive Matching

```
ex:ColorShape a sh:NodeShape ;
    sh:property [
        sh:path ex:color ;
        sh:pattern "^(red|blue|green)$" ;
        sh:flags "i" ;  # Case-insensitive
    ] ;
.

# All of these match:
ex:Item1 ex:color "RED" .
ex:Item2 ex:color "Red" .
ex:Item3 ex:color "red" .
ex:Item4 ex:color "BLUE" .
ex:Item5 ex:color "GrEeN" .
```

#### `s` - Dot-All Mode (Dot Matches Newlines)

```
ex:MultilineTextShape a sh:NodeShape ;
    sh:property [
        sh:path ex:content ;
        sh:pattern "^Start.*End$" ;
        sh:flags "s" ;  # Dot matches newline characters
    ] ;
.

# Matches:
ex:Text1 ex:content "Start middle End" .
ex:Text2 ex:content """Start
line 2
line 3
End""" .

# Without 's' flag, the second example would NOT match
```

**Without** `s` **flag**: `.` matches any character **except newline** (`\n`)

**With** `s` **flag**: `.` matches **any character, including newline**

#### `m` - Multiline Mode

```
ex:MultilineShape a sh:NodeShape ;
    sh:property [
        sh:path ex:text ;
        sh:pattern "^Line" ;
        sh:flags "m" ;  # ^ and $ match line boundaries
    ] ;
.

# Matches (each line starts with "Line"):
ex:Text1 ex:text """Line 1
Line 2
Line 3""" .

# Without 'm' flag, only the first line starting with "Line" would work
```

**Without** `m` **flag**:

-   `^` matches **start of string**
    
-   `$` matches **end of string**
    

**With** `m` **flag**:

-   `^` matches **start of string OR start of any line**
    
-   `$` matches **end of string OR end of any line**
    

#### `x` - Comments and Whitespace Mode

```
ex:ComplexPatternShape a sh:NodeShape ;
    sh:property [
        sh:path ex:phone ;
        sh:pattern """
            ^           # Start of string
            \\(?        # Optional opening parenthesis
            [0-9]{3}    # Area code (3 digits)
            \\)?        # Optional closing parenthesis
            [-.\\s]?    # Optional separator
            [0-9]{3}    # Exchange (3 digits)
            [-.\\s]?    # Optional separator
            [0-9]{4}    # Number (4 digits)
            $           # End of string
        """ ;
        sh:flags "x" ;  # Ignore whitespace and allow comments
    ] ;
.
```

**With** `x` **flag**:

-   Whitespace in the pattern is **ignored**
    
-   `#` starts a **comment** (to end of line)
    
-   Makes complex patterns more readable
    

**To match the literal space with** `x` **flag**: Use `\s` or `\` (escaped space)

### Language Constraints

There are two language-specific constraints: `sh:languageIn` and `sh:UniqueLang` .

The `sh:languageIn` property constrains the languages allowed to a value within a linked list, and works specifically with the @lang extension on strings. For example,

```
 @prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:ProductShape a sh:NodeShape ;
    sh:targetClass ex:Product ;
    sh:property [
        sh:path ex:name ;
        sh:languageIn ( "en" "es" "fr" ) ;
        sh:minCount 1 ;
        sh:message "Product name must be in English, Spanish, or French" ;
    ] ;
.

# Valid data
ex:Product1 a ex:Product ;
    ex:name "Widget"@en .

ex:Product2 a ex:Product ;
    ex:name "Dispositivo"@es .

ex:Product3 a ex:Product ;
    ex:name "Gadget"@fr .

ex:Product4 a ex:Product ;
    ex:name "Widget"@en ;
    ex:name "Dispositivo"@es ;
    ex:name "Gadget"@fr .

# Invalid data
ex:Product5 a ex:Product ;
    ex:name "Gerät"@de .  # ✗ German not in allowed list

ex:Product6 a ex:Product ;
    ex:name "Widget" .    # ✗ No language tag (plain literal)
```

The sh:uniqueLang property, on the other hand, solves a common problem in queries: labels, in particular, may have multiple values, but you only want one value _per language_.

```
ex:ProductNameShape a sh:NodeShape ;
    sh:targetClass ex:Product ;
    sh:property [
        sh:path ex:name ;
        sh:languageIn ( "en" "es" "fr" "de" ) ;
        sh:uniqueLang true ;  # Only one name per language
        sh:minCount 1 ;
        sh:message "Product must have exactly one name per language" ;
    ] ;
.

# Valid data - one name per language
ex:Product1 a ex:Product ;
    ex:name "Widget"@en ;
    ex:name "Dispositivo"@es ;
    ex:name "Gadget"@fr .

# Invalid data - two English names
ex:Product2 a ex:Product ;
    ex:name "Widget"@en ;
    ex:name "Gadget"@en ;    # ✗ Violates uniqueLang
    ex:name "Dispositivo"@es .

# Invalid data - two Spanish names
ex:Product3 a ex:Product ;
    ex:name "Widget"@en ;
    ex:name "Dispositivo"@es ;
    ex:name "Aparato"@es .   # ✗ Violates uniqueLang
```

### The `sh:hasValue` Constraint and the `sh:value` Response

There are a couple of properties in SHACL that can be confusing: `sh:hasValue` and `sh:value`. The first, `sh:hasValue`, is a constraint. It indicates, within a property shape, that the object of a given path must have a specific value. For instance, suppose that you wanted to create a user NodeShape with an “active” status property:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:ActiveUserShape a sh:NodeShape ;
    sh:targetClass ex:User ;
    sh:property [
        sh:path ex:status ;
        sh:hasValue "active" ;
        sh:message "User must have active status" ;
    ] ;
.

# Valid data
ex:User1 a ex:User ;
    ex:name "John" ;
    ex:status "active" .  # ✓ Matches exactly

# Invalid data
ex:User2 a ex:User ;
    ex:name "Jane" ;
    ex:status "inactive" .  # ✗ Different value
```

Note that there is a subtle distinction between how you build NodeShapes and how you validate. You may use `sh:hasValue` to create different shapes for active vs. inactive users:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

#######################################
# Shape 1: Active Users
#######################################

ex:ActiveUserShape a sh:NodeShape ;
    sh:targetClass ex:User ;
    
    # Only applies to users with status "active"
    sh:property [
        sh:path ex:status ;
        sh:hasValue "active" ;
    ] ;
    
    # Active users must have a lastLoginDate
    sh:property [
        sh:path ex:lastLoginDate ;
        sh:minCount 1 ;
        sh:datatype xsd:date ;
        sh:message "Active users must have a last login date" ;
    ] ;
    
    # Active users must have an email
    sh:property [
        sh:path ex:email ;
        sh:minCount 1 ;
        sh:pattern "^[^@]+@[^@]+\\.[^@]+$" ;
        sh:message "Active users must have a valid email" ;
    ] ;
    
    # Active users cannot have a deactivation reason
    sh:property [
        sh:path ex:deactivationReason ;
        sh:maxCount 0 ;
        sh:message "Active users should not have a deactivation reason" ;
    ] ;
.

#######################################
# Shape 2: Inactive Users
#######################################

ex:InactiveUserShape a sh:NodeShape ;
    sh:targetClass ex:User ;
    
    # Only applies to users with status "inactive"
    sh:property [
        sh:path ex:status ;
        sh:hasValue "inactive" ;
    ] ;
    
    # Inactive users must have a deactivation date
    sh:property [
        sh:path ex:deactivationDate ;
        sh:minCount 1 ;
        sh:datatype xsd:date ;
        sh:message "Inactive users must have a deactivation date" ;
    ] ;
    
    # Inactive users must have a deactivation reason
    sh:property [
        sh:path ex:deactivationReason ;
        sh:minCount 1 ;
        sh:datatype xsd:string ;
        sh:minLength 10 ;
        sh:message "Inactive users must have a deactivation reason (at least 10 chars)" ;
    ] ;
    
    # Inactive users should not have login activity
    sh:property [
        sh:path ex:lastLoginDate ;
        sh:maxCount 0 ;
        sh:message "Inactive users should not have recent login dates" ;
    ] ;
.

#######################################
# Example Data
#######################################

# Valid active user
ex:User1 a ex:User ;
    ex:name "John Doe" ;
    ex:status "active" ;
    ex:email "john@example.com" ;
    ex:lastLoginDate "2025-02-09"^^xsd:date .

# Valid inactive user
ex:User2 a ex:User ;
    ex:name "Jane Smith" ;
    ex:status "inactive" ;
    ex:deactivationDate "2024-12-01"^^xsd:date ;
    ex:deactivationReason "Account closed by user request" .

# Invalid active user (missing email)
ex:User3 a ex:User ;
    ex:name "Bob Johnson" ;
    ex:status "active" ;
    ex:lastLoginDate "2025-02-08"^^xsd:date .
    # ✗ Missing email (violates ActiveUserShape)

# Invalid inactive user (missing deactivation reason)
ex:User4 a ex:User ;
    ex:name "Alice Brown" ;
    ex:status "inactive" ;
    ex:deactivationDate "2024-11-15"^^xsd:date .
    # ✗ Missing deactivationReason (violates InactiveUserShape)

# User with no status (not validated by either shape)
ex:User5 a ex:User ;
    ex:name "Charlie Wilson" .
    # No status - neither shape applies
```

On the other hand, you may have a situation where you are only interested in inactive users, where sh:targetWhere may be more appropriate:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

#######################################
# Shape: Inactive Users Only
#######################################

ex:InactiveUserValidationShape a sh:NodeShape ;
    
    # Target ONLY users with status "inactive"
    sh:targetWhere """
        ?this a ex:User .
        ?this ex:status "inactive" .
    """ ;
    
    sh:name "Inactive User Validation" ;
    sh:description "Validates that inactive users have all required deactivation information" ;
    
    # Must have deactivation date
    sh:property [
        sh:path ex:deactivationDate ;
        sh:name "Deactivation Date" ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:date ;
        sh:lessThan ex:reactivationDate ;  # If reactivated, must be after deactivation
        sh:message "Inactive user must have exactly one deactivation date" ;
    ] ;
    
    # Must have deactivation reason
    sh:property [
        sh:path ex:deactivationReason ;
        sh:name "Deactivation Reason" ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:minLength 10 ;
        sh:maxLength 500 ;
        sh:message "Inactive user must have a deactivation reason (10-500 characters)" ;
    ] ;
    
    # Must have who deactivated them
    sh:property [
        sh:path ex:deactivatedBy ;
        sh:name "Deactivated By" ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:class ex:User ;
        sh:message "Inactive user must record which user deactivated them" ;
    ] ;
    
    # Status must be inactive (explicit check)
    sh:property [
        sh:path ex:status ;
        sh:name "Status" ;
        sh:hasValue "inactive" ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "User status must be 'inactive'" ;
    ] ;
    
    # Cannot have active sessions
    sh:property [
        sh:path ex:activeSession ;
        sh:name "Active Sessions" ;
        sh:maxCount 0 ;
        sh:message "Inactive users cannot have active sessions" ;
    ] ;
    
    # Cannot have permissions
    sh:property [
        sh:path ex:permissions ;
        sh:name "Permissions" ;
        sh:maxCount 0 ;
        sh:message "Inactive users should have no permissions" ;
    ] ;
    
    # Optional reactivation date (if user was reactivated then deactivated again)
    sh:property [
        sh:path ex:reactivationDate ;
        sh:name "Reactivation Date" ;
        sh:datatype xsd:date ;
        sh:message "Reactivation date must be a valid date" ;
    ] ;
.

#######################################
# Example Data
#######################################

# Valid inactive user
ex:User1 a ex:User ;
    ex:name "Jane Smith" ;
    ex:status "inactive" ;
    ex:deactivationDate "2024-12-01"^^xsd:date ;
    ex:deactivationReason "Account closed by user request" ;
    ex:deactivatedBy ex:AdminUser1 .

# Valid inactive user with reactivation history
ex:User2 a ex:User ;
    ex:name "Bob Johnson" ;
    ex:status "inactive" ;
    ex:deactivationDate "2025-01-15"^^xsd:date ;
    ex:deactivationReason "Violated community guidelines after second warning" ;
    ex:deactivatedBy ex:AdminUser2 ;
    ex:reactivationDate "2024-11-01"^^xsd:date .  # Was reactivated before

# Active user (NOT validated - not targeted by shape)
ex:User3 a ex:User ;
    ex:name "John Doe" ;
    ex:status "active" ;
    ex:email "john@example.com" ;
    ex:lastLoginDate "2025-02-09"^^xsd:date ;
    ex:permissions ex:ReadPermission, ex:WritePermission .
    # This user is ignored by InactiveUserValidationShape

# Pending user (NOT validated - not targeted by shape)
ex:User4 a ex:User ;
    ex:name "Alice Williams" ;
    ex:status "pending" ;
    ex:email "alice@example.com" .
    # This user is ignored by InactiveUserValidationShape

# Invalid inactive user (deactivation reason too short)
ex:User5 a ex:User ;
    ex:name "Charlie Brown" ;
    ex:status "inactive" ;
    ex:deactivationDate "2024-11-15"^^xsd:date ;
    ex:deactivationReason "Banned" ;  # ✗ Only 6 chars (needs 10+)
    ex:deactivatedBy ex:AdminUser1 .

# Invalid inactive user (missing deactivatedBy)
ex:User6 a ex:User ;
    ex:name "Diana Prince" ;
    ex:status "inactive" ;
    ex:deactivationDate "2024-10-20"^^xsd:date ;
    ex:deactivationReason "User requested account deletion" .
    # ✗ Missing ex:deactivatedBy

# Invalid inactive user (has active session)
ex:User7 a ex:User ;
    ex:name "Eve Martinez" ;
    ex:status "inactive" ;
    ex:deactivationDate "2024-09-05"^^xsd:date ;
    ex:deactivationReason "Account suspended for review" ;
    ex:deactivatedBy ex:AdminUser2 ;
    ex:activeSession ex:Session123 .  # ✗ Should not have active session

# Invalid inactive user (reactivation date before deactivation date)
ex:User8 a ex:User ;
    ex:name "Frank Castle" ;
    ex:status "inactive" ;
    ex:deactivationDate "2024-12-01"^^xsd:date ;
    ex:reactivationDate "2024-11-01"^^xsd:date ;  # ✗ Before deactivation date
    ex:deactivationReason "Terms of service violation" ;
    ex:deactivatedBy ex:AdminUser1 .

# Admin users
ex:AdminUser1 a ex:User ;
    ex:name "Admin Alice" ;
    ex:status "active" ;
    ex:email "admin1@example.com" ;
    ex:lastLoginDate "2025-02-10"^^xsd:date ;
    ex:permissions ex:AdminPermission .

ex:AdminUser2 a ex:User ;
    ex:name "Admin Bob" ;
    ex:status "active" ;
    ex:email "admin2@example.com" ;
    ex:lastLoginDate "2025-02-10"^^xsd:date ;
    ex:permissions ex:AdminPermission .

# Session reference
ex:Session123 a ex:Session ;
    ex:startTime "2025-02-10T10:00:00"^^xsd:dateTime .
```

_**Note:** The_ `sh:hasValue` _constraint is not the same thing as the_ `sh:value` _responses. The latter only appears in messages to report on the current value of the object for the matching target node’s subject, based upon the_ `sh:path`_._

### The sh:in Constraint

The `sh:in` property is the multi-item version of sh:hasValue - it indicates that the value must be one of the items from a linked list of items:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

#######################################
# SHACL Shape
#######################################

ex:TaskShape a sh:NodeShape ;
    sh:targetClass ex:Task ;
    
    sh:property [
        sh:path ex:priority ;
        sh:in ( "low" "medium" "high" "critical" ) ;  # Only these values allowed
        sh:minCount 1 ;
        sh:message "Priority must be: low, medium, high, or critical" ;
    ] ;
.

#######################################
# Data
#######################################

# Valid
ex:Task1 a ex:Task ;
    ex:priority "high" .  # ✓ In the list

ex:Task2 a ex:Task ;
    ex:priority "low" .   # ✓ In the list

# Invalid
ex:Task3 a ex:Task ;
    ex:priority "urgent" .  # ✗ Not in the list
```

This can also be used with IRIs rather than literals:

```
ex:TaskShape a sh:NodeShape ;
    sh:targetClass ex:Task ;
    
    sh:property [
        sh:path ex:status ;
        sh:in ( ex:Open ex:InProgress ex:Completed ex:Closed ) ;  # IRI values
        sh:minCount 1 ;
    ] ;
.

# Valid
ex:Task1 a ex:Task ;
    ex:status ex:InProgress .  # ✓ In the list

# Invalid
ex:Task2 a ex:Task ;
    ex:status ex:Cancelled .   # ✗ Not in the list
```

### The `sh:class` Constraint

Similarly, the `sh:targetClass` and `sh:class` properties are frequently confused. The sh:targetClass is used for node selection in the `sh:NodeShape` and determines the _subject’s_ class. The `sh:class` constraint, on the other hand, is used to constrain the _object’s_ class, as determined by the `sh:path` property in the property shape.

There’s a lot of similarity (and a few key differences) between these two properties and the `rdfs:domain` and `rdfs:range` properties.

[

![](https://substackcdn.com/image/fetch/$s_!n43H!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7a9ef1c-c839-4272-94d6-388b6fe864fa_1392x2224.png)

](https://substackcdn.com/image/fetch/$s_!n43H!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7a9ef1c-c839-4272-94d6-388b6fe864fa_1392x2224.png)

As an example, suppose that you wanted to validate where a person works:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

#######################################
# SHACL Shape
#######################################

ex:PersonShape a sh:NodeShape ;
    sh:targetClass ex:Person ;  # Validate all Person instances
    
    sh:property [
        sh:path ex:worksFor ;
        sh:class ex:Company ;   # Value must be a Company
        sh:minCount 1 ;
    ] ;
.

#######################################
# Data
#######################################

# Valid
ex:John a ex:Person ;
    ex:worksFor ex:Acme .

ex:Acme a ex:Company ;
    ex:name "Acme Corp" .

# Invalid
ex:Jane a ex:Person ;
    ex:worksFor ex:NotACompany .  # ✗ Wrong type

ex:NotACompany a ex:Building .
```

The target class in this case covers all person objects. The `sh:class`, on the other hand, is tied into the `ex:worksFor` path in the associated property shape, and indicates that the object should be of type `ex:Company.`

The s`h:class` constraint is quite common in SHACL primarily because most people (currently) use SHACL in conjunction with RDFS or OWL, where class-based logic is strongest.

## `sh:datatype` and `sh:nodeKind`

While on the topic of classes, there are two other constraints that overlap somewhat with `sh:class`, the `sh:datatype` and `sh:nodeKind` constraints.

The sh:datatype constraint is to literals what sh:class is to URIs - it’s a way of identifying what literal type a given value is meant to represent. For instance, the following property shape indicates that ex:startDate must use a date representation:

```
[] a sh:PropertyShape ;
     sh:name "Start Date" ;
     sh:path ex:startDate ;
     sh:datatype xsd:date ;
     sh:minCount 1 ;
     sh:maxCount 1 ;
     .
```

Datatypes need not be W3C atomic types. My own personal belief is that a datatype is the IRI for identifying a parsing model for a string (such as Markdown or WGS-84 lat-long-height coordinates). I’ll cover that in a subsequent post.

The sh:nodeKind constraint indicates the type of node that the property can accept as an object, as listed in the following table:

[

![](https://substackcdn.com/image/fetch/$s_!DxzA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4df7b51e-b7d8-40a5-a71b-49861c400cf9_1101x731.png)

](https://substackcdn.com/image/fetch/$s_!DxzA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4df7b51e-b7d8-40a5-a71b-49861c400cf9_1101x731.png)

A blank node is usually used to indicate an anonymous data structure (it has no public identifier), but such blank nodes will be treated as private identifiers (not literals). If the `sh:datatype` is used, then the assumption is that `sh:nodeKind` will be `sh:Literal`. If `sh:class` property is set, then `sh:nodeKind` will default to `sh:BlankNodeOrIRI`.

The sh:nodeKind property is useful as a safety check (because it can be checked fast), and can force the validator to recognize only nodes with IRIs rather than blank nodes (or vice versa). It can also provide a quick switch for testing UI generation and mapping conversions. However, in most cases, it’s somewhat redundant.

## The `sh:node` Constraint

One critical aspect of SHAPEs is that you can build shapes with other shapes. If you think of an SHACL node shape as a way of describing a particular graph pattern, you need to have the ability to compose shapes using other shapes. This is what the `sh:node` property does: it provides a pointer to another shape that describes the object of a given property shape.

For instance, let’s go back to our Car Keys example. In this particular case,

```
###########################################
# Property Shape: Car Keys
###########################################

ex:CarKeysPropertyShape
    a sh:PropertyShape ;
    sh:path ex:hasCarKeys ;
    sh:name "Car Keys Check" ;
    sh:codeIdentifier "carKeysCheck" ;
    sh:description "Verify that you have YOUR car keys (not someone else's)" ;
    
    # Must have exactly one car key set
    sh:minCount 1 ;
    sh:maxCount 1 ;
    
    # Must be a CarKeys instance
    sh:class ex:CarKeys ;
    
    # Must be owned by the person making the trip
    sh:node ex:OwnedByPersonShape ; # This provides the shape for the Car Keys
    
    sh:message "You must have YOUR car keys (check if they're yours, not someone else's)" ;
.

ex:OwnedByPersonShape
    a sh:NodeShape ;
    sh:targetClass ex:CarKeys ;
    sh:property [
        sh:path ex:ownedBy ;
        sh:minCount 1 ;
        sh:class ex:Person ;
        sh:message "Keys are owned by someone." ;
    ] ;
.
```

In this case, the `sh:node` constraint points to a named property shape, `ex:OwnedByPersonShape`, which is on the `ex:CarKeys` target class. This in turn defines its own set of property shapes, including the anonymous property shape around `sh:path` `ex:ownedBy`.

The following illustrates instances (valid and invalid) that satisfied the grocery trip object (with just the Car Keys path).

```
@prefix ex: <http://example.org/household/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

###########################################
# Instance Data: Valid Grocery Shopping Trip
###########################################

# A person
ex:Alice
    a ex:Person ;
    rdfs:label "Alice Smith" ;
.

# Alice's car keys
ex:AlicesCarKeys
    a ex:CarKeys ;
    rdfs:label "Alice's Toyota Keys" ;
    ex:ownedBy ex:Alice ;
.

# Alice's grocery shopping trip
ex:AliceGroceryTrip
    a ex:GroceryShoppingTrip ;
    rdfs:label "Alice's Saturday Grocery Run" ;
    ex:hasCarKeys ex:AlicesCarKeys ;
.
# This can also be represented inline:

ex:AliceGroceryTrip
    a ex:GroceryShoppingTrip ;
    rdfs:label "Alice's Saturday Grocery Run" ;
    ex:hasCarKeys [
        a ex:CarKeys ;
        rdfs:label "Alice's Toyota Keys" ;
        ex:ownedBy [
            a ex:Person ;
            rdfs:label "Alice Smith" ;
             ] ;
       ] .

###########################################
# Additional Valid Example
###########################################

ex:Bob
    a ex:Person ;
    rdfs:label "Bob Johnson" ;
.

ex:BobsCarKeys
    a ex:CarKeys ;
    rdfs:label "Bob's Honda Keys" ;
    ex:ownedBy ex:Bob ;
.

ex:BobGroceryTrip
    a ex:GroceryShoppingTrip ;
    rdfs:label "Bob's Weekly Shopping" ;
    ex:hasCarKeys ex:BobsCarKeys ;
.

###########################################
# Invalid Examples (for testing)
###########################################

# Invalid: Bob has Alice's keys
ex:BobInvalidTrip
    a ex:GroceryShoppingTrip ;
    rdfs:label "Bob's Invalid Trip" ;
    ex:hasCarKeys ex:AlicesCarKeys ;  # Wrong! These belong to Alice
.

# Invalid: No keys assigned
ex:CharlieNoKeysTrip
    a ex:GroceryShoppingTrip ;
    rdfs:label "Charlie's Trip Without Keys" ;
    # Missing ex:hasCarKeys - violates sh:minCount 1
.

# Invalid: Keys with no owner
ex:OrphanKeys
    a ex:CarKeys ;
    rdfs:label "Keys Without Owner" ;
    # Missing ex:ownedBy - violates OwnedByPersonShape
.

ex:DaveInvalidTrip
    a ex:GroceryShoppingTrip ;
    rdfs:label "Dave's Trip With Orphan Keys" ;
    ex:hasCarKeys ex:OrphanKeys ;
.
```

This can be illustrated as follows (Alice path only):

[

![](https://substackcdn.com/image/fetch/$s_!hRAU!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa376bc5d-0009-4601-b02e-6208c4048f10_5766x7400.png)

](https://substackcdn.com/image/fetch/$s_!hRAU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa376bc5d-0009-4601-b02e-6208c4048f10_5766x7400.png)

The `sh:node` property is the glue that holds together the shape and extends it beyond simply one immediate path. It is also what allows you to compose alternative shapes, not just for validation, but in general.

There’s one additional consequence of s`h:node`. The DESCRIBE verb, as typically implemented in SPARQL, can be frustrating because it typically stops at the first IRI it encounters. This means that the envelope, when using it as described, is often incomplete, either providing information you don’t want or (as is more usually the case) not providing enough information that you do want, such as labels.

The `sh:node` constraint lets you build a better DESCRIBE in SPARQL (or elsewhere), as you can follow each `sh:node` to retrieve relevant properties and bindings that can truly determine the envelope of your data. I’ll revisit this idea in a future post.

## Summary

Property shapes do much of the heavy lifting in validation and also provide the schematic completeness required for a data modelling language. This post focused on the basics of property constraints and touched on reporting, but there are several more advanced aspects of constraints modelling that should be covered as you gain more depth in SHACL, which I will address soon.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!WqLY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F526f4722-af9a-4bff-94f9-ab2760c5f5ac_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!WqLY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F526f4722-af9a-4bff-94f9-ab2760c5f5ac_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.

