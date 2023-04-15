""" Implementation of rules of group UFO Specific. """
from rdflib import RDFS, URIRef

from scior.modules.logger_config import initialize_logger
from scior.modules.rules_type_implementations import register_incompleteness

logger = initialize_logger()


def result_treatment_r28cs(ontology_dataclass_list, sortal_dataclass,
                           can_kind_supertypes, is_kind_supertypes,
                           arguments):
    """ Treats the results from function run_r28cs.

    Two lists are received as parameters:
        1) a list of superclasses of the ontology_dataclass that ARE Kinds (is_kind_supertypes), and
        2) a list of superclasses of the ontology_dataclass that CAN be Kinds (can_kind_supertypes).

    GENERAL CASES:
        If len(is_kind_supertypes) > 1, then an error occurred and the program is aborted.
        Elif len(is_kind_supertypes) = 1. Move "Kind" to not list to all elements (if any) in can_kind_supertypes.
        Else, the action depends on if CWA is assumed or not.
    IF OWA:
        If len(can_kind_supertypes) > 0 then no action taken when automatic (if interactive, user can choose)
        If len(can_kind_supertypes) = 0 then INCOMPLETENESS
    IF CWA:
        If len(can_kind_supertypes) > 1 then no action taken when automatic (if interactive, user can choose)
        If len(can_kind_supertypes) = 1 then set element as Kind.
        If len(can_kind_supertypes) = 0 then INCONSISTENCY
    """

    len_is_kind = len(is_kind_supertypes)
    len_can_kind = len(can_kind_supertypes)

    # GENERAL CASES

    if len_is_kind > 1:
        logger.error(f"Error detected. The Sortal {sortal_dataclass.uri} "
                     f"has more than one Kind as supertypes ({is_kind_supertypes}). Program aborted.")
        raise Exception("INCONSISTENCY FOUND!")

    elif len_is_kind == 1:
        # Only need to move if there are elements to be moved.
        if len_can_kind != 0:
            for ontology_dataclass_sub in ontology_dataclass_list:
                if ontology_dataclass_sub.uri in can_kind_supertypes:
                    ontology_dataclass_sub.move_element_to_not_list("Kind")

    # OWA CASES (len_is_kind == 0)
    elif arguments["is_owa"]:

        # if len_can_kind > 0 and if interactive:
        # TODO (@pedropaulofb): Implement interactive actions.

        if len_can_kind == 0:
            register_incompleteness("R28Cs", sortal_dataclass)

    # CWA CASES (len_is_kind == 0)
    elif arguments["is_cwa"]:

        # if len_can_kind > 1 and if interactive:
        # TODO (@pedropaulofb): Implement interactive actions.

        if len_can_kind == 1:
            for ontology_dataclass_sub in ontology_dataclass_list:
                if ontology_dataclass_sub.uri == can_kind_supertypes[0]:
                    ontology_dataclass_sub.move_element_to_is_list("Kind")

        elif len_can_kind == 0:
            logger.error(f"The Sortal {sortal_dataclass.uri} does not have an identity provider (Kind). "
                         f"Program aborted.")
            raise Exception("INCONSISTENCY FOUND!")


def run_r28cs(ontology_dataclass_list, ontology_graph, arguments):
    """ Executes rule R28Cs from group UFO.

    Code: R28Cs
    Definition: E! y (Sortal(x) ^ subClassOf (x,y) -> Kind(y))
    Description: Every Sortal must have a unique identity provider, i.e., a single Kind.
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

            print(f"{all_supertypes =}")
            print(f"{can_kind_supertypes =}")
            print(f"{is_kind_supertypes =}")

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
