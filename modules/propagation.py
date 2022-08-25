""" Functions related to the propagation of modifications in the graph. """
from modules.rules_hierarchy_types import perform_rule_actions
from modules.utils_graph import get_subclasses, get_superclasses, get_related_roots, get_related_leaves


def propagate_up(ontology_dataclasses_list, graph, nodes_list, input_node, action_code, call):
    """ Propagates from a specific node up to the graph's root nodes. """

    if input_node not in nodes_list["roots"]:
        parent_nodes = get_superclasses(graph, nodes_list["all"], input_node)

        # Execute actions.
        perform_rule_actions(ontology_dataclasses_list, parent_nodes, action_code)

        for i in range(len(parent_nodes)):
            call = call + 1
            propagate_up(ontology_dataclasses_list, graph, nodes_list, parent_nodes[i], action_code, call)

    else:
        if call > 0:
            perform_rule_actions(ontology_dataclasses_list, input_node, action_code)


def propagate_down(ontology_dataclasses_list, graph, nodes_list, input_node, action_code, call):
    """ Propagates from a specific node up to the graph's leaf nodes. """

    if input_node not in nodes_list["leaves"]:
        child_nodes = get_subclasses(graph, nodes_list["all"], input_node)

        # Execute actions.
        perform_rule_actions(ontology_dataclasses_list, child_nodes, action_code)

        for i in range(len(child_nodes)):
            call = call + 1
            propagate_down(ontology_dataclasses_list, graph, nodes_list, child_nodes[i], action_code, call)

    else:
        if call > 0:
            perform_rule_actions(ontology_dataclasses_list, input_node, action_code)


def propagate_branch_top_down(graph, nodes_list, input_node):
    """ Propagate from root nodes to leaf nodes the changes in the graph's branches that contains the input node. """

    related_root_nodes = get_related_roots(graph, nodes_list, input_node)

    if len(related_root_nodes) == 0:
        related_root_nodes.append(input_node)

    for i in range(len(related_root_nodes)):
        propagate_down(graph, nodes_list, related_root_nodes[i])


def propagate_branch_bottom_up(ontology_dataclasses_list, graph, nodes_list, input_node, action_code, call):
    """ Propagate from leaf nodes to root nodes the changes in the graph's branches that contains the input node. """

    related_leaf_nodes = get_related_leaves(graph, nodes_list, input_node)

    if len(related_leaf_nodes) == 0:
        related_leaf_nodes.append(input_node)

    for i in range(len(related_leaf_nodes)):
        propagate_up(ontology_dataclasses_list, graph, nodes_list, related_leaf_nodes[i], action_code, call)


def propagate_graph_top_down(graph, nodes_list):
    """ Propagates from root nodes up to the graph's leaf nodes. """

    for i in range(len(nodes_list["roots"])):
        propagate_down(graph, nodes_list, nodes_list["roots"][i])


def propagate_graph_bottom_up(ontology_dataclasses_list, graph, nodes_list, action_code, call):
    """ Propagates from leaf nodes up to the graph's root nodes. """

    for i in range(len(nodes_list["leaves"])):
        propagate_up(ontology_dataclasses_list, graph, nodes_list, nodes_list["leaves"][i], action_code, call)
