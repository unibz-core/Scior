"""Main module for OntCatOWL"""

import time

from rdflib import Graph

from modules.data_initialization_gufo import get_list_of_gufo_types, get_list_of_gufo_individuals
from modules.data_initialization_gufo2 import initialize_gufo_dictionary
from modules.data_initialization_ontology import initialize_ontology, initialize_nodes_lists
from modules.dataclass_verifications import verify_all_list_consistency
from modules.logger_config import initialize_logger
from modules.propagation import propagate_graph_top_down

if __name__ == "__main__":

    logger = initialize_logger()

    ontology = Graph()

    # TODO (@pedropaulofb): Read from argument
    # Input ontology to be evaluated
    try:
        ontology.parse("resources/d3fend.ttl")
    except OSError:
        logger.error("Could not load resources/d3fend.ttl file. Exiting program.")
        exit(1)

    logger.debug("Initializing list of Ontology concepts.")
    ontology_data = initialize_ontology(ontology)
    ontology_nodes = initialize_nodes_lists(ontology)

    verify_all_list_consistency(ontology_data)

    gufo_data = initialize_gufo_dictionary()

    # TODO (@pedropaulofb): The ontology may already contain relations with GUFO. Treat that.

    # # logger.debug("Initializing RDFS reasoning. This may take a while...")
    # st = time.perf_counter()
    # DeductiveClosure(RDFS_Semantics).expand(ontology)  # Performs RDFS inferences
    # et = time.perf_counter()
    # elapsed_time = round((et - st), 3)
    # logger.debug(f"Reasoning process completed in {elapsed_time} seconds.")

    logger.debug("Initializing list of GUFO concepts.")
    gufo_types = get_list_of_gufo_types()
    gufo_individuals = get_list_of_gufo_individuals()

    ontology_data[1].create_hash()

    st = time.perf_counter()
    propagate_graph_top_down(ontology, ontology_nodes)
    et = time.perf_counter()
    elapsed_time = round((et - st), 3)
    logger.info(f"Execution time: {elapsed_time} seconds.")

# TODO (@pedropaulofb): Argument -d for printing log file
# TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions
# TODO (@pedropaulofb): Verify possibility to check consistency using a reasoner.
# TODO (@pedropaulofb): Is there a way to define the GUFO list as read-only?
# TODO (@pedropaulofb): Evaluate on Linux before release first version
# TODO (@pedropaulofb): Update requirements.txt
# TODO (@pedropaulofb): OntCatOWL can became a generic mapper tool!
# TODO (@pedropaulofb): Treat problem with huge ontologies (stack overflow)
