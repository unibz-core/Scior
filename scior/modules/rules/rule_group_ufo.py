""" Implementation of caller/switcher for rules of group UFO. """

from scior.modules.logger_config import initialize_logger

logger = initialize_logger()


def run_r22cg(ontology_dataclass_list, ontology_graph):
    """ Executes rule R22Cg from group UFO.

    Code: R22Cg
    Definition: RigidType(x) ^ subClassOf(x,y) -> ~AntiRigidType(y)
    Description: AntiRigid types cannot generalize Rigid types.
    """

    rule_code = "R22Cg"

    logger.debug(f"Starting rule {rule_code}")

    query_string = """
    PREFIX gufo: <http://purl.org/nemo/gufo#>
    SELECT DISTINCT ?class_y
    WHERE {
        ?class_x rdf:type gufo:RigidType .
        ?class_x rdfs:subClassOf ?class_y .
    } """

    query_result = ontology_graph.query(query_string)

    for row in query_result:
        for ontology_dataclass in ontology_dataclass_list:
            if ontology_dataclass.uri == row.class_y.toPython():
                ontology_dataclass.move_element_to_not_list("AntiRigidType")

    logger.debug(f"Rule {rule_code} concluded")


def run_r23cg(ontology_dataclass_list, ontology_graph):
    """ Executes rule R23Cg from group UFO.

    Code: R23Cg
    Definition: SemiRigidType(x) ^ subClassOf(x,y) -> ~AntiRigidType(y)
    Description: AntiRigid types cannot generalize SemiRigid types.
    """

    rule_code = "R23Cg"

    logger.debug(f"Starting rule {rule_code}")

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
                ontology_dataclass.move_element_to_not_list("AntiRigidType")

    logger.debug(f"Rule {rule_code} concluded")


def run_r26cg(ontology_dataclass_list, ontology_graph):
    """ Executes rule R26Cg from group UFO.

    Code: R26Cg
    Definition: x != y ^ Kind(x) ^ subClassOf(x,y) -> NonSortal(y)
    Description: All entities must have a single or aggregate multiple identity principles.
    """

    rule_code = "R26Cg"

    logger.debug(f"Starting rule {rule_code}")

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
            ontology_dataclass.move_element_to_is_list("NonSortal")

    logger.debug(f"Rule {rule_code} concluded")


def run_r27cg(ontology_dataclass_list, ontology_graph):
    """ Executes rule R27Cg from group UFO.

    Code: R27Cg
    Definition: NonSortal(x) ^ subClassOf(x,y) -> NonSortal(y)
    Description: NonSortals can only specialize other NonSortals
    """

    rule_code = "R27Cg"

    logger.debug(f"Starting rule {rule_code}")

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
                ontology_dataclass.move_element_to_is_list("NonSortal")

    logger.debug(f"Rule {rule_code} concluded")


def run_r32cg(ontology_dataclass_list, ontology_graph):
    """ Executes rule R32Cg from group UFO.

    Code: R32Cg
    Definition: Phase(x) ^ subClassOf(x,y) -> ~Role(y) ^ ~RoleMixin(y)
    Description: Phases cannot specialize Roles and RoleMixins
    """

    rule_code = "R32Cg"

    logger.debug(f"Starting rule {rule_code}")

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
                ontology_dataclass.move_element_to_not_list("Role")
                ontology_dataclass.move_element_to_not_list("RoleMixin")

    logger.debug(f"Rule {rule_code} concluded")


def run_r33cg(ontology_dataclass_list, ontology_graph):
    """ Executes rule R33Cg from group UFO.

    Code: R33Cg
    Definition: PhaseMixin(x) ^ subClassOf(x,y) -> ~RoleMixin(y)
    Description: PhaseMixins cannot specialize RoleMixins
    """

    rule_code = "R33Cg"

    logger.debug(f"Starting rule {rule_code}")

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
                ontology_dataclass.move_element_to_not_list("RoleMixin")

    logger.debug(f"Rule {rule_code} concluded")


def execute_ufo_rules(ontology_dataclass_list, ontology_graph):
    """Executes all rules of the UFO group."""

    logger.debug("Executing all rules from group AUX.")

    run_r22cg(ontology_dataclass_list, ontology_graph)
    run_r23cg(ontology_dataclass_list, ontology_graph)
    run_r26cg(ontology_dataclass_list, ontology_graph)
    run_r27cg(ontology_dataclass_list, ontology_graph)
    run_r32cg(ontology_dataclass_list, ontology_graph)
    run_r33cg(ontology_dataclass_list, ontology_graph)

# TODO (@pedropaulofb): Implement CWA rules
# R24Cs (CWA): E! z (AntiRigidType(x) ^ Sortal(x) ^ Category(y) ^ subClassOf(x,y) ^ subClassOf(x,z) ^ subClassOf(z,y) ->
#           RigidType(z) ^ Sortal(z))
# R25Cs1 (CWA): E! z (Mixin(x) ^ subClassOf(y,x) ^ RigidType(y) ^ subClassOf(z,x) -> AntiRigidType(z))
# R25Cs2 (CWA): E! y (Mixin(x) ^ subClassOf(y,x) ^ AntiRigidType(z) ^ subClassOf(z,x) -> RigidType(y))
# R28Cs (CWA): E! y (Sortal(x) ^ subClassOf (x,y) ->  Kind(y))
# R29Cs (CWA): E! z (shareKind(x,y) ^ subClassOf(x,z) ^ subClassOf(y,z) -> Kind(z))
# R31Cs (CWA): E! y, z (y != z ^ NonSortal(x) ^ ~shareKind(y,z) ^ (subClassOf(y,x) v shareSuperClass(x,y)) ^
#           (subClassOf(z,x) v shareSuperClass(x,z)) -> Sortal(y) ^ Sortal(z))
# R34Cs (CWA): E! z (Role(x) ^ PhaseMixin(y) ^ subClassOf(x,y) ^ subClassOf(x,z) ^ subClassOf(z,y) -> Phase(z))
# R35Cs (CWA): E! y (Phase(x) ^ shareKind(x,y) ^ ~isSubClassOf(x,y) ^ ~isSubClassOf(y,x) -> Phase(y))
# R36Cs (CWA): E! y (PhaseMixin(x) ^ isSubClassOf(x,y) -> Category (y))
# R37Cs (CWA): E! z (PhaseMixin(x) ^ Category(y) ^ subClassOf(x,y) ^ ~isSubClassOf(x,z) ^ ~isSubClassOf(z,x) ^
#           isSubClassOf(z,y) -> PhaseMixin(z))
