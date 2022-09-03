""" Execution of rules actions. """
from modules.logger_config import initialize_logger


def perform_rule_actions_types(list_ontology_dataclasses, gufo_dictionary, list_nodes, action, list_restrictions=None):
    """ Runs actions to be performed in propagation functions for enforced rules.
    The actions are informed through the parameter list_actions_code.
    """

    if list_restrictions is None:
        list_restrictions = []

    logger = initialize_logger()

    for ontology_dataclass in list_ontology_dataclasses:

        # Condition 1: ontology dataclass must be in the list of nodes
        if ontology_dataclass.uri not in list_nodes:
            continue

        # Condition 2: ontology dataclass must not be in the list of restrictions
        if ontology_dataclass.uri not in list_restrictions:

            logger.debug(f"Executing {action} in {ontology_dataclass}...")

            if (action == "k_s_sup") or (action == "ns_s_sup"):
                ontology_dataclass.move_element_to_not_list("gufo:Sortal", gufo_dictionary)

            if (action == "k_ns_sub") or (action == "s_ns_sub"):
                ontology_dataclass.move_element_to_not_list("gufo:NonSortal", gufo_dictionary)

            if (action == "k_k_sub") or (action == "t_k_sup"):
                ontology_dataclass.move_element_to_not_list("gufo:Kind", gufo_dictionary)

            if action == "r_ar_sup":
                ontology_dataclass.move_element_to_not_list("gufo:AntiRigidType", gufo_dictionary)

            if action == "ar_r_sub":
                ontology_dataclass.move_element_to_not_list("gufo:RigidType", gufo_dictionary)
                ontology_dataclass.move_element_to_not_list("gufo:SemiRigidType", gufo_dictionary)

            logger.debug(f"Successfully executed {action} in {ontology_dataclass}.")
