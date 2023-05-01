""" Implementation of caller/switcher for rules of group GUFO. """

import random
import string

# Used this way to avoid circular dependency
import scior.modules.initialization_arguments as args
from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_hashing import create_ontology_dataclass_list_hash
from scior.modules.rules.rule_group_gufo_leaves import execute_gufo_leaves_rules
from scior.modules.rules.rule_group_gufo_negative import execute_gufo_negative_rules
from scior.modules.rules.rule_group_gufo_positive import execute_gufo_positive_rules

LOGGER = initialize_logger()


def loop_execute_gufo_rules(ontology_dataclass_list):
    """ Executes in loop all rules of the GUFO group."""

    if args.ARGUMENTS["is_debug"]:
        loop_id = ''.join(random.choices(string.ascii_lowercase, k=4))
        LOGGER.debug(f"gUFO loop ID = {loop_id}. Executing in loop all rules from group gUFO.")

    initial_hash = create_ontology_dataclass_list_hash(ontology_dataclass_list)
    final_hash = initial_hash + 1

    while initial_hash != final_hash:
        initial_hash = final_hash

        execute_gufo_positive_rules(ontology_dataclass_list)
        execute_gufo_negative_rules(ontology_dataclass_list)
        execute_gufo_leaves_rules(ontology_dataclass_list)

        final_hash = create_ontology_dataclass_list_hash(ontology_dataclass_list)

        if args.ARGUMENTS["is_debug"]:
            if initial_hash == final_hash:
                LOGGER.debug(f"gUFO loop ID = {loop_id}. Final hash equals initial hash "
                             f"gUFO types hierarchy rules successfully concluded.")
            else:
                LOGGER.debug(f"gUFO loop ID = {loop_id}. Final hash does not equals initial hash. Re-executing rules.")
