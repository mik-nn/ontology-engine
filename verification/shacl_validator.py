import sys
from pyshacl import validate
from rdflib import Graph

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 shacl_validator.py <data.ttl> <shapes.ttl>")
        sys.exit(1)

    data_file = sys.argv[1]
    shapes_file = sys.argv[2]

    data_graph = Graph().parse(data_file, format="turtle")
    shapes_graph = Graph().parse(shapes_file, format="turtle")

    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference='rdfs',
        abort_on_first=False,
        meta_shacl=False,
        debug=False
    )

    print(results_text)

    if conforms:
        print("SHACL validation passed.")
        sys.exit(0)
    else:
        print("SHACL validation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
