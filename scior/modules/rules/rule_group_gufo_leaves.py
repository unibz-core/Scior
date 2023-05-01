""" Implementation of all rules from the group gUFO Leaves. """

# Used this way to avoid circular dependency
import scior.modules.ontology_dataclassess.dataclass_moving as m
from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


def execute_gufo_leaves_rules(ontology_dataclass_list):
    """ Executes once all rules of the group gUFO Leaves."""

    # LOGGER.debug("Executing all positive rules from group gUFO.")

    for ontology_dataclass in ontology_dataclass_list:

        # RL01: RigidType(x) ^ ~Kind(x) ^ ~SubKind(x) -> Category(x)
        if "RigidType" in ontology_dataclass.is_type and "Kind" in ontology_dataclass.not_type and "SubKind" in ontology_dataclass.not_type:
            rule_code = "RL01"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)

        # RL02: RigidType(x) ^ ~SubKind(x) ^ ~Category(x) -> Kind(x)
        if "RigidType" in ontology_dataclass.is_type and "SubKind" in ontology_dataclass.not_type and "Category" in ontology_dataclass.not_type:
            rule_code = "RL02"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)

        # RL03: RigidType(x) ^ ~Kind(x) ^ ~Category(x) -> SubKind(x)
        if "RigidType" in ontology_dataclass.is_type and "Kind" in ontology_dataclass.not_type and "Category" in ontology_dataclass.not_type:
            rule_code = "RL03"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # RL04: AntiRigidType(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) -> Role(x)
        if "AntiRigidType" in ontology_dataclass.is_type and "Phase" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type:
            rule_code = "RL04"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)

        # RL05: AntiRigidType(x) ^ ~Role(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) -> Phase(x)
        if "AntiRigidType" in ontology_dataclass.is_type and "Role" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type:
            rule_code = "RL05"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)

        # RL06: AntiRigidType(x) ^ ~Role(x) ^ ~Phase(x) ^ ~PhaseMixin(x) -> RoleMixin(x)
        if "AntiRigidType" in ontology_dataclass.is_type and "Role" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type:
            rule_code = "RL06"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)

        # RL07: AntiRigidType(x) ^ ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) -> PhaseMixin(x)
        if "AntiRigidType" in ontology_dataclass.is_type and "Role" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type:
            rule_code = "RL07"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)

        # RL08: Sortal(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x) -> Kind(x)
        if "Sortal" in ontology_dataclass.is_type and "Phase" in ontology_dataclass.not_type and "Role" in ontology_dataclass.not_type and "SubKind" in ontology_dataclass.not_type:
            rule_code = "RL08"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)

        # RL09: Sortal(x) ^ ~Kind(x) ^ ~Role(x) ^ ~SubKind(x) -> Phase(x)
        if "Sortal" in ontology_dataclass.is_type and "Kind" in ontology_dataclass.not_type and "Role" in ontology_dataclass.not_type and "SubKind" in ontology_dataclass.not_type:
            rule_code = "RL09"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)

        # RL10: Sortal(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~SubKind(x) -> Role(x)
        if "Sortal" in ontology_dataclass.is_type and "Kind" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and "SubKind" in ontology_dataclass.not_type:
            rule_code = "RL10"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)

        # RL11: Sortal(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~Role(x) -> SubKind(x)
        if "Sortal" in ontology_dataclass.is_type and "Kind" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and "Role" in ontology_dataclass.not_type:
            rule_code = "RL11"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # RL12: NonSortal(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~Mixin(x) -> Category(x)
        if "NonSortal" in ontology_dataclass.is_type and "PhaseMixin" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type and "Mixin" in ontology_dataclass.not_type:
            rule_code = "RL12"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)

        # RL13: NonSortal(x) ^ ~Category(x) ^ ~RoleMixin(x) ^ ~Mixin(x) -> PhaseMixin(x)
        if "NonSortal" in ontology_dataclass.is_type and "Category" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type and "Mixin" in ontology_dataclass.not_type:
            rule_code = "RL13"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)

        # RL14: NonSortal(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~Mixin(x) -> RoleMixin(x)
        if "NonSortal" in ontology_dataclass.is_type and "Category" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type and "Mixin" in ontology_dataclass.not_type:
            rule_code = "RL14"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)

        # RL15: NonSortal(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) -> Mixin(x)
        if "NonSortal" in ontology_dataclass.is_type and "Category" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type:
            rule_code = "RL15"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)
