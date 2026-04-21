---
databook:
  created: '2026-04-21'
  depends_on:
  - https://ontologist.ai/ns/oe/module/docs-databooks-architecture-md
  hierarchy: 1
  id: AGENTS
  layer: architecture
  process:
    transformer: human
  scope: permanent
  synced_at: '2026-04-21T14:10:51.404337+00:00'
  title: Agents
  type: plain-doc
  version: '0.1'
---

## Skills Required (API Layer)

| Skill ID | Module | Description |
|---|---|---|
| `ontology.query` | `api/skills/` | SPARQL SELECT/CONSTRUCT against graph store |
| `ontology.extend` | `api/skills/` | Add validated triples to graph (checks SHACL first) |
| `ontology.validate` | `api/skills/` | Run full SHACL pass, return report |
| `context.build` | `api/skills/` | Build context packet for a given Task URI |
| `context.explain` | `api/skills/` | Return include/exclude reasoning for context |
| `interview.ask` | `api/skills/` | Trigger interview for a specific SHACL gap |
| `model.select` | `api/skills/` | Select executor type (LLM/ML/Reasoning) for a Task |
| `llm.invoke` | `api/skills/` | Call LLM executor with context packet, return validated result |
| `git.commit` | `api/skills/` | Stage + commit specified paths with message |
| `doc.sync` | `api/skills/` | Regenerate Databook for changed entities |
| `pipeline.run` | `api/skills/` | Start/resume pipeline from current graph state |
| `pipeline.status` | `api/skills/` | Query current pipeline step and pending tasks |











