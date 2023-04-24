""" Main module for Scior """
import time
from datetime import datetime

from rdflib import RDF, RDFS

import scior.modules.initialization_arguments as args
from scior.modules.graph_ontology import save_ontology_gufo_statements, save_ontology_file_as_configuration
from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_initialization import initialize_ontology_dataclasses, \
    load_known_gufo_information
from scior.modules.report_printer import print_report_file
from scior.modules.results_calculation import generates_partial_statistics_list, calculate_final_statistics, \
    create_knowledge_matrix
from scior.modules.rules.rules_execution import execute_rules_types
from scior.modules.utils_rdf import load_all_graph_safely, reduce_graph_considering_restrictions

SOFTWARE_ACRONYM = "Scior"
SOFTWARE_NAME = "Identification of Ontological Categories for OWL Ontologies"
SOFTWARE_VERSION = "2023.04.23"
SOFTWARE_URL = "https://github.com/unibz-core/Scior/"
SCOPE_RESTRICTION = "ENDURANT_TYPES"
LIST_GRAPH_RESTRICTIONS = [RDF.type, RDFS.subClassOf]


def run_scior():
    """ Main function. """

    # DATA LOADINGS AND INITIALIZATIONS

    st = time.perf_counter()

    args.treat_arguments(SOFTWARE_ACRONYM, SOFTWARE_NAME, SOFTWARE_VERSION, SOFTWARE_URL)

    print(args.ARGUMENTS)
    exit(2)

    logger = initialize_logger("Scior")

    now = datetime.now()
    start_date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"Scior started on {start_date_time}!")

    # Loading OWL ontologies from files to the working memory
    original_graph = load_all_graph_safely(args.ARGUMENTS["ontology_path"])
    working_graph = reduce_graph_considering_restrictions(original_graph, LIST_GRAPH_RESTRICTIONS)

    # Creating empty list of classes and their respective classifications
    ontology_dataclass_list = initialize_ontology_dataclasses(working_graph, SCOPE_RESTRICTION)

    # Loading the gUFO information already stated into the ontology
    load_known_gufo_information(working_graph, ontology_dataclass_list)

    logger.debug("Saving initial data for calculating future statistics.")
    before_statistics = generates_partial_statistics_list(ontology_dataclass_list)

    # EXECUTION

    execute_rules_types(ontology_dataclass_list, working_graph)

    # SAVING RESULTS - OUTPUT

    after_statistics = generates_partial_statistics_list(ontology_dataclass_list)

    resulting_graph = save_ontology_gufo_statements(ontology_dataclass_list, original_graph, SCOPE_RESTRICTION)

    # Calculating results
    consolidated_statistics = calculate_final_statistics(before_statistics, after_statistics)
    knowledge_matrix = create_knowledge_matrix(before_statistics, after_statistics)

    # print_statistics_screen(ontology_dataclass_list, consolidated_statistics, arguments, SCOPE_RESTRICTION)

    now = datetime.now()
    end_date_time_screen = now.strftime("%d-%m-%Y %H:%M:%S")
    end_date_time_files = now.strftime("%Y%m%d-%H%M%S")
    et = time.perf_counter()
    elapsed_time = round((et - st), 3)
    logger.info(f"Scior concluded on {end_date_time_screen}! Total execution time: {elapsed_time} seconds.")

    # Printing results
    save_ontology_file_as_configuration(resulting_graph, end_date_time_files)

    print_report_file(ontology_dataclass_list,
                      start_date_time, end_date_time_files, elapsed_time,
                      before_statistics, after_statistics, consolidated_statistics,
                      SCOPE_RESTRICTION, SOFTWARE_VERSION, knowledge_matrix)


def run_scior_tester(global_configurations, working_graph):
    """ Main function for the Scior-Tester.
        No printings and reports are generated. Logger is differently configured.
        This function is exported at the __init__.py file for being used by the Scior-Tester.
        For more detailed information, please check: https://github.com/unibz-core/Scior-Tester/
    """

    # DATA LOADINGS AND INITIALIZATIONS
    logger = initialize_logger("Scior-Tester")
    ontology_dataclass_list = initialize_ontology_dataclasses(working_graph, SCOPE_RESTRICTION)
    load_known_gufo_information(working_graph, ontology_dataclass_list)

    # EXECUTION
    before_statistics = generates_partial_statistics_list(ontology_dataclass_list)
    execute_rules_types(ontology_dataclass_list, working_graph, global_configurations)
    after_statistics = generates_partial_statistics_list(ontology_dataclass_list)
    consolidated_statistics = calculate_final_statistics(before_statistics, after_statistics)
    knowledge_matrix = create_knowledge_matrix(before_statistics, after_statistics)

    return ontology_dataclass_list, consolidated_statistics, knowledge_matrix, SOFTWARE_VERSION


if __name__ == "__main__":
    run_scior()

# TODO (@pedropaulofb): Implement interactive mode and light automatic.
# TODO (@pedropaulofb): Document SCOPE_RESTRICTION variable
# TODO (@pedropaulofb): Clear unused code. Check PyCharm Analyze or install Vulture.
