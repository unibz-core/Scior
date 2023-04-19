""" Functions for Ontology Dataclasses """
import operator

from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


def generate_hash_ontology_dataclass_list(ontology_dataclass_list, hash_type="TOTAL"):
    """ Generates a hash for the complete list of ontology dataclasses.

    hash_type allowed values are:
        - TOTAL: creates a hash with all six lists of the dataclasses
        - TYPES_ONLY: creates a hash with only the three types' lists of the dataclasses
        - INDIVIDUALS_ONLY: creates a hash with only the three individuals' lists of the dataclasses

    """

    LOGGER.debug("Generating hash for the complete list of ontology dataclasses...")

    total_hash = 0

    for ontology_dataclass in ontology_dataclass_list:
        class_hash = ontology_dataclass.create_hash(hash_type)
        total_hash += class_hash

    LOGGER.debug(
        f"Hash for the complete list of ontology dataclasses successfully created. Hash value is: {total_hash}")

    return total_hash


def get_list_gufo_classification(ontology_dataclass_list, list_uris, search_list, gufo_element):
    """ Receives a list of URIs (list_uris), the name of the list to be searched (search_list), and the element that
    must be in that list. Allowed search_list values can be: IS, CAN or NOT (valid for both types or individuals).

    Returns a list of URIs of the elements from the list_uris that have the element in its search_list.
    """

    global search_individual, search_type

    return_list = []

    for ontology_dataclass in ontology_dataclass_list:

        # CONDITION 1: The searched occurs for the URIs inside the list_uris.
        if ontology_dataclass.uri not in list_uris:
            continue

        if search_list == "IS":
            search_type = ontology_dataclass.is_type
            search_individual = ontology_dataclass.is_individual
        elif search_list == "CAN":
            search_type = ontology_dataclass.can_type
            search_individual = ontology_dataclass.can_individual
        elif search_list == "NOT":
            search_type = ontology_dataclass.not_type
            search_individual = ontology_dataclass.not_individual
        else:
            LOGGER.error(f"Unexpected search list value {search_list}. Program aborted.")
            exit(1)

        if (gufo_element in search_type) or (gufo_element in search_individual):
            return_list.append(ontology_dataclass.uri)

    return return_list


def get_element_list(ontology_dataclass_list, element, desired_list):
    """ Returns the list of known types for the inputted element (string). """

    returned_object = None

    for ontology_dataclass in ontology_dataclass_list:

        # Element identified. Returning list.
        if ontology_dataclass.uri == element:
            if desired_list == "is_type":
                returned_object = ontology_dataclass.is_type
                break
            elif desired_list == "can_type":
                returned_object = ontology_dataclass.can_type
                break
            elif desired_list == "not_type":
                returned_object = ontology_dataclass.not_type
                break
            elif desired_list == "is_individual":
                returned_object = ontology_dataclass.is_individual
                break
            elif desired_list == "can_individual":
                returned_object = ontology_dataclass.can_individual
                break
            elif desired_list == "not_individual":
                returned_object = ontology_dataclass.not_individual
                break
            else:
                # Error. List unknown.
                LOGGER.error(f"Could not return the unknown list {desired_list} for "
                             f"element {element}. Program aborted.")
                exit(1)
    else:
        # Error. Element not found, report problem and exit program.
        LOGGER.error(f"Could not return list {desired_list} for the unknown element {element}. Program aborted.")
        exit(1)

    return returned_object


def external_move_to_is_list(list_ontology_dataclasses, class_name, classification):
    """ Receives the URI of an ontology dataclass and moves an element (from inputted element name) to its is list. """

    for ontology_dataclass in list_ontology_dataclasses:
        if ontology_dataclass.uri == class_name:
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, classification)


def external_move_list_to_is_list(list_ontology_dataclasses, list_classes_to_move, classification):
    """ Receives a list of URIs of ontology classes and moves the classification (e.g., 'gufo:Kind')
    to their is_list. """

    for dataclass_to_move in list_classes_to_move:
        for ontology_dataclass in list_ontology_dataclasses:
            if ontology_dataclass.uri == dataclass_to_move:
                ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, classification)


def return_dataclass_from_class_name(list_ontology_dataclasses, class_name):
    """ Receives a class name and returns the corresponding dataclass element from the list of dataclasses. """

    return_object = None

    for ontology_dataclass in list_ontology_dataclasses:
        if ontology_dataclass.uri == class_name:
            return_object = ontology_dataclass
            break
    else:
        LOGGER.error(f"Class {ontology_dataclass.uri} not found in the list of ontology dataclasses. Program aborted.")
        exit(1)

    return return_object


def select_list(list_of_options):
    """ User can select between one of the lists received in the parameter list_of_options.
    Possible return values are lowercase strings. """

    valid_option = False
    selected_list = "invalid"

    while not valid_option:
        selected_list = input(f"Select a list. Options are: {list_of_options}: ")
        selected_list = selected_list.strip().lower()
        if selected_list not in list_of_options:
            print("Invalid selection. Please try again.")
        else:
            print(f"The chosen list was: {selected_list} list.")
            valid_option = True

    return selected_list


def sort_all_ontology_dataclass_list(ontology_dataclass_list):
    """ Receives an ontology_dataclass_list and:
            1) Sorts it via its dataclasses' uris
            2) Sorts all lists inside each dataclass of the list.
    """

    ontology_dataclass_list.sort(key=operator.attrgetter('uri'))

    for ontology_dataclass in ontology_dataclass_list:
        ontology_dataclass.is_type.sort()
        ontology_dataclass.can_type.sort()
        ontology_dataclass.not_type.sort()
        ontology_dataclass.is_individual.sort()
        ontology_dataclass.can_individual.sort()
        ontology_dataclass.not_individual.sort()


def get_dataclass_by_uri(ontology_dataclass_list, desired_uri: str):
    """ Receives the complete ontology_dataclass_list and return the specific Ontology DataClass that has the
    desired URI received as parameter or None, if this URI is not found. """

    for ontology_dataclass in ontology_dataclass_list:
        if ontology_dataclass.uri == desired_uri:
            return ontology_dataclass

    LOGGER.debug(f"No ontology_dataclass matches the desired URI.")
    return None
