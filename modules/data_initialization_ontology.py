""" Module for initializing data read from the ontology to be evaluated """

from rdflib import RDF, OWL

from modules.dataclass_definitions_ontology import OntologyDataClass
from modules.logger_config import initialize_logger
from modules.utils_graph import get_list_all_classes, get_list_root_classes, get_list_leaf_classes


def initialize_ontology(ontology, gufo_dictionary):
    """ Return an OntologyClass list of all classes in the ontology to be evaluated with its related sub-lists """

    logger = initialize_logger()
    logger.debug("Initializing list of Ontology concepts...")

    ontology_list = []
    classes_list = get_list_of_classes(ontology)
    gufo_can_list_types, gufo_can_list_individuals = get_gufo_possibilities(gufo_dictionary)

    for i in range(len(classes_list)):
        ontology_list.append(OntologyDataClass(uri=classes_list[i],
                                               can_type=gufo_can_list_types.copy(),
                                               can_individual=gufo_can_list_individuals.copy()))

    logger.debug("List of Ontology concepts successfully initialized.")
    return ontology_list


def get_list_of_classes(ontology):
    """ Returns a list of all classes as URI strings without repetitions available in a Graph """

    classes_list = []

    for sub, pred, obj in ontology:
        if (sub, RDF.type, OWL.Class) in ontology:
            # N3 necessary for returning string and [1:-1] necessary for removing <>
            classes_list.append(sub.n3()[1:-1])
        if (obj, RDF.type, OWL.Class) in ontology:
            # N3 necessary for returning string and [1:-1] necessary for removing <>
            classes_list.append(obj.n3()[1:-1])

    # Removing repetitions
    classes_list = [*set(classes_list)]

    return classes_list


def get_gufo_possibilities(gufo_dictionary):
    """ Returns list of all GUFO classes available for classification in two lists (for types and individuals).
        The data is loaded from the gufo dictionary obtained from the GUFO YAML file. """

    can_list_types = list(gufo_dictionary["types"].keys())
    can_list_individuals = list(gufo_dictionary["individuals"].keys())

    return can_list_types, can_list_individuals


def initialize_nodes_lists(ontology):
    """ Return lists of different types of classes (string with the class URI) for the input ontology to be used
        in other functions. This lists of classes must be initializated and, after that, not be edited anymore.
    """
    logger = initialize_logger()
    logger.debug("Initializing list of Ontology nodes...")

    nodes = {"all": get_list_all_classes(ontology),
             "roots": [],
             "leaves": []
             }

    nodes["roots"] = get_list_root_classes(ontology, nodes["all"])
    nodes["leaves"] = get_list_leaf_classes(ontology, nodes["all"])

    logger.debug("List of Ontology concepts successfully initialized.")

    return nodes
