""" Functions related to the propagation of modifications in the graph. """
from ontcatowl.modules.logger_config import initialize_logger
from ontcatowl.modules.rules_types_actions import perform_rule_actions_types
from ontcatowl.modules.utils_graph import get_subclasses, get_superclasses


def execute_and_propagate_up(ontology_dataclasses_list, graph, nodes_list, input_node, action_code,
                             list_restrictions=None):
    """ Propagates from a specific node up to the graph's root nodes.

        Warning: the propagation begins with the input_node itself (so the action applies to it).
            If the action must not be performed in the input_node, it must be ni the list_restrictions.

        Info: The list_restrictions guarantees that the action_code is not going to be performed to that node, but it
            does not interrupt the propagation for upper nodes.
    """

    logger = initialize_logger()

    if list_restrictions is None:
        list_restrictions = []

    # Execute actions if input_node is not in list_restrictions.
    if input_node not in list_restrictions:
        perform_rule_actions_types(ontology_dataclasses_list, [input_node], action_code,
                                   list_restrictions)

    # If input_node is not a root node, propagate to upper nodes.
    if input_node not in nodes_list["roots"]:
        list_parent_nodes = get_superclasses(graph, nodes_list["all"], input_node)
        logger.debug(f"Propagating {action_code} from {input_node} to UP nodes: {list_parent_nodes}.")
        for parent_node in list_parent_nodes:
            execute_and_propagate_up(ontology_dataclasses_list, graph, nodes_list, parent_node,
                                     action_code, list_restrictions)


def execute_and_propagate_down(ontology_dataclasses_list, graph, nodes_list, input_node, action_code,
                               list_restrictions=None):
    """ Propagates from a specific node up to the graph's leaf nodes.

        Warning: the propagation begins with the input_node itself (so the action applies to it).
            If the action must not be performed in the input_node, it must be ni the list_restrictions.

        Info: The list_restrictions guarantees that the action_code is not going to be performed to that node, but it
            does not interrupt the propagation for upper nodes.
    """

    logger = initialize_logger()

    if list_restrictions is None:
        list_restrictions = []

    # Execute actions if input_node is not in list_restrictions.
    if input_node not in list_restrictions:
        perform_rule_actions_types(ontology_dataclasses_list, [input_node], action_code,
                                   list_restrictions)

    # If input_node is not a leaf node, propagate to lower nodes.
    if input_node not in nodes_list["leaves"]:
        list_child_nodes = get_subclasses(graph, nodes_list["all"], input_node)
        logger.debug(f"Propagating {action_code} from {input_node} to DOWN nodes: {list_child_nodes}.")
        for child_node in list_child_nodes:
            execute_and_propagate_down(ontology_dataclasses_list, graph, nodes_list, child_node,
                                       action_code, list_restrictions)
