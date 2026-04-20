---
created: '2024-04-20'
id: TODO
synced_at: '2026-04-20T17:22:21.049582+00:00'
title: TODO
type: plain-doc
version: '0.1'
---

---
created: '2024-04-20'
id: TODO
synced_at: '2026-04-20T17:20:05.135727+00:00'
title: TODO
type: plain-doc
version: '0.1'
---

# TODO: Enable Local Ollama Models & Generate README

## Steps from Approved Plan

- [x] 1. Edit .ontology.toml: Activate [llm] section with Ollama config to avoid Claude CLI fallback.
- [x] 2. litellm installed (pyproject.toml supports [litellm]; run `pip install -e .[litellm]` if issues).
- [ ] 3. Start Ollama: `ollama serve` (background) & `ollama pull qwen2.5-coder
