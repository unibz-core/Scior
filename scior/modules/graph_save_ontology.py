""" Functions related to reading and writing OWL files using RDFLib. """
import os

from rdflib import URIRef, RDF, RDFS, OWL, BNode

from scior.modules.logger_config import initialize_logger
from scior.modules.utils_rdf import get_ontology_uri


def save_ontology_gufo_statements(dataclass_list, ontology_graph, restriction):
    """ Receives the list of dataclasses and use its information for creating new statements in the ontology graph.
    Returns an updated ontology graph.


    Restriction can be: TYPES_ONLY, INDIVIDUALS_ONLY, TOTAL

    """
    ontology_graph.bind("gufo", "http://purl.org/nemo/gufo#")

    if restriction == "TOTAL" or restriction == "TYPES_ONLY":
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


def save_ontology_file_as_configuration(ontology_graph, gufo_graph, end_date_time, global_configurations):
    """Prints in a file the output ontology according to the related configuration, which can be:
    global_configurations["save_gufo"] = True
    global_configurations["import_gufo"] = True
    global_configurations["save_gufo"] = False && global_configurations["import_gufo"] = False
    """

    if global_configurations["save_gufo"]:
        graph = ontology_graph + gufo_graph
    else:
        graph = ontology_graph

    if global_configurations["import_gufo"]:
        ontology_uri = get_ontology_uri(ontology_graph)
        gufo_import = URIRef("https://purl.org/nemo/gufo#")
        graph.add((ontology_uri, OWL.imports, gufo_import))

    save_ontology_file_caller(end_date_time, graph, global_configurations)


def save_ontology_file_caller(end_date_time, ontology_graph, configurations):
    """
    Saves the ontology graph into a TTL file.
    If import_gufo parameter is set as True, the saved output is going to import the GUFO ontology.
    """

    # Creating report file
    output_file_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    output_file_name = output_file_path + "\\" + \
                       os.path.splitext(configurations["ontology_path"])[0] + \
                       "-" + end_date_time + ".out.ttl"

    safe_save_ontology_file(ontology_graph, output_file_name)


def safe_save_ontology_file(ontology_graph, output_file_name: str, syntax: str = 'turtle'):
    """ Safely saves the ontology graph into a TTL file in the informed destination. """

    logger = initialize_logger()
    logger.debug("Saving the output ontology file...")

    try:
        ontology_graph.serialize(destination=output_file_name, encoding='utf-8', format=syntax)
        logger.info(f"Output ontology file saved. Access it in {os.path.abspath(output_file_name)}.")
    except OSError as error:
        logger.error(f"Could not save the output ontology file ({output_file_name}). Exiting program."
                     f"System error reported: {error}")
        exit(1)


def treat_name(gufo_short_name: str) -> str:
    """
    Receives a short gUFO classification string (e.g., 'Kind') and
    returns a full GUFO URI string (e.g., http://purl.org/nemo/gufo#Kind).
    """

    gufo_url = "http://purl.org/nemo/gufo#"
    return gufo_url + gufo_short_name
