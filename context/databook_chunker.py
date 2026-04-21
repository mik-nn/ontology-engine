"""Relevance-based chunking of Databook markdown content.

Splits a document by heading boundaries (H1–H3), scores each chunk
against a query using word-overlap (Jaccard), then greedily fills a
token budget with the highest-scoring chunks — preserving their
original document order in the output.

Used by DatabookSelector.select_relevant() when the total databook
content exceeds the available context budget.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


_CHARS_PER_TOKEN = 4 / 1.2   # inverse of the existing token estimate formula
_HEADING_RE = re.compile(r'^(#{1,3})\s+(.+)$', re.MULTILINE)
_WORD_RE = re.compile(r'\b[a-zA-Z][a-zA-Z0-9_]{2,}\b')


@dataclass
class Chunk:
    heading: str        # full heading text (e.g. "## Design Goals")
    level: int          # 1, 2, or 3
    text: str           # heading line + body text
    score: float = 0.0
    char_count: int = field(init=False)

    def __post_init__(self) -> None:
        self.char_count = len(self.text)

    @property
    def token_estimate(self) -> int:
        return max(1, int(self.char_count / _CHARS_PER_TOKEN))


class DataBookChunker:
    """Split markdown into heading-bounded chunks and select by relevance.

    Parameters
    ----------
    min_chunk_chars : int
        Chunks shorter than this are merged with the next sibling.
    """

    def __init__(self, min_chunk_chars: int = 80):
        self.min_chunk_chars = min_chunk_chars

    # ──────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────

    def select_relevant(
        self,
        content: str,
        query: str,
        token_budget: int,
        title: str = "",
    ) -> str:
        """Return the most relevant portion of *content* within *token_budget*.

        If *query* is empty, returns content from the top until budget.
        Always prepends the document title as a H1 marker so the LLM
        knows which databook the excerpt came from.

        Returns a markdown string (may be shorter than the original).
        """
        chunks = self._split(content)
        if not chunks:
            return content[:int(token_budget * _CHARS_PER_TOKEN)]

        if query:
            q_words = _words(query)
            for chunk in chunks:
                chunk.score = _jaccard(q_words, _words(chunk.text))
        else:
            # No query — preserve document order, score by position (earlier = higher)
            for i, chunk in enumerate(chunks):
                chunk.score = 1.0 / (i + 1)

        selected = self._fill_budget(chunks, token_budget)
        # Restore original document order
        order = {id(c): i for i, c in enumerate(chunks)}
        selected.sort(key=lambda c: order[id(c)])

        header = f"# {title}\n\n" if title else ""
        return header + "\n\n".join(c.text for c in selected)

    def chunk_count(self, content: str) -> int:
        return len(self._split(content))

    # ──────────────────────────────────────────────────────────────────────
    # Splitting
    # ──────────────────────────────────────────────────────────────────────

    def _split(self, content: str) -> list[Chunk]:
        """Split content at heading boundaries."""
        matches = list(_HEADING_RE.finditer(content))
        if not matches:
            # No headings — treat entire content as one chunk
            text = content.strip()
            return [Chunk(heading="", level=1, text=text)] if text else []

        chunks: list[Chunk] = []

        # Text before first heading (preamble)
        preamble = content[:matches[0].start()].strip()
        if preamble:
            chunks.append(Chunk(heading="preamble", level=1, text=preamble))

        for i, m in enumerate(matches):
            level = len(m.group(1))
            heading = m.group(2).strip()
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            text = content[start:end].strip()
            if len(text) >= self.min_chunk_chars or not chunks:
                chunks.append(Chunk(heading=heading, level=level, text=text))
            else:
                # Merge tiny chunk into the previous one
                chunks[-1] = Chunk(
                    heading=chunks[-1].heading,
                    level=chunks[-1].level,
                    text=chunks[-1].text + "\n\n" + text,
                )

        return chunks

    # ──────────────────────────────────────────────────────────────────────
    # Budget filling
    # ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _fill_budget(chunks: list[Chunk], token_budget: int) -> list[Chunk]:
        """Greedily pick highest-scoring chunks that fit within token_budget."""
        sorted_chunks = sorted(chunks, key=lambda c: c.score, reverse=True)
        selected: list[Chunk] = []
        remaining = token_budget

        for chunk in sorted_chunks:
            if chunk.token_estimate <= remaining:
                selected.append(chunk)
                remaining -= chunk.token_estimate
            if remaining <= 0:
                break

        return selected


# ──────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────

def _words(text: str) -> set[str]:
    return {w.lower() for w in _WORD_RE.findall(text)}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)
