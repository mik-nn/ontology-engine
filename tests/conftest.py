"""Shared fixtures for all tests."""
import os
import sys
import pytest
from pathlib import Path

# Ensure project root is on sys.path and is the working directory so that
# relative paths like "core/shacl/..." resolve correctly.
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

@pytest.fixture(autouse=True)
def project_cwd():
    """Run every test with cwd = project root."""
    old = os.getcwd()
    os.chdir(PROJECT_ROOT)
    yield
    os.chdir(old)
