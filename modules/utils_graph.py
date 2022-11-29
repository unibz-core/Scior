""" Auxiliary functions for extending and complementing RDFLib's graph functions """
from rdflib import RDFS, URIRef

from modules.logger_config import initialize_logger
from modules.utils_general import remove_duplicates, lists_subtraction


def get_superclasses(graph, all_classes, element):
    """ Returns a list of all direct superclasses of the given element of a graph.
        Element received as parameter is of type string.
        Analogous to function get_subclasses.
    """

    logger = initialize_logger()
    logger.debug(f"Getting superclasses of node {element}...")

    elem = URIRef(element)
    superclasses = []

    for obj in graph.objects(elem, RDFS.subClassOf):
        ins = obj.n3()[1:-1]
        if ins in all_classes:
            superclasses.append(ins)

    logger.debug(f"Superclasses of node {element} are: {superclasses}.")

    return superclasses


def get_subclasses(graph, all_classes, element):
    """ Returns a list of all direct subclasses of the given element of a graph.
        Element received as parameter is of type string.
        Analogous to function get_superclasses.
    """

    elem = URIRef(element)
    subclasses = []

    for subj in graph.subjects(RDFS.subClassOf, elem):
        ins = subj.n3()[1:-1]
        if ins in all_classes:
            subclasses.append(ins)

    return subclasses


def get_list_root_classes(graph, all_classes):
    """ Returns a list without repetitions with the URI of all root classes in a graph.
        Root classes are:  (1) classes that (2) have no SUPERclasses besides owl:Thing.
        Isolated classes are both root and leaf at the same time.
    """

    # List of all entities that have a rdfs:subclass property with other entity (participating as source)
    cond2 = []
    for subj, pred, obj in graph.triples((None, RDFS.subClassOf, None)):
        cond2.append(subj.n3()[1:-1])

    list_root_classes = lists_subtraction(all_classes, cond2)

    return list_root_classes


def get_list_leaf_classes(graph, all_classes):
    """ Returns a list without repetitions with the URI of all leaf classes in a graph.
        Leaf classes are:  (1) classes that (2) have no SUBclasses.
        Isolated classes are both root and leaf nodes at the same time.
    """

    # List of all entities that have a rdfs:subclass property with other entity (participating as target)
    cond2 = []
    for subj, pred, obj in graph.triples((None, RDFS.subClassOf, None)):
        cond2.append(obj.n3()[1:-1])

    list_leaf_nodes = lists_subtraction(all_classes, cond2)

    return list_leaf_nodes


def get_related_roots(graph, nodes_list, element):
    """ Return list of all roots of the given graph that are (in)directly related to the given element."""

    related_roots = []
    list_superclasses = get_superclasses(graph, nodes_list["all"], element)

    for superclass in list_superclasses:
        if superclass in nodes_list["roots"]:
            related_roots.append(superclass)
        else:
            temp = get_related_roots(graph, nodes_list, superclass)
            related_roots.extend(temp)

    related_roots = remove_duplicates(related_roots)
    return related_roots


def get_related_leaves(graph, nodes_list, element):
    """ Return list of all leaves of the given graph that are (in)directly related to the given element."""

    related_leaves = []
    list_subclasses = get_subclasses(graph, nodes_list["all"], element)

    for subclass in list_subclasses:
        if subclass in nodes_list["leaves"]:
            related_leaves.append(subclass)
        else:
            temp = get_related_leaves(graph, nodes_list, subclass)
            related_leaves.extend(temp)

    related_leaves = remove_duplicates(related_leaves)
    return related_leaves


def get_all_superclasses(graph, nodes_list, element):
    """ Return list of all nodes of the given graph that are direct or indirect superclasses of the given element.
        The return list DOES NOT include the own element.
        Analogous to function get_all_subclasses.
    """

    all_superclasses = []
    list_superclasses = get_superclasses(graph, nodes_list["all"], element)

    for superclass in list_superclasses:
        all_superclasses.append(superclass)
        if list_superclasses not in nodes_list["roots"]:
            temp = get_all_superclasses(graph, nodes_list, superclass)
            all_superclasses.extend(temp)

    all_superclasses = remove_duplicates(all_superclasses)

    return all_superclasses


def get_all_subclasses(graph, nodes_list, element):
    """ Return list of all nodes of the given graph that are direct or indirect subclasses of the given element.
        The return list DOES NOT include the own element.
        Analogous to function get_all_superclasses.
    """

    all_subclasses = []
    list_subclasses = get_subclasses(graph, nodes_list["all"], element)

    for subclass in list_subclasses:
        all_subclasses.append(subclass)
        if list_subclasses not in nodes_list["leaves"]:
            temp = get_all_subclasses(graph, nodes_list, subclass)
            all_subclasses.extend(temp)

    all_subclasses = remove_duplicates(all_subclasses)

    return all_subclasses


def get_all_related_nodes_inc(graph, nodes_list, node, queue=None, visited=None, related=None):
    """ Implements the BFS algorithm to return the list of all nodes of the given graph that are directly or indirectly
    related to the given element. I.e., return all nodes that are reachable from the ontologies node (element).

    The return list DOES INCLUDE the own element.
    """

    if visited is None:
        visited = []
    if queue is None:
        queue = []
    if related is None:
        related = []

    visited.append(node)
    queue.append(node)

    while queue:
        related.append(queue.pop(0))

    neighbours_list = get_subclasses(graph, nodes_list["all"], node) + get_superclasses(graph, nodes_list["all"], node)

    for neighbour in neighbours_list:
        if neighbour not in visited:
            result = get_all_related_nodes_inc(graph, nodes_list, neighbour, queue, visited, related)
            for r in result:
                if r not in related:
                    related.append(r)

    return related


def get_all_related_nodes(graph, nodes_list, node):
    """ Return the list of all nodes of the given graph that are directly or indirectly
        related to the given element. I.e., return all nodes that are reachable from the ontologies node (element).

        The return list DOES NOT INCLUDE the own element.
        """

    result = get_all_related_nodes_inc(graph, nodes_list, node)

    return result[1:]
