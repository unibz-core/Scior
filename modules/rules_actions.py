""" Execution of rules actions. """


def perform_rule_actions_types(ontology_dataclasses_list, nodes, list_actions_code):
    """ Runs actions to be performed in propagation functions.
    The actions are informed through the parameter list_actions_code.
    """

    for action in range(len(list_actions_code)):
        for i in range(len(nodes)):
            for j in range(len(ontology_dataclasses_list)):
                if ontology_dataclasses_list[j].uri == nodes[i]:

                    if list_actions_code[action] == "rule_t1":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:Sortal")

                    if list_actions_code[action] == "rule_t2":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:NonSortal")

                    if list_actions_code[action] == "rule_t3":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:Kind")

                    # if list_actions_code[action] == "rule_t4":
                    # TO BE DONE

                    if list_actions_code[action] == "rule_t5":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:Sortal")

                    if list_actions_code[action] == "rule_t6":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:AntiRigidType")
