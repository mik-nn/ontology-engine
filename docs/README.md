# docs/

## Structure

```
docs/
├── databooks/      SHACL-validated Markdown design documents (frontmatter required)
├── adr/            Architecture Decision Records — immutable, numbered, append-only
├── agents/         Per-agent specifications (mirrors AGENTS.md at module level)
├── ontology/       Ontology class/property reference, namespace docs
├── guides/         How-to guides for using the engine
├── api/            API skill/tool reference
└── logs/           Log format specs (actual log files are in /logs/)
```

## Databooks

Every file in `docs/databooks/` must have YAML frontmatter validated by `core/shacl/databook_shapes.ttl`.
Required fields: `id`, `title`, `version`, `type`, `content` (body counts as content).

New databooks are created by `DocSyncAgent` after ontology changes, or manually then validated via:

```bash
python pipeline/generate_databook.py docs/databooks/YourFile.md
```

## ADRs

Format: `docs/adr/NNN-title.md`. Once merged, ADRs are never edited — supersede with a new one.
