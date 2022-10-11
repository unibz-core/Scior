""" Implementation of rules related to the GUFO types hierarchy. """
import time

from prettytable import PrettyTable

from modules.global_configurations import PRINT_TIME
from modules.logger_config import initialize_logger
from modules.propagation import execute_and_propagate_down, execute_and_propagate_up
from modules.utils_dataclass import get_list_gufo_classification, get_element_list, external_move_to_is_list
from modules.utils_graph import get_all_related_nodes, get_subclasses, get_superclasses, get_all_superclasses

INTERVENTION_WARNING = "MANUAL INTERVENTION NEEDED!\n"

# Frequent GUFO types
GUFO_KIND = "gufo:Kind"
GUFO_SORTAL = "gufo:Sortal"
GUFO_NON_SORTAL = "gufo:NonSortal"


def rule_k_s_sup(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: A gufo:Kind cannot have gufo:Sortals as its direct or indirect supertypes.

    - BEHAVIOUR:

        - Complete + Automatic Only: Enforce. (IMPLEMENTED)
        - Complete + Automatic: Enforce. (IMPLEMENTED)
        - Complete + Interactive: User can apply or report deficiency. (NOT IMPLEMENTED)

        - Incomplete + Automatic Only: Enforce. (IMPLEMENTED)
        - Incomplete + Automatic: Enforce. (IMPLEMENTED)
        - Incomplete + Interactive: User can apply or include new. (NOT IMPLEMENTED)

    """

    if PRINT_TIME:
        st = time.perf_counter()

    rule_code = "k_s_sup"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_KIND in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")
            # The selected dataclass is included in the exclusion list because the action must not be performed on it.
            execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list,
                                     ontology_dataclass.uri,
                                     rule_code, [ontology_dataclass.uri])
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

    if PRINT_TIME:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_s_k_sub(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: gufo:Sortals cannot have a gufo:Kind as direct or indirect subtypes.

    - BEHAVIOUR:

        - Complete + Automatic Only: Enforce. If not possible, report deficiency. (NOT IMPLEMENTED)
        - Complete + Automatic: Enforce. If not possible, report deficiency. (PARTIALLY IMPLEMENTED)
        - Complete + Interactive: User can apply or report deficiency. (PARTIALLY IMPLEMENTED)

        - Incomplete + Automatic Only: Enforce. (IMPLEMENTED)
        - Incomplete + Automatic: Enforce. (IMPLEMENTED)
        - Incomplete + Interactive: User can apply or report deficiency. (NOT IMPLEMENTED)


    """

    if PRINT_TIME:
        st = time.perf_counter()

    rule_code = "s_k_sub"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_SORTAL in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")
            # The selected dataclass is included in the exclusion list because the action must not be performed on it.
            execute_and_propagate_down(list_ontology_dataclasses, graph, nodes_list,
                                       ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

    if PRINT_TIME:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_t_k_sup(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: A type cannot have more than one Kind as its direct or indirect supertypes.

    - BEHAVIOUR:

        - Complete + Automatic Only: Enforce. If not possible, report deficiency. (NOT IMPLEMENTED)
        - Complete + Automatic: Enforce. If not possible, report deficiency. (PARTIALLY IMPLEMENTED)
        - Complete + Interactive: User can apply or report deficiency. (PARTIALLY IMPLEMENTED)

        - Incomplete + Automatic Only: Enforce. (IMPLEMENTED)
        - Incomplete + Automatic: Enforce. (IMPLEMENTED)
        - Incomplete + Interactive: User can apply or report deficiency. (NOT IMPLEMENTED)
    """

    if PRINT_TIME:
        st = time.perf_counter()

    rule_code = "t_k_sup"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_KIND in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

            # Get all subclasses
            all_subclasses = get_subclasses(graph, nodes_list["all"], ontology_dataclass.uri).copy()

            # For all subclasses
            for subclass in all_subclasses:
                # Get all superclasses
                all_superclasses_of_subclasses = get_superclasses(graph, nodes_list["all"], subclass).copy()
                # Return all superclasses that are of type Kind
                return_list = get_list_gufo_classification(list_ontology_dataclasses, all_superclasses_of_subclasses,
                                                           "IS", GUFO_KIND)
                counter = len(return_list)
                if counter != 1:
                    logger.error(f"Inconsistency detected. Number of gufo:Kinds types as supertypes "
                                 f"of {ontology_dataclass.uri} is {counter}, while it must be exactly 1. "
                                 f"Program aborted.")
                    exit(1)
                else:
                    # set all supertypes as NOT KIND (except for the one that is already a kind)
                    execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list, subclass,
                                             "t_k_sup",
                                             return_list)
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

    if PRINT_TIME:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_ns_s_sup(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: NonSortals aggregates identities from at least two different identity principles providers.

    - RULE: A gufo:NonSortal cannot have a gufo:Sortal as its direct or indirect supertype.

    - BEHAVIOUR:

        - Complete + Automatic Only: Enforce. If not possible, report deficiency. (NOT IMPLEMENTED)
        - Complete + Automatic: Enforce. If not possible, report deficiency. (PARTIALLY IMPLEMENTED)
        - Complete + Interactive: User can apply or report deficiency. (PARTIALLY IMPLEMENTED)

        - Incomplete + Automatic Only: Enforce. (IMPLEMENTED)
        - Incomplete + Automatic: Enforce. (IMPLEMENTED)
        - Incomplete + Interactive: User can apply or report deficiency. (NOT IMPLEMENTED)
    """
    if PRINT_TIME:
        st = time.perf_counter()

    rule_code = "ns_s_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_NON_SORTAL in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")
            execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list,
                                     ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

    if PRINT_TIME:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_s_ns_sub(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: A gufo:Sortal cannot have a gufo:NonSortal as its direct or indirect subtype.

    - BEHAVIOUR:

        - Complete + Automatic Only: Enforce. If not possible, report deficiency. (NOT IMPLEMENTED)
        - Complete + Automatic: Enforce. If not possible, report deficiency. (PARTIALLY IMPLEMENTED)
        - Complete + Interactive: User can apply or report deficiency. (PARTIALLY IMPLEMENTED)

        - Incomplete + Automatic Only: Enforce. (IMPLEMENTED)
        - Incomplete + Automatic: Enforce. (IMPLEMENTED)
        - Incomplete + Interactive: User can apply or report deficiency. (NOT IMPLEMENTED)
    """

    if PRINT_TIME:
        st = time.perf_counter()

    rule_code = "s_ns_sub"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_SORTAL in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")
            execute_and_propagate_down(list_ontology_dataclasses, graph, nodes_list,
                                       ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

    if PRINT_TIME:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_r_ar_sup(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Rigid types cannot specialize AntiRigid types.

    - RULE: A Rigid or SemiRigid type cannot have an AntiRigid type as its direct or indirect supertypes.

    - BEHAVIOUR:

        - Complete + Automatic Only: Enforce. If not possible, report deficiency. (NOT IMPLEMENTED)
        - Complete + Automatic: Enforce. If not possible, report deficiency. (PARTIALLY IMPLEMENTED)
        - Complete + Interactive: User can apply or report deficiency. (PARTIALLY IMPLEMENTED)

        - Incomplete + Automatic Only: Enforce. (IMPLEMENTED)
        - Incomplete + Automatic: Enforce. (IMPLEMENTED)
        - Incomplete + Interactive: User can apply or report deficiency. (NOT IMPLEMENTED)
    """

    if PRINT_TIME:
        st = time.perf_counter()

    rule_code = "r_ar_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        # Getting RigidType or SemiRigidType types
        if ("gufo:RigidType" in ontology_dataclass.is_type) or ("gufo:SemiRigidType" in ontology_dataclass.is_type):
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

            # No RigidType or SemiRigidType can have AntiRigidType as direct or indirect superclasses and (... cont.)
            execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list,
                                     ontology_dataclass.uri,
                                     rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

    if PRINT_TIME:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_ar_r_sub(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Rigid types cannot specialize AntiRigid types.

    - RULE: A AntiRigid type cannot have a Rigid or SemiRigid type as its direct or indirect subtypes.

    - BEHAVIOUR:

        - Complete + Automatic Only: Enforce. If not possible, report deficiency. (NOT IMPLEMENTED)
        - Complete + Automatic: Enforce. If not possible, report deficiency. (PARTIALLY IMPLEMENTED)
        - Complete + Interactive: User can apply or report deficiency. (PARTIALLY IMPLEMENTED)

        - Incomplete + Automatic Only: Enforce. (IMPLEMENTED)
        - Incomplete + Automatic: Enforce. (IMPLEMENTED)
        - Incomplete + Interactive: User can apply or report deficiency. (NOT IMPLEMENTED)
    """

    if PRINT_TIME:
        st = time.perf_counter()

    rule_code = "ar_r_sub"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if "gufo:AntiRigidType" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

            execute_and_propagate_down(list_ontology_dataclasses, graph, nodes_list,
                                       ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

    if PRINT_TIME:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_n_r_t(list_ontology_dataclasses, nodes_list):
    """
    - REASON: Every type must supply (Kinds) or carry (Non-Kind Sortals) a single identity principle or
    aggregate (NonSortals) multiple identity principles.

    - RULE: In complete models, every type without supertypes and without subtypes must be a gufo:Kind.

    - BEHAVIOUR:

        - Complete + Automatic Only: Enforce. If it is set as something else than a Kind, report error.
        (PARTIALLY IMPLEMENTED)
        - Complete + Automatic: Enforce. If it is set as something else than a Kind, report error.
        (PARTIALLY IMPLEMENTED)
        - Complete + Interactive: User can: apply or report deficiency. (NOT IMPLEMENTED)

        - Incomplete + Automatic Only: Not available. No action. (IMPLEMENTED)
        - Incomplete + Automatic: User can: apply or include new. (NOT IMPLEMENTED)
        - Incomplete + Interactive: User can: apply or include new. (NOT IMPLEMENTED)
    """

    if PRINT_TIME:
        st = time.perf_counter()

    rule_code = "n_r_t"
    gufo_kind = GUFO_KIND

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if gufo_kind not in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

            if (ontology_dataclass.uri in nodes_list["roots"]) and (ontology_dataclass.uri in nodes_list["leaves"]):
                if gufo_kind in ontology_dataclass.can_type:
                    ontology_dataclass.move_element_to_is_list(gufo_kind)
                else:
                    logger.error(f"Cannot set class {ontology_dataclass.uri} as {gufo_kind}. "
                                 f"Inconsistency detected. Program aborted.")
                    exit(1)

            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

    if PRINT_TIME:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


# TODO (@pedropaulofb): Treat the special case of a NonSortal single class (root and leaf at the same time).
def rule_ns_s_spe(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: NonSortals aggregates identities from at least two different identity principles providers.

    - RULE: Given a gufo:NonSortal N, there must be at least two gufo:Sortals S1 and S2 with different
    identity principles (i.e., that are specializations of different gufo:Kinds) that:
        (1) directly or indirectly specializes N, OR
        (2) directly or indirectly specializes
            (i) a supertype of N OR
            (ii) a supertype of one of the subtypes of N.

    In other words, from any gufo:NonSortal at least two gufo:Kinds must be reachable by navigating its
    generalization/specialization relations.

    BEHAVIOUR:

        - Complete + Automatic Only: Enforce. Verify number of possibilities. (PARTIALLY IMPLEMENTED)
            1) If the possibilities are equal to the necessary number, set as Kind.
            2) If the possibilities are higher than the necessary number, do nothing.
            3) If the possibilities are smaller than the necessary number, report problem.
        - Complete + Automatic: Enforce. Verify number of possibilities. (PARTIALLY IMPLEMENTED)
            1) If the possibilities are equal to the necessary number, set as Kind.
            2) If the possibilities are higher than the necessary number, do nothing.
            3) If the possibilities are smaller than the necessary number, report problem.
        - Complete + Interactive: Verify number of possibilities. User can: (PARTIALLY IMPLEMENTED)
            1) If the possibilities are higher or equal to the necessary number: apply.
            2) If the possibilities are smaller than the necessary number: apply and report problem.

        - Incomplete + Automatic Only: Not available. No action. (IMPLEMENTED)
        - Incomplete + Automatic: User can: apply or include new. (PARTIALLY IMPLEMENTED)
        - Incomplete + Interactive: User can: apply or include new. (PARTIALLY IMPLEMENTED)
    """

    if PRINT_TIME:
        st1 = time.perf_counter()
        # Necessary for the calculation when interactive mode.
        st2 = -1

    rule_code = "ns_s_spe"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_NON_SORTAL in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

            # Get all ontology dataclasses that are reachable from the input dataclass
            list_all_related_nodes = get_all_related_nodes(graph, nodes_list, ontology_dataclass.uri)

            logger.debug(f"Related nodes of {ontology_dataclass.uri} are: {list_all_related_nodes}")

            # From the previous list, get all the ones that ARE gufo:Kinds
            related_can_kinds_list = get_list_gufo_classification(list_ontology_dataclasses, list_all_related_nodes,
                                                                  "IS", GUFO_KIND)
            number_related_kinds = len(related_can_kinds_list)

            # Get all related classes that CAN be classified as gufo:Kinds
            related_can_kinds_list = get_list_gufo_classification(list_ontology_dataclasses, list_all_related_nodes,
                                                                  "CAN", GUFO_KIND)
            related_can_kinds_list.sort()

            number_can_kinds_list = len(related_can_kinds_list)

            if number_related_kinds < 2:

                # A number of possibilities lower than the necessary indicates a deficiency in complete models.
                if (number_can_kinds_list + number_related_kinds) < 2:
                    logger.error(f"Inconsistency detected for {ontology_dataclass.uri}. The number of related Kinds is "
                                 f"{number_related_kinds} and the number of possible Kinds is {number_can_kinds_list}, "
                                 f"which is lower than the necessary number (2). "
                                 f"Aborting the program.")
                    exit(1)

                if PRINT_TIME:
                    et1 = time.perf_counter()

                logger.info(INTERVENTION_WARNING)
                time.sleep(0.2)

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

                if PRINT_TIME:
                    st2 = time.perf_counter()

                external_move_to_is_list(list_ontology_dataclasses, related_can_kinds_list[new_sortal_id - 1],
                                         GUFO_KIND)

            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")

    if PRINT_TIME:
        et2 = time.perf_counter()
        if st2 > 0:
            elapsed_time_final = round((et1 - st1 + et2 - st2), 3)
        else:
            elapsed_time_final = round((et2 - st1), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time_final} seconds.")


def rule_nk_k_sup(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: Every non-Kind gufo:Sortal (is gufo:Sortal and is not gufo:Kind) must have exactly one gufo:Kind
    as direct or indirect supertype.

    - BEHAVIOUR:

        - Complete + Automatic Only: Enforce. If not possible, report deficiency. (NOT IMPLEMENTED)
        - Complete + Automatic: Enforce. If not possible, report deficiency. (PARTIALLY IMPLEMENTED)
        - Complete + Interactive: User can apply or report deficiency. (PARTIALLY IMPLEMENTED)

        - Incomplete + Automatic Only: Enforce. (IMPLEMENTED)
        - Incomplete + Automatic: Enforce. (IMPLEMENTED)
        - Incomplete + Interactive: User can apply or report deficiency. (NOT IMPLEMENTED)

    """

    if PRINT_TIME:
        st1 = time.perf_counter()
        # Necessary for the calculation when interactive mode.
        st2 = -1

    rule_code = "nk_k_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1: class has is_type Sortal and not_type Kind:
        if (GUFO_SORTAL not in ontology_dataclass.is_type) or (GUFO_KIND not in ontology_dataclass.not_type):
            continue

        logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

        # Get all ontology dataclasses that are directly or indirectly superclasses of ontology_dataclass
        list_superclasses = get_all_superclasses(graph, nodes_list, ontology_dataclass.uri)
        logger.debug(f"Superclasses from {ontology_dataclass.uri} are: {list_superclasses}")

        # Verify if there is a Kind in the superclass list
        kind_sortals = get_list_gufo_classification(list_ontology_dataclasses, list_superclasses, "IS", GUFO_KIND)

        # CONDITION 2: Kind not found in list of superclasses
        if len(kind_sortals) != 0:
            continue

        list_possibilities = []
        # select which can be kind (can_type)
        for possible_kind in list_superclasses:

            possible_kind_can = get_element_list(list_ontology_dataclasses, possible_kind, "can_type")

            if GUFO_KIND in possible_kind_can:
                list_possibilities.append(possible_kind)

            # TODO (@pedropaulofb): Treat the case where there is no possibility (e.g., root class or a class
            # that all supertypes are have kind in its not_type list. In this case an incompleteness was found
            # and the user must (a) create a new kind class and define its relation with one of the classes in
            # the list_superclasses or (b) reclassify one of the classes.

        # If automatic, then the unique possibility can be directly asserted.
        # TODO (@pedropaulofb): Treat case not automatic.
        if len(list_possibilities) == 1:
            external_move_to_is_list(list_ontology_dataclasses, list_possibilities[0], GUFO_KIND)
            logger.debug(f"Class {list_possibilities[0]} is the unique possible identity provider "
                         f"for {ontology_dataclass.uri}. Hence, it was automatically asserted as gufo:Kind.")

        # Case multiple possibilities, user must choose.
        elif len(list_possibilities) > 1:

            if PRINT_TIME:
                et1 = time.perf_counter()

            logger.info(INTERVENTION_WARNING)
            time.sleep(0.2)

            # User must choose an option to become a Kind.
            print(f"No identity provider (Kind) was identified for the class {ontology_dataclass.uri}.")
            print(f"The following classes were identified as possible identity providers:")
            for item in list_possibilities:
                print(f"\t - {item}")
            new_kind = input(f"Enter the class to be set as gufo:Kind: ")
            new_kind.strip()

            if PRINT_TIME:
                st2 = time.perf_counter()

            external_move_to_is_list(list_ontology_dataclasses, new_kind, GUFO_KIND)

    if PRINT_TIME:
        et2 = time.perf_counter()
        if st2 > 0:
            elapsed_time_final = round((et1 - st1 + et2 - st2), 3)
        else:
            elapsed_time_final = round((et2 - st1), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time_final} seconds.")

def rule_s_nsup_k(list_ontology_dataclasses, graph, nodes_list):
    """
        - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly
        one identity principle, which is provided by a Kind.

        - RULE: In complete models, every gufo:Sortal without supertypes is a gufo:Kind.

        - BEHAVIOUR:

            - Complete + Automatic Only: Enforce. (IMPLEMENTED)
            - Complete + Automatic: Enforce. (IMPLEMENTED)
            - Complete + Interactive: User can: apply or report deficiency. (NOT IMPLEMENTED)

            - Incomplete + Automatic Only: Not available. No action. (IMPLEMENTED)
            - Incomplete + Automatic: User can: apply or include new. (NOT IMPLEMENTED)
            - Incomplete + Interactive: User can: apply or include new. (NOT IMPLEMENTED)
        """

    if PRINT_TIME:
        st = time.perf_counter()

    rule_code = "s_nsup_k"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1: ontology_dataclass must be a gufo:Sortal
        if GUFO_SORTAL not in ontology_dataclass.is_type:
            continue

        logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")

        # Get list of all superclasses up to leaves.
        all_superclasses = get_all_superclasses(graph, nodes_list, ontology_dataclass.uri)

        # CONDITION 2: list of superclasses must be empty

        if len(all_superclasses) == 0:
            ontology_dataclass.move_element_to_is_list(GUFO_KIND)

    if PRINT_TIME:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")
