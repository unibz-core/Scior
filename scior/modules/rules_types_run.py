""" Rules applied to the TYPES HIERARCHY. """

from scior.modules.logger_config import initialize_logger
from scior.modules.rules.rule_group_base import execute_base_rules
from scior.modules.rules.rule_group_gufo import execute_gufo_rules
from scior.modules.utils_dataclass import generate_hash_ontology_dataclass_list

logger = initialize_logger()


def execute_rules_types(ontology_dataclass_list, ontology_graph, nodes_list, configurations):
    """ Executes all rules related to types. """

    logger.info("Starting gUFO types' hierarchy rules ...")

    # Groups of rules and their containing rules' codes. Base rules are not here included.
    list_rules_groups = ["rule_group_gufo"]

    # "rule_group_aux", "rule_group_ufo",
    # "rule_group_restriction"]  # checks incompleteness (OWA) or inconsistencies (CWA)
    # TODO (@pedropaulofb): Check if incomp/incons validation can be done only once by the end.

    # Execute rule_group_base just once
    execute_base_rules(ontology_graph)

    # Execute other groups of rules in loop
    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = initial_hash + 1

    while initial_hash != final_hash:

        initial_hash = final_hash
        for rule_group in list_rules_groups:
            switch_rule_group_execution(ontology_dataclass_list, ontology_graph, nodes_list, rule_group, configurations)
        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        if initial_hash == final_hash:
            logger.debug("Final hash equals initial hash for the dataclass list. "
                         "GUFO types hierarchy rules successfully concluded.")
        else:
            logger.debug("Final hash does not equals initial hash for the dataclass list. Re-executing rules.")

    logger.info("gUFO types' hierarchy rules concluded.")


def switch_rule_group_execution(ontology_dataclass_list, graph, nodes_list, rule_code, configurations):
    """ A switch function that calls the rule received in its parameter. """

    logger.debug(f"Acessing rule {rule_code} ...")

    if rule_code == "rule_group_gufo":
        execute_gufo_rules(ontology_dataclass_list)
    else:
        logger.error(f"Unexpected rule code ({rule_code}) received as parameter! Program aborted.")
        exit(1)

    logger.debug(f"Rule {rule_code} successfully performed.")
