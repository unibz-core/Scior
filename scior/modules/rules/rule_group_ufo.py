""" Implementation of caller/switcher for rules of group UFO. """
from scior.modules.logger_config import initialize_logger

logger = initialize_logger()

def run_r22cg(ontology_dataclass_list, ontology_graph):
    """ Executes rule R22Cg from group UFO.

    Code: R22Cg
    Definition: RigidType(x) ^ subClassOf(x,y) -> ~AntiRigidType(y)
    Description: AntiRigid types cannot specialize Rigid types.
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



def execute_ufo_rules(ontology_dataclass_list, ontology_graph):
    """Executes all rules of the UFO group."""

    logger.debug("Executing all rules from group AUX.")

    run_r22cg(ontology_dataclass_list, ontology_graph)

    # R23Cg: SemiRigidType(x) ^ subClassOf(x,y) -> ~AntiRigidType(y)
    # R26Cg: x != y ^ Kind(x) ^ subClassOf(x,y) -> NonSortal(y)
    # R27Cg: NonSortal(x) ^ subClassOf(x,y) -> NonSortal(y)
    # R32Cg: Phase(x) ^ subClassOf(x,y) -> ~Role(y) ^ ~RoleMixin(y)
    # R33Cg: PhaseMixin(x) ^ subClassOf(x,y) -> ~RoleMixin(y)


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
