""" Functions for Ontology Dataclasses """
from modules.logger_config import initialize_logger


def update_all_ontology_dataclass_list(ontology_dataclass_list):
    """ Updates all lists of all dataclasses inside the ontology dataclass list. """

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = 0

    while initial_hash != final_hash:
        initial_hash = final_hash
        for ontology_dataclass in ontology_dataclass_list:
            ontology_dataclass.update_all_internal_lists_from_gufo()
        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)


def generate_hash_ontology_dataclass_list(ontology_dataclass_list):
    """ Generates a hash for the complete list of ontology dataclasses. """

    logger = initialize_logger()
    logger.debug("Generating hash for the complete list of ontology dataclasses...")

    total_hash = 0

    for ontology_dataclass in ontology_dataclass_list:
        class_hash = ontology_dataclass.create_hash()
        total_hash += class_hash

    logger.debug(
        f"Hash for the complete list of ontology dataclasses successfully created. Hash value is: {total_hash}")

    return total_hash


def get_list_gufo_classification(ontology_dataclass_list, list_uris, search_list, gufo_element):
    """ Receives a list of URIs (list_uris), the name of the list to be searched (search_list), and the element that
    must be in that list. Allowed search_list values can be: IS, CAN or NOT (valid for both types or individuals).

    Returns a list of URIs of the elements from the list_uris that have the element in its search_list.
    """

    global search_individual, search_type

    logger = initialize_logger()
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
            logger.error("Unexpected search list value. Program aborted.")
            exit(1)

        if (gufo_element in search_type) or (gufo_element in search_individual):
            return_list.append(ontology_dataclass.uri)

    return return_list


def get_element_list(ontology_dataclass_list, element, desired_list):
    """ Returns the list of known types for the inputted element (string). """

    logger = initialize_logger()

    for ontology_dataclass in ontology_dataclass_list:

        if ontology_dataclass.uri == element:

            if desired_list == "is_type":
                return ontology_dataclass.is_type
            elif desired_list == "can_type":
                return ontology_dataclass.can_type
            elif desired_list == "not_type":
                return ontology_dataclass.not_type
            elif desired_list == "is_individual":
                return ontology_dataclass.is_individual
            elif desired_list == "can_individual":
                return ontology_dataclass.can_individual
            elif desired_list == "not_individual":
                return ontology_dataclass.not_individual
            else:
                logger.error(f"Could not return the unknown list {desired_list} for "
                             f"element {element}. Program aborted.")
                exit(1)

    # If not found, report problem and exit program.
    logger.error(f"Could not return list {desired_list} for the unknown element {element}. Program aborted.")
    exit(1)


def external_move_to_is_list(list_ontology_dataclasses, class_name, classification):
    """ Receives the URI of an ontology dataclass and moves an element (from inputted element name) to its is list. """

    for ontology_dataclass in list_ontology_dataclasses:
        if ontology_dataclass.uri == class_name:
            ontology_dataclass.move_element_to_is_list(classification)
