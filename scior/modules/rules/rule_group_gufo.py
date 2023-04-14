""" Implementation of caller/switcher for rules of group GUFO. """
from scior.modules.logger_config import initialize_logger


def execute_gufo_rules(ontology_dataclass_list):
    """Executes once all rules of the BASE group."""

    logger = initialize_logger()

    logger.debug("Executing all rules from group gUFO.")

    for ontology_dataclass in ontology_dataclass_list:

        # RART: RigidType(x) -> ~NonRigidType(x) ^ ~AntiRigidType(x) ^ ~SemiRigidType(x) 
        if "RigidType" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_not_list("NonRigidType")
            ontology_dataclass.move_element_to_not_list("AntiRigidType")
            ontology_dataclass.move_element_to_not_list("SemiRigidType")

        # R03Cg3: NonRigidType(x) -> ~RigidType(x)
        if "NonRigidType" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_not_list("RigidType")

        # R04Cg1: AntiRigidType(x) -> NonRigidType(x) ^ ~SemiRigidType(x)
        if "AntiRigidType" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_is_list("NonRigidType")
            ontology_dataclass.move_element_to_not_list("SemiRigidType")

        # RASR: SemiRigidType(x) -> Mixin(x) ^ NonRigidType(x) ^ ~AntiRigidType(x)
        if "SemiRigidType" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_is_list("Mixin")
            ontology_dataclass.move_element_to_is_list("NonRigidType")
            ontology_dataclass.move_element_to_not_list("AntiRigidType")

        # R05Cg1: Sortal(x) -> ~NonSortal(x)
        if "Sortal" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_not_list("NonSortal")

        # R05Cg2: NonSortal(x) -> ~Sortal(x)
        if "NonSortal" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_not_list("Sortal")

        # RAM: Mixin(x) -> NonSortal(x) ^ SemiRigidType(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x)
        if "Mixin" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_is_list("NonSortal")
            ontology_dataclass.move_element_to_is_list("SemiRigidType")
            ontology_dataclass.move_element_to_not_list("Category")
            ontology_dataclass.move_element_to_not_list("PhaseMixin")
            ontology_dataclass.move_element_to_not_list("RoleMixin")

        # RAC: Category(x) ->
        #           NonSortal(x) ^ RigidType(x) ^ ~Kind(x) ^ ~Mixin(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Category" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_is_list("NonSortal")
            ontology_dataclass.move_element_to_is_list("RigidType")
            ontology_dataclass.move_element_to_not_list("Kind")
            ontology_dataclass.move_element_to_not_list("Mixin")
            ontology_dataclass.move_element_to_not_list("PhaseMixin")
            ontology_dataclass.move_element_to_not_list("RoleMixin")
            ontology_dataclass.move_element_to_not_list("SubKind")

        # RARM: RoleMixin(x) ->
        #           AntiRigidType(x) ^ NonSortal(x) ^ ~Category(x) ^ ~Mixin(x) ^ ~Phase(x) ^ ~PhaseMixin(x) ^ ~Role(x)
        if "RoleMixin" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_is_list("AntiRigidType")
            ontology_dataclass.move_element_to_is_list("NonSortal")
            ontology_dataclass.move_element_to_not_list("Category")
            ontology_dataclass.move_element_to_not_list("Mixin")
            ontology_dataclass.move_element_to_not_list("Phase")
            ontology_dataclass.move_element_to_not_list("PhaseMixin")
            ontology_dataclass.move_element_to_not_list("Role")

        # RAPM: PhaseMixin(x) ->
        #           AntiRigidType(x) ^ NonSortal(x) ^ ~Category(x) ^ ~Mixin(x) ^ ~Phase(x) ^ ~Role(x) ^ ~RoleMixin(x)
        if "PhaseMixin" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_is_list("AntiRigidType")
            ontology_dataclass.move_element_to_is_list("NonSortal")
            ontology_dataclass.move_element_to_not_list("Category")
            ontology_dataclass.move_element_to_not_list("Mixin")
            ontology_dataclass.move_element_to_not_list("Phase")
            ontology_dataclass.move_element_to_not_list("Role")
            ontology_dataclass.move_element_to_not_list("RoleMixin")

        # RAK: Kind(x) -> RigidType(x) ^ Sortal(x) ^ ~Category(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x)
        if "Kind" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_is_list("RigidType")
            ontology_dataclass.move_element_to_is_list("Sortal")
            ontology_dataclass.move_element_to_not_list("Category")
            ontology_dataclass.move_element_to_not_list("Phase")
            ontology_dataclass.move_element_to_not_list("Role")
            ontology_dataclass.move_element_to_not_list("SubKind")

        # RAS: SubKind(x) -> RigidType(x) ^ Sortal(x) ^ ~Category(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~Role(x)
        if "SubKind" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_is_list("RigidType")
            ontology_dataclass.move_element_to_is_list("Sortal")
            ontology_dataclass.move_element_to_not_list("Category")
            ontology_dataclass.move_element_to_not_list("Kind")
            ontology_dataclass.move_element_to_not_list("Phase")
            ontology_dataclass.move_element_to_not_list("Role")

        # RAR: Role(x) ->
        #           AntiRigidType(x) ^ Sortal(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Role" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_is_list("AntiRigidType")
            ontology_dataclass.move_element_to_is_list("Sortal")
            ontology_dataclass.move_element_to_not_list("Kind")
            ontology_dataclass.move_element_to_not_list("Phase")
            ontology_dataclass.move_element_to_not_list("PhaseMixin")
            ontology_dataclass.move_element_to_not_list("RoleMixin")
            ontology_dataclass.move_element_to_not_list("SubKind")

        # RAP: Phase(x) ->
        #           AntiRigidType(x) ^ Sortal(x) ^ ~Kind(x) ^ ~PhaseMixin(x) ^ ~Role(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Phase" in ontology_dataclass.is_type:
            ontology_dataclass.move_element_to_is_list("AntiRigidType")
            ontology_dataclass.move_element_to_is_list("Sortal")
            ontology_dataclass.move_element_to_not_list("Kind")
            ontology_dataclass.move_element_to_not_list("PhaseMixin")
            ontology_dataclass.move_element_to_not_list("Role")
            ontology_dataclass.move_element_to_not_list("RoleMixin")
            ontology_dataclass.move_element_to_not_list("SubKind")
