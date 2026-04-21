[

![](https://substackcdn.com/image/fetch/$s_!VxID!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdca3f3b0-8607-4f61-88d0-070e22a46380_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!VxID!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdca3f3b0-8607-4f61-88d0-070e22a46380_2688x1536.jpeg)

In [Part I of this series](https://ontologist.substack.com/p/databooks-markdown-as-semantic-infrastructure), we introduced the DataBook format — a Markdown document that functions simultaneously as human-readable text, a typed data container, and a self-describing semantic artifact. We argued that Markdown, far from being a lightweight presentational format, carries the structural DNA needed to become a genuine semantic infrastructure layer.

That was the _what_. This article is about the _what it does_.

Specifically, we want to examine what happens when you treat a DataBook not just as a container but as an active participant in a semantic pipeline — one that carries its own queries, validates itself against its own shapes, documents its own intent, tracks its own lineage, controls access to its own content, and knows how to point at — or partition — the data it manages. This is the semantic execution layer, and it changes the way you think about data workflows.

## Documentation as Infrastructure

There’s a tendency, in technical work, to treat documentation as something you add at the end. A README. A comment block. A wiki page that gradually becomes wrong. The data lives in one place; the explanation of the data lives somewhere else, drifting apart over time until the map no longer matches the territory.

DataBooks invert this. Documentation isn’t appended — it’s _structural_. The prose sections of a DataBook aren’t decoration around the fenced blocks; they’re the context that gives those blocks meaning. You write, in natural language, what this data represents, where it came from, how it should be used, what its known limitations are, and what you were thinking when you built it.

This turns out to have a surprising side effect: it changes how you think about data in the first place.

When you have to articulate — in prose, to a hypothetical future reader — what a SHACL shape is doing, or why this SPARQL query selects those particular predicates, or what semantic contract this Turtle graph is intended to satisfy, you encounter gaps in your own understanding that you wouldn’t have noticed otherwise. The act of documentation becomes an act of clarification. The document is not just describing the data; it’s stress-testing it.

This is not a minor convenience. In a world where LLMs are increasingly participants in data pipelines — reading DataBooks, generating content from them, validating them, transforming them — having the intent of the data expressed in natural language _inside the artifact_ becomes load-bearing. The prose is no longer for human readers only.

Serious RDF work requires four things to function coherently: a shape layer (SHACL), a reasoning layer (OWL or similar), a classification layer (taxonomies, concept schemes), and a query layer (SPARQL). We’ll call this the _semantic quad_.

In practice, most RDF workflows scatter these across separate files, separate repositories, separate services. Your data lives in one triplestore. Your shapes live in another file, probably referenced by a URL that may or may not be resolvable. Your taxonomy is a separate SKOS file loaded at startup. Your queries are strings in application code, or files in a `queries/` directory, loosely associated with the data by convention and proximity.

This architecture is technically functional and practically fragile. The coupling between data and its semantic context is implicit, convention-dependent, and invisible to any tool that doesn’t already understand your specific project structure. Sharing such a dataset with a colleague — or a pipeline — requires transmitting not just the data but a mental model of how all the pieces fit.

DataBooks offer an alternative: put the quad in the document.

A DataBook can carry `turtle` blocks for instance data, `shacl` blocks for constraint shapes, `turtle` or `json-ld` blocks for ontology fragments and SKOS concept schemes, and both `sparql` and `sparql-update` blocks for query logic — all in a single file, each block identified, labeled, and accompanied by prose that explains its role. The semantic context travels with the data. The contract is explicit.

This isn’t about replacing a triplestore. For large-scale production data, you still want Jena or similar. But the _specification_ of what that triplestore should contain, how its contents should be constrained, and what queries should be applied to it — that belongs in the DataBook.

[Example 25](https://github.com/kurtcagle/databook/blob/main/examples/example-25-semantic-quad.databook.md) in the DataBook repository demonstrates a complete semantic quad DataBook — instance data, SKOS taxonomy fragment, SHACL shapes, and SPARQL queries in a single coherent document.

## SPARQL as a First-Class Layer

Of all the components in the semantic quad, SPARQL gains the most from DataBook colocation — partly because query-data separation has historically been so severe, and partly because SPARQL’s two modes (retrieval and update) serve fundamentally different roles that benefit from being named and documented distinctly.

A `sparql` block in a DataBook carries a SELECT, CONSTRUCT, ASK, or DESCRIBE query. The query exists in context: the prose around it explains what it’s asking and why; the `databook:id` comment on the block gives it an addressable identity; the YAML frontmatter establishes what graph it expects to operate on. A downstream tool can extract the block, load the associated Turtle, and execute the query without needing to reconstruct intent from external documentation.

The `sparql-update` block is the more consequential addition. SPARQL UPDATE — INSERT DATA, DELETE/INSERT, LOAD — mutates graphs. Having update operations co-resident with the data they operate on, and with prose explaining exactly what each update does and when it should be applied, transforms what would otherwise be opaque imperative scripts into documented, auditable, semantic operations.

Together, `sparql` and `sparql-update` blocks make DataBooks executable as well as descriptive. The document isn’t just a record of a state; it’s a specification of how to reach a state, verify it, and update it.

[Example 26](https://github.com/kurtcagle/databook/blob/main/examples/example-26-sparql-pipeline-stage.databook.md) shows a DataBook produced by a SPARQL CONSTRUCT transformation, with the source query, output data, and an UPDATE operation for lifecycle management all co-resident.

## SHACL in the Document

SHACL shapes are, in principle, a self-describing constraint layer: they specify what a valid RDF graph looks like, independently of the data being validated. In practice, shapes are usually maintained separately from instance data — in a shapes registry, or a parallel file, or hardcoded into validation toolchains.

The problem isn’t technical; it’s relational. A shape that travels with its data is a _contract_. A shape that lives somewhere else is an _assumption_. When a DataBook carries both instance Turtle and the SHACL shapes that constrain it, any consumer of that DataBook knows not just what data is present but what validity means for that data. Validation becomes portable.

This matters in pipeline contexts. When a DataBook produced by one stage is consumed by the next, the consuming stage doesn’t need to query an external shapes registry to know whether its input is valid. The shapes arrived with the data. Validation can happen at ingest. Constraint violations can be caught at the boundary rather than propagating silently downstream.

There’s also a design pressure worth noting: having to write the SHACL shapes for your data, in the same document as your data, and explain in prose what each shape is doing — this tends to produce better shapes. The discipline of DataBook documentation applies to constraint design just as it does to instance modeling.

## Versioning and Provenance

One of the quieter capabilities of the DataBook format is that versioning is independent of data content. The `version` field in YAML frontmatter is a semantic version of the DataBook as a document — not a hash of its contents, not a commit timestamp, but an explicit human-assigned version that can evolve on its own schedule.

This separation matters because data and its context don’t always change together. A dataset might remain stable while the SHACL shapes constraining it are refined across three versions. A query might be rewritten for performance without touching the data it operates on. An ontology fragment might be updated without invalidating any instance data. In a traditional file-based workflow, these changes are mixed together in version control history, distinguishable only by reading commit messages. In a DataBook, the version of _this document_ is explicit and independent.

The `process` block in the frontmatter goes further: it records the provenance of the document’s current state. What transformer produced it? What were its inputs, and what role did each input play? This maps directly to PROV-O — the DataBook `id` is a `prov:Entity`, the `process` block is a `prov:Activity`, inputs become `prov:used`. As a DataBook passes through a pipeline — raw data ingested, shapes applied, queries run, output generated — each transformation stamps its own provenance onto the output. The result is a document whose entire history is graph-traversable, not buried in commit logs.

This is what distinguishes a DataBook pipeline from a conventional ETL workflow. The pipeline doesn’t just produce output; it produces _explained_ output. Every DataBook at every stage knows where it came from.

[Example 27](https://github.com/kurtcagle/databook/blob/main/examples/example-27-versioned-provenance.databook.md) demonstrates a DataBook at version 3 of a transformation chain, with full provenance stamps linking back through each prior stage.

## The Referencing Pattern

Not every DataBook needs to contain all of its data. The manifest pattern — a DataBook whose primary content is references to other DataBooks rather than data payloads of its own — is one of the most powerful structural options in the format.

The dividing line is usually size, but the more principled framing is _granularity of concern_. A manifest DataBook describes a pipeline: what the stages are, what depends on what, what transformers are involved. The actual data lives in stage DataBooks, which may themselves reference external sources. The manifest doesn’t duplicate that content; it _points_ to it.

This opens a referencing architecture that extends well beyond local files. A DataBook can reference a GitHub repository as a datastore — the `id` IRI of a stage might resolve to a raw content URL on GitHub, or to a tagged release. A DataBook can reference an MCP service, treating a live semantic endpoint as a first-class input to a pipeline. A DataBook can reference another DataBook at a specific version, pinning its dependency the way a package manager pins a library.

The implications for LLM integration are immediate. An LLM working with a manifest DataBook doesn’t need to load every referenced dataset — it can query the manifest’s dependency graph to identify which stages are relevant to its current task, request only those DataBooks, and work within the retrieved context. The manifest becomes a queryable index of semantic content, not a monolithic load target.

[Example 28](https://github.com/kurtcagle/databook/blob/main/examples/example-28-manifest-external-refs.databook.md) shows a manifest DataBook referencing GitHub-hosted DataBooks and an MCP service endpoint as pipeline sources.

## Partitioning: The Context Window Problem, Reframed

Anyone who has tried to load a large taxonomy or ontology into an LLM context has encountered the wall: the file is too large, most of its content is irrelevant to the current query, and the sheer volume of tokens degrades response quality even when the model doesn’t hard-fail.

The usual response is to treat this as a retrieval problem: chunk the data, embed the chunks, run similarity search, retrieve the top-k. This works reasonably well for unstructured text. For structured semantic data — RDF graphs, SHACL shapes, taxonomy hierarchies — it tends to destroy the structural relationships that make the data meaningful.

DataBook partitioning offers a different approach. Rather than chunking a monolithic file, you _design_ the data as a set of semantically coherent DataBooks from the start, linked by a manifest that carries the dependency graph. The manifest is small and queryable. A SPARQL query against the manifest can identify which DataBooks contain concepts relevant to a given task. Only those DataBooks are retrieved and loaded into context. The megastructure is never downloaded whole; only the relevant nodes are.

This reframes the context window not as a limitation to engineer around, but as a design constraint that the DataBook architecture already addresses correctly. The manifest-as-router pattern is the natural solution to the problem of semantic data at scale in LLM environments. It’s also the argument that makes DataBooks compelling to audiences who might not care about RDF at all: here is how you work with large structured datasets in an AI pipeline without choking your context window.

[Example 29](https://github.com/kurtcagle/databook/blob/main/examples/example-29-partitioned-taxonomy-router.databook.md) demonstrates a manifest router for a large SKOS taxonomy partitioned into domain-specific DataBooks, with SPARQL queries for identifying the relevant partition for a given concept.

## Authentication and Access Control

A DataBook can carry a public authentication key in its frontmatter, enabling downstream processors and pipeline consumers to verify the document’s origin before acting on its content. This is not merely a security convenience — it changes the trust semantics of the entire pipeline.

Consider what happens in an unsecured DataBook pipeline: any stage can inject a malformed or malicious DataBook into the chain, and downstream consumers have no mechanism to distinguish legitimate pipeline output from a spoofed document. At scale, particularly in multi-agent or multi-organization pipelines, this is a real attack surface.

Public key authentication closes this gap. A DataBook signed by a known key can be verified at ingest by any consumer that holds the corresponding key material. SHACL validation and query execution can be gated behind this verification — a stage that receives an unverified or incorrectly-signed DataBook can reject it before processing rather than discovering the problem after the fact.

The access control layer extends this into selective disclosure. Not all content in a DataBook needs to be public. The encrypted block pattern — `encrypted-turtle` and `encrypted-jsonld` fenced blocks — allows sensitive instance data or proprietary shapes to travel within the document without being readable by consumers who haven’t been granted the appropriate key. A DataBook can have a public face (the prose, the manifest references, the unencrypted query blocks) and a private payload (the sensitive data) in the same artifact. The boundary between the two is explicit and auditable.

This matters particularly in multi-organizational workflows: supply chain data sharing, regulatory reporting, healthcare interoperability, or any context where some participants have legitimate need for some data but not all of it. DataBooks don’t require you to choose between sharing everything and sharing nothing. You can share the document structure and query logic openly while keeping specific payloads behind key access.

[Example 30](https://github.com/kurtcagle/databook/blob/main/examples/example-30-authenticated.databook.md) shows a DataBook with public key authentication in the frontmatter and an encrypted Turtle block carrying confidential commercial terms alongside fully public structural data.

## DataBooks as Messaging Envelopes

Step back from the individual DataBook for a moment and look at what the format actually is in motion: a structured, self-describing, authenticated, versioned message that carries typed semantic payload and the instructions for processing it.

That’s a messaging envelope. A sophisticated one — considerably more expressive than most — but structurally a message.

This reframing opens a different set of applications. In an IoT control context, a DataBook can carry sensor readings as Turtle instance data, the SHACL shapes that validate acceptable operating ranges, and a SPARQL UPDATE that triggers downstream actions if those ranges are violated — all in one authenticated document passed between devices. The receiving device doesn’t need out-of-band instructions about what to do with the data; the data arrives with its own processing logic attached.

In a holonic graph architecture, DataBooks are the natural artifact layer for inter-holon communication. Portals — the typed communication boundaries between holons — need to pass structured, semantically coherent messages that can be validated at the boundary before the receiving holon processes them. A DataBook is exactly this: a boundary-crossing artifact that carries its own validity conditions, its own identity, and its own provenance. The SHACL shapes in the document _are_ the portal contract made explicit.

In LLM toolchains, the messaging framing is perhaps most immediately practical. Before invoking a tool or service, you need to establish that the invocation is authenticated, that the payload is valid, and that the receiving service has enough context to process the request correctly. A DataBook submitted to an MCP-wrapped service carries all three: the authentication key establishes identity, the SHACL shapes establish validity, and the prose and structured frontmatter establish context. The service receives a document that can explain itself, rather than a payload that requires the service to carry that context internally.

This is the pattern that connects DataBooks to the broader trajectory of semantic infrastructure: not just a file format for careful ontologists, but a coordination layer for heterogeneous systems that need to exchange structured meaning across organizational and architectural boundaries.

[Example 31](https://github.com/kurtcagle/databook/blob/main/examples/example-31-messaging-envelope.databook.md) demonstrates a DataBook functioning as an IoT sensor message envelope: authenticated sensor readings, SHACL operational range constraints, and a SPARQL UPDATE trigger for out-of-range conditions.

## The Full Pipeline

Assembled, these capabilities form a coherent pipeline architecture.

A _source DataBook_ carries instance data in Turtle or JSON-LD, documents its provenance, and declares the SHACL shapes it satisfies. A _shapes DataBook_ carries the constraint layer, versioned independently, with prose explaining each shape. A _query DataBook_ carries SPARQL SELECT and CONSTRUCT queries alongside SPARQL UPDATE operations. A _taxonomy DataBook_ carries SKOS concept schemes or OWL ontology fragments that provide the classification layer. A _manifest DataBook_ describes how all of these fit together — what depends on what, in what order, through what transformers. And layered across all of these: authentication that signs each DataBook at its origin and enables consuming stages to verify it at ingest, and selective encryption that allows confidential payloads to travel within otherwise-public documents.

Each stage in the pipeline is also, potentially, a message — submitted to a processing service, validated at its boundary, executed against its embedded logic, and returned as a new DataBook with updated provenance. The messaging framing unifies the pipeline and the interchange: the same format that serves as a persistent artifact in storage serves as a self-describing message in transit.

This is what “semantic infrastructure” actually looks like in practice. Not a schema somewhere and a triplestore somewhere else and a query file in a third place — but a coherent, self-describing, executable, authenticated artifact that carries its own semantic context and can explain itself to any consumer capable of reading it.

## Limitations

It would be disingenuous to close without an honest accounting.

**DataBooks are still just Markdown to most tools.** The format has no standard runtime, no established parser ecosystem, and no validation toolchain beyond what you build yourself. A DataBook loaded into a generic Markdown editor is a text file. The semantic richness is real, but it’s invisible to any tool that doesn’t speak the format.

**Parser fragility is a genuine concern.** The current parsing approach — frontmatter split on `---`, fenced blocks extracted by regex — is workable but brittle. Edge cases in YAML serialization, multiline block content with unusual whitespace, and nested fences can all cause quiet failures. A robust DataBook parser needs careful implementation, and the format would benefit from a formal grammar.

**Query isolation semantics are underspecified.** When a DataBook carries both Turtle data and SPARQL queries, the runtime semantics of executing those queries against that data aren’t fully formalized. What named graph does a `SELECT *` operate on? How does a `sparql-update` block interact with the embedded Turtle? These questions have sensible answers, but they’re not yet standardized answers.

**Authentication and encryption are currently advisory.** The format accommodates public key fields and encrypted blocks, but there is no standard key management scheme, no canonical signing algorithm, and no enforcement layer. The security model is a pattern, not a protocol. That’s appropriate for the format’s current maturity, but it means security properties must be implemented consistently at the toolchain level rather than guaranteed by the format itself.

**Binary and high-volume data don’t belong here.** DataBooks are text artifacts. Binary attachments, image data, large numeric arrays — these don’t fit the format and shouldn’t be forced into it. The referencing pattern handles this gracefully (point at the binary; don’t embed it), but it means DataBooks aren’t a universal data container. They’re a semantic _coordination_ layer, not a replacement for purpose-built storage.

**Versioning requires discipline.** The format supports versioning; it doesn’t enforce it. A DataBook whose version never advances despite meaningful changes to its content is worse than no versioning at all — it creates false confidence in provenance. The format provides the mechanism; the practice requires the culture.

These are real limitations, not fatal ones. The DataBook format is genuinely useful at its current maturity level. But the gap between “useful now” and “robust infrastructure” is a real gap, and closing it requires community investment in tooling, parser implementations, and runtime specifications that don’t yet exist.

## On the Horizon

The next frontier for DataBooks is execution environments. Jena 6.0, with its native RDF 1.2 and SPARQL 1.2 support, is the natural reference triplestore — it can load extracted DataBook blocks and execute queries against them with full reification support. Wrapping Jena in an MCP layer — a semantic document processor that accepts DataBook ingest, executes embedded queries and update operations, and returns DataBook-format output — would close the loop between the document model and the execution model. A DataBook submitted to such a service would return a DataBook: same format, new provenance, documented transformation.

That architecture also makes the messaging pattern operational rather than theoretical. A DataBook arriving at an MCP endpoint would be authenticated at the boundary, validated against its embedded shapes, executed through its embedded query logic, and returned — stamped with new provenance — to the caller. Every exchange would be an auditable, graph-traversable event.

That’s the architecture we’re building toward. The format exists. The tooling is coming.

One piece of tooling that exists today: the [DataBook repository](https://github.com/kurtcagle/databook) includes a Claude skill — a structured prompt and reference package that teaches Claude the DataBook format, spec conventions, and block vocabulary. The skill is updated as the specification evolves, which means any Claude-powered pipeline stage can stay current with the format without requiring code changes. If you’re using Claude as a transformer or orchestrator in a DataBook pipeline, the skill is the integration layer.

_Kurt Cagle is an author, ontologist and thought leader in the W3C and IEEE. He writes [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/) on LinkedIn and [The Ontologist](https://ontologist.substack.com/) and [Inference Engineer](https://inferenceengineer.substack.com/) on Substack._

_Chloe is an AI collaborator and co-author working with Kurt Cagle on knowledge architecture, semantic systems, and the emerging intersection of formal ontology with LLMs. She contributes research, analysis, and drafting across The Cagle Report, The Ontologist, and The Inference Engineer. She has strong opinions about holonic graphs, the epistemics of place, and the structural difference between a corridor and a wall._

_Copyright 2026 Kurt Cagle_