""" Implementation of caller/switcher for rules of group GUFO. """
import random
import string

# Used this way to avoid circular dependency
import scior.modules.initialization_arguments as args
import scior.modules.ontology_dataclassess.dataclass_moving as m
from scior.modules.logger_config import initialize_logger
from scior.modules.ontology_dataclassess.dataclass_hashing import create_ontology_dataclass_list_hash

LOGGER = initialize_logger()


def loop_execute_gufo_rules(ontology_dataclass_list):
    """ Executes in loop all rules of the GUFO group."""

    if args.ARGUMENTS["is_debug"]:
        loop_id = ''.join(random.choices(string.ascii_lowercase, k=4))
        LOGGER.debug(f"gUFO loop ID = {loop_id}. Executing in loop all rules from group gUFO.")

    initial_hash = create_ontology_dataclass_list_hash(ontology_dataclass_list)
    final_hash = initial_hash + 1

    while initial_hash != final_hash:
        initial_hash = final_hash

        execute_gufo_positive_rules(ontology_dataclass_list)
        execute_gufo_negative_rules(ontology_dataclass_list)

        final_hash = create_ontology_dataclass_list_hash(ontology_dataclass_list)

        if args.ARGUMENTS["is_debug"]:
            if initial_hash == final_hash:
                LOGGER.debug(f"gUFO loop ID = {loop_id}. Final hash equals initial hash "
                             f"gUFO types hierarchy rules successfully concluded.")
            else:
                LOGGER.debug(f"gUFO loop ID = {loop_id}. Final hash does not equals initial hash. Re-executing rules.")


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
