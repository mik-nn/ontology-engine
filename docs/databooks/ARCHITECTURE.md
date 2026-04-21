---
databook:
  created: '2026-04-18'
  hierarchy: 3
  id: ARCHITECTURE
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:15.807789+00:00'
  title: Architecture
  type: plain-doc
  version: '0.1'
---

# Architecture

## Core Sections (Required)

### 1) Architectural Style

- Primary style: [layered/feature/event-driven/other]
- Why this classification: [short evidence-backed rationale]
- Primary constraints: [2-3 constraints that shape design]

### 2) System Flow

```text
[entry] -> [processing] -> [domain logic] -> [data/integration] -> [response/output]
```

Describe the flow in 4-6 steps using file-backed evidence.

### 3) Layer/Module Responsibilities

| Layer or module | Owns | Must not own | Evidence |
|-----------------|------|--------------|----------|
| [name] | [responsibility] | [non-responsibility] | [file] |

### 4) Reused Patterns

| Pattern | Where found | Why it exists |
|---------|-------------|---------------|
| [singleton/repository/adapter/etc] | [path] | [reason] |

### 5) Known Architectural Risks

- [Risk 1 + impact]
- [Risk 2 + impact]

### 6) Evidence

- [path/to/entrypoint]
- [path/to/main-layer-files]
- [path/to/data-or-integration-layer]

## Extended Sections (Optional)

Add only when needed:

- Startup or initialization order details
- Async/event topology diagrams
- Anti-pattern catalog with refactoring paths
- Failure-mode analysis and resilience posture












