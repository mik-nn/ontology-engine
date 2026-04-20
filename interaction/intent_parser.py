"""Parse free-form user text into a structured Intent.

Two backends, tried in order:
  1. AnthropicParser  — Anthropic SDK + tool_choice (requires ANTHROPIC_API_KEY)
  2. ClaudeCodeParser — `claude --print` CLI (requires claude auth login, no API key)

The LLM only classifies intent and extracts parameters.
All execution logic lives in cli/repl.py and is deterministic.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from typing import Optional

from interaction.intents import Intent

_SYSTEM = """\
You are the intent parser for `ont`, the ontology-engine CLI.

Available operations:
  run        — execute a pipeline with a natural-language request
  verify     — validate the introspection graph via SHACL rules
  introspect — scan source code, rebuild the introspection graph
  status     — show recent pipeline events from the event log
  explain    — explain a concept, rule ID, entity, or decision chain
  init       — initialise the ontology engine for a new project
  visualize  — open the RDF graph viewer
  tools      — manage LLM tool adapters
  help       — show available commands
  quit       — exit the REPL
  unknown    — use when none of the above fits

Extraction rules:
1. For "run": put the user's change request verbatim into `request`.
2. For "explain": put the topic (rule ID like G01/R04, stage name, entity URI,
   or free-form question) into `concept`.
3. Set is_dangerous=true + fill danger_description when the action involves:
   git commit, git push, file deletion, graph overwrite.
4. Set needs_clarification=true + clarification_question when the input is
   too ambiguous to pick an intent confidently.\
"""

_JSON_SUFFIX = """

Respond with ONLY a JSON object matching this schema (no markdown, no explanation):
{schema}
"""


def _build_json_prompt(user_text: str) -> str:
    schema = json.dumps(Intent.model_json_schema(), indent=2)
    return f"{_SYSTEM}{_JSON_SUFFIX.format(schema=schema)}\n\nUser input: {user_text}"


def _extract_json(text: str) -> dict:
    """Extract the first JSON object from raw LLM output."""
    # Strip markdown code fences if present
    text = re.sub(r"```(?:json)?\s*", "", text).strip()
    # Find first {...} block
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        return json.loads(m.group(0))
    return json.loads(text)


# ─────────────────────────────────────────────────────────
# Backend 1 — Anthropic SDK (tool use, most reliable)
# ─────────────────────────────────────────────────────────

class _AnthropicParser:
    def __init__(self, model: str, api_key: str) -> None:
        import anthropic
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model
        self._tool = {
            "name": "parse_intent",
            "description": "Parse user input into a structured intent",
            "input_schema": Intent.model_json_schema(),
        }

    def parse(self, text: str) -> Intent:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=512,
            system=[{"type": "text", "text": _SYSTEM, "cache_control": {"type": "ephemeral"}}],
            tools=[self._tool],
            tool_choice={"type": "tool", "name": "parse_intent"},
            messages=[{"role": "user", "content": text}],
        )
        for block in response.content:
            if getattr(block, "type", None) == "tool_use" and block.name == "parse_intent":
                return Intent.model_validate(block.input)
        raise ValueError("No tool_use block in response")


# ─────────────────────────────────────────────────────────
# Backend 2 — claude CLI (OAuth / Pro subscription)
# ─────────────────────────────────────────────────────────

class _ClaudeCodeParser:
    def __init__(self, model: str) -> None:
        if not shutil.which("claude"):
            raise RuntimeError("claude CLI not found")
        self._model = model

    def parse(self, text: str) -> Intent:
        prompt = _build_json_prompt(text)
        result = subprocess.run(
            ["claude", "--print", "--model", self._model, prompt],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(f"claude CLI error: {result.stderr[:200]}")
        data = _extract_json(result.stdout)
        return Intent.model_validate(data)


# ─────────────────────────────────────────────────────────
# Public facade — auto-selects backend
# ─────────────────────────────────────────────────────────

class IntentParser:
    """Translates raw text → Intent. Uses Anthropic SDK if key is set,
    falls back to `claude` CLI (no API key needed)."""

    def __init__(
        self,
        model: str = "claude-haiku-4-5-20251001",
        api_key: Optional[str] = None,
    ) -> None:
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")

        if key:
            self._backend = _AnthropicParser(model=model, api_key=key)
            self._backend_name = "anthropic-sdk"
        elif shutil.which("claude"):
            self._backend = _ClaudeCodeParser(model=model)
            self._backend_name = "claude-cli"
        else:
            raise RuntimeError(
                "No LLM backend available. "
                "Either set ANTHROPIC_API_KEY or authenticate `claude` CLI."
            )

    @property
    def backend_name(self) -> str:
        return self._backend_name

    def parse(self, text: str) -> Intent:
        """Parse text → Intent. Never raises — returns unknown on any error."""
        try:
            return self._backend.parse(text)
        except Exception as exc:
            return Intent(
                type="unknown",
                concept=text,
                needs_clarification=True,
                clarification_question=f"(Parser error: {exc}) Could you rephrase or use /help?",
            )
