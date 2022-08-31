""" Auxiliary functions for extending and complementing RDFLib's RDF treatment functions """
from rdflib import URIRef, RDF

from modules.logger_config import initialize_logger


def has_prefix(graph, prefix):
    """ Return boolean indicating if the argument prefix exists in the graph"""
    result = False

    for pre, nam in graph.namespaces():
        if prefix == pre:
            result = True

    return result


def has_namespace(graph, namespace):
    """ Return boolean indicating if the argument namespace exists in the graph.
        The argument namespace must be provided without the surrounding <>"""
    result = False

    for pre, nam in graph.namespaces():
        if namespace == nam.n3()[1:-1]:
            result = True

    return result


def list_prefixes(graph):
    """ Return a list of all prefixes in the graph"""
    result = []

    for pre, nam in graph.namespaces():
        result.append(pre)

    return result


def list_namespaces(graph):
    """ Return a list of all namespaces in the graph without the surrounding <>"""
    result = []

    for pre, nam in graph.namespaces():
        # N3 necessary for returning string and [1:-1] necessary for removing <>
        result.append(nam.n3()[1:-1])

    return result


# TODO (@pedropaulofb): The input gufo_type_short must still be treated!
def insert_new_element_type_hierarchy(ontology_graph, class_name, gufo_type_short):
    """ Allows user to manually insert a triple into the ontology for verifying its effects """

    gufo_base_prefix = "http://purl.org/nemo/gufo#"
    gufo_type = gufo_base_prefix + gufo_type_short

    logger = initialize_logger()

    logger.debug(f"Inserting the following triple into the ontology: "
                 f"{class_name} rdf:type {gufo_type} ...")

    subject_uri = URIRef(class_name)
    object_uri = URIRef(gufo_type)

    ontology_graph.add((subject_uri, RDF.type, object_uri))

    logger.debug(f"The following triple was successfully inserted into the ontology: "
                 f"{class_name} rdf:type {gufo_type}.")

    return ontology_graph
