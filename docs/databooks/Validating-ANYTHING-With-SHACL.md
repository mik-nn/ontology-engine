---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Validating-ANYTHING-With-SHACL
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:39.305700+00:00'
  title: Validating Anything With Shacl
  type: plain-doc
  version: '0.1'
---

# Validating Anything With Shacl

[

![](https://substackcdn.com/image/fetch/$s_!Rd2m!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66534b24-56f2-4148-871b-74cd2dcf4035_1408x768.png)

](https://substackcdn.com/image/fetch/$s_!Rd2m!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66534b24-56f2-4148-871b-74cd2dcf4035_1408x768.png)

SHACL (the Shape Constraint Language) was first introduced in 2017 as a variation of another RDF standard called SHEX (Shape Expression Language). It’s purpose was to provide a schema language that more closely aligned with languages such as the XML Schema Definition Language (XSD), a language that could be used to better validate data structures within RDF.

## A History of Validation

_**Validation**_ is an interesting concept. In general, when you create a data structure in code, it is typically created by specifying data types or class types. This goes way back to the earliest days of coding, where there were explicit types of registers that were used for storing integers vs. floating point numbers vs. character arrays (what we now refer to as strings). This later extended to identifying specific _types,_ which created aggregate structures for these values (a similar evolution was happening in the database world).

By the late 1970s, we were making the transition from type-oriented systems (passing data structures to piped processes) to object-oriented, keeping objects persistent in memory, and binding methods to specific properties. This didn’t translate quite as well in database systems, even with the advent of stored procedures, but because most database systems had fixed schemas, validation was largely a function of data entry programming that was intended to catch errors and apply business logic outside of the database.

It was really not until the advent of XML that this began to change. XML was the original soft data format (though you can argue that this honour actually goes to SGML - the Standard Generalised Markup Language - which dates back to work that [Charles Goldfarb](https://en.wikipedia.org/wiki/Charles_Goldfarb), Edward Mosher, and Raymond Lorie did in the 1960s. The one distinction was that SGML’s primary focus was on documents, while XML represented the fusion of this principle with HTML’s Document Object Model (DOM), and its real use for representing data didn’t really emerge until the late 1990s.

_Historical Note:_ My first book, ([Visual Basic 6 Client/Server Programming Gold Book](https://dl.acm.org/doi/abs/10.5555/552284)) written in 1998, as the XML spec was getting finalized, was one of the first to talk about XML as a data representation language rather than just a document language. Much of this book is now very dated, of course, but I’ve been thinking about data representation for a while now.

XML made a fairly radical shift in data representation. Prior to that, schema was intrinsic: when you created a database, your tools would generate a DDL (Data Definition Language) schema that would then be embedded into the database itself. With XML, on the other hand, you could create an XML file without specifically requiring that you had a schema, though you could create a link to that schema (originally an SGML schema, later the XML Schema Definition Language, or XSD), which was also structured in XML.

This was important for several reasons. First, it meant that you could parse an XML file into an XML DOM that had an implicit structure without needing to formally specify that structure. While the XML wasn’t formally self-describing, it met many of the key criteria for doing so. If you _did_ have that schema, however, you could use tools like XSLT and later XQuery to read in the schema and determine which elements were displayed, in which order, using which datatype, and indicating the structures and cardinality information. XML is a graph language, albeit one that is mostly hierarchical in nature, and as a consequence, many of the characteristics that were wanted in a schematic structure were fairly well known for some time.

XSD was the third (or arguably the fifth, if you count XPath as a separate spec) major specification, and like all of the XML “support” stack, XPath plays a very large role in XSD. The language defines a structure. A document can be parsed in one pass and validated in a second, where the _validator_ looks at each node in turn of the XML traversal tree and checks to see if it satisfies the requirements for that element. If it does, XSD does nothing, but if it fails, XSD provides a mechanism to identify WHY that particular node failed.

In the earliest incarnations of XSD, validation was an all or nothing affair - a document either passed, or it failed, though it would give all of the failure points as a result set of messages through the validator (again, the earliest were just text, but more recent iterations include XML and (later) JSON iterations giving errors that were found by the validator when using XSD as the validation format.

While XSD was a necessary first step, it didn’t handle a number of fairly common use cases as well as it could have. One of the biggest of these was contextual constraints, in which the validity of a given node was dependent upon some other node in the XML DOM. _Rick Jeliffe_ (whom I have worked with) created an additional language called Schematron in 1999 that filled this gap, while also making it possible to create specific phases or profiles that could validate a document based upon different conditions in the XML. Much of Schematron, in turn, was folded into the XSD 1.1 update in 2012.

JSON was originally notable for “not needing a schema” (based upon several discussions I had with Douglas Crockford in the late oughts), but by 2013, the need for consistency weighed in to a sufficient level that a JSON Schema language was first proposed, and formally ratified as an ISO standard in 2017. It contains many of the same elements of assertions and validations that XSD utilised, albeit in a somewhat simpler format (naturally) compared to XSD, which is a monster of a specification, a charge that has been levelled against the spec by a number of authorities. More recently, the OpenAPI specification (formerly Swagger) and the Model Context Protocol used for LLM-based agentic services both borrow fairly heavily from JSON Schema, drawing a lineage back to XSD.

## RDF and OWL

RDF emerged about the same time as XML, but took a fairly different turn with regard to validation. Much of the initial design for RDF came out of the work with Cyc and formal logical systems. The initial RDF schema was very basic, incorporating a few essential classes (such as rdfs:Class and rdfs:Property), a few set definitions (rdf:Bag, rdf:Seq and rdf:Alt) and some primary inheritance properties (rdfs:subClassOf, rdfs:subPropertyOf, rdfs:domain and rdfs:range). It is possible to do a surprising amount with even the minimal set of RDFS, but at the same time, it was clearly a first step that never really evolved beyond its initial design. This was likely due to the presence of OWL.

Most of the real power came from the introduction of OWL, which established a much broader set of classes and properties in order to build fully inferential systems. In order to make such systems work, OWL also introduced the concept of inferential predicates that, when imported into the knowledge graph, would trigger a set of rules that would then generate additional triples. For instance, let’s say that you had a set of statements such as:

```
person:JD1 a Class:Person ;
    person:hasName "Jane Doe" ;
    person:hasAddress "1313 Mockingbird Ln" ;
    .

person:JD2 a Class:Person ;
    person:hasSchool School:GarfieldElementarySchool ;
    .

person:JD1 owl:sameAs person:JD2 .
```

When that final statement is parsed, a reasoner system would apply a specific set of rules (one for symmetry, one for transitive relationships, and one for copying) that would end up with both entries looking like the following:

```
person:JD1 a Class:Person ;
    person:hasName "Jane Doe" ; 
    person:hasAddress "1313 Mockingbird Ln" ;
    person:hasSchool School:GarfieldElementarySchool ; # Added from JD2
    .

person:JD2 a Class:Person ;
    person:hasName "Jane Doe" ; # Added from JD1
    person:hasAddress "1313 Mockingbird Ln" ;  # Added from JD1
    person:hasSchool School:GarfieldElementarySchool ;
    .

person:JD1 owl:sameAs person:JD2 .
```

If applied sparingly, this can be a very useful utility, but it effectively serves to double the number of triples defined within a system. Transitive relationships (if A → B and B → C, then A → C) could similarly be defined, but typically this also added considerably to the number of triples.

OWL makes extensive use of restrictions to qualify properties, which can be useful but also lead to very confusing files from an analysis perspective, especially as the number of alternative properties makes modelling very incumbent upon the modeller’s own experience and training. Inference worked great if you had been trained in formal logical systems, but especially as information shifted increasingly towards storing data rather than just relationships, OWL became an impediment for those who were already predisposed not to get into RDF because it didn’t fit into the JavaScript paradigm and, worse, had … _namespaces_.

It’s also worth noting that while OWL was designed around inferencing, it was fairly lacklustre with regard to the ability to control how invalid constraints were handled, especially since it assumed a binary state with regard to how structures were defined - something was either valid or it was not. While it was possible to create rules that would let you specify this as data, there was no single standard for managing validation rules or reporting.

This situation was then exacerbated by the rise of SPARQL, which made it possible to create ad hoc queries that could do everything that inferencing rules could do, but were easier to express. Finally, by the mid-2010s, the balance of use for RDF was beginning to shift away from large-scale inferential systems and toward data-oriented infrastructure that was more consistent in design, especially with the advent of SPARQL UPDATE in 2013, the standardisation on Turtle, and a new generation of ontologists who were more familiar with JSON than they were XML.

## Validation via SHACL

OWL is not going away, but there is definitely a shift occurring within the semantic community around the use of SHAPES, rather than classes and properties. A **shape** is, at its core, simply a pattern that is common to one or more nodes in a graph. A shape can describe an individual node or class of nodes, a property, or other constraints, including those described by SPARQL, a function, or templates of various sorts. Most of the time, SHACL files contain primarily _**Node Shapes**_ and _**Property Shapes**_.

Node shapes typically describe a given node instance, and are usually intended to describe the set of properties that the instance should have. A NodeShape is not a class, but you can associate a node shape with a class, though you don’t necessarily need to. For instance, consider the following node shape:

```
# pet.shacl.ttl
prefix sh: <http://www.w3.org/ns/shacl#>
prefix ex: <http://www.example.com#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#> 


ex:Pet_Shape a sh:NodeShape ;
    sh:targetClass ex:Class_Pet ;
    sh:property [
        sh:path ex:hasBreed ;
        sh:nodeKind sh:IRI ;
        sh:class ex:Breed ;
        ] ;
    sh:property [
        sh:path ex:hasAge ;
        sh:nodeKind sh:Literal ;
        sh:datatype xsd:nonNegativeInteger ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        ] ;
   sh:property [
        sh:path ex:hasName ;
        sh:nodeKind sh:Literal ;
        sh:datatype xsd:string ;
        ] ; 
   sh:property [
        sh:path ex:hasSpecies ;
        sh:nodeKind sh:IRI ;
        sh:class ex:Species ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
       ] ;
   sh:property [
        sh:path ex:hasCoat ;
        sh:nodeKind sh:IRI ;
        sh:class ex:Coat ;
       ] ;
.
```

The name of the shape in this particular case is unimportant; it could just as readily be a blank node, though it is sometimes convenient to give names just to make them more readily identifiable. In this particular case, the shape is associated with a class of Pets, with four property shapes that are bound to a particular property shape.

The following is an example of a valid node in Turtle:

```
# pet1.ttl
prefix sh: <http://www.w3.org/ns/shacl#>
prefix ex: <http://www.example.com#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#> 


ex:Felicia a ex:Class_Pet ;
    ex:hasBreed ex:Breed_AmericanShorthair ;
    ex:hasAge "5"^^xsd:nonNegativeInteger ;
    ex:hasName "Felicia" ;
    ex:hasSpecies ex:Species_Cat ;
    ex:hasCoat ex:Calico ;
    .

ex:Breed_AmericanShorthair a ex:Breed .
ex:Species_Cat a ex:Species .
ex:Calico a ex:Coat .
```

There are a number of different tools for validating an RDF source with shacl. I use the Jena command line utilities (https://jena.apache.org/documentation/tools/) as they are generally the most up to date with respect to the SHACL documentation. The shacl tool that can then validate the above file would be invoked as:

```
> shacl validate --shapes pet.shacl.ttl --data pet1.ttl
```

This generates the following output:

```
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh:   <http://www.w3.org/ns/shacl#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

[ rdf:type     sh:ValidationReport;
  sh:conforms  true
] .
```

The validation report is what you get back when you validate a data file against a SHACL file. If everything is copacetic, then you should get the simple confirmation:

```
[] sh:conforms true .
```

This should of course what you want to have come back. On the other hand, let’s say that your file was not conformant:

```
# pet2.ttl
prefix sh: <http://www.w3.org/ns/shacl#>
prefix ex: <http://www.example.com#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#> 


ex:Felicia a ex:Class_Pet ;
    ex:hasBreed ex:Breed_AmericanShorthair ;
    ex:hasAge "Five"^^xsd:nonNegativeInteger ;
    ex:hasName "Felicia" ;
    ex:hasSpecies ex:Species_Cat, ex:Species_Dog ;
    ex:hasCoat ex:Calico ;
    .

ex:Breed_AmericanShorthair a ex:Breed .
ex:Species_Cat a ex:Species .
ex:Species_Dog a ex:Species .

ex:Calico a ex:Coat .
```

Running the utility from the command line:

```
shacl validate --shapes pet.shacl.ttl --data pet2.ttl
```

will yield a rather different result:

```
PREFIX ex:   <http://www.example.com#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh:   <http://www.w3.org/ns/shacl#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

[ rdf:type     sh:ValidationReport;
  sh:conforms  false;
  sh:result    [ rdf:type                      sh:ValidationResult;
                 sh:focusNode                  ex:Felicia;
                 sh:resultMessage              "DatatypeConstraint[xsd:nonNegativeInteger] : Not valid value : Node \"Five\"^^xsd:nonNegativeInteger";
                 sh:resultPath                 ex:hasAge;
                 sh:resultSeverity             sh:Violation;
                 sh:sourceConstraintComponent  sh:DatatypeConstraintComponent;
                 sh:sourceShape                [] ;
                 sh:value                      "Five"^^xsd:nonNegativeInteger
               ];
  sh:result    [ rdf:type                      sh:ValidationResult;
                 sh:focusNode                  ex:Felicia;
                 sh:resultMessage              "maxCount[1]: Invalid cardinality: expected max 1: Got count = 2";
                 sh:resultPath                 ex:hasSpecies;
                 sh:resultSeverity             sh:Violation;
                 sh:sourceConstraintComponent  sh:MaxCountConstraintComponent;
                 sh:sourceShape                []
               ]
] .
```

In this particular case, two errors were introduced: the number 5 was replaced with the string “five”, and Felicia has two species declared - cat and dog. Note that the validator returns both of these errors, which is one of the benefits of working with validators: you can identify all of the problem spots in our documents at once, rather than have to step through each error, correct it, then go on to the next.

> It’s worth noting that there is a distinction between _parsing_ and _validating_. The file pet2.ttl is valid Turtle syntactically, and as a consequence a parser should parser it just fine. It is, however, _invalid_ with respect to the shapes that you have created - it does not conform to expectations, and it will likely break your system if allowed to propagate.

## Using SHACL with JSON-LD

While on the topic of command utilities, the \`riot\` command in the same utility set is useful for converting between different formats. For instance, you could convert the pet2.ttl file to JSON-LD with a single command line call:

```
riot -output=JSONLD pet2.ttl > pet2.jsonld
```

This generates the output:

```
{
    "@graph": [
        {
            "@id": "ex:Calico",
            "@type": "ex:Coat"
        },
        {
            "@id": "ex:Species_Dog",
            "@type": "ex:Species"
        },
        {
            "@id": "ex:Species_Cat",
            "@type": "ex:Species"
        },
        {
            "@id": "ex:Breed_AmericanShorthair",
            "@type": "ex:Breed"
        },
        {
            "@id": "ex:Felicia",
            "ex:hasCoat": {
                "@id": "ex:Calico"
            },
            "ex:hasSpecies": [
                {
                    "@id": "ex:Species_Dog"
                },
                {
                    "@id": "ex:Species_Cat"
                }
            ],
            "ex:hasName": "Felicia",
            "ex:hasAge": {
                "@value": "Five",
                "@type": "xsd:nonNegativeInteger"
            },
            "ex:hasBreed": {
                "@id": "ex:Breed_AmericanShorthair"
            },
            "@type": "ex:Class_Pet"
        }
    ],
    "@context": {
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "sh": "http://www.w3.org/ns/shacl#",
        "ex": "http://www.example.com#"
    }
}
```

Moreover, you can validate that same JSON-LD file just as you would the turtle file:

```
shacl validate --shapes pet.shacl.ttl --data pet2.jsonld
```

with the same response (ditto for using pet.shacl.jsonld).

Let me emphasise why this is so significant:

> You can use SHACL in your JSON based workflows to validate that JSON without having to write a lick of Turtle or XML.

You can even get the output in JSON-LD by using riot. The command

```
shacl validate --shapes pet.shacl.ttl --data pet2.jsonld | riot --syntax turtle --output jsonld > report2.jsonld
```

The SHACL generates the report on pet2.jsonld, with the output then being a turtle file. You can then use riot via a pipe by setting the syntax to turtle and output to JSON-LD, then saving this to report2.jsonld.

```
// report2.jsonld
{
    "@graph": [
        {
            "@id": "_:b0",
            "sh:sourceShape": {
                "@id": "_:b1"
            },
            "sh:sourceConstraintComponent": {
                "@id": "sh:MaxCountConstraintComponent"
            },
            "sh:resultSeverity": {
                "@id": "sh:Violation"
            },
            "sh:resultPath": {
                "@id": "ex:hasSpecies"
            },
            "sh:resultMessage": "maxCount[1]: Invalid cardinality: expected max 1: Got count = 2",
            "sh:focusNode": {
                "@id": "ex:Felicia"
            },
            "@type": "sh:ValidationResult"
        },
        {
            "@id": "_:b2",
            "sh:value": {
                "@value": "Five",
                "@type": "xsd:nonNegativeInteger"
            },
            "sh:sourceShape": {
                "@id": "_:b3"
            },
            "sh:sourceConstraintComponent": {
                "@id": "sh:DatatypeConstraintComponent"
            },
            "sh:resultSeverity": {
                "@id": "sh:Violation"
            },
            "sh:resultPath": {
                "@id": "ex:hasAge"
            },
            "sh:resultMessage": "DatatypeConstraint[xsd:nonNegativeInteger] : Not valid value : Node \"Five\"^^xsd:nonNegativeInteger",
            "sh:focusNode": {
                "@id": "ex:Felicia"
            },
            "@type": "sh:ValidationResult"
        },
        {
            "@id": "_:b4",
            "sh:result": [
                {
                    "@id": "_:b0"
                },
                {
                    "@id": "_:b2"
                }
            ],
            "sh:conforms": {
                "@value": "false",
                "@type": "xsd:boolean"
            },
            "@type": "sh:ValidationReport"
        }
    ],
    "@context": {
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "ex": "http://www.example.com#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "sh": "http://www.w3.org/ns/shacl#"
    }
}
```

This is one of the reasons why I believe that SHACL has a bright future: as long as you use the JSONLD form of JSON (which usually means adding in a @context section to your JSON file), you can use the expressivity of SHACL to give you deep-level validation without having to deal with Turtle at all.

By the way, the shacl file itself in JSONLD is very straightforward (this is using the compact JSONLD profile):

```
{
  "@context": {
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "sh": "http://www.w3.org/ns/shacl#",
    "ex": "http://www.example.com#"
  },
  "@id": "ex:Pet_Shape",
  "@type": "sh:NodeShape",
  "sh:targetClass": "ex:Class_Pet",
  "sh:property": [
    {
      "sh:path": "ex:hasCoat",
      "sh:class": "ex:Coat",
      "sh:nodeKind": "sh:IRI"
    },
    {
      "sh:path": "ex:hasSpecies",
      "sh:class": "ex:Species",
      "sh:nodeKind": "sh:IRI",
      "sh:minCount": 1,
      "sh:maxCount": 1
    },
    {
      "sh:path": "ex:hasName",
      "sh:datatype": "xsd:string",
      "sh:nodeKind": "sh:Literal"
    },
    {
      "sh:path": "ex:hasAge",
      "sh:datatype": "xsd:nonNegativeInteger",
      "sh:nodeKind": "sh:Literal",
      "sh:minCount": 1,
      "sh:maxCount": 1
    },
    {
      "sh:path": "ex:hasBreed",
      "sh:class": "ex:Breed",
      "sh:nodeKind": "sh:IRI"
    }
  ]
}
```

The same thing can apply to rdf-xml validation (user `rdfxml` rather than `jsonld` for syntax or output parameters), though given the robustness of XSD, this makes up a much less significant use case.

## Controlling Messages and Severity

The example given above is very simple and represents only a small portion of what SHACL is capable of doing. For instance, you might want to add a check to make sure that the age of the pet in question is not less than 0 nor greater than 40 (the oldest cat on record was 38 years old). A new property shape can be added to the above SHACL definition:

```
# Separate constraint for age >= 0
ex:Age_NonNegative_Shape a sh:NodeShape ;
    sh:targetClass ex:Class_Pet ;
    sh:property [
        sh:path ex:hasAge ;
        sh:minInclusive 0 ;
        sh:message "Age must be 0 or greater"
    ] .

# Warning for age >= 40
ex:Age_Warning_Shape a sh:NodeShape ;
    sh:targetClass ex:Class_Pet ;
    sh:property [
        sh:path ex:hasAge ;
        sh:maxExclusive 40 ;
        sh:severity sh:Warning ;
        sh:message "It is unlikely the animal is older than 40"
    ] .
```

Note here that each of these shapes applies to the same path (`ex:hasAge`) but they test for different conditions. Adding these into pet.shacl.ttl, we can then put it to the test in pet3.ttl

```
# pet3.ttl
prefix sh: <http://www.w3.org/ns/shacl#>
prefix ex: <http://www.example.com#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#> 


ex:Felicia a ex:Class_Pet ;
    ex:hasBreed ex:Breed_AmericanShorthair ;
    ex:hasAge "55"^^xsd:nonNegativeInteger ;
    ex:hasName "Felicia" ;
    ex:hasSpecies ex:Species_Cat ;
    ex:hasCoat ex:Calico ;
    .

ex:Breed_AmericanShorthair a ex:Breed .
ex:Species_Cat a ex:Species .
ex:Species_Dog a ex:Species .

ex:Calico a ex:Coat .
```

When validating this node against the updated shape, as follows:

```
shacl validate --shapes pet.shacl.ttl --data pet3.ttl > report3.ttl
```

you get the following response (report3.ttl):

```
PREFIX ex:   <http://www.example.com#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh:   <http://www.w3.org/ns/shacl#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

[ rdf:type     sh:ValidationReport;
  sh:conforms  false;
  sh:result    [ rdf:type                      sh:ValidationResult;
                 sh:focusNode                  ex:Felicia;
                 sh:resultMessage              "It is unlikely the animal is older than 40";
                 sh:resultPath                 ex:hasAge;
                 sh:resultSeverity             sh:Warning;
                 sh:sourceConstraintComponent  sh:MaxExclusiveConstraintComponent;
                 sh:sourceShape                [] ;
                 sh:value                      "55"^^xsd:nonNegativeInteger
               ]
] .
```

This report indicates that the example doesn’t conform, but this isn’t necessarily a showstopper. The result identifies the focus node (`ex:Felicia`), and it indicates that there’s a very low likelihood that Felicia is the indicated age of 55. Additionally, this is a warning (as opposed to a `sh:Violation` or `sh:Info` severity): the data should be examined, preferably from the source (it may simply be a typo where “5” was intended), but it’s still possible that the pet in question is in fact that age.

The `sh:focusNode` property identifies the node being examined. If the data file contained a number of different objects, then there will be one result for each node that matches the conditions in the NodeShape section (here, that the node in question is an `ex:Pet`) and ignores any nodes where this is not the case. You can set additional constraints. For instance, the NodeShape may have the sh:targetSubjectsOf or sh:targetObjectsOf statements, with the object in each case being a predicate, such as ex:hasSpecies (added to a new SHACL query pet4.shacl.ttl):

```
PREFIX ex:   <http://www.example.com#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh:   <http://www.w3.org/ns/shacl#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

[] a sh:NodeShape ;
     sh:targetSubjectsOf ex:hasSpecies ;
     sh:property [
          sh:path ex:hasSpecies ;
          sh:hasvalue ex:Species_Cat ;
     ] .
```

In this particular case, the only nodes that are targets are those that have a predicate of `ex:hasSpecies` for which the value of the corresponding object is `ex:Species_Cat`. This approach creates something akin to a class without actually creating one, relying instead on a common constraint (all entries of the species “cat”).

The advantage to this (and consequently one of the big advantages that SHACL offers) is that you don’t end up trying to overload classes, to me one of the biggest problems that OWL has.

## Uses of SHACL

SHACL Validation serves a number of functions.

-   **Data Quality Assurance.** When data, whether generated by a computer system or through a user interface, enters a system, SHACL can serve as an inspector, flagging suspect data and making it easier to ascertain why it is problematic, while letting clean data through. As such, it should be seen as part of a streaming pipeline.
    
-   **Classification.** On the flip side, sometimes data comes in that has no classification and consists of many facets, each of which has a specific range where the values of those facets are valid. This is especially true of sensor data. By identifying that a given shape can be associated with a node (and with several potential shapes bound to that same node) it makes it possible to provide classification on that node.
    
-   **Structural Definition.** By establishing validation, you also determine the structure that data should take. This becomes critical for data entry and submission, as these in turn determine characteristics of the objects in question.
    
-   **Binding Functional Metadata.** A method is simply a property with an associated action (potentially contextually parameterised). This makes it possible to bridge the gap between object-oriented programming and graph storage.
    
-   **User Interfaces.** The forms necessary for data entry can be derived from SHACL structures in a way that is difficult to do from OWL. This can also be used in conjunction with generative AI.
    

In short, SHACL can work with both streaming data (small graphs) and knowledge graphs to build out large-scale, consistent applications.

I will be exploring these topics in greater depth in subsequent posts.

In Media Res,

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.

