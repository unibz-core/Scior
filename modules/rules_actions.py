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
        for node in range(len(list_nodes)):
            for ontology_dataclass in range(len(list_ontology_dataclasses)):

                # Condition 1
                if list_ontology_dataclasses[ontology_dataclass].uri != list_nodes[node]:
                    continue

                # Condition 2
                if list_ontology_dataclasses[ontology_dataclass].uri not in list_restrictions:

                    logger.debug(
                        f"Executing {list_actions_code[action]} in {list_ontology_dataclasses[ontology_dataclass]}...")

                    if list_actions_code[action] == "rule_t1":
                        list_ontology_dataclasses[ontology_dataclass].move_element_to_not_list("gufo:Sortal")

                    if list_actions_code[action] == "rule_t2":
                        list_ontology_dataclasses[ontology_dataclass].move_element_to_not_list("gufo:NonSortal")

                    if list_actions_code[action] == "rule_t3":
                        list_ontology_dataclasses[ontology_dataclass].move_element_to_not_list("gufo:Kind")

                    if list_actions_code[action] == "rule_t4":
                        list_ontology_dataclasses[ontology_dataclass].move_element_to_not_list("gufo:Kind")

                    if list_actions_code[action] == "rule_t5":
                        list_ontology_dataclasses[ontology_dataclass].move_element_to_not_list("gufo:Sortal")

                    if list_actions_code[action] == "rule_t6":
                        list_ontology_dataclasses[ontology_dataclass].move_element_to_not_list("gufo:AntiRigidType")

                    logger.debug(
                        f"Successfully executed {list_actions_code[action]} "
                        f"in {list_ontology_dataclasses[ontology_dataclass]}.")
