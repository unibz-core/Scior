""" Implementation of rules of group UFO Specific. """
from rdflib import RDFS, URIRef

from scior.modules.logger_config import initialize_logger

logger = initialize_logger()


def result_treatment_r28cs(ontology_dataclass_list, ontology_dataclass,
                           can_kind_supertypes, is_kind_supertypes,
                           arguments):
    """ Treats the results from function run_r28cs. """

    if len(is_kind_supertypes) > 1:
        logger.error(f"Error detected. The Sortal {ontology_dataclass.uri} "
                     f"has more than one Kind as supertypes ({is_kind_supertypes}). Program aborted.")
        exit(1)
    # elif  len(all_supertypes) == 0:
    # If is_list = 1 and can_list > 0, move 'Kind' in all elements from can_list to not_type

    # If list higher than one, error.
    # If list is empty, treat.

    pass


def run_r28cs(ontology_dataclass_list, ontology_graph, arguments):
    """ Executes rule R28Cs from group UFO.

    Code: R28Cs
    Definition: E! y (Sortal(x) ^ subClassOf (x,y) -> Kind(y))
    Description: One of the Sortal superclasses must be a Kind.
    """

    rule_code = "R28Cs"

    logger.debug(f"Starting rule {rule_code}")

    for ontology_dataclass in ontology_dataclass_list:
        all_supertypes = []
        can_kind_supertypes = []

        # For every Sortal
        if "Sortal" in ontology_dataclass.is_type:

            print(ontology_dataclass.uri)

            # Creating a list of all superclasses
            for superclass in ontology_graph.objects(URIRef(ontology_dataclass.uri), RDFS.subClassOf):
                all_supertypes.append(superclass.toPython())

            is_kind_supertypes = all_supertypes.copy()

            # Removing all superclasses that are not Kinds
            for ontology_dataclass_sub in ontology_dataclass_list:
                # Creating list of supertypes that can be Kind
                if (ontology_dataclass_sub.uri in all_supertypes) and ("Kind" in ontology_dataclass_sub.can_type):
                    can_kind_supertypes.append(ontology_dataclass_sub.uri)
                # Creating list of supertypes that are Kind
                if (ontology_dataclass_sub.uri in all_supertypes) and ("Kind" not in ontology_dataclass_sub.is_type):
                    is_kind_supertypes.remove(ontology_dataclass_sub.uri)

            print(f"all = {all_supertypes}")
            print(f"can = {can_kind_supertypes}")
            print(f"is = {is_kind_supertypes}")

            result_treatment_r28cs(ontology_dataclass_list, ontology_dataclass,
                                   can_kind_supertypes, is_kind_supertypes,
                                   arguments)

    logger.debug(f"Rule {rule_code} concluded")


def execute_rules_ufo_specific(ontology_dataclass_list, ontology_graph, arguments):
    """Executes all rules of the UFO Specific group."""

    run_r28cs(ontology_dataclass_list, ontology_graph, arguments)

# R24Cs: E! z (AntiRigidType(x) ^ Sortal(x) ^ Category(y) ^ subClassOf(x,y) ^ subClassOf(x,z) ^ subClassOf(z,y) -> RigidType(z) ^ Sortal(z))
# R25Cs1: E! z (Mixin(x) ^ subClassOf(y,x) ^ RigidType(y) ^ subClassOf(z,x) -> AntiRigidType(z))
# R25Cs2: E! y (Mixin(x) ^ subClassOf(y,x) ^ AntiRigidType(z) ^ subClassOf(z,x) -> RigidType(y))
# R29Cs: E! z (shareKind(x,y) ^ subClassOf(x,z) ^ subClassOf(y,z) -> Kind(z))
# R31Cs: E! y, z (y != z ^ NonSortal(x) ^ ~shareKind(y,z) ^ (subClassOf(y,x) v shareSuperClass(x,y)) ^ (subClassOf(z,x) v shareSuperClass(x,z)) -> Sortal(y) ^ Sortal(z))
# R34Cs: E! z (Role(x) ^ PhaseMixin(y) ^ subClassOf(x,y) ^ subClassOf(x,z) ^ subClassOf(z,y) -> Phase(z))
# R35Cs: E! y (Phase(x) ^ shareKind(x,y) ^ ~isSubClassOf(x,y) ^ ~isSubClassOf(y,x) -> Phase(y))
# R36Cs: E! y (PhaseMixin(x) ^ isSubClassOf(x,y) -> Category (y))
# R37Cs: E! z (PhaseMixin(x) ^ Category(y) ^ subClassOf(x,y) ^ ~isSubClassOf(x,z) ^ ~isSubClassOf(z,x) ^ isSubClassOf(z,y) -> PhaseMixin(z))
