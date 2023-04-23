""" Rules applied to the TYPES HIERARCHY. """
import random
import string

from rdflib import Graph
from scior.modules.dataclass_definitions_ontology import OntologyDataClass

from scior.modules.graph_ontology import update_ontology_graph_with_gufo
from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_hashing import create_ontology_dataclasses_list_hash
from scior.modules.ontology_dataclassess.dataclass_verifications import verify_all_ontology_dataclasses_consistency
from scior.modules.problems_treatment.treat_errors import report_error_end_of_switch
from scior.modules.problems_treatment.treat_incomplete import IncompletenessEntry, print_all_incompleteness
from scior.modules.rules.rule_group_aux import execute_rules_aux
from scior.modules.rules.rule_group_base import execute_rules_base
from scior.modules.rules.rule_group_ufo_all import execute_rules_ufo_all
from scior.modules.rules.rule_group_ufo_some import execute_rules_ufo_some
from scior.modules.rules.rule_group_ufo_unique import execute_rules_ufo_unique

LOGGER = initialize_logger()


def loop_rule(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, list_rules_groups: list[str],
              incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Receives a list of rule groups to perform in loop until no modifications are found.
        AUXILIARY FUNCTION ONLY! MUST NOT BE USED OUTSIDE FUNCTION execute_rules_types.
    """

    loop_id = ''.join(random.choices(string.ascii_lowercase, k=4))

    LOGGER.debug(f"Rules loop ID = {loop_id}. Executing in loop rules groups.")

    initial_hash = create_ontology_dataclasses_list_hash(ontology_dataclass_list)
    final_hash = initial_hash + 1

    while initial_hash != final_hash:

        initial_hash = final_hash
        for rule_group in list_rules_groups:
            switch_rule_group_execution(ontology_dataclass_list, ontology_graph, rule_group, incompleteness_stack,
                                        arguments)
        final_hash = create_ontology_dataclasses_list_hash(ontology_dataclass_list)

        if initial_hash == final_hash:
            LOGGER.debug(f"Rules loop ID = {loop_id}. Final hash equals initial hash. Rules execution concluded.")
        else:
            LOGGER.debug(f"Rules loop ID = {loop_id}. Final hash does not equals initial hash. Re-executing rules.")


def switch_rule_group_execution(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
                                rule_group_code: str, incompleteness_stack: list[IncompletenessEntry],
                                arguments: dict) -> None:
    """ A switch function that calls the rule received in its parameter.
        AUXILIARY FUNCTION ONLY! MUST NOT BE USED OUTSIDE FUNCTION loop_rule.
    """

    LOGGER.debug(f"Accessing rule {rule_group_code} ...")

    if rule_group_code == "rule_group_aux":
        execute_rules_aux(ontology_graph)

    elif rule_group_code == "rule_group_ufo_all":
        execute_rules_ufo_all(ontology_dataclass_list, ontology_graph)

    elif rule_group_code == "rule_group_ufo_unique":
        execute_rules_ufo_unique(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)

    elif rule_group_code == "rule_group_ufo_some":
        execute_rules_ufo_some(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)

    else:
        report_error_end_of_switch(rule_group_code, __name__)

    update_ontology_graph_with_gufo(ontology_dataclass_list, ontology_graph)
    LOGGER.debug(f"Rule {rule_group_code} successfully performed.")


def execute_rules_types(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
                        arguments: dict) -> None:
    """ Executes all rules related to types.

        Every time that a classification is moved between lists, all gUFO rules are executed in loop.
        Implemented in (move_classification_between_type_lists).

        MUST BE CALLED ONCE FROM MAIN FILE.
    """

    LOGGER.info("Starting the execution of the inference rules. This may take some time.")

    # Verify consistency once BEFORE the rules' executions
    verify_all_ontology_dataclasses_consistency(ontology_dataclass_list)

    # Creating the incompleteness stack
    incompleteness_stack = []

    # Groups of rules and their containing rules' codes. Base rules are not here included.
    list_rules_groups = ["rule_group_aux", "rule_group_ufo_all", "rule_group_ufo_unique", "rule_group_ufo_some"]

    # Execute rule_group_base just once
    execute_rules_base(ontology_graph)

    # Execute all groups of rules in loop (except groups base and gufo) until there are no new modifications
    loop_rule(ontology_dataclass_list, ontology_graph, list_rules_groups, incompleteness_stack, arguments)

    # Verify consistency once AFTER the rules' executions
    verify_all_ontology_dataclasses_consistency(ontology_dataclass_list)

    # Print incompleteness detection results
    print_all_incompleteness(incompleteness_stack, arguments)

    LOGGER.info("Execution of inference rules successfully concluded.")
