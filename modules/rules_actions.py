""" Execution of rules actions. """
from modules.logger_config import initialize_logger


def perform_rule_actions_types(ontology_dataclasses_list, nodes, list_actions_code, list_restrictions=[]):
    """ Runs actions to be performed in propagation functions.
    The actions are informed through the parameter list_actions_code.
    """

    logger = initialize_logger()

    for action in range(len(list_actions_code)):
        for i in range(len(nodes)):
            for j in range(len(ontology_dataclasses_list)):

                # Condition 1
                if ontology_dataclasses_list[j].uri != nodes[i]:
                    continue

                # Condition 2
                if ontology_dataclasses_list[j].uri not in list_restrictions:

                    logger.debug(f"Executing {list_actions_code[action]} in {ontology_dataclasses_list[j]}...")

                    if list_actions_code[action] == "rule_t1":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:Sortal")

                    if list_actions_code[action] == "rule_t2":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:NonSortal")

                    if list_actions_code[action] == "rule_t3":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:Kind")

                    if list_actions_code[action] == "rule_t4":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:Kind")

                    if list_actions_code[action] == "rule_t5":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:Sortal")

                    if list_actions_code[action] == "rule_t6":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:AntiRigidType")

                    logger.debug(
                        f"Successfully executed {list_actions_code[action]} in {ontology_dataclasses_list[j]}.")
