# Ontology Engine Project

## How it works

The Ontology Engine project is a software pipeline designed to handle graph storage and management using Python. The pipeline consists of several modules that work together to provide a comprehensive solution for managing ontologies.

1. **Initialization**: The `GraphStore` class initializes the storage system.
2. **Namespace Binding**: The `_bind_namespaces` method binds necessary namespaces for storing ontology data.
3. **Data Loading and Saving**: Data can be loaded using methods like `load_turtle` or saved using `save`.
4. **Addition of Data**: Individual triples can be added to the store using the `add` function, while multiple triples can be added using `add_many`.
5. **Validation**: The `validate` method ensures that the stored data adheres to the specified schema.
6. **Querying and Projection**: The `query` method allows for querying the graph, and `projection` can be used to project specific parts of the graph.
7. **Finalizing Storage**: The `declare_holon` function finalizes the storage process.

## System Requirements

| Requirement  | Version        |
|--------------|----------------|
| Python       | 3.10+          |
| Git          | 2.30+          |
| pip dependencies: |                |
| - rdflib     |                |
| - pyshacl      |                |

## Installation

### Linux/macOS

To install the Ontology Engine on Linux or macOS, use pip:

```bash
pip install ontology-engine
```

### Windows PowerShell

On Windows using PowerShell, you can install the package like this:

```powershell
pip install ontology-engine
```

### WSL2

For Windows Subsystem for Linux (WSL2), installation is similar to Linux:

```bash
pip install ontology-engine
```

## Quick start

To get started with the Ontology Engine, use the `ont` CLI:

```bash
ont init
ont load data.ttl
ont add <subject> <predicate> <object>
ont query "SELECT * WHERE { ?s ?p ?o }"
ont save output.ttl
```

## Project Structure

The project structure is organized as follows:

- `graph_store.py`: Contains the core classes and functions for graph storage.
- `utils.py`: Utility functions for handling data and operations.
- `cli.py`: Command-line interface for interacting with the ontology engine.

For more detailed information, refer to the source code in the repository.