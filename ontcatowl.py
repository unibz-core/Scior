""" Main module  for OntCatOWL """

import time
from datetime import datetime

from rdflib import Graph

from modules.dataclass_verifications import verify_all_ontology_dataclasses_consistency
from modules.graph_save_ontology import save_ontology_file, save_ontology_gufo_statements
from modules.initialization_arguments import treat_arguments
from modules.initialization_data_graph import initialize_nodes_lists
from modules.initialization_data_gufo import initialize_gufo_dictionary
from modules.initialization_data_ontology_dataclass import initialize_ontology_dataclasses
from modules.logger_config import initialize_logger
from modules.report_printer import print_report_file
from modules.rules_types_run import execute_rules_types

if __name__ == "__main__":

    SOFTWARE_VERSION = "OntCatOWL version 0.1"

    # DATA LOADINGS AND INITIALIZATIONS

    configuration = treat_arguments(SOFTWARE_VERSION)
    print(configuration)
    exit(1)

    # Logger initialization
    logger = initialize_logger()

    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"OntCatOWL started on {date_time}!")

    # Input ontology_graph to be evaluated
    graph_file = "resources/d3fend.ttl"
    ontology_graph = Graph()
    try:
        ontology_graph.parse(graph_file)
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
        if ont_dataclass.uri == "http://d3fend.mitre.org/ontologies/d3fend.owl#Root2":
            break

    ont_dataclass.move_element_to_is_list("gufo:Mixin")

    stile = "all"

    ############################## END TESTS

    execute_rules_types(ontology_dataclass_list, ontology_graph, ontology_nodes, stile)
    ontology_graph = save_ontology_gufo_statements(ontology_dataclass_list, ontology_graph)
    save_ontology_file(ontology_graph)
    print_report_file(ontology_dataclass_list, ontology_nodes)

    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"OntCatOWL concluded on {date_time}!")

# TODO (@pedropaulofb): Use argparse module for loading arguments
# TODO (@pedropaulofb): Currently reasoning cannot be done after the initialization (e.g., after the rules exec).
# TODO (@pedropaulofb): Read input ontology from user"s argument
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
# TODO (@pedropaulofb): It must be possible to print in a file the current state of the ontology during interactions
#   with the user, so he can open and evaluate the current status of the ontology.
# TODO (@pedropaulofb): Also, the user must be able to add other information whenever he/she considers necessary.
# TODO (@pedropaulofb): Add option to skip interactive rule iteration (to add other processing first).
# TODO (@pedropaulofb): Ordinate all lists that are exhibited to the user.
# TODO (@pedropaulofb): Run automatic only for some different configurations and figure out which is the best order
#  for executing the rules.
# TODO (@pedropaulofb): Verify inclusion of menus:
#  https://pypi.org/project/simple-term-menu/ or https://python-inquirer.readthedocs.io/en/latest/
# TODO (@pedropaulofb): Verify https://github.com/chriskiehl/Gooey
