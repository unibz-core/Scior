""" Implementation of rules of group UFO Some. """
from rdflib import Graph, URIRef, RDFS

from scior.modules.dataclass_definitions_ontology import OntologyDataClass
from scior.modules.logger_config import initialize_logger
from scior.modules.utils_dataclass import get_dataclass_by_uri
from scior.modules.utils_deficiencies import register_incompleteness, report_error_dataclass_not_found

LOGGER = initialize_logger()

# TODO (@pedropaulofb): Modify selected_dataclass to INCOMPLETE_CLASSES (and use all classes from the left side of the definition)! RULE 35 already OK!
def treat_result_ufo_some(ontology_dataclass_list: list[OntologyDataClass], selected_dataclass: OntologyDataClass,
                          can_classes_list: list[str], is_classes_list: list[str], types_to_set_list: list[str],
                          rule_code: str, arguments: dict) -> None:
    """ Treats the results from all rules from the group UFO Some. """

    length_is_list = len(is_classes_list)
    length_can_list = len(can_classes_list)

    is_classes_list.sort()
    can_classes_list.sort()

    if length_is_list > 0:
        LOGGER.debug(f"Rule {rule_code} satisfied. No action is required.")

    elif length_can_list > 1:
        # Incompleteness found. Reporting incompleteness and possibilities (OR).
        additional_message = f"Solution: set one or more classes from {can_classes_list} as {types_to_set_list}."
        register_incompleteness(rule_code, selected_dataclass, additional_message)

    elif length_can_list == 1:
        # Set single candidate as desired types.
        candidate_dataclass = get_dataclass_by_uri(ontology_dataclass_list, can_classes_list[0])

        if candidate_dataclass is None:
            report_error_dataclass_not_found(can_classes_list[0])

        candidate_dataclass.move_list_of_elements_to_is_list(types_to_set_list)

    elif length_can_list == 0:
        # Incompleteness found. Reporting incompleteness no known possibilities.
        if arguments["is_owa"]:
            additional_message = f"There are no known classes that can be set as {types_to_set_list} " \
                                 f"to satisfy the rule."
            register_incompleteness(rule_code, selected_dataclass, additional_message)

        # Report inconsistency
        if arguments["is_cwa"]:
            LOGGER.error(f"Inconsistency detected in rule {rule_code} for class {selected_dataclass.uri}. "
                         f"There are no asserted classes that satisfy the rule.")
            raise ValueError(f"INCONSISTENCY FOUND IN RULE {rule_code}!")

    else:
        LOGGER.error(f"Error detected in rule {rule_code}. Unexpected else clause reached.")
        raise ValueError(f"UNEXPECTED BEHAVIOUR IN RULE {rule_code}!")


