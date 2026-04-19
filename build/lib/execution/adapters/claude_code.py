"""ClaudeCode adapter — uses `claude` CLI via OAuth session.

Works with Claude Pro/Max subscription — no API key required.
The claude CLI must be authenticated (`claude auth login` or existing session).

Calls: claude --print "<prompt>" [--model <model>]
"""
from __future__ import annotations

import re
import subprocess
import shutil

from execution.adapters.base import LLMAdapter, AdapterResult, ThinkingBlock


def _extract_think_tags(text: str) -> tuple[list[ThinkingBlock], str]:
    """Split <think>…</think> blocks out of raw model output."""
    blocks: list[ThinkingBlock] = []
    def _collect(m: re.Match) -> str:
        blocks.append(ThinkingBlock(content=m.group(1).strip()))
        return ""
    cleaned = re.sub(r"<think>(.*?)</think>", _collect, text, flags=re.DOTALL)
    return blocks, cleaned.strip()

DEFAULT_MODEL = "claude-sonnet-4-6"


class ClaudeCodeAdapter(LLMAdapter):
    """Delegates to the local `claude` CLI — uses Pro subscription OAuth."""

    def __init__(self, model: str = DEFAULT_MODEL):
        if not shutil.which("claude"):
            raise RuntimeError(
                "claude CLI not found. Install Claude Code: https://claude.ai/code"
            )
        self.model = model

    @property
    def provider_name(self) -> str:
        return "claude-code"

    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = 8096,
        thinking: bool = False,
        thinking_budget: int = 8000,
    ) -> AdapterResult:
        # thinking= is not supported via claude CLI --print mode
        # Combine system + user into one prompt (claude -p doesn't split them)
        prompt = f"{system}\n\n---\n\n{user}" if system else user

        cmd = ["claude", "--print", "--model", self.model, prompt]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"claude CLI failed (exit {result.returncode}): {result.stderr[:300]}"
            )

        raw = result.stdout.strip()
        thinking_blocks, output = _extract_think_tags(raw)
        return AdapterResult(
            output=output,
            model=self.model,
            provider=self.provider_name,
            thinking_blocks=thinking_blocks,
        )
