""" Rules applied to the TYPES HIERARCHY. """

from modules.logger_config import initialize_logger
from modules.rules_types_definitions import rule_k_s_sup, rule_s_k_sub, rule_t_k_sup, rule_ns_s_sup, rule_s_ns_sub, \
    rule_r_ar_sup, rule_ar_r_sub, rule_n_r_t, rule_ns_s_spe, rule_nk_k_sup, rule_s_nsup_k, rule_ns_sub_r, \
    rule_nrs_ns_r, rule_ks_sf_in
from modules.utils_dataclass import generate_hash_ontology_dataclass_list


def execute_rules_types(ontology_dataclass_list, graph, nodes_list, configurations):
    """ Executes all rules related to types. """
    logger = initialize_logger()
    logger.info("Starting GUFO types hierarchy rules ...")

    always_automatic_rules = ["k_s_sup", "s_k_sub", "t_k_sup", "ns_s_sup", "s_ns_sub", "r_ar_sup", "ar_r_sub",
                              "ns_sub_r", "ks_sf_in"]

    general_rules = ["n_r_t", "ns_s_spe", "nk_k_sup", "s_nsup_k", "nrs_ns_r"]

    list_of_rules = always_automatic_rules + general_rules

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = 0

    # LOOP(LOOP(automatic) + interactive)
    while initial_hash != final_hash:

        # Loop always_automatic_rules only
        while initial_hash != final_hash:
            initial_hash = final_hash
            for automatic_rule in always_automatic_rules:
                switch_rule_execution(ontology_dataclass_list, graph, nodes_list, automatic_rule, configurations)
            final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        # Loop always_automatic_rules + general_rules
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

    logger.debug(f"Acessing rule {rule_code} ...")

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
    elif rule_code == "ns_sub_r":
        rule_ns_sub_r(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "nrs_ns_r":
        rule_nrs_ns_r(ontology_dataclass_list, graph, nodes_list, configurations)
    elif rule_code == "ks_sf_in":
        rule_ks_sf_in(ontology_dataclass_list, graph, nodes_list, configurations)
    else:
        logger.error(f"Unexpected rule code ({rule_code}) received as parameter! Program aborted.")
        exit(1)

    logger.debug(f"Rule {rule_code} successfully performed.")