def run_r24rg(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
    """ Executes rule R24Rg from group UFO.

    Code: R24Rg
    Definition: AntiRigidType(x) ^ Sortal(x) ^ Category(y) ^ subClassOf(x,y) ->
                    E z (RigidType(z) ^ Sortal(z) ^ subClassOf(x,z) ^ subClassOf(z,y))
    Description: AntiRigid Sortals cannot "directly specialize" Categories. This must be done through a Ridig Sortal.
    """

    rule_code = "R24Rg"

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

    for row in query_result:

        is_list = []
        can_list = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_z.toPython())

        if selected_dataclass is None:
            report_error_dataclass_not_found(row.class_z.toPython())

        # Creating IS List
        if "RigidType" in selected_dataclass.is_type and "Sortal" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "RigidType" not in selected_dataclass.not_type and "Sortal" not in selected_dataclass.not_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, selected_dataclass, can_list, is_list, ["RigidType", "Sortal"],
                              rule_code, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_r25rg1(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
    """ Executes rule R25Rg1 from group UFO Some.

    Code: R25Rg1
    Definition: Mixin(x) -> E y (subClassOf(y,x) ^ RigidType(y))
    Description: Mixins must generalize at least one RigidType.
    """

    rule_code = "R25Rg1"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdf:type gufo:Mixin .
            ?class_x rdfs:subClassOf ?class_y .
        } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:

        is_list = []
        can_list = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_y.toPython())

        if selected_dataclass is None:
            report_error_dataclass_not_found(row.class_y.toPython())

        # Creating IS List
        if "RigidType" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "RigidType" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, selected_dataclass, can_list, is_list, ["RigidType"], rule_code,
                              arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_r25rg2(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
    """ Executes rule R25Rg2 from group UFO Some.

    Code: R25Rg2
    Definition: Mixin(x) -> E y (subClassOf(y,x) ^ AntiRigidType(y))
    Description: Mixins must generalize at least one AntiRigidType.
    """

    rule_code = "R25Rg2"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdf:type gufo:Mixin .
            ?class_x rdfs:subClassOf ?class_y .
        } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:

        is_list = []
        can_list = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_y.toPython())

        if selected_dataclass is None:
            report_error_dataclass_not_found(row.class_y.toPython())

        # Creating IS List
        if "AntiRigidType" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "AntiRigidType" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, selected_dataclass, can_list, is_list, ["AntiRigidType"],
                              rule_code, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_r34rg(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
    """ Executes rule R34Rg from group UFO Some.

    Code: R34Rg
    Definition: Role(x) ^ PhaseMixin(y) ^ subClassOf(x,y) -> Es z (Phase(z) ^ subClassOf(x,z) ^ subClassOf(z,y))
    Description: A Role cannot "specialize directly"  a PhaseMixin. This must be done through a Phase.
    """

    rule_code = "R34Rg"

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

    for row in query_result:

        is_list = []
        can_list = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_z.toPython())

        if selected_dataclass is None:
            report_error_dataclass_not_found(row.class_z.toPython())

        # Creating IS List
        if "Phase" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "Phase" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, selected_dataclass, can_list, is_list, ["Phase"],
                              rule_code, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_r35rg(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
    """ Executes rule R35Rg from group UFO Some.

    Code: R35Rg
    Definition: Phase(x) -> E y (Phase (y) ^ shareKind(x,y) ^ ~isSubClassOf(x,y) ^ ~isSubClassOf(y,x))
    Description: There must exist at least two phases that shares the same Kind and that do not specialize each other.
    """

    rule_code = "R35Rg"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
            PREFIX gufo: <http://purl.org/nemo/gufo#> 
            PREFIX scior: <https://purl.org/scior/>
            SELECT DISTINCT ?class_x ?class_y
            WHERE {
                ?class_x rdf:type gufo:Phase .
                ?class_x scior:shareKind ?class_y .
            } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:

        is_list = []
        can_list = []

        if (URIRef(row.class_x.toPython()), RDFS.subClassOf, URIRef(row.class_y.toPython())) in ontology_graph:
            is_subclass = True
        else:
            is_subclass = False

        if (URIRef(row.class_y.toPython()), RDFS.subClassOf, URIRef(row.class_x.toPython())) in ontology_graph:
            is_superclass = True
        else:
            is_superclass = False

        if not is_subclass and not is_superclass:
            source_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_x.toPython())
            target_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_y.toPython())

            if target_dataclass is None:
                report_error_dataclass_not_found(row.class_y.toPython())

            # Creating IS List
            if "Phase" in target_dataclass.is_type:
                is_list.append(target_dataclass.uri)

            # Creating CAN List
            elif "Phase" in target_dataclass.can_type:
                can_list.append(target_dataclass.uri)

            treat_result_ufo_some(ontology_dataclass_list, source_dataclass, can_list, is_list, ["Phase"],
                                  rule_code, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_r36rg(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
    """ Executes rule R36Rg from group UFO Some.

    Code: R36Rg
    Definition: PhaseMixin(x) -> E y (Category (y) ^ isSubClassOf(x,y))
    Description: EveryPhaseMixin specialize at least one Category.
    """

    rule_code = "R36Rg"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdf:type gufo:PhaseMixin .
            ?class_x rdfs:subClassOf ?class_y .
        } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:

        is_list = []
        can_list = []

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_y.toPython())

        if selected_dataclass is None:
            report_error_dataclass_not_found(row.class_y.toPython())

        # Creating IS List
        if "Category" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "Category" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, selected_dataclass, can_list, is_list, ["Category"],
                              rule_code, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def execute_rules_ufo_some(ontology_dataclass_list, ontology_graph, arguments):
    """Call execution all rules from the group UFO Some."""

    LOGGER.debug("Starting execution of all rules from group UFO Some.")

    run_r24rg(ontology_dataclass_list, ontology_graph, arguments)
    run_r25rg1(ontology_dataclass_list, ontology_graph, arguments)
    run_r25rg2(ontology_dataclass_list, ontology_graph, arguments)
    run_r34rg(ontology_dataclass_list, ontology_graph, arguments)
    run_r35rg(ontology_dataclass_list, ontology_graph, arguments)
    run_r36rg(ontology_dataclass_list, ontology_graph, arguments)

    LOGGER.debug("Execution of all rules from group UFO Some completed.")
