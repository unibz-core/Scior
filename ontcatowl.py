"""Main module  for OntCatOWL

Arguments: TO BE IMPLEMENTED

-m: ask for user confirmation before any modifications
-n: do not ask for user confirmation before any modifications (DEFAULT)

-i: when inconsistencies are found, treat them
-x: when inconsistencies are found, inform user and exit program (DEFAULT)

-c: allows possibility to reclassificate classes.

-a: run only automatic rules
-m: run automatic and interactive rules (DEFAULT)

-j: prints to user justification for every classification performed
-t: prints to user the execution times of all functions
-v: verbose mode (same as -jt)

-s: print options (j|t|v) in the console (DEFAULT)
-l: print options (j|t|v) in the log file

"""

import time
from datetime import datetime

from rdflib import Graph

from modules.data_initialization_graph import initialize_nodes_lists
from modules.data_initialization_gufo import initialize_gufo_dictionary
from modules.data_initialization_ontology_dataclass import initialize_ontology_dataclasses
from modules.dataclass_verifications import verify_all_ontology_dataclasses_consistency
from modules.logger_config import initialize_logger
from modules.report_printer import print_report_file
from modules.rules_types_run import execute_rules_types

if __name__ == "__main__":

    # DATA LOADINGS AND INITIALIZATIONS

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
    elapsed_time = round((et - st), 4)
    logger.info(f"Reasoning process completed in {elapsed_time} seconds.")

    ontology_dataclass_list = initialize_ontology_dataclasses(ontology_graph, gufo_dictionary)
    ontology_nodes = initialize_nodes_lists(ontology_graph)

    verify_all_ontology_dataclasses_consistency(ontology_dataclass_list)

    ############################## BEGIN TESTS

    for ont_dataclass in ontology_dataclass_list:
        if ont_dataclass.uri == "http://d3fend.mitre.org/ontologies/d3fend.owl#ATTACKMitigation":
            break

    ont_dataclass.move_element_to_is_list("gufo:SubKind")

    stile = "a"

    execute_rules_types(ontology_dataclass_list, ontology_graph, ontology_nodes, stile)

    print_report_file(ontology_dataclass_list, ontology_nodes)

    ############################## END TESTS

    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"OntCatOWL concluded on {date_time}!")

# TODO (@pedropaulofb): Currently reasoning cannot be done after the initialization (e.g., after the rules exec).
# TODO (@pedropaulofb): Read input ontology from user's argument
# TODO (@pedropaulofb): The ontology_graph may already contain relations with GUFO. Treat that.
# TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions
# TODO (@pedropaulofb): Verify possibility to check consistency using a reasoner.
# TODO (@pedropaulofb): Instead of using exit(1) for all problems, identify which ones can generate a warning instead.
# TODO (@pedropaulofb): Is there a way to define the GUFO list as read-only?
# TODO (@pedropaulofb): Verify if there is any unused module, function or method
# TODO (@pedropaulofb): Evaluate on Linux before release first version
# TODO (@pedropaulofb): Update requirements.txt
# TODO (@pedropaulofb): Treat problem with huge ontologies (stack overflow)
# TODO (@pedropaulofb): Verify "dataclass with slots" and the use of __slot__ for better performance.
# TODO (@pedropaulofb): As log files are getting big, maybe it is going to be necessary to compact them into a zip file.
