from rdflib import Graph, RDF

g = Graph()
g.bind("rdf", RDF)

# TODO: Read https://rdflib.readthedocs.io/en/stable/namespaces_and_bindings.html

# TODO: Load GUFO from ./resources in a graph
# TODO: Load the ontology to be evaluated from fix path (for testing purposes) in a second graph
# TODO: Load the ontology to be evaluated from argument in a second graph
# TODO: Verify if there is a way tor reason over the input ontology
# TODO: update requirements.txt