import os
import subprocess
from datetime import datetime

PLAN_MD = "docs/implementation_plan.md"
PLAN_DB = "docs/databooks/ImplementationPlan.md"
TTL_OUT = "core/ontology/implementation_plan.ttl"
SHACL_SHAPES = "core/shacl/databook_shapes.ttl"
CONVERTER = "api/tools/md_to_rdf.py"
VALIDATOR = "verification/shacl_validator.py"

YAML_HEADER = f"""databook:
  id: implementation_plan
  title: "Implementation Plan for Ontology Engine"
  version: 1.0.0
  type: architecture
  domain: ontology-engine
  status: draft
  created: {datetime.now().strftime("%Y-%m-%d")}
  updated: {datetime.now().strftime("%Y-%m-%d")}
  author:
    - name: Michael
      iri: https://ontologist.ai/agents/michael
  process:
    transformer: human
    inputs: []
  license: CC-BY-4.0
  tags:
    - ontology
    - architecture
    - pipeline
    - planning
    - shacl
    - reasoning
---
"""

def ensure_directories():
    os.makedirs("docs/databooks", exist_ok=True)
    os.makedirs("core/ontology", exist_ok=True)

def add_yaml_header():
    with open(PLAN_MD, "r", encoding="utf-8") as f:
        body = f.read()

    if body.strip().startswith("databook:"):
        print("YAML header already present — skipping header injection.")
        with open(PLAN_DB, "w", encoding="utf-8") as f:
            f.write(body)
        return

    with open(PLAN_DB, "w", encoding="utf-8") as f:
        f.write(YAML_HEADER + body)

    print(f"Databook created: {PLAN_DB}")

def convert_to_rdf():
    print("Converting Databook to RDF...")
    subprocess.run(["python3", CONVERTER, PLAN_DB, TTL_OUT], check=True)
    print(f"RDF saved to {TTL_OUT}")

def validate_rdf():
    print("Validating RDF with SHACL...")
    subprocess.run(["python3", VALIDATOR, TTL_OUT, SHACL_SHAPES], check=True)
    print("SHACL validation completed.")

def main():
    ensure_directories()
    add_yaml_header()
    convert_to_rdf()
    validate_rdf()
    print("\nDatabook generation pipeline completed successfully.")

if __name__ == "__main__":
    main()
