""" Implementation of rules of group UFO Some. """
from rdflib import Graph, URIRef, RDFS

from scior.modules.dataclass_definitions_ontology import OntologyDataClass
from scior.modules.logger_config import initialize_logger
from scior.modules.rules.rule_group_gufo import loop_execute_gufo_rules
from scior.modules.utils_dataclass import get_dataclass_by_uri
from scior.modules.utils_deficiencies import register_incompleteness, report_error_dataclass_not_found

LOGGER = initialize_logger()


def treat_result_ufo_some(ontology_dataclass_list: list[OntologyDataClass], evaluated_dataclass: OntologyDataClass,
                          can_classes_list: list[str], is_classes_list: list[str], types_to_set_list: list[str],
                          rule_code: str, arguments: dict) -> None:
    """ Treats the results from all rules from the group UFO Some. """

    length_is_list = len(is_classes_list)
    length_can_list = len(can_classes_list)

    is_classes_list.sort()
    can_classes_list.sort()

    if length_is_list > 0:
        LOGGER.debug(f"Rule {rule_code} satisfied for {evaluated_dataclass.uri}. No action is required.")

    elif length_can_list > 1:
        # Incompleteness found. Reporting incompleteness and possibilities (OR).
        additional_message = f"Solution: set one or more classes from {can_classes_list} as {types_to_set_list}."
        register_incompleteness(rule_code, evaluated_dataclass, additional_message)

    elif length_can_list == 1:
        # Set single candidate as desired types.
        candidate_dataclass = get_dataclass_by_uri(ontology_dataclass_list, can_classes_list[0])

        if candidate_dataclass is None:
            report_error_dataclass_not_found(can_classes_list[0])

        candidate_dataclass.move_list_of_elements_to_is_list(types_to_set_list, rule_code)

    elif length_can_list == 0:
        # Incompleteness found. Reporting incompleteness no known possibilities.
        if arguments["is_owa"]:
            additional_message = f"There are no known classes that can be set as {types_to_set_list} " \
                                 f"to satisfy the rule."
            register_incompleteness(rule_code, evaluated_dataclass, additional_message)

        # Report inconsistency
        if arguments["is_cwa"]:
            LOGGER.error(f"Inconsistency detected in rule {rule_code} for class {evaluated_dataclass.uri}. "
                         f"There are no asserted classes that satisfy the rule.")
            raise ValueError(f"INCONSISTENCY FOUND IN RULE {rule_code}!")

    else:
        LOGGER.error(f"Error detected in rule {rule_code}. Unexpected else clause reached.")
        raise ValueError(f"UNEXPECTED BEHAVIOUR IN RULE {rule_code}!")

    loop_execute_gufo_rules(ontology_dataclass_list)


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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_y.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_z.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)
        if selected_dataclass is None:
            report_error_dataclass_not_found(selected_class)

        # Creating IS List
        if "RigidType" in selected_dataclass.is_type and "Sortal" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "RigidType" not in selected_dataclass.not_type and "Sortal" not in selected_dataclass.not_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["RigidType", "Sortal"],
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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)
        if selected_dataclass is None:
            report_error_dataclass_not_found(selected_class)

        # Creating IS List
        if "RigidType" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "RigidType" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["RigidType"], rule_code,
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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)
        if selected_dataclass is None:
            report_error_dataclass_not_found(selected_class)

        # Creating IS List
        if "AntiRigidType" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "AntiRigidType" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["AntiRigidType"],
                              rule_code, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")

