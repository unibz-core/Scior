"""Main module for OntCatOWL"""
from modules.data_initialization_ontology import initialize_ontology, initialize_nodes_lists
from modules.dataclass_verifications import verify_all_list_consistency

if __name__ == "__main__":

    from modules.data_initialization_gufo import get_list_of_gufo_types, get_list_of_gufo_individuals
    from modules.logger_module import initialize_logger
    from rdflib import Graph
    import time
    import sys
    from modules.propagation import propagate_graph_top_down

    logger = initialize_logger()

    # TODO (@pedropaulofb): Analyse the size of the ontology first before modifying the system parameter below.
    sys.setrecursionlimit(2000)

    ontology = Graph()

    # TODO (@pedropaulofb): Read from argument
    # Input ontology to be evaluated
    try:
        ontology.parse("resources/d3fend.ttl")
    except OSError:
        logger.error("Could not load resources/d3fend.ttl file. Exiting program.")
        exit(1)

    logger.debug("Initializing list of Ontology concepts.")
    ontology_classes = initialize_ontology(ontology)
    ontology_nodes = initialize_nodes_lists(ontology)

    verify_all_list_consistency(ontology_classes)

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

    ontology_classes[1].create_hash()

    st = time.perf_counter()
    propagate_graph_top_down(ontology, ontology_nodes)
    et = time.perf_counter()
    elapsed_time = round((et - st), 3)
    logger.info(f"Execution time: {elapsed_time} seconds.")

# TODO (@pedropaulofb): Argument -d for printing log file
# TODO (@pedropaulofb): Use different colors for logs levels printed on std.out
#       (e.g. https://betterstack.com/community/questions/how-to-color-python-logging-output/)
# TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions
# TODO (@pedropaulofb): Verify possibility to check consistency using a reasoner.
# TODO (@pedropaulofb): Is there a way to define the GUFO list as read-only?
# TODO (@pedropaulofb): Evaluate on Linux before release first version
# TODO (@pedropaulofb): Update requirements.txt
# TODO (@pedropaulofb): OntCatOWL can became a generic mapper tool!
