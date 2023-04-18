""" Implementation of rules from the group UFO Unique. """

from rdflib import RDFS, URIRef

from scior.modules.dataclass_definitions_ontology import OntologyDataClass
from scior.modules.logger_config import initialize_logger
from scior.modules.rules.rule_group_gufo import loop_execute_gufo_rules
from scior.modules.utils_dataclass import get_dataclass_by_uri
from scior.modules.utils_deficiencies import register_incompleteness, report_error_dataclass_not_found

LOGGER = initialize_logger()


def treat_result_ufo_unique(ontology_dataclass_list: list[OntologyDataClass], selected_dataclass: OntologyDataClass,
                            can_classes_list: list[str], is_classes_list: list[str], types_to_set_list: list[str],
                            rule_code: str, arguments: dict) -> None:
    """ Treats the results from all rules from the group UFO Unique. """

    length_is_list = len(is_classes_list)
    length_can_list = len(can_classes_list)
    can_classes_list.sort()
    is_classes_list.sort()

    if length_is_list > 1:
        # report inconsistency
        LOGGER.error(f"Inconsistency found for rule {rule_code} when analyzing {selected_dataclass.uri}. "
                     f"A unique class was expected, but {length_is_list} were found ({is_classes_list}). "
                     f"Program aborted.")
        raise ValueError(f"INCONSISTENCY FOUND IN RULE {rule_code}!")

    elif length_is_list == 1 and length_can_list == 0:
        LOGGER.debug(f"Rule {rule_code} satisfied. No action is required.")

    elif length_is_list == 1 and length_can_list > 0:

        # Set all classes in can list as not type.
        for can_class in can_classes_list:
            candidate_dataclass = get_dataclass_by_uri(ontology_dataclass_list, can_class)

            if candidate_dataclass is None:
                report_error_dataclass_not_found(can_class)

            candidate_dataclass.move_list_of_elements_to_not_list(types_to_set_list, rule_code)

    elif length_is_list == 0 and length_can_list > 1:
        # Incompleteness found. Reporting incompleteness and possibilities (XOR).
        additional_message = f"Solution: set exactly one class from {can_classes_list} as {types_to_set_list}."
        register_incompleteness(rule_code, selected_dataclass, additional_message)

    elif length_is_list == 0 and length_can_list == 1:
        # Set class in can list as type.
        candidate_dataclass = get_dataclass_by_uri(ontology_dataclass_list, can_classes_list[0])

        if candidate_dataclass is None:
            report_error_dataclass_not_found(can_classes_list[0])

        candidate_dataclass.move_list_of_elements_to_is_list(types_to_set_list, rule_code)

    elif length_is_list == 0 and length_can_list == 0:
        # Incompleteness found. Reporting incompleteness no known possibilities.
        if arguments["is_owa"]:
            additional_message = f"There are no known classes that can be set as {types_to_set_list} " \
                                 f"to satisfy the rule."
            register_incompleteness(rule_code, selected_dataclass, additional_message)

        # Report inconsistency.
        if arguments["is_cwa"]:
            LOGGER.error(f"Inconsistency detected in rule {rule_code} for class {selected_dataclass.uri}. "
                         f"There are no asserted classes that satisfy the rule.")
            raise ValueError(f"INCONSISTENCY FOUND IN RULE {rule_code}!")

    else:
        LOGGER.error(f"Error detected in rule {rule_code}. Unexpected else clause reached.")
        raise ValueError(f"UNEXPECTED BEHAVIOUR IN RULE {rule_code}!")

    loop_execute_gufo_rules(ontology_dataclass_list)


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

    LOGGER.debug(f"Rule {rule_code} concluded.")


def execute_rules_ufo_unique(ontology_dataclass_list, ontology_graph, arguments):
    """Call execution of all rules from the group UFO Unique. """

    LOGGER.debug("Starting execution of all rules from group UFO Unique.")

    run_r28rg(ontology_dataclass_list, ontology_graph, arguments)

    LOGGER.debug("Execution of all rules from group UFO Unique completed.")
