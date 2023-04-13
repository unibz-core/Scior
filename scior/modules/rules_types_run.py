""" Rules applied to the TYPES HIERARCHY. """
import time

from scior.modules.logger_config import initialize_logger
from scior.modules.rules.rule_group_base import execute_base_rules
from scior.modules.rules_types_definitions import rule_k_s_sup, rule_s_k_sub, rule_t_k_sup, rule_ns_s_sup, \
    rule_s_ns_sub, \
    rule_r_ar_sup, rule_ar_r_sub, rule_n_r_t, rule_ns_s_spe, rule_nk_k_sup, rule_s_nsup_k, rule_ns_sub_r, \
    rule_nrs_ns_r, rule_ks_sf_in, rule_sub_r_r
from scior.modules.utils_dataclass import generate_hash_ontology_dataclass_list


def execute_rules_types(ontology_dataclass_list, ontology_graph, nodes_list, configurations):
    """ Executes all rules related to types. """

    logger = initialize_logger()
    logger.info("Starting gUFO types' hierarchy rules ...")

    # Groups of rules and their containing rules' codes. Base rules are not here included.
    list_rules_groups = ["rule_group_gufo",
                         "rule_group_aux",
                         "rule_group_ufo",
                         "rule_group_restriction"]  # checks incompleteness (OWA) or inconsistencies (CWA)

    # Execution time calculation
    # TODO (@pedropaulofb): Time registers are untreated now, but must be treated.
    # TODO (@pedropaulofb): Create a class containing two types of time_registers, one for groups and other for rules.
    time_register = {"rule_group_base": 0,
                     "rule_group_gufo": 0,
                     "rule_group_aux": 0,
                     "rule_group_ufo": 0,
                     "rule_group_restriction": 0}

    # Execute rule_group_base just once

    execute_base_rules(ontology_graph)

    # Execute other groups of rules in loop

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = initial_hash + 1

    # LOOP(LOOP(automatic) + interactive)
    while initial_hash != final_hash:

        # Loop always_automatic_rules only
        while initial_hash != final_hash:
            initial_hash = final_hash
            for automatic_rule in always_automatic_rules:
                switch_rule_execution(ontology_dataclass_list, ontology_graph, nodes_list, automatic_rule,
                                      configurations,time_register)
            final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        initial_hash = final_hash
        for rule in general_rules:
            switch_rule_execution(ontology_dataclass_list, ontology_graph, nodes_list, rule, configurations,
                                  time_register)
        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        if initial_hash == final_hash:
            logger.debug("Final hash equals initial hash for the dataclass list. "
                         "GUFO types hierarchy rules successfully concluded.")
        else:
            logger.debug("Final hash does not equals initial hash for the dataclass list. Re-executing rules.")

    logger.info("gUFO types' hierarchy rules concluded.")

    return time_register


def switch_rule_execution(ontology_dataclass_list, graph, nodes_list, rule_code, configurations, time_register):
    """ A switch function that calls the rule received in its parameter. """

    logger = initialize_logger()

    logger.debug(f"Acessing rule {rule_code} ...")

    st = time.perf_counter()

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
        rule_n_r_t(ontology_dataclass_list, nodes_list, configurations)
    elif rule_code == "ns_s_spe":
        rule_ns_s_spe(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "nk_k_sup":
        rule_nk_k_sup(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "s_nsup_k":
        rule_s_nsup_k(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "ns_sub_r":
        rule_ns_sub_r(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "nrs_ns_r":
        rule_nrs_ns_r(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "ks_sf_in":
        rule_ks_sf_in(ontology_dataclass_list, graph, nodes_list)
    elif rule_code == "sub_r_r":
        rule_sub_r_r(ontology_dataclass_list, graph, nodes_list)
    else:
        logger.error(f"Unexpected rule code ({rule_code}) received as parameter! Program aborted.")
        exit(1)

    et = time.perf_counter()
    elapsed_time = et - st
    time_register[rule_code] += elapsed_time
    time_register["total_time"] += elapsed_time

    if configurations["print_time"]:
        logger.info(f"Execution time for rule {rule_code}: {round(elapsed_time, 3)} seconds.")

    logger.debug(f"Rule {rule_code} successfully performed.")

    return time_register
