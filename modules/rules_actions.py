""" Execution of rules actions. """
from modules.logger_config import initialize_logger


def perform_rule_actions_types(list_ontology_dataclasses, list_nodes, list_actions_code, list_restrictions=None):
    """ Runs actions to be performed in propagation functions.
    The actions are informed through the parameter list_actions_code.
    """

    if list_restrictions is None:
        list_restrictions = []

    logger = initialize_logger()

    for action in range(len(list_actions_code)):
        for ontology_dataclass in range(len(list_ontology_dataclasses)):

            # Condition 1: ontology dataclass must be in the list of nodes
            if list_ontology_dataclasses[ontology_dataclass].uri not in list_nodes:
                continue

            # Condition 2: ontology dataclass must not be in the list of restrictions
            if list_ontology_dataclasses[ontology_dataclass].uri not in list_restrictions:

                logger.debug(
                    f"Executing {list_actions_code[action]} in {list_ontology_dataclasses[ontology_dataclass]}...")

                # Rules t1 and t5
                if (list_actions_code[action] == "rule_t1") or (list_actions_code[action] == "rule_t5"):
                    list_ontology_dataclasses[ontology_dataclass].move_element_to_not_list("gufo:Sortal")

                # Rule t2
                if list_actions_code[action] == "rule_t2":
                    list_ontology_dataclasses[ontology_dataclass].move_element_to_not_list("gufo:NonSortal")

                # Rules t3 and t4
                if (list_actions_code[action] == "rule_t3") or (list_actions_code[action] == "rule_t4"):
                    list_ontology_dataclasses[ontology_dataclass].move_element_to_not_list("gufo:Kind")

                # Rule t6
                if list_actions_code[action] == "rule_t6":
                    list_ontology_dataclasses[ontology_dataclass].move_element_to_not_list("gufo:AntiRigidType")

                logger.debug(f"Successfully executed {list_actions_code[action]} "
                             f"in {list_ontology_dataclasses[ontology_dataclass]}.")
