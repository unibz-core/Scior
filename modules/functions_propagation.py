""" Functions related to the propagation of modifications in the graph. """
from rdflib import URIRef


def propagate_up(graph, input_node):
    """ Propagates from a specific node up to the graph's root nodes. """

    node = URIRef(input_node)

    pass

def propagate_down(graph, input_node):
    """ Propagates from a specific node up to the graph's leaf nodes. """
    pass

def propagate_top_down(graph):
    """ Propagates from root nodes up to the graph's leaf nodes. """
    pass

def propagate_bottom_up(graph):
    """ Propagates from leaf nodes up to the graph's root nodes. """
    pass

