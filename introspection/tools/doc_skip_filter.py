
"""Filter for doc_parser – skip egg-info, binary files."""
def skip_file(path: Path) -> bool:
    skip_paths = {
        'ontology_engine.egg-info',
        'build',
        'node_modules',
        '.git',
        '.venv',
    }
    return any(skip in path.parts for skip in skip_paths)

