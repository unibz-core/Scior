""" Implementation of rules related to the GUFO types hierarchy. """

import time

from modules.logger_config import initialize_logger
from modules.propagation import execute_and_propagate_down, execute_and_propagate_up
from modules.rule_type_implementations import treat_rule_n_r_t, treat_rule_ns_s_spe
from modules.utils_dataclass import get_list_gufo_classification, get_element_list, external_move_to_is_list
from modules.utils_graph import get_subclasses, get_superclasses, get_all_superclasses

INTERVENTION_WARNING = "MANUAL INTERVENTION NEEDED!\n"

# Frequent GUFO types
GUFO_KIND = "gufo:Kind"
GUFO_SORTAL = "gufo:Sortal"
GUFO_NON_SORTAL = "gufo:NonSortal"


def rule_k_s_sup(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: A gufo:Kind cannot have gufo:Sortals as its direct or indirect supertypes.

    - DESCRIPTION: When a class is identified as a gufo:Kind, this rule identifies all its supertypes and set them as
    not gufo:Sortal.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    if configurations["print_time"]:
        st = time.perf_counter()

    rule_code = "k_s_sup"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_KIND in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

            # The selected dataclass is included in the exclusion list because the action must not be performed on it.
            execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list,
                                     ontology_dataclass.uri,
                                     rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")

    if configurations["print_time"]:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_s_k_sub(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: gufo:Sortals cannot have a gufo:Kind as direct or indirect subtypes.

    - DESCRIPTION: When a class is identified as a gufo:Sortal, this rule identifies all its subtypes and set them as
    not gufo:Kind.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    if configurations["print_time"]:
        st = time.perf_counter()

    rule_code = "s_k_sub"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_SORTAL in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

            # The selected dataclass is included in the exclusion list because the action must not be performed on it.
            execute_and_propagate_down(list_ontology_dataclasses, graph, nodes_list,
                                       ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")

    if configurations["print_time"]:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_t_k_sup(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: A type cannot have more than one Kind as its direct or indirect supertypes.

    - DESCRIPTION: Identifies a Kind. With the exception for the Kind itself,
    all direct and indirect superclasses of all subclasses of this Kind are set as not Kinds.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    if configurations["print_time"]:
        st = time.perf_counter()

    rule_code = "t_k_sup"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_KIND in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

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
                # If there are more than one Kind superclass, report error and abort program.
                if counter != 1:
                    logger.error(f"Inconsistency detected. Number of gufo:Kinds types as supertypes "
                                 f"of {ontology_dataclass.uri} is {counter}, while it must be exactly 1. "
                                 f"Program aborted.")
                    exit(1)
                # If only one Kind superclass, proceed with rule.
                else:
                    # set all supertypes as NOT KIND (except for the one that is already a Kind)
                    execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list, subclass,
                                             "t_k_sup", return_list)

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")

    if configurations["print_time"]:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_ns_s_sup(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
    - REASON: NonSortals aggregates identities from at least two different identity principles providers.

    - RULE: A gufo:NonSortal cannot have a gufo:Sortal as its direct or indirect supertype.

    - DESCRIPTION: For each NonSortal identified, set all its direct and indirect superclasses as not Sortals.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """
    if configurations["print_time"]:
        st = time.perf_counter()

    rule_code = "ns_s_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_NON_SORTAL in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

            execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list,
                                     ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")

    if configurations["print_time"]:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_s_ns_sub(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: A gufo:Sortal cannot have a gufo:NonSortal as its direct or indirect subtype.

    - DESCRIPTION: For each Sortal identified, set all its direct and indirect subclasses as not NonSortal.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    if configurations["print_time"]:
        st = time.perf_counter()

    rule_code = "s_ns_sub"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_SORTAL in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

            execute_and_propagate_down(list_ontology_dataclasses, graph, nodes_list,
                                       ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")

    if configurations["print_time"]:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_r_ar_sup(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
    - REASON: Rigid types cannot specialize AntiRigid types.

    - RULE: A Rigid or SemiRigid type cannot have an AntiRigid type as its direct or indirect supertypes.

    - DESCRIPTION: For each Rigid or SemiRigid class identified,
    set all its direct and indirect superclasses as not AntiRigid.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    if configurations["print_time"]:
        st = time.perf_counter()

    rule_code = "r_ar_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        # Getting RigidType or SemiRigidType types
        if ("gufo:RigidType" in ontology_dataclass.is_type) or ("gufo:SemiRigidType" in ontology_dataclass.is_type):
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

            # No RigidType or SemiRigidType can have AntiRigidType as direct or indirect superclasses and (... cont.)
            execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list,
                                     ontology_dataclass.uri,
                                     rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")

    if configurations["print_time"]:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_ar_r_sub(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
    - REASON: Rigid types cannot specialize AntiRigid types.

    - RULE: A AntiRigid type cannot have a Rigid or SemiRigid type as its direct or indirect subtypes.

    - DESCRIPTION: For each AntiRigid class identified,
    set all its direct and indirect subclasses as not Rigid and as not SemiRigid.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    if configurations["print_time"]:
        st = time.perf_counter()

    rule_code = "ar_r_sub"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if "gufo:AntiRigidType" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

            execute_and_propagate_down(list_ontology_dataclasses, graph, nodes_list,
                                       ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")

    if configurations["print_time"]:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_n_r_t(list_ontology_dataclasses, nodes_list, configurations):
    """
    - REASON: Every type must supply (Kinds) or carry (Non-Kind Sortals) a single identity principle or
    aggregate (NonSortals) multiple identity principles.

    - RULE: In complete models, every type without supertypes and without subtypes must be a gufo:Kind.

    - DESCRIPTION:

    - BEHAVIOR:
        - C: If can be a Kind, set as Kind. If cannot be, report inconsistency.
        - N+A: Report incompleteness.
        - N+I: User receives information and can set the class type (using IS, NOT, or SKIP).
            After the user option, if not Kind, report incompleteness.
    """

    if configurations["print_time"]:
        st = time.perf_counter()

    rule_code = "n_r_t"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1
        if GUFO_KIND in ontology_dataclass.is_type:
            continue

        # CONDITION 2
        if (ontology_dataclass.uri not in nodes_list["roots"]) or (ontology_dataclass.uri not in nodes_list["leaves"]):
            continue

        # Rule treatment when conditions are met
        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

        treat_rule_n_r_t(ontology_dataclass, configurations)

        logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")

    if configurations["print_time"]:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


# TODO (@pedropaulofb): Treat the special case of a NonSortal single class (root and leaf at the same time).
def rule_ns_s_spe(list_ontology_dataclasses, graph, nodes_list, configurations):
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

    BEHAVIOR:
        Considering P the number of possibilities and N the necessary number (N>0).

        If N <= 0: do nothing.

        Actions:
            - US: User can set a class as Kind or SKIP.
            - SA: Automatically set all P as Kinds.
            - RI: Report incompleteness.

        - RI: P<=0 or N+A or (C+A and P>N)
        - SA: P>0 and (C and P<=N)
        - US: P>0 and (N+I or (C+I and P>N))

        Resume (All cases only if N > 0):
        - C+A:
            - RI when P<=0 or when (P>0 and P>N)
            - SA when (P>0 and P<=N)
        - C+I:
            - RI when P<=0
            - US when (P>0 and P>N)
            - SA when (P>0 and P<=N)
        - N+A:
            - RI always
        - N+I:
            - RI when P<=0
            - US when P>0


    """

    if configurations["print_time"]:
        st = time.perf_counter()

    rule_code = "ns_s_spe"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1
        if GUFO_NON_SORTAL not in ontology_dataclass.is_type:
            continue

        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

        treat_rule_ns_s_spe(ontology_dataclass, list_ontology_dataclasses, graph, nodes_list, configurations)

        logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")

    if configurations["print_time"]:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")


def rule_nk_k_sup(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: Every non-Kind gufo:Sortal (is gufo:Sortal and is not gufo:Kind) must have exactly one gufo:Kind
    as direct or indirect supertype.

    BEHAVIOR:
        - C+A:
        - C+I:
        - N+A:
        - N+I:



        - Complete + Automatic Only: Enforce. If not possible, report deficiency. (NOT IMPLEMENTED)
        - Complete + Automatic: Enforce. If not possible, report deficiency. (PARTIALLY IMPLEMENTED)
        - Complete + Interactive: User can apply or report deficiency. (PARTIALLY IMPLEMENTED)

        - Incomplete + Automatic Only: Enforce. (IMPLEMENTED)
        - Incomplete + Automatic: Enforce. (IMPLEMENTED)
        - Incomplete + Interactive: User can apply or report deficiency. (NOT IMPLEMENTED)

    """

    if configurations["print_time"]:
        st1 = time.perf_counter()
        # Necessary for the calculation when interactive mode.
        st2 = -1

    rule_code = "nk_k_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1: class has is_type Sortal and not_type Kind:
        if (GUFO_SORTAL not in ontology_dataclass.is_type) or (GUFO_KIND not in ontology_dataclass.not_type):
            continue

        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

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

            if configurations["print_time"]:
                et1 = time.perf_counter()

            logger.info(INTERVENTION_WARNING)
            time.sleep(0.1)

            # User must choose an option to become a Kind.
            print(f"No identity provider (Kind) was identified for the class {ontology_dataclass.uri}.")
            print(f"The following classes were identified as possible identity providers:")
            for item in list_possibilities:
                print(f"\t - {item}")
            new_kind = input(f"Enter the class to be set as gufo:Kind: ")
            new_kind.strip()

            if configurations["print_time"]:
                st2 = time.perf_counter()

            external_move_to_is_list(list_ontology_dataclasses, new_kind, GUFO_KIND)

    if configurations["print_time"]:
        et2 = time.perf_counter()
        if st2 > 0:
            elapsed_time_final = round((et1 - st1 + et2 - st2), 3)
        else:
            elapsed_time_final = round((et2 - st1), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time_final} seconds.")


def rule_s_nsup_k(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
        - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly
        one identity principle, which is provided by a Kind.

        - RULE: In complete models, every gufo:Sortal without supertypes is a gufo:Kind.

        - BEHAVIOR:
            - C+A:
            - C+I:
            - N+A:
            - N+I:

            - Complete + Automatic Only: Enforce. (IMPLEMENTED)
            - Complete + Automatic: Enforce. (IMPLEMENTED)
            - Complete + Interactive: User can: apply or report deficiency. (NOT IMPLEMENTED)

            - Incomplete + Automatic Only: Not available. No action. (IMPLEMENTED)
            - Incomplete + Automatic: User can: apply or include new. (NOT IMPLEMENTED)
            - Incomplete + Interactive: User can: apply or include new. (NOT IMPLEMENTED)
        """

    if configurations["print_time"]:
        st = time.perf_counter()

    rule_code = "s_nsup_k"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1: ontology_dataclass must be a gufo:Sortal
        if GUFO_SORTAL not in ontology_dataclass.is_type:
            continue

        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri}...")

        # Get list of all superclasses up to leaves.
        all_superclasses = get_all_superclasses(graph, nodes_list, ontology_dataclass.uri)

        # CONDITION 2: list of superclasses must be empty

        if len(all_superclasses) == 0:
            ontology_dataclass.move_element_to_is_list(GUFO_KIND)

    if configurations["print_time"]:
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)
        logger.info(f"Execution time for rule {rule_code}: {elapsed_time} seconds.")
