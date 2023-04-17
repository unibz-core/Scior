""" Implementation of rules of group UFO Specific. """
from rdflib import RDFS, URIRef

from scior.modules.dataclass_definitions_ontology import OntologyDataClass
from scior.modules.logger_config import initialize_logger
from scior.modules.rules_type_implementations import register_incompleteness

logger = initialize_logger()


def treat_specific_ufo_result(ontology_dataclass_list: list[OntologyDataClass], sortal_dataclass: OntologyDataClass,
                              can_classes_list: list[str], is_classes_list: list[str], types_to_set_list: list[str],
                              rule_code: str, arguments: dict, is_exists_one: bool = False) -> None:
    """ Treats the results from all rules from the group UFO Specific.

    Two lists are received as parameters:
        1) a list of superclasses of the ontology_dataclass that ARE (is_classes_list), and
        2) a list of superclasses of the ontology_dataclass that CAN be (can_classes_list).

    GENERAL CASES:
        If len(is_classes_list) > 1, then an error occurred and the program is aborted.
        Elif len(is_classes_list) = 1. Move elements from types_to_set_list to not list to all elements
            (if any) in can_classes_list.
        Else, the action depends on if CWA is assumed or not.
    IF OWA:
        If len(can_classes_list) > 0 then no action taken when automatic (if interactive, user can choose)
        If len(can_classes_list) = 0 then INCOMPLETENESS
    IF CWA:
        If len(can_classes_list) > 1 then no action taken when automatic (if interactive, user can choose)
        If len(can_classes_list) = 1 then set element as types_to_set_list.
        If len(can_classes_list) = 0 then INCONSISTENCY
    """

    len_is_list = len(is_classes_list)
    len_can_list = len(can_classes_list)

    # GENERAL CASES

    if is_exists_one and len_is_list > 1:
        logger.error(f"Error detected in rule {rule_code}. "
                     f"Class {sortal_dataclass.uri} was expected only one from: ({is_classes_list}). Program aborted.")
        raise Exception(f"INCONSISTENCY FOUND IN RULE {rule_code}!")

    elif len_is_list == 1:
        # Only need to move if there are elements to be moved.
        if len_can_list != 0:
            for ontology_dataclass_sub in ontology_dataclass_list:
                if ontology_dataclass_sub.uri in can_classes_list:
                    ontology_dataclass_sub.move_list_of_elements_to_not_list(types_to_set_list)

    # OWA CASES (len_is_list == 0)
    elif arguments["is_owa"]:

        # if len_can_list > 0 and if interactive:
        # TODO (@pedropaulofb): Implement interactive actions.

        if len_can_list == 0:
            register_incompleteness(rule_code, sortal_dataclass)

    # CWA CASES (len_is_list == 0)
    elif arguments["is_cwa"]:

        # if len_can_list > 1 and if interactive:
        # TODO (@pedropaulofb): Implement interactive actions.

        if len_can_list == 1:
            for ontology_dataclass_sub in ontology_dataclass_list:
                if ontology_dataclass_sub.uri == can_classes_list[0]:
                    ontology_dataclass_sub.move_list_of_elements_to_is_list(types_to_set_list)

        elif len_can_list == 0:
            logger.error(f"Error detected in rule {rule_code}. "
                         f"Class {sortal_dataclass.uri} was expected exactly one type but no possibility was found. "
                         f"Program aborted.")
            raise Exception(f"INCONSISTENCY FOUND IN RULE {rule_code}!")


