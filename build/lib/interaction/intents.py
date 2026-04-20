"""Structured intent models for the REPL dialog mode."""
from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field

IntentType = Literal[
    "run", "verify", "introspect", "status", "explain",
    "init", "visualize", "tools", "help", "quit", "unknown",
]


class Intent(BaseModel):
    type: IntentType = Field(description="Primary intent category")

    # --- run ---
    request: Optional[str] = Field(
        None, description="Natural-language pipeline request (only for 'run')"
    )
    auto: bool = Field(False, description="Skip interactive prompts")
    commit: bool = Field(False, description="Commit graph results to git")
    push: bool = Field(False, description="Push to remote after commit")

    # --- verify ---
    target: Optional[str] = Field(
        None, description="Specific graph file or entity URI to verify"
    )

    # --- explain / introspect ---
    concept: Optional[str] = Field(
        None,
        description=(
            "Concept, rule ID (G01–G06, R01–R08), entity URI, "
            "stage number, or free-form question topic"
        ),
    )

    # --- knowledge gap: LLM signals it needs more info before acting ---
    needs_clarification: bool = Field(
        False,
        description=(
            "Set True when the user's input is too ambiguous to proceed — "
            "the system must ask a follow-up question first"
        ),
    )
    clarification_question: Optional[str] = Field(
        None,
        description="The clarifying question to present to the user",
    )

    # --- dangerous action guard ---
    is_dangerous: bool = Field(
        False,
        description=(
            "True if this action may overwrite files, delete data, "
            "commit to git, or push to a remote"
        ),
    )
    danger_description: Optional[str] = Field(
        None,
        description="One-sentence summary of the irreversible side-effect",
    )
