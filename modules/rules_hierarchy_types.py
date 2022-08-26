""" Rules applied to the TYPES HIERARCHY. """
from modules.logger_config import initialize_logger
from modules.propagation import propagate_up, propagate_down
from modules.utils_general import count_gufo_classification_in_list
from modules.utils_graph import get_superclasses, get_subclasses


def execute_rules_gufo_type(ontology_dataclass_list, graph, nodes_list):
    """ Implements rules for gufo:Kind types

    - RULE T1: All direct or indirect superclasses of an ontology class that is a type of gufo:Kind
    cannot be a type of gufo:Sortal.

    - RULE T2: All direct or indirect subclasses of an ontology class that is a type of gufo:Kind
    cannot be a type of gufo:NonSortal.

    - RULE T3: All direct or indirect subclasses of an ontology class that is a type of gufo:Kind
    cannot be a type of gufo:Kind.

    - RULE T4: If a class has a direct or indirect superclass that is a gufo:Kind,
    all others direct or indirect superclasses are not gufo:Kinds.

    - RULE T5: All direct or indirect superclasses of an ontology class that is a type of gufo:NonSortal
    cannot be a type of gufo:Sortal.

    - RULE T6: No rigid type can have an anti-rigid type as direct or indirect superclass

    """

    logger = initialize_logger()

    for i in range(len(ontology_dataclass_list)):

        # RULES: 1, 2, 3
        if "gufo:Kind" in ontology_dataclass_list[i].is_type:
            propagate_up(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri, ["rule_t1"], 0)
            propagate_down(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri,
                           ["rule_t2", "rule_t3"], 0)

        # RULES: 4
        # if a kind
        if "gufo:Kind" in ontology_dataclass_list[i].is_type:
            # get all subclasses
            all_subclasses = get_subclasses(graph, nodes_list["all"], ontology_dataclass_list[i].uri).copy()

            # for all subclasses
            for ir41 in range(len(all_subclasses)):
                # get all superclasses
                all_superclasses_of_subclasses = get_superclasses(graph, nodes_list["all"], all_subclasses[ir41]).copy()
                # count how many of them are kinds
                counter = count_gufo_classification_in_list(ontology_dataclass_list, all_superclasses_of_subclasses,
                                                            "gufo:Kind")
                if counter != 1:
                    # TODO (@pedropaulofb): This error could be substituted by a warning and a possibility
                    #  of correction for the user
                    logger.error(f"Inconsistency detected. Number of gufo:Kinds types as supertypes "
                                 f"of {ontology_dataclass_list[i].uri} is {counter}, while it must be exactly 1.")
                # else:
                # TODO (@pedropaulofb): Modify propagate functions: create a new optional argument which is
                #  a list of classes where the propagation must not be applied. I.e., if node in list, do nothing.
                # set all supertypes as NOT KIND (except for the one which is already a kind)

        # RULES: 5
        if "gufo:NonSortal" in ontology_dataclass_list[i].is_type:
            propagate_up(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri, ["rule_t5"], 0)

        # RULES: 6
        if "gufo:RigidType" in ontology_dataclass_list[i].is_type:
            propagate_up(ontology_dataclass_list, graph, nodes_list, ontology_dataclass_list[i].uri, ["rule_t6"], 0)
