""" Implementation of rules from the group UFO All. """
from rdflib import Graph

from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_definitions import OntologyDataClass
from scior.modules.ontology_dataclassess.dataclass_moving import move_classification_to_is_type, \
    move_classification_to_not_type
from scior.modules.utils_dataclass import get_dataclass_by_uri

LOGGER = initialize_logger()


def run_ra01(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Executes rule RA01 from group UFO All.

        Definition: Sortal(x) ^ subClassOf(y,x) -> Sortal(y)
        Description: Everything that specialize a Sortal is also a Sortal
    """

    rule_code = "RA01"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_y
        WHERE {
            ?class_x rdf:type gufo:Sortal .
            ?class_y rdfs:subClassOf ?class_x .
        } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        new_sortal = get_dataclass_by_uri(ontology_dataclass_list, row.class_y.toPython())
        move_classification_to_is_type(ontology_dataclass_list, new_sortal, "Sortal", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ra02(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Executes rule RA02 from group UFO All.

        Definition: RigidType(x) ^ subClassOf(x,y) -> ~AntiRigidType(y)
    Description: AntiRigid types cannot generalize Rigid types.
    """

    rule_code = "RA02"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
    PREFIX gufo: <http://purl.org/nemo/gufo#>
    SELECT DISTINCT ?class_y
    WHERE {
        ?class_x rdf:type gufo:RigidType .
        ?class_x rdfs:subClassOf ?class_y .
    } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        ontology_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_y.toPython())
        move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ra03(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Executes rule RA03 from group UFO All.

        Definition: SemiRigidType(x) ^ subClassOf(x,y) -> ~AntiRigidType(y)
    Description: AntiRigid types cannot generalize SemiRigid types.
    """

    rule_code = "RA03"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
    PREFIX gufo: <http://purl.org/nemo/gufo#>
    SELECT DISTINCT ?class_y
    WHERE {
        ?class_x rdf:type gufo:SemiRigidType .
        ?class_x rdfs:subClassOf ?class_y .
    } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        ontology_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_y.toPython())
        move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ra04(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Executes rule RA04 from group UFO All.

        Definition: x != y ^ Kind(x) ^ subClassOf(x,y) -> NonSortal(y)
    Description: All entities must have a single or aggregate multiple identity principles.
    """

    rule_code = "RA04"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
    PREFIX gufo: <http://purl.org/nemo/gufo#>
    SELECT DISTINCT ?class_x ?class_y
    WHERE {
        ?class_x rdf:type gufo:Kind .
        ?class_x rdfs:subClassOf ?class_y .
    } """

    query_result = ontology_graph.query(query_string)

    result = []

    for row in query_result:
        if row.class_x.toPython() != row.class_y.toPython():
            result.append(row.class_y.toPython())

    for ontology_dataclass in ontology_dataclass_list:
        if ontology_dataclass.uri in result:
            move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ra05(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Executes rule RA05 from group UFO All.

        Definition: NonSortal(x) ^ subClassOf(x,y) -> NonSortal(y)
    Description: NonSortals can only specialize other NonSortals
    """

    rule_code = "RA05"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
    PREFIX gufo: <http://purl.org/nemo/gufo#>
    SELECT DISTINCT ?class_y
    WHERE {
        ?class_x rdf:type gufo:NonSortal .
        ?class_x rdfs:subClassOf ?class_y .
    } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        ontology_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_y.toPython())
        move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ra06(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Executes rule RA06 from group UFO All.

        Definition: Phase(x) ^ subClassOf(x,y) -> ~Role(y) ^ ~RoleMixin(y)
    Description: Phases cannot specialize Roles and RoleMixins
    """

    rule_code = "RA06"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
    PREFIX gufo: <http://purl.org/nemo/gufo#>
    SELECT DISTINCT ?class_y
    WHERE {
        ?class_x rdf:type gufo:Phase .
        ?class_x rdfs:subClassOf ?class_y .
    } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        ontology_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_y.toPython())
        move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
        move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ra07(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """ Executes rule RA07 from group UFO All.

        Definition: PhaseMixin(x) ^ subClassOf(x,y) -> ~RoleMixin(y)
    Description: PhaseMixins cannot specialize RoleMixins
    """

    rule_code = "RA07"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
    PREFIX gufo: <http://purl.org/nemo/gufo#>
    SELECT DISTINCT ?class_y
    WHERE {
        ?class_x rdf:type gufo:PhaseMixin .
        ?class_x rdfs:subClassOf ?class_y .
    } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        ontology_dataclass = get_dataclass_by_uri(ontology_dataclass_list, row.class_y.toPython())
        move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def execute_rules_ufo_all(ontology_dataclass_list: list[OntologyDataClass], ontology_graph: Graph) -> None:
    """Call the execution of all rules from the group UFO All."""

    LOGGER.debug("Starting execution of all rules from group UFO All.")

    run_ra01(ontology_dataclass_list, ontology_graph)
    run_ra02(ontology_dataclass_list, ontology_graph)
    run_ra03(ontology_dataclass_list, ontology_graph)
    run_ra04(ontology_dataclass_list, ontology_graph)
    run_ra05(ontology_dataclass_list, ontology_graph)
    run_ra06(ontology_dataclass_list, ontology_graph)
    run_ra07(ontology_dataclass_list, ontology_graph)

    LOGGER.debug("Execution of all rules from group UFO All completed.")
