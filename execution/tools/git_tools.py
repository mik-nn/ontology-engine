"""Git tools — deterministic git operations, no LLM."""
from __future__ import annotations

import re
from typing import Any

from execution.tools.base import Tool, ToolResult
from execution.tools.registry import register


class GitStatusTool(Tool):
    """Show working tree status."""

    name = "git:status"
    description = "Show changed, staged and untracked files."
    patterns = [
        r"\bgit status\b",
        r"\bwhat.s (changed|modified|new|staged)\b",
        r"\bshow (changes|diff|status)\b",
    ]

    def run(self, request: str, **ctx: Any) -> ToolResult:
        from pipeline.git_client import GitClient
        git: GitClient = ctx.get("git") or GitClient()
        status = git.status()
        output = status if status else "Working tree is clean."
        return ToolResult(tool_name=self.name, success=True, output=output)


class GitStageTool(Tool):
    """Stage all modified and untracked files."""

    name = "git:stage"
    description = "Stage all changes (git add .)."
    patterns = [
        r"\bgit (add|stage)\b",
        r"\bstage (all|everything|changes)\b",
    ]

    def run(self, request: str, **ctx: Any) -> ToolResult:
        from pipeline.git_client import GitClient
        git: GitClient = ctx.get("git") or GitClient()
        changed = git.changed_files()
        if not changed:
            return ToolResult(tool_name=self.name, success=True,
                              output="Nothing to stage — working tree clean.")
        git.stage(changed)
        return ToolResult(
            tool_name=self.name, success=True,
            output=f"Staged {len(changed)} file(s).",
            metadata={"files": changed},
        )


class GitCommitTool(Tool):
    """Stage all changes and create a commit."""

    name = "git:commit"
    description = "Stage and commit all changes with an optional message."
    patterns = [
        r"\bgit commit\b",
        r"\bcommit (changes|everything|all|files)\b",
        r"\bсоздай коммит\b",
    ]

    def run(self, request: str, **ctx: Any) -> ToolResult:
        from pipeline.git_client import GitClient
        git: GitClient = ctx.get("git") or GitClient()
        changed = git.changed_files()
        if not changed:
            return ToolResult(tool_name=self.name, success=True,
                              output="Nothing to commit — working tree clean.")
        git.stage(changed)
        # Extract a commit message hint from the request
        msg = _extract_message(request) or f"ont: {request[:72]}"
        result = git.commit(msg)
        if result.success:
            return ToolResult(
                tool_name=self.name, success=True,
                output=f"Committed {len(changed)} file(s): {result.commit_hash} on {result.branch}",
                metadata={"hash": result.commit_hash, "branch": result.branch},
            )
        return ToolResult(tool_name=self.name, success=False, output="", error=result.error)


class GitPushTool(Tool):
    """Push current branch to origin (no commit)."""

    name = "git:push"
    description = "Push the current branch to origin."
    patterns = [
        r"\bgit push\b",
        r"\bpush (to )?(origin|remote)\b",
        r"\b(отправь|запушь) (в|на) (github|origin|remote)\b",
    ]

    def run(self, request: str, **ctx: Any) -> ToolResult:
        from pipeline.git_client import GitClient
        git: GitClient = ctx.get("git") or GitClient()
        result = git.push()
        if result.success:
            return ToolResult(
                tool_name=self.name, success=True,
                output=f"Pushed '{result.branch}' → {result.remote}.",
                metadata={"remote": result.remote, "branch": result.branch},
            )
        return ToolResult(tool_name=self.name, success=False, output="", error=result.error)


class GitSyncTool(Tool):
    """Stage + commit + push in one step.

    Matches the most common developer intent: "push to github", "sync everything", etc.
    """

    name = "git:sync"
    description = "Stage all changes, commit, and push to origin."
    patterns = [
        r"\bpush (to |into )?(github|gitlab|bitbucket|remote|origin|master|main|repo)\b",
        r"\b(sync|upload|send|отправь).*(github|gitlab|origin|remote|repo)\b",
        r"\b(запушь|выложи|залей).*(github|gitlab|origin)\b",
        r"\bgit sync\b",
        r"\bpush (all|everything|changes)\b",
    ]

    def run(self, request: str, **ctx: Any) -> ToolResult:
        from pipeline.git_client import GitClient
        git: GitClient = ctx.get("git") or GitClient()

        changed = git.changed_files()
        lines: list[str] = []

        if changed:
            git.stage(changed)
            lines.append(f"Staged {len(changed)} file(s).")
            msg = _extract_message(request) or f"ont: {request[:72]}"
            commit_r = git.commit(msg)
            if commit_r.success:
                lines.append(f"Committed {commit_r.commit_hash} on {commit_r.branch}.")
            else:
                return ToolResult(
                    tool_name=self.name, success=False,
                    output="\n".join(lines), error=commit_r.error,
                )
        else:
            lines.append("Working tree clean — nothing to commit.")

        push_r = git.push()
        if push_r.success:
            lines.append(f"Pushed '{push_r.branch}' → {push_r.remote}.")
            return ToolResult(tool_name=self.name, success=True, output="\n".join(lines))
        return ToolResult(
            tool_name=self.name, success=False,
            output="\n".join(lines), error=push_r.error,
        )


# ── helpers ───────────────────────────────────────────────────────────────────

def _extract_message(request: str) -> str:
    """Extract a quoted string from the request to use as commit message."""
    m = re.search(r'["\u201c\u201d](.+?)["\u201c\u201d]', request)
    return m.group(1) if m else ""


# ── auto-register all tools in priority order ─────────────────────────────────

register(GitSyncTool())      # most specific first
register(GitPushTool())
register(GitCommitTool())
register(GitStageTool())
register(GitStatusTool())
