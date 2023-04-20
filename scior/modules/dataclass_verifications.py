""" This module implements functions for validate Ontology DataClasses. """

from scior.modules.logger_config import initialize_logger
from scior.modules.resources_gufo import GUFO_FINAL_CLASSIFICATIONS
from scior.modules.utils_general import has_duplicates, lists_intersection

LOGGER = initialize_logger()


def verify_duplicates_in_lists_ontology(ontology_dataclass):
    """ No same string must be in two lists at the same time. """

    merged_list = ontology_dataclass.is_type + ontology_dataclass.is_individual + ontology_dataclass.can_type + ontology_dataclass.can_individual + ontology_dataclass.not_type + ontology_dataclass.not_individual

    if has_duplicates(merged_list):
        LOGGER.error(f"INCONSISTENCY DETECTED: Same element in two lists for {ontology_dataclass.uri}. "
                     f"Program aborted.")
        exit(1)


# For versions dealing with individuals, implement this verification for that hierarchy.
def verify_multiple_final_classifications_for_types(ontology_dataclass):
    """ No two final classifications can be in the is_type list at the same moment """

    result_list = lists_intersection(GUFO_FINAL_CLASSIFICATIONS, ontology_dataclass.is_type)

    if len(result_list) > 1:
        LOGGER.error(f"Software execution problem found! "
                     f"The class {ontology_dataclass.uri} is of multiple final types, which is not allowed. "
                     f"The classifications are: {result_list}. Execution aborted! ")
        exit(1)


def verify_all_ontology_dataclasses_consistency(ontology_dataclass_list):
    """ Calls the consistency verification of all elements in a list of Ontology DataClasses. """

    LOGGER.debug("Initializing consistency checking for all ontology dataclasses...")

    for ontology_dataclass in ontology_dataclass_list:
        ontology_dataclass.is_consistent()

    LOGGER.debug("Consistency checking for all ontology dataclasses successfully performed.")
