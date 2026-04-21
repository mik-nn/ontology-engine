---
databook:
  created: '2026-04-21'
  hierarchy: 1
  id: project-inventory
  layer: documentation
  scope: project
  title: Ontology Engine - Project Inventory
  type: plain-doc
  version: '1.0'
---

# Ontology Engine Project Inventory

## Directory Structure
```
ontology-engine/ (cwd)
├── .gitignore
├── .ontology.toml (LLM config)
├── AGENTS.md
├── pyproject.toml | requirements.txt | pytest.ini
├── README.md.back
├── TODO*.md
├── api/ (skills/tools/md_to_rdf.py)
├── build/ (wheel egg-info)
├── cli/ (__init__.py config main repl commands/*: ai_todo init introspect run status tools verify visualize)
├── context/ (__init__.py builder explainer
