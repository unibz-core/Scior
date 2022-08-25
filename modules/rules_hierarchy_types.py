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

    - RULE T4: No rigid type can have an anti-rigid type as direct or indirect superclass

    """

    for i in range(len(ontology_dataclass_list)):
        if "gufo:Kind" in ontology_dataclass_list[i].is_type:
            propagate_up(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri, ["rule_t1"], 0)
            propagate_down(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri,
                           ["rule_t2", "rule_t3"], 0)

        if "gufo:RigidType" in ontology_dataclass_list[i].is_type:
            propagate_up(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri, ["rule_t4"], 0)


def perform_rule_actions(ontology_dataclasses_list, nodes, list_actions_code):
    """ Runs actions to be performed in propagation functions.
    The actions are informed through the parameter list_actions_code.
    """

    for action in range(len(list_actions_code)):

        if list_actions_code[action] == "rule_t1":
            for i_t1 in range(len(nodes)):
                for j_t1 in range(len(ontology_dataclasses_list)):
                    if ontology_dataclasses_list[j_t1].uri == nodes[i_t1]:
                        ontology_dataclasses_list[j_t1].move_element_to_not_list("gufo:Sortal")

        if list_actions_code[action] == "rule_t2":
            for i_t2 in range(len(nodes)):
                for j_t2 in range(len(ontology_dataclasses_list)):
                    if ontology_dataclasses_list[j_t2].uri == nodes[i_t2]:
                        ontology_dataclasses_list[j_t2].move_element_to_not_list("gufo:NonSortal")

        if list_actions_code[action] == "rule_t3":
            for i_t3 in range(len(nodes)):
                for j_t3 in range(len(ontology_dataclasses_list)):
                    if ontology_dataclasses_list[j_t3].uri == nodes[i_t3]:
                        ontology_dataclasses_list[j_t3].move_element_to_not_list("gufo:Kind")

        if list_actions_code[action] == "rule_t4":
            for i_t4 in range(len(nodes)):
                for j_t4 in range(len(ontology_dataclasses_list)):
                    if ontology_dataclasses_list[j_t4].uri == nodes[i_t4]:
                        ontology_dataclasses_list[j_t4].move_element_to_not_list("gufo:AntiRigidType")
