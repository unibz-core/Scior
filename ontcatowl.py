"""Main module for OntCatOWL"""

import time
from datetime import datetime

from rdflib import Graph

from modules.data_initialization_gufo import initialize_gufo_dictionary
from modules.data_initialization_ontology import initialize_ontology, initialize_nodes_lists
from modules.dataclass_verifications import verify_all_ontology_dataclasses_consistency
from modules.logger_config import initialize_logger

if __name__ == "__main__":

    ### DATA LOADINGS AND INITIALIZATIONS

    # Logger initialization
    logger = initialize_logger()

    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"OntCatOWL started on {date_time}!")

    # TODO (@pedropaulofb): Read from argument

    # Input ontology_graph to be evaluated
    ontology_graph = Graph()
    try:
        ontology_graph.parse("resources/d3fend.ttl")
    except OSError:
        logger.error("Could not load resources/d3fend.ttl file. Exiting program.")
        exit(1)

    gufo_dictionary = initialize_gufo_dictionary()

    logger.info("Initializing RDFS reasoning. This may take a while...")
    st = time.perf_counter()
    # DeductiveClosure(RDFS_Semantics).expand(ontology_graph)
    et = time.perf_counter()
    elapsed_time = round((et - st), 3)
    logger.info(f"Reasoning process completed in {elapsed_time} seconds.")

    ontology_dataclass = initialize_ontology(ontology_graph, gufo_dictionary)
    ontology_nodes = initialize_nodes_lists(ontology_graph)

    verify_all_ontology_dataclasses_consistency(ontology_dataclass)

    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"OntCatOWL concluded on {date_time}!")

# TODO (@pedropaulofb): The ontology_graph may already contain relations with GUFO. Treat that.
# TODO (@pedropaulofb): Argument -d for printing log file
# TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions
# TODO (@pedropaulofb): Verify possibility to check consistency using a reasoner.
# TODO (@pedropaulofb): Is there a way to define the GUFO list as read-only?
# TODO (@pedropaulofb): Verify if there is any unused module, function or method
# TODO (@pedropaulofb): Evaluate on Linux before release first version
# TODO (@pedropaulofb): Update requirements.txt
# TODO (@pedropaulofb): OntCatOWL can became a generic mapper tool!
# TODO (@pedropaulofb): Treat problem with huge ontologies (stack overflow)
