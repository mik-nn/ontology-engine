"""Stage 8 — GitClient.

Real subprocess-based git operations. Returns typed results.
LLM never touches git — this module is the only git actor.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class GitCommitResult:
    success: bool
    commit_hash: Optional[str]
    branch: Optional[str]
    message: str
    error: Optional[str] = None


@dataclass
class GitPushResult:
    success: bool
    remote: str
    branch: str
    error: Optional[str] = None


class GitClient:
    """Wraps subprocess git calls. All operations are explicit — no auto-push."""

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root).resolve()

    def _run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args],
            cwd=str(self.repo_root),
            capture_output=True,
            text=True,
            check=check,
        )

    def status(self) -> str:
        result = self._run("status", "--short", check=False)
        return result.stdout.strip()

    def stage(self, paths: list[str]) -> bool:
        """Stage specific files. Returns True on success."""
        try:
            self._run("add", "--", *paths)
            return True
        except subprocess.CalledProcessError:
            return False

    def commit(self, message: str, author: str = "OntologyEngine") -> GitCommitResult:
        """Create a commit. Returns GitCommitResult with hash."""
        try:
            # Check there's something staged
            diff = self._run("diff", "--cached", "--name-only")
            if not diff.stdout.strip():
                return GitCommitResult(
                    success=False,
                    commit_hash=None,
                    branch=self._current_branch(),
                    message=message,
                    error="Nothing staged to commit.",
                )

            self._run(
                "commit",
                f"--author={author} <noreply@ontologist.ai>",
                "-m", message,
            )
            hash_result = self._run("rev-parse", "--short", "HEAD")
            branch = self._current_branch()
            return GitCommitResult(
                success=True,
                commit_hash=hash_result.stdout.strip(),
                branch=branch,
                message=message,
            )
        except subprocess.CalledProcessError as exc:
            return GitCommitResult(
                success=False,
                commit_hash=None,
                branch=self._current_branch(),
                message=message,
                error=exc.stderr.strip(),
            )

    def push(self, remote: str = "origin", branch: Optional[str] = None) -> GitPushResult:
        """Push to remote. Requires explicit call — never auto-invoked."""
        branch = branch or self._current_branch()
        try:
            self._run("push", remote, branch)
            return GitPushResult(success=True, remote=remote, branch=branch)
        except subprocess.CalledProcessError as exc:
            return GitPushResult(
                success=False,
                remote=remote,
                branch=branch,
                error=exc.stderr.strip(),
            )

    def _current_branch(self) -> Optional[str]:
        try:
            result = self._run("rev-parse", "--abbrev-ref", "HEAD")
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def changed_files(self) -> list[str]:
        """Return list of modified/untracked files."""
        result = self._run("status", "--short", check=False)
        files = []
        for line in result.stdout.splitlines():
            if line.strip():
                files.append(line[3:].strip())
        return files
