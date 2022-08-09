""" Module for initializing data read from the ontology to be evaluated """
from rdflib import RDF, OWL

from modules.dataclass_definitions_ontology import OntologyClass


def initialize_ontology(ontology):
    """ Return an OntologyClass list of all classes in the ontology to be evaluated with its related sub-lists """

    ontology_list = []

    classes_list = get_list_of_classes(ontology)

    for i in range(len(classes_list)):
        ontology_list.append(OntologyClass(uri=classes_list[i]))

    return ontology_list


def get_list_of_classes(ontology):
    """ Returns a list of all classes as URI strings without repetitions available in a Graph """

    classes_list = []

    for sub, pred, obj in ontology:
        if (sub, RDF.type, OWL.Class) in ontology:
            # N3 necessary for returning string and [1:-1] necessary for removing <>
            classes_list.append(sub.n3()[1:-1])
        if (obj, RDF.type, OWL.Class) in ontology:
            # N3 necessary for returning string and [1:-1] necessary for removing <>
            classes_list.append(obj.n3()[1:-1])

    # Removing repetitions
    classes_list = [*set(classes_list)]

    return classes_list

# TODO (@pedropaulofb): In the end of the initializing, verify if there is any redundant URI - there must be none.
