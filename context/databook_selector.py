"""Databook selection — scope-aware, task-driven.

Queries the graph for db:Databook instances and returns a filtered list
of databook fragments ready for injection into a ContextPacket.

Selection rules (applied in order, additive):
  1. scope=permanent   — always included
  2. scope=project     — always included
  3. scope=task        — included only when task_type matches db:taskType
  4. scope=ephemeral   — excluded unless include_ephemeral=True

Fragments are ordered by (hierarchy ASC, scope priority) so that the
most foundational knowledge appears first in the context.

depends_on edges are resolved: if a selected databook depends on another,
that dependency is also pulled in (one level deep).
"""
from __future__ import annotations

from rdflib import Namespace, RDF, URIRef

from storage.graph_store import GraphStore
from context.databook_chunker import DataBookChunker

DB   = Namespace("https://ontologist.ai/ns/databook#")
PROV = Namespace("http://www.w3.org/ns/prov#")

_SCOPE_PRIORITY = {"permanent": 0, "project": 1, "task": 2, "ephemeral": 3}


class DatabookSelector:
    """Select databook fragments from the graph based on scope and task context.

    Parameters
    ----------
    store : GraphStore
        The loaded RDF graph store.
    content_max_chars : int
        Maximum characters of db:content to include in each fragment.
    """

    def __init__(self, store: GraphStore, content_max_chars: int = 600):
        self.store = store
        self.content_max_chars = content_max_chars

    # ──────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────

    def select(
        self,
        task_type: str | None = None,
        include_ephemeral: bool = False,
        layer_filter: str | None = None,
        max_hierarchy: int = 3,
    ) -> list[dict]:
        """Return ordered list of databook fragment dicts.

        Each dict has: uri, title, scope, layer, hierarchy,
        content_excerpt (optional), task_types (optional),
        depends_on (list of URIs).

        Parameters
        ----------
        task_type : str | None
            Current task type (e.g. "testing", "planning"). Used to match
            scope=task databooks against their db:taskType values.
        include_ephemeral : bool
            If True, ephemeral databooks (TODOs, changelogs) are included.
        layer_filter : str | None
            If set, only include databooks matching this layer
            (e.g. "architecture", "reference").
        max_hierarchy : int
            Exclude databooks with hierarchy > this value (default: all).
        """
        all_frags = self._load_all()

        selected: dict[str, dict] = {}

        for frag in all_frags:
            scope = frag.get("scope", "project")
            hierarchy = frag.get("hierarchy", 3)

            if hierarchy > max_hierarchy:
                continue
            if layer_filter and frag.get("layer") != layer_filter:
                continue

            if scope == "permanent":
                selected[frag["uri"]] = frag
            elif scope == "project":
                selected[frag["uri"]] = frag
            elif scope == "task":
                if task_type and self._matches_task_type(frag, task_type):
                    selected[frag["uri"]] = frag
            elif scope == "ephemeral":
                if include_ephemeral:
                    selected[frag["uri"]] = frag

        # Resolve one level of depends_on — pull in dependencies of selected
        to_add: dict[str, dict] = {}
        all_by_uri = {f["uri"]: f for f in all_frags}
        for frag in list(selected.values()):
            for dep_uri in frag.get("depends_on", []):
                if dep_uri not in selected and dep_uri in all_by_uri:
                    dep = all_by_uri[dep_uri]
                    dep_scope = dep.get("scope", "project")
                    if dep_scope != "ephemeral" or include_ephemeral:
                        to_add[dep_uri] = dep
        selected.update(to_add)

        return self._sort(list(selected.values()))

    def select_relevant(
        self,
        task_request: str | None = None,
        task_type: str | None = None,
        token_budget: int = 1600,
        include_ephemeral: bool = False,
    ) -> tuple[list[dict], bool]:
        """Select databooks within *token_budget*, chunking when needed.

        Returns (fragments, was_chunked).  Each fragment may carry a
        ``content_excerpt`` that is a relevance-filtered subset of the
        full databook content rather than a plain head-truncation.

        Budget allocation strategy
        --------------------------
        1. Run ``select()`` to get candidate set.
        2. Estimate total tokens for all candidates.
        3. If total <= token_budget → return as-is (was_chunked=False).
        4. Otherwise, iterate candidates in sort order (most foundational
           first).  For each databook:
           - If it fits whole → include whole.
           - If not → chunk it; include only sections relevant to
             ``task_request``; stop if remaining budget exhausted.

        Parameters
        ----------
        task_request : str | None
            The user's original request text — used to score chunk relevance.
        task_type : str | None
            Passed through to ``select()`` for task-scoped databooks.
        token_budget : int
            Maximum tokens allocated to all databook fragments combined.
        """
        candidates = self.select(task_type=task_type,
                                 include_ephemeral=include_ephemeral)

        total = sum(self._token_estimate(f.get("content_excerpt", ""))
                    for f in candidates)

        if total <= token_budget:
            return candidates, False

        # ── Chunked mode ──────────────────────────────────────────────────
        chunker = DataBookChunker()
        result: list[dict] = []
        remaining = token_budget

        for frag in candidates:
            if remaining <= 0:
                break

            excerpt = frag.get("content_excerpt", "")
            frag_tokens = self._token_estimate(excerpt)

            if frag_tokens <= remaining:
                result.append(frag)
                remaining -= frag_tokens
            else:
                # Chunk this databook — include only relevant sections
                relevant_text = chunker.select_relevant(
                    content=excerpt,
                    query=task_request or "",
                    token_budget=remaining,
                    title=frag.get("title", ""),
                )
                if relevant_text.strip():
                    chunked_frag = {**frag, "content_excerpt": relevant_text,
                                    "chunked": True}
                    result.append(chunked_frag)
                    remaining -= self._token_estimate(relevant_text)

        return result, True

    def select_chain(self, databook_uris: list[str]) -> list[dict]:
        """Return the reasoning chain for given databook URIs.

        Follows db:dependsOn recursively and returns all reachable databooks
        in dependency order (roots first). Used for chain visualization.
        """
        all_by_uri = {f["uri"]: f for f in self._load_all()}
        visited: list[str] = []
        self._dfs_chain(databook_uris, all_by_uri, set(), visited)
        result = [all_by_uri[uri] for uri in visited if uri in all_by_uri]
        return self._sort(result)

    # ──────────────────────────────────────────────────────────────────────
    # Graph loading
    # ──────────────────────────────────────────────────────────────────────

    def _load_all(self) -> list[dict]:
        g = self.store._g
        frags: list[dict] = []

        for db_uri in g.subjects(RDF.type, DB.Databook):
            frag = self._load_one(db_uri)
            if frag:
                frags.append(frag)

        return frags

    def _load_one(self, db_uri: URIRef) -> dict | None:
        g = self.store._g

        def val(pred):
            v = g.value(db_uri, pred)
            return str(v) if v is not None else None

        title = val(DB.title)
        if not title:
            return None

        frag: dict = {
            "uri":   str(db_uri),
            "title": title,
        }

        scope = val(DB.scope)
        if scope:
            frag["scope"] = scope

        layer = val(DB.layer)
        if layer:
            frag["layer"] = layer

        h = g.value(db_uri, DB.hierarchy)
        if h is not None:
            frag["hierarchy"] = int(h)

        task_type_str = val(DB.taskType)
        if task_type_str:
            frag["task_types"] = [t.strip() for t in task_type_str.split(",") if t.strip()]

        content = val(DB.content)
        if content:
            frag["content_excerpt"] = (
                content[:self.content_max_chars]
                + ("…" if len(content) > self.content_max_chars else "")
            )

        deps = [str(o) for o in g.objects(db_uri, DB.dependsOn)]
        if deps:
            frag["depends_on"] = sorted(deps)

        return frag

    # ──────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _matches_task_type(frag: dict, task_type: str) -> bool:
        task_types = frag.get("task_types", [])
        return task_type in task_types

    @staticmethod
    def _sort(frags: list[dict]) -> list[dict]:
        """Sort by (hierarchy ASC, scope priority ASC, title ASC)."""
        return sorted(
            frags,
            key=lambda f: (
                f.get("hierarchy", 3),
                _SCOPE_PRIORITY.get(f.get("scope", "project"), 1),
                f.get("title", ""),
            ),
        )

    @staticmethod
    def _token_estimate(text: str) -> int:
        return max(1, int(len(text) / 4 * 1.2))

    def _dfs_chain(
        self,
        uris: list[str],
        all_by_uri: dict[str, dict],
        seen: set[str],
        result: list[str],
    ) -> None:
        for uri in uris:
            if uri in seen:
                continue
            seen.add(uri)
            frag = all_by_uri.get(uri)
            if not frag:
                continue
            deps = frag.get("depends_on", [])
            self._dfs_chain(deps, all_by_uri, seen, result)
            result.append(uri)
