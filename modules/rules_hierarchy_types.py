""" Rules applied to the TYPES HIERARCHY. """

import time

from prettytable import PrettyTable

from modules.logger_config import initialize_logger
from modules.propagation import propagate_up, propagate_down
from modules.utils_dataclass import generate_hash_ontology_dataclass_list, get_list_gufo_classification, \
    get_element_list, external_move_to_is_list
from modules.utils_graph import get_superclasses, get_subclasses, get_all_related_nodes


# GENERAL FUNCTIONS FOR RULES -----------------------------------------------------------------------------------------

def execute_rules_types(ontology_dataclass_list, gufo_dictionary, graph, nodes_list):
    """ Executes all rules related to types. """
    logger = initialize_logger()
    logger.info("Starting GUFO types hierarchy rules ...")

    list_of_rules = ["k_s_sup", "k_ns_sub", "k_k_sub", "t_k_sup", "ns_s_sup", "r_ar_sup", "ns_s_spe"]

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = 0

    while initial_hash != final_hash:
        initial_hash = final_hash

        for rule in list_of_rules:
            # TODO (@pedropaulofb): Correct time counting.
            # Time counter cannot be performed here, as it includes user interactions that must be removed.
            st = time.perf_counter()

            switch_rule_execution(ontology_dataclass_list, gufo_dictionary, graph, nodes_list, rule)

            et = time.perf_counter()
            elapsed_time = round((et - st), 3)
            logger.info(f"Execution time for rule {rule}: {elapsed_time} seconds.")

        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        if initial_hash == final_hash:
            logger.debug("Final hash equals initial hash for the dataclass list. "
                         "GUFO types hierarchy rules successfully concluded.")
        else:
            logger.debug("Final hash does not equals initial hash for the dataclass list. Re-executing rules.")


def switch_rule_execution(ontology_dataclass_list, gufo_dictionary, graph, nodes_list, rule_code):
    """ A switch function that calls the rule received in its parameter. """

    logger = initialize_logger()

    if rule_code == "k_s_sup":
        rule_k_s_sup(ontology_dataclass_list, gufo_dictionary, graph, nodes_list)
    elif rule_code == "k_ns_sub":
        rule_k_ns_sub(ontology_dataclass_list, gufo_dictionary, graph, nodes_list)
    elif rule_code == "k_k_sub":
        rule_k_k_sub(ontology_dataclass_list, gufo_dictionary, graph, nodes_list)
    elif rule_code == "t_k_sup":
        rule_t_k_sup(ontology_dataclass_list, gufo_dictionary, graph, nodes_list)
    elif rule_code == "ns_s_sup":
        rule_ns_s_sup(ontology_dataclass_list, gufo_dictionary, graph, nodes_list)
    elif rule_code == "r_ar_sup":
        rule_r_ar_sup(ontology_dataclass_list, gufo_dictionary, graph, nodes_list)
    elif rule_code == "ns_s_spe":
        rule_ns_s_spe(ontology_dataclass_list, gufo_dictionary, graph, nodes_list)
    else:
        logger.error("Unexpected rule code received as parameter! Program aborted.")
        exit(1)


# IMPLEMENTATIONS OF SPECIFIC RULES -----------------------------------------------------------------------------------

