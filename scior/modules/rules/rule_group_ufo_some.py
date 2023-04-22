""" Implementation of rules of group UFO Some. """
from rdflib import Graph, URIRef, RDFS

from scior.modules.dataclass_definitions_ontology import OntologyDataClass
from scior.modules.logger_config import initialize_logger
from scior.modules.problems_treatment.treat_incomplete import IncompletenessEntry, register_incompleteness
from scior.modules.problems_treatment.treat_inconsistent import report_inconsistency_case_in_rule
from scior.modules.utils_dataclass import get_dataclass_by_uri

LOGGER = initialize_logger()


def treat_result_ufo_some(ontology_dataclass_list: list[OntologyDataClass], evaluated_dataclass: OntologyDataClass,
                          can_classes_list: list[str], is_classes_list: list[str], types_to_set_list: list[str],
                          rule_code: str, incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Treats the results from all rules from the group UFO Some. """

    length_is_list = len(is_classes_list)
    length_can_list = len(can_classes_list)

    is_classes_list.sort()
    can_classes_list.sort()

    if length_is_list > 0:
        LOGGER.debug(f"Rule {rule_code} satisfied for {evaluated_dataclass.uri}. No action is required.")

    elif length_can_list > 1:
        # Incompleteness found. Reporting problems_treatment and possibilities (OR).
        additional_message = f"Solution: set one or more classes from {can_classes_list} as {types_to_set_list}."
        register_incompleteness(incompleteness_stack, rule_code, evaluated_dataclass, additional_message)

    elif length_can_list == 1:
        # Set single candidate as desired types.
        candidate_dataclass = get_dataclass_by_uri(ontology_dataclass_list, can_classes_list[0])
        candidate_dataclass.move_classifications_list_to_is_list(ontology_dataclass_list, types_to_set_list, rule_code)

    elif length_can_list == 0:
        # Incompleteness found. Reporting problems_treatment no known possibilities.
        if arguments["is_owa"]:
            additional_message = f"There are no known classes that can be set as {types_to_set_list} " \
                                 f"to satisfy the rule."
            register_incompleteness(incompleteness_stack, rule_code, evaluated_dataclass, additional_message)

        # Report inconsistency
        if arguments["is_cwa"]:
            report_inconsistency_case_in_rule(rule_code, evaluated_dataclass)

    else:
        LOGGER.error(f"Error detected in rule {rule_code}. Unexpected else clause reached.")
        raise ValueError(f"UNEXPECTED BEHAVIOUR IN RULE {rule_code}!")


def run_ir30(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Executes rule IR30 from group UFO.

    Code: IR30
    Definition: AntiRigidType(x) ^ Sortal(x) ^ Category(y) ^ subClassOf(x,y) ->
                    E z (RigidType(z) ^ Sortal(z) ^ subClassOf(x,z) ^ subClassOf(z,y))
    Description: AntiRigid Sortals cannot "directly specialize" Categories. This must be done through a Ridig Sortal.
    """

    rule_code = "IR30"

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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_y.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_z.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "RigidType" in selected_dataclass.is_type and "Sortal" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "RigidType" not in selected_dataclass.not_type and "Sortal" not in selected_dataclass.not_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["RigidType", "Sortal"],
                              rule_code, incompleteness_stack, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir31(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Executes rule IR31 from group UFO Some.

    Code: IR31
    Definition: Mixin(x) -> E y (subClassOf(y,x) ^ AntiRigidType(y))
    Description: Mixins must generalize at least one AntiRigidType.
    """

    rule_code = "IR31"

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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "AntiRigidType" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "AntiRigidType" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["AntiRigidType"],
                              rule_code, incompleteness_stack, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir32(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Executes rule IR32 from group UFO Some.

    Code: IR32
    Definition: Mixin(x) -> E y (subClassOf(y,x) ^ RigidType(y))
    Description: Mixins must generalize at least one RigidType.
    """

    rule_code = "IR32"

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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "RigidType" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "RigidType" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["RigidType"], rule_code,
                              incompleteness_stack, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir39(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Executes rule IR39 from group UFO Some.

    Code: IR39
    Definition: NonSortal(x) -> E y (Sortal(y) ^ (subClassOf(y,x) v shareSuperClass(x,y)))
    Description: NonSortals must be related to at least one Sortal that has a subClassOf or shareSuperClass
                    relation with it.
    """

    rule_code = "IR39"

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

    for row in query_result:

        is_list = []
        can_list = []

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "Sortal" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "Sortal" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["Sortal"], rule_code,
                              incompleteness_stack, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir40(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Executes rule IR40 from group UFO Some.

    Code: IR40
    Definition: NonSortal(x) ^ Sortal(y) ^ (subClassOf(y,x) v shareSuperClass(x,y)) ->
                E z (y != z ^ Sortal(z) ^ ~shareKind(y,z) ^ (subClassOf(z,x) v shareSuperClass(x,z)))
    Description:    NonSortals thar are related to one Sortal that has a subClassOf or shareSuperClass relation with it
                    must be related to another Sortal that has a subClassOf or shareSuperClass relation with it.
    """

    rule_code = "IR40"

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

    for row in query_result:

        is_list = []
        can_list = []

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_z.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "Sortal" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "Sortal" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["Sortal"], rule_code,
                              incompleteness_stack, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir43(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Executes rule IR43 from group UFO Some.

    Code: IR43
    Definition: Role(x) ^ PhaseMixin(y) ^ subClassOf(x,y) -> Es z (Phase(z) ^ subClassOf(x,z) ^ subClassOf(z,y))
    Description: A Role cannot "specialize directly"  a PhaseMixin. This must be done through a Phase.
    """

    rule_code = "IR43"

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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_y.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_z.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "Phase" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "Phase" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["Phase"], rule_code,
                              incompleteness_stack, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir44(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Executes rule IR44 from group UFO Some.

    Code: IR44
    Definition: Phase(x) -> E y (Phase (y) ^ shareKind(x,y) ^ ~isSubClassOf(x,y) ^ ~isSubClassOf(y,x))
    Description: There must exist at least two Phases that share the same Kind and that do not specialize each other.
    """

    rule_code = "IR44"

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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

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
                is_list.append(selected_dataclass.uri)

            # Creating CAN List
            elif "Phase" in selected_dataclass.can_type:
                can_list.append(selected_dataclass.uri)

            treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["Phase"], rule_code,
                                  incompleteness_stack, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir45(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Executes rule IR45 from group UFO Some.

    Code: IR45
    Definition: PhaseMixin(x) -> E y (Category (y) ^ isSubClassOf(x,y))
    Description: EveryPhaseMixin specialize at least one Category.
    """

    rule_code = "IR45"

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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)

        # Creating IS List
        if "Category" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "Category" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["Category"], rule_code,
                              incompleteness_stack, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_ir46(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
             incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """ Executes rule IR46 from group UFO Some.

    Code: IR46
    Definition: PhaseMixin(x) ^ Category(y) ^ subClassOf(x,y) ->
                E z (PhaseMixin(z) ^ ~isSubClassOf(x,z) ^ ~isSubClassOf(z,x) ^ isSubClassOf(z,y))
    Description: There must exist at least two PhaseMixins that share the same Category
                    and that do not specialize each other.
    """

    rule_code = "IR46"

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

    for row in query_result:

        is_list = []
        can_list = []

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_y.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_z.toPython()
        # Class to be used during the analysis
        related_class = row.class_x.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
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
                is_list.append(selected_dataclass.uri)

            # Creating CAN List
            elif "PhaseMixin" in selected_dataclass.can_type:
                can_list.append(selected_dataclass.uri)

            treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["PhaseMixin"],
                                  rule_code, incompleteness_stack, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def execute_rules_ufo_some(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
                           incompleteness_stack: list[IncompletenessEntry], arguments: dict) -> None:
    """Call execution all rules from the group UFO Some."""

    LOGGER.debug("Starting execution of all rules from group UFO Some.")

    run_ir30(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)
    run_ir31(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)
    run_ir32(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)
    run_ir39(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)
    run_ir40(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)
    run_ir43(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)
    run_ir44(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)
    run_ir45(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)
    run_ir46(ontology_dataclass_list, ontology_graph, incompleteness_stack, arguments)

    LOGGER.debug("Execution of all rules from group UFO Some completed.")
