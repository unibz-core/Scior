""" Rules applied to the TYPES HIERARCHY. """
from scior.modules.graph_ontology import update_ontology_graph_with_gufo
from scior.modules.logger_config import initialize_logger
from scior.modules.rules.rule_group_aux import execute_rules_aux
from scior.modules.rules.rule_group_base import execute_rules_base
from scior.modules.rules.rule_group_gufo import execute_gufo_rules
from scior.modules.rules.rule_group_ufo_general import execute_rules_ufo_general
from scior.modules.rules.rule_group_ufo_specific import execute_rules_ufo_specific
from scior.modules.utils_dataclass import generate_hash_ontology_dataclass_list

logger = initialize_logger()


def execute_rules_types(ontology_dataclass_list, ontology_graph, arguments):
    """ Executes all rules related to types. """

    logger.info("Starting gUFO types' hierarchy rules ...")

    # Groups of rules and their containing rules' codes. Base rules are not here included.
    list_rules_groups = ["rule_group_gufo", "rule_group_aux", "rule_group_ufo_general"]

    # Execute rule_group_base just once
    execute_rules_base(ontology_graph)

    # Execute other groups of rules in loop
    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = initial_hash + 1

    while initial_hash != final_hash:

        initial_hash = final_hash
        for rule_group in list_rules_groups:
            switch_rule_group_execution(ontology_dataclass_list, ontology_graph, rule_group, arguments)
        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        if initial_hash == final_hash:
            logger.debug("Final hash equals initial hash for the dataclass list. "
                         "GUFO types hierarchy rules successfully concluded.")
        else:
            logger.debug("Final hash does not equals initial hash for the dataclass list. Re-executing rules.")

    logger.info("gUFO types' hierarchy rules concluded.")


def switch_rule_group_execution(ontology_dataclass_list, ontology_graph, rule_group_code, arguments):
    """ A switch function that calls the rule received in its parameter. """

    logger.debug(f"Accessing rule {rule_group_code} ...")

    if rule_group_code == "rule_group_gufo":
        execute_gufo_rules(ontology_dataclass_list)

    elif rule_group_code == "rule_group_aux":
        execute_rules_aux(ontology_graph)

    elif rule_group_code == "rule_group_ufo_general":
        execute_rules_ufo_general(ontology_dataclass_list, ontology_graph)

    elif rule_group_code == "rule_group_ufo_specific":
        execute_rules_ufo_specific(ontology_dataclass_list, ontology_graph, arguments)

    else:
        logger.error(f"Unexpected rule code ({rule_group_code}) received as parameter! Program aborted.")
        exit(1)

    update_ontology_graph_with_gufo(ontology_dataclass_list, ontology_graph)
    logger.debug(f"Rule {rule_group_code} successfully performed.")
