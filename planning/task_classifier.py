"""Stage 7 — Task Classifier.

Mode 1 (no LLM): keyword/regex scoring across 14 task types.
Mode 2 (micro-model): TF-IDF + LogisticRegression trained on embedded corpus.
  Fully deterministic — no API calls, fits in < 5ms at import time.

Emits a TaskClassified RDF event so downstream pipeline stages can react
to the task type without re-reading Python state (event-driven routing).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from rdflib import Namespace, RDF

from storage.graph_store import GraphStore
from planning.task_type_registry import ALL_TYPES

OE    = Namespace("https://ontologist.ai/ns/oe/")
BUILD = Namespace("https://ontologist.ai/ns/build#")

# ──────────────────────────────────────────────────────────
# Scoring rules: (pattern, task_type, weight)
# Higher weight = stronger signal. GitTask listed first to prevent
# "push/deploy" from bleeding into AnalysisTask or ImplementTask.
# ──────────────────────────────────────────────────────────
_RULES: list[tuple[str, str, float]] = [
    # GitTask
    (r"\b(git (push|commit|add|stage|sync|pull|merge|tag))\b",                  "GitTask", 1.5),
    (r"\b(push|commit|deploy|publish|release|ship|upload to github)\b",         "GitTask", 1.2),
    (r"\b(to (github|remote|origin|main|master|repo|repository))\b",            "GitTask", 0.9),
    # DebugTask — before AnalysisTask (debug keywords would score AnalysisTask)
    (r"\b(debug|trace.*error|diagnose|root.?cause|stack.?trace|why.*fail)\b",    "DebugTask", 1.2),
    (r"\b(broken|crash(ed|ing)?|exception|bug|error.*in|failing test)\b",        "DebugTask", 0.9),
    # ValidateTask
    (r"\b(run tests?|run pytest|validate|check shacl|type.?check|run mypy)\b",  "ValidateTask", 1.2),
    (r"\b(lint|compliance|test suite|coverage report)\b",                        "ValidateTask", 0.8),
    # ReviewTask — before AnalysisTask to prevent "review" → "scan/audit"
    (r"\b(code.?review|pull.?request review|pr review|security audit)\b",       "ReviewTask", 1.3),
    (r"\b(review (the|this|for|code)|assess the|critique|feedback on)\b",        "ReviewTask", 1.0),
    (r"\b(security flaw|security issue|vulnerabilit)\b",                         "ReviewTask", 0.9),
    # SearchTask — high weight to beat "migration" appearing in search queries
    (r"\b(search (for|the|online)|look.?up|find (docs?|the api)|fetch.*api)\b", "SearchTask", 1.5),
    (r"\b(external docs?|pypi|crates\.io|npm package|api docs|openapi)\b",      "SearchTask", 0.9),
    # DocumentTask — before ImplementTask to capture "write docs/documentation"
    (r"\b(write (docs?|documentation)|update readme|create documentation|add docstring)\b", "DocumentTask", 1.4),
    (r"\b(readme|changelog|docstring|api docs|mkdocs|sphinx|databook)\b",       "DocumentTask", 0.8),
    # MigrateTask — require migrate/upgrade as verb, not as noun in "migration docs"
    (r"\b(migrat(e|ing)|upgrade (to|from)|port (to|from)|convert from|deprecat)\b", "MigrateTask", 1.2),
    (r"\b(migration (plan|guide|path|strategy|steps?)|breaking.?change|api version)\b", "MigrateTask", 1.0),
    (r"\b(legacy|schema change|v\d+ (to|migration))\b",                         "MigrateTask", 0.7),
    # IntegrateTask
    (r"\b(integrat(e|ion)|wire.?up|connect.+with|bridge|hook.?up)\b",           "IntegrateTask", 1.2),
    (r"\b(adapter|connector|glue code|interface between)\b",                     "IntegrateTask", 0.8),
    # ComplexTask
    (r"\b(complex|end.?to.?end|full pipeline|multi.?stage|comprehensive)\b",    "ComplexTask", 1.0),
    # ExplainTask
    (r"\b(explain|describe|what is|how does|why|clarify|show me|tell me)\b",    "ExplainTask", 1.0),
    (r"\b(understand|overview|summary|summarize)\b",                             "ExplainTask", 0.7),
    # ImplementTask
    (r"\b(implement|create|build|write|add|generate|make|develop|code)\b",      "ImplementTask", 1.0),
    (r"\b(new (module|class|function|method|feature|endpoint))\b",              "ImplementTask", 0.9),
    # RefactorTask
    (r"\b(refactor|improve|optimize|clean|restructure|rename|move|extract)\b",  "RefactorTask", 1.0),
    (r"\b(simplify|reduce|decouple|split|merge|consolidate)\b",                 "RefactorTask", 0.8),
    # AnalysisTask
    (r"\b(analy[sz]e|investigate|inspect|audit|check|scan)\b",                  "AnalysisTask", 1.0),
    (r"\b(find|detect|discover|list|show|report|count)\b",                      "AnalysisTask", 0.6),
    # DesignTask
    (r"\b(design|architect|plan|structure|model|schema|blueprint)\b",           "DesignTask", 1.0),
    (r"\b(decide|choose|select|evaluate|compare|trade.?off)\b",                 "DesignTask", 0.7),
]

_TASK_TYPES: set[str] = set(ALL_TYPES)
_CONFIDENCE_THRESHOLD = 0.45   # below this → micro-model (Mode 2)

# ──────────────────────────────────────────────────────────
# Micro-model training corpus (TF-IDF + LogisticRegression)
# No LLM — fits in < 5ms at import time.
# ──────────────────────────────────────────────────────────
_TRAIN: list[tuple[str, str]] = [
    # ImplementTask
    ("implement the login module", "ImplementTask"),
    ("create a new API endpoint", "ImplementTask"),
    ("build a caching layer", "ImplementTask"),
    ("write tests for the auth module", "ImplementTask"),
    ("add error handling to the pipeline", "ImplementTask"),
    ("generate a new SHACL shape", "ImplementTask"),
    ("develop the dashboard view", "ImplementTask"),
    ("make a new decorator", "ImplementTask"),
    ("code the ingestion pipeline", "ImplementTask"),
    ("produce a graph exporter", "ImplementTask"),
    ("set up the verification engine", "ImplementTask"),
    ("bootstrap the new adapter", "ImplementTask"),
    # ExplainTask
    ("explain how the ontology works", "ExplainTask"),
    ("what is the purpose of GraphStore", "ExplainTask"),
    ("describe the pipeline stages", "ExplainTask"),
    ("how does SHACL validation work", "ExplainTask"),
    ("summarize the verification module", "ExplainTask"),
    ("tell me about the adapter factory", "ExplainTask"),
    ("why does the planner decompose tasks", "ExplainTask"),
    ("show me how introspection works", "ExplainTask"),
    ("clarify the difference between holons and modules", "ExplainTask"),
    ("what happens during the interview stage", "ExplainTask"),
    # RefactorTask
    ("refactor the adapter to use composition", "RefactorTask"),
    ("optimize the SPARQL query for speed", "RefactorTask"),
    ("rename all snake_case methods to camelCase", "RefactorTask"),
    ("simplify the context builder logic", "RefactorTask"),
    ("clean up the duplicate code in parsers", "RefactorTask"),
    ("restructure the module hierarchy", "RefactorTask"),
    ("decouple the planner from the executor", "RefactorTask"),
    ("extract the token counter into a helper", "RefactorTask"),
    ("move the config loader to a separate module", "RefactorTask"),
    # AnalysisTask
    ("analyze code coverage gaps in tests", "AnalysisTask"),
    ("investigate why the pipeline fails", "AnalysisTask"),
    ("audit the dependency graph for cycles", "AnalysisTask"),
    ("find unused modules in the project", "AnalysisTask"),
    ("check which adapters are missing", "AnalysisTask"),
    ("review the SHACL violations report", "AnalysisTask"),
    ("scan for missing docstrings", "AnalysisTask"),
    ("detect duplicate entity URIs", "AnalysisTask"),
    ("list all open AI-todos", "AnalysisTask"),
    ("trace why the interview skips gaps", "AnalysisTask"),
    # DesignTask
    ("design the new authentication flow", "DesignTask"),
    ("architect the plugin system for adapters", "DesignTask"),
    ("plan the migration to Dataset from ConjunctiveGraph", "DesignTask"),
    ("model the new event schema", "DesignTask"),
    ("create a blueprint for the metrics dashboard", "DesignTask"),
    ("decide between SPARQL and property paths", "DesignTask"),
    ("evaluate tradeoffs of streaming vs batch", "DesignTask"),
    # GitTask
    ("commit all changed files", "GitTask"),
    ("push to github", "GitTask"),
    ("deploy the new version to main", "GitTask"),
    ("publish the release", "GitTask"),
    ("git commit and push", "GitTask"),
    ("stage the modified adapters", "GitTask"),
    ("sync to remote origin", "GitTask"),
    # DebugTask
    ("debug why the pipeline fails on verify stage", "DebugTask"),
    ("trace the root cause of the SHACL error", "DebugTask"),
    ("diagnose why tests are crashing", "DebugTask"),
    ("investigate the broken import in adapter", "DebugTask"),
    ("why is the context builder returning empty results", "DebugTask"),
    ("find out why execution is failing", "DebugTask"),
    ("stack trace from the plan executor", "DebugTask"),
    # SearchTask
    ("search for the rdflib Dataset migration guide", "SearchTask"),
    ("look up the ollama REST API docs", "SearchTask"),
    ("find documentation for deepseek-r1 parameters", "SearchTask"),
    ("fetch the pyshacl changelog", "SearchTask"),
    ("what are the litellm ollama options", "SearchTask"),
    # DocumentTask
    ("write documentation for the context builder", "DocumentTask"),
    ("update README with new CLI commands", "DocumentTask"),
    ("add docstrings to all public methods in rule_engine", "DocumentTask"),
    ("create a databook for the metrics module", "DocumentTask"),
    ("document the adapter factory interface", "DocumentTask"),
    # ValidateTask
    ("run the full test suite", "ValidateTask"),
    ("check SHACL conformance on the current graph", "ValidateTask"),
    ("run pytest and report failures", "ValidateTask"),
    ("validate the ontology against all shapes", "ValidateTask"),
    ("run mypy type checking", "ValidateTask"),
    # MigrateTask
    ("migrate from ConjunctiveGraph to Dataset", "MigrateTask"),
    ("upgrade the anthropic SDK to the latest version", "MigrateTask"),
    ("port the old adapter API to the new interface", "MigrateTask"),
    ("convert legacy config format to TOML", "MigrateTask"),
    ("update rdflib from 6 to 7 API changes", "MigrateTask"),
    # ReviewTask
    ("review the plan_executor code for issues", "ReviewTask"),
    ("do a code review of the new adapter", "ReviewTask"),
    ("audit the authentication module for security flaws", "ReviewTask"),
    ("review the PR changes in context_builder", "ReviewTask"),
    ("assess quality of the test coverage", "ReviewTask"),
    # IntegrateTask
    ("integrate the ollama adapter with the factory", "IntegrateTask"),
    ("wire up the web search tool to the pipeline", "IntegrateTask"),
    ("connect the metrics module to the orchestrator", "IntegrateTask"),
    ("bridge the old config system with the new TOML loader", "IntegrateTask"),
    ("hook up the graph exporter to the CLI", "IntegrateTask"),
    # ComplexTask
    ("end-to-end implementation of the full enrichment pipeline", "ComplexTask"),
    ("comprehensive redesign of the context building strategy", "ComplexTask"),
    ("multi-stage migration and integration of new storage backend", "ComplexTask"),
    ("full pipeline: introspect, enrich, validate, deploy", "ComplexTask"),
]

_micro_model = None  # lazy-loaded singleton


def _get_micro_model():
    global _micro_model
    if _micro_model is not None:
        return _micro_model
    try:
        from sklearn.pipeline import Pipeline
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression

        texts  = [t for t, _ in _TRAIN]
        labels = [l for _, l in _TRAIN]

        model = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf",   LogisticRegression(max_iter=500, C=2.0)),
        ])
        model.fit(texts, labels)
        _micro_model = model
    except ImportError:
        _micro_model = None  # sklearn unavailable — stay with keyword fallback
    return _micro_model


@dataclass
class ClassificationResult:
    task_type: str              # one of _TASK_TYPES
    confidence: float           # 0.0–1.0
    matched_entities: list[str] = field(default_factory=list)  # URIs
    mode_used: str              = "keyword"
    raw_request: str            = ""
    scores: dict[str, float]    = field(default_factory=dict)


class TaskClassifier:
    """Classifies a free-text user request into an oe:TaskType."""

    def __init__(self, store: GraphStore, use_llm_fallback: bool = False):
        self.store = store
        self.use_llm_fallback = use_llm_fallback
        self._module_index = self._build_module_index()

    def classify(self, request: str) -> ClassificationResult:
        result = self._mode1(request)

        if result.confidence < _CONFIDENCE_THRESHOLD and self.use_llm_fallback:
            result = self._mode2(request, result)

        result.matched_entities = self._match_entities(request)
        self._emit_event(result)
        return result

    def _emit_event(self, result: ClassificationResult) -> None:
        """Write TaskClassified event — enables event-driven downstream routing."""
        from datetime import datetime, timezone
        from storage.id_manager import uri as make_uri, graph_uri
        from rdflib import Literal, URIRef

        PIPE = URIRef("https://ontologist.ai/ns/oe/pipeline/interior")
        ev   = make_uri("event", f"task-classified-{result.task_type[:4].lower()}-"
                        f"{abs(hash(result.raw_request)) % 0xFFFF:04x}")

        self.store.add(ev, RDF.type,          OE.TaskClassified,              PIPE)
        self.store.add(ev, OE.hasAgent,       Literal("TaskClassifier"),       PIPE)
        self.store.add(ev, OE.taskType,       Literal(result.task_type),       PIPE)
        self.store.add(ev, OE.confidence,     Literal(f"{result.confidence:.3f}"), PIPE)
        self.store.add(ev, OE.classifierMode, Literal(result.mode_used),       PIPE)
        self.store.add(ev, OE.rawRequest,     Literal(result.raw_request[:200]), PIPE)
        self.store.add(ev, OE.hasStatus,      Literal("completed"),            PIPE)
        self.store.add(ev, OE.matchedEntities,
                       Literal(str(len(result.matched_entities))),             PIPE)
        now = datetime.now(timezone.utc).isoformat()
        from rdflib import XSD
        self.store.add(ev, OE.classifiedAt,
                       Literal(now, datatype=XSD.dateTime),                   PIPE)

    # ──────────────────────────────────────────────
    # Mode 1: keyword scoring
    # ──────────────────────────────────────────────

    def _mode1(self, request: str) -> ClassificationResult:
        text = request.lower()
        scores: dict[str, float] = {t: 0.0 for t in _TASK_TYPES}

        for pattern, task_type, weight in _RULES:
            if re.search(pattern, text, re.IGNORECASE):
                scores[task_type] += weight

        total = sum(scores.values()) or 1.0
        best_type = max(scores, key=lambda t: scores[t])
        best_score = scores[best_type]
        confidence = round(best_score / total, 3) if best_score > 0 else 0.0

        return ClassificationResult(
            task_type=best_type,
            confidence=confidence,
            mode_used="keyword",
            raw_request=request,
            scores={t: round(s, 3) for t, s in scores.items()},
        )

    # ──────────────────────────────────────────────
    # Mode 2: TF-IDF + LogisticRegression micro-model
    # Trained on embedded corpus at import time (~3ms).
    # No LLM, no API calls — fully deterministic.
    # ──────────────────────────────────────────────

    def _mode2(self, request: str, fallback: ClassificationResult) -> ClassificationResult:
        """Classify with sklearn micro-model when keyword score is below threshold."""
        model = _get_micro_model()
        if model is None:
            return ClassificationResult(
                task_type=fallback.task_type,
                confidence=max(fallback.confidence, 0.5),
                mode_used="keyword_fallback",
                raw_request=request,
                scores=fallback.scores,
            )

        proba = model.predict_proba([request])[0]
        classes = model.classes_
        best_idx = proba.argmax()
        task_type = classes[best_idx]
        confidence = round(float(proba[best_idx]), 3)

        if task_type not in _TASK_TYPES:
            task_type = fallback.task_type
            confidence = max(fallback.confidence, 0.5)

        return ClassificationResult(
            task_type=task_type,
            confidence=confidence,
            mode_used="micro_model",
            raw_request=request,
            scores=fallback.scores,
        )

    # ──────────────────────────────────────────────
    # Entity matching: find module/function URIs mentioned in request
    # ──────────────────────────────────────────────

    def _match_entities(self, request: str) -> list[str]:
        text = request.lower()
        matched = []
        for local_name, uri in self._module_index.items():
            # match slug form (dashes/underscores interchangeable)
            slug = local_name.replace("-", "_").replace(".", "_")
            if slug in text or local_name.replace("-", " ") in text:
                matched.append(uri)
        return matched

    def _build_module_index(self) -> dict[str, str]:
        """Build {local_name → full_uri} for all CodeModules and CodeFunctions."""
        index: dict[str, str] = {}
        for ctx in self.store._g.contexts():
            for s in ctx.subjects(RDF.type, OE.CodeModule):
                local = str(s).split("/")[-1]
                index[local] = str(s)
            for s in ctx.subjects(RDF.type, OE.CodeFunction):
                fn_name = self.store._g.value(s, OE.functionName)
                if fn_name:
                    index[str(fn_name)] = str(s)
        return index
