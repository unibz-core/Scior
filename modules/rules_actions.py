""" Actions to be performed in propagation functions. """


def perform_rule_action(ontology_dataclasses_list, nodes, list_actions_code):
    """ Runs actions to be performed in propagation functions.
    The actions are informed trough the parameter list_actions_code.
    """

    for i in range(len(list_actions_code)):

        if list_actions_code == "rule_t1":
            for i in range(len(nodes)):
                for j in range(len(ontology_dataclasses_list)):
                    if ontology_dataclasses_list[j].uri == nodes[i]:
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:Sortal")