def rule_k_s_sup(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list):
    """
    - DESCRIPTION: All direct or indirect superclasses of an ontology class that is a type of gufo:Kind
                    cannot be a type of gufo:Sortal.
    - DEFAULT: Enforce
    - CODE: k_s_sup
    """

    rule_code = "k_s_sup"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if "gufo:Kind" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")
            # The selected dataclass is included in the exclusion list because the action must not be performed on it.
            propagate_up(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list, ontology_dataclass.uri,
                         rule_code, 0, [ontology_dataclass.uri])
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_k_ns_sub(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list):
    """
    - DESCRIPTION: All direct or indirect subclasses of an ontology class that is a type of gufo:Kind
                    cannot be a type of gufo:NonSortal.
    - DEFAULT: Enforce
    - CODE: k_ns_sub
    """

    rule_code = "k_ns_sub"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if "gufo:Kind" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")
            propagate_down(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list, ontology_dataclass.uri,
                           rule_code, 0)
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_k_k_sub(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list):
    """
    - DESCRIPTION: All direct or indirect subclasses of an ontology class that is a type of gufo:Kind
                    cannot be a type of gufo:Kind.
    - DEFAULT: Enforce
    - CODE: k_k_sub
    """

    rule_code = "k_k_sub"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if "gufo:Kind" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")
            # The selected dataclass is included in the exclusion list because the action must not be performed on it.
            propagate_down(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list, ontology_dataclass.uri,
                           rule_code, 0, [ontology_dataclass.uri])
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_t_k_sup(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list):
    """
    - DESCRIPTION: If a class has a direct or indirect superclass that is a gufo:Kind, all others direct or indirect
                    superclasses are not gufo:Kinds.
    - DEFAULT: Enforce
    - CODE: t_k_sup
    """

    rule_code = "t_k_sup"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if "gufo:Kind" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

            # Get all subclasses
            all_subclasses = get_subclasses(graph, nodes_list["all"], ontology_dataclass.uri).copy()

            # For all subclasses
            for subclass in all_subclasses:
                # Get all superclasses
                all_superclasses_of_subclasses = get_superclasses(graph, nodes_list["all"], subclass).copy()
                # Return all superclasses that are of type Kind
                return_list = get_list_gufo_classification(list_ontology_dataclasses, all_superclasses_of_subclasses,
                                                           "gufo:Kind")
                counter = len(return_list)
                if counter != 1:
                    # TODO (@pedropaulofb): This error could be substituted by a warning and a possibility
                    #  of correction for the user
                    logger.error(f"Inconsistency detected. Number of gufo:Kinds types as supertypes "
                                 f"of {ontology_dataclass.uri} is {counter}, while it must be exactly 1.")
                else:
                    # set all supertypes as NOT KIND (except for the one that is already a kind)
                    propagate_up(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list, subclass, "t_k_sup",
                                 0, return_list)
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_ns_s_sup(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list):
    """
    - DESCRIPTION: All direct or indirect superclasses of an ontology class that is a type of gufo:NonSortal
                    cannot be a type of gufo:Sortal.
    - DEFAULT: Enforce
    - CODE: ns_s_sup
    """

    rule_code = "ns_s_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if "gufo:NonSortal" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")
            propagate_up(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list, ontology_dataclass.uri,
                         rule_code, 0, [ontology_dataclass.uri])
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_r_ar_sup(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list):
    """
    - DESCRIPTION: No rigid or semi-rigid type can have an anti-rigid type as direct or indirect superclass.
    - DEFAULT: Enforce
    - CODE: r_ar_sup
    """

    rule_code = "r_ar_sup"
    rule_code_up = "r_ar_sup_up"
    rule_code_down = "r_ar_sup_down"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        # Getting RigidType or SemiRigidType types
        if ("gufo:RigidType" in ontology_dataclass.is_type) or ("gufo:SemiRigidType" in ontology_dataclass.is_type):
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

            # No RigidType or SemiRigidType can have AntiRigidType as direct or indirect superclasses and (... cont.)
            propagate_up(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list, ontology_dataclass.uri,
                         rule_code_up, 0, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

        # Getting AntiRigidType types
        if "gufo:AntiRigidType" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

            # (...) consequently, no AntiRigidType can have RigidType or SemiRigidType as direct or indirect subclasses
            propagate_down(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list, ontology_dataclass.uri,
                           rule_code_down, 0, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_ns_s_spe(list_ontology_dataclasses, gufo_dictionary, graph, nodes_list):
    """
    - DESCRIPTION: A NonSortal must be directly or indirectly specialized by a Sortal OR it must directly or indirectly
                    specialize another NonSortal that is directly or indirectly specialized by a Sortal.
    - DEFAULT: Suggest
    - CODE: ns_s_spe
    """

    # TODO (@pedropaulofb): The special case of a NonSortal single class (root and leaf at the same time)
    #  must be treated. In this case,
    #   (a) the user must input a new Sortal class specializing it,
    #   (b) create a specialization relation between an already existent class and this NonSortal class, and
    #   (c) modify the classification of the single class.

    rule_code = "ns_s_spe"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if "gufo:NonSortal" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

            # Get all ontology dataclasses that are reachable from the input dataclass
            list_related_nodes = get_all_related_nodes(graph, nodes_list, ontology_dataclass.uri)
            logger.debug(f"Related nodes from {ontology_dataclass.uri} are: {list_related_nodes}")

            # Check if one of these related dataclasses is a gufo:Sortal
            sortal_list = get_list_gufo_classification(list_ontology_dataclasses, list_related_nodes, "gufo:Sortal")

            if len(sortal_list) == 0:
                logger.debug(f"None of the nodes related to from {ontology_dataclass.uri} is a gufo:Sortal")

                print(f"\nFor {ontology_dataclass.uri}, one of the following related classes must be a gufo:Sortal "
                      f"or must be specialized by a gufo:Sortal:")

                table = PrettyTable(['URI', 'Known IS Types', "Known NOT Types"])

                for related_node in list_related_nodes:
                    related_node_is_types = get_element_list(list_ontology_dataclasses, related_node, "is_type")
                    related_node_not_types = get_element_list(list_ontology_dataclasses, related_node, "not_type")
                    table.add_row([related_node, related_node_is_types, related_node_not_types])

                table.align = "l"
                print(table)

                new_sortal_uri = input("Enter the URI of the element to be classified as a Sortal: ")
                new_sortal_type = "gufo:" + input("Enter the type of the element (options are: "
                                                  "Sortal, Kind, Phase, Role, or SubKind): ")

                # TODO (@pedropaulofb): Treat invalid input from user (for both data entries).

                external_move_to_is_list(list_ontology_dataclasses, new_sortal_uri, new_sortal_type, gufo_dictionary)

            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

# TODO (@pedropaulofb): rule_ns_s_spe must be treated in the following way:
#   a) Show to user only classes that CAN BE Sortals.
#       a1) User can set one of them as Sortal.
#       a2) User can specialize it with a new Sortal.
#   b) Show to user only classes that ARE NonSortals.
#       b1) User can reclassify one of them as Sortal.
#       b2) User can specialize it with a new Sortal.
# With that information, the action provided by the user must be performed.
