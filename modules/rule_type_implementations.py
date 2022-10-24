""" Implementation of rules for types. """
import time

from modules.logger_config import initialize_logger
from modules.user_interactions import select_class_from_list, set_type_for_class, print_class_types
from modules.utils_dataclass import get_list_gufo_classification, external_move_to_is_list, \
    external_move_list_to_is_list
from modules.utils_graph import get_all_related_nodes

# Frequent GUFO types
GUFO_KIND = "gufo:Kind"


def interaction_rule_n_r_t(ontology_dataclass):
    """ User interaction for rule n_r_t. """

    option = None
    valid = False

    while not valid:
        time.sleep(0.1)
        option = input(f"Would you like to set the type of {ontology_dataclass.uri} ('y' or 'n')? ")
        option = option.strip().lower()
        valid = (option == "y") or (option == "n")
        if not valid:
            print("Invalid input. Please retry.")

    if option == "y":
        print("The list of possible types to be associated with the class are:\n")
        set_type_for_class(ontology_dataclass)


def treat_rule_n_r_t(ontology_dataclass, configurations):
    """ Implements rule n_r_t for types."""
    logger = initialize_logger()

    if configurations["is_complete"]:
        if GUFO_KIND in ontology_dataclass.can_type:
            ontology_dataclass.move_element_to_is_list(GUFO_KIND)
        else:
            logger.error(f"Inconsistency detected! Class {ontology_dataclass.uri} must be a gufo:Kind, "
                         f"however it cannot be. Program aborted.")
            print_class_types(ontology_dataclass)

            exit(1)
    else:
        logger.warning(f"Incompleteness detected. "
                       f"There is not identity principle associated to class {ontology_dataclass.uri}.")
        if (not configurations["is_automatic"]) and (len(ontology_dataclass.can_type) > 0):
            interaction_rule_n_r_t(ontology_dataclass)


def interaction_rule_ns_s_spe(list_ontology_dataclasses, ontology_dataclass, number_related_kinds,
                              related_can_kinds_list):
    """ Implements the user interaction for rule ns_s_spe for types. """

    print(f"\nAs a gufo:NonSortal, the class {ontology_dataclass.uri} must aggregate entities with "
          f"at least two different identity principles, which are provided by gufo:Kinds. "
          f"Currently, there is/are {number_related_kinds} gufo:Kind(s) related to this class. ")

    print(f"\nThe following list presents all classes that are related to {ontology_dataclass.uri} and that "
          f"can possibly be classified as gufo:Kinds.")

    selected_class = select_class_from_list(list_ontology_dataclasses, related_can_kinds_list)

    if selected_class != "skipped":
        external_move_to_is_list(list_ontology_dataclasses, selected_class, GUFO_KIND)


def decide_action_rule_ns_s_spe(configurations, number_possibilities, number_necessary):
    """ Returns the action to be performed for rule ns_s_spe. """

    ni = not (configurations["is_complete"] or configurations["is_automatic"])
    ci = configurations["is_complete"] and not configurations["is_automatic"]

    if number_possibilities <= 0:
        action = "report_incompleteness"
    elif configurations["is_complete"] and number_possibilities <= number_necessary:
        action = "set_all_as_kinds"
    elif ni or (ci and number_possibilities > number_necessary):
        action = "user_can_set"
    else:
        action = "report_incompleteness"

    return action


def treat_rule_ns_s_spe(ontology_dataclass, list_ontology_dataclasses, graph, nodes_list, configurations):
    """ Implements rule ns_s_spe for types."""
    logger = initialize_logger()

    # Get all ontology dataclasses that are reachable from the input dataclass
    list_all_related_nodes = get_all_related_nodes(graph, nodes_list, ontology_dataclass.uri)

    logger.debug(f"Related nodes of {ontology_dataclass.uri} are: {list_all_related_nodes}")

    # From the previous list, get all the ones that ARE gufo:Kinds
    related_is_kinds_list = get_list_gufo_classification(list_ontology_dataclasses, list_all_related_nodes, "IS",
                                                         GUFO_KIND)
    number_related_kinds = len(related_is_kinds_list)

    logger.debug(f"Related nodes of {ontology_dataclass.uri} that ARE Kinds: {list_all_related_nodes}")

    # Get all related classes that CAN be classified as gufo:Kinds
    related_can_kinds_list = get_list_gufo_classification(list_ontology_dataclasses, list_all_related_nodes, "CAN",
                                                          GUFO_KIND)

    logger.debug(f"Related nodes of {ontology_dataclass.uri} that CAN BE Kinds: {list_all_related_nodes}")

    number_can_kinds_list = len(related_can_kinds_list)

    number_possibilities = number_can_kinds_list
    number_necessary = 2 - number_related_kinds

    logger.info(f"For {ontology_dataclass.uri}: K = {number_related_kinds}, "
                f"P = {number_possibilities}, N = {number_necessary}"
                f"\n\t K = {related_is_kinds_list}"
                f"\n\t P = {related_can_kinds_list}")

    # The rule is already accomplished, so there is no need to do any action.
    if number_necessary <= 0:
        return

    action = decide_action_rule_ns_s_spe(configurations, number_possibilities, number_necessary)

    logger.warning(f"Incompleteness detected during rule ns_s_spe! "
                   f"The class {ontology_dataclass.uri} "
                   f"is associated to {2 - number_necessary} Kind(s), "
                   f"but it should be related to at least 2 Kinds. ")

    if action == "report_incompleteness":
        logger.info(f"Classes that are associated with {ontology_dataclass.uri} and that "
                    f"can be Kinds are: {related_can_kinds_list}")
    elif action == "set_all_as_kinds":
        logger.info(f"The following classes are going to be set as Kinds "
                    f"to solve the incompleteness: {related_can_kinds_list}.")
        external_move_list_to_is_list(list_ontology_dataclasses, related_can_kinds_list, GUFO_KIND)
    elif action == "user_can_set":
        interaction_rule_ns_s_spe(list_ontology_dataclasses, ontology_dataclass, number_related_kinds,
                                  related_can_kinds_list)
    else:
        logger.error("Unexpected evaluation result! Program aborted.")
        exit(1)
