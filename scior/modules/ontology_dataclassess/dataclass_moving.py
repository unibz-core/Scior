""" Functions related to moving elements between different lists in a OntologyDataClass or
in the ontology_data_class_list. """

import bisect
import inspect

from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.problems_treatment.treat_errors import report_error_end_of_switch
from scior.modules.problems_treatment.treat_inconsistent import report_inconsistency_case_moving
from scior.modules.rules.rule_group_gufo import loop_execute_gufo_rules

LOGGER = initialize_logger()


def move_classification_between_type_lists(ontology_dataclass_list: list[OntologyDataClass],
                                           ontology_dataclass: OntologyDataClass, classification_to_move: str,
                                           target_list: str, caller: str) -> None:
    """ Unique function that performs moving of classifications between lists of an ontology_dataclass.
        It is used for all other moving functions.
        Always insert in ordered position. I.e., final lists are always kept sorted.
    """

    ontology_dataclass.can_type.remove(classification_to_move)

    if target_list == "is_type":
        bisect.insort(ontology_dataclass.is_type, classification_to_move)
    elif target_list == "not_type":
        bisect.insort(ontology_dataclass.not_type, classification_to_move)
    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch(target_list, current_function)

    # Every time a classification is moved the class will be reanalyzed by all rules, so the incompleteness is
    # cleared to be updated if detected again.
    ontology_dataclass.is_incomplete = False

    LOGGER.debug(f"{caller}: Classification moved from CAN_TYPE to {target_list.upper()} in {ontology_dataclass.uri}.")

    # All list must be re-evaluated to comply with the gUFO rules.
    loop_execute_gufo_rules(ontology_dataclass_list)


def move_classification_to_is_type(ontology_dataclass_list: list[OntologyDataClass],
                                   ontology_dataclass: OntologyDataClass, classification_to_move: str,
                                   caller: str) -> None:
    """ Receives an ontology_dataclass and a classification and moves this classification to the
        dataclass' is_type list.
    """

    destination_list = "is_type"

    # LOGGER.debug(f"{caller}: Move requested to classify {classification_to_move} "
    #              f"to {destination_list.upper()} in {ontology_dataclass.uri}.")

    if classification_to_move in ontology_dataclass.can_type:
        move_classification_between_type_lists(ontology_dataclass_list, ontology_dataclass, classification_to_move,
                                               destination_list, caller)



    elif classification_to_move in ontology_dataclass.is_type:
        # LOGGER.debug(f"{caller}: Classification {classification_to_move} already "
        #              f"in {destination_list.upper()} list of {ontology_dataclass.uri}.")
        pass

    elif classification_to_move in ontology_dataclass.not_type:
        additional_message = f"{caller}: Classification {classification_to_move} is in NOT_LIST and " \
                             f"cannot be moved to {destination_list.upper()}. "
        report_inconsistency_case_moving(ontology_dataclass, additional_message)

    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch(classification_to_move, current_function)


def move_classifications_list_to_is_type(ontology_dataclass_list: list[OntologyDataClass],
                                         ontology_dataclass: OntologyDataClass, list_classifications_to_move: list[str],
                                         caller_rule: str = "") -> None:
    """ Receives an ontology_dataclass and a list of classifications. Moves all classifications of the list to the
        dataclass' is_type list.
    """

    for classification_to_move in list_classifications_to_move:
        move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, classification_to_move,
                                       caller_rule)


def move_classification_to_not_type(ontology_dataclass_list: list[OntologyDataClass],
                                    ontology_dataclass: OntologyDataClass, classification_to_move: str,
                                    caller: str = "") -> None:
    """ Receives an ontology_dataclass and a classification and moves this classification to the
        dataclass' not_type list.
    """

    destination_list = "not_type"

    # LOGGER.debug(f"{caller}: Move requested to classify {classification_to_move} "
    #              f"to {destination_list.upper()} in {ontology_dataclass.uri}.")

    if classification_to_move in ontology_dataclass.can_type:
        move_classification_between_type_lists(ontology_dataclass_list, ontology_dataclass, classification_to_move,
                                               destination_list, caller)

    elif classification_to_move in ontology_dataclass.not_type:
        # LOGGER.debug(f"{caller}: Classification {classification_to_move} already "
        #              f"in {destination_list.upper()} list of {ontology_dataclass.uri}.")
        pass

    elif classification_to_move in ontology_dataclass.is_type:
        additional_message = f"{caller}: Classification {classification_to_move} is in IS_LIST and " \
                             f"cannot be moved to {destination_list.upper()}. "
        report_inconsistency_case_moving(ontology_dataclass, additional_message)

    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch(classification_to_move, current_function)


def move_classifications_list_to_not_type(ontology_dataclass_list: list[OntologyDataClass],
                                          ontology_dataclass: OntologyDataClass,
                                          list_classifications_to_move: list[str], caller_rule: str = "") -> None:
    """ Receives an ontology_dataclass and a list of classifications. Moves all classifications of the list to the
        dataclass' not_type list.
    """

    for classification_to_move in list_classifications_to_move:
        move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass,
                                        classification_to_move, caller_rule)


def sort_all_ontology_dataclass_list(ontology_dataclass_list: list[OntologyDataClass]) -> None:
    """ Use ontology_dataclass sort method to order all ontology_dataclasses inside the ontology_dataclass_list.

        Is used ONCE after the ontology_dataclass_list is loadaded with the known gUFO classifications from the input
        ontology. initialization. After that all classification moving between lists is done in a sorted way.
    """

    for ontology_dataclass in ontology_dataclass_list:
        ontology_dataclass.sort_all_internal_lists()