def run_r28rg(ontology_dataclass_list, ontology_graph, arguments):
    """ Executes rule R28Rg from group UFO.

    Code: R28Rg
    Definition: Sortal(x) -> E! y (subClassOf (x,y) ^ Kind(y))
    Description: Every Sortal must have a unique identity provider, i.e., a single Kind as supertype.
    """

    rule_code = "R28Rg"

    logger.debug(f"Starting rule {rule_code}")

    for ontology_dataclass in ontology_dataclass_list:
        all_supertypes = []
        can_kind_supertypes = []

        # For every Sortal
        if "Sortal" in ontology_dataclass.is_type:

            # # TODO (@pedropaulofb): Remove test.
            # if "R28Cs" not in ontology_dataclass.uri:
            #     continue
            #
            # print()
            # print(ontology_dataclass.uri)

            # Creating a list of all superclasses
            for superclass in ontology_graph.objects(URIRef(ontology_dataclass.uri), RDFS.subClassOf):
                all_supertypes.append(superclass.toPython())

            is_kind_supertypes = all_supertypes.copy()

            # Removing all superclasses that are not Kinds
            for ontology_dataclass_sub in ontology_dataclass_list:
                # Creating list of supertypes that CAN BE Kind
                if (ontology_dataclass_sub.uri in all_supertypes) and ("Kind" in ontology_dataclass_sub.can_type):
                    can_kind_supertypes.append(ontology_dataclass_sub.uri)
                # Creating list of supertypes that ARE Kind
                if (ontology_dataclass_sub.uri in all_supertypes) and ("Kind" not in ontology_dataclass_sub.is_type):
                    is_kind_supertypes.remove(ontology_dataclass_sub.uri)

            # print(f"{all_supertypes =}")
            # print(f"{can_kind_supertypes =}")
            # print(f"{is_kind_supertypes =}")

            treat_specific_ufo_result(ontology_dataclass_list, ontology_dataclass, can_kind_supertypes,
                                      is_kind_supertypes, ["Kind"], rule_code, arguments, is_exists_one=True)

    logger.debug(f"Rule {rule_code} concluded")


def run_r24rg(ontology_dataclass_list, ontology_graph, arguments):
    """ Executes rule R24Rg from group UFO.

    Code: R24Rg
    Definition: AntiRigidType(x) ^ Sortal(x) ^ Category(y) ^ subClassOf(x,y) ->
                    E z (RigidType(z) ^ Sortal(z) ^ subClassOf(x,z) ^ subClassOf(z,y))
    Description: AntiRigid Sortals cannot "only directly specialize" Categories.
    """

    rule_code = "R24Rg"

    logger.debug(f"Starting rule {rule_code}")

    # for ontology_dataclass in ontology_dataclass_list:
    #     all_supertypes = []
    #     can_kind_supertypes = []
    #
    #     # For every Sortal
    #     if "Sortal" in ontology_dataclass.is_type:
    #
    #         # # TODO (@pedropaulofb): Remove test.
    #         # if "R28Cs" not in ontology_dataclass.uri:
    #         #     continue
    #         #
    #         # print()
    #         # print(ontology_dataclass.uri)
    #
    #         # Creating a list of all superclasses
    #         for superclass in ontology_graph.objects(URIRef(ontology_dataclass.uri), RDFS.subClassOf):
    #             all_supertypes.append(superclass.toPython())
    #
    #         is_kind_supertypes = all_supertypes.copy()
    #
    #         # Removing all superclasses that are not Kinds
    #         for ontology_dataclass_sub in ontology_dataclass_list:
    #             # Creating list of supertypes that CAN BE Kind
    #             if (ontology_dataclass_sub.uri in all_supertypes) and ("Kind" in ontology_dataclass_sub.can_type):
    #                 can_kind_supertypes.append(ontology_dataclass_sub.uri)
    #             # Creating list of supertypes that ARE Kind
    #             if (ontology_dataclass_sub.uri in all_supertypes) and ("Kind" not in ontology_dataclass_sub.is_type):
    #                 is_kind_supertypes.remove(ontology_dataclass_sub.uri)
    #
    #         # print(f"{all_supertypes =}")
    #         # print(f"{can_kind_supertypes =}")
    #         # print(f"{is_kind_supertypes =}")
    #
    #         treat_specific_ufo_result(ontology_dataclass_list, ontology_dataclass, can_kind_supertypes,
    #                                   is_kind_supertypes, ["Kind"], rule_code, arguments)

    logger.debug(f"Rule {rule_code} concluded")


def execute_rules_ufo_specific(ontology_dataclass_list, ontology_graph, arguments):
    """Executes all rules of the UFO Specific group."""

    run_r28rg(ontology_dataclass_list, ontology_graph, arguments)
