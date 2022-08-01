from owlrl import DeductiveClosure, RDFS_Semantics
from rdflib import Graph
import logging

gufo = Graph()
ontology = Graph()

# Input GUFO ontology
# TODO (@pedropaulofb): Change for the complete version of GUFO after the tests are finished.
try:
    gufo.parse("resources/gufoEndurantsOnly.ttl")
except OSError:
    logging.error("Could not load resources/gufoEndurantsOnly.ttl file. Exiting program.")
    exit(1)

# TODO (@pedropaulofb): Read from argument
# Input ontology to be evaluated
try:
    ontology.parse("resources/d3fend.ttl")
except OSError:
    logging.error("Could not load resources/d3fend.ttl file. Exiting program.")
    exit(1)

# Performs RDFS inferences
DeductiveClosure(RDFS_Semantics).expand(ontology)

# TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions
# TODO (@pedropaulofb): Study loggers for Python
# TODO (@pedropaulofb): update requirements.txt
