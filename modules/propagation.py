""" Functions related to the propagation of modifications in the graph. """
from modules.rules_actions import perform_rule_actions_types
from modules.utils_graph import get_subclasses, get_superclasses


def propagate_up(ontology_dataclasses_list, graph, nodes_list, input_node, action_code, call, list_restrictions=None):
    """ Propagates from a specific node up to the graph's root nodes. """

    if list_restrictions is None:
        list_restrictions = []

    if input_node not in nodes_list["roots"]:
        list_parent_nodes = get_superclasses(graph, nodes_list["all"], input_node)

        # Execute actions if not in restriction list.
        if input_node not in list_restrictions:
            perform_rule_actions_types(ontology_dataclasses_list, list_parent_nodes, action_code, list_restrictions)

        for parent_node in list_parent_nodes:
            call = call + 1
            propagate_up(ontology_dataclasses_list, graph, nodes_list, parent_node, action_code, call,
                         list_restrictions)

    else:
        if (call > 0) and (input_node not in list_restrictions):
            perform_rule_actions_types(ontology_dataclasses_list, input_node, action_code, list_restrictions)


def propagate_down(ontology_dataclasses_list, graph, nodes_list, input_node, action_code, call, list_restrictions=None):
    """ Propagates from a specific node up to the graph's leaf nodes. """

    if list_restrictions is None:
        list_restrictions = []

    if input_node not in nodes_list["leaves"]:
        list_child_nodes = get_subclasses(graph, nodes_list["all"], input_node)

        # Execute actions if not in restriction list.
        if input_node not in list_restrictions:
            perform_rule_actions_types(ontology_dataclasses_list, list_child_nodes, action_code, list_restrictions)

        for child_node in list_child_nodes:
            call = call + 1
            propagate_down(ontology_dataclasses_list, graph, nodes_list, child_node, action_code, call,
                           list_restrictions)

    else:
        if (call > 0) and (input_node not in list_restrictions):
            perform_rule_actions_types(ontology_dataclasses_list, input_node, action_code, list_restrictions)
