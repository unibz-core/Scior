""" Execution of rules actions. """
from scior.modules.logger_config import initialize_logger


def perform_rule_actions_types(list_ontology_dataclasses, list_nodes, action, list_restrictions=None):
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
        if ontology_dataclass.uri in list_restrictions:
            continue

        # Conditions met. Executing.
        logger.debug(f"Executing {action} in {ontology_dataclass}...")

        if (action == "k_s_sup") or (action == "ns_s_sup"):
            ontology_dataclass.move_classification_to_not_list("gufo:Sortal")

        if action == "s_ns_sub":
            ontology_dataclass.move_classification_to_not_list("gufo:NonSortal")

        if (action == "s_k_sub") or (action == "t_k_sup"):
            ontology_dataclass.move_classification_to_not_list("gufo:Kind")

        if action == "r_ar_sup":
            ontology_dataclass.move_classification_to_not_list("gufo:AntiRigidType")

        if action == "ar_r_sub":
            ontology_dataclass.move_classification_to_not_list("gufo:RigidType")
            ontology_dataclass.move_classification_to_not_list("gufo:SemiRigidType")

        logger.debug(f"Successfully executed {action} in {ontology_dataclass}.")
