---
created: '2024-04-20'
id: AGENTS
synced_at: '2026-04-20T17:22:21.241369+00:00'
title: AGENTS
type: plain-doc
version: '0.1'
---

---
created: '2024-04-20'
id: AGENTS
synced_at: '2026-04-20T17:20:07.200340+00:00'
title: AGENTS
type: plain-doc
version: '0.1'
---

# AGENTS.md — Ontology Engine Agent Specifications

## Core Philosophy

**LLMs are atomic task executors only — never orchestrators.**

The pipeline is driven exclusively by ontology logic and SHACL rules. Every agent listed here is either:
- A **System Agent** — deterministic Python module, no LLM, pure reasoning/rules
- An **LLM Executor Agent** — a constrained L
