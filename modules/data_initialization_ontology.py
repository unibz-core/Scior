""" Module for initializing data read from the ontology to be evaluated """
from rdflib import RDF, OWL

if __name__ != "__main__":

    def initialize_ontology(ontology):
        """ Return an OWLClass list of all classes in the ontology to be evaluated with its related sub-lists """

        # classes_list = get_list_of_all_classes(ontology)
        # classes_list = remove_gufo_classes(classes_list)
        # ontology_list = create_list_ontology(classes_list)

        # return ontology_list
        pass


    def get_list_of_classes(ontology):

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


    def create_list_ontology(classes_list):
        # return ontology_list
        pass
