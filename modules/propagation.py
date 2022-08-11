""" Functions related to the propagation of modifications in the graph. """

from modules.utils_graph import is_root_node, is_leaf_node, get_list_root_classes, get_list_leaf_classes, \
    get_subclasses, get_superclasses


def propagate_up(graph, input_node):
    """ Propagates from a specific node up to the graph's root nodes. """

    is_root = is_root_node(graph, input_node)

    if is_root == False:
        parent_nodes = get_superclasses(graph, input_node)
        # TODO (@pedropaulofb): Include actions to be performed.
        for i in range(len(parent_nodes)):
            propagate_up(graph, parent_nodes[i])


def propagate_down(graph, input_node):
    """ Propagates from a specific node up to the graph's leaf nodes. """

    is_leaf = is_leaf_node(graph, input_node)

    if is_leaf == False:
        child_nodes = get_subclasses(graph, input_node)
        # TODO (@pedropaulofb): Include actions to be performed.
        for i in range(len(child_nodes)):
            propagate_down(graph, child_nodes[i])


def propagate_top_down(graph):
    """ Propagates from root nodes up to the graph's leaf nodes. """

    list_root_nodes = get_list_root_classes(graph)

    for i in range(len(list_root_nodes)):
        propagate_down(graph, list_root_nodes[i])


def propagate_bottom_up(graph):
    """ Propagates from leaf nodes up to the graph's root nodes. """

    list_leaf_nodes = get_list_leaf_classes(graph)

    for i in range(len(list_leaf_nodes)):
        propagate_up(graph, list_leaf_nodes[i])
