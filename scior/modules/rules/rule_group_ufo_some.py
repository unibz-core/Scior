""" Implementation of rules of group UFO Some. """

import inspect

from rdflib import Graph, URIRef, RDFS

import scior.modules.initialization_arguments as args
from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.ontology_dataclassess.dataclass_moving import move_classifications_list_to_is_type
from scior.modules.problems_treatment.treat_errors import report_error_end_of_switch
from scior.modules.problems_treatment.treat_incomplete import IncompletenessEntry, register_incompleteness
from scior.modules.problems_treatment.treat_inconsistent import report_inconsistency_case_in_rule
from scior.modules.utils_dataclass import get_dataclass_by_uri

LOGGER = initialize_logger()


def treat_result_ufo_some(ontology_dataclass_list: list[OntologyDataClass], evaluated_dataclass: OntologyDataClass,
                          can_classes_list: list[str], is_classes_list: list[str], types_to_set_list: list[str],
                          rule_code: str, incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Treats the results from all rules from the group UFO Some.

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
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

    is_classes_list.sort()
    can_classes_list.sort()

    if length_is_list > 0:
        LOGGER.debug(f"Rule {rule_code} satisfied for {evaluated_dataclass.uri}. No action is required.")

    # IS = 0 AND CAN > 1
    elif length_can_list > 1:
        # Incompleteness found. Reporting problems_treatment and possibilities (OR).
        additional_message = f"Solution: set one or more classes from {can_classes_list} as {types_to_set_list}."
        register_incompleteness(incompleteness_stack, rule_code, evaluated_dataclass, additional_message)

    # IS = 0 AND CAN = 1
    elif length_can_list == 1:

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
    elif length_can_list == 0:
        # Incompleteness found. Reporting problems_treatment no known possibilities.
        if args.ARGUMENTS["is_owa"]:
            additional_message = f"There are no known classes that can be set as {types_to_set_list} " \
                                 f"to satisfy the rule."
            register_incompleteness(incompleteness_stack, rule_code, evaluated_dataclass, additional_message)

        # Report inconsistency
        if args.ARGUMENTS["is_cwa"]:
            additional_message = f"There are no asserted classes that satisfy the rule."
            report_inconsistency_case_in_rule(rule_code, evaluated_dataclass, additional_message)

    else:
        report_error_end_of_switch(rule_code, current_function)


def run_rs01(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Executes rule RS01 from group UFO.

    Definition: AntiRigidType(x) ^ Sortal(x) ^ Category(y) ^ subClassOf(x,y) ->
                E z (RigidType(z) ^ Sortal(z) ^ subClassOf(x,z) ^ subClassOf(z,y))
    Description: AntiRigid Sortals cannot "directly specialize" Categories. This must be done through a Ridig Sortal.

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Updated ontology's working (RDFLib) graph on memory to be manipulated.
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    rule_code = "RS01"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y ?class_z
        WHERE {
            ?class_x rdf:type gufo:AntiRigidType .
            ?class_x rdf:type gufo:Sortal .
            ?class_y rdf:type gufo:Category .
            ?class_x rdfs:subClassOf ?class_y .
            ?class_x rdfs:subClassOf ?class_z .
            ?class_z rdfs:subClassOf ?class_y .
        } """

    query_result = ontology_graph.query(query_string)
    is_dictionary = {}
    can_dictionary = {}

    for row in query_result:

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_y.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_z.toPython()

        # If evaluated_class not in dictionary yet, create it
        if evaluated_class not in is_dictionary.keys():
            is_dictionary[evaluated_class] = []
            can_dictionary[evaluated_class] = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "RigidType" in selected_dataclass.is_type and "Sortal" in selected_dataclass.is_type:
            is_dictionary[evaluated_class].append(selected_class)

        # Creating CAN List
        elif "RigidType" not in selected_dataclass.not_type and "Sortal" not in selected_dataclass.not_type:
            can_dictionary[evaluated_class].append(selected_class)

    # Treat after collecting all necessary information
    for evaluated in is_dictionary.keys():
        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated)
        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_dictionary[evaluated],
                              is_dictionary[evaluated], ["RigidType", "Sortal"], rule_code, incompleteness_stack)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_rs02(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Executes rule RS02 from group UFO Some.

    Definition: Mixin(x) -> E y (subClassOf(y,x) ^ AntiRigidType(y))
    Description: Mixins must generalize at least one AntiRigidType.

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Updated ontology's working (RDFLib) graph on memory to be manipulated.
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    rule_code = "RS02"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdf:type gufo:Mixin .
            ?class_y rdfs:subClassOf ?class_x .
        } """

    query_result = ontology_graph.query(query_string)
    is_dictionary = {}
    can_dictionary = {}

    for row in query_result:

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        # If evaluated_class not in dictionary yet, create it
        if evaluated_class not in is_dictionary.keys():
            is_dictionary[evaluated_class] = []
            can_dictionary[evaluated_class] = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "AntiRigidType" in selected_dataclass.is_type:
            is_dictionary[evaluated_class].append(selected_class)

        # Creating CAN List
        elif "AntiRigidType" in selected_dataclass.can_type:
            can_dictionary[evaluated_class].append(selected_class)

    # Treat after collecting all necessary information
    for evaluated in is_dictionary.keys():
        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated)
        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_dictionary[evaluated],
                              is_dictionary[evaluated], ["AntiRigidType"], rule_code, incompleteness_stack)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_rs03(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Executes rule RS03 from group UFO Some.

    Definition: Mixin(x) -> E y (subClassOf(y,x) ^ RigidType(y))
    Description: Mixins must generalize at least one RigidType.

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Updated ontology's working (RDFLib) graph on memory to be manipulated.
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    rule_code = "RS03"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdf:type gufo:Mixin .
            ?class_y rdfs:subClassOf ?class_x .
        } """

    query_result = ontology_graph.query(query_string)
    is_dictionary = {}
    can_dictionary = {}

    for row in query_result:

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        # If evaluated_class not in dictionary yet, create it
        if evaluated_class not in is_dictionary.keys():
            is_dictionary[evaluated_class] = []
            can_dictionary[evaluated_class] = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "RigidType" in selected_dataclass.is_type:
            is_dictionary[evaluated_class].append(selected_class)

        # Creating CAN List
        elif "RigidType" in selected_dataclass.can_type:
            can_dictionary[evaluated_class].append(selected_class)

    # Treat after collecting all necessary information
    for evaluated in is_dictionary.keys():
        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated)
        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_dictionary[evaluated],
                              is_dictionary[evaluated], ["RigidType"], rule_code, incompleteness_stack)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_rs04(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Executes rule RS04 from group UFO Some.

    Definition: NonSortal(x) -> E y (Sortal(y) ^ (subClassOf(y,x) v shareSuperClass(x,y)))
    Description: NonSortals must be related to at least one Sortal that has a subClassOf or shareSuperClass
                relation with it.

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Updated ontology's working (RDFLib) graph on memory to be manipulated.
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    rule_code = "RS04"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        PREFIX scior: <https://purl.org/scior/>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdf:type gufo:NonSortal .
            ?class_y rdfs:subClassOf|scior:shareSuperClass ?class_x .
        } """

    query_result = ontology_graph.query(query_string)
    is_dictionary = {}
    can_dictionary = {}

    for row in query_result:

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        # If evaluated_class not in dictionary yet, create it
        if evaluated_class not in is_dictionary.keys():
            is_dictionary[evaluated_class] = []
            can_dictionary[evaluated_class] = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "Sortal" in selected_dataclass.is_type:
            is_dictionary[evaluated_class].append(selected_class)

        # Creating CAN List
        elif "Sortal" in selected_dataclass.can_type:
            can_dictionary[evaluated_class].append(selected_class)

    for evaluated in is_dictionary.keys():
        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated)
        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_dictionary[evaluated],
                              is_dictionary[evaluated], ["Sortal"], rule_code, incompleteness_stack)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_rs05(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Executes rule RS05 from group UFO Some.

    Definition: NonSortal(x) ^ Sortal(y) ^ (subClassOf(y,x) v shareSuperClass(x,y)) ->
                E z (y != z ^ Sortal(z) ^ ~shareKind(y,z) ^ (subClassOf(z,x) v shareSuperClass(x,z)))
    Description: NonSortals thar are related to one Sortal that has a subClassOf or shareSuperClass relation with it
                must be related to another Sortal that has a subClassOf or shareSuperClass relation with it.

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Updated ontology's working (RDFLib) graph on memory to be manipulated.
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    rule_code = "RS05"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        PREFIX scior: <https://purl.org/scior/>
        SELECT DISTINCT ?class_x ?class_y ?class_z
        WHERE {
            ?class_x rdf:type gufo:NonSortal .
            ?class_y rdf:type gufo:Sortal .
            ?class_y rdfs:subClassOf|scior:shareSuperClass ?class_x .
            ?class_z rdfs:subClassOf|scior:shareSuperClass ?class_x .
            FILTER (?class_y != ?class_z) .
            FILTER (NOT EXISTS {?class_y scior:shareKind ?class_z}) .
        } """

    query_result = ontology_graph.query(query_string)
    is_dictionary = {}
    can_dictionary = {}

    for row in query_result:

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_z.toPython()

        # If evaluated_class not in dictionary yet, create it
        if evaluated_class not in is_dictionary.keys():
            is_dictionary[evaluated_class] = []
            can_dictionary[evaluated_class] = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "Sortal" in selected_dataclass.is_type:
            is_dictionary[evaluated_class].append(selected_class)

        # Creating CAN List
        elif "Sortal" in selected_dataclass.can_type:
            can_dictionary[evaluated_class].append(selected_class)

    for evaluated in is_dictionary.keys():
        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated)
        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_dictionary[evaluated],
                              is_dictionary[evaluated], ["Sortal"], rule_code, incompleteness_stack)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_rs06(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Executes rule RS06 from group UFO Some.

    Definition: Role(x) ^ PhaseMixin(y) ^ subClassOf(x,y) -> E z (Phase(z) ^ subClassOf(x,z) ^ subClassOf(z,y))
    Description: A Role cannot "specialize directly"  a PhaseMixin. This must be done through a Phase.

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Updated ontology's working (RDFLib) graph on memory to be manipulated.
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    rule_code = "RS06"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y ?class_z
        WHERE {
            ?class_x rdf:type gufo:Role .
            ?class_y rdf:type gufo:PhaseMixin .
            ?class_x rdfs:subClassOf ?class_y .
            ?class_x rdfs:subClassOf ?class_z .
            ?class_z rdfs:subClassOf ?class_y .
        } """

    query_result = ontology_graph.query(query_string)
    is_dictionary = {}
    can_dictionary = {}

    for row in query_result:

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_y.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_z.toPython()

        # If evaluated_class not in dictionary yet, create it
        if evaluated_class not in is_dictionary.keys():
            is_dictionary[evaluated_class] = []
            can_dictionary[evaluated_class] = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "Phase" in selected_dataclass.is_type:
            is_dictionary[evaluated_class].append(selected_class)

        # Creating CAN List
        elif "Phase" in selected_dataclass.can_type:
            can_dictionary[evaluated_class].append(selected_class)

    for evaluated in is_dictionary.keys():
        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated)
        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_dictionary[evaluated],
                              is_dictionary[evaluated], ["Phase"], rule_code, incompleteness_stack)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_rs07(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Executes rule RS07 from group UFO Some.

    Definition: Phase(x) -> E y (Phase (y) ^ shareKind(x,y) ^ ~isSubClassOf(x,y) ^ ~isSubClassOf(y,x))
    Description: There must exist at least two Phases that share the same Kind and that do not specialize each other

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Updated ontology's working (RDFLib) graph on memory to be manipulated.
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    rule_code = "RS07"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
            PREFIX gufo: <http://purl.org/nemo/gufo#>
            PREFIX scior: <https://purl.org/scior/>
            SELECT DISTINCT ?class_x ?class_y
            WHERE {
                ?class_x rdf:type gufo:Phase .
                ?class_x scior:shareKind ?class_y .
                FILTER (?class_x != ?class_y)
            } """

    query_result = ontology_graph.query(query_string)
    is_dictionary = {}
    can_dictionary = {}

    for row in query_result:

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        # If evaluated_class not in dictionary yet, create it
        if evaluated_class not in is_dictionary.keys():
            is_dictionary[evaluated_class] = []
            can_dictionary[evaluated_class] = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # x must not specialize y
        if (URIRef(evaluated_class), RDFS.subClassOf, URIRef(selected_class)) in ontology_graph:
            is_subclass = True
        else:
            is_subclass = False

        # y must not specialize x
        if (URIRef(selected_class), RDFS.subClassOf, URIRef(evaluated_class)) in ontology_graph:
            is_superclass = True
        else:
            is_superclass = False

        if not is_subclass and not is_superclass:

            # Creating IS List
            if "Phase" in selected_dataclass.is_type:
                is_dictionary[evaluated_class].append(selected_dataclass.uri)

            # Creating CAN List
            elif "Phase" in selected_dataclass.can_type:
                can_dictionary[evaluated_class].append(selected_dataclass.uri)

    for evaluated in is_dictionary.keys():
        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated)
        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_dictionary[evaluated],
                              is_dictionary[evaluated], ["Phase"], rule_code, incompleteness_stack)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_rs08(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Executes rule RS08 from group UFO Some.

    Definition: PhaseMixin(x) -> E y (Category (y) ^ isSubClassOf(x,y))
    Description: Every PhaseMixin specializes at least one Category.

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Updated ontology's working (RDFLib) graph on memory to be manipulated.
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    rule_code = "RS08"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdf:type gufo:PhaseMixin .
            ?class_x rdfs:subClassOf ?class_y .
        } """

    query_result = ontology_graph.query(query_string)
    is_dictionary = {}
    can_dictionary = {}

    for row in query_result:

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        # If evaluated_class not in dictionary yet, create it
        if evaluated_class not in is_dictionary.keys():
            is_dictionary[evaluated_class] = []
            can_dictionary[evaluated_class] = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "Category" in selected_dataclass.is_type:
            is_dictionary[evaluated_class].append(selected_class)

        # Creating CAN List
        elif "Category" in selected_dataclass.can_type:
            can_dictionary[evaluated_class].append(selected_class)

    for evaluated in is_dictionary.keys():
        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated)
        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_dictionary[evaluated],
                              is_dictionary[evaluated], ["Category"], rule_code, incompleteness_stack)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_rs09(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry]) -> None:
    """ Executes rule RS09 from group UFO Some.

    Definition: PhaseMixin(x) ^ Category(y) ^ subClassOf(x,y) ->
                E z (PhaseMixin(z) ^ ~isSubClassOf(x,z) ^ ~isSubClassOf(z,x) ^ isSubClassOf(z,y))
    Description: There must exist at least two PhaseMixins that share the same Category
                and that do not specialize each other.

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Updated ontology's working (RDFLib) graph on memory to be manipulated.
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    rule_code = "RS09"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
            PREFIX gufo: <http://purl.org/nemo/gufo#>
            SELECT DISTINCT ?class_x ?class_y ?class_z
            WHERE {
                ?class_x rdf:type gufo:PhaseMixin .
                ?class_y rdf:type gufo:Category .
                ?class_x rdfs:subClassOf ?class_y .
                ?class_z rdfs:subClassOf ?class_y .
            } """

    query_result = ontology_graph.query(query_string)
    is_dictionary = {}
    can_dictionary = {}

    for row in query_result:

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_y.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_z.toPython()
        # Class to be used during the analysis
        related_class = row.class_x.toPython()

        # If evaluated_class not in dictionary yet, create it
        if evaluated_class not in is_dictionary.keys():
            is_dictionary[evaluated_class] = []
            can_dictionary[evaluated_class] = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Class z must not be subclass of class x
        if (URIRef(selected_class), RDFS.subClassOf, URIRef(related_class)) in ontology_graph:
            is_subclass = True
        else:
            is_subclass = False

        # Class x must not be subclass of class z
        if (URIRef(related_class), RDFS.subClassOf, URIRef(selected_class)) in ontology_graph:
            is_superclass = True
        else:
            is_superclass = False

        # Classes x and z must not be subclass or superclass of each other
        if not is_subclass and not is_superclass:

            # Creating IS List
            if "PhaseMixin" in selected_dataclass.is_type:
                is_dictionary[evaluated_class].append(selected_class)

            # Creating CAN List
            elif "PhaseMixin" in selected_dataclass.can_type:
                can_dictionary[evaluated_class].append(selected_class)

    for evaluated in is_dictionary.keys():
        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated)
        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_dictionary[evaluated],
                              is_dictionary[evaluated], ["PhaseMixin"], rule_code, incompleteness_stack)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def execute_rules_ufo_some(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
                           incompleteness_stack: list[IncompletenessEntry]) -> None:
    """Call execution all rules from the group UFO Some.

    :param ontology_dataclass_list: List with all OntologyDataClass elements, including their URIs and internal lists.
    :type ontology_dataclass_list: list[OntologyDataClass]
    :param ontology_graph: Updated ontology's working (RDFLib) graph on memory to be manipulated.
    :type ontology_graph: Graph
    :param incompleteness_stack: List of identified incompleteness to be updated if necessary.
    :type incompleteness_stack: list[IncompletenessEntry]
    """

    LOGGER.debug("Starting execution of all rules from group UFO Some.")

    run_rs01(ontology_dataclass_list, ontology_graph, incompleteness_stack)
    run_rs02(ontology_dataclass_list, ontology_graph, incompleteness_stack)
    run_rs03(ontology_dataclass_list, ontology_graph, incompleteness_stack)
    run_rs04(ontology_dataclass_list, ontology_graph, incompleteness_stack)
    run_rs05(ontology_dataclass_list, ontology_graph, incompleteness_stack)
    run_rs06(ontology_dataclass_list, ontology_graph, incompleteness_stack)
    run_rs07(ontology_dataclass_list, ontology_graph, incompleteness_stack)
    run_rs08(ontology_dataclass_list, ontology_graph, incompleteness_stack)
    run_rs09(ontology_dataclass_list, ontology_graph, incompleteness_stack)

    LOGGER.debug("Execution of all rules from group UFO Some completed.")
