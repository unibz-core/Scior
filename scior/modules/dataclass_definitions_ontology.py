""" Definition of dataclass as the data structure used for loading the ontologies ontology in Scior.
    This module contains the data structure fields, initial value assignments and methods.
"""
import hashlib
from dataclasses import dataclass, field

from scior.modules.dataclass_verifications import verify_duplicates_in_lists_ontology, \
    verify_multiple_final_classifications_for_types
from scior.modules.logger_config import initialize_logger
from scior.modules.utils_general import lists_intersection

logger = initialize_logger()

@dataclass
class OntologyDataClass(object):
    """ Each loaded ontology dataclass has a URI (identifier) and six lists of GUFO elements.
    The lists indicate which gUFO element the dataclass is, can, or cannot be for the types and individuals hierarchies.

    incompleteness_info is a dictionary with the following filds:
        - is_incomplete: True or False
        - detected_in: list of rule codes where the incompleteness was detected (no repetitions are allowed).
    """

    uri: str = field(default_factory=str)
    is_type: list[str] = field(default_factory=list[str])
    is_individual: list[str] = field(default_factory=list[str])
    can_type: list[str] = field(default_factory=list[str])
    can_individual: list[str] = field(default_factory=list[str])
    not_type: list[str] = field(default_factory=list[str])
    not_individual: list[str] = field(default_factory=list[str])
    incompleteness_info: dict = field(default_factory=dict)

    def is_consistent(self):
        """ Performs a consistency check on the dataclass. """

        verify_duplicates_in_lists_ontology(self)
        verify_multiple_final_classifications_for_types(self)

    def clear_incompleteness(self):
        "When a user define the type of the dataclass, its incompleteness status must be set to its initial state."

        self.incompleteness_info["is_incomplete"] = False
        self.incompleteness_info["detected_in"] = []

    def move_element_between_lists(self, element, source_list, target_list):
        """ Move an element between two lists in the same OntologyClass
            Elements can only be moved from CAN lists to IS or NOT lists
        """

        logger.debug(
            f"Starting to move element {element} from {source_list} list to {target_list} list in {self.uri}...")

        source = []
        target = []

        # VERIFICATION 1: Source and target lists must be different
        if source_list == target_list:
            logger.error(f"Error for {self.uri} when trying to move {element} from list {source_list} "
                         f"to list {target_list}. Source equals target list. Program aborted.")
            exit(1)

        # VERIFICATION 2: Only CAN lists are allowed as source list
        if source_list == "can_type":
            source = self.can_type
        elif source_list == "can_individual":
            source = self.can_individual
        else:
            logger.error(f"Error for {self.uri} when trying to move {element} from list {source_list} "
                         f"to list {target_list}. Source list {source_list} is unknown. Program aborted.")
            exit(1)

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
            logger.error(f"Error for {self.uri} when trying to move {element} from list {source_list} "
                         f"to list {target_list}. Target list {target_list} is unknown. Program aborted.")
            exit(1)

        # VERIFICATION 4: Element must be in source list
        if element not in source:
            logger.error(f"Error for {self.uri} when trying to move {element} from list {source_list} "
                         f"to list {target_list}. The element {element} to be moved was not found "
                         f"in {source_list}. Program aborted.")
            exit(1)

        # Move element
        source.remove(element)
        target.append(element)

        # Performs consistency check
        self.is_consistent()

        logger.debug(f"Element {element} moved successfully from list {source_list} "
                     f"to list {target_list} in {self.uri}.")

    def move_element_to_is_list(self, element):
        """ Check if the element to be moved is a type or instance
                and move it from the corresponding CAN to the corresponding IS list.

            The element is only moved if it still not in the IS list.
            E.g. 1) if the element is in the can_type list, it is going to be moved to the is_type list.
            E.g. 2) if the element is in the is_type list, it is not going to be moved.

            This is a specific case of the move_element_between_lists method and
            is analogous to the move_element_to_not_list method.
        """

        source_list = self.return_containing_list_name(element)

        if source_list == "is_type" or source_list == "is_individual":
            logger.debug(f"Element {element} already in {source_list} for {self.uri}. No moving is necessary.")
        else:
            if source_list == "can_type":
                target_list = "is_type"
            elif source_list == "can_individual":
                target_list = "is_individual"
            else:
                logger.error(f"Inconsistency found. Error when trying to move the element {element} to the IS LIST "
                             f"in {self.uri}. The element was not found in the CAN list. Program aborted.")
                raise Exception("INCONSISTENCY FOUND!")

            # Consistency checking is already performed inside the move_between_ontology_lists function.
            self.move_element_between_lists(element, source_list, target_list)
            self.clear_incompleteness()
            self.verify_final_type_classification()

    def move_element_to_not_list(self, element):
        """ Check if the element to be moved is a type or instance
                and move it from the corresponding CAN to the corresponding NOT list.

            The element is only moved if it still not in the NOT list.
            E.g. 1) if the element is in the can_type list, it is going to be moved to the not_type list.
            E.g. 2) if the element is in the not_type list, it is not going to be moved.

            This is a specific case of the move_element_between_lists method and
            is analogous to the move_element_to_is_list method.
        """

        source_list = self.return_containing_list_name(element)

        if source_list == "not_type" or source_list == "not_individual":
            logger.debug(f"Element {element} already in {source_list} for {self.uri}. No moving is necessary.")
        else:
            if source_list == "can_type":
                target_list = "not_type"
            elif source_list == "can_individual":
                target_list = "not_individual"
            else:
                logger.error(f"When trying to move the element {element} to the NOT LIST in {self.uri}. "
                             f"The element was not found in the CAN list. Program aborted.")
                raise Exception("INCONSISTENCY FOUND!")

            # Consistency checking is already performed inside the move_between_ontology_lists function.
            self.move_element_between_lists(element, source_list, target_list)

    def move_list_of_elements_to_is_list(self, elem_list):
        """ Moves a list of elements to the IS list. Analogous to move_list_of_elements_to_not_list function.
        This is a specific case of the move_element_to_is_list function. """

        for elem in elem_list:
            self.move_element_to_is_list(elem)

    def move_list_of_elements_to_not_list(self, elem_list:list):
        """ Moves a list of elements to the NOT list. Analogous to move_list_of_elements_to_is_list function.
        This is a specific case of the move_element_to_not_list function. """

        for elem in elem_list:
            self.move_element_to_not_list(elem)

    def return_containing_list_name(self, element):
        """ Verify to which of the dataclass lists the element belongs and returns the list name. """

        containing_list_name = "not set"

        if element in self.is_type:
            containing_list_name = "is_type"
        elif element in self.is_individual:
            containing_list_name = "is_individual"
        elif element in self.can_type:
            containing_list_name = "can_type"
        elif element in self.can_individual:
            containing_list_name = "can_individual"
        elif element in self.not_type:
            containing_list_name = "not_type"
        elif element in self.not_individual:
            containing_list_name = "not_individual"
        else:
            logger.error(f"Element {element} does not belong to any list for {self.uri}. Program aborted.")
            exit(1)

        return containing_list_name

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
        list_hash = "not set"

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
            logger.error(f"Unknown list type {input_list}. Unable to create hash. Program aborted.")
            exit(1)

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

        class_hash = self.uri + hash_is_type + hash_is_individual + hash_can_type + \
                     hash_can_individual + hash_not_type + hash_not_individual

        # Used for generating fix hashes
        enc_hash = class_hash.encode('utf-8')
        final_hash = int(hashlib.sha256(enc_hash).hexdigest(), 16)

        return final_hash

    def verify_final_type_classification(self):
        """
        This function applies only to the types' hierarchy.

        1) If only a single leaf classification is present in the can_list, then moves it to the is list.
        2) If a leaf classification is already in the is_list, all other leaf classifications are moved to the not_list.

        Justification can be found here: https://github.com/nemo-ufes/gufo/issues/7
        """

        type_leaf_classifications = ["Category",
                                     "Kind",
                                     "Mixin",
                                     "Phase",
                                     "PhaseMixin",
                                     "Role",
                                     "RoleMixin",
                                     "SubKind"]

        # Verification 1 (single leaf classification in can_list)
        if len(self.can_type) > 0:
            can_intersection_list = lists_intersection(type_leaf_classifications, self.can_type)
            if len(can_intersection_list) == 1:
                self.move_element_to_is_list(can_intersection_list[0])

        # Verification 2 (leaf classification in is_list)
        is_intersection_list = lists_intersection(type_leaf_classifications, self.is_type)
        if len(is_intersection_list) == 1:
            for leaf_classification in type_leaf_classifications:
                if leaf_classification not in is_intersection_list:
                    self.move_element_to_not_list(leaf_classification)
        elif len(is_intersection_list) > 1:
            logger.error(f"Consistency violation for class {self.uri}. "
                         f"More than one leaf classifications ({is_intersection_list}) in its is_type list.")
