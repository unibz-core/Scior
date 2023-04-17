""" Rules applied to the TYPES HIERARCHY. """
from rdflib import Graph

from scior.modules.dataclass_definitions_ontology import OntologyDataClass
from scior.modules.graph_ontology import update_ontology_graph_with_gufo
from scior.modules.logger_config import initialize_logger
from scior.modules.rules.rule_group_aux import execute_rules_aux
from scior.modules.rules.rule_group_base import execute_rules_base
from scior.modules.rules.rule_group_gufo import execute_gufo_rules
from scior.modules.rules.rule_group_ufo_all import execute_rules_ufo_all
from scior.modules.rules.rule_group_ufo_some import execute_rules_ufo_some
from scior.modules.rules.rule_group_ufo_unique import execute_rules_ufo_unique
from scior.modules.utils_dataclass import generate_hash_ontology_dataclass_list

LOGGER = initialize_logger()


def loop_rule(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, list_rules_groups: list[str],
              arguments: dict) -> None:
    """ Receives a list of rule groups to perform in loop until no modifications are found. """

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = initial_hash + 1

    while initial_hash != final_hash:

        initial_hash = final_hash
        for rule_group in list_rules_groups:
            switch_rule_group_execution(ontology_dataclass_list, ontology_graph, rule_group, arguments)
        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        if initial_hash == final_hash:
            LOGGER.debug("Final hash equals initial hash for the dataclass list. "
                         "gUFO types hierarchy rules successfully concluded.")
        else:
            LOGGER.debug("Final hash does not equals initial hash for the dataclass list. Re-executing rules.")


def execute_rules_types(ontology_dataclass_list, ontology_graph, arguments):
    """ Executes all rules related to types. """

    LOGGER.info("Starting gUFO types' hierarchy rules ...")

    # Groups of rules and their containing rules' codes. Base rules are not here included.
    list_rules_groups = ["rule_group_gufo", "rule_group_aux", "rule_group_ufo_all", "rule_group_ufo_unique",
                         "rule_group_ufo_some"]

    # Execute rule_group_base just once
    execute_rules_base(ontology_graph)

    # Loop rule_group_gufo
    loop_rule(ontology_dataclass_list, ontology_graph, ["rule_group_gufo"], arguments)

    # Execute all groups of rules in loop (except group base) until there are no new modifications
    loop_rule(ontology_dataclass_list, ontology_graph, list_rules_groups, arguments)

    LOGGER.info("gUFO types' hierarchy rules concluded.")


def switch_rule_group_execution(ontology_dataclass_list, ontology_graph, rule_group_code, arguments):
    """ A switch function that calls the rule received in its parameter. """

    LOGGER.debug(f"Accessing rule {rule_group_code} ...")

    if rule_group_code == "rule_group_gufo":
        execute_gufo_rules(ontology_dataclass_list)

    elif rule_group_code == "rule_group_aux":
        execute_rules_aux(ontology_graph)

    elif rule_group_code == "rule_group_ufo_all":
        execute_rules_ufo_all(ontology_dataclass_list, ontology_graph)

    elif rule_group_code == "rule_group_ufo_unique":
        execute_rules_ufo_unique(ontology_dataclass_list, ontology_graph, arguments)

    elif rule_group_code == "rule_group_ufo_some":
        execute_rules_ufo_some(ontology_dataclass_list, ontology_graph, arguments)

    else:
        LOGGER.error(f"Unexpected rule code ({rule_group_code}) received as parameter! Program aborted.")
        exit(1)

    update_ontology_graph_with_gufo(ontology_dataclass_list, ontology_graph)
    LOGGER.debug(f"Rule {rule_group_code} successfully performed.")
