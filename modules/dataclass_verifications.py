""" This module implements the methods of the classes defined in dataclass_definitions_gufo.py """

import logging

# TODO (@pedropaulofb): Maybe the verification funct should only be performed when a parameter is provided by the user
from modules.aux_general import has_duplicates

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)


def check_duplicated_same_list_ontology(ontology_class):
    """ Verifies if there are duplicated elements in each one of the OntologyClass lists"""
    duplicated_list = []

    if has_duplicates(ontology_class.is_type):
        duplicated_list.append("is_type")
    elif has_duplicates(ontology_class.is_individual):
        duplicated_list.append("is_individual")
    elif has_duplicates(ontology_class.can_type):
        duplicated_list.append("can_type")
    elif has_duplicates(ontology_class.can_individual):
        duplicated_list.append("can_individual")
    elif has_duplicates(ontology_class.not_type):
        duplicated_list.append("not_type")
    elif has_duplicates(ontology_class.not_individual):
        duplicated_list.append("not_individual")

    if len(duplicated_list) != 0:
        logging.error(f"INCONSISTENCY DETECTED: Same element in two lists for element {ontology_class.uri} "
                      f"in list {duplicated_list} in function {check_duplicated_same_list_ontology.__name__}.")
        exit(1)
    else:
        logging.debug(f"No inconsistency detected in {ontology_class.uri} "
                      f"in function {check_duplicated_same_list_ontology.__name__}.")

        # There is no need for a return because the errors area already displayed case detected.


def check_duplicated_same_list_gufo(gufo_dataclass):
    """ Verifies if there are duplicated elements in each one of the GUFOClass lists"""

    duplicated_list = []

    if has_duplicates(gufo_dataclass.is_list):
        duplicated_list.append("is_list")
    elif has_duplicates(gufo_dataclass.can_list):
        duplicated_list.append("can_list")
    elif has_duplicates(gufo_dataclass.not_list):
        duplicated_list.append("not_list")

    if len(duplicated_list) != 0:
        logging.error(f"INCONSISTENCY DETECTED: Same element in two lists for element {gufo_dataclass.uri} "
                      f"in list {duplicated_list} in function {check_duplicated_same_list_gufo.__name__}.")
        exit(1)
    else:
        logging.debug(f"No inconsistency detected in {gufo_dataclass.uri} "
                      f"in function {check_duplicated_same_list_gufo.__name__}.")

    # There is no need for a return because the errors area already displayed case detected.


def correct_number_of_elements_ontology(ontology_dataclass):
    """ Sum of elements from all the lists in a dataclass must be equal to expected_number """

    # Total number of gufo elements (classes)
    expected_number = 27

    total_length = len(ontology_dataclass.is_type) + len(ontology_dataclass.is_individual) + len(
        ontology_dataclass.can_type) + len(ontology_dataclass.can_individual) + len(ontology_dataclass.not_type) + len(
        ontology_dataclass.not_individual)

    if total_length != expected_number:
        logging.error(f"INCONSISTENCY DETECTED: The number of elements in {ontology_dataclass.uri} is {total_length}, "
                      f"which is different from the expected number ({expected_number}) "
                      f"in function {correct_number_of_elements_ontology.__name__}.")
        exit(1)
    else:
        logging.debug(f"No inconsistency detected in {ontology_dataclass.uri} "
                      f"in function {correct_number_of_elements_ontology.__name__}.")


def correct_number_of_elements_gufo(gufo_dataclass):
    """Sum of elements from all the lists in a dataclass must be equal to expeted_number"""

    types_number = 14
    individuals_number = 13

    total_length = len(gufo_dataclass.is_list) + len(gufo_dataclass.can_list) + len(gufo_dataclass.not_list)

    if (total_length != types_number) and (total_length != individuals_number):
        logging.error(f"INCONSISTENCY DETECTED: The number of elements in {gufo_dataclass.uri} is {total_length}, "
                      f"which is different from the expected number in "
                      f"function {correct_number_of_elements_gufo.__name__}.")
        exit(1)
    else:
        logging.debug(f"No inconsistency detected in {gufo_dataclass.uri} "
                      f"in function {correct_number_of_elements_gufo.__name__}.")


def duplicated_other_list(list1, list2):
    """ Returns a boolean indicating if the value of one list appears in another """

    check_1in2 = any(item in list1 for item in list2)
    check_2in1 = any(item in list2 for item in list1)
    result = check_1in2 or check_2in1

    return result


