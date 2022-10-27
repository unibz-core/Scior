""" Main module  for OntCatOWL """
from datetime import datetime

from modules.dataclass_verifications import verify_all_ontology_dataclasses_consistency
from modules.graph_save_ontology import save_ontology_file, save_ontology_gufo_statements
from modules.initialization_arguments import treat_arguments
from modules.initialization_data_graph import initialize_nodes_lists
from modules.initialization_data_gufo_dictionary import initialize_gufo_dictionary
from modules.initialization_data_ontology_dataclass import initialize_ontology_dataclasses, load_known_gufo_information
from modules.logger_config import initialize_logger
from modules.report_printer import print_report_file
from modules.rules_types_run import execute_rules_types
from modules.utils_rdf import load_graph_safely, perform_reasoning

SOFTWARE_VERSION = "OntCatOWL - Identification of Ontological Categories for OWL Ontologies\n" \
                   "Version 0.20221026 - https://github.com/unibz-core/OntCatOWL/\n"

if __name__ == "__main__":
    # DATA LOADINGS AND INITIALIZATIONS

    global_configurations = treat_arguments(SOFTWARE_VERSION)

    # Logger initialization
    logger = initialize_logger()

    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"OntCatOWL started on {date_time}!")

    # Loading owl ontologies from files to the working memory
    ontology_graph = load_graph_safely(global_configurations["ontology_path"])
    gufo_graph = load_graph_safely("resources/gufoEndurantsOnly.ttl")

    if global_configurations["reasoning"]:
        perform_reasoning(ontology_graph)

    gufo_dictionary = initialize_gufo_dictionary()

    ontology_dataclass_list = initialize_ontology_dataclasses(ontology_graph, gufo_dictionary)
    verify_all_ontology_dataclasses_consistency(ontology_dataclass_list)

    ontology_nodes = initialize_nodes_lists(ontology_graph)

    # Loading the GUFO information already known from the ontology and updating the ontology_dataclass_list
    load_known_gufo_information(ontology_graph, gufo_graph, ontology_dataclass_list)

    # ############################## BEGIN TESTS

    for ont_dataclass in ontology_dataclass_list:
        if ont_dataclass.uri == "http://d3fend.mitre.org/ontologies/d3fend.owl#B":
            ont_dataclass.move_element_to_is_list("gufo:Sortal")
            ont_dataclass.move_element_to_is_list("gufo:NonRigidType")
        if ont_dataclass.uri == "http://d3fend.mitre.org/ontologies/d3fend.owl#E":
            ont_dataclass.move_element_to_is_list("gufo:Sortal")
            ont_dataclass.move_element_to_is_list("gufo:NonRigidType")
        if ont_dataclass.uri == "http://d3fend.mitre.org/ontologies/d3fend.owl#H":
            ont_dataclass.move_element_to_is_list("gufo:Sortal")
            ont_dataclass.move_element_to_is_list("gufo:NonRigidType")
        if ont_dataclass.uri == "http://d3fend.mitre.org/ontologies/d3fend.owl#M":
            ont_dataclass.move_element_to_is_list("gufo:Sortal")
            ont_dataclass.move_element_to_is_list("gufo:NonRigidType")

    # ############################## END TESTS

    execute_rules_types(ontology_dataclass_list, ontology_graph, ontology_nodes, global_configurations)

    ontology_graph = save_ontology_gufo_statements(ontology_dataclass_list, ontology_graph)
    if global_configurations["import_gufo"]:
        united_graph = ontology_graph + gufo_graph
        save_ontology_file(ontology_graph, global_configurations)
    else:
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
# Hash is generated differently when list is [A, B] and [B, A]. So maybe is the case to keep it always sorted.
# Create argument for cleaning all generated logs and reports (e.g., ontcatowl.py --clean)

# TODO (@pedropaulofb): USER INTERACTIONS
# Ordinate all lists that are exhibited to the user.
# Create menus for better user interactions: https://pypi.org/project/simple-term-menu/
# Provide option for the user to print report and ontology in every interaction. Do not use an argument.

# TODO (@pedropaulofb): PERFORMANCE
# Treat problem with huge ontologies (stack overflow)
# Verify "dataclass with slots" and the use of __slot__ for better performance.
# As log files are getting big, maybe it is going to be necessary to compact them into a zip file.
# Run automatic only for some different configurations and figure out which is the best order for executing the rules.
# Insert "break" after moving commands (name == class.uri) because there are no repetitions. Verify for/break statement

# TODO (@pedropaulofb): BEFORE RELEASE OF VERSION
# Evaluate on Linux before release first version
# Update requirements.txt
# Verify if there is any unused module, function or methods
# Create release notes file
# Move TO DO comments to GitHub issues
