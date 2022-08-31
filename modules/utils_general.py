""" General auxiliary functions. """
from modules.logger_config import initialize_logger


def has_duplicates(input_list):
    """ Check if given list contains any duplicated element """
    if len(input_list) == len(set(input_list)):
        return False
    else:
        return True


def remove_duplicates(input_list):
    """ Remove duplicated elements from a list. """

    output_list = [*set(input_list)]

    return output_list


def lists_intersection(list1, list2):
    """ Returns the intersection of two lists. """
    temp = set(list2)
    list3 = [value for value in list1 if value in temp]
    return list3


def lists_subtraction(list1, list2):
    """ Returns the subtraction between two lists. """

    list3 = list(set(list1) - set(list2))

    return list3


def update_all_ontology_dataclass_list(ontology_dataclass_list, gufo_dictionary):
    """ Updates all lists of all dataclasses inside the ontology dataclass list. """

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = 0

    while initial_hash != final_hash:
        initial_hash = final_hash
        for ontology_dataclass in ontology_dataclass_list:
            ontology_dataclass.update_all_internal_lists_from_gufo(gufo_dictionary)
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


def get_list_gufo_classification(ontology_dataclass_list, list_uris, classification):
    """ Receives a list of URIs and returns a list of dataclasses with the elements in the input list which have
    the given classification in its is_type or is_individual list.
    """

    return_list = []

    for ontology_dataclass in ontology_dataclass_list:
        if ontology_dataclass.uri in list_uris:
            if (classification in ontology_dataclass.is_type) or (classification in ontology_dataclass.is_individual):
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


def external_move_to_is_list(list_ontology_dataclasses, class_name, classification, gufo_dictionary):
    """ Receives the URI of an ontology dataclass and moves an element (from inputted element name) to its is list. """

    for ontology_dataclass in list_ontology_dataclasses:
        if ontology_dataclass.uri == class_name:
            ontology_dataclass.move_element_to_is_list(classification, gufo_dictionary)
