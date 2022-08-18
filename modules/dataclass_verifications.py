""" This module implements the methods of the classes defined in dataclass_definitions_ontology.py """

# TODO (@pedropaulofb): Maybe the verification funct should only be performed when a parameter is provided by the user

from modules.logger_config import initialize_logger
from modules.utils_general import has_duplicates


def check_duplicated_same_list_ontology(ontology_class):
    """ Verifies if there are duplicated elements in each one of the OntologyClass lists"""

    logger = initialize_logger()
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
        logger.error(f"INCONSISTENCY DETECTED: Same element in two lists for element {ontology_class.uri} "
                     f"in list {duplicated_list}.")
        exit(1)
    else:
        logger.debug(f"No inconsistency detected in {ontology_class.uri}.")

    # There is no need for a return because the errors area already displayed case detected.


def correct_number_of_elements_ontology(ontology_dataclass):
    """ Sum of elements from all the lists in a dataclass must be equal to expected_number """

    logger = initialize_logger()

    # Total number of gufo elements (classes)
    expected_number = 27

    total_length = len(ontology_dataclass.is_type) + len(ontology_dataclass.is_individual) + len(
        ontology_dataclass.can_type) + len(ontology_dataclass.can_individual) + len(ontology_dataclass.not_type) + len(
        ontology_dataclass.not_individual)

    if total_length != expected_number:
        logger.error(f"INCONSISTENCY DETECTED: The number of elements in {ontology_dataclass.uri} is {total_length}, "
                     f"which is different from the expected number ({expected_number}.")
        exit(1)
    else:
        logger.debug(f"No inconsistency detected in {ontology_dataclass.uri}.")


def duplicated_other_list(list1, list2):
    """ Returns a boolean indicating if the value of one list appears in another """

    check_1in2 = any(item in list1 for item in list2)
    check_2in1 = any(item in list2 for item in list1)
    result = check_1in2 or check_2in1

    return result


def duplicated_other_list_ontology(ontology_dataclass):
    """ No same string must be in two lists at the same time. """

    logger = initialize_logger()
    merged_list = ontology_dataclass.is_type + ontology_dataclass.is_individual + ontology_dataclass.can_type + ontology_dataclass.can_individual + ontology_dataclass.not_type + ontology_dataclass.not_individual

    if has_duplicates(merged_list):
        logger.error(f"INCONSISTENCY DETECTED: Same element in two lists for {ontology_dataclass.uri}")
        exit(1)
    else:
        logger.debug(f"No inconsistency detected in {ontology_dataclass.uri}. ")


def verify_all_list_consistency(list):
    """ Calls the consistency verification of all elements in a list of Ontology DataClasses. """
    for i in range(len(list)):
        list[i].is_consistent()
