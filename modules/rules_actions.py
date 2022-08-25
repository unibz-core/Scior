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

                    if list_actions_code[action] == "rule_t4":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:Sortal")

                    if list_actions_code[action] == "rule_t5":
                        ontology_dataclasses_list[j].move_element_to_not_list("gufo:AntiRigidType")


def perform_rule_actions_types_BAK(ontology_dataclasses_list, nodes, list_actions_code):
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
                        ontology_dataclasses_list[j_t4].move_element_to_not_list("gufo:Sortal")

        if list_actions_code[action] == "rule_t5":
            for i_t5 in range(len(nodes)):
                for j_t5 in range(len(ontology_dataclasses_list)):
                    if ontology_dataclasses_list[j_t5].uri == nodes[i_t5]:
                        ontology_dataclasses_list[j_t5].move_element_to_not_list("gufo:AntiRigidType")
