"""Main module for OntCatOWL

Arguments: TO BE IMPLEMENTED

-1: suggest all modifications that are identified
-2: suggestions and enforcements according to the rule types (DEFAULT)
-3: enforce all modifications that are identified

-s (same as -1):
-e (same as -3):

"""

import time
from datetime import datetime

from rdflib import Graph

from modules.data_initialization_gufo import initialize_gufo_dictionary
from modules.data_initialization_ontology import initialize_ontology, initialize_nodes_lists
from modules.dataclass_verifications import verify_all_ontology_dataclasses_consistency
from modules.logger_config import initialize_logger
from modules.report_printer import print_report_file
from modules.rules_hierarchy_types import execute_rules_gufo_type
from modules.utils_general import update_all_ontology_dataclass_list

if __name__ == "__main__":

    ### DATA LOADINGS AND INITIALIZATIONS

    # Logger initialization
    logger = initialize_logger()

    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"OntCatOWL started on {date_time}!")

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

    ontology_dataclass_list = initialize_ontology(ontology_graph, gufo_dictionary)
    ontology_nodes = initialize_nodes_lists(ontology_graph)

    verify_all_ontology_dataclasses_consistency(ontology_dataclass_list)

    ############################## BEGIN TESTS

    num = 0
    for num in range(len(ontology_dataclass_list)):
        if ontology_dataclass_list[num].uri == "http://d3fend.mitre.org/ontologies/d3fend.owl#PedroPaulo-A":
            break

    ontology_dataclass_list[num].move_element_to_is_list("gufo:Kind")
    ontology_dataclass_list[num].update_all_internal_lists_from_gufo(gufo_dictionary)

    execute_rules_gufo_type(ontology_dataclass_list, ontology_graph, ontology_nodes)

    update_all_ontology_dataclass_list(ontology_dataclass_list, gufo_dictionary)

    print_report_file(ontology_dataclass_list)

    ############################## END TESTS

    now = datetime.now()
    logger.info(f"OntCatOWL concluded on {date_time}!")

# TODO (@pedropaulofb): Read input ontology from user's argument
# TODO (@pedropaulofb): The ontology_graph may already contain relations with GUFO. Treat that.
# TODO (@pedropaulofb): Argument -t for saving functions'execution times in log
# TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions
# TODO (@pedropaulofb): Verify possibility to check consistency using a reasoner.
# TODO (@pedropaulofb): Instead of using exit(1) for all problems, identify which ones can generate a warning instead.
# TODO (@pedropaulofb): Is there a way to define the GUFO list as read-only?
# TODO (@pedropaulofb): Verify if there is any unused module, function or method
# TODO (@pedropaulofb): Evaluate on Linux before release first version
# TODO (@pedropaulofb): Update requirements.txt
# TODO (@pedropaulofb): Treat problem with huge ontologies (stack overflow)
# TODO (@pedropaulofb): Verify "dataclass with slots" and the use of __slot__ for better performance.
