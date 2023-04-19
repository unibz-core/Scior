""" Implementation of caller/switcher for rules of group GUFO. """

from scior.modules.logger_config import initialize_logger
from scior.modules.utils_dataclass import generate_hash_ontology_dataclass_list

LOGGER = initialize_logger()


def loop_execute_gufo_rules(ontology_dataclass_list):
    """ Executes in loop all rules of the GUFO group."""

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = initial_hash + 1

    while initial_hash != final_hash:
        initial_hash = final_hash

        execute_gufo_positive_rules(ontology_dataclass_list)
        execute_gufo_negative_rules(ontology_dataclass_list)

        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        if initial_hash == final_hash:
            LOGGER.debug("Final hash equals initial hash for the dataclass list. "
                         "gUFO types hierarchy rules successfully concluded.")
        else:
            LOGGER.debug("Final hash does not equals initial hash for the dataclass list. Re-executing rules.")


def execute_gufo_positive_rules(ontology_dataclass_list):
    """ Executes once all "positive" rules of the GUFO group."""

    LOGGER.debug("Executing all positive rules from group gUFO.")

    for ontology_dataclass in ontology_dataclass_list:

        # RART: RigidType(x) -> ~NonRigidType(x) ^ ~AntiRigidType(x) ^ ~SemiRigidType(x) ^
        #                       ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) ^ ~Mixin(x)
        if "RigidType" in ontology_dataclass.is_type:
            rule_code = "RART"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "NonRigidType", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "AntiRigidType", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "SemiRigidType", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Role", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Phase", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RoleMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "PhaseMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Mixin", rule_code)

        # R03Cg3: NonRigidType(x) -> ~RigidType(x)
        if "NonRigidType" in ontology_dataclass.is_type:
            rule_code = "R03Cg3"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RigidType", rule_code)

        # RAAR: AntiRigidType(x) -> NonRigidType(x) ^
        #                           ~SemiRigidType(x) ^ ~Category(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Mixin(x)
        if "AntiRigidType" in ontology_dataclass.is_type:
            rule_code = "RAAR"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonRigidType", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "SemiRigidType", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Category", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Kind", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "SubKind", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Mixin", rule_code)

        # RARS: SemiRigidType(x) -> Mixin(x) ^ NonRigidType(x) ^ ~AntiRigidType(x) ^ ~Category(x) ^
        #                           ~Kind(x) ^ ~SubKind(x) ^ ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x)
        if "SemiRigidType" in ontology_dataclass.is_type:
            rule_code = "RASR"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "Mixin", rule_code)
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonRigidType", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "AntiRigidType", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Category", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Kind", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "SubKind", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Role", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Phase", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RoleMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "PhaseMixin", rule_code)

        # RAS: Sortal(x) -> ~NonSortal(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~Mixin(x)
        if "Sortal" in ontology_dataclass.is_type:
            rule_code = "RAS"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")

            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "NonSortal", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Category", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "PhaseMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RoleMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Mixin", rule_code)

        # RANS: NonSortal(x) -> ~Sortal(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x)
        if "NonSortal" in ontology_dataclass.is_type:
            rule_code = "RANS"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Sortal", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Kind", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Phase", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Role", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "SubKind", rule_code)

        # RAM: Mixin(x) -> NonSortal(x) ^ SemiRigidType(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x)
        if "Mixin" in ontology_dataclass.is_type:
            rule_code = "RAM"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonSortal", rule_code)
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "SemiRigidType", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Category", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "PhaseMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RoleMixin", rule_code)

        # RAC: Category(x) ->   NonSortal(x) ^ RigidType(x) ^
        #                       ~Kind(x) ^ ~Mixin(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Category" in ontology_dataclass.is_type:
            rule_code = "RAC"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonSortal", rule_code)
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "RigidType", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Kind", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Mixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "PhaseMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RoleMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "SubKind", rule_code)

        # RARM: RoleMixin(x) -> AntiRigidType(x) ^ NonSortal(x) ^
        #                       ~Category(x) ^ ~Mixin(x) ^ ~Phase(x) ^ ~PhaseMixin(x) ^ ~Role(x)
        if "RoleMixin" in ontology_dataclass.is_type:
            rule_code = "RARM"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "AntiRigidType", rule_code)
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonSortal", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Category", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Mixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Phase", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "PhaseMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Role", rule_code)

        # RAPM: PhaseMixin(x) ->    AntiRigidType(x) ^ NonSortal(x) ^
        #                           ~Category(x) ^ ~Mixin(x) ^ ~Phase(x) ^ ~Role(x) ^ ~RoleMixin(x)
        if "PhaseMixin" in ontology_dataclass.is_type:
            rule_code = "RAPM"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "AntiRigidType", rule_code)
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonSortal", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Category", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Mixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Phase", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Role", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RoleMixin", rule_code)

        # RAK: Kind(x) -> RigidType(x) ^ Sortal(x) ^ ~Category(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x)
        if "Kind" in ontology_dataclass.is_type:
            rule_code = "RAK"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "RigidType", rule_code)
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "Sortal", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Category", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Phase", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Role", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "SubKind", rule_code)

        # RASK: SubKind(x) -> RigidType(x) ^ Sortal(x) ^ ~Category(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~Role(x)
        if "SubKind" in ontology_dataclass.is_type:
            rule_code = "RASK"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "RigidType", rule_code)
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "Sortal", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Category", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Kind", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Phase", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Role", rule_code)

        # RAR: Role(x) ->   AntiRigidType(x) ^ Sortal(x) ^ ~Kind(x) ^ ~Phase(x) ^
        #                   ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Role" in ontology_dataclass.is_type:
            rule_code = "RAR"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "AntiRigidType", rule_code)
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "Sortal", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Kind", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Phase", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "PhaseMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RoleMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "SubKind", rule_code)

        # RAP: Phase(x) ->  AntiRigidType(x) ^ Sortal(x) ^ ~Kind(x) ^
        #                   ~PhaseMixin(x) ^ ~Role(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Phase" in ontology_dataclass.is_type:
            rule_code = "RAP"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "AntiRigidType", rule_code)
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "Sortal", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Kind", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "PhaseMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "Role", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "RoleMixin", rule_code)
            ontology_dataclass.move_classification_to_not_list(ontology_dataclass_list, "SubKind", rule_code)


