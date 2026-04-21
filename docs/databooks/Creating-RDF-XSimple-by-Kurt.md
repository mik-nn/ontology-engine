---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Creating-RDF-XSimple-by-Kurt
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:55.146240+00:00'
  title: Creating Rdf Xsimple By Kurt
  type: plain-doc
  version: '0.1'
---

# Creating Rdf Xsimple By Kurt

[

![](https://substackcdn.com/image/fetch/$s_!lky8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35bcfa40-f770-4264-95e7-1716ce4be9d9_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!lky8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35bcfa40-f770-4264-95e7-1716ce4be9d9_2688x1536.jpeg)

I frequently use SPARQL CONSTRUCT statements (and increasingly SHACL 1.2 node expressions and rules) to generate RDF graphs for output - sometimes to Turtle, sometimes to JSON-LD, and surprisingly often to RDF/XML. However, I think it fair to say that there are very few people who actually _like_ the RDF/XML format. There are several problems with it:

-   **Long URIs everywhere.** People who are finally getting comfortable with the JSON-LD context format find the use of long URIs in attributes and the difficulty of accessing namespaces in XQuery and XSLT to be a real pain. It’s also hard to read.
    
-   **Normalisation.** RDF is normalised - you have blocks with references that point to other blocks in Turtle, but you end up having to write a lot of id/idref code to convert these structures into trees, which are far more natural in XML. This plays a big role in the complexity of both XPath and XSLT**.**
    
-   **Lists, Collections and Obsolete Structures.** RDF-XML was one of the earliest serialisations of RDF, at a time when the RDF specification itself was still relatively new, and as such, there were a number of constructs such as rdf:partType, collections, and linked lists that heavily influenced the XML structure. Many of these are now fairly obsolete.
    
-   `rdf:Description`**,** `rdf:about`**,** `rdf:resource`**, etc.** The enveloping mechanism for RDF/XML was just awkward. You could simplify it a bit, but the reality was that much of the language's human readability was lost.
    

This has been bothering me for a while, because to be perfectly honest, I did want to use XSLT more closely with RDF but it was such a pain to write it that it wasn’t worth the effort.

Finally, I bit the bullet and put in some time (and some coding work with Claude) to create **RDF-XSimple**. The code and specification are available at [https://github.com/kurtcagle/rdf-xsimple](https://github.com/kurtcagle/rdf-xsimple) .

## Design Goals

When I was designing RDF-XSimple (RDF-XS), I turned those pain points into code requirements. Specifically:

-   **Curies.** Just as the context section has made JSON-LD much more useful, there needs to be a way to reduce the need for long IRIs within XML files that identify local resources, replacing them with curies when prefixes are defined.
    
-   **Tree Structures.** When there is only one reference within a dataset to a given entity, it should be possible to make this a subordinate child of that entity, making the output (mostly) hierarchical, simplifying XPath expressions.
    
-   **Simpler Lists.** XML handles lists easier than RDF, so turning the rdf:Collection, rdf:Bag and rdf:Seq into attributes can simplify structures.
    
-   **Support for Reifications.** Reifications are becoming more important in working with RDF, and capturing them consistently should be a high priority for an XML format.
    
-   **Round Tripping.** Any serialisation format should be capable of round-tripping back to RDF with no lossiness or spurious additions.
    

## RDF-XSimple Format

The RDF-XSimple format is standard XML, but designed for RDF production. The following provides a number of examples illustrating the difference between RDF-XML and RDF-XSimple:

## **Example: Namespace Declarations**

### **Traditional RDF/XML**

```
<rdf:RDF 
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
  xmlns:schema="http://schema.org/"
  xmlns:foaf="http://xmlns.com/foaf/0.1/">
```

### **RDF-XSimple**

```
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:context>
    <rdf:prefix name="schema" uri="http://schema.org/"/>
    <rdf:prefix name="foaf" uri="http://xmlns.com/foaf/0.1/"/>
    <rdf:prefix name="ex" uri="http://example.org/"/>
  </rdf:context>
```

**Benefits:**

-   ✅ All prefixes in one place
    
-   ✅ Easy to add/modify
    
-   ✅ Can be externalized/reused
    
-   ✅ Consistent with JSON-LD `@context`
    

## **Example: Resource Identifiers**

### **Traditional RDF/XML**

```
<rdf:Description rdf:about="http://example.org/people/alice-smith">
  <schema:worksFor rdf:resource="http://example.org/organizations/tech-corp"/>
</rdf:Description>
```

### **RDF-XSimple**

```
<schema:Person rdf:about="ex:people/alice-smith">
  <schema:worksFor rdf:resource="ex:organizations/tech-corp"/>
</schema:Person>
```

**Benefits:**

-   ✅ 70% shorter URIs
    
-   ✅ Easier to read and type
    
-   ✅ Namespace changes only affect context
    
-   ✅ Matches Turtle/SPARQL syntax
    

## **Example: Datatypes**

### **Traditional RDF/XML**

```
<schema:age rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">32</schema:age>
<schema:height rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">1.68</schema:height>
<schema:birthDate rdf:datatype="http://www.w3.org/2001/XMLSchema#date">1992-03-15</schema:birthDate>
```

### **RDF-XSimple**

```
<schema:age type="integer">32</schema:age>
<schema:height type="decimal">1.68</schema:height>
<schema:birthDate type="date">1992-03-15</schema:birthDate>
```

**Benefits:**

-   ✅ 75% shorter datatype declarations
    
-   ✅ More readable
    
-   ✅ Matches common programming languages
    
-   ✅ Still supports custom datatypes
    

## **Example: Structure (Denormalization)**

### **Traditional RDF/XML (Normalized)**

```
<rdf:Description rdf:about="http://example.org/people/alice-smith">
  <schema:address rdf:resource="http://example.org/addresses/addr-1001"/>
</rdf:Description>

<rdf:Description rdf:about="http://example.org/addresses/addr-1001">
  <rdf:type rdf:resource="http://schema.org/PostalAddress"/>
  <schema:streetAddress>742 Evergreen Terrace</schema:streetAddress>
  <schema:addressCountry rdf:resource="http://example.org/countries/usa"/>
</rdf:Description>

<rdf:Description rdf:about="http://example.org/countries/usa">
  <rdf:type rdf:resource="http://schema.org/Country"/>
  <schema:name xml:lang="en">United States</schema:name>
</rdf:Description>
```

### **RDF-XSimple (Smart Denormalized)**

```
<schema:Person rdf:about="ex:people/alice-smith">
  <schema:address>
    <schema:PostalAddress rdf:about="ex:addresses/addr-1001">
      <schema:streetAddress>742 Evergreen Terrace</schema:streetAddress>
      <schema:addressCountry>
        <schema:Country rdf:about="ex:countries/usa">
          <schema:name lang="en">United States</schema:name>
        </schema:Country>
      </schema:addressCountry>
    </schema:PostalAddress>
  </schema:address>
</schema:Person>
```

**Benefits:**

-   ✅ Hierarchical structure matches data relationships
    
-   ✅ Single-reference resources automatically inlined
    
-   ✅ Preserves resource identity with `rdf:about`
    
-   ✅ Easier to understand data model
    
-   ✅ Still produces identical RDF triples
    

## **Example: Lists**

### **Traditional RDF/XML**

```
<rdf:Description>
  <schema:skillRanking rdf:parseType="Collection">
    <rdf:Description>
      <schema:name>Python</schema:name>
      <schema:proficiencyLevel rdf:datatype="...#integer">5</schema:proficiencyLevel>
    </rdf:Description>
    <rdf:Description>
      <schema:name>JavaScript</schema:name>
      <schema:proficiencyLevel rdf:datatype="...#integer">4</schema:proficiencyLevel>
    </rdf:Description>
  </schema:skillRanking>
</rdf:Description>
```

### **RDF-XSimple**

```
<schema:skillRanking rdf:list="true">
  <schema:Skill>
    <schema:name>Python</schema:name>
    <schema:proficiencyLevel type="integer">5</schema:proficiencyLevel>
  </schema:Skill>
  <schema:Skill>
    <schema:name>JavaScript</schema:name>
    <schema:proficiencyLevel type="integer">4</schema:proficiencyLevel>
  </schema:Skill>
</schema:skillRanking>
```

**Benefits:**

-   ✅ Clear `rdf:list="true"` attribute
    
-   ✅ Also supports `rdf:bag="true"` and `rdf:seq="true"`
    
-   ✅ More XML-idiomatic
    
-   ✅ Distinguishes ordered vs. unordered collections
    

## **Example: RDF-star (NEW!)**

### **Traditional RDF/XML**

```
<!-- NOT SUPPORTED -->
```

### **RDF-XSimple**

```
<ex:EmploymentClaim rdf:about="ex:claims/claim-001">
  <rdf:quotes>
    <rdf:QuotedTriple>
      <rdf:subject rdf:resource="ex:people/alice-smith"/>
      <rdf:predicate rdf:resource="schema:worksFor"/>
      <rdf:object rdf:resource="ex:organizations/tech-corp"/>
    </rdf:QuotedTriple>
  </rdf:quotes>
  <ex:verifiedBy rdf:resource="ex:hr-database"/>
  <ex:verifiedDate type="dateTime">2024-01-15T10:30:00Z</ex:verifiedDate>
  <ex:confidence type="decimal">1.0</ex:confidence>
</ex:EmploymentClaim>
```

**Benefits:**

-   ✅ Make statements about statements
    
-   ✅ Track provenance and confidence
    
-   ✅ Support temporal validity
    
-   ✅ Critical for knowledge graphs
    

Note that while the RDF-XSimple spec supports RDF-Star reification, RDF/XML doesn’t yet. RDF-XSimple should (soon) support Turtle 1.2, which does have reification capabilities.

## Using RDF-XSimple

RDF-XSimple is intended principally as a target format for RDF-XML (and vice versa) - once you generate the RDF-XML from a SPARQL call, then you can transform it into RDF-XSimple in a number of different ways:

```
# Using Saxon
saxon -s:input.rdf -xsl:xslt/rdfxml1-to-rdfxml2.xsl -o:output.rdf

# Using xsltproc
xsltproc xslt/rdfxml1-to-rdfxml2.xsl input.rdf > output.rdf
```

where the transformations are contained in the GitHub project listed above.

Transform RDF-XSimple back to standard RDF/XML:

```
saxon -s:input.rdf -xsl:xslt/rdfxml2-to-rdfxml1.xsl -o:output.rdf
```

### **Schema Validation**

Validate documents against the XSD schema:

```
# Validate single file
xmllint --schema schema/rdfxml2.xsd examples/simple-person.rdf

# Validate all examples
./validate-examples.sh
```

Using Python:

```
from lxml import etree

schema = etree.XMLSchema(file=’schema/rdfxml2.xsd’)
doc = etree.parse(’examples/simple-person.rdf’)

if schema.validate(doc):
    print(”Valid!”)
else:
    print(schema.error_log)
```

### **Node.js**

```
const { transform } = require(’saxon-js’);
const fs = require(’fs’);

transform({
  stylesheetFileName: ‘xslt/rdfxml1-to-rdfxml2.xsl’,
  sourceFileName: ‘input.rdf’,
  destination: ‘serialized’
}).then(output => {
  fs.writeFileSync(’output.rdf’, output.principalResult);
});
```

### **Python**

```
from lxml import etree

# Load XSLT
xslt = etree.parse(’xslt/rdfxml1-to-rdfxml2.xsl’)
transform = etree.XSLT(xslt)

# Load RDF/XML
doc = etree.parse(’input.rdf’)

# Transform
result = transform(doc)
print(str(result))
```

The resulting XML can then be used more effectively within an XSLT toolchain, with XQuery, or with XProc.

## Caveats

I’m working on direct Turtle2RDF-XSimple and JSONLD2RDF-XSimple projects related to this.

RDF-XSimple is a work in progress and should definitely be considered alpha software at this point. Please contact me at kurt.cagle@gmail.com with bug reports, questions or comments.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!i8Zl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Facdad02d-1872-4838-8574-f8e9e026e11c_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!i8Zl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Facdad02d-1872-4838-8574-f8e9e026e11c_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.

