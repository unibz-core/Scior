""" Implementation of rules related to the GUFO types hierarchy. """

from ontcatowl.modules.logger_config import initialize_logger
from ontcatowl.modules.propagation import execute_and_propagate_down, execute_and_propagate_up
from ontcatowl.modules.rules_type_implementations import treat_rule_n_r_t, treat_rule_ns_s_spe, treat_rule_nk_k_sup, \
    treat_rule_s_nsup_k, treat_rule_ns_sub_r, treat_rule_nrs_ns_r, treat_rule_ks_sf_in
from ontcatowl.modules.utils_dataclass import get_list_gufo_classification
from ontcatowl.modules.utils_graph import get_subclasses, get_superclasses

# Frequent GUFO types
GUFO_KIND = "gufo:Kind"
GUFO_SORTAL = "gufo:Sortal"
GUFO_NON_SORTAL = "gufo:NonSortal"


def rule_k_s_sup(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: A gufo:Kind cannot have gufo:Sortals as its direct or indirect supertypes.

    - DESCRIPTION: When a class is identified as a gufo:Kind, this rule identifies all its supertypes and set them as
    not gufo:Sortal.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    rule_code = "k_s_sup"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_KIND in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

            # The selected dataclass is included in the exclusion list because the action must not be performed on it.
            execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list,
                                     ontology_dataclass.uri,
                                     rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


def rule_s_k_sub(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: gufo:Sortals cannot have a gufo:Kind as direct or indirect subtypes.

    - DESCRIPTION: When a class is identified as a gufo:Sortal, this rule identifies all its subtypes and set them as
    not gufo:Kind.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    rule_code = "s_k_sub"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_SORTAL in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

            # The selected dataclass is included in the exclusion list because the action must not be performed on it.
            execute_and_propagate_down(list_ontology_dataclasses, graph, nodes_list,
                                       ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


def rule_t_k_sup(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: A type cannot have more than one Kind as its direct or indirect supertypes.

    - DESCRIPTION: Identifies a Kind. With the exception for the Kind itself,
    all direct and indirect superclasses of all subclasses of this Kind are set as not Kinds.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    rule_code = "t_k_sup"
    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_KIND in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

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


def rule_ns_s_sup(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: NonSortals aggregates identities from at least two different identity principles providers.

    - RULE: A gufo:NonSortal cannot have a gufo:Sortal as its direct or indirect supertype.

    - DESCRIPTION: For each NonSortal identified, set all its direct and indirect superclasses as not Sortals.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    rule_code = "ns_s_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_NON_SORTAL in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

            execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list,
                                     ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


def rule_s_ns_sub(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: A gufo:Sortal cannot have a gufo:NonSortal as its direct or indirect subtype.

    - DESCRIPTION: For each Sortal identified, set all its direct and indirect subclasses as not NonSortal.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    rule_code = "s_ns_sub"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if GUFO_SORTAL in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

            execute_and_propagate_down(list_ontology_dataclasses, graph, nodes_list,
                                       ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


def rule_r_ar_sup(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Rigid types cannot specialize AntiRigid types.

    - RULE: A Rigid or SemiRigid type cannot have an AntiRigid type as its direct or indirect supertypes.

    - DESCRIPTION: For each Rigid or SemiRigid class identified,
    set all its direct and indirect superclasses as not AntiRigid.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    rule_code = "r_ar_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        # Getting RigidType or SemiRigidType types
        if ("gufo:RigidType" in ontology_dataclass.is_type) or ("gufo:SemiRigidType" in ontology_dataclass.is_type):
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

            execute_and_propagate_up(list_ontology_dataclasses, graph, nodes_list,
                                     ontology_dataclass.uri,
                                     rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


def rule_ar_r_sub(list_ontology_dataclasses, graph, nodes_list):
    """
    - REASON: Rigid types cannot specialize AntiRigid types.

    - RULE: A AntiRigid type cannot have a Rigid or SemiRigid type as its direct or indirect subtypes.

    - DESCRIPTION: For each AntiRigid class identified,
    set all its direct and indirect subclasses as not Rigid and as not SemiRigid.

    - BEHAVIOR:
        - AUTOMATION: Same execution for both complete and incomplete models.
        - COMPLETENESS: Automatic rule. Interaction is not needed in any case.
    """

    rule_code = "ar_r_sub"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if "gufo:AntiRigidType" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

            execute_and_propagate_down(list_ontology_dataclasses, graph, nodes_list,
                                       ontology_dataclass.uri, rule_code, [ontology_dataclass.uri])

            logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


def rule_n_r_t(list_ontology_dataclasses, nodes_list, configurations):
    """
    - REASON: Every type must supply (Kinds) or carry (Non-Kind Sortals) a single identity principle or
    aggregate (NonSortals) multiple identity principles.

    - RULE: In complete models, every type without supertypes and without subtypes must be a gufo:Kind.

    - DESCRIPTION:

    - BEHAVIOR:
        - C: Set as gufo:Kind.
        - N+A: Report incompleteness.
        - N+I: User can set as gufo:Kind or skip.

        * Only if not reported before.
    """

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
        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

        treat_rule_n_r_t(rule_code, ontology_dataclass, configurations)

        logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


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

    rule_code = "ns_s_spe"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1
        if GUFO_NON_SORTAL not in ontology_dataclass.is_type:
            continue

        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

        treat_rule_ns_s_spe(rule_code, ontology_dataclass, list_ontology_dataclasses, graph, nodes_list, configurations)

        logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


def rule_nk_k_sup(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
    - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly one identity principle.

    - RULE: Every non-Kind gufo:Sortal (is gufo:Sortal and is not gufo:Kind) must have exactly one gufo:Kind
    as direct or indirect supertype.

    BEHAVIOR: Only executed if no direct or indirect supertype is classified as a Kind.

        P = number of directly or indirectly related supertypes that can be Kinds.

        -- RESULTS ACCORDING TO ACTIONS:
            Actions:
                - US: User can choose a class and set it as Kind or SKIP.
                - SA: Automatically set the possible class as Kind.
                - RI: Report incompleteness.

            - RI: P=0 or N+A or (P>1 and C+A)
            - SA: P=1 and C
            - US: (P=1 and N+I) or (P>1 and I)

        -- RESULTS ACCORDING TO CONFIGURATIONS:
            - C+A:
                - RI when P=0 or when P>1
                - SA when P=1
            - C+I:
                - RI when P=0
                - SA when P=1
                - US when P>1
            - N+A:
                - RI always
            - N+I:
                - RI when P=0
                - US when P>=1

        -- RESULTS ACCORDING TO NUMBER OF POSSIBILITIES:
            - P=0: always RI
            - P=1: (SA when C) or (RI when N+A) or (US when N+I)
            - P>1: (RI when A) or (US when I)

    """

    rule_code = "nk_k_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1: class has is_type Sortal and not_type Kind:
        if (GUFO_SORTAL not in ontology_dataclass.is_type) or (GUFO_KIND not in ontology_dataclass.not_type):
            continue

        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

        treat_rule_nk_k_sup(rule_code, ontology_dataclass, list_ontology_dataclasses, graph, nodes_list, configurations)

        logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


def rule_s_nsup_k(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
        - REASON: Every Sortal (types that carry or supply an identity principle) must have exactly
        one identity principle, which is provided by a Kind.

        - RULE: In complete models, every non-Kind gufo:Sortal without supertypes is a gufo:Kind.

        - BEHAVIOR:

            - Complete + Automatic: Set as gufo:Kind.
            - Complete + Interactive: Set as gufo:Kind.

            - Incomplete + Automatic: Report incompleteness.
            - Incomplete + Interactive: User can set as gufo:Kind.
        """

    rule_code = "s_nsup_k"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1: ontology_dataclass must be a gufo:Sortal and must not be a gufo:Kind
        if (GUFO_SORTAL not in ontology_dataclass.is_type) or (GUFO_KIND in ontology_dataclass.is_type):
            continue

        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

        treat_rule_s_nsup_k(rule_code, ontology_dataclass, graph, nodes_list, configurations)

        logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


def rule_ns_sub_r(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
        - REASON: Rigid types cannot specialize AntiRigid types.

        - RULE: In complete models, gufo:NonSortals with only gufo:Rigid direct subtypes are always gufo:Categories.

        - BEHAVIOR:

            - Complete (Automatic or Interactive): Set as gufo:Category.
            - Incomplete (Automatic or Interactive): Not executed.
        """

    rule_code = "ns_sub_r"

    # CONDITION 1: This rule is only executed for complete models
    if not configurations["is_complete"]:
        return

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 2: ontology_dataclass must be a gufo:NonSortals and must be able to be a gufo:Category
        if ("gufo:NonSortal" not in ontology_dataclass.is_type) or ("gufo:Category" not in ontology_dataclass.can_type):
            continue

        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

        treat_rule_ns_sub_r(rule_code, list_ontology_dataclasses, ontology_dataclass, graph, nodes_list)

        logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


def rule_nrs_ns_r(list_ontology_dataclasses, graph, nodes_list, configurations):
    """
        - REASON: Phases always occur in phase partitions.

        - RULE: In complete models, NonRigid Sortals with no sibling classes are always Roles.

        - BEHAVIOR:

            - Complete + Automatic: If can be role, Set as gufo:Role. If cannot, report incompleteness.
            - Complete + Interactive: If can be role, Set as gufo:Role. If cannot, report incompleteness.
            - Incomplete + Automatic: Report incompleteness.
            - Incomplete + Interactive: Ask user if should be set to gufo:Role. If not, report incompleteness.
        """

    rule_code = "nrs_ns_r"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1: ontology_dataclass must be able to be classified as a gufo:Role
        if "gufo:Role" not in ontology_dataclass.can_type:
            continue

        # CONDITION 2: ontology_dataclass must be a gufo:Sortals and must be a gufo:NonRigidType
        if ("gufo:Sortal" not in ontology_dataclass.is_type) \
                or ("gufo:NonRigidType" not in ontology_dataclass.is_type):
            continue

        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

        treat_rule_nrs_ns_r(rule_code, ontology_dataclass, graph, nodes_list, configurations)

        logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")


# TODO (@pedropaulofb): This rule must be improved with identification of partition sets. The rule to be created to
#  substitute this one is: Partition sets with at least one known phase must have all its components as phases.
def rule_ks_sf_in(list_ontology_dataclasses, graph, nodes_list):
    """
        - REASON: Phases always occur in phase partitions.

        - RULE: For every class classified as a gufo:Phase, there is an incompleteness if:
            (i) the Phase has no sibling classes, OR
            (ii) all its siblings are (NonSortals OR RigidType).

        - BEHAVIOR: Report incompleteness in all cases.
        """

    rule_code = "ks_sf_in"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # CONDITION 1: ontology_dataclass must be a Phase
        if "gufo:Phase" not in ontology_dataclass.is_type:
            continue

        logger.debug(f"Starting rule {rule_code} for ontology class {ontology_dataclass.uri} ...")

        treat_rule_ks_sf_in(rule_code, list_ontology_dataclasses, ontology_dataclass, graph, nodes_list)

        logger.debug(f"Rule {rule_code} successfully concluded for ontology class {ontology_dataclass.uri}.")
