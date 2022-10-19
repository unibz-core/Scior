""" Implementation of rules for types. """
from prettytable import PrettyTable

from modules.logger_config import initialize_logger
from modules.utils_dataclass import get_list_gufo_classification, external_move_to_is_list, get_element_list, \
    external_move_list_to_is_list
from modules.utils_graph import get_all_related_nodes

# Frequent GUFO types
GUFO_KIND = "gufo:Kind"
GUFO_SORTAL = "gufo:Sortal"
GUFO_NON_SORTAL = "gufo:NonSortal"


def treat_rule_n_r_t(ontology_dataclass, configurations):
    """ Implements rule n_r_t for types."""
    logger = initialize_logger()

    if configurations["is_complete"]:
        if GUFO_KIND in ontology_dataclass.can_type:
            ontology_dataclass.move_element_to_is_list(GUFO_KIND)
        else:
            logger.error(f"Inconsistency detected! Class {ontology_dataclass.uri} must be a gufo:Kind, "
                         f"however it cannot be. Program aborted.\n"
                         f"\t{ontology_dataclass.uri} is: {ontology_dataclass.is_type}\n"
                         f"\t{ontology_dataclass.uri} can be: {ontology_dataclass.can_type}\n"
                         f"\t{ontology_dataclass.uri} cannot be: {ontology_dataclass.not_type}\n")
            exit(1)
    elif configurations["is_automatic"]:
        logger.warning(f"Incompleteness detected. "
                       f"There is not identity principle associated to class {ontology_dataclass.uri}.")
    else:
        # TODO (@pedropaulofb): Create user interaction.
        print("User interaction to be created.")


def interaction_rule_ns_s_spe(list_ontology_dataclasses, ontology_dataclass, number_related_kinds,
                              related_can_kinds_list):
    """ Implements the user interaction for rule ns_s_spe for types. """
    print(f"\nAs a gufo:NonSortal, the class {ontology_dataclass.uri} must aggregate entities with "
          f"at least two different identity principles, which are provided by gufo:Kinds. "
          f"Currently, there is {number_related_kinds} gufo:Kinds related to this class. ")

    print(
        f"\nThe following list presents all classes that are related to {ontology_dataclass.uri} and that "
        f"can possibly be classified as gufo:Kinds.")

    table = PrettyTable(['ID', 'URI', 'Known IS Types', "Known CAN Types", "Known NOT Types"])

    node_id = 0
    for related_node in related_can_kinds_list:
        node_id += 1
        related_node_is_types = get_element_list(list_ontology_dataclasses, related_node, "is_type")
        related_node_can_types = get_element_list(list_ontology_dataclasses, related_node, "can_type")
        related_node_not_types = get_element_list(list_ontology_dataclasses, related_node, "not_type")
        table.add_row([node_id, related_node, related_node_is_types,
                       related_node_can_types, related_node_not_types])

    table.align = "l"
    print(table)

    new_sortal_id = input("Enter the ID of the class to be classified as a gufo:Kind: ")
    new_sortal_id.strip()
    new_sortal_id = int(new_sortal_id)

    print(f"The chosen class is: {related_can_kinds_list[new_sortal_id - 1]}")

    external_move_to_is_list(list_ontology_dataclasses, related_can_kinds_list[new_sortal_id - 1],
                             GUFO_KIND)


def treat_rule_ns_s_spe(ontology_dataclass, list_ontology_dataclasses, graph, nodes_list, configurations):
    """ Implements rule ns_s_spe for types."""
    logger = initialize_logger()

    # Get all ontology dataclasses that are reachable from the input dataclass
    list_all_related_nodes = get_all_related_nodes(graph, nodes_list, ontology_dataclass.uri)

    logger.debug(f"Related nodes of {ontology_dataclass.uri} are: {list_all_related_nodes}")

    # From the previous list, get all the ones that ARE gufo:Kinds
    related_is_kinds_list = get_list_gufo_classification(list_ontology_dataclasses, list_all_related_nodes,
                                                         "IS", GUFO_KIND)
    number_related_kinds = len(related_is_kinds_list)

    logger.debug(f"Related nodes of {ontology_dataclass.uri} that ARE Kinds: {list_all_related_nodes}")

    # Get all related classes that CAN be classified as gufo:Kinds
    related_can_kinds_list = get_list_gufo_classification(list_ontology_dataclasses, list_all_related_nodes,
                                                          "CAN", GUFO_KIND)
    related_can_kinds_list.sort()

    logger.debug(f"Related nodes of {ontology_dataclass.uri} that CAN BE Kinds: {list_all_related_nodes}")

    number_can_kinds_list = len(related_can_kinds_list)

    number_possibilities = number_can_kinds_list - number_related_kinds
    number_necessary = 2 - number_related_kinds

    if configurations["is_complete"]:
        # Case P=N for C+A and C+I
        if number_possibilities == number_necessary:
            external_move_list_to_is_list(list_ontology_dataclasses, related_can_kinds_list, GUFO_KIND)
        # Case P<N for C+A and C+I
        elif number_possibilities < number_necessary:
            external_move_list_to_is_list(list_ontology_dataclasses, related_can_kinds_list, GUFO_KIND)
            logger.error(f"Inconsistency detected (rule ns_s_spe)! "
                         f"The class {ontology_dataclass.uri} "
                         f"is associated to only {number_necessary - number_possibilities} Kinds, "
                         f"but it should be related to 2 Kinds.")
        # Case P>N for C+A
        elif configurations["is_automatic"]:
            logger.warning(f"Incompleteness detected (rule ns_s_spe)! "
                           f"The class {ontology_dataclass.uri} "
                           f"is associated to only {number_necessary} Kinds, "
                           f"but it should be related to 2 Kinds. "
                           f"The following classes are possibilities for the completion: {related_can_kinds_list}.")
        # Case P>N for C+I
        else:
            interaction_rule_ns_s_spe(list_ontology_dataclasses, ontology_dataclass, number_related_kinds,
                                      related_can_kinds_list)
    else:
        # All cases for N+A
        if configurations["is_automatic"]:
            logger.warning(f"Incompleteness detected (rule ns_s_spe)! "
                           f"The class {ontology_dataclass.uri} "
                           f"is associated to only {number_necessary} Kinds, "
                           f"but it should be related to 2 Kinds.")
        # Case P>=N for N+I
        elif number_possibilities >= number_necessary:
            interaction_rule_ns_s_spe(list_ontology_dataclasses, ontology_dataclass, number_related_kinds,
                                      related_can_kinds_list)
            print("Create user interaction.")
        # Case P<N for N+I
        else:
            interaction_rule_ns_s_spe(list_ontology_dataclasses, ontology_dataclass, number_related_kinds,
                                      related_can_kinds_list)
            logger.warning(f"Incompleteness detected (rule ns_s_spe)! "
                           f"The class {ontology_dataclass.uri} "
                           f"is associated to only {number_necessary} Kinds, "
                           f"but it should be related to 2 Kinds.")
