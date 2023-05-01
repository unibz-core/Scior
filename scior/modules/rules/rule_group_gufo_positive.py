""" Implementation of all rules from the group gUFO Positive. """

# Used this way to avoid circular dependency
import scior.modules.ontology_dataclassess.dataclass_moving as m
from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


def execute_gufo_positive_rules(ontology_dataclass_list):
    """ Executes once all "positive" rules of the GUFO group."""

    # LOGGER.debug("Executing all positive rules from group gUFO.")

    for ontology_dataclass in ontology_dataclass_list:

        # RP01: NonRigidType(x) -> ~RigidType(x)
        if "NonRigidType" in ontology_dataclass.is_type:
            rule_code = "RP01"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)

        # RP02: RigidType(x) -> ~NonRigidType(x) ^ ~AntiRigidType(x) ^ ~SemiRigidType(x) ^
        #                       ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) ^ ~Mixin(x)
        if "RigidType" in ontology_dataclass.is_type:
            rule_code = "RP02"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "NonRigidType", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SemiRigidType", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)

        # RP03: AntiRigidType(x) -> NonRigidType(x) ^
        #                           ~SemiRigidType(x) ^ ~Category(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Mixin(x)
        if "AntiRigidType" in ontology_dataclass.is_type:
            rule_code = "RP03"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonRigidType", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SemiRigidType", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)

        # RP04: SemiRigidType(x) -> Mixin(x) ^ NonRigidType(x) ^ ~AntiRigidType(x) ^ ~Category(x) ^
        #                           ~Kind(x) ^ ~SubKind(x) ^ ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x)
        if "SemiRigidType" in ontology_dataclass.is_type:
            rule_code = "RP04"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonRigidType", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)

        # RP05: NonSortal(x) -> ~Sortal(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x)
        if "NonSortal" in ontology_dataclass.is_type:
            rule_code = "RP05"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # RP06: Sortal(x) -> ~NonSortal(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~Mixin(x)
        if "Sortal" in ontology_dataclass.is_type:
            rule_code = "RP06"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")

            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)

        # RP07: Kind(x) -> RigidType(x) ^ Sortal(x) ^ ~Category(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x)
        if "Kind" in ontology_dataclass.is_type:
            rule_code = "RP07"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # RP08: SubKind(x) -> RigidType(x) ^ Sortal(x) ^ ~Category(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~Role(x)
        if "SubKind" in ontology_dataclass.is_type:
            rule_code = "RP08"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)

        # RP09: Role(x) ->   AntiRigidType(x) ^ Sortal(x) ^ ~Kind(x) ^ ~Phase(x) ^
        #                   ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Role" in ontology_dataclass.is_type:
            rule_code = "RP09"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # RP10: Phase(x) ->  AntiRigidType(x) ^ Sortal(x) ^ ~Kind(x) ^
        #                   ~PhaseMixin(x) ^ ~Role(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Phase" in ontology_dataclass.is_type:
            rule_code = "RP10"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # RP11: Category(x) ->   NonSortal(x) ^ RigidType(x) ^
        #                       ~Kind(x) ^ ~Mixin(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Category" in ontology_dataclass.is_type:
            rule_code = "RP11"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # RP12: RoleMixin(x) -> AntiRigidType(x) ^ NonSortal(x) ^
        #                       ~Category(x) ^ ~Mixin(x) ^ ~Phase(x) ^ ~PhaseMixin(x) ^ ~Role(x)
        if "RoleMixin" in ontology_dataclass.is_type:
            rule_code = "RP12"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)

        # RP13: PhaseMixin(x) ->    AntiRigidType(x) ^ NonSortal(x) ^
        #                           ~Category(x) ^ ~Mixin(x) ^ ~Phase(x) ^ ~Role(x) ^ ~RoleMixin(x)
        if "PhaseMixin" in ontology_dataclass.is_type:
            rule_code = "RP13"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)

        # RP14: Mixin(x) -> NonSortal(x) ^ SemiRigidType(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x)
        if "Mixin" in ontology_dataclass.is_type:
            rule_code = "RP14"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "SemiRigidType", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
