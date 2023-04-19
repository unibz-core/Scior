""" Implementation of rules from the group UFO All. """

from scior.modules.logger_config import initialize_logger
from scior.modules.utils_dataclass import get_dataclass_by_uri

LOGGER = initialize_logger()


def run_ir19(ontology_dataclass_list, ontology_graph):
    """ Executes rule IR19 from group UFO All.

        Code: IR19
        Definition: Sortal(x) ^ subClassOf(y,x) -> Sortal(y)
        Description: Everything that specialize a Sortal is also a Sortal
        """

    rule_code = "IR19"

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
        new_sortal.move_classification_to_is_list(ontology_dataclass_list, "Sortal", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ir28(ontology_dataclass_list, ontology_graph):
    """ Executes rule IR28 from group UFO All.

    Code: IR28
    Definition: RigidType(x) ^ subClassOf(x,y) -> ~AntiRigidType(y)
    Description: AntiRigid types cannot generalize Rigid types.
    """

    rule_code = "IR28"

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
        ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "AntiRigidType", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ir29(ontology_dataclass_list, ontology_graph):
    """ Executes rule IR29 from group UFO All.

    Code: IR29
    Definition: SemiRigidType(x) ^ subClassOf(x,y) -> ~AntiRigidType(y)
    Description: AntiRigid types cannot generalize SemiRigid types.
    """

    rule_code = "IR29"

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
        for ontology_dataclass in ontology_dataclass_list:
            if ontology_dataclass.uri == row.class_y.toPython():
                ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "AntiRigidType", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ir33(ontology_dataclass_list, ontology_graph):
    """ Executes rule IR33 from group UFO All.

    Code: IR33
    Definition: x != y ^ Kind(x) ^ subClassOf(x,y) -> NonSortal(y)
    Description: All entities must have a single or aggregate multiple identity principles.
    """

    rule_code = "IR33"

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
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonSortal", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ir34(ontology_dataclass_list, ontology_graph):
    """ Executes rule IR34 from group UFO All.

    Code: IR34
    Definition: NonSortal(x) ^ subClassOf(x,y) -> NonSortal(y)
    Description: NonSortals can only specialize other NonSortals
    """

    rule_code = "IR34"

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
        for ontology_dataclass in ontology_dataclass_list:
            if ontology_dataclass.uri == row.class_y.toPython():
                ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonSortal", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ir41(ontology_dataclass_list, ontology_graph):
    """ Executes rule IR41 from group UFO All.

    Code: IR41
    Definition: Phase(x) ^ subClassOf(x,y) -> ~Role(y) ^ ~RoleMixin(y)
    Description: Phases cannot specialize Roles and RoleMixins
    """

    rule_code = "IR41"

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
        for ontology_dataclass in ontology_dataclass_list:
            if ontology_dataclass.uri == row.class_y.toPython():
                ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Role", rule_code)
                ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RoleMixin", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def run_ir42(ontology_dataclass_list, ontology_graph):
    """ Executes rule IR42 from group UFO All.

    Code: IR42
    Definition: PhaseMixin(x) ^ subClassOf(x,y) -> ~RoleMixin(y)
    Description: PhaseMixins cannot specialize RoleMixins
    """

    rule_code = "IR42"

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
        for ontology_dataclass in ontology_dataclass_list:
            if ontology_dataclass.uri == row.class_y.toPython():
                ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RoleMixin", rule_code)

    LOGGER.debug(f"Rule {rule_code} concluded")


def execute_rules_ufo_all(ontology_dataclass_list, ontology_graph):
    """Call the execution of all rules from the group UFO All."""

    LOGGER.debug("Starting execution of all rules from group UFO All.")

    run_ir19(ontology_dataclass_list, ontology_graph)
    run_ir28(ontology_dataclass_list, ontology_graph)
    run_ir29(ontology_dataclass_list, ontology_graph)
    run_ir33(ontology_dataclass_list, ontology_graph)
    run_ir34(ontology_dataclass_list, ontology_graph)
    run_ir41(ontology_dataclass_list, ontology_graph)
    run_ir42(ontology_dataclass_list, ontology_graph)

    LOGGER.debug("Execution of all rules from group UFO All completed.")

# TODO (@pedropaulofb): Only loop rules when a classification is IN FACT moved, not when called.
# TODO (@pedropaulofb): Uniform all warnings with Rule at the beginning.
