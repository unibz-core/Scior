"""Main module for OntCatOWL"""
from modules.data_initialization_ontology import get_list_of_classes
from modules.test.test_functions import print_list_file

if __name__ == "__main__":

    import logging
    from rdflib import Graph, Namespace
    from modules.data_initialization_gufo import get_list_of_gufo_types, get_list_of_gufo_individuals

    # TODO (@pedropaulofb): Set base level for printing log
    #   e.g., only print if called with -d parameter (debug)
    #   e.g., print debut only to file
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

    ontology_classes = get_list_of_classes(ontology)
    print_list_file(ontology_classes)

    # ontology_classes = initialize_ontology(ontology)
    # TODO (@pedropaulofb): The ontology may already contain relations with GUFO. Treat that.

    # logging.debug("Initializing RDFS reasoning. This may take a while...")
    # st = time.time()
    # DeductiveClosure(RDFS_Semantics).expand(ontology)  # Performs RDFS inferences
    # et = time.time()
    # elapsed_time = round((et - st), 2)
    # logging.debug(f"Reasoning process completed in {elapsed_time} seconds.")

    logging.debug("Initializing list of GUFO concepts.")
    gufo_types = get_list_of_gufo_types()
    gufo_individuals = get_list_of_gufo_individuals()

# TODO (@pedropaulofb): Create log file parallel to logs printed on std.out
#       (e.g., https://github.com/borntyping/jsonlog)
# TODO (@pedropaulofb): Use different colors for logs levels printed on std.out
#       (e.g. https://betterstack.com/community/questions/how-to-color-python-logging-output/)
# TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions
# TODO (@pedropaulofb): Verify possibility to check consistency using a reasoner.
# TODO (@pedropaulofb): Evaluate on Linux before release first version
# TODO (@pedropaulofb): Update requirements.txt
# TODO (@pedropaulofb): OntCatOWL can became a generic mapper tool!
