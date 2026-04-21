---
title: "Lions and Tigers and Bears, Oh My!"
source: "https://ontologist.substack.com/p/lions-and-tigers-and-bears-oh-my?utm_source=profile&utm_medium=reader2"
date: "Feb 26"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!oDoM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F634e47fb-7abd-4b7a-877f-d102fbdfeaa7_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!oDoM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F634e47fb-7abd-4b7a-877f-d102fbdfeaa7_2688x1536.jpeg)

I’ve been working with a number of LLMs - Claude Opus and Sonata, Deepseek, Google’s Gemini CLI, etc., in the process of exploring RDF around SHACL and SPARQL. Over that period, I’ve found that there are approaches that work for the ontologist, and aproaches that you should generally avoid.

If you’ve tried using ChatGPT or Claude to generate SHACL shapes or SPARQL queries, you’ve probably noticed something frustrating: ask it twice for “the same thing” and you get two different results. Different formatting. Different namespace conventions. Different assumptions about what properties to include. It’s enough to make you wonder if LLMs are even useful for RDF work.

They are — but only if you stop trying to use them like deterministic code generators.

After several months of integrating LLMs into my semantic web toolkit development, I’ve landed on a pattern that actually works: **treat LLM output as disposable scaffolding, not canonical artifacts**. Generate once, refine by hand, commit your version, and never regenerate.

Here’s why this matters and how to make it work.

## The Round-Trip Illusion

The promise is seductive: describe your domain in natural language, get working RDF back, iterate by asking for modifications. Like having a junior ontologist on call 24/7.

The reality is messier. Let’s say you prompt Claude with:

```
Generate a SHACL shape for a Person with name and email
```

You might get:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:PersonShape 
    a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:name "Person Shape" ;
    sh:description "Validates Person instances" ;
    sh:property [
        sh:path ex:name ;
        sh:name "name" ;
        sh:description "Person's full name" ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "Person must have exactly one name"
    ] ;
    sh:property [
        sh:path ex:email ;
        sh:name "email" ;
        sh:datatype xsd:string ;
        sh:pattern "^[^@]+@[^@]+$" ;
        sh:minCount 1 ;
        sh:message "Person must have a valid email address"
    ] .
```

That’s... a lot. You wanted a minimal shape. You got comprehensive documentation, defensive cardinality constraints, and a regex that wouldn’t pass production review.

Fine, you think. I’ll refine it. So you prompt:

```
Make it more minimal - remove the documentation
```

Now you get:

```
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix : <http://example.com/> .

