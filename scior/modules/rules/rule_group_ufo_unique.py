""" Implementation of rules from the group UFO Unique. """
from rdflib import RDFS, URIRef

from scior.modules.dataclass_definitions_ontology import OntologyDataClass
from scior.modules.logger_config import initialize_logger
from scior.modules.rules_type_implementations import register_incompleteness

LOGGER = initialize_logger()


def treat_result_ufo_unique(ontology_dataclass_list: list[OntologyDataClass], selected_dataclass: OntologyDataClass,
                            can_classes_list: list[str], is_classes_list: list[str], types_to_set_list: list[str],
                            rule_code: str, arguments: dict) -> None:
    """ Treats the results from all rules from the group UFO Unique. """

    length_is_list = len(is_classes_list)
    length_can_list = len(can_classes_list)

    # GENERAL CASES

    # If is_exists_one, then no more can be allowed. Reports error if more than one.
    if length_is_list > 1:
        LOGGER.error(f"Error detected in rule {rule_code}. "
                     f"Class {selected_dataclass.uri} was expected only one from: ({is_classes_list}). "
                     f"Program aborted.")
        raise Exception(f"INCONSISTENCY FOUND IN RULE {rule_code}!")

    # If is_exists_one, then if this one is found, no more can be allowed. Move all other elements to not list.
    elif length_is_list == 1:
        # Only need to move if there are elements to be moved.
        if length_can_list != 0:
            for ontology_dataclass_sub in ontology_dataclass_list:
                if ontology_dataclass_sub.uri in can_classes_list:
                    ontology_dataclass_sub.move_list_of_elements_to_not_list(types_to_set_list)

    # OWA CASES (length_is_list == 0)
    elif arguments["is_owa"]:

        # if length_can_list > 0 and if interactive:
        # TODO (@pedropaulofb): Implement interactive actions.

        if length_can_list == 0:
            register_incompleteness(rule_code, selected_dataclass)

    # CWA CASES (length_is_list == 0)
    elif arguments["is_cwa"]:

        # if length_can_list > 1 and if interactive:
        # TODO (@pedropaulofb): Implement interactive actions.

        if length_can_list == 1:
            for ontology_dataclass_sub in ontology_dataclass_list:
                if ontology_dataclass_sub.uri == can_classes_list[0]:
                    ontology_dataclass_sub.move_list_of_elements_to_is_list(types_to_set_list)

        elif length_can_list == 0:
            LOGGER.error(f"Error detected in rule {rule_code}. "
                         f"Class {selected_dataclass.uri} was expected exactly one type but no possibility was found. "
                         f"Program aborted.")
            raise Exception(f"INCONSISTENCY FOUND IN RULE {rule_code}!")


def run_r28rg(ontology_dataclass_list, ontology_graph, arguments):
    """ Executes rule R28Rg from group UFO.

    Code: R28Rg
    Definition: Sortal(x) -> E! y (subClassOf (x,y) ^ Kind(y))
    Description: Every Sortal must have a unique identity provider, i.e., a single Kind as supertype.
    """

    rule_code = "R28Rg"

    LOGGER.debug(f"Starting rule {rule_code}")

    for ontology_dataclass in ontology_dataclass_list:
        all_supertypes = []
        can_kind_supertypes = []

        # For every Sortal
        if "Sortal" in ontology_dataclass.is_type:

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

            treat_result_ufo_unique(ontology_dataclass_list, ontology_dataclass, can_kind_supertypes,
                                    is_kind_supertypes, ["Kind"], rule_code, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded")


def execute_rules_ufo_specific(ontology_dataclass_list, ontology_graph, arguments):
    """Call execution of all rules from the group UFO Unique. """

    LOGGER.debug("Starting execution of all rules from group UFO Unique.")

    run_r28rg(ontology_dataclass_list, ontology_graph, arguments)

    LOGGER.debug("Execution of all rules from group UFO Unique completed.")

