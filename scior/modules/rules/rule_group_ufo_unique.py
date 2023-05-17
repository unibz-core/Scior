""" Implementation of rules from the group UFO Unique. """
import inspect

from rdflib import RDFS, URIRef, Graph

import scior.modules.initialization_arguments as args
from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.ontology_dataclassess.dataclass_moving import move_classifications_list_to_is_type, \
    move_classifications_list_to_not_type
from scior.modules.problems_treatment.treat_errors import report_error_end_of_switch
from scior.modules.problems_treatment.treat_incomplete import IncompletenessEntry, register_incompleteness
from scior.modules.problems_treatment.treat_inconsistent import report_inconsistency_case_in_rule
from scior.modules.utils_dataclass import get_dataclass_by_uri

LOGGER = initialize_logger()


def treat_result_ufo_unique(ontology_dataclass_list: list[OntologyDataClass], evaluated_dataclass: OntologyDataClass,
                            can_classes_list: list[str], is_classes_list: list[str], types_to_set_list: list[str],
                            rule_code: str, incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Treats the results from all rules from the group UFO Unique.

    :param ontology_dataclass_list: List of ontology dataclasses (all classes and is, can, and not lists of types).
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param evaluated_dataclass:
    :type evaluated_dataclass: OntologyDataClass
    :param can_classes_list: List of candidate classes to solve the rule.
    :type can_classes_list: list[str]
    :param is_classes_list: List classes that already solve the rule.
    :type is_classes_list: list[str]
    :param types_to_set_list: gUFO types that must be set to the candidates to solve the rule.
    :type types_to_set_list: list[str]
    :param rule_code: Code of the rule being handled.
    :type rule_code: str
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    current_function = inspect.stack()[0][3]

    length_is_list = len(is_classes_list)
    length_can_list = len(can_classes_list)
    can_classes_list.sort()
    is_classes_list.sort()

    if length_is_list > 1:
        # report inconsistency
        additional_message = f"A unique class was expected, but {length_is_list} were found ({is_classes_list})."
        report_inconsistency_case_in_rule(rule_code, evaluated_dataclass, additional_message)

    # IS = 1 AND CAN = 0
    elif length_is_list == 1 and length_can_list == 0:
        LOGGER.debug(f"Rule {rule_code} satisfied. No action is required.")

    # IS = 1 AND CAN > 0
    elif length_is_list == 1 and length_can_list > 0:

        # Set all classes in can list as not type.
        for can_class in can_classes_list:
            candidate_dataclass = get_dataclass_by_uri(ontology_dataclass_list, can_class)
            move_classifications_list_to_not_type(ontology_dataclass_list, candidate_dataclass, types_to_set_list,
                                                  rule_code)

    # IS = 0 AND CAN > 1
    elif length_is_list == 0 and length_can_list > 1:
        # Incompleteness found. Reporting problems_treatment and possibilities (XOR).
        additional_message = f"Solution: set exactly one class from {can_classes_list} as {types_to_set_list}."
        register_incompleteness(incompleteness_stack, rule_code, evaluated_dataclass, additional_message)

    # IS = 0 AND CAN = 1
    elif length_is_list == 0 and length_can_list == 1:

        if args.ARGUMENTS["is_owa"]:
            # Incompleteness found. Reporting problems_treatment and single possibility.
            additional_message = f"Solution: set class {can_classes_list[0]} as {types_to_set_list}."
            register_incompleteness(incompleteness_stack, rule_code, evaluated_dataclass, additional_message)

        elif args.ARGUMENTS["is_owaf"] or args.ARGUMENTS["is_cwa"]:
            # Set single candidate as desired types.
            candidate_dataclass = get_dataclass_by_uri(ontology_dataclass_list, can_classes_list[0])
            move_classifications_list_to_is_type(ontology_dataclass_list, candidate_dataclass, types_to_set_list,
                                                 rule_code)
        else:
            report_error_end_of_switch(rule_code, current_function)

    # IS = 0 AND CAN = 0
    elif length_is_list == 0 and length_can_list == 0:
        # Incompleteness found. Reporting problems_treatment no known possibilities.
        if args.ARGUMENTS["is_owa"]:
            additional_message = f"There are no known classes that can be set as {types_to_set_list} " \
                                 f"to satisfy the rule."
            register_incompleteness(incompleteness_stack, rule_code, evaluated_dataclass, additional_message)

        # Report inconsistency.
        if args.ARGUMENTS["is_cwa"]:
            additional_message = "There are no asserted classes that satisfy the rule."
            report_inconsistency_case_in_rule(rule_code, evaluated_dataclass, additional_message)

    else:
        report_error_end_of_switch(rule_code, current_function)


def run_ru01(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Executes rule RU01 from group UFO.

    Definition: Sortal(x) -> E! y (subClassOf (x,y) ^ Kind(y))
    Description: Every Sortal must have a unique identity provider, i.e., a single Kind as supertype.

    :param ontology_dataclass_list: List of ontology dataclasses (all classes and is, can, and not lists of types).
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Ontology's updated working graph
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    rule_code = "RU01"

    LOGGER.debug(f"Starting rule {rule_code}")

    is_dictionary = {}
    can_dictionary = {}

    for ontology_dataclass in ontology_dataclass_list:

        # For every Sortal
        if "Sortal" in ontology_dataclass.is_type:

            # Class to be completed or that may be incomplete
            evaluated_class = ontology_dataclass.uri

            # If dataclass not in dictionary yet, create it
            if evaluated_class not in is_dictionary.keys():
                is_dictionary[evaluated_class] = []
                can_dictionary[evaluated_class] = []

            # Collecting all superclasses
            for superclass in ontology_graph.objects(URIRef(evaluated_class), RDFS.subClassOf):
                superclass_dataclass = get_dataclass_by_uri(ontology_dataclass_list, superclass.toPython())

                # if IS Kind, add to is dictionary
                if "Kind" in superclass_dataclass.is_type:
                    is_dictionary[evaluated_class].append(superclass_dataclass.uri)
                # if CAN BE Kind, add to can dictionary (else, do nothing)
                elif "Kind" in superclass_dataclass.can_type:
                    can_dictionary[evaluated_class].append(superclass_dataclass.uri)
                # if CANNOT BE Kind, evaluate the next superclass

        # Treat after collecting all necessary information
        for evaluated in is_dictionary.keys():
            evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated)
            treat_result_ufo_unique(ontology_dataclass_list, evaluated_dataclass, can_dictionary[evaluated],
                                    is_dictionary[evaluated], ["Kind"], rule_code, incompleteness_stack)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def execute_rules_ufo_unique(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
                             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """Call execution of all rules from the group UFO Unique.

    :param ontology_dataclass_list: List of ontology dataclasses (all classes and is, can, and not lists of types).
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Ontology's updated working graph
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    LOGGER.debug("Starting execution of all rules from group UFO Unique.")

    run_ru01(ontology_dataclass_list, ontology_graph, incompleteness_stack)

    LOGGER.debug("Execution of all rules from group UFO Unique completed.")
