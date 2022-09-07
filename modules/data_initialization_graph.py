""" Initialization of node lists """

from modules.logger_config import initialize_logger
from modules.utils_graph import get_list_all_classes, get_list_root_classes, get_list_leaf_classes


def initialize_nodes_lists(ontology_graph):
    """ Return lists of different types of classes (string with the class URI) for the input ontology to be used
        in other functions. This lists of classes must be initializated and, after that, not be edited anymore.
    """
    logger = initialize_logger()
    logger.debug("Initializing list of Ontology nodes...")

    nodes = {"all": get_list_all_classes(ontology_graph),
             "roots": [],
             "leaves": []
             }

    nodes["roots"] = get_list_root_classes(ontology_graph, nodes["all"])
    nodes["leaves"] = get_list_leaf_classes(ontology_graph, nodes["all"])

    logger.debug("List of Ontology concepts successfully initialized.")

    return nodes