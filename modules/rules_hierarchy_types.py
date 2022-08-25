""" Rules applied to the TYPES HIERARCHY. """

from modules.propagation import propagate_up, propagate_down


def gufo_type_rules(ontology_dataclass_list, graph, nodes_list):
    """ Implements rules for gufo:Kind types

    - RULE T1: All direct or indirect superclasses of an ontology class that is a type of gufo:Kind
    cannot be a type of gufo:Sortal.

    - RULE T2: All direct or indirect subclasses of an ontology class that is a type of gufo:Kind
    cannot be a type of gufo:NonSortal.

    - RULE T3: All direct or indirect subclasses of an ontology class that is a type of gufo:Kind
    cannot be a type of gufo:Kind.

    - RUTLE T4: All direct or indirect superclasses of an ontology class that is a type of gufo:NonSortal
    cannot be a type of gufo:Sortal.

    - RULE T5: No rigid type can have an anti-rigid type as direct or indirect superclass

    """

    for i in range(len(ontology_dataclass_list)):

        if "gufo:Kind" in ontology_dataclass_list[i].is_type:
            propagate_up(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri, ["rule_t1"], 0)
            propagate_down(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri,
                           ["rule_t2", "rule_t3"], 0)

        if "gufo:NonSortal" in ontology_dataclass_list[i].is_type:
            propagate_up(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri, ["rule_t4"], 0)

        if "gufo:RigidType" in ontology_dataclass_list[i].is_type:
            propagate_up(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri, ["rule_t5"], 0)
