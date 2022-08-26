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
        for i in range(len(ontology_dataclass_list)):
            ontology_dataclass_list[i].update_all_internal_lists_from_gufo(gufo_dictionary)
        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)


def generate_hash_ontology_dataclass_list(ontology_dataclass_list):
    """ Generates a hash for the complete list of ontology dataclasses. """

    logger = initialize_logger()
    logger.debug("Generating hash for the complete list of ontology dataclasses...")

    total_hash = 0

    for i in range(len(ontology_dataclass_list)):
        class_hash = ontology_dataclass_list[i].create_hash()
        total_hash += class_hash

    logger.debug(
        f"Hash for the complete list of ontology dataclasses successfully created. Hash value is: {total_hash}")

    return total_hash


def count_gufo_classification_in_list(ontology_dataclass_list, list_uris, classification):
    """ Receives a list of URIs and returns the number of elements in this list which have the given classification
    in its is_type or is_individual list. """

    counter = 0

    for i in range(len(ontology_dataclass_list)):
        if ontology_dataclass_list[i].uri in list_uris:
            if (classification in ontology_dataclass_list[i].is_type) or (
                    classification in ontology_dataclass_list[i].is_individual):
                counter = counter + 1

    return counter
