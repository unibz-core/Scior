""" Functions related to reading and writing OWL files using RDFLib. """
import os
from pathlib import Path

from rdflib import URIRef, RDF, RDFS, OWL, BNode, Graph

from scior.modules.logger_config import initialize_logger
from scior.modules.resources_gufo import GUFO_NAMESPACE
from scior.modules.utils_general import create_directory_if_not_exists
from scior.modules.utils_rdf import get_ontology_uri, load_all_graph_safely

LOGGER = initialize_logger()


def save_ontology_gufo_statements(dataclass_list, ontology_graph, restriction):
    """ Receives the list of dataclasses and use its information for creating new statements in the ontology graph.
    Returns an updated ontology graph.


    Restriction can be: TYPES_ONLY, INDIVIDUALS_ONLY, TOTAL

    """
    ontology_graph.bind("gufo", GUFO_NAMESPACE)

    if restriction == "TOTAL" or restriction == "ENDURANT_TYPES":
        for dataclass in dataclass_list:

            # Hierarchy of Types - positive assertions
            for is_type in dataclass.is_type:
                gufo_treated_name = treat_name(is_type)
                new_type = URIRef(gufo_treated_name)
                class_name = URIRef(dataclass.uri)
                ontology_graph.add((class_name, RDF.type, new_type))

            # # Hierarchy of Types - negative assertions
            for not_type in dataclass.not_type:
                gufo_treated_name_not_type = treat_name(not_type)
                new_gufo_type_not = URIRef(gufo_treated_name_not_type)
                blank_node = BNode()
                class_name_not = URIRef(dataclass.uri)
                ontology_graph.add((class_name_not, RDF.type, blank_node))
                ontology_graph.add((blank_node, OWL.complementOf, new_gufo_type_not))

    if restriction == "TOTAL" or restriction == "INDIVIDUALS_ONLY":
        for dataclass in dataclass_list:

            # Hierarchy of Individuals - positive assertions
            for is_individual in dataclass.is_individual:
                gufo_treated_name_is = treat_name(is_individual)
                new_gufo_individual_is = URIRef(gufo_treated_name_is)
                class_name_is = URIRef(dataclass.uri)
                ontology_graph.add((class_name_is, RDFS.subClassOf, new_gufo_individual_is))

            # Hierarchy of Individuals - negative assertions - NOT TESTED YET!
            for not_individual in dataclass.not_individual:
                gufo_treated_name_not_individual = treat_name(not_individual)
                new_gufo_individual_not = URIRef(gufo_treated_name_not_individual)
                blank_node = BNode()
                class_name_not = URIRef(dataclass.uri)
                ontology_graph.add((class_name_not, RDFS.subClassOf, blank_node))
                ontology_graph.add((blank_node, OWL.complementOf, new_gufo_individual_not))

    return ontology_graph


def save_ontology_file_as_configuration(ontology_graph: Graph, end_date_time, arguments: dict):
    """Prints in a file the output ontology according to the related configuration, which can be:
    """

    # Getting gUFO HTTPS information instead of HTTP
    gufo_namespace_http = GUFO_NAMESPACE.replace("http", "https")

    if arguments["gufo_results"]:
        graph = ontology_graph

    elif arguments["import_gufo"]:
        ontology_uri = get_ontology_uri(ontology_graph)
        gufo_import = URIRef(gufo_namespace_http)
        graph = ontology_graph
        graph.add((ontology_uri, OWL.imports, gufo_import))

    elif arguments["gufo_write"]:
        # Loading gUFO file form its remote location
        gufo_graph = load_all_graph_safely(gufo_namespace_http)
        graph = ontology_graph + gufo_graph

    save_ontology_file_caller(end_date_time, graph, arguments)


def save_ontology_file_caller(end_date_time, ontology_graph, arguments: dict):
    """
    Saves the ontology graph into a TTL file.
    If import_gufo parameter is set as True, the saved output is going to import the GUFO ontology.
    """

    # Collecting information for result file name and path
    project_directory = os.getcwd()
    results_directory = "results"
    loaded_file_name = Path(arguments['ontology_path']).stem

    # If directory 'results_directory' not exists, create it
    create_directory_if_not_exists(results_directory)

    # Setting file complete path
    output_file_name = loaded_file_name + "-" + end_date_time + ".ttl"
    output_file_path = project_directory + "\\" + results_directory + "\\" + output_file_name

    safe_save_ontology_file(ontology_graph, output_file_path)


def safe_save_ontology_file(ontology_graph, output_file_name: str, syntax: str = 'turtle'):
    """ Safely saves the ontology graph into a TTL file in the informed destination. """

    LOGGER.debug("Saving the output ontology file...")

    try:
        ontology_graph.serialize(destination=output_file_name, encoding='utf-8', format=syntax)
        LOGGER.info(f"Output ontology file saved. Access it in {os.path.abspath(output_file_name)}.")
    except OSError as error:
        LOGGER.error(f"Could not save the output ontology file ({output_file_name}). Exiting program."
                     f"System error reported: {error}")


def treat_name(gufo_short_name: str) -> str:
    """
    Receives a short gUFO classification string (e.g., 'Kind') and
    returns a full GUFO URI string (e.g., http://purl.org/nemo/gufo#Kind).
    """

    gufo_url = GUFO_NAMESPACE
    return gufo_url + gufo_short_name


def update_ontology_graph_with_gufo(ontology_dataclass_list, ontology_graph):
    """ Include all known gUFO classifications (got from ontology_dataclass_list) into the ontology_graph.
        Currently implemented only for Types.
    """

    ontology_graph.bind("gufo", GUFO_NAMESPACE)

    for ontology_class in ontology_dataclass_list:
        for gufo_type in ontology_class.is_type:
            gufo_classification = URIRef(GUFO_NAMESPACE + gufo_type)
            ontology_graph.add((URIRef(ontology_class.uri), RDF.type, gufo_classification))