def execute_gufo_negative_rules(ontology_dataclass_list):
    """ Executes once all "negative" rules of the GUFO group."""

    LOGGER.debug("Executing all negative rules from group gUFO.")

    for ontology_dataclass in ontology_dataclass_list:

        # RNCg0: ~RigidType(x) -> NonRigidType(x)
        if "RigidType" in ontology_dataclass.not_type:
            rule_code = "RNCg0"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonRigidType", rule_code)

        # RNCg1: ~AntiRigidType(x) ^ ~SemiRigidType(x) -> RigidType(x)
        if "AntiRigidType" in ontology_dataclass.not_type and "SemiRigidType" in ontology_dataclass.not_type:
            rule_code = "RNCg1"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "RigidType", rule_code)

        # RNCg2: ~NonRigidType(x) -> RigidType(x)
        if "NonRigidType" in ontology_dataclass.not_type:
            rule_code = "RNCg2"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "RigidType", rule_code)

        # RNCg3: ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) ^ ~Mixin(x) -> RigidType(x)
        if "Role" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type and "Mixin" in ontology_dataclass.not_type:
            rule_code = "RNCg3"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "RigidType", rule_code)

        # RNCg4: ~Category(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Mixin(x) -> AntiRigidType(x)
        if "Category" in ontology_dataclass.not_type and "Kind" in ontology_dataclass.not_type and "SubKind" in ontology_dataclass.not_type and "Mixin" in ontology_dataclass.not_type:
            rule_code = "RNCg4"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "AntiRigidType", rule_code)

        # RNCg5:    ~Category(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) ->
        #           SemiRigidType(x)
        if "Category" in ontology_dataclass.not_type and "Kind" in ontology_dataclass.not_type and "SubKind" in ontology_dataclass.not_type and "Role" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type:
            rule_code = "RNCg5"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "SemiRigidType", rule_code)

        # RNCg6: ~Sortal(x) -> NonSortal(x)
        if "Sortal" in ontology_dataclass.not_type:
            rule_code = "RNCg6"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonSortal", rule_code)

        # RNCg7: ~NonSortal(x) -> Sortal(x)
        if "NonSortal" in ontology_dataclass.not_type:
            rule_code = "RNCg7"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "Sortal", rule_code)

        # RNCg8: ~Kind(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x) -> NonSortal(x)
        if "Kind" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and "Role" in ontology_dataclass.not_type and "SubKind" in ontology_dataclass.not_type:
            rule_code = "RNCg8"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "NonSortal", rule_code)

        # RNCg9: ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~Mixin(x) -> Sortal(x)
        if "Category" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type and "Mixin" in ontology_dataclass.not_type:
            rule_code = "RNCg9"
            LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            ontology_dataclass.move_classification_to_is_list(ontology_dataclass_list, "Sortal", rule_code)
