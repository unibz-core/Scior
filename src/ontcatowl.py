""" Main module  for OntCatOWL """
import time
from datetime import datetime

from rdflib import RDFS, RDF

from src.modules.dataclass_verifications import verify_all_ontology_dataclasses_consistency
from src.modules.graph_save_ontology import save_ontology_gufo_statements, \
    save_ontology_file_as_configuration
from src.modules.initialization_arguments import treat_arguments
from src.modules.initialization_data_graph import initialize_nodes_lists
from src.modules.initialization_data_gufo_dictionary import initialize_gufo_dictionary
from src.modules.initialization_data_ontology_dataclass import initialize_ontology_dataclasses, \
    load_known_gufo_information
from src.modules.logger_config import initialize_logger
from src.modules.report_printer import print_report_file
from src.modules.results_calculation import generates_partial_statistics_list, calculate_final_statistics
from src.modules.results_printer import print_statistics_screen
from src.modules.rules_types_run import execute_rules_types
from src.modules.utils_rdf import load_all_graph_safely, perform_reasoning, \
    load_graph_safely_considering_restrictions, reduce_graph_considering_restrictions

SOFTWARE_ACRONYM = "OntCatOWL"
SOFTWARE_NAME = "Identification of Ontological Categories for OWL Ontologies"
SOFTWARE_VERSION = "0.22.12.02"
SOFTWARE_URL = "https://github.com/unibz-core/OntCatOWL/"
VERSION_RESTRICTION = "TYPES_ONLY"
LIST_GRAPH_RESTRICTIONS = [RDF.type, RDFS.subClassOf]


def run_ontcatowl():
    """ Main function. """

    # DATA LOADINGS AND INITIALIZATIONS

    st = time.perf_counter()

    global_configurations = treat_arguments(SOFTWARE_ACRONYM, SOFTWARE_NAME, SOFTWARE_VERSION, SOFTWARE_URL)

    logger = initialize_logger()

    now = datetime.now()
    start_date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    logger.info(f"OntCatOWL started on {start_date_time}!")

    # Loading owl ontologies from files to the working memory
    original_graph = load_all_graph_safely(global_configurations["ontology_path"])
    working_graph = reduce_graph_considering_restrictions(original_graph, LIST_GRAPH_RESTRICTIONS)
    gufo_graph = load_graph_safely_considering_restrictions("src/resources/gufoEndurantsOnly.ttl",
                                                            LIST_GRAPH_RESTRICTIONS)

    # Loading GUFO dictionary from yaml file
    gufo_dictionary = initialize_gufo_dictionary()

    if global_configurations["reasoning"]:
        perform_reasoning(working_graph)

    ontology_dataclass_list = initialize_ontology_dataclasses(working_graph, gufo_dictionary)

    verify_all_ontology_dataclasses_consistency(ontology_dataclass_list)

    ontology_nodes = initialize_nodes_lists(working_graph)

    # Loading the GUFO information already known from the ontology
    load_known_gufo_information(working_graph, gufo_graph, ontology_dataclass_list)
    before_statistics = generates_partial_statistics_list(ontology_dataclass_list)

    # EXECUTION

    try:
        time_register = execute_rules_types(ontology_dataclass_list, working_graph, ontology_nodes,
                                            global_configurations)
    except Exception:
        exit(1)

    # SAVING RESULTS - OUTPUT

    after_statistics = generates_partial_statistics_list(ontology_dataclass_list)
    resulting_graph = save_ontology_gufo_statements(ontology_dataclass_list, original_graph, VERSION_RESTRICTION)

    # In this version of OntCatOWL, only types are executed and, hence, only them should be printed/reported.
    consolidated_statistics = calculate_final_statistics(before_statistics, after_statistics)
    print_statistics_screen(ontology_dataclass_list, consolidated_statistics, time_register, global_configurations,
                            VERSION_RESTRICTION)

    now = datetime.now()
    end_date_time_here = now.strftime("%d-%m-%Y %H:%M:%S")
    end_date_time = now.strftime("%Y.%m.%d-%H.%M.%S")
    et = time.perf_counter()
    elapsed_time = round((et - st), 3)
    logger.info(f"OntCatOWL concluded on {end_date_time_here}! Total execution time: {elapsed_time} seconds.")

    save_ontology_file_as_configuration(resulting_graph, gufo_graph, end_date_time, global_configurations)

    print_report_file(ontology_dataclass_list, start_date_time, end_date_time_here, end_date_time, elapsed_time,
                      global_configurations, before_statistics, after_statistics,
                      consolidated_statistics, time_register, VERSION_RESTRICTION)


if __name__ == "__main__":
    run_ontcatowl()
