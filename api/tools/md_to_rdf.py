import sys
import yaml
from rdflib import Graph, Namespace, Literal, RDF, URIRef

DB = Namespace("https://ontologist.ai/ns/databook#")
DB_INST = Namespace("https://ontologist.ai/databooks/")

def md_to_rdf(md_path: str, ttl_path: str) -> None:
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Format: YAML block (no leading ---) then --- then markdown body
    sep = content.find("\n---\n")
    if sep == -1:
        sep = content.find("\n---")
    if sep == -1:
        raise ValueError(f"No --- separator found in {md_path}")

    meta = yaml.safe_load(content[:sep])
    body = content[sep:].lstrip("\n-").lstrip()

    databook = meta.get("databook", meta)
    book_id = databook["id"]
    book_uri = DB_INST[book_id]

    g = Graph()
    g.bind("db", DB)
    g.add((book_uri, RDF.type, DB.Databook))

    scalar_fields = {"id", "title", "version", "type", "created", "updated",
                     "status", "domain", "license"}

    for key, value in databook.items():
        if key in scalar_fields:
            g.add((book_uri, DB[key], Literal(str(value))))
        elif key == "author":
            # canonical: author is list of {name, iri} or plain strings
            authors = value if isinstance(value, list) else [value]
            for a in authors:
                if isinstance(a, dict):
                    g.add((book_uri, DB["authorName"], Literal(a.get("name", ""))))
                    if "iri" in a:
                        g.add((book_uri, DB["authorIRI"], URIRef(a["iri"])))
                else:
                    g.add((book_uri, DB["authorName"], Literal(str(a))))
        elif key == "authors":
            # legacy list-of-strings form
            for a in (value if isinstance(value, list) else [value]):
                g.add((book_uri, DB["authorName"], Literal(str(a))))
        elif key == "process":
            if isinstance(value, dict):
                if "transformer" in value:
                    g.add((book_uri, DB["transformer"], Literal(str(value["transformer"]))))
                for inp in value.get("inputs", []):
                    g.add((book_uri, DB["processInput"], URIRef(inp) if inp.startswith("http") else Literal(inp)))
        elif key == "tags":
            for tag in (value if isinstance(value, list) else [value]):
                g.add((book_uri, DB["tag"], Literal(str(tag))))

    g.add((book_uri, DB["content"], Literal(body.strip())))
    g.serialize(ttl_path, format="turtle")
    print(f"Saved RDF to {ttl_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 md_to_rdf.py <input.md> <output.ttl>")
        sys.exit(1)
    md_to_rdf(sys.argv[1], sys.argv[2])
