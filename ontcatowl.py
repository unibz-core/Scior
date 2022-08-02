import logging
from os import times

from owlrl import DeductiveClosure, RDFS_Semantics
from rdflib import Graph
import time

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)

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

# TODO (@pedropaulofb): Read all classes from input ontology and create a list with no repetitions

logging.info("Initializing RDFS inferences. This may take a while...")
st = time.time()
DeductiveClosure(RDFS_Semantics).expand(ontology)   # Performs RDFS inferences
et = time.time()
elapsed_time = et - st
elapsed_time = round(elapsed_time, 2)
logging.info(f"Inferencing process successfully completed on {elapsed_time} seconds.")

# TODO (@pedropaulofb): Create log file parallel to logs printed on std.out (e.g., https://github.com/borntyping/jsonlog)
# TODO (@pedropaulofb): Use different colors for logs levels printed on std.out (e.g. https://betterstack.com/community/questions/how-to-color-python-logging-output/)
# TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions
# TODO (@pedropaulofb): Evaluate on Linux before release first version
# TODO (@pedropaulofb): update requirements.txt
