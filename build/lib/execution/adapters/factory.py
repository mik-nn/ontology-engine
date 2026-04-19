"""AdapterFactory — creates the right LLM adapter from provider config dict.

Config dict schema (from .ontology.toml [llm] section or llm.json):

    provider   : "claude-code" | "anthropic" | "ollama/<model>" | "gemini/<model>"
                 | "openai/<model>" | "litellm/<any-litellm-model-string>"
    model      : model name (provider-specific, overrides provider suffix)
    api_key    : optional explicit key (prefer env vars)
    api_key_env: env var name to read key from (e.g. "GEMINI_API_KEY")
    base_url   : optional base URL (Ollama: "http://localhost:11434", custom endpoints)
    extra      : dict of extra kwargs passed to the provider

Examples:
    {"provider": "claude-code", "model": "claude-sonnet-4-6"}
    {"provider": "anthropic",   "model": "claude-opus-4-7"}
    {"provider": "ollama",      "model": "llama3.2"}
    {"provider": "gemini",      "model": "gemini-2.0-flash", "api_key_env": "GEMINI_API_KEY"}
    {"provider": "openai",      "model": "gpt-4o"}
    {"provider": "litellm",     "model": "bedrock/anthropic.claude-v2"}
"""
from __future__ import annotations

import os
from typing import Any

from execution.adapters.base import LLMAdapter

# Providers that route through LiteLLM with their LiteLLM prefix
_LITELLM_PROVIDERS = {
    "gemini":     "gemini",
    "openai":     "openai",
    "azure":      "azure",
    "ollama":     "ollama",
    "vertex_ai":  "vertex_ai",
    "bedrock":    "bedrock",
    "cohere":     "cohere",
    "mistral":    "mistral",
    "groq":       "groq",
    "together":   "together_ai",
    "huggingface": "huggingface",
}


def create(config: dict[str, Any]) -> LLMAdapter:
    """Instantiate the right adapter from a provider config dict."""
    provider = config.get("provider", "claude-code").lower()
    model    = config.get("model", "")
    api_key  = config.get("api_key") or _env(config.get("api_key_env", ""))
    base_url = config.get("base_url")
    extra    = config.get("extra", {})

    # ── Claude Code (Pro subscription, no API key) ─────────────────────────
    if provider == "claude-code":
        from execution.adapters.claude_code import ClaudeCodeAdapter
        return ClaudeCodeAdapter(model=model or "claude-sonnet-4-6")

    # ── Anthropic SDK direct (with caching) ────────────────────────────────
    if provider == "anthropic":
        from execution.adapters.anthropic_adapter import AnthropicAdapter
        return AnthropicAdapter(model=model or "claude-sonnet-4-6", api_key=api_key)

    # ── LiteLLM passthrough (explicit) ─────────────────────────────────────
    if provider == "litellm":
        from execution.adapters.litellm_adapter import LiteLLMAdapter
        return LiteLLMAdapter(model=model, api_key=api_key,
                              api_base=base_url, extra_params=extra)

    # ── Named providers → LiteLLM with correct prefix ──────────────────────
    litellm_prefix = _LITELLM_PROVIDERS.get(provider)
    if litellm_prefix:
        from execution.adapters.litellm_adapter import LiteLLMAdapter
        # model may already have prefix (e.g. "ollama/llama3.2") or just name
        full_model = (model if model.startswith(f"{litellm_prefix}/")
                      else f"{litellm_prefix}/{model}")
        return LiteLLMAdapter(model=full_model, api_key=api_key,
                              api_base=base_url, extra_params=extra)

    raise ValueError(
        f"Unknown provider '{provider}'. "
        f"Supported: claude-code, anthropic, litellm, "
        + ", ".join(_LITELLM_PROVIDERS)
    )


def _env(var_name: str) -> str | None:
    return os.environ.get(var_name) if var_name else None
