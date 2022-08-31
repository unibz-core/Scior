""" Auxiliary functions for extending and complementing RDFLib's RDF treatment functions """
from rdflib import URIRef, RDFS, RDF

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


def insert_new_element_type_hierarchy(ontology_graph, class_name, gufo_type):
    """ Allows user to manually insert a triple into the ontology for verifying its effects """

    logger = initialize_logger()
    logger.debug(f"Inserting the following triple into the ontology: "
                 f"{class_name} rdf:type {gufo_type} ...")

    subject_uri = URIRef(class_name)
    ontology_graph.add((subject_uri, RDF.type, gufo_type))

    logger.debug(f"The following triple was successfully inserted into the ontology: "
                 f"{class_name} rdf:type {gufo_type}.")

    return ontology_graph


def insert_new_element_individual_hierarchy(ontology_graph, class_name, gufo_individual):
    """ Allows user to manually insert a triple into the ontology for verifying its effects """

    logger = initialize_logger()
    logger.debug(f"Inserting the following triple into the ontology: "
                 f"{class_name} rdfs:subClassOf {gufo_individual} ...")

    subject_uri = URIRef(class_name)
    ontology_graph.add((subject_uri, RDFS.subClassOf, gufo_individual))

    logger.debug(f"The following triple was successfully inserted into the ontology: "
                 f"{class_name} rdfs:subClassOf {gufo_individual}.")

    return ontology_graph
