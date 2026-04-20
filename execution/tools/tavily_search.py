"""Tavily search tool — AI-optimized search engine API.

Requires TAVILY_API_KEY env var.
"""
import os
import requests
from typing import Any

from execution.tools.base import Tool, ToolResult
# from storage.id_manager import next_id  # unused

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
BASE_URL = "https://api.tavily.com/search"


class TavilySearchTool(Tool):
    name = "tavily_search"
    description = "Search the web using Tavily (AI-powered search API). Use for internet research, docs lookup, API references."

    def matches(self, request: str) -> float:
        score = 0.0
        text = request.lower()
        if any(word in text for word in ["search", "google", "find online", "docs", "tutorial", "api reference"]):
            score += 0.8
        if "tavily" in text:
            score += 0.2
        return min(1.0, score)

    def run(self, query: str, max_results: int = 5, **kwargs) -> ToolResult:
        if not TAVILY_API_KEY:
            return ToolResult(
                success=False,
                output="TAVILY_API_KEY not set. Get free key: https://app.tavily.com (pip install tavily-python)",
                model="tool_error",
            )

        params = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": True,
            "include_images": False,
            "include_raw_content": False,
        }
        try:
            resp = requests.post(BASE_URL, json=params, timeout=30)
            data = resp.json()
            if resp.status_code != 200:
                return ToolResult(
                    success=False,
                    output=f"Tavily API error {resp.status_code}: {data.get('error', 'unknown')}",
                )

            answer = data.get("answer", "No summary generated.")
            results = data.get("results", [])
            urls = [r["url"] for r in results]
            output = f"**Tavily Summary:** {answer}\\n\\n**Top URLs:**\\n" + "\\n".join(f"- {u}" for u in urls[:3])

            return ToolResult(
                success=True,
                output=output,
                metadata={"urls": urls, "answer": answer, "query": query},
                model=self.name,
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=f"Tavily search failed: {str(e)}",
                model=self.name,
            )


# Register automatically
from .registry import register
register(TavilySearchTool())
