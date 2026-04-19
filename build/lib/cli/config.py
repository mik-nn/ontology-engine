"""Reads .ontology.toml from the current working directory (project root)."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ImportError:
        raise ImportError("Install tomli: pip install tomli")


CONFIG_FILE = ".ontology.toml"


def find_config(start: Path | None = None) -> Path | None:
    """Walk up from start (default: cwd) to find .ontology.toml."""
    current = (start or Path.cwd()).resolve()
    for directory in [current, *current.parents]:
        candidate = directory / CONFIG_FILE
        if candidate.exists():
            return candidate
    return None


def load_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or find_config()
    if config_path is None:
        return {}
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def project_root(cfg: dict[str, Any], config_path: Path | None = None) -> Path:
    """Resolve the project root from config or config file location."""
    if config_path is None:
        config_path = find_config()
    if config_path:
        return config_path.parent
    return Path.cwd()