def duplicated_other_list_ontology(ontology_dataclass):
    """ No same string must be in two lists at the same time. """

    duplicated_list = []

    if duplicated_other_list(ontology_dataclass.is_type, ontology_dataclass.is_individual):
        duplicated_list.append("is_type")
        duplicated_list.append("is_individual")
    elif duplicated_other_list(ontology_dataclass.is_type, ontology_dataclass.can_individual):
        duplicated_list.append("is_type")
        duplicated_list.append("can_individual")
    elif duplicated_other_list(ontology_dataclass.is_type, ontology_dataclass.not_individual):
        duplicated_list.append("is_type")
        duplicated_list.append("not_individual")
    elif duplicated_other_list(ontology_dataclass.can_type, ontology_dataclass.is_individual):
        duplicated_list.append("can_type")
        duplicated_list.append("is_individual")
    elif duplicated_other_list(ontology_dataclass.can_type, ontology_dataclass.can_individual):
        duplicated_list.append("can_type")
        duplicated_list.append("can_individual")
    elif duplicated_other_list(ontology_dataclass.can_type, ontology_dataclass.not_individual):
        duplicated_list.append("can_type")
        duplicated_list.append("not_individual")
    elif duplicated_other_list(ontology_dataclass.not_type, ontology_dataclass.is_individual):
        duplicated_list.append("not_type")
        duplicated_list.append("is_individual")
    elif duplicated_other_list(ontology_dataclass.not_type, ontology_dataclass.can_individual):
        duplicated_list.append("not_type")
        duplicated_list.append("can_individual")
    elif duplicated_other_list(ontology_dataclass.not_type, ontology_dataclass.not_individual):
        duplicated_list.append("not_type")
        duplicated_list.append("not_individual")
    elif duplicated_other_list(ontology_dataclass.is_type, ontology_dataclass.can_type):
        duplicated_list.append("is_type")
        duplicated_list.append("can_type")
    elif duplicated_other_list(ontology_dataclass.is_type, ontology_dataclass.not_type):
        duplicated_list.append("is_type")
        duplicated_list.append("not_type")
    elif duplicated_other_list(ontology_dataclass.can_type, ontology_dataclass.not_type):
        duplicated_list.append("can_type")
        duplicated_list.append("not_type")
    elif duplicated_other_list(ontology_dataclass.is_individual, ontology_dataclass.can_individual):
        duplicated_list.append("is_individual")
        duplicated_list.append("can_individual")
    elif duplicated_other_list(ontology_dataclass.is_individual, ontology_dataclass.not_individual):
        duplicated_list.append("is_individual")
        duplicated_list.append("not_individual")
    elif duplicated_other_list(ontology_dataclass.can_individual, ontology_dataclass.not_individual):
        duplicated_list.append("can_individual")
        duplicated_list.append("not_individual")

    if len(duplicated_list) != 0:
        logging.error(
            f"INCONSISTENCY DETECTED: Same element in two lists for element {ontology_dataclass.uri} in function "
            f"{duplicated_other_list_ontology.__name__}. Lists {duplicated_list[0]} and {duplicated_list[1]}.")
        exit(1)
    else:
        logging.debug(f"No inconsistency detected in {ontology_dataclass.uri} "
                      f"in function {duplicated_other_list_ontology.__name__}. ")

    # There is no need for a return because the errors area already displayed case detected.


def duplicated_other_list_gufo(gufo_dataclass):
    """ No same string must be in two lists at the same time."""
    duplicated_list = []

    if duplicated_other_list(gufo_dataclass.is_list, gufo_dataclass.can_list):
        duplicated_list.append("is_list")
        duplicated_list.append("can_list")
    elif duplicated_other_list(gufo_dataclass.is_list, gufo_dataclass.not_list):
        duplicated_list.append("is_list")
        duplicated_list.append("not_list")
    elif duplicated_other_list(gufo_dataclass.can_list, gufo_dataclass.not_list):
        duplicated_list.append("can_list")
        duplicated_list.append("not_list")

    if len(duplicated_list) != 0:
        logging.error(f"INCONSISTENCY DETECTED: Same element in two lists for element {gufo_dataclass.uri} in function "
                      f"{duplicated_other_list_gufo.__name__}. Lists {duplicated_list[0]} and {duplicated_list[1]}.")
        exit(1)
    else:
        logging.debug(
            f"No inconsistency detected in {gufo_dataclass.uri} in function {duplicated_other_list_gufo.__name__}. ")

    # There is no need for a return because the errors area already displayed case detected.


# Tested only for List of GUFO classes
def verify_all_list_consistency(list):
    """ Calls the consistency verification of all elements in a list of GUFO or Ontology classes. """
    for i in range(len(list)):
        list[i].is_consistent()
