""" Definition of dataclass as the data structure used for loading the ontologies ontology in Scior.
    This module contains the data structure fields, initial value assignments and methods.
"""
import hashlib
from dataclasses import dataclass, field

from scior.modules.logger_config import initialize_logger
from scior.modules.rules.rule_group_gufo import loop_execute_gufo_rules

LOGGER = initialize_logger()


@dataclass
class OntologyDataClass(object):
    """ Each loaded ontology dataclass has a URI (identifier) and six lists of GUFO elements.
        Lists indicate which gUFO element the dataclass is, can, or cannot be for the types and individuals hierarchies.
    """

    uri: str = field(default_factory=str)
    is_type: list[str] = field(default_factory=list[str])
    is_individual: list[str] = field(default_factory=list[str])
    can_type: list[str] = field(default_factory=list[str])
    can_individual: list[str] = field(default_factory=list[str])
    not_type: list[str] = field(default_factory=list[str])
    not_individual: list[str] = field(default_factory=list[str])

    def move_classification_between_lists(self, ontology_dataclass_list, element: str, source_list: str,
                                          target_list: str, invoker_rule: str):
        """ Move an element between two lists in the same OntologyClass
            Elements can only be moved from CAN lists to IS or NOT lists
        """

        LOGGER.debug(f"Rule {invoker_rule}: Starting to move gUFO classification {element} from {source_list} list "
                     f"to {target_list} list in {self.uri}...")

        # VERIFICATION 1: Source and target lists must be different
        if source_list == target_list:
            LOGGER.error(f"Rule {invoker_rule}: Error for {self.uri} when trying to move the gUFO classification "
                         f"{element} from list {source_list} to list {target_list}. "
                         f"Source equals target list. Program aborted.")
            raise ValueError(f"INCONSISTENCY FOUND!")

        # VERIFICATION 2: Only CAN lists are allowed as source list
        if source_list == "can_type":
            source = self.can_type
        elif source_list == "can_individual":
            source = self.can_individual
        else:
            LOGGER.error(
                f"Rule {invoker_rule}: Error for {self.uri} when trying to move the gUFO classification {element} from "
                f"list {source_list} to list {target_list}. Source list {source_list} is unknown. Program aborted.")
            raise ValueError(f"INCONSISTENCY FOUND!")

        # VERIFICATION 3: Only IS or NOT lists are allowed as target list
        if target_list == "is_type":
            target = self.is_type
        elif target_list == "is_individual":
            target = self.is_individual
        elif target_list == "not_type":
            target = self.not_type
        elif target_list == "not_individual":
            target = self.not_individual
        else:
            LOGGER.error(
                f"Rule {invoker_rule}: Error for {self.uri} when trying to move the gUFO classification {element} from "
                f"list {source_list} to list {target_list}. Target list {target_list} is unknown. Program aborted.")
            raise ValueError(f"INCONSISTENCY FOUND!")

        # VERIFICATION 4: Element must be in source list
        if element not in source:
            LOGGER.error(
                f"Rule {invoker_rule}: Error for {self.uri} when trying to move the gUFO classification {element} from "
                f"list {source_list} to list {target_list}. The classification was not found in {source_list}. "
                f"Program aborted.")
            raise ValueError(f"INCONSISTENCY FOUND!")

        # move gUFO classification
        source.remove(element)
        target.append(element)

        # Every time a classification is moved the class will be reanalyzed by all rules, so the incompleteness is
        # cleared so it can be updated if detected again.
        self.is_incomplete = False

        loop_execute_gufo_rules(ontology_dataclass_list)

        LOGGER.debug(f"Rule {invoker_rule}: gUFO classification {element} moved successfully from list {source_list} "
                     f"to list {target_list} in {self.uri}.")

    def sort_all_internal_lists(self):
        """ Sorts all internal lists. """
        self.is_type.sort()
        self.is_individual.sort()
        self.can_type.sort()
        self.can_individual.sort()
        self.not_type.sort()
        self.not_individual.sort()

    def create_partial_hash(self, input_list):
        """ Creates a hash for a single list inside an Ontology DataClass.
            Hashes are the concatenation of all the names of all elements inside a list.
        """

        partial_hash = input_list

        if input_list == "is_type":
            list_hash = self.is_type
        elif input_list == "is_individual":
            list_hash = self.is_individual
        elif input_list == "can_type":
            list_hash = self.can_type
        elif input_list == "can_individual":
            list_hash = self.can_individual
        elif input_list == "not_type":
            list_hash = self.not_type
        elif input_list == "not_individual":
            list_hash = self.not_individual
        else:
            LOGGER.error(f"Unknown list type {input_list}. Unable to create hash. Program aborted.")
            raise ValueError(f"INCONSISTENCY FOUND!")

        for hash_part in list_hash:
            partial_hash += hash_part

        return partial_hash

    def create_hash(self, hash_type="TOTAL"):
        """ Creates a hash of the Ontology DataClass using all its lists.
            The python builtin function hash is applied to the concatenation
                of the dataclass uri with all partial hashes of all the dataclass lists.
            The hash function can be used for verifying if the state of the class was modified after an operation.

            hash_type allowed values are:
                - TOTAL: creates a hash with all six lists of a dataclass
                - TYPES_ONLY: creates a hash with only the three types' lists of a dataclass
                - INDIVIDUALS_ONLY: creates a hash with only the three individuals' lists of a dataclass
        """

        self.sort_all_internal_lists()

        hash_is_type = ""
        hash_is_individual = ""
        hash_can_type = ""
        hash_can_individual = ""
        hash_not_type = ""
        hash_not_individual = ""

        if (hash_type == "TOTAL") or (hash_type == "TYPES_ONLY"):
            hash_is_type = self.create_partial_hash("is_type")
            hash_can_type = self.create_partial_hash("can_type")
            hash_not_type = self.create_partial_hash("not_type")

        if (hash_type == "TOTAL") or (hash_type == "INDIVIDUALS_ONLY"):
            hash_is_individual = self.create_partial_hash("is_individual")
            hash_can_individual = self.create_partial_hash("can_individual")
            hash_not_individual = self.create_partial_hash("not_individual")

        class_hash = self.uri + hash_is_type + hash_is_individual + hash_can_type + hash_can_individual + \
                     hash_not_type + hash_not_individual

        # Used for generating fix hashes
        enc_hash = class_hash.encode('utf-8')
        final_hash = int(hashlib.sha256(enc_hash).hexdigest(), 16)

        return final_hash
