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

SOFTWARE_VERSION = "OntCatOWL - Identification of Ontological Categories for OWL Ontologies\n" \
                   "Version 0.20221011 - https://github.com/unibz-core/OntCatOWL/\n"

if __name__ == "__main__":

    # DATA LOADINGS AND INITIALIZATIONS

    global_configurations = treat_arguments(SOFTWARE_VERSION)

    # Logger initialization
    logger = initialize_logger()

    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"OntCatOWL started on {date_time}!")

    # Input ontology_graph to be evaluated
    ontology_graph = Graph()
    try:
        ontology_graph.parse(global_configurations["ontology_path"])
    except OSError:
        logger.error(f"Could not load {global_configurations['ontology_path']} file. Exiting program.")
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
        if ont_dataclass.uri == "http://d3fend.mitre.org/ontologies/d3fend.owl#AA":
            ont_dataclass.move_element_to_is_list("gufo:Sortal")

############################## END TESTS

execute_rules_types(ontology_dataclass_list, ontology_graph, ontology_nodes, global_configurations)
ontology_graph = save_ontology_gufo_statements(ontology_dataclass_list, ontology_graph)
save_ontology_file(ontology_graph, global_configurations)
print_report_file(ontology_dataclass_list, ontology_nodes)

now = datetime.now()
date_time = now.strftime("%d-%m-%Y %H:%M:%S")
logger.info(f"OntCatOWL concluded on {date_time}!")

# TODO (@pedropaulofb): IMPROVEMENTS
# Verify possibility to check consistency using a reasoner.
# Currently reasoning cannot be done after the initialization (e.g., after the rules exec).
# The ontology_graph may already contain relations with GUFO. Treat that.
# Instead of using exit(1) for all problems, identify which ones can generate a warning instead.
# Present to user all different namespaces of different classes found and ask him in which ones he wants to execute.
# Create a (much) better deficiency (incompleteness)(inconsistency?) report.

# TODO (@pedropaulofb): USER INTERACTIONS
# Ordinate all lists that are exhibited to the user.
# Create menus for better user interactions: https://pypi.org/project/simple-term-menu/

# TODO (@pedropaulofb): PERFORMANCE
# Treat problem with huge ontologies (stack overflow)
# Verify "dataclass with slots" and the use of __slot__ for better performance.
# As log files are getting big, maybe it is going to be necessary to compact them into a zip file.
# Run automatic only for some different configurations and figure out which is the best order for executing the rules.
# Insert "break" after moving commands (name == class.uri) because there are no repetitions. Verify for/break statement

# TODO (@pedropaulofb): BEFORE RELEASE OF VERSION 1.0
# Evaluate on Linux before release first version
# Update requirements.txt
# Verify if there is any unused module, function or methods
