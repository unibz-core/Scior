""" Implementation of all rules from the group gUFO Leaves. """

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
