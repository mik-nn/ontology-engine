"""Anthropic SDK adapter — direct API with prompt caching and extended thinking.

Requires ANTHROPIC_API_KEY environment variable.
Set thinking=True in .ontology.toml [llm] to enable extended thinking output.
"""
from __future__ import annotations

import os

from execution.adapters.base import LLMAdapter, AdapterResult, ThinkingBlock

DEFAULT_MODEL = "claude-sonnet-4-6"


class AnthropicAdapter(LLMAdapter):
    """Direct Anthropic SDK with prompt caching and optional extended thinking."""

    def __init__(self, model: str = DEFAULT_MODEL, api_key: str | None = None):
        try:
            import anthropic as _a  # noqa: F401
        except ImportError:
            raise RuntimeError("anthropic not installed. Run: pip install anthropic")

        import anthropic
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY not set. "
                "Export it or use provider=claude-code for Pro subscription."
            )
        self._client = anthropic.Anthropic(api_key=key)
        self.model = model

    @property
    def provider_name(self) -> str:
        return "anthropic"

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = 8096,
        thinking: bool = False,
        thinking_budget: int = 8000,
    ) -> AdapterResult:
        import anthropic

        system_blocks = []
        if system:
            system_blocks = [{"type": "text", "text": system,
                              "cache_control": {"type": "ephemeral"}}]

        kwargs: dict = dict(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": user}],
        )
        if system_blocks:
            kwargs["system"] = system_blocks

        if thinking:
            # Extended thinking — budget_tokens must be < max_tokens
            kwargs["thinking"] = {
                "type": "enabled",
                "budget_tokens": min(thinking_budget, max_tokens - 1000),
            }

        response = self._client.messages.create(**kwargs)

        # Separate thinking blocks from text blocks
        thinking_parts: list[ThinkingBlock] = []
        text_parts: list[str] = []
        for block in response.content:
            if block.type == "thinking":
                thinking_parts.append(ThinkingBlock(content=block.thinking))
            elif block.type == "text":
                text_parts.append(block.text)

        usage = response.usage
        return AdapterResult(
            output="\n".join(text_parts),
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            cache_read_tokens=getattr(usage, "cache_read_input_tokens", 0),
            cache_write_tokens=getattr(usage, "cache_creation_input_tokens", 0),
            model=self.model,
            provider=self.provider_name,
            thinking_blocks=thinking_parts,
        )
