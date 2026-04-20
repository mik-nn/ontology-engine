---
created: '2024-04-20'
id: inquiry-checkpoints
synced_at: '2026-04-20T17:22:20.823333+00:00'
title: inquiry-checkpoints
type: plain-doc
version: '0.1'
---

# Inquiry Checkpoints

Per-template investigation questions for Phase 2 of the acquire-codebase-knowledge workflow. For each template area, look for answers in the scan output first, then read source files to fill gaps.

---

## 1. STACK.md — Tech Stack

- What is the primary language and exact version? (check `.nvmrc`, `go.mod`, `pyproject.toml`, Docker `FROM` line)
- What package manager is used? (`npm`, `yarn`, `pnpm`, `go mod`, `pip`, `uv`)
- What are the core runtime frameworks? (web server
