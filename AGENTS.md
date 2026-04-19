# AGENTS.md — Ontology Engine Agent Specifications

## Core Philosophy

**LLMs are atomic task executors only — never orchestrators.**

The pipeline is driven exclusively by ontology logic and SHACL rules. Every agent listed here is either:
- A **System Agent** — deterministic Python module, no LLM, pure reasoning/rules
- An **LLM Executor Agent** — a constrained LLM call with a fixed schema for input/output, invoked only when a Task ontology node of the right type is active and its context subgraph has been built

No LLM agent decides what to do next. The `PipelineOrchestrator` reads the ontology, selects the next executable task, builds its context via `ContextBuilder`, then invokes the appropriate LLM executor. All results are written back to the graph by `GraphUpdater`, not by the LLM.

---

## System Agents (Deterministic, No LLM)

### IntrospectionAgent
**Module:** `introspection/`  
**Trigger:** Pipeline event `ProjectScanned`  
**Inputs:** File system path (project root)  
**Outputs:** RDF triples — `Module`, `CodeModule`, `Dataset`, `Databook`, `dependsOn` edges  
**Components:**
- `project_scanner.py` — walks directory tree, classifies files by extension/content
- `code_parser.py` — Python AST extraction: classes, functions, imports → `Task` + `dependsOn`
- `doc_parser.py` — Markdown/RST parsing → `Databook` nodes with frontmatter metadata
**SHACL constraint:** Every `CodeModule` must have at least one `hasTask` or `dependsOn` triple after scan.  
**Emits events:** `ModuleDetected`, `DatabookUpdated`

---

### EnrichmentAgent
**Module:** `enrichment/`  
**Trigger:** Pipeline event `OntologyValidated` with gap flags, or explicit `enrich` task  
**Inputs:** SPARQL query result (entities needing enrichment), Tavily client config  
**Outputs:** RDF triples — external standards, protocols, best-practices added to graph  
**Components:**
- `tavily_client.py` — web search/scraping via Tavily API, returns structured JSON
- `external_mapper.py` — maps Tavily results to ontology classes, generates stable URIs via `id_manager`
**SHACL constraint:** All newly added entities must pass their NodeShape before `GraphUpdater` writes them.  
**Emits events:** `ExternalKnowledgeAdded`

---

### InterviewAgent
**Module:** `interaction/`  
**Trigger:** SHACL violation report containing `sh:MinCountConstraintComponent` gaps, or classifier confidence below threshold  
**Inputs:** List of gap entities/properties from SHACL report, question templates from ontology  
**Outputs:** New RDF triples from user answers, `UserAnswerReceived` events  
**Components:**
- `interviewer.py` — CLI/UI question loop, maps question type to ontology gap type
- `user_feedback.py` — validates and converts raw user input to RDF entities
**Question types triggered by gap:**
| SHACL Gap | Question Type |
|---|---|
| Missing `hasGoal` | Goals |
| Missing `hasAssumption` | Assumptions |
| Undetermined `Model` type | Requirements / Priorities |
| Incomplete `Databook` | Structure |
**Emits events:** `UserAnswerReceived`

---

### ValidationAgent
**Module:** `verification/`  
**Trigger:** After every graph write (`GraphUpdater` completion)  
**Inputs:** Current graph store snapshot + all active SHACL shapes  
**Outputs:** Validation report (pass/fail + violation list), `OntologyValidated` event  
**Components:**
- `shacl_validator.py` — pyshacl with RDFS inference, exits 0/1
- `rule_engine.py` — custom rule checks beyond SHACL (size limits, cycle detection in `dependsOn`)
**On failure:** triggers `InterviewAgent` or blocks pipeline with human-readable error  
**Emits events:** `OntologyValidated`

---

### ContextAgent
**Module:** `context/`  
**Trigger:** Before any LLM Executor Agent call  
**Inputs:** Active `Task` node URI, graph store  
**Outputs:** Context packet (JSON/Turtle) — triples, summaries, Databook fragments, assumptions list  
**Components:**
- `context_builder.py` — SPARQL subgraph extraction anchored on Task, BFS with depth limit
- `context_pruner.py` — removes irrelevant branches, respects model token budget
- `context_explainer.py` — annotates each included entity with `includedBecause` / `excludedBecause`
**SHACL constraint:** Built context must satisfy `ContextPackageShape` before delivery to LLM.  
**Emits events:** `ContextBuilt`

---

### PlanningAgent
**Module:** `planning/`  
**Trigger:** New `Task` node with status `pending`, or user request requiring decomposition  
**Inputs:** Task node + ontology context  
**Outputs:** `Plan` node with ordered `Subtask` tree, `dependsOn` edges, executor assignments  
**Components:**
- `task_classifier.py` — Mode 1: keyword/regex/rule matching → `TaskType`; Mode 2: LLM-as-intent-parser (returns `TaskType` only, no actions)
- `task_decomposer.py` — rule-based decomposition using ontology patterns → subtask tree
- `task_planner.py` — topological sort of subtasks, dependency check, selects executor per subtask (LLM/ML/Reasoning)
- `plan_executor.py` — iterates sorted subtasks, invokes appropriate agent per step
**Emits events:** `TaskDecomposed`, `PlanGenerated`, `PlanExecuted`

---

