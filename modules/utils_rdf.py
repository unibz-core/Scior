""" Auxiliary functions for extending and complementing RDFLib """
from rdflib import RDF, OWL, RDFS

from modules.utils_general import remove_duplicates, lists_subtraction


def has_prefix(graph, prefix):
    """ Return boolean indicating if the argument prefix exists in the graph"""
    result = False

    for pre, nam in graph.namespaces():
        if prefix == pre:
            result = True

    return result


def has_namespace(graph, namespace):
    """ Return boolean indicating if the argument namespace exists in the graph.
        The argument namespace must be provided without the surrounding <>"""
    result = False

    for pre, nam in graph.namespaces():
        if namespace == nam.n3()[1:-1]:
            result = True

    return result


def list_prefixes(graph):
    """ Return a list of all prefixes in the graph"""
    result = []

    for pre, nam in graph.namespaces():
        result.append(pre)

    return result


def list_namespaces(graph):
    """ Return a list of all namespaces in the graph without the surrounding <>"""
    result = []

    for pre, nam in graph.namespaces():
        # N3 necessary for returning string and [1:-1] necessary for removing <>
        result.append(nam.n3()[1:-1])

    return result


def get_list_all_classes(graph):
    """ Returns a list without repetitions with the URI of all classes in a graph. """

    list_classes = []

    for subj, pred, obj in graph.triples((None, RDF.type, OWL.Class)):
        # N3 necessary for returning string and [1:-1] necessary for removing <>
        list_classes.append(subj.n3()[1:-1])

    list_classes = remove_duplicates(list_classes)

    return list_classes


def get_list_root_classes(graph):
    """ Returns a list without repetitions with the URI of all root classes in a graph.
        Root classes are:  (1) classes that (2) have no SUPERclasses besides owl:Thing
    """

    # List of all classes
    cond1 = get_list_all_classes(graph)

    # List of all entities that have a rdfs:subclass property with other entity (participating as source)
    cond2 = []
    for subj, obj, pred in graph.triples((None, RDFS.subClassOf, None)):
        cond2.append(subj.n3()[1:-1])

    list_root_classes = lists_subtraction(cond1, cond2)

    return list_root_classes


def get_list_leaf_classes(graph):
    """ Returns a list without repetitions with the URI of all leaf classes in a graph.
        Leaf classes are:  (1) classes that (2) have no SUBclasses and that (3) are not root classes.
    """

    # List of all classes
    cond1 = get_list_all_classes(graph)

    # List of all entities that have a rdfs:subclass property with other entity (participating as target)
    cond2 = []
    for subj, obj, pred in graph.triples((None, RDFS.subClassOf, None)):
        cond2.append(pred.n3()[1:-1])

    # List of root classes
    cond3 = get_list_root_classes(graph)

    partial = lists_subtraction(cond1, cond2)
    list_leaf_nodes = lists_subtraction(partial, cond3)

    return list_leaf_nodes
