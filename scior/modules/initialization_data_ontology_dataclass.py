""" Module for initializing data read from the ontology to be evaluated """
import copy

from scior.modules.dataclass_definitions_ontology import OntologyDataClass
from scior.modules.logger_config import initialize_logger
from scior.modules.utils_rdf import get_list_of_all_classes


def initialize_ontology_dataclasses(ontology_graph, SCOPE_RESTRICTION: str) -> list:
    """
    Receives the ontology graph (taxonomy only) and the gUFO scope to be considered.
    Returns an OntologyClass list of all classes in the ontology to be evaluated with its related sub-lists. """

    logger = initialize_logger()
    logger.debug("Initializing list of Ontology concepts...")

    ontology_list = []
    classes_list = get_list_of_all_classes_no_gufo(ontology_graph)

    gufo_can_list_types, gufo_can_list_individuals = get_gufo_possibilities(SCOPE_RESTRICTION)

    incompleteness_dict = {"is_incomplete": False, "detected_in": []}

    # - URI: Ontology class name
    # - CAN_TYPE and CAN_INDIVIDUAL: list of all possible ontological categories. Receive VALUES (not a pointer)
    # loaded from the gufo_data.yaml file because the data needs to be manipulated.
    # - OTHER LISTS (IS and NOT): Empty lists. No value received.

    for new_class in classes_list:
        new_incompleteness_dict = copy.deepcopy(incompleteness_dict)
        ontology_list.append(OntologyDataClass(uri=new_class,
                                               can_type=gufo_can_list_types.copy(),
                                               can_individual=gufo_can_list_individuals.copy(),
                                               incompleteness_info=new_incompleteness_dict))

    logger.debug("List of Ontology concepts successfully initialized.")
    return ontology_list


def get_list_of_all_classes_no_gufo(ontology_graph):
    """ Returns a list of all classes *that are not GUFO classes* as URI strings without
    repetitions available in a Graph. """

    list_exceptions = ["http://purl.org/nemo/gufo"]

    classes_list_no_gufo = get_list_of_all_classes(ontology_graph, list_exceptions)

    return classes_list_no_gufo


def get_gufo_possibilities(scope_restriction):
    """ Returns list of all GUFO classes available for classification in two lists (for types and individuals). """

    logger = initialize_logger()

    can_list_types = []
    can_list_individuals = []

    gufo_endurant_types = [
        "AntiRigidType",
        "Category",
        "EndurantType",
        "Kind",
        "Mixin",
        "NonRigidType",
        "NonSortal",
        "Phase",
        "PhaseMixin",
        "RigidType",
        "Role",
        "RoleMixin",
        "SemiRigidType",
        "Sortal",
        "SubKind"
    ]

    if scope_restriction == "ENDURANT_TYPES":
        can_list_types = gufo_endurant_types
    else:
        logger.error(f"Invalid SCOPE_RESTRICTION {scope_restriction}. Program aborted.")
        exit(1)

    return can_list_types, can_list_individuals


def get_known_gufo_types(ontology_graph):
    """ For each class in the ontology_graph, return all its known GUFO TYPES in a tuple format.
    Returned tuple format is: (ontology_class,gufo_type), being both fields strings.
    Analogous to get_known_gufo_individuals.
    """

    list_elements = []
    list_types = []

    query_string = """
    PREFIX gufo: <http://purl.org/nemo/gufo#>
    SELECT DISTINCT ?ontology_element ?element_type
    WHERE {
        ?ontology_element rdf:type owl:Class .
        ?ontology_element rdf:type ?element_type .
        FILTER(STRSTARTS(STR(?element_type), STR(gufo:)))
    } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        list_elements.append(row.ontology_element.n3()[1:-1])
        list_types.append(row.element_type.n3()[1:-1].replace("http://purl.org/nemo/gufo#", ""))

    list_tuples = list(zip(list_elements, list_types))

    return list_tuples


# Not used. Not tested yet. Requires implementation of new value of SCOPE_RESTRICTION.
def get_known_gufo_individuals(united_graph):
    """ For each class in the ontology_graph, return all its known GUFO INDIVIDUALS in a tuple format.
    Returned tuple format is: (ontology_class,gufo_type), being both fields strings.
    Analogous to get_known_gufo_types.
    """

    list_elements = []
    list_individuals = []

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?ontology_element ?element_type
        WHERE {
            ?ontology_element rdf:type owl:Class .
            ?element_type rdf:type owl:Class .
            ?ontology_element rdfs:subClassOf ?element_type .
            ?element_type rdfs:subClassOf+ gufo:Endurant .
            FILTER(STRSTARTS(STR(?element_type), STR(gufo:)))
        } """

    query_result = united_graph.query(query_string)

    for row in query_result:
        list_elements.append(row.ontology_element.n3()[1:-1])
        list_individuals.append(row.element_type.n3()[1:-1].replace("http://purl.org/nemo/gufo#", ""))

    list_tuples = list(zip(list_elements, list_individuals))

    return list_tuples


def insert_known_gufo_information(list_known_gufo, ontology_dataclass_list):
    """ Receives a list of known gUFO information and performs the necessary movements of elements in the
    ontology_dataclass_list.
    list_known_gufo is a list of tuples containing (i) ontology class full URI, (ii) short gufo stereotype (e.g. Kind).
    """

    for ontology_dataclass in ontology_dataclass_list:
        for known_gufo in list_known_gufo:
            if known_gufo[0] == ontology_dataclass.uri:
                ontology_dataclass.move_element_to_is_list(known_gufo[1])


def load_known_gufo_information(ontology_graph, ontology_dataclass_list, restriction):
    """ Reads gUFO information about types and instances that are available in the inputted ontology file.

    I.e., if a class is already known to have any GUFO type, this information is updated in the ontology_dataclass_list.
    E.g., if the class Person is set as a gufo:Kind in the loaded ontology, this stereotype is moved from the
    dataclass's can_type (default) list to its is_type list.
    """

    logger = initialize_logger()

    if restriction == "ENDURANT_TYPES":
        # Setting all classes as EndurantType
        for ontology_dataclass in ontology_dataclass_list:
            ontology_dataclass.move_element_to_is_list("EndurantType")
        # Collecting and adding other known classifications
        list_known_gufo = get_known_gufo_types(ontology_graph)
        insert_known_gufo_information(list_known_gufo, ontology_dataclass_list)
    else:
        # function get_known_gufo_individuals implemented but not used or tested
        logger.error(f"Invalid SCOPE_RESTRICTION {restriction}. Program aborted.")
        exit(1)
