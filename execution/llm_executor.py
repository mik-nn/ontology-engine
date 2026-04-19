"""Universal LLM executor — Stage 8.

Builds a structured prompt from task + context packet + AI-Todos,
then delegates to the configured LLM adapter.

Provider is selected from .ontology.toml [llm] section:
    [llm]
    provider = "claude-code"          # Pro subscription, no API key
    model    = "claude-sonnet-4-6"

    # or any other provider:
    provider = "ollama"
    model    = "llama3.2"
    base_url = "http://localhost:11434"

    provider = "gemini"
    model    = "gemini-2.0-flash"
    api_key_env = "GEMINI_API_KEY"
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from context.context_builder import ContextPacket
from execution.adapters.base import AdapterResult, LLMAdapter

_SYSTEM = """\
You are an atomic executor inside an ontology-driven software pipeline.
You receive:
  1. A TASK — exactly what needs to be implemented or written.
  2. A CONTEXT PACKET — structured facts from the project ontology graph.
  3. An AI-TODO LIST — incomplete stub implementations to address (optional).

Rules:
- Implement ONLY what the task asks. Do not refactor unrelated code.
- Output implementation-ready code or documentation, not explanations.
- When writing code: output ONLY the file content, no markdown fences unless asked.
- When the task is analysis/reasoning: output a concise structured report.
- Never invent facts not present in the context packet.

MANDATORY for every Python file you generate:
- The very first statement after imports must be a module-level docstring (\"\"\"...\"\"\").
- Every function and class you write must have a one-line docstring.
- No undocumented code may be committed — the SHACL shape oe:CodeModuleShape
  enforces sh:Warning on missing oe:description, and the pipeline will surface it as G04.
"""


@dataclass
class LLMResult:
    output: str
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    model: str
    provider: str

    @property
    def summary(self) -> str:
        r = AdapterResult(
            output=self.output,
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
            cache_read_tokens=self.cache_read_tokens,
            cache_write_tokens=self.cache_write_tokens,
            model=self.model,
            provider=self.provider,
        )
        return r.summary


class LLMExecutor:
    """Composes prompt and calls adapter. Provider-agnostic."""

    def __init__(
        self,
        adapter: LLMAdapter,
        max_tokens: int = 8096,
        thinking: bool = False,
        thinking_budget: int = 8000,
        verbose: bool = False,
    ):
        self._adapter = adapter
        self.max_tokens = max_tokens
        self.thinking = thinking
        self.thinking_budget = thinking_budget
        self.verbose = verbose

    @classmethod
    def from_config(cls, llm_config: dict[str, Any], max_tokens: int = 8096) -> "LLMExecutor":
        """Create executor from .ontology.toml [llm] dict."""
        from execution.adapters import factory
        adapter = factory.create(llm_config)
        return cls(
            adapter=adapter,
            max_tokens=max_tokens,
            thinking=llm_config.get("thinking", False),
            thinking_budget=llm_config.get("thinking_budget", 8000),
            verbose=llm_config.get("verbose", False),
        )

    def run(
        self,
        task_description: str,
        context: ContextPacket,
        ai_todos: list[dict] | None = None,
        target_file: str | None = None,
        target_file_content: str | None = None,
    ) -> LLMResult:
        user_msg = self._build_user(
            task_description, context, ai_todos,
            target_file=target_file,
            target_file_content=target_file_content,
        )
        result = self._adapter.complete(
            system=_SYSTEM,
            user=user_msg,
            max_tokens=self.max_tokens,
            thinking=self.thinking,
            thinking_budget=self.thinking_budget,
        )

        if self.verbose and result.thinking_blocks:
            print("\n── Model reasoning ──────────────────────────")
            for i, tb in enumerate(result.thinking_blocks, 1):
                print(f"[thinking {i}]\n{tb.content}\n")
            print("─────────────────────────────────────────────\n")

        return LLMResult(
            output=result.output,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            cache_read_tokens=result.cache_read_tokens,
            cache_write_tokens=result.cache_write_tokens,
            model=result.model,
            provider=result.provider,
        )

    def _build_user(
        self,
        task_description: str,
        context: ContextPacket,
        ai_todos: list[dict] | None,
        target_file: str | None = None,
        target_file_content: str | None = None,
    ) -> str:
        parts = [context.to_prompt_text()]

        if target_file and target_file_content is not None:
            parts.append(
                f"## TARGET FILE\n{target_file}\n\n"
                f"## CURRENT CONTENT\n```python\n{target_file_content}\n```"
            )

        parts.append(f"## TASK\n{task_description}")

        if ai_todos:
            todo_lines = [
                f"  - {t.get('function', '?')} in {t.get('file', '?')}: {t.get('reason', '')}"
                for t in ai_todos[:10]
            ]
            parts.append("## AI-TODO (stubs in scope)\n" + "\n".join(todo_lines))

        if target_file:
            parts.append(
                f"Output the COMPLETE new content of {target_file}. "
                "No markdown fences, no explanation — file content only."
            )
        else:
            parts.append("Implement the task. Output implementation only.")
        return "\n\n".join(parts)
