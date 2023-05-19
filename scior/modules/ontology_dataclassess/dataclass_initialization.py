""" Module for initializing data read from the ontology to be evaluated """
import inspect

from rdflib import Graph

from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.ontology_dataclassess.dataclass_moving import move_classification_to_is_type, \
    move_classification_to_not_type
from scior.modules.problems_treatment.treat_errors import report_error_end_of_switch, report_error_requirement_not_met
from scior.modules.resources_gufo import GUFO_NAMESPACE, GUFO_LIST_ENDURANT_TYPES
from scior.modules.utils_dataclass import get_dataclass_by_uri, sort_all_ontology_dataclass_list
from scior.modules.utils_rdf import get_list_of_all_classes

LOGGER = initialize_logger()


def initialize_ontology_dataclasses(ontology_graph: Graph, scope_restriction: str) -> list[OntologyDataClass]:
    """ Receives the ontology graph (taxonomy only) and the gUFO scope to be considered.
        Returns the ontology_dataclass_list, a list with all classes in the ontology to be evaluated.
    """

    LOGGER.debug("Initializing list of Ontology concepts...")

    ontology_dataclass_list = []
    classes_list = get_list_of_all_classes_no_gufo(ontology_graph)

    gufo_can_list_types, gufo_can_list_individuals = get_gufo_possibilities(scope_restriction)

    # - URI: Ontology class name
    # - CAN_TYPE and CAN_INDIVIDUAL: list of all possible ontological categories. Receive VALUES (not a pointer)
    # loaded from the gufo_data.yaml file because the data needs to be manipulated.
    # - OTHER LISTS (IS and NOT): Empty lists. No value received.

    for new_class in classes_list:
        ontology_dataclass_list.append(OntologyDataClass(uri=new_class,
                                                         can_type=gufo_can_list_types.copy(),
                                                         can_individual=gufo_can_list_individuals.copy()))

    # Validating results: Scior requires the list to be non-empty. OWL Classes must exist in the input file.
    if not len(ontology_dataclass_list):
        error_message = f"Invalid input file. The provided ontology does not have entities of type owl:Class."
        report_error_requirement_not_met(error_message)

    LOGGER.debug("List of Ontology concepts successfully initialized.")

    return ontology_dataclass_list


def get_list_of_all_classes_no_gufo(ontology_graph: Graph):
    """ Returns a list of all classes *that are not GUFO classes* as URI strings without
    repetitions available in a Graph. """

    list_exceptions = [GUFO_NAMESPACE]

    classes_list_no_gufo = get_list_of_all_classes(ontology_graph, list_exceptions)

    return classes_list_no_gufo


def get_gufo_possibilities(scope_restriction: str):
    """ Returns list of all GUFO classes available for classification in two lists (for types and individuals). """

    can_list_types = []
    can_list_individuals = []

    if scope_restriction == "ENDURANT_TYPES":
        can_list_types = GUFO_LIST_ENDURANT_TYPES.copy()
    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch(scope_restriction, current_function)

    return can_list_types, can_list_individuals


def gufo_type_assertion_query(query_type: str) -> str:
    """ Returns the query to identify all positive or negative assertions of gUFO types in an ontology graph.

    :param query_type: Indication of the SPARQL query type to be returned. Allowed values are 'positive' or 'negative'.
    If invalid value is provided a ValueError exception is raised.
    :type query_type: str
    :return: Positive or negative SPARQL query.
    :rtype: str
    """

    selected_query = "not selected"

    positive_query = """
    PREFIX gufo: <http://purl.org/nemo/gufo#>
    SELECT DISTINCT ?ontology_class ?class_type
    WHERE {
        ?ontology_class rdf:type owl:Class .
        ?ontology_class rdf:type ?class_type .
        FILTER(STRSTARTS(STR(?class_type), STR(gufo:)))
    } """

    negative_query = """
    PREFIX gufo: <http://purl.org/nemo/gufo#>
    SELECT DISTINCT ?ontology_class ?class_type
    WHERE {
        ?ontology_class rdf:type owl:Class .
        ?ontology_class rdf:type ?x .
        ?x owl:complementOf ?class_type .
        FILTER(STRSTARTS(STR(?class_type), STR(gufo:)))
    } """

    if query_type == 'positive':
        selected_query = positive_query
    elif query_type == 'negative':
        selected_query = negative_query
    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch(query_type, current_function)

    return selected_query


