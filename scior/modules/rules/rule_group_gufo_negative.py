""" Implementation of all rules from the group gUFO Negative. """

# Used this way to avoid circular dependency
import scior.modules.ontology_dataclassess.dataclass_moving as m
from scior.modules.logger_config import initialize_logger

LOGGER = initialize_logger()


def execute_gufo_negative_rules(ontology_dataclass_list):
    """ Executes once all "negative" rules of the GUFO group."""

    # LOGGER.debug("Executing all negative rules from group gUFO.")

    for ontology_dataclass in ontology_dataclass_list:

        # RN01: ~NonRigidType(x) -> RigidType(x)
        if "NonRigidType" in ontology_dataclass.not_type:
            rule_code = "RN01"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)

        # RN02: ~AntiRigidType(x) ^ ~SemiRigidType(x) -> RigidType(x)
        if "AntiRigidType" in ontology_dataclass.not_type and "SemiRigidType" in ontology_dataclass.not_type:
            rule_code = "RN02"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)

        # RN03:    ~Category(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) ->
        #           SemiRigidType(x)
        if "Category" in ontology_dataclass.not_type and "Kind" in ontology_dataclass.not_type and \
                "SubKind" in ontology_dataclass.not_type and "Role" in ontology_dataclass.not_type and \
                "Phase" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type and \
                "PhaseMixin" in ontology_dataclass.not_type:
            rule_code = "RN03"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "SemiRigidType",
                                             rule_code)

        # RN04: ~Category(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Mixin(x) -> AntiRigidType(x)
        if "Category" in ontology_dataclass.not_type and "Kind" in ontology_dataclass.not_type and \
                "SubKind" in ontology_dataclass.not_type and "Mixin" in ontology_dataclass.not_type:
            rule_code = "RN04"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)

        # RN05: ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) ^ ~Mixin(x) -> RigidType(x)
        if "Role" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and \
                "RoleMixin" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type and \
                "Mixin" in ontology_dataclass.not_type:
            rule_code = "RN05"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)

        # RN06: ~RigidType(x) -> NonRigidType(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Category(x)
        if "RigidType" in ontology_dataclass.not_type:
            rule_code = "RN06"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonRigidType", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)

        # RN07: ~Sortal(x) -> NonSortal(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Role(x) ^ ~Phase(x)
        if "Sortal" in ontology_dataclass.not_type:
            rule_code = "RN07"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)

        # RN08: ~NonSortal(x) -> Sortal(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~Mixin(x)
        if "NonSortal" in ontology_dataclass.not_type:
            rule_code = "RN08"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)

        # RN09: ~Kind(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x) -> NonSortal(x)
        if "Kind" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and \
                "Role" in ontology_dataclass.not_type and "SubKind" in ontology_dataclass.not_type:
            rule_code = "RN09"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)

        # RN10: ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~Mixin(x) -> Sortal(x)
        if "Category" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type and \
                "RoleMixin" in ontology_dataclass.not_type and "Mixin" in ontology_dataclass.not_type:
            rule_code = "RN10"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_is_type(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)

        # RN11: ~AntiRigidType(x) -> ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x)
        if "AntiRigidType" in ontology_dataclass.not_type:
            rule_code = "RN10"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            m.move_classification_to_not_type(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
