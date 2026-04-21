---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Designing-Meaningful-IRIs-by-Kurt
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:37.857213+00:00'
  title: Designing Meaningful Iris By Kurt
  type: plain-doc
  version: '0.1'
---

# Designing Meaningful Iris By Kurt

[

![](https://substackcdn.com/image/fetch/$s_!s2Pi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe20a1f7c-7eb0-4100-86a9-c7b3211b8c49_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!s2Pi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe20a1f7c-7eb0-4100-86a9-c7b3211b8c49_2688x1536.png)

There are many ways that you can build IRIs, from using generated UUIDs all the way to parsing out the label of a given resource to generate the identifier. Typically, an IRI will have a form something like:

```
http://{authority}/{path/to/term}[#|/]{localName}
```

… where authority is typically a domain name, path/to/term provides a local contextual reference, and localName is the specific term being described in that namespace. The use of # vs. / is optional (and indeed, can be any symbol character, though these two are the ones most generally used).

Thus, http://www.example.com/ns/person#JaneDoe may be considered a valid "standard" URL. However, it's worth noting that any globally unique identifier can be used as an identifier. For instance, [jane.doe123@gmail.com](mailto:jane.doe123@gmail.com) is a valid name for an IRI, although sticklers might prefer to go with:

```
urn:mailto:janedoe123@gmail.com
```

This latter form can then be namespaced as:

```
PREFIX mailto: <urn:mailto:>
```

The PREFIX directive (found in both TURTLE and SPARQL) indicate that anytime you see the prefix with a following colon in a Turtle file, this should be replaced with the namespace. The angle bracketed expression indicates that this is a fully qualified IRI, rather than just a string.

Thus, [mailto:janedoe123@gmail.com](mailto:janedoe123@gmail.com) becomes

```
<urn:mailto:janedoe123@gmail.com>
```

Similarly, if you have the prefix declaration:

```
PREFIX Person: <http://www.example.com/ns/Person#>
```

Then the expression:

```
Person:JaneDoe rdf:type Person: .
```

Is a shorthand for:

```
<http://www.example.com/ns/Person#JaneDoe> http://www.w3.org/1999/02/22-rdf-syntax-ns# <http://www.example.com/nsPerson#> .
```

The shortened form of prefix + localname is referred to as a **curie**, short for **condensed** **URI**. Curies in this context have nothing to do with radiation, and everything to do with making namespaces more manageable.

One aspect that seems to emerge with readable IRIs is that they almost invariably include an authority reference of some sort, as well as a protocol. The authority echoes the use of domain names, as in who owns this particular term, but whereas domain names in the web address space exist primarily to indicate a server location (via the Domain Naming System, or DNS) with IRIs the authority focuses more upon which authority claims a given term, or a given ontology of terms. IRIs inherited this structure, but in the conceptual resource space, the role of the authority is just as valid, even if it is not specifically used to resolve DNS names into IP addresses anymore.

The path structures that are also an artefact of the URL are arguably more vestigial, but they can be used to provide a certain degree of semantics as well. This path structure could be used, for instance, to indicate class designations in inheritance models, though there is less of a consistent best-practice here. Many URI schemes have a single universal namespace (such as rdfs: or sh: or schema:), though in practice what frequently emerges instead is clusters of classes that form subdomains, though the jump from this to formal subclassing is usually quite small.

Local-name practices also tend to vary. Numeric identifiers are easy to fabricate and have no intrinsic semantics, but this also makes it more difficult to identify and debug problems in the graph. Meaningful names, on the other hand, may be easier to use from a pedagogical perspective, but there is also the possibility that such names may very well change if labels change. This event does happen, but it is surprisingly rare, and Sparql Update can be used to change all terms and references to reflect the new label if that happens, meaning that it is not in fact as serious a problem today as it may have been ten or fifteen years ago when such a facility didn't exist.

One key aspect that probably shouldn't be in URI identifiers is versioning information, even though it often is. Versioning is in fact a form of metadata, and as such should be seen as being tied not to a given resource's direct characteristics but rather to annotations that provide scope for when a given assertion is changed. This may be a better discussion to make with respect to reification.

Predicates, properties, classes and shapes usually have a greater need to be human readable, in part because they are more likely to be used "bare" in Turtle, SPARQL, or SHACL, than identifiers for other resources. One particular scheme may be to use TitleCase expressions for namespace prefixes, instances, and class names, and camelCase expressions for predicate local names, just to make them more readily apparent as predicates. However, different organizations may use different conventions. The important aspect is consistency in how you mint your IRIs.

As a final note, beware of putting too much semantics into your identifiers. If you have to parse an identifier to get some crucial piece of information, this is information that is better given as an annotative property. Remember that a human readable IRI is that way primarily for debugging purposes and simplifying queries - it actually has little impact upon the knowledge graph itself.

There’s more that I need to write on decentralized identifiers (DiDs), but this can get deeper into the topic than I want to deal with here.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!hjiN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58c3264e-a788-480b-8124-802ccf351c23_1344x768.png)

](https://substackcdn.com/image/fetch/$s_!hjiN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58c3264e-a788-480b-8124-802ccf351c23_1344x768.png)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.

[

## Knowledge Graphs and AIs

](https://ontologist.substack.com/p/knowledge-graphs-and-ais)

·

February 27, 2025

[![Knowledge Graphs and AIs](https://substackcdn.com/image/fetch/$s_!AkCv!,w_1300,h_650,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80d78cbe-3014-4639-a8cd-3a389b216bd9_1344x768.png)](https://ontologist.substack.com/p/knowledge-graphs-and-ais)

I was asked a question recently - what’s preferable costwise for an enterprise: LLMs or knowledge graphs? This was worth digging into a bit, and while I don’t have hard numbers here, the answer really comes down to what you want to do.

[

## Why Use RDF

](https://ontologist.substack.com/p/why-use-rdf)

·

February 23, 2025

[![Why Use RDF](https://substackcdn.com/image/fetch/$s_!mptG!,w_1300,h_650,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccc4699e-ca44-4f62-988a-0da7bb80ca12_1344x768.png)](https://ontologist.substack.com/p/why-use-rdf)

Here’s a question? Is this RDF?

