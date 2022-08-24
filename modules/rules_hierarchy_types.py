""" Rules applied to the TYPES HIERARCHY. """

from modules.propagation import propagate_up


def rule_t1_no_sortal_supertype(ontology_dataclass_list, graph, nodes_list):
    """ All direct or indirect superclasses of an ontology class that is a type of gufo:Kind
    cannot be a type of gufo:Sortal. """

    for i in range(len(ontology_dataclass_list)):
        if "gufo:Kind" in ontology_dataclass_list[i].is_type:
            propagate_up(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri, "rule_t1", 0)
