"""Stage 7 — Task Classifier.

Mode 1 (no LLM): keyword/regex scoring against known task types.
Mode 2 (LLM intent parser): structured JSON output, validated by SHACL.
  Only the classification is delegated to LLM — no actions, no orchestration.

Returns ClassificationResult with task_type, confidence, matched_entities, mode_used.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from rdflib import Namespace, RDF

from storage.graph_store import GraphStore

OE    = Namespace("https://ontologist.ai/ns/oe/")
BUILD = Namespace("https://ontologist.ai/ns/build#")

# ──────────────────────────────────────────────────────────
# Scoring rules: (pattern, task_type, weight)
# ──────────────────────────────────────────────────────────
_RULES: list[tuple[str, str, float]] = [
    # GitTask — must come first (high-specificity; prevents "push" matching AnalysisTask)
    (r"\b(push|commit|deploy|publish|release|ship|upload to github|send to github)\b", "GitTask", 1.2),
    (r"\b(git (push|commit|add|stage|sync|pull|merge|tag))\b",                         "GitTask", 1.5),
    (r"\b(to (github|remote|origin|main|master|repo|repository))\b",                   "GitTask", 0.9),
    # ExplainTask
    (r"\b(explain|describe|what is|how does|why|clarify|show me|tell me)\b", "ExplainTask", 1.0),
    (r"\b(understand|overview|summary|summarize|document)\b",                "ExplainTask", 0.7),
    # ImplementTask
    (r"\b(implement|create|build|write|add|generate|make|develop|code)\b",   "ImplementTask", 1.0),
    (r"\b(new (module|class|function|method|feature|endpoint))\b",           "ImplementTask", 0.9),
    # RefactorTask
    (r"\b(refactor|improve|optimize|clean|restructure|rename|move|extract)\b","RefactorTask", 1.0),
    (r"\b(simplify|reduce|decouple|split|merge|consolidate)\b",              "RefactorTask", 0.8),
    # AnalysisTask
    (r"\b(analy[sz]e|investigate|inspect|audit|check|review|scan|trace)\b",  "AnalysisTask", 1.0),
    (r"\b(find|detect|discover|list|show|report|count)\b",                   "AnalysisTask", 0.6),
    # DesignTask
    (r"\b(design|architect|plan|structure|model|schema|blueprint)\b",        "DesignTask", 1.0),
    (r"\b(decide|choose|select|evaluate|compare|trade.?off)\b",              "DesignTask", 0.7),
]

_TASK_TYPES = {"ExplainTask", "ImplementTask", "RefactorTask", "AnalysisTask", "DesignTask", "GitTask"}
_CONFIDENCE_THRESHOLD = 0.45   # below this → ask LLM (Mode 2)


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
        return result

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
    # Mode 2: LLM as intent parser (stub until Stage 8)
    # Input → structured JSON: {task_type, confidence}
    # SHACL validates the output schema before use.
    # ──────────────────────────────────────────────

    def _mode2(self, request: str, fallback: ClassificationResult) -> ClassificationResult:
        # Stage 8 will wire the actual LLM call here.
        # For now return the Mode 1 result with mode annotated.
        return ClassificationResult(
            task_type=fallback.task_type,
            confidence=max(fallback.confidence, 0.5),  # stub: assume LLM is confident
            mode_used="llm_stub",
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
