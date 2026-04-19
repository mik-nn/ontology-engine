import os
import subprocess
from rdflib import Graph, Namespace

DEPENDENCIES_TTL = "core/ontology/dependencies.ttl"
SHACL_SHAPES = "core/shacl/dependencies_shapes.ttl"
REQUIREMENTS_OUT = "requirements.txt"
VALIDATOR = "verification/shacl_validator.py"

BUILD = Namespace("https://ontologist.ai/ns/build#")

def validate_dependencies():
    print("Validating dependencies with SHACL...")
    subprocess.run(["python3", VALIDATOR, DEPENDENCIES_TTL, SHACL_SHAPES], check=True)
    print("SHACL validation OK.")

def load_dependencies():
    print("Loading dependencies from RDF...")
    g = Graph()
    g.parse(DEPENDENCIES_TTL, format="turtle")

    deps = []
    for pkg in g.subjects():
        name = g.value(pkg, BUILD.name)
        version = g.value(pkg, BUILD.version)
        if name:
            deps.append(f"{name}{version}" if version else str(name))

    deps = sorted(set(deps))
    print(f"Found {len(deps)} dependencies.")
    return deps

def write_requirements(deps):
    print(f"Writing {REQUIREMENTS_OUT}...")
    with open(REQUIREMENTS_OUT, "w", encoding="utf-8") as f:
        for d in deps:
            f.write(d + "\n")
    print("requirements.txt generated.")

def main():
    validate_dependencies()
    deps = load_dependencies()
    write_requirements(deps)
    print("\nDependency generation pipeline completed.")

if __name__ == "__main__":
    main()
