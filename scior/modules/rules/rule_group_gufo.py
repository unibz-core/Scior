""" Implementation of caller/switcher for rules of group GUFO. """
import random
import string

from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_moving import move_classification_to_is_type_list, \
    move_classification_to_not_type_list
from scior.modules.utils_dataclass import generate_hash_ontology_dataclass_list

LOGGER = initialize_logger()


def loop_execute_gufo_rules(ontology_dataclass_list):
    """ Executes in loop all rules of the GUFO group."""

    loop_id = ''.join(random.choices(string.ascii_lowercase, k=4))

    LOGGER.debug(f"gUFO loop ID = {loop_id}. Executing in loop all rules from group gUFO.")

    initial_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)
    final_hash = initial_hash + 1

    while initial_hash != final_hash:
        initial_hash = final_hash

        execute_gufo_positive_rules(ontology_dataclass_list)
        execute_gufo_negative_rules(ontology_dataclass_list)

        final_hash = generate_hash_ontology_dataclass_list(ontology_dataclass_list)

        if initial_hash == final_hash:
            LOGGER.debug(f"gUFO loop ID = {loop_id}. Final hash equals initial hash "
                         f"gUFO types hierarchy rules successfully concluded.")
        else:
            LOGGER.debug(f"gUFO loop ID = {loop_id}. Final hash does not equals initial hash. Re-executing rules.")


def execute_gufo_positive_rules(ontology_dataclass_list):
    """ Executes once all "positive" rules of the GUFO group."""

    # LOGGER.debug("Executing all positive rules from group gUFO.")

    for ontology_dataclass in ontology_dataclass_list:

        # IR07: RigidType(x) -> ~NonRigidType(x) ^ ~AntiRigidType(x) ^ ~SemiRigidType(x) ^
        #                       ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) ^ ~Mixin(x)
        if "RigidType" in ontology_dataclass.is_type:
            rule_code = "IR07"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "NonRigidType", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "AntiRigidType",
                                                 rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "SemiRigidType",
                                                 rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)

        # IR03: NonRigidType(x) -> ~RigidType(x)
        if "NonRigidType" in ontology_dataclass.is_type:
            rule_code = "IR03"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)

        # IR10: AntiRigidType(x) -> NonRigidType(x) ^
        #                           ~SemiRigidType(x) ^ ~Category(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Mixin(x)
        if "AntiRigidType" in ontology_dataclass.is_type:
            rule_code = "IR10"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "NonRigidType", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "SemiRigidType",
                                                 rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)

        # IR12: SemiRigidType(x) -> Mixin(x) ^ NonRigidType(x) ^ ~AntiRigidType(x) ^ ~Category(x) ^
        #                           ~Kind(x) ^ ~SubKind(x) ^ ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x)
        if "SemiRigidType" in ontology_dataclass.is_type:
            rule_code = "IR12"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "NonRigidType", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "AntiRigidType",
                                                 rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)

        # IR18: Sortal(x) -> ~NonSortal(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~Mixin(x)
        if "Sortal" in ontology_dataclass.is_type:
            rule_code = "IR18"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")

            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)

        # IR16: NonSortal(x) -> ~Sortal(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x)
        if "NonSortal" in ontology_dataclass.is_type:
            rule_code = "IR16"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # IR27: Mixin(x) -> NonSortal(x) ^ SemiRigidType(x) ^ ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x)
        if "Mixin" in ontology_dataclass.is_type:
            rule_code = "IR27"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "SemiRigidType", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)

        # IR24: Category(x) ->   NonSortal(x) ^ RigidType(x) ^
        #                       ~Kind(x) ^ ~Mixin(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Category" in ontology_dataclass.is_type:
            rule_code = "IR24"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # IR25: RoleMixin(x) -> AntiRigidType(x) ^ NonSortal(x) ^
        #                       ~Category(x) ^ ~Mixin(x) ^ ~Phase(x) ^ ~PhaseMixin(x) ^ ~Role(x)
        if "RoleMixin" in ontology_dataclass.is_type:
            rule_code = "IR25"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)

        # IR26: PhaseMixin(x) ->    AntiRigidType(x) ^ NonSortal(x) ^
        #                           ~Category(x) ^ ~Mixin(x) ^ ~Phase(x) ^ ~Role(x) ^ ~RoleMixin(x)
        if "PhaseMixin" in ontology_dataclass.is_type:
            rule_code = "IR26"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Mixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)

        # IR20: Kind(x) -> RigidType(x) ^ Sortal(x) ^ ~Category(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x)
        if "Kind" in ontology_dataclass.is_type:
            rule_code = "IR20"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # IR21: SubKind(x) -> RigidType(x) ^ Sortal(x) ^ ~Category(x) ^ ~Kind(x) ^ ~Phase(x) ^ ~Role(x)
        if "SubKind" in ontology_dataclass.is_type:
            rule_code = "IR21"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Category", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)

        # IR22: Role(x) ->   AntiRigidType(x) ^ Sortal(x) ^ ~Kind(x) ^ ~Phase(x) ^
        #                   ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Role" in ontology_dataclass.is_type:
            rule_code = "IR22"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Phase", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)

        # IR23: Phase(x) ->  AntiRigidType(x) ^ Sortal(x) ^ ~Kind(x) ^
        #                   ~PhaseMixin(x) ^ ~Role(x) ^ ~RoleMixin(x) ^ ~SubKind(x)
        if "Phase" in ontology_dataclass.is_type:
            rule_code = "IR23"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Kind", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "PhaseMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "Role", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "RoleMixin", rule_code)
            move_classification_to_not_type_list(ontology_dataclass_list, ontology_dataclass, "SubKind", rule_code)