:PersonShape 
    a sh:NodeShape ;
    sh:targetClass :Person ;
    sh:property [
        sh:path :name ;
        sh:minCount 1
    ] , [
        sh:path :email ;
        sh:pattern "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    ] .
```

Wait — now the namespace changed (`ex:` became `:`), the formatting is different (comma-separated property list), and it added a better email regex but lost `sh:datatype` declarations. This isn’t an “improved version” of the first output. It’s a completely different artifact.

Welcome to the contamination problem.

## Why LLMs Can’t Preserve RDF

StructureLLMs are trained on vast amounts of RDF code from tutorials, documentation, Stack Overflow, and published examples. Every source has different conventions:

-   Some use verbose property shapes with `sh:name` and `sh:description`
    
-   Others prefer terse blank node lists
    
-   Some always declare `rdf:` and `rdfs:` prefixes “just in case”
    
-   Others use only what’s strictly necessary
    
-   Tutorial code tends toward defensive over-specification
    
-   Production code leans minimal
    

When you ask an LLM to generate SHACL, it’s not retrieving a template from memory. It’s predicting token sequences based on statistical patterns across all that training data. The result is a blend — usually leaning toward “helpful” (verbose, documented, defensive) rather than “minimal” (terse, production-ready, trust-the-user).

Even with temperature set to 0, you’ll get variation because:

-   Context window effects change token probabilities
    
-   Your phrasing (”make it minimal” vs. “remove documentation”) triggers different patterns
    
-   Model updates alter behavior between sessions
    
-   Semantic equivalence doesn’t guarantee syntactic identity
    

The harsh truth: **you cannot get deterministic RDF output from non-deterministic language models**.

## The Single-Pass Pattern

Once you accept that LLMs won’t give you repeatable results, a simpler pattern emerges:

**Use LLMs to generate scaffolding once, then take over manually.**

Here’s the workflow:

### 1\. Generation (AI does the grunt work)

Prompt for minimal output with explicit constraints:

```
Generate minimal SHACL shapes for an e-commerce domain:

Entities: Customer, Order, Product
- Customer: email (required), name (required)
- Order: orderDate (required), total (required, positive)
- Product: sku (required), price (positive)

No sh:message, sh:description, or sh:name properties.
Use sh:targetClass for each entity.
```

The AI generates 70-80% correct structure in 30 seconds. Good enough to start.

### 2\. Normalization (You apply your style)

Strip the contamination:

-   Remove documentation properties you didn’t ask for
    
-   Fix namespace inconsistencies
    
-   Canonicalize formatting to your project standards
    
-   Remove inferred properties (AI loves to add `rdf:type` assertions)
    
-   Validate the regex patterns (they’re often simplistic)
    

This takes 5-10 minutes but gives you full control.

### 3\. Validation (Test, don’t trust)

LLMs generate plausible but often insufficient constraints. Test rigorously:

```
def validate_shapes(shapes_graph, test_cases):
    """Don't trust AI logic - test it"""
    
    # Test positive cases (should validate)
    for valid_data in test_cases['valid']:
        result = validate(shapes_graph, valid_data)
        assert result.conforms, f"False negative: {valid_data}"
    
    # Test negative cases (should fail)
    for invalid_data in test_cases['invalid']:
        result = validate(shapes_graph, invalid_data)
        assert not result.conforms, f"False positive: {invalid_data}"
```

I’ve found AI-generated shapes fail ~20% of semantic tests despite being syntactically perfect.

### 4\. Commitment (Version control your work, not the AI’s)

Save the normalized, validated version as your canonical artifact:

```
# shapes/person.ttl
# LLM-assisted generation, hand-refined
# Maintain manually - do not regenerate

@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:PersonShape 
    a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:property [
        sh:path ex:name ;
        sh:datatype xsd:string ;
        sh:minCount 1
    ] ;
    sh:property [
        sh:path ex:email ;
        sh:datatype xsd:string ;
        sh:pattern "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$" ;
        sh:minCount 1
    ] .
```

**This is now your source of truth.** Future modifications are manual edits, not regenerations.

## When to Use This Pattern

The single-pass approach shines for:

**✅ Bootstrapping new domains**

-   20+ classes to model? AI scaffolding saves hours
    
-   Get 70% structure in minutes, refine the 30% yourself
    
-   Batch generation keeps internal consistency
    

**✅ Complex SPARQL queries**

-   Draft the logic with AI, optimize by hand
    
-   Especially useful for queries with 5+ joins
    
-   AI handles boilerplate, you handle performance
    

**✅ Converting legacy schemas**

-   AI excels at pattern recognition across many entities
    
-   Database schema → OWL conversion
    
-   XML Schema → SHACL translation
    

**✅ Documentation and explanations**

-   AI is genuinely good at prose
    
-   Generate property descriptions, then edit
    
-   Create usage examples, then validate
    

## When to Skip the AI

**❌ Adding 1-2 properties to existing shapes**

-   Hand-editing is faster than prompting + normalization
    
-   No risk of AI restructuring your existing work
    

**❌ Production query optimization**

-   AI might completely restructure your query
    
-   Better: specific asks like “add index hint for property X”
    

**❌ Maintaining existing RDF artifacts**

-   Never feed existing RDF back to an LLM for “improvements”
    
-   The contamination problem makes merges painful
    

**❌ Simple validation rules**

-   Template-based generation is faster for single constraints
    
-   Your own snippet library beats prompting time
    

## Tooling the Pattern

For my consulting work, I’ve wrapped this into a reusable Python class:

```
class LLMAssistedGenerator:
    """Single-pass RDF generation with normalization"""
    
    def generate_draft(self, prompt: str) -> str:
        """Step 1: Get AI scaffolding"""
        return self.llm.complete(prompt)
    
    def normalize(self, draft: str) -> rdflib.Graph:
        """Step 2: Apply project style"""
        g = self.parse_turtle(draft)
        g = self.remove_documentation_props(g)
        g = self.canonicalize_namespaces(g)
        return self.serialize_minimal(g)
    
    def validate(self, graph: rdflib.Graph, 
                 test_cases: list) -> ValidationReport:
        """Step 3: Semantic validation"""
        syntax_ok = self.validate_syntax(graph)
        logic_ok = self.validate_constraints(graph, test_cases)
        return ValidationReport(syntax_ok and logic_ok)
    
    def commit(self, graph: rdflib.Graph, path: str):
        """Step 4: Save canonical version"""
        with open(path, 'w') as f:
            f.write("# LLM-assisted, hand-validated\n")
            f.write("# Maintain manually\n\n")
            f.write(graph.serialize(format='turtle'))
```

The key insight: **keep AI in the generation role, not the maintenance role.**

## Measuring the Return

Track these metrics to understand your efficiency gains:

-   **Generation time**: ~30 seconds (AI draft)
    
-   **Normalization time**: ~5 minutes (cleanup)
    
-   **Validation time**: ~10 minutes (testing)
    
-   **Total**: ~15 minutes
    

Compare to hand-coding from scratch (~45 minutes for equivalent complexity):

-   **Time saved**: ~30 minutes (66%)
    
-   **Quality overhead**: validation time is essential regardless
    

The contamination rate matters too:

-   Lines generated by AI: 150
    
-   Lines after normalization: 75
    
-   **Contamination**: 50% bloat
    

Understanding this helps you write better prompts. “Generate minimal shapes” gets you closer to the 75 lines you actually want.

## The Meta-Lesson

LLMs are best understood as **probabilistic scaffolding generators**, not deterministic code tools. They excel at:

-   Recognizing structural patterns across domains
    
-   Generating boilerplate you’d write anyway
    
-   Drafting logic you’ll refine
    
-   Creating documentation you’ll edit
    

They fail at:

-   Preserving exact formatting across generations
    
-   Maintaining consistency with existing artifacts
    
-   Understanding your project’s implicit conventions
    
-   Producing production-ready validation logic without testing
    

The single-pass pattern respects these boundaries. Generate once, take ownership, maintain manually. It’s faster than coding from scratch but more controlled than hoping for reproducible AI output.

## Practical Takeaways

1.  **Prompt for minimalism** - “No sh:message or sh:description” reduces cleanup by ~40%
    
2.  **Batch related entities** - Generate 5 shapes at once for internal consistency
    
3.  **Test semantic correctness** - AI syntax is usually fine, logic is often wrong
    
4.  **Never regenerate** - Edit your canonical version, don’t ask AI to modify it
    
5.  **Document the process** - Note “LLM-assisted, hand-refined” for future maintainers
    

The semantic web community is just beginning to figure out productive AI integration. The round-trip illusion is tempting but ultimately frustrating. Single-pass scaffolding is less magical but actually works.

_Note: Some of this was developed in conjunction with Claude’s Sonnet 4.6 AI engine._

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!u3pI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5688f056-92cf-45bc-aba2-19ecc4130c6e_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!u3pI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5688f056-92cf-45bc-aba2-19ecc4130c6e_2688x1536.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

If you like these articles, please consider becoming a paid subscriber. It helps support me so that I can continue writing code, in-depth analyses, educational pieces, and more.

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.