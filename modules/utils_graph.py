""" Auxiliary functions for extending and complementing RDFLib's graph functions """
from rdflib import RDF, OWL, RDFS, URIRef

from modules.logger_config import initialize_logger
from modules.utils_general import remove_duplicates, lists_subtraction


def get_list_all_classes(graph):
    """ Returns a list without repetitions with the URI of all classes in a graph. """

    list_classes = []

    for subj, pred, obj in graph.triples((None, RDF.type, OWL.Class)):
        # N3 necessary for returning string and [1:-1] necessary for removing <>
        list_classes.append(subj.n3()[1:-1])

    list_classes = remove_duplicates(list_classes)

    return list_classes


def get_superclasses(graph, all_classes, element):
    """ Returns a list of all superclasses of the given element of a graph. """

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
    """ Returns a list of all subclasses of the given element of a graph. """

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
    superclasses = get_superclasses(graph, nodes_list["all"], element)

    for i in range(len(superclasses)):
        if superclasses[i] in nodes_list["roots"]:
            related_roots.append(superclasses[i])
        else:
            temp = get_related_roots(graph, nodes_list, superclasses[i])
            related_roots.extend(temp)

    related_roots = remove_duplicates(related_roots)
    return related_roots


def get_related_leaves(graph, nodes_list, element):
    """ Return list of all leaves of the given graph that are (in)directly related to the given element."""

    related_leaves = []
    subclasses = get_subclasses(graph, nodes_list["all"], element)

    for i in range(len(subclasses)):
        if subclasses[i] in nodes_list["leaves"]:
            related_leaves.append(subclasses[i])
        else:
            temp = get_related_leaves(graph, nodes_list, subclasses[i])
            related_leaves.extend(temp)

    related_leaves = remove_duplicates(related_leaves)
    return related_leaves
