"""Base adapter interface — all LLM providers implement this."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AdapterResult:
    output: str
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    model: str = ""
    provider: str = ""
    thinking_blocks: list["ThinkingBlock"] = None  # type: ignore[assignment]

    def __post_init__(self):
        if self.thinking_blocks is None:
            self.thinking_blocks = []

    @property
    def summary(self) -> str:
        parts = [f"provider={self.provider}", f"model={self.model}"]
        if self.input_tokens:
            parts.append(f"in={self.input_tokens} out={self.output_tokens}")
        if self.cache_read_tokens:
            parts.append(f"cache_read={self.cache_read_tokens}")
        return " ".join(parts)


@dataclass
class ThinkingBlock:
    """Extended thinking content — reasoning the model did before answering."""
    content: str


class LLMAdapter(ABC):
    """Stateless adapter: (system, user) → AdapterResult."""

    @abstractmethod
    def complete(
        self,
        system: str,
        user: str,
        max_tokens: int = 8096,
        thinking: bool = False,
        thinking_budget: int = 8000,
    ) -> AdapterResult: ...

    @property
    @abstractmethod
    def provider_name(self) -> str: ...
