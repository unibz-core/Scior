""" Rules applied to the TYPES HIERARCHY. """

from modules.logger_config import initialize_logger
from modules.propagation import propagate_up, propagate_down
from modules.utils_general import get_list_gufo_classification, update_all_ontology_dataclass_list, \
    generate_hash_ontology_dataclass_list
from modules.utils_graph import get_superclasses, get_subclasses, get_all_related_nodes


# GENERAL FUNCTIONS FOR RULES -----------------------------------------------------------------------------------------

def execute_rules_types(ontology_dataclass_list, graph, nodes_list, gufo_dictionary):
    """ Executes all rules related to types. """
    logger = initialize_logger()
    logger.info("Starting GUFO types hierarchy rules ...")

    list_of_rules = ["k_s_sup", "k_ns_sub", "k_k_sub", "t_k_sup", "ns_s_sup", "r_ar_sup", "ns_s_spe"]

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = 0

    while initial_hash != final_hash:
        initial_hash = final_hash

        for rule in list_of_rules:
            switch_rule_execution(ontology_dataclass_list, graph, nodes_list, rule)
            update_all_ontology_dataclass_list(ontology_dataclass_list, gufo_dictionary)

        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

    logger.info("GUFO types hierarchy rules successfully concluded.")


def switch_rule_execution(ontology_dataclass_list, graph, nodes_list, rule_code):
    """ A switch function that calls the rule received in its parameter. """

    logger = initialize_logger()

    if rule_code == "k_s_sup":
        rule_k_s_sup(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "k_ns_sub":
        rule_k_ns_sub(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "k_k_sub":
        rule_k_k_sub(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "t_k_sup":
        rule_t_k_sup(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "ns_s_sup":
        rule_ns_s_sup(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "r_ar_sup":
        rule_r_ar_sup(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "ns_s_spe":
        rule_ns_s_spe(ontology_dataclass_list, graph, nodes_list)
    else:
        logger.error("Unexpected rule code received as parameter! Program aborted.")
        exit(1)


# IMPLEMENTATIONS OF SPECIFIC RULES -----------------------------------------------------------------------------------

def rule_k_s_sup(list_ontology_dataclasses, graph, nodes_list):
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
            propagate_up(list_ontology_dataclasses, graph, nodes_list, ontology_dataclass.uri, rule_code, 0)
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_k_ns_sub(list_ontology_dataclasses, graph, nodes_list):
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
            propagate_down(list_ontology_dataclasses, graph, nodes_list, ontology_dataclass.uri, rule_code, 0)
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_k_k_sub(list_ontology_dataclasses, graph, nodes_list):
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
            propagate_down(list_ontology_dataclasses, graph, nodes_list, ontology_dataclass.uri, rule_code, 0)
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_t_k_sup(list_ontology_dataclasses, graph, nodes_list):
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
                    propagate_up(list_ontology_dataclasses, graph, nodes_list, subclass, "t_k_sup", 0, return_list)
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_ns_s_sup(list_ontology_dataclasses, graph, nodes_list):
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
            propagate_up(list_ontology_dataclasses, graph, nodes_list, ontology_dataclass.uri, rule_code, 0)
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_r_ar_sup(list_ontology_dataclasses, graph, nodes_list):
    """
    - DESCRIPTION: No rigid type can have an anti-rigid type as direct or indirect superclass.
    - DEFAULT: Enforce
    - CODE: r_ar_sup
    """

    rule_code = "r_ar_sup"

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:
        if "gufo:RigidType" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule {rule_code} for ontology dataclass {ontology_dataclass.uri}...")
            propagate_up(list_ontology_dataclasses, graph, nodes_list, ontology_dataclass.uri, rule_code, 0)
            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")


def rule_ns_s_spe(list_ontology_dataclasses, graph, nodes_list):
    """
    - DESCRIPTION: A NonSortal must be directly or indirectly specialized by a Sortal OR it must directly or indirectly
                    specialize another NonSortal that is directly or indirectly specialized by a Sortal.
    - DEFAULT: Suggest
    - CODE: ns_s_spe
    """

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
                # TODO (@pedropaulofb): This must be treated in the following way:
                #   a) Show to user only classes that CAN BE Sortals.
                #       a1) User can set one of them as Sortal.
                #       a2) User can specialize it with a new Sortal.
                #   b) Show to user only classes that ARE NonSortals.
                #       b1) User can reclassify one of them as Sortal.
                #       b2) User can specialize it with a new Sortal.
                # With that information, the action provided by the user must be performed.

                logger.warning(f"For {ontology_dataclass.uri}, one of the following related classes "
                               f"must be a gufo:Sortal or must be specialized by a gufo:Sortal: {list_related_nodes}")

            logger.debug(f"Rule {rule_code} successfully concluded for ontology dataclass {ontology_dataclass.uri}.")
