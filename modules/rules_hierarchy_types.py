""" Rules applied to the TYPES HIERARCHY. """

from modules.logger_config import initialize_logger
from modules.propagation import propagate_up, propagate_down
from modules.utils_general import get_list_gufo_classification
from modules.utils_graph import get_superclasses, get_subclasses


def execute_rules_types(ontology_dataclass_list, graph, nodes_list):
    """ Executes all rules related to types. """
    rules_gufo_type_enforced(ontology_dataclass_list, graph, nodes_list)


def rules_gufo_type_enforced(list_ontology_dataclasses, graph, nodes_list):
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

    for ontology_dataclass in list_ontology_dataclasses:

        # RULES 1, 2, 3, and 4 ----------------------------------------------------------------------------------------
        if "gufo:Kind" in ontology_dataclass.is_type:
            logger.debug(f"Starting rules t1, t2, t3, and t4 for gufo:Kind {ontology_dataclass.uri}...")

            # Rule 1
            propagate_up(list_ontology_dataclasses, graph, nodes_list, ontology_dataclass.uri, ["rule_t1"], 0)

            # Rules 2 and 3
            propagate_down(list_ontology_dataclasses, graph, nodes_list, ontology_dataclass.uri,
                           ["rule_t2", "rule_t3"], 0)

            # Rule 4
            # Get all subclasses
            all_subclasses = get_subclasses(graph, nodes_list["all"], ontology_dataclass.uri).copy()

            # For all subclasses
            for subclass in all_subclasses:
                # Get all superclasses
                all_superclasses_of_subclasses = get_superclasses(graph, nodes_list["all"], subclass).copy()
                # Return all superclasses that are of type Kind
                return_list = get_list_gufo_classification(list_ontology_dataclasses, all_superclasses_of_subclasses,
                                                           "gufo:Kind")
                counter = len(return_list)
                if counter != 1:
                    # TODO (@pedropaulofb): This error could be substituted by a warning and a possibility
                    #  of correction for the user
                    logger.error(f"Inconsistency detected. Number of gufo:Kinds types as supertypes "
                                 f"of {ontology_dataclass.uri} is {counter}, while it must be exactly 1.")
                else:
                    # set all supertypes as NOT KIND (except for the one that is already a kind)
                    propagate_up(list_ontology_dataclasses, graph, nodes_list, subclass, ["rule_t4"], 0,
                                 return_list)

        # RULES: 5 ----------------------------------------------------------------------------------------------------
        if "gufo:NonSortal" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule t5 for gufo:NonSortal {ontology_dataclass.uri}...")
            propagate_up(list_ontology_dataclasses, graph, nodes_list, ontology_dataclass.uri, ["rule_t5"], 0)

        # RULES: 6 ----------------------------------------------------------------------------------------------------
        if "gufo:RigidType" in ontology_dataclass.is_type:
            logger.debug(f"Starting rule t6 for gufo:RigidType {ontology_dataclass.uri}...")
            propagate_up(list_ontology_dataclasses, graph, nodes_list, ontology_dataclass.uri, ["rule_t6"], 0)
