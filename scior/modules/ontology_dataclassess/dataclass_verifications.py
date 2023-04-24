""" This module implements functions to validate OntologyDataClasses and the OntologyDataClasses list. """

from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.problems_treatment.treat_inconsistent import report_inconsistency_case_in_dataclass
from scior.modules.resources_gufo import GUFO_LIST_FINAL_CLASSIFICATIONS, GUFO_LIST_ENDURANT_TYPES

LOGGER = initialize_logger()


def verify_dataclass_invalid_strings_in_lists(ontology_dataclass: OntologyDataClass) -> None:
    """ Checks if there are invalid strings in all lists of the OntologyDataClass.
        AUXILIARY FUNCTION! MUST NOT BE USED OUTSIDE FUNCTION verify_all_ontology_dataclasses_consistency.
    """

    evaluated_list = "IS_TYPE LIST"
    for classification_is in ontology_dataclass.is_type:
        if classification_is not in GUFO_LIST_ENDURANT_TYPES:
            additional_message = f"Invalid value {classification_is} found in the ontology_dataclass {evaluated_list}."
            report_inconsistency_case_in_dataclass(ontology_dataclass, additional_message)

    evaluated_list = "CAN_TYPE LIST"
    for classification_can in ontology_dataclass.can_type:
        if classification_can not in GUFO_LIST_ENDURANT_TYPES:
            additional_message = f"Invalid value {classification_can} found in the ontology_dataclass {evaluated_list}."
            report_inconsistency_case_in_dataclass(ontology_dataclass, additional_message)

    evaluated_list = "NOT_TYPE LIST"
    for classification_not in ontology_dataclass.not_type:
        if classification_not not in GUFO_LIST_ENDURANT_TYPES:
            additional_message = f"Invalid value {classification_not} found in the ontology_dataclass {evaluated_list}."
            report_inconsistency_case_in_dataclass(ontology_dataclass, additional_message)


def verify_dataclass_classifications_quantity(ontology_dataclass: OntologyDataClass) -> None:
    """ Verifies if the amount of classifications found in the list corresponds to the expected value.
        AUXILIARY FUNCTION! MUST NOT BE USED OUTSIDE FUNCTION verify_all_ontology_dataclasses_consistency.
    """

    merged_list = ontology_dataclass.is_type + ontology_dataclass.can_type + ontology_dataclass.not_type

    expected_size = len(GUFO_LIST_ENDURANT_TYPES)
    current_size = len(merged_list)

    if expected_size != current_size:
        additional_message = f"Invalid amount of classifications. Expected {expected_size} but found {current_size}."
        report_inconsistency_case_in_dataclass(ontology_dataclass, additional_message)


def verify_dataclass_multiple_final_classifications(ontology_dataclass: OntologyDataClass) -> None:
    """ No two final classifications can be in the is_type list at the same moment.
        AUXILIARY FUNCTION! MUST NOT BE USED OUTSIDE FUNCTION verify_all_ontology_dataclasses_consistency.
    """

    final_classifications = set(ontology_dataclass.is_type).intersection(GUFO_LIST_FINAL_CLASSIFICATIONS)

    if len(final_classifications) > 1:
        additional_message = f"Multiple final classification(s) ({final_classifications}) found in IS_TYPE list."
        report_inconsistency_case_in_dataclass(ontology_dataclass, additional_message)


def verify_dataclass_duplicates_in_lists(ontology_dataclass: OntologyDataClass) -> None:
    """ No same string must be in two lists at the same time.
        AUXILIARY FUNCTION! MUST NOT BE USED OUTSIDE FUNCTION verify_all_ontology_dataclasses_consistency.
    """

    duplicated_is_can = set(ontology_dataclass.is_type).intersection(ontology_dataclass.can_type)
    duplicated_is_not = set(ontology_dataclass.is_type).intersection(ontology_dataclass.not_type)
    duplicated_can_not = set(ontology_dataclass.can_type).intersection(ontology_dataclass.not_type)

    if len(duplicated_is_can) > 0:
        additional_message = f"Duplicated classification(s) ({duplicated_is_can}) found in lists IS_TYPE and CAN_TYPE."
        report_inconsistency_case_in_dataclass(ontology_dataclass, additional_message)

    if len(duplicated_is_not) > 0:
        additional_message = f"Duplicated classification(s) ({duplicated_is_not}) found in lists IS_TYPE and NOT_TYPE."
        report_inconsistency_case_in_dataclass(ontology_dataclass, additional_message)

    if len(duplicated_can_not) > 0:
        additional_message = f"Duplicated classification(s) ({duplicated_can_not}) found in lists " \
                             f"CAN_TYPE and NOT_TYPE."
        report_inconsistency_case_in_dataclass(ontology_dataclass, additional_message)


def verify_all_ontology_dataclasses_consistency(ontology_dataclass_list: list[OntologyDataClass]) -> None:
    """ Performs a consistency verification of all elements in the ontology_dataclass_list. """

    LOGGER.debug("Initializing consistency checking for all ontology dataclasses.")

    for ontology_dataclass in ontology_dataclass_list:
        verify_dataclass_invalid_strings_in_lists(ontology_dataclass)
        verify_dataclass_classifications_quantity(ontology_dataclass)
        verify_dataclass_duplicates_in_lists(ontology_dataclass)
        verify_dataclass_multiple_final_classifications(ontology_dataclass)

    LOGGER.debug("Consistency checking for all ontology dataclasses successfully performed.")
