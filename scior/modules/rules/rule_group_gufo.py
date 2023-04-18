""" Implementation of caller/switcher for rules of group GUFO. """
from scior.modules.logger_config import initialize_logger


def execute_gufo_rules(ontology_dataclass_list):
    """Executes once all rules of the BASE group."""

    logger = initialize_logger()

    logger.debug("Executing all rules from group gUFO.")

    for ontology_dataclass in ontology_dataclass_list:

        # RART: RigidType(x) -> ~NonRigidType(x) ^ ~AntiRigidType(x) ^ ~SemiRigidType(x)
        if "RigidType" in ontology_dataclass.is_type:
            rule_code = "RART"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_not_list("NonRigidType", rule_code)
            ontology_dataclass.move_element_to_not_list("AntiRigidType", rule_code)
            ontology_dataclass.move_element_to_not_list("SemiRigidType", rule_code)

        # R03Cg3: NonRigidType(x) -> ~RigidType(x)
        if "NonRigidType" in ontology_dataclass.is_type:
            rule_code = "R03Cg3"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_not_list("RigidType", rule_code)

        # R04Cg1: AntiRigidType(x) -> NonRigidType(x) ^ ~SemiRigidType(x)
        if "AntiRigidType" in ontology_dataclass.is_type:
            rule_code = "R04Cg1"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_is_list("NonRigidType", rule_code)
            ontology_dataclass.move_element_to_not_list("SemiRigidType", rule_code)

        # RASR: SemiRigidType(x) -> Mixin(x) ^ NonRigidType(x) ^ ~AntiRigidType(x)
        if "SemiRigidType" in ontology_dataclass.is_type:
            rule_code = "RASR"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_is_list("Mixin", rule_code)
            ontology_dataclass.move_element_to_is_list("NonRigidType", rule_code)
            ontology_dataclass.move_element_to_not_list("AntiRigidType", rule_code)

        # R05Cg1: Sortal(x) -> ~NonSortal(x)
        if "Sortal" in ontology_dataclass.is_type:
            rule_code = "R05Cg1"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_not_list("NonSortal", rule_code)

        # R05Cg2: NonSortal(x) -> ~Sortal(x)
        if "NonSortal" in ontology_dataclass.is_type:
            rule_code = "R05Cg2"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_not_list("Sortal", rule_code)

        # RAM: Mixin(x) -> NonSortal(x) ^ SemiRigidType(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x)
        if "Mixin" in ontology_dataclass.is_type:
            rule_code = "RAM"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_is_list("NonSortal", rule_code)
            ontology_dataclass.move_element_to_is_list("SemiRigidType", rule_code)
            ontology_dataclass.move_element_to_not_list("Category", rule_code)
            ontology_dataclass.move_element_to_not_list("PhaseMixin", rule_code)
            ontology_dataclass.move_element_to_not_list("RoleMixin", rule_code)

        # RAC: Category(x) ->
        #           NonSortal(x) ^ RigidType(x) ^ ~Kind(x) ^ ~Mixin(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Category" in ontology_dataclass.is_type:
            rule_code = "RAC"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_is_list("NonSortal", rule_code)
            ontology_dataclass.move_element_to_is_list("RigidType", rule_code)
            ontology_dataclass.move_element_to_not_list("Kind", rule_code)
            ontology_dataclass.move_element_to_not_list("Mixin", rule_code)
            ontology_dataclass.move_element_to_not_list("PhaseMixin", rule_code)
            ontology_dataclass.move_element_to_not_list("RoleMixin", rule_code)
            ontology_dataclass.move_element_to_not_list("SubKind", rule_code)

        # RARM: RoleMixin(x) ->
        #           AntiRigidType(x) ^ NonSortal(x) ^ ~Category(x) ^ ~Mixin(x) ^ ~Phase(x) ^ ~PhaseMixin(x) ^ ~Role(x)
        if "RoleMixin" in ontology_dataclass.is_type:
            rule_code = "RARM"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_is_list("AntiRigidType", rule_code)
            ontology_dataclass.move_element_to_is_list("NonSortal", rule_code)
            ontology_dataclass.move_element_to_not_list("Category", rule_code)
            ontology_dataclass.move_element_to_not_list("Mixin", rule_code)
            ontology_dataclass.move_element_to_not_list("Phase", rule_code)
            ontology_dataclass.move_element_to_not_list("PhaseMixin", rule_code)
            ontology_dataclass.move_element_to_not_list("Role", rule_code)

        # RAPM: PhaseMixin(x) ->
        #           AntiRigidType(x) ^ NonSortal(x) ^ ~Category(x) ^ ~Mixin(x) ^ ~Phase(x) ^ ~Role(x) ^ ~RoleMixin(x)
        if "PhaseMixin" in ontology_dataclass.is_type:
            rule_code = "RAPM"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_is_list("AntiRigidType", rule_code)
            ontology_dataclass.move_element_to_is_list("NonSortal", rule_code)
            ontology_dataclass.move_element_to_not_list("Category", rule_code)
            ontology_dataclass.move_element_to_not_list("Mixin", rule_code)
            ontology_dataclass.move_element_to_not_list("Phase", rule_code)
            ontology_dataclass.move_element_to_not_list("Role", rule_code)
            ontology_dataclass.move_element_to_not_list("RoleMixin", rule_code)

        # RAK: Kind(x) -> RigidType(x) ^ Sortal(x) ^ ~Category(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x)
        if "Kind" in ontology_dataclass.is_type:
            rule_code = "RAK"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_is_list("RigidType", rule_code)
            ontology_dataclass.move_element_to_is_list("Sortal", rule_code)
            ontology_dataclass.move_element_to_not_list("Category", rule_code)
            ontology_dataclass.move_element_to_not_list("Phase", rule_code)
            ontology_dataclass.move_element_to_not_list("Role", rule_code)
            ontology_dataclass.move_element_to_not_list("SubKind", rule_code)

        # RAS: SubKind(x) -> RigidType(x) ^ Sortal(x) ^ ~Category(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~Role(x)
        if "SubKind" in ontology_dataclass.is_type:
            rule_code = "RAS"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_is_list("RigidType", rule_code)
            ontology_dataclass.move_element_to_is_list("Sortal", rule_code)
            ontology_dataclass.move_element_to_not_list("Category", rule_code)
            ontology_dataclass.move_element_to_not_list("Kind", rule_code)
            ontology_dataclass.move_element_to_not_list("Phase", rule_code)
            ontology_dataclass.move_element_to_not_list("Role", rule_code)

        # RAR: Role(x) ->
        #           AntiRigidType(x) ^ Sortal(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Role" in ontology_dataclass.is_type:
            rule_code = "RAR"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_is_list("AntiRigidType", rule_code)
            ontology_dataclass.move_element_to_is_list("Sortal", rule_code)
            ontology_dataclass.move_element_to_not_list("Kind", rule_code)
            ontology_dataclass.move_element_to_not_list("Phase", rule_code)
            ontology_dataclass.move_element_to_not_list("PhaseMixin", rule_code)
            ontology_dataclass.move_element_to_not_list("RoleMixin", rule_code)
            ontology_dataclass.move_element_to_not_list("SubKind", rule_code)

        # RAP: Phase(x) ->
        #           AntiRigidType(x) ^ Sortal(x) ^ ~Kind(x) ^ ~PhaseMixin(x) ^ ~Role(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Phase" in ontology_dataclass.is_type:
            rule_code = "RAP"
            logger.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_element_to_is_list("AntiRigidType", rule_code)
            ontology_dataclass.move_element_to_is_list("Sortal", rule_code)
            ontology_dataclass.move_element_to_not_list("Kind", rule_code)
            ontology_dataclass.move_element_to_not_list("PhaseMixin", rule_code)
            ontology_dataclass.move_element_to_not_list("Role", rule_code)
            ontology_dataclass.move_element_to_not_list("RoleMixin", rule_code)
            ontology_dataclass.move_element_to_not_list("SubKind", rule_code)