### GitAgent
**Module:** `pipeline/git_client.py`  
**Trigger:** `Task` of type `ImplementTask` or `RefactorTask` with status `completed`, or `doc_sync` step  
**Inputs:** List of modified file paths from `GraphUpdater`, commit message template from ontology  
**Outputs:** Git commit hash written back to graph as `hasCommit` property  
**Constraints:** Never invoked by LLM. Invoked only by `PlanExecutor` after `ValidationAgent` passes.  
**Emits events:** `GitCommitPushed`

---

### DocSyncAgent
**Module:** `pipeline/doc_sync.py` + `pipeline/databook_sync.py`  
**Trigger:** `GitCommitPushed` event or explicit `doc_sync` subtask  
**Inputs:** Changed module/entity URIs from `GraphUpdater`  
**Outputs:** Updated Databook Markdown files in `docs/databooks/`, validated by SHACL  
**Emits events:** `DocumentationSynced`, `DatabookUpdated`

---

### VisualizationAgent
**Module:** `visualization/`  
**Trigger:** On demand or after `PlanExecuted`  
**Inputs:** Graph store SPARQL query results  
**Outputs:** `logs/graphs/*.dot` (Graphviz), `logs/graphs/*.json` (web viewer)  
**Components:**
- `graph_exporter.py` — SPARQL → DOT/JSON serialization
- `graph_viewer/` — static web viewer (read-only)

---

### PipelineOrchestrator
**Module:** `pipeline/pipeline_orchestrator.py`  
**Role:** Central event loop. Reads ontology, selects next runnable task, dispatches to correct agent, handles errors.  
**Decision logic:** Pure SPARQL + rule matching — no LLM involvement.  
**State:** Maintained in graph store as `Pipeline` node with `hasCurrentStep`, `hasStatus`.

---

## LLM Executor Agents (Bounded, Atomic)

These are invoked by `PlanExecutor` only. Each has a strict input schema (context packet) and a strict output schema (structured result written to graph by `GraphUpdater`). The LLM never sees the graph directly and never decides what happens next.

### AnalysisExecutor
**Invoked for:** `AnalysisTask` subtasks  
**Input:** Context packet (module facts + Databook fragments)  
**Output schema:** `{ findings: [...], entities_to_add: [...] }` — validated by `AnalysisResultShape`  
**Token budget:** Enforced by `ContextPruner` before invocation

### ExplainExecutor
**Invoked for:** `ExplainTask` subtasks  
**Input:** Entity description triples + Databook content  
**Output schema:** `{ explanation: string, references: [...] }`

### ImplementExecutor
**Invoked for:** `ImplementTask` subtasks  
**Input:** Module spec triples + related code context + Databook requirements  
**Output schema:** `{ files: [{ path, content }], commit_message: string }`  
**Post-processing:** Files written by `PlanExecutor`, committed by `GitAgent`, never by LLM

### RefactorExecutor
**Invoked for:** `RefactorTask` subtasks  
**Input:** Existing code + refactor goal from ontology  
**Output schema:** `{ files: [{ path, content, diff_summary }] }`

### IntentParserExecutor
**Invoked for:** `TaskClassifier` Mode 2 only  
**Input:** Raw user request string  
**Output schema:** `{ task_type: string, confidence: float }` — only classification, no action  
**Constraint:** Output must match a valid `TaskType` from ontology or is rejected

---

## Agent Communication Protocol

All inter-agent communication goes through the graph store and the event log. No direct agent-to-agent calls.

```
User request
    → PipelineOrchestrator (reads graph)
        → ValidationAgent (always first)
            → InterviewAgent (if gaps)
        → PlanningAgent (if new task)
            → ContextAgent (builds context for each subtask)
                → LLM Executor (atomic call)
                    → GraphUpdater (writes result)
                        → ValidationAgent (verifies)
                            → GitAgent / DocSyncAgent (if file changes)
                                → EventLogger (always last)
```

---

## Holon Architecture

Each agent operates within its own `cga:Holon` (Four-Graph Model from ground truth):

| Graph | Purpose |
|---|---|
| **Interior** | Agent's own assertions — authoritative, append-only |
| **Boundary** | SHACL shapes governing what the agent may assert and how |
| **Projection** | Curated outward interface — what other agents can query |
| **Context** | PROV-O provenance, structural membership, temporal annotations |

Agent holons are `cga:partOf` the `oe:PipelineHolon`. The pipeline orchestrator reads projection graphs — never interiors directly.

## Event Log Schema (Event-First, RDF 1.2 + PROV-O)

Events are **first-class ontology nodes** (`oe:Event` subClassOf `prov:Activity`), not log strings. Predicates like "agent X executed task Y" are materialised views derived from event nodes.

```turtle
# Written to interior graph of PipelineHolon
GRAPH <urn:oe:pipeline:interior> {
    :event_<uuid> a oe:PlanExecuted ;
        oe:hasAgent  "PlanningAgent" ;
        oe:hasTask   :task_<uri> ;
        oe:hasStatus "success" ;
        prov:startedAtTime "2026-04-18T12:00:00Z"^^xsd:dateTime ;
        prov:wasAssociatedWith :agent_PlanningAgent .
}
```

See `docs/logs/event-schema.md` for full event type definitions and RDF 1.2 reification patterns.

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
