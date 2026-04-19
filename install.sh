#!/usr/bin/env bash
# Install ont CLI globally via pipx (Linux / macOS / WSL)
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v pipx &>/dev/null; then
    echo "pipx not found. Installing..."
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    echo "Restart your shell or run: source ~/.bashrc"
fi

echo "Installing ont from $REPO_DIR ..."
pipx install --editable "$REPO_DIR"

echo ""
echo "Done. Run: ont --help"
