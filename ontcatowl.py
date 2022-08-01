from rdflib import Graph

gufo = Graph()
ontology = Graph()

# Input GUFO Ontology
try:
    gufo.parse("resources/gufoEndurantsOnly.ttl")
except OSError:
    print(f"\nERROR. Could not load resources/gufoEndurantsOnly.ttl file. Exiting program.\n")
    exit(1)

# TODO: Read from argument
# Input Ontology
try:
    ontology.parse("resources/d3fend.ttl")
except OSError:
    print(f"\nERROR. Could not load resources/d3fend.ttl file. Exiting program.\n")
    exit(1)

# TODO: Future argument options: save in one file (ont + gufo), save inferences as assertions

# TODO: Verify if there is a way tor reason over the input ontology
# TODO: Study loggers for Python
# TODO: update requirements.txt
