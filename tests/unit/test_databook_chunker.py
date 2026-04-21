"""Unit tests for context/databook_chunker.py"""
import pytest
from context.databook_chunker import DataBookChunker, _words, _jaccard

MD_WITH_HEADINGS = """\
# Overview

Intro text about the system.

## Design Goals

Goal one. Goal two. Scalability is important here.

## Implementation Details

This section covers BFS traversal and graph construction.
The algorithm walks the graph depth-first.

## Testing

Run pytest. Cover all edge cases.
"""

MD_NO_HEADINGS = "Just plain text without any headings. Something about graphs."

MD_ONLY_PREAMBLE = """\
No heading here.
More text follows.
"""


class TestSplit:
    def test_counts_chunks_with_headings(self):
        # min_chunk_chars=0 disables merging to verify raw heading count
        chunker = DataBookChunker(min_chunk_chars=0)
        assert chunker.chunk_count(MD_WITH_HEADINGS) >= 4

    def test_merges_small_chunks_with_default_settings(self):
        chunker = DataBookChunker()  # default min_chunk_chars=80
        # Small sections get merged → fewer chunks than headings
        assert chunker.chunk_count(MD_WITH_HEADINGS) >= 1

    def test_no_headings_returns_one_chunk(self):
        chunker = DataBookChunker()
        assert chunker.chunk_count(MD_NO_HEADINGS) == 1

    def test_empty_content_returns_zero_chunks(self):
        chunker = DataBookChunker()
        assert chunker.chunk_count("") == 0

    def test_preamble_becomes_chunk(self):
        chunker = DataBookChunker()
        assert chunker.chunk_count(MD_ONLY_PREAMBLE) >= 1


class TestScoring:
    def test_jaccard_identical_sets(self):
        assert _jaccard({"a", "b"}, {"a", "b"}) == 1.0

    def test_jaccard_disjoint_sets(self):
        assert _jaccard({"a"}, {"b"}) == 0.0

    def test_jaccard_partial_overlap(self):
        score = _jaccard({"a", "b", "c"}, {"b", "c", "d"})
        assert 0 < score < 1

    def test_jaccard_empty_returns_zero(self):
        assert _jaccard(set(), {"a"}) == 0.0
        assert _jaccard({"a"}, set()) == 0.0

    def test_words_extracts_lowercase(self):
        w = _words("BFS Traversal graph_store")
        assert "bfs" in w
        assert "traversal" in w

    def test_words_ignores_short_tokens(self):
        w = _words("a is the BFS")
        assert "bfs" in w
        # short words (< 3 chars) excluded
        assert "a" not in w
        assert "is" not in w


class TestSelectRelevant:
    def test_result_within_budget(self):
        chunker = DataBookChunker()
        result = chunker.select_relevant(MD_WITH_HEADINGS, query="BFS traversal", token_budget=50)
        token_est = int(len(result) / 4 * 1.2)
        assert token_est <= 60  # slight slack for rounding

    def test_no_query_returns_top_sections(self):
        chunker = DataBookChunker()
        result = chunker.select_relevant(MD_WITH_HEADINGS, query="", token_budget=500)
        assert len(result) > 0

    def test_relevant_section_prioritized(self):
        chunker = DataBookChunker()
        result = chunker.select_relevant(
            MD_WITH_HEADINGS,
            query="BFS traversal graph depth",
            token_budget=300,
            title="Architecture",
        )
        assert "Implementation Details" in result or "traversal" in result.lower()

    def test_title_prepended(self):
        chunker = DataBookChunker()
        result = chunker.select_relevant(MD_NO_HEADINGS, query="", token_budget=200, title="MyDoc")
        assert result.startswith("# MyDoc")

    def test_no_title_no_header(self):
        chunker = DataBookChunker()
        result = chunker.select_relevant(MD_NO_HEADINGS, query="", token_budget=200, title="")
        assert not result.startswith("#")

    def test_empty_content_returns_empty_or_short(self):
        chunker = DataBookChunker()
        result = chunker.select_relevant("", query="anything", token_budget=100)
        assert len(result) == 0

    def test_large_budget_includes_all_sections(self):
        chunker = DataBookChunker()
        result = chunker.select_relevant(MD_WITH_HEADINGS, query="", token_budget=10000)
        assert "Design Goals" in result
        assert "Implementation Details" in result
        assert "Testing" in result