def execute_gufo_negative_rules(ontology_dataclass_list):
    """ Executes once all "negative" rules of the GUFO group."""

    # LOGGER.debug("Executing all negative rules from group gUFO.")

    for ontology_dataclass in ontology_dataclass_list:

        # IR13: ~Sortal(x) -> NonSortal(x)
        if "Sortal" in ontology_dataclass.not_type:
            rule_code = "IR13"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)

        # IR14: ~NonSortal(x) -> Sortal(x)
        if "NonSortal" in ontology_dataclass.not_type:
            rule_code = "IR14"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)

        # IR04: ~RigidType(x) -> NonRigidType(x)
        if "RigidType" in ontology_dataclass.not_type:
            rule_code = "IR04"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "NonRigidType", rule_code)

        # IR06: ~AntiRigidType(x) ^ ~SemiRigidType(x) -> RigidType(x)
        if "AntiRigidType" in ontology_dataclass.not_type and "SemiRigidType" in ontology_dataclass.not_type:
            rule_code = "IR06"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)

        # IR05: ~NonRigidType(x) -> RigidType(x)
        if "NonRigidType" in ontology_dataclass.not_type:
            rule_code = "IR05"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)

        # IR11: ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) ^ ~Mixin(x) -> RigidType(x)
        if "Role" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and \
                "RoleMixin" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type and \
                "Mixin" in ontology_dataclass.not_type:
            rule_code = "IR11"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "RigidType", rule_code)

        # IR09: ~Category(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Mixin(x) -> AntiRigidType(x)
        if "Category" in ontology_dataclass.not_type and "Kind" in ontology_dataclass.not_type and \
                "SubKind" in ontology_dataclass.not_type and "Mixin" in ontology_dataclass.not_type:
            rule_code = "IR09"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "AntiRigidType", rule_code)

        # IR08:    ~Category(x) ^ ~Kind(x) ^ ~SubKind(x) ^ ~Role(x) ^ ~Phase(x) ^ ~RoleMixin(x) ^ ~PhaseMixin(x) ->
        #           SemiRigidType(x)
        if "Category" in ontology_dataclass.not_type and "Kind" in ontology_dataclass.not_type and \
                "SubKind" in ontology_dataclass.not_type and "Role" in ontology_dataclass.not_type and \
                "Phase" in ontology_dataclass.not_type and "RoleMixin" in ontology_dataclass.not_type and \
                "PhaseMixin" in ontology_dataclass.not_type:
            rule_code = "IR08"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "SemiRigidType", rule_code)

        # IR15: ~Kind(x) ^ ~Phase(x) ^ ~Role(x) ^ ~SubKind(x) -> NonSortal(x)
        if "Kind" in ontology_dataclass.not_type and "Phase" in ontology_dataclass.not_type and \
                "Role" in ontology_dataclass.not_type and "SubKind" in ontology_dataclass.not_type:
            rule_code = "IR15"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "NonSortal", rule_code)

        # IR17: ~Category(x) ^ ~PhaseMixin(x) ^ ~RoleMixin(x) ^ ~Mixin(x) -> Sortal(x)
        if "Category" in ontology_dataclass.not_type and "PhaseMixin" in ontology_dataclass.not_type and \
                "RoleMixin" in ontology_dataclass.not_type and "Mixin" in ontology_dataclass.not_type:
            rule_code = "IR17"
            # LOGGER.debug(f"Executing rule {rule_code} for {ontology_dataclass.uri}.")
            move_classification_to_is_type_list(ontology_dataclass_list, ontology_dataclass, "Sortal", rule_code)
