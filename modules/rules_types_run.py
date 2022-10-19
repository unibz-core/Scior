""" Rules applied to the TYPES HIERARCHY. """

from modules.logger_config import initialize_logger
from modules.rules_types_definitions import rule_k_s_sup, rule_s_k_sub, rule_t_k_sup, rule_ns_s_sup, rule_s_ns_sub, \
    rule_r_ar_sup, rule_ar_r_sub, rule_n_r_t, rule_ns_s_spe, rule_nk_k_sup, rule_s_nsup_k
from modules.utils_dataclass import generate_hash_ontology_dataclass_list
from modules.utils_general import lists_intersection


def select_list(configurations):
    """ Receives information about the arguments and returns the corresponding list of rules to be executed. """

    logger = initialize_logger()
    logger.debug("Selecting list of rules to be executed according to the provided arguments.")

    automation_level_list = []

    # List classifications according to the automation level
    list_rules_interactive = ["k_s_sup", "s_k_sub", "t_k_sup", "ns_s_sup", "s_ns_sub", "r_ar_sup", "ar_r_sub"]
    list_rules_automatic = ["k_s_sup", "s_k_sub", "t_k_sup", "ns_s_sup", "s_ns_sub", "r_ar_sup", "ar_r_sub"]

    # List selection according to the automation level
    if configurations["automation_level"] == "interactive":
        automation_level_list = list_rules_interactive
    elif configurations["automation_level"] == "automatic":
        automation_level_list = list_rules_automatic
    else:
        logger.error(f"Unknown configuration for automation level. "
                     f"Current automation level is {configurations['automation_level']}.")
        exit(1)

    # List classifications according to the ontology completeness
    list_rules_complete = ["k_s_sup", "s_k_sub", "t_k_sup", "ns_s_sup", "s_ns_sub", "r_ar_sup", "ar_r_sub"]
    list_rules_incomplete = ["k_s_sup", "s_k_sub", "t_k_sup", "ns_s_sup", "s_ns_sub", "r_ar_sup", "ar_r_sub"]

    # List selection according to the automation level
    if configurations["is_complete"]:
        completeness_list = list_rules_complete
    else:
        completeness_list = list_rules_incomplete

    selected_list = lists_intersection(automation_level_list, completeness_list)

    logger.debug(f"Selection successfully performed. "
                 f"The list of rules to be executed according the the arguments is: {selected_list}.")

    return selected_list


def execute_rules_types(ontology_dataclass_list, graph, nodes_list, configurations):
    """ Executes all rules related to types. """
    logger = initialize_logger()
    logger.info("Starting GUFO types hierarchy rules ...")

    list_not_evaluated_rules = ["n_r_t", "s_nsup_k", "ns_s_spe", "nk_k_sup"]
    list_of_rules = ["k_s_sup", "s_k_sub", "t_k_sup", "ns_s_sup", "s_ns_sub", "r_ar_sup", "ar_r_sub"]

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = 0

    # TODO (@pedropaulofb): LOOP(LOOP(automatic) + interactive)

    while initial_hash != final_hash:
        initial_hash = final_hash

        for rule in list_of_rules:
            switch_rule_execution(ontology_dataclass_list, graph, nodes_list, rule, configurations)

        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        if initial_hash == final_hash:
            logger.debug("Final hash equals initial hash for the dataclass list. "
                         "GUFO types hierarchy rules successfully concluded.")
        else:
            logger.debug("Final hash does not equals initial hash for the dataclass list. Re-executing rules.")

    logger.info("GUFO types hierarchy rules concluded.")


def switch_rule_execution(ontology_dataclass_list, graph, nodes_list, rule_code, configurations):
    """ A switch function that calls the rule received in its parameter. """

    logger = initialize_logger()

    if rule_code == "k_s_sup":
        rule_k_s_sup(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "s_k_sub":
        rule_s_k_sub(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "t_k_sup":
        rule_t_k_sup(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "ns_s_sup":
        rule_ns_s_sup(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "s_ns_sub":
        rule_s_ns_sub(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "r_ar_sup":
        rule_r_ar_sup(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "ar_r_sub":
        rule_ar_r_sub(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "n_r_t":
        rule_n_r_t(ontology_dataclass_list, nodes_list, configurations)
    elif rule_code == "ns_s_spe":
        rule_ns_s_spe(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "nk_k_sup":
        rule_nk_k_sup(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "s_nsup_k":
        rule_s_nsup_k(ontology_dataclass_list, graph, nodes_list, configurations)
    else:
        logger.error("Unexpected rule code received as parameter! Program aborted.")
        exit(1)