def get_known_gufo_types(input_ontology_graph: Graph, query_type: str) -> list[tuple]:
    """ For each class in the inputted ontology_graph, return all its known IS or NOT gUFO types in a tuple format.

    Only POSITIVE assertions are collected.
    Analogous to get_known_gufo_not_types and to get_known_gufo_individuals.

    :param query_type: Indication of the SPARQL query type to be returned. Allowed values are 'positive' or 'negative'.
    If invalid value is provided a ValueError exception is raised.
    :type query_type: str
    :param input_ontology_graph: Ontology's input graph.
    :type input_ontology_graph: Graph
    :return: List of tuples containing an ontology class (str) and a gufo_type (str). The tuple's first element is the
    ontology class to receive the assertion and the second is the type to be asserted to it (in short form, e.g., Kind).
    :rtype: list[tuple]
    """

    list_classes = []
    list_types = []

    query_string = gufo_type_assertion_query(query_type)
    query_result = input_ontology_graph.query(query_string)

    for row in query_result:
        list_classes.append(row.ontology_class.toPython())
        list_types.append(row.class_type.toPython().replace(GUFO_NAMESPACE, ""))

    list_tuples = list(zip(list_classes, list_types))
    LOGGER.debug(f"{query_type.title()} gUFO type assertions in the input file: {list_tuples}.")

    return list_tuples


# Not used. Not tested yet. Requires implementation of new value of SCOPE_RESTRICTION.
def get_known_gufo_individuals(united_graph: Graph) -> list[tuple]:
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
        list_elements.append(row.ontology_element.toPython())
        list_individuals.append(row.element_type.toPython().replace(GUFO_NAMESPACE, ""))

    list_tuples = list(zip(list_elements, list_individuals))

    return list_tuples


def insert_known_gufo_information(list_known_gufo: list[tuple], ontology_dataclass_list: list[OntologyDataClass],
                                  assertion_type: str) -> None:
    """ Receives a list of known (positive or negative) gUFO information and performs the necessary movements of
    elements in the ontology_dataclass_list.

    :param list_known_gufo: List of tuples containing an ontology class (str) and a gufo_type (str).
    The tuple's first element is the ontology class to receive the assertion and the second is the type to be
    asserted to it (in short form, e.g., Kind).
    :type list_known_gufo: list[tuple]
    :param ontology_dataclass_list: List of ontology dataclasses (all classes and is, can, and not lists of types).
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param assertion_type: Indication of the assertion to be included into the ontology_dataclass elements.
    Allowed values are 'positive' or 'negative'. If invalid value is provided a ValueError exception is raised.
    :type assertion_type: str
    """

    # Including POSITIVE information present in the input graph into the ontology_dataclass_list' is_type list
    if assertion_type == 'positive':
        for known_gufo in list_known_gufo:
            receptor_dataclass = get_dataclass_by_uri(ontology_dataclass_list, known_gufo[0])
            move_classification_to_is_type(ontology_dataclass_list, receptor_dataclass, known_gufo[1], "Known IS type")

    # Including NEGATIVE information present in the input graph into the ontology_dataclass_list' not_type list
    elif assertion_type == 'negative':
        for known_gufo in list_known_gufo:
            receptor_dataclass = get_dataclass_by_uri(ontology_dataclass_list, known_gufo[0])
            move_classification_to_not_type(ontology_dataclass_list, receptor_dataclass, known_gufo[1],
                                            "Known NOT type")

    # Valid values are "positive" and "negative" only
    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch(assertion_type, current_function)


def load_known_gufo_information(ontology_graph: Graph, ontology_dataclass_list: list[OntologyDataClass]) -> None:
    """ Reads gUFO information about types and instances that are available in the inputted ontology file.

    I.e., if a class is already known to have any GUFO type, this information is updated in the ontology_dataclass_list.
    E.g., if the class Person is set as a gufo:Kind in the loaded ontology, this stereotype is moved from the
    dataclass's can_type (default) list to its is_type list.

    :param ontology_graph: Ontology's updated working graph
    :type ontology_graph: Graph
    :param ontology_dataclass_list: List of ontology dataclasses (all classes and is, can, and not lists of types).
    :type ontology_dataclass_list: list[OntologyDataClass]
    """

    # Setting all classes as EndurantType
    for ontology_dataclass in ontology_dataclass_list:
        move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "EndurantType", "Initialization")

    # Collecting and adding known IS classifications
    list_known_is_gufo = get_known_gufo_types(ontology_graph, "positive")
    insert_known_gufo_information(list_known_is_gufo, ontology_dataclass_list)

    # Collecting and adding known NOT classifications
    list_known_not_gufo = get_known_gufo_types(ontology_graph, "negative")

    # TODO (@pedropaulofb): To be implemented.
    # insert_known_gufo_information(list_known_not_gufo, ontology_dataclass_list)

    sort_all_ontology_dataclass_list(ontology_dataclass_list)

    LOGGER.debug("Known gUFO information from input file transferred to dataclass_ontology_list.")
