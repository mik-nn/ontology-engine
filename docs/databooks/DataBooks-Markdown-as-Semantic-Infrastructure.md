---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: DataBooks-Markdown-as-Semantic-Infrastructure
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:10:51.761091+00:00'
  title: Databooks  markdown as semantic infrastructure
  type: plain-doc
  version: '0.1'
---

## Encryption as a Designed-In Profile

Sensitive graph content — personal data, proprietary taxonomies, confidential business rules — needs to travel securely. DataBooks are designed to support encryption without requiring it in the core pattern.

The core specification reserves a small YAML key namespace for encryption metadata and defines what an encrypted block looks like structurally: an opaque fenced block with an encryption type annotation, which parsers that don’t support the encryption profile treat as inert rather than attempting to interpret.

````
encryption:
  profile: rsa-oaep-256-aes-gcm
  key_id: https://holongraph.com/keys/public/2026-04
  scope: selective  # 'full' | 'selective' | 'none'
  applies_to:#encrypted-block1

```base46-encoded {#encrypted-block1}
[base64-encoded ciphertext]
````

A parser that understands the encryption profile decrypts the block using the referenced key and treats the result as a normal typed fenced block. A parser that doesn’t understand the profile sees an opaque block with a declared type and skips it gracefully. The document remains parseable; the sensitive content remains protected.

The analogy is [XML Signature and XML Encryption](https://www.w3.org/TR/xmlenc-core1/) in relation to XML core — the base language doesn’t implement security, but it doesn’t make security impossible to add cleanly. The DataBook encryption profile follows the same principle: designed-in at the architecture level, deferred to implementation at the cryptographic level.

---

## What DataBooks Are Not

Intellectual honesty requires a clear scope boundary.

DataBooks are not a replacement for indexed triple stores. For large, frequently queried, persistent graph data — enterprise knowledge graphs, public Linked Data endpoints, production ontology services — a proper triple store with SPARQL endpoint remains the right tool. DataBooks serve the small-data niche that triple stores systematically over-engineer.

DataBooks are not a deterministic processing environment. The process stamp acknowledges non-determinism rather than eliminating it. Pipelines that require guaranteed reproducibility should use deterministic transformers (XSLT, SPARQL CONSTRUCT) for their critical stages and treat LLM stages as enrichment rather than ground truth.

DataBooks are not yet a standard. What is described here is a design pattern and a proposal, not a specification. The Markdown fragmentation problem is real — CommonMark, GitHub Flavored Markdown, Pandoc, and others diverge in ways that matter when you are relying on fence block interpretation. A DataBooks specification would need to pin down a specific Markdown dialect, define the required YAML keys, specify the type annotation vocabulary for fenced blocks, and establish a conformance profile. That work is ahead of us, not behind.

What DataBooks _are_ is a pattern worth adopting now, in anticipation of the specification work. The core elements — YAML frontmatter, typed fenced blocks, process stamps, IRI-based identity — are implementable today with existing tools. The value is available before the standard exists.

---

## The Holonic Connection

It is worth pausing to name something that may not be immediately obvious: DataBooks are not just a convenient format. They are the architectural instantiation of a principle that runs through everything we have been building.

Each DataBook is a [holon](https://en.wikipedia.org/wiki/Holon_\(philosophy\)) — a self-contained whole that is simultaneously a component of larger wholes. It has its own identity (IRI), its own boundary condition (the YAML frontmatter, which declares what it is and how it should be interpreted), its own internal coherence (the typed fenced blocks and prose that constitute its content), and its own provenance (the process stamp that records how it came to be).

A DataBook pipeline is a holarchy. Each stage is a holon; the manifest is the boundary condition that makes the stages a coherent system rather than an unrelated collection of files. The compiled output is a holon that contains, references, and depends on the holons that produced it.

This is not architectural coincidence. The holonic pattern — bounded coherence at every scale, explicit interfaces at every boundary, provenance that travels with the artifact — is the structural response to the problem we described in the companion piece to this article: the failure of centralized systems to accommodate local variation and temporal change. DataBooks apply that structural response at the level of knowledge artifacts.

A DataBook doesn’t ask “what does the central repository say this means?” It says “here is what I am, here is what I contain, here is how I was produced, here is how I relate to my neighbors.” The ground truth is local, explicit, and portable. The boundary condition travels with the artifact.

This is what semantic infrastructure looks like when it takes the holonic principle seriously.

---

## Where This Goes

DataBooks are a seed, not a finished edifice. The immediate invitation is to adoption: try the pattern, find its edges, extend it for your use cases, report back.

The medium-term work includes several threads worth tracking:

**A DataBooks community specification** that pins down a Markdown dialect, defines the required and optional YAML keys, establishes the type annotation vocabulary, and specifies conformance profiles for encryption, provenance, and manifest handling. This is natural territory for a W3C Community Group note or an IEEE working group contribution.

**Tooling**: a reference parser that validates DataBook structure, extracts typed fenced blocks, and resolves IRI references; a build tool that processes DataBook manifests and executes pipelines; integration with existing RDF toolchains (Apache Jena, RDFLib, Oxigraph).

**The LLM integration layer**: patterns for using DataBooks as the input/output format for LLM pipeline stages, with standard process stamp generation and provenance chain management. This is where the accountability layer for AI-assisted knowledge work becomes practically deployable.

**The archive format question**: DataBooks as the canonical archival format for AI-assisted ontology development, SHACL validation runs, taxonomy evolution, and other knowledge work that currently produces outputs with no formal provenance record.

We will be developing these threads in subsequent issues of The Ontologist and The Inference Engineer, and in the pages of _The End of the Universal Map_ — the Leanpub book in which the DataBooks architecture, the holonic graph model, and the broader argument about knowledge infrastructure are being assembled into a coherent whole.

The pieces exist. The synthesis is underway.


