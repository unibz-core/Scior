""" Functions related to the propagation of modifications in the graph. """

from modules.utils_graph import is_root_node, is_leaf_node, get_list_root_classes, get_list_leaf_classes, \
    get_subclasses, get_superclasses, get_related_roots, get_related_leaves


def propagate_up(graph, input_node):
    """ Propagates from a specific node up to the graph's root nodes. """

    is_root = is_root_node(graph, input_node)

    if is_root == False:
        parent_nodes = get_superclasses(graph, input_node)
        # TODO (@pedropaulofb): Include actions to be performed.
        print(input_node)
        for i in range(len(parent_nodes)):
            propagate_up(graph, parent_nodes[i])
    else:
        # TODO (@pedropaulofb): Include actions to be performed.
        print(input_node)


def propagate_down(graph, input_node):
    """ Propagates from a specific node up to the graph's leaf nodes. """

    is_leaf = is_leaf_node(graph, input_node)

    if is_leaf == False:
        child_nodes = get_subclasses(graph, input_node)
        # TODO (@pedropaulofb): Include actions to be performed.
        print(input_node)
        for i in range(len(child_nodes)):
            propagate_down(graph, child_nodes[i])
    else:
        # TODO (@pedropaulofb): Include actions to be performed.
        print(input_node)


def propagate_branch_top_down(graph, input_node):
    """ Propagate from root nodes to leaf nodes the changes in the graph's branches that contains the input node. """

    root_nodes = get_related_roots(graph, input_node)

    if len(root_nodes) == 0:
        root_nodes.append(input_node)

    for i in range(len(root_nodes)):
        propagate_down(graph, root_nodes[i])


def propagate_branch_bottom_up(graph, input_node):
    """ Propagate from leaf nodes to root nodes the changes in the graph's branches that contains the input node. """

    leaf_nodes = get_related_leaves(graph, input_node)

    if len(leaf_nodes) == 0:
        leaf_nodes.append(input_node)

    for i in range(len(leaf_nodes)):
        propagate_up(graph, leaf_nodes[i])


def propagate_graph_top_down(graph):
    """ Propagates from root nodes up to the graph's leaf nodes. """

    list_root_nodes = get_list_root_classes(graph)

    for i in range(len(list_root_nodes)):
        propagate_down(graph, list_root_nodes[i])


def propagate_graph_bottom_up(graph):
    """ Propagates from leaf nodes up to the graph's root nodes. """

    list_leaf_nodes = get_list_leaf_classes(graph)

    for i in range(len(list_leaf_nodes)):
        propagate_up(graph, list_leaf_nodes[i])
