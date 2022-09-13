""" Rules applied to the TYPES HIERARCHY. """

import time

from modules.logger_config import initialize_logger
from modules.rules_types_definitions import rule_k_s_sup, rule_s_k_sub, rule_t_k_sup, rule_ns_s_sup, rule_s_ns_sub, \
    rule_r_ar_sup, \
    rule_ar_r_sub, rule_n_r_t, rule_ns_s_spe, rule_nk_k_sup, rule_ns_k_sub, rule_s_nsup_k
from modules.utils_dataclass import generate_hash_ontology_dataclass_list


def execute_rules_types(ontology_dataclass_list, graph, nodes_list, stile):
    """ Executes all rules related to types. """
    logger = initialize_logger()
    logger.info("Starting GUFO types hierarchy rules ...")

    automatic_rules = ["k_s_sup", "s_k_sub", "t_k_sup", "ns_s_sup", "s_ns_sub", "r_ar_sup", "ar_r_sub",
                       "n_r_t", "s_nsup_k"]
    interactive_rules = ["ns_s_spe", "nk_k_sup", "ns_k_sub"]

    if stile == "automatic":
        list_of_rules = automatic_rules.copy()
    elif stile == "interactive":
        list_of_rules = automatic_rules + interactive_rules
    else:
        list_of_rules = []
        list_of_rules.append(stile)

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = 0

    # TODO (@pedropaulofb): LOOP(LOOP(automatic) + interactive)

    while initial_hash != final_hash:
        initial_hash = final_hash

        for rule in list_of_rules:
            # TODO (@pedropaulofb): Correct time counting.
            # Time counter cannot be performed here, as it includes user interactions that must be removed.
            st = time.perf_counter()

            switch_rule_execution(ontology_dataclass_list, graph, nodes_list, rule)

            et = time.perf_counter()
            elapsed_time = round((et - st), 3)
            logger.info(f"Execution time for rule {rule}: {elapsed_time} seconds.")

        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        if initial_hash == final_hash:
            logger.debug("Final hash equals initial hash for the dataclass list. "
                         "GUFO types hierarchy rules successfully concluded.")
        else:
            logger.debug("Final hash does not equals initial hash for the dataclass list. Re-executing rules.")


def switch_rule_execution(ontology_dataclass_list, graph, nodes_list, rule_code):
    """ A switch function that calls the rule received in its parameter. """

    logger = initialize_logger()

    if rule_code == "k_s_sup":
        rule_k_s_sup(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "s_k_sub":
        rule_s_k_sub(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "t_k_sup":
        rule_t_k_sup(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "ns_s_sup":
        rule_ns_s_sup(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "s_ns_sub":
        rule_s_ns_sub(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "r_ar_sup":
        rule_r_ar_sup(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "ar_r_sub":
        rule_ar_r_sub(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "n_r_t":
        rule_n_r_t(ontology_dataclass_list, nodes_list)
    elif rule_code == "ns_s_spe":
        rule_ns_s_spe(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "nk_k_sup":
        rule_nk_k_sup(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "ns_k_sub":
        rule_ns_k_sub(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "s_nsup_k":
        rule_s_nsup_k(ontology_dataclass_list, graph, nodes_list)
    else:
        logger.error("Unexpected rule code received as parameter! Program aborted.")
        exit(1)
