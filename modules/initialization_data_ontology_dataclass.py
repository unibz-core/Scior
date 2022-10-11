""" Module for initializing data read from the ontology to be evaluated """

from rdflib import RDF, OWL

from modules.dataclass_definitions_ontology import OntologyDataClass
from modules.logger_config import initialize_logger


def initialize_ontology_dataclasses(ontology_graph, gufo_input_yaml):
    """ Return an OntologyClass list of all classes in the ontology to be evaluated with its related sub-lists """

    logger = initialize_logger()
    logger.debug("Initializing list of Ontology concepts...")

    ontology_list = []
    classes_list = get_list_of_classes(ontology_graph)
    gufo_can_list_types, gufo_can_list_individuals = get_gufo_possibilities(gufo_input_yaml)

    # - URI: Ontology class name
    # - CAN_TYPE and CAN_INDIVIDUAL: list of all possible ontological categories. Receive VALUES (not a pointer)
    # loaded from the gufo_data.yaml file because the data needs to be manipulated.
    # - OTHER LISTS (IS and NOT): Empty lists. No value received.
    # - GUFO DICTIONARY: Receives a POINTER (not values) to the dictionary loaded from the gufo_data.yaml file.
    # It is used inside the dataclass for updating the other lists. The information is read-only.
    for new_class in classes_list:
        ontology_list.append(OntologyDataClass(uri=new_class,
                                               can_type=gufo_can_list_types.copy(),
                                               can_individual=gufo_can_list_individuals.copy(),
                                               gufo_dictionary=gufo_input_yaml))

    logger.debug("List of Ontology concepts successfully initialized.")
    return ontology_list


def get_list_of_classes(ontology_graph):
    """ Returns a list of all classes as URI strings without repetitions available in a Graph """

    classes_list = []

    for sub, pred, obj in ontology_graph:
        if (sub, RDF.type, OWL.Class) in ontology_graph:
            # N3 necessary for returning string and [1:-1] necessary for removing <>
            classes_list.append(sub.n3()[1:-1])
        if (obj, RDF.type, OWL.Class) in ontology_graph:
            # N3 necessary for returning string and [1:-1] necessary for removing <>
            classes_list.append(obj.n3()[1:-1])

    # Removing repetitions
    classes_list = [*set(classes_list)]

    return classes_list


def get_gufo_possibilities(gufo_input_yaml):
    """ Returns list of all GUFO classes available for classification in two lists (for types and individuals).
        The data is loaded from the gufo dictionary obtained from the GUFO YAML file. """

    can_list_types = list(gufo_input_yaml["types"].keys())
    can_list_individuals = list(gufo_input_yaml["individuals"].keys())

    return can_list_types, can_list_individuals
