The write was blocked. The file content to replace `execution/adapters/base.py` adds docstrings to all previously undocumented members (`AdapterResult`, `__post_init__`, `summary`, `complete`, `provider_name`) to satisfy the `oe:CodeModuleShape` SHACL constraint. The abstract `complete()` body changes from `...` to a proper docstring string, which is valid Python for an abstract method.

Here is the complete file content:

```python
"""Base adapter interface — all LLM providers implement this."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AdapterResult:
    """Normalised result returned by every LLM adapter."""

    output: str
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    model: str = ""
    provider: str = ""
    thinking_blocks: list["ThinkingBlock"] = None  # type: ignore[assignment]

    def __post_init__(self):
        """Ensure thinking_blocks is always a list, never None."""
        if self.thinking_blocks is None:
            self.thinking_blocks = []

    @property
    def summary(self) -> str:
        """Return a single-line human-readable token/provider summary."""
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
    ) -> AdapterResult:
        """Send (system, user) to the provider and return a normalised AdapterResult."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the short provider identifier (e.g. 'anthropic', 'claude-code')."""
```

Changes from current state:
- `AdapterResult` — added class docstring
- `__post_init__` — added one-line docstring
- `summary` — added one-line docstring
- `complete` — body changed from `...` to a docstring (valid abstract method body in Python)
- `provider_name` — body changed from `...` to a docstring