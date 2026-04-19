"""LiteLLM adapter — universal router for 100+ providers.

Model string format (LiteLLM convention):
  anthropic/claude-sonnet-4-6       → Anthropic API
  ollama/llama3.2                   → local Ollama
  gemini/gemini-2.0-flash           → Google Gemini
  openai/gpt-4o                     → OpenAI
  azure/gpt-4                       → Azure OpenAI
  vertex_ai/gemini-pro              → Google Vertex AI
  bedrock/anthropic.claude-v2       → AWS Bedrock

API keys are read from environment variables per LiteLLM convention:
  ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, etc.
For local models (Ollama) no key is needed.
"""
from __future__ import annotations

import os
import re

from execution.adapters.base import LLMAdapter, AdapterResult, ThinkingBlock


def _extract_think_tags(text: str) -> tuple[list[ThinkingBlock], str]:
    """Split <think>…</think> blocks out of raw model output."""
    blocks: list[ThinkingBlock] = []
    def _collect(m: re.Match) -> str:
        blocks.append(ThinkingBlock(content=m.group(1).strip()))
        return ""
    cleaned = re.sub(r"<think>(.*?)</think>", _collect, text, flags=re.DOTALL)
    return blocks, cleaned.strip()


class LiteLLMAdapter(LLMAdapter):
    """Routes to any provider via LiteLLM."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        api_base: str | None = None,
        extra_params: dict | None = None,
    ):
        try:
            import litellm as _ll  # noqa: F401
        except ImportError:
            raise RuntimeError(
                "litellm not installed. Run: pip install litellm\n"
                "Or add to pyproject.toml dependencies."
            )
        self.model = model
        self.api_key = api_key
        self.api_base = api_base
        self.extra_params = extra_params or {}

    @property
    def provider_name(self) -> str:
        return self.model.split("/")[0] if "/" in self.model else "litellm"

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = 8096,
        thinking: bool = False,
        thinking_budget: int = 8000,
    ) -> AdapterResult:
        import litellm

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})

        kwargs: dict = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            **self.extra_params,
        }
        if self.api_key:
            kwargs["api_key"] = self.api_key
        if self.api_base:
            kwargs["api_base"] = self.api_base

        response = litellm.completion(**kwargs)

        raw = response.choices[0].message.content or ""
        thinking_blocks, output = _extract_think_tags(raw)

        usage = response.usage or {}
        return AdapterResult(
            output=output,
            input_tokens=getattr(usage, "prompt_tokens", 0),
            output_tokens=getattr(usage, "completion_tokens", 0),
            model=self.model,
            provider=self.provider_name,
            thinking_blocks=thinking_blocks,
        )
