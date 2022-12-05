""" Initialization of node lists """
from src.modules.initialization_data_ontology_dataclass import get_list_of_all_classes_no_gufo
from src.modules.logger_config import initialize_logger
from src.modules.utils_graph import get_list_root_classes, get_list_leaf_classes


def initialize_nodes_lists(ontology_graph):
    """ Return lists of different types of classes (string with the class URI) for the ontologies ontology to be used
        in other functions. This lists of classes must be initializated and, after that, not be edited anymore.
    """
    logger = initialize_logger()
    logger.debug("Initializing list of Ontology nodes...")

    nodes = {"all": [], "roots": [], "leaves": []}

    nodes["all"] = get_list_of_all_classes_no_gufo(ontology_graph)
    nodes["roots"] = get_list_root_classes(ontology_graph, nodes["all"])
    nodes["leaves"] = get_list_leaf_classes(ontology_graph, nodes["all"])

    logger.debug("List of Ontology concepts successfully initialized.")

    return nodes
