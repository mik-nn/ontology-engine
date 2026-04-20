---
created: '2024-04-20'
id: stack-detection
synced_at: '2026-04-20T17:22:18.544409+00:00'
title: stack-detection
type: plain-doc
version: '0.1'
---

# Stack Detection Reference

Load this file when the tech stack is ambiguous — e.g., multiple manifest files present, unfamiliar file extensions, or no obvious `package.json` / `go.mod`.

---

## Manifest File → Ecosystem

| File | Ecosystem | Key fields to read |
|------|-----------|--------------------|
| `package.json` | Node.js / JavaScript / TypeScript | `dependencies`, `devDependencies`, `scripts`, `main`, `type`, `engines` |
| `go.mod` | Go | Module path, Go version, `require` block |
| `
