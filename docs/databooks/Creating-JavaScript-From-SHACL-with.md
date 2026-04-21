---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Creating-JavaScript-From-SHACL-with
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:56.676288+00:00'
  title: Creating Javascript From Shacl With
  type: plain-doc
  version: '0.1'
---

# Creating Javascript From Shacl With

[

![](https://substackcdn.com/image/fetch/$s_!o0ei!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad684eda-d8fc-4e87-9b1c-0c744bb912f0_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!o0ei!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad684eda-d8fc-4e87-9b1c-0c744bb912f0_2688x1536.jpeg)

I have a secret. I hate programming … okay, maybe that’s a little too strong, but I find, especially as I get older, that I don’t have as much interest in working with JavaScript or Python as I used to, mostly because a lot of it is just boilerplate code anymore. I’d rather be designing enterprise data models, but sometimes it’s necessary. However, there are times when I’d really prefer to have someone else write up the code … or even (gasp) using an AI to do it.

Here’s the thing. I don’t trust AIs, especially AI code generation. It’s not that I don’t think that such code isn’t useful - I use Claude especially most days anymore, because you can’t talk about data modelling without giving your model a workout. Rather, I don’t believe that you can arbitrarily tell any computer process, “Hey, write up code that will magically allow me to manipulate my data exactly the way I want it by reading my mind.” I don’t care how good your code generator is; if you approach coding this way, you’ll spend a lot of time cleaning up useless or even erroneous code.

I’ve been writing up a series on SHACL 1.2 for a little while now. A SHACL file, when you get right down to it, is a description of an interface. You have classes and properties (setters and getters), you have functions (node expressions of various flavours), cardinality information, constraints, error messages, enumerations, and internal state. You don’t necessarily have all of the fiddling internals with regard to setting up configurations or calling out to external services, but that shouldn’t be the role of an interface anyway. What it does give you, ultimately, is structure.

My philosophy on AI code gen is simple: use it with a structural document to constrain its output to meet expectations, then, once the AI is applied, finish the resulting document by hand. By using SHACL as the starting point, you have done most of the major design work ahead of time, and the likelihood that any generated code covers the bases rises dramatically as a consequence.

Let’s take a simple case: modelling a name and age. In my experience the best place to start is to figure out both what you’re working with (call it the source graph) and what you want to end up with (the target graph). The source graph is straightforward, and likely hidden:

```
prefix ex: <http://example.com/ex#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>

ex:JaneDoe a ex:Person ;
   ex:firstName "Jane" ;
   ex:lastName "Doe" ;
   ex:birthDate "2000-01-01"^^xsd:date ;
   .
```

The target graph is the graph that is exposed to an end user, and is mostly computed via node expressions.

```
prefix Person: <http://example.com/ns/Person#>
prefix Class: <http://example.com/ns/Class#>
prefix ex: <http://example.com/ex#>
prefix xsd: <http://example.com/ex#>

Person:JaneDoe a Class:Person ;
   ex:firstName "Jane" ;
   ex:lastName "Doe" ;
   Person:fullName "Jane Doe" ;
   Person:age 26 ;
   .
```

Here, ex:firstName and ex:lastName are carried over from the source graph, while Person:fullName and Person:age are computed. Also notice that the birth date is NOT carried over, it’s internal only.

I’m going to use Claude here to generate a transformation SHACL. Here’s the prompt:

````
Given a source Turtle RDF file of:

```
prefix ex: <http://example.com/ex#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>

ex:JaneDoe a ex:Person ;
   ex:firstName "Jane" ;
   ex:lastName "Doe" ;
   ex:birthDate "2000-01-01"^^xsd:date ;
   
```

and a target Turtle RDF file of:

```
prefix Person: <http://example.com/ns/Person#>
prefix Class: <http://example.com/ns/Class#>
prefix ex: <http://example.com/ex#>
prefix xsd: <http://example.com/ex#>

Person:JaneDoe a Class:Person ;
   ex:firstName "Jane" ;
   ex:lastName "Doe" ;
   Person:fullName "Jane Doe" ;
   Person:age 26 ;
   .
```

Generate a SHACL 1.2 file using https://www.w3.org/TR/shacl12-core/ including node expressions. Include sh:codeIdentifier, sh:name and sh:description resources, and be as comprehensive as possible.
````

This generates the following SHACL Turtle:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.com/ex#> .
@prefix Person: <http://example.com/ns/Person#> .
@prefix Class: <http://example.com/ns/Class#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dash: <http://datashapes.org/dash#> .

#####################################################
# Person Transformation Shape
#####################################################

ex:PersonTransformationShape
    a sh:NodeShape ;
    sh:codeIdentifier "PersonTransformationShape" ;
    sh:name "Person Transformation Shape" ;
    sh:description """Transforms source Person data (ex: namespace) to target Person data (Person:/Class: namespaces).
        Handles namespace migration, derives fullName from firstName and lastName, 
        and calculates age from birthDate.""" ;
    sh:targetClass ex:Person ;
    sh:severity sh:Violation ;
    
    # Rule 1: Transform the subject URI
    sh:rule [
        a sh:SPARQLRule ;
        sh:codeIdentifier "TransformPersonURI" ;
        sh:name "Transform Person URI" ;
        sh:description "Transforms ex:JaneDoe to Person:JaneDoe" ;
        sh:construct """
            PREFIX ex: <http://example.com/ex#>
            PREFIX Person: <http://example.com/ns/Person#>
            PREFIX Class: <http://example.com/ns/Class#>
            
            CONSTRUCT {
                ?targetSubject a Class:Person .
            }
            WHERE {
                $this a ex:Person .
                BIND(IRI(REPLACE(STR($this), "http://example.com/ex#", "http://example.com/ns/Person#")) AS ?targetSubject)
            }
        """ ;
    ] ;
    
    # Rule 2: Copy firstName property
    sh:rule [
        a sh:SPARQLRule ;
        sh:codeIdentifier "CopyFirstName" ;
        sh:name "Copy First Name" ;
        sh:description "Copies ex:firstName to target namespace" ;
        sh:construct """
            PREFIX ex: <http://example.com/ex#>
            PREFIX Person: <http://example.com/ns/Person#>
            
            CONSTRUCT {
                ?targetSubject ex:firstName ?firstName .
            }
            WHERE {
                $this ex:firstName ?firstName .
                BIND(IRI(REPLACE(STR($this), "http://example.com/ex#", "http://example.com/ns/Person#")) AS ?targetSubject)
            }
        """ ;
    ] ;
    
    # Rule 3: Copy lastName property
    sh:rule [
        a sh:SPARQLRule ;
        sh:codeIdentifier "CopyLastName" ;
        sh:name "Copy Last Name" ;
        sh:description "Copies ex:lastName to target namespace" ;
        sh:construct """
            PREFIX ex: <http://example.com/ex#>
            PREFIX Person: <http://example.com/ns/Person#>
            
            CONSTRUCT {
                ?targetSubject ex:lastName ?lastName .
            }
            WHERE {
                $this ex:lastName ?lastName .
                BIND(IRI(REPLACE(STR($this), "http://example.com/ex#", "http://example.com/ns/Person#")) AS ?targetSubject)
            }
        """ ;
    ] ;
    
    # Rule 4: Generate fullName from firstName + lastName using node expression
    sh:rule [
        a sh:SPARQLRule ;
        sh:codeIdentifier "GenerateFullName" ;
        sh:name "Generate Full Name" ;
        sh:description "Derives Person:fullName by concatenating firstName and lastName with a space" ;
        sh:construct """
            PREFIX ex: <http://example.com/ex#>
            PREFIX Person: <http://example.com/ns/Person#>
            
            CONSTRUCT {
                ?targetSubject Person:fullName ?fullName .
            }
            WHERE {
                $this ex:firstName ?firstName ;
                      ex:lastName ?lastName .
                BIND(CONCAT(?firstName, " ", ?lastName) AS ?fullName)
                BIND(IRI(REPLACE(STR($this), "http://example.com/ex#", "http://example.com/ns/Person#")) AS ?targetSubject)
            }
        """ ;
    ] ;
    
    # Rule 5: Calculate age from birthDate using node expression
    sh:rule [
        a sh:SPARQLRule ;
        sh:codeIdentifier "CalculateAge" ;
        sh:name "Calculate Age" ;
        sh:description "Calculates Person:age from ex:birthDate based on current date (2026-01-10)" ;
        sh:construct """
            PREFIX ex: <http://example.com/ex#>
            PREFIX Person: <http://example.com/ns/Person#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            
            CONSTRUCT {
                ?targetSubject Person:age ?age .
            }
            WHERE {
                $this ex:birthDate ?birthDate .
                BIND(IRI(REPLACE(STR($this), "http://example.com/ex#", "http://example.com/ns/Person#")) AS ?targetSubject)
                # Calculate age: current year - birth year
                BIND(YEAR("2026-01-10"^^xsd:date) - YEAR(?birthDate) AS ?yearDiff)
                # Adjust if birthday hasn't occurred this year
                BIND(IF(
                    (MONTH("2026-01-10"^^xsd:date) < MONTH(?birthDate)) ||
                    (MONTH("2026-01-10"^^xsd:date) = MONTH(?birthDate) && DAY("2026-01-10"^^xsd:date) < DAY(?birthDate)),
                    ?yearDiff - 1,
                    ?yearDiff
                ) AS ?age)
            }
        """ ;
    ] ;
    
    # Property shape for firstName validation
    sh:property [
        sh:path ex:firstName ;
        sh:codeIdentifier "firstNameProperty" ;
        sh:name "First Name Property" ;
        sh:description "Validates that firstName exists and is a non-empty string" ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minLength 1 ;
        sh:severity sh:Violation ;
    ] ;
    
    # Property shape for lastName validation
    sh:property [
        sh:path ex:lastName ;
        sh:codeIdentifier "lastNameProperty" ;
        sh:name "Last Name Property" ;
        sh:description "Validates that lastName exists and is a non-empty string" ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minLength 1 ;
        sh:severity sh:Violation ;
    ] ;
    
    # Property shape for birthDate validation
    sh:property [
        sh:path ex:birthDate ;
        sh:codeIdentifier "birthDateProperty" ;
        sh:name "Birth Date Property" ;
        sh:description "Validates that birthDate exists, is a valid date, and is in the past" ;
        sh:datatype xsd:date ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:maxInclusive "2026-01-10"^^xsd:date ;
        sh:severity sh:Violation ;
    ] ;
    .

#####################################################
# Target Person Validation Shape
#####################################################

ex:TargetPersonShape
    a sh:NodeShape ;
    sh:codeIdentifier "TargetPersonShape" ;
    sh:name "Target Person Validation Shape" ;
    sh:description """Validates the transformed Person data in the target namespace (Person:/Class:).
        Ensures all required properties exist with correct datatypes and constraints.""" ;
    sh:targetClass Class:Person ;
    sh:severity sh:Violation ;
    
    # Validate firstName in target
    sh:property [
        sh:path ex:firstName ;
        sh:codeIdentifier "targetFirstNameProperty" ;
        sh:name "Target First Name" ;
        sh:description "Validates firstName in transformed data" ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minLength 1 ;
    ] ;
    
    # Validate lastName in target
    sh:property [
        sh:path ex:lastName ;
        sh:codeIdentifier "targetLastNameProperty" ;
        sh:name "Target Last Name" ;
        sh:description "Validates lastName in transformed data" ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minLength 1 ;
    ] ;
    
    # Validate fullName in target
    sh:property [
        sh:path Person:fullName ;
        sh:codeIdentifier "fullNameProperty" ;
        sh:name "Full Name Property" ;
        sh:description "Validates that fullName exists and matches the pattern 'FirstName LastName'" ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minLength 3 ;
        sh:pattern "^[A-Za-z]+ [A-Za-z]+$" ;
        sh:message "Full name must be in format 'FirstName LastName'" ;
    ] ;
    
    # Validate age in target
    sh:property [
        sh:path Person:age ;
        sh:codeIdentifier "ageProperty" ;
        sh:name "Age Property" ;
        sh:description "Validates that age is a non-negative integer less than 150" ;
        sh:datatype xsd:integer ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minInclusive 0 ;
        sh:maxInclusive 150 ;
    ] ;
    .

#####################################################
# Node Expression Functions (SHACL 1.2)
#####################################################

ex:FullNameExpression
    a sh:NodeExpression ;
    sh:codeIdentifier "fullNameExpression" ;
    sh:name "Full Name Expression" ;
    sh:description "Node expression that concatenates firstName and lastName to create fullName" ;
    sh:select """
        PREFIX ex: <http://example.com/ex#>
        SELECT ?fullName
        WHERE {
            $this ex:firstName ?firstName ;
                  ex:lastName ?lastName .
            BIND(CONCAT(?firstName, " ", ?lastName) AS ?fullName)
        }
    """ ;
    .

ex:AgeCalculationExpression
    a sh:NodeExpression ;
    sh:codeIdentifier "ageCalculationExpression" ;
    sh:name "Age Calculation Expression" ;
    sh:description "Node expression that calculates age from birthDate relative to 2026-01-10" ;
    sh:select """
        PREFIX ex: <http://example.com/ex#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?age
        WHERE {
            $this ex:birthDate ?birthDate .
            BIND(YEAR("2026-01-10"^^xsd:date) - YEAR(?birthDate) AS ?yearDiff)
            BIND(IF(
                (MONTH("2026-01-10"^^xsd:date) < MONTH(?birthDate)) ||
                (MONTH("2026-01-10"^^xsd:date) = MONTH(?birthDate) && DAY("2026-01-10"^^xsd:date) < DAY(?birthDate)),
                ?yearDiff - 1,
                ?yearDiff
            ) AS ?age)
        }
    """ ;
    .

ex:NamespaceTransformExpression
    a sh:NodeExpression ;
    sh:codeIdentifier "namespaceTransformExpression" ;
    sh:name "Namespace Transform Expression" ;
    sh:description "Node expression that transforms ex: namespace URIs to Person: namespace" ;
    sh:select """
        PREFIX ex: <http://example.com/ex#>
        PREFIX Person: <http://example.com/ns/Person#>
        SELECT ?targetURI
        WHERE {
            BIND(IRI(REPLACE(STR($this), "http://example.com/ex#", "http://example.com/ns/Person#")) AS ?targetURI)
        }
    """ ;
    .

#####################################################
# Property Path Expressions for Derived Values
#####################################################

ex:FullNamePath
    a sh:PropertyShape ;
    sh:codeIdentifier "derivedFullNamePath" ;
    sh:name "Derived Full Name Path" ;
    sh:description "Property path that derives fullName using node expression" ;
    sh:path Person:fullName ;
    sh:values ex:FullNameExpression ;
    sh:severity sh:Info ;
    .

ex:AgePath
    a sh:PropertyShape ;
    sh:codeIdentifier "derivedAgePath" ;
    sh:name "Derived Age Path" ;
    sh:description "Property path that calculates age using node expression" ;
    sh:path Person:age ;
    sh:values ex:AgeCalculationExpression ;
    sh:severity sh:Info ;
    .

#####################################################
# Constraint Components
#####################################################

ex:NameConsistencyConstraint
    a sh:ConstraintComponent ;
    sh:codeIdentifier "nameConsistencyConstraint" ;
    sh:name "Name Consistency Constraint" ;
    sh:description "Validates that fullName matches the concatenation of firstName and lastName" ;
    sh:parameter [
        sh:path ex:checkFullName ;
        sh:datatype xsd:boolean ;
    ] ;
    sh:validator [
        a sh:SPARQLSelectValidator ;
        sh:message "Full name must equal 'firstName lastName'" ;
        sh:select """
            PREFIX ex: <http://example.com/ex#>
            PREFIX Person: <http://example.com/ns/Person#>
            SELECT $this ?value
            WHERE {
                $this ex:firstName ?firstName ;
                      ex:lastName ?lastName ;
                      Person:fullName ?fullName .
                BIND(CONCAT(?firstName, " ", ?lastName) AS ?expected)
                FILTER(?fullName != ?expected)
                BIND(?fullName AS ?value)
            }
        """ ;
    ] ;
    .

#####################################################
# Metadata and Annotations
#####################################################

ex:PersonTransformationShape
    rdfs:comment "Primary transformation shape for converting ex:Person instances to Class:Person instances" ;
    rdfs:seeAlso <https://www.w3.org/TR/shacl12-core/> ;
    sh:order 1 ;
    .

ex:TargetPersonShape
    rdfs:comment "Validation shape for transformed Person data" ;
    rdfs:seeAlso <https://www.w3.org/TR/shacl12-core/> ;
    sh:order 2 ;
    .
```

The SHACL here is fairly complex, primarily because it involves a combination of properties and rules, but the upshot is that it transfers over the `ex:firstName` and `exLastName` properties, then calculates the `Person:fullName` and `Person:age` properties. Comments from Claude:

_This comprehensive SHACL 1.2 file includes:_

## _Key Features:_

1.  _**Transformation Rules** - Five SPARQL-based rules that:_
    
    -   _Transform URIs from_ `ex:` _to_ `Person:` _namespace_
        
    -   _Copy firstName and lastName properties_
        
    -   _Derive fullName by concatenating firstName + lastName_
        
    -   _Calculate age from birthDate (accounting for whether birthday has passed)_
        
2.  _**Node Expressions (SHACL 1.2)** - Three reusable expressions for:_
    
    -   _Full name concatenation_
        
    -   _Age calculation logic_
        
    -   _Namespace URI transformation_
        
3.  _**Complete Metadata** - Every shape and rule includes:_
    
    -   `sh:codeIdentifier` _for programmatic reference_
        
    -   `sh:name` _for human-readable labels_
        
    -   `sh:description` _for detailed documentation_
        
4.  _**Validation Constraints**:_
    
    -   _Property existence and cardinality_
        
    -   _Datatype validation_
        
    -   _Pattern matching (fullName format)_
        
    -   _Range validation (age 0-150, birthDate in past)_
        
5.  _**Source & Target Shapes**:_
    
    -   `PersonTransformationShape` _validates and transforms source data_
        
    -   `TargetPersonShape` _validates the transformed output_
        
6.  _**Custom Constraint Component** - Validates fullName consistency_
    

Note that I’ve explicitly requested that this uses the lastest in-progress version of SHACL (December 2025), since the language is evolving quickly at this point. The code is worth reviewing, but nothing else worth calling out here.

Once you have the SHACL, save it as a file so that you can reference it later.

## Creating the JavaScript

The next stage is to take the SHACL and convert it to JavaScript. I’ve used the following prompt:

```
Using the generated SHACL, create a corresponding set of JavaScript classes using contemporary ECMAScript, with getters (and setters where appropriate), including a global DataModel class for managing otherwise unbound SHACL classes. 

Include relevant documentation, test data and a test suite. 

Additionally include a Connector class that lets the user connect to a triple store (target Jena/Fuseki specifically) to save and retrieve content.
```

This process generates a lot of code (it took about five minutes using Clause Sonnet). Rather than dumping all of it into this post, I’ve uploaded it to a [github repositor](https://github.com/kurtcagle/person-shacl-to-javascript)y where you can examine it at your leisure.

They key point is that you can use this to create objects such as Person and TransformedPerson. That lets you manipulate the database directly with Javascript code, rather than having to write SPARQL directly. Significantly, it is NOT directly dependent upon a SHACL processor for anything but test validation - the SHACL is used solely to drive the Javascript generation processs.

I’ve added a configuration class that can be customized for different outputs; you should be able to use claude to build additional configurations for different triple stores and processes.

## 💡 Usage Examples

The following illustrates a number of basic examples, and was generated as part of the Javascript creation.

### _Example 1: Age Calculation with Birthday Logic_

_javascript_

```
import { Person } from './person.js';

const person = new Person({
  firstName: 'Jane',
  lastName: 'Doe',
  birthDate: '2000-01-01'
});

// Calculate age on different dates
const age2026 = person.getAge(new Date('2026-01-10')); // 26
const age2025 = person.getAge(new Date('2025-12-31')); // 25 (birthday not reached)
```

### _Example 2: Batch Transformation_

_javascript_

```
import { DataModel } from './data-model.js';

DataModel.clearAll();

// Create multiple people
const peopleData = [
  { firstName: 'Alice', lastName: 'Johnson', birthDate: '1992-03-22' },
  { firstName: 'Bob', lastName: 'Williams', birthDate: '1978-11-30' },
  { firstName: 'Carol', lastName: 'Brown', birthDate: '2005-07-04' }
];

peopleData.forEach(data => DataModel.create('Person', data));

// Transform all
const referenceDate = new Date('2026-01-10');
DataModel.getInstances('Person').forEach(person => {
  DataModel.transform(person, 'TransformedPerson', { referenceDate });
});

// Validate all
const validations = DataModel.validateAll('TransformedPerson');
console.log('All valid:', validations.every(v => v.validation.valid));
```

### _Example 3: RDF Export_

_javascript_

```
import { DataModel } from './data-model.js';

// Export all instances to Turtle
const turtle = DataModel.exportToTurtle();
console.log(turtle);

// Export specific class to JSON
const json = DataModel.exportToJSON('Person');
console.log(JSON.stringify(json, null, 2));
```

### _Example 4: SPARQL Queries_

_javascript_

```
import { createLocalConnector } from './fuseki-connector.js';

const connector = createLocalConnector('test');

// SELECT query
const query = `
  PREFIX ex: <http://example.com/ex#>
  SELECT ?person ?name
  WHERE {
    ?person a ex:Person ;
            ex:firstName ?name .
  }
`;

const results = await connector.query(query);
console.log(results.results.bindings);

// CONSTRUCT query
const construct = `
  PREFIX ex: <http://example.com/ex#>
  CONSTRUCT { ?s ?p ?o }
  WHERE { ?s a ex:Person ; ?p ?o }
`;

const rdf = await connector.construct(construct);
console.log(rdf);

// ASK query
const ask = `
  PREFIX ex: <http://example.com/ex#>
  ASK { ex:JaneDoe a ex:Person }
`;

const exists = await connector.ask(ask);
console.log('Exists:', exists);
```

### _Example 5: Graph Store Protocol_

_javascript_

```
import { createLocalConnector } from './fuseki-connector.js';
import { Person } from './person.js';

const connector = createLocalConnector('test');
const graphUri = 'http://example.com/graph/people';

// Save to named graph
const person = new Person({
  firstName: 'Graph',
  lastName: 'Test',
  birthDate: '1995-05-15'
});

await connector.save(person, graphUri);

// Retrieve from named graph
const data = await connector.retrieve(graphUri);
console.log(data);

// Clear named graph
await connector.clear(graphUri);
```

## _🔌 Fuseki Integration_

### _Starting Fuseki_

_bash_

```
# Download Fuseki from Apache Jena website
# https://jena.apache.org/download/

# Start with in-memory dataset
fuseki-server --mem /test

# Or start with persistent dataset
fuseki-server --loc=./data /test

# Fuseki UI available at: http://localhost:3030
```

### _Configuration_

_The default configuration connects to:_

-   _**Base URL**:_
    

_http://localhost:3030_

-   _**Dataset**:_ `test`
    

_To use a different configuration:_

_javascript_

```
import { FusekiConnector } from './fuseki-connector.js';

const connector = new FusekiConnector({
  baseUrl: 'http://my-server:3030',
  dataset: 'my-dataset',
  username: 'admin',  // Optional
  password: 'secret'  // Optional
});
```

### _Complete Workflow with Fuseki_

_javascript_

```
import { DataModel } from './data-model.js';
import { createLocalConnector } from './fuseki-connector.js';

// 1. Create data
DataModel.clearAll();
DataModel.create('Person', {
  firstName: 'Workflow',
  lastName: 'Example',
  birthDate: '1990-01-01'
});

// 2. Transform
DataModel.getInstances('Person').forEach(person => {
  DataModel.transform(person, 'TransformedPerson');
});

// 3. Save to Fuseki
const connector = createLocalConnector('test');
await connector.clear();  // Clear existing data

const people = DataModel.getInstances('Person');
await connector.saveAll(people);

// 4. Query from Fuseki
const uris = await connector.findByType('http://example.com/ex#Person');
console.log('Found', uris.length, 'people in triple store');

// 5. Retrieve and reconstruct
for (const uri of uris) {
  const data = await connector.getPerson(uri);
  const person = Person.fromJSON({ ...data, uri });
  console.log(person.toString());
}
```

## _🧪 Testing_

### _Running Tests_

_bash_

```
# Run the complete test suite
node test-suite.js

# Run demo examples
node index.js
```

### _Test Coverage_

_The test suite includes:_

-   _✅ Person class creation and validation_
    
-   _✅ Age calculation with birthday logic_
    
-   _✅ TransformedPerson creation and validation_
    
-   _✅ Transformation from Person to TransformedPerson_
    
-   _✅ DataModel registration and management_
    
-   _✅ Instance querying and filtering_
    
-   _✅ Import/export (JSON, Turtle, JSON-LD)_
    
-   _✅ FusekiConnector configuration_
    
-   _✅ Error handling and validation_
    
-   _✅ Integration workflows_
    

### _Sample Test Output_

```
🧪 Starting Test Suite

============================================================
✅ Person: Create with valid data
✅ Person: Calculate age correctly
✅ Person: Export to Turtle
✅ TransformedPerson: Transform from Person
✅ DataModel: Create Person instance
✅ FusekiConnector: Create instance
... [60+ tests]
============================================================

📊 Test Results:
   Passed: 65
   Failed: 0
   Total:  65

✅ All tests passed!
```

## _📄 SHACL Schema_

_The system is based on a comprehensive SHACL 1.2 schema that includes:_

### _Shapes_

-   `ex:PersonTransformationShape` _- Transforms source to target_
    
-   `ex:TargetPersonShape` _- Validates transformed data_
    

### _Rules_

1.  _Transform subject URI (ex: → Person:)_
    
2.  _Copy firstName property_
    
3.  _Copy lastName property_
    
4.  _Generate fullName from firstName + lastName_
    
5.  _Calculate age from birthDate_
    

### _Node Expressions_

-   _Full name concatenation_
    
-   _Age calculation with birthday logic_
    
-   _Namespace transformation_
    

### _Constraints_

-   _Property existence and cardinality_
    
-   _Datatype validation_
    
-   _Pattern matching_
    
-   _Range validation_
    
-   _Custom constraint components_
    

_See_ `person-transformation-shacl.ttl` _for the complete schema._

## _🔧 Requirements_

-   _Node.js 18+ (for ES modules and private fields)_
    
-   _Apache Jena Fuseki 4.x+ (for triple store operations)_
    

## _📝 License_

_MIT License - See LICENSE file for details_

## _👥 Contributing_

_Contributions welcome! Please submit pull requests or open issues._

## _📧 Contact_

_For questions or support, please open an issue in the repository._

## Summary

The example given here was extremely simple, but should be able to be scaled up with more comprehensive SHACL schemas (I’ve created versions with several dozen RDF classes without significant rework). What this does (and why I think this is VERY important) is allow you to start with a data description of your RDF to test your internal data logic, then read and manipulate that back end as if they were objects, in effect creating a very rich data binding and validation layer. The code also has no implicit dependency on GenAI - once you generate the code, it can be deployed without ever needing to touch an LLM again.

I’ve targeted this for JavaScript, but the same approach can also be used for Python or other languages. As always, spend some time reviewing and validating your code once created. This still does not give you generation consistency, though this may be a case where you also point your LLM generator at your github repository and indicate that you should maintain backward compatibility with the code as much as possible when doing the transformation.

Again, perhaps the biggest takeaway is that a little investment in creating an appropriate SHACL schema can pay huge dividends in terms of building operational code regardless of the language.

_The use of SHACL to generate JavaScript is not new … TopQuadrant has been doing it for several years now (pre-AI) with TopBraid EDG’s Active Data Shapes (ADS), and have definitely taken the concept much farther than I’ve explored here (they have also been a major shaper of SHACL). I think SHACL 1.2 is evolving to a stage where this connection between RDF Shapes and programmatic languages is going to prove tighter over time, but I wanted to give credit where credit is due._

In media res,

[

![](https://substackcdn.com/image/fetch/$s_!4hj0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4957a9f2-ea38-4ee9-b6fc-0332a9cbd2cd_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!4hj0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4957a9f2-ea38-4ee9-b6fc-0332a9cbd2cd_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.