# TODO (@pedropaulofb): Test new option and remove.
def run_r31rg1_bak(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
    """ Executes rule R31Rg1 from group UFO Some.

    Code: R31Rg1
    Definition: NonSortal(x) -> E y (Sortal(y) ^ (subClassOf(y,x) v shareSuperClass(x,y)))
    Description: NonSortals must be related to at least one Sortal that has a subClassOf or shareSuperClass
                    relation with it.
    """

    rule_code = "R31Rg1"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string_subclassof = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdf:type gufo:NonSortal .
            ?class_y rdfs:subClassOf ?class_x .
        } """

    query_string_sharesuperclass = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        PREFIX scior: <https://purl.org/scior/>
        SELECT DISTINCT ?class_x ?class_y
        WHERE {
            ?class_x rdf:type gufo:NonSortal .
            ?class_x scior:shareSuperClass ?class_y .
        } """

    query_subclassof_result = ontology_graph.query(query_string_subclassof)
    query_sharesuperclass_result = ontology_graph.query(query_string_sharesuperclass)

    for row_subclassof in query_subclassof_result:
        evaluated_class_subclassof = row_subclassof.class_x.toPython()

        for row_sharesuperclass in query_sharesuperclass_result:
            evaluated_class_sharesuperclass = row_sharesuperclass.class_x.toPython()

            if evaluated_class_subclassof != evaluated_class_sharesuperclass:
                continue

            # Class to be completed or that may be incomplete
            evaluated_class = evaluated_class_sharesuperclass
            # Class that may be used to complete the evaluated_dataclass: via superClassOf
            selected_class_superclassof = row_subclassof.class_y.toPython()
            # Class that may be used to complete the evaluated_dataclass: via shareSuperClass
            selected_class_sharesuperclass = row_sharesuperclass.class_y.toPython()

            # ACRONYMS: sco = superClassOf, ssc = sharedSuperClass

            evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
            if evaluated_dataclass is None:
                report_error_dataclass_not_found(evaluated_class)

            selected_dataclass_sco = get_dataclass_by_uri(ontology_dataclass_list, selected_class_superclassof)
            if selected_dataclass_sco is None:
                report_error_dataclass_not_found(selected_class_superclassof)

            selected_dataclass_ssc = get_dataclass_by_uri(ontology_dataclass_list, selected_class_sharesuperclass)
            if selected_dataclass_ssc is None:
                report_error_dataclass_not_found(selected_class_sharesuperclass)

            is_list_sco = []
            can_list_sco = []

            is_list_ssc = []
            can_list_ssc = []

            # Creating IS List: via superClassOf
            if "Sortal" in selected_dataclass_sco.is_type:
                is_list_sco.append(selected_dataclass_sco.uri)

            # Creating CAN List
            elif "Sortal" in selected_dataclass_sco.can_type:
                can_list_sco.append(selected_dataclass_sco.uri)

            # Creating IS List: via superClassOf
            if "Sortal" in selected_dataclass_ssc.is_type:
                is_list_ssc.append(selected_dataclass_ssc.uri)

            # Creating CAN List: via superClassOf
            if "Sortal" in selected_dataclass_ssc.can_type:
                can_list_ssc.append(selected_dataclass_ssc.uri)

            # Merging lists
            is_list = is_list_sco + is_list_ssc
            can_list = can_list_sco + can_list_ssc
            # Removing duplicates
            is_list = list(set(is_list))
            can_list = list(set(can_list))

            treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["Sortal"],
                                  rule_code, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_r31rg1(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
    """ Executes rule R31Rg1 from group UFO Some.

    Code: R31Rg1
    Definition: NonSortal(x) -> E y (Sortal(y) ^ (subClassOf(y,x) v shareSuperClass(x,y)))
    Description: NonSortals must be related to at least one Sortal that has a subClassOf or shareSuperClass
                    relation with it.
    """

    rule_code = "R31Rg1"

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
        if selected_dataclass is None:
            report_error_dataclass_not_found(selected_class)

        # Creating IS List
        if "Sortal" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "Sortal" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["Sortal"], rule_code,
                              arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")

    LOGGER.debug(f"Rule {rule_code} concluded.")


# def run_r31rg2(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
#     """ Executes rule R31Rg2 from group UFO Some.
#
#     Code: R31Rg2
#     Definition: NonSortal(x) ^ Sortal(y) ^ (subClassOf(y,x) v shareSuperClass(x,y)) ->
#                 E z (y != z ^ Sortal(z) ^ ~shareKind(y,z) ^ (subClassOf(z,x) v shareSuperClass(x,z)))
#     Description:    NonSortals thar are related to one Sortal that has a subClassOf or shareSuperClass relation with it
#                     must be related to another Sortal that has a subClassOf or shareSuperClass relation with it.
#     """
#
#     rule_code = "R31Rg2"
#
#     LOGGER.debug(f"Starting rule {rule_code}")
#
#     query_string_subclassof = """
#         PREFIX gufo: <http://purl.org/nemo/gufo#>
#         SELECT DISTINCT ?class_x ?class_y ?class_z
#         WHERE {
#             ?class_x rdf:type gufo:NonSortal .
#             ?class_y rdf:type gufo:Sortal .
#             ?class_y rdfs:subClassOf|scior:shareSuperClass ?class_x .
#         } """
#
#     query_string_sharesuperclass = """
#         PREFIX gufo: <http://purl.org/nemo/gufo#>
#         PREFIX scior: <https://purl.org/scior/>
#         SELECT DISTINCT ?class_x ?class_y ?class_z
#         WHERE {
#             ?class_x rdf:type gufo:NonSortal .
#             ?class_x scior:shareSuperClass ?class_y .
#         } """
#
#     query_subclassof_result = ontology_graph.query(query_string_subclassof)
#     query_sharesuperclass_result = ontology_graph.query(query_string_sharesuperclass)
#
#     for row_subclassof in query_subclassof_result:
#         evaluated_class_subclassof = row_subclassof.class_x.toPython()
#
#         for row_sharesuperclass in query_sharesuperclass_result:
#             evaluated_class_sharesuperclass = row_sharesuperclass.class_x.toPython()
#
#             if evaluated_class_subclassof != evaluated_class_sharesuperclass:
#                 continue
#
#             # Class to be completed or that may be incomplete
#             evaluated_class = evaluated_class_sharesuperclass
#             # Class that may be used to complete the evaluated_dataclass: via superClassOf
#             selected_class_superclassof = row_subclassof.class_y.toPython()
#             # Class that may be used to complete the evaluated_dataclass: via shareSuperClass
#             selected_class_sharesuperclass = row_sharesuperclass.class_y.toPython()
#
#             # ACRONYMS: sco = superClassOf, ssc = sharedSuperClass
#
#             evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
#             if evaluated_dataclass is None:
#                 report_error_dataclass_not_found(evaluated_class)
#
#             selected_dataclass_sco = get_dataclass_by_uri(ontology_dataclass_list, selected_class_superclassof)
#             if selected_dataclass_sco is None:
#                 report_error_dataclass_not_found(selected_class_superclassof)
#
#             selected_dataclass_ssc = get_dataclass_by_uri(ontology_dataclass_list, selected_class_sharesuperclass)
#             if selected_dataclass_ssc is None:
#                 report_error_dataclass_not_found(selected_class_sharesuperclass)
#
#             is_list_sco = []
#             can_list_sco = []
#
#             is_list_ssc = []
#             can_list_ssc = []
#
#             # Creating IS List: via superClassOf
#             if "Sortal" in selected_dataclass_sco.is_type:
#                 is_list_sco.append(selected_dataclass_sco.uri)
#
#             # Creating CAN List
#             elif "Sortal" in selected_dataclass_sco.can_type:
#                 can_list_sco.append(selected_dataclass_sco.uri)
#
#             # Creating IS List: via superClassOf
#             if "Sortal" in selected_dataclass_sco.is_type:
#                 is_list_ssc.append(selected_dataclass_sco.uri)
#
#             # Merging lists
#             is_list = is_list_sco + is_list_ssc
#             can_list = can_list_sco + can_list_ssc
#             # Removing duplicates
#             is_list = list(set(is_list))
#             can_list = list(set(can_list))
#
#             treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["Sortal"],
#                                   rule_code, arguments)
#
#     LOGGER.debug(f"Rule {rule_code} concluded.")

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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_y.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_z.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)
        if selected_dataclass is None:
            report_error_dataclass_not_found(selected_class)

        # Creating IS List
        if "Phase" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "Phase" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["Phase"], rule_code,
                              arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_r35rg(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
    """ Executes rule R35Rg from group UFO Some.

    Code: R35Rg
    Definition: Phase(x) -> E y (Phase (y) ^ shareKind(x,y) ^ ~isSubClassOf(x,y) ^ ~isSubClassOf(y,x))
    Description: There must exist at least two Phases that share the same Kind and that do not specialize each other.
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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)
        if selected_dataclass is None:
            report_error_dataclass_not_found(selected_class)

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
                                  arguments)

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

        # Class to be completed or that may be incomplete
        evaluated_class = row.class_x.toPython()
        # Class that may be used to complete the evaluated_dataclass
        selected_class = row.class_y.toPython()

        evaluated_dataclass = get_dataclass_by_uri(ontology_dataclass_list, evaluated_class)
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)
        if selected_dataclass is None:
            report_error_dataclass_not_found(selected_class)

        # Creating IS List
        if "Category" in selected_dataclass.is_type:
            is_list.append(selected_dataclass.uri)

        # Creating CAN List
        elif "Category" in selected_dataclass.can_type:
            can_list.append(selected_dataclass.uri)

        treat_result_ufo_some(ontology_dataclass_list, evaluated_dataclass, can_list, is_list, ["Category"], rule_code,
                              arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def run_r37rg(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph, arguments: dict):
    """ Executes rule R37Rg from group UFO Some.

    Code: R37Rg
    Definition: PhaseMixin(x) ^ Category(y) ^ subClassOf(x,y) ->
                E z (PhaseMixin(z) ^ ~isSubClassOf(x,z) ^ ~isSubClassOf(z,x) ^ isSubClassOf(z,y))
    Description: There must exist at least two PhaseMixins that share the same Category
                    and that do not specialize each other.
    """

    rule_code = "R37Rg"

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
        if evaluated_dataclass is None:
            report_error_dataclass_not_found(evaluated_class)

        selected_dataclass = get_dataclass_by_uri(ontology_dataclass_list, selected_class)
        if selected_dataclass is None:
            report_error_dataclass_not_found(selected_class)

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
                                  rule_code, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded.")


def execute_rules_ufo_some(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph,
                           arguments: dict) -> None:
    """Call execution all rules from the group UFO Some."""

    LOGGER.debug("Starting execution of all rules from group UFO Some.")

    run_r24rg(ontology_dataclass_list, ontology_graph, arguments)
    run_r25rg1(ontology_dataclass_list, ontology_graph, arguments)
    run_r25rg2(ontology_dataclass_list, ontology_graph, arguments)
    run_r31rg1(ontology_dataclass_list, ontology_graph, arguments)
    # run_r31rg2(ontology_dataclass_list, ontology_graph, arguments)
    run_r34rg(ontology_dataclass_list, ontology_graph, arguments)
    run_r35rg(ontology_dataclass_list, ontology_graph, arguments)
    run_r36rg(ontology_dataclass_list, ontology_graph, arguments)
    run_r37rg(ontology_dataclass_list, ontology_graph, arguments)

    LOGGER.debug("Execution of all rules from group UFO Some completed.")
